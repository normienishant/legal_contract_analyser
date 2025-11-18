"""Create training dataset from real legal documents (PDF, DOCX, TXT)."""
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

# Improved risk classifier
def classify_clause_risk_improved(clause: str) -> str:
    """Improved risk classification matching the backend analyzer."""
    clause_lower = clause.lower()
    clause_clean = re.sub(r'\s+', ' ', clause_lower).strip()
    
    # Use RuleBasedAnalyzer if available
    if EXTRACTOR_AVAILABLE:
        try:
            analyzer = RuleBasedAnalyzer()
            results = analyzer.analyze_clauses([clause])
            if results:
                return results[0]["risk_label"]
        except:
            pass
    
    # HIGH RISK patterns (rental/lease + general)
    high_risk_patterns = [
        r'unilateral\s+amendment',
        r'reserves\s+the\s+right\s+to\s+modify\s+or\s+amend\s+any\s+term',
        r'landlord.*reserves.*right.*modify',
        r'enter.*at\s+any\s+time.*without\s+(prior\s+)?notice',
        r'right\s+of\s+entry.*without\s+notice',
        r'indemnify.*own\s+negligence',
        r'hold\s+harmless.*own\s+negligence',
        r'exclusively\s+by\s+the\s+courts\s+located',
        r'terminate.*30\s+days.*written\s+notice.*sale',
        r'vacate.*30\s+days',
        r'unlimited\s+liability',
        r'indemnify.*without\s+limitation',
        r'automatic\s+renewal',
        r'penalty.*equal\s+to.*100%',
        r'non-refundable.*any\s+circumstances',
        r'waiver.*jury\s+trial',
        r'termination\s+fee.*remaining\s+contract',
        r'penalty.*contract\s+value',
        r'shall\s+be\s+penalized',
        r'liquidated\s+damages.*100%',
    ]
    
    # MEDIUM RISK patterns
    medium_risk_patterns = [
        r'security\s+deposit.*deduct',
        r'deposit.*deduct.*damages',
        r'late\s+payment\s+fee',
        r'late\s+fee.*rent',
        r'sublet.*without.*prior\s+written\s+consent',
        r'assign.*without.*consent',
        r'rent\s+escalation',
        r'increase\s+rent.*annually',
        r'terminate.*liable\s+for\s+rent',
        r'early\s+termination.*liable',
        r'fixtures.*property\s+of\s+landlord',
        r'arbitration',
        r'confidentiality',
        r'dispute\s+resolution',
        r'governing\s+law',
        r'jurisdiction',
        r'force\s+majeure',
        r'termination.*30\s+days',
        r'breach.*remedy',
    ]
    
    # LOW RISK patterns
    low_risk_patterns = [
        r'^this\s+agreement\s+has\s+been\s+made',
        r'^this\s+agreement.*between',
        r'^whereas\s+',
        r'^now\s+therefore',
        r'rent\s+amount\s+and\s+payment',
        r'tenant\s+shall\s+pay\s+monthly\s+rent',
        r'maintenance\s+and\s+repairs',
        r'utilities\s+and\s+service',
        r'insurance\s+requirement',
        r'guarantor',
        r'force\s+majeure.*events\s+beyond',
        r'confidentiality.*keep.*terms',
    ]
    
    # Check HIGH first
    for pattern in high_risk_patterns:
        if re.search(pattern, clause_clean, re.IGNORECASE):
            return "HIGH"
    
    # Check LOW (boilerplate)
    for pattern in low_risk_patterns:
        if re.search(pattern, clause_clean, re.IGNORECASE):
            return "LOW"
    
    # Check MEDIUM
    for pattern in medium_risk_patterns:
        if re.search(pattern, clause_clean, re.IGNORECASE):
            return "MEDIUM"
    
    return "LOW"


