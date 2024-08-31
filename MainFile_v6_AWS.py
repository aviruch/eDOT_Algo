#!/usr/bin/python
import math
import re
import sys
import os
import time
#import BeautifulSoup
import linecache
#from myconfig import *
# Sytesm Argument must be in order AREA, Weatherfile, Orientation, OVerhang, WWR, AR, U-value glass, SHGC, and VLT
print sys.argv

print sys.argv[0],sys.argv[1]
# #### define static params ######
# Area=1000.0;
Area=float(sys.argv[1])
Height=3.0;
# WeatherFile = "IND_Ahmedabad.426470_ISHRAE.epw"
WeatherFile = str(sys.argv[2])
BuildingType = str(sys.argv[3])
HVAC_Type = str(sys.argv[4])
DaylightCtrl = str(sys.argv[5])
CoolRoof = str(sys.argv[6])
ShadingCtrl = str(sys.argv[7])
Floors = int(sys.argv[8])
WindowType = str(sys.argv[9])
# #### define dynamic params ######
# Orientation = 45
Wwr = float(sys.argv[10])

WindowHeight = float(sys.argv[11])
SilHeight= float(sys.argv[12])
WindowWidthP=float(sys.argv[13])



# #Glass
# U_value = 3.1
# Shgc = 0.3
# Vlt = 0.5# U_value = 3.1
# Shgc = 0.3
# Vlt = 0.5
U_value = float(sys.argv[14])
Shgc = float(sys.argv[15])
Vlt = float(sys.argv[16])


Orientation = float(sys.argv[17])
# Overhang = 5
Overhang = float(sys.argv[18])
# Wwr = 0.4

# Aspect_Ratio = 2
Aspect_Ratio = float(sys.argv[20])

zonemultiplier = Floors - 2;


print ("AREA, Weatherfile, Orientation, OVerhang, WWR, AR, U-value glass, SHGC, and VLT")

print (Area, WeatherFile, Orientation, Overhang, Wwr, Aspect_Ratio, U_value, Shgc,Vlt)


# #cost fixed as of now
cost_glass = 5000
glass=(Shgc,Vlt,U_value,cost_glass)
# #glass=(0.1, 0.175, 3.1, 5000.0)


def generate_co(Orientation,Area,Ar,Wwr,glass,Overhang):
	
	#STRUCTURAL REPRESENTATION

	P = 3.0; #Perimeter
	H = 3.0;  #Floor to  floor height



	### Independent Params ###

	W = math.sqrt(Area/Ar);
	L = W*Ar ; 

	## Derived Vars ##


	North_Wall_Area	= L*H
	South_Wall_Area	= L*H
	East_Wall_Area	= W*H
	West_Wall_Area	= W*H
	
	North_Win_area	= Wwr*L*H
	South_Win_area	= Wwr*L*H
	East_Win_area	= Wwr*W*H
	West_Win_area	= Wwr*W*H






	# DICTIONARY REPRESENTATION 

	RQ_VAL={};
	
	#RQ_VAL['#ORIENTATION'] = Orientation
	#RQ_VAL['#GLASS_U_FACTOR'] = glass[2]
	#RQ_VAL['#GLASS_SHGC'] = glass[0]
	#RQ_VAL['#GLASS_VT'] =  glass[1]	
	#RQ_VAL['#GLASS_COST'] = glass[3]

	RQ_VAL['###ORIENT'] = Orientation 
	RQ_VAL['###GLASS_U_FACTOR'] =  glass[2]
	RQ_VAL['###GLASS_SHGC'] =  glass[0]
	RQ_VAL['###GLASS_VT'] =  glass[1]
	RQ_VAL['###Glass_Cost'] = glass[3] 
	
	RQ_VAL['###Z_2_X'] =  L-P
	RQ_VAL['###Z_2_Y'] =  P
	RQ_VAL['###Z_3_X'] =  P
	RQ_VAL['###Z_3_Y'] =  W-P
	RQ_VAL['###Z_C_X'] =  P
	RQ_VAL['###Z_C_Y'] =  P
	
