# AI Contract Analyzer - Technical Explanation

## Risk Scoring Formula

### Clause-Level Risk Score

The system calculates risk scores for individual clauses using either ML-based or rule-based analysis.

#### ML-Based Scoring

When using the ML model (`ML_MODE=ml`):

1. **Model Prediction**: The DistilBERT model outputs probabilities for three classes: LOW, MEDIUM, HIGH
2. **Score Mapping**:
   - **HIGH risk**: `risk_score = model_probability * 100` (0-100 range)
   - **MEDIUM risk**: `risk_score = 50 + (model_probability * 30)` (50-80 range)
   - **LOW risk**: `risk_score = model_probability * 20` (0-20 range)
3. **Normalization**: Scores are clamped to 0-100 range

#### Rule-Based Scoring

When using rule-based analysis (`ML_MODE=rules`):

1. **Keyword Matching**: Count occurrences of high-risk and medium-risk keywords
2. **Score Calculation**:
   - **HIGH**: 75-100 points (2+ high-risk keywords, or 1+ with long clause)
   - **MEDIUM**: 30-80 points (1+ high-risk or 3+ medium-risk keywords)
   - **LOW**: 10-20 points (few or no risk keywords)
3. **Adjustments**: Longer clauses with risk keywords get higher scores

### Global Document Risk Score

The global score aggregates clause-level scores using weighted averaging:

```
global_score = Σ(clause_score * clause_weight) / Σ(clause_weight)
```

**Weight Calculation**:
- **Base weights**:
  - HIGH risk clauses: 2.0x
  - MEDIUM risk clauses: 1.5x
  - LOW risk clauses: 1.0x
- **Severity multiplier**: Clauses containing high-severity keywords (liability, penalty, indemnify, damages, breach) get an additional 1.3x multiplier

**Example**:
- Clause 1: HIGH risk, score 85, contains "liability" → weight = 2.0 * 1.3 = 2.6
- Clause 2: MEDIUM risk, score 50 → weight = 1.5
- Clause 3: LOW risk, score 15 → weight = 1.0

Global score = (85 * 2.6 + 50 * 1.5 + 15 * 1.0) / (2.6 + 1.5 + 1.0) = 60.2

## Clause Segmentation

The system uses heuristic-based segmentation:

1. **Paragraph Splitting**: Split by double newlines
2. **Clause Markers**: Identify clauses starting with:
   - Numbered/bulleted lists (1., 2., a., b.)
   - Legal markers (WHEREAS, THEREFORE, NOW THEREFORE, IN CONSIDERATION)
   - Agreement phrases (THE PARTIES AGREE)
3. **Sentence Boundaries**: Split by sentence endings after keywords (shall, must, will, agrees, warrants)
4. **Fallback**: If no clauses found, split by sentences

## ML Training Pipeline

### Data Format

CSV with columns:
- `doc_id`: Document identifier
- `clause_text`: The clause text
- `label`: Risk label (LOW, MEDIUM, HIGH)
- `explanation`: Optional explanation

### Training Process

1. **Data Loading**: Load and validate CSV
2. **Preprocessing**: Clean text, map labels to integers
3. **Tokenization**: Use DistilBERT tokenizer (max length 512)
4. **Model**: Fine-tune DistilBERT with 3-class classification head
5. **Training**: Train for N epochs with learning rate 2e-5
6. **Evaluation**: Calculate accuracy, precision, recall, F1-score
7. **Saving**: Save model, tokenizer, and label mappings

### Model Architecture

- **Base**: DistilBERT (distilbert-base-uncased)
- **Head**: Linear classification layer (768 → 3)
- **Output**: Logits for LOW, MEDIUM, HIGH

## Rule-Based Fallback

When ML model is unavailable, the system uses keyword-based analysis:

### High-Risk Keywords
- unlimited liability, sole discretion, without limitation
- indemnify, hold harmless, penalty, liquidated damages
- automatic renewal, binding arbitration, waiver of rights
- exclusive jurisdiction, no refund, as-is, no warranty
- force majeure, termination without cause, confidentiality breach

### Medium-Risk Keywords
- termination, breach, default, remedy, dispute
- governing law, jurisdiction, assignment, modification
- severability, entire agreement, notices

### Scoring Logic
- Count keyword matches
- Apply thresholds for risk level assignment
- Adjust scores based on clause length and keyword density

## Mitigation Suggestions

The system generates mitigation suggestions based on risk level:

