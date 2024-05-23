import os
import time

import google.generativeai as genai
import markdown as md
from flask import Flask, redirect, request

app = Flask(__name__)

genai.configure(api_key=os.environ["apikey"])

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}
safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
]

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash-latest",
  safety_settings=safety_settings,
  generation_config=generation_config,
)

chat_session = model.start_chat(
  history=[
  ]
)

@app.route("/gpt", methods=['POST', 'GET'])
def gpt():
  global response
  time.sleep(3)
  page = ""
  f = open("display.html", "r")
  page = f.read()
  f.close()
  response_md = md.markdown(response.text)
  page = page.replace("{text}", response_md)
  return page
@app.route("/", methods=['POST', 'GET'])
def index():
  global response
  if request.method == 'POST':
    form = request.form
    response = chat_session.send_message(form["query"])
    return redirect("/gpt")
  else:
    f = open("form.html", "r")
    page = f.read()
    f.close()
    return page

app.run(host='0.0.0.0', port=81)
