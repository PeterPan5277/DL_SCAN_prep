# -*- coding: utf-8 -*-
"""
Created on Thu May 19 14:58:32 2022

@author: peteprpan
"""

'''
讀取已經處理好的scan_processed 然後把他以動畫呈現出來
'''
import conda
import os


conda_file_dir = conda.__file__
conda_dir = conda_file_dir.split('lib')[0]
proj_lib = os.path.join(os.path.join(conda_dir, 'share'), 'proj')
os.environ["PROJ_LIB"] = proj_lib


from os import listdir
from datetime import datetime, timedelta
import pickle
from tqdm import tqdm
import numpy as np
import cv2

import matplotlib.pyplot as plt
import mpl_toolkits
from mpl_toolkits.basemap import Basemap
import matplotlib as mpl



class Create_video():  
    def __init__(self, des_dir, start_t, end_t, plot_save_dir):

        self.des_path = des_dir
        self.s_t = start_t
        self.e_t = end_t
        self.plotdir = plot_save_dir
        
    def load_data_from_processed(self):

        cur_t = self.s_t
        cur_t = datetime(2021,6,4,4,0)
        end_t = datetime(2021,6,4,6,0)
        
        
        #cur_t=datetime(2015,2,15,7,30)
        #end_t=datetime(2015,2,15,7,30)
        
        while cur_t <= end_t:
           
            
            
            path_end = cur_t.strftime('%Y/%m/%Y%m%d/%H%M')
            
            
                 
            data = {'year'  : int(path_end[:4]),
                    'month' : int(path_end[5:7]),
                    'day'   : int(path_end[-7:-5]),
                    'hh'    : int(path_end[-4:-2]),
                    'mm'    : int(path_end[-2:])
                }
          
            
            today = datetime(data['year'],
                             data['month'],
                             data['day'],
                             data['hh'],
                             data['mm'])     
            
            path = self.des_path+path_end
            hhmm = path_end[-4:]            
            path_in = os.path.join(path,f'{hhmm}.pkl')
               
            if os.path.isdir(path) == True :
                
           
                print(path_in)
                
                with open(path_in, 'rb') as f :
         
                    opt=pickle.load(f)
    
                    lon = opt['lon']
                    lat = opt['lat']
                    print(len(lon))

                     
                    
                
                
                
                plotpath = (self.plotdir+(path_end[:4])+'/'+(path_end[5:7])+
                            '/'+(path_end[-7:-5])+'/')
                         
                             
                if os.path.isdir(plotpath) == False :
                    os.makedirs(plotpath)
                
                
                self.create_figure_first(lon,lat)
                
                plt.title((path_end[-13:])+'Z', fontsize=8)   
                plt.savefig(plotpath+
                        f'{hhmm}'+'.png', dpi=300)
                plt.close()
                
                    
                    
                
                cur_t = cur_t + timedelta(minutes=10)
                
              
                
            else: #若沒有東西就直接做一個空矩陣
                data_matrix = (np.zeros((561, 441), dtype=np.int))
            
                cur_t = cur_t + timedelta(minutes=10)
                
            
                
    def create_figure_first(self, lon, lat):
        #basic setting
        plt.figure(figsize=(7,5))
        
        m = Basemap(projection='cyl', llcrnrlat=24.0675, urcrnrlat=25.56595,\
             llcrnrlon=120.68, urcrnrlon=122.17, resolution='l', lat_ts=20)
            
            
        m.fillcontinents()
        m.drawparallels(np.arange(20,27,1),labels=[1,1,0,1], fontsize=8)
        m.drawmeridians(np.arange(118,124,1),labels=[1,1,0,1], rotation=45, fontsize=8)
        
        m.drawcoastlines()
        m.drawmapboundary()
        
        
        x, y = m(lon, lat)
        m.scatter(x, y, color='r', marker='+', zorder = 2)
        
        plt.xlabel('Longitude', labelpad=30)
        plt.ylabel('Latitude', labelpad=30)
        
   
    def create_video(self):
        pass
  
     


if __name__ == '__main__' :
    
    des_dir  = '/bk2/peterpan/SCAN_processed/TAHOPE_ONLYgrid_renew/'
    plot_save_dir = '/wk171/peterpan/SCAN/SCAN_eval/TAHOPE/'
    s_t = datetime(2021,6,16,4,0)
    e_t = datetime(2021,6,16,6,0)
    
    vid = Create_video(des_dir, s_t, e_t, plot_save_dir)
    vid.load_data_from_processed()
    #vid.create_video()
    
    
    
    
    