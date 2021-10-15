from telegram.ext import *
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode, ReplyKeyboardMarkup, KeyboardButton, Message, Bot, ReplyKeyboardRemove
import keyboards



def show_instructions(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    text = "Game Play & Rules"
    text += "\n\n- Humans accumulate points by banding together with other humans. This is done by convincing a fellow human to share their code. One of the humans then sends the code of the person they have convinced to the bot. Upon the bot’s confirmation, 10 points are added to each human's score.  Please note that only one of the humans needs to send the code."
    text += "\n\n- Zombies accumulate points by preying on humans. This is done by convincing a human to share their code. Upon the bot’s confirmation, 10 points are added to each human's score. Please note that only one of the parties involved needs to send the code."
    text += "\n\n - If a human sends the code of a zombie, they will be infected and their score reset."
    text += "\n\n- If a zombie scans a zombie's code, 10 points will be deducted from each zombie."
    text += "\n\n- You get TWICE as many points for successfully submitting the code of someone from another house."
    text += "\n\n- You can only send the same individual's code ONCE, regardless of whether they have changed roles. e.g. if SpongeBob has already sent Patrick's code to the bot previously, SpongeBob can't send it again even if he has changed roles"
    text += "\n\n- Everyone in the house that has most points per person by the end of day will get 50 points added to their final scores."

    context.bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text,
        reply_markup=keyboards.main_menu_back()
    )

    return ConversationHandler.END