- **HIGH**: "Consider revising to limit liability, add exceptions, or include mutual obligations. Consult legal counsel."
- **MEDIUM**: "Review for clarity and ensure terms are balanced. Consider adding specific conditions or limitations."
- **LOW**: "This clause appears acceptable, but always review with legal counsel for your specific context."

## Manual Steps & TODOs

### Initial Setup

1. **Environment Configuration**:
   - Copy `.env.example` to `.env` in backend directory
   - Update API keys and paths as needed
   - Set `ML_MODE=rules` if you don't have a trained model yet

2. **Database Initialization**:
   - Database is auto-created on first run
   - Tables are created automatically via SQLAlchemy
   - For production, consider using PostgreSQL instead of SQLite

3. **ML Model Training** (Optional):
   ```bash
   # Generate sample data
   cd ml_data
   python generate_sample_data.py --output training_data.csv --samples 100
   
   # Train model
   cd ../backend
   python -m app.ml.train --data ../ml_data/training_data.csv --output ./models/risk_classifier --epochs 5
   ```

### Production Deployment

1. **Security**:
   - [ ] Set strong `API_KEY` in environment
   - [ ] Enable HTTPS/TLS
   - [ ] Configure CORS properly for production domain
   - [ ] Set up rate limiting
   - [ ] Add authentication/authorization

2. **Database**:
   - [ ] Migrate from SQLite to PostgreSQL/MySQL
   - [ ] Set up database backups
   - [ ] Configure connection pooling

3. **ML Model**:
   - [ ] Train on real contract data
   - [ ] Fine-tune hyperparameters
   - [ ] Set up model versioning
   - [ ] Implement A/B testing for model updates

4. **Monitoring**:
   - [ ] Add logging aggregation (e.g., ELK stack)
   - [ ] Set up error tracking (e.g., Sentry)
   - [ ] Configure health checks and alerts
   - [ ] Monitor API performance

5. **Scaling**:
   - [ ] Use container orchestration (Kubernetes)
   - [ ] Set up load balancing
   - [ ] Configure auto-scaling
   - [ ] Use CDN for frontend assets

### Testing

1. **Unit Tests**:
   - [ ] Add more test cases for edge cases
   - [ ] Test file upload with various formats
   - [ ] Test clause segmentation with different document structures

2. **Integration Tests**:
   - [ ] Test full upload → extract → analyze pipeline
   - [ ] Test with real PDF/DOCX files
   - [ ] Test error handling and recovery

3. **Performance Tests**:
   - [ ] Load testing for API endpoints
   - [ ] Test with large documents
   - [ ] Benchmark ML inference time

### Future Enhancements

1. **Features**:
   - [ ] Add document comparison (diff analysis)
   - [ ] Support for more file formats (ODT, RTF)
   - [ ] Export analysis to PDF/Word reports
   - [ ] Batch processing for multiple documents
   - [ ] Custom risk categories and rules

2. **ML Improvements**:
   - [ ] Fine-tune on domain-specific contracts
   - [ ] Add explainability (SHAP, LIME)
   - [ ] Implement active learning for model improvement
   - [ ] Add clause rewriting suggestions using LLMs

3. **UI/UX**:
   - [ ] Add dark mode
   - [ ] Improve mobile responsiveness
   - [ ] Add real-time analysis progress
   - [ ] Implement document preview

## Assumptions

1. **Document Format**: Assumes standard contract structure with clear clause boundaries
2. **Language**: Currently optimized for English contracts
3. **Risk Categories**: Three-level classification (LOW, MEDIUM, HIGH) - can be extended
4. **Model Size**: Uses DistilBERT for faster inference - can upgrade to larger models
5. **Storage**: Local file storage for uploads - should use cloud storage in production
6. **Database**: SQLite for development - should use production-grade DB in production

## Known Limitations

1. **Clause Segmentation**: Heuristic-based segmentation may not work perfectly for all document formats
2. **ML Model**: Trained on synthetic data - needs real-world data for production use
3. **Language Support**: English only
4. **File Size**: Limited by `MAX_UPLOAD_SIZE_MB` (default 10MB)
5. **Concurrent Processing**: Single-threaded processing - may need queue system for scale

## Troubleshooting

### Model Not Loading
- Check `MODEL_PATH` in config
- Ensure model files exist (config.json, pytorch_model.bin, tokenizer files)
- Try `ML_MODE=rules` as fallback

### Poor Segmentation
- Adjust heuristics in `app/services/extract.py`
- Consider using NLP libraries (spaCy) for better sentence/clause detection

### Low Accuracy
- Train on more diverse, real-world data
- Increase training epochs
- Fine-tune hyperparameters
- Consider larger base model

