"""Generate realistic contract training data based on real-world patterns."""
import pandas as pd
import random

# Real-world contract clauses with actual risk patterns
REALISTIC_CLAUSES = {
    "HIGH": [
        # Unlimited Liability
        "The Service Provider shall indemnify, defend, and hold harmless the Client, its affiliates, officers, directors, employees, and agents from and against any and all claims, damages, losses, liabilities, costs, and expenses (including reasonable attorneys' fees) arising out of or relating to the Services, without limitation.",
        
        # Automatic Renewal with Penalties
        "This Agreement shall automatically renew for successive one-year periods unless either party provides written notice of non-renewal at least 90 days prior to the expiration of the then-current term. Early termination by Client shall result in payment of all remaining fees plus a termination penalty equal to 50% of the annual contract value.",
        
        # Binding Arbitration with Waiver
        "Any dispute arising under this Agreement shall be resolved exclusively through binding arbitration in accordance with the rules of the American Arbitration Association. The parties hereby waive any right to a jury trial and agree that arbitration shall be the sole and exclusive remedy for any disputes.",
        
        # No Refund Policy
        "All fees paid hereunder are non-refundable under any circumstances, including but not limited to termination by either party, breach of contract, force majeure events, or dissatisfaction with the Services. Client acknowledges that no refunds will be provided for any reason whatsoever.",
        
        # Sole Discretion
        "The Service Provider reserves the right, in its sole and absolute discretion, to modify, suspend, or terminate the Services at any time, with or without notice, and without liability to Client or any third party.",
        
        # Liquidated Damages
        "In the event of breach by Client, Client shall pay liquidated damages equal to 100% of the total contract value as a penalty, which amount the parties agree represents a reasonable estimate of damages and is not a penalty.",
        
        # Confidentiality Breach Penalties
        "Any breach of the confidentiality obligations set forth herein shall result in immediate payment of $500,000 as liquidated damages, in addition to any other remedies available at law or in equity.",
        
        # Exclusive Jurisdiction
        "This Agreement shall be governed by the laws of the State of Delaware, and any disputes shall be subject to the exclusive jurisdiction of the courts of Delaware, regardless of conflicts of law principles.",
        
        # As-Is Warranty Disclaimer
        "THE SERVICES ARE PROVIDED 'AS IS' AND 'AS AVAILABLE' WITHOUT ANY WARRANTIES OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, OR NON-INFRINGEMENT.",
        
        # Data Loss Liability Waiver
        "Service Provider shall not be liable for any loss, corruption, or unauthorized access to Client data, regardless of the cause, including but not limited to system failures, security breaches, or acts of third parties. Client assumes all risk related to data storage and transmission.",
    ],
    
    "MEDIUM": [
        # Standard Termination
        "Either party may terminate this Agreement upon 60 days written notice to the other party in the event of a material breach that remains uncured after such notice period.",
        
        # Governing Law
        "This Agreement shall be governed by and construed in accordance with the laws of the State of California, without regard to its conflict of law provisions.",
        
        # Assignment Restrictions
        "Neither party may assign this Agreement or any rights or obligations hereunder without the prior written consent of the other party, except that either party may assign this Agreement to an affiliate or in connection with a merger or acquisition.",
        
        # Limitation of Liability
        "IN NO EVENT SHALL EITHER PARTY'S LIABILITY EXCEED THE TOTAL AMOUNT PAID BY CLIENT TO SERVICE PROVIDER IN THE TWELVE (12) MONTHS PRECEDING THE CLAIM.",
        
        # Dispute Resolution
        "Any disputes arising under this Agreement shall first be addressed through good faith negotiations between the parties. If such negotiations are unsuccessful, the parties agree to submit the dispute to mediation before pursuing other remedies.",
        
        # Modification Requirements
        "This Agreement may only be modified by a written instrument signed by both parties. No oral modifications or course of conduct shall be deemed to modify this Agreement.",
        
        # Confidentiality Standard
        "Each party agrees to maintain the confidentiality of all proprietary and confidential information received from the other party during the term of this Agreement and for a period of three (3) years thereafter.",
        
        # Force Majeure
        "Neither party shall be liable for any failure or delay in performance under this Agreement due to circumstances beyond its reasonable control, including but not limited to acts of God, war, terrorism, or government actions.",
        
        # Entire Agreement
        "This Agreement, together with any exhibits attached hereto, constitutes the entire agreement between the parties and supersedes all prior agreements, understandings, and communications, whether written or oral, relating to the subject matter hereof.",
        
        # Severability
        "If any provision of this Agreement is held to be invalid or unenforceable, the remaining provisions shall remain in full force and effect, and the invalid provision shall be modified to the minimum extent necessary to make it valid and enforceable.",
    ],
    
    "LOW": [
        # Standard Commencement
        "This Agreement shall commence on the Effective Date and continue until terminated in accordance with its terms.",
        
        # Good Faith
        "The parties agree to act in good faith and deal fairly with each other in all matters relating to this Agreement.",
        
        # Authority Representation
        "Each party represents and warrants that it has the full power and authority to enter into this Agreement and to perform its obligations hereunder.",
        
        # Counterparts
        "This Agreement may be executed in counterparts, each of which shall be deemed an original, and all of which together shall constitute one and the same instrument.",
        
        # Electronic Signatures
        "This Agreement may be executed and delivered by facsimile or electronic transmission, and such execution and delivery shall be as effective as delivery of an original executed counterpart.",
        
        # Notices
        "All notices required or permitted under this Agreement shall be in writing and shall be deemed given when delivered personally, sent by certified mail, or sent by email to the addresses specified in this Agreement.",
        
        # Headings
        "The headings in this Agreement are for convenience only and shall not affect the interpretation of any provision.",
        
        # Binding Effect
        "This Agreement shall be binding upon and inure to the benefit of the parties and their respective successors and permitted assigns.",
        
        # No Third-Party Beneficiaries
        "This Agreement is for the sole benefit of the parties and their permitted assigns and nothing herein shall be construed to give any other person or entity any legal or equitable right, remedy, or claim.",
        
        # Survival
        "The provisions of this Agreement that by their nature should survive termination shall survive termination, including but not limited to confidentiality obligations, indemnification, and limitation of liability.",
    ]
}

