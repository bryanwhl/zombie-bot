import Constants as keys
from telegram.ext import *
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode, ReplyKeyboardMarkup, KeyboardButton, Message, Bot, ReplyKeyboardRemove
from functools import partial
from database import Database
import usertable

db = Database()
# db.create_tables()

def main():
    updater = Updater(keys.API_KEY_ADMIN)
    dp = updater.dispatcher

    # check user table
    dp.add_handler(
        ConversationHandler(
            entry_points=[CommandHandler("usertable", usertable.query)],
            states={
                1: [MessageHandler(Filters.text, partial(usertable.get_table, db=db))],
            },
            fallbacks=[],
            per_user=False
        )
    )

    updater.start_polling()
    updater.idle()


main()