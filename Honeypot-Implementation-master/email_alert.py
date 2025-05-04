import smtplib
import os
from email.message import EmailMessage

def send_intruder_alert(to_email, subject, body, image_path, ip_info):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = os.environ.get("ALERT_EMAIL")
    msg['To'] = to_email
    msg.set_content(f"{body}\n\nIntruder IP Info:\n{ip_info}")

    # Attach image if it exists
    if image_path and os.path.exists(image_path):
        with open(image_path, 'rb') as img:
            img_data = img.read()
            msg.add_attachment(img_data, maintype='image', subtype='jpeg', filename=os.path.basename(image_path))

    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_user = os.environ.get("ALERT_EMAIL")
    smtp_pass = os.environ.get("ALERT_EMAIL_PASS")

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)