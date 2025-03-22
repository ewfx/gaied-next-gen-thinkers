import imaplib
import email
from email.policy import default
from bs4 import BeautifulSoup
from transformers import pipeline
import os
import pdfplumber
import pytesseract
from PIL import Image
import docx
import io
from classification_prompt import classify_request_type



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

from google import genai

classification_data = classify_request_type()
def classify_email(subject, body, attachment_text):
    client = genai.Client(api_key="AIzaSyBgD85PrdkN2M8bFQA0HYOreAFkc_Z-TSA")
    combined_text = f"Subject: {subject}\nBody: {body}\nAttachments: {attachment_text}"
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=f"""Read the content below and classify the content based on the given classifications. 

    {classification_data}
    Also provide the confidence score for each classification.

    Content: Subject: {subject}\nBody: {body}\nAttachments: {attachment_text} Use this JSON schema for output: Information= {{'date': str, 'time': str, 'pnr': str, 'departure': str, 'arrival': str}}
    Provide output in JSON format with confidence score and reasoning.""")
    print("nextGenThinkers",response.text)

# Gmail IMAP credentials
EMAIL = "nextgenthinkers2025@gmail.com"  # Replace with your email "jagadeesh.soppimat@gmail.com","nextgenthinkers2025@gmail.com"
PASSWORD = "whvh mirp guwi yquu"  # Use App Password if needed "wiax ixav dqzz xzif", "whvh mirp guwi yquu"
IMAP_SERVER = "imap.gmail.com"  # Change if using Outlook/Yahoo

# Connect to IMAP server
mail = imaplib.IMAP4_SSL(IMAP_SERVER)
mail.login(EMAIL, PASSWORD)
mail.select("inbox")

# Fetch unread emails
status, email_ids = mail.search(None, "UNSEEN") # "UNSEEN"
email_ids = email_ids[0].split()

for email_id in email_ids:
    status, data = mail.fetch(email_id, "(RFC822)")
    raw_email = data[0][1]
    msg = email.message_from_bytes(raw_email, policy=default)

    # Extract subject and body
    subject = msg["subject"] or ""
    sender = msg["from"]
    body = ""
    attachment_text = ""

    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            if "attachment" in content_disposition:
                attachment_text += process_attachment(part) + "\n"
            elif content_type == "text/html":
                body += extract_plain_text(part.get_payload(decode=True).decode(errors="ignore")) + "\n"
            elif content_type == "text/plain":
                body += part.get_payload(decode=True).decode(errors="ignore") + "\n"
    else:
        body = extract_plain_text(msg.get_payload(decode=True).decode(errors="ignore"))

    # Classify email based on subject, body, and attachments
    classification = classify_email(subject, body, attachment_text)
    
    print(f"\n📧 Email Subject: {subject}")
    print(f"📩 From: {sender}")
    print(f"📜 Message:\n{body}")
    print(f"📜 attachment_text:\n{attachment_text}")
    # print(f"🔍 Email Classified as: {classification}")
    print("-" * 50)

# Close IMAP connection
mail.logout()
