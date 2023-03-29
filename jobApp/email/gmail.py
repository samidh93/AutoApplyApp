import os
import json
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

class Gmail:
    def __init__(self, credentials_path):
        self.cwd = os.getcwd()
        self.token_path  = str
        self.credentials_path = os.path.join(self.cwd, credentials_path)
        # Construct the path to the token.json file relative to the current working directory
        # Check if the file exists
        if os.path.exists(self.credentials_path ):
            print("credentials.json found at:", self.credentials_path )
        else:
            print("credentials.json not found at:", self.credentials_path )

        self.creds = self._authenticate()
        self.service = build('gmail', 'v1', credentials=self.creds)

    def send_email_with_attachments(self, to, subject, body, attachment_paths):

        # Create the message body
        msg = MIMEMultipart()
        msg['to'] = to
        msg['subject'] = subject

        # Add some text to the email
        msg.attach(MIMEText(body))

        # Attach the files to the email
        for attachment_path in attachment_paths:
            attachment_path =os.path.join(self.cwd, attachment_path)
            filename = attachment_path.split('/')[-1]
            with open(attachment_path, 'rb') as f:
                file_data = f.read()
            attachment = MIMEBase('application', 'octet-stream')
            attachment.set_payload(file_data)
            encoders.encode_base64(attachment)
            attachment.add_header('Content-Disposition', 'attachment', filename=filename)
            msg.attach(attachment)

        # Send the email
        raw_message = base64.urlsafe_b64encode(msg.as_bytes()).decode()
        try:
            message = self.service.users().messages().send(userId='me', body={'raw': raw_message}).execute()
            print(f'Sent message: {message["id"]}')
        except HttpError as error:
            print(f'An error occurred: {error}')
            message = None

    def _authenticate(self, token_file="secrets/token.json"):
        self.token_path = os.path.join(self.cwd, token_file)
        SCOPES = ['https://mail.google.com/']
        creds = None
        if os.path.exists(self.token_path):
            print("token file exists")
            creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)
        if not creds or not creds.valid:
            print("token file missing")
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)
            with open(self.token_path, 'w') as token:
                token.write(creds.to_json())
        return creds

if __name__ == '__main__':
    gmail = Gmail('secrets/credentials.json')
    gmail.send_email_with_attachments('dhiebzayneb89@gmail.com', 'job application for project manager position in Paris, France', 'ai generated email content based on resume', ['data/resume.pdf', 'data/jobs.png'])