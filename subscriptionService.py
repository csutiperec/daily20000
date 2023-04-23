from email.utils import parseaddr
import imaplib
import json
import os
import time
from email import policy
from email.parser import BytesParser
from datetime import datetime

USERNAME = os.getenv("DAILY20000UNAME")
PASSWORD = os.getenv("DAILY20000PWD")
LOCAL_PATH_TO_FOLDER = os.getenv("DAILY20000_PATH") or ''
SEARCH_CRITERIA = '(UNSEEN)'
SUBSCRIBERS_FILE = f'{LOCAL_PATH_TO_FOLDER}subscribedUsers.json'

while True:
    try:
        # Connect to Gmail
        imap = imaplib.IMAP4_SSL('imap.gmail.com')
        imap.login(USERNAME, PASSWORD)

        imap.select('inbox')
        status, messages = imap.search(None, SEARCH_CRITERIA)

        try:
            with open("log.txt", "r") as f:
                log = f.read()
        except FileNotFoundError:
            log = ''

        # Process each message
        for message_id in messages[0].split():

            # Fetch the message data
            status, message_data = imap.fetch(message_id, '(RFC822)')
            message_raw = message_data[0][1]

            # Parse the message
            message = BytesParser(policy=policy.default).parsebytes(message_raw)
            sender = parseaddr(message['From'])[1]
            body = message.get_body(preferencelist=('plain')).get_content().lower().strip()

            log += f'{datetime.now().strftime("%H:%M:%S")}: New message with the message_id of {message_id} arrived from {sender}, with the content of {body}\r\n'

            # Check if the sender is subscribed
            with open(SUBSCRIBERS_FILE, 'r') as f:
                subscribers = json.load(f)
            is_subscribed = sender in subscribers

            log += f"{datetime.now().strftime('%H:%M:%S')}: {sender} seems to {'already be subscribed' if is_subscribed else 'be a new subscriber'}\r\n"

            # Process the message based on the body
            if body == 'subscribe':
                if not is_subscribed:
                    subscribers.append(sender)
                    with open(SUBSCRIBERS_FILE, 'w') as f:
                        json.dump(subscribers, f)
                    log += f'{datetime.now().strftime("%H:%M:%S")}: Subscribed {sender}\r\n'
                else:
                    log += f'{datetime.now().strftime("%H:%M:%S")}: {sender} is already subscribed, but send another subscribe message\r\n'
            elif body == 'unsubscribe':
                if is_subscribed:
                    subscribers.remove(sender)
                    with open(SUBSCRIBERS_FILE, 'w') as f:
                        json.dump(subscribers, f)
                    log += f'{datetime.now().strftime("%H:%M:%S")}: Unsubscribed {sender}\r\n'
                else:
                    log += f'{datetime.now().strftime("%H:%M:%S")}: {sender} is already unsubscribed, but send another unsubscribe message\r\n'

            # Mark the message as read
            imap.store(message_id, '+FLAGS', '\\Seen')
            log += f'{datetime.now().strftime("%H:%M:%S")}: Marked message with message_is {message_id} as Seen\r\n'

        # Close the connection
        imap.close()
        imap.logout()
    except Exception as e:
        log += f'{datetime.now().strftime("%H:%M:%S")}: An error occurred: {e}\r\n'
    
    with open("log.txt", "w") as f:
        f.write(log)
    
    # Wait for 10 seconds before checking for new messages again
    time.sleep(10)
