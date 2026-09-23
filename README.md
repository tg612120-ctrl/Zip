# Telegram Session → ZIP Bot

Ek chhota Telegram bot jo aapki **Telethon string session** ko `.txt` file mein
daal kar `.zip` bana deta hai, taaki use easily store/backup kiya ja sake.

## Kaise kaam karta hai
1. Bot ko `/start` karo.
2. Bot poochega apni string session bhejo.
3. Aap plain text mein session string bhejo.
4. Bot `session.zip` bana kar wapas bhej dega (isme ek `session.txt` hoti hai).

## Setup

```bash
git clone <your-repo-url>
cd tg-session-zipper
pip install -r requirements.txt
cp .env.example .env   # phir .env mein apna BOT_TOKEN daalo
export BOT_TOKEN=$(grep BOT_TOKEN .env | cut -d '=' -f2)
python bot.py
```

Ya seedha:

```bash
BOT_TOKEN="123456:ABC..." python bot.py
```

## ⚠️ Security note
Telethon string session ka matlab hai **full login access** aapke Telegram
account ka — password jaisi hi sensitive hai.

- Ye bot session string ko disk par sirf temporarily rakhta hai, zip bhejne ke
  turant baad delete kar deta hai.
- Phir bhi, is bot ko sirf apne **private/trusted bot instance** par chalao —
  kisi shared/public server par mat chalao jahan logs ya disk doosre log dekh
  sakein.
- Zip file khud encrypted nahi hai. Agar extra security chahiye to zip ko
  password-protect karo (e.g. `pyzipper` library se AES encryption).
- Kisi ko bhi apni session string ya uski zip file forward mat karo.

## Requirements
- Python 3.9+
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) v21
