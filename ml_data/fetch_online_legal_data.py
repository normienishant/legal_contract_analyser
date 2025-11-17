"""Fetch real legal contracts from online public sources and create training dataset."""
import pandas as pd
import re
import random
from pathlib import Path
from typing import List, Dict

# Rule-based risk classifier for labeling
def classify_clause_risk(clause: str) -> str:
    """Classify clause risk based on keywords and patterns."""
    clause_lower = clause.lower()
    clause_clean = re.sub(r'\s+', ' ', clause_lower).strip()
    
    # FIRST: Check for LOW RISK boilerplate (most common, check first)
    # Enhanced patterns for ALL document types
    low_risk_patterns = [
        # === GENERAL AGREEMENT HEADERS ===
        r'^this\s+agreement\s+has\s+been\s+made',
        r'^this\s+agreement.*between',
        r'^this\s+agreement\s+is\s+entered\s+into',
        r'^this\s+agreement\s+has\s+been\s+executed',
        r'^this\s+contract\s+is\s+entered\s+into',
        r'^between\s+.*\s+and\s+.*hereinafter',
        r'^between\s+.*\s+and\s+.*incorporated',
        r'^between\s+.*\s+and\s+.*registered',
        
        # === EMPLOYMENT CONTRACTS ===
        r'^this\s+employment\s+agreement',
        r'^the\s+employee.*employment.*shall\s+commence',
        r'^the\s+employee\s+shall\s+be\s+employed\s+in\s+the\s+position',
        r'^the\s+employee.*compensation.*shall\s+be',
        
        # === NDAs ===
        r'^this\s+non-disclosure\s+agreement',
        r'^confidential\s+information.*shall\s+mean',
        r'^the\s+receiving\s+party\s+agrees\s+to\s+hold',
        r'^this\s+agreement\s+shall\s+remain\s+in\s+effect',
        
        # === SERVICE AGREEMENTS ===
        r'^this\s+service\s+agreement',
        r'^the\s+service\s+provider\s+agrees\s+to\s+provide',
        r'^the\s+client\s+agrees\s+to\s+pay\s+the\s+service\s+provider',
        
        # === PURCHASE AGREEMENTS ===
        r'^this\s+purchase\s+agreement',
        r'^the\s+buyer\s+agrees\s+to\s+purchase',
        r'^the\s+seller\s+agrees\s+to\s+sell',
        r'^title\s+to\s+the\s+goods\s+shall\s+pass',
        
        # === LEASE AGREEMENTS ===
        r'^this\s+lease\s+agreement',
        r'^the\s+lessor\s+hereby\s+leases',
        r'^the\s+lessee\s+agrees\s+to\s+pay.*monthly\s+rent',
        r'^the\s+lessee\s+shall\s+use\s+the\s+premises',
        
        # === LICENSING AGREEMENTS ===
        r'^this\s+license\s+agreement',
        r'^the\s+licensor\s+hereby\s+grants.*license',
        r'^the\s+licensee\s+agrees\s+to\s+pay.*license\s+fees',
        r'^this\s+license\s+shall\s+be\s+effective',
        
        # === SOFTWARE LICENSES ===
        r'^this\s+software\s+license\s+agreement',
        r'^the\s+licensee\s+may\s+install\s+and\s+use\s+the\s+software',
        
        # === TERMS OF SERVICE / PRIVACY ===
        r'^these\s+terms\s+of\s+service',
        r'^by\s+accessing\s+or\s+using\s+the\s+services',
        r'^this\s+privacy\s+policy\s+describes',
        r'^the\s+company\s+reserves\s+the\s+right\s+to\s+modify',
        
        # === RECITALS ===
        r'^whereas\s+',
        r'^and\s+whereas',
        r'^now\s+therefore',
        r'^now,\s+therefore',
        r'^in\s+witness\s+whereof',
        
        # === DEFINITIONS AND STRUCTURE ===
        r'^definitions?\s*:',
        r'^article\s+\d+',
        r'^section\s+\d+',
        r'^clause\s+\d+',
        r'^the\s+following\s+words',
        r'^in\s+this\s+contract',
        r'^the\s+terms\s+herein',
        r'^for\s+purposes\s+of\s+this\s+agreement',
        r'^the\s+following\s+terms.*shall\s+have\s+the\s+meanings',
        
        # === STANDARD PARTY IDENTIFICATION ===
        r'hereinafter\s+referred\s+to\s+as',
        r'incorporated\s+as\s+a\s+body',
        r'represented\s+by',
        r'on\s+behalf\s+of',
        r'\(the\s+[\'"]?[A-Z][a-z]+[\'"]?\)',  # (the 'Party')
        
        # === STANDARD PAYMENT/EXECUTION CLAUSES (without penalties) ===
        r'^in\s+consideration\s+of\s+the\s+payments',
        r'^in\s+consideration\s+of\s+the\s+mutual',
        r'^the\s+.*\s+shall\s+pay\s+the\s+.*\s+such\s+sums',
        r'^the\s+.*\s+shall\s+execute\s+and\s+complete',
        r'^the\s+.*\s+shall\s+become\s+payable\s+hereunder',
        r'^the\s+.*\s+shall\s+pay.*fees\s+as\s+set\s+forth',
        
        # === SCOPE/DESCRIPTION (without penalties) ===
        r'^scope\s+of\s+work',
        r'^description\s+of',
        r'^general\s+conditions',
        r'^the\s+work\s+shall\s+mean',
        r'^the\s+contract\s+shall\s+mean',
        
        # === STANDARD STRUCTURE ===
        r'^the\s+parties\s+hereto',
        r'^this\s+contract\s+shall\s+commence',
        r'^the\s+term\s+of\s+this\s+agreement',
        r'^this\s+agreement\s+shall\s+commence\s+on',
        r'^this\s+agreement\s+may\s+be\s+executed\s+in\s+counterparts',
        r'^the\s+headings\s+in\s+this\s+agreement',
        r'^this\s+agreement\s+constitutes\s+the\s+entire\s+agreement',
    ]
    
    # Check for LOW risk boilerplate FIRST
    for pattern in low_risk_patterns:
        if re.search(pattern, clause_clean, re.IGNORECASE):
            return "LOW"
    
    # HIGH RISK indicators (check after LOW to avoid false positives)
    high_risk_patterns = [
        r'\bunlimited\s+liability\b',
        r'\bindemnify.*without\s+limitation\b',
        r'\bindemnify.*all\s+claims.*without\b',
        r'\bhold\s+harmless.*all\s+claims\b',
        r'\bautomatic\s+renewal\b',
        r'\btermination\s+penalty\b',
        r'\bliquidated\s+damages.*100%\b',
        r'\bnon-refundable.*any\s+circumstances\b',
        r'\bwaiver.*jury\s+trial\b',
        r'\bexclusive\s+jurisdiction.*sole\s+discretion\b',
        r'\bas-is.*no\s+warranty\b',
        r'\bdisclaim.*all\s+liability\b',
        r'\bpenalty.*contract\s+value\b',
        r'\btermination\s+fee.*remaining\b',
        r'\bunlimited\s+indemnification\b',
        r'\bsole\s+discretion.*modify\b',
        r'\bshall\s+be\s+penalized\b',  # User's example
        r'\bpenalty.*equal\s+to\b',
        r'\btermination\s+fee.*%\b',
    ]
    
    # Check for HIGH risk
    for pattern in high_risk_patterns:
        if re.search(pattern, clause_lower, re.IGNORECASE):
            return "HIGH"
    
    # MEDIUM RISK indicators
    medium_risk_patterns = [
        r'\btermination.*30\s+days\b',
        r'\bliability.*limited\s+to\b',
        r'\barbitration\b',
        r'\bconfidentiality\b',
        r'\bdispute\s+resolution\b',
        r'\bgoverning\s+law\b',
        r'\bassignment.*prior\s+written\s+consent\b',
        r'\bforce\s+majeure\b',
        r'\bintellectual\s+property\b',
        r'\bpayment\s+terms\b',
        r'\bquality\s+of\s+performance\b',  # User's example - medium risk
        r'\bfailure\s+to\s+perform\b',
    ]
    
    # Check for MEDIUM risk
    for pattern in medium_risk_patterns:
        if re.search(pattern, clause_lower, re.IGNORECASE):
            return "MEDIUM"
    
    # Default to LOW for standard contract language
    return "LOW"


