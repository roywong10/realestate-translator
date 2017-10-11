import pickle
import re
import sys
import os
import funcs
import baidutrans
import nltk
import pymysql
import json
import pymssql
from collections import  OrderedDict
from operator import itemgetter

def build_paragraphs(lines, paragraphs = []):
    for line in lines:
        paragraph = (nltk.sent_tokenize(line))
        paragraphs.append([])
        for sentence in paragraph:
            words = nltk.word_tokenize(sentence)
            if not words:
                continue
            words[0] = funcs.normalWord(words[0])
            tags = nltk.pos_tag(words)
            if not tags:
                continue
            paragraphs[-1].append(tags)
    return paragraphs

def print_paragraphs(paragraphs):
    for par in paragraphs:
        for sen in par:
            for wor in sen:
                print(wor[0]+"("+wor[1]+")", end=" ")
        print("\n")

def translate(paragraphs, delete_tags= [], unchange_tags=[], phraseNum = 3):
    # tranlate
    translation1 = []
    for para in paragraphs:
        for sen in para:
            i = -1
            while i < len(sen) - 1:
                i += 1
                # if phrase in dict
                phrase = ""
                step = 0
                tempTrans = ""
                for p in range(phraseNum):
                    if i + p > len(sen) - 1:
                        break
                    phrase += funcs.normalWord(sen[i + p][0])
                    if phrase in translateDict:
                        if translateDict[phrase]:
                            tempTrans = translateDict[phrase][0]
                            step = p
                    phrase += ' '

                i += step
                if tempTrans:
                    translation1.append(tempTrans)
                    continue

                if sen[i][0].lower() + 's' in translateDict:
                    if translateDict[sen[i][0].lower() + 's']:
                        translation1.append(translateDict[sen[i][0].lower() + 's'][0])
                        continue

                if sen[i][-1] in delete_tags:
                    print('delete', sen[i])
                    continue
                # if in unchange_tags
                if sen[i][-1] in unchange_tags:
                    print('unchange', sen[i])
                    translation1.append('XYZ' + sen[i][0])
                    continue
                translation1.append(sen[i][0])
        translation1.append('\n')
    # build script
    script = ""
    for s in translation1:
        script += ' ' + s
    print(script)

    # print
    translation2 = baidutrans.en_to_zh(script)
    if not translation2:
        print("翻译出错")
        return False

    translation3 = []
    for p in translation2['trans_result']:
        translation3.append(p['dst'])
    # relieve un change tags
    final_translation = []
    pat = ['xyz', 'XYZ']
    for s in translation3:
        text = ""
        i = 0
        while i < len(s):
            if s[i:i + 3] in pat:
                i += 3
                continue
            text += s[i]
            i += 1
        final_translation.append(text)
    return final_translation

def extract_phrase(paragraphs):
    adjs = ['JJ', 'JJR', 'JJS']
    nouns = ['NN', 'NNS', 'NNP', 'NNPS']
    advs = ['RB', 'RBR', 'RBS']
    JJ= {}
    NN = {}
    for p in paragraphs:
        for s in p:
            for i in range(len(s)-1):
                if s[i][-1] in adjs:
                    if s[i+1][-1] in nouns:
                        key = s[i][0]+" "+s[i+1][0]
                        key = funcs.normalWord(key)
                        if key in JJ:
                            JJ[key][-1]+=1
                        else:
                            JJ[key] = [s[i][1], s[i+1][1], 1 ]
                if s[i][-1] in nouns:
                    if s[i+1][-1] in nouns:
                        key = s[i][0]+" "+s[i+1][0]
                        key = funcs.normalWord(key)
                        if key in NN:
                            NN[key][-1]+=1
                        else:
                            NN[key] =  [s[i][1], s[i+1][1], 1 ]
    return JJ, NN

def write_extract(dict,dictName):
    sortedDict = sorted(dict.items(), key=lambda item: item[1][2], reverse=True)
    with open(os.path.join("extracts", dictName+"_extract.txt"), "w", encoding='utf-8') as f:
        for i in sortedDict:
            f.write(str(i[0]) + "\t " + str(i[1][0]) + "\t"+str(i[1][1]) + "\t" + str(i[1][2]) + "\t"+ str(i[1][-1])+"\n")
    f.close()

def execute_sql_query(cur,sql):
    cur.execute(sql)
    return cur

if __name__ == '__main__':

    #### define varibles
    phraseNum = 3
    pathToDict = sys.argv[1]
    # pathToEnglish = sys.argv[2]
    pathToEnglish = 'descriptions.json'
    # delete_tags = ['CC', 'DT', 'IN', 'TO', 'VBG', 'VBN', 'VBP', 'VBZ', 'WDT']
    # delete_tags = ['CC', 'VBG', 'VBN', 'VBP', 'VBZ', 'WDT']
    delete_tags = ['RB']
    unchange_tags = ['NNP', 'NNPS']
    #### define varibles end

    #### connect romote mysql
    server = "ozhome-test-db.cwqcl73rsxql.ap-southeast-2.rds.amazonaws.com"
    user = "ozhome_admin"
    password = "admin_ozhome"
    dbname = "ozhomecomau"
    conn = pymssql.connect(host = server, user = user, password = password, database = dbname)
    cur = conn.cursor()
    #### connect remote mysql end

    #### read dictionary
    with open(pathToDict, 'rb') as f:
        translateDict = pickle.load(f)
    f.close()
    #### read dictionary end

    #### read english script
    with open(pathToEnglish, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    file.close()
    paragraphs = build_paragraphs(lines)
    # print_paragraphs(paragraphs)
    #### read English script end

    ########################################################
    #### test
    # sql = "select top 3 Description FROM residential"
    # result = execute_sql_query(cur, sql)
    # for row in result:
    #     print(row[0])


    # for para in paragraphs:
    #     print(para)

    # for ss in translate(paragraphs, delete_tags, unchange_tags, phraseNum):
    #     print(ss)

    JJ, NN= extract_phrase(paragraphs)
    count = 0
    for key, value in JJ.items():
        if value[2] >1:
            try:
                print(key, count)
                count+=1
                trans = baidutrans.en_to_zh(key)
                value.append(trans['trans_result']['dst'])
            except:
                print("translate failed for:", key)
                continue

    write_extract(JJ, 'JJ')
    # write_extract(NN, 'NN')


    # translate process
