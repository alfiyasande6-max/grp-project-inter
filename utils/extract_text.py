"""
Text Extraction Module
Extracts text from PDF and DOCX files
"""

import fitz  # PyMuPDF
from docx import Document
import os


def extract_text_from_pdf(file_path):
    """
    Extract text from PDF file using PyMuPDF
    
    Args:
        file_path: Path to the PDF file
        
    Returns:
        Extracted text as string
    """
    try:
        text = ""
        pdf_document = fitz.open(file_path)
        
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            text += page.get_text()
        
        pdf_document.close()
        return text
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")


def extract_text_from_docx(file_path):
    """
    Extract text from DOCX file using python-docx
    
    Args:
        file_path: Path to the DOCX file
        
    Returns:
        Extracted text as string
    """
    try:
        doc = Document(file_path)
        text = ""
        
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        
        return text
    except Exception as e:
        raise Exception(f"Error extracting text from DOCX: {str(e)}")


def extract_text(file_path):
    """
    Extract text based on file extension
    
    Args:
        file_path: Path to the file
        
    Returns:
        Extracted text as string
    """
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()
    
    if ext == '.pdf':
        return extract_text_from_pdf(file_path)
    elif ext == '.docx':
        return extract_text_from_docx(file_path)
    else:
        raise ValueError(f"Unsupported file format: {ext}")
