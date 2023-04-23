import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import questionAsker

USERNAME = os.getenv("DAILY20000UNAME")
PASSWORD = os.getenv("DAILY20000PWD")
LOCAL_PATH_TO_FOLDER = os.getenv("DAILY20000_PATH") or ''

# Set up the SMTP server
smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
smtp_server.starttls()
smtp_server.login(USERNAME, PASSWORD)

# Compose the email message
message = MIMEMultipart('related')

with open(f'{LOCAL_PATH_TO_FOLDER}subscribedUsers.json', 'r') as f:
    subscribers = json.load(f)

message['Subject'] = 'Daily 20000'
message['From'] = USERNAME
message['Bcc'] = ', '.join(subscribers)

with open(f'{LOCAL_PATH_TO_FOLDER}message.html', 'r') as f:
    html = f.read()

chatGPTAnswer = questionAsker.askQuestion()

html = html.replace("$ChatGPTResponse", chatGPTAnswer)
text = MIMEText(html, "html")
message.attach(text)

# Attach the image file
with open(f'{LOCAL_PATH_TO_FOLDER}20000HUF.png', 'rb') as f:
    img_data = f.read()
img_part = MIMEImage(img_data, name='20000HUF.png')
img_part.add_header('Content-ID', '<deak')
message.attach(img_part)

smtp_server.send_message(message)
smtp_server.quit()
