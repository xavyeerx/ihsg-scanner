# Quick Telegram Test
import requests

BOT_TOKEN = "8421417558:AAGSldYyzkQ59uxpuPeGIaz8sW_GUtISSq8"
CHAT_ID = "1342806965"

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
