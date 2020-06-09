#This script plots the average daily lake level, forecast, and release for a specified policy

import matplotlib.pyplot as plt
import numpy as np


policy_data = np.loadtxt('./SST/compromise/Sol5_Average.txt')

fig = plt.figure()
ax = plt.axes()
ax.plot(policy_data[:,0],policy_data[:,1]);
ax.set_xticks([15,45,75,106,137,167,198,229,259,289,319,350])
ax.tick_params(axis='both', which='major', labelsize=14)
ax.set_xticklabels(['J','F','M','A','M','J','J','A','S','O','N','D'],fontsize=14)
ax.set_xlabel(xlabel='Month', fontsize=14)
ax.set_ylabel(ylabel='Lake Level [m]', fontsize=14)


fig = plt.figure()
ax = plt.axes()
ax.plot(policy_data[:,0],policy_data[:,2],color='green');
ax.set_xticks([15,45,75,106,137,167,198,229,259,289,319,350])
ax.tick_params(axis='both', which='major', labelsize=14)
ax.set_xticklabels(['J','F','M','A','M','J','J','A','S','O','N','D'],fontsize=14)
ax.set_xlabel(xlabel='Month', fontsize=14)
ax.set_ylabel(ylabel='SST Forecast', fontsize=14)


fig = plt.figure()
ax = plt.axes()
ax.plot(policy_data[:,0],policy_data[:,3],color='red');
ax.set_xticks([15,45,75,106,137,167,198,229,259,289,319,350])
ax.tick_params(axis='both', which='major', labelsize=14)
ax.set_xticklabels(['J','F','M','A','M','J','J','A','S','O','N','D'],fontsize=14)
ax.set_xlabel(xlabel='Month', fontsize=14)
ax.set_ylabel(ylabel='Release ($m^3$/s)', fontsize=14)
