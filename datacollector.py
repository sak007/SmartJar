from time import sleep
from datetime import datetime
from scale import *
# https://www.waveshare.com/w/upload/7/75/BME280_Environmental_Sensor_User_Manual_EN.pdf
# https://projects.raspberrypi.org/en/projects/build-your-own-weather-station/2
MY_FLAG = 1
FILE_TS = "%m_%d_%Y_%H_%M_%S"

HIST_DIR = "data/"
RT_FILE = HIST_DIR + "realtime/realtime.txt"


def main():
    
    ts = datetime.now().strftime(FILE_TS)
    file = HIST_DIR + "env_" + ts + ".txt"

    myScale = Scale(CAL_WEIGHT_G_Radek, REF_1135_G_Radek)

    with open(file, "w") as f:
        #f.write(str(MY_FLAG) + "\n")
        f.write("timestamp,weight\n")
        while True:
            ts = datetime.now().strftime(FILE_TS)
            weight = myScale.readWeight()

            print(ts, "{:.2f}".format(weight))

            # Write Historical Data
            f.write(ts + "," + "{:.2f}".format(weight) + "," + "\n")
            f.flush()

            # Write Real time file updates
            with open(RT_FILE, "w") as rtF:
                rtF.write("timestamp,weight\n")
                rtF.write(ts + "," + "{:.2f}".format(weight) + "\n")
                rtF.flush()
            sleep(1)

if __name__ == "__main__":
    #test()
    main()