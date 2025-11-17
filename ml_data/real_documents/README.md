# Real Legal Documents Directory

## Purpose
This directory is for storing real legal documents (PDF, DOCX, TXT) that will be processed and used for training the ML model.

## Supported Formats
- **PDF** (.pdf)
- **Word Documents** (.docx, .doc)
- **Text Files** (.txt)

## How to Use

1. **Add Documents:**
   - Copy your legal documents (contracts, agreements, etc.) to this directory
   - You can create subdirectories to organize them
   - The script will process all documents recursively

2. **Run Training Script:**
   ```bash
   cd ml_data
   python create_real_document_dataset.py --samples 12000 --output large_real_legal_dataset.csv
   ```

3. **Documents Will Be:**
   - Extracted (text extracted from PDF/DOCX)
   - Segmented (split into individual clauses)
   - Classified (labeled as LOW, MEDIUM, or HIGH risk)
   - Added to training dataset

## Document Types Supported

- Rental/Lease Agreements
- Employment Contracts
- Service Agreements
- Purchase Agreements
- Partnership Agreements
- Software License Agreements
- NDAs (Non-Disclosure Agreements)
- Any other legal contracts

## Notes

- Documents are processed automatically
- Text extraction handles multiple encodings
- Clause segmentation works with numbered clauses
- Risk classification uses improved patterns
- Maximum 50 files processed per run (to avoid long processing times)

## Privacy

- Only use documents you have permission to use
- Documents are processed locally
- No data is sent to external servers
- Extracted text is only used for training

