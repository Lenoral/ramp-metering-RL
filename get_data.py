# -*- coding: utf-8 -*-
"""
Created on Thu May 14 17:34:17 2020

@author: Mr.Du
"""

from ALINEA import coor
from generate_random_flow import random_flow
from organize_RLdata import read_detectorout
import json
import os 

flag = 12
queue = []
redtime = []
Carnum = []
Carnum_ramp = []
mainline_set_flow = []
ramp_set_flow = []
detector_list = ['812 SB', '813 SB', 'A']
warmup = 600
speed_detector = {'813 SB': [], '812 SB': []}
occupancy_detector = {'813 SB': [], '812 SB': []}
flow_detector = {'813 SB': [], '812 SB': [], 'A': []}

for run in range(20):
    m, r = random_flow()
    mainline_set_flow.extend(m)
    ramp_set_flow.extend(r)
    for i in range(5):
        os.system(r"duarouter -n C:\Users\Mr.Du\Desktop\RLDemo\Anet.net.xml -r C:\Users\Mr.Du\Desktop\RLDemo\random_routes.xml --randomize-flows --random -o C:\Users\Mr.Du\Desktop\RLDemo\myrandomroutes.rou.xml")
        # 运行
        q, r, c, cr = coor(i, 18)
        # 存储数据
        queue.append(q)
        redtime.append(r)
        Carnum.append(c)
        Carnum_ramp.append(cr)
        #获取输出文件中的检测器数据
        s, o, f = read_detectorout(detector_list, str(i+18)+'out.xml', warmup)
        for d in detector_list:
            if d != 'A':
                speed_detector[d].extend(s[d])
                occupancy_detector[d].extend(o[d])
            flow_detector[d].extend(f[d])
car = []
rcar = []
for i in range(len(Carnum)):
    car.extend([float(x) for x in Carnum[i]])
    rcar.extend([float(x) for x in Carnum_ramp[i]])
    
with open('carnum'+str(flag)+'.json','w',encoding='utf-8') as f:
    json.dump(car,f,ensure_ascii=False)
with open('carnumr'+str(flag)+'.json','w',encoding='utf-8') as f:
    json.dump(rcar,f,ensure_ascii=False)
with open('queue'+str(flag)+'.json','w',encoding='utf-8') as f:
    json.dump(queue,f,ensure_ascii=False)
with open('redtime'+str(flag)+'.json','w',encoding='utf-8') as f:
    json.dump(redtime,f,ensure_ascii=False)
with open('speed_detector'+str(flag)+'.json','w',encoding='utf-8') as f:
    json.dump(speed_detector,f,ensure_ascii=False)
with open('occupancy_detector'+str(flag)+'.json','w',encoding='utf-8') as f:
    json.dump(occupancy_detector,f,ensure_ascii=False)
with open('flow_detector'+str(flag)+'.json','w',encoding='utf-8') as f:
    json.dump(flow_detector,f,ensure_ascii=False)
with open('mainline_set_flow'+str(flag)+'.json','w',encoding='utf-8') as f:
    json.dump(mainline_set_flow,f,ensure_ascii=False)
with open('ramp_set_flow'+str(flag)+'.json','w',encoding='utf-8') as f:
    json.dump(ramp_set_flow,f,ensure_ascii=False)