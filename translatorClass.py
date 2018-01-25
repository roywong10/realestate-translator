import os
from funcs import *
import baidutrans
import nltk
import re
import pickle

class translator:
    with open('dict.dat', 'rb') as f:
        translateDict = pickle.load(f)
    f.close()

    def __init__(self, phraseNum, unchange_tags,delete_tags):
        self.phraseNum = phraseNum
        self.unchange_tags = unchange_tags
        self.delete_tags = delete_tags

    def build_paragraph(self,line):
        paragraph = (nltk.sent_tokenize(line))
        result = []
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
            result.append(tags)
        return result

    def build_pre_script(self,line):
        paragraph = self.build_paragraph(line)
        # tranlate based on dict key words
        translation1 = []
        for sen in paragraph:
            senLen = len(sen)
            i = -1
            while i < len(sen) - 1:
                i += 1

                # if phrase in dict
                phrase = ""
                step = 0
                tempTrans = ""
                for p in range(self.phraseNum):
                    if i + p > senLen - 1:
                        break
                    phrase += normalWord(sen[i + p][0])
                    if phrase in self.translateDict:
                        if self.translateDict[phrase]:
                            tempTrans = self.translateDict[phrase]
                            step = p
                        if phrase + 's' in self.translateDict:
                            if self.translateDict[phrase + 's']:
                                tempTrans = self.translateDict[phrase + 's']
                                step = p
                    phrase += ' '
                i += step
                if tempTrans == '#':
                    continue
                if tempTrans:
                    translation1.append(tempTrans)
                    continue
                # if of between 2 NNP tag
                if sen[i][0] == 'of' and i > 0 and i < senLen - 1:
                    if sen[i - 1][1] == 'NNP' and sen[i + 1][1] == 'NNP':
                        # print('unchange', sen[i], end="\t")
                        translation1.append('XYZ' + sen[i][0])
                        continue

                # if is tag $
                if sen[i][1] in ['$']:
                    # print('unchange', sen[i], end="\t")
                    translation1.append('XZY')
                    continue

                # if in delete tags
                if sen[i][-1] in self.delete_tags:
                    # print('delete', sen[i], end="\t")
                    continue

                # if in unchange_tags
                if sen[i][-1] in self.unchange_tags:
                    # print('unchange', sen[i], end="\t")
                    translation1.append('XYZ' + sen[i][0])
                    continue

                translation1.append(sen[i][0])
        # print()

        # build pre script
        t = translation1
        script = ""
        for i in range(len(t)):
            if i > 0:
                if t[i - 1] == 'XZY':
                    script += t[i]
                    continue
                if t[i - 1][:3] in ['XYZ', 'ZYX'] and t[i][:3] == 'XYZ':
                    script += 'ZZZ' + t[i][3:]
                    continue
                script += ' ' + t[i]
            else:
                script += t[i]
        return script

    def translate(self,line):
        script = self.build_pre_script(line)
        # translate use baidutrans Api
        try:
            translation2 = baidutrans.en_to_zh(script)
        except:
            return "Translate Failed"

        # restore the translate
        try:
            trans3 = translation2['trans_result'][0]['dst']
        except:
            return "Translate Failed: KeyError"
        # relieve un change tags
        trans3 = re.sub('[xX][zZ][yY]', '$',trans3 )
        trans3 = re.sub('[xX][yY][zZ]', '', trans3)
        trans3 = re.sub('zzz|ZZZ', ' ', trans3)
        return trans3

