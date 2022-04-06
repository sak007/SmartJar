import warnings
warnings.simplefilter(action="ignore", category=FutureWarning) # Suppress matplotlib warnings

import matplotlib
matplotlib.use("TkAGG")

import matplotlib.pyplot as plt
from os import walk
from datetime import datetime
import pandas as pd

from datacollector import HIST_DIR

FILE_TS = "%m_%d_%Y_%H_%M_%S"
PLOT_TS = "%m/%d/%Y %H:%M:%S"
PLOT_TS2 = "%H:%M"


# Sorts the list of filenames according to their timestamps, most recent first
def sortByDT(files, ts):
	zipped = zip(files, ts)
	return zip(*sorted(zipped, reverse=True))

# Extracts the datetime string from a file name (cuts off env and .txt)
def extractTSFromFileName(file):
	return datetime.strptime(file[4:-4], FILE_TS)

def getFiles(dir):
	files = next(walk(dir))[2]
	ts = []
	for file in files:
		ts.append(extractTSFromFileName(file))
	return sortByDT(files, ts)

# Prints list of files and timestamps
def printFiles(path=HIST_DIR):
	files, ts = getFiles(path)
	for i in range(len(files)):
		print(files[i], ts[i])
	print()

# Reads env data into numpy structured array
def readData(path):
	df = pd.read_csv(path, index_col=False)
	df["timestamp"] = pd.to_datetime(df["timestamp"], format=FILE_TS)
	return df

# Creates title for plot based on timestamp start/stop
def makeTitle(data):
	start = data.iloc[0].strftime("%m/%d/%y")
	end = data.iloc[-1].strftime("%m/%d/%y")
	if start == end:
		return start
	else:
		return start + " - " + end

def main():
	files, ts = getFiles(HIST_DIR)
	data = readData(HIST_DIR + files[0])
	plt.figure()
	plt.title(makeTitle(data["timestamp"]))
	plt.xlabel("Time (H:S)")
	plt.ylabel("Weight (g)")
	plt.plot(data["timestamp"], data["weight"])
	plt.gcf().autofmt_xdate()
	plt.xlim([data["timestamp"].iloc[0], data["timestamp"].iloc[-1]]) # Set x axis range (prevent too many xticks)
	plt.gca().xaxis.set_major_formatter(matplotlib.dates.DateFormatter(PLOT_TS2))
	plt.savefig("myfig")
	plt.show()



if __name__ == "__main__":
#	printFiles()
	main()