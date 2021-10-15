from telegram.ext import *
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode, ReplyKeyboardMarkup, KeyboardButton, Message, Bot, ReplyKeyboardRemove
import keyboards

NUMBER_LEADERBOARD = 10

def show_leaderboard(update, context, db):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    number_humans = db.query_number_humans()
    number_zombies = db.query_number_zombies()
    top_10_names = db.query_top_usernames(NUMBER_LEADERBOARD)
    text = "Following are the leaderboard:\n\nHumans v.s. Zombies: \nHumans: " + str(number_humans) +  "\nZombies: " + str(number_zombies) +  "\n\nTop 10 players:\n"

    for idx, val in enumerate(top_10_names):
        text += str(idx+1) + ". " + val + "\n"

    aquila_points = db.query_house_points("Aquila")
    noctua_points = db.query_house_points("Noctua")
    draco_points = db.query_house_points("Draco")
    leo_points = db.query_house_points("Leo")
    ursa_points = db.query_house_points("Ursa")

    text += "\nHouse Average Points:" + "\nAquila: " + str(aquila_points) + "\nNoctua: " + str(noctua_points) + "\nDraco: " + str(draco_points) + "\nLeo: " + str(leo_points) + "\nUrsa: " + str(ursa_points)
    
    context.bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text,
        reply_markup=keyboards.main_menu_back()
    )

    return ConversationHandler.END
