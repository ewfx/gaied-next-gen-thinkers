import imaplib
import email
from email.policy import default
import os
from duplicate_email import TicketSystem
from dotenv import load_dotenv
from update_classification_prompt import update_request_for_duplicate
from classification_prompt import classify_email
from email_helper import *
import json
from database import *
import asyncio
import websockets
from websocket_helper import *

# Load environment variables from .env file
load_dotenv()
storage = SRMemoryStorage()

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

async def process_email(mail, read_last_email = False):
    """Process emails from the connected email account."""
    ts = TicketSystem()
    print("Trying to fetch emails!")

    try:
        # If read_last_email is True, only read the last email else read all emails
        if (read_last_email == True):
            toggle = "ALL"
        else:
            toggle = "UNSEEN"

        # Fetch email
        status, email_ids = mail.search(None, toggle)

        # Use last email in case of read_last_email is True else use all emails
        if (read_last_email == True):
            sorted(email_ids[0].split(), key=int, reverse=True)[:1]
        else:
            email_ids = sorted(email_ids[0].split(), key=int, reverse=False)

        print("Reading email with flag", read_last_email)

        for email_id in email_ids:
            await send_new_email_event()
            status, data = mail.fetch(email_id, "(RFC822)")
            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email, policy=default)
            # Process email with ticket system
            ticket_number, is_duplicate = ts.process_server_email(raw_email) # is_duplicate true in case of reply and forward
            # Extract subject and body
            subject = msg["subject"] or ""
            sender = msg["from"]
            body = ""
            attachment_text = ""

            print("*" * 70)
            print(f"Email ID: {sender} => Ticket: {ticket_number}")

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
            # print("Subject: ", subject)
            # print("Body: ", body)

            await send_classification_started_event(ticket_number)

            if not is_duplicate :  # new email for service request
                # Classify email based on subject, body, and attachments
                classification = classify_email(subject, body, attachment_text) # return json object
                print(f"\n📧 Email Subject: {subject}")
                print(f"📩 From: {sender}")
                # print(f"📜 Message:\n{body}")
                # print(f"📜 attachment_text:\n{attachment_text}")
                if classification:
                    print(f"🔍 Email Classified as: {json.dumps(classification, indent=4)}")
                    storage.add_request(
                        ticket_id=ticket_number,
                        email_subject=subject,
                        email_body=body,
                        classification_info = classification)
                    await send_classification_data(ticket_number, classification)
            else :
                # processing previously process email
                print(f"Email ID: {sender} => Ticket: {ticket_number} => Duplicate")
                old_classification = storage.get_request(ticket_number)["classification_info"]
                new_classification = update_request_for_duplicate(subject, body, attachment_text, old_classification)
                storage.update_request(ticket_number, new_classification)
                await send_classification_data(ticket_number, new_classification)

    except Exception as e:
        print(f"Error while processing emails: {e}")

def close_email_connection(mail):
    """Close the email connection safely."""
    try:
        print("Logging out from email")
        mail.logout()
        print("Database: \n", json.dumps(storage.get_all_requests(),  indent=4))
    except Exception as e:
        print("Error logging out from email", e)

async def main_loop():
    """Main loop to continuously check for new emails."""
    mail = None
    try:
        mail = initialize_email_connection()
        while True:
            await process_email(mail)
            await asyncio.sleep(os.getenv("EMAIL_CHECK_INTERVAL"))  # Wait before checking again
    except Exception as e:
        print(f"An error occurred in the main loop: {e}")
    finally:
        if mail:
            close_email_connection(mail)

async def main():
    """Main function to run both the email processing and the WebSocket server."""
    # Start the WebSocket server
    WEBSOCKET_PORT = os.getenv("WEBSOCKET_PORT")
    websocket_server = await websockets.serve(websocket_handler, "localhost", WEBSOCKET_PORT)
    print(f"WebSocket server started at ws://localhost:{WEBSOCKET_PORT}")

    # Run the email processing loop
    await main_loop()

    # Keep the WebSocket server running until manually stopped
    await websocket_server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())