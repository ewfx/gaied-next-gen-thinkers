import imaplib
import email
from email.policy import default
from bs4 import BeautifulSoup
from transformers import pipeline
import os
import pdfplumber
import pytesseract
from PIL import Image
import json
import docx
import io
from google import genai
import asyncio
import websockets

# Gmail IMAP credentials
EMAIL = "nextgenthinkers2025@gmail.com"  # Replace with your email "jagadeesh.soppimat@gmail.com","nextgenthinkers2025@gmail.com"
PASSWORD = "whvh mirp guwi yquu"  # Use App Password if needed "wiax ixav dqzz xzif", "whvh mirp guwi yquu"
IMAP_SERVER = "imap.gmail.com"  # Change if using Outlook/Yahoo

# Connect to IMAP server
mail = imaplib.IMAP4_SSL(IMAP_SERVER)
mail.login(EMAIL, PASSWORD)
mail.select("inbox")

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

def classify_email(subject, body, attachment_text):
    client = genai.Client(api_key="AIzaSyBgD85PrdkN2M8bFQA0HYOreAFkc_Z-TSA")
    combined_text = f"Subject: {subject}\nBody: {body}\nAttachments: {attachment_text}"
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=f"""Read the content below and classify the content based on the given classifications. 

    Classifications: [Access Request, Finance, HR Request, Vacation, IT Support Request, Travel Plan, Change Request, Engineering, Leave Request]

    Also provide the confidence score for each classification.

    Content: Subject: {subject}\nBody: {body}\nAttachments: {attachment_text} Use this JSON schema for output: Information= {{'date': str, 'time': str, 'pnr': str, 'departure': str, 'arrival': str}}
    Provide output in JSON format with confidence score and reasoning.""")
    json_response = response.text.split("```json")[1].strip().split("```")[0].strip()
    print(json_response)
    return json_response 

    merged_prompt = f"""Read the content below and classify the content based on the given classifications. 

    {classification_data}
    Also provide the confidence score for each classification.
    
    **Content to Analyze:**
    Subject: {subject}
    Body: {body}
    Attachments: {attachment_text}

    **Output JSON Format:**
    {{
    "request_types": [
        {{
        "type": "[Classification Type]",
        "subtype": "[Classification Subtype]",
        "confidence_score": [Confidence Score between 0.0-1.0],
        "reasoning": "[Explanation for classification]"
        }}
        // Add more types/subtypes if applicable
    ],
    "extracted_information": {{
        "date": "[Extracted Date in YYYY-MM-DD format or 'Not Found']",
        "time": "[Extracted Time in HH:MM format or 'Not Found']",
        "pnr": "[Extracted PNR number or 'Not Found']",
        "departure": "[Extracted Departure location or 'Not Found']",
        "arrival": "[Extracted Arrival location or 'Not Found']",
        "amount": "[Extracted Amount or 'Not Found']",
        "transaction_id": "[Extracted Transaction ID or 'Not Found']",
        "loan_number": "[Extracted Loan Number or 'Not Found']",
        "account_number": "[Extracted Account Number or 'Not Found']",
        "expiration_date": "[Extracted Expiration Date in YYYY-MM-DD or 'Not Found']",
        "deal_name": "[Extracted Deal Name or 'Not Found']",
        "previous_allocation": "[Extracted Previous Allocation or 'Not Found']",
        "new_allocation": "[Extracted New Allocation or 'Not Found']",
        "principal_amount": "[Extracted Principal Amount or 'Not Found']",
        "interest_amount": "[Extracted Interest Amount or 'Not Found']",
        "fee_type": "[Extracted Fee Type or 'Not Found']",
        "submission_document_type": "[Extracted Document Type or 'Not Found']"
        // you can also add more fields which might be relevant to that specific request type
    }}
    }}
    **Rules:**
    1. Provide confidence scores for each classification
    2. Include reasoning for classifications
    3. Use 'Not Found' for missing information
    4. Maintain all fields from both original output formats
    5. Follow strict JSON formatting

    Return only the JSON response with your analysis."""

# Gmail IMAP credentials
EMAIL = "nextgenthinkers2025@gmail.com"  # Replace with your email "jagadeesh.soppimat@gmail.com","nextgenthinkers2025@gmail.com"
PASSWORD = "whvh mirp guwi yquu"  # Use App Password if needed "wiax ixav dqzz xzif", "whvh mirp guwi yquu"
IMAP_SERVER = "imap.gmail.com"  # Change if using Outlook/Yahoo

# Connect to IMAP server
mail = imaplib.IMAP4_SSL(IMAP_SERVER)
mail.login(EMAIL, PASSWORD)
mail.select("inbox")

# Fetch unread emails
# fetch_and_classify_emails()

async def main():
    server = await websockets.serve(fetch_and_classify_emails, "localhost", 8765, process_request=None)  # ✅ Use the correct function
    await server.wait_closed()

asyncio.run(main())  # ✅ Proper event loop usage

# Close IMAP connection
mail.logout()
