import pickle 
import re
import sys
import os
import funcs

pathToDict = sys.argv[1]
pathToEnglish = sys.argv[2]

# read dict 
with open(pathToDict,'rb') as f:
    translateDict = pickle.load(f)
f.close()

# read english script
file = open(pathToEnglish)
line = file.readline()
script = []

while line:
    print(line)
    script.extend(line.split(" "))
    script.append('\n')
    line = file.readline()

file.close()

translation = []
# tranlate
for w in script:
    if w[-1] == '\n' and len(w)>1:
        w = w[:-1]
    if w in translateDict:
        if translateDict[w]:
            translation.append(translateDict[w][0])
            continue
    elif w.lower() in translateDict:
        if translateDict[w.lower()]:
            translation.append(translateDict[w.lower()][0])
            continue
    elif w.lower()+'s' in translateDict:
        if translateDict[w.lower() + 's']:
            translation.append(translateDict[w.lower() + 's'][0])
            continue
  
    elif w.upper() in translateDict:
        if translateDict[w.upper()]:
            translation.append(translateDict[w.upper()][0])
            continue
    translation.append(w)



# print 

print('\n###################\n')

for i in translation:
    print(i,end=' ')

# translate process
