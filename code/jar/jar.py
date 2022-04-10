import wiotp.sdk.device
import json
import uuid
import time
import statistics
from collections import deque
from scale import *
from hx711 import HX711
import RPi.GPIO as GPIO

#REF_1135_G_Radek = 430.37    # Reference Value
#CAL_WEIGHT_G_Radek = 1031    # Calibration weight grams
REF_1135_G = 428.15           # Reference Value
CAL_WEIGHT_G = 1031.76667     # Calibration weight grams
LOJ_PIN = 38                  # Lid On Jar Pin
JOS_PIN = 40                  # Jar On Scale Pin
LR_PIN = 8                    # Lock Relay Pin
HX711_DATA_PIN = 29           # HX711 Data Pin
HX711_CLK_PIN = 31            # HX711 Clock Pin

class DeviceClient:

    def __init__(self):
        f = open('properties.json')
        properties = json.load(f)
        f.close()
        self.typeId = properties['DEVICE_TYPE']
        self.deviceId = properties['DEVICE_ID']
        options = wiotp.sdk.device.parseConfigFile("device.yaml")
        self.client = wiotp.sdk.device.DeviceClient(config=options)
        self.client.commandCallback = self.commandCallback

    def connect(self):
        self.client.connect()

    def disconnect(self):
        self.client.disconnect()

    def publish(self, eventId, eventData):
        self.client.publishEvent(eventId=eventId, msgFormat="json", data=eventData, qos=2, onPublish=self.publishEventCallback)

    def publishEventCallback(self):
        #print ("Event data published!")
        pass

    def commandCallback(self, data):
        print("Command callback")
        print(data.data)

