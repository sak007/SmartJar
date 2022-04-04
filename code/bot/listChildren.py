import helper

def run(message, bot):
    chat_id = message.chat.id
    helper.list(bot, chat_id, 'CHILD')
