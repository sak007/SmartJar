import json
import jarHelper

def run(message, bot):
    chat_id = message.chat.id
    
    msg = ''
    msg += 'connectionStatus: ' + jarHelper.get('connectionStatus') + '\n'
    msg += 'lidState: '+ jarHelper.get('lidState')+ '\n'
    msg += 'jarOnScaleState'+ jarHelper.get('jarOnScaleState')+ '\n'
    msg += 'lockState' + jarHelper('lockState')+ '\n'
    msg += 'weight' + jarHelper.get('weight')+ '\n'
    bot.send_message_(chat_id, msg)


