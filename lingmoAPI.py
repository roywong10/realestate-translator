import requests
import time
import os
import json
import sys
from funcs import tokenize_replace_keywords, regx_replace_keywords, build_dict_from_xlsx


class lingmoAPI:
    Token = ""
    TokenExpire = ""
    TokenExpireInterval = 2 * 60 * 59
    tempDir = os.path.join(os.getcwd(), 'tmp')
    tempToken = '_token.tmp'

    def __init__(self):
        self.get_token()
        return

    def get_token(self):
        need_new_token = False
        if os.path.exists(os.path.join(self.tempDir, self.tempToken)):
            with open(os.path.join(self.tempDir, self.tempToken), 'r') as f:
                t = json.load(f)
            f.close()

            if time.time() < t['TokenExpire']:
                self.Token = t['token']
            else:
                need_new_token = True
        else:
            need_new_token = True

        if need_new_token:
            self.get_new_token()
            self.save_token()

    def get_new_token(self):
        url = "http://cmg.lingmo-api.com/v1/token/get/ChineseMediaGroup"
        r = requests.get(url)
        if r.status_code != 200:
            return False
        self.Token = r.json()['Token']
        current_time = time.time()
        self.TokenExpire = current_time + self.TokenExpireInterval

    def save_token(self):

        if not os.path.exists(self.tempDir):
            os.mkdir(self.tempDir)

        with open(os.path.join(self.tempDir, self.tempToken), 'w+') as f:
            json.dump({"token": self.Token, "TokenExpire": self.TokenExpire}, f)
        f.close()

    def token_is_valid(self):
        url = "http://cmg.lingmo-api.com/v1/token/check?id=" + self.Token
        r = requests.get(url)
        r = r.json()
        if r['Code'] != 101:
            return False
        return True

    def en_to_ch(self, data):
        url = "http://cmg.lingmo-api.com/v1/translation/dotranslate?sourceLang=en-US&targetLang=zh-CN"
        r = requests.post(url, data=data.encode('utf8'), headers={'Authorization': self.Token})
        if r.status_code == 200:
            return r.json()['ResponseText']
        return False

    def ch_to_en(self, data):
        url = "http://cmg.lingmo-api.com/v1/translation/dotranslate?sourceLang=zh-CN&targetLang=en-US"
        r = requests.post(url, data=data.encode('utf8'), headers={'Authorization': self.Token})
        if r.status_code == 200:
            return r.json()['ResponseText']
        return False

    def show_token(self):
        print(self.Token)

def api_translate_from_EN_to_CH(text=None, english_keywords_replacement_dict=None, chinese_keywords_replacement_dict=None):
    api = lingmoAPI()
    if not text or len(text) < 1:
        return ""
    if english_keywords_replacement_dict:
        value = tokenize_replace_keywords(text, english_keywords_replacement_dict)

    translation = api.en_to_ch(value)

    if chinese_keywords_replacement_dict:
        treated_translation = regx_replace_keywords(translation, chinese_keywords_replacement_dict)




if __name__ == '__main__':
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    print(sys.argv)
    if len(sys.argv) <= 1:
        sys.exit('No text provided')

    text = sys.argv[1]
    english_keywords_dict = build_dict_from_xlsx(os.path.join(ROOT_DIR, 'tmp/SampleEnglishKeyword-20180703.xlsx'), 'English')
    chinese_keywords_dict = build_dict_from_xlsx(os.path.join(ROOT_DIR, 'tmp/SampleEnglishKeyword-20180703.xlsx'), 'Chinese')
    print(api_translate_from_EN_to_CH(text, english_keywords_dict, chinese_keywords_dict))







