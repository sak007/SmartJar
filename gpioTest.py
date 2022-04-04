from IOConfig import *
import time

def testRelay():
    print("Relay On")
    turnRelaysOn()
    time.sleep(10)
    print("Relay Off")
    turnRelaysOff()

def testContact():
    print("Activating contact sensor")
    activateContactSensor()
    time.sleep(1)
    for i in range(10):
        if readContactSensor():
            print("Contact detected")
        else:
            print("No contact detected")
        time.sleep(1)

def main():
    setup()
    #testRelay()
    testContact()
    GPIO.cleanup()


if __name__ == "__main__":
    main()