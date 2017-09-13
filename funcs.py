import sys
import pickle

def normalWord(word):
    r = word
    # if re.search('s$',word):
    #     r = word[:len(word)-1]
    if not word.isupper():
        r = r.lower()
    return r

def isEnglish(src):
    for d in src:
        if ord(d)>122:
            return False
    return True
