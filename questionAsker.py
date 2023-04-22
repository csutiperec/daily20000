import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def askQuestion():
  response = openai.Completion.create(
    model="text-davinci-003",
    prompt="Ki van a 20000 ft-os bankjegyen?",
    max_tokens=256,
  )
  return(response['choices'][0]['text'])



