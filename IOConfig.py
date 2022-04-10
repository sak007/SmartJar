import RPi.GPIO as GPIO
import time

LOCK_RELAY_PIN_1 = 8
LOCK_RELAY_PIN_2 = 10
UNLOCK_LED = 22
RELAY_BTN = 32
CONTACT_LID = 38
CONTACT_SCALE = 40

BTN_NO_CHANGE = 0
BTN_RELEASE = 1
BTN_PRESS = 2

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(LOCK_RELAY_PIN_1, GPIO.OUT)
    GPIO.setup(LOCK_RELAY_PIN_2, GPIO.OUT)
    GPIO.setup(LOCK_RELAY_PIN_2, GPIO.OUT)
    GPIO.setup(UNLOCK_LED, GPIO.OUT)
    GPIO.setup(CONTACT_LID, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(CONTACT_SCALE, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(RELAY_BTN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def turnRelaysOn():
    GPIO.output(LOCK_RELAY_PIN_1, GPIO.HIGH)
    GPIO.output(LOCK_RELAY_PIN_2, GPIO.HIGH)
def turnRelaysOff():
    GPIO.output(LOCK_RELAY_PIN_1, GPIO.LOW)
    GPIO.output(LOCK_RELAY_PIN_2, GPIO.LOW)


def readCSLid():
    return GPIO.input(CONTACT_LID)
def readCSScale():
    return GPIO.input(CONTACT_SCALE)

def turnUnlockLEDOn():
    GPIO.output(UNLOCK_LED, GPIO.HIGH)
def turnUnlockLEDOff():
    GPIO.output(UNLOCK_LED, GPIO.LOW)

class Button:
    # debounceTime is the time to sleep after a button release is detected, this prevents
    # the debounce effect, where the reading switches between low and high before finally settling
    # at low, only occurs on for button release using Radek's buttons
    def __init__(self, pin, debounceTime=.2):
        self.pin = pin
        self.lastState = GPIO.input(pin) # Track the last state of the button
        self.debounceTime = .2
    
    # Checks the state of the button and compares it to the last checked state
    # If the state has not changed, then we are waiting for button release or press,
    # If the state goes from high to low, then the button was released, 
    # If the state goes from low to high, then the button was pressed
    # Return True if button was pressed, False if the state has not changed or reset back to low
    def checkState(self):
        curState = GPIO.input(self.pin) # No change since last check
        if curState == self.lastState: 
            return BTN_NO_CHANGE
        elif curState == GPIO.LOW: # Hi -> Low, button release
            self.lastState = curState
            time.sleep(self.debounceTime)
            return BTN_RELEASE
        else: # Low -> Hi, btn press
            self.lastState = curState
            return BTN_PRESS