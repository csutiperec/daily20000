import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import questionAsker

# Gmail API credentials
USERNAME = os.getenv("DAILY20000UNAME")
PASSWORD = os.getenv("DAILY20000PWD")

# Set up the SMTP server
smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
smtp_server.starttls()
smtp_server.login(USERNAME, PASSWORD)

with open('subscribedUsers.json', 'r') as f:
    subscribers = json.load(f)

# Compose the email message
sender = USERNAME
subject = 'Daily 20000'
message = MIMEMultipart('related')

message['Subject'] = subject
message['From'] = sender
message['Bcc'] = ', '.join(subscribers)

with open('message.html', 'r') as f:
    html = f.read()

chatGPTAnswer = questionAsker.askQuestion()

html = html.replace("$ChatGPTResponse", chatGPTAnswer)

text = MIMEText(html, "html")
message.attach(text)

# Attach the image file
with open('20000HUF.png', 'rb') as f:
    img_data = f.read()
img_part = MIMEImage(img_data, name='20000HUF.png')
img_part.add_header('Content-ID', '<deak')
message.attach(img_part)

smtp_server.send_message(message)

# Close the SMTP server
smtp_server.quit()
