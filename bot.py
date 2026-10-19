import os, random, requests, asyncio, textwrap
import google.generativeai as genai
import edge_tts
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip

# 100% Free Stock Horror Videos - Coverr.co + Mixkit.co
BG_VIDEOS = [
    "https://cdn.coverr.co/videos/coverr-dark-forest-at-night-1578332012/1080p.mp4",
    "https://cdn.coverr.co/videos/coverr-misty-forest-1578023003/1080p.mp4",
    "https://cdn.coverr.co/videos/coverr-foggy-forest-1578023186/1080p.mp4",
    "https://cdn.coverr.co/videos/coverr-a-forest-at-night-1578031350/1080p.mp4",
    "https://cdn.coverr.co/videos/coverr-abandoned-cemetery-1578031585/1080p.mp4"
]

print("Story generate ho rahi hai...")
genai.configure(api_key=os.environ["GEMINI_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')
prompt = "Ek 25 second ki darawani Hindi horror kahani likh. Hook se start kar. Sirf kahani de, koi extra text nahi."
story = model.generate_content(prompt).text
print(story)

async def make_voice():
    await edge_tts.Communicate(story, "hi-IN-SwaraNeural").save("voice.mp3")
asyncio.run(make_voice())

print("Stock video download...")
video_url = random.choice(BG_VIDEOS)
r = requests.get(video_url, timeout=120)
open("bg.mp4","wb").write(r.content)

audio = AudioFileClip("voice.mp3")
video = VideoFileClip("bg.mp4").subclip(0, audio.duration)
video = video.loop(duration=audio.duration)
video = video.crop(x1=600, width=720, height=1280).resize((720,1280))

# Text with stroke
wrapped_text = textwrap.fill(story, width=20)
txt = TextClip(wrapped_text, fontsize=60, color='white', stroke_color='black', stroke_width=3, method='caption', size=(650, None), font='DejaVu-Sans-Bold')
txt = txt.set_duration(audio.duration).set_position('center')

final = CompositeVideoClip([video, txt]).set_audio(audio).set_duration(audio.duration)
final.write_videofile("short.mp4", fps=24, codec='libx264')
