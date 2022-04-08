import helper
import logging
from telebot import types
from datetime import datetime
from wiotpApplicationClient import ApplicationClient



def run(message, bot):
    chat_id = message.chat.id
    message = bot.send_message(chat_id, 'Enter number of cookies: ')
    bot.register_next_step_handler(message, post_count_input, bot)


def post_count_input(message, bot):
    chat_id = message.chat.id
    name = helper.get_name(chat_id)
    # TODO: validate
    count = int(message.text)
    for partent_chat_id in helper.get_parents_chat_ids():
        request_approval(partent_chat_id, name, count, bot, message)

def request_approval(chat_id, name, count, bot, request_message):
    msg = name + ' requested ' + str(count) + ' cookies'
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 2
    markup.add('Approve')
    markup.add('Partially Approve')
    markup.add('Reject')
    message = bot.send_message(chat_id, msg)
    msg = bot.reply_to(message, 'Select Response', reply_markup=markup)
    bot.register_next_step_handler(msg, post_response_selection, bot, count, request_message)

def post_response_selection(message, bot, count, request_message):
    chat_id = message.chat.id
    response = message.text
    if response == 'Approve':
        approve(bot, count, request_message, message)
    elif response == 'Reject':
        reject(bot, request_message, message)
    elif response == 'Partially Approve':
        partially_approve(bot, request_message, message)

def approve(bot, count, request_message, responder_message):
    parent_name = helper.get_name(responder_message.chat.id)
    msg = 'Request Approved by ' + parent_name + ' for ' + str(count) + ' cookies\n';
    msg += "Don't take more than " + str(count) + " cookies"
    bot.reply_to(request_message, msg)
    openJar(count)

def reject(bot, request_message, responder_message):
    parent_name = helper.get_name(responder_message.chat.id)
    msg = 'Sorry :( \nRequest rejected by ' + parent_name
    bot.reply_to(request_message, msg)

def partially_approve(bot, request_message, responder_message):
    chat_id = responder_message.chat.id
    message = bot.send_message(chat_id, 'Enter number of cookies: ')
    bot.register_next_step_handler(message, post_approved_count_input, bot, request_message)

def post_approved_count_input(message, bot, request_message):
    count = int(message.text)
    approve(bot, count, request_message, message)

def openJar(count):
    try:
        client = ApplicationClient()
        eventData = {'Open': True, 'Count': count}
        client.sendCommand('Jar', eventData)
        client.client.disconnect()
    except Exception as e:
        print("Exception: ", e)
