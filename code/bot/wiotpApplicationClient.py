import wiotp.sdk.application
import json
import uuid
from time import sleep
import jarHelper

class ApplicationClient:

    def __init__(self):
        f = open('properties.json')
        properties = json.load(f)
        self.typeId = properties['DEVICE_TYPE']
        self.deviceId = properties['DEVICE_ID']
        options = wiotp.sdk.application.parseConfigFile("application.yaml")
        self.client = wiotp.sdk.application.ApplicationClient(config=options)
        self.client.connect()
        self.client.deviceEventCallback = self.onMessage

    def sendCommand(self, commandId, data):
        self.client.publishCommand(self.typeId, self.deviceId, commandId, "json", data)
        print(data)
        print('Command Sent')

    def onMessage(self, event):
        print(event.eventId, event.data)
        for key in jarHelper.get_info().keys():
            if key in event.data:
                jarHelper.update(key, event.data[key])

if __name__ == "__main__":
    try:
        client = ApplicationClient()
        while True:
            eventData = {'Test' : True}
            client.sendCommand('Jar', eventData)
            sleep(5)

    except Exception as e:
        print("Exception: ", e)
