import sys
import pickle

def normalWord(word):
    # if re.search('s$',word):
    #     r = word[:len(word)-1]
    if not word.isupper():
        word = word.lower()
    start = 0
    end = len(word) - 1
    while word[start] == " " and start < (len(word) - 1):
        start+=1
    while word[end] == " " and end > 0:
        end -=1
    return word[start: end+1]

def isEnglish(src):
    for d in src:
        if ord(d)>126:
            return False
    return True

def correctStart(word):
    a = ["-", "*", "+", "=", "/", "^", "#", "@", "~" ,"•","· ", "?"]
    if word[0] in a and len(word) == 1:
        return False
    result = word
    for i in range(len(word)):
        if word[i] in a:
            result = word[i+1:]
        else:
            return normalWord(result)
    return False

def script_pre(script ):
    return script.replace("/", " ")





