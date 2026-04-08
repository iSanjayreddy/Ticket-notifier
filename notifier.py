import requests
import os

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

print("Testing Telegram...")

if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
    try:
        response = requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
            json={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": "✅ Test message from GitHub Actions\nIf you see this, Telegram is working!",
                "parse_mode": "HTML"
            },
            timeout=10
        )
        print(f"Telegram response: {response.status_code}")
        print(response.text)
    except Exception as e:
        print(f"Error: {e}")
else:
    print("Missing token or chat id")
