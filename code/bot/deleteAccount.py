import helper
import logging
from telebot import types
from datetime import datetime

def run(message, bot):
    chat_id = message.chat.id
    msg = 'Are you sure you want to delete the account?'
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 2
    markup.add('YES')
    markup.add('NO')
    message = bot.send_message(chat_id, msg)
    msg = bot.reply_to(message, 'Select', reply_markup=markup)
    bot.register_next_step_handler(msg, post_response_selection, bot)

def post_response_selection(message, bot):
    chat_id = message.chat.id
    response = message.text
    if response == 'YES':
        helper.delete_account(chat_id)
        bot.send_message(chat_id, 'Account deleted!')
