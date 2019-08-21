#!/usr/bin/env python3
# coding=utf-8

import os
from urllib.parse import urlparse

from dotenv import load_dotenv
from requests import Request
from telegram import ParseMode
from telegram.ext import Updater, MessageHandler, Filters

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')


def convert_tvkinoradio_link_to_iv(bot, update):
    source_url = update.effective_message.text
    if not source_url or not source_url.startswith('https://tvkinoradio.ru/'):
        source_url = update.effective_message.entities[0].url
    if not source_url or not source_url.startswith('https://tvkinoradio.ru/'):
        return
    chat_id = update.effective_chat.id
    message_id = update.effective_message.message_id
    tvkinoradio_url = urlparse(source_url)._replace(query='').geturl()
    url = 'https://t.me/iv'
    params = {'rhash': '64dd90f37f7751', 'url': tvkinoradio_url}
    request = Request(url=url, params=params)
    request = request.prepare()
    iv_url = request.url
    camera_emoji = b'\xF0\x9F\x93\xB9'.decode('utf8')
    new_text = "[IV]({}) {} [Открыть сайт]({})".format(iv_url, camera_emoji, tvkinoradio_url)
    bot.delete_message(chat_id, message_id)
    bot.sendMessage(chat_id, text=new_text, parse_mode=ParseMode.MARKDOWN)


if __name__ == '__main__':
    updater = Updater(BOT_TOKEN, workers=1)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text, convert_tvkinoradio_link_to_iv))
    updater.start_polling(timeout=10)
    updater.idle()
