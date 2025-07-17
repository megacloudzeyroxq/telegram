import json
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

TOKEN = '7961842023:AAEXgSZXzfspEhJ8fwNaJgy-pjP7lBA7QkI'
GROUP_USERNAME = '@Red_Bangladesh_69'
REQUIRED_INVITES = 3

# Store invite counts here
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import time
import threading
from flask import Flask

# === KEEP ALIVE SERVER FOR REPLIT ===
app = Flask(__name__)

@app.route('/')
def home():
    return "Red_Bangladesh_69 bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8000)

threading.Thread(target=run).start()

# === BOT TOKEN & RULES ===
TOKEN = '7961842023:AAEXgSZXzfspEhJ8fwNaJgy-pjP7lBA7QkI'
REQUIRED_INVITES = 3

# === Track user invites ===
user_invite_count = {}

# === Enable Logging ===
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# === Handle New Member Joined ===
def new_member(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    new_users = update.message.new_chat_members
    inviter = update.message.from_user

    if not new_users:
        return

    count = user_invite_count.get(inviter.id, 0)
    user_invite_count[inviter.id] = count + len(new_users)

    if user_invite_count[inviter.id] >= REQUIRED_INVITES:
        try:
            context.bot.restrict_chat_member(chat_id, inviter.id, can_send_messages=True)
            update.message.reply_text(
                f"✅ {inviter.first_name}, you can now chat! You've invited {user_invite_count[inviter.id]} members."
            )
        except Exception as e:
            logger.error(f"Restrict Error: {e}")
    else:
        remaining = REQUIRED_INVITES - user_invite_count[inviter.id]
        update.message.reply_text(
            f"⚠️ {inviter.first_name}, invite {remaining} more to unlock chatting."
        )

# === Block new users from chatting until invites met ===
def restrict_new_user(update: Update, context: CallbackContext):
    user = update.message.from_user
    chat_id = update.effective_chat.id
    try:
        context.bot.restrict_chat_member(chat_id, user.id, can_send_messages=False)
        update.message.reply_text(
            f"{user.first_name}, welcome! Please invite {REQUIRED_INVITES} members to unlock chatting."
        )
    except Exception as e:
        logger.error(f"Restriction failed: {e}")

# === Handle "/start" command ===
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "👋 Welcome to Red_Bangladesh_69! Invite 3 members to unlock chatting."
    )

# === Handle messages from users without permission ===
def handle_text(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    chat_id = update.effective_chat.id
    if user_invite_count.get(user_id, 0) < REQUIRED_INVITES:
        try:
            context.bot.delete_message(chat_id=chat_id, message_id=update.message.message_id)
            needed = REQUIRED_INVITES - user_invite_count.get(user_id, 0)
            context.bot.send_message(
                chat_id=chat_id,
                text=f"❌ You must invite {needed} more members to chat."
            )
        except Exception as e:
            logger.warning(f"Message delete failed: {e}")

# === MAIN FUNCTION ===
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, new_member))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))
    dp.add_handler(MessageHandler(Filters.status_update.left_chat_member, restrict_new_user))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()t invite {REQUIRED_INVITES} members to chat. You have invited {invited} so far."
        )

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome! Invite 3 members to unlock chatting.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, new_member))
    dp.add_handler(MessageHandler(Filters.text & (~Filters.command), check_permission))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
