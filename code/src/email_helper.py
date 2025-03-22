import imaplib
import os
from bs4 import BeautifulSoup
import pdfplumber
import pytesseract
from PIL import Image
import docx
import io

def extract_plain_text(html_content):
    """Convert HTML email content to plain text."""
    soup = BeautifulSoup(html_content, "html.parser")
    return soup.get_text(separator=" ", strip=True)

def extract_pdf_text(pdf_bytes):
    """Extract text from a PDF file."""
    text = ""
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text.strip()

def extract_doc_text(doc_bytes):
    """Extract text from a Word document."""
    doc = docx.Document(io.BytesIO(doc_bytes))
    return "\n".join([para.text for para in doc.paragraphs])

def extract_image_text(image_bytes):
    """Extract text from an image using OCR (Tesseract)."""
    image = Image.open(io.BytesIO(image_bytes))
    return pytesseract.image_to_string(image)

def process_attachment(part):
    """Extract text from attachments like PDFs, DOCX, Images."""
    filename = part.get_filename()
    content_type = part.get_content_type()
    payload = part.get_payload(decode=True)

    if not filename or not payload:
        return ""

    text = ""
    if content_type == "application/pdf":
        text = extract_pdf_text(payload)
    elif content_type in ["application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        text = extract_doc_text(payload)
    elif content_type.startswith("image/"):
        text = extract_image_text(payload)
    
    return text