import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
#from utils import getFormulations, getSolns, getSolns_u, getSolns_r

sns.set_style("dark")

# plotting features
inputs = ['lake level','forecast']
#reservoir = inputs[1] # HoaBinh
#colors = ['#fb9a99','#e31a1c','#33a02c','#6a3d9a','#1f78b4','#ff7f00']
colors = ['#e31a1c','#1f78b4','#ff7f00','#33a02c']
pSt = plt.Rectangle((0,0), 1, 1, fc=colors[0], edgecolor='none')
pFcst = plt.Rectangle((0,0), 1, 1, fc=colors[1], edgecolor='none')
pInteract = plt.Rectangle((0,0), 1, 1, fc=colors[2], edgecolor='none')
pNegInt = plt.Rectangle((0,0), 1, 1, fc=colors[3], edgecolor='none')

SI = np.loadtxt('C:/Users/Rohini/Box Sync/LakeComo/solution_perfect.txt',skiprows = 1,delimiter = ",")

def averageSensitivity(sens):
    input1 = sens[:,0]
    input2 = sens[:,1]
    inter = sens[:,2]

    input1 = np.reshape(input1, (13,365))
    input2 = np.reshape(input2, (13,365))
    inter = np.reshape(inter, (13,365))

    avg_1 = np.mean(input1, axis = 0)
    avg_2 = np.mean(input2, axis = 0)
    avg_inter = np.mean(inter, axis = 0)
    
    si = np.vstack((avg_1,avg_2,avg_inter))
    return np.transpose(si)

avgsi = averageSensitivity(SI)
#yr = 4 # 4 for 1936, 59 for 1991

fig = plt.figure()
ymaxs = np.ones(1)
ymins = np.zeros(1)
y1 = np.zeros([365]) # Days * Hour Clusters
ax = fig.add_subplot(1,1,1)
# for k in range(len(inputs)): # Two 1st order SIs
for k in range(3):
    y2 = np.zeros([365]) # Days * Hour Clusters
    posIndices = np.where(np.sum(avgsi[:,len(inputs)::],1) > 0)

    y2[posIndices] = np.sum(avgsi[:,0:(k+1)],1)[posIndices]/ \
            np.sum(avgsi[:,:],1)[posIndices]
    x = range(365)
    ax.plot(x,y2,c='None')
    ax.fill_between(x, y1, y2, where=y2>y1, color=colors[k])
    ymaxs = max(ymaxs,np.max(y2))
    y1 = y2   

# y1 = np.zeros([2190]) # Days * Hour Clusters 
colors = ['#e31a1c','#1f78b4','#33a02c']
   
for k in range(3):
    y2 = np.zeros([365]) # Days * Hour Clusters
    negIndices = np.where(np.sum(avgsi[:,len(inputs)::],1)<0)

    y2[negIndices] = np.sum(abs(avgsi[:,0:(k+1)]),1)[negIndices]/ \
            np.sum(abs(avgsi[:,:]),1)[negIndices]
    x = range(365)
    ax.plot(x,y2,c='None')
    ax.fill_between(x, y1, y2, where=y2>y1, color=colors[k])
    ymaxs = max(ymaxs,np.max(y2))
    y1 = y2
    
fig.text(0.01, 0.5, 'Portion of Variance', va='center', rotation='vertical', fontsize=18)
# fig.subplots_adjust(bottom=0.15,hspace=0.3)
# plt.figlegend([pSt,pFcst,pInteract,pNegInt],\
#             [r'$s_t$',r'$\tilde{q}_{t+3}$','Pos. Interactions', 'Neg. Interactions'],\
#             loc='lower center', ncol=3, fontsize=16, frameon=True)

plt.show()