import imaplib
import email
from email.policy import default
import os
import pdfplumber
import pytesseract
import openai
from PIL import Image
import pandas as pd
from io import BytesIO
from bs4 import BeautifulSoup
from docx import Document
from transformers import pipeline

# Set Hugging Face API key
os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"

# Load a text classification model from Hugging Face
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Gmail IMAP credentials
EMAIL = "nextgenthinkers2025@gmail.com"  # Replace with your email "jagadeesh.soppimat@gmail.com","nextgenthinkers2025@gmail.com"
PASSWORD = "whvh mirp guwi yquu"  # Use App Password if needed "wiax ixav dqzz xzif", "whvh mirp guwi yquu"
IMAP_SERVER = "imap.gmail.com"  # Change if using Outlook/Yahoo

# Create a folder for attachments
ATTACHMENT_DIR = "attachments"
os.makedirs(ATTACHMENT_DIR, exist_ok=True)

# Connect to Gmail IMAP
mail = imaplib.IMAP4_SSL(IMAP_SERVER)
mail.login(EMAIL, PASSWORD)
mail.select("inbox")

# Search for all emails
status, messages = mail.search(None, "UNSEEN")
email_ids = messages[0].split()

def classify_email(text):
    """Classifies the email content using Hugging Face's zero-shot classification model."""
    labels = ["IT Support Request", "Access Request", "Finance Request", "HR Request", "General Inquiry"]

    result = classifier(text, candidate_labels=labels)
    print(f"\n📧 Confidence Score: {result["scores"][0]}")
    return result["labels"][0]  # The highest confidence label

# Test the function
# email_text = "Hello, I need access to the VPN for remote work."
# classification = classify_email(email_text)
# print(f"🔍 Classified as: {classification}")

for e_id in email_ids[-5:]:  # Get last 5 emails for testing
    status, msg_data = mail.fetch(e_id, "(RFC822)")
    
    for response_part in msg_data:
        if isinstance(response_part, tuple):
            msg = email.message_from_bytes(response_part[1])
            subject = msg["subject"]
            sender = msg["from"]

            # Extract email content
            email_body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))

                    if "attachment" not in content_disposition:
                        payload = part.get_payload(decode=True)
                        if payload:
                            if content_type == "text/plain":
                                email_body += payload.decode(errors="ignore")
                            elif content_type == "text/html":
                                soup = BeautifulSoup(payload.decode(errors="ignore"), "html.parser")
                                email_body += soup.get_text()

                    # Handle attachments
                    if part.get_filename():
                        filename = part.get_filename()
                        filepath = os.path.join(ATTACHMENT_DIR, filename)

                        with open(filepath, "wb") as f:
                            f.write(part.get_payload(decode=True))

                        extracted_text = ""
                        if filename.lower().endswith(".pdf"):
                            with pdfplumber.open(filepath) as pdf:
                                extracted_text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
                        elif filename.lower().endswith(".docx"):
                            doc = Document(filepath)
                            extracted_text = "\n".join([para.text for para in doc.paragraphs])
                        elif filename.lower().endswith((".xlsx", ".csv")):
                            df = pd.read_excel(filepath) if filename.endswith(".xlsx") else pd.read_csv(filepath)
                            extracted_text = df.to_string()
                        elif filename.lower().endswith((".png", ".jpg", ".jpeg")):
                            image = Image.open(filepath)
                            extracted_text = pytesseract.image_to_string(image)

                        email_body += f"\n[Attachment Extracted Text: {extracted_text}]"

            else:
                email_body = msg.get_payload(decode=True).decode(errors="ignore")

            # Classify the email using GPT-4
            def extract_plain_text(email_html):
                """Convert HTML email content to plain text."""
                soup = BeautifulSoup(email_html, "html.parser")
                return soup.get_text(separator=" ", strip=True)

            # Classify the email using hugging face AI
            emailBodyText = extract_plain_text(email_body)
            classification = classify_email(emailBodyText)

            print(f"\n📧 Email Subject: {subject}")
            print(f"📩 From: {sender}")
            print(f"📜 Message:\n{emailBodyText}")
            print(f"🔍 **Classified as: {classification}**")
            print("-" * 50)

# Close connection
mail.logout()
