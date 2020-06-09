# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 13:47:04 2020

@author: Rohini
"""

import numpy as np
import matplotlib.pyplot as plt

reference_set_streamflow = np.loadtxt('ComoTest_perfect.reference')
reference_set_precip=np.loadtxt('ComoTest_precip.reference')
reference_set_SST=np.loadtxt('ComoTestDVs_SST.reference')

x = reference_set_streamflow[:,0]
y = reference_set_streamflow[:,1]

plt.scatter(x, y,alpha=0.5,color='red',label='streamflow')


x = reference_set_precip[:,0]
y = reference_set_precip[:,1]

plt.scatter(x, y,alpha=0.5,color='blue',label='precipitation')

x = reference_set_SST[:,0]
y = reference_set_SST[:,1]

plt.scatter(x, y,alpha=0.5,color='green',label='SST')

plt.xlabel(xlabel='Flood Control [days/year]', fontsize=14)
plt.ylabel(ylabel='Water Supply Deficit[($m^3$/s)$^2$', fontsize=14)
plt.ylim(2200,3200)
plt.xlim(5,15)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.legend(loc="upper right")


plt.show()