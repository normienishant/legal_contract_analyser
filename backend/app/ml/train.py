"""ML training pipeline for risk classification."""
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, classification_report
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
    DataCollatorWithPadding,
)
from datasets import Dataset
import torch
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RiskClassificationTrainer:
    """Trainer for contract clause risk classification."""
    
    def __init__(
        self,
        model_name: str = "distilbert-base-uncased",
        output_dir: str = "./models/risk_classifier",
        num_labels: int = 3,
    ):
        """Initialize trainer."""
        self.model_name = model_name
        self.output_dir = output_dir
        self.num_labels = num_labels
        self.label_map = {"LOW": 0, "MEDIUM": 1, "HIGH": 2}
        self.reverse_label_map = {v: k for k, v in self.label_map.items()}
        
        # Initialize tokenizer and model
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_name,
            num_labels=num_labels,
        )
        
        # Data collator
        self.data_collator = DataCollatorWithPadding(tokenizer=self.tokenizer)
    
    def load_data(self, csv_path: str) -> pd.DataFrame:
        """Load and preprocess training data from CSV with real-world data handling."""
        import re
        
        df = pd.read_csv(csv_path)
        
        # Validate required columns
        required_cols = ["clause_text", "label"]
        missing = [col for col in required_cols if col not in df.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
        
        # Clean data
        df = df.dropna(subset=["clause_text", "label"])
        df["clause_text"] = df["clause_text"].astype(str).str.strip()
        df["label"] = df["label"].str.upper().str.strip()
        
        # Filter valid labels
        valid_labels = set(self.label_map.keys())
        df = df[df["label"].isin(valid_labels)]
        
        # Real-world data preprocessing
        def preprocess_text(text: str) -> str:
            """Preprocess text for better model training on real-world data."""
            if not isinstance(text, str):
                return ""
            
            # Normalize whitespace (multiple spaces/tabs/newlines to single space)
            text = re.sub(r'\s+', ' ', text)
            
            # Remove excessive punctuation (keep legal punctuation)
            # Keep: . , ; : ( ) [ ] { } " ' - 
            # Remove: multiple consecutive punctuation
            text = re.sub(r'([.,;:!?])\1+', r'\1', text)
            
            # Normalize quotes
            text = re.sub(r'["""]', '"', text)
            text = re.sub(r"[''']", "'", text)
            
            # Remove control characters but keep newlines/spaces
            text = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f-\x9f]', '', text)
            
            # Trim and ensure minimum length
            text = text.strip()
            
            # If text is too short, return as is (will be filtered later)
            if len(text) < 10:
                return text
            
            return text
        
        # Apply preprocessing
        df["clause_text"] = df["clause_text"].apply(preprocess_text)
        
        # Filter out very short or very long clauses (real-world data quality)
        df = df[df["clause_text"].str.len() >= 15]  # Minimum 15 chars
        df = df[df["clause_text"].str.len() <= 5000]  # Maximum 5000 chars
        
        # Remove duplicates (common in real-world data)
        initial_count = len(df)
        df = df.drop_duplicates(subset=["clause_text"], keep="first")
        duplicates_removed = initial_count - len(df)
        if duplicates_removed > 0:
            logger.info(f"Removed {duplicates_removed} duplicate clauses")
        
        # Enhanced balancing for legal data
        label_counts = df["label"].value_counts()
        min_count = label_counts.min()
        max_count = label_counts.max()
        
        logger.info(f"Initial label distribution:\n{label_counts}")
        
        # For legal data, we want better balance but preserve diversity
        # Target: More balanced distribution (50% LOW, 30% MEDIUM, 20% HIGH)
        target_ratios = {"LOW": 0.5, "MEDIUM": 0.3, "HIGH": 0.2}
        total_samples = len(df)
        
        # If imbalance is severe (ratio > 3:1), apply smart balancing
        if max_count / min_count > 3:
            logger.info(f"Dataset imbalance detected (ratio: {max_count/min_count:.2f}:1). Applying smart balancing...")
            balanced_dfs = []
            
            for label in self.label_map.keys():
                label_df = df[df["label"] == label]
                current_count = len(label_df)
                target_count = int(total_samples * target_ratios.get(label, 0.33))
                
                if current_count < target_count:
                    # Need more samples - use oversampling with replacement
                    needed = target_count - current_count
                    additional = label_df.sample(n=needed, replace=True, random_state=42)
                    balanced_df = pd.concat([label_df, additional], ignore_index=True)
                    logger.info(f"   {label}: {current_count} -> {len(balanced_df)} (oversampled)")
                elif current_count > target_count * 1.5:
                    # Too many samples - undersample
                    balanced_df = label_df.sample(n=target_count, random_state=42)
                    logger.info(f"   {label}: {current_count} -> {len(balanced_df)} (undersampled)")
                else:
                    # Keep as is
                    balanced_df = label_df
                    logger.info(f"   {label}: {current_count} (kept)")
                
                balanced_dfs.append(balanced_df)
            
            df = pd.concat(balanced_dfs, ignore_index=True)
            df = df.sample(frac=1, random_state=42).reset_index(drop=True)
            logger.info(f"Balanced dataset. New distribution:\n{df['label'].value_counts()}")
        
        logger.info(f"Loaded {len(df)} samples after preprocessing")
        logger.info(f"Label distribution:\n{df['label'].value_counts()}")
        
        return df
    
    def prepare_dataset(self, df: pd.DataFrame):
        """Prepare dataset for training."""
        # Map labels to integers
        df["label_id"] = df["label"].map(self.label_map)
        
        # Tokenize with better handling for real-world data
        def tokenize_function(examples):
            # For real-world data, use dynamic padding during training
            # but fixed max_length for consistency
            return self.tokenizer(
                examples["clause_text"],
                truncation=True,
                padding="max_length",  # Use max_length for consistency
                max_length=512,
                return_attention_mask=True,
            )
        
        # Create dataset
        dataset = Dataset.from_pandas(df[["clause_text", "label_id"]])
        tokenized_dataset = dataset.map(tokenize_function, batched=True)
        
        # Rename label_id to labels for Trainer
        tokenized_dataset = tokenized_dataset.rename_column("label_id", "labels")
        
        return tokenized_dataset
    
    def train(
        self,
        train_dataset,
        eval_dataset=None,
        num_epochs: int = 3,
        batch_size: int = 16,
        learning_rate: float = 2e-5,
    ):
        """Train the model."""
        # Training arguments optimized for real-world data
        training_args = TrainingArguments(
            output_dir=self.output_dir,
            num_train_epochs=num_epochs,
            per_device_train_batch_size=batch_size,
            per_device_eval_batch_size=batch_size,
            learning_rate=learning_rate,
            weight_decay=0.01,
            warmup_steps=200,  # More warmup for large datasets
            logging_dir=f"{self.output_dir}/logs",
            logging_steps=50,  # More frequent logging
            eval_strategy="epoch" if eval_dataset else "no",
            save_strategy="epoch",
            load_best_model_at_end=True if eval_dataset else False,
            metric_for_best_model="f1" if eval_dataset else None,  # Use F1 for imbalanced data
            greater_is_better=True,
            save_total_limit=3,  # Keep only best 3 checkpoints
            push_to_hub=False,
            fp16=torch.cuda.is_available(),  # Use mixed precision if GPU available
            dataloader_num_workers=4,  # More workers for faster loading
            report_to="none",  # Disable wandb/tensorboard
            gradient_accumulation_steps=2,  # Effective batch size = batch_size * 2
            max_grad_norm=1.0,  # Gradient clipping for stability
        )
        
        # Metrics function
        def compute_metrics(eval_pred):
            predictions, labels = eval_pred
            predictions = np.argmax(predictions, axis=1)
            
            precision, recall, f1, _ = precision_recall_fscore_support(
                labels, predictions, average="weighted", zero_division=0
            )
            accuracy = accuracy_score(labels, predictions)
            
            return {
                "accuracy": accuracy,
                "f1": f1,
                "precision": precision,
                "recall": recall,
            }
        
        # Trainer
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
            data_collator=self.data_collator,
            compute_metrics=compute_metrics if eval_dataset else None,
        )
        
        # Train
        logger.info("Starting training...")
        train_result = trainer.train()
        
        # Save model
        os.makedirs(self.output_dir, exist_ok=True)
        trainer.save_model()
        self.tokenizer.save_pretrained(self.output_dir)
        
        logger.info(f"Model saved to {self.output_dir}")
        
        return train_result
    
    def evaluate(self, test_dataset):
        """Evaluate the model."""
        trainer = Trainer(
            model=self.model,
            data_collator=self.data_collator,
        )
        
        predictions = trainer.predict(test_dataset)
        pred_labels = np.argmax(predictions.predictions, axis=1)
        true_labels = predictions.label_ids
        
        # Calculate metrics
        accuracy = accuracy_score(true_labels, pred_labels)
        precision, recall, f1, _ = precision_recall_fscore_support(
            true_labels, pred_labels, average="weighted", zero_division=0
        )
        
        # Classification report
        report = classification_report(
            true_labels,
            pred_labels,
            target_names=[self.reverse_label_map[i] for i in range(self.num_labels)],
        )
        
        logger.info(f"\nEvaluation Results:")
        logger.info(f"Accuracy: {accuracy:.4f}")
        logger.info(f"Precision: {precision:.4f}")
        logger.info(f"Recall: {recall:.4f}")
        logger.info(f"F1-Score: {f1:.4f}")
        logger.info(f"\nClassification Report:\n{report}")
        
        return {
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "report": report,
        }


