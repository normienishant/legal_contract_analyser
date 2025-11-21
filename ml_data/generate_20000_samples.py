"""Generate 20000 training samples for model training."""
import pandas as pd
import random
import os

# Load existing production clauses
from generate_production_data import PRODUCTION_CLAUSES

def generate_variations(base_clause: str, num_variations: int = 5) -> list:
    """Generate variations of a clause."""
    variations = []
    
    # Template variables to replace
    replacements = {
        'Provider': ['Service Provider', 'Company', 'Vendor', 'Supplier', 'Contractor'],
        'Client': ['Customer', 'Buyer', 'User', 'Licensee', 'Purchaser'],
        'Agreement': ['Contract', 'Agreement', 'Terms', 'Service Agreement'],
        'Services': ['Services', 'Products', 'Deliverables', 'Work'],
        'INR': ['USD', 'EUR', 'INR', 'GBP'],
        '20000': ['10000', '20000', '50000', '100000', '200000'],
        '30 days': ['15 days', '30 days', '45 days', '60 days', '90 days'],
        '1 year': ['6 months', '1 year', '2 years', '3 years'],
    }
    
    for _ in range(num_variations):
        variation = base_clause
        for old, new_list in replacements.items():
            if old in variation:
                variation = variation.replace(old, random.choice(new_list), 1)
        variations.append(variation)
    
    return variations

def generate_20000_samples():
    """Generate 20000 training samples."""
    print("Generating 20000 training samples...")
    
    all_clauses = []
    
    # Generate from existing production clauses
    for risk_level, clauses in PRODUCTION_CLAUSES.items():
        for clause in clauses:
            # Add original
            all_clauses.append({
                'clause_text': clause,
                'label': risk_level
            })
            
            # Add variations
            variations = generate_variations(clause, num_variations=3)
            for var in variations:
                all_clauses.append({
                    'clause_text': var,
                    'label': risk_level
                })
    
    # Calculate how many more we need
    current_count = len(all_clauses)
    needed = 20000 - current_count
    
    print(f"Generated {current_count} samples from base clauses")
    print(f"Need {needed} more samples...")
    
    # Generate additional samples by combining patterns
    additional_patterns = {
        'HIGH': [
            "The {party1} shall be liable for all damages, losses, and expenses, without limitation, arising from {event}.",
            "This Agreement may be terminated by {party1} at any time, for any reason, without notice or liability.",
            "{party1} waives all rights to {right} and agrees that {party2} shall not be liable for any {damage_type}.",
            "All payments are non-refundable under any circumstances, including {circumstance1} or {circumstance2}.",
            "{party1} agrees to indemnify {party2} for all claims, without limitation, regardless of fault.",
        ],
        'MEDIUM': [
            "{party1} shall maintain {requirement} in accordance with {standard}.",
            "In the event of {event}, {party1} shall provide {notice_period} days written notice to {party2}.",
            "{party1}'s liability shall not exceed {amount} or {percentage}% of the contract value, whichever is less.",
            "This Agreement shall be governed by the laws of {jurisdiction}.",
            "{party1} agrees to maintain confidentiality of {information} for a period of {duration}.",
        ],
        'LOW': [
            "{party1} shall provide {service} in a professional and timely manner.",
            "Both parties agree to act in good faith and cooperate in {activity}.",
            "This Agreement may be amended by mutual written consent of both parties.",
            "{party1} shall comply with all applicable laws and regulations.",
            "The parties agree to resolve disputes through {method} before pursuing legal action.",
        ]
    }
    
    parties = ['Provider', 'Client', 'Company', 'Customer', 'Vendor', 'Buyer']
    events = ['breach', 'termination', 'default', 'non-performance', 'violation']
    rights = ['jury trial', 'class action', 'punitive damages', 'injunctive relief']
    damage_types = ['direct damages', 'indirect damages', 'consequential damages', 'lost profits']
    circumstances = ['termination', 'breach', 'dissatisfaction', 'force majeure']
    requirements = ['insurance', 'licenses', 'certifications', 'compliance']
    standards = ['industry standards', 'applicable laws', 'best practices']
    notice_periods = ['15', '30', '45', '60']
    amounts = ['INR 50000', 'USD 5000', 'EUR 4000']
    percentages = ['50', '100', '150']
    jurisdictions = ['Delaware', 'New York', 'California', 'India']
    information = ['Confidential Information', 'Proprietary Data', 'Trade Secrets']
    durations = ['1 year', '2 years', '3 years', '5 years']
    services = ['services', 'products', 'deliverables']
    activities = ['performing this Agreement', 'resolving disputes', 'completing the project']
    methods = ['good faith negotiation', 'mediation', 'arbitration']
    
    # Fill in templates
    for risk_level, templates in additional_patterns.items():
        samples_per_template = needed // (len(templates) * len(PRODUCTION_CLAUSES))
        for template in templates:
            for _ in range(samples_per_template):
                try:
                    clause = template.format(
                        party1=random.choice(parties),
                        party2=random.choice(parties),
                        event=random.choice(events),
                        right=random.choice(rights),
                        damage_type=random.choice(damage_types),
                        circumstance1=random.choice(circumstances),
                        circumstance2=random.choice(circumstances),
                        requirement=random.choice(requirements),
                        standard=random.choice(standards),
                        notice_period=random.choice(notice_periods),
                        amount=random.choice(amounts),
                        percentage=random.choice(percentages),
                        jurisdiction=random.choice(jurisdictions),
                        information=random.choice(information),
                        duration=random.choice(durations),
                        service=random.choice(services),
                        activity=random.choice(activities),
                        method=random.choice(methods),
                    )
                    all_clauses.append({
                        'clause_text': clause,
                        'label': risk_level
                    })
                except KeyError:
                    # Skip if template has issues
                    continue
    
    # Shuffle
    random.shuffle(all_clauses)
    
    # Take exactly 20000
    final_clauses = all_clauses[:20000]
    
    # Create DataFrame
    df = pd.DataFrame(final_clauses)
    
    # Save
    output_path = 'training_data_20000.csv'
    df.to_csv(output_path, index=False)
    
    print(f"\n[SUCCESS] Generated {len(final_clauses)} samples")
    print(f"Label distribution:")
    print(df['label'].value_counts())
    print(f"\nSaved to: {output_path}")
    
    return output_path

if __name__ == "__main__":
    random.seed(42)
    generate_20000_samples()

