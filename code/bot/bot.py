#!/usr/bin/env python3
import logging
import telebot
import time
import request
import helper
import deleteAccount
import listChildren
import listParents
from datetime import datetime
from jproperties import Properties
import jarStatus

# configs = Properties()
#
# with open('user.properties', 'rb') as read_prop:
#     configs.load(read_prop)
#
# api_token = str(configs.get('api_token').data)

api_token = '5275953450:AAFSNDwpryicF8JvovlVZuliO3oMGTBwunU'
bot = telebot.TeleBot(api_token)

telebot.logger.setLevel(logging.INFO)

option = {}


# Define listener for requests by user
def listener(user_requests):
    for req in user_requests:
        if(req.content_type == 'text'):
            print("{} name:{} chat_id:{} \nmessage: {}\n".format(str(datetime.now()), str(req.chat.first_name), str(req.chat.id), str(req.text)))


bot.set_update_listener(listener)


# defines how the /start and /help commands have to be handled/processed
@bot.message_handler(commands=['start', 'menu'])
def start_and_menu_command(m):
    chat_id = m.chat.id
    if helper.user_role(chat_id) == None:
        text_intro = "Welcome to SmartJar Bot\n\n"
        bot.send_message(chat_id, text_intro)
        helper.setup_account(chat_id, bot)
    else:
        helper.home(bot, chat_id)
    return True


# defines how the /new command has to be handled/processed
@bot.message_handler(commands=['request'])
def command_add(message):
    request.run(message, bot)

@bot.message_handler(commands=['deleteAccount'])
def command_add(message):
    deleteAccount.run(message, bot)

@bot.message_handler(commands=['listChildren'])
def command_add(message):
    listChildren.run(message, bot)

@bot.message_handler(commands=['listParents'])
def command_add(message):
    listParents.run(message, bot)

@bot.message_handler(commands=['jarStatus'])
def command_add(message):
    jarStatus.run(message, bot)
def main():
    try:
        helper.init()
        bot.polling(none_stop=True)
    except Exception as e:
        logging.exception(str(e))
        time.sleep(3)
        print("Connection Timeout")


if __name__ == '__main__':
    main()
