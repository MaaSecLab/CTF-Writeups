from email.message import EmailMessage
from email.utils import parseaddr
from tempfile import TemporaryDirectory
import imaplib, smtplib, time
import email, os, re

# Email configuration
COMPANY_EMAIL = os.getenv('EMAIL_USERNAME') + "@" + os.getenv('EMAIL_DOMAIN')
PASSWORD = os.getenv('EMAIL_PASSWORD')
EMAIL_REGEX = r'user-\w+@%s' % os.getenv('EMAIL_DOMAIN')
IMAP_SERVER = "mail" # mail.skillissue.it
SMTP_SERVER = "mail" # mail.skillissue.it

# Polling configuration
MAX_WAIT = 2 * 60 
INTERVAL = 10 

subject_prefix = 'Surgo Company Customer Support - Request no.'
body = 'Hello dear customer! Thank you for contacting us.\n\nReply to this email describing your problem.\nTo help us better understand your issue, please attach any relevant file related to the problem.\n\nThank you for your cooperation!\nBest regards,\nSurgo Company'

def send_email(recipient_address, pid):
    msg = EmailMessage()
    msg['From'] = COMPANY_EMAIL
    msg['To'] = recipient_address
    msg['Subject'] = subject_prefix + str(pid)
    msg.set_content(body)

    if COMPANY_EMAIL is None or PASSWORD is None:
        raise ValueError("Environment error.")

    with smtplib.SMTP_SSL(SMTP_SERVER, 465) as smtp:
        smtp.login(COMPANY_EMAIL, PASSWORD)
        smtp.send_message(msg)

def find_email(session, email_ids, sender_address, pid):
    for email_id in email_ids:
        _, msg_data = session.uid('fetch', email_id, '(RFC822)')

        # Check, to avoid parsing errors
        if not msg_data or not isinstance(msg_data[0], tuple) or not isinstance(msg_data[0][1], (bytes, bytearray)):
            continue

        msg = email.message_from_bytes(msg_data[0][1])
        current_sender = parseaddr(msg.get("From", ""))[1]
        current_subject = msg.get("Subject", "")

        # Verify if the email is the customer's reply
        if current_sender == sender_address and f"{subject_prefix}{pid}" in current_subject:
            session.uid('store', email_id, '+FLAGS', '(\\Seen)') # Mark email as read
            return msg
    
    return None

def receive_email(sender_address, pid) -> tuple[bool, str | None, TemporaryDirectory | None]:
    if COMPANY_EMAIL is None or PASSWORD is None:
        raise ValueError("Environment error.")

    found = False
    attachment_path = None
    tempdir = None
    session = imaplib.IMAP4_SSL(IMAP_SERVER)

    try:
        session.login(COMPANY_EMAIL, PASSWORD)

        start = time.time()
        while time.time() - start < MAX_WAIT:
            # Select all unread emails
            session.select('inbox')
            _, data = session.uid('search', 'UNSEEN')

            if len(data[0]) == 0:
                print("...")
                time.sleep(INTERVAL)
                continue

            email_ids = data[0].split()
            response = find_email(session, email_ids, sender_address, pid)
            
            if response is None:
                print("...")
                time.sleep(INTERVAL)
                continue

            # Read email content
            for part in response.walk():
                if part.get_content_maintype() == "multipart":
                    continue
                
                content_disposition = part.get("Content-Disposition")
                if content_disposition is not None and "attachment" in content_disposition:
                    filename = part.get_filename()
                    if filename is not None:
                        tempdir = TemporaryDirectory()
                        path = os.path.join(tempdir.name, filename)
                        with open(path, "wb") as f:
                            payload = part.get_payload(decode=True)
                            if not isinstance(payload, (bytes, bytearray)):
                                payload = bytes(payload)
                            f.write(payload)
                        attachment_path = path  # Save attachment path
                        break

            found = True
            break

    except KeyboardInterrupt:
        print("\nOperation canceled.")
    finally:
        session.close()
        session.logout()

    return found, attachment_path, tempdir

# Check if the attachment contains dangerous executable code
def check_attachment(filepath):
    if filepath is None:
        return False

    print(f"Checking attachment '{filepath}'...")

    # Read the attachment content
    # If it can't be read, then it can't be executable code
    try:
        with open(filepath, "r") as f:
            content = f.read()
    except Exception as e:
        print("The attachment passed the security check.")
        print(f"Error: {e}")
        return

    # Execute the attachment's code
    # If it raises an error, then it's not executable code and therefore not dangerous
    try:
        exec(content)
        print("The attachment did not pass the security check.")
        print("Removing the attachment...")

    except Exception as e:
        print("The attachment passed the security check.")
        print(f"Error: {e}")
        

def forward_email(filepath):
    # TODO : Implement email forwarding to the support team
    try:
        os.remove(filepath)
    except:
        return

def main():
    pid = os.getpid()

    print(r'''
     ___                        ___                                              
    / __\ _ _  _ _  ___  ___   /  _\  ___  _ _ _  ___  ___  _ _  _ _                
    \__ \| | || '_>/ . |/ . \  | |__ / . \| ' ' || . \<_> || ' || | |
    /___/\___||_|  \_. |\___/  \___/ \___/|_|_|_||  _/<___||_|_|\_  |
                   <___/                         |_|            <___/
     ___          _       _                       ___   _  _             _    _
    | . | ___ ___<_> ___<| |> ___  _ _  ___ ___  /  _\ | |<_> ___  _ _ <| |> <_>
    |   |<_-<<_-<| |<_-< | | / ._>| ' | / /<_> | | |__ | || |/ ._>| ' | | |  | |
    |_|_|/__//__/|_|/__/ |_| \___\|_|_|/___<___| \___/ |_||_|\___\|_|_| |_|  |_|
                                                                                
    ''')
    print("Our customer support system is currently under development.")
    print("In the meantime, you can contact us about your problem via email.")

    client_address = ""
    while not re.match(EMAIL_REGEX, client_address): # Email address validation
        print("\nEnter your email address:")
        client_address = input().strip()

    print(f"\nThank you ({client_address})! We will contact you as soon as possible.")
    send_email(client_address, pid)

    print("We have sent you an email with instructions to resolve your issue.")
    print(f"We are waiting for your reply... (approximately {MAX_WAIT // 60} minutes maximum wait)\n")

    result, attachment_path, tempdir = receive_email(client_address, pid)
    if result:
        print("\nYour reply has been received!\n")

        check_attachment(attachment_path)
        print("\nThe request will be forwarded to our support team.")
        forward_email(attachment_path)

        print("We will contact you as soon as possible, goodbye!\n")
    else:
        print("No response received within the maximum time.\n")
        return
    
    if tempdir is not None:
        tempdir.cleanup()

if __name__ == "__main__":
    main()