import helper
from telebot import types
import csv

def run(message, bot):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 2
    markup.add('PARENT')
    markup.add('CHILD')
    msg = "Who's history do you want to see?"
    message = bot.send_message(chat_id, msg)
    msg = bot.reply_to(message, 'Select Response', reply_markup=markup)
    bot.register_next_step_handler(msg, post_type_select, bot)

def post_type_select(message, bot):
    chat_id = message.chat.id
    file = None
    msg = None
    fields = None
    if message.text == 'PARENT':
        file  = helper.ADULT_LOG_FILE
        fields = ["TIMESTAMP", "REQUESTER", "QTY"]
    elif message.text == 'CHILD':
        file = helper.CHILD_LOG_FILE
        fields = ["TIMESTAMP", "REQUESTER", "APPROVED BY", "APPROVED QTY", "ACTUAL QTY"]
    helper.sendTable(bot, chat_id, file, fields)
