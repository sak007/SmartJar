# Based on https://github.com/tatobari/hx711py
# Depending on the quality of the scale setup, the zero point can easily range +-20 g (Radek's setup)
# This may also be due to the nature of the load cell (It sucks!)
# In otherwords 0 will not read as 0 but -20 <-> 20, same goes for any reading
# This seems to occur b/c the load cell cannot relax in the same way each time it is loaded and unloaded

from hx711 import HX711
import RPi.GPIO as GPIO
import time

REF_1135_G_Radek = 430.37    # Reference Value
CAL_WEIGHT_G_Radek = 1135    # Calibration weight grams

# Wraps around the HX711 class to make it easier to use
# Needs to know the calibration weight and the reference unit obtained from
# running calibration()

class Scale:
    def __init__(self, calWeight, referenceUnit):
        self.calWeight = calWeight
        self.hx = HX711(5, 6)
        self.hx.set_reading_format("MSB", "MSB")
        self.hx.set_reference_unit(referenceUnit)
        self.hx.reset()
    
    # Untared readings need to subtract half the calibration weight
    def readWeight(self):
        return self.hx.get_weight(5) + self.calWeight / 2

    # Set current reading as 0, only use in calibration()
    def tare(self):
        self.hx.tare()

# Used to get the reference value
# Make sure to record the reference value and the weight you used
def calibration():
    myScale = Scale(0, 1)
    print()
    a = input("Remove all weight from the scale and hit enter when ready")
    myScale.tare()
    zeroReadings = []
    print("Reading 10 values")
    for i in range(10):
        val = myScale.readWeight()
        zeroReadings.append(val)
        print(val)
        time.sleep(.1)
    print()
    a = input("Load weight and enter the weight used in grams:   ")
    calReadings = []
    print("Reading 10 values")
    for i in range(10):
        val = myScale.readWeight()
        calReadings.append(val)
        print(val)
        time.sleep(.1)

    zero = sum(zeroReadings) / len(zeroReadings)
    cal = sum(calReadings) / len(calReadings)

    referenceValue = (cal - zero) / int(a)
    print()
    print("Calibration weight: ", int(a))
    print("Reference value: {:.2f}".format(referenceValue))


# Sample reading of the scale
def main():
    myScale = Scale(CAL_WEIGHT_G_Radek, REF_1135_G_Radek)
    while True:
        try:
            print(myScale.readWeight())
            time.sleep(.1)

        except (KeyboardInterrupt, SystemExit):
            GPIO.cleanup()
            break


if __name__ == "__main__":
    #calibration()
    main()