class SmartJar:

    def __init__(self):
        self.weightBuffer = deque()
        self.weightBufferSize = 5
        self.steadyStateCheckBuffer = deque()
        self.steadySteateCheckCount = 10
        self.steadyStateCheckThreshold = 5
        self.weight = 0
        self.lidOnJarState = -1   # -1 = Unknown / 1 = On / 0 = Off
        self.jarOnScaleState = -1 # -1 = Unknown / 1 = On / 0 = Off
        self.lockState = -1       # -1 = Unknown / 1 = On / 0 = Off
        self.unlockLatch = 0
        self.unlockRequestFlag = 0
        self.contactSWDebounceTimeSec = 1
        self.lidOnJarStateDebounceStartTime = 0
        self.jarOnScaleStateDebounceStartTime = 0
        self.takeWeightMeasurementFlag = 1 
        self.weightReadyFlag = 0
        self.alarmDebounceSecRem = 0
        self.cloudClient = DeviceClient()
        self.hx = HX711(HX711_DATA_PIN, HX711_CLK_PIN)
        self.hx.set_reading_format("MSB", "MSB")
        self.hx.set_reference_unit(REF_1135_G)
        self.hx.reset()
        GPIO.setup(LOJ_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Lid On Jar Contact Sensor
        GPIO.setup(JOS_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Jar On Scale Contact Sensor
        GPIO.setup(LR_PIN, GPIO.OUT)                             # Lock Relay

    def connect(self):
        self.cloudClient.connect()

    def updateSteadyStateBuffer(self,data):
        self.steadyStateCheckBuffer.append(data)
        if len(self.steadyStateCheckBuffer) > self.steadySteateCheckCount:
            # Keep the steady state buffer at the correct size
            self.steadyStateCheckBuffer.popleft()

    def isSteadyStateBufferReady(self):
        buffReadyFlag = False
        if len(self.steadyStateCheckBuffer) >= self.steadySteateCheckCount:       
            buffReadyFlag = True
        return buffReadyFlag

    # Helper function to tell if the sensor is in a steady state
    def isSteadyState(self):
        isSteadyFlag = False
        if self.isSteadyStateBufferReady() == True:
            if self.getSteadyStateBufferDelta() <= self.steadyStateCheckThreshold:
                isSteadyFlag = True
        return isSteadyFlag

    def getSteadyStateBufferDelta(self):
        return max(self.steadyStateCheckBuffer) - min(self.steadyStateCheckBuffer)

    def updateWeight(self):
        rawWeight = self.readRawWeight()

        # Update steady state buffer value
        self.updateSteadyStateBuffer(rawWeight)

        # Update calibrated weight buffer value
        self.weightBuffer.append(rawWeight + CAL_WEIGHT_G)
        if len(self.weightBuffer) > self.weightBufferSize:
            self.weightBuffer.popleft()
        self.weight = statistics.mean(self.weightBuffer)

        if self.weightReadyFlag == 0 and len(self.weightBuffer) == self.weightBufferSize and self.isSteadyState() == True:
            self.weightReadyFlag = 1

        if self.weightReadyFlag == 1 and self.takeWeightMeasurementFlag == 1 and self.isSteadyState() == True and self.lidOnJarState == 1 and self.jarOnScaleState ==1:
            self.publish("valueChange_weight", "weight",self.weight)
            self.takeWeightMeasurementFlag = 0

    # Function to monitor and publish the state of the lid on the jar and set
    # the flag that a new weight measurement needs to be taken. The contact 
    # sensor is debounced before a new lid state is determined.
    def updateLidOnJarState(self):
        lidOnJarStateNew = GPIO.input(LOJ_PIN)
        if lidOnJarStateNew == self.lidOnJarState or self.lidOnJarStateDebounceStartTime == 0:
            self.lidOnJarStateDebounceStartTime = time.time()
        elif (time.time() - self.lidOnJarStateDebounceStartTime) > self.contactSWDebounceTimeSec:
            self.lidOnJarState = lidOnJarStateNew
            self.publish("valueChange_lidState", "lidState",self.getFormattedLidState())
            if self.lidOnJarState == 0:
                self.takeWeightMeasurementFlag = 1

    # Function to monitor and publish the state of the jar on the scale. The 
    # contact sensor is debounced before a new jar on scale state is 
    # determined.
    def updateJarOnScaleState(self):
        jarOnScaleStateNew = GPIO.input(JOS_PIN)
        if jarOnScaleStateNew == self.jarOnScaleState or self.jarOnScaleStateDebounceStartTime == 0:
            self.jarOnScaleStateDebounceStartTime = time.time()
        elif (time.time() - self.jarOnScaleStateDebounceStartTime) > self.contactSWDebounceTimeSec:
            self.jarOnScaleState = jarOnScaleStateNew
            self.publish("valueChange_jarOnScaleState", "jarOnScaleState",self.getFormattedJarOnScaleState())

    # Function to control and publish the state of the lock. 
    def updateLock(self):
        # Unlock when requested
        if self.unlockRequestFlag == 1:
            self.publish("valueChange_lockState", "lockState","unlocked")
            GPIO.output(LR_PIN, GPIO.LOW)
            self.lockState = 0
            self.unlockLatch = 1
            self.unlockRequestFlag = 0

        # Don't relock until the lid has been removed
        if self.lidOnJarState == 0 and self.unlockLatch == 1:
            self.unlockLatch = 0

        # Once unlocked, and the lid has been replaced, relock
        if self.lidOnJarState == 1 and self.lockState != 1 and self.unlockLatch == 0:
            self.publish("valueChange_lockState", "lockState","locked")
            GPIO.output(LR_PIN, GPIO.HIGH)
            self.lockState = 1

    # Helper function to set the unlock request flag.
    def unlock(self):
        self.unlockRequestFlag = 1

    # Helper function to control publishing event data to the cloud service.
    def publish(self, event, tag, value):
        eventData = {tag : value}
        print("Publishing Tag: " + str(tag) + ", Value: " + str(value))
        self.cloudClient.publish(event, eventData)

    # Read raw weight from the load cell.
    def readRawWeight(self):
        rawWeight = 0
        self.hx.power_up()
        rawWeight = self.hx.get_weight(1)
        self.hx.power_down()
        return rawWeight


    # Read calibrated weight of the jar.
    def readWeight(self):
        return self.weight

    # Disconnect from the cloud service.
    def disconnect(self):
        self.cloudClient.disconnect()

    # Helper function to get formatted lid state.
    def getFormattedLidState(self):
        if self.lidOnJarState == 1:
            return "on"
        elif self.lidOnJarState == 0:
            return "off"
        else:
            return "unknown"

    # Helper function to get formatted lock state.
    def getFormattedLockState(self):
        if self.lockState == 1:
            return "on"
        elif self.lockState == 0:
            return "off"
        else:
            return "unknown"    

    # Helper function to get formatted jar on scale state.
    def getFormattedJarOnScaleState(self):
        if self.jarOnScaleState == 1:
            return "on"
        elif self.jarOnScaleState == 0:
            return "off"
        else:
            return "unknown"    

if __name__ == "__main__":
    try:
        jar = SmartJar()
        jar.connect()

        GPIO.setup(32, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Lid On Jar Contact Sensor
        prevButtonState = GPIO.input(32)

        while True:

            if GPIO.input(32) == 0 and prevButtonState == 1:
                jar.unlock()
            prevButtonState = GPIO.input(32)

            jar.updateLidOnJarState()
            jar.updateJarOnScaleState()
            jar.updateLock()
            jar.updateWeight()

            #print("Steady: " + str(jar.isSteadyState()) + ", Weight:" + str(jar.readWeight()))

    except KeyboardInterrupt as e:
        print("Disconnecting Jar From Cloud.")
        jar.disconnect()
        print("Cleaning up GPIO config.")
        GPIO.cleanup()
