import os
import re
import sys

from kleinanzeigen import scraper

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from telegram import Update, Message
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import utils

jobstores = {
    'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
}
# TODO: re-enable SQLite storage for persistency
#scheduler = BackgroundScheduler(jobstores=jobstores)
scheduler = BackgroundScheduler()
scheduler.start()

last_items = {}

logger = utils.get_logger()

def start(update, context):
    """Send a message when the command /start is issued."""
    log = utils.get_logger()
    log.info('Start')
    update.message.reply_text("Cheers! Send me links to ebay-kleinanzeigen.de searches and I'll notify you when new items appear in them.")


def error(update, context):
    """Log Errors caused by Updates."""
    print('Update "%s" caused error "%s"', update, context.error)


def echo(update: Update, context):
    msg: Message = update.message

    url = update.message.text
    chat_id = update.effective_chat.id

    log = utils.get_logger()
    log.info('Started echo')

    if chat_id not in last_items:
        # Nothing here, schedule
        scheduler.add_job(echo, trigger='interval', args=(update, context), minutes=1, id=str(chat_id))
        log.info('Scheduled job')
        last_items[chat_id] = {'last_item': None, 'url': url}

    items = scraper.scrape_url(url)

    for item in items:
        if chat_id in last_items and item.url == last_items[chat_id]['last_item']:
            #log.info('Breaking the loop')
            break
        msg.reply_markdown(str(item))
        # update.message.reply_photo(item.image)
    last_items[chat_id] = {'last_item': items[0].url, 'search_url': url}


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary

    updater = Updater(bot=utils.get_bot(), use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    DEBUG = True if os.getenv("DEBUG") else False
    BOT_TOKEN = os.getenv("TG_TOKEN")
    if DEBUG:
        updater.start_polling()
        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        updater.idle()
    else:
        logger.info('Starting bot in production webhook mode')
        HOST_URL = os.environ.get("HOST_URL")
        if HOST_URL is None:
            logger.critical('HOST URL is not set!')
            sys.exit(-1)
        updater.start_webhook(listen="0.0.0.0",
                              port='8443',
                              url_path=BOT_TOKEN,
                              key='private.key',
                              cert='cert.pem',
                              webhook_url="https://{}/{}".format(HOST_URL, BOT_TOKEN))

if __name__ == '__main__':
    main()
