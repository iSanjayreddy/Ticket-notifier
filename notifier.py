import requests
from datetime import datetime
import os
import json

TARGET_DATE = "2026-04-11"

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

BASE_URL = "https://www.district.in/movies/_next/data/INOMfV5bcOMEZK62SSACD/project-hail-mary-movie-tickets-in-chennai-MV200953.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json",
    "Referer": "https://www.district.in/movies/project-hail-mary-movie-tickets-in-chennai-MV200953"
}

def send_notification(message):
    print("Sending to Telegram:", message[:200])
    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        try:
            resp = requests.post(
                f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                json={"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"},
                timeout=10
            )
            print(f"Telegram status: {resp.status_code}")
        except Exception as e:
            print(f"Telegram error: {e}")

print(f"🎟️ DEBUG CHECK for {TARGET_DATE}")

try:
    params = {
        "frmtid": "etarl9n_zj",
        "fromdate": TARGET_DATE,
        "slug": "project-hail-mary-movie-tickets-in-chennai-MV200953"
    }
    
    r = requests.get(BASE_URL, params=params, headers=HEADERS, timeout=15)
    print(f"HTTP Status: {r.status_code}")
    data = r.json()
    
    # Print key parts for debugging
    movies = data.get("pageProps", {}).get("initialState", {}).get("movies", {})
    discovery = movies.get("discoveryResults", {})
    sessions = movies.get("movieSessions", {})
    
    print(f"discoveryResults exists: {bool(discovery)}")
    print(f"discovery.data exists: {bool(discovery.get('data'))}")
    print(f"movieSessions exists: {bool(sessions)}")
    print(f"movieSessions keys: {list(sessions.keys()) if isinstance(sessions, dict) else 'not dict'}")
    
    # Always send a status message
    status = f"<b>DEBUG CHECK - {TARGET_DATE}</b>\n"
    status += f"Discovery data: {'YES' if discovery.get('data') else 'NO'}\n"
    status += f"Sessions: {'YES' if sessions and sessions != {} else 'NO'}\n"
    status += f"Time: {datetime.now().strftime('%H:%M:%S')}"
    
    send_notification(status)
    
    if discovery.get("data") or (sessions and sessions != {}):
        send_notification(f"<b>🎟️ IMAX ALERT - Shows detected on {TARGET_DATE}!</b>")
    else:
        send_notification("Still no shows loaded yet.")

except Exception as e:
    send_notification(f"❌ Error: {str(e)[:300]}")

print("Check finished.")
