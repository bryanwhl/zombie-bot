import Constants as keys
from telegram.ext import *
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode, ReplyKeyboardMarkup, KeyboardButton, Message, Bot, ReplyKeyboardRemove
from functools import partial
from database import Database
import initialization

db = Database()
db.create_tables()

def main():
    updater = Updater(keys.API_KEY)
    dp = updater.dispatcher
    # Conversation for initialization
    dp.add_handler(
        ConversationHandler(
            entry_points=[CommandHandler("start", initialization.start)],
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