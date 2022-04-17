from telebot import types
import os
import json
import jarHelper
from wiotpApplicationClient import ApplicationClient
from csv import writer
import datetime

CHILD_LOG_FILE = "childRequests.csv"
ADULT_LOG_FILE = "adultRequests.csv"

initial_users_map = {
    'PARENT': {},
    'CHILD': {}
}



commands = {
    'CHILD': {
        'menu': 'Display this menu',
        'start': 'Display this menu',
        'request': 'Request parent for cookie',
        'deleteAccount': 'Delete the user account'
    },
    'PARENT': {
        'menu': 'Display this menu',
        'start': 'Display this menu',
        'refill': 'Initiate Refill',
        'unlock': 'Unlock Jar',
        'listChildren': 'Display all the children registered',
        'listParents': 'Display all the parents registered',
        'deleteAccount': 'Delete the user account',
        # 'deleteChildAccount': 'TODO: Delete a specific child account',
        # 'deleteParentAccount': 'TODO: Delete a specific parent account',
        'jarStatus':'Gives the status of the jar'
    }
}

def init():
    load_users()
    jarHelper.load_jar_status()
    connectApp()

def connectApp():
    global client
    client = ApplicationClient()
    client.client.subscribeToDeviceEvents(eventId="jar")

def load_users():
    global users
    if not os.path.exists('users.json'):
        with open('users.json', 'w') as json_file:
            json.dump(initial_users_map, json_file, ensure_ascii=False, indent=4)
        users = initial_users_map
    elif os.stat('users.json').st_size != 0:
        with open('users.json') as json_file:
            users_data = json.load(json_file)
        users = format_users_data(users_data)

def format_users_data(users_data):
    data = initial_users_map
    for role in users_data.keys():
        for chat_id in users_data[role].keys():
            data[role][int(chat_id)] = users_data[role][chat_id]
    return data

def save_users():
     with open('users.json', 'w') as json_file:
        json.dump(users, json_file, ensure_ascii=False, indent=4)

def get_parents_chat_ids():
    return users['PARENT'].keys()

def get_name(chat_id):
    if chat_id in users['PARENT'].keys():
        return users['PARENT'][chat_id]
    if chat_id in users['CHILD'].keys():
        return users['CHILD'][chat_id]

def user_role(chat_id):
    if chat_id in users['PARENT'].keys():
        return 'PARENT'
    elif chat_id in users['CHILD'].keys():
        return 'CHILD'

def home(bot, chat_id):
    text_intro = 'Welcome to SmartJar Bot, ' + get_name(chat_id) + '\n\n'
    for c in commands[user_role(chat_id)]:  # generate help text out of the commands dictionary defined at the top
        text_intro += "/" + c + ": "
        text_intro += commands[user_role(chat_id)][c] + "\n\n"
    bot.send_message(chat_id, text_intro)

def delete_account(chat_id):
    role = user_role(chat_id)
    if role != None:
        del users[role][chat_id]
        save_users()

def setup_account(chat_id, bot):
    message = bot.send_message(chat_id, 'Select Role: ')
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 2
    markup.add('PARENT')
    markup.add('CHILD')
    msg = bot.reply_to(message, 'Parent or Child?', reply_markup=markup)
    bot.register_next_step_handler(message, post_role_select, bot)

def post_role_select(message, bot):
    chat_id = message.chat.id
    role = message.text
    message = bot.send_message(chat_id, 'Enter Name: ')
    bot.register_next_step_handler(message, post_name_input, bot, role)

def post_name_input(message, bot, role):
    chat_id = message.chat.id
    name = message.text
    users[role][chat_id] = name
    bot.send_message(chat_id, 'User Added!')
    save_users()
    home(bot, chat_id)

def list(bot, chat_id, role):
    msg = role + ' list:\n'
    i = 1
    for user_name in users[role].values():
        msg += str(i) + ". " + user_name + '\n'
        i += 1
    bot.send_message(chat_id, msg)

def openJar(unlock, weight):
    try:
        # client = ApplicationClient()
        eventData = {'unlock': unlock, 'weight': weight}
        client.sendCommand('jar', eventData)
        # client.client.disconnect()
    except Exception as e:
        print("Exception: ", e)

def triggerAlarm():
    try:
        eventData = {'triggerAlarm': 5}
        client.sendCommand('jar', eventData)
    except Exception as e:
        print("Exception: ", e)

def addLogs(requester, approvedBy, approvedQty, actualQty):
    if not os.path.exists(CHILD_LOG_FILE):
        with open(CHILD_LOG_FILE, 'w', newline='') as f:
            w = writer(f)
            w.writerow(['TIMESTAMP', 'REQUESTER', 'APPROVED BY', 'APPROVED QTY', 'ACTUAL QTY'])
            f.close()
    timestamp = datetime.datetime.now()
    with open(CHILD_LOG_FILE, 'a', newline='') as f:
        w = writer(f)
        w.writerow([timestamp, requester, approvedBy, approvedQty, actualQty])
        f.close()

def addAdultLogs(requester, qty):
    if not os.path.exists(ADULT_LOG_FILE):
        with open(ADULT_LOG_FILE, 'w', newline='') as f:
            w = writer(f)
            w.writerow(['TIMESTAMP', 'REQUESTER', 'QTY'])
            f.close()
    timestamp = datetime.datetime.now()
    with open(ADULT_LOG_FILE, 'a', newline='') as f:
        w = writer(f)
        w.writerow([timestamp, requester, qty])
        f.close()
