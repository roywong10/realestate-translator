import re

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


def check_contain_chinese(str):
    count = 0
    for ch in str:
        if u'\u4e00' <= ch <= u'\u9fff':
            count+=1
    if count:
        return count
    return False

def mssql_query(query):
    query = re.sub('(\n){2,5}', '\n', query)
    return query

def format_correct(str):
    return re.sub('\'', '"', str)

if __name__ == "__main__":
    print(check_contain_chinese('中国天天hasdh'))
    print(check_contain_chinese('xxx'))
    print(check_contain_chinese('xx中国'))





