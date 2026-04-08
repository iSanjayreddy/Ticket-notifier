import requests
from datetime import datetime
import os

# ================== CONFIG ==================
DATES_TO_CHECK = ["2026-04-11", "2026-04-12"]   # Saturday + Sunday

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

BASE_URL = "https://www.district.in/movies/_next/data/INOMfV5bcOMEZK62SSACD/project-hail-mary-movie-tickets-in-chennai-MV200953.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json",
    "Referer": "https://www.district.in/movies/project-hail-mary-movie-tickets-in-chennai-MV200953"
}

def send_notification(message):
    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        try:
            requests.post(
                f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                json={"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"},
                timeout=10
            )
        except:
            pass
    print(message)

print(f"🎟️ Starting District check for {DATES_TO_CHECK}")

found_any = False

for target_date in DATES_TO_CHECK:
    try:
        params = {
            "frmtid": "etarl9n_zj",
            "fromdate": target_date,
            "slug": "project-hail-mary-movie-tickets-in-chennai-MV200953"
        }
        
        r = requests.get(BASE_URL, params=params, headers=HEADERS, timeout=15)
        data = r.json()
        
        movies = data.get("pageProps", {}).get("initialState", {}).get("movies", {})
        discovery = movies.get("discoveryResults", {})
        sessions = movies.get("movieSessions", {})
        
        has_shows = bool(discovery.get("data")) or bool(sessions and sessions != {})
        
        if has_shows:
            send_notification(
                f"<b>🎟️ PROJECT HAIL MARY TICKETS ARE NOW LIVE!</b>\n\n"
                f"📅 Date: <b>{target_date}</b>\n"
                f"📍 Chennai\n\n"
                f"🚨 Go book IMAX immediately on District before they sell out!"
            )
            found_any = True
        else:
            print(f"[{datetime.now().strftime('%H:%M')}] No shows yet for {target_date}")
            
    except Exception as e:
        print(f"Error checking {target_date}: {e}")

# Final summary message
if not found_any:
    send_notification(f"[{datetime.now().strftime('%d-%m %H:%M')}] Still no tickets for 11th & 12th April... checking again in 5 min.")
else:
    send_notification("✅ Tickets found for one or more dates!")

print("✅ Full check completed.")
