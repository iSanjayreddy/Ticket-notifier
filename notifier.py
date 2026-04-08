import requests
from datetime import datetime
import os

# ================== CONFIG ==================
TARGET_DATE = "2026-04-11"          # ← Change this when you want to monitor another date

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

BASE_URL = "https://www.district.in/movies/_next/data/INOMfV5bcOMEZK62SSACD/project-hail-mary-movie-tickets-in-chennai-MV200953.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json",
    "Referer": "https://www.district.in/movies/project-hail-mary-movie-tickets-in-chennai-MV200953"
}

def send_notification(message):
    print(message)
    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        try:
            requests.post(
                f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                json={"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"},
                timeout=10
            )
        except Exception as e:
            print(f"Telegram send error: {e}")

print(f"🎟️ Checking District for Project Hail Mary IMAX on {TARGET_DATE} (Chennai)")

try:
    params = {
        "frmtid": "etarl9n_zj",
        "fromdate": TARGET_DATE,
        "slug": "project-hail-mary-movie-tickets-in-chennai-MV200953"
    }
    
    r = requests.get(BASE_URL, params=params, headers=HEADERS, timeout=15)
    r.raise_for_status()
    data = r.json()
    
    movies = data.get("pageProps", {}).get("initialState", {}).get("movies", {})
    discovery = movies.get("discoveryResults", {})
    sessions = movies.get("movieSessions", {})
    
    if discovery.get("data") or (sessions and sessions != {}):
        send_notification(
            f"<b>🎟️ PROJECT HAIL MARY IMAX IS NOW LIVE!</b>\n\n"
            f"📅 Date: {TARGET_DATE}\n"
            f"📍 Chennai\n\n"
            f"Go book immediately on District!"
        )
        print("✅ IMAX shows detected!")
    else:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Still no IMAX shows yet.")

except Exception as e:
    error_msg = f"⚠️ Error checking District: {str(e)[:150]}"
    print(error_msg)
    send_notification(error_msg)

print("✅ Check completed. Next check in ~5 minutes.")
