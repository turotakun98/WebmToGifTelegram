from telegram import Update, Message
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
import urllib.request
import urllib
import re
import os
import string
import random
import codecs

urlPattern = '^(http://www.|https://www.|http://|https://)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$'
basePath = 'files/'


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def messageReceiver(update: Update, context: CallbackContext) -> None:
    try:
        if re.match(urlPattern, update.message.text) is not None:
            filename = id_generator(6)
            while(os.path.isfile(filename)):
                filename = id_generator(6)

            opener = urllib.request.URLopener()
            opener.addheader('User-Agent', 'whatever')
            opener.retrieve(
                update.message.text, '{0}{1}.webm'.format(basePath, filename))
            msgLoading = update.message.reply_text('loading ...')
            os.system(
                'ffmpeg -i {baseDir}{filename}.webm -vf "fps=10,scale=320:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -loop 0 {baseDir}{filename}.gif'.format(baseDir=basePath, filename=filename))

            update.message.reply_animation(
                animation=open(('{0}{1}.gif'.format(basePath, filename)), 'rb'))
            msgLoading.delete()

        else:
            update.message.reply_text('Invalid url')
    except:
        update.message.reply_text('An error occured')


updater = Updater('635156026:AAElQGaPkRKafynTGQh9kMjKj0tYoojdQs4')

    updater.dispatcher.add_handler(
        MessageHandler(filters=Filters.all, callback=messageReceiver))

    updater.start_polling()
    updater.idle()
