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
        if ord(d)>126:
            return False
    return True

def correctStart(word):
    a = ["-", "*", "+", "=", "/", "^", "#", "@", "~" ,"•"]
    if word[0] in a and len(word) == 1:
        return False
    result = word
    for i in range(len(word)):
        if word[i] in a:
            result = word[i+1:]
        else:
            return normalWord(result)
    return False






