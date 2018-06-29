import re
import os
from openpyxl import load_workbook
from nltk import sent_tokenize, word_tokenize

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

def str_join(a, b):
    return str(a) + str(b)

def build_dict_from_xlsx(dest_file):
    wb = load_workbook(filename = dest_file)
    ws = wb.active
    key_words_dict = {}

    index = 1
    while index <= ws.max_row:
        key = ws[str_join('B', index)].value
        value = ws[str_join('A', index)].value
        if key:
            key_words_dict[key] = value

        index += 1

    return key_words_dict

def build_tokenize(text):
    result = []
    for para in text.split('\n'):
        sents = sent_tokenize(para)
        result.append([])
        for sent in sents:
            words = word_tokenize(sent)
            result[-1].append(tuple(words))

    return result


def regx_replace_keywords(text, keywords_dict):
    for key, value in keywords_dict.items():
        try:
            text = re.sub(key, value, text, flags=re.IGNORECASE)
        except Exception as e:
            continue
    return text


if __name__ == "__main__":
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    # print(check_contain_chinese('中国天天hasdh'))
    # print(check_contain_chinese('xxx'))
    # print(check_contain_chinese('xx中国'))
    text = 'I love you baby, do you love me?\n oh, you will never bechave me, is it? you reall think i am a idoit?, enhancement unbeatable location moments away'
    keywords_dict = build_dict_from_xlsx(os.path.join(ROOT_DIR, 'tmp\SampleEnglishKeyword2.xlsx'))
    print(regx_replace_keywords(text, keywords_dict))


    # text = 'I love you baby, do you love me?\n oh, you will never bechave me, is it? you reall think i am a idoit?'
    # a = build_tokenize(text)
    # for i in a:
    #     print(i)





