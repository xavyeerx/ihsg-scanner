# IHSG Supertrend Scanner 🚀

Scanner otomatis untuk mendeteksi sinyal trading pada saham-saham IHSG dengan notifikasi Telegram.

## Fitur

- ✅ **Supertrend Break** - Deteksi saat saham masuk/keluar zona bullish
- ✅ **DCA Zone Alert** - Sinyal saat saham masuk zona Fibonacci retracement
- ✅ **Accumulation Signal** - Deteksi akumulasi berdasarkan Stoch RSI + Volume
- ✅ **Strong Buy Transition** - Alert saat status berubah ke STRONG BUY
- ✅ **600+ Saham IHSG** - Cover hampir semua saham aktif

## Quick Start

### 1. Install Python
Pastikan Python 3.9+ sudah terinstall. Download dari [python.org](https://python.org)

### 2. Install Dependencies
```bash
cd ihsg-supertrend-scanner
pip install -r requirements.txt
```

### 3. Setup Telegram Bot

1. Buka Telegram, cari **@BotFather**
2. Ketik `/newbot`
3. Ikuti instruksi, beri nama bot (contoh: `IHSG Scanner Bot`)
4. Copy **Bot Token** yang diberikan

5. Untuk mendapatkan Chat ID:
   - Cari **@userinfobot** di Telegram
   - Ketik `/start`
   - Copy **ID** yang ditampilkan

6. Edit file `config/settings.py`:
```python
TELEGRAM_BOT_TOKEN = "paste_token_disini"
TELEGRAM_CHAT_ID = "paste_chat_id_disini"
```

### 4. Test Manual
```bash
python main.py
```

### 5. Jalankan Scheduler (15 menit)
```bash
python scheduler.py
```

## Struktur Project

```
ihsg-supertrend-scanner/
├── config/
│   ├── settings.py        # Konfigurasi (token, parameter)
│   └── stocks_list.py     # Daftar saham IHSG
├── core/
│   ├── data_fetcher.py    # Ambil data dari Yahoo Finance
│   ├── supertrend.py      # Kalkulasi Supertrend
│   ├── indicators.py      # Indikator teknikal
│   ├── scoring.py         # Sistem scoring
│   └── scanner.py         # Logic scanning
├── database/
│   └── state_manager.py   # Track state saham
├── notifications/
│   └── telegram_bot.py    # Kirim alert Telegram
├── logs/                  # Log files
├── main.py                # Entry point
├── scheduler.py           # Scheduler 15 menit
└── requirements.txt       # Dependencies
```

## Contoh Alert Telegram

```
━━━━━━━━━━━━━━━━━━━━━━━━━━
🟢 SUPERTREND BULLISH BREAK
━━━━━━━━━━━━━━━━━━━━━━━━━━
⏰ 22 Jan 2026, 10:15 WIB

📈 BBCA | 9,850 (+2.3%)
   └─ ST: 9,650 | Score: 78

📈 ASII | 5,200 (+1.8%)
   └─ ST: 5,050 | Score: 65

━━━━━━━━━━━━━━━━━━━━━━━━━━
Total: 2 saham break bullish
```

## Troubleshooting

### Error: No module named 'xxx'
```bash
pip install -r requirements.txt
```

### Error: Telegram not configured
Edit `config/settings.py` dengan token dan chat ID yang benar.

### Tidak ada alert yang muncul
- Pastikan ini BUKAN first run (first run digunakan untuk establish baseline)
- Check logs di folder `logs/`
- Pastikan ada saham yang memenuhi kriteria

## Parameter Settings

Edit di `config/settings.py`:

| Parameter | Default | Keterangan |
|-----------|---------|------------|
| SUPERTREND_PERIOD | 10 | Period Supertrend |
| SUPERTREND_MULTIPLIER | 3.0 | Multiplier Supertrend |
| SCAN_INTERVAL_MINUTES | 15 | Interval scan |
| BUY_THRESHOLD | 60 | Minimum score untuk BUY |

## License
MIT License - Free to use and modify
