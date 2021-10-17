import Constants as keys
import keyboards
import initialization
import editinfo
import codesubmit
import leaderboard
import instructions
import accountdetails
import usertable
from telegram.ext import *
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode, ReplyKeyboardMarkup, KeyboardButton, Message, Bot, ReplyKeyboardRemove
from functools import partial
from database import Database
from datetime import datetime
from datetime import date

db = Database()
db.create_tables()

FULL_NAME = 0
USERNAME = 1
HOUSE = 2
TELEGRAM_ID = 3
CODE = 4
IS_HUMAN = 5
POINTS = 6

def welcome_message(update, context):
    chat_id = update.message.chat.id    
    username = str(update.message.from_user.username)

    text = "Welcome to the game, " + username + ". Press /signup to begin!"

    update.message.reply_text(text)

    return ConversationHandler.END  

def show_home(update, context):
    chat_id = update.message.chat.id

    today = datetime.today()
    timestart = datetime.strptime("20/10/2021 19:00", "%d/%m/%Y %H:%M")
    if (today < timestart):
        text = "Game have not started! Game only starts on 20 Oct 7pm."
        update.message.reply_text(text)
        return ConversationHandler.END

    if not (db.telegram_id_exist(chat_id)):
        text = "You did not register for the game! If this is an error, please contact our administrators."
        update.message.reply_text(text=text)
        return ConversationHandler.END

    user = db.query_user(chat_id)
    if (user[IS_HUMAN] == '1'):
        role = "Human"
    else:
        role = "Zombie"

    text = "Welcome to the game! Please select an option below:"
    text2 = "You are a " + role + ". You can get your code by going to \"Account Details\" or pressing /getcode."
    update.message.reply_text(
        text=text, reply_markup=keyboards.main_options_keyboard()
    )
    update.message.reply_text(text2)

def show_back_home(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id

    ## check if chat_id exists in database here

    text = "Welcome back home! Please select one of the options:"
    context.bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text,
        reply_markup=keyboards.main_options_keyboard()
    )

    return ConversationHandler.END

def get_code(update, context):
    chat_id = update.message.chat.id
    user = db.query_user(chat_id)
    
    text = user[CODE]
    update.message.reply_text(text)
    return ConversationHandler.END

def main():
    updater = Updater(keys.API_KEY)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", welcome_message))

    dp.add_handler(
        ConversationHandler(
            entry_points=[CommandHandler("signup", partial(initialization.start, db=db))],
            states={
                1: [MessageHandler(Filters.text, partial(initialization.get_name, db=db))],
                2: [MessageHandler(Filters.text, partial(initialization.get_player, db=db))],
                3: [MessageHandler(Filters.text, partial(initialization.get_house, db=db))],
            },
            fallbacks=[],
            per_user=False
        )
    )

    dp.add_handler(
        ConversationHandler(
            entry_points=[CommandHandler("editinfo", partial(editinfo.start, db=db))],
            states={
                1: [MessageHandler(Filters.text, partial(editinfo.get_name, db=db))],
                2: [MessageHandler(Filters.text, partial(editinfo.get_player, db=db))],
                3: [MessageHandler(Filters.text, partial(editinfo.get_house, db=db))],
            },
            fallbacks=[],
            per_user=False
        )
    )

    # /start
    dp.add_handler(CommandHandler("startgame", show_home))

    # submit code
    dp.add_handler(ConversationHandler(
        entry_points=[CallbackQueryHandler(partial(codesubmit.verify), pattern="submit_code")],
        states={
            1: [MessageHandler(Filters.text, partial(codesubmit.confirmed, db=db))],
        },
        fallbacks=[CallbackQueryHandler(show_back_home, pattern="return_menu")],
        per_user=False
    ))

    # check leaderboard
    dp.add_handler(CallbackQueryHandler(partial(leaderboard.show_leaderboard, db=db), pattern="leaderboard"))

    # instructions
    dp.add_handler(CallbackQueryHandler(partial(instructions.show_instructions), pattern="instructions"))

    # account details
    dp.add_handler(CallbackQueryHandler(partial(accountdetails.show_details, db=db), pattern="account_details"))

    dp.add_handler(CallbackQueryHandler(show_back_home, pattern="return_menu"))

    # access code
    dp.add_handler(CommandHandler("getcode", partial(get_code)))


    updater.start_polling()
    updater.idle()

main()