"""Create enhanced training dataset with extensive legal data, especially Indian legal documents."""
import pandas as pd
import re
import random
from pathlib import Path
from typing import List, Dict
import sys
import os

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))
try:
    from app.services.extract import DocumentExtractor
    from app.services.analysis import RuleBasedAnalyzer
    EXTRACTOR_AVAILABLE = True
except ImportError:
    EXTRACTOR_AVAILABLE = False
    print("Warning: Could not import DocumentExtractor. Will use basic text extraction.")


def get_extensive_indian_legal_clauses() -> List[Dict[str, str]]:
    """Get extensive Indian legal document clauses with proper risk classification."""
    print("Generating extensive Indian legal document clauses...")
    
    clauses_data = []
    
    # HIGH RISK - Indian Legal Documents
    high_risk_indian = [
        # Unilateral Amendment (Indian context)
        "The Landlord reserves the right to modify or amend any term of this Rental Agreement at any time by providing written notice to the Tenant; such modifications shall become effective 14 days after notice is given, and Tenant's continued occupation shall constitute acceptance.",
        "The Company reserves the right, in its sole discretion, to modify, suspend, or discontinue the Services (or any part thereof) at any time, with or without notice, and without liability to Customer, notwithstanding any provisions of the Indian Contract Act, 1872.",
        "Provider may unilaterally amend this Agreement at any time by posting the modified Agreement on its website. Customer's continued use constitutes acceptance, and Customer waives any right to object under the Indian Contract Act.",
        
        # Entry without notice (Indian Rental)
        "The Landlord or their agents may enter the premises at any time, without prior notice, for inspection, repairs, or to show the property to prospective tenants or buyers, and Tenant shall not unreasonably withhold access.",
        "Landlord reserves the right to enter the premises without notice for any reason deemed necessary by Landlord in its sole discretion, including but not limited to emergency repairs, property inspection, or showing to prospective buyers.",
        
        # Indemnification including own negligence (Indian context)
        "Tenant agrees to indemnify and hold Landlord harmless from any claims, losses, liabilities, or expenses (including legal fees and court costs) arising from Tenant's use of the premises, including claims arising from Landlord's own negligence, gross negligence, or willful misconduct, to the fullest extent permitted by Indian law.",
        "Customer shall indemnify, defend, and hold harmless Provider and its officers, directors, employees, agents, affiliates, successors, and assigns from and against any and all claims, demands, losses, costs, expenses, damages, judgments, penalties, interest, and liabilities (including, without limitation, reasonable attorneys' fees and costs) arising out of or relating to Customer's breach of this Agreement, without limitation or exception, including claims arising from Provider's own negligence, notwithstanding any provisions of the Indian Contract Act, 1872.",
        
        # Distant/exclusive jurisdiction (Indian courts)
        "Any dispute arising under this Agreement shall be resolved exclusively by the courts located in {city}, {state}, India, regardless of where the parties are located or where the cause of action arose. The parties hereby submit to the exclusive jurisdiction of such courts and waive any objection to venue.",
        "All disputes, controversies, or claims arising out of or in connection with this Agreement shall be subject to the exclusive jurisdiction of the courts in {city}, {state}, India, and the parties irrevocably submit to such jurisdiction.",
        
        # Short termination (Indian Rental)
        "Landlord may terminate this Rental Agreement with 30 days' written notice if Landlord intends to sell the property, commence redevelopment, or for any other reason; Tenant shall vacate the premises by the termination date without any right to compensation or extension.",
        "Either party may terminate this Agreement with 30 days' written notice, and Tenant must vacate immediately upon termination. Tenant shall remain liable for all rent and charges until the premises are vacated and keys are returned.",
        
        # Automatic renewal with penalties
        "This Agreement will automatically renew for additional periods equal to the expiring term or one year (whichever is shorter), unless either party gives the other notice of non-renewal at least 30 days before the end of the relevant term. If Customer terminates before the end of the term, Customer will remain responsible for all fees payable for the remainder of the term, plus a termination fee equal to 75% of the remaining contract value.",
        
        # Excessive penalties (Indian context)
        "In the event of any material breach of this Agreement by Customer, Customer shall pay to Provider, as liquidated damages and not as a penalty, an amount equal to the greater of: (a) 100% of the total fees payable under this Agreement, or (b) INR {amount}, plus applicable GST and interest at 18% per annum.",
        "If Customer terminates this Agreement before the end of the then-current term, Customer will remain responsible for all fees payable for the remainder of the term, and Provider may charge Customer a termination fee equal to 100% of the remaining contract value, plus applicable taxes.",
        
        # Non-refundable (Indian context)
        "All fees paid by Customer are non-refundable under any circumstances, including but not limited to: (i) termination of this Agreement by either party for any reason; (ii) Customer's dissatisfaction with the Services; (iii) Customer's inability to access or use the Services; (iv) force majeure events; or (v) any other reason whatsoever, notwithstanding any provisions of the Indian Consumer Protection Act, 2019.",
        
        # Unlimited liability
        "Customer's liability to Provider for any claims, damages, losses, or expenses arising out of or relating to this Agreement or the Services, whether based on contract, tort (including negligence), strict liability, or any other legal theory, will be unlimited and will include, without limitation, direct, indirect, incidental, special, consequential, exemplary, and punitive damages, to the fullest extent permitted by Indian law.",
        
        # Waiver of rights (Indian context)
        "Customer hereby waives, to the fullest extent permitted by applicable Indian law, any and all rights it may have against Provider, including without limitation: (a) the right to a trial by jury (where applicable); (b) the right to participate in a class action lawsuit; (c) the right to seek punitive or exemplary damages; (d) any rights under the Indian Consumer Protection Act, 2019; and (e) any other rights that may be available under applicable law.",
        
        # Binding arbitration (Indian context)
        "Any dispute, controversy, or claim arising out of or relating to this Agreement, including the formation, interpretation, breach, or termination thereof, will be referred to and finally determined by arbitration in accordance with the Arbitration and Conciliation Act, 2015, and the rules of the Indian Council of Arbitration. The arbitration shall be conducted in {city}, {state}, India, and the language of arbitration shall be English. The parties waive any right to a jury trial and to appeal.",
    ]
    
    # MEDIUM RISK - Indian Legal Documents
    medium_risk_indian = [
        # Security deposit (Indian Rental)
        "Tenant shall pay a security deposit equal to {months} months' rent (INR {amount}) upon execution of this Agreement. Landlord may deduct from the deposit for unpaid rent, repairs for damages beyond normal wear and tear, unpaid utilities, and any other charges owed by Tenant. The deposit shall be returned within 30 days after tenancy termination, less any lawful deductions, with an itemized statement as required under Indian law.",
        "A security deposit of INR {amount} shall be paid by Tenant upon execution of this Agreement. Landlord may apply the deposit to any unpaid rent, damages, or other charges owed by Tenant, and Tenant shall not be entitled to interest on the deposit.",
        
        # Late payment fees (Indian context)
        "If rent is not received by the {day}th day of each month, Tenant shall pay a late fee equal to {percent}% of the monthly rent per week until payment is made, capped at {cap}% of the monthly rent, plus applicable GST.",
        "Late payments will bear interest at the rate of {percent}% per month or the maximum rate permitted by applicable Indian law, whichever is less, compounded monthly.",
        
        # Subletting restrictions (Indian Rental)
        "Tenant shall not sublet, assign, or transfer the premises or any part thereof without the prior written consent of the Landlord, which may be withheld in Landlord's sole discretion. Any unauthorized subletting shall constitute a material breach of this Agreement.",
        "Customer may not assign, transfer, or delegate this Agreement or any of its rights or obligations hereunder without Provider's prior written consent, which may be withheld in Provider's sole discretion for any reason.",
        
        # Pet restrictions (Indian Rental)
        "No pets are permitted on the premises without the Landlord's prior written consent. If permitted, Tenant must pay a refundable pet deposit of INR {amount} and is responsible for any damage or nuisance caused by the pet, including but not limited to noise complaints, property damage, or health hazards.",
        
        # Alterations (Indian Rental)
        "Tenant shall not make any structural alterations, install fixtures, or make improvements to the premises without prior written consent of the Landlord. Any approved fixtures affixed by Tenant shall become the property of the Landlord at lease end unless otherwise agreed in writing, in accordance with Indian property law.",
        
        # Termination with liability (Indian context)
        "Either party may terminate this Agreement with {days} days' written notice. If Tenant terminates before the lease term ends without Landlord's consent, Tenant shall be liable for rent until the premises are re-let or for {months} months' rent, whichever is lesser, plus any costs incurred by Landlord in re-letting the premises.",
        "If Customer terminates this Agreement before the end of the then-current term, Customer will be responsible for {percent}% of the remaining fees, plus any costs incurred by Provider in connection with such early termination.",
        
        # Rent escalation (Indian context)
        "Landlord may increase rent annually by up to {percent}% or by the change in the Consumer Price Index (CPI) for urban areas published by the Government of India, whichever is lower, upon providing {days} days' written notice prior to the effective increase, subject to applicable rent control laws.",
        
        # Fixtures (Indian Rental)
        "Tenant may not remove built-in fixtures, appliances, or cabinetry installed by Landlord. Portable furniture or Tenant-installed appliances may be removed provided Tenant repairs any damage caused by removal to Landlord's satisfaction.",
        
        # Arbitration (Indian context)
        "Any disputes arising under this Agreement will first be addressed through good faith negotiations between the parties. If such negotiations are unsuccessful within {days} days, the parties agree to submit the dispute to mediation before a mutually agreed mediator in accordance with the Arbitration and Conciliation Act, 2015.",
        
        # Confidentiality (Indian context)
        "Each party agrees to maintain the confidentiality of all Confidential Information received from the other party during the term of this Agreement and for a period of {years} years thereafter, in accordance with applicable Indian laws including the Information Technology Act, 2000.",
        
        # Liability limits (Indian context)
        "IN NO EVENT WILL EITHER PARTY'S LIABILITY UNDER THIS AGREEMENT EXCEED THE TOTAL AMOUNT PAID BY CUSTOMER TO PROVIDER IN THE TWELVE (12) MONTHS PRECEDING THE CLAIM, OR INR {amount}, WHICHEVER IS LESSER, NOTWITHSTANDING ANY PROVISIONS OF THE INDIAN CONTRACT ACT, 1872.",
        "Provider's total liability for any claims arising out of or relating to this Agreement shall not exceed INR {amount} or the amount paid by Customer in the {months} months preceding the claim, whichever is less, plus applicable taxes.",
        
        # Force majeure (Indian context)
        "Neither party shall be liable for delays or failures to perform due to events beyond their reasonable control, including natural disasters, government actions, pandemics, war, terrorism, acts of God, strikes, lockouts, or any other cause beyond the party's reasonable control, as recognized under Indian law.",
    ]
    
    # LOW RISK - Indian Legal Documents
    low_risk_indian = [
        # Agreement headers (Indian format)
        "THIS RENTAL AGREEMENT is made on this {day} day of {month}, {year} at {city}, {state}, India BETWEEN {landlord}, residing at {address} (hereinafter referred to as the 'Landlord') AND {tenant}, residing at {address} (hereinafter referred to as the 'Tenant').",
        "THIS EMPLOYMENT AGREEMENT is entered into on {day} {month}, {year} at {city}, {state}, India BETWEEN {company}, a company incorporated under the Companies Act, 2013, having its registered office at {address} (hereinafter referred to as the 'Employer') AND {employee}, residing at {address} (hereinafter referred to as the 'Employee').",
        "THIS SERVICE AGREEMENT is made on {day} {month}, {year} at {city}, {state}, India BETWEEN {client}, a {entity_type} having its office at {address} (hereinafter referred to as the 'Client') AND {service_provider}, a {entity_type} having its office at {address} (hereinafter referred to as the 'Service Provider').",
        
        # Recitals (Indian format)
        "WHEREAS the Landlord is the absolute owner of the property situated at {address}, {city}, {state}, India, and the Tenant desires to take the said property on rent, the parties agree as follows:",
        "WHEREAS the parties desire to enter into this Agreement to set forth the terms and conditions governing their business relationship, NOW, THEREFORE, in consideration of the mutual covenants and agreements contained herein, the parties agree as follows:",
        
        # Rent amount (Indian context)
        "Tenant shall pay monthly rent of INR {amount} on or before the {day}th day of each calendar month by bank transfer to the Landlord's designated account. All payments shall be made in Indian Rupees, and Tenant shall bear any bank charges or transaction fees.",
        "The monthly rent for the premises shall be INR {amount}, payable in advance on the first day of each month by bank transfer, cheque, or demand draft, as agreed between the parties.",
        
        # Maintenance (Indian Rental)
        "Tenant is responsible for routine upkeep and minor repairs (e.g., light bulbs, faucets, minor plumbing). Landlord will be responsible for major structural, electrical, and plumbing repairs unless damage is caused by Tenant's negligence, misuse, or breach of this Agreement.",
        
        # Utilities (Indian context)
        "Tenant shall be responsible for payment of electricity, water, gas, internet, cable TV, and any other utilities unless otherwise stated in writing. Shared building services will be charged proportionally when applicable, and Tenant shall pay such charges along with the monthly rent.",
        
        # Insurance (Indian context)
        "Tenant shall maintain at their expense renter's insurance covering personal property and liability, with minimum liability coverage of INR {amount}. Landlord's insurance will not cover Tenant's personal belongings, and Tenant is advised to obtain appropriate insurance coverage.",
        
        # Guarantor (Indian context)
        "If required by the Landlord, the Tenant shall provide a guarantor who agrees to be jointly and severally liable for all Tenant obligations under this Agreement. The guarantor must be a resident Indian citizen with sufficient financial means, as determined by Landlord.",
        
        # Force majeure (standard - Indian context)
        "Neither party shall be liable for delays or failures to perform due to events beyond their reasonable control, including natural disasters, government actions, pandemics, war, terrorism, or acts of God, provided that the affected party gives prompt notice to the other party.",
        
        # Confidentiality (standard - Indian context)
        "Both parties agree to keep the terms and conditions of this Agreement confidential and not disclose them to third parties except as required by law, court order, or with prior written consent of the other party, in accordance with applicable Indian laws.",
        
        # Standard clauses (Indian context)
        "This Agreement shall be governed by and construed in accordance with the laws of India, without regard to its conflict of law principles. The courts in {city}, {state}, India shall have jurisdiction over any disputes arising out of or in connection with this Agreement.",
        "This Agreement may be executed in counterparts, each of which shall be deemed an original, but all of which together shall constitute one and the same instrument. This Agreement may be executed and delivered by facsimile, email, or electronic signature, which shall be valid and binding.",
        "The headings in this Agreement are for convenience only and shall not affect the interpretation of this Agreement. Any reference to 'days' shall mean calendar days unless otherwise specified.",
        "This Agreement constitutes the entire agreement between the parties with respect to the subject matter hereof and supersedes all prior agreements, understandings, negotiations, and discussions, whether oral or written, relating to the subject matter of this Agreement.",
    ]
    
    # Fill placeholders and create clauses
    cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune", "Ahmedabad", "Jaipur", "Kanpur", "Surat", "Lucknow"]
    states = ["Maharashtra", "Delhi", "Karnataka", "Tamil Nadu", "West Bengal", "Telangana", "Gujarat", "Rajasthan", "Uttar Pradesh"]
    addresses = [
        "123 MG Road, {city}, {state} 400001",
        "456 Commercial Street, {city}, {state} 500001",
        "789 Business Park, {city}, {state} 600001",
    ]
    
    # Process HIGH risk
    for template in high_risk_indian:
        for _ in range(15):  # Generate 15 variations
            try:
                clause = template.format(
                    city=random.choice(cities),
                    state=random.choice(states),
                    amount=random.choice([500000, 1000000, 2000000, 5000000]),
                )
                clauses_data.append({"clause_text": clause, "label": "HIGH"})
            except KeyError:
                clauses_data.append({"clause_text": template, "label": "HIGH"})
    
    # Process MEDIUM risk
    for template in medium_risk_indian:
        for _ in range(20):  # Generate 20 variations
            try:
                clause = template.format(
                    months=random.choice([1, 2, 3]),
                    days=random.choice([30, 45, 60, 90]),
                    day=random.choice([5, 10, 15]),
                    percent=random.choice([2, 3, 5, 10]),
                    cap=random.choice([10, 15, 20]),
                    amount=random.choice([10000, 15000, 20000, 25000, 30000, 50000]),
                    years=random.choice([1, 2, 3, 5]),
                )
                clauses_data.append({"clause_text": clause, "label": "MEDIUM"})
            except KeyError:
                clauses_data.append({"clause_text": template, "label": "MEDIUM"})
    
    # Process LOW risk
    parties = [
        ("Mr. Rajesh Kumar", "Mr. Amit Singh", "company", "company", "landlord", "tenant"),
        ("Ms. Priya Sharma", "Ms. Anjali Patel", "LLP", "LLP", "landlord", "tenant"),
        ("ABC Properties Pvt. Ltd.", "XYZ Corporation", "corporation", "corporation", "landlord", "tenant"),
        ("ABC Technologies Pvt. Ltd.", "Mr. Rohit Verma", "company", "individual", "employer", "employee"),
    ]
    
    for template in low_risk_indian:
        for party1, party2, entity1, entity2, name1, name2 in parties:
            for _ in range(8):  # Generate 8 variations
                try:
                    clause = template.format(
                        day=random.randint(1, 28),
                        month=random.choice(["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]),
                        year=random.randint(2020, 2024),
                        city=random.choice(cities),
                        state=random.choice(states),
                        address=random.choice(addresses).format(city=random.choice(cities), state=random.choice(states)),
                        landlord=party1,
                        tenant=party2,
                        company=party1,
                        employee=party2,
                        client=party1,
                        service_provider=party2,
                        entity_type=random.choice(["company", "LLP", "partnership", "proprietorship"]),
                        amount=random.choice([10000, 15000, 20000, 25000, 30000, 50000]),
                    )
                    clauses_data.append({"clause_text": clause, "label": "LOW"})
                except KeyError:
                    clauses_data.append({"clause_text": template, "label": "LOW"})
    
    print(f"   Generated {len(clauses_data)} Indian legal clauses")
    return clauses_data


def get_international_legal_clauses() -> List[Dict[str, str]]:
    """Get international legal document clauses."""
    print("Generating international legal document clauses...")
    
    clauses_data = []
    
    # Add international patterns (similar structure but with international context)
    # This would include US, UK, EU, etc. legal patterns
    # For brevity, using similar templates but with international context
    
    international_high = [
        "Provider reserves the right, in its sole discretion, to modify, suspend, or discontinue the Services at any time, with or without notice, and without liability to Customer.",
        "This Agreement will automatically renew for additional periods unless either party gives notice of non-renewal at least 30 days before the end of the term.",
        "Customer shall indemnify Provider from all claims, including those arising from Provider's own negligence, without limitation.",
    ]
    
    for clause in international_high:
        for _ in range(10):
            clauses_data.append({"clause_text": clause, "label": "HIGH"})
    
    print(f"   Generated {len(clauses_data)} international legal clauses")
    return clauses_data


def process_real_documents_enhanced(doc_dir: Path) -> List[Dict[str, str]]:
    """Process real PDF, DOCX, TXT files with enhanced extraction."""
    clauses_data = []
    
    if not doc_dir.exists():
        print(f"   Directory {doc_dir} does not exist. Skipping real document processing.")
        return clauses_data
    
    if not EXTRACTOR_AVAILABLE:
        print("   DocumentExtractor not available. Skipping real document processing.")
        return clauses_data
    
    extractor = DocumentExtractor()
    analyzer = RuleBasedAnalyzer() if EXTRACTOR_AVAILABLE else None
    
    # Find all document files
    pdf_files = list(doc_dir.glob("**/*.pdf"))
    docx_files = list(doc_dir.glob("**/*.docx")) + list(doc_dir.glob("**/*.doc"))
    txt_files = list(doc_dir.glob("**/*.txt"))
    
    all_files = pdf_files + docx_files + txt_files
    
    print(f"   Found {len(all_files)} document files")
    
    for file_path in all_files[:100]:  # Process up to 100 files
        try:
            print(f"   Processing: {file_path.name}")
            text = extractor.extract_text(str(file_path))
            clauses = extractor.segment_clauses(text)
            
            # Classify each clause
            for clause in clauses:
                if len(clause.strip()) < 30:
                    continue
                
                if analyzer:
                    try:
                        results = analyzer.analyze_clauses([clause])
                        if results:
                            label = results[0]["risk_label"]
                            clauses_data.append({"clause_text": clause, "label": label})
                    except:
                        # Fallback to default
                        clauses_data.append({"clause_text": clause, "label": "LOW"})
                else:
                    clauses_data.append({"clause_text": clause, "label": "LOW"})
                    
        except Exception as e:
            print(f"   Error processing {file_path.name}: {e}")
            continue
    
    print(f"   Processed {len(clauses_data)} clauses from real documents")
    return clauses_data


def create_enhanced_legal_dataset(num_samples: int = 20000) -> pd.DataFrame:
    """Create enhanced training dataset with extensive legal data."""
    print(f"Creating enhanced legal training dataset with {num_samples} samples...")
    print("=" * 70)
    
    all_clauses_data = []
    
    # 1. Get extensive Indian legal clauses
    print("\n[1/5] Generating extensive Indian legal clauses...")
    indian_clauses = get_extensive_indian_legal_clauses()
    all_clauses_data.extend(indian_clauses)
    print(f"   Total: {len(indian_clauses)} clauses")
    
    # 2. Get international legal clauses
    print("\n[2/5] Generating international legal clauses...")
    international_clauses = get_international_legal_clauses()
    all_clauses_data.extend(international_clauses)
    print(f"   Total: {len(international_clauses)} clauses")
    
    # 3. Process real documents if available
    print("\n[3/5] Processing real documents (if available)...")
    real_docs_dir = Path(__file__).parent / "real_documents"
    real_clauses = process_real_documents_enhanced(real_docs_dir)
    all_clauses_data.extend(real_clauses)
    print(f"   Total: {len(real_clauses)} clauses from real documents")
    
    # 4. Create DataFrame
    print("\n[4/5] Creating dataset...")
    df = pd.DataFrame(all_clauses_data)
    
    if len(df) == 0:
        raise ValueError("No clauses generated! Check your data sources.")
    
    # Remove duplicates
    initial_count = len(df)
    df = df.drop_duplicates(subset=["clause_text"], keep="first")
    duplicates_removed = initial_count - len(df)
    if duplicates_removed > 0:
        print(f"   Removed {duplicates_removed} duplicate clauses")
    
    # 5. Balance dataset with emphasis on HIGH and MEDIUM
    print("\n[5/5] Balancing dataset with emphasis on HIGH and MEDIUM risk...")
    label_counts = df["label"].value_counts()
    print(f"   Initial distribution: {dict(label_counts)}")
    
    # Target: 50% LOW, 30% MEDIUM, 20% HIGH (balanced for better accuracy)
    target_low = int(num_samples * 0.5)
    target_medium = int(num_samples * 0.3)
    target_high = int(num_samples * 0.2)
    
    balanced_data = []
    
    for label, target_count in [("HIGH", target_high), ("MEDIUM", target_medium), ("LOW", target_low)]:
        label_df = df[df["label"] == label]
        if len(label_df) > 0:
            sample_size = min(target_count, len(label_df))
            if sample_size > 0:
                sampled = label_df.sample(n=sample_size, replace=True if len(label_df) < sample_size else False, random_state=42)
                balanced_data.append(sampled)
                print(f"   {label}: {len(sampled)} samples")
        else:
            print(f"   WARNING: No {label} samples found!")
    
    if not balanced_data:
        raise ValueError("No balanced data created! Check your clause generation.")
    
    final_df = pd.concat(balanced_data, ignore_index=True)
    final_df = final_df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    # Add more if needed
    while len(final_df) < num_samples:
        sample = final_df.sample(n=1, random_state=42).iloc[0]
        final_df = pd.concat([final_df, pd.DataFrame([sample])], ignore_index=True)
    
    final_df = final_df.head(num_samples)
    
    print(f"\n[SUCCESS] Created dataset with {len(final_df)} samples")
    print(f"\nFinal label distribution:")
    print(final_df["label"].value_counts())
    print(f"\nPercentage distribution:")
    for label in ["LOW", "MEDIUM", "HIGH"]:
        count = len(final_df[final_df["label"] == label])
        pct = (count / len(final_df)) * 100
        print(f"   {label}: {pct:.1f}%")
    
    return final_df


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Create enhanced legal training dataset")
    parser.add_argument("--output", type=str, default="enhanced_legal_dataset.csv",
                       help="Output CSV file path")
    parser.add_argument("--samples", type=int, default=20000,
                       help="Number of samples to generate (default: 20000)")
    
    args = parser.parse_args()
    
    # Create dataset
    df = create_enhanced_legal_dataset(num_samples=args.samples)
    
    # Save to CSV
    output_path = Path(__file__).parent / args.output
    df.to_csv(output_path, index=False, encoding='utf-8')
    print(f"\n[SUCCESS] Saved to {output_path}")
    print(f"\n[INFO] File size: {output_path.stat().st_size / (1024*1024):.2f} MB")
    print(f"\n[INFO] Next step: Train the model")
    print(f"   cd backend")
    print(f"   .\\venv\\Scripts\\Activate.ps1")
    print(f"   python -m app.ml.train --data ../ml_data/{args.output} --output ./models/risk_classifier --epochs 5 --batch-size 16")

