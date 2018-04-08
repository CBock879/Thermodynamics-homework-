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
    total_life_power =  4000000.0*60.0*60.0*24.0*365.25*20.0
    
    #fuel properties
    fuel_cost_per_unit = 0.28
   
    
    #finds total lifetime fuel cost of power plant
    total_life_heat =  total_life_power/eta_th
    fuel_cost = (total_life_heat/heat_per_unit)*fuel_cost_per_unit
    return fuel_cost


fig1 = pyp.figure(1)

#Part A
print()
for i in range (1,5):
    epsilon_sweep = np.linspace(0,1,200)
    eff = PPT.power_plant(i,i,epsilon_sweep,300,K(1150),100,9)
    fuel_cost = life_cost(eff)
    
      
    pyp.xlabel('regenerator effectiveness')
    pyp.subplot(211)
    pyp.xticks([])
    pyp.ylabel('efficency')
    
    pyp.plot(epsilon_sweep, eff)
    pyp.subplot(212)
    pyp.ylabel('cost')
    pyp.plot(epsilon_sweep,fuel_cost)
    
    

pyp.legend('1234') 
fig1.show()

#

#part B

print("Part B")
max = 5
cst_min = 9000000000000000.0 
regen_cost = 0
best_config = PPT.PPlant(1,1,0,300,1000,100,9)

for i in range(0,max):
        for k in range(1,5):
            
            #finds data for this configuration
            eff = PPT.power_plant(i+1,i+1,regen_epsilon[k],300,K(1150),100,9) 
            cost = total_cost(i+1,i+1,regen_costs[k]) + life_cost(eff)
            
            
            #finds if this configuration is better
            if (cst_min > cost):  
                best_config = PPT.PPlant(i+1,i+1,regen_epsilon[k],300,K(1150),100,9)
                cst_min = cost
                regen_cost = regen_costs[k]


print('best config', best_config.compressors, "compressors",
      best_config.turbines, "turbines", + best_config.epsilon , 'regenerator')

#gets efficency
print('Thermal efficency of best configuration', best_config.eta)
         
print()

#prints outlet states       
best_config.outlet_states()

print()

#prints net work
print('Net specific work of cycle',best_config.nwork, 'kJ/kg')
print()


#prints back work ratio
print('Back work ratio' , best_config.back_work_ratio)
print()


#calculates air flow
mass_flow = best_config.air_flow(4000000)
print("Air flow of best configuration",mass_flow, 'kg/s')
print()

#heat input
print('rate of heat input', best_config.nq, 'kJ/kg')
print()

#calculated fuel consumption
mass_flow = best_config.fuel_flow(heat_per_unit,4000000)
print("Fuel flow of best configuration",mass_flow, 'kg/s')
print()

#gets total lifetime fuel cost
print('total fuel cost over 20 years  $',life_cost(best_config.eta), )
print()

#gets total equipment cost
print('total equipment cost  $', best_config.equipement_cost(regen_cost))
print()

#gets cost of best configuration
print('Total cost of best configuration: $', (cst_min))
print()

comps  = best_config.compressors
turbs  = best_config.turbines

temp_range = np.linspace(-30,40,100)
epsilon = best_config.epsilon
eta_range = PPT.power_plant(comps,turbs,epsilon,K(temp_range),K(1150),100,9)

fig2 = pyp.figure(2)
pyp.plot(temp_range,eta_range)
pyp.title('Tempature vs $\eta_{th}$')
pyp.xlabel('Temperature (deg C)')
pyp.ylabel('$\eta_{th}$')
fig2.show()

print()
print()
print()


#Part C

print("PartC")
best_config = PPT.PPlant(1,1,0,300,1000,100,9)
cst_min = 9000000000000000.0


for i in range(0,max):
    for j in range(0,max):
        for k in range(0,6):
            #finds data for this configuration
            eff = PPT.power_plant(i+1,j+1,regen_epsilon[k],300,K(1150),100,9) 
            cost = total_cost(i+1,j+1,regen_costs[k]) + life_cost(eff)
            #finds if this configuration is better
            if (cst_min> cost):
                best_config = PPT.PPlant(i+1,j+1,regen_epsilon[k],300,K(1150),100,9)
                cst_min = cost
                regen_cost = regen_costs[k]
                
#gets efficency
print('Thermal efficency of best configuration', best_config.eta)
         
print()

print('best config', best_config.compressors, "compressors",
      best_config.turbines, "turbines", + best_config.epsilon , 'regenerator')


#prints outlet states       
best_config.outlet_states()

print()

#prints net work
print('Net specific work of cycle',best_config.nwork, 'kJ/kg')

print()

#prints back work ratio
print('Back work ratio' , best_config.back_work_ratio)

print()

#calculates air flow
mass_flow = best_config.air_flow(4000000)
print("Air flow of best configuration",mass_flow, 'kg/s')
print()

#heat input
print('rate of heat input', best_config.nq, 'kJ/kg')
print()

#calculated fuel consumption
mass_flow = best_config.fuel_flow(heat_per_unit,4000000)
print("Fuel flow of best configuration",mass_flow, 'kg/s')

print()
#gets total lifetime fuel cost
print('total fuel cost over 20 years  $',life_cost(best_config.eta), )
print()

#gets total equipment cost
print('total equipment cost  $', best_config.equipement_cost(regen_cost))
print()

#gets cost of best configuration
print('Total cost of best configuration: $', (cst_min))
print()

comps  = best_config.compressors 
turbs  = best_config.turbines

temp_range = np.linspace(-30,40,100)
epsilon = best_config.epsilon
eta_range = PPT.power_plant(comps,turbs,epsilon,K(temp_range),K(1150),100,9)

fig3 = pyp.figure(2)
pyp.plot(temp_range,eta_range)
pyp.title('Tempature vs $\eta_{th}$')
pyp.xlabel('Temperature (deg C)')
pyp.ylabel('$\eta_{th}$')
fig3.show()

