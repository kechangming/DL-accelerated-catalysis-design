# -*- coding: utf-8 -*-
"""
Created on Mon Jul 12 14:26:51 2021

@author: rulaishenzhang
"""

from scipy.optimize import root,fsolve
import numpy as np
import scipy.io as sio

R=8.314E-3

def MSRrate_func(x,*args):
        P_total=float(args[0])
        T=float(args[1])
        Vin=float(args[2])
        surface=float(args[3])
        PCH3OH_in=float(args[4])
        PH2O_in=float(args[5])
        PH2_in=float(args[6])
        eF = float(args[7])
        PCH3OH_out=float(x[0])
        PH2O_out=float(x[1])
        PH2_out=float(x[2])
        PCO_out=float(x[3])
        PCO2_out=float(x[4])
        Vout=float(x[5])

        R = 8.314E-3
        A = 5.95E17*T**-6.87   # mol/sqrt(kPa)/s/cm^2
        ACO = 2.56E-14*T**1.19  #  
        AO = 2.67E+17*T**-6.46
        ACO_O = 1.79E+13*T**0.09
        D_CH3O = 0.22
        D_CO = -0.18
        D_CO_O = -0.01
        D_CO2 = -0.02
        W_CH3O = 0.156
        W_CO = 0.096
        W_CO_O = -0.0275
        W_CO2 = 0.045
        detaE_CH3O = (-D_CH3O*eF-1/2*W_CH3O*eF**2.0)*96.1538
        detaE_CO = (-D_CO*eF-1/2*W_CO*eF**2.0)*96.1538
        detaE_CO_O = (-D_CO_O*eF-1/2*W_CO_O*eF**2.0)*96.1538
        detaE_CO2 = (-D_CO2*eF-1/2*W_CO2*eF**2.0)*96.1538

        E_CO = (0.5254*EC+1.927)*96.1538
        E_CH3O_TS = (0.17*EC+0.36*EO-23.0044+1/2*-6.96+30.34)*96.1538
        E_CO_O_TS = (0.25*EC+0.825*EO-16.036-6.96+14.83+14.28+1.40)*96.1538
        E_CO2_TS = (0.25*EC+0.825*EO-16.036+23.02115)*96.1538
        
        sita=1/(1+ACO*np.exp(-(E_CO+detaE_CO)/R/T)*PCO_out+AO*np.exp(-(EO+5.6805)*96.1538/R/T)*PH2O_out/PH2_out)
        rCH3OH=A*np.exp(-(E_CH3O_TS+detaE_CH3O)/R/T)*PCH3OH_out/(PH2_out)**0.5*sita**2.0
        rCO2=ACO_O*3.09E-9*np.exp(-(E_CO_O_TS+detaE_CO_O)/R/T)*ACO*PCO_out*sita*AO*PH2O_out/PH2_out*sita-3.09E-9*1.77E10*T**0.76*np.exp(-(E_CO2_TS+detaE_CO2)/R/T)*1.36E-5*T**-0.56*PCO2_out*sita*sita
        
        return [PCH3OH_in/P_total*Vin-PCH3OH_out/P_total*Vout-rCH3OH*surface,
                        (rCH3OH-rCO2)*surface-PCO_out/P_total*Vout,
                        PCH3OH_in*Vin-(PCH3OH_out+PCO_out+PCO2_out)*Vout,
                        (PH2_in+PH2O_in+2*PCH3OH_in)*Vin-(2*PCH3OH_out+PH2O_out+PH2_out)*Vout,
                        PH2O_in*Vin-(PCO_out+2*PCO2_out+PH2O_out)*Vout,
                        PH2O_out+PCO_out+PCO2_out+PH2_out+PCH3OH_out-P_total]


surface = 0.14E4*100# cm^2
PH2_in = 0   #kPa
PH2O_in = 66.66    #kPa
PCH3OH = 33.33  #kPa
P_total = 100 #kPa
Vin = 7.44E-6*100 # mol/s
T = 523
#initial = [25, 10, 5.0, 0.054, 0.924, 0.0008, 0.1] # PCH3OH, PH2, PCO, PCO2, Vout, sitaO
initial = [20.04,5,59,0.058,0.92,0.001]
save_matrix=[]
for EO in np.arange(-6.0,-4.5,0.1):
    for EC in np.arange(-6,-4.5,0.1):
        for eF in np.arange(-0.6,0.7,0.1):
            result=root(MSRrate_func,initial,method='lm',args=(P_total,T,Vin,surface,PCH3OH,PH2O_in,PH2_in,eF,EC,EO),tol=1E-10)
            x=result["x"]
            CH3OH_conv=(33.33-x[0])/33.33
            if CH3OH_conv < 0 or x[1] < 0 or x[2] < 0 or x[3] < 0 or x[4] < 0 or x[5] < 0 and CH3OH_conv >1 or str(result["success"])=='False':
                CH3OH_conv=-100
                save_matrix.append([EC,EO,eF,CH3OH_conv])
            else:
                save_matrix.append([EC,EO,eF,CH3OH_conv])
mat_len=len(save_matrix)
for initial in [[50,50,1,0.058,0.92,0.001],[44,44,9.1,3.04,1.3E-7,0.0008],[20,20,60,3.04,1.3E-7,0.0008],[2,2,80,3.04,1E-7,0.0008]]:
    for EO in np.arange(-6.0,-4.,0.1):
        for EC in np.arange(-6,-4.5,0.1):
            for eF in np.arange(-0.6,0.7,0.1):
                result=root(MSRrate_func,initial,method='lm',args=(P_total,T,Vin,surface,PCH3OH,PH2O_in,PH2_in,eF,EC,EO),tol=1E-10)
                x=result["x"]
                CH3OH_conv=(50-x[0])/50
                if CH3OH_conv < 0 or x[1] < 0 or x[2] < 0 or x[3] < 0 or x[4] < 0 or x[5] < 0 and CH3OH_conv >1 or str(result["success"])=='False':
                    xx=0
                else:
                    for i in np.arange(mat_len):
                        if save_matrix[i][0] == EC and save_matrix[i][1] == EO and save_matrix[i][2] == eF and CH3OH_conv > 0:
                            save_matrix[i][3] = CH3OH_conv
np.savetxt('newn_T523K.csv', save_matrix,delimiter=',')