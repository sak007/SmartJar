import helper
import jarHelper

def run(message, bot):
    chat_id = message.chat.id
    helper.openJar(True, None)
    msg = 'Jar is open now.\nBegin Refill.\nRemove all the items, refill and close the lid.'
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 1
    markup.add('Done Refilling?')
    message = bot.send_message(chat_id, msg)
    msg = bot.reply_to(message, 'Select Response', reply_markup=markup)
    bot.register_next_step_handler(msg, post_refill, bot)


def post_refill(message, bot):
    helper.openJar(False, None)
    while jarHelper.get('lidState') != 'on':
        pass

    chat_id = message.chat.id
    message = bot.send_message(chat_id, 'Enter number of cookies added:')
    bot.register_next_step_handler(message, post_count_input, bot)


def post_count_input(message, bot):
    chat_id = message.chat.id
    # TODO: validate
    count = int(message.text)
    weight = jarHelper.setWeightPerItem(count)
