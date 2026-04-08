import requests
import time
from datetime import datetime
import os

# ================== CONFIG ==================
TARGET_DATE = "2026-04-11"          # ← change this whenever you want
CHECK_INTERVAL_SECONDS = 300        # 5 minutes

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

BASE_URL = "https://www.district.in/movies/_next/data/INOMfV5bcOMEZK62SSACD/project-hail-mary-movie-tickets-in-chennai-MV200953.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Referer": "https://www.district.in/movies/project-hail-mary-movie-tickets-in-chennai-MV200953"
}

def send_notification(message):
    print(f"🚨 {message}")
    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        try:
            requests.post(
                f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                json={"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"}
            )
        except:
            pass

def has_imax_shows(data):
    try:
        movies = data.get("pageProps", {}).get("initialState", {}).get("movies", {})
        discovery = movies.get("discoveryResults", {})
        sessions = movies.get("movieSessions", {})
        if discovery.get("data") or (sessions and sessions != {}):
            return True
    except:
        pass
    return False

print(f"🎟️ District IMAX Notifier started for {TARGET_DATE} (Chennai)")

while True:
    try:
        params = {
            "frmtid": "etarl9n_zj",
            "fromdate": TARGET_DATE,
            "slug": "project-hail-mary-movie-tickets-in-chennai-MV200953"
        }
        
        r = requests.get(BASE_URL, params=params, headers=HEADERS, timeout=15)
        r.raise_for_status()
        data = r.json()
        
        if has_imax_shows(data):
            send_notification(
                f"<b>🎟️ PROJECT HAIL MARY IMAX IS NOW LIVE!</b>\n"
                f"Date: {TARGET_DATE}\n"
                f"Chennai → Go book immediately!"
            )
            break
        else:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Still no IMAX shows...")
            
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Error: {e}")
    
    time.sleep(CHECK_INTERVAL_SECONDS)
