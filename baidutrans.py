#-*-coding:utf-8-*-
import json
import urllib.request, urllib.error, urllib.parse
import sys
import imp
imp.reload(sys)
# sys.setdefaultencoding('utf-8')
import hashlib

def md5(str):#生成md5
    m = hashlib.md5()
    m.update(str.encode(encoding= 'utf-8'))
    return m.hexdigest()
def auto_to_zh(src):#英译中
    ApiKey = "20170912000082297"
    pwd = "RKsWYtiRhv67PVccG62G"
    salt = "1435660288"
    all = ApiKey + src + salt + pwd
    sign = md5(all)
    url = "http://api.fanyi.baidu.com/api/trans/vip/translate?q="\
          + src + "&from=auto&to=zh&appid=" + ApiKey + \
          "&salt=" + salt + "&sign=" + sign
    try:
        # req = urllib.request.Request(url)
        res = urllib.request.urlopen(url)
        data = json.loads(res.read().decode('utf-8'))
        return data
    except:
        return "出错了"

def en_to_zh(src):#英译中
    ApiKey = "20170912000082297"
    pwd = "RKsWYtiRhv67PVccG62G"
    salt = "1435660288"
    all = ApiKey + src + salt + pwd
    sign = md5(all)
    url = "http://api.fanyi.baidu.com/api/trans/vip/translate?q="\
          + urllib.parse.quote(src) + "&from=en&to=zh&appid=" + ApiKey + \
          "&salt=" + salt + "&sign=" + sign
    try:
        # req = urllib.request.Request(url)
        res = urllib.request.urlopen(url)
        data = json.loads(res.read().decode('utf-8'))
        return data
    except:
        return False

def zh_to_en(src):#中译英
    ApiKey = "20170912000082297"
    pwd = "RKsWYtiRhv67PVccG62G"
    salt = "1435660288"
    all = ApiKey + src + salt + pwd
    sign = md5(all)
    url = "http://api.fanyi.baidu.com/api/trans/vip/translate?q="\
          + src + "&from=zh&to=en&appid=" + ApiKey + \
          "&salt=" + salt + "&sign=" + sign
    try:
        req = urllib.request.Request(url)
        con = urllib.request.urlopen(req)
        res = json.load(con)
        return res['trans_result'][0]['dst']
    except:
        return False

# def main():
#     choice = input("English to Chinese:Enter 1 \n"
#                       "Chinese to English:Enter 2 \n"
#                       "Enter:")
#     if choice == "1":
#         while True:
#             word = input("Input the word you want to search:")
#             print("translate......")
#             target = en_to_zh(word)
#             print(target)
#     else:
#         while True:
#             word = input("Input the word you want to search:")
#             print("translate......")
#             target = zh_to_en(word)
#             print(target)

# if __name__ == '__main__':
#     main()
