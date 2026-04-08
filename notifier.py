import requests
from datetime import datetime
import os

# ================== TEST MODE ==================
# This version will FORCE the alert so you can see how it looks

DATES_TO_CHECK = ["2026-04-11", "2026-04-12"]

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
    print("Sent:", message[:150] + "..." if len(message) > 150 else message)

print("🧪 RUNNING TEST MODE - Forcing ticket alert...")

# Simulate that tickets are available
for target_date in DATES_TO_CHECK:
    send_notification(
        f"<b>🎟️ PROJECT HAIL MARY TICKETS ARE NOW LIVE!</b>\n\n"
        f"📅 Date: <b>{target_date}</b>\n"
        f"📍 Chennai\n\n"
        f"🚨 Go book IMAX immediately on District before they sell out!\n\n"
        f"⏰ Checked at: {datetime.now().strftime('%H:%M:%S')}"
    )

print("✅ Test completed - You should have received 2 bold alerts on Telegram.")