def generate_realistic_dataset(num_samples_per_class: int = 100) -> pd.DataFrame:
    """Generate realistic training dataset."""
    data = []
    
    for risk_level, clauses in REALISTIC_CLAUSES.items():
        for _ in range(num_samples_per_class):
            clause = random.choice(clauses)
            
            # Add some variation
            variations = [
                clause,
                clause.replace("Service Provider", random.choice(["Provider", "Vendor", "Company"])),
                clause.replace("Client", random.choice(["Customer", "Buyer", "Company"])),
            ]
            selected_clause = random.choice(variations)
            
            # Generate explanations
            explanations = {
                "HIGH": "Contains high-risk language including unlimited liability, penalties, automatic renewal, or waiver of rights that may expose parties to significant legal and financial risk.",
                "MEDIUM": "Contains moderate-risk language that requires careful review, including standard termination clauses, liability limitations, or dispute resolution mechanisms.",
                "LOW": "Contains standard, low-risk language typical of commercial agreements with balanced terms and standard legal protections.",
            }
            
            data.append({
                "doc_id": f"contract_{random.randint(1000, 9999)}",
                "clause_text": selected_clause,
                "label": risk_level,
                "explanation": explanations[risk_level],
            })
    
    return pd.DataFrame(data)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate realistic contract training data")
    parser.add_argument("--output", type=str, default="realistic_training_data.csv", help="Output CSV file")
    parser.add_argument("--samples", type=int, default=100, help="Samples per class")
    
    args = parser.parse_args()
    
    print("Generating realistic contract training data...")
    df = generate_realistic_dataset(args.samples)
    df.to_csv(args.output, index=False)
    
    print(f"\n✅ Generated {len(df)} samples")
    print(f"\nLabel distribution:")
    print(df["label"].value_counts())
    print(f"\n📁 Saved to {args.output}")
    print(f"\n💡 Use this to train the model:")
    print(f"   cd backend")
    print(f"   python -m app.ml.train --data ../ml_data/{args.output} --output ./models/risk_classifier --epochs 5")

