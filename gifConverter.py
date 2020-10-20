from telegram import Update, Message
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

def hello(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Hello {update.effective_user.first_name}')

def test(update: Update, context: CallbackContext) -> None:
    

updater = Updater('635156026:AAElQGaPkRKafynTGQh9kMjKj0tYoojdQs4')

updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(MessageHandler(filters=Filters.all , callback= test))

updater.start_polling()
updater.idle()
