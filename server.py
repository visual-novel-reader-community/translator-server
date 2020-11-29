#-*- coding:utf-8 -*-
from flask import Flask
from flask import request
app = Flask(__name__)
import http.client
import hashlib
import urllib
import random
import json
from google.cloud import translate_v2 as translate
import logging
import requests

BAIDU = 1
GOOGLE = 0
if GOOGLE:
    translate_client = translate.Client()

"""
requestText
Take input postData, and return  translated text
"""
@app.route('/callback/requestText', methods=['POST'])
def requestText():
    text = request.data.decode('utf-8')
    if BAIDU:
        ret = baidu_translate(text)
    elif GOOGLE:
        ret = google_translate(text)

    return ret


"""
baidu_translate
Translate to Chinese using baidu open api
"""
def baidu_translate(q):
    logging.info(q)
    appid = ''  # 填写你的appid
    secretKey = ''  # 填写你的密钥

    httpClient = None
    myurl = '/api/trans/vip/translate'

    fromLang = 'auto'   #原文语种
    toLang = 'zh'   #译文语种
    salt = random.randint(32768, 65536)
    sign = appid + q + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(salt) + '&sign=' + sign

    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)

        # response是HTTPResponse对象
        response = httpClient.getresponse()
        result_all = response.read().decode("utf-8")
        result = json.loads(result_all)

        if httpClient:
                    httpClient.close()

        logging.info(f"Translated {result['trans_result'][0]['dst']}")
        return result["trans_result"][0]["dst"]


    except Exception as e:
        print (e)

        if httpClient:
            httpClient.close()

        logging.error("Error Translating Baidu API")
        return "Error"

"""
google_translate
Translate to Chinese using Google API
"""
def google_translate(q):
    if not translate_client:
        logging.error("Translate client google not available")
    text = translate_client.translate(q, target_language="zh")
    logging.info(f"Translated {text}")
    return text





if __name__ == '__main__':
    app.run()

