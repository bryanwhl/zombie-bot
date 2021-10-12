from telegram.ext import *
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode, ReplyKeyboardMarkup, KeyboardButton, Message, Bot, ReplyKeyboardRemove
import keyboards

'''
CONSTANTS
'''
FULL_NAME = 0
USERNAME = 1
HOUSE = 2
TELEGRAM_ID = 3
CODE = 4
IS_HUMAN = 5
POINTS = 6
TELEGRAM_HANDLE = 7

def query(update, context):
    chat_id = update.message.chat.id

    text = "Password?"

    update.message.reply_text(text)

    return 1


def insert_admin(update, context, db):
    chat_id = update.message.chat.id
    user_input = update.message.text

    if (user_input != "humansrule"):
        update.message.reply_text(
            text = "Sorry, invalid password. Please key in again."
        )
        return 1

    db.insert_admin(chat_id)
    text = "Admin added!"

    update.message.reply_text(text)

    return ConversationHandler.END