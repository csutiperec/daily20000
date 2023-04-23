from email.mime.image import MIMEImage
import os
import openai
import smtplib

openai.api_key = os.getenv("OPENAI_API_KEY")
USERNAME = os.getenv("DAILY20000UNAME")
PASSWORD = os.getenv("DAILY20000PWD")

def askQuestion(question):
  response = openai.Completion.create(
    model="text-davinci-003",
    prompt=question,
    max_tokens=256,
  )
  return(response['choices'][0]['text'])

def sendEmail(Subject, To, Message):
  smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
  smtp_server.starttls()
  smtp_server.login(USERNAME, PASSWORD)

  Message['Subject'] = Subject
  Message['From'] = USERNAME
  Message['Bcc'] = To

  smtp_server.send_message(Message)
  smtp_server.quit()

def createDailyChatGPTMessageBody(messageTemplateHtmlUri):
  with open(messageTemplateHtmlUri, 'r') as f:
    html = f.read()
  chatGPTAnswer = askQuestion("Ki van a 20000 ft-os bankjegyen?")

  return html.replace("$ChatGPTResponse", chatGPTAnswer)
  
def createAttachableImage(imageUri, name, contentId):
  with open(imageUri, 'rb') as f:
    img_data = f.read()
  img_part = MIMEImage(img_data, name=name)
  img_part.add_header('Content-ID', contentId)

  return img_part

def getLocalPathToFolder():
  return os.getenv("DAILY20000_PATH") or os.path.dirname(os.path.abspath(__file__))
