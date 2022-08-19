from scipy.optimize import root,fsolve
import numpy as np

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
        D_CO = -0.26
        D_CO_O = -0.25
        D_CO2 = -0.25
        W_CH3O = 0.135
        W_CO = 0.096
        W_CO_O = 0.151
        W_CO2 = 0.151
        detaE_CH3O = (-D_CH3O*eF-1/2*W_CH3O*eF**2.0)*96.1538
        detaE_CO = (-D_CO*eF-1/2*W_CO*eF**2.0)*96.1538
        detaE_CO_O = (-D_CO_O*eF-1/2*W_CO_O*eF**2.0)*96.1538
        detaE_CO2 = (-D_CO2*eF-1/2*W_CO2*eF**2.0)*96.1538
        sita=1/(1+ACO*np.exp(-(-184.3+detaE_CO)/R/T)*PCO_out+AO*np.exp(-(-5.72)/R/T)*PH2O_out/PH2_out)
        rCH3OH=A*np.exp(-(51.1-detaE_CH3O)/R/T)*PCH3OH_out/(PH2_out)**0.5*sita**2.0
        rCO2=ACO_O*3.09E-9*np.exp(-(134.8+detaE_CO_O)/R/T)*ACO*np.exp(-(-184.3)/R/T)*PCO_out*sita*AO*np.exp(-(-5.72)/R/T)*PH2O_out/PH2_out*sita-3.09E-9*1.77E10*T**0.76*np.exp(-(38.2+detaE_CO2)/R/T)*1.36E-5*T**-0.56*np.exp(-5.34/R/T)*PCO2_out*sita*sita
        
        return [PCH3OH_in/P_total*Vin-PCH3OH_out/P_total*Vout-rCH3OH*surface,
                        (rCH3OH-rCO2)*surface-PCO_out/P_total*Vout,
                        PCH3OH_in*Vin-(PCH3OH_out+PCO_out+PCO2_out)*Vout,
                        (PH2_in+PH2O_in+2*PCH3OH_in)*Vin-(2*PCH3OH_out+PH2O_out+PH2_out)*Vout,
                        (PH2O_in+PCH3OH_in)*Vin-(PCO_out+2*PCO2_out+PH2O_out+PCH3OH_out)*Vout,
                        PH2O_out+PCO_out+PCO2_out+PH2_out+PCH3OH_out-P_total]



surface = 0.14E4 # cm^2
PH2_in = 1E-6   #kPa
PH2O_in = 75    #kPa
PCH3OH = 25   #kPa
P_total = 100 #kPa
Vin =        7.44E-6  # mol/s
for eF in [-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4]:
    print("EF="+str(eF))
    for T in [473,498,523,548,573,598,623,648,673]:
            result=root(MSRrate_func,[15,20,15,2E-7,10,Vin],method='lm',args=(P_total,T,Vin,surface,PCH3OH,PH2O_in,PH2_in,eF),tol=1E-9,options={"maxiter":1000000})
            x=result["x"]
            CH3OH_conv=(25-x[0])/25*100
            print(str(CH3OH_conv)+" "+str(x[1])+" "+str(x[2])+" "+str(x[3])+" "+str(x[4])+" "+str(x[5])+str(result["success"]))

