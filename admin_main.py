import Constants as keys
from telegram.ext import *
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode, ReplyKeyboardMarkup, KeyboardButton, Message, Bot, ReplyKeyboardRemove
from functools import partial
from database import Database
import usertable
import add_admin

NUMBER_LEADERBOARD = 10

FULL_NAME = 0
USERNAME = 1
HOUSE = 2
TELEGRAM_ID = 3
CODE = 4
IS_HUMAN = 5
POINTS = 6

def show_leaderboard(update, context, db):
    chat_id = update.message.chat.id
    number_humans = db.query_number_humans()
    number_zombies = db.query_number_zombies()
    top_10_names = db.query_top_usernames(NUMBER_LEADERBOARD)
    text = "Following are the leaderboard:\n\nHumans v.s. Zombies: \nHumans: " + str(number_humans) +  "\nZombies: " + str(number_zombies) +  "\n\nTop 10 players:\n"

    for idx, val in enumerate(top_10_names):
        text += str(idx+1) + ". " + val[USERNAME] + ", " + str(val[POINTS]) + "\n"

    aquila_points = db.query_house_points("Aquila")
    noctua_points = db.query_house_points("Noctua")
    draco_points = db.query_house_points("Draco")
    leo_points = db.query_house_points("Leo")
    ursa_points = db.query_house_points("Ursa")

    text += "\nHouse Average Points:" + "\nAquila: " + str(aquila_points) + "\nNoctua: " + str(noctua_points) + "\nDraco: " + str(draco_points) + "\nLeo: " + str(leo_points) + "\nUrsa: " + str(ursa_points)
    
    update.message.reply_text(
        text=text,
    )

    return ConversationHandler.END

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

    # add admin
    dp.add_handler(
        ConversationHandler(
            entry_points=[CommandHandler("receivenotif", add_admin.query)],
            states={
                1: [MessageHandler(Filters.text, partial(add_admin.insert_admin, db=db))],
            },
            fallbacks=[],
            per_user=False
        )
    )

    # show leaderboard
    dp.add_handler(CommandHandler("leaderboard", partial(show_leaderboard, db=db)))

    updater.start_polling()
    updater.idle()


main()