def generate_high_risk_clauses() -> List[str]:
    """Generate HIGH risk clauses for training."""
    high_risk_templates = [
        # Unilateral Amendment
        "The Landlord reserves the right to modify or amend any term of this Agreement at any time by providing written notice to the Tenant; such modifications shall become effective {days} days after notice is given.",
        "The Company reserves the right, in its sole discretion, to modify, suspend, or discontinue the Services (or any part thereof) at any time, with or without notice, and without liability to Customer.",
        "Provider may unilaterally amend this Agreement at any time by posting the modified Agreement on its website. Customer's continued use constitutes acceptance.",
        
        # Entry without notice
        "The Landlord or their agents may enter the premises at any time, without prior notice, for inspection, repairs, or to show the property to prospective tenants or buyers.",
        "Landlord reserves the right to enter the premises without notice for any reason deemed necessary by Landlord in its sole discretion.",
        
        # Indemnification including own negligence
        "Tenant agrees to indemnify and hold Landlord harmless from any claims, losses, liabilities, or expenses (including legal fees) arising from Tenant's use of the premises, including claims arising from Landlord's own negligence unless caused by Landlord's willful misconduct.",
        "Customer shall indemnify, defend, and hold harmless Provider and its officers, directors, employees, agents, affiliates, successors, and assigns from and against any and all claims, demands, losses, costs, expenses, damages, judgments, penalties, interest, and liabilities (including, without limitation, reasonable attorneys' fees and costs) arising out of or relating to Customer's breach of this Agreement, without limitation or exception, including claims arising from Provider's own negligence.",
        "Provider shall be indemnified by Customer for all losses, including those resulting from Provider's own negligence, gross negligence, or willful misconduct.",
        
        # Distant/exclusive jurisdiction
        "Any dispute arising under this Agreement shall be resolved exclusively by the courts located in {distant_city}, {distant_state}. The prevailing party shall be entitled to recover reasonable attorneys' fees and costs.",
        "All disputes shall be subject to the exclusive jurisdiction of courts in {distant_city}, {distant_state}, regardless of where the parties are located.",
        
        # Short termination
        "Landlord may terminate this Agreement with {days} days' written notice if Landlord intends to sell the property or commence redevelopment; Tenant shall vacate the premises by the termination date.",
        "Either party may terminate this Agreement with {days} days' written notice, and Tenant must vacate immediately upon termination.",
        
        # Automatic renewal
        "This Agreement will automatically renew for additional periods equal to the expiring term or one year (whichever is shorter), unless either party gives the other notice of non-renewal at least 30 days before the end of the relevant term. If Customer terminates before the end of the term, Customer will remain responsible for all fees payable for the remainder of the term.",
        "This Agreement shall automatically renew for successive one-year periods unless either party provides written notice of termination at least 60 days prior to the expiration of the then-current term.",
        
        # Excessive penalties
        "In the event of any material breach of this Agreement by Customer, Customer shall pay to Provider, as liquidated damages and not as a penalty, an amount equal to the greater of: (a) 100% of the total fees payable under this Agreement, or (b) ${amount}.",
        "If Customer terminates this Agreement before the end of the then-current term, Customer will remain responsible for all fees payable for the remainder of the term, and Provider may charge Customer a termination fee equal to {percent}% of the remaining contract value.",
        
        # Non-refundable
        "All fees paid by Customer are non-refundable. Customer acknowledges that Provider has no obligation to refund any fees under any circumstances, including but not limited to: (i) termination of this Agreement by either party for any reason; (ii) Customer's dissatisfaction with the Services; (iii) Customer's inability to access or use the Services; or (iv) any other reason.",
        
        # Unlimited liability
        "Customer's liability to Provider for any claims, damages, losses, or expenses arising out of or relating to this Agreement or the Services, whether based on contract, tort (including negligence), strict liability, or any other legal theory, will be unlimited and will include, without limitation, direct, indirect, incidental, special, consequential, exemplary, and punitive damages.",
        
        # Waiver of rights
        "Customer hereby waives, to the fullest extent permitted by applicable law, any and all rights it may have against Provider, including without limitation: (a) the right to a trial by jury; (b) the right to participate in a class action lawsuit; (c) the right to seek punitive or exemplary damages; and (d) any other rights that may be available under applicable law.",
        
        # Binding arbitration
        "Any dispute, controversy, or claim arising out of or relating to this Agreement, including the formation, interpretation, breach, or termination thereof, will be referred to and finally determined by arbitration in accordance with the JAMS Comprehensive Arbitration Rules and Procedures. The parties waive any right to a jury trial.",
    ]
    
    clauses = []
    cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "New York", "Los Angeles", "London", "Singapore"]
    states = ["Maharashtra", "Delhi", "Karnataka", "Tamil Nadu", "West Bengal", "California", "New York", "England", "Singapore"]
    distant_cities = ["Mumbai", "Delhi", "New York", "London", "Singapore", "Dubai"]
    distant_states = ["Maharashtra", "Delhi", "New York", "England", "Singapore", "UAE"]
    
    for template in high_risk_templates:
        for _ in range(10):  # Generate 10 variations of each
            try:
                clause = template.format(
                    days=random.choice([14, 30, 45]),
                    distant_city=random.choice(distant_cities),
                    distant_state=random.choice(distant_states),
                    amount=random.choice([500000, 1000000, 2000000]),
                    percent=random.choice([75, 80, 90, 100]),
                )
                clauses.append(clause)
            except KeyError:
                clauses.append(template)
    
    return clauses


