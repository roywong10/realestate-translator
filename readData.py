import sys
import codecs
import re
import pickle
import os
from funcs import *
import nltk

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

dictLen = len(dict)


file = open(pathToData, encoding="utf8")
line = file.readline()

while line:
    
    lineData = nltk.word_tokenize(line)
    if not lineData:
        continue
    i = 1
    attribute = lineData[0]
    while i < len(lineData):
        if isEnglish(lineData[i]):
            attribute+=' '+lineData[i]
        else:
            break
        i += 1

    attribute = normalWord(attribute)

    # if attribute not in dict:
    dict[attribute] = lineData[i:]
    # else:
    #     for w in lineData[i:]:
    #         if w not in dict[attribute]:
    #             dict[attribute].append(w)
    line = file.readline()
file.close()

with open(pathToDict, 'wb') as f2:
    pickle.dump(dict, f2)
f2.close()

print(dict)
print( "新增{:}个字典条目, 共{:}条".format(len(dict) - dictLen, len(dict)))

