"""Generate comprehensive realistic training data based on real-world contract patterns."""
import pandas as pd
import random
import re

# Comprehensive real-world contract clauses with actual risk patterns
REALISTIC_CLAUSES = {
    "HIGH": [
        # Unlimited Liability Patterns
        "The Service Provider shall indemnify, defend, and hold harmless the Client, its affiliates, officers, directors, employees, and agents from and against any and all claims, damages, losses, liabilities, costs, and expenses (including reasonable attorneys' fees) arising out of or relating to the Services, without limitation.",
        "Provider agrees to indemnify and hold harmless Customer from any and all claims, demands, losses, costs, and expenses, including attorneys' fees, arising out of or relating to Provider's performance under this Agreement, without any limitation whatsoever.",
        "Vendor shall defend, indemnify, and hold harmless Company and its officers, directors, employees, and agents from and against all claims, damages, losses, and expenses, including legal fees, without limitation, arising from Vendor's breach of this Agreement.",
        
        # Automatic Renewal with Penalties
        "This Agreement shall automatically renew for successive one-year periods unless either party provides written notice of non-renewal at least 90 days prior to the expiration of the then-current term. Early termination by Client shall result in payment of all remaining fees plus a termination penalty equal to 50% of the annual contract value.",
        "The term of this Agreement shall automatically extend for additional one-year periods unless terminated by either party with 60 days written notice. Client agrees that early termination will result in immediate payment of all fees for the remainder of the then-current term plus a cancellation fee of 75% of the annual fee.",
        "This contract will automatically renew for consecutive twelve-month periods. Termination requires 90 days advance written notice. If Client terminates early, Client must pay all remaining monthly fees plus a penalty equal to 100% of one year's fees.",
        
        # Binding Arbitration with Waiver
        "Any dispute arising under this Agreement shall be resolved exclusively through binding arbitration in accordance with the rules of the American Arbitration Association. The parties hereby waive any right to a jury trial and agree that arbitration shall be the sole and exclusive remedy for any disputes.",
        "All disputes, controversies, or claims arising out of or relating to this Agreement shall be settled by binding arbitration. The parties expressly waive their right to a trial by jury and agree that arbitration is the exclusive method for resolving disputes.",
        "Any controversy or claim arising out of or relating to this contract shall be settled by arbitration, and judgment upon the award rendered by the arbitrator may be entered in any court having jurisdiction. The parties waive all rights to a jury trial.",
        
        # No Refund Policy
        "All fees paid hereunder are non-refundable under any circumstances, including but not limited to termination by either party, breach of contract, force majeure events, or dissatisfaction with the Services. Client acknowledges that no refunds will be provided for any reason whatsoever.",
        "Payments made under this Agreement are final and non-refundable. No refunds will be issued for any reason, including but not limited to service cancellation, breach by Provider, or Client dissatisfaction.",
        "All amounts paid are non-refundable and non-transferable. Client understands and agrees that fees are earned upon payment and will not be refunded under any circumstances.",
        
        # Sole Discretion
        "The Service Provider reserves the right, in its sole and absolute discretion, to modify, suspend, or terminate the Services at any time, with or without notice, and without liability to Client or any third party.",
        "Provider may, in its sole discretion, change, modify, or discontinue any aspect of the Services without prior notice and without any liability to Customer.",
        "Company reserves the right to alter, modify, or discontinue the Services at any time in its sole discretion, with or without notice, and Customer shall have no recourse against Company for such changes.",
        
        # Liquidated Damages
        "In the event of breach by Client, Client shall pay liquidated damages equal to 100% of the total contract value as a penalty, which amount the parties agree represents a reasonable estimate of damages and is not a penalty.",
        "If Client breaches this Agreement, Client agrees to pay liquidated damages in the amount of 150% of the total fees paid or payable under this Agreement, which the parties agree is a reasonable estimate of damages.",
        "Upon breach by Customer, Customer shall immediately pay liquidated damages equal to two times the annual contract value, which amount is agreed to be a reasonable estimate of actual damages.",
        
        # Confidentiality Breach Penalties
        "Any breach of the confidentiality obligations set forth herein shall result in immediate payment of $500,000 as liquidated damages, in addition to any other remedies available at law or in equity.",
        "Violation of the confidentiality provisions of this Agreement shall result in liquidated damages of $1,000,000, payable immediately upon breach, in addition to all other available legal and equitable remedies.",
        "Any unauthorized disclosure of confidential information shall result in immediate payment of $750,000 as liquidated damages, which the parties agree is a reasonable estimate of the harm caused by such breach.",
        
        # Exclusive Jurisdiction
        "This Agreement shall be governed by the laws of the State of Delaware, and any disputes shall be subject to the exclusive jurisdiction of the courts of Delaware, regardless of conflicts of law principles.",
        "This Agreement is governed by Delaware law. All disputes must be brought exclusively in the state and federal courts located in Delaware, and each party consents to the personal jurisdiction of such courts.",
        "The laws of Delaware govern this Agreement. Any legal action must be commenced exclusively in Delaware courts, and the parties waive any objection to venue or jurisdiction in Delaware.",
        
        # As-Is Warranty Disclaimer
        "THE SERVICES ARE PROVIDED 'AS IS' AND 'AS AVAILABLE' WITHOUT ANY WARRANTIES OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, OR NON-INFRINGEMENT.",
        "PROVIDER DISCLAIMS ALL WARRANTIES, EXPRESS OR IMPLIED, INCLUDING WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT. THE SERVICES ARE PROVIDED 'AS IS' WITHOUT WARRANTY OF ANY KIND.",
        "TO THE MAXIMUM EXTENT PERMITTED BY LAW, COMPANY DISCLAIMS ALL WARRANTIES, WHETHER EXPRESS, IMPLIED, STATUTORY, OR OTHERWISE, INCLUDING WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.",
        
        # Data Loss Liability Waiver
        "Service Provider shall not be liable for any loss, corruption, or unauthorized access to Client data, regardless of the cause, including but not limited to system failures, security breaches, or acts of third parties. Client assumes all risk related to data storage and transmission.",
        "Provider is not responsible for any loss, damage, or unauthorized access to Customer data, whether caused by Provider's negligence, system failures, security breaches, or any other cause. Customer bears all risk of data loss.",
        "Company shall have no liability whatsoever for any loss, corruption, or unauthorized disclosure of data, regardless of the cause. Customer is solely responsible for backing up and protecting its data.",
        
        # Unilateral Modification Rights
        "Provider reserves the right to modify the terms of this Agreement at any time by posting revised terms. Continued use of the Services after such modifications constitutes acceptance of the revised terms.",
        "Company may amend this Agreement at any time by providing notice to Customer. Customer's continued use of the Services after such amendment constitutes acceptance of the amended terms.",
        "This Agreement may be modified by Provider at any time without Customer's consent. Customer's continued use of the Services constitutes acceptance of any modifications.",
        
        # Excessive Termination Fees
        "If Client terminates this Agreement for any reason prior to the expiration of the initial term, Client shall pay an early termination fee equal to 200% of the remaining fees due under this Agreement.",
        "Early termination by Customer will result in immediate payment of all remaining fees for the entire contract term, plus an additional termination penalty of 100% of the annual fee.",
        "Customer may not terminate this Agreement before the end of the term without paying all remaining fees plus a cancellation charge equal to 150% of one year's fees.",
    ],
    
    "MEDIUM": [
        # Standard Termination
        "Either party may terminate this Agreement upon 60 days written notice to the other party in the event of a material breach that remains uncured after such notice period.",
        "This Agreement may be terminated by either party upon 30 days written notice if the other party materially breaches this Agreement and fails to cure such breach within the notice period.",
        "Either party may terminate this Agreement for cause upon 45 days written notice if the other party fails to cure a material breach within such notice period.",
        
        # Governing Law
        "This Agreement shall be governed by and construed in accordance with the laws of the State of California, without regard to its conflict of law provisions.",
        "This Agreement is governed by the laws of New York, without regard to conflict of law principles.",
        "The laws of Texas govern this Agreement, excluding its conflict of law rules.",
        
        # Assignment Restrictions
        "Neither party may assign this Agreement or any rights or obligations hereunder without the prior written consent of the other party, except that either party may assign this Agreement to an affiliate or in connection with a merger or acquisition.",
        "This Agreement may not be assigned by either party without the prior written consent of the other party, provided that either party may assign this Agreement to an affiliate or successor in connection with a merger or sale of assets.",
        "Assignment of this Agreement requires the prior written consent of the other party, except that either party may assign to an affiliate or in connection with a corporate reorganization.",
        
        # Limitation of Liability
        "IN NO EVENT SHALL EITHER PARTY'S LIABILITY EXCEED THE TOTAL AMOUNT PAID BY CLIENT TO SERVICE PROVIDER IN THE TWELVE (12) MONTHS PRECEDING THE CLAIM.",
        "Neither party's liability shall exceed the total fees paid by Customer in the 12 months preceding the claim giving rise to liability.",
        "Each party's total liability under this Agreement shall not exceed the amount paid by Customer in the year prior to the event giving rise to liability.",
        
        # Dispute Resolution
        "Any disputes arising under this Agreement shall first be addressed through good faith negotiations between the parties. If such negotiations are unsuccessful, the parties agree to submit the dispute to mediation before pursuing other remedies.",
        "The parties agree to attempt to resolve any disputes through good faith negotiation. If negotiation fails, the parties will submit the dispute to mediation before initiating litigation.",
        "Disputes shall first be addressed through direct discussions between the parties. If resolution cannot be reached, the parties agree to participate in mediation before pursuing other legal remedies.",
        
        # Modification Requirements
        "This Agreement may only be modified by a written instrument signed by both parties. No oral modifications or course of conduct shall be deemed to modify this Agreement.",
        "This Agreement may be amended only by a written agreement signed by both parties. No oral agreements or course of dealing shall modify this Agreement.",
        "Modifications to this Agreement must be in writing and signed by both parties. No oral modifications are permitted.",
        
        # Confidentiality Standard
        "Each party agrees to maintain the confidentiality of all proprietary and confidential information received from the other party during the term of this Agreement and for a period of three (3) years thereafter.",
        "The parties agree to keep confidential all proprietary information disclosed during the term of this Agreement and for two years following termination.",
        "Each party shall maintain the confidentiality of the other party's confidential information during the term and for a period of five years after termination.",
        
        # Force Majeure
        "Neither party shall be liable for any failure or delay in performance under this Agreement due to circumstances beyond its reasonable control, including but not limited to acts of God, war, terrorism, or government actions.",
        "Neither party will be liable for delays or failures in performance resulting from circumstances beyond its reasonable control, including natural disasters, war, terrorism, or government actions.",
        "If either party is unable to perform due to circumstances beyond its reasonable control, including acts of God, war, or government actions, such party shall not be liable for such failure or delay.",
        
        # Entire Agreement
        "This Agreement, together with any exhibits attached hereto, constitutes the entire agreement between the parties and supersedes all prior agreements, understandings, and communications, whether written or oral, relating to the subject matter hereof.",
        "This Agreement, including all exhibits, represents the complete agreement between the parties and supersedes all prior agreements and understandings, whether written or oral.",
        "This Agreement, together with its exhibits, is the entire agreement between the parties and replaces all prior agreements and discussions relating to the subject matter.",
        
        # Severability
        "If any provision of this Agreement is held to be invalid or unenforceable, the remaining provisions shall remain in full force and effect, and the invalid provision shall be modified to the minimum extent necessary to make it valid and enforceable.",
        "If any term of this Agreement is found to be unenforceable, the remaining terms shall continue in effect, and the unenforceable term shall be modified to the extent necessary to make it enforceable.",
        "Should any provision of this Agreement be declared invalid, the remainder of this Agreement shall remain in full force and effect, and the invalid provision shall be reformed to the minimum extent necessary.",
        
        # Payment Terms
        "Payment is due within 30 days of invoice date. Late payments shall incur interest at a rate of 1.5% per month on the outstanding balance.",
        "All invoices are due and payable within 30 days of the invoice date. Overdue amounts shall bear interest at the rate of 1% per month.",
        "Payment terms are net 30 days from invoice date. Past due amounts will accrue interest at 1.5% per month.",
        
        # Intellectual Property
        "All intellectual property rights in the Services remain the exclusive property of Provider. Customer receives only a limited license to use the Services as provided in this Agreement.",
        "Provider retains all rights, title, and interest in and to the Services and all intellectual property therein. Customer has no ownership rights in the Services.",
        "All intellectual property in the Services is owned by Company. Customer receives a non-exclusive, non-transferable license to use the Services subject to the terms of this Agreement.",
        
        # Service Level Agreements
        "Provider will use commercially reasonable efforts to maintain 99% uptime for the Services, but Provider does not guarantee uninterrupted or error-free operation.",
        "Company will strive to provide 99.9% availability of the Services, but does not warrant that the Services will be available at all times or free from errors.",
        "Provider targets 99.5% uptime but makes no guarantees regarding service availability or uninterrupted operation.",
    ],
    
    "LOW": [
        # Standard Commencement
        "This Agreement shall commence on the Effective Date and continue until terminated in accordance with its terms.",
        "This Agreement begins on the Effective Date and continues until terminated as provided herein.",
        "The term of this Agreement commences on the Effective Date and continues until terminated in accordance with the terms set forth below.",
        
        # Good Faith
        "The parties agree to act in good faith and deal fairly with each other in all matters relating to this Agreement.",
        "Each party agrees to act in good faith in the performance of its obligations under this Agreement.",
        "The parties will deal with each other in good faith and in a fair and reasonable manner.",
        
        # Authority Representation
        "Each party represents and warrants that it has the full power and authority to enter into this Agreement and to perform its obligations hereunder.",
        "Each party represents that it has the legal capacity and authority to enter into and perform this Agreement.",
        "Both parties represent that they have the necessary power and authority to execute and perform this Agreement.",
        
        # Counterparts
        "This Agreement may be executed in counterparts, each of which shall be deemed an original, and all of which together shall constitute one and the same instrument.",
        "This Agreement may be signed in multiple counterparts, each of which is an original, and all counterparts together constitute one agreement.",
        "The parties may execute this Agreement in one or more counterparts, each of which shall be deemed an original.",
        
        # Electronic Signatures
        "This Agreement may be executed and delivered by facsimile or electronic transmission, and such execution and delivery shall be as effective as delivery of an original executed counterpart.",
        "This Agreement may be executed electronically, and electronic signatures shall have the same legal effect as original signatures.",
        "The parties may sign this Agreement using electronic signatures, which shall be binding and enforceable.",
        
        # Notices
        "All notices required or permitted under this Agreement shall be in writing and shall be deemed given when delivered personally, sent by certified mail, or sent by email to the addresses specified in this Agreement.",
        "Notices under this Agreement must be in writing and shall be effective when delivered to the address specified in this Agreement, either by mail, email, or personal delivery.",
        "Any notice required by this Agreement shall be in writing and delivered to the address set forth in this Agreement by mail, email, or personal delivery.",
        
        # Headings
        "The headings in this Agreement are for convenience only and shall not affect the interpretation of any provision.",
        "Section headings are for reference purposes only and do not affect the meaning or interpretation of this Agreement.",
        "The headings used in this Agreement are for convenience and do not affect the construction or interpretation of the provisions.",
        
        # Binding Effect
        "This Agreement shall be binding upon and inure to the benefit of the parties and their respective successors and permitted assigns.",
        "This Agreement is binding on the parties and their successors and permitted assigns.",
        "This Agreement shall be binding on and inure to the benefit of the parties and their lawful successors.",
        
        # No Third-Party Beneficiaries
        "This Agreement is for the sole benefit of the parties and their permitted assigns and nothing herein shall be construed to give any other person or entity any legal or equitable right, remedy, or claim.",
        "This Agreement is intended solely for the benefit of the parties and does not create any rights in favor of third parties.",
        "Nothing in this Agreement shall be construed to confer any rights or benefits on any person or entity other than the parties to this Agreement.",
        
        # Survival
        "The provisions of this Agreement that by their nature should survive termination shall survive termination, including but not limited to confidentiality obligations, indemnification, and limitation of liability.",
        "Provisions that by their nature should survive termination, including confidentiality, indemnification, and limitation of liability, shall survive the termination of this Agreement.",
        "Terms that should logically survive termination, such as confidentiality, indemnification, and limitation of liability, will continue in effect after termination.",
        
        # Independent Contractors
        "The parties are independent contractors, and nothing in this Agreement shall be construed to create a partnership, joint venture, or agency relationship between the parties.",
        "This Agreement does not create a partnership, joint venture, or agency relationship. The parties are independent contractors.",
        "The parties are independent contractors. This Agreement does not establish a partnership, joint venture, or agency relationship.",
        
        # Waiver
        "The failure of either party to enforce any provision of this Agreement shall not constitute a waiver of such provision or any other provision.",
        "A party's failure to enforce any term of this Agreement does not waive that term or any other term.",
        "No waiver of any provision of this Agreement shall be effective unless in writing and signed by the party waiving such provision.",
        
        # Time of Essence
        "Time is of the essence in the performance of this Agreement.",
        "The parties agree that time is of the essence with respect to all obligations under this Agreement.",
        "All time periods specified in this Agreement are of the essence.",
    ]
}

