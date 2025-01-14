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
    def __init__(self, credentials_path, token_path, api_key_file="jobApp/secrets/gmail_key.json"):
        self.cwd = os.getcwd()
        self.token_path = os.path.join(self.cwd, token_path)
        self.credentials_path = os.path.join(self.cwd, credentials_path)
        self.api_key_file = api_key_file
        # Construct the path to the token.json file relative to the current working directory
        # Check if the file exists
        if os.path.exists(self.credentials_path ):
            print("credentials.json found at:", self.credentials_path )
        else:
            print("credentials.json not found at:", self.credentials_path )
        if self.credentials_path:
            self.creds = self._authenticate_via_file_cred()
            self.service = build('gmail', 'v1', credentials=self.creds)
        #if self.api_key_file:
        #    self.key = self._authenticate_via_api_key()
        #    self.service = build('gmail', 'v1', developerKey=self.key)

    def send_email_with_attachments(self, from_, to, subject, body, attachment_paths):

        # Create the message body
        msg = MIMEMultipart()
        msg['from']= from_
        msg['to'] = to
        msg['subject'] = subject
        # integrate email verification into sending (only for @gmail clients)
        #if self._verify_email(msg['to']) is not True:
        #    return False
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
            return True
        except HttpError as error:
            print(f'An error occurred: {error}')
            message = None

    def _verify_email(self, email)-> bool:
        print(f"verify if email {email} exists in gmail")
        result = self.service.users().messages().list(userId='me', q=email).execute()
        # Check if any emails were found
        messages = result.get('messages', [])
        if not messages:
            print("email not valid")
            return False
        # Return the ID of the first email found
        print("email valid")
        print(f"id: messages[0]['id']")
        return True

    def _authenticate_via_api_key(self):
        SCOPES = ['https://mail.google.com/']
        key = None
        if os.path.exists(self.api_key_file):
            print("api key file file exists")
            with open(self.api_key_file, 'r') as f:
                data = json.load(f)
        key = data["first"]["api_key"]
        print(f"api key loaded: {key}")
        return key
    
    def _authenticate_via_file_cred(self):
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
    gmail = Gmail('jobApp/secrets/credentials.json', 'jobApp/secrets/gmail_token.json' )
    gmail.send_email_with_attachments('email@gmail.com','email@gmail.com',  'job application for project manager position in Paris, France', 'ai generated email content based on resume', ['jobApp/data/resume.pdf', 'jobApp/data/jobs.png'])