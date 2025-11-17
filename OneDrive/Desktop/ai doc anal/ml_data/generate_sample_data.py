"""Generate synthetic training data for risk classification."""
import pandas as pd
import random

# Sample clauses with different risk levels
HIGH_RISK_CLAUSES = [
    "The party agrees to indemnify and hold harmless the other party from any and all claims, damages, losses, and expenses without limitation.",
    "In the event of breach, the defaulting party shall pay liquidated damages equal to 100% of the contract value as a penalty.",
    "This agreement shall automatically renew for successive one-year terms unless terminated by either party with 30 days notice, and termination fees apply.",
    "The parties agree to binding arbitration with exclusive jurisdiction in [State], waiving all rights to a jury trial.",
    "The service is provided 'as-is' without any warranty, express or implied, and the provider disclaims all liability for any damages.",
    "Confidentiality obligations survive termination indefinitely, and breach may result in immediate legal action without prior notice.",
    "The customer agrees to unlimited liability for any data loss, security breaches, or service interruptions, regardless of cause.",
    "Payment is non-refundable under any circumstances, including service cancellation, breach by provider, or force majeure events.",
]

MEDIUM_RISK_CLAUSES = [
    "Either party may terminate this agreement with 60 days written notice in the event of material breach by the other party.",
    "Disputes arising from this agreement shall be resolved through mediation, and if unsuccessful, through binding arbitration.",
    "This agreement shall be governed by the laws of [State], and any disputes shall be subject to the exclusive jurisdiction of courts in [State].",
    "The parties agree that this agreement may not be assigned without prior written consent of the other party.",
    "In the event of termination, each party shall return or destroy all confidential information received from the other party.",
    "Modifications to this agreement must be made in writing and signed by both parties to be effective.",
    "If any provision of this agreement is found to be unenforceable, the remaining provisions shall remain in full force and effect.",
    "Notices required under this agreement shall be sent to the addresses specified below via certified mail.",
]

LOW_RISK_CLAUSES = [
    "This agreement shall commence on the effective date and continue until terminated in accordance with its terms.",
    "Both parties agree to act in good faith and deal fairly with each other in all matters relating to this agreement.",
    "Each party represents that it has the authority to enter into this agreement and perform its obligations hereunder.",
    "This agreement constitutes the entire understanding between the parties and supersedes all prior agreements and understandings.",
    "The parties may execute this agreement in counterparts, each of which shall be deemed an original and all of which together shall constitute one instrument.",
    "This agreement may be executed and delivered by facsimile or electronic transmission, and such execution and delivery shall be as effective as delivery of an original.",
    "The headings in this agreement are for convenience only and shall not affect the interpretation of any provision.",
    "This agreement shall be binding upon and inure to the benefit of the parties and their respective successors and permitted assigns.",
]

def generate_dataset(num_samples_per_class: int = 50) -> pd.DataFrame:
    """Generate synthetic dataset."""
    data = []
    
    # High risk
    for _ in range(num_samples_per_class):
        clause = random.choice(HIGH_RISK_CLAUSES)
        # Add some variation
        clause = clause.replace("[State]", random.choice(["California", "New York", "Texas", "Florida"]))
        data.append({
            "doc_id": f"doc_{random.randint(1, 100)}",
            "clause_text": clause,
            "label": "HIGH",
            "explanation": "Contains high-risk language such as unlimited liability, penalties, or automatic renewal terms.",
        })
    
    # Medium risk
    for _ in range(num_samples_per_class):
        clause = random.choice(MEDIUM_RISK_CLAUSES)
        clause = clause.replace("[State]", random.choice(["California", "New York", "Texas", "Florida"]))
        data.append({
            "doc_id": f"doc_{random.randint(1, 100)}",
            "clause_text": clause,
            "label": "MEDIUM",
            "explanation": "Contains moderate-risk language that may require careful review.",
        })
    
    # Low risk
    for _ in range(num_samples_per_class):
        clause = random.choice(LOW_RISK_CLAUSES)
        data.append({
            "doc_id": f"doc_{random.randint(1, 100)}",
            "clause_text": clause,
            "label": "LOW",
            "explanation": "Contains standard, low-risk language typical of commercial agreements.",
        })
    
    return pd.DataFrame(data)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate synthetic training data")
    parser.add_argument("--output", type=str, default="training_data.csv", help="Output CSV file")
    parser.add_argument("--samples", type=int, default=50, help="Samples per class")
    
    args = parser.parse_args()
    
    df = generate_dataset(args.samples)
    df.to_csv(args.output, index=False)
    
    print(f"Generated {len(df)} samples")
    print(f"\nLabel distribution:")
    print(df["label"].value_counts())
    print(f"\nSaved to {args.output}")

