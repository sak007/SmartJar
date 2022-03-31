from IOConfig import *
import time

def testRelay():
    for i in range(3):
        print("Relay On")
        turnRelayOn()
        time.sleep(2)
        print("Relay Off")
        turnRelayOff()
        time.sleep(2)

def main():
    setup()
    testRelay()
    GPIO.cleanup()


if __name__ == "__main__":
    main()