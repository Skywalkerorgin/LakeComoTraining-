import numpy as np
from matplotlib import pyplot as plt

# plot tradeoffs
ref_set = np.loadtxt('ComoTest.reference', delimiter=' ', skiprows=3)

# plot reference set tradeoffs
plt.scatter(ref_set[:,0], ref_set[:,1], alpha=.7)
plt.xlabel('$\leftarrow$ Flood Control (Days/Year)')
plt.ylabel('$\leftarrow$ Water Supply Deficit ($m^3/s)^2$')
plt.savefig('tradeoffs.png')

# Plot runtime diagnostics
# (need a folder called "runtime_metrics" and all metric files to be named
# according to their seed and master ie. S1_M1.metrics for seed 1 master 1)
NFE = np.linspace(0, 200, 101)

# plot runtime diagnostics
for S in range(0, 6):
    for M in [0, 1]:
        metrics = np.loadtxt('runtime_metrics/S' + str(S) + '_M' +str(M)+ 
                             '.metrics', delimiter=' ', skiprows=1)
        HV = metrics[:,0]
        HV = np.hstack([0, HV])
        
        plt.plot(NFE, HV, alpha=.75, label='S' + str(S)+ '_M' + str(M))

plt.xlabel('NFE ($10^4$)')
plt.ylabel('Relative HV')
plt.xlim([0, 200])
plt.ylim([0,1])
plt.savefig("runtime_HV.png")