def generate_medium_risk_clauses() -> List[str]:
    """Generate MEDIUM risk clauses for training."""
    medium_risk_templates = [
        # Security deposit
        "Tenant shall pay a security deposit equal to {months} months' rent. Landlord may deduct for unpaid rent, repairs for damages beyond normal wear and tear, and unpaid utilities. The deposit shall be returned within {days} days after tenancy termination, less any lawful deductions, with an itemized statement.",
        "A security deposit of ${amount} shall be paid by Tenant upon execution of this Agreement. Landlord may apply the deposit to any unpaid rent, damages, or other charges owed by Tenant.",
        
        # Late payment fees
        "If rent is not received by the {day}th, Tenant shall pay a late fee equal to {percent}% of the monthly rent per week until payment is made, capped at {cap}% of the monthly rent.",
        "Late payments will bear interest at the rate of {percent}% per month or the maximum rate permitted by applicable law, whichever is less.",
        
        # Subletting restrictions
        "Tenant shall not sublet, assign, or transfer the premises or any part thereof without the prior written consent of the Landlord, which shall not be unreasonably withheld. Any unauthorized subletting shall constitute a breach of this Agreement.",
        "Customer may not assign, transfer, or delegate this Agreement or any of its rights or obligations hereunder without Provider's prior written consent, which may be withheld in Provider's sole discretion.",
        
        # Pet restrictions
        "No pets are permitted without the Landlord's prior written consent. If permitted, Tenant must pay a refundable pet deposit of {amount} and is responsible for any damage or nuisance caused by the pet.",
        
        # Alterations
        "Tenant shall not make any structural alterations, install fixtures, or make improvements without prior written consent of the Landlord. Any approved fixtures affixed by Tenant shall become the property of the Landlord at lease end unless otherwise agreed in writing.",
        
        # Termination with liability
        "Either party may terminate this Agreement with {days} days' written notice. If Tenant terminates before the lease term ends without Landlord's consent, Tenant shall be liable for rent until the premises are re-let or for {months} months' rent, whichever is lesser.",
        "If Customer terminates this Agreement before the end of the then-current term, Customer will be responsible for {percent}% of the remaining fees.",
        
        # Rent escalation
        "Landlord may increase rent annually by up to {percent}% or by the change in the Consumer Price Index (CPI), whichever is lower, upon providing {days} days' written notice prior to the effective increase.",
        
        # Fixtures
        "Tenant may not remove built-in fixtures, appliances, or cabinetry. Portable furniture or Tenant-installed appliances may be removed provided Tenant repairs any damage caused by removal.",
        
        # Arbitration
        "Any disputes arising under this Agreement will first be addressed through good faith negotiations between the parties. If such negotiations are unsuccessful within {days} days, the parties agree to submit the dispute to mediation before a mutually agreed mediator.",
        
        # Confidentiality
        "Each party agrees to maintain the confidentiality of all Confidential Information received from the other party during the term of this Agreement and for a period of {years} years thereafter.",
        
        # Liability limits
        "IN NO EVENT WILL EITHER PARTY'S LIABILITY UNDER THIS AGREEMENT EXCEED THE TOTAL AMOUNT PAID BY CUSTOMER TO PROVIDER IN THE TWELVE (12) MONTHS PRECEDING THE CLAIM.",
        "Provider's total liability for any claims arising out of or relating to this Agreement shall not exceed ${amount} or the amount paid by Customer in the {months} months preceding the claim, whichever is less.",
        
        # Force majeure
        "Neither party shall be liable for delays or failures to perform due to events beyond their reasonable control, including natural disasters, government actions, pandemics, war, terrorism, or acts of God.",
    ]
    
    clauses = []
    
    for template in medium_risk_templates:
        for _ in range(15):  # Generate 15 variations of each
            try:
                clause = template.format(
                    months=random.choice([1, 2, 3]),
                    days=random.choice([30, 45, 60, 90]),
                    day=random.choice([5, 10, 15]),
                    percent=random.choice([2, 3, 5, 10]),
                    cap=random.choice([10, 15, 20]),
                    amount=random.choice([500, 1000, 2000, 5000]),
                    years=random.choice([1, 2, 3, 5]),
                )
                clauses.append(clause)
            except KeyError:
                clauses.append(template)
    
    return clauses


