# -*- coding: utf-8 -*-
"""
Created on Sun Mar 25 12:10:55 2018

@author: Chris
"""


import numpy as np
import matplotlib.pyplot as pyp




#class regen:
#    cost = 100
#    effect = 0.9
#    ratio = 0.8
#    def __init__(self,c,e):
#        cost = c
#        effect = e
#        ratio = effect/cost




regen_epsilon = [0.5,0.7,0.8,0.9,0.96,0.98]
regen_costs =   [2200000,2500000,3100000,4000000,5200000,6700000]
 
#no_comp: number of no_compressors
#no_turb: number of no_turbines
#rgn_ep regenerator epsilon ( effectivnes)

#t1 = 27.0 + 273.13                #t1 = temperature 1
#t3 = 1150.0 + 273.13            #t3: temperature 3
#Pr = 9.0                        #Pr = pressure ratio
#P1 = 100.0
def power_plant(no_comp, no_turb, rgn_ep,t1,t3,P1,Pr):
    Cp = 1.004                          #Specific heat                    
    k = 1.4 

    #fluid = IAPWS97(T = 0, P = 2)
    P = []
    T = []
    win = 0 

    
    # runs through each of the stages of the no_compression
    Prs  = Pr ** ( 1.0/ no_comp)    #Prs: pressure ratio for individual stages
                 
    #first compression stage
    t2 = (Prs)**((k-1.0)/k) * t1       #t2: tempature 2
    win = (t2-t1)*Cp
    T.append(t1)
    T.append(t2)
    P.append(P1)
    p = P1*Prs
    P.append(p)
    
    
    #subseqent compression stages
    if (no_comp > 1):
        for i in range(1,no_comp):
            
            T.append(t1)     
            #t2 = (Prs)**((k-1.0)/k) * t2
            T.append(t2)
            
            win += (t2-t1)*Cp
                  
            
            
            P.append(p)
            p = p*Prs
            P.append(p)
            
            
    # find qin from inital heat addition
    qin = (t3 - t2) * Cp            #qin: heat input 

    #recalculates stage pressure ratio
    Prs  = Pr ** (1.0/ no_turb)    #Prs: pressure ratio for individual stages  
    
                 
    #inital turbine stage
    t4 = t3 * (1/Prs)**((k-1)/k)    #t4: temperature 4
    wout = (t3-t4) * Cp 
    T.append(t3)
    T.append(t4)
    P.append(p)
    p = p/Prs
    P.append(p)
    
    
    #subsequent turbine stages
    if( no_turb > 1):
        for i in range(1,no_turb):
            qin += wout
            T.append(t3)
            #t4 = t4 * (1/Prs)**((k-1)/k)   
            wout += (t3-t4) * Cp 
            T.append(t4)        
            
            
            P.append(p)
            p = p/Prs
            P.append(p)

    #print(wout)
    
    #find heat regained from regenerator
    q_regenable = (t4-t2)*Cp        # q_regnenable: heat able to be regenerated
    q_regen = q_regenable*rgn_ep    # q_regen: heat regenerated
     
    #accounts for heat regenerated 
    qin = qin - q_regen
    
    #find net work 
    nwout = wout - win 
    
    output = float(nwout/qin)
    return output
    


def total_cost(no_comp, no_turb, regencost):
    cst_trbn= 1100000                   #Cost of turbine
    cst_no_compressor  = 400000        #Cost of compressor   
    cost = no_comp*cst_no_compressor + no_turb*cst_trbn + 5500000.0 + regencost
    return cost




#finds the total total cost of fuel for the lifetime of the turbine
def life_cost(eta_th):
    
    #total amount of energy (J) power plant puts out in life
    total_life_power =  4000000.0*60.0*60.0*24.0*365.0*20.0
    
    #fuel properties
    fuel_cost_per_unit = 0.28
    heat_per_unit = 52200000.0
    
    #finds total lifetime fuel cost of power plant
    total_life_heat =  total_life_power/eta_th
    fuel_cost = (total_life_heat/heat_per_unit)*fuel_cost_per_unit
    return fuel_cost



effs = np.zeros([max,max],dtype=float)
costs = np.zeros([max,max],dtype = float )


cst_min = 9000000000000000.0

best_config = np.zeros([3])

max = 5
for i in range(0,max):
    for j in range(0,max):
        for k in range(0,6):
            
            #finds data for this configuration
            eff = power_plant(i+1,j+1,regen_epsilon[k],300,1400,100,9) 
            effs[i,j] = eff
            costs[i,j] = total_cost(i+1,j+1,regen_costs[k]) + life_cost(eff)
            
            #finds if this configuration is better
            if (cst_min> costs[i,j]):
                cst_min = costs[i,j]
                best_config=[i,j,k]
                print(i+1,"compressors",j+1,"turbines",regen_costs[k])


temp_range = np.linspace(250,300,100,float)
temp_sweep = []
for i in range (0,100):
    
    eta =  power_plant(best_config[0]+1,best_config[1]+1,regen_epsilon[best_config[2]],
                         temp_range[i],1400,100,9)
    temp_sweep.append(eta)
    
pyp.plot(temp_sweep)