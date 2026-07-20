from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp

app = FastAPI()

# إضافة حزمة CORS للسماح بالاتصالات من أي موقع/تطبيق
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # يتيح الاتصال من كل المصادر
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "online", "message": "YouTube Audio Extractor API"}

@app.get("/audio_url/{video_id}")
def get_audio_url(video_id: str):
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
    }
    url = f"https://www.youtube.com/watch?v={video_id}"
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            audio_url = info.get('url')
            return {"status": "success", "audio_url": audio_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))