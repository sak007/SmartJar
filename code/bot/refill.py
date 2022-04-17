import helper
import jarHelper
from telebot import types

def run(message, bot):
    chat_id = message.chat.id
    helper.openJar(True, None)
    msg = 'Jar is open now.\nPlease empty the jar and place it back on the scale.'
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 1
    markup.add('Done Emptying?')
    message = bot.send_message(chat_id, msg)
    msg = bot.reply_to(message, 'Select Response', reply_markup=markup)
    bot.register_next_step_handler(msg, post_empty, bot)

def post_empty(message, bot):
    chat_id = message.chat.id
    jarHelper.updateZeroWeight()
    helper.openJar(True, None)
    msg = 'Jar is open now.\nAdd 5 items and close the lid.'
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 1
    markup.add('Done Refilling?')
    message = bot.send_message(chat_id, msg)
    msg = bot.reply_to(message, 'Select Response', reply_markup=markup)
    bot.register_next_step_handler(msg, post_initial_refill, bot)

def post_initial_refill(message, bot):
    chat_id = message.chat.id
    weight = jarHelper.setWeightPerItem(5)

    helper.openJar(True, None)
    msg = 'Jar is open now.\nRefill the jar and close the lid.'
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 1
    markup.add('Done Refilling?')
    message = bot.send_message(chat_id, msg)
    msg = bot.reply_to(message, 'Select Response', reply_markup=markup)
    bot.register_next_step_handler(msg, post_refill, bot)

def post_refill(message, bot):
    chat_id = message.chat.id
    jarHelper.updateCount();
    msg = 'Refill completed.'
    bot.send_message(chat_id, msg)
