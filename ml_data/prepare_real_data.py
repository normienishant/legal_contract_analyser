"""Helper script to prepare real-world training data from contracts."""
import pandas as pd
import os
from pathlib import Path

def create_training_data_template():
    """Create a template CSV for manual data entry."""
    template_data = {
        "clause_text": [
            "Example: The Service Provider shall indemnify...",
            "Example: Either party may terminate...",
            "Example: This Agreement shall commence...",
        ],
        "label": ["HIGH", "MEDIUM", "LOW"],
        "explanation": [
            "Contains unlimited indemnification",
            "Standard termination clause",
            "Standard commencement clause",
        ]
    }
    
    df = pd.DataFrame(template_data)
    output_path = "real_world_training_template.csv"
    df.to_csv(output_path, index=False)
    print(f"✅ Template created: {output_path}")
    print(f"\nInstructions:")
    print(f"1. Open {output_path} in Excel or text editor")
    print(f"2. Replace example rows with your real contract clauses")
    print(f"3. Assign labels: HIGH, MEDIUM, or LOW")
    print(f"4. Add explanations (optional)")
    print(f"5. Save and use for training:")
    print(f"   python -m app.ml.train --data {output_path} --output ./models/risk_classifier")


def validate_training_data(csv_path: str):
    """Validate training data CSV."""
    try:
        df = pd.read_csv(csv_path)
        
        # Check required columns
        required_cols = ["clause_text", "label"]
        missing = [col for col in required_cols if col not in df.columns]
        if missing:
            print(f"❌ Missing required columns: {missing}")
            return False
        
        # Check labels
        valid_labels = {"HIGH", "MEDIUM", "LOW"}
        invalid_labels = set(df["label"].str.upper().unique()) - valid_labels
        if invalid_labels:
            print(f"❌ Invalid labels found: {invalid_labels}")
            print(f"   Valid labels: HIGH, MEDIUM, LOW")
            return False
        
        # Check data quality
        empty_clauses = df[df["clause_text"].isna() | (df["clause_text"].str.strip() == "")]
        if len(empty_clauses) > 0:
            print(f"⚠️  Warning: {len(empty_clauses)} empty clauses found")
        
        # Statistics
        print(f"\n✅ Data validation passed!")
        print(f"\nStatistics:")
        print(f"  Total clauses: {len(df)}")
        print(f"\nLabel distribution:")
        print(df["label"].value_counts())
        
        # Check minimum requirements
        label_counts = df["label"].value_counts()
        min_required = 50
        for label in valid_labels:
            count = label_counts.get(label, 0)
            if count < min_required:
                print(f"\n⚠️  Warning: Only {count} {label} clauses (recommended: {min_required}+)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error validating data: {e}")
        return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Prepare real-world training data")
    parser.add_argument("--template", action="store_true", help="Create template CSV")
    parser.add_argument("--validate", type=str, help="Validate existing CSV file")
    
    args = parser.parse_args()
    
    if args.template:
        create_training_data_template()
    elif args.validate:
        validate_training_data(args.validate)
    else:
        print("Usage:")
        print("  Create template: python prepare_real_data.py --template")
        print("  Validate data:   python prepare_real_data.py --validate your_data.csv")

