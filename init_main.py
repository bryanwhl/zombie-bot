import Constants as keys
from telegram.ext import *
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode, ReplyKeyboardMarkup, KeyboardButton, Message, Bot, ReplyKeyboardRemove
from functools import partial
from database import Database
import initialization

db = Database()
db.create_tables()

def welcome_message(update, context):
    chat_id = update.message.chat.id    
    username = str(update.message.from_user.username)

    text = "Welcome to the game, " + username + "."

    update.message.reply_text(text)

    return ConversationHandler.END    

def main():
    updater = Updater(keys.API_KEY)
    dp = updater.dispatcher
    # Conversation for initialization

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
            entry_points=[CommandHandler("editinfo", partial(initialization.start, db=db))],
            states={
                1: [MessageHandler(Filters.text, partial(initialization.get_name, db=db))],
                2: [MessageHandler(Filters.text, partial(initialization.get_player, db=db))],
                3: [MessageHandler(Filters.text, partial(initialization.get_house, db=db))],
            },
            fallbacks=[],
            per_user=False
        )
    )

    updater.start_polling()
    updater.idle()


main()