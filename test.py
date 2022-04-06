'''
Author: xyx
Date: 2022-04-06 16:23:55
LastEditTime: 2022-04-06 16:24:56
'''
# -*- coding = utf-8 -*-
# @Time : 2022/4/6 14:12
# @Author : 谢扬筱
# @File : test.py



import requests
import CWRU_URL

response=requests.get(url="https://engineering.case.edu/sites/default/files/97.mat",stream=True)
total=int(response.headers.get("content-length"))
print(total)

for save_name,url in CWRU_URL.URLS["Normal Baseline Data"].items():
    print(save_name)
    print(url)