import imaplib
import email
from email.policy import default
import os
from duplicate_email import TicketSystem
from dotenv import load_dotenv
from email_classification_gemini import classify_email
from email_helper import *

# Load environment variables from .env file
load_dotenv()

def initialize_email_connection():
    """Initialize and return an IMAP email connection."""
    # Gmail IMAP credentials
    EMAIL = os.getenv("EMAIL")  # Replace with your email "jagadeesh.soppimat@gmail.com","nextgenthinkers2025@gmail.com"
    PASSWORD = os.getenv("PASSWORD")  # Use App Password if needed "wiax ixav dqzz xzif", "whvh mirp guwi yquu"
    IMAP_SERVER = os.getenv("IMAP_SERVER")  # Change if using Outlook/Yahoo

    try:
        # Connect to IMAP server
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL, PASSWORD)
        mail.select("inbox")
        print("Email connection initialized successfully.")
        return mail

    except imaplib.IMAP4.error as e:
        print(f"IMAP Error: {e}")
        raise  # Re-raise the exception to handle it in the calling function

    except Exception as e:
        print(f"General Error: {e}")
        raise

def process_email(mail):
    """Process emails from the connected email account."""
    ts = TicketSystem()
    print("Trying to fetch emails!")
    
    try:
        # Fetch unread emails
        status, email_ids = mail.search(None, "ALL")  # "UNSEEN"
        # email_ids = sorted(email_ids[0].split(), key=int, reverse=False)
        email_ids = sorted(email_ids[0].split(), key=int, reverse=True)[:1]

        for email_id in email_ids:
            status, data = mail.fetch(email_id, "(RFC822)")
            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email, policy=default)
            # Process email with ticket system
            ticket_number = ts.process_server_email(raw_email)
            print("*" * 70)
            print(f"Email ID: {email_id.decode()} => Ticket: {ticket_number}")

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
            print("Subject: ", subject)
            print("Body: ", body)

            # Classify email based on subject, body, and attachments
            classification = classify_email(subject, body, attachment_text)

            print(f"\n📧 Email Subject: {subject}")
            print(f"📩 From: {sender}")
            print(f"📜 Message:\n{body}")
            print(f"📜 attachment_text:\n{attachment_text}")
            if classification:
                print(f"🔍 Email Classified as: {classification}")
            print("-" * 50)

    except Exception as e:
        print(f"Error while processing emails: {e}")

def close_email_connection(mail):
    """Close the email connection safely."""
    try:
        print("Logging out from email")
        mail.logout()
    except Exception as e:
        print("Error logging out from email", e)

def main():
    """Main function to initialize and process emails."""
    try:
        mail = initialize_email_connection()
        process_email(mail)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        close_email_connection(mail)

if __name__ == "__main__":
    main()
