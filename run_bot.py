from aux import load_yaml, extract_one, extract_two, thread_pages_range
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
    def __init__(self,settings_name, credentials_name, max_urls, url_id_pattern, next_page_arg, next_page_patt):
        # Enable logging
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)
        self.settings = load_yaml(settings_name)
        self.credentials = load_yaml(credentials_name)
        self.logger = logging.getLogger(__name__)
        self.max_urls = max_urls
        self.url_id_pattern = url_id_pattern
        self.next_page_arg = next_page_arg
        self.next_page_patt = next_page_patt

    # Bot commands
    def get(self, bot, update, args):
        """Use the python requests library to get the thread"""
        self.logger.info('/get issued by "%s" with text: "%s"', update.message.chat_id, update.message.text)

        thread_html  = self.settings['fnames']['thread_html']
        cj = get_cookie_jar(self.settings['fnames']['cookies'])
        if len(args) > self.max_urls:
            update.message.reply_text("Hey 1 url at a time if you don't mind.")
            return None
        for url in args:
            id = extract_one(url, self.url_id_pattern)
            if id is None:
                bot_reply = "Not a valid url, give me something like `{0}`".format(self.url_id_pattern)
                update.message.reply_text(bot_reply)
                continue
            response = requests.get(url, cookies=cj)
            first, last = thread_pages_range(response.text, self.next_page_patt)
            #if first == last:
            #    out_file = self.settings['fnames']['thread_html'] + id + '.html'
            #    with codecs.open(out_file, 'w', 'ISO-8859-1') as f:
            #        f.write(response.text)
            #    bot.send_document(chat_id=update.message.chat_id, document=open(out_file, 'rb'))
            #    break
            for i in range(first, last + 1): #inclusive upper bound
                clean_url_re = '(' + self.url_id_pattern + ')'
                url_with_page = extract_one(url,clean_url_re) + self.next_page_arg + str(i)
                response = requests.get(url_with_page, cookies=cj)
                out_file = self.settings['fnames']['thread_html'] + id + '_page' + str(i) + '.html'
                with codecs.open(out_file, 'w', 'ISO-8859-1') as f:
                    f.write(response.text)
                bot.send_document(chat_id=update.message.chat_id, document=open(out_file, 'rb'))

    def start(self, bot, update):
        self.logger.info('/start issued by "%s"', update.message.chat_id)
        reply = "Hi there {0}".format(update.message.chat_id)
        update.message.reply_text(reply)

    def help(self, bot, update):
        """Send a message when the command /help is issued."""
        self.logger.info('/help issued by "%s"', update.message.chat_id)
        update.message.reply_text('WIP: List of commands help goes here)')

def main():
    fc_pattern = 'https:\/\/www\.forocoches\.com.+?showthread.php\?t=(\d+)'
    fc_next_page_label = '&page='
    fc_next_page_patt = 'P&aacute;g (\d+) de (\d+)'
    dw_bot = DownloadBot('config.yml','bot_credentials.yml', 1, fc_pattern, fc_next_page_label, fc_next_page_patt)
    updater = Updater(dw_bot.credentials['credentials']['token'])
    dp = updater.dispatcher

    # Register commmands
    dp.add_handler(CommandHandler("help", dw_bot.help))
    dp.add_handler(CommandHandler("start", dw_bot.start))
    dp.add_handler(CommandHandler("get", dw_bot.get, pass_args=True))

    # Start the bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