# Roof coordinates	
	RQ_VAL['###Z_1_R_1_X'] =  0
	RQ_VAL['###Z_1_R_1_Y'] =  0
	RQ_VAL['###Z_1_R_1_Z'] =  H
	RQ_VAL['###Z_1_R_1_Z_1'] =  H
	RQ_VAL['###Z_1_R_2_X'] =  L
	RQ_VAL['###Z_1_R_2_Y'] =  0
	RQ_VAL['###Z_1_R_2_Z'] =  H
	RQ_VAL['###Z_1_R_2_Z_1'] =  H
	
	RQ_VAL['###Z_1_R_3_X'] =  L-P
	RQ_VAL['###Z_1_R_3_Y'] =  P
	RQ_VAL['###Z_1_R_3_Z'] =  H
	RQ_VAL['###Z_1_R_3_Z_1'] =  H
	
	
	RQ_VAL['###Z_1_R_4_X'] =  P
	RQ_VAL['###Z_1_R_4_Y'] =  P
	RQ_VAL['###Z_1_R_4_Z'] =  H
	RQ_VAL['###Z_1_R_4_Z_1'] =  H
	
	
	RQ_VAL['###Z_2_R_1_X'] =  0
	RQ_VAL['###Z_2_R_1_Y'] =  0
	RQ_VAL['###Z_2_R_1_Z'] =  H
	RQ_VAL['###Z_2_R_1_Z_1'] =  H
	
	RQ_VAL['###Z_2_R_2_X'] =  P
	RQ_VAL['###Z_2_R_2_Y'] =  - P
	RQ_VAL['###Z_2_R_2_Z'] =  H
	RQ_VAL['###Z_2_R_2_Z_1'] =  H
	
	RQ_VAL['###Z_2_R_3_X'] =  P
	RQ_VAL['###Z_2_R_3_Y'] =  W-P
	RQ_VAL['###Z_2_R_3_Z'] =  H
	RQ_VAL['###Z_2_R_3_Z_1'] =  H
	
	RQ_VAL['###Z_2_R_4_X'] =  0
	RQ_VAL['###Z_2_R_4_Y'] =  W-2*P
	RQ_VAL['###Z_2_R_4_Z'] =  H
	RQ_VAL['###Z_2_R_4_Z_1'] =  H
	
	
	RQ_VAL['###Z_3_R_1_X'] =  0
	RQ_VAL['###Z_3_R_1_Y'] =  0
	RQ_VAL['###Z_3_R_1_Z'] =  H
	RQ_VAL['###Z_3_R_1_Z_1'] =  H
	
	RQ_VAL['###Z_3_R_2_X'] =  L-2*P
	RQ_VAL['###Z_3_R_2_Y'] =  0
	RQ_VAL['###Z_3_R_2_Z'] =  H
	RQ_VAL['###Z_3_R_2_Z_1'] =  H
	
	RQ_VAL['###Z_3_R_3_X'] =  L-P
	RQ_VAL['###Z_3_R_3_Y'] =  P
	RQ_VAL['###Z_3_R_3_Z'] =  H
	RQ_VAL['###Z_3_R_3_Z_1'] =  H
	
	RQ_VAL['###Z_3_R_4_X'] =  - P
	RQ_VAL['###Z_3_R_4_Y'] =  P
	RQ_VAL['###Z_3_R_4_Z'] =  H
	RQ_VAL['###Z_3_R_4_Z_1'] =  H
	
	RQ_VAL['###Z_4_R_1_X'] =  0
	RQ_VAL['###Z_4_R_1_Y'] =  0
	RQ_VAL['###Z_4_R_1_Z'] =  H
	RQ_VAL['###Z_4_R_1_Z_1'] =  H
	
	RQ_VAL['###Z_4_R_2_X'] =  P
	RQ_VAL['###Z_4_R_2_Y'] =  P
	RQ_VAL['###Z_4_R_2_Z'] =  H
	RQ_VAL['###Z_4_R_2_Z_1'] =  H
	
	RQ_VAL['###Z_4_R_3_X'] =  P
	RQ_VAL['###Z_4_R_3_Y'] =  W-P
	RQ_VAL['###Z_4_R_3_Z'] =  H
	RQ_VAL['###Z_4_R_3_Z_1'] =  H
	
	RQ_VAL['###Z_4_R_4_X'] =  0
	RQ_VAL['###Z_4_R_4_Y'] =  W
	RQ_VAL['###Z_4_R_4_Z'] =  H
	RQ_VAL['###Z_4_R_4_Z_1'] =  H
	
