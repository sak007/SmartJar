import helper
import jarHelper
from telebot import types

def run(message, bot):
    chat_id = message.chat.id
    helper.openJar(True, None)
    msg = 'Jar is open now.\nPlease empty the jar, close the lid and keep it back on the scale.'
    message = bot.send_message(chat_id, msg)
    jarHelper.waitForLidOpen()
    jarHelper.waitForNewWeight()

    jarHelper.updateZeroWeight()
    message = bot.reply_to(message, "Zero Weight Updated.")
    helper.openJar(True, None)

    msg = 'Jar is open now.\nAdd 5 items, close the lid and keep it back on the scale.'
    message = bot.send_message(chat_id, msg)
    jarHelper.waitForLidOpen()
    jarHelper.waitForNewWeight()

    jarHelper.setWeightPerItem(5)
    message = bot.reply_to(message, "Weight per item updated.")

    msg = 'Jar is open now.\nRefill the jar and close the lid and keep it back on the scale.'
    message = bot.send_message(chat_id, msg)
    jarHelper.waitForLidOpen()
    jarHelper.waitForNewWeight()

    post_refill(message, bot)



def post_refill(message, bot):
    chat_id = message.chat.id
    jarHelper.updateCount();
    msg = 'Refill process completed successfully.'
    bot.send_message(chat_id, msg)
