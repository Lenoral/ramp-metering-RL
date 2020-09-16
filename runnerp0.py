# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 20:29:57 2020

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
from sumolib import checkBinary  # noqa
import optparse
import json
import random

def cal_redtime(rate, NumLanes):
    redtime = 3600*NumLanes/rate - 2 #绿灯时间定为2
    return round(redtime,1) #红灯时间保留一位小数即可

def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options

def runner(pid, t1, t2, t3, t4):
#def runner(pid):
    options = get_options()
    # this script has been called from the command line. It will start sumo as a
    # server, then connect and run
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')
    #假设是所需的，完整的数据
    #with open('C:\\Users\\Mr.Du\\Desktop\\BH_f\\0903\\megerate0903.json','r') as load_f:
    with open('C:\\Users\\Mr.Du\\Desktop\\help\\megerate0902.json','r') as load_f:
        megerate = json.load(load_f)
    redtime_A = 12
    redtime_B = 10
    redtime_D = 10
    #信号灯ID
    tlsID_A = '30885212'
    tlsID_B = '5535842383'
    tlsID_D = '1877642863'
    #车道数
    Num_A = 4
    Num_B = 2
    Num_D = 2
    j = 0 #处于第几个20秒
    p_A = []
    p_B = []
    p_D = []#存储信号灯相位
    # this is the normal way of using traci. sumo is started as a
    # subprocess and then the python script connects and runs
    traci.start(['sumo-gui', "-c", r"C:\Users\Mr.Du\Desktop\help\BH.sumocfg", "--output-prefix", str(pid)])
    #traci.start(['sumo', "-c", r"C:\Users\Mr.Du\Desktop\BH_f\0903\BH.sumocfg", "--output-prefix", str(pid)])
    for step in range(0,18600):
        '''if step%20 == 0:#0.1步长
            r_A = megerate['Anzac'][j]
            r_B = megerate['Boundary'][j]
            r_D = megerate['Deception'][j]#每20s重新计算一次merge rate；此时步长为1
            j = j+1
            redtime_A = max(min(cal_redtime(r_A, Num_A), redtime_A+10), redtime_A-5)
            redtime_B = max(min(cal_redtime(r_B, Num_B), redtime_B+10), redtime_B-5)
            redtime_D = max(min(cal_redtime(r_D, Num_D), redtime_D+10), redtime_D-5)'''
        traci.simulationStep()
        '''p_A.append(traci.trafficlight.getPhase(tlsID_A))
        p_B.append(traci.trafficlight.getPhase(tlsID_B))
        p_D.append(traci.trafficlight.getPhase(tlsID_D))
        #第一步的时候不能进行以下计算
        if step != 0:
            if p_A[step] == 2 and (p_A[step-1] == 0 or p_A[step-1] == 1): #进入红灯,但是只能是刚进入
                traci.trafficlight.setPhaseDuration(tlsID_A, redtime_A)#每个周期都设置一下红灯时长
            if p_B[step] == 2 and (p_B[step-1] == 0 or p_B[step-1] == 1): #进入红灯,但是只能是刚进入
                traci.trafficlight.setPhaseDuration(tlsID_B, redtime_B)#每个周期都设置一下红灯时长
            if p_D[step] == 2 and (p_D[step-1] == 0 or p_D[step-1] == 1): #进入红灯,但是只能是刚进入
                traci.trafficlight.setPhaseDuration(tlsID_D, redtime_D)'''#每个周期都设置一下红灯时长
        '''vehicles = traci.inductionloop.getLastStepVehicleIDs('815 SB_0')+traci.inductionloop.getLastStepVehicleIDs('815 SB_1')+traci.inductionloop.getLastStepVehicleIDs('815 SB_2')
        for v in vehicles:
            traci.vehicle.updateBestLanes(v)
        vehicles = traci.inductionloop.getLastStepVehicleIDs('814 SB_0')+traci.inductionloop.getLastStepVehicleIDs('814 SB_1')+traci.inductionloop.getLastStepVehicleIDs('814 SB_2')
        for v in vehicles:
            traci.vehicle.updateBestLanes(v)
        vehicles = traci.inductionloop.getLastStepVehicleIDs('813 SB_0')+traci.inductionloop.getLastStepVehicleIDs('813 SB_1')+traci.inductionloop.getLastStepVehicleIDs('813 SB_2')
        for v in vehicles:
            traci.vehicle.updateBestLanes(v)'''

        if step > 5400:
            vehicles1 = traci.edge.getLastStepVehicleIDs('444071858.7')
            '''vehicles12 = traci.edge.getLastStepVehicleIDs('577463657')
            vehicles13 = traci.edge.getLastStepVehicleIDs('444071852')
            vehicles14 = traci.edge.getLastStepVehicleIDs('583369727#1')'''
            vehicles2 = traci.edge.getLastStepVehicleIDs('444071862')#从该路段开始修改车辆属性
            vehicles3 = traci.edge.getLastStepVehicleIDs('444071865')
            vehicles4 = traci.edge.getLastStepVehicleIDs('M2.4')
            
            for v in vehicles1:
                sigma = max(min(random.normalvariate(0.2, 0.1),1),0)#生成随机sigma，在0,1之间
                tau1 = max(random.normalvariate(t1, 0.3), 0)
                traci.vehicle.setTau(v, tau1)
                traci.vehicle.setImperfection(v, sigma)
            '''for v in vehicles12:
                tau2 = max(random.normalvariate(1.35, 0.2), 0)
                traci.vehicle.setTau(v, tau2) 
            for v in vehicles13:
                tau2 = max(random.normalvariate(1.4, 0.2), 0)
                traci.vehicle.setTau(v, tau2)
            for v in vehicles14:
                tau2 = max(random.normalvariate(1.36, 0.2), 0)
                traci.vehicle.setTau(v, tau2)''' 
            for v in vehicles2:
                tau2 = max(random.normalvariate(t2, 0.3), 0)
                traci.vehicle.setTau(v, tau2)   
            for v in vehicles3:
                tau3 = max(random.normalvariate(t3, 0.3), 0)
                traci.vehicle.setTau(v, tau3)    
            for v in vehicles4:
                tau4 = max(random.normalvariate(t4, 0.3), 0)
                traci.vehicle.setTau(v, tau4) 
    traci.close()
    #return p_A, p_B, p_D
    return