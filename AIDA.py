# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 01:51:03 2020

@author: Matthew
"""
import numpy as np     #importing necessary packages

print("Enter Building Volume [m^3]:")             #The following controls the input of quantities needed for calculations.
Volume=float(input())
print("Enter Number of Flow Paths:")
N=int(input())

Height=np.zeros(N)         #defining arrays for relevant quantities. 
FlowCoefficient=np.zeros(N)        
FlowExponent=np.zeros(N)
WindPressureCoefficient=np.zeros(N)
TotalExternalPressure=np.zeros(N)
WindInducedPressure=np.zeros(N)
StackInducedPressure=np.zeros(N)
FlowRate=np.zeros(N)
AirDensity=1.29                 


for I in range(N):
    print("Enter Height of Path %s [m]" %(I+1))
    Height[I]=float(input())
    print("Enter Flow Coefficient for Path %s" %(I+1))
    FlowCoefficient[I]=float(input())
    print("Enter Flow Exponent for Path %s" %(I+1))
    FlowExponent[I]=float(input())
    print("Enter Wind Pressure Coefficient for Path %s" %(I+1))
    WindPressureCoefficient[I]=float(input())
    
while True:                    #This 'while' loop allows the program to continue after the first set of calculations,
    print("Enter External Temperature [Celsius]:")  #however you can't change the building data.
    ExternalTemp=float(input())
    print("Enter Internal Temperature [Celsius]:")
    InternalTemp=float(input())
    print("Enter Wind Speed at Building Height [m/s]:")
    WindSpeed=float(input())

    for J in range(N):
        WindInducedPressure[J]=0.5*AirDensity*WindPressureCoefficient[J]*WindSpeed**2
        StackInducedPressure[J]=-3455*Height[J]*(1/(ExternalTemp+273)-1/(InternalTemp+273))
        TotalExternalPressure[J]=WindInducedPressure[J]+StackInducedPressure[J]
        
    InternalPressure=-100
    X=50                      #X is the iteration step for the internal pressure.
    
    while True:         #Loop which calculates the flow rate by iteration. When the flow balance is within 0.0001,
        FlowBalance=0   # the loop will terminate.
        InternalPressure=InternalPressure+X
        for K in range(N):
            O= TotalExternalPressure[K] - InternalPressure
            if O==0:
                FlowRate[K] = 0
                continue
            FlowRate[K] = FlowCoefficient[K] * abs(O)**FlowExponent[K] * O/abs(O)
            FlowBalance=FlowBalance+FlowRate[K]
        if FlowBalance<0:
            InternalPressure=InternalPressure-X
            X=X/2
            continue
        if FlowBalance<0.0001:
            break
    
    InfiltrationRate=0
    for L in range(N):
        if (FlowRate[L]>0):
            InfiltrationRate=InfiltrationRate+FlowRate[L]

    print("Infiltration Rate = %.5f m^3/s" %InfiltrationRate)
    AirChangeRate=InfiltrationRate*3600/Volume
    print("Air Change Rate = %.5f per hour\n" %AirChangeRate)
    print("y: Continue\nn: Stop")
    answer=input()
    if(answer=='n' or 'N'):
        break