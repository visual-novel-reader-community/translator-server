#-*- coding:utf-8 -*-
# server.py
# Copyright (C) 2020 VNR Community（仮）.
# 
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License version 2 as 
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
# 
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License version 2 for more details.
# 
#   You should have received a copy of the GNU General Public License
#   version 2 along with this program. If not, see
#   <http://www.gnu.org/licenses/>.
# 

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
import os
import html

BAIDU = 1
GOOGLE = 1
if GOOGLE:
    translate_client = translate.Client()

"""
requestText
Take input postData, and return  translated text
"""
@app.route('/callback/reportText', methods=['POST'])
def requestText():
    text = request.data.decode('utf-8')
    print("\n", flush=True)
    print(text, flush=True)
    print("", flush=True)
    if BAIDU:
        print(baidu_translate(text), flush=True)
        print("", flush=True)
    if GOOGLE:
        print(google_translate(text), flush=True)
        print("", flush=True)
    print("==========", flush=True)

    return "OK"


"""
baidu_translate
Translate to Chinese using baidu open api
"""
def baidu_translate(q):
    q = q.replace("\n", " ")
    logging.info(q)
    appid = os.environ.get("BAIDU_API_APPID")  # 填写你的appid
    secretKey = os.environ.get("BAIDU_API_SECRETKEY")  # 填写你的密钥

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
    text = translate_client.translate(q, target_language="zh")["translatedText"]
    text += "\n" + translate_client.translate(q, target_language="en")["translatedText"]
    logging.info(f"Translated {text}")
    return html.unescape(text)


if __name__ == '__main__':
    logging.getLogger('werkzeug').setLevel(logging.ERROR)
    app.run(host='127.0.0.1', port=12345)

