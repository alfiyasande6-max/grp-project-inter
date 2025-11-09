# Testing Guide

## 🧪 Testing Your Resume Parser

### Manual Testing Checklist

#### ✅ Backend Tests

1. **Server Startup**
   ```bash
   cd api
   uvicorn api:app --reload
   ```
   - [ ] Server starts without errors
   - [ ] Visit http://localhost:8000 shows API info
   - [ ] Visit http://localhost:8000/docs shows Swagger UI

2. **Health Check**
   ```bash
   curl http://localhost:8000/health
   ```
   Expected: `{"status":"healthy"}`

3. **File Upload (Using curl)**
   ```bash
   curl -X POST "http://localhost:8000/upload" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@path/to/resume.pdf"
   ```
   - [ ] Returns JSON with extracted data
   - [ ] No errors in console

#### ✅ Frontend Tests

1. **Page Load**
   - [ ] Open `web/index.html` in browser
   - [ ] No console errors
   - [ ] UI displays correctly
   - [ ] Upload area is visible

2. **File Upload UI**
   - [ ] Click upload area opens file dialog
   - [ ] Drag and drop works
   - [ ] File validation works (try .txt file - should fail)
   - [ ] File size validation (try >10MB - should fail)

3. **Parse Functionality**
   - [ ] Upload valid PDF resume
   - [ ] Click "Parse Resume"
   - [ ] Loading indicator appears
   - [ ] Results display after parsing
   - [ ] All sections show data

4. **Data Export**
   - [ ] Click "Download JSON" downloads file
   - [ ] Click "Copy Data" shows success message
   - [ ] Pasted data is valid JSON

#### ✅ Error Handling Tests

1. **Invalid File Types**
   - [ ] Upload .txt file → shows error
   - [ ] Upload .jpg file → shows error

2. **Large Files**
   - [ ] Upload >10MB file → shows error

3. **Backend Offline**
   - [ ] Stop backend server
   - [ ] Try to parse → shows connection error

4. **Corrupted Files**
   - [ ] Upload corrupted PDF → shows extraction error

### Test Cases

#### Test Case 1: Standard Resume
**Input:** Resume with all sections  
**Expected Output:**
- Name extracted
- Email extracted
- Phone extracted
- Skills list populated
- Education entries present
- Experience entries present

#### Test Case 2: Minimal Resume
**Input:** Resume with only name and email  
**Expected Output:**
- Name and email extracted
- Other fields show "Not detected"
- No errors thrown

#### Test Case 3: Skills-Heavy Resume
**Input:** Resume listing 20+ skills  
**Expected Output:**
- Most skills detected
- Skills displayed as tags
- No duplicates

#### Test Case 4: PDF vs DOCX
**Input:** Same resume in both formats  
**Expected Output:**
- Both extract same information
- No format-specific errors

### Performance Tests

1. **Small File (< 100KB)**
   - [ ] Parses in < 3 seconds

2. **Medium File (100KB - 1MB)**
   - [ ] Parses in < 5 seconds

3. **Large File (1MB - 10MB)**
   - [ ] Parses in < 10 seconds

### Browser Compatibility

Test in multiple browsers:
- [ ] Chrome/Chromium
- [ ] Firefox
- [ ] Safari
- [ ] Edge

### Sample Test Resume

Create a test resume with this content:

```
Jane Smith
Full Stack Developer

Contact Information:
Email: jane.smith@example.com
Phone: +1-555-123-4567

TECHNICAL SKILLS
Python, JavaScript, React, Node.js, FastAPI, Django, PostgreSQL, 
MongoDB, Docker, Kubernetes, AWS, Git, HTML, CSS, TypeScript

EDUCATION
Master of Science in Computer Science
Stanford University, 2020-2022

Bachelor of Engineering in Software Engineering  
MIT, 2016-2020

PROFESSIONAL EXPERIENCE

Senior Software Engineer
Google, Mountain View, CA
July 2022 - Present
- Led development of microservices architecture using FastAPI and Docker
- Implemented CI/CD pipelines reducing deployment time by 60%
- Mentored junior developers and conducted code reviews

Software Developer
Microsoft, Redmond, WA  
June 2020 - June 2022
- Developed scalable web applications using React and Node.js
- Optimized database queries improving response time by 45%
- Collaborated with product team on feature planning
```

### Automated Testing (Optional)

Create `test_api.py`:

```python
import pytest
from fastapi.testclient import TestClient
from api.api import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_upload_invalid_file():
    files = {"file": ("test.txt", b"test content", "text/plain")}
    response = client.post("/upload", files=files)
    assert response.status_code == 400

def test_upload_no_file():
    response = client.post("/upload")
    assert response.status_code == 422
```

Run with:
```bash
pip install pytest
pytest test_api.py
```

### Troubleshooting Common Issues

| Issue | Solution |
|-------|----------|
| Import errors | Run `pip install -r requirements.txt` |
| spaCy model not found | Run `python -m spacy download en_core_web_sm` |
| Port already in use | Change port in uvicorn command |
| CORS errors | Ensure backend is running first |
| No data extracted | Check resume format and content |

### Success Criteria

Your resume parser is working correctly if:
- ✅ Backend starts without errors
- ✅ Frontend loads properly
- ✅ Can upload PDF and DOCX files
- ✅ Extracts at least 3 out of 6 data fields
- ✅ Displays results in organized format
- ✅ Can download JSON
- ✅ Error messages display for invalid inputs

### Deployment Testing

After deploying to Render/Railway:

1. **Verify API Endpoint**
   ```bash
   curl https://your-api.render.com/health
   ```

2. **Update Frontend**
   - Change `API_URL` in `script.js` to deployed URL

3. **Test End-to-End**
   - Upload resume through deployed frontend
   - Verify parsing works
   - Check response times

### Reporting Issues

If you find bugs, note:
1. Steps to reproduce
2. Expected behavior
3. Actual behavior
4. Error messages
5. Browser/environment details

---

Happy Testing! 🧪
