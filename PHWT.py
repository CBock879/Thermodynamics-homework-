# -*- coding: utf-8 -*-
"""
Created on Sun Mar 25 12:10:55 2018

@author: Chris
"""


import numpy as np
import matplotlib.pyplot as pyp
import PPTools as PPT





K = lambda C: C+273.15

outside_temp = 27
regen_epsilon = [0.5,0.7,0.8,0.9,0.96,0.98]
regen_costs =   [2200000,2500000,3100000,4000000,5200000,6700000]
heat_per_unit = 52200000.0
 



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
   
    
    #finds total lifetime fuel cost of power plant
    total_life_heat =  total_life_power/eta_th
    fuel_cost = (total_life_heat/heat_per_unit)*fuel_cost_per_unit
    return fuel_cost



#Part A
print()
for i in range (1,5):
    epsilon_sweep = np.linspace(0,1,200)
    eff = PPT.power_plant(i,i,epsilon_sweep,300,K(1150),100,9)
    pyp.plot(epsilon_sweep, eff)
pyp.legend('4321')   
pyp.xlabel('regenerator effectiveness')
pyp.ylabel('efficency')
pyp.show()
#
#
#part B
max = 5
effs = np.zeros([max,6])
costs = np.zeros([max,6]) 
print()
cst_min = 9000000000000000.0
best_stages = 0 
best_rgn = 0
for i in range(0,max):
        for k in range(1,5):
            #finds data for this configuration
            eff = PPT.power_plant(i+1,i+1,regen_epsilon[k],300,K(1150),100,9) 
            effs[i,k] = eff
            costs[i,k] = total_cost(i+1,i+1,regen_costs[k]) + life_cost(eff)
            print (eff)
            #finds if this configuration is better
            
            if (cst_min > costs[i,k]):
                cst_min = costs[i,k]
                best_stages = i+1
                best_rgn = k
                print(eff)
                print ("test",i)

                
#
eta_TH = PPT.power_plant(best_stages,best_stages,
                         regen_epsilon[best_rgn],300,K(1150),100,9)
print("eta" ,eta_TH)

#calculates mass flow
mass_flow = (((5 * 10**6)/eta_TH)/heat_per_unit)
print("mass flow of best configuration",mass_flow)



#max = 5
#effs = np.zeros([max,max,6],dtype=float)
#costs = np.zeros([max,max,6],dtype = float )
#cst_min = 9000000000000000.0
#best_config = np.zeros([3]) 
#for i in range(0,max):
#        for k in range(0,6):
#            
#            #finds data for this configuration
#            eff = PPT.power_plant(i+1,j+1,regen_epsilon[k],300,K(1150),100,9) 
#            effs[i,j,k] = eff
#            costs[i,j,k] = total_cost(i+1,j+1,regen_costs[k]) + life_cost(eff)
#            #finds if this configuration is better
#            if (cst_min> costs[i,j,k]):
#                cst_min = costs[i,j,k]
#                best_config=[i+1,j+1,k]
#                print(i+1,"compressors",j+1,"turbines",regen_costs[k])
##temp_range = np.linspace(250,500,100)
#temp_sweep = []
#for i in range (0,100):
#    eta =  power_plant(best_config[0]+1,best_config[1]+1,regen_epsilon[best_config[2]],
#                         temp_range[i],1400,100,9)
#    temp_sweep.append(eta)
#
#temp_diff = np.diff(temp_sweep)
#    

#pyp.ylabel(r'$\eta_{th}$')
#pyp.xlabel("Outside Temperature (K)")
#pyp.plot(temp_range,temp_sweep)     
