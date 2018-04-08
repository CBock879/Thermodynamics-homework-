
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  7 15:11:40 2018

@author: Chris
"""

import matplotlib.pyplot as pyp

def power_plant(no_comp, no_turb, rgn_ep,t1,t3,P1,Pr):
    
    
    Cp = 1.004                          #Specific heat                    
    k = 1.4 
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
            
    #find heat regained from regenerator
    q_regenable = (t4-t2)*Cp        # q_regnenable: heat able to be regenerated
    q_regen = q_regenable*rgn_ep    # q_regen: heat regenerated
     
    #accounts for heat regenerated 
    qin = qin - q_regen
    
    #find net work 
    nwout = wout - win 
    
    
    
    

    
    output = (nwout/qin)
    return output





class PPlant:
    
    P = []
    T = []
    back_work_ratio = 0 
    nwork = 0
    nq = 0
    eta  = 0
    compressors = 0
    turbines = 0

    def __init__(self,no_comp, no_turb, rgn_ep,t1,t3,P1,Pr):
        
        self.P = []
        self.T = []
        Cp = 1.004                          #Specific heat                    
        k = 1.4 
        # runs through each of the stages of the no_compression
        Prs  = Pr ** ( 1.0/ no_comp)    #Prs: pressure ratio for individual stages
                     
        p = P1            
        self.compressors = no_comp
        self.turbines = no_turb
        
        #first compression stage
        t2 = (Prs)**((k-1.0)/k) * t1       #t2: tempature 2
        win = (t2-t1)*Cp
        self.T.append(t1)
        self.T.append(t2)
        self.P.append(p)
        p = p*Prs
        self.P.append(p)
        
        
        #subseqent compression stages
        if (no_comp > 1):
            for i in range(1,no_comp):
                
                self.T.append(t1)     
                #t2 = (Prs)**((k-1.0)/k) * t2
                self.T.append(t2)
                
                win += (t2-t1)*Cp
                      
                
                
                self.P.append(p)
                p = p*Prs
                self.P.append(p)
                
                
        # find qin from inital heat addition
        qin = (t3 - t2) * Cp            #qin: heat input 
    
        #recalculates stage pressure ratio
        Prs  = Pr ** (1.0/ no_turb)    #Prs: pressure ratio for individual stages  
        
                     
        #inital turbine stage
        t4 = t3 * (1/Prs)**((k-1)/k)    #t4: temperature 4
        wout = (t3-t4) * Cp 
        self.T.append(t3)
        self.T.append(t4)
        self.P.append(p)
        p = p/Prs
        self.P.append(p)
        
        
        #subsequent turbine stages
        if( no_turb > 1):
            for i in range(1,no_turb):
                qin += wout
                self.T.append(t3)
                #t4 = t4 * (1/Prs)**((k-1)/k)   
                wout += (t3-t4) * Cp 
                self.T.append(t4)        
                
                
                self.P.append(p)
                p = p/Prs
                self.P.append(p)
                
        #find heat regained from regenerator
        q_regenable = (t4-t2)*Cp        # q_regnenable: heat able to be regenerated
        q_regen = q_regenable*rgn_ep    # q_regen: heat regenerated
         
        #accounts for heat regenerated 
        
        qin = qin - q_regen
        
        self.nq = qin
        
        #print(win)
        #print(wout)
        
        self.back_work_ratio = win/wout
        
        #find net work 
        self.nwork = wout - win 
        
        
        
        self.eta = self.nwork/qin
        
    #prints inlet and 
    def outlet_states(self):

        #pyp.plot(self.T,self.P)
        for i in range(0,self.compressors+self.turbines+4,2):
            if i<self.compressors*2:
                print('inlet at compressor ',self.P[i],'kPa  ',self.T[i], "K")
                print('outlet at compressor',self.P[i+1],'kPa  ',self.T[i+1], "K")
            else:
                print('inlet at turbine ',self.P[i],'kPa  ',self.T[i], "K")
                print('outlet at turbine',self.P[i+1],'kPa  ',self.T[i+1], "K")
        
    #finds air mass flow        
    def air_flow(self,load):
        return load/self.nwork
    
    def equipement_cost(self,regen_cost):
        cost_turbine= 1100000                   #Cost of turbine
        cost_compressor  = 400000        #Cost of compressor   
        cost = cost_turbine*self.turbines+cost_compressor*self.compressors + 5500000.0 + regen_cost
        return cost
    
    #finds fuel consumed
    def fuel_flow(self,energy_unit,load):
        return  (load/self.eta)/energy_unit
    
        
        


