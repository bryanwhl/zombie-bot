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

def show_details(update, context, db):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    user_details = db.query_user(chat_id)

    if (user_details[IS_HUMAN] == '1'):
        role = "Human"
    else:
        role = "Zombie"

    text = "Following are the your details: \nName: " + user_details[FULL_NAME] + "\nUsername: " + user_details[USERNAME] + "\nHouse: " + user_details[HOUSE] + "\nCode: " + user_details[CODE] + "\nRole: " + role + "\nPoints: " + str(user_details[POINTS])
    text += "\n\nYou can copy code by pressing /getcode."
    context.bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text,
        reply_markup=keyboards.main_menu_back()
    )

    return ConversationHandler.END