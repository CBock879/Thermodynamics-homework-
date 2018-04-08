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
    fuel_cost = life_cost(eff)
    print(fuel_cost)
    pyp.legend('4321')   
    pyp.xlabel('regenerator effectiveness')
    pyp.subplot(211)
    pyp.xticks([])
    pyp.ylabel('efficency')
    
    pyp.plot(epsilon_sweep, eff)
    pyp.subplot(212)
    pyp.ylabel('cost')
    pyp.plot(epsilon_sweep,fuel_cost)
    
    


pyp.show()

#

#part B
max = 5
effs = np.zeros([max,6])
costs = np.zeros([max,6]) 
cst_min = 9000000000000000.0 
regen_cost = 0
best_config = PPT.PPlant(1,1,0,300,1000,100,9)

for i in range(0,max):
        for k in range(1,5):
            
            #finds data for this configuration
            eff = PPT.power_plant(i+1,i+1,regen_epsilon[k],300,K(1150),100,9) 
            effs[i,k] = eff
            costs[i,k] = total_cost(i+1,i+1,regen_costs[k]) + life_cost(eff)
            
            
            #finds if this configuration is better
            if (cst_min > costs[i,k]):  
                best_config = PPT.PPlant(i+1,i+1,regen_epsilon[k],300,K(1150),100,9)
                cst_min = costs[i,k]
                regen_cost = regen_costs[k]


#gets efficency
print('Thermal efficency of best configuration', best_config.eta)
         
print()

#prints outlet states       
best_config.outlet_states()

print()

#prints net work
print('Net specific work of cycle',best_config.nwork)

#prints back work ratio
print('Back work ratio' , best_config.back_work_ratio)


#calculates air flow
mass_flow = best_config.air_flow(4000000)
print("Air flow of best configuration",mass_flow, 'kg/s')

#heat input
print('rate of heat input', best_config.nq, 'kJ/kg')

#calculated fuel consumption
mass_flow = best_config.fuel_flow(heat_per_unit,4000000)
print("Fuel flow of best configuration",mass_flow)

#gets total lifetime fuel cost
print('total fuel cost over 20 years',life_cost(best_config.eta))

#gets total equipment cost
print('total equipment cost', best_config.equipement_cost(regen_cost))

#gets cost of best configuration
print('Total cost of best configuration: $', (cst_min))


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
