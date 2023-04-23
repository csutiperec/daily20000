from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import parseaddr
import imaplib
import json
import os
import time
from email import policy
from email.parser import BytesParser
import helperFunctions
from logger import Logger

USERNAME = os.getenv("DAILY20000UNAME")
PASSWORD = os.getenv("DAILY20000PWD")
LOCAL_PATH_TO_FOLDER = helperFunctions.getLocalPathToFolder()

SEARCH_CRITERIA = '(UNSEEN)'
SUBSCRIBERS_FILE = f'{LOCAL_PATH_TO_FOLDER}/assets/subscribedUsers.json'

SUBSCRIPTION_SUCCESS_MSG = 'Sikeresen feliratkoztál a napi 20000-esre. Minden reggel 9kor újabb választ kaphatsz arra ki van a 20000ft-os bankjegyen. \nHa le szeretnél iratkozni, küldd el az "unsubscribe" szót'
UNSUBSCRIPTION_SUCCESS_MSG = 'Sikeresen leiratkoztál a napi 20000-esről.'
BAD_FORMAT_MSG = 'Csak a "subscribe" szót küldd el email üzenetben, ha fel akarsz iratkozni a napi 20000-es tényekre.'

logger = Logger('ss_log.txt')

if not os.path.isfile(SUBSCRIBERS_FILE):
    with open(SUBSCRIBERS_FILE, 'w') as f:
        json.dump([], f)
        logger.log(f'Created new subscribedUsers.json file at {SUBSCRIBERS_FILE}')

while True:
    try:
        # Connect to Gmail
        imap = imaplib.IMAP4_SSL('imap.gmail.com')
        imap.login(USERNAME, PASSWORD)

        imap.select('inbox')
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

            logger.log(f'New message with the message_id of {message_id} arrived from {sender}, with the content of {body}')

            # Check if the sender is subscribed
            with open(SUBSCRIBERS_FILE, 'r') as f:
                subscribers = json.load(f)
            is_subscribed = sender in subscribers

            logger.log(f"{sender} seems to {'already be subscribed' if is_subscribed else 'be a new subscriber'}")

            responseMsg = MIMEMultipart('related')

            # Process the message based on the body
            if body == 'subscribe':
                if not is_subscribed:
                    subscribers.append(sender)
                    with open(SUBSCRIBERS_FILE, 'w') as f:
                        json.dump(subscribers, f)
                    logger.log(f'Subscribed {sender}')
                    responseMsg.attach(MIMEText(SUBSCRIPTION_SUCCESS_MSG))
                    helperFunctions.sendEmail('Daily20000: Feliratkozás visszaigazolás', sender, responseMsg)
                else:
                    logger.log(f'{sender} is already subscribed, but send another subscribe message')
            elif body == 'unsubscribe':
                if is_subscribed:
                    subscribers.remove(sender)
                    with open(SUBSCRIBERS_FILE, 'w') as f:
                        json.dump(subscribers, f)
                    logger.log(f'Unsubscribed {sender}')
                    responseMsg.attach(MIMEText(UNSUBSCRIPTION_SUCCESS_MSG))
                    helperFunctions.sendEmail('Daily20000: Leiratkozás visszaigazolás', sender, responseMsg)
                else:
                    logger.log(f'{sender} is already unsubscribed, but send another unsubscribe message')
            else:
                logger.log('Body is not "subscribe" or "unsubscribe"')
                responseMsg.attach(MIMEText(BAD_FORMAT_MSG))
                helperFunctions.sendEmail('Daily20000: Válasz', sender, responseMsg)
            # Mark the message as read
            imap.store(message_id, '+FLAGS', '\\Seen')
            logger.log(f'Marked message with message_is {message_id} as Seen')

        # Close the connection
        imap.close()
        imap.logout()
    except Exception as e:
        logger.log(f'An error occurred: {e}')
    
    # Wait for 10 seconds before checking for new messages again
    time.sleep(10)
