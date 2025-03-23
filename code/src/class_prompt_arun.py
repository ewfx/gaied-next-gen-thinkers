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
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts.pipeline import PipelinePromptTemplate
from langchain_core.prompts.prompt import PromptTemplate
import json



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

classification_data = json.dumps(classify_request_type())


os.environ["GOOGLE_API_KEY"] = "AIzaSyBgD85PrdkN2M8bFQA0HYOreAFkc_Z-TSA"

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

def classify_email(subject, body, attachment_text):

    output_json_example = json.dumps(
        {
            "request_type": "",
            "confidence_score": 0.0,
            "sub_request_type": [
                {
                    "sub_request_type": "",
                    "confidence_score": 0.0,
                    "reasoning":""
                }
            ],
            "reasoning":""
        }
    )
    additional_information_json_format = json.dumps({
                "extracted_information": {
                    "amount": "1500.00",
                    "currency": "AU",
                    "date": "2025-03-28 14:32:00",
                    "transaction_id": "Not Found",
                    "loan_number": "LN12345",
                    "account_number": "ACC67890",
                    "expiration_date": "Not Found",
                    "deal_name": "Acme Corp Loan",
                    "previous_allocation": "Department A",
                    "new_allocation": "Department B",
                    "transfer_from_account": "Not Found",
                    "transfer_to_account": "Not Found",
                    "principal_amount": "1000.00",
                    "interest_amount": "500.00",
                    "fee_type": "Reallocation Fee",
                    "payment_amount": "Not Found",
                    "submission_document_type": "Not Found",
                    "closing_date": "2025-03-28",
                    "amendment_fees": "1000.00",
                    "reallocation_principal": "5000.00",
                    "cashless_roll_details": "Not Found",
                    "change_type": "Increase",
                    "previous_commitment_amount": "10000.00",
                    "reallocation_fee": "15000.00",
                    "new_commitment_amount": "25000.00",
                    "full_name": "Not Found",
                    "email": "Not Found",
                    "complete_residential_address": "Not Found",
                    "phone_number": "Not Found",
                    "sending_bank": "Not Found",
                    "receiving_bank": "Not Found",
                    "swift_code": "Not Found",
                    "bic_code": "Not Found",
                    "sending_bank_account_number": "Not Found",
                    "transfer_mode": "[Wire transfer/Online]",
                    "service_request_number": "Not Found",
                    "invoice_number": "Not Found",
                    "type_of_adjustment": "[Correxion/Refund/Reversal]",
                    "transaction_type": "Not Found",
                    "reason_of_adjustment": "[incorrect calculation/overpayment/underpayment/undisclosed fees/unncessary charges]",
                    "original_commitment_date": "[Not Found]",
                    "original_commitment_amount": "[Not Found]",
                    "commitment_change": "[increase in commitment amount/extension of maturity date/changes to interest rates]",
                    "change_impact": "[changes to loan balance/changes to monthly payments/changes to loan term etc]",
                    "legal_document_type": "Not Found",
                    "actual_credit_line_amount": "Not Found",
                    "decreased_credit_line_amount": "Not Found",
                    "increased_credit_line_amount": "Not Found",
                    "effective_date": "Not Found",
                    "letter_of_credit_number": "Not Found",
                    "fee_type": "[issuance fee, amendment fee, confirmation fee, negotiation fee, Reallocation Fee etc]",
                    "transfer_reference_number": "Not Found",
                    "anti_money_laundaring_doc_available": "[true/false]",
                    "kyc_doc_available": "[true/false]",
                }
            })


    print("*" * 50)

    email_content = r"""
        ** Email Content **
            Subject: {subject}
            Body: {body}
            Attachments: {attachment_text}

        Summarize the email content for financial and banking analysis.
    """
    email_content_prompt = PromptTemplate.from_template(email_content)

    classification_content = r"""
        Analyze the content and provide JSON array listing all the classifications from {classification_data} in the format given below with the fitting confidence score.
        Note: We want all of the classifications to be assessed and provided in the output. 
    """
    classification_content_prompt = PromptTemplate.from_template(classification_content)

    classification_example = r"""
        **Output JSON Example**:
            {output_json_example}
    """
    classification_example_prompt = PromptTemplate.from_template(classification_example)

    additional_content = r"""
        Also, provide all of the extra financial information from the email content provided above.
    """
    additional_content_prompt = PromptTemplate.from_template(additional_content)

    additional_example = r"""
        **Output JSON Format:**
            {additional_information_json_format}
        Note: We have to skip all the fields that are not found in the email content.
    """
    additional_example_prompt = PromptTemplate.from_template(additional_example)
    

    prompt = """
        {email_content}
        {classification_content}
        {classification_example}
        {additional_content}
        {additional_example}
    """
    full_prompt = PromptTemplate.from_template(prompt)

    input_prompts = [
        ("email_content", email_content_prompt),
        ("classification_content", classification_content_prompt),
        ("classification_example", classification_example_prompt),
        ("additional_content", additional_content_prompt),
        ("additional_example", additional_example_prompt),
    ]

    pipeline = PipelinePromptTemplate(final_prompt = full_prompt, pipeline_prompts = input_prompts)

    formattedPrompt = pipeline.format(
        subject=subject,
        body=body,
        attachment_text=attachment_text,
        classification_data=classification_data,
        output_json_example=output_json_example,
        additional_information_json_format=additional_information_json_format
    )

    print("Formmated Prompt: ", formattedPrompt)
    print("Response: ", llm.invoke(input=formattedPrompt).content)
    print("*" * 50)
    

