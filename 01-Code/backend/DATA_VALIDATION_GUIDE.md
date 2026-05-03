# Data Validation Workflow

## Overview

The Resume Tailor project includes a large dataset of real resumes in `C:\Projects\ResumeTailor\02-Data\`. **Before deploying or testing the AI features**, we need to validate that our parsing and AI extraction works correctly with this real-world data.

## Data Structure

### Available Data

```
02-Data/
├── UpdatedResumeDataSet.csv       # 2000+ resumes with categories
├── Resume.csv                      # Additional resume data
├── resume_data.csv                 # More resume samples
├── Resumes PDF/                    # PDF files organized by category
│   ├── Data Science/               # Data Science resumes
│   ├── Python Developer/           # Python developer resumes
│   ├── Java Developer/             # Java developer resumes
│   ├── HR/                         # HR resumes
│   └── ... (90+ categories)
└── why_resume_data_is_needed.md   # Documentation
```

### CSV Format

**UpdatedResumeDataSet.csv**:
- `Category`: Job category (Data Science, HR, etc.)
- `Resume`: Full resume text (already extracted)

## Validation Process

### Step 1: Validate CSV Parsing

Tests that we can read and process resume text from CSV files.

**What it checks**:
- CSV file is readable
- Resume text is not empty
- Text has minimum length (50 chars)
- Text structure is valid

**Run**:
```bash
cd c:\Projects\ResumeTailor\01-Code\backend
python validate_data.py
# Choose option 1
```

**Expected Output**:
```
Starting CSV validation...
Row 1 (Data Science): 1847 words, 11234 chars ✓
Row 2 (HR): 982 words, 5892 chars ✓
...
CSV validation complete: 10/10 successful
```

### Step 2: Validate PDF Parsing

Tests that we can extract text from actual PDF files.

**What it checks**:
- PDF files can be opened
- Text extraction works (pdfplumber/PyMuPDF)
- Extracted text has meaningful content
- Parser handles different PDF formats

**Run**:
```bash
python validate_data.py
# Choose option 2
# Enter category: "Data Science"
# Enter limit: 5
```

**Expected Output**:
```
Processing: DataScience_Resume_123.pdf
  ✓ Extracted 1500 words
Processing: DataScience_Resume_456.pdf
  ✓ Extracted 1200 words
...
PDF validation complete: 5/5 successful
```

### Step 3: Validate AI Extraction

Tests that OpenAI API successfully extracts skills, experience, and education.

**What it checks**:
- OpenAI API key is valid
- API connection works
- Skill extraction returns structured data
- Response matches expected schema
- Pydantic validation passes

**Prerequisites**:
- OpenAI API key in `.env` file
- `pip install openai pydantic-settings`

**Run**:
```bash
python validate_data.py
# Choose option 3
```

**Expected Output**:
```
Validating AI extraction on 3 samples
Sample 1: Extracting skills...
  ✓ Extracted: 15 skills, 3 experience, 2 education
Sample 2: Extracting skills...
  ✓ Extracted: 12 skills, 2 experience, 1 education
Sample 3: Extracting skills...
  ✓ Extracted: 18 skills, 4 experience, 2 education
AI validation complete: 3/3 successful
```

### Step 4: Load Sample Data to Database

Loads sample resumes into PostgreSQL database for end-to-end testing.

**What it does**:
- Reads resumes from CSV
- Creates database entries
- Returns resume IDs for testing

**Run**:
```bash
python validate_data.py
# Choose option 4
# Enter limit: 5
```

**Expected Output**:
```
Loading 5 sample resumes into database...
Loaded: Data Science_sample_1.txt (ID: 1)
Loaded: HR_sample_2.txt (ID: 2)
Loaded: Python Developer_sample_3.txt (ID: 3)
...
Successfully loaded 5 resumes into database
```

### Step 5: Full Validation Suite

Runs all validations in sequence (CSV → PDF → AI).

**Run**:
```bash
python validate_data.py
# Choose option 5
```

## Common Issues & Solutions

### Issue 1: CSV File Not Found

**Error**:
```
CSV file not found: C:\Projects\ResumeTailor\02-Data\UpdatedResumeDataSet.csv
```

**Solution**:
- Verify data folder exists
- Check file path is correct
- Ensure CSV file is present

### Issue 2: PDF Parsing Fails

**Error**:
```
  ✗ Failed: No text extracted from PDF
