# System Architecture

## 🏗️ High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         USER                                 │
│                    (Web Browser)                             │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND LAYER                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  index.html - UI Structure                            │  │
│  │  style.css  - Visual Design                           │  │
│  │  script.js  - Client Logic & API Communication        │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ HTTP POST /upload
                         │ (multipart/form-data)
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                     BACKEND LAYER                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              FastAPI Application                      │  │
│  │              (api/api.py)                             │  │
│  │                                                        │  │
│  │  • File Upload Handler                                │  │
│  │  • Validation Logic                                   │  │
│  │  • Response Formatter                                 │  │
│  └────────────┬────────────────────┬────────────────────┘  │
└───────────────┼────────────────────┼────────────────────────┘
                │                    │
                ▼                    ▼
┌───────────────────────┐  ┌────────────────────────────────┐
│  TEXT EXTRACTION      │  │    NLP PROCESSING              │
│  (utils/extract_text) │  │    (utils/parse_resume)        │
│                       │  │                                │
│  • PDF → Text         │  │  • Name Extraction (NER)       │
│  • DOCX → Text        │  │  • Email Detection (Regex)     │
│  • Error Handling     │  │  • Phone Extraction (Regex)    │
│                       │  │  • Skills Matching             │
│                       │  │  • Section Parsing             │
└───────────────────────┘  └────────────────────────────────┘
                │                    │
                └────────┬───────────┘
                         │
                         ▼
                 ┌───────────────┐
                 │  JSON Response │
                 └───────────────┘
```

## 🔄 Data Flow

### 1. Upload Phase
```
User → Select File → Validate (Frontend) → Enable Parse Button
```

### 2. Processing Phase
```
Parse Button Click
    ↓
Create FormData with file
    ↓
POST request to /upload
    ↓
Backend receives file
    ↓
Save to temporary location
    ↓
Determine file type (.pdf or .docx)
    ↓
Extract text using appropriate library
    ↓
Pass text to NLP parser
    ↓
Extract structured information
    ↓
Format as JSON response
    ↓
Delete temporary file
    ↓
Return JSON to frontend
```

### 3. Display Phase
```
Frontend receives JSON
    ↓
Parse response data
    ↓
Update DOM elements
    ↓
Display in organized sections
    ↓
Enable export options
```

## 🧩 Component Details

### Frontend Components

#### 1. Upload Component
- **Responsibility**: File selection and validation
- **Files**: index.html, script.js, style.css
- **Features**:
  - Drag & drop
  - Click to browse
  - File type validation
  - Size validation

#### 2. Parse Component
- **Responsibility**: Trigger parsing and show loading
- **Files**: script.js, style.css
- **Features**:
  - Loading animation
  - Error handling
  - Progress indication

#### 3. Results Component
- **Responsibility**: Display parsed data
- **Files**: index.html, script.js, style.css
- **Features**:
  - Structured layout
  - Skill tags
  - List formatting

#### 4. Export Component
- **Responsibility**: Data export functionality
- **Files**: script.js
- **Features**:
  - JSON download
  - Clipboard copy
  - Success feedback

### Backend Components

#### 1. API Layer (api/api.py)
```python
FastAPI App
├── Middleware (CORS)
├── Endpoints
│   ├── GET  /          (API info)
│   ├── GET  /health    (Health check)
│   └── POST /upload    (Main processing)
└── Error Handlers
```

#### 2. Text Extraction (utils/extract_text.py)
```python
extract_text()
├── extract_text_from_pdf()
│   └── Uses PyMuPDF (fitz)
└── extract_text_from_docx()
    └── Uses python-docx
```

#### 3. Resume Parser (utils/parse_resume.py)
```python
parse_resume()
├── extract_name()        (spaCy NER)
├── extract_email()       (Regex)
├── extract_phone()       (Regex)
├── extract_skills()      (Keyword matching)
├── extract_education()   (Section parsing)
└── extract_experience()  (Section parsing)
```

## 📦 Module Dependencies

```
api/api.py
    ├── fastapi
    ├── utils/extract_text
    └── utils/parse_resume

utils/extract_text.py
    ├── PyMuPDF (fitz)
    └── python-docx

utils/parse_resume.py
    ├── spacy
    └── re (regex)

web/script.js
    └── fetch API (browser native)
```

## 🔐 Security Layers

```
┌─────────────────────────────┐
│  Frontend Validation        │
│  • File type check          │
│  • Size check               │
└────────────┬────────────────┘
             ▼
┌─────────────────────────────┐
│  Backend Validation         │
│  • Extension verification   │
│  • Size limit enforcement   │
│  • MIME type check          │
└────────────┬────────────────┘
             ▼
┌─────────────────────────────┐
│  File Processing            │
│  • Temporary storage        │
│  • Automatic cleanup        │
│  • Error handling           │
└─────────────────────────────┘
```

## 💾 Data Storage

### Temporary Storage
```
uploads/
├── [filename].pdf   (during processing)
└── [filename].docx  (during processing)

Note: Files are deleted immediately after processing
```

### No Persistent Storage
- No database
- No user data retention
- Stateless operation
- Privacy-focused

## 🌐 API Architecture

### Request Format
```
POST /upload HTTP/1.1
Host: localhost:8000
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary
Content-Length: [length]

------WebKitFormBoundary
Content-Disposition: form-data; name="file"; filename="resume.pdf"
Content-Type: application/pdf

[PDF binary data]
------WebKitFormBoundary--
```

### Response Format
```json
{
  "success": true,
  "filename": "resume.pdf",
  "file_size": 245678,
  "extracted_data": {
    "name": "John Doe",
    "email": "john@email.com",
    "phone": "+1-234-567-8900",
    "skills": ["Python", "JavaScript"],
    "education": ["B.Sc Computer Science"],
    "experience": ["Software Engineer at ABC"]
  }
}
```

## ⚡ Performance Optimization

### Frontend
- Minimal dependencies (vanilla JS)
- CSS animations (GPU accelerated)
- Async file reading
- Debounced events

### Backend
- Async request handling
- Limited text processing (first 2000 chars for NER)
- Efficient regex patterns
- Immediate file cleanup

## 🚀 Deployment Architecture

### Local Development
```
localhost:8000 (Backend)
    ↕
localhost:3000 (Frontend)
```

### Production (Render/Railway)
```
https://your-api.render.com (Backend)
    ↕
https://your-frontend.netlify.com (Frontend)
```

## 🔧 Configuration

### Environment Variables
```bash
# Backend
PORT=8000
PYTHON_VERSION=3.11.0

# Frontend (in script.js)
API_URL=http://localhost:8000
```

## 📊 Processing Pipeline

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  Upload  │ → │ Extract  │ → │  Parse   │ → │  Return  │
│   File   │    │   Text   │    │   NLP    │    │   JSON   │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
     │               │                │               │
   Validate       PDF/DOCX        spaCy/Regex    Structured
   Format         Libraries       Processing      Data
```

## 🎯 Design Patterns

1. **Separation of Concerns**
   - Frontend: UI only
   - Backend: Business logic
   - Utils: Reusable functions

2. **Modularity**
   - Each component has single responsibility
   - Easy to test and maintain

3. **Error Handling**
   - Try-catch blocks
   - User-friendly messages
   - Graceful degradation

4. **Stateless Design**
   - No session management
   - Each request independent
   - Easy to scale

---

This architecture ensures:
- **Scalability**: Easy to add features
- **Maintainability**: Clear structure
- **Performance**: Optimized processing
- **Security**: Multiple validation layers
- **Reliability**: Comprehensive error handling
