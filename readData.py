import sys
import codecs
import re
import pickle
import os
from funcs import *

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


file = open(pathToData, encoding="utf8")
line = file.readline()

while line:
    
    lineData = line.split("\t")
    attribute = normalWord(lineData[0])
    if attribute not in dict:   
        dict[attribute] = []
    for i in range(1,len(lineData)):       
        if lineData[i] and lineData[i] != '\n' and lineData[i] not in dict[attribute]:
            dict[attribute].append(lineData[i])
    line = file.readline()
file.close()

with open(pathToDict, 'wb') as f2:
    pickle.dump(dict, f2)
f2.close()

print(dict)
print(len(dict))

