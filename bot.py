import os, requests
from google import genai

GEMINI_KEY = os.environ['GEMINI_KEY']
TG_TOKEN = os.environ['TG_TOKEN']
TG_CHAT_ID = os.environ['TG_CHAT_ID']

client = genai.Client(api_key=GEMINI_KEY)

prompt = "Write a 200 word horror story in Hindi (Hinglish mix) for YouTube Shorts. Creepy, 1st person, twist ending. Only story."

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=prompt
)
story = response.text

url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
requests.post(url, data={"chat_id": TG_CHAT_ID, "text": f"👻 Horror Short:\n\n{story}"})
print("Done!")
