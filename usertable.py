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


def get_table(update, context, db):
    chat_id = update.message.chat.id
    user_input = update.message.text

    db.insert_admin(chat_id)

    if (user_input != "zombiesrule"):
        update.message.reply_text(
            text = "Sorry, invalid password. Please key in again."
        )
        return 1

    text = "Following are the users full name, username, telegram handle, house, role, code, points: \n\n"

    userbase = db.query_all_users()
    for user in userbase:
        if (user[IS_HUMAN] == '1'):
            role = "Human"
        else:
            role = "Zombie"
        text += user[FULL_NAME] + ", " + user[USERNAME] + ", " + user[TELEGRAM_HANDLE] + ", " + user[HOUSE] + ", " + role + ", " + user[CODE] + ", " + str(user[POINTS]) + "\n"

    if len(text) > 4096:
        for x in range(0, len(text), 4096):
            update.message.reply_text(text[x: x+4096])
    else:
        update.message.reply_text(text)

    return ConversationHandler.END