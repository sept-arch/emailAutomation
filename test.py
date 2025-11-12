import smtplib # Simple mail transfer protocol; works across gmail, outlook, etc.
from google_auth_oauthlib.flow import InstalledAppFlow #Allows the google-sign in screen to appear
from googleapiclient.discovery import build #Gmail service object
from google.auth.transport.requests import Request #Allows user to stay logged in; requests a new token, which is basically your permission to be logged in
from google.oauth2.credentials import Credentials #More authentication; represents the google account within the code
from email.mime.text import MIMEText #Allows for formatting of email
import base64 #encodes and decodes data for compatibility
import os #code can see files and directories

#SCOPES = ['https://mail.google.com/'] Gives the script FULL Access to the Email: Overkill
SCOPE = ['https://www.googleapis.com/auth/gmail.send'] # from https://developers.google.com/workspace/gmail/api/auth/scopes, script only has send permission

#Authenticates user via Google sign-in
def getGmailCredentials():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file("token.json", SCOPE ) #prevents from having to constantly logging in
    
    #if not already logged in, go through authentication
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPE)
            creds = flow.run_local_server(port=0)
            #save token if ran again
            with open('token.json,', 'w') as token: #opens tokens (credentials) file with write permissions
                token.write(creds.to_json())
    return creds
    


sender_email = input("Type your Email Address: ") # Sender's email address
receiver_email = input("Type the recipient's Email Address: ") # Receiver's email address; eventually to be a list using pandas


subject = input("Please type the subject of the email: ") #Subject of email
message_body = input("Please type the contents of the email: ") #Contents of email

creds = getGmailCredentials() #Logs into gmail
service = build('gmail', 'v1', credentials=creds) #connects to

#body of email
message = MIMEText(message_body)
message['to'] = receiver_email
message['subject'] = subject
encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

# send email
send_message = (
    service.users()
    .messages()
    .send(userId="me", body={"raw": encoded_message})
    .execute()
)

print("Success!")