def is_duplicate(content1, content2, threshold=0.9):
    similarity = difflib.SequenceMatcher(None, content1.strip(), content2.strip()).ratio()
    return similarity >= threshold


# Gmail IMAP credentials
EMAIL = "nextgenthinkers2025@gmail.com"  # Replace with your email "jagadeesh.soppimat@gmail.com","nextgenthinkers
PASSWORD = "whvh mirp guwi yquu"  # Use App Password if needed "wiax ixav dqzz xzif", "whvh mirp guwi yquu"
IMAP_SERVER = "imap.gmail.com"  # Change if using Outlook/Yahoo

# Connect to IMAP server
mail = imaplib.IMAP4_SSL(IMAP_SERVER)
mail.login(EMAIL, PASSWORD)
mail.select("inbox")

# Fetch unread emails
status, email_ids = mail.search(None, "ALL")  # Fetch unread emails
email_ids = sorted(email_ids[0].split(), key=int, reverse=True)[:1]

original_emails = {}  # Dictionary to store original emails for comparison

for email_id in email_ids:
    status, data = mail.fetch(email_id, "(RFC822)")
    raw_email = data[0][1]
    msg = email.message_from_bytes(raw_email, policy=default)

    # Extract subject and sender
    subject = msg["subject"] or ""
    sender = msg["from"]
    
    # Detect if the email is a reply or forward
    is_reply = subject.lower().startswith("re:")
    is_forward = subject.lower().startswith(("fw:", "fwd:"))

    # Extract body content
    body = ""
    attachment_text = ""
    original_body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            # if content_type == "text/plain":
            #     body = part.get_payload(decode=True).decode("utf-8", errors="ignore")
            #     break

            if "attachment" in content_disposition:
                attachment_text += process_attachment(part) + "\n"
            elif content_type == "text/html":
                body += extract_plain_text(part.get_payload(decode=True).decode(errors="ignore")) + "\n"
            elif content_type == "text/plain":
                body += part.get_payload(decode=True).decode(errors="ignore") + "\n"
    else:
        body = msg.get_payload(decode=True).decode("utf-8", errors="ignore")

    # Identify quoted text (original email)
    quoted_text_start = body.find("On ")
    if quoted_text_start != -1:
        original_body = body[quoted_text_start:]  # Extract quoted section
        reply_body = body[:quoted_text_start]  # Keep only the new reply content
    else:
        original_body = ""
        reply_body = body

    # Store original emails for reference (if it's not a reply)
    if not is_reply:
        original_emails[subject] = reply_body

    # Check if reply body is the same as original body
    is_duplicate_reply = False
    if is_reply and subject in original_emails:
        is_duplicate_reply = is_duplicate(reply_body, original_emails[subject])

    print(f"🔹 IsDuplicate: {is_duplicate_reply}")

    # Classify email based on subject, body, and attachments
    classification = classify_email(subject, body, attachment_text)

    # Print email details
    print("\n📧 Email Received:")
    print(f"🔹 Sender: {sender}")
    print(f"🔹 Subject: {subject}")
    print(f"🔹 Is Reply: {is_reply}")
    print(f"🔹 Is Forward: {is_forward}")
    print(f"🔹 Is Duplicate Reply: {is_duplicate_reply}")
    print(f"🔹 Reply Body:\n{reply_body}")

mail.logout()