def main():
    """Main training function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Train risk classification model")
    parser.add_argument("--data", type=str, required=True, help="Path to training CSV")
    parser.add_argument("--output", type=str, default="./models/risk_classifier", help="Output directory")
    parser.add_argument("--epochs", type=int, default=3, help="Number of epochs")
    parser.add_argument("--batch-size", type=int, default=16, help="Batch size")
    parser.add_argument("--learning-rate", type=float, default=2e-5, help="Learning rate")
    parser.add_argument("--test-split", type=float, default=0.2, help="Test split ratio")
    parser.add_argument("--model", type=str, default="distilbert-base-uncased", help="Base model name")
    
    args = parser.parse_args()
    
    # Initialize trainer
    trainer = RiskClassificationTrainer(
        model_name=args.model,
        output_dir=args.output,
    )
    
    # Load data
    df = trainer.load_data(args.data)
    
    # Split data
    train_df, test_df = train_test_split(
        df,
        test_size=args.test_split,
        stratify=df["label"],
        random_state=42,
    )
    
    # Prepare datasets
    train_dataset = trainer.prepare_dataset(train_df)
    test_dataset = trainer.prepare_dataset(test_df)
    
    # Split train into train/eval
    train_size = int(0.8 * len(train_dataset))
    train_subset = train_dataset.select(range(train_size))
    eval_subset = train_dataset.select(range(train_size, len(train_dataset)))
    
    # Train
    trainer.train(
        train_subset,
        eval_subset,
        num_epochs=args.epochs,
        batch_size=args.batch_size,
        learning_rate=args.learning_rate,
    )
    
    # Evaluate on test set
    trainer.evaluate(test_dataset)
    
    logger.info("Training completed!")


if __name__ == "__main__":
    main()

