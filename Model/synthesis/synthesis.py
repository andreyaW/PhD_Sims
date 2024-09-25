'''
Simple vessel synthesis model to help understand the impact of differing
machinery architectures.  

Resistance code is adapted from an older project, and is based on the NPL series
'''


import numpy as np
from scipy.interpolate import Rbf
from scipy.interpolate import CubicSpline
import math as math
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import minimize

class EvalVessel:


    def __init__(self, cargoMass, MissionRoundTripLength, transit_speed, detailed_output=False):

        #Constants in one place
        self.number_bulkheads = 3
        self.rho = 1025 #kg/m^3
        self.g = 9.81 #m/s^2
        self.rho_air = 1.225 #kg/m^3 Air density
        self.nu = 1.1831 * 10.**(-6)      #Kinematic viscosity of SW, 15C
        self.cargoMass = cargoMass #kg
        self.MissionRoundTripLength = MissionRoundTripLength #nautical miles
        self.transit_speed = transit_speed #knots

        self.detailed_output = detailed_output

        #Pre-load the resistance data for the interpolation
        self.res_data = np.genfromtxt("Model/synthesis/Molland_NPL_Data_NumpyRead.csv",delimiter=",")
        #The first column is the Lvol
        self.Lvol = self.res_data[0,1:]

        #The second columns are the b/t 
        self.BT = self.res_data[1,1:]
        
        #Then we need the number of speeds remembering two header rows
        self.numspeed_tested = self.res_data.shape[0]-2

        #Get the engine table.  Engines are given by model number, weight(kg), power (kw), fuel consumption (g)kwh) Use pandas for this as we have string names
        self.engine_table = pd.read_csv("Model/synthesis/engines.csv",delimiter=",")

        #Sort the engines by power so it is ascending
        self.engine_table = self.engine_table.sort_values(by='power kw')

        print(self.engine_table)

        #Basic gearbox weight data from Reintjes WAF/LAF 164-573 series and LAF 665-1173
        gearbox_power = [0., 350., 450., 650., 750., 950., 1150., 1800. , 2600.]
        gearbox_wt = [0., 475., 650., 740., 940., 2190., 2450., 3000., 3850. ]

        #Make a spline of the gearbox weight
        self.gearbox_inter = CubicSpline(gearbox_power, gearbox_wt)



    def StructuralWeights(self, L, B, T, Cb):
        '''
        Based on the Grubisic 2009/2012 papers, rough structural weight esimate

        Inputs:
        L - length (m)
        B - breadth (m)
        T   - draft (m)
        Cb - block coefficient
        '''
        
        Disp = (self.rho/1000)*Cb*L*B*T #metric tonnes

        # Approximate depth based on draft, eqn from Grubisic 2012
        D = (2.493)*math.pow(T,0.582)  

        # estimate surface areas
        S1 = 2.825*math.sqrt((Disp/self.rho)*L) #bottom
        S2 = 1.09*(2*(L+B))*(D-T) #sides
        S3 = 0.823*L*B #deck
        S4 = 0.6*self.number_bulkheads*B*D #Bulkheads

        SR = S1 + (0.73*S2) + (0.69*S3) + (0.65*S4) #total reduced surface area  

        # correction factors
        DispLR = 0.125*((L*L)-15.8) #tonnes
        nabla = (DispLR + Disp)/self.rho
        fdis = 0.7 + (2.4*(nabla/((L*L)-15.8)))
        CTD = 1.144*math.pow((T/(D+0.0001)),0.244) #modified to prevent a divide by zero

        # structural numeral
        Es = fdis*CTD*SR # meters^2
        
        # service type and weight constant
        Gf = 1.20 #for patrol craft
        Sf = 1.25 #for unrestricted service
        K = 0.002 + (0.0064*Gf*Sf) # weight constant for aluminium hull

        # structural weights
        W100 = K*math.pow(Es,1.33)*1000.  #kilograms 

        if(self.detailed_output):
            print("Structural weight is " + str(W100) + " kilograms")

        return W100


    def plot_model(model, Lvol, BT, crvals, currLv, currBt, vk):
        '''
        Utility function to plot the resistance interplation model
        when checking runs
        '''
        Lvols = np.linspace(np.min(Lvol), np.max(Lvol), 101)
        BTs = np.linspace(np.min(BT), np.max(BT), 101)
        
        # full coorindate arrays
        pltLV, pltBT = np.meshgrid(Lvols, BTs)
        
        #Generate the interpolation
        pltCr = model(pltLV, pltBT)
        
        #Do the plot
        plt.figure(figsize=(6,4)) 
        img = plt.contourf(pltLV, pltBT, pltCr)
        plt.scatter(Lvol, BT, c='k', label="Exp. data points")
        plt.scatter(currLv, currBt, c='r', label="Current eval. pt")
        plt.colorbar(img)
        plt.xlabel(r'$\frac{L}{\nabla^{1/3}}$')
        plt.ylabel(r'$\frac{B}{T}$')
        plt.legend()
        plt.title("Contours of CR x 1000 from RBF at speed of " + str(round(vk,2)) + " knots")
        filename = "check_regression_" + str(round(vk,2)) + ".png"
        plt.savefig(filename)
        plt.close()



    def FindResistance(self, L, B, T, Cb, WettedSurface=-1, Cair=0, Windage_Area=0 , CA=0, debug=False):
        '''
        Uses a modified NPL series to estimate resistance
        
        Inputs:
        L - length (m)
        B - breadth (m)
        T   - draft (m)
        Cb - block coefficient
        Surface Area - m^2
        V - speed (knots) - vector of speeds to evaluate

        Returns:
        Tuple: Min speed, Max speed, Scipy cubic spline interpolator. All in knots/kN of resistance
        
        Returns a Scipy cubic spline interpolation of the resistance vs. speed, using the full range of data available from the NPL 
        series experiments.   Internally, a Scipy RBF regression model is built of each tested speed, and the target's vessel dimensions are used to estimate wave drag. ITTC 1957 friction drag is added, along with air drag and correlation drag, both of which default to zero if input not provided.  
        '''

        #Calculate the overall coefficients
        Vol = L*B*T*Cb
        L_vol = L/(Vol**(1.0/3.0))
        BT = B/T

        #If no wetted surface is provided, use the Denny-Mumford appoximation
        if WettedSurface == -1:
            WettedSurface = 1.7*L*T + Vol/T

        #Model loop - build a RBF at each speed the models were tested at, and find the Cr for that speed.  This will then be splined to interpolate at the target speed value. This avoids building a single model over the entire data set, which has differing number of features/points at each speed.  This loop is barely started!
        output = np.zeros((self.numspeed_tested,10))

        #Skipping header rows.
        for k in range(2, self.numspeed_tested+2):
            i = k - 2
            
            #Do speed
            output[i,0] = self.res_data[k,0]                #Old Vk/sqrt(Lf) ratio
            Vk = self.res_data[k,0] * (L * 3.28084)**(0.5)  #Get speed in kts
            Vms = Vk*6076.0/3600.0*0.3048          #Speed in meters per second
            output[i,2] = Vk
            output[i,1] = Vms/((self.g*L)**(0.5))  #Modern froude number
            
            #Do an RBF 
            crvals = self.res_data[k,1:]
            #We have to work around the missing data - lowest L/Vol^(1/3) not tested at higher speeds
            if self.res_data[k,0] < 3.3:
                LvolUse = self.Lvol
                BTUse = self.BT
                crvalsUse = crvals
            else:
                LvolUse = self.Lvol[3:] 
                BTUse = self.BT[3:] 
                crvalsUse = crvals[3:]
            interpol = Rbf(LvolUse, BTUse, crvalsUse)
            Cr = interpol(L_vol, BT)/1000.  #Raw data was x1000 in textbook
            output[i,3] = Cr
            
            #If checking the regression, do a contour plot
            if debug:
                self.plot_model(interpol, LvolUse, BTUse, crvalsUse, Lvol, BT, Vk)
            
            #Calculate ITTC 1957 friction line
            Rn = Vms*L/self.nu
            Cf = 0.075/((math.log10(Rn) -  2.0)**(2.0))
            output[i,4] = Cf
            output[i,5] = CA
            
            #Total hydro drag
            Ct = Cr + Cf + CA
            output[i,6] = Ct
            Rt_hydro = Ct* 0.5 * self.rho * WettedSurface * Vms**2.0/1000.  #in Kn
            output[i,7] = Rt_hydro
            
            #Do air drag
            R_air = Cair * 0.5 * Windage_Area *self.rho_air * Vms**2.0/1000.  #in Kn
            output[i,8] = R_air
            output[i,9] = R_air + Rt_hydro

        #If deugging, dump the full output
        if self.detailed_output:
            print('''Vk/(LF)^0.5    Fn         V          Cr         Cf         Ca         Ct         R_Hydro    R_Air     R_Total ''')
            print('''                          (kts)                                                  (kN)       (kN)      (kN)    ''')
            np.set_printoptions(linewidth=130)   
            np.set_printoptions(formatter={'float': '{: 10.5f}'.format})
            for row in output:
                print(row)
        
        #Make the spline
        spline_inter = CubicSpline(output[:,2], output[:,9])
        min_speed = output[0,2]
        max_speed = output[-1,2]

        return min_speed, max_speed, spline_inter
    

    
    def FindRightEngines(self, numEngines, rt, seamargin=1.2):
        '''
        This function needs to find the propulsion wt, given the resitance and
        whatever redundency is specified.  It will also return the fuel weight
        as that calculation uses many of the same variables.

        Inputs:
            numEngines - number of engines
            rt - total resistance in kN
            seamargin - added factor for waves on top of resistance

        Outputs:
            Engine index from the engine table that fits the power requirements
        '''

        #Get transit speed in m/s
        Vms = self.transit_speed*6076.0/3600.0*0.3048

        #Effective power per engine
        effectivePowerPerEngine = rt*seamargin*Vms/numEngines #kW, as rt is in kN already

        #Find the right engine
        row_engine = self.engine_table[(self.engine_table['power kw'] > effectivePowerPerEngine)].index[0]
        
        if self.detailed_output:
            print("Effective power per engine is " + str(effectivePowerPerEngine) + " kilowatts")
            print("Selected engine is " + self.engine_table.loc[row_engine,'Name'])
        
        #Fuel consumption makes sense to be done here 
        fuel_burn_kg_hr = self.engine_table.loc[row_engine,'sfc g/kw*hr']*effectivePowerPerEngine/1000.0 #kg/hr
        total_fuel_wt = self.MissionRoundTripLength/self.transit_speed*fuel_burn_kg_hr*numEngines #kg

        return (row_engine, total_fuel_wt)
    
    def FindShaftWt(self, power):
        '''
        This function needs to find the shafting weight, given the length and power, using ABYC standards
        with a safety factor of 10. AquaMet 19 steel is assumed, along with a 3m shaft length

        Inputs:
            power - power in KW
        
        Outputs:
            shaft weight in kg
        '''

        PowerHP = power*1.34102     #convert from KW to HP
        ShaftRPM = 300              #Assumed for a higher-speed prop
        ShaftTorsional = 36000      #Torsional yield, up to 3" diameter, in psi AquaMet 19 steel
        SafetyFactor = 10           #ABYC standard
        MaterialDensity = 7930.0    #kg/m^3, AquaMet 19 steel
        AssumedLength  = 3.0        #Assumed length in meters

        ShaftDiaInches = (321000. * PowerHP * SafetyFactor/(ShaftTorsional*ShaftRPM))**(1./3.)

        ShaftDiaMeters = ShaftDiaInches*0.0254

        ShaftWt  = math.pi*(ShaftDiaMeters/2.0)**2.0*AssumedLength*MaterialDensity

        if self.detailed_output:
            print("Shaft diameters is " + str(ShaftDiaMeters*1000.) + "millimeters")

        return ShaftWt



    def FindPropulsionWt(self, numEngines, rt, seamargin=1.2, extras=1):
        '''
        This function needs to find the propulsion wt, given the resitance and
        '''

        engine_selection, fuel_wt  = self.FindRightEngines(numEngines, rt, seamargin)

        #Engine weight is dry wt from manufacture, Grubisic 2008 recommends 1.066 to get to wet weight
        engine_wt = self.engine_table.loc[engine_selection,'wt kg']*1.066*numEngines

        #This is highly! approximate.  We need to do a better job of this.
        #Idea is to approximate redundant pumps, filters etc. as a percentage of the engine weight
        
        # estimating fraction for other machinery weight
        # added 5 % for the first redundandt system and 1% for the any extras after that
        if extras > 2:
            wt_1st_extra = 0.05*engine_wt
            wt_other_extras = (extras-2)*0.05*engine_wt*0.7
            wt_extras = wt_1st_extra + wt_other_extras 
        else:
            wt_extras = (extras-1)*0.05*engine_wt
        
        #shaft weight 
        shaft_wt = self.FindShaftWt(self.engine_table.loc[engine_selection,'power kw'])*numEngines

        #Gearbox weight
        gearbox_wt  = self.gearbox_inter(self.engine_table.loc[engine_selection,'power kw'])

        #Other weights - this comes from Grubisic 2009. We don't have a good way of making this change with 
        #the level of redudency yet. 
        other_wt  = 1.6*(engine_wt + gearbox_wt)

        #Total machinery weight
        propulsion_wt = engine_wt + shaft_wt + gearbox_wt + other_wt + wt_extras

        # save variables to self for comparison
        self.prop_wt = propulsion_wt
        self.fuel_wt = fuel_wt

        if self.detailed_output:
            print("Engine weight is " + str(engine_wt) + " kilograms")
            print("Shaft weight is " + str(shaft_wt) + " kilograms")
            print("Gearbox weight is " + str(gearbox_wt) + " kilograms")
            print("Other machinery weight is " + str(other_wt) + " kilograms")
            print("Total propulsion weight is " + str(propulsion_wt) + " kilograms")
            print("Total fuel weight is " + str(fuel_wt) + " kilograms")

        return propulsion_wt, fuel_wt


    def EvalShip(self,L ,B, T, Cb, numEngines, extras):
        '''
        '''

        allowable_wt = L*B*T*Cb*self.rho   #kilgrams

        structural_wt = self.StructuralWeights(L,B,T,Cb)

        min_speed, max_speed, spline_inter = self.FindResistance(L,B,T,Cb)

        if (self.transit_speed < min_speed) or (self.transit_speed > max_speed):
            print("Warning: Transit speed is outside of the tested range of the resistance data")
            raise ValueError("Transit speed is outside of the tested range of the resistance data")
        
        #This comes back with the total resistance in kN against speed in kts 
        rt = spline_inter(self.transit_speed)

        prop_wt, fuel_wt  = self.FindPropulsionWt(numEngines, rt, 1.2, extras)

        #Do the balance
        mass_balance = allowable_wt - (structural_wt + prop_wt + fuel_wt + self.cargoMass)

        if self.detailed_output:
            print("Mass inbalance is " + str(mass_balance) + " kilograms")

        return mass_balance
    

    def FindBalancedShip(self, refL, refB, refT, Cb, numEngines, extras):
        '''
        makes a balanced ship by scaling up a given design until the mass balance comes out ok
        '''

        self.detailed_output = False

        #Make a hidden function that can be passed to an optimizer
        def hiddenEvalShip(scale):
            print(scale)
            if scale < 0:
                return 100000.*scale**2.0
            L = refL*scale
            B = refB*scale
            T = refT*scale
            
            self.L = L
            self.B = B
            self.T = T
            
            return (self.EvalShip(L,B,T,Cb,numEngines,extras))**2.0
            #return (self.EvalShip(L,B,T,Cb,numEngines,extras))**2.0, L , B ,T
        
        res = minimize(hiddenEvalShip, [1.], method='nelder-mead', options={'xatol': 1e-6, 'disp': True})

        print("Balanced scale is " + str(res.x[0]))

        self.detailed_output = True
        
        hiddenEvalShip(res.x[0])
        
        # __, L, B, T= hiddenEvalShip(res.x[0])
        # print(f"final parameters are  L:{L}, B:{B}, T:{T}")

        return res.x[0] 

