import json
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

TOKEN = '7961842023:AAEXgSZXzfspEhJ8fwNaJgy-pjP7lBA7QkI'
GROUP_USERNAME = '@Red_Bangladesh_69'
REQUIRED_INVITES = 3

# Store invite counts here
try:
    with open("invites.json", "r") as f:
        data = json.load(f)
except:
    data = {}

def save():
    with open("invites.json", "w") as f:
        json.dump(data, f)

def new_member(update: Update, context: CallbackContext):
    inviter = update.message.from_user
    for member in update.message.new_chat_members:
        inviter_id = str(inviter.id)
        data.setdefault(inviter_id, 0)
        data[inviter_id] += 1
        save()

        if data[inviter_id] == REQUIRED_INVITES:
            context.bot.send_message(
                chat_id=update.message.chat_id,
                text=f"🎉 {inviter.first_name}, you have invited {REQUIRED_INVITES} members! You can now chat freely."
            )

def check_permission(update: Update, context: CallbackContext):
    user_id = str(update.message.from_user.id)
    invited = data.get(user_id, 0)
    if invited < REQUIRED_INVITES:
        try:
            context.bot.delete_message(update.message.chat_id, update.message.message_id)
        except:
            pass
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=f"🚫 You must invite {REQUIRED_INVITES} members to chat. You have invited {invited} so far."
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
