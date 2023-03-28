from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from base64 import urlsafe_b64encode
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email import encoders

# Replace with the path to your service account key file
KEY_FILE_LOCATION = 'key.json'

# Replace with your service account email address
SERVICE_ACCOUNT_EMAIL = 'autoapplyapp@autoapplyapp-381922.iam.gserviceaccount.com'

# Replace with the email address of the recipient
TO = 'sami.dhiab.x@gmail.com'

# Authenticate and build the service object
credentials = service_account.Credentials.from_service_account_file(
    KEY_FILE_LOCATION,
    scopes=['https://www.googleapis.com/auth/gmail.send'])
delegated_credentials = credentials#.with_subject('samihomiebro@gmail.com')
service = build('gmail', 'v1', credentials=delegated_credentials)

# Create a message object
msg = MIMEMultipart()

# Add the recipient's email address
msg['to'] = TO

# Add the subject of the email
msg['subject'] = 'Test Email'

# Add the body of the email
body = 'This is a test email sent using the Gmail API.'
msg.attach(MIMEText(body))

# Add an image attachment (optional)
with open('data/jobs.PNG', 'rb') as f:
    img_data = f.read()
image = MIMEImage(img_data, name='image.jpg')
msg.attach(image)

# Convert the message to a raw string
raw_msg = urlsafe_b64encode(msg.as_bytes()).decode()

# Send the email
try:
    message = service.users().messages().send(userId='me', body={'raw': raw_msg}).execute()
    print(F'The email was sent to {TO} with Id: {message["id"]}')
except HttpError as error:
    print(F'An error occurred: {error}')
    message = None
