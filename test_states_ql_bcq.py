# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 16:02:52 2020

@author: Mr.Du
"""

from BCQ_simulation import BCQchoose_action
import pandas as pd
import numpy as np
from ql import Discretization_mainlineflow, Discretization_occupancy, Discretization_rampflow, Discretization_qratio

def qlchoose_action(q_table, state):
    s = [str(int(i)) for i in state]
    state = [Discretization_occupancy(state[0]), Discretization_rampflow(state[1]),  Discretization_qratio(state[2]) ]
    s = [str(int(i)) for i in state]
    s = ' '.join(s)
    default_action = [0, 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
    if str(s) in q_table.index:
        state_action = q_table.loc[s, :]
        action = np.random.choice(state_action[state_action == np.max(state_action)].index)
    else:
        print('State {} is not visited in training!'.format(s))
        #action = np.random.choice(default_action)
        action=-1
        with open('qlerror.txt', 'a') as file_object:
            file_object.write('State {} is not visited in training!\n'.format(s))
    return int(action)

state_dim = 3
action_dim = 1
data = pd.read_csv(r'C:\Users\Mr.Du\Desktop\30jours\RLDemo\0720\resample.csv')
states = np.array(data.iloc[:,:state_dim])
action = np.array(data.iloc[:,state_dim])

COUNT = 0
qred = []
bcqred = []
qtable = pd.read_csv(r'C:\Users\Mr.Du\Desktop\30jours\RLDemo\0720\2qtable_10w_revisit.csv')
qtable.set_index(['Unnamed: 0'], inplace=True)
for i in range(10000):
    state = states[i]
    qred.append(qlchoose_action(qtable, state))
    bcqred.append(BCQchoose_action(policy, state))

import matplotlib.pyplot as plt
fig,(ax0,ax1) = plt.subplots(nrows=2,figsize=(9,6))
x = np.arange(1000)
ax0.plot(x, np.array(qred)[:1000]+2)
ax0.set_title('QL')
ax1.plot(x, np.array(bcqred)[:1000])
ax1.set_title('BCQ')