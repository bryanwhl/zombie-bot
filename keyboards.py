from telegram.ext import *
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode, ReplyKeyboardMarkup, KeyboardButton, Message, Bot, ReplyKeyboardRemove


# def main_options_keyboard():
#     keyboard = [
#         [InlineKeyboardButton(
#             "Welfare Events", callback_data='welfare_events')],
#         [InlineKeyboardButton("Provide Feedback", callback_data='feedback')],
#         [InlineKeyboardButton("Account Settings", callback_data='settings')]
#     ]
#     return InlineKeyboardMarkup(keyboard)


def house_keyboard():
    keyboard = [
        [KeyboardButton("Aquila")],
        [KeyboardButton("Draco")],
        [KeyboardButton("Ursa")],
        [KeyboardButton("Leo")],
        [KeyboardButton("Noctua")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, one_time_keyboard=True)

def main_options_keyboard():
    keyboard = [
        [InlineKeyboardButton(
            "Submit Unique Code", callback_data='submit_code')],
        [InlineKeyboardButton("Check Leaderboard", callback_data='leaderboard')],
        [InlineKeyboardButton("Instructions", callback_data='instructions')],
        [InlineKeyboardButton("Account Details", callback_data='account_details')],        
    ]
    return InlineKeyboardMarkup(keyboard)

def main_menu_back():
    keyboard = [[InlineKeyboardButton("Back", callback_data="return_menu")]]
    return InlineKeyboardMarkup(keyboard)