# Floor Coordinates	
	RQ_VAL['###Z_1_F_1_X'] =  0
	RQ_VAL['###Z_1_F_1_Y'] =  0
	RQ_VAL['###Z_1_F_1_Z'] =  0
	RQ_VAL['###Z_1_F_1_Z_1'] =  0
	
	RQ_VAL['###Z_1_F_2_X'] =  P
	RQ_VAL['###Z_1_F_2_Y'] =  P
	RQ_VAL['###Z_1_F_2_Z'] =  0
	RQ_VAL['###Z_1_F_2_Z_1'] =  0
	
	RQ_VAL['###Z_1_F_3_X'] =  L-P
	RQ_VAL['###Z_1_F_3_Y'] =  P
	RQ_VAL['###Z_1_F_3_Z'] =  0
	RQ_VAL['###Z_1_F_3_Z_1'] =  0
	
	RQ_VAL['###Z_1_F_4_X'] =  L
	RQ_VAL['###Z_1_F_4_Y'] =  0
	RQ_VAL['###Z_1_F_4_Z'] =  0
	RQ_VAL['###Z_1_F_4_Z_1'] =  0
	
	RQ_VAL['###Z_2_F_1_X'] =  0
	RQ_VAL['###Z_2_F_1_Y'] =  0
	RQ_VAL['###Z_2_F_1_Z'] =  0
	RQ_VAL['###Z_2_F_1_Z_1'] =  0
	
	RQ_VAL['###Z_2_F_2_X'] =  0
	RQ_VAL['###Z_2_F_2_Y'] =  W-2*P
	RQ_VAL['###Z_2_F_2_Z'] =  0
	RQ_VAL['###Z_2_F_2_Z_1'] =  0
	
	RQ_VAL['###Z_2_F_3_X'] =  P
	RQ_VAL['###Z_2_F_3_Y'] =  W-P
	RQ_VAL['###Z_2_F_3_Z'] =  0
	RQ_VAL['###Z_2_F_3_Z_1'] =  0
	
	RQ_VAL['###Z_2_F_4_X'] =  P
	RQ_VAL['###Z_2_F_4_Y'] =  - P
	RQ_VAL['###Z_2_F_4_Z'] =  0
	RQ_VAL['###Z_2_F_4_Z_1'] =  0
	
	RQ_VAL['###Z_3_F_1_X'] =  0
	RQ_VAL['###Z_3_F_1_Y'] =  0
	RQ_VAL['###Z_3_F_1_Z'] =  0
	RQ_VAL['###Z_3_F_1_Z_1'] =  0
	
	RQ_VAL['###Z_3_F_2_X'] =  - P
	RQ_VAL['###Z_3_F_2_Y'] =  P
	RQ_VAL['###Z_3_F_2_Z'] =  0
	RQ_VAL['###Z_3_F_2_Z_1'] =  0
	
	RQ_VAL['###Z_3_F_3_X'] =  L-P
	RQ_VAL['###Z_3_F_3_Y'] =  P
	RQ_VAL['###Z_3_F_3_Z'] =  0
	RQ_VAL['###Z_3_F_3_Z_1'] =  0
	
	RQ_VAL['###Z_3_F_4_X'] =  L-2*P
	RQ_VAL['###Z_3_F_4_Y'] =  0
	RQ_VAL['###Z_3_F_4_Z'] =  0
	RQ_VAL['###Z_3_F_4_Z_1'] =  0
	
	RQ_VAL['###Z_4_F_1_X'] =  0
	RQ_VAL['###Z_4_F_1_Y'] =  0
	RQ_VAL['###Z_4_F_1_Z'] =  0
	RQ_VAL['###Z_4_F_1_Z_1'] = 0
	
	RQ_VAL['###Z_4_F_2_X'] =  0
	RQ_VAL['###Z_4_F_2_Y'] =  W
	RQ_VAL['###Z_4_F_2_Z'] =  0
	RQ_VAL['###Z_4_F_2_Z_1'] =  0
	
	RQ_VAL['###Z_4_F_3_X'] =  P
	RQ_VAL['###Z_4_F_3_Y'] =  W-P
	RQ_VAL['###Z_4_F_3_Z'] =  0
	RQ_VAL['###Z_4_F_3_Z_1'] =  0
	
	RQ_VAL['###Z_4_F_4_X'] =  P
	RQ_VAL['###Z_4_F_4_Y'] =  P
	RQ_VAL['###Z_4_F_4_Z'] =  0
	RQ_VAL['###Z_4_F_4_Z_1'] =  0
	
	RQ_VAL['###Z_3_ExWall_X'] =  L-P
	RQ_VAL['###Z_3_ExWall_Y'] =  P
	RQ_VAL['###Z_3_ExWall_Z'] =  0
	RQ_VAL['###Z_3_ExWall_Z_1'] =  0
	
	RQ_VAL['###Z_3_ExWall_L'] =  L
	RQ_VAL['###Z_3_ExWall_H'] =  H
	RQ_VAL['###Z_1_ExWall_X'] =  0
	RQ_VAL['###Z_1_ExWall_Y'] =  0
	RQ_VAL['###Z_1_ExWall_Z'] =  0
	RQ_VAL['###Z_1_ExWall_Z_1'] =  0
	
	
	RQ_VAL['###Z_1_ExWall_L'] =  L
	RQ_VAL['###Z_1_ExWall_H'] =  H
	RQ_VAL['###Z_2_ExWall_X'] =  P
	RQ_VAL['###Z_2_ExWall_Y'] =  - P
	RQ_VAL['###Z_2_ExWall_Z'] =  0
	RQ_VAL['###Z_2_ExWall_Z_1'] =  0
	
	
	RQ_VAL['###Z_2_ExWall_L'] =  W
	RQ_VAL['###Z_2_ExWall_H'] =  H
	RQ_VAL['###Z_4_ExWall_X'] =  0
	RQ_VAL['###Z_4_ExWall_Y'] =  W
	RQ_VAL['###Z_4_ExWall_Z'] =  0
	RQ_VAL['###Z_4_ExWall_Z_1'] =  0
	
	
	RQ_VAL['###Z_4_ExWall_L'] =  W
	RQ_VAL['###Z_4_ExWall_H'] =  H
	RQ_VAL['###Z_3_IntWall_S_X'] =  0
	RQ_VAL['###Z_3_IntWall_S_Y'] =  0
	RQ_VAL['###Z_3_IntWall_S_Z'] =  0
	RQ_VAL['###Z_3_IntWall_S_Z_1'] =  0
	
	RQ_VAL['###Z_3_IntWall_S_L'] =  L-2*P
	RQ_VAL['###Z_3_IntWall_S_H'] =  H
	RQ_VAL['###Z_3_IntWall_E_X'] =  L-2*P
	RQ_VAL['###Z_3_IntWall_E_Y'] =  0
	RQ_VAL['###Z_3_IntWall_E_Z'] =  0
	RQ_VAL['###Z_3_IntWall_E_Z_1'] =  0
	
	
	RQ_VAL['###Z_3_IntWall_E_L'] =  1.414*P
	RQ_VAL['###Z_3_IntWall_E_H'] =  H
	RQ_VAL['###Z_3_IntWall_W_X'] =  0
	RQ_VAL['###Z_3_IntWall_W_Y'] =  0
	RQ_VAL['###Z_3_IntWall_W_Z'] =  0
	RQ_VAL['###Z_3_IntWall_W_Z_1'] =  0
	
	RQ_VAL['###Z_3_IntWall_W_L'] =  1.414*P
	RQ_VAL['###Z_3_IntWall_W_H'] =  H
	RQ_VAL['###Z_1_IntWall_N_X'] =  P
	RQ_VAL['###Z_1_IntWall_N_Y'] =  P
	RQ_VAL['###Z_1_IntWall_N_Z'] =  0
	RQ_VAL['###Z_1_IntWall_N_Z_1'] =  0
	
	RQ_VAL['###Z_1_IntWall_N_L'] =  L-2*P
	RQ_VAL['###Z_1_IntWall_N_H'] =  H
	RQ_VAL['###Z_1_IntWall_W_X'] =  0
	RQ_VAL['###Z_1_IntWall_W_Y'] =  0
	RQ_VAL['###Z_1_IntWall_W_Z'] =  0
	RQ_VAL['###Z_1_IntWall_W_Z_1'] =  0
	
	RQ_VAL['###Z_1_IntWall_W_L'] =  1.414*P
	RQ_VAL['###Z_1_IntWall_W_H'] =  H
	RQ_VAL['###Z_1_IntWall_E_X'] =  L
	RQ_VAL['###Z_1_IntWall_E_Y'] =  0
	RQ_VAL['###Z_1_IntWall_E_Z'] =  0
	RQ_VAL['###Z_1_IntWall_E_Z_1'] =  0
	
	RQ_VAL['###Z_1_IntWall_E_L'] =  1.414*P
	RQ_VAL['###Z_1_IntWall_E_H'] =  H
	RQ_VAL['###Z_2_IntWall_S_X'] =  0
	RQ_VAL['###Z_2_IntWall_S_Y'] =  0
	RQ_VAL['###Z_2_IntWall_S_Z'] =  0
	RQ_VAL['###Z_2_IntWall_S_Z_1'] =  0
	
	RQ_VAL['###Z_2_IntWall_S_L'] =  1.414*P
	RQ_VAL['###Z_2_IntWall_S_H'] =  H
	RQ_VAL['###Z_2_IntWall_W_X'] =  0
	RQ_VAL['###Z_2_IntWall_W_Y'] =  0
	RQ_VAL['###Z_2_IntWall_W_Z'] =  0
	RQ_VAL['###Z_2_IntWall_W_Z_1'] =  0
	
	RQ_VAL['###Z_2_IntWall_W_L'] =  W-2*P
	RQ_VAL['###Z_2_IntWall_W_H'] =  H
	RQ_VAL['###Z_2_IntWall_N_X'] =  0
	RQ_VAL['###Z_2_IntWall_N_Y'] =  W-2*P
	RQ_VAL['###Z_2_IntWall_N_Z'] =  0
	RQ_VAL['###Z_2_IntWall_N_Z_1'] =  0
	
	RQ_VAL['###Z_2_IntWall_N_L'] =  1.414*P
	RQ_VAL['###Z_2_IntWall_N_H'] =  H
	RQ_VAL['###Z_4_IntWall_S_X'] =  0
	RQ_VAL['###Z_4_IntWall_S_Y'] =  0
	RQ_VAL['###Z_4_IntWall_S_Z'] =  0
	RQ_VAL['###Z_4_IntWall_S_Z_1'] =  0
	
	RQ_VAL['###Z_4_IntWall_S_L'] =  1.414*P
	RQ_VAL['###Z_4_IntWall_S_H'] =  H
	RQ_VAL['###Z_4_IntWall_N_X'] =  P
	RQ_VAL['###Z_4_IntWall_N_Y'] =  W-P
	RQ_VAL['###Z_4_IntWall_N_Z'] =  0
	RQ_VAL['###Z_4_IntWall_N_Z_1'] =  0
	
	
	RQ_VAL['###Z_4_IntWall_N_L'] =  1.414*P
	RQ_VAL['###Z_4_IntWall_N_H'] =  H
	RQ_VAL['###Z_4_IntWall_E_X'] =  P
	RQ_VAL['###Z_4_IntWall_E_Y'] =  P
	RQ_VAL['###Z_4_IntWall_E_Z'] =  0
	RQ_VAL['###Z_4_IntWall_E_Z_1'] =  0
	
	RQ_VAL['###Z_4_IntWall_E_L'] =  W-2*P
	RQ_VAL['###Z_4_IntWall_E_H'] =  H
	
	RQ_VAL['###Z_C_R_X'] =  L-2*P
	RQ_VAL['###Z_C_R_Y'] =  0
	RQ_VAL['###Z_C_R_Z'] =  H
	RQ_VAL['###Z_C_R_Z_1'] =  H
	
	
	RQ_VAL['###Z_C_R_L'] =  L-2*P
	RQ_VAL['###Z_C_R_W'] =  W-2*P
	
	RQ_VAL['###Z_C_F_X'] =  L-2*P
	RQ_VAL['###Z_C_F_Y'] =  0
	RQ_VAL['###Z_C_F_Z'] =  0
	RQ_VAL['###Z_C_F_Z_1'] =   H
	RQ_VAL['###Z_C_F_L'] =  L-2*P
	RQ_VAL['###Z_C_F_W'] =  W-2*P
	
	RQ_VAL['###Z_1_Win_X'] =  1
	RQ_VAL['###Z_1_Win_L'] =  L-2
	RQ_VAL['###Z_1_Win_H'] =  South_Win_area/(L-2)
	RQ_VAL['###Z_1_Win_Z'] =  (H - RQ_VAL['###Z_1_Win_H'])/2;
	
	RQ_VAL['###Z_2_Win_X'] =  1
	RQ_VAL['###Z_2_Win_L'] =  W-2 
	RQ_VAL['###Z_2_Win_H'] =  East_Win_area/(W-2)
	RQ_VAL['###Z_2_Win_Z'] =  (H - RQ_VAL['###Z_2_Win_H'])/2;
	
	RQ_VAL['###Z_3_Win_X'] =  1
	RQ_VAL['###Z_3_Win_L'] =  L-2
	RQ_VAL['###Z_3_Win_H'] =  North_Win_area/(L-2)
	RQ_VAL['###Z_3_Win_Z'] =  (H - RQ_VAL['###Z_3_Win_H'])/2
	
	RQ_VAL['###Z_4_Win_X'] =  1
	RQ_VAL['###Z_4_Win_L'] =  W-2 
	RQ_VAL['###Z_4_Win_H'] =  West_Win_area/(W-2)
	RQ_VAL['###Z_4_Win_Z'] =  (H - RQ_VAL['###Z_4_Win_H'])/2
	
	RQ_VAL['###Shade_N'] = RQ_VAL['###Z_3_Win_H'] * math.tan(Overhang*3.14/180) 
	RQ_VAL['###Shade_S'] = RQ_VAL['###Z_1_Win_H'] * math.tan(Overhang*3.14/180)
	RQ_VAL['###Shade_E'] = RQ_VAL['###Z_2_Win_H'] * math.tan(Overhang*3.14/180)
	RQ_VAL['###Shade_W'] = RQ_VAL['###Z_4_Win_H'] * math.tan(Overhang*3.14/180)

	RQ_VAL['###Z_1_DLC_X'] = L/2
	RQ_VAL['###Z_1_DLC_Y'] = P/2
	
	RQ_VAL['###Z_2_DLC_X'] = P/2
	RQ_VAL['###Z_2_DLC_Y'] = W/2
	
	RQ_VAL['###Z_3_DLC_X'] = L/2
	RQ_VAL['###Z_3_DLC_Y'] = P/2
	
	RQ_VAL['###Z_4_DLC_X'] = P/2
	RQ_VAL['###Z_4_DLC_Y'] = W/2

        RQ_VAL['###zonemultiplier'] = zonemultiplier



	return RQ_VAL



