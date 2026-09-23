"""
Telegram Session -> ZIP Bot
----------------------------
Flow:
1. User sends /start
2. Bot asks: "Apna Telethon string session bhejo"
3. User sends the string session as plain text
4. Bot writes it to session.txt, zips it (session_<user_id>.zip),
   sends the zip back, then deletes local temp files.

Run:
    pip install -r requirements.txt
    export BOT_TOKEN="123456:ABC-your-bot-token"
    python bot.py
"""

import logging
import os
import zipfile
from pathlib import Path

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
TMP_DIR = Path("tmp_sessions")
TMP_DIR.mkdir(exist_ok=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "👋 Namaste!\n\n"
        "Apna Telethon *string session* yahan bhejo (plain text ke roop mein).\n"
        "Main usko .txt file mein daal ke .zip bana ke wapas bhej dunga.\n\n"
        "⚠️ Session string password jaisi sensitive hoti hai — sirf apne trusted "
        "bot/chat me hi use karo, kisi aur ko forward mat karo.",
        parse_mode="Markdown",
    )


async def handle_session(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (update.message.text or "").strip()
    user_id = update.effective_user.id

    if not text:
        await update.message.reply_text("Khali message mila. Session string bhejo please.")
        return

    # Basic sanity check: Telethon string sessions are fairly long base64-ish strings
    if len(text) < 20:
        await update.message.reply_text(
            "Ye session string jaisi nahi lag rahi (bahut chhoti hai). "
            "Dubara check karke bhejo."
        )
        return

    txt_path = TMP_DIR / f"session_{user_id}.txt"
    zip_path = TMP_DIR / f"session_{user_id}.zip"

    try:
        # Write session to txt
        txt_path.write_text(text, encoding="utf-8")

        # Zip it
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.write(txt_path, arcname="session.txt")

        # Send back to user
        with open(zip_path, "rb") as f:
            await update.message.reply_document(
                document=f,
                filename="session.zip",
                caption="✅ Yeh raha tumhara zipped session. Ise safe jagah rakho.",
            )
    except Exception as e:
        logger.exception("Failed to process session")
        await update.message.reply_text(f"❌ Error: {e}")
    finally:
        # Clean up temp files so session string doesn't sit on disk
        txt_path.unlink(missing_ok=True)
        zip_path.unlink(missing_ok=True)


def main() -> None:
    if not BOT_TOKEN:
        raise SystemExit("BOT_TOKEN environment variable set nahi hai. Set karke dubara run karo.")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_session))

    logger.info("Bot starting...")
    app.run_polling()


if __name__ == "__main__":
    main()
