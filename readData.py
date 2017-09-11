import sys
import codecs
import re
import pickle
import os

pathToData = sys.argv[1] 
pathToDict = sys.argv[2]

if os.path.exists(pathToDict):
    if os.path.getsize(pathToDict):
        with open(pathToDict, 'rb') as f1:
            dict = pickle.load(f1)
        f1.close()
    else:
        dict = {}
else:
    dict = {}


print(dict)
print(len(dict))


file = open(pathToData, encoding="utf8")
line = file.readline()

while line:
    line = file.readline()
    lineData = line.split("\t")
    if lineData[0] not in dict:
        dict[lineData[0]] = []
    for i in range(1,len(lineData)):       
        if lineData[i] and lineData[i] != '\n' and lineData[i] not in dict[lineData[0]]:
            dict[lineData[0]].append(lineData[i])
file.close()

with open(pathToDict, 'wb') as f2:
    pickle.dump(dict, f2)
f2.close()

