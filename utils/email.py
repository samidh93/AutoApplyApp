import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

class GmailSender:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def send_email(self, recipient, subject, body, attachment_path):
        # Create message container
        message = MIMEMultipart()
        message['From'] = self.username
        message['To'] = recipient
        message['Subject'] = subject

        # Add message body
        message.attach(MIMEText(body))

        # Attach PDF file
        with open(attachment_path, 'rb') as f:
            attachment = MIMEApplication(f.read(), _subtype='pdf')
            attachment.add_header('content-disposition', 'attachment', filename=os.path.basename(attachment_path))
            message.attach(attachment)

        # Connect to Gmail's SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        # Login with Gmail account
        server.login(self.username, self.password)

        # Send email and quit
        server.sendmail(self.username, recipient, message.as_string())
        server.quit()
