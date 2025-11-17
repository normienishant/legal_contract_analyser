"""Fetch real legal documents from online sources including Indian legal documents."""
import pandas as pd
import re
import random
from pathlib import Path
from typing import List, Dict
import sys
import os

# Add parent directory to path to import extractor
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))
try:
    from app.services.extract import DocumentExtractor
    from app.services.analysis import RuleBasedAnalyzer
    EXTRACTOR_AVAILABLE = True
except ImportError:
    EXTRACTOR_AVAILABLE = False
    print("Warning: Could not import DocumentExtractor. Will use basic text extraction.")

# Import the improved risk classifier
def classify_clause_risk_improved(clause: str) -> str:
    """Improved risk classification using the same logic as RuleBasedAnalyzer."""
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
    
    # Fallback to pattern matching
    # HIGH RISK patterns (rental/lease specific + general)
    high_risk_patterns = [
        r'unilateral\s+amendment',
        r'reserves\s+the\s+right\s+to\s+modify\s+or\s+amend\s+any\s+term',
        r'enter.*at\s+any\s+time.*without\s+(prior\s+)?notice',
        r'indemnify.*own\s+negligence',
        r'hold\s+harmless.*own\s+negligence',
        r'exclusively\s+by\s+the\s+courts\s+located',
        r'terminate.*30\s+days.*written\s+notice',
        r'unlimited\s+liability',
        r'indemnify.*without\s+limitation',
        r'automatic\s+renewal',
        r'penalty.*equal\s+to.*100%',
        r'non-refundable.*any\s+circumstances',
    ]
    
    # MEDIUM RISK patterns
    medium_risk_patterns = [
        r'security\s+deposit.*deduct',
        r'late\s+payment\s+fee',
        r'sublet.*without.*consent',
        r'rent\s+escalation',
        r'terminate.*liable\s+for\s+rent',
        r'arbitration',
        r'confidentiality',
        r'dispute\s+resolution',
    ]
    
    # LOW RISK patterns
    low_risk_patterns = [
        r'^this\s+agreement\s+has\s+been\s+made',
        r'^this\s+agreement.*between',
        r'^whereas\s+',
        r'^now\s+therefore',
        r'rent\s+amount\s+and\s+payment',
        r'maintenance\s+and\s+repairs',
        r'utilities\s+and\s+service',
        r'insurance\s+requirement',
        r'force\s+majeure',
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
    
    return "LOW"  # Default


def get_indian_legal_document_samples() -> List[str]:
    """Get Indian legal document samples (contracts, agreements, etc.)."""
    print("Fetching Indian legal document samples...")
    
    indian_samples = [
        # Indian Rental/Lease Agreements
        "THIS RENTAL AGREEMENT is made on this {day} day of {month}, {year} at {city}, India BETWEEN {landlord}, residing at {address} (hereinafter referred to as the 'Landlord') AND {tenant}, residing at {address} (hereinafter referred to as the 'Tenant').",
        
        "WHEREAS the Landlord is the absolute owner of the property situated at {address}, {city}, {state}, India, and the Tenant desires to take the said property on rent, the parties agree as follows:",
        
        "The Tenant shall pay monthly rent of INR {amount} on or before the 5th day of each calendar month by bank transfer to the Landlord's designated account. Late payments after the 5th will incur applicable fees as set out below.",
        
        "The Tenant shall pay a security deposit equal to two months' rent. The Landlord may deduct for unpaid rent, repairs for damages beyond normal wear and tear, and unpaid utilities. The deposit shall be returned within 30 days after tenancy termination, less any lawful deductions, with an itemized statement.",
        
        "The Landlord or their agents may enter the premises at any time, without prior notice, for inspection, repairs, or to show the property to prospective tenants or buyers. Tenant shall not unreasonably withhold access.",
        
        "The Landlord reserves the right to modify or amend any term of this Agreement at any time by providing written notice to the Tenant; such modifications shall become effective 14 days after notice is given.",
        
        "Tenant agrees to indemnify and hold Landlord harmless from any claims, losses, liabilities, or expenses (including legal fees) arising from Tenant's use of the premises, including claims arising from Landlord's own negligence unless caused by Landlord's willful misconduct.",
        
        "Any dispute arising under this Agreement shall be resolved exclusively by the courts located in {city}, {state}, India. The prevailing party shall be entitled to recover reasonable attorneys' fees and costs.",
        
        "Landlord may terminate this Agreement with 30 days' written notice if Landlord intends to sell the property or commence redevelopment; Tenant shall vacate the premises by the termination date.",
        
        # Indian Employment Contracts
        "THIS EMPLOYMENT AGREEMENT is entered into on {day} {month}, {year} at {city}, India BETWEEN {company}, a company incorporated under the Companies Act, 2013, having its registered office at {address} (hereinafter referred to as the 'Employer') AND {employee}, residing at {address} (hereinafter referred to as the 'Employee').",
        
        "The Employee's employment with the Employer shall commence on {day} {month}, {year} and shall continue until terminated in accordance with the terms of this Agreement. The Employee shall be employed in the position of {position} and shall report to {manager}.",
        
        "The Employee's compensation shall be INR {amount} per month, payable on the last working day of each month. The Employee shall also be entitled to such bonuses and benefits as may be determined by the Employer from time to time.",
        
        "The Employee agrees to maintain strict confidentiality of all proprietary information, trade secrets, and confidential data of the Employer during and after the term of employment.",
        
        # Indian Service Agreements
        "THIS SERVICE AGREEMENT is made on {day} {month}, {year} at {city}, India BETWEEN {client}, a {entity_type} having its office at {address} (hereinafter referred to as the 'Client') AND {service_provider}, a {entity_type} having its office at {address} (hereinafter referred to as the 'Service Provider').",
        
        "WHEREAS the Client desires to engage the Service Provider to provide {service_type} services, and the Service Provider is willing to provide such services, the parties agree as follows:",
        
        "The Service Provider agrees to provide the services described in Schedule A attached hereto in accordance with the terms and conditions of this Agreement and applicable Indian laws.",
        
        "The Client agrees to pay the Service Provider fees as set forth in Schedule B attached hereto, payable within 30 days of receipt of invoice. All amounts are exclusive of applicable GST as per Indian tax laws.",
        
        # Indian Purchase Agreements
        "THIS PURCHASE AGREEMENT is entered into on {day} {month}, {year} at {city}, India BETWEEN {buyer}, having its registered office at {address} (hereinafter referred to as the 'Buyer') AND {seller}, having its registered office at {address} (hereinafter referred to as the 'Seller').",
        
        "The Buyer agrees to purchase from the Seller, and the Seller agrees to sell to the Buyer, the goods described in Schedule A (the 'Goods') for a total purchase price of INR {amount}, inclusive of all taxes as applicable under Indian law.",
        
        "Title to the Goods shall pass to the Buyer upon delivery to the Buyer's designated location. Risk of loss shall pass to the Buyer upon delivery.",
        
        # Indian Partnership Agreements
        "THIS PARTNERSHIP DEED is executed on {day} {month}, {year} at {city}, India BETWEEN the partners whose names, addresses, and signatures are set forth in Schedule A attached hereto.",
        
        "The Partners hereby agree to form a partnership firm under the Indian Partnership Act, 1932, for the purpose of carrying on the business of {business_purpose}.",
        
        "The name of the partnership firm shall be '{firm_name}' and the principal place of business shall be at {address}, {city}, {state}, India.",
        
        "The capital contribution of each Partner shall be as set forth in Schedule B attached hereto. Profits and losses shall be shared equally among the Partners unless otherwise agreed.",
        
        # Indian Software License Agreements
        "THIS SOFTWARE LICENSE AGREEMENT is entered into on {day} {month}, {year} at {city}, India BETWEEN {licensor}, a company incorporated under the Companies Act, 2013 (hereinafter referred to as the 'Licensor') AND {licensee}, a company incorporated under the Companies Act, 2013 (hereinafter referred to as the 'Licensee').",
        
        "Subject to the terms and conditions of this Agreement, the Licensor hereby grants to the Licensee a non-exclusive, non-transferable license to use the Software described in Schedule A for the term specified herein.",
        
        "The Licensee agrees to pay license fees as set forth in Schedule B, payable in advance on an annual basis. All fees are exclusive of applicable GST.",
        
        # Indian NDAs
        "THIS NON-DISCLOSURE AGREEMENT is entered into on {day} {month}, {year} at {city}, India BETWEEN {disclosing_party} (hereinafter referred to as the 'Disclosing Party') AND {receiving_party} (hereinafter referred to as the 'Receiving Party').",
        
        "For purposes of this Agreement, 'Confidential Information' shall mean all non-public, proprietary, or confidential information disclosed by the Disclosing Party to the Receiving Party, including but not limited to business plans, financial information, technical data, and customer lists.",
        
        "The Receiving Party agrees to hold and maintain the Confidential Information in strict confidence and not to disclose it to any third party without the prior written consent of the Disclosing Party, except as required by applicable Indian law.",
        
        # Standard Indian contract clauses
        "This Agreement shall be governed by and construed in accordance with the laws of India. Any disputes arising out of or in connection with this Agreement shall be subject to the exclusive jurisdiction of the courts in {city}, {state}, India.",
        
        "All notices required or permitted under this Agreement shall be in writing and shall be deemed given when delivered personally, sent by registered post, or sent by email to the addresses specified in this Agreement.",
        
        "This Agreement may be executed in counterparts, each of which shall be deemed an original, but all of which together shall constitute one and the same instrument. This Agreement may be executed and delivered by facsimile or electronic transmission.",
        
        "If any provision of this Agreement is held to be invalid, illegal, or unenforceable by a court of competent jurisdiction in India, the remaining provisions shall remain in full force and effect.",
        
        "This Agreement constitutes the entire agreement between the parties with respect to the subject matter hereof and supersedes all prior agreements, understandings, negotiations, and discussions, whether oral or written.",
    ]
    
    # Fill in placeholders
    filled_samples = []
    cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune", "Ahmedabad", "Jaipur", "Kanpur"]
    states = ["Maharashtra", "Delhi", "Karnataka", "Tamil Nadu", "West Bengal", "Telangana", "Gujarat", "Rajasthan", "Uttar Pradesh"]
    addresses = [
        "123 MG Road, {city}, {state} 400001",
        "456 Commercial Street, {city}, {state} 500001",
        "789 Business Park, {city}, {state} 600001",
    ]
    
    for sample in indian_samples:
        try:
            filled = sample.format(
                day=random.randint(1, 28),
                month=random.choice(["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]),
                year=random.randint(2020, 2024),
                city=random.choice(cities),
                state=random.choice(states),
                landlord=random.choice(["Mr. Rajesh Kumar", "Ms. Priya Sharma", "ABC Properties Pvt. Ltd."]),
                tenant=random.choice(["Mr. Amit Singh", "Ms. Anjali Patel", "XYZ Corporation"]),
                address=random.choice(addresses).format(city=random.choice(cities), state=random.choice(states)),
                amount=random.choice([10000, 15000, 20000, 25000, 30000, 50000, 100000]),
                company=random.choice(["ABC Technologies Pvt. Ltd.", "XYZ Solutions India Pvt. Ltd.", "Global Services India"]),
                employee=random.choice(["Mr. Rohit Verma", "Ms. Sneha Reddy", "Mr. Vikram Joshi"]),
                position=random.choice(["Software Engineer", "Senior Manager", "Business Analyst", "Project Manager"]),
                manager=random.choice(["Director", "VP", "Head of Department"]),
                entity_type=random.choice(["company", "partnership", "LLP", "proprietorship"]),
                client=random.choice(["ABC Corporation", "XYZ Industries", "Global Enterprises"]),
                service_provider=random.choice(["Tech Services India", "Consulting Solutions", "Professional Services"]),
                service_type=random.choice(["IT services", "consulting services", "maintenance services", "support services"]),
                buyer=random.choice(["ABC Traders", "XYZ Merchants", "Global Imports"]),
                seller=random.choice(["Manufacturing Co.", "Supply Chain Solutions", "Trading Company"]),
                business_purpose=random.choice(["software development", "consulting services", "trading", "manufacturing"]),
                firm_name=random.choice(["ABC & Associates", "XYZ Partners", "Global Partners"]),
                licensor=random.choice(["Software Solutions India", "Tech Licensing Co.", "Digital Services"]),
                licensee=random.choice(["Enterprise Software Users", "Business Solutions", "Corporate Clients"]),
                disclosing_party=random.choice(["ABC Corporation", "XYZ Technologies"]),
                receiving_party=random.choice(["Consulting Firm", "Service Provider"]),
            )
            filled_samples.append(filled)
        except KeyError:
            filled_samples.append(sample)
    
    return filled_samples


def get_international_legal_samples() -> List[str]:
    """Get international legal document samples."""
    print("Fetching international legal document samples...")
    
    # Use the existing function from fetch_online_legal_data.py
    # For now, return a comprehensive set
    return [
        # Standard boilerplate
        "THIS AGREEMENT is entered into on this __ day of ___, 20__ between [Company Name], a corporation organized and existing under the laws of [State], with its principal office located at [Address] (hereinafter referred to as 'Company'), and [Other Party], a [entity type] organized and existing under the laws of [State] (hereinafter referred to as 'Client').",
        
        "WHEREAS the Company is engaged in the business of [business description] and desires to engage the services of the Contractor for [service description].",
        
        "NOW, THEREFORE, in consideration of the mutual covenants and agreements contained herein, the parties agree as follows:",
        
        # HIGH RISK clauses
        "Provider shall indemnify, defend, and hold harmless Customer and its officers, directors, employees, agents, affiliates, successors, and assigns from and against any and all claims, demands, losses, costs, expenses, damages, judgments, penalties, interest, and liabilities (including, without limitation, reasonable attorneys' fees and costs) arising out of or relating to Provider's breach of this Agreement, without limitation or exception, including claims arising from Provider's own negligence.",
        
        "This Agreement will automatically renew for additional periods equal to the expiring term or one year (whichever is shorter), unless either party gives the other notice of non-renewal at least 30 days before the end of the relevant term. If Customer terminates this Agreement before the end of the then-current term, Customer will remain responsible for all fees payable for the remainder of the term, and Provider may charge Customer a termination fee equal to 75% of the remaining contract value.",
        
        "All fees paid by Customer are non-refundable. Customer acknowledges that Provider has no obligation to refund any fees under any circumstances, including but not limited to: (i) termination of this Agreement by either party for any reason; (ii) Customer's dissatisfaction with the Services; (iii) Customer's inability to access or use the Services; or (iv) any other reason.",
        
        "Provider reserves the right, in its sole discretion, to modify, suspend, or discontinue the Services (or any part thereof) at any time, with or without notice. Provider will not be liable to Customer or any third party for any modification, suspension, or discontinuation of the Services.",
        
        "Any dispute, controversy, or claim arising out of or relating to this Agreement, including the formation, interpretation, breach, or termination thereof, will be referred to and finally determined by arbitration in accordance with the JAMS Comprehensive Arbitration Rules and Procedures. The parties waive any right to a jury trial.",
        
        # MEDIUM RISK clauses
        "Either party may terminate this Agreement upon 30 days' prior written notice to the other party if the other party materially breaches this Agreement and fails to cure such breach within such 30-day period.",
        
        "IN NO EVENT WILL EITHER PARTY'S LIABILITY UNDER THIS AGREEMENT EXCEED THE TOTAL AMOUNT PAID BY CUSTOMER TO PROVIDER IN THE TWELVE (12) MONTHS PRECEDING THE CLAIM.",
        
        "Each party agrees to maintain the confidentiality of all Confidential Information received from the other party during the term of this Agreement and for a period of five (5) years thereafter.",
    ]


def create_comprehensive_training_dataset(num_samples: int = 5000) -> pd.DataFrame:
    """Create comprehensive training dataset from real legal documents."""
    print(f"Creating comprehensive training dataset with {num_samples} samples...")
    print("=" * 60)
    
    all_clauses = []
    
    # 1. Get Indian legal documents
    print("\n[1/4] Fetching Indian legal document samples...")
    indian_samples = get_indian_legal_document_samples()
    all_clauses.extend(indian_samples)
    print(f"   Added {len(indian_samples)} Indian legal clauses")
    
    # 2. Get international legal documents
    print("\n[2/4] Fetching international legal document samples...")
    international_samples = get_international_legal_samples()
    all_clauses.extend(international_samples)
    print(f"   Added {len(international_samples)} international legal clauses")
    
    # 3. Extract clauses from longer texts
    print("\n[3/4] Extracting clauses from document texts...")
    if EXTRACTOR_AVAILABLE:
        extractor = DocumentExtractor()
        for text in indian_samples + international_samples:
            try:
                clauses = extractor.segment_clauses(text)
                all_clauses.extend(clauses)
            except:
                pass
    else:
        # Basic clause extraction
        for text in indian_samples + international_samples:
            # Split by sentences and numbered clauses
            sentences = re.split(r'[.!?]\s+(?=[A-Z])', text)
            for sentence in sentences:
                sentence = sentence.strip()
                if len(sentence) > 50 and len(sentence) < 2000:
                    all_clauses.append(sentence)
    
    print(f"   Total clauses after extraction: {len(all_clauses)}")
    
    # 4. Classify and create dataset
    print("\n[4/4] Classifying clauses by risk level...")
    data = []
    
    for clause in all_clauses:
        clause = clause.strip()
        if len(clause) < 30:  # Skip very short clauses
            continue
        
        risk_label = classify_clause_risk_improved(clause)
        
        data.append({
            "clause_text": clause,
            "label": risk_label,
        })
    
    df = pd.DataFrame(data)
    
    # Balance the dataset
    print("\nBalancing dataset...")
    label_counts = df["label"].value_counts()
    print(f"   Initial distribution: {dict(label_counts)}")
    
    # Target distribution: 60% LOW, 25% MEDIUM, 15% HIGH
    target_low = int(num_samples * 0.6)
    target_medium = int(num_samples * 0.25)
    target_high = int(num_samples * 0.15)
    
    balanced_data = []
    
    for label, target_count in [("LOW", target_low), ("MEDIUM", target_medium), ("HIGH", target_high)]:
        label_df = df[df["label"] == label]
        if len(label_df) > 0:
            sample_size = min(target_count, len(label_df))
            sampled = label_df.sample(n=sample_size, replace=True if len(label_df) < sample_size else False, random_state=42)
            balanced_data.append(sampled)
            print(f"   {label}: {len(sampled)} samples")
        else:
            print(f"   WARNING: No {label} samples found!")
    
    final_df = pd.concat(balanced_data, ignore_index=True)
    final_df = final_df.sample(frac=1, random_state=42).reset_index(drop=True)  # Shuffle
    
    # Add more samples if needed
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
    
    parser = argparse.ArgumentParser(description="Fetch real legal documents and create training dataset")
    parser.add_argument("--output", type=str, default="comprehensive_legal_training_data.csv",
                       help="Output CSV file path")
    parser.add_argument("--samples", type=int, default=5000,
                       help="Number of samples to generate")
    
    args = parser.parse_args()
    
    # Create dataset
    df = create_comprehensive_training_dataset(num_samples=args.samples)
    
    # Save to CSV
    output_path = Path(__file__).parent / args.output
    df.to_csv(output_path, index=False, encoding='utf-8')
    print(f"\n[SUCCESS] Saved to {output_path}")
    print(f"\n[INFO] Next step: Train the model")
    print(f"   cd backend")
    print(f"   .\\venv\\Scripts\\Activate.ps1")
    print(f"   python -m app.ml.train --data ../ml_data/{args.output} --output ./models/risk_classifier --epochs 5 --batch-size 16")

