# -*- coding: utf-8 -*-
"""
Created on Tue May 19 17:31:43 2020

@author: Mr.Du
"""
import os
import sys

if 'SUMO_HOME' in os.environ:
     tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
     sys.path.append(tools)
else:
     sys.exit("please declare environment variable 'SUMO_HOME'")
     
import traci 
import numpy as np
from functools import reduce
import random


def BCQchoose_action(policy, state):
    action = policy.select_action(state)
    #print(action[0])
    return action[0]+10


def BCQ_control(flag, policy):
    #信号灯ID
    tlsID = {'A': '30885212', 'B': '5535842383', 'D': '1877642863'}#信号灯ID
    Num = {'A': 4, 'B': 2, 'D': 2}#车道数
    mNum = {'A': 4, 'B': 3, 'D': 3}#主线车道数
    interval = 20 #每20秒更新计算1次
    Ramp = ['A']#作为共同的索引
    space = {'A': 110, 'B': 140, 'D': 65}

    #匝道下游主路检测器，用于获取占有率，流量
    detector_down = {'A': ["812 SB_0", "812 SB_1", "812 SB_2", "812 SB_3", "812 SB_4"], 'B': ["820AN SB_0", "820AN SB_1", "820AN SB_2"], 'D': ['208-SB_0', "208-SB_1", "208-SB_2"]}
    #匝道上游主路检测器，用于获取占有率，流量
    detector_up = {'A': ["813 SB_0", "813 SB_1", "813 SB_2"]}
    edgeRamp = {'A': ['On3', '-160415#0'], 'B': ['-160330', '577463705'], 'D': ['On1', '577723261']}
    vehicles = {}#主线各检测器20s经过的车辆ID
    vehicles0 = {}
    nrdetector = {}#匝道各检测器20s经过的车辆ID
    nrdetector0 = {}
    occupied_duration = {}

    for key in Ramp:
        for d in detector_down[key]:
            occupied_duration[d] = 0#为所有要用到的检测器创造储存数组
            vehicles[d] = []
            vehicles0[d] = []
        for d in detector_up[key]:
            occupied_duration[d] = 0#
            vehicles[d] = []
            vehicles0[d] = []
        for j in range(Num[key]):
            nrdetector[key+'_'+str(j+1)] = []
            nrdetector0[key+'_'+str(j+1)] = []
    Carnum_list=[]
    CarnumRamp_list =[]       
    q = {'A': [0], 'B': [0], 'D': [0]}#
    qt = {'A': 0, 'B': 0, 'D': 0}#
    redtime = {'A': [12], 'B': [12], 'D': [12]}#记录当前计算所得红灯时长
    p = {'A': [], 'B': [], 'D': []}#存储信号灯相位

    # 开始仿真
    traci.start(['sumo-gui', "-c", "BH4eval.sumocfg", "--output-prefix", str(flag)])
    # 道路所有路段id，其实可以通过traci获取
    edgeIDs = ['-160415#0', '-160415#1', '443921506', '444071852', '444071857.6', '444071865', '578076505', '578076510', '583369725', '583369727#1', ':1837357028_0', ':1837537313_0', ':30885211_0', ':30885212_0', ':5540085417_0', ':5540085534_0', ':5576783866_0', ':cluster_1837537309_gneJ1_0', ':cluster_5780610093_gneJ0_gneJ1_0', ':cluster_5780610093_gneJ0_gneJ1_2', ':cluster_gneJ11_gneJ12_0', 'M2.4', 'On3']
    # 开始单步循环仿真
    for step in range(0,18600): #仿真时长
        # 每一秒记录所有在路网的车辆数
        carnum = np.sum([traci.edge.getLastStepVehicleNumber(x) for x in edgeIDs])
        Carnum_list.append(carnum)
        # 每一秒记录在匝道的车辆数
        CarnumRamp_list.append(traci.edge.getLastStepVehicleNumber(edgeRamp['A'][0]) + traci.edge.getLastStepVehicleNumber(edgeRamp['A'][1]))
        if step!=0 and step%interval == 0: #第一步是不调节的              
            for ramp in Ramp:
                flowr = reduce(lambda x, y: x+y, [len(set([vid for vid in nrdetector[d] if vid not in nrdetector0[d]])) for d in nrdetector.keys() if ramp in d ])
                flow_up = reduce(lambda x, y: x+y, [len(set([vid for vid in vehicles[d] if vid not in vehicles0[d]])) for d in vehicles.keys() if d in detector_up[ramp] ])
                flow_down = reduce(lambda x, y: x+y, [len(set([vid for vid in vehicles[d] if vid not in vehicles0[d]])) for d in vehicles.keys() if d in detector_down[ramp] ])
                o_up = np.mean(reduce(lambda x, y: x+y, [occupied_duration[d] for d in detector_up[ramp]])) /mNum[ramp]/interval*100
                o_down = np.mean(reduce(lambda x, y: x+y, [occupied_duration[d] for d in detector_down[ramp]])) /mNum[ramp]/interval*100
                q[ramp].append(qt[ramp])                
                state = np.array([ o_down, flowr, qt[ramp]/space[ramp]])
                qt[ramp] = 0
                redtime1 = BCQchoose_action(policy, state)
                redtime[ramp].append(redtime1)
                #print(redtime1)
            for d in nrdetector.keys():
                nrdetector0[d] = nrdetector[d]
                nrdetector[d] = []#每20s清空一次通过车辆ID
            for d in vehicles.keys():
                vehicles0[d] = vehicles[d]
                vehicles[d] = []#每20s清空一次通过车辆ID
            for d in occupied_duration.keys():
                occupied_duration[d] = 0
        traci.simulationStep()
        for d in occupied_duration.keys():
            v_info = traci.inductionloop.getVehicleData(d)
            for car in v_info:
                if car[3] != -1.0:
                    occupied_duration[d] += car[3]-car[2]
            vehicles[d] += traci.inductionloop.getLastStepVehicleIDs(d)
        for ramp in Ramp:
            # 每一秒数一下匝道上的车，并取最大值
            qt[ramp] = max(qt[ramp], (traci.edge.getLastStepVehicleNumber(edgeRamp[ramp][0]) + traci.edge.getLastStepVehicleNumber(edgeRamp[ramp][1])))
            p[ramp].append(traci.trafficlight.getPhase(tlsID[ramp]))#记录信号灯相位
        for d in nrdetector.keys():
            nrdetector[d] += traci.inductionloop.getLastStepVehicleIDs(d)
            
        #第一步的时候不能进行以下计算
        if step > 15:#第一个周期无调节
            for ramp in Ramp:
                if p[ramp][step] == 1 and p[ramp][step-1] == 0: 
                    traci.trafficlight.setPhaseDuration(tlsID[ramp], redtime[ramp][-1]-1)
        if step > 5400: 
            vehicles3 = traci.edge.getLastStepVehicleIDs('444071865')
 
            for v in vehicles3:
                tau3 = max(random.normalvariate(1.3, 0.2), 0)
                traci.vehicle.setTau(v, tau3)    
    traci.close()
    return q['A'], redtime['A'], Carnum_list, CarnumRamp_list
    #return o_test, redtime
    
