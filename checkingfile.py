from os import listdir
from datetime import datetime, timedelta
import pickle
import os
from pyrsistent import l
from tqdm import tqdm
import numpy as np
# /bk2/handsomedong/DLRA_database/
with open('/bk2/peterpan/PKL_rain_radar/AllDataDict_20210601-0000_20210630-2350.pkl','rb') as f:
    data_dic = pickle.load(f)
    print(data_dic.keys())
    print(len(data_dic['rain']))

    #print(max(a[2]))
    #print(np.max(np.array(data_dic['radar'][datetime(2021, 6, 4, 4, 40)])))
    #print((np.array(data_dic['radar'][datetime(2021, 6, 4, 4, 40)])).shape)
    #print(data_dic['radar'][datetime(2021, 6,4, 0, 0)])
    #a= np.array((data_dic['scan']))
    #print(np.where(a!=None))


    #print(list(data_dic['rain'].keys())[1000])#dic
 
    #print(list(data_dic['rain'].values())[3])#dic
   #print(list(data_dic['rain'].values())[1000].shape)#dic
   # print(list(data_dic['radar'].values())[1000].shape)
    #print(list(data_dic['scan'].values()))
    #print(type(data_dic['rain']))#dic

    #print(len(data_dic['radar'].keys()))