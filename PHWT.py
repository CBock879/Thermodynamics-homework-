# -*- coding: utf-8 -*-
"""
Created on Sun Mar 25 12:10:55 2018

@author: Chris
"""


import numpy as np
import matplotlib.pyplot as pyp
import matplotlib



#class regen:
#    cost = 100
#    effect = 0.9
#    ratio = 0.8
#    def __init__(self,c,e):
#        cost = c
#        effect = e
#        ratio = effect/cost

#effects = np.array([0.3,0.4,0.5],
#                   [10, 20, 30],
#                   [0,0,0])
Cp = 1.004                          #Specific heat 
Cv= 0.8                     
k = 1.4                             #Specific heat ratio
cst_trbn= 1100000                   #Cost of turbine
cst_no_compressor  = 400000        #Cost of compressor 
cst_reheater =  1   

##finds the most cost effiecent regenerator cost per % 
#for i in effects:
#    effects[2][i] = effects[0][i] / effects[1][i]
##sorts
#effects.sort(key=lambda x:x[2])


#no_comp: number of no_compressors
#no_turb: number of no_turbines
#rgn_ep regenerator epsilon ( effectivnes)

t1 = 27.0 + 273.13                #t1 = temperature 1
t3 = 1150.0 + 273.13            #t3: temperature 3
Pr = 9.0                        #Pr = pressure ratio
def power_plant(no_comp, no_turb, rgn_ep):
    # runs through each of the stages of the no_compression
    Prs  = Pr ** ( 1.0/ no_comp)    #Prs: pressure ratio for individual stages
    
    t2 = (Prs)**((k-1.0)/k) *t1       #t2: tempature 2
    win = (t2-t1) * Cp              #win: work in
    nwin = win * no_comp
    
    T[1] = t2
     
    # find qin from inital heat addition
    qin = (t3 - t2) * Cp            #qin: heat input 

    #find work extracted and heat needed for reheat
    t4 = t3 * (1/Prs)**((k-1)/k)    #t4: temperature 4
    T[3] = t4 
    print(t4)
    wout = (t3-t4) * Cp *no_turb             #wout: work out 
    if( no_turb > 1):
        qin = qin +  (wout/no_turb) * (no_turb - 1)
    nwout = wout * - nwin
    
    #find heat regained from regenerator
    q_regenable = (t4-t2)*Cp        # q_regnenable: heat able to be regenerated
    q_regen = q_regenable*rgn_ep    # q_regen: heat regenerated
    
    # accounts for heat regenerated 
    qin = qin - q_regen
    
    output = (nwout/qin)
    return output
    
def total_cost(no_comp, no_turb, regencost):
    cost = no_comp*cst_no_compressor + no_turb*cst_trbn + 5500000.0 + regencost
    return cost

#finds the total total cost of fuel for the lifetime of the turbine
def life_cost(eta_th):
    total_life_power =  4000000.0*60.0*60.0*24.0*365.0*20.0
    fuel_cost_per_unit = 0.28
    heat_per_unit = 52200000.0
    total_life_heat =  total_life_power/eta_th
    fuel_cost = (total_life_heat/heat_per_unit)*fuel_cost_per_unit
    return fuel_cost


max = 5 



#levels =  [0,1,2,3,4,5]
#print(power_plant(1.0,1.0,0.0))
#effs = np.zeros([max,max])
#costs = np.zeros([max,max])
#for i in range(1,max):
#    for j in range(1,max):
#        effs[i,j] = power_plant(i,j,0.6)
#        costs[i,j] = total_cost(i,j,5000.0) + life_cost(effs[i,j])


lin_eff  = np.zeros([max])      
for i in range(1,max):
       lin_eff[i] = power_plant(i,i,0.6)

p1 = pyp.figure(1)
pyp.contourf(costs, 100, vmin=0)
p2 = pyp.figure(2)
pyp.contourf(effs, 100)
p3 = pyp.figure(3)
pyp.plot(lin_eff)
p1.show()
p2.show()
p3.show()

        
        
