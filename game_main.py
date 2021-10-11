import Constants as keys
import keyboards
import initialization
import codesubmit
import leaderboard
import instructions
import accountdetails
import usertable
from telegram.ext import *
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode, ReplyKeyboardMarkup, KeyboardButton, Message, Bot, ReplyKeyboardRemove
from functools import partial
from database import Database

db = Database()
#db.create_tables()

def show_home(update, context):
    chat_id = update.message.chat.id

    if not (db.telegram_id_exist(chat_id)):
        text = "You did not register for the game! If this is an error, please contact our administrators."
        update.message.reply_text(text=text)
        return ConversationHandler.END

    text = "Welcome to the game! Please select an option below:"
    update.message.reply_text(
        text=text, reply_markup=keyboards.main_options_keyboard()
    )

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

def main():
    updater = Updater(keys.API_KEY)
    dp = updater.dispatcher

    # /start
    dp.add_handler(CommandHandler("start", show_home))

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


    updater.start_polling()
    updater.idle()

main()