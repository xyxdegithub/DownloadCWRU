'''
Author: xyx
Date: 2022-04-06 21:19:50
LastEditTime: 2022-04-06 22:16:19
'''


import glob
from pathlib import Path
from tqdm.auto import tqdm
import requests
import scipy.io

#处理下载的.mat文件
#folderPath是含有.mat文件夹
def matfile_to_dic(folderPath):
    out={}
    for filePath in glob.glob(f"{folderPath}\\*.mat"):
        #print(filePath)
        key_name=filePath.split("\\")[-1]
        #print(key_name)
        out[key_name]=scipy.io.loadmat(filePath)
        print(out)


matfile_to_dic("CWRU\\1.Normal Baseline Data")