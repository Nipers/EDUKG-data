from time import sleep
import requests
import random
import json
from hashlib import md5
import jsonlines

# Set your own appid/appkey.
appid = '20220312001121573'
appkey = 'RBVmEc3mLTfjm49lW62H'

# For list of language codes, please refer to `https://api.fanyi.baidu.com/doc/21`
from_lang = 'en'
to_lang =  'zh'

endpoint = 'http://api.fanyi.baidu.com'
path = '/api/trans/vip/translate'
url = endpoint + path

def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()

def translate(query):
    # query = 'Hello World! This is 1st paragraph.\nThis is 2nd paragraph.'
    # print(query)
    # Generate salt and sign

    salt = random.randint(32768, 65536)
    sign = make_md5(appid + query + str(salt) + appkey)

    # Build request
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'appid': appid, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}

    # Send request
    r = requests.post(url, params=payload, headers=headers)
    result = r.json()

    # Show response
    return result



