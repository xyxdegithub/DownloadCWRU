'''
Author: xyx
Date: 2022-04-06 16:23:55
LastEditTime: 2022-04-06 20:49:19
'''
# -*- coding = utf-8 -*-
# @Time : 2022/4/6 13:47
# @Author : xyx
# @File : downloadCWRU.py
from pathlib import Path

import CWRU_URL
import requests
from tqdm.auto import tqdm
import os

#下载数据的方法
def download(url: str, save_dir: str, save_name: str, suffix=None):
    if save_name == None:
        fileName = url.split("/")[-1]
    else:
        #下载的数据文件的名称
        fileName = save_name + suffix
    #filePath是在设置下载的数据放在那个文件夹下    
    filePath = save_dir + fileName
    if filePath:
        print(f"正在下载{filePath}")
        with open(filePath, "wb") as f:
            response = requests.get(url, stream=True)
            total = int(response.headers.get('content-length'))
            with tqdm(total=total, unit='B', unit_scale=True,
                      desc=fileName) as pbar:
                for data in response.iter_content(chunk_size=1024 * 1024):
                    f.write(data)
                    pbar.update(1024 * 1024)
    else:
        return filePath
    return filePath


if __name__ == "__main__":
    category1 = "1.Normal Baseline Data"
    category2 = "2.12k Drive End Bearing Fault Data"
    category3 = "3.48k Drive End Bearking Fault Data"
    category4 = "4.12k Fan End Bearing Fault Data"

    category = [category1, category2, category3, category4]
    #使用循环遍历把四种数据依次下载
    for i in category:
        path = f"./CWRU/{i}/"

        if not os.path.exists(path):
            os.makedirs(path)

        save_dir = path

        for save_name, url in CWRU_URL.URLS[i].items():
            download(url, save_dir, save_name, suffix=".mat")
    print("CWRU轴承数据集全部文件下载完成")
