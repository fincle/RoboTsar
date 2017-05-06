from __future__ import print_function
import httplib2
import os
from datetime import datetime


#Import packages used for email sending
from apiclient import discovery
from apiclient import errors

from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import base64
from email.mime.text import MIMEText


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


## Test flags these will be replaced with python option flags
debug = 1
dryrun = 1


phase = 0
startdate = datetime(2017,4,21)

listposition =  (datetime.now()-startdate).days/7 + phase

print(listposition)





# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/gmail.send'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'JCTsar'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,'gmail-python-quickstart.json')


    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def create_message(sender, to, subject, message_text):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject

  if dryrun == 1:
      print('--- Message to send ---')
      print(message)
      print('--- End message ---')

  return {'raw': base64.urlsafe_b64encode(message.as_string())}

def send_message(service, user_id, message):
  """Send an email message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

  Returns:
    Sent Message.
  """

  if dryrun == 0:
      try:
          message = (service.users().messages().send(userId=user_id, body=message).execute())
          print('Message Id: %s' % message['id'])
          return message
      except errors.HttpError, error:
          print('An error occurred: %s' % error)
          # print('There was an error lol')
  elif dryrun == 1:
      print('No message sent')


def main():
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)


    msgsender = 'JournalClubRoboTsar@gmail.com'
    tousr = 'wadean@gmail.com'
    msgsubject = 'Hello google api'
    message_text = """
    This is an email send by awade
    There is more text but this is from my MacBookPro"""
    userId_set = 'me'

    # Make the message
    mkMessage = create_message(msgsender, tousr, msgsubject, message_text)

    # Send the message
    send_message(service,"me",mkMessage)

    # results = service.users().labels().list(userId='me').execute()
    # labels = results.get('labels', [])
    #
    # if not labels:
    #     print('No labels found.')
    # else:
    #   print('Labels:')
    #   for label in labels:
    #     print(label['name'])


if __name__ == '__main__':
    main()
