# Quick Start Guide

## ⚡ Get Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### Step 2: Start Backend
```bash
cd api
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

Keep this terminal running. The API will be at http://localhost:8000

### Step 3: Open Frontend
Open `web/index.html` in your browser, or:
```bash
cd web
python -m http.server 3000
```
Visit http://localhost:3000

## 🎯 Usage
1. Upload a resume (PDF/DOCX)
2. Click "Parse Resume"
3. View extracted information
4. Download as JSON or copy data

## 🔧 Troubleshooting

### Port already in use?
```bash
uvicorn api.api:app --port 8001
```
Update API_URL in `web/script.js` to match

### CORS errors?
Make sure backend is running before opening frontend

### Module not found?
```bash
pip install -r requirements.txt
```

## 📚 Full Documentation
See `README.md` for complete details