# testCase = EvalVessel(10000., 500., 20.)
# testCase.FindBalancedShip(10, 1.5, 1., 0.6, 2, 1)
# # testCase.FindBalancedShip(10, 1.5, 1., 0.6, 2, 2)



##----------------- AMTS TESTING -----------------##

# Small Vessel- similar to US Navy patrol boats
AMTS_test_vessel = EvalVessel(5000., 1000., 25., False) # cargoMass - #kg , MissionRoundTripLength - #nm, transit_speed- #knots, detailed_output=False
prop_weight = []
fuel_weight = []
vessel_sizes = np.empty((0,3))

# Small Vessel 1 - 2 engines 1 system each
AMTS_test_vessel.FindBalancedShip(25., 5., 2, 0.6, 2, 1) 
prop_weight.append(AMTS_test_vessel.prop_wt)
fuel_weight.append(AMTS_test_vessel.fuel_wt)
vessel_sizes = np.append(vessel_sizes, np.array([[AMTS_test_vessel.L, AMTS_test_vessel.B, AMTS_test_vessel.T]]) , axis=0)

# Small Vessel 2 - 2 engines 2 system each
AMTS_test_vessel.FindBalancedShip(25., 5., 2, 0.6, 2, 2) # Vessel 2 - 2 engines 2 systems each
prop_weight.append(AMTS_test_vessel.prop_wt)
fuel_weight.append(AMTS_test_vessel.fuel_wt)
vessel_sizes = np.append(vessel_sizes, np.array([[AMTS_test_vessel.L, AMTS_test_vessel.B, AMTS_test_vessel.T]]) , axis=0)

