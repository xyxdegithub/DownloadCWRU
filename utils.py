'''
Author: xyx
Date: 2022-04-06 21:19:50
LastEditTime: 2022-04-08 20:45:18
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
import numpy as np

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

'''这个函数将信号分成若干段，每段都有一个特定的数字由段长定义的点。'''
def divide_signal(df,length):
    dic={}
    index=0
    #df.shape[0]是df的行数
    for i in range(df.shape[0]):
        n_sample_points=len(df.iloc[i,1])
        n_segments=n_sample_points//length
        for segment in range(n_segments):
            dic[index]={
                'signal': df.iloc[i,1][length * segment:length * (segment+1)], 
                'label': df.iloc[i,2],
                'filename' : df.iloc[i,0]
            }
            index+=1
    df_tmp = pd.DataFrame.from_dict(dic,orient='index')
    #把两个df 水平concat一起
    df_output = pd.concat(
        [df_tmp[['label', 'filename']], 
         pd.DataFrame(np.hstack(df_tmp["signal"].values).T)
        ], 
        axis=1 )
    return df_output

def normalize_signal(df):
    #求平均值和方差
    mean = df['DE_time'].apply(np.mean)
    std = df['DE_time'].apply(np.std)
    #正则化
    df['DE_time'] = (df['DE_time'] - mean) / std
 

def get_df_all(data_path, segment_length=512, normalize=False):

    df = mat_to_df(data_path)

    if normalize:
        normalize_signal(df)
    df_processed = divide_signal(df, segment_length)

    map_label = {'N':0, 'B':1, 'IR':2, 'OR':3}
    #把标签替换成对应的数字
    df_processed['label'] = df_processed['label'].map(map_label)
    return df_processed
