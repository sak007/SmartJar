from IOConfig import *
import time

def testRelay():
    print("Relay On")
    turnRelaysOn()
    turnUnlockLEDOn()
    time.sleep(10)
    print("Relay Off")
    turnRelaysOff()
    turnUnlockLEDOff()

def testContact():
    print("Activating contact sensor")
    time.sleep(3)
    for i in range(10):
        if readCSLid():
            print("Lid Contact detected")
        else:
            print("Lid contact not detected")
        if readCSScale():
            print("Scale Contact detected")
        else:
            print("Scale contact not detected")
        print("_______________________________")
        time.sleep(3)

def relayTest2():
    btn = Button(RELAY_BTN)
    relayOn = False
    while True:
        time.sleep(.01)
        if btn.checkState() == BTN_PRESS:
            if relayOn:
                print("Relay Off")
                relayOn = False
                turnRelaysOff()
                turnUnlockLEDOff()
            else:
                print("Relay On")
                relayOn = True
                turnRelaysOn()
                turnUnlockLEDOn()

def main():
    setup()
    #testRelay()
    #testContact()
    relayTest2()
    GPIO.cleanup()


if __name__ == "__main__":
    main()