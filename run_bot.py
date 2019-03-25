from firefox_cookies import get_cookie_jar
from GrabzIt import GrabzItClient
from GrabzIt import GrabzItImageOptions
from telegram.ext import Updater, InlineQueryHandler, CommandHandler

import http.cookiejar as cookielib
import codecs
import imgkit
import logging
import os
import re
import requests
import subprocess
import sys
import yaml

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
gsettings = {}
gcredentials = {}

# Funcs
def save_cookies_lwp(cookiejar, filename):
    lwp_cookiejar = cookielib.LWPCookieJar()
    for c in cookiejar:
        args = dict(vars(c).items())
        args['rest'] = args['_rest']
        del args['_rest']
        c = cookielib.Cookie(**args)
        lwp_cookiejar.set_cookie(c)
    lwp_cookiejar.save(filename, ignore_discard=True)

def load_cookies_from_lwp(filename):
    # lwp_cookiejar = cookielib.LWPCookieJar()
    # lwp_cookiejar.load(filename, ignore_discard=True)
    lwp_cookiejar = cookielib.MozillaCookieJar(filename)
    lwp_cookiejar.load()
    return lwp_cookiejar

# Using Grabzit propietary software but you can try with open source libsself.
# I played for a while with this but everything good about it is behind a paywall
def as_image(source, output):
    global gcredentials
    key = gcredentials['credentials']['grabzit_key']
    secret = gcredentials['credentials']['grabzit_secret']
    grabzIt = GrabzItClient.GrabzItClient(key, secret)
    options = GrabzItImageOptions.GrabzItImageOptions()
    options.browserHeight = -1
    options.width = -1
    options.height = -1
    options.format = 'png'
    options.quality = 100
    grabzIt.FileToImage(source, options)
    grabzIt.SaveTo(output)  # (!) synchonous call to Grabzit API

def get(bot, update, args):
    """Use the python requests library to get the thread"""
    logger.info('/get issued by "%s" with text: "%s"', update.message.chat_id, update.message.text)

    global gsettings
    thread_html  = gsettings['fnames']['thread_html']
    cj = get_cookie_jar(gsettings['fnames']['cookies'])
    for url in args:
        response = requests.get(url, cookies=cj)
        with codecs.open(gsettings['fnames']['thread_html'], 'w', 'ISO-8859-1') as f:
            f.write(response.text)
        bot.send_document(chat_id=update.message.chat_id, document=open(thread_html, 'rb'))

def start(bot, update):
    logger.info('/start issued by "%s"', update.message.chat_id)
    reply = "Hi there {0}".format(update.message.chat_id)
    update.message.reply_text(reply)

def help(bot, update):
    """Send a message when the command /help is issued."""
    logger.info('/help issued by "%s"', update.message.chat_id)
    update.message.reply_text('WIP: List of commands help goes here)')

def load_config(fname):
    with open(fname, "r") as f:
        global gsettings
        gsettings = yaml.safe_load(f)
        return gsettings

def load_credentials(fname):
    with open(fname, "r") as f:
        global gcredentials
        gcredentials = yaml.safe_load(f)
        return gcredentials

def main():
    settings = load_config('config.yml')
    credentials = load_credentials('bot_credentials.yml')
    updater = Updater(credentials['credentials']['token'])
    dp = updater.dispatcher

    # Register commmands
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("get", get, pass_args=True))

    # Start the bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
