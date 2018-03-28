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

#effects = np.array([0.3,0.4,0.5],
#                   [10, 20, 30],
#                   [0,0,0])
Cp = 1.004                          #Specific heat 
Cv= 0.8                     
k = 1.4                             #Specific heat ratio
cst_trbn= 400000                    #Cost of turbine
cst_no_compressor  = 1000000        #Cost of compressor 
cst_reheater =  1   

##finds the most cost effiecent regenerator cost per % 
#for i in effects:
#    effects[2][i] = effects[0][i] / effects[1][i]
##sorts
#effects.sort(key=lambda x:x[2])


#no_comp: number of no_compressors
#no_turb: number of no_turbines
#rgn_ep regenerator epsilon ( effectivnes)
class power_plant:
    t1 = 27 + 273.13                #t1 = temperature 1
    t3 = 1150.0 + 273.13            #t3: temperature 3
    Pr = 9.0                        #Pr = pressure ratio
    def cycle(self,no_comp, no_turb, rgn_ep):
        
         
        # runs through each of the stages of the no_compression
        Prs  = self.Pr ** ( 1.0/ no_comp)    #Prs: pressure ratio for individual stages
        
        t2 = (Prs)**((k-1)/k) *self.t1       #t2: tempature 2
        win = (t2-self.t1) * Cp              #win: work in
        nwin = win * no_comp
        
        
        # find qin from inital heat addition
        qin = (self.t3 - t2) * Cp            #qin: heat input 
    
        #find work extracted and heat needed for reheat
        t4 = self.t3 * (1/Prs)**((k-1)/k)    #t4: temperature 4
        print(t4)
        wout = (self.t3-t4) * Cp             #wout: work out 
        if( no_turb > 1):
            qin = qin +  wout * (no_turb - 1)
        
        nwout = (wout * no_turb) - nwin
        
        #find heat regained from regenerator
        q_regenable = (t4-t2)*Cp        # q_regnenable: heat able to be regenerated
        q_regen = q_regenable*rgn_ep    # q_regen: heat regenerated
        
        # accounts for heat regenerated 
        qin = qin - q_regen
        
        output = (nwout/qin)
        return output

max = 5 
print(cycle(1,1,0))
#effs = np.zeros([max,max])
#for i in range(1,max):
#    for j in range(1,max):
#        effs[i,j] = cycle(i,j,0.1)

#pyp.contourf(effs, 100)



        
        