def generate_low_risk_clauses() -> List[str]:
    """Generate LOW risk clauses for training."""
    low_risk_templates = [
        # Agreement headers
        "THIS AGREEMENT has been made on this {day} day of {month}, {year} at {city} BETWEEN {party1} (hereinafter referred to as the '{name1}') AND {party2} (hereinafter referred to as the '{name2}').",
        "THIS AGREEMENT is entered into on this {day} day of {month}, {year} between {party1}, a {entity1} organized under the laws of {state}, and {party2}, a {entity2} organized under the laws of {state}.",
        
        # Recitals
        "WHEREAS the {party1} is engaged in the business of {business} and desires to engage the services of the {party2}, the parties agree as follows:",
        "WHEREAS the parties desire to enter into this Agreement to set forth the terms and conditions governing their business relationship.",
        "NOW, THEREFORE, in consideration of the mutual covenants and agreements contained herein, the parties agree as follows:",
        
        # Rent amount
        "Tenant shall pay monthly rent of INR {amount} on or before the {day}th day of each calendar month by bank transfer to the Landlord's designated account.",
        "The monthly rent for the premises shall be ${amount}, payable in advance on the first day of each month.",
        
        # Maintenance
        "Tenant is responsible for routine upkeep and minor repairs (e.g., light bulbs, faucets). Landlord will be responsible for major structural, electrical, and plumbing repairs unless damage is caused by Tenant's negligence.",
        
        # Utilities
        "Tenant shall be responsible for payment of electricity, water, gas, internet, and any other utilities unless otherwise stated in writing. Shared building services will be charged proportionally when applicable.",
        
        # Insurance
        "Tenant shall maintain at their expense renter's insurance covering personal property and liability, with minimum liability coverage of INR {amount}. Landlord's insurance will not cover Tenant's personal belongings.",
        
        # Guarantor
        "If required by the Landlord, the Tenant shall provide a guarantor who agrees to be jointly and severally liable for all Tenant obligations under this Agreement.",
        
        # Force majeure
        "Neither party shall be liable for delays or failures to perform due to events beyond their reasonable control, including natural disasters, government actions, or pandemics.",
        
        # Confidentiality (standard)
        "Both parties agree to keep the terms and conditions of this Agreement confidential and not disclose them to third parties except as required by law or with prior written consent.",
        
        # Standard clauses
        "This Agreement shall be governed by and construed in accordance with the laws of {state}.",
        "This Agreement may be executed in counterparts, each of which shall be deemed an original, but all of which together shall constitute one and the same instrument.",
        "The headings in this Agreement are for convenience only and shall not affect the interpretation of this Agreement.",
        "This Agreement constitutes the entire agreement between the parties with respect to the subject matter hereof and supersedes all prior agreements, understandings, negotiations, and discussions, whether oral or written.",
    ]
    
    clauses = []
    parties = [
        ("Company", "Customer", "corporation", "partnership", "company", "customer"),
        ("Landlord", "Tenant", "individual", "individual", "landlord", "tenant"),
        ("Employer", "Employee", "corporation", "individual", "employer", "employee"),
        ("Client", "Service Provider", "corporation", "LLC", "client", "service_provider"),
    ]
    cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "New York", "London"]
    states = ["Maharashtra", "Delhi", "Karnataka", "Tamil Nadu", "California", "New York"]
    businesses = ["software development", "consulting services", "real estate", "technology services"]
    
    for template in low_risk_templates:
        for party1, party2, entity1, entity2, name1, name2 in parties:
            for _ in range(5):  # Generate 5 variations
                try:
                    clause = template.format(
                        day=random.randint(1, 28),
                        month=random.choice(["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]),
                        year=random.randint(2020, 2024),
                        city=random.choice(cities),
                        state=random.choice(states),
                        party1=party1,
                        party2=party2,
                        entity1=entity1,
                        entity2=entity2,
                        name1=name1,
                        name2=name2,
                        business=random.choice(businesses),
                        amount=random.choice([10000, 15000, 20000, 25000, 30000]),
                    )
                    clauses.append(clause)
                except KeyError:
                    clauses.append(template)
    
    return clauses


def process_real_documents(doc_dir: Path) -> List[str]:
    """Process real PDF, DOCX, TXT files from a directory."""
    all_clauses = []
    
    if not doc_dir.exists():
        print(f"   Directory {doc_dir} does not exist. Skipping real document processing.")
        return all_clauses
    
    if not EXTRACTOR_AVAILABLE:
        print("   DocumentExtractor not available. Skipping real document processing.")
        return all_clauses
    
    extractor = DocumentExtractor()
    
    # Find all document files
    pdf_files = list(doc_dir.glob("**/*.pdf"))
    docx_files = list(doc_dir.glob("**/*.docx")) + list(doc_dir.glob("**/*.doc"))
    txt_files = list(doc_dir.glob("**/*.txt"))
    
    all_files = pdf_files + docx_files + txt_files
    
    print(f"   Found {len(all_files)} document files")
    
    for file_path in all_files[:50]:  # Limit to 50 files to avoid too much processing
        try:
            print(f"   Processing: {file_path.name}")
            text = extractor.extract_text(str(file_path))
            clauses = extractor.segment_clauses(text)
            all_clauses.extend(clauses)
        except Exception as e:
            print(f"   Error processing {file_path.name}: {e}")
            continue
    
    return all_clauses


def create_large_training_dataset(num_samples: int = 10000) -> pd.DataFrame:
    """Create large training dataset with emphasis on HIGH and MEDIUM risk."""
    print(f"Creating large training dataset with {num_samples} samples...")
    print("=" * 70)
    
    all_clauses = []
    
    # 1. Generate HIGH risk clauses (more samples)
    print("\n[1/5] Generating HIGH risk clauses...")
    high_clauses = generate_high_risk_clauses()
    all_clauses.extend(high_clauses)
    print(f"   Generated {len(high_clauses)} HIGH risk clauses")
    
    # 2. Generate MEDIUM risk clauses (more samples)
    print("\n[2/5] Generating MEDIUM risk clauses...")
    medium_clauses = generate_medium_risk_clauses()
    all_clauses.extend(medium_clauses)
    print(f"   Generated {len(medium_clauses)} MEDIUM risk clauses")
    
    # 3. Generate LOW risk clauses
    print("\n[3/5] Generating LOW risk clauses...")
    low_clauses = generate_low_risk_clauses()
    all_clauses.extend(low_clauses)
    print(f"   Generated {len(low_clauses)} LOW risk clauses")
    
    # 4. Process real documents if available
    print("\n[4/5] Processing real documents (if available)...")
    real_docs_dir = Path(__file__).parent / "real_documents"
    real_clauses = process_real_documents(real_docs_dir)
    all_clauses.extend(real_clauses)
    print(f"   Processed {len(real_clauses)} clauses from real documents")
    
    # 5. Classify all clauses
    print("\n[5/5] Classifying all clauses...")
    data = []
    
    for clause in all_clauses:
        clause = clause.strip()
        if len(clause) < 30:
            continue
        
        risk_label = classify_clause_risk_improved(clause)
        
        data.append({
            "clause_text": clause,
            "label": risk_label,
        })
    
    df = pd.DataFrame(data)
    
    # Balance with emphasis on HIGH and MEDIUM
    print("\nBalancing dataset with emphasis on HIGH and MEDIUM risk...")
    label_counts = df["label"].value_counts()
    print(f"   Initial distribution: {dict(label_counts)}")
    
    # Target: 50% LOW, 30% MEDIUM, 20% HIGH (more balanced for better accuracy)
    target_low = int(num_samples * 0.5)
    target_medium = int(num_samples * 0.3)
    target_high = int(num_samples * 0.2)
    
    balanced_data = []
    
    for label, target_count in [("HIGH", target_high), ("MEDIUM", target_medium), ("LOW", target_low)]:
        label_df = df[df["label"] == label]
        if len(label_df) > 0:
            sample_size = min(target_count, len(label_df))
            sampled = label_df.sample(n=sample_size, replace=True if len(label_df) < sample_size else False, random_state=42)
            balanced_data.append(sampled)
            print(f"   {label}: {len(sampled)} samples")
        else:
            print(f"   WARNING: No {label} samples found!")
    
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
    
    parser = argparse.ArgumentParser(description="Create large training dataset from real documents")
    parser.add_argument("--output", type=str, default="large_real_legal_dataset.csv",
                       help="Output CSV file path")
    parser.add_argument("--samples", type=int, default=10000,
                       help="Number of samples to generate")
    
    args = parser.parse_args()
    
    # Create dataset
    df = create_large_training_dataset(num_samples=args.samples)
    
    # Save to CSV
    output_path = Path(__file__).parent / args.output
    df.to_csv(output_path, index=False, encoding='utf-8')
    print(f"\n[SUCCESS] Saved to {output_path}")
    print(f"\n[INFO] Next step: Train the model")
    print(f"   cd backend")
    print(f"   .\\venv\\Scripts\\Activate.ps1")
    print(f"   python -m app.ml.train --data ../ml_data/{args.output} --output ./models/risk_classifier --epochs 5 --batch-size 16")