# Small Vessel 3 - 2 engines 3 system each
AMTS_test_vessel.FindBalancedShip(25., 5., 2, 0.6, 2, 3) # Vessel 2 - 2 engines 2 systems each
prop_weight.append(AMTS_test_vessel.prop_wt)
fuel_weight.append(AMTS_test_vessel.fuel_wt)
vessel_sizes = np.append(vessel_sizes, np.array([[AMTS_test_vessel.L, AMTS_test_vessel.B, AMTS_test_vessel.T]]) , axis=0)

# Store differences in designs
prop_wt_increase_sv= [((prop_weight[1]- prop_weight[0])/prop_weight[0])*100 , ((prop_weight[2]- prop_weight[0])/prop_weight[0])*100]
fuel_wt_increase_sv= [((fuel_weight[1]- fuel_weight[0])/fuel_weight[0])*100 , ((fuel_weight[2]- fuel_weight[0])/fuel_weight[0])*100]
vessel_size_diff_sv= [((vessel_sizes[1][:]- vessel_sizes[0][:])/vessel_sizes[0][:])*100, ((vessel_sizes[2][:]- vessel_sizes[0][:])/vessel_sizes[0][:])*100 ]



# Large Vessel- similar to US Navy small logistics boats
AMTS_test_vessel = EvalVessel(10000., 10000., 25., False) # cargoMass - #kg , MissionRoundTripLength - #nm, transit_speed- #knots, detailed_output=False
prop_weight = []
fuel_weight = []
vessel_sizes = np.empty((0,3))

