import RPi.GPIO as GPIO

LOCK_RELAY_PIN = 8

def setup():
    GPIO.setmode(GPIO.BOARD)
    #GPIO.setup(LOCK_RELAY_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(LOCK_RELAY_PIN, GPIO.OUT)

def turnRelayOn():
    GPIO.output(LOCK_RELAY_PIN, GPIO.HIGH)
def turnRelayOff():
    GPIO.output(LOCK_RELAY_PIN, GPIO.LOW)