```

**Possible Causes**:
- PDF is image-based (no text layer)
- PDF is encrypted
- PDF has unusual encoding

**Solution**:
- Skip problematic PDFs (log them)
- Use OCR for image-based PDFs (future enhancement)
- Check PDF with PDF reader

### Issue 3: AI Extraction Fails

**Error**:
```
AI service initialization failed. Check OPENAI_API_KEY.
```

**Solution**:
1. Create `.env` file:
   ```bash
   copy .env.example .env
   ```

2. Add your OpenAI API key:
   ```
   OPENAI_API_KEY=sk-proj-your-key-here
   ```

3. Install dependencies:
   ```bash
   pip install openai==1.12.0 pydantic-settings==2.1.0
   ```

### Issue 4: Rate Limit Exceeded

**Error**:
```
  ✗ AI extraction failed: Rate limit exceeded
```

**Solution**:
- Wait 60 seconds
- Reduce validation sample size
- Check OpenAI usage limits

### Issue 5: Database Connection Failed

**Error**:
```
Failed to load resume: connection to server at "localhost" (::1), port 5432 failed
```

**Solution**:
- Start PostgreSQL service
- Verify database "resumetailor" exists
- Check connection string in `.env`

## Validation Metrics

### Success Criteria

| Validation Type | Target Success Rate | Acceptable Threshold |
|----------------|---------------------|----------------------|
| CSV Parsing | 100% | 95% |
| PDF Parsing | 90% | 80% (some PDFs may be image-based) |
| AI Extraction | 95% | 85% (API may have transient issues) |

### Interpretation

**CSV Parsing**: Should be near 100% as text is pre-extracted.

**PDF Parsing**: 80-90% is normal. Some PDFs are:
- Image scans (no text layer)
- Encrypted
- Corrupt

**AI Extraction**: 85-95% is expected. Failures may be:
- Network issues (retry)
- Rate limits (wait)
- Content policy violations (rare for resumes)

## Integration with Development Workflow

### When to Run Validation

1. **Initial Setup**: Before starting development
2. **After Parser Changes**: Whenever you modify resume_parser.py or jd_parser.py
3. **Before Deployment**: Final check before production
4. **Data Updates**: When adding new resume datasets

### Integration with Tests

The validation script can be integrated into pytest:

```python
# test_data_validation.py
import pytest
from validate_data import DataValidator

def test_csv_parsing():
    validator = DataValidator()
    results = validator.validate_csv_parsing(limit=10)
    assert results["parsing_success"] >= 9  # 90% success rate

def test_ai_extraction():
    validator = DataValidator()
    # Sample texts...
    results = validator.validate_ai_extraction(sample_texts)
    assert results["ai_extraction_success"] >= len(sample_texts) * 0.85
```

## Next Steps After Validation

Once validation passes:

1. **✅ CSV Parsing Validated** → Resume text extraction works
2. **✅ PDF Parsing Validated** → File upload flow is functional
3. **✅ AI Extraction Validated** → OpenAI integration is working
4. **✅ Sample Data Loaded** → Ready for end-to-end testing

### Next: End-to-End Testing

```bash
# Start server
uvicorn main:app --reload

# Test workflow:
# 1. Upload resume (auto AI extraction)
curl -X POST "http://localhost:8000/upload-resume/" -F "file=@resume.pdf"

# 2. Upload JD
curl -X POST "http://localhost:8000/upload-jd/" -F "file=@jd.pdf"

# 3. Gap analysis
curl -X POST "http://localhost:8000/gap-analysis/?resume_id=1&jd_id=1"

# 4. ATS score
curl -X POST "http://localhost:8000/ats-score/?resume_id=1&jd_id=1"
```

## Logging

Validation generates detailed logs:

**Console Output**: Real-time progress  
**Log File**: `data_validation.log` - Full details including errors

**Check logs**:
```bash
cat data_validation.log | grep "✗"  # Show failures
cat data_validation.log | grep "ERROR"  # Show errors
```

## Cost Considerations

AI validation calls OpenAI API. **Estimated costs**:

| Samples | Model | Cost |
|---------|-------|------|
| 10 resumes | GPT-4o-mini | ~$0.005 |
| 50 resumes | GPT-4o-mini | ~$0.025 |
| 100 resumes | GPT-4o-mini | ~$0.05 |

**Recommendation**: Start with 2-3 samples for initial validation.

## Summary

**Purpose**: Ensure parsing and AI extraction work with real data before production.

**Steps**:
1. Validate CSV parsing (quick)
2. Validate PDF parsing (medium)
3. Validate AI extraction (requires API key)
4. Load sample data

**Timeline**: 10-15 minutes for full validation

**Outcome**: Confidence that the system handles real-world resumes correctly.

---

**Ready to validate?** Run: `python validate_data.py`