def add_variations(clause: str) -> list:
    """Add variations to a clause for data augmentation."""
    variations = [clause]
    
    # Replace common terms
    replacements = {
        "Service Provider": ["Provider", "Vendor", "Company", "Supplier"],
        "Client": ["Customer", "Buyer", "Company", "Purchaser"],
        "Agreement": ["Contract", "Agreement", "Service Agreement"],
        "Services": ["Services", "Service", "Work", "Deliverables"],
    }
    
    for old_term, new_terms in replacements.items():
        if old_term in clause:
            for new_term in new_terms[:2]:  # Limit variations
                variations.append(clause.replace(old_term, new_term))
    
    # Add slight modifications
    if "shall" in clause.lower():
        variations.append(clause.replace("shall", "will").replace("Shall", "Will"))
    if "may" in clause.lower():
        variations.append(clause.replace("may", "is authorized to").replace("May", "Is authorized to"))
    
    return variations[:3]  # Return max 3 variations

def generate_comprehensive_dataset(num_samples_per_class: int = 500) -> pd.DataFrame:
    """Generate comprehensive realistic training dataset."""
    data = []
    
    for risk_level, clauses in REALISTIC_CLAUSES.items():
        # Use each base clause multiple times with variations
        clauses_per_base = max(1, num_samples_per_class // len(clauses))
        
        for base_clause in clauses:
            variations = add_variations(base_clause)
            
            for _ in range(clauses_per_base):
                # Select a variation
                selected_clause = random.choice(variations)
                
                # Add minor text variations
                if random.random() < 0.3:  # 30% chance
                    # Add slight modifications
                    if "State of" in selected_clause:
                        states = ["California", "New York", "Texas", "Delaware", "Florida", "Illinois"]
                        selected_clause = selected_clause.replace("State of California", f"State of {random.choice(states)}")
                        selected_clause = selected_clause.replace("State of New York", f"State of {random.choice(states)}")
                
                # Generate explanations
                explanations = {
                    "HIGH": "Contains high-risk language including unlimited liability, penalties, automatic renewal, or waiver of rights that may expose parties to significant legal and financial risk.",
                    "MEDIUM": "Contains moderate-risk language that requires careful review, including standard termination clauses, liability limitations, or dispute resolution mechanisms.",
                    "LOW": "Contains standard, low-risk language typical of commercial agreements with balanced terms and standard legal protections.",
                }
                
                data.append({
                    "doc_id": f"contract_{random.randint(1000, 99999)}",
                    "clause_text": selected_clause,
                    "label": risk_level,
                    "explanation": explanations[risk_level],
                })
    
    # Shuffle data
    random.shuffle(data)
    
    return pd.DataFrame(data)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate comprehensive realistic contract training data")
    parser.add_argument("--output", type=str, default="comprehensive_training_data.csv", help="Output CSV file")
    parser.add_argument("--samples", type=int, default=500, help="Samples per class")
    
    args = parser.parse_args()
    
    print("Generating comprehensive realistic contract training data...")
    print(f"Target: {args.samples} samples per class (HIGH, MEDIUM, LOW)")
    print("This may take a moment...")
    
    df = generate_comprehensive_dataset(args.samples)
    df.to_csv(args.output, index=False)
    
    print(f"\n[SUCCESS] Generated {len(df)} total samples")
    print(f"\nLabel distribution:")
    print(df["label"].value_counts())
    print(f"\n[INFO] Saved to {args.output}")
    print(f"\n[INFO] Next step - Train the model:")
    print(f"   cd backend")
    print(f"   .\\venv\\Scripts\\Activate.ps1")
    print(f"   python -m app.ml.train --data ../ml_data/{args.output} --output ./models/risk_classifier --epochs 5 --batch-size 16")

