# -*- coding: utf-8 -*-
"""
Created on Thu May 28 22:07:14 2020

@author: Mr.Du
"""
import os
import sys
import random

if 'SUMO_HOME' in os.environ:
     tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
     sys.path.append(tools)
else:
     sys.exit("please declare environment variable 'SUMO_HOME'")
     
import traci 

def non_control(flag):
    edgeRamp =  ['On3', '-160415#0']
    q = []
    traci.start(['sumo-gui', "-c", "BH4non.sumocfg", "--output-prefix", str(flag)])
    for step in range(0,3600): #仿真时长
        traci.simulationStep()
        qt = 0
        vehicles_on_ramp = traci.edge.getLastStepVehicleIDs(edgeRamp[0]) + traci.edge.getLastStepVehicleIDs(edgeRamp[1])
        for v in vehicles_on_ramp:
            if traci.vehicle.getSpeed(v)<5:
                qt += 1
        q.append(qt)
            
    traci.close()
    return q