from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import helperFunctions
import json
import sys

LOCAL_PATH_TO_FOLDER = helperFunctions.getLocalPathToFolder()

MESSAGEHTML_FILE = f'{LOCAL_PATH_TO_FOLDER}/assets/message.html'
SUBSCRIBERS_FILE = f'{LOCAL_PATH_TO_FOLDER}/assets/subscribedUsers.json'
IMAGE_FILE = f'{LOCAL_PATH_TO_FOLDER}/assets/20000HUF.png'

try:
    with open(SUBSCRIBERS_FILE, 'r') as f:
        subscribers = json.load(f)
        if len(subscribers) == 0:
            sys.exit()
except FileNotFoundError:
    sys.exit()

message = MIMEMultipart('related')

message.attach(MIMEText(helperFunctions.createDailyChatGPTMessageBody(MESSAGEHTML_FILE), "html"))
message.attach(helperFunctions.createAttachableImage(IMAGE_FILE, '20000HUF.png', '<deak>'))

helperFunctions.sendEmail('Daily 20000', ', '.join(subscribers), message)
