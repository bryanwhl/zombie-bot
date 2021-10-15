from telegram.ext import *
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode, ReplyKeyboardMarkup, KeyboardButton, Message, Bot, ReplyKeyboardRemove
import keyboards
from datetime import datetime
from datetime import date

def start(update, context, db):
    chat_id = update.message.chat.id
    username = str(update.message.from_user.username)
    context.user_data["telegram_handle"] = username

    today = datetime.today()
    timestart = datetime.strptime("16/10/2021 11:00", "%d/%m/%Y %H:%M")
    timeend = datetime.strptime("16/10/2021 12:00", "%d/%m/%Y %H:%M")
    if (today < timestart or today > timeend):
        text = "Signups are closed! Signups are open from 19 Oct, 12pm to 8pm."
        update.message.reply_text(text)
        return ConversationHandler.END

    if (db.telegram_id_exist(chat_id)):
        update.message.reply_text(text = "Sorry! You have signed up before. Please contact the administrators if this is an error.")
        return ConversationHandler.END


    text = "Hi @" + username + "! Let's get you started!"
    text2 = "May I know your name (full name on matric card)?"

    update.message.reply_text(text)
    update.message.reply_text(text2)

    return 1


def get_name(update, context, db):
    chat_id = update.message.chat.id
    user_input = update.message.text
    user_input = user_input.title()

    if (db.full_name_exist(user_input)):
        update.message.reply_text(
            text = "Sorry, this name has been taken! Please contact the adminstrators if this is an error. Please insert another name."
        )
        return 1
    context.user_data["full_name"] = user_input

    text = "Your name " + user_input + " has been registered."
    text2 = "Please enter an anonymous username you would like to play with! (e.g. troller1234)"

    update.message.reply_text(text)
    update.message.reply_text(text2)

    return 2


def get_player(update, context, db):
    chat_id = update.message.chat.id
    user_input = update.message.text
    if (db.username_exist(user_input)):
        update.message.reply_text(
            text = "Sorry, this player's name has already been taken! Please use another player name."
        )
        return 2
    context.user_data["username"] = user_input

    text = "Your player name, " + \
        user_input + ", has been registered."
    text2 = "Please select your house."

    update.message.reply_text(text)
    update.message.reply_text(text2, reply_markup=keyboards.house_keyboard())

    return 3


def get_house(update, context, db):
    chat_id = update.message.chat.id
    user_input = update.message.text
    house = user_input.title()
    if not (house == "Leo" or house == "Aquila" or house == "Ursa" or house == "Draco" or house == "Noctua"):
        update.message.reply_text(
            text="Please input a correct house."
        )
        return 3
    telegram_handle = context.user_data["telegram_handle"]
    full_name = context.user_data["full_name"]
    username = context.user_data["username"]
    code = db.generate_code()
    is_human = db.assign_role(house)
    if (is_human == 0):
        role = "Zombie"
    else:
        role = "Human"

    # insert data into database here

    text = "Great! Your house, " + house + ", has been registered."
    # text2 = "You have been assigned code: " + code +  "\nThis code will be used for the game."
    text3 = "Thank you for registering for RC4's Humans Vs Zombies event. These are your details:\n\nFull Name: " + full_name + "\nUsername: " + username + "\nHouse: " + house
    text3 += "\nPress /editinfo to edit your details."
    text4 = "Sorry, there have been some issues with your registration. Please contact the administrators! Press /start to initialize new details."

    if (db.insert_user(full_name, username, house, chat_id, code, is_human, 0, telegram_handle)):
        update.message.reply_text(text)
        # update.message.reply_text(text2)
        update.message.reply_text(text3)
    else:
        update.message.reply_text(text4)

    return ConversationHandler.END
