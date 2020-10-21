from telegram import Update, Message
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
import urllib.request
import re
import os
import string
import random


def hello(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Hello {update.effective_user.first_name}')


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def test(update: Update, context: CallbackContext) -> None:
    regex = '^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$'
    if re.match(regex, update.message.text) is not None:
        filename = id_generator(6)
        while(os.path.isfile(filename)):
            filename = id_generator(6)

        opener = urllib.request.URLopener()
        opener.addheader('User-Agent', 'whatever')
        opener.retrieve(
            update.message.text, '/home/turotakun98/repo/gifConvertTG/{0}.webm'.format(filename))

        os.system(
            'ffmpeg -i {0}.webm -vf "fps=10,scale=320:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -loop 0 {0}.gif'.format(filename))

    else:
        print('invalid')


updater = Updater('635156026:AAElQGaPkRKafynTGQh9kMjKj0tYoojdQs4')

updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(
    MessageHandler(filters=Filters.all, callback=test))

updater.start_polling()
updater.idle()