# Large Vessel 1 - 2 engines 1 system each
AMTS_test_vessel.FindBalancedShip(120, 20., 3., 0.3, 2, 1)
prop_weight.append(AMTS_test_vessel.prop_wt)
fuel_weight.append(AMTS_test_vessel.fuel_wt)
vessel_sizes = np.append(vessel_sizes, np.array([[AMTS_test_vessel.L, AMTS_test_vessel.B, AMTS_test_vessel.T]]) , axis=0)

# Large Vessel 2 - 2 engines 2 system each
AMTS_test_vessel.FindBalancedShip(120, 20., 3., 0.3, 2, 2) # Vessel 2 - 2 engines 2 systems each
prop_weight.append(AMTS_test_vessel.prop_wt)
fuel_weight.append(AMTS_test_vessel.fuel_wt)
vessel_sizes = np.append(vessel_sizes, np.array([[AMTS_test_vessel.L, AMTS_test_vessel.B, AMTS_test_vessel.T]]) , axis=0)

# Large Vessel 3 - 2 engines 3 system each
AMTS_test_vessel.FindBalancedShip(120, 20., 3., 0.3, 2, 3) # Vessel 2 - 2 engines 2 systems each
prop_weight.append(AMTS_test_vessel.prop_wt)
fuel_weight.append(AMTS_test_vessel.fuel_wt)
vessel_sizes = np.append(vessel_sizes, np.array([[AMTS_test_vessel.L, AMTS_test_vessel.B, AMTS_test_vessel.T]]) , axis=0)

