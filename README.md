# 📄 Resume Parser Website

A complete end-to-end web application that extracts structured information from resume files (PDF/DOCX) using Natural Language Processing and presents it in a clean, user-friendly interface.

![Project Status](https://img.shields.io/badge/status-active-success.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

---

## 🎯 Project Overview

This Resume Parser extracts key information from uploaded resumes including:
- **Personal Information**: Name, Email, Phone Number
- **Skills**: Technical and professional skills
- **Education**: Academic qualifications and institutions
- **Work Experience**: Employment history and responsibilities

### 🌟 Key Features

✅ **File Upload Support**: PDF and DOCX formats  
✅ **Intelligent Parsing**: Uses spaCy NLP + Regex patterns  
✅ **Clean UI**: Modern, responsive web interface  
✅ **Data Export**: Download as JSON or copy to clipboard  
✅ **Error Handling**: Comprehensive validation and user feedback  
✅ **Fast Processing**: Efficient text extraction and parsing  
✅ **Deployment Ready**: Configured for Render/Railway deployment  

---

## 🧱 Project Structure

```
resume-parser-website/
├── api/
│   └── api.py                 # FastAPI backend server
├── web/
│   ├── index.html            # Frontend HTML
│   ├── style.css             # Styling
│   └── script.js             # JavaScript logic
├── utils/
│   ├── extract_text.py       # Text extraction from PDF/DOCX
│   └── parse_resume.py       # NLP-based resume parsing
├── sample_resumes/           # Sample resume files
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

---

## ⚙️ Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **spaCy**: Industrial-strength NLP library
- **PyMuPDF (fitz)**: PDF text extraction
- **python-docx**: DOCX file processing
- **Uvicorn**: ASGI server for FastAPI

### Frontend
- **HTML5**: Structure
- **CSS3**: Modern styling with gradients and animations
- **Vanilla JavaScript**: API communication and DOM manipulation

### NLP Approach
- **Named Entity Recognition (NER)**: spaCy's `en_core_web_sm` model for extracting person names
- **Regular Expressions**: Pattern matching for emails and phone numbers
- **Keyword Matching**: Skills detection using predefined database
- **Section Detection**: Identifying Education and Experience sections

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone/Download the Project
```bash
cd /Users/alfiya/Desktop/grp\ project\ inter
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Download spaCy Model
```bash
python -m spacy download en_core_web_sm
```

### Step 4: Run the Backend Server
```bash
cd api
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

### Step 5: Open the Frontend
Simply open `web/index.html` in your browser, or use a local server:

```bash
# Using Python's built-in server
cd web
python -m http.server 3000
```

Then visit: `http://localhost:3000`

---

## 📖 Usage Guide

### 1. **Upload Resume**
   - Click the upload area or drag & drop a resume file
   - Supported formats: PDF, DOCX (max 10MB)

### 2. **Parse Resume**
   - Click "Parse Resume" button
   - Wait for processing (usually 2-5 seconds)

### 3. **View Results**
   - Extracted information displayed in organized sections
   - Personal info, skills, education, and experience

### 4. **Export Data**
   - **Download JSON**: Save parsed data as JSON file
   - **Copy Data**: Copy to clipboard for use elsewhere

---

## 🔌 API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. Upload and Parse Resume
```http
POST /upload
Content-Type: multipart/form-data

Parameters:
  file: Resume file (PDF or DOCX)

Response:
{
  "success": true,
  "filename": "john_doe_resume.pdf",
  "file_size": 245678,
  "extracted_data": {
    "name": "John Doe",
    "email": "john.doe@email.com",
    "phone": "+1-234-567-8900",
    "skills": ["Python", "JavaScript", "SQL"],
    "education": ["B.Sc Computer Science - XYZ University"],
    "experience": ["Software Engineer at ABC Corp"]
  }
}
```

#### 2. Health Check
```http
GET /health

Response:
{
  "status": "healthy"
}
```

#### 3. API Info
```http
GET /

Response:
{
  "message": "Resume Parser API",
  "version": "1.0.0",
  "endpoints": {...}
}
```

---

## 🧠 NLP Implementation Details

### Text Extraction
- **PDF**: PyMuPDF extracts text from each page
- **DOCX**: python-docx reads paragraphs sequentially

### Information Extraction

#### Name Detection
- Uses spaCy's NER to identify PERSON entities
- Focuses on first 1000 characters for efficiency

#### Email Extraction
```regex
\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b
```

#### Phone Number Extraction
```regex
\+?\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}
```

#### Skills Detection
- Maintains database of 50+ common technical skills
- Case-insensitive keyword matching
- Categories: Programming, Web, Databases, DevOps, ML

#### Education & Experience
- Section header detection
- Line-by-line parsing within sections
- Degree/institution keyword matching

---

## 🌐 Deployment

### Deploy on Render

1. **Create `render.yaml`**:
```yaml
services:
  - type: web
    name: resume-parser-api
    env: python
    buildCommand: pip install -r requirements.txt && python -m spacy download en_core_web_sm
    startCommand: uvicorn api.api:app --host 0.0.0.0 --port $PORT
```

2. Push to GitHub and connect to Render

### Deploy on Railway

1. **Create new project** on Railway
2. **Add build command**:
   ```bash
   pip install -r requirements.txt && python -m spacy download en_core_web_sm
   ```
3. **Add start command**:
   ```bash
   uvicorn api.api:app --host 0.0.0.0 --port $PORT
   ```

### Environment Variables
```env
PORT=8000
```

---

## 📸 Screenshots

### Upload Interface
![Upload Interface - Clean drag & drop area with file type indicators]

### Parsing in Progress
![Loading State - Progress indicator while processing]

### Results Display
![Parsed Results - Organized display of extracted information with skills tags and structured education/experience]

---

## ⚠️ Limitations & Considerations

### Current Limitations
- **Language**: Works best with English resumes
- **Format**: Optimized for standard resume formats
- **Accuracy**: NER accuracy depends on resume structure
- **Skills**: Limited to predefined skills database

### Recommended Resume Formats
- Clear section headers (Education, Experience, Skills)
- Standard fonts and formatting
- Non-scanned documents (no image-based PDFs)
- Properly formatted contact information

---

## 🎁 Bonus Feature: Job Description Matcher (Optional)

To implement job description matching:

1. **Add endpoint** to accept job description
2. **Extract required skills** from job description
3. **Calculate match percentage**:
   ```python
   match_score = (len(candidate_skills & job_skills) / len(job_skills)) * 100
   ```
4. **Display compatibility score** in frontend

---

## 🛠️ Troubleshooting

### Backend won't start
```bash
# Check if port 8000 is in use
lsof -i :8000

# Use different port
uvicorn api.api:app --port 8001
```

### spaCy model not found
```bash
python -m spacy download en_core_web_sm
```

### CORS errors
- Ensure backend CORS middleware is enabled
- Check API_URL in `script.js` matches backend

### File upload fails
- Check file size (<10MB)
- Verify file format (PDF/DOCX)
- Ensure file is not password-protected

---

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Add more skills to database
- Improve section detection algorithms
- Support for more languages
- Better entity extraction
- Additional file format support

---

## 📝 License

This project is created for educational/internship purposes.

---

## 👨‍💻 Author

Created as an internship project demonstrating:
- Full-stack development skills
- API design and implementation
- NLP and text processing
- Modern web development practices

---

## 📞 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review API documentation
3. Verify all dependencies are installed
4. Ensure backend server is running

---

## 🎯 Future Enhancements

- [ ] Multi-language support
- [ ] Advanced ML-based parsing
- [ ] Resume scoring system
- [ ] Batch processing
- [ ] Database integration
- [ ] User authentication
- [ ] Resume comparison tool
- [ ] Export to other formats (CSV, XML)

---

**Built with ❤️ using FastAPI, spaCy, and Modern Web Technologies**
# grp-project-inter-
