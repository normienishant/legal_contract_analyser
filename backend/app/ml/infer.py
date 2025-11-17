"""ML inference wrapper for clause risk analysis."""
import logging
from typing import List, Dict
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import os
from app.core.config import settings

logger = logging.getLogger(__name__)


class RiskClassifier:
    """Risk classifier for contract clauses."""
    
    def __init__(self, model_path: str | None = None):
        """Initialize the classifier."""
        self.model_path = model_path or settings.model_path
        self.device = "cuda" if settings.use_gpu and torch.cuda.is_available() else "cpu"
        self.classifier = None
        self.tokenizer = None
        self.model = None
        self.label_map = {"LABEL_0": "LOW", "LABEL_1": "MEDIUM", "LABEL_2": "HIGH"}
        self._load_model()
    
    def _load_model(self):
        """Load the trained model."""
        if not os.path.exists(self.model_path):
            logger.warning(f"Model not found at {self.model_path}. Using fallback.")
            return
        
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
            self.model = AutoModelForSequenceClassification.from_pretrained(
                self.model_path
            )
            self.model.to(self.device)
            self.model.eval()
            self.classifier = pipeline(
                "text-classification",
                model=self.model,
                tokenizer=self.tokenizer,
                device=0 if self.device == "cuda" else -1,
            )
            logger.info(f"Model loaded from {self.model_path}")
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            self.classifier = None
    
    def analyze_clauses(self, clauses: List[str]) -> List[Dict]:
        """
        Analyze clauses and return risk assessments with improved real-world handling.
        
        Returns:
            List of dicts with keys: clause_text, clause_index, risk_label,
            risk_score, explanation, suggested_mitigation
        """
        if not self.classifier:
            logger.warning("ML model not available, using rule-based fallback")
            return self._rule_based_analysis(clauses)
        
        import re
        
        # Preprocess clauses (same as training)
        def preprocess_clause(text: str) -> str:
            """Preprocess clause text for inference."""
            if not isinstance(text, str):
                return ""
            text = re.sub(r'\s+', ' ', text)
            text = re.sub(r'([.,;:!?])\1+', r'\1', text)
            text = re.sub(r'["""]', '"', text)
            text = re.sub(r'[''']', "'", text)
            text = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f-\x9f]', '', text)
            return text.strip()
        
        results = []
        for idx, clause in enumerate(clauses):
            try:
                # Preprocess clause
                processed_clause = preprocess_clause(clause)
                
                # Skip if too short
                if len(processed_clause) < 10:
                    logger.warning(f"Clause {idx} too short, using rule-based")
                    rule_result = self._rule_based_analysis([clause])[0]
                    rule_result["clause_index"] = idx
                    results.append(rule_result)
                    continue
                
                # Truncate if too long (model max is 512 tokens)
                if len(processed_clause) > 2000:
                    processed_clause = processed_clause[:2000] + "..."
                
                prediction = self.classifier(processed_clause, return_all_scores=True)[0]
                
                # Get highest probability label
                best_pred = max(prediction, key=lambda x: x['score'])
                label_str = best_pred['label']
                score = best_pred['score']
                
                # Map to risk label
                risk_label = self.label_map.get(label_str, "MEDIUM")
                
                # Improved risk score calculation based on confidence
                # Use all scores for better calibration
                all_scores = {self.label_map.get(p['label'], "MEDIUM"): p['score'] for p in prediction}
                
                # Calculate risk score with confidence weighting
                if risk_label == "HIGH":
                    # High risk: 70-100 based on confidence
                    risk_score = 70 + (score * 30)
                elif risk_label == "MEDIUM":
                    # Medium risk: 30-70 based on confidence
                    risk_score = 30 + (score * 40)
                else:
                    # Low risk: 0-30 based on confidence
                    risk_score = score * 30
                
                # Adjust based on other class probabilities (uncertainty)
                if risk_label == "HIGH" and all_scores.get("MEDIUM", 0) > 0.3:
                    # If medium is also high, reduce confidence
                    risk_score = risk_score * 0.9
                elif risk_label == "MEDIUM" and all_scores.get("HIGH", 0) > 0.25:
                    # If high is also significant, increase risk
                    risk_score = min(100, risk_score + 10)
                
                # Ensure score is in 0-100 range
                risk_score = min(100, max(0, risk_score))
                
                explanation = self._generate_explanation(clause, risk_label, score)
                mitigation = self._generate_mitigation(clause, risk_label)
                
                results.append({
                    "clause_text": clause,  # Keep original clause text
                    "clause_index": idx,
                    "risk_label": risk_label,
                    "risk_score": round(risk_score, 2),
                    "explanation": explanation,
                    "suggested_mitigation": mitigation,
                })
            except Exception as e:
                logger.error(f"Error analyzing clause {idx}: {e}", exc_info=True)
                # Fallback to rule-based for this clause
                rule_result = self._rule_based_analysis([clause])[0]
                rule_result["clause_index"] = idx
                results.append(rule_result)
        
        return results
    
    def _rule_based_analysis(self, clauses: List[str]) -> List[Dict]:
        """Rule-based fallback analysis."""
        from app.services.analysis import RuleBasedAnalyzer
        analyzer = RuleBasedAnalyzer()
        return analyzer.analyze_clauses(clauses)
    
    def _generate_explanation(self, clause: str, label: str, confidence: float) -> str:
        """Generate explanation for the risk assessment."""
        explanations = {
            "HIGH": f"This clause contains high-risk language that may expose parties to significant liability, penalties, or unfavorable terms (confidence: {confidence:.2%}).",
            "MEDIUM": f"This clause contains moderate-risk language that may require careful review (confidence: {confidence:.2%}).",
            "LOW": f"This clause appears to contain standard, low-risk language (confidence: {confidence:.2%}).",
        }
        return explanations.get(label, "Risk assessment completed.")
    
    def _generate_mitigation(self, clause: str, label: str) -> str:
        """Generate mitigation suggestion."""
        if label == "HIGH":
            return "Consider revising to limit liability, add exceptions, or include mutual obligations. Consult legal counsel."
        elif label == "MEDIUM":
            return "Review for clarity and ensure terms are balanced. Consider adding specific conditions or limitations."
        else:
            return "This clause appears acceptable, but always review with legal counsel for your specific context."

