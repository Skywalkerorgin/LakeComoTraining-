# -*- coding: utf-8 -*-
"""
Created on Fri May 29 15:33:32 2020

@author: Rohini
"""

import numpy as np
import math
import os

#M = 5 # number of inputs: storage at the 4 reservoirs, forecasted water level at Hanoi, \
# ignore sin(2*pi*t/365 - phi1) and cos(2*pi*t/365 - phi2) b/c their centers and radii are fixed
M=4
#N = 12 # number of RBFs
N=5
#K = 4 # number of outputs: release at the 4 reservoirs
K=1

def calcAnalyticalSIs():
    #policyVars_2 = np.loadtxt('HydroInfo_100_thinned.resultfile')
    policyVars = np.loadtxt('C:/Users/Rohini/Box Sync/LakeComo/ComoTestDVs_perfect.reference')
    
    #solns = [35, 37, 52, 33]
    solns=[210]
    days = 365
    #years = 1000
    years=13
    #inputNames = ['sSL','sHB','sTQ','sTB','HNfcst']
    inputNames=['lake_level','p_fcast']
    #outputNames = ['uSL','uHB','uTQ','uTB']
    outputNames=['release']
    # first row inputs lower bounds, second row outputs lower bounds (including bounds on sin() and cos())
    # third row inputs upper bounds, fourth row output upper bounds
#    IO_ranges = np.array([[2223600000, 3215000000, 402300000, 402300000, 0, -1, -1, \
#                           0, 0, 0, 0], \
#                            [12457000000, 10890000000, 2481000000, 3643000000, 20, 1, 1, \
#                             40002, 35784, 13551, 3650]])
    IO_ranges = np.array([[-0.5,-10114.1, -1, -1, \
                           0], \
                            [1.3,21640, 1, 1, \
                             4961.6]])
    header = ''
    for input in inputNames:
        header = header + ',' + input + '_1' # first order indices
        
    for i in range(len(inputNames)-1):
        for j in range(i+1,len(inputNames)):
            header = header + ',' + inputNames[i] + '+' + inputNames[j]
            
    header = header[1:] # remove beginning comma
    
    #doy = np.array(np.concatenate((np.arange(121,366,1),np.arange(1,121,1)),0))
    doy = np.array(np.arange(1,366,1))
    
    for soln in solns:
        # load decision variables of this solution
        #policy = policyVars[soln-1,0:168]
        policy=policyVars[soln-1,0:46]
        #phi1 = policyVars[soln-1,168]
        #phi2 = policyVars[soln-1,169]
        C, B, W = reorganizeVars(M, N, K, policy)
        os.chdir('C:/Users/Rohini/Box Sync/LakeComo/streamflow/deficit')
        # find covariances at each day
        cov = np.zeros([days, M-2, M-2])
        allData = np.zeros([years, days, M+K])
        for day in range(days):
            dailyData = np.loadtxt('day' + str(doy[day]) + '.txt')
            # append sin() and cos() functions to inputs
            #sinArray = np.ones([years,1])*np.sin(2*math.pi*doy[day]/365.0 - phi1)
            sinArray = np.ones([years,1])*np.sin(2*math.pi*doy[day]/365.0)
            cosArray = np.ones([years,1])*np.cos(2*math.pi*doy[day]/365.0)
            dailyData = np.concatenate((np.concatenate((dailyData[:,0:M-2],sinArray),1),dailyData[:,(M-2):(M-2+K)]),1)
            dailyData = np.concatenate((np.concatenate((dailyData[:,0:(M-1)],cosArray),1),dailyData[:,(M-1):(M-1+K)]),1)
            dailyData = normalizeInputs(dailyData[:,0:(M+K)], IO_ranges)
            allData[:,day,:] = dailyData
            cov[day,:,:] = np.cov(np.transpose(dailyData[:,0:M-2]))
            
        # find sensitivity indices at each time step
        for output in range(K):
            allSI = np.zeros([days*years, int((M-2) + (M-2)*(M-3)/2)])
            allD = np.zeros([days*years, int(M-2 + (M-2)*(M-3)/2)])
            for year in range(years):
                for day in range(days):
                    inputValues = allData[year,day,0:(M)]
                    for col in range(M-2): # first order indices
                        D = calcD(C, B, W, col, inputValues, output)
                        allSI[year*365+day,col] = D**2 * cov[day,col,col]
                        allD[year*365+day,col] = D
                        
                    count = 0
                    for col1 in range(M-3): # second order indices
                        for col2 in range(col1+1,M-2):
                            D1 = calcD(C, B, W, col1, inputValues, output)
                            D2 = calcD(C, B, W, col2, inputValues, output)
                            allSI[year*365+day,(M+count-2)] = 2*D1*D2*cov[day,col1,col2]
                            count = count + 1
                            
            np.savetxt('Solution_210.txt', \
                       allSI, header=header, comments='', delimiter=',')
            np.savetxt('Derivative.txt', \
                       allD, header=header, comments='', delimiter=',')
                    
    return None
                    
def calcD(C, B, W, inputNumber, inputValues, outputNumber):
    # calculate analytical first order partial derivative of RBF outputNumber with respect to inputNumber 
    # located at inputValues
    D = 0
    for n in range(N):
        innerSum = 0
        for m in range(M):
            innerSum = innerSum - (inputValues[m] - C[m,n])**2 / B[m,n]**2
        
        D = D - 2 * ((inputValues[inputNumber]-C[inputNumber,n])/(B[inputNumber, n])**2) * W[outputNumber,n] * np.exp(innerSum)
    
    return D

def reorganizeVars(M, N, K, policy):    
    # Re-organize decision variables into weight (W), center (C) and raddi (B) matrices
    # C and R are M x N, W is K X N where M = # of inputs, K = # of outputs and N = # of RBFs
    #C = np.zeros([M+2,N])
    #B = np.zeros([M+2,N])
    C = np.zeros([M,N])
    B = np.zeros([M,N])
    W = np.zeros([K,N])
    for n in range(N):
        for m in range(M):
            C[m,n] = policy[(2*M+K)*n + 2*m]
            if policy[(2*M+K)*n + 2*m + 1] < 10**-6:
                B[m,n] = 10**-6
            else:
                B[m,n] = policy[(2*M+K)*n + 2*m + 1]
        
        #C[M,n] = 0.0 # center for sin(2*pi*t/365 - phi1)
        #C[M+1,n] = 0.0 # center for cos(2*pi*t/365 - phi1)
        #B[M,n] = 1.0 # radius for sin(2*pi*t/365 - phi1)
        #B[M+1,n] = 1.0 # radius for cos(2*pi*t/365 - phi1)
        for k in range(K):
            W[k,n] = policy[(2*M+K)*n + 2*M + k]
            
    # Normalize weights to sum to 1 across N RBFs (so each row of W should sum to 1)
    totals = np.sum(W,1)
    for k in range(K):
        if totals[k] > 10**-6:
            W[k,:] = W[k,:]/totals[k]
        
    return C, B, W

def normalizeInputs(inputs, input_ranges):
    normInputs = np.zeros(np.shape(inputs))
    for i in range(np.shape(input_ranges)[1]):
        normInputs[:,i] = (inputs[:,i] - input_ranges[0,i]) / (input_ranges[1,i] - input_ranges[0,i])
    
    return normInputs

calcAnalyticalSIs()