import json
import time
from datetime import datetime
from os import stat

from flask import Flask, Response, render_template

import plot
from datacollector import HIST_DIR, RT_FILE

TEMPLATES_DIR = "templates/"
application = Flask(__name__, template_folder = TEMPLATES_DIR)

#http://192.168.0.111:5000/

@application.route('/')
def index():
    return render_template('index.html')

def getHistoricalData():
    #plot.printFiles()
    files,_ = plot.getFiles(HIST_DIR)
    #print(files[0])
    data = plot.readData(HIST_DIR + files[0]).tail(240)
    return data

def wasRTDataUpdated(lastMod):
    modTime = stat(RT_FILE).st_mtime
    if modTime != lastMod:
        return True, modTime
    else:
        return False, lastMod


def getRealtimeData():
    return plot.readData(RT_FILE)

@application.route('/chart-data')
def chart_data():
    def generate_data():
        # Historical Data
        data = getHistoricalData()
        for i in range(len(data.index)):
            json_data = json.dumps(
                {'time': data["timestamp"].iloc[i].strftime('%Y-%m-%d %H:%M'), 'value': data["weight"].iloc[i]})
            yield f"data:{json_data}\n\n"

        rtLastMod = stat(RT_FILE).st_mtime
        # Realtime updates
        while True:
            rtWasUpdated, rtLastMod = wasRTDataUpdated(rtLastMod)
            if rtWasUpdated:
                data = getRealtimeData()
                json_data = json.dumps(
                    {'time': data["timestamp"].iloc[0].strftime('%Y-%m-%d %H:%M'), 'value': data["weight"].iloc[0]})
                yield f"data:{json_data}\n\n"
            time.sleep(5)

    return Response(generate_data(), mimetype='text/event-stream')


if __name__ == '__main__':
    print("Starting Flask App")
    application.run("0.0.0.0",debug=True, threaded=True)