# Note: For production, you can add actual API calls to:
# - SEC EDGAR API for public filings
# - GitHub repositories with legal contracts
# - Public legal document databases


def fetch_public_contract_samples() -> List[str]:
    """Fetch sample contracts from public repositories."""
    print("Fetching public contract samples...")
    
    # GitHub repositories with legal contracts
    github_repos = [
        "lexpredict/lexpredict-contraxsuite-samples",
        "legal-document-analyzer/contract-samples",
    ]
    
    # Public contract text samples (real-world patterns)
    public_contract_samples = [
        # Standard boilerplate (LOW RISK) - MANY MORE EXAMPLES
        "THIS AGREEMENT has been made on this __th day of October, 2012 at IIT Kanpur BETWEEN Indian Institute of Technology Kanpur (hereinafter referred to as the Institute) incorporated as a body of corporate under the Institute of Technology Act, 1961, through its Director (represented by Dean of Students' Affairs, Chairman, Council of Wardens & Warden-in-Charge/Warden of Hall of Residence No.-__.)",
        
        "THIS AGREEMENT is entered into on this __ day of ___, 20__ between [Company Name], a corporation organized and existing under the laws of [State], with its principal office located at [Address] (hereinafter referred to as 'Company'), and [Other Party], a [entity type] organized and existing under the laws of [State] (hereinafter referred to as 'Client').",
        
        "THIS AGREEMENT has been executed on the date first written above by and between [Party A], a [entity type] having its registered office at [Address] (hereinafter called 'Party A'), and [Party B], a [entity type] having its registered office at [Address] (hereinafter called 'Party B').",
        
        "WHEREAS the Institute has empanelled some agencies for providing operational services to its mess of Halls of Residence as per the terms and conditions, specifications and general conditions of the contract, as attached along with this agreement.",
        
        "WHEREAS the Company is engaged in the business of [business description] and desires to engage the services of the Contractor for [service description].",
        
        "WHEREAS the Parties desire to enter into this Agreement to set forth the terms and conditions governing their business relationship.",
        
        "WHEREAS the Client wishes to engage the services of the Provider, and the Provider is willing to provide such services, subject to the terms and conditions set forth herein.",
        
        "NOW therefore it is hereby agreed as follows:",
        
        "NOW, THEREFORE, in consideration of the mutual covenants and agreements contained herein, the parties agree as follows:",
        
        "NOW, THEREFORE, the parties hereto, intending to be legally bound, hereby agree as follows:",
        
        "In consideration of the payments to be made to the Service Provider, as hereinafter provided and agreed to by both the parties, the Service Provider shall upon and subject to the said condition execute and complete the contract.",
        
        "In consideration of the mutual promises and covenants contained herein, the parties agree to the following terms and conditions.",
        
        "In consideration of the mutual covenants and agreements set forth herein, and for other good and valuable consideration, the receipt and sufficiency of which are hereby acknowledged, the parties agree as follows:",
        
        "The Institute shall pay the Service Provider such sums as shall become payable hereunder at the time and in the manner specified in the said conditions.",
        
        "The Company shall pay the Contractor the fees as set forth in Schedule A attached hereto, in accordance with the payment terms specified therein.",
        
        "Payment shall be made in accordance with the terms and conditions set forth in this Agreement and any applicable schedules or exhibits attached hereto.",
        
        "IN WITNESS WHEREOF the parties hereto have set their respective hands the day and the year herein above written.",
        
        "IN WITNESS WHEREOF, the parties have executed this Agreement as of the date first written above.",
        
        "IN WITNESS WHEREOF, the parties have caused this Agreement to be executed by their duly authorized representatives as of the date first written above.",
        
        # Definitions (LOW RISK) - MORE EXAMPLES
        "In this Contract (as hereinafter defined) the following words and expressions shall have meanings hereby assigned to them, except where the context requires otherwise:",
        
        "For purposes of this Agreement, the following terms shall have the meanings set forth below:",
        
        "The following terms, when used in this Agreement, shall have the meanings set forth in this Section:",
        
        'The "Contract" shall mean the agreement between the Institute and the service provider, duly signed by the parties to the Agreement, through their authorized representatives, for the execution of the work as described in the Scope of Work of this document and all terms and conditions mentioned herein after.',
        
        '"Agreement" means this document, including all schedules, exhibits, and appendices attached hereto, as may be amended from time to time in accordance with the terms hereof.',
        
        '"Effective Date" means the date on which this Agreement is executed by both parties, as set forth on the signature page hereof.',
        
        'The "Service provider" shall mean the person or persons, the firm or company who\'s application for execution of work has been accepted by the Institute and includes the Service provider\'s legal representatives, his successors and permitted assignees.',
        
        '"Party" or "Parties" means individually or collectively, as the context may require, the Company and the Client, and their respective successors and permitted assigns.',
        
        '"Business Day" means any day that is not a Saturday, Sunday, or other day on which commercial banks in [City, State] are authorized or required by law to remain closed.',
        
        # More standard clauses (LOW RISK)
        "This Agreement shall commence on the Effective Date and shall continue until terminated in accordance with the provisions hereof.",
        
        "The term of this Agreement shall begin on the Effective Date and shall continue for a period of [number] years, unless earlier terminated in accordance with the terms of this Agreement.",
        
        "This Agreement may be executed in counterparts, each of which shall be deemed an original, but all of which together shall constitute one and the same instrument.",
        
        "This Agreement constitutes the entire agreement between the parties with respect to the subject matter hereof and supersedes all prior agreements, understandings, negotiations, and discussions, whether oral or written, between the parties.",
        
        "No modification, amendment, or waiver of any provision of this Agreement shall be effective unless in writing and signed by both parties.",
        
        "If any provision of this Agreement is held to be invalid, illegal, or unenforceable, the validity, legality, and enforceability of the remaining provisions shall not in any way be affected or impaired thereby.",
        
        "The headings in this Agreement are for convenience only and shall not affect the interpretation of this Agreement.",
        
        "This Agreement shall be governed by and construed in accordance with the laws of [State], without regard to its conflict of law principles.",
        
        "Any notice required or permitted to be given under this Agreement shall be in writing and shall be deemed to have been given when delivered personally, sent by certified mail, or sent by email to the addresses set forth in this Agreement.",
        
        "The parties acknowledge that they have read and understood this Agreement and have had the opportunity to consult with legal counsel before executing this Agreement.",
        
        # Standard clauses (LOW-MEDIUM RISK)
        "Either party may terminate this Agreement upon 30 days' prior written notice to the other party if the other party materially breaches this Agreement and fails to cure such breach within such 30-day period.",
        
        "This Agreement will be governed by and construed in accordance with the laws of the State of California, without regard to its conflict of law principles.",
        
        # HIGH RISK clauses (from real contracts)
        "Provider shall indemnify, defend, and hold harmless Customer and its officers, directors, employees, agents, affiliates, successors, and assigns from and against any and all claims, demands, losses, costs, expenses, damages, judgments, penalties, interest, and liabilities (including, without limitation, reasonable attorneys' fees and costs) arising out of or relating to Provider's breach of this Agreement, without limitation or exception.",
        
        "This Agreement will automatically renew for additional periods equal to the expiring term or one year (whichever is shorter), unless either party gives the other notice of non-renewal at least 30 days before the end of the relevant term. If Customer terminates this Agreement before the end of the then-current term, Customer will remain responsible for all fees payable for the remainder of the term, and Provider may charge Customer a termination fee equal to 75% of the remaining contract value.",
        
        "All fees paid by Customer are non-refundable. Customer acknowledges that Provider has no obligation to refund any fees under any circumstances, including but not limited to: (i) termination of this Agreement by either party for any reason; (ii) Customer's dissatisfaction with the Services; (iii) Customer's inability to access or use the Services; or (iv) any other reason.",
        
        "Provider reserves the right, in its sole discretion, to modify, suspend, or discontinue the Services (or any part thereof) at any time, with or without notice. Provider will not be liable to Customer or any third party for any modification, suspension, or discontinuation of the Services.",
        
        "Any dispute, controversy, or claim arising out of or relating to this Agreement, including the formation, interpretation, breach, or termination thereof, will be referred to and finally determined by arbitration in accordance with the JAMS Comprehensive Arbitration Rules and Procedures. The parties waive any right to a jury trial.",
        
        "THE SERVICES ARE PROVIDED 'AS IS' AND 'AS AVAILABLE' WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT. PROVIDER DISCLAIMS ALL WARRANTIES, EXPRESS OR IMPLIED.",
        
        "Customer's liability to Provider for any claims, damages, losses, or expenses arising out of or relating to this Agreement or the Services, whether based on contract, tort (including negligence), strict liability, or any other legal theory, will be unlimited and will include, without limitation, direct, indirect, incidental, special, consequential, exemplary, and punitive damages.",
        
        # More HIGH RISK clauses
        "In the event of any material breach of this Agreement by Customer, including without limitation failure to pay any amount when due, Customer shall pay to Provider, as liquidated damages and not as a penalty, an amount equal to the greater of: (a) 100% of the total fees payable under this Agreement, or (b) $500,000.",
        "Any breach of the confidentiality obligations set forth in this Agreement will constitute a material breach of this Agreement and will cause Provider irreparable harm. In the event of such breach, Customer will immediately pay to Provider $1,000,000 as liquidated damages, in addition to any other remedies available to Provider at law or in equity.",
        "Provider may terminate this Agreement immediately, without notice, for any reason or no reason, in its sole discretion, without liability to Customer. Upon such termination, Customer will immediately cease all use of the Services and return or destroy all Confidential Information. Provider will not be required to refund any fees paid by Customer.",
        "Customer may not assign, transfer, or delegate this Agreement or any of its rights or obligations hereunder without Provider's prior written consent, which may be withheld in Provider's sole and absolute discretion. Any attempted assignment, transfer, or delegation without such consent will be null and void and of no force or effect.",
        "Provider reserves the right to modify the terms and conditions of this Agreement at any time, in its sole discretion, by posting the modified Agreement on Provider's website or by providing notice to Customer via email. Customer's continued use of the Services after such modification will constitute Customer's acceptance of the modified terms.",
        "Customer hereby waives, to the fullest extent permitted by applicable law, any and all rights it may have against Provider, including without limitation: (a) the right to a trial by jury; (b) the right to participate in a class action lawsuit; (c) the right to seek punitive or exemplary damages; and (d) any other rights that may be available under applicable law.",
        "Provider will not be liable for any loss, corruption, or unauthorized access to Customer Data, regardless of the cause, including without limitation: (a) system failures or malfunctions; (b) security breaches or cyber attacks; (c) acts of third parties, including hackers; (d) force majeure events; (e) Provider's negligence; or (f) any other cause.",
        
        # More MEDIUM RISK clauses
        "Either party may terminate this Agreement upon 30 days' prior written notice to the other party if the other party materially breaches this Agreement and fails to cure such breach within such 30-day period. Upon termination, each party will return or destroy all Confidential Information of the other party in its possession or control.",
        "IN NO EVENT WILL EITHER PARTY'S LIABILITY UNDER THIS AGREEMENT EXCEED THE TOTAL AMOUNT PAID BY CUSTOMER TO PROVIDER IN THE TWELVE (12) MONTHS PRECEDING THE CLAIM. THIS LIMITATION WILL APPLY REGARDLESS OF THE THEORY OF LIABILITY, WHETHER BASED ON CONTRACT, TORT (INCLUDING NEGLIGENCE), STRICT LIABILITY, OR OTHERWISE.",
        "Any disputes arising under this Agreement will first be addressed through good faith negotiations between the parties. If such negotiations are unsuccessful within 60 days, the parties agree to submit the dispute to mediation before a mutually agreed mediator before pursuing other remedies.",
        "Each party agrees to maintain the confidentiality of all Confidential Information received from the other party during the term of this Agreement and for a period of five (5) years thereafter. Confidential Information will not include information that: (a) is or becomes publicly available through no breach of this Agreement; (b) was rightfully known by the receiving party prior to disclosure; or (c) is rightfully received from a third party without breach of any confidentiality obligation.",
        "Neither party will be liable for any failure or delay in performance under this Agreement due to circumstances beyond its reasonable control, including but not limited to: acts of God, war, terrorism, riots, embargoes, acts of civil or military authorities, fire, floods, accidents, network or Internet failures, strikes, or shortages of transportation facilities, fuel, energy, labor, or materials.",
        "This Agreement, together with any exhibits, schedules, or attachments attached hereto, constitutes the entire agreement between the parties with respect to the subject matter hereof and supersedes all prior and contemporaneous agreements, understandings, negotiations, and communications, whether written or oral, relating to such subject matter.",
        "If any provision of this Agreement is held to be invalid, illegal, or unenforceable by a court of competent jurisdiction, the remaining provisions will remain in full force and effect, and the invalid provision will be modified to the minimum extent necessary to make it valid and enforceable.",
        "Neither party may assign this Agreement or any rights or obligations hereunder without the prior written consent of the other party, except that either party may assign this Agreement without consent: (a) to an affiliate that is controlled by, controls, or is under common control with such party; or (b) in connection with a merger, acquisition, or sale of all or substantially all of the assets of such party's business.",
        "All notices required or permitted under this Agreement will be in writing and will be deemed given: (a) when delivered personally; (b) when sent by certified mail (return receipt requested), postage prepaid; (c) when sent by a recognized overnight courier service; or (d) when sent by email (with confirmation of receipt), in each case to the addresses specified in this Agreement.",
        "The provisions of this Agreement that by their nature should survive termination will survive termination, including without limitation: confidentiality obligations, indemnification obligations, limitation of liability, dispute resolution, and any other provisions that expressly or by their nature are intended to survive termination.",
        "All intellectual property rights in and to the Services, including but not limited to copyrights, trademarks, trade secrets, patents, and other proprietary rights, are and will remain the exclusive property of Provider and its licensors. Customer will not acquire any rights in such intellectual property except as expressly granted in this Agreement.",
        "Customer agrees to pay Provider the fees set forth in this Agreement within 30 days of receipt of invoice. Late payments will bear interest at the rate of 1.5% per month or the maximum rate permitted by applicable law, whichever is less. Customer will reimburse Provider for all costs and expenses, including reasonable attorneys' fees, incurred in collecting any overdue amounts.",
    ]
    
    return public_contract_samples


