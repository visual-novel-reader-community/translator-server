#coding:utf-8
import requests
# TEST
ret = requests.post(url="http://127.0.0.1:5000/callback/requestText", data="試して".encode("utf-8"))
print(ret.text)