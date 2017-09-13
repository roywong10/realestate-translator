import pickle 
import re
import sys
import os
import funcs
import baidutrans
import nltk


#############
phraseNum = 3
pathToDict = sys.argv[1]
pathToEnglish = sys.argv[2]

# read dict
with open(pathToDict,'rb') as f:
    translateDict = pickle.load(f)
f.close()

# read english script
file = open(pathToEnglish)
lines = file.readlines()
file.close()
paragraphs = []

for line in lines:
    paragraph = (nltk.sent_tokenize(line))
    paragraphs.append([])
    for sentence in paragraph:
        words = nltk.word_tokenize(sentence)
        words[0] = words[0].lower()
        tags = nltk.pos_tag(words)
        paragraphs[-1].append(tags)

print(paragraphs)


# tranlate
translation1 = []
delete_tags = ['CC', 'DT', 'IN', 'TO', 'VBG', 'VBN', 'VBP', 'VBZ', 'WDT']
unchange_tags = ['NNP', 'NNPS']
for para in paragraphs:
    for sen in para:
        i = -1
        while i < len(sen)-1:
            i+=1
            translatedFlag = False
            #if phrase in dict
            phrase = ""
            for p in range(phraseNum):
                if i +p > len(sen)-1:
                    break
                phrase +=funcs.normalWord(sen[i+p][0])
                if phrase in translateDict:
                    if translateDict[phrase]:
                        translation1.append(translateDict[phrase][0])
                        translatedFlag =True
                        i+=p
                        break
                phrase+=' '

            if translatedFlag:
                continue

            if sen[i][0].lower() + 's' in translateDict:
                if translateDict[sen[i][0].lower() + 's']:
                    translation1.append(translateDict[sen[i][0].lower() + 's'][0])
                    continue

            if sen[i][-1] in delete_tags:
                print('delete', sen[i])
                continue
            #  if in unchange_tags
            if sen[i][-1] in unchange_tags:
                print('unchange', sen[i])
                translation1.append('XYZ'+sen[i][0])
                continue
            translation1.append(sen[i][0])
    translation1.append('\n')

# build script
script = ""
for s in translation1:
    script+=' '+s
print(script)

# print 



translation2 = baidutrans.en_to_zh(script)
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
        if s[i:i+3] in pat:
            i+=3
            continue
        text += s[i]
        i+=1
    final_translation.append(text)
for ss in final_translation:
    print(ss)

# print(baidutrans.en_to_zh(script))
# translate process
