import sys
import codecs
import re
import pickle
import os
from funcs import *
import nltk
import xlrd

class readData:
    def __init__(self, pathToData, pathToDict):
        self.pathToData = pathToData
        self.pathToDict = pathToDict
        self.data = xlrd.open_workbook(pathToData)
        self.table = self.data.sheets()[0]
        self.nrows = self.table.nrows
        self.ncols = self.table.ncols
        self.dict = {}

    def loadDict(self):
        if os.path.exists(self.pathToDict):
            if os.path.getsize(self.pathToDict):
                with open(self.pathToDict, 'rb') as f1:
                    self.dict = pickle.load(f1)
                f1.close()
            else:
                self.dict = {}
        else:
            self.dict = {}

    def getDictLen(self):
        return len(self.dict)

    def buildDict(self):
        self.loadDict()
        prevLen = self.getDictLen()
        for rownum in range(1,self.nrows):
            row = self.table.row_values(rownum)
            if row:
                attribute = normalWord(row[0])
                if len(row[1])>0:
                    self.dict[attribute] = row[1]
        with open(self.pathToDict, 'wb') as f:
            pickle.dump(self.dict, f)
        f.close()
        print("新增{:}条数据, 共{:}条数据".format(len(self.dict) - prevLen, len(self.dict)))
        return 1

    def buildNewDict(self):
        newDict = {}
        for rownum in range(1,self.nrows):
            row = self.table.row_values(rownum)
            if row:
                attribute = normalWord(row[0])
                if len(row[1])>0:
                    newDict[attribute] = row[1]
        self.dict = newDict
        with open(self.pathToDict, 'wb') as f:
            pickle.dump(self.dict, f)
        f.close()
        print("共{:}条数据".format(len(self.dict)))
        return 1



if __name__ == '__main__':
    pathToDict = sys.argv[1]
    reader = readData('dataPhrases.xlsx', pathToDict)
    reader.buildNewDict()
    reader2 = readData('DataSingleWord.xlsx', pathToDict)
    reader2.buildDict()
    print(reader2.dict)







# file = open(pathToData, encoding="utf8")
# line = file.readline()
#
# count = 0
# while line:
#
#     lineData = nltk.word_tokenize(line)
#     if not lineData:
#         continue
#     i = 1
#     attribute = lineData[0]
#     while i < len(lineData):
#         if isEnglish(lineData[i]):
#             attribute+=' '+lineData[i]
#         else:
#             break
#         i += 1
#
#     attribute = normalWord(attribute)
#
#     # if attribute not in dict:
#     dict[attribute] = lineData[i:]
#     # else:
#     #     for w in lineData[i:]:
#     #         if w not in dict[attribute]:
#     #             dict[attribute].append(w)
#     line = file.readline()
#     print(count)
#     count+=1
# file.close()
#
# with open(pathToDict, 'wb') as f2:
#     pickle.dump(dict, f2)
# f2.close()
#
# print( "新增{:}个字典条目, 共{:}条".format(len(dict) - dictLen, len(dict)))

# pathToData = sys.argv[1]
# pathToDict = sys.argv[2]
#
# if os.path.exists(pathToDict):
#     if os.path.getsize(pathToDict):
#         with open(pathToDict, 'rb') as f1:
#             dict = pickle.load(f1)
#         f1.close()
#     else:
#         dict = {}
# else:
#     dict = {}
#
# dictLen = len(dict)
#
# file = open(pathToData, encoding="utf8")
# line = file.readline()
#
# count = 0
# while line:
#
#     lineData = nltk.word_tokenize(line)
#     if not lineData:
#         continue
#     i = 1
#     attribute = lineData[0]
#     while i < len(lineData):
#         if isEnglish(lineData[i]):
#             attribute += ' ' + lineData[i]
#         else:
#             break
#         i += 1
#
#     attribute = normalWord(attribute)
#
#     # if attribute not in dict:
#     dict[attribute] = lineData[i:]
#     # else:
#     #     for w in lineData[i:]:
#     #         if w not in dict[attribute]:
#     #             dict[attribute].append(w)
#     line = file.readline()
#     print(count)
#     count += 1
# file.close()
#
# with open(pathToDict, 'wb') as f2:
#     pickle.dump(dict, f2)
# f2.close()
#
# print("新增{:}个字典条目, 共{:}条".format(len(dict) - dictLen, len(dict)))