# store differences in designs
prop_wt_increase_lv = [((prop_weight[1]- prop_weight[0])/prop_weight[0])*100 , ((prop_weight[2]- prop_weight[0])/prop_weight[0])*100]
fuel_wt_increase_lv = [((fuel_weight[1]- fuel_weight[0])/fuel_weight[0])*100 , ((fuel_weight[2]- fuel_weight[0])/fuel_weight[0])*100]
vessel_size_diff_lv = [((vessel_sizes[1][:]- vessel_sizes[0][:])/vessel_sizes[0][:])*100, ((vessel_sizes[2][:]- vessel_sizes[0][:])/vessel_sizes[0][:])*100 ]


# Print Results 
# Small Vessel (sv) Results 
print(f"\n SMALL SHIP RESULT")
print(f"The increase in propulsion weight between designs 1 to 2 is {prop_wt_increase_sv[0]:.2f}% and between 1 and 3 is {prop_wt_increase_sv[1]:.2f}%")
print(f"The increase in fuel weight between designs 1 to 2 is {fuel_wt_increase_sv[0]:.2f}% and between 1 and 3 is {fuel_wt_increase_sv[1]:.2f}%")
print(f"The increase in ship dimensions (L,B,T) between designs 1 to 2 is {vessel_size_diff_sv[0][0]:.2f}%, {vessel_size_diff_sv[0][1]:.2f}%, {vessel_size_diff_sv[0][2]:.2f}%" + 
      f" and between 1 and 3 is {vessel_size_diff_sv[1][0]:.2f}%, {vessel_size_diff_sv[1][1]:.2f}%, {vessel_size_diff_sv[1][2]:.2f}%  \n")
