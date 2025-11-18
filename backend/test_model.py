"""Test the trained model."""
from app.ml.infer import RiskClassifier

# Test with the user's example clause
test_clause = "THIS AGREEMENT has been made on this __th day of October, 2012 at IIT Kanpur BETWEEN Indian Institute of Technology Kanpur (hereinafter referred to as the Institute) incorporated as a body of corporate under the Institute of Technology Act, 1961"

print("Loading model...")
rc = RiskClassifier()

if rc.classifier:
    print("[SUCCESS] Model loaded successfully!")
    
    print("\nTesting with standard boilerplate clause:")
    result = rc.analyze_clauses([test_clause])
    print(f"Risk Label: {result[0]['risk_label']}")
    print(f"Risk Score: {result[0]['risk_score']}")
    print(f"Explanation: {result[0]['explanation']}")
    
    # Test with a HIGH risk clause
    print("\n\nTesting with HIGH risk clause:")
    high_risk = "Provider shall indemnify, defend, and hold harmless Customer from any and all claims, without limitation or exception."
    result2 = rc.analyze_clauses([high_risk])
    print(f"Risk Label: {result2[0]['risk_label']}")
    print(f"Risk Score: {result2[0]['risk_score']}")
    
    # Test with MEDIUM risk clause
    print("\n\nTesting with MEDIUM risk clause:")
    medium_risk = "Either party may terminate this Agreement upon 30 days' prior written notice."
    result3 = rc.analyze_clauses([medium_risk])
    print(f"Risk Label: {result3[0]['risk_label']}")
    print(f"Risk Score: {result3[0]['risk_score']}")
    
else:
    print("[ERROR] Model not loaded")