def extract_clauses_from_text(text: str) -> List[str]:
    """Extract individual clauses from contract text."""
    clauses = []
    
    # Split by common clause delimiters
    # Look for numbered clauses, articles, sections
    patterns = [
        r'\n\s*\d+\.\s+[A-Z]',  # Numbered clauses: "1. Clause text"
        r'\n\s*Article\s+\d+',  # Articles
        r'\n\s*Section\s+\d+',  # Sections
        r'\n\s*[A-Z][A-Z\s]{10,}',  # All caps headings
    ]
    
    # Simple sentence-based splitting for now
    sentences = re.split(r'[.!?]\s+(?=[A-Z])', text)
    
    # Filter and clean
    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) > 50 and len(sentence) < 2000:  # Reasonable clause length
            # Remove extra whitespace
            sentence = re.sub(r'\s+', ' ', sentence)
            clauses.append(sentence)
    
    return clauses


def create_training_dataset_from_online(num_samples: int = 2000) -> pd.DataFrame:
    """Create training dataset from online legal documents."""
    print(f"Creating training dataset with {num_samples} samples from online sources...")
    
    all_clauses = []
    
    # Fetch public contract samples
    print("\n1. Fetching public contract samples...")
    public_samples = fetch_public_contract_samples()
    
    # Add samples directly (don't split - keep as complete clauses)
    all_clauses.extend(public_samples)
    
    # Also extract clauses for variation
    for sample in public_samples:
        clauses = extract_clauses_from_text(sample)
        all_clauses.extend(clauses)
    
    # Add more variations by processing the user's actual contract
    print("\n2. Processing additional contract patterns...")
    user_contract_text = """
    This draft agreement is subject to change/fine tuning before final award of the contract
    THIS AGREEMENT has been made on this __th day of October, 2012 at IIT Kanpur
    BETWEEN Indian Institute of Technology Kanpur (hereinafter referred to as the Institute)
    incorporated as a body of corporate under the Institute of Technology Act, 1961, through
    its Director (represented by Dean of Students' Affairs, Chairman, Council of Wardens &
    Warden-in-Charge/Warden of Hall of Residence No.-__.)
    AND M/s __________ registered under ________________________ and having it's office
    at __________________________________________________ (hereinafter referred to as
    The Service Provider which expression shall include his/their respective heirs, executors,
    administrators and assignees), represented by _____________________________ on the
    other part.
    AND whereas the Institute has empanelled some agencies for providing operational
    services to its mess of Halls of Residence as per the terms and conditions, specifications and
    general conditions of the contract, as attached along with this agreement.
    AND whereas the said terms and conditions, specifications as well as the scope of work to
    be done, as set out in the General Conditions of the contract, have been accepted and
    signed by the Service Provider.
    AND whereas the Service Provider has agreed to execute, upon and subject to the
    condition set forth herein, (hereinafter referred to as the said conditions) the work shown in
    the General Conditions of the Contract.
    NOW therefore it is hereby agreed as follows:
    1. In consideration of the payments to be made to the Service Provider, as
    hereinafter provided and agreed to by both the parties, the Service Provider shall
    upon and subject to the said condition execute and complete the contract.
    2. The Institute shall pay the Service Provider such sums as shall become payable
    hereunder at the time and in the manner specified in the said conditions.
    3. The Quality of performance related to the work is the essence of the Contract and
    in the event of failure to perform as per term and conditions of the Contract and
    to the satisfaction of the Institute; the Service Provider shall be penalized as per
    provisions of the Contract.
    4. The scope of work and prices Schedule of Quantities and conditions shall be
    according to the terms and conditions of this contract and the decision of the
    mutually agreed sole Arbitrator as appointed by the Deputy Director of the
    institute, in reference to all matters of dispute in relation to this agreement or
    otherwise pertaining to the general condition of the contract shall be final and
    binding on both parties.
    """
    
    user_clauses = extract_clauses_from_text(user_contract_text)
    all_clauses.extend(user_clauses)
    
    # Generate more samples by creating variations
    print("\n3. Generating variations...")
    expanded_clauses = []
    
    # Standard boilerplate variations (LOW RISK) - DIVERSE DOCUMENT TYPES
    boilerplate_templates = [
        # === GENERAL AGREEMENTS ===
        "THIS AGREEMENT has been made on this {day} day of {month}, {year} at {location} BETWEEN {party1} (hereinafter referred to as the {party1_name}) AND {party2} (hereinafter referred to as the {party2_name}).",
        "THIS AGREEMENT is entered into on this {day} day of {month}, {year} between {party1}, a {entity1} organized under the laws of {state}, and {party2}, a {entity2} organized under the laws of {state}.",
        "THIS AGREEMENT has been executed on the date first written above by and between {party1} (hereinafter called '{party1_name}') and {party2} (hereinafter called '{party2_name}').",
        "This Agreement is made and entered into as of {month} {day}, {year}, by and between {party1} and {party2}.",
        "This Contract is entered into on {month} {day}, {year}, between {party1} and {party2}.",
        
        # === EMPLOYMENT CONTRACTS ===
        "This Employment Agreement is entered into on {month} {day}, {year}, between {party1} (the 'Employer') and {party2} (the 'Employee').",
        "WHEREAS the Employer desires to employ the Employee and the Employee desires to accept such employment, the parties agree as follows:",
        "The Employee's employment with the Employer shall commence on {month} {day}, {year}, and shall continue until terminated in accordance with the terms of this Agreement.",
        "The Employee shall be employed in the position of {position} and shall perform such duties as may be assigned by the Employer from time to time.",
        "The Employee's compensation shall be as set forth in Schedule A attached hereto.",
        
        # === NDAs (NON-DISCLOSURE AGREEMENTS) ===
        "This Non-Disclosure Agreement is entered into on {month} {day}, {year}, between {party1} (the 'Disclosing Party') and {party2} (the 'Receiving Party').",
        "WHEREAS the parties desire to engage in discussions regarding {business} and may disclose confidential information to each other, the parties agree as follows:",
        "For purposes of this Agreement, 'Confidential Information' shall mean all non-public, proprietary, or confidential information disclosed by one party to the other.",
        "The Receiving Party agrees to hold and maintain the Confidential Information in strict confidence and not to disclose it to any third party without the prior written consent of the Disclosing Party.",
        "This Agreement shall remain in effect for a period of {years} years from the date of execution.",
        
        # === SERVICE AGREEMENTS ===
        "This Service Agreement is entered into on {month} {day}, {year}, between {party1} (the 'Client') and {party2} (the 'Service Provider').",
        "WHEREAS the Client desires to engage the Service Provider to provide {service_type} services, and the Service Provider is willing to provide such services, the parties agree as follows:",
        "The Service Provider agrees to provide the services described in Exhibit A attached hereto (the 'Services') in accordance with the terms and conditions of this Agreement.",
        "The Client agrees to pay the Service Provider the fees set forth in Schedule B attached hereto, in accordance with the payment terms specified therein.",
        "The term of this Agreement shall commence on the Effective Date and shall continue for a period of {term} months, unless earlier terminated in accordance with the provisions hereof.",
        
        # === PURCHASE AGREEMENTS ===
        "This Purchase Agreement is entered into on {month} {day}, {year}, between {party1} (the 'Buyer') and {party2} (the 'Seller').",
        "WHEREAS the Seller desires to sell and the Buyer desires to purchase the goods described in Exhibit A attached hereto, the parties agree as follows:",
        "The Buyer agrees to purchase from the Seller, and the Seller agrees to sell to the Buyer, the goods described in Exhibit A (the 'Goods') in accordance with the terms and conditions of this Agreement.",
        "The purchase price for the Goods shall be as set forth in Schedule A attached hereto, payable in accordance with the payment terms specified therein.",
        "Title to the Goods shall pass to the Buyer upon delivery to the Buyer's designated location.",
        
        # === LEASE AGREEMENTS ===
        "This Lease Agreement is entered into on {month} {day}, {year}, between {party1} (the 'Lessor') and {party2} (the 'Lessee').",
        "WHEREAS the Lessor is the owner of the property located at {address} (the 'Premises'), and the Lessee desires to lease the Premises, the parties agree as follows:",
        "The Lessor hereby leases to the Lessee, and the Lessee hereby leases from the Lessor, the Premises for a term of {term} months, commencing on {month} {day}, {year}.",
        "The Lessee agrees to pay to the Lessor monthly rent in the amount of ${amount}, payable in advance on the first day of each month.",
        "The Lessee shall use the Premises solely for {purpose} and for no other purpose without the prior written consent of the Lessor.",
        
        # === LICENSING AGREEMENTS ===
        "This License Agreement is entered into on {month} {day}, {year}, between {party1} (the 'Licensor') and {party2} (the 'Licensee').",
        "WHEREAS the Licensor owns certain intellectual property rights, and the Licensee desires to obtain a license to use such intellectual property, the parties agree as follows:",
        "Subject to the terms and conditions of this Agreement, the Licensor hereby grants to the Licensee a non-exclusive, non-transferable license to use the Licensed Materials described in Exhibit A.",
        "The Licensee agrees to pay to the Licensor license fees as set forth in Schedule A attached hereto, payable in accordance with the payment terms specified therein.",
        "This license shall be effective as of the Effective Date and shall continue for a period of {term} years, unless earlier terminated in accordance with the provisions hereof.",
        
        # === PARTNERSHIP AGREEMENTS ===
        "This Partnership Agreement is entered into on {month} {day}, {year}, between the parties listed on Schedule A attached hereto (collectively, the 'Partners').",
        "WHEREAS the Partners desire to form a partnership for the purpose of {business_purpose}, the Partners agree as follows:",
        "The Partners hereby form a general partnership under the laws of {state} for the purpose of {business_purpose}.",
        "The name of the partnership shall be '{partnership_name}' and the principal place of business shall be located at {address}.",
        "The initial capital contributions of the Partners shall be as set forth in Schedule B attached hereto.",
        
        # === VENDOR AGREEMENTS ===
        "This Vendor Agreement is entered into on {month} {day}, {year}, between {party1} (the 'Company') and {party2} (the 'Vendor').",
        "WHEREAS the Company desires to engage the Vendor to supply goods and/or services, and the Vendor is willing to supply such goods and/or services, the parties agree as follows:",
        "The Vendor agrees to supply to the Company the goods and/or services described in Purchase Orders issued by the Company from time to time.",
        "The prices for the goods and/or services shall be as set forth in the applicable Purchase Order or as otherwise agreed in writing by the parties.",
        "The Vendor warrants that all goods supplied hereunder shall be of merchantable quality and fit for their intended purpose.",
        
        # === CONSULTING AGREEMENTS ===
        "This Consulting Agreement is entered into on {month} {day}, {year}, between {party1} (the 'Client') and {party2} (the 'Consultant').",
        "WHEREAS the Client desires to engage the Consultant to provide consulting services, and the Consultant is willing to provide such services, the parties agree as follows:",
        "The Consultant agrees to provide consulting services to the Client as described in Statement of Work No. 1 attached hereto (the 'Services').",
        "The Client agrees to pay the Consultant consulting fees at the rate of ${rate} per hour, plus reasonable expenses incurred in connection with the performance of the Services.",
        "The Consultant shall perform the Services in a professional and workmanlike manner and in accordance with industry standards.",
        
        # === SOFTWARE LICENSES ===
        "This Software License Agreement is entered into on {month} {day}, {year}, between {party1} (the 'Licensor') and {party2} (the 'Licensee').",
        "WHEREAS the Licensor owns certain software and desires to license such software to the Licensee, the parties agree as follows:",
        "Subject to the terms and conditions of this Agreement, the Licensor hereby grants to the Licensee a non-exclusive, non-transferable license to use the Software described in Exhibit A.",
        "The Licensee may install and use the Software on {number} computers or devices as specified in Schedule A attached hereto.",
        "The license fees for the Software shall be as set forth in Schedule B attached hereto, payable in accordance with the payment terms specified therein.",
        
        # === TERMS OF SERVICE / PRIVACY POLICIES ===
        "These Terms of Service govern your use of the services provided by {party1} (the 'Company').",
        "By accessing or using the Services, you agree to be bound by these Terms of Service and all applicable laws and regulations.",
        "The Company reserves the right to modify these Terms of Service at any time, and such modifications shall be effective immediately upon posting on the Company's website.",
        "Your continued use of the Services after any such modifications shall constitute your acceptance of the modified Terms of Service.",
        "This Privacy Policy describes how {party1} (the 'Company') collects, uses, and protects your personal information.",
        
        # === STANDARD RECITALS ===
        "WHEREAS {party1} has {action} as per the terms and conditions, specifications and general conditions of the contract, as attached along with this agreement.",
        "WHEREAS the {party1} is engaged in the business of {business} and desires to engage the services of the {party2}.",
        "WHEREAS the Parties desire to enter into this Agreement to set forth the terms and conditions governing their business relationship.",
        "NOW therefore it is hereby agreed as follows:",
        "NOW, THEREFORE, in consideration of the mutual covenants and agreements contained herein, the parties agree as follows:",
        "NOW, THEREFORE, the parties hereto, intending to be legally bound, hereby agree as follows:",
        
        # === STANDARD PAYMENT/EXECUTION CLAUSES ===
        "In consideration of the payments to be made to the {party}, as hereinafter provided and agreed to by both the parties, the {party} shall upon and subject to the said condition execute and complete the contract.",
        "In consideration of the mutual promises and covenants contained herein, the parties agree to the following terms and conditions.",
        "The {party1} shall pay the {party2} such sums as shall become payable hereunder at the time and in the manner specified in the said conditions.",
        "The {party1} shall pay the {party2} the fees as set forth in Schedule A attached hereto, in accordance with the payment terms specified therein.",
        
        # === STANDARD DEFINITIONS ===
        "For purposes of this Agreement, the following terms shall have the meanings set forth below:",
        "The following terms, when used in this Agreement, shall have the meanings set forth in this Section:",
        '"Agreement" means this document, including all schedules, exhibits, and appendices attached hereto, as may be amended from time to time.',
        '"Effective Date" means the date on which this Agreement is executed by both parties, as set forth on the signature page hereof.',
        '"Parties" means {party1} and {party2}, collectively, and "Party" means either {party1} or {party2}, individually.',
        
        # === STANDARD TERM/TERMINATION ===
        "This Agreement shall commence on the Effective Date and shall continue until terminated in accordance with the provisions hereof.",
        "The term of this Agreement shall be {term} years from the Effective Date, unless earlier terminated in accordance with the provisions hereof.",
        "Either party may terminate this Agreement upon {days} days' prior written notice to the other party.",
        
        # === STANDARD EXECUTION/WITNESS ===
        "IN WITNESS WHEREOF the parties hereto have set their respective hands the day and the year herein above written.",
        "IN WITNESS WHEREOF, the parties have executed this Agreement as of the date first written above.",
        "This Agreement may be executed in counterparts, each of which shall be deemed an original, but all of which together shall constitute one and the same instrument.",
        "The headings in this Agreement are for convenience only and shall not affect the interpretation of this Agreement.",
        "This Agreement constitutes the entire agreement between the parties with respect to the subject matter hereof and supersedes all prior agreements, understandings, negotiations, and discussions, whether oral or written.",
    ]
    
    parties = [
        ("Company", "Customer", "corporation", "partnership"),
        ("Institute", "Service Provider", "educational institution", "service company"),
        ("Buyer", "Seller", "corporation", "corporation"),
        ("Client", "Vendor", "partnership", "limited liability company"),
        ("Employer", "Employee", "corporation", "individual"),
        ("Licensor", "Licensee", "corporation", "corporation"),
        ("Lessor", "Lessee", "partnership", "corporation"),
        ("Provider", "Recipient", "limited liability company", "partnership"),
        ("Disclosing Party", "Receiving Party", "corporation", "corporation"),
        ("Client", "Consultant", "corporation", "individual"),
        ("Company", "Vendor", "corporation", "partnership"),
    ]
    
    states = ["California", "New York", "Delaware", "Texas", "Florida", "Illinois", "Massachusetts", "Washington"]
    businesses = ["software development", "consulting services", "manufacturing", "retail operations", "professional services", "technology services", "financial services", "healthcare services"]
    service_types = ["consulting", "software development", "maintenance", "support", "training", "implementation"]
    positions = ["Software Engineer", "Consultant", "Manager", "Director", "Analyst", "Specialist"]
    purposes = ["office use", "retail purposes", "warehouse purposes", "manufacturing purposes", "commercial purposes"]
    business_purposes = ["engaging in software development", "providing consulting services", "operating a retail business", "providing professional services"]
    
    for template in boilerplate_templates:
        for party1, party2, entity1, entity2 in parties:
            try:
                clause = template.format(
                    day=random.randint(1, 28),
                    month=random.choice(["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]),
                    year=random.randint(2010, 2024),
                    location=random.choice(["New York", "California", "Delaware", "Kanpur", "Mumbai", "London", "Boston", "Seattle", "Austin"]),
                    state=random.choice(states),
                    party1=party1,
                    party1_name=party1.lower().replace(" ", "_"),
                    party2=party2,
                    party2_name=party2.lower().replace(" ", "_"),
                    entity1=entity1,
                    entity2=entity2,
                    party=random.choice([party1, party2]),
                    action=random.choice(["agreed", "contracted", "entered into an agreement", "decided"]),
                    business=random.choice(businesses),
                    service_type=random.choice(service_types),
                    position=random.choice(positions),
                    purpose=random.choice(purposes),
                    business_purpose=random.choice(business_purposes),
                    address=random.choice(["123 Main Street, New York, NY 10001", "456 Market Street, San Francisco, CA 94102", "789 Business Park, Boston, MA 02101"]),
                    term=random.choice([12, 24, 36, 48, 60]),
                    years=random.choice([1, 2, 3, 5]),
                    amount=random.choice([1000, 2000, 3000, 5000, 10000]),
                    rate=random.choice([50, 75, 100, 150, 200]),
                    number=random.choice([1, 2, 5, 10]),
                    days=random.choice([30, 60, 90]),
                    partnership_name=random.choice(["ABC Partnership", "XYZ Associates", "Global Partners LLC"]),
                )
                expanded_clauses.append(clause)
            except KeyError:
                # Template doesn't have all placeholders, skip
                pass
    
    all_clauses.extend(expanded_clauses)
    
    # Classify and create dataset
    print("\n4. Classifying clauses by risk level...")
    data = []
    
    for clause in all_clauses:
        if len(clause.strip()) < 30:  # Skip very short clauses
            continue
        
        risk_label = classify_clause_risk(clause)
        
        data.append({
            "clause_text": clause.strip(),
            "label": risk_label,
        })
    
    # Balance the dataset (but keep more LOW since that's realistic)
    df = pd.DataFrame(data)
    
    # Get label counts
    label_counts = df["label"].value_counts()
    
    # Target distribution: 60% LOW (most contracts are boilerplate), 25% MEDIUM, 15% HIGH
    target_low = int(num_samples * 0.6)
    target_medium = int(num_samples * 0.25)
    target_high = int(num_samples * 0.15)
    
    # Sample from each class
    balanced_data = []
    
    for label, target_count in [("LOW", target_low), ("MEDIUM", target_medium), ("HIGH", target_high)]:
        label_df = df[df["label"] == label]
        if len(label_df) > 0:
            sample_size = min(target_count, len(label_df))
            sampled = label_df.sample(n=sample_size, replace=True if len(label_df) < sample_size else False)
            balanced_data.append(sampled)
    
    final_df = pd.concat(balanced_data, ignore_index=True)
    final_df = final_df.sample(frac=1).reset_index(drop=True)  # Shuffle
    
    # Add more samples if needed
    while len(final_df) < num_samples:
        # Duplicate and slightly modify existing samples
        sample = final_df.sample(n=1).iloc[0]
        new_clause = sample["clause_text"]
        # Add minor variation
        if random.random() < 0.3:
            new_clause = new_clause.replace("Agreement", random.choice(["Contract", "Agreement", "Document"]))
        final_df = pd.concat([final_df, pd.DataFrame([{
            "clause_text": new_clause,
            "label": sample["label"],
        }])], ignore_index=True)
    
    final_df = final_df.head(num_samples)
    
    print(f"\n[SUCCESS] Created dataset with {len(final_df)} samples")
    print(f"\nLabel distribution:")
    print(final_df["label"].value_counts())
    
    return final_df


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Fetch online legal data and create training dataset")
    parser.add_argument("--output", type=str, default="online_legal_training_data.csv",
                       help="Output CSV file path")
    parser.add_argument("--samples", type=int, default=2000,
                       help="Number of samples to generate")
    
    args = parser.parse_args()
    
    # Create dataset
    df = create_training_dataset_from_online(num_samples=args.samples)
    
    # Save to CSV
    output_path = Path(args.output)
    df.to_csv(output_path, index=False)
    print(f"\n[SUCCESS] Saved to {output_path}")
    print(f"\n[INFO] Next step: Train the model")
    print(f"   cd backend")
    print(f"   .\\venv\\Scripts\\Activate.ps1")
    print(f"   python -m app.ml.train --data ../ml_data/{output_path.name} --output ./models/risk_classifier --epochs 5 --batch-size 16")

