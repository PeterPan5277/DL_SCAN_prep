# -*- coding: utf-8 -*-
"""
Created on Sun May 22 19:44:32 2022

@author: peteprpan
For the purpose of finding how many data are in the TAHOPE region, and this 
is to make our training process more convincible.
"""




from os import listdir
from datetime import datetime, timedelta
import pickle
import os
from tqdm import tqdm
import numpy as np


#This method is for checking whether the points are in the region or not,
#and then we try to save this to another directory called SCAN_processed_TAHOPE

def check_TAHOPE_region(s_t, e_t, des_dir):
    times = 0
    pocket =[]
    
    while s_t <= e_t:
        path_end = s_t.strftime('%Y/%m/%Y%m%d/%H%M')
        #print(path_end)
        path_pkl = des_dir+path_end
        intheTAHOPE = 0

    
       
        
        if os.path.isdir(path_pkl) == True :
            
            hhmm = path_pkl[-4:]
            path_in = os.path.join(path_pkl,f'{hhmm}.pkl')
            #print(path_in)
            
            with open(path_in, 'rb') as f:
                opt = pickle.load(f)
                #opt = 'grid' 'lon' 'lat'
                lon = opt['lon']
                lat = opt['lat']
                pairs = [(lon[i],lat[i]) for i in range (len(lon))]
                #for i in range(len(lon)):
                    #for j in range(len(lat)):
                for p in pairs:               
                    if (p[0]>=120.68) and (p[0]<=122.17) and (p[1]>=24.0675) and (p[1]<=25.56595):
                        intheTAHOPE = 1
                        times+=1
                        
                        
                if intheTAHOPE == 1:        
                    pocket.append(True)
                else:
                    pocket.append(False)
        
        s_t = s_t + timedelta(minutes=10)
        
        
    return(times, pocket)
        
        

def create_TAHOPEdir(s_t, e_t, des_dir, Root_TAHOPE):
    notinTAHOPE =0
    winter = 0
    MayJune = 0
    summer = 0


    while s_t <= e_t:

        path_end = s_t.strftime('%Y/%m/%Y%m%d/%H%M')
        
        path_pkl = des_dir+path_end
        intheTAHOPE = 0

        #print(path_pkl)
      
         

        if os.path.isdir(path_pkl) == True :
        
            hhmm = path_pkl[-4:]
            path_in = os.path.join(path_pkl,f'{hhmm}.pkl')
            print(path_in)
            
            with open(path_in, 'rb') as f:
                opt = pickle.load(f)
                #opt = 'grid' 'lon' 'lat'
                lon = opt['lon']
                lat = opt['lat']
                pairs = [(lon[i],lat[i]) for i in range (len(lon))]
                #for i in range(len(lon)):
                    #for j in range(len(lat)):
                for p in pairs:   

                    if (p[0]>=120.68) and (p[0]<=122.17) and (p[1]>=24.0675) and (p[1]<=25.56595):
                        intheTAHOPE = 1
                        break

                if intheTAHOPE == 1:
                    #And we categorize them by season
                    print(path_end)
                    mm = int(path_end[-9:-7])
                    if mm==5 or mm==6:
                        MayJune+=1
                    elif mm>= 11 or mm<=4:
                        winter+=1

                    else:
                        summer+=1
                     
                    

                    path_TAHOPE = Root_TAHOPE+path_end
                    os.makedirs(path_TAHOPE)
                    path_final = os.path.join(path_TAHOPE,f'{hhmm}.pkl')
                    print(path_final)
                    
                    with open(path_final, 'wb') as f:

                        pickle.dump(opt , f)   


                else:
                    notinTAHOPE+=1
            

                    #print('No any points in TAHOPE date is:', path_end )

        category = {'winter':winter, 'summer':summer, 'MayJune':MayJune}
        s_t = s_t + timedelta(minutes=10)

    return(notinTAHOPE, category)
                        

def check_seasonal(s_t, e_t,Root_TAHOPE):
    winter = 0
    MayJune = 0
    summer = 0


    while s_t <= e_t:
        path_end = s_t.strftime('%Y/%m/%Y%m%d/%H%M')        
        path_pkl = Root_TAHOPE+path_end       
        if os.path.isdir(path_pkl) == True :

            mm = int(path_end[-9:-7])
            if mm==5 or mm==6:
                MayJune+=1
            elif mm>= 11 or mm<=4:
                winter+=1
            else:
                summer+=1
            s_t = s_t + timedelta(minutes=10)
        else:
            
            s_t = s_t + timedelta(minutes=10)

    print('winter:', winter)
    print('summer:', summer)
    print('MayJune:', MayJune)



    
if __name__ == '__main__' :
    
    des_dir  = '/bk2/peterpan/SCAN_processed/'
    s_t = datetime(2015,1,1,0,0)
    e_t = datetime(2021,12,31,23,50)
    Root_TAHOPE = '/bk2/peterpan/SCAN_processed/TAHOPE_ONLYgrid/'
    check_seasonal(s_t, e_t,Root_TAHOPE)

    #create TAHOPE directory
    # notinTAHOPE, category = create_TAHOPEdir(s_t, e_t, des_dir, Root_TAHOPE)
    # print('files_outTAHOPE', notinTAHOPE) #141624
    # print('winter', category['winter'])   #33210
    # print('summer', category['summer'])   #46096
    # print('Mayjune',category['MayJune'])  #24377 (for 2013-2021)
    
    
    
    
    #times計算在TAHOPE總共有幾個點
    #pocket裡面存著F and T, 如果此筆資料是有在TAHOPE就是TRUE

    #times, pocket = check_TAHOPE_region(s_t, e_t, des_dir)
    #numbers_of_files_inTAHOPE = len([i for i in pocket if i == True])
    #numbers_of_files_outTAHOPE = len(pocket)-numbers_of_files_inTAHOPE
    
    #print('in :' ,numbers_of_files_inTAHOPE) #103683
    #print('out:', numbers_of_files_outTAHOPE) #141624
    #print('How many dots in regions :', times) #有幾個點 707086


    