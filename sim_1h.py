# -*- coding: utf-8 -*-
"""
Created on Sat Aug 22 11:02:12 2020

@author: Mr.Du
"""

import os
from nocontrol import non_control

path = r'C:\Users\Mr.Du\Desktop\anzac_recalibrate\sim_1h'
os.chdir(path)
for i in range(1):
    
    os.system(r"duarouter -n A_calib.net.xml -r random_routes_lctest.xml -o myrandomroutes.rou.xml")
    # 运行
    q2 = non_control(i)