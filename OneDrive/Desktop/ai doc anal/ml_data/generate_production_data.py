"""Generate production-quality training data based on real-world contract patterns."""
import pandas as pd
import random

# Real-world contract clauses based on actual legal patterns
PRODUCTION_CLAUSES = {
    "HIGH": [
        # Unlimited Indemnification
        "The Service Provider shall indemnify, defend, and hold harmless the Client, its affiliates, officers, directors, employees, agents, and successors from and against any and all claims, demands, losses, costs, expenses, damages, judgments, penalties, interest, and liabilities (including reasonable attorneys' fees and costs) of any kind whatsoever, whether known or unknown, arising out of or relating to this Agreement, the Services, or any breach thereof, without limitation or exception.",
        
        # Automatic Renewal with Penalties
        "This Agreement shall automatically renew for successive periods of one (1) year each unless either party provides written notice of non-renewal at least ninety (90) days prior to the expiration of the then-current term. In the event of early termination by Client for any reason other than Provider's material breach, Client shall pay to Provider all remaining fees due under this Agreement for the entire term, plus a termination fee equal to fifty percent (50%) of the annual contract value, which Client acknowledges is a reasonable estimate of Provider's damages and not a penalty.",
        
        # Binding Arbitration with Waiver
        "Any dispute, controversy, or claim arising out of or relating to this Agreement, or the breach, termination, or validity thereof, shall be settled exclusively by binding arbitration in accordance with the Commercial Arbitration Rules of the American Arbitration Association. The arbitration shall be conducted in [City, State], and the arbitrator's decision shall be final and binding. The parties hereby waive any right to a jury trial and agree that arbitration shall be the sole and exclusive remedy for any disputes. Each party shall bear its own costs and attorneys' fees.",
        
        # No Refund Policy
        "All fees paid by Client hereunder are non-refundable under any and all circumstances, including but not limited to: (a) termination of this Agreement by either party for any reason; (b) breach of this Agreement by Provider; (c) force majeure events; (d) Client's dissatisfaction with the Services; (e) Client's inability to use the Services; or (f) any other reason whatsoever. Client acknowledges and agrees that no refunds, credits, or reimbursements will be provided under any circumstances.",
        
        # Sole Discretion
        "Provider reserves the right, in its sole and absolute discretion, without prior notice or liability to Client or any third party, to modify, suspend, discontinue, or terminate the Services, or any portion thereof, at any time, for any reason or no reason, including but not limited to maintenance, updates, or business decisions. Provider shall not be liable for any damages, losses, or expenses incurred by Client as a result of such modification, suspension, discontinuation, or termination.",
        
        # Liquidated Damages
        "In the event of any breach of this Agreement by Client, including but not limited to failure to make timely payment, unauthorized use of the Services, or violation of any term or condition hereof, Client shall pay to Provider as liquidated damages and not as a penalty, an amount equal to one hundred percent (100%) of the total contract value, which amount the parties agree represents a reasonable estimate of the damages that Provider would incur as a result of such breach.",
        
        # Confidentiality Breach Penalties
        "Any breach of the confidentiality obligations set forth in this Agreement by Client shall constitute a material breach of this Agreement and shall result in immediate payment to Provider of Five Hundred Thousand Dollars ($500,000) as liquidated damages, in addition to any other remedies available to Provider at law or in equity, including but not limited to injunctive relief and recovery of attorneys' fees and costs.",
        
        # Exclusive Jurisdiction
        "This Agreement shall be governed by and construed in accordance with the laws of the State of Delaware, without regard to its conflict of law principles. Any legal action or proceeding arising under or relating to this Agreement shall be brought exclusively in the federal or state courts located in Delaware, and the parties hereby irrevocably consent to the personal jurisdiction and venue of such courts. The parties waive any objection to such jurisdiction and venue.",
        
        # As-Is Warranty Disclaimer
        "THE SERVICES ARE PROVIDED 'AS IS' AND 'AS AVAILABLE' WITHOUT ANY WARRANTIES OF ANY KIND, WHETHER EXPRESS, IMPLIED, STATUTORY, OR OTHERWISE, INCLUDING BUT NOT LIMITED TO WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, NON-INFRINGEMENT, TITLE, QUIET ENJOYMENT, OR ACCURACY. PROVIDER DISCLAIMS ALL WARRANTIES TO THE MAXIMUM EXTENT PERMITTED BY APPLICABLE LAW.",
        
        # Data Loss Liability Waiver
        "Provider shall not be liable for any loss, corruption, destruction, alteration, or unauthorized access to Client data, information, or content, regardless of the cause, including but not limited to system failures, security breaches, cyber attacks, acts of third parties, force majeure events, or Provider's negligence. Client acknowledges that it is solely responsible for maintaining adequate backups of all Client data and that Provider has no obligation to maintain, store, or backup Client data.",
        
        # Unlimited Liability Exposure
        "Client agrees that Provider's liability for any claims, damages, losses, or expenses arising out of or relating to this Agreement or the Services, whether based on contract, tort, strict liability, or any other legal theory, shall be unlimited and shall include, without limitation, direct, indirect, incidental, special, consequential, and punitive damages, even if Provider has been advised of the possibility of such damages.",
        
        # Waiver of Rights
        "Client hereby waives, to the fullest extent permitted by applicable law, any and all rights, claims, or causes of action it may have against Provider, including but not limited to rights to a jury trial, rights to participate in class actions, rights to seek punitive or exemplary damages, and any other rights that may be available under applicable law.",
        
        # Termination Without Cause
        "Provider may terminate this Agreement at any time, for any reason or no reason, with or without cause, immediately upon written notice to Client, without liability, penalty, or obligation of any kind. Upon such termination, Client shall immediately cease all use of the Services and return or destroy all Confidential Information.",
        
        # Assignment Restrictions
        "Client may not assign, transfer, or delegate this Agreement or any of its rights or obligations hereunder without the prior written consent of Provider, which consent may be withheld in Provider's sole and absolute discretion. Any attempted assignment, transfer, or delegation without such consent shall be null and void.",
        
        # Modification Rights
        "Provider reserves the right to modify, amend, or change the terms and conditions of this Agreement at any time, in its sole discretion, by posting the modified Agreement on its website or by providing notice to Client. Client's continued use of the Services after such modification shall constitute acceptance of the modified terms.",
    ],
    
    "MEDIUM": [
        # Standard Termination
        "Either party may terminate this Agreement upon sixty (60) days written notice to the other party in the event of a material breach of this Agreement by the other party that remains uncured after such notice period. Upon termination, each party shall return or destroy all Confidential Information of the other party.",
        
        # Governing Law
        "This Agreement shall be governed by and construed in accordance with the laws of the State of California, without regard to its conflict of law provisions. Any disputes arising under this Agreement shall be subject to the exclusive jurisdiction of the state and federal courts located in California.",
        
        # Limitation of Liability
        "IN NO EVENT SHALL EITHER PARTY'S LIABILITY UNDER THIS AGREEMENT EXCEED THE TOTAL AMOUNT PAID BY CLIENT TO PROVIDER IN THE TWELVE (12) MONTHS PRECEDING THE CLAIM. THIS LIMITATION SHALL APPLY REGARDLESS OF THE THEORY OF LIABILITY, WHETHER BASED ON CONTRACT, TORT, STRICT LIABILITY, OR OTHERWISE.",
        
        # Dispute Resolution
        "Any disputes arising under this Agreement shall first be addressed through good faith negotiations between the parties. If such negotiations are unsuccessful within thirty (30) days, the parties agree to submit the dispute to mediation before a mutually agreed mediator before pursuing other remedies.",
        
        # Confidentiality Standard
        "Each party agrees to maintain the confidentiality of all proprietary and confidential information received from the other party during the term of this Agreement and for a period of three (3) years thereafter. Confidential Information shall not include information that is publicly available or independently developed.",
        
        # Force Majeure
        "Neither party shall be liable for any failure or delay in performance under this Agreement due to circumstances beyond its reasonable control, including but not limited to acts of God, war, terrorism, natural disasters, government actions, labor strikes, or failures of third-party services.",
        
        # Entire Agreement
        "This Agreement, together with any exhibits, schedules, or attachments attached hereto, constitutes the entire agreement between the parties and supersedes all prior agreements, understandings, negotiations, and communications, whether written or oral, relating to the subject matter hereof.",
        
        # Severability
        "If any provision of this Agreement is held to be invalid, illegal, or unenforceable by a court of competent jurisdiction, the remaining provisions shall remain in full force and effect, and the invalid provision shall be modified to the minimum extent necessary to make it valid and enforceable.",
        
        # Assignment with Consent
        "Neither party may assign this Agreement or any rights or obligations hereunder without the prior written consent of the other party, except that either party may assign this Agreement to an affiliate or in connection with a merger, acquisition, or sale of all or substantially all of its assets.",
        
        # Modification Requirements
        "This Agreement may only be modified by a written instrument signed by both parties. No oral modifications, course of conduct, or trade usage shall be deemed to modify this Agreement.",
        
        # Notices
        "All notices required or permitted under this Agreement shall be in writing and shall be deemed given when delivered personally, sent by certified mail (return receipt requested), or sent by email to the addresses specified in this Agreement.",
        
        # Survival
        "The provisions of this Agreement that by their nature should survive termination shall survive termination, including but not limited to confidentiality obligations, indemnification, limitation of liability, and dispute resolution provisions.",
        
        # Intellectual Property
        "All intellectual property rights in the Services, including but not limited to copyrights, trademarks, trade secrets, and patents, shall remain the exclusive property of Provider. Client shall not acquire any rights in such intellectual property except as expressly granted in this Agreement.",
        
        # Payment Terms
        "Client agrees to pay Provider the fees set forth in this Agreement within thirty (30) days of receipt of invoice. Late payments shall bear interest at the rate of one and one-half percent (1.5%) per month or the maximum rate permitted by law, whichever is less.",
        
        # Service Level
        "Provider shall use commercially reasonable efforts to make the Services available 99.9% of the time, measured monthly, excluding scheduled maintenance and force majeure events. Provider does not guarantee uninterrupted or error-free operation of the Services.",
    ],
    
    "LOW": [
        # Standard Commencement
        "This Agreement shall commence on the Effective Date and continue until terminated in accordance with its terms.",
        
        # Good Faith
        "The parties agree to act in good faith and deal fairly with each other in all matters relating to this Agreement.",
        
        # Authority Representation
        "Each party represents and warrants that it has the full power and authority to enter into this Agreement and to perform its obligations hereunder, and that the execution and delivery of this Agreement has been duly authorized.",
        
        # Counterparts
        "This Agreement may be executed in counterparts, each of which shall be deemed an original, and all of which together shall constitute one and the same instrument. Execution and delivery may be evidenced by facsimile or electronic signature.",
        
        # Electronic Signatures
        "This Agreement may be executed and delivered by facsimile, electronic mail, or other electronic means, and such execution and delivery shall be as effective as delivery of an original executed counterpart of this Agreement.",
        
        # Headings
        "The headings in this Agreement are for convenience only and shall not affect the interpretation of any provision of this Agreement.",
        
        # Binding Effect
        "This Agreement shall be binding upon and inure to the benefit of the parties and their respective successors and permitted assigns.",
        
        # No Third-Party Beneficiaries
        "This Agreement is for the sole benefit of the parties and their permitted assigns and nothing herein, express or implied, is intended to or shall confer upon any other person or entity any legal or equitable right, benefit, or remedy of any nature whatsoever under or by reason of this Agreement.",
        
        # Independent Contractors
        "The parties are independent contractors, and nothing in this Agreement shall be construed to create a partnership, joint venture, agency, or employment relationship between the parties.",
        
        # Waiver
        "No waiver of any term or condition of this Agreement shall be effective unless in writing and signed by the party against whom such waiver is sought to be enforced. No failure or delay by either party in exercising any right hereunder shall operate as a waiver thereof.",
        
        # Time of Essence
        "Time is of the essence with respect to all obligations of the parties under this Agreement.",
        
        # Further Assurances
        "Each party agrees to execute and deliver such additional documents and instruments and to take such further actions as may be reasonably necessary to effectuate the purposes of this Agreement.",
        
        # Publicity
        "Neither party shall issue any press release or make any public announcement regarding this Agreement without the prior written consent of the other party, except as required by law.",
        
        # Expenses
        "Each party shall bear its own costs and expenses incurred in connection with the negotiation, execution, and performance of this Agreement.",
        
        # Language
        "This Agreement has been prepared in the English language, and the English language version shall control in all respects.",
    ]
}

def generate_production_dataset(num_samples_per_class: int = 300) -> pd.DataFrame:
    """Generate production-quality training dataset."""
    data = []
    
    for risk_level, clauses in PRODUCTION_CLAUSES.items():
        # Use each clause multiple times with variations
        for _ in range(num_samples_per_class):
            base_clause = random.choice(clauses)
            
            # Create variations
            variations = [
                base_clause,
                base_clause.replace("Service Provider", random.choice(["Provider", "Vendor", "Company", "Supplier"])),
                base_clause.replace("Client", random.choice(["Customer", "Buyer", "Company", "Purchaser"])),
                base_clause.replace("[City, State]", random.choice(["New York, New York", "San Francisco, California", "Chicago, Illinois", "Boston, Massachusetts"])),
                base_clause.replace("Delaware", random.choice(["California", "New York", "Texas", "Florida"])),
            ]
            
            selected_clause = random.choice(variations)
            
            # Generate explanations
            explanations = {
                "HIGH": "Contains high-risk language including unlimited liability, penalties, automatic renewal, waiver of rights, or other terms that may expose parties to significant legal and financial risk.",
                "MEDIUM": "Contains moderate-risk language that requires careful review, including standard termination clauses, liability limitations, dispute resolution mechanisms, or other terms that may need negotiation.",
                "LOW": "Contains standard, low-risk language typical of commercial agreements with balanced terms and standard legal protections that are generally acceptable in business transactions.",
            }
            
            data.append({
                "doc_id": f"contract_{random.randint(10000, 99999)}",
                "clause_text": selected_clause,
                "label": risk_level,
                "explanation": explanations[risk_level],
            })
    
    return pd.DataFrame(data)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate production-quality training data")
    parser.add_argument("--output", type=str, default="production_training_data.csv", help="Output CSV file")
    parser.add_argument("--samples", type=int, default=300, help="Samples per class")
    
    args = parser.parse_args()
    
    print("Generating production-quality training data...")
    print("This dataset is based on real-world contract patterns...")
    
    df = generate_production_dataset(args.samples)
    df.to_csv(args.output, index=False)
    
    print(f"\n[SUCCESS] Generated {len(df)} high-quality samples")
    print(f"\nLabel distribution:")
    print(df["label"].value_counts())
    print(f"\n[INFO] Saved to {args.output}")
    print(f"\n[INFO] Now train the model:")
    print(f"   cd backend")
    print(f"   .\\venv\\Scripts\\Activate.ps1")
    print(f"   python -m app.ml.train --data ../ml_data/{args.output} --output ./models/risk_classifier --epochs 5 --batch-size 16")