# Main starts here
filename ='b.idf'
angle=Overhang

RQ_VAL=generate_co(Orientation,Area,Aspect_Ratio,Wwr,glass,angle);

f=open('/home/ec2-user/aviruch/MultiFloorTemplate.idf');
w=open(filename,'w');
for line in f:
		sets=re.findall(r'#.*?[,;]',line);
		for j in sets:
			j=j[:-1];
			line=line.replace(j,str(RQ_VAL[j]));

		w.write(line);
w.close();




# Run EnergyPlus
WeatherFilePath = '/home/ec2-user/aviruch/WeatherData/' + WeatherFile

#energyplus -w IND_Ahmedabad.426470_ISHRAE.epw -p ./Output/b -s C -x -m -r b_86.idf
cmd_test = "/usr/local/bin/energyplus -w "+ WeatherFilePath+ " -p /home/ec2-user/aviruch/Output/b -s C -x -m -r "+filename 

print (cmd_test)
os.system("rm -rf /home/ec2-user/aviruch/Output")
os.system("mkdir /home/ec2-user/aviruch/Output")
os.system(cmd_test)

# # Fetch EnergySimualtion resutls
time.sleep(1)
os.system("clear")


html = linecache.getline('/home/ec2-user/aviruch/Output/bTable.htm',37)

m=re.findall(r"\d+\.\d+", html)


print ("Total Energy =")
os.system("clear")
print (m[0])



# # Delete all files

os.system("rm -rf /home/ec2-user/aviruch/Output")

#os.system("rm -rf expanded*")
#os.system("rm -rf eplusout*")
os.system("rm -rf /home/ec2-user/aviruch/b.idf")
os.system("rm -rf /home/ec2-user/aviruch/sq*")
os.system("rm -rf /home/ec2-user/aviruch/ep*")
print ("Process Completed")

