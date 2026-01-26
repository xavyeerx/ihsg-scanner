# Quick Telegram Test
import requests
import sys
sys.path.insert(0, '.')
from config.settings import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

BOT_TOKEN = TELEGRAM_BOT_TOKEN
CHAT_ID = TELEGRAM_CHAT_ID

message = """🧪 TEST MESSAGE
━━━━━━━━━━━━━━━━━━━━━━━━━━
IHSG Scanner berhasil terhubung!
Bot Telegram aktif ✅
━━━━━━━━━━━━━━━━━━━━━━━━━━"""

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
payload = {
    'chat_id': CHAT_ID,
    'text': message,
    'parse_mode': 'HTML'
}

try:
    response = requests.post(url, json=payload, timeout=10)
    if response.status_code == 200:
        print("✅ SUCCESS! Pesan terkirim ke Telegram!")
    else:
        print(f"❌ ERROR: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"❌ ERROR: {e}")
