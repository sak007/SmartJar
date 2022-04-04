import RPi.GPIO as GPIO

LOCK_RELAY_PIN_1 = 8
LOCK_RELAY_PIN_2 = 10
CONTACT_OUT = 38
CONTACT_IN = 40

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(LOCK_RELAY_PIN_1, GPIO.OUT)
    GPIO.setup(LOCK_RELAY_PIN_2, GPIO.OUT)
    GPIO.setup(LOCK_RELAY_PIN_2, GPIO.OUT)
    GPIO.setup(CONTACT_OUT, GPIO.OUT)
    GPIO.setup(CONTACT_IN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def turnRelaysOn():
    GPIO.output(LOCK_RELAY_PIN_1, GPIO.HIGH)
    GPIO.output(LOCK_RELAY_PIN_2, GPIO.HIGH)
def turnRelaysOff():
    GPIO.output(LOCK_RELAY_PIN_1, GPIO.LOW)
    GPIO.output(LOCK_RELAY_PIN_2, GPIO.LOW)

def activateContactSensor():
    GPIO.output(CONTACT_OUT, GPIO.HIGH)
def deactivateContactSensor():
    GPIO.output(CONTACT_OUT, GPIO.LOW)

def readContactSensor():
    return GPIO.input(CONTACT_IN)