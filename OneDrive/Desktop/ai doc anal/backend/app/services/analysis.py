"""Analysis service for document risk assessment."""
import logging
from typing import List, Dict
from app.core.config import settings

logger = logging.getLogger(__name__)

# Lazy import for ML - only import when needed
RiskClassifier = None
def _get_risk_classifier():
    global RiskClassifier
    if RiskClassifier is None:
        try:
            from app.ml.infer import RiskClassifier as RC
            RiskClassifier = RC
        except ImportError as e:
            logger.warning(f"ML module not available: {e}")
            RiskClassifier = None
    return RiskClassifier


class RuleBasedAnalyzer:
    """Rule-based risk analyzer as fallback."""
    
    HIGH_RISK_KEYWORDS = [
        "unlimited liability", "sole discretion", "without limitation",
        "indemnify", "hold harmless", "penalty", "liquidated damages",
        "automatic renewal", "binding arbitration", "waiver of rights",
        "exclusive jurisdiction", "no refund", "as-is", "no warranty",
        "force majeure", "termination without cause", "confidentiality breach",
        # Additional real-world patterns
        "at any time without notice", "without prior notice", "immediate termination",
        "no recourse", "no liability", "disclaim all warranties", "as-is basis",
        "consequential damages", "punitive damages", "treble damages",
        "non-compete", "non-solicitation", "restrictive covenant",
        "assignment prohibited", "transfer prohibited", "no assignment",
        "confidential information", "proprietary information", "trade secrets",
        "liquidated damages", "penalty clause", "forfeiture",
        "right to modify", "right to amend", "unilateral modification",
        "binding on successors", "survival clause", "severability",
    ]
    
    # Rental/Lease Agreement Specific HIGH RISK Patterns
    HIGH_RISK_PATTERNS = [
        # Unilateral amendment/modification rights
        r'unilateral\s+amendment',
        r'reserves\s+the\s+right\s+to\s+modify\s+or\s+amend\s+any\s+term',
        r'landlord.*reserves.*right.*modify',
        r'landlord.*reserves.*right.*amend',
        r'modify.*any\s+term.*at\s+any\s+time',
        r'amend.*any\s+term.*at\s+any\s+time',
        
        # Entry without notice
        r'enter.*at\s+any\s+time.*without\s+(prior\s+)?notice',
        r'enter.*premises.*without\s+(prior\s+)?notice',
        r'right\s+of\s+entry.*without\s+notice',
        r'landlord.*may\s+enter.*at\s+any\s+time',
        
        # Indemnification including own negligence
        r'indemnify.*own\s+negligence',
        r'hold\s+harmless.*own\s+negligence',
        r'indemnify.*landlord.*negligence',
        r'including\s+claims.*arising\s+from.*own\s+negligence',
        r'indemnify.*including.*landlord.*negligence',
        
        # Distant/exclusive jurisdiction (unfair to tenant)
        r'exclusively\s+by\s+the\s+courts\s+located\s+in',
        r'exclusive\s+jurisdiction.*distant',
        r'courts\s+located\s+in.*\(.*city',
        r'jurisdiction.*exclusively',
        
        # Very short termination notice (30 days or less for major changes)
        r'terminate.*30\s+days.*written\s+notice',
        r'30\s+days.*written\s+notice.*terminate',
        r'termination.*30\s+days.*notice',
        r'vacate.*30\s+days',
        
        # Excessive penalties or fees
        r'penalty.*exceed.*monthly\s+rent',
        r'late\s+fee.*per\s+week',
        r'penalty.*uncapped',
        
        # Unfair termination for sale/redevelopment
        r'terminate.*sale.*property',
        r'terminate.*redevelopment',
        r'terminate.*30\s+days.*sale',
    ]
    
    MEDIUM_RISK_KEYWORDS = [
        "termination", "breach", "default", "remedy", "dispute",
        "governing law", "jurisdiction", "assignment", "modification",
        "severability", "entire agreement", "notices",
        # Additional real-world patterns
        "cure period", "notice period", "grace period",
        "material breach", "substantial breach", "default under",
        "remedy available", "specific performance", "injunctive relief",
        "dispute resolution", "mediation", "arbitration",
        "choice of law", "venue", "forum selection",
        "assignment and delegation", "transfer of rights",
        "amendment", "modification", "waiver",
        "survival", "severability", "invalidity",
        "entire agreement", "merger clause", "integration clause",
        "notices", "service of process", "communication",
        "confidentiality", "non-disclosure", "proprietary",
        "intellectual property", "work product", "derivative works",
    ]
    
    # Rental/Lease Agreement Specific MEDIUM RISK Patterns
    MEDIUM_RISK_PATTERNS = [
        # Security deposit with deductions
        r'security\s+deposit.*deduct',
        r'deposit.*deduct.*damages',
        r'security\s+deposit.*forfeiture',
        
        # Late payment fees (need to check if reasonable)
        r'late\s+payment\s+fee',
        r'late\s+fee.*rent',
        r'penalty.*late\s+payment',
        
        # Subletting restrictions
        r'sublet.*without.*prior\s+written\s+consent',
        r'assign.*without.*consent',
        r'no\s+subletting',
        
        # Pet restrictions
        r'no\s+pets.*without.*consent',
        r'pet\s+deposit',
        
        # Alterations restrictions
        r'no.*alterations.*without.*consent',
        r'structural\s+alterations.*consent',
        
        # Termination with liability
        r'terminate.*liable\s+for\s+rent',
        r'early\s+termination.*liable',
        r'terminate.*two\s+months.*rent',
        
        # Rent escalation
        r'rent\s+escalation',
        r'increase\s+rent.*annually',
        r'rent.*increase.*cpi',
        
        # Fixtures and removal
        r'fixtures.*property\s+of\s+landlord',
        r'remove.*fixtures',
    ]
    
    def analyze_clauses(self, clauses: List[str]) -> List[Dict]:
        """Analyze clauses using rule-based approach."""
        import re
        results = []
        
        for idx, clause in enumerate(clauses):
            clause_lower = clause.lower()
            clause_clean = re.sub(r'\s+', ' ', clause_lower).strip()
            
            # FIRST: Check for LOW RISK boilerplate patterns (ALL document types + Rental specific)
            low_risk_patterns = [
                # Rental/Lease Agreement LOW RISK patterns
                r'^rent\s+amount\s+and\s+payment\s+terms',
                r'tenant\s+shall\s+pay\s+monthly\s+rent',
                r'pay.*rent.*on\s+or\s+before',
                r'bank\s+transfer.*landlord',
                
                r'maintenance\s+and\s+repairs',
                r'tenant.*responsible.*routine\s+upkeep',
                r'landlord.*responsible.*major.*repairs',
                
                r'utilities\s+and\s+service\s+charges',
                r'tenant.*responsible.*payment.*electricity',
                r'utilities.*unless\s+otherwise\s+stated',
                
                r'insurance\s+requirement',
                r'tenant.*maintain.*renter.*insurance',
                r'liability\s+coverage',
                
                r'guarantor',
                r'provide\s+a\s+guarantor',
                
                r'force\s+majeure',
                r'events\s+beyond.*reasonable\s+control',
                r'natural\s+disasters.*government\s+actions',
                
                r'confidentiality',
                r'keep.*terms.*confidential',
                r'not\s+disclose.*third\s+parties',
                
                # General agreements
                r'^this\s+agreement\s+has\s+been\s+made',
                r'^this\s+agreement.*between',
                r'^this\s+agreement\s+is\s+entered\s+into',
                r'^this\s+agreement\s+has\s+been\s+executed',
                r'^this\s+contract\s+is\s+entered\s+into',
                r'^between\s+.*\s+and\s+.*hereinafter',
                r'^between\s+.*\s+and\s+.*incorporated',
                r'^between\s+.*\s+and\s+.*registered',
                # Employment
                r'^this\s+employment\s+agreement',
                r'^the\s+employee.*employment.*shall\s+commence',
                r'^the\s+employee\s+shall\s+be\s+employed',
                # NDAs
                r'^this\s+non-disclosure\s+agreement',
                r'^confidential\s+information.*shall\s+mean',
                # Service agreements
                r'^this\s+service\s+agreement',
                r'^the\s+service\s+provider\s+agrees\s+to\s+provide',
                # Purchase agreements
                r'^this\s+purchase\s+agreement',
                r'^the\s+buyer\s+agrees\s+to\s+purchase',
                # Lease agreements
                r'^this\s+lease\s+agreement',
                r'^the\s+lessor\s+hereby\s+leases',
                # Licensing
                r'^this\s+license\s+agreement',
                r'^the\s+licensor\s+hereby\s+grants.*license',
                # Software licenses
                r'^this\s+software\s+license\s+agreement',
                # Terms/Privacy
                r'^these\s+terms\s+of\s+service',
                r'^this\s+privacy\s+policy',
                # Recitals
                r'^whereas\s+',
                r'^and\s+whereas',
                r'^now\s+therefore',
                r'^now,\s+therefore',
                r'^in\s+witness\s+whereof',
                # Definitions
                r'^definitions?\s*:',
                r'^article\s+\d+',
                r'^section\s+\d+',
                r'^for\s+purposes\s+of\s+this\s+agreement',
                # Party identification
                r'hereinafter\s+referred\s+to\s+as',
                r'incorporated\s+as\s+a\s+body',
                r'represented\s+by',
                # Payment/execution
                r'^in\s+consideration\s+of\s+the\s+payments',
                r'^in\s+consideration\s+of\s+the\s+mutual',
                r'^the\s+.*\s+shall\s+pay\s+the\s+.*\s+such\s+sums',
                r'^the\s+.*\s+shall\s+pay.*fees\s+as\s+set\s+forth',
                # Structure
                r'^this\s+agreement\s+shall\s+commence\s+on',
                r'^this\s+agreement\s+may\s+be\s+executed\s+in\s+counterparts',
                r'^the\s+headings\s+in\s+this\s+agreement',
                r'^this\s+agreement\s+constitutes\s+the\s+entire\s+agreement',
            ]
            
            is_boilerplate = False
            for pattern in low_risk_patterns:
                if re.search(pattern, clause_clean, re.IGNORECASE):
                    is_boilerplate = True
                    break
            
            # Count keyword matches
            high_count = sum(1 for kw in self.HIGH_RISK_KEYWORDS if kw in clause_lower)
            medium_count = sum(1 for kw in self.MEDIUM_RISK_KEYWORDS if kw in clause_lower)
            
            # Check HIGH RISK patterns (rental/lease specific)
            high_pattern_matches = sum(1 for pattern in self.HIGH_RISK_PATTERNS 
                                      if re.search(pattern, clause_clean, re.IGNORECASE))
            
            # Check MEDIUM RISK patterns (rental/lease specific)
            medium_pattern_matches = sum(1 for pattern in self.MEDIUM_RISK_PATTERNS 
                                        if re.search(pattern, clause_clean, re.IGNORECASE))
            
            # Combine keyword and pattern matches
            total_high_indicators = high_count + high_pattern_matches
            total_medium_indicators = medium_count + medium_pattern_matches
            
            # Determine risk label (check boilerplate FIRST, but HIGH patterns override)
            if is_boilerplate and total_high_indicators == 0 and high_pattern_matches == 0:
                risk_label = "LOW"
                risk_score = 5 + min(15, len(clause) // 100)
            elif total_high_indicators >= 2 or high_pattern_matches >= 1 or (total_high_indicators >= 1 and len(clause) > 200):
                # HIGH RISK: Multiple high-risk indicators OR any high-risk pattern match
                risk_label = "HIGH"
                risk_score = 80 + min(20, (total_high_indicators + high_pattern_matches * 2) * 3)
            elif total_high_indicators >= 1 or total_medium_indicators >= 3 or medium_pattern_matches >= 2:
                # MEDIUM RISK: Some high-risk indicators OR multiple medium-risk indicators
                risk_label = "MEDIUM"
                risk_score = 45 + min(25, (total_high_indicators + total_medium_indicators) * 4)
            elif total_medium_indicators >= 1 or medium_pattern_matches >= 1:
                # MEDIUM RISK: At least one medium-risk indicator
                risk_label = "MEDIUM"
                risk_score = 35 + min(15, total_medium_indicators * 5)
            else:
                # LOW RISK: No significant risk indicators
                risk_label = "LOW"
                risk_score = 10 + min(10, len(clause) // 50)
            
            risk_score = min(100, max(0, risk_score))
            
            explanation = self._generate_explanation(clause, risk_label, high_count, medium_count)
            mitigation = self._generate_mitigation(clause, risk_label)
            
            results.append({
                "clause_text": clause,
                "clause_index": idx,
                "risk_label": risk_label,
                "risk_score": round(risk_score, 2),
                "explanation": explanation,
                "suggested_mitigation": mitigation,
            })
        
        return results
    
    def _generate_explanation(self, clause: str, label: str, high_count: int, medium_count: int) -> str:
        """Generate explanation for the risk assessment."""
        import re
        clause_lower = clause.lower()
        clause_clean = re.sub(r'\s+', ' ', clause_lower).strip()
        
        if label == "HIGH":
            reasons = []
            
            # Check for specific high-risk patterns
            if re.search(r'unilateral\s+amendment|reserves\s+the\s+right\s+to\s+modify', clause_clean, re.IGNORECASE):
                reasons.append("unilateral amendment rights (landlord can change terms without tenant consent)")
            if re.search(r'enter.*without\s+(prior\s+)?notice|at\s+any\s+time.*without\s+notice', clause_clean, re.IGNORECASE):
                reasons.append("entry without prior notice (privacy concerns)")
            if re.search(r'indemnify.*own\s+negligence|hold\s+harmless.*own\s+negligence', clause_clean, re.IGNORECASE):
                reasons.append("indemnification including landlord's own negligence (extremely unfair)")
            if re.search(r'exclusively\s+by\s+the\s+courts\s+located|exclusive\s+jurisdiction', clause_clean, re.IGNORECASE):
                reasons.append("exclusive jurisdiction in distant location (unfair to tenant)")
            if re.search(r'terminate.*30\s+days.*written\s+notice|30\s+days.*terminate', clause_clean, re.IGNORECASE):
                reasons.append("very short termination notice (30 days is insufficient)")
            
            # Standard high-risk keywords
            if "indemnify" in clause_lower or "hold harmless" in clause_lower:
                if "own negligence" not in clause_lower:  # Already covered above
                    reasons.append("indemnification language")
            if "penalty" in clause_lower or "liquidated damages" in clause_lower:
                reasons.append("penalty or damage clauses")
            if "automatic renewal" in clause_lower:
                reasons.append("automatic renewal terms")
            if "binding arbitration" in clause_lower or "waiver of rights" in clause_lower:
                reasons.append("dispute resolution restrictions")
            if "unlimited liability" in clause_lower or "without limitation" in clause_lower:
                reasons.append("unlimited liability exposure")
            
            reason_text = ", ".join(reasons) if reasons else "high-risk language"
            return f"This clause contains {reason_text} that may expose parties to significant legal and financial risk. This is particularly unfair to tenants in rental agreements."
        
        elif label == "MEDIUM":
            return f"This clause contains moderate-risk language that requires careful review. Medium-risk keywords detected: {medium_count}. Standard legal terms may need clarification or negotiation."
        
        else:
            return "This clause appears to contain standard, low-risk language typical of commercial agreements. However, always review with legal counsel for your specific context."
    
    def _generate_mitigation(self, clause: str, label: str) -> str:
        """Generate mitigation suggestion."""
        clause_lower = clause.lower()
        
        if label == "HIGH":
            suggestions = []
            if "indemnify" in clause_lower:
                suggestions.append("Limit indemnification to direct damages and exclude consequential damages")
            if "penalty" in clause_lower or "liquidated damages" in clause_lower:
                suggestions.append("Ensure penalties are reasonable and proportional to actual damages")
            if "automatic renewal" in clause_lower:
                suggestions.append("Add clear opt-out mechanism and advance notice requirements")
            if "binding arbitration" in clause_lower:
                suggestions.append("Consider allowing court proceedings for certain disputes")
            if "unlimited liability" in clause_lower:
                suggestions.append("Cap liability to a reasonable amount (e.g., contract value)")
            
            if suggestions:
                return "Consider: " + "; ".join(suggestions) + ". Consult legal counsel before signing."
            return "Consider revising to limit liability, add exceptions, or include mutual obligations. Consult legal counsel."
        
        elif label == "MEDIUM":
            return "Review for clarity and ensure terms are balanced. Consider adding specific conditions, limitations, or mutual obligations. Seek legal review if uncertain."
        
        else:
            return "This clause appears acceptable, but always review with legal counsel for your specific context and jurisdiction."


class AnalysisService:
    """Main analysis service."""
    
    def __init__(self):
        """Initialize analysis service."""
        self.ml_mode = settings.ml_mode
        self.classifier = None
        if self.ml_mode == "ml":
            try:
                RC = _get_risk_classifier()
                if RC:
                    self.classifier = RC()
                else:
                    logger.warning("ML module not available. Falling back to rules.")
                    self.ml_mode = "rules"
            except Exception as e:
                logger.warning(f"Failed to load ML model: {e}. Falling back to rules.")
                self.ml_mode = "rules"
    
    def analyze_document(self, clauses: List[str]) -> Dict:
        """
        Analyze a document and return risk assessment.
        
        Returns:
            Dict with global_risk_score, total_clauses, counts, and clause analyses
        """
        # Analyze individual clauses
        if self.ml_mode == "ml" and self.classifier and self.classifier.classifier:
            clause_analyses = self.classifier.analyze_clauses(clauses)
        else:
            rule_analyzer = RuleBasedAnalyzer()
            clause_analyses = rule_analyzer.analyze_clauses(clauses)
        
        # Calculate global risk score
        global_score = self._calculate_global_score(clause_analyses)
        
        # Count risk levels
        counts = {
            "high": sum(1 for c in clause_analyses if c["risk_label"] == "HIGH"),
            "medium": sum(1 for c in clause_analyses if c["risk_label"] == "MEDIUM"),
            "low": sum(1 for c in clause_analyses if c["risk_label"] == "LOW"),
        }
        
        return {
            "global_risk_score": round(global_score, 2),
            "total_clauses": len(clauses),
            "high_risk_count": counts["high"],
            "medium_risk_count": counts["medium"],
            "low_risk_count": counts["low"],
            "clauses": clause_analyses,
        }
    
    def _calculate_global_score(self, clause_analyses: List[Dict]) -> float:
        """
        Calculate global document risk score.
        
        Formula:
        - Weight clauses by importance (presence of high-severity keywords)
        - High-risk clauses get 2x weight
        - Medium-risk clauses get 1.5x weight
        - Low-risk clauses get 1x weight
        - Weighted average of clause scores
        """
        if not clause_analyses:
            return 0.0
        
        total_weighted_score = 0.0
        total_weight = 0.0
        
        for clause in clause_analyses:
            score = clause["risk_score"]
            label = clause["risk_label"]
            
            # Determine weight based on risk level
            if label == "HIGH":
                weight = 2.0
            elif label == "MEDIUM":
                weight = 1.5
            else:
                weight = 1.0
            
            # Additional weight for clauses with high-severity keywords
            clause_text = clause["clause_text"].lower()
            severity_keywords = ["liability", "penalty", "indemnify", "damages", "breach"]
            if any(kw in clause_text for kw in severity_keywords):
                weight *= 1.3
            
            total_weighted_score += score * weight
            total_weight += weight
        
        if total_weight == 0:
            return 0.0
        
        global_score = total_weighted_score / total_weight
        return min(100, max(0, global_score))

