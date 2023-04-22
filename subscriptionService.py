from email.utils import parseaddr
import imaplib
import json
import os
import time
from email import policy
from email.parser import BytesParser

# Gmail API credentials
USERNAME = os.getenv("DAILY20000UNAME")
PASSWORD = os.getenv("DAILY20000PWD")

# Email search criteria
SEARCH_CRITERIA = '(UNSEEN)'

# JSON file for storing subscribed users
SUBSCRIBERS_FILE = 'subscribedUsers.json'

while True:
    try:
        # Connect to Gmail
        imap = imaplib.IMAP4_SSL('imap.gmail.com')
        imap.login(USERNAME, PASSWORD)

        # Select the inbox
        imap.select('inbox')

        # Search for new messages matching the search criteria
        status, messages = imap.search(None, SEARCH_CRITERIA)

        # Process each message
        for message_id in messages[0].split():
            # Fetch the message data
            status, message_data = imap.fetch(message_id, '(RFC822)')
            message_raw = message_data[0][1]

            # Parse the message
            message = BytesParser(policy=policy.default).parsebytes(message_raw)
            sender = parseaddr(message['From'])[1]
            body = message.get_body(preferencelist=('plain')).get_content().lower().strip()

            # Check if the sender is subscribed
            with open(SUBSCRIBERS_FILE, 'r') as f:
                subscribers = json.load(f)
            is_subscribed = sender in subscribers

            # Process the message based on the body
            if body == 'subscribe':
                if not is_subscribed:
                    subscribers.append(sender)
                    with open(SUBSCRIBERS_FILE, 'w') as f:
                        json.dump(subscribers, f)
                    print(f'Subscribed {sender}')
                else:
                    print(f'{sender} is already subscribed')
            elif body == 'unsubscribe':
                if is_subscribed:
                    subscribers.remove(sender)
                    with open(SUBSCRIBERS_FILE, 'w') as f:
                        json.dump(subscribers, f)
                    print(f'Unsubscribed {sender}')
                else:
                    print(f'{sender} is not subscribed')

            # Mark the message as read
            imap.store(message_id, '+FLAGS', '\\Seen')

        # Close the connection
        imap.close()
        imap.logout()
    except Exception as e:
        print('An error occurred:', e)
    
    # Wait for 10 seconds before checking for new messages again
    time.sleep(10)
