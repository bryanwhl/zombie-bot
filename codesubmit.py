from telegram.ext import *
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode, ReplyKeyboardMarkup, KeyboardButton, Message, Bot, ReplyKeyboardRemove
import keyboards

def verify(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    text = "Please key in your friend's code."
    
    context.bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text,
        reply_markup=keyboards.main_menu_back()
    )

    return 1
    
def confirmed(update, context, db):
    chat_id = update.message.chat.id
    user_input = update.message.text
    result = db.submit_code(chat_id, user_input)

    # verify user's input here
    if (result == 0):
        update.message.reply_text(
            text = "This is an invalid code. Please try again.",
            reply_markup=keyboards.main_menu_back()
        )
        return 1
    elif (result == -1):
        update.message.reply_text(
            text = "Please do not submit your own code. Please enter another code.",
            reply_markup=keyboards.main_menu_back()
        )
        return 1
    elif (result == -2):
        update.message.reply_text(
            text = "You or your friend have submitted this code pairing before. Please enter another code.",
            reply_markup=keyboards.main_menu_back()
        )
        return 1

    # Check for conditional here
    if (result == 1): ## human submit human
        text = "Congratulations! You found a fellow survivor. Points added."
    elif (result == 2): ## human submit zombie
        text = "You have been zombified! You are now a zombie with 0 points."        
    elif (result == 3): ## zombie submit human
        text = "GRRRR! You have zombified a human... Points added."
    elif (result == 4): ## zombie submit zombie
        text = "Wrong target! You submitted a fellow zombie's code. Minus 10 points!"

    text2 = "Welcome back! Please select an option:"
    update.message.reply_text(text)
    update.message.reply_text(text=text2, reply_markup=keyboards.main_options_keyboard())

    return ConversationHandler.END