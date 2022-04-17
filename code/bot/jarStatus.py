import json
import jarHelper

def run(message, bot):
    chat_id = message.chat.id

    msg = ''
    # msg += 'connectionStatus: ' + jarHelper.get('connectionStatus') + '\n'
    msg += 'lidState: '+ jarHelper.get('lidState')+ '\n'
    msg += 'jarOnScaleState: '+ jarHelper.get('jarOnScaleState')+ '\n'
    msg += 'lockState: ' + jarHelper.get('lockState')+ '\n'
    msg += 'weight: ' + str(round(jarHelper.get('weight') - jarHelper.get('zeroWeight')))+ 'g\n'
    msg += 'count: ' + str(jarHelper.get('count'))
    bot.send_message(chat_id, msg)
