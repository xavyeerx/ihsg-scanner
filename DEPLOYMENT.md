# Panduan Deployment IHSG Scanner Bot

---

## 🚀 DEPLOY KE RAILWAY (GRATIS)

### Langkah 1: Buat Akun GitHub (jika belum ada)
1. Buka https://github.com
2. Klik **Sign up** dan buat akun

### Langkah 2: Upload Project ke GitHub
**Dari folder project, jalankan di terminal:**
```bash
cd "d:\ALGO TRADE\ihsg-supertrend-scanner"

# Inisialisasi Git
git init
git add .
git commit -m "Initial commit - IHSG Scanner"

# Buat repository baru di GitHub, lalu:
git remote add origin https://github.com/USERNAME/ihsg-scanner.git
git branch -M main
git push -u origin main
```

> ⚠️ **PENTING:** Pastikan `config/settings.py` TIDAK berisi token/secret sebelum push!

### Langkah 3: Setup Environment Variables
Edit `config/settings.py` untuk menggunakan environment variables:
```python
import os

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "YOUR_CHAT_ID_HERE")
```

### Langkah 4: Deploy ke Railway
1. Buka https://railway.app
2. Klik **Login with GitHub**
3. Klik **New Project** → **Deploy from GitHub repo**
4. Pilih repository `ihsg-scanner`
5. Railway akan otomatis detect Python dan deploy

### Langkah 5: Set Environment Variables di Railway
1. Di dashboard Railway, klik project Anda
2. Klik tab **Variables**
3. Tambahkan:
   - `TELEGRAM_BOT_TOKEN` = (token bot Anda)
   - `TELEGRAM_CHAT_ID` = (chat ID Anda)
4. Klik **Deploy** untuk restart dengan variabel baru

### Langkah 6: Cek Status
1. Klik tab **Deployments**
2. Klik deployment terbaru
3. Lihat **Logs** - harusnya ada: `IHSG SUPERTREND SCANNER - SCHEDULER`

---

### ✅ Selesai!
Bot akan berjalan otomatis 24/7. Cek Telegram untuk menerima alerts.

### Troubleshooting
| Issue | Solusi |
|-------|--------|
| Bot tidak jalan | Cek Logs di Railway dashboard |
| Telegram error | Pastikan TOKEN dan CHAT_ID benar |
| Crashing | Railway auto-restart, cek error di logs |

---
---

| Platform | Harga | Kelebihan |
|----------|-------|-----------|
| **DigitalOcean** | $6/bulan | Murah, stabil, tutorial lengkap |
| **Vultr** | $6/bulan | Banyak lokasi Asia |
| **Railway** | Free tier | Gratis untuk low usage |
| **Google Cloud** | Free tier 1 tahun | Gratis e2-micro |

> [!TIP]
> Rekomendasi: **DigitalOcean Droplet $6/bulan** - Cukup untuk bot ini

---

## Quick Deploy ke VPS (Ubuntu)

### Step 1: Buat VPS
1. Daftar di [DigitalOcean](https://digitalocean.com) atau [Vultr](https://vultr.com)
2. Buat Droplet/Instance:
   - OS: **Ubuntu 22.04 LTS**
   - Plan: **$6/bulan (1 vCPU, 1GB RAM)**
   - Region: **Singapore** (terdekat ke IHSG)
3. Catat IP address dan password/SSH key

### Step 2: Koneksi ke Server
```bash
ssh root@YOUR_SERVER_IP
```

### Step 3: Setup Environment
```bash
# Update system
apt update && apt upgrade -y

# Install Python dan tools
apt install -y python3 python3-pip python3-venv git

# Buat folder project
mkdir -p /opt/ihsg-scanner
cd /opt/ihsg-scanner
```

### Step 4: Upload Files
Dari komputer lokal (PowerShell/CMD):
```bash
scp -r "d:\ALGO TRADE\ihsg-supertrend-scanner\*" root@YOUR_SERVER_IP:/opt/ihsg-scanner/
```

### Step 5: Install Dependencies
```bash
cd /opt/ihsg-scanner
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 6: Test Manual
```bash
source venv/bin/activate
python scheduler.py
# Ctrl+C untuk stop jika berhasil
```

---

## Setup Auto-Start dengan Systemd

### Step 7: Buat Service File
```bash
nano /etc/systemd/system/ihsg-scanner.service
```

Paste isi berikut:
```ini
[Unit]
Description=IHSG Supertrend Scanner Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/ihsg-scanner
ExecStart=/opt/ihsg-scanner/venv/bin/python scheduler.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Step 8: Aktifkan Service
```bash
# Reload systemd
systemctl daemon-reload

# Enable auto-start on boot
systemctl enable ihsg-scanner

# Start service
systemctl start ihsg-scanner

# Cek status
systemctl status ihsg-scanner
```

---

## Perintah Berguna

| Aksi | Command |
|------|---------|
| Lihat status | `systemctl status ihsg-scanner` |
| Lihat log | `journalctl -u ihsg-scanner -f` |
| Restart | `systemctl restart ihsg-scanner` |
| Stop | `systemctl stop ihsg-scanner` |
| Start | `systemctl start ihsg-scanner` |

---

## Checklist Sebelum Deploy

- [ ] Pastikan `config/settings.py` sudah diisi TELEGRAM_BOT_TOKEN dan CHAT_ID
- [ ] Test dulu di lokal bahwa bot mengirim Telegram
- [ ] Pastikan `stocks_list.py` sudah berisi saham yang ingin di-scan
