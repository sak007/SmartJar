import helper
import jarHelper

def run(message, bot):
    chat_id = message.chat.id
    helper.openJar(True, None)
    jarHelper.resetIsNewWeight()
    itemsTaken = jarHelper.getItemsTaken()
    helper.addAdultLogs(chat_id, itemsTaken)
