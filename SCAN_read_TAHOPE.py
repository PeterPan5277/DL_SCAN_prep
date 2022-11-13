# -*- coding: utf-8 -*-
"""
Created on Fri May  6 13:01:23 2022
@author: peteprpan
"""
'''
Rawdata is 2013-2021
My target is to automatically read the all files and intend to localize the 
cell position on the 120*120 map.
Output will be the 0 and 1 in 120*120 map which indicates whether cell existed in last 10 minutes .
'''
from os import listdir
from datetime import datetime, timedelta
import pickle
import os
from tqdm import tqdm
import numpy as np
def major(Root_dir, des_dir): 
    skip_files = 0
    year  = sorted(listdir(Root_dir))
    year_length = len(year)
    for y in tqdm(range(year_length)):       
        month = sorted(listdir(Root_dir+year[y]))
        month_length = len(month)
        for m in range(month_length):
            day   = sorted(listdir(Root_dir+year[y]+'/'+month[m]))
            day_length = len(day)
            for d in range(day_length):
            #files = [files for files in listdir(Root_dir+'2015/05/20150501/'+sites[0]+'StormCellInfo/')]
            #需要做一個大迴圈run整筆資料一次          
            #要做一個判斷式先判斷某年某月某日底下是否有資料，若無則跳下一筆，有才要存
                Full_dir = Root_dir+year[y]+'/'+month[m]+'/'+day[d]+'/'
                if bool(listdir(Full_dir)) == True :
                    site_numbers = len(listdir(Full_dir))
                    sites = listdir(Full_dir)
                    for s in range(site_numbers):
                        #要在一個判斷是判斷是否有/stormcellinfo/
                        stormcellinfo_inornot = listdir(Full_dir+sites[s])
                        #如果沒有就直接跳過
                        if 'StormCellInfo' in stormcellinfo_inornot :
                            files = sorted([files for files in listdir(Full_dir+sites[s]+'/StormCellInfo/')])
                            for i in range(len(files)) :
                                if len(files[i]) == 13:
                                    #make sure is YYYYMMMMM_HHmm
                                    file_path = Full_dir+sites[s]+'/StormCellInfo/'+files[i]
                                    #print(file_path)
                                    with open(file_path, encoding="unicode_escape") as scan_file :
                                        for lines in scan_file.readlines():
                                            factors = lines.split()
                                            if (len(factors))  == 39: #有39項
                                                elementidx = {} #39項目所有
                                                parameters = {} #存重點
                                                for idx, element in enumerate(factors, start= 1):      
                                                    idx = str(idx)
                                                    elementidx[idx] = element      
                                                parameters = {
                                                'Site' : factors[1],
                                                'ident' : factors[2],
                                                'lon' : factors[28],
                                                'lat' : factors[27],
                                                'mdbz' : factors[12],
                                                'storm_top' : factors[14]
                                                }
                                        #把位置點出來後做成120*120(其中裡面是只有0跟1)之後輸出到pickle
                                                lon = parameters['lon']
                                                lat = parameters['lat']                                                                 
                                                path_pkl = create_directory(file_path, des_dir)
                                                cell_localize_thendump(lon, lat, path_pkl)
                else:
                    skip_files += 1
                    print('There are no cells in :',Full_dir)
                    pass
                    #跳至下一筆資料
    return(skip_files)
def create_directory(file_path, des_dir):
    #利用timedelta+10min即可
    Root_pick = des_dir
    path_idx = file_path.split('/')
    path_idx_together = path_idx[2]+'/'+path_idx[3]+'/'+path_idx[4]+'/'
    year  = int(path_idx[-1][0:4])
    month = int(path_idx[-1][4:6]) 
    day   = int(path_idx[-1][6:8])
    hh    = int(path_idx[-1][-4:-2])
    mm    = (int(path_idx[-1][-2:])-1)
    if mm == -1 : #處理最後分為00情況
        mm = int(0)
        today = datetime(year , month, day, hh, mm)  
        pathend = today.strftime('%Y/%m/%Y%m%d/%H%M')  
        path_pkl = Root_pick+pathend
        return(path_pkl)
    else :
        mm = str("%02d" %mm)       
        mm = int(mm[0]+'0')
        today = datetime(year , month, day, hh, mm)  
        next_10min = (today + timedelta(minutes = 10))
        pathend = next_10min.strftime('%Y/%m/%Y%m%d/%H%M')  
        path_pkl = Root_pick+pathend 
        return(path_pkl)    
