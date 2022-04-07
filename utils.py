'''
Author: xyx
Date: 2022-04-06 21:19:50
LastEditTime: 2022-04-07 21:37:50
'''
'''这个文件是处理数据'''

import glob
from pathlib import Path
from tqdm.auto import tqdm
import requests
import scipy.io
import sys
import time
import pandas as pd

#处理下载的.mat文件
#folderPath是含有.mat文件夹
def matfile_to_dic(folderPath):
    out_dic={}
    for filePath in glob.glob(f"{folderPath}\\*.mat"):
        #print(filePath)
        key_name=filePath.split("\\")[-1]
        #print(key_name)
        out_dic[key_name]=scipy.io.loadmat(filePath)
        #print(out_dic)
    return out_dic

#matfile_to_dic("CWRU\\1.Normal Baseline Data")

#去除一些不必要的数据
#遍历字典中的（键，值）对
def remove_dic_items(dic):
    for key,values in dic.items():
        del values["__header__"]
        del values["__version__"]
        del values["__globals__"]
        # print(key,values)
    

#dic=matfile_to_dic("CWRU\\1.Normal Baseline Data")
# dic=matfile_to_dic("CWRU\\2.12k Drive End Bearing Fault Data")
# remove_dic_items(dic)

def rename_keys(dic):
    '''X236_DE_time X236_FE_time X236_BA_time X236RPM 这样的key2重新命名'''
    for key1,values1 in dic.items():
        # print(key1)
        # print(values1)
        for key2,values2 in list(values1.items()):
            # print(key2)
            # print(values2)
            if 'DE_time' in key2:
                #key2从values1中弹出，删除
                values1['DE_time'] = values1.pop(key2)
            elif 'BA_time' in key2:
                values1['BA_time'] = values1.pop(key2)
            elif 'FE_time' in key2:
                values1['FE_time'] = values1.pop(key2)
            elif 'RPM' in key2:
                values1['RPM'] = values1.pop(key2)
        # print(key1)
        # print(values1)


# dic=matfile_to_dic("CWRU\\2.12k Drive End Bearing Fault Data")
# rename_keys(dic)


#根据文件名对确定信号的标签
def label(file_name):
    if "B" in file_name:
        return "B"
    elif "IR" in file_name:
        return "IR"
    elif "OR" in file_name:
        return "OR"
    elif "Normal" in file_name:
        return "N"


def mat_to_df(folder_path):
    #先把.mat文件变成字典
    dic = matfile_to_dic(folder_path)
    #把字典内容进行一些处理
    remove_dic_items(dic)
    rename_keys(dic)
    #字典到dataframe
    df = pd.DataFrame.from_dict(dic).T
    #将新增的index列名变为filename
    df = df.reset_index().rename(mapper={'index':'filename'},axis=1)
    df['label'] = df['filename'].apply(label)
    return df.drop(['BA_time','FE_time', 'RPM', 'ans'], axis=1, errors='ignore')




 
