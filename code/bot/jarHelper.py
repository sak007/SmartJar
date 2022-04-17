import os
import json

# connectionStatus: ‘online’/’offline’
# lidState: ‘on’/’off/unknown’
# jarOnScaleState: ‘on’/’off/unknown’
# lockState: ‘locked’/’unlocked/unknown’
# weight: grams
# weightPerItem: grams

FILE_NAME = 'jar_info.json'

initial_jar_info_map = {
    # 'connectionStatus': 'unknown',
    'lidState': 'unknown',
    'jarOnScaleState': 'unknown',
    'lockState': 'unknown',
    'weight': -1,
    'weightPerItem': -1,
    'zeroWeight': -1,
    'count': -1
}

newWeight = False

def load_jar_status():
    global jar_info
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, 'w') as json_file:
            json.dump(initial_jar_info_map, json_file, ensure_ascii=False, indent=4)
        users = initial_jar_info_map
    elif os.stat(FILE_NAME).st_size != 0:
        with open(FILE_NAME) as json_file:
            jar_data = json.load(json_file)
        jar_info = format_jar_data(jar_data)

def format_jar_data(jar_data):
    jar_data['weight'] = jar_data['weight']
    return jar_data

def get_info():
    return jar_info

def save_info():
     with open(FILE_NAME, 'w') as json_file:
        json.dump(jar_info, json_file, ensure_ascii=False, indent=4)

def update(key, value):
    jar_info[key] = value
    save_info()

def get(key):
    return jar_info[key]

def setWeightPerItem(count):
    weight = get('weight') - get('zeroWeight')
    update('weightPerItem', weight/count)

def updateZeroWeight():
    update('zeroWeight', get('weight'))

def updateCount():
    count = round((get('weight') - get('zeroWeight'))/get('weightPerItem'))
    update('count', count)

def isNewWeight():
    global newWeight
    return newWeight

def resetIsNewWeight():
    global newWeight
    newWeight = False

def waitForNewWeight():
    global newWeight
    resetIsNewWeight()
    print(newWeight)
    while get('lidState') != 'on':
        # print(newWeight)
        continue
    while not newWeight:
        continue

def waitForLidOpen():
    while get('lidState') != 'off':
        continue

def getItemsTaken():
    oldWeight = get('weight')
    waitForNewWeight()
    newWeight = get('weight')
    count = round((oldWeight - newWeight)/get('weightPerItem'))
    updateCount()
    return count
