# -*- coding: utf-8 -*-
"""
Created on Thu May 14 16:42:35 2020

@author: Mr.Du
"""
import random
import xml.etree.ElementTree
import os

def random_flow():
    # 设置流量范围
    index_m = 0
    index_r = 0
    mflow_range = range(1600, 2000, 25)
    rflow_range = range(250, 800, 25)
    # 随机取出15个（可重复）
    mflow = random.choices(mflow_range, k=15)
    rflow = random.choices(rflow_range, k=15)
    tree = xml.etree.ElementTree.parse('random_routes.xml')
    root = tree.getroot()
    for elem in root.iter(tag='routes'):
        for flow in elem.iter(tag='flow'):
            if 'm' in flow.get('id'):
                flow.attrib['number'] = str(mflow[index_m])
                index_m+=1
            if 'r' in flow.get('id'):
                flow.attrib['number'] = str(rflow[index_r])
                index_r+=1
    tree.write('random_routes.xml')
    return mflow, rflow