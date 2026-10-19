import os, requests
import google.generativeai as genai

GEMINI_KEY = os.environ['GEMINI_KEY']
TG_TOKEN = os.environ['TG_TOKEN']
TG_CHAT_ID = os.environ['TG_CHAT_ID']

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

prompt = "Write a 200 word horror story in Hindi for YouTube Shorts. Creepy, 1st person, twist ending."

res = model.generate_content(prompt)
story = res.text

url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
requests.post(url, data={"chat_id": TG_CHAT_ID, "text": f"👻 Horror Short:\n\n{story}"})
print("Sent!")