print("\n")

# Large Vessel (sv) Results 
print(f"\n LARGE SHIP RESULT")
print(f"The increase in propulsion weight between designs 1 to 2 is {prop_wt_increase_lv[0]:.2f}% and between 1 and 3 is {prop_wt_increase_lv[1]:.2f}%")
print(f"The increase in fuel weight between designs 1 to 2 is {fuel_wt_increase_lv[0]:.2f}% and between 1 and 3 is {fuel_wt_increase_lv[1]:.2f}%")
print(f"The increase in ship dimensions (L,B,T) between designs 1 to 2 is {vessel_size_diff_lv[0][0]:.2f}%, {vessel_size_diff_lv[0][1]:.2f}%, {vessel_size_diff_lv[0][2]:.2f}%" + 
      f" and between 1 and 3 is {vessel_size_diff_lv[1][0]:.2f}%, {vessel_size_diff_lv[1][1]:.2f}%, {vessel_size_diff_lv[1][2]:.2f}%  \n")
print("\n")



# AMTS_test_vessel.FindBalancedShip(120, 20., 3., 0.3, 2, 1)

# AMTS_test_vessel.FindBalancedShip(120, 20., 2., 0.8, 2, 1) # Vessel 1 - 2 engines 1 system each
# AMTS_test_vessel.FindBalancedShip(50, 10., 2., 0.6, 2, 2) # Vessel 1 - 2 engines 1 system each

