"""
FastAPI Backend for Resume Parser
Handles file uploads and returns parsed resume data
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import sys
from pathlib import Path

# Add utils directory to path
sys.path.append(str(Path(__file__).parent.parent))

from utils.extract_text import extract_text
from utils.parse_resume import parse_resume


app = FastAPI(
    title="Resume Parser API",
    description="API for parsing resumes and extracting structured information",
    version="1.0.0"
)

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads directory if it doesn't exist
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'.pdf', '.docx'}


def validate_file_extension(filename: str) -> bool:
    """
    Validate file extension
    
    Args:
        filename: Name of the uploaded file
        
    Returns:
        True if valid, False otherwise
    """
    ext = os.path.splitext(filename)[1].lower()
    return ext in ALLOWED_EXTENSIONS


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Resume Parser API",
        "version": "1.0.0",
        "endpoints": {
            "/upload": "POST - Upload and parse resume",
            "/health": "GET - Health check"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    """
    Upload and parse resume file
    
    Args:
        file: Uploaded file (PDF or DOCX)
        
    Returns:
        JSON with parsed resume data
    """
    # Validate file extension
    if not validate_file_extension(file.filename):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file format. Only PDF and DOCX files are allowed. Got: {file.filename}"
        )
    
    # Validate file size (max 10MB)
    file_size = 0
    temp_file_path = None
    
    try:
        # Save uploaded file temporarily
        temp_file_path = UPLOAD_DIR / file.filename
        
        with open(temp_file_path, "wb") as buffer:
            content = await file.read()
            file_size = len(content)
            
            if file_size > 10 * 1024 * 1024:  # 10MB limit
                raise HTTPException(
                    status_code=400,
                    detail="File size exceeds 10MB limit"
                )
            
            buffer.write(content)
        
        # Extract text from file
        try:
            text = extract_text(str(temp_file_path))
        except Exception as e:
            raise HTTPException(
                status_code=422,
                detail=f"Unable to extract text from file: {str(e)}"
            )
        
        # Check if text was extracted
        if not text or len(text.strip()) < 10:
            raise HTTPException(
                status_code=422,
                detail="No readable text found in the file. Please ensure the file is not corrupted or password-protected."
            )
        
        # Parse resume
        try:
            parsed_data = parse_resume(text)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error parsing resume: {str(e)}"
            )
        
        # Add metadata
        response_data = {
            "success": True,
            "filename": file.filename,
            "file_size": file_size,
            "extracted_data": parsed_data
        }
        
        return JSONResponse(content=response_data)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )
    
    finally:
        # Clean up temporary file
        if temp_file_path and temp_file_path.exists():
            try:
                os.remove(temp_file_path)
            except Exception as e:
                print(f"Warning: Could not delete temporary file {temp_file_path}: {e}")


@app.delete("/cleanup")
async def cleanup_uploads():
    """
    Clean up all uploaded files (admin endpoint)
    """
    try:
        count = 0
        for file_path in UPLOAD_DIR.glob("*"):
            if file_path.is_file():
                os.remove(file_path)
                count += 1
        
        return {"message": f"Cleaned up {count} files"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error during cleanup: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
