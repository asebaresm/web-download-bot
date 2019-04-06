from aux import load_yaml
from firefox_cookies import get_cookie_jar
from telegram.ext import Updater, InlineQueryHandler, CommandHandler

import codecs
import logging
import os
import re
import requests
import subprocess
import sys

class DownloadBot(object):
    def __init__(self,settings_name, credentials_name):
        # Enable logging
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)
        self.settings = load_yaml(settings_name)
        self.credentials = load_yaml(credentials_name)
        self.logger = logging.getLogger(__name__)

    # Bot commands
    def get(self, bot, update, args):
        """Use the python requests library to get the thread"""
        self.logger.info('/get issued by "%s" with text: "%s"', update.message.chat_id, update.message.text)

        thread_html  = self.settings['fnames']['thread_html']
        cj = get_cookie_jar(self.settings['fnames']['cookies'])
        for url in args:
            response = requests.get(url, cookies=cj)
            print (response)
            with codecs.open(self.settings['fnames']['thread_html'], 'w', 'ISO-8859-1') as f:
                f.write(response.text)
            bot.send_document(chat_id=update.message.chat_id, document=open(thread_html, 'rb'))

    def start(self, bot, update):
        self.logger.info('/start issued by "%s"', update.message.chat_id)
        reply = "Hi there {0}".format(update.message.chat_id)
        update.message.reply_text(reply)

    def help(self, bot, update):
        """Send a message when the command /help is issued."""
        self.logger.info('/help issued by "%s"', update.message.chat_id)
        update.message.reply_text('WIP: List of commands help goes here)')

def main():
    fc_bot = DownloadBot('config.yml','bot_credentials.yml')
    updater = Updater(fc_bot.credentials['credentials']['token'])
    dp = updater.dispatcher

    # Register commmands
    dp.add_handler(CommandHandler("help", fc_bot.help))
    dp.add_handler(CommandHandler("start", fc_bot.start))
    dp.add_handler(CommandHandler("get", fc_bot.get, pass_args=True))

    # Start the bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
