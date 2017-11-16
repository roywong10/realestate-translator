import pickle
import re
import sys
import os
from funcs import *
import baidutrans
import nltk
import pymysql
import json
import pymssql
from collections import  OrderedDict
from operator import itemgetter

def build_paragraphs(lines):
    paragraphs = []
    for line in lines:
        paragraph = (nltk.sent_tokenize(line))
        paragraphs.append([])
        for sentence in paragraph:
            words = nltk.word_tokenize(sentence)
            if not words:
                continue
            words[0] = correctStart(words[0])
            while not words[0]:
                words = words[1:]
                words[0] = correctStart(words[0])
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

def translate(paragraphs, delete_tags= [], unchange_tags=[], phraseNum = 4):
    # tranlate based on dict key words
    translation1 = []
    for para in paragraphs:
        for sen in para:
            senLen = len(sen)
            i = -1
            while i < len(sen) - 1:
                i += 1

                # if phrase in dict
                phrase = ""
                step = 0
                tempTrans = ""
                for p in range(phraseNum):
                    if i + p > senLen - 1:
                        break
                    phrase += normalWord(sen[i + p][0])
                    if phrase in translateDict:
                        if translateDict[phrase]:
                            tempTrans = translateDict[phrase]
                            step = p
                        if phrase + 's' in translateDict:
                            if translateDict[phrase + 's']:
                                tempTrans = translateDict[phrase + 's']
                                step = p
                    phrase += ' '
                i += step
                if tempTrans == '#':
                    continue
                if tempTrans:
                    translation1.append(tempTrans)
                    continue
                # if of between 2 NNP tag
                if sen[i][0] == 'of' and i>0 and i <senLen-1:
                    if sen[i-1][1] == 'NNP' and sen[i+1][1] == 'NNP':
                        print('unchange', sen[i], end="\t")
                        translation1.append('XYZ' + sen[i][0])
                        continue

                # if is tag $
                if sen[i][1] in ['$']:
                    print('unchange', sen[i], end="\t")
                    translation1.append('XZY')
                    continue

                # if in delete tags
                if sen[i][-1] in delete_tags:
                    print('delete', sen[i], end="\t")
                    continue


                # if in unchange_tags
                if sen[i][-1] in unchange_tags:
                    print('unchange', sen[i], end="\t")
                    translation1.append('XYZ' + sen[i][0])
                    continue

                translation1.append(sen[i][0])
        translation1.append('\n')
    print()
    # build script
    t = translation1
    script = ""
    for i in range(len(t)):
        if i >0:
            if t[i-1] == 'XZY':
                script += t[i]
                continue
            if t[i-1][:3] in ['XYZ',  'ZYX'] and t[i][:3] == 'XYZ':
                script += 'ZZZ'+ t[i][3:]
                continue
            script += ' ' + t[i]
        else:
            script +=t[i]

    print(script)

    # print
    translation2 = baidutrans.en_to_zh(script)
    if not translation2:
        print("翻译出错")
        return False

    # restore the translate
    translation3 = []
    for p in translation2['trans_result']:
        translation3.append(p['dst'])
    # relieve un change tags
    final_translation = []
    pat1 = ['xyz', 'XYZ']
    pat2 = ['zzz','ZZZ']
    pat3 = ['xzy', 'XZY']
    for s in translation3:
        text = ""
        i = 0
        while i < len(s):
            if s[i:i + 3] in pat3:
                i += 3
                text += '$'
                continue
            if s[i:i + 3] in pat1:
                i += 3
                continue
            if s[i:i + 3] in pat2:
                i+=3
                text += ' '
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
            if len(i[1])>3:
                f.write(str(i[0]) + "\t " + str(i[1][0]) + "\t"+str(i[1][1]) + "\t" + str(i[1][2]) + "\t"+ str(i[1][-1])+"\n")
            else:
                f.write(str(i[0]) + "\t " + str(i[1][0]) + "\t" + str(i[1][1]) + "\t" + str(i[1][2]) + "\n")
    f.close()

def execute_sql_query(cur,sql):
    cur.execute(sql)
    return cur

if __name__ == '__main__':

    #### define varibles
    phraseNum = 4
    pathToDict = sys.argv[1]
    # pathToEnglish = sys.argv[2]
    pathToEnglish = 'eng4.txt'
    # delete_tags = ['CC', 'DT', 'IN', 'TO', 'VBG', 'VBN', 'VBP', 'VBZ', 'WDT']
    # delete_tags = ['CC', 'VBG', 'VBN', 'VBP', 'VBZ', 'WDT']
    unchange_tags = ['NNP', 'NNPS']
    #### define varibles end

    #### connect romote mysql
    # server = "ozhome-test-db.cwqcl73rsxql.ap-southeast-2.rds.amazonaws.com"
    # user = "ozhome_admin"
    # password = "admin_ozhome"
    # dbname = "ozhomecomau"
    # conn = pymssql.connect(host = server, user = user, password = password, database = dbname)
    # cur = conn.cursor()
    #### connect remote mysql end

    #### read dictionary
    with open(pathToDict, 'rb') as f:
        translateDict = pickle.load(f)
    f.close()
    #### read dictionary end

    #### read english script
    with open(pathToEnglish, 'r', encoding='utf8') as file:
        lines = file.readlines()
    file.close()

    #### read English script end

    ########################################################


    for l in lines:
        if l == '\n':
            continue
        print(l)
        paragraphs =   build_paragraphs([l])
        print(paragraphs)
        # print("*************delete tags = CC,IN,TO,DT ****************")
        try:
            # for ss in translate(paragraphs, ['CC','IN','TO','DT'], unchange_tags, phraseNum):
            #     print(ss)
            # print()
            print("*************delete tags = VBG,VBN,VBP,VBZ,WDT,'VBD'*****************")
            for ss in translate(paragraphs, ['VBG','VBN','VBP','VBZ','WDT','VBD'], unchange_tags, phraseNum):
                print(ss)
            # print("*************delete tags = VBG,VBN,VBP,VBZ,WDT,CC,IN,TO,VBD,DT*****************")
            # for ss in translate(paragraphs, ['VBG', 'VBN', 'VBP', 'VBZ', 'WDT','CC','IN','TO','VBD','DT'], unchange_tags, phraseNum):
            #     print(ss)
        except:
            print("出错了")
        print("======================================================\n")

    # JJ, NN= extract_phrase(paragraphs)
    # with open("NN.dict", "rb") as f:
    #     NN = pickle.load(f)
    # f.close()

    # count = 0
    # for key, value in NN.items():
    #     if value[2] >1 and len(value) <=3:
    #         try:
    #             print(key, count)
    #             count+=1
    #             trans = baidutrans.en_to_zh(key)
    #             value.append(trans['trans_result'][0]['dst'])
    #         except:
    #             print("translate failed for:", key)
    #             continue
    # with open("NN.dict", 'wb') as f:
    #     pickle.dump(NN,f)
    # f.close()
    # # write_extract(JJ, 'JJ')
    # write_extract(NN, 'NN')


    # translate process
