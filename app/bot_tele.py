from app.glo import *
import telebot
from telebot import types
import json
# from telegram import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode

BOT_ALERT = telebot.TeleBot(TOKEN_ALERT)
# BOT_GROUP_Zero = telebot.TeleBot(TOKEN_GROUP[0])
BOT_GROUP = []
for token in TOKEN_GROUP:
    BOT_GROUP.append(telebot.TeleBot(token))

BOT_ALERT_ID = int(TOKEN_ALERT.split(":")[0])
BOT_GROUP_ID = int(TOKEN_GROUP[0].split(":")[0])

def get_channel_info(link="", channel_id=0):
    try:
        if link != "":
            target_xet = link.split("/")[3]
            channel_info = BOT_GROUP[0].get_chat("@" + target_xet)
            is_url = True
            gr_id = channel_info.id
            gr_title = channel_info.title
            gr_username = channel_info.username

            is_member = BOT_GROUP[0].get_chat_member(gr_id, BOT_GROUP_ID).status != "left"
        elif channel_id != 0:
            channel_info = BOT_GROUP[0].get_chat(channel_id)
            is_url = True
            gr_id = channel_info.id
            gr_title = channel_info.title
            gr_username = channel_info.username

            is_member = BOT_GROUP[0].get_chat_member(gr_id, BOT_GROUP_ID).status != "left"
        else:
            is_url = False
            is_member = False
            gr_id = 0
            gr_title = ""
            gr_username = ""

    except:
        is_url = False
        is_member = False
        gr_id = 0
        gr_title = ""
        gr_username = ""
    return is_url, is_member, gr_id, gr_title, gr_username

def send_signal(bot, chat_id, text, reply_id=0):
    try:
        mess_id = bot.send_message(chat_id=chat_id,
                                   text=text,
                                   parse_mode='HTML',
                                   reply_to_message_id=reply_id,
                                   disable_web_page_preview=True).id
        return mess_id, "Send done"
    except Exception as e:
        print("Cant send mess to ", chat_id, " - ", str(e))
        return -1, str(e)