def cell_localize_thendump(lon, lat, path_pkl) :   
    lon= float(lon)
    lat= float(lat)      
    lat_grid = 120  #24.0675-25.56595 
    lon_grid = 120  #120.68-122.17
    lat_per_grid = (25.56595-24.0675)/lat_grid
    lon_per_grid = (122.17-120.68)/lon_grid
    #若檔案不存在 可以重新創np.zeros，再點上cell position
    #print(path_pkl)
    if os.path.isdir(path_pkl) == False :     
        #Cell_loc_output = np.zeros((lat_grid, lon_grid), dtype=np.int) 
        if (lon) <= 120.68 or (lon) >=122.17 or (lat) >= 25.56595 or (lat) <= 24.0675:
            pass
        else:
            move_grid_lon = int( (lon - 120.68) / lon_per_grid )
            move_grid_lat = int( (lat - 24.0675)  / lat_per_grid )
            #Cell_loc_output[move_grid_lat,move_grid_lon] = 1
            # return(Cell_loc_output)
            os.makedirs(path_pkl)
            hhmm = path_pkl[-4:]
            path_in = os.path.join(path_pkl,f'{hhmm}.pkl')         
            lon_list = []
            lat_list = []
            grid_x_list = []
            grid_y_list = []        
            grid_x_list.append(move_grid_lon)
            grid_y_list.append(move_grid_lat)
            lon_list.append(lon)
            lat_list.append(lat)
            data= {'grid_x':grid_x_list,
                   'grid_y':grid_y_list,
                   'lon' :lon_list,
                   'lat' :lat_list
                }          
            with open(path_in, 'wb') as f:
                pickle.dump(data , f)
     #如果檔案已存在，先讀取原檔之後再點一個新的上去dump
    else:
        hhmm = path_pkl[-4:]
        path_in = os.path.join(path_pkl,f'{hhmm}.pkl')
        with open(path_in, 'rb') as f:
            opt = pickle.load(f)
            grid_x_list = opt["grid_x"]
            grid_y_list = opt["grid_y"] 
            lon_list = opt["lon"]
            lat_list = opt["lat"]       
            if (lon) <= 120.68 or (lon) >=122.17 or (lat) >= 25.56595 or (lat) <= 24.0675:
                pass
            else:
                move_grid_lon = int( (lon - 120.68) / lon_per_grid )
                move_grid_lat = int( (lat - 24.0675) / lat_per_grid )               
                hhmm = path_pkl[-4:]
                path_in = os.path.join(path_pkl,f'{hhmm}.pkl')             
                grid_x_list.append(move_grid_lon)
                grid_y_list.append(move_grid_lat)
                lon_list.append(lon)
                lat_list.append(lat)                
                data= {'grid_x':grid_x_list,
                       'grid_y':grid_y_list,
                       'lon' :lon_list,
                       'lat' :lat_list
                }          
                with open(path_in, 'wb') as f:
                    pickle.dump(data , f)
                    
if __name__ == '__main__' :  
    Root_dir = '/bk2/peterpan/SCAN_rawData/Data/'
    des_dir  = '/bk2/peterpan/SCAN_processed/TAHOPE_ONLYgrid_renew/'
    s_t = datetime(2013,1,1,0,0)
    e_t = datetime(2021,12,31,23,50)
    
    major(Root_dir, des_dir)
    
   