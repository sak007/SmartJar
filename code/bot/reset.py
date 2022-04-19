import os
import helper

def run(message, bot):
    if os.path.exists(helper.ADULT_LOG_FILE):
        os.remove(helper.ADULT_LOG_FILE)
    if os.path.exists(helper.CHILD_LOG_FILE):
        os.remove(helper.CHILD_LOG_FILE)
    bot.reply_to(message, "Reset Successful.")
