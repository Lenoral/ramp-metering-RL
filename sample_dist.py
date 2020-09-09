# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 10:04:13 2020

@author: Mr.Du
"""

import pandas as pd
import random
e = pd.read_csv(r'C:\Users\Mr.Du\Desktop\30jours\RLDemo\0720\origin.csv')
e = e.iloc[:100000,:]
indexs = e.shape[0]
j = indexs
for i in range(indexs):
    try:
        s1 = e.loc[i,"occupancy812"]
        s2 = e.loc[i,"rampflow"]
        s3 = e.loc[i,"queue_ratio"]
        a = e.loc[i,"redtime"]
        e_sub = e.loc[(e["occupancy812"] >= s1-0.5) & (e["occupancy812"] <= s1+0.5) 
                      & (e["rampflow"] >= s2-2) & (e["rampflow"] >= s2-2)
                      & (e["queue_ratio"] >= s3-0.05) & (e["queue_ratio"] <= s3+0.05), :]
                      #& (e["redtime"] >= a-0.5) & (e["redtime"] <= a+0.5) ,:]
        index_sub = e_sub.index
        if e_sub.shape[0] > 200:
            kd = e_sub.shape[0] - 200
            drop_idx = random.choices(index_sub, k=kd)
            e.drop(drop_idx, axis =0,inplace=True,errors='ignore')
            print(f'{kd} samples droped for {s1}, {s2}, {s3} neighbor')
        elif e_sub.shape[0] < 200:
            kd = 200 - e_sub.shape[0]
            add_idx = random.choices(index_sub, k=kd)
            for idx in add_idx:
                row = e.loc[idx,:]
                row.name = j
                e = e.append(row)
                j+=1
            print(f'{kd} samples added for {s1}, {s2}, {s3} neighbor')
    except KeyError:
        print('Already droped!')