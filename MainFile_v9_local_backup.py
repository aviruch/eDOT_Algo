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
Aspect_Ratio = float(sys.argv[19])




print ("AREA, Weatherfile, Orientation, OVerhang, WWR, AR, U-value glass, SHGC, and VLT")

print (Area, WeatherFile, Orientation, Overhang, Wwr, Aspect_Ratio, U_value, Shgc,Vlt)


# #cost fixed as of now
cost_glass = 5000
glass=(Shgc,Vlt,U_value,cost_glass)
# #glass=(0.1, 0.175, 3.1, 5000.0)




def generate_co_SingleFloor(Orientation,Area,Ar,Wwr,glass,Overhang):
	
	#STRUCTURAL REPRESENTATION

	P = 3.0; # Perimeter Depth
	H = 3.0; # Floor to floor height

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
	RQ_VAL['###Z_1_R_1_X'] =  0
	RQ_VAL['###Z_1_R_1_Y'] =  0
	RQ_VAL['###Z_1_R_1_Z'] =  H
	RQ_VAL['###Z_1_R_2_X'] =  L
	RQ_VAL['###Z_1_R_2_Y'] =  0
	RQ_VAL['###Z_1_R_2_Z'] =  H
	RQ_VAL['###Z_1_R_3_X'] =  L-P
	RQ_VAL['###Z_1_R_3_Y'] =  P
	RQ_VAL['###Z_1_R_3_Z'] =  H
	RQ_VAL['###Z_1_R_4_X'] =  P
	RQ_VAL['###Z_1_R_4_Y'] =  P
	RQ_VAL['###Z_1_R_4_Z'] =  H
	RQ_VAL['###Z_2_R_1_X'] =  0
	RQ_VAL['###Z_2_R_1_Y'] =  0
	RQ_VAL['###Z_2_R_1_Z'] =  H
	RQ_VAL['###Z_2_R_2_X'] =  P
	RQ_VAL['###Z_2_R_2_Y'] =  - P
	RQ_VAL['###Z_2_R_2_Z'] =  H
	RQ_VAL['###Z_2_R_3_X'] =  P
	RQ_VAL['###Z_2_R_3_Y'] =  W-P
	RQ_VAL['###Z_2_R_3_Z'] =  H
	RQ_VAL['###Z_2_R_4_X'] =  0
	RQ_VAL['###Z_2_R_4_Y'] =  W-2*P
	RQ_VAL['###Z_2_R_4_Z'] =  H
	RQ_VAL['###Z_3_R_1_X'] =  0
	RQ_VAL['###Z_3_R_1_Y'] =  0
	RQ_VAL['###Z_3_R_1_Z'] =  H
	RQ_VAL['###Z_3_R_2_X'] =  L-2*P
	RQ_VAL['###Z_3_R_2_Y'] =  0
	RQ_VAL['###Z_3_R_2_Z'] =  H
	RQ_VAL['###Z_3_R_3_X'] =  L-P
	RQ_VAL['###Z_3_R_3_Y'] =  P
	RQ_VAL['###Z_3_R_3_Z'] =  H
	RQ_VAL['###Z_3_R_4_X'] =  - P
	RQ_VAL['###Z_3_R_4_Y'] =  P
	RQ_VAL['###Z_3_R_4_Z'] =  H
	RQ_VAL['###Z_4_R_1_X'] =  0
	RQ_VAL['###Z_4_R_1_Y'] =  0
	RQ_VAL['###Z_4_R_1_Z'] =  H
	RQ_VAL['###Z_4_R_2_X'] =  P
	RQ_VAL['###Z_4_R_2_Y'] =  P
	RQ_VAL['###Z_4_R_2_Z'] =  H
	RQ_VAL['###Z_4_R_3_X'] =  P
	RQ_VAL['###Z_4_R_3_Y'] =  W-P
	RQ_VAL['###Z_4_R_3_Z'] =  H
	RQ_VAL['###Z_4_R_4_X'] =  0
	RQ_VAL['###Z_4_R_4_Y'] =  W
	RQ_VAL['###Z_4_R_4_Z'] =  H
	
	RQ_VAL['###Z_1_F_1_X'] =  0
	RQ_VAL['###Z_1_F_1_Y'] =  0
	RQ_VAL['###Z_1_F_1_Z'] =  0
	
	RQ_VAL['###Z_1_F_2_X'] =  P
	RQ_VAL['###Z_1_F_2_Y'] =  P
	RQ_VAL['###Z_1_F_2_Z'] =  0
	
	RQ_VAL['###Z_1_F_3_X'] =  L-P
	RQ_VAL['###Z_1_F_3_Y'] =  P
	RQ_VAL['###Z_1_F_3_Z'] =  0
	
	RQ_VAL['###Z_1_F_4_X'] =  L
	RQ_VAL['###Z_1_F_4_Y'] =  0
	RQ_VAL['###Z_1_F_4_Z'] =  0
	
	RQ_VAL['###Z_2_F_1_X'] =  0
	RQ_VAL['###Z_2_F_1_Y'] =  0
	RQ_VAL['###Z_2_F_1_Z'] =  0
	RQ_VAL['###Z_2_F_2_X'] =  0
	RQ_VAL['###Z_2_F_2_Y'] =  W-2*P
	RQ_VAL['###Z_2_F_2_Z'] =  0
	RQ_VAL['###Z_2_F_3_X'] =  P
	RQ_VAL['###Z_2_F_3_Y'] =  W-P
	RQ_VAL['###Z_2_F_3_Z'] =  0
	RQ_VAL['###Z_2_F_4_X'] =  P
	RQ_VAL['###Z_2_F_4_Y'] =  - P
	RQ_VAL['###Z_2_F_4_Z'] =  0
	RQ_VAL['###Z_3_F_1_X'] =  0
	RQ_VAL['###Z_3_F_1_Y'] =  0
	RQ_VAL['###Z_3_F_1_Z'] =  0
	RQ_VAL['###Z_3_F_2_X'] =  - P
	RQ_VAL['###Z_3_F_2_Y'] =  P
	RQ_VAL['###Z_3_F_2_Z'] =  0
	RQ_VAL['###Z_3_F_3_X'] =  L-P
	RQ_VAL['###Z_3_F_3_Y'] =  P
	RQ_VAL['###Z_3_F_3_Z'] =  0
	RQ_VAL['###Z_3_F_4_X'] =  L-2*P
	RQ_VAL['###Z_3_F_4_Y'] =  0
	RQ_VAL['###Z_3_F_4_Z'] =  0
	
	RQ_VAL['###Z_4_F_1_X'] =  0
	RQ_VAL['###Z_4_F_1_Y'] =  0
	RQ_VAL['###Z_4_F_1_Z'] =  0
	RQ_VAL['###Z_4_F_2_X'] =  0
	RQ_VAL['###Z_4_F_2_Y'] =  W
	RQ_VAL['###Z_4_F_2_Z'] =  0
	RQ_VAL['###Z_4_F_3_X'] =  P
	RQ_VAL['###Z_4_F_3_Y'] =  W-P
	RQ_VAL['###Z_4_F_3_Z'] =  0
	RQ_VAL['###Z_4_F_4_X'] =  P
	RQ_VAL['###Z_4_F_4_Y'] =  P
	RQ_VAL['###Z_4_F_4_Z'] =  0
	
	RQ_VAL['###Z_3_ExWall_X'] =  L-P
	RQ_VAL['###Z_3_ExWall_Y'] =  P
	RQ_VAL['###Z_3_ExWall_Z'] =  0

	RQ_VAL['###Z_3_ExWall_L'] =  L
	RQ_VAL['###Z_3_ExWall_H'] =  H
	RQ_VAL['###Z_1_ExWall_X'] =  0
	RQ_VAL['###Z_1_ExWall_Y'] =  0
	RQ_VAL['###Z_1_ExWall_Z'] =  0
	RQ_VAL['###Z_1_ExWall_L'] =  L
	RQ_VAL['###Z_1_ExWall_H'] =  H
	RQ_VAL['###Z_2_ExWall_X'] =  P
	RQ_VAL['###Z_2_ExWall_Y'] =  - P
	RQ_VAL['###Z_2_ExWall_Z'] =  0
	RQ_VAL['###Z_2_ExWall_L'] =  W
	RQ_VAL['###Z_2_ExWall_H'] =  H
	RQ_VAL['###Z_4_ExWall_X'] =  0
	RQ_VAL['###Z_4_ExWall_Y'] =  W
	RQ_VAL['###Z_4_ExWall_Z'] =  0
	RQ_VAL['###Z_4_ExWall_L'] =  W
	RQ_VAL['###Z_4_ExWall_H'] =  H
	RQ_VAL['###Z_3_IntWall_S_X'] =  0
	RQ_VAL['###Z_3_IntWall_S_Y'] =  0
	RQ_VAL['###Z_3_IntWall_S_Z'] =  0
	RQ_VAL['###Z_3_IntWall_S_L'] =  L-2*P
	RQ_VAL['###Z_3_IntWall_S_H'] =  H
	RQ_VAL['###Z_3_IntWall_E_X'] =  L-2*P
	RQ_VAL['###Z_3_IntWall_E_Y'] =  0
	RQ_VAL['###Z_3_IntWall_E_Z'] =  0
	RQ_VAL['###Z_3_IntWall_E_L'] =  1.414*P
	RQ_VAL['###Z_3_IntWall_E_H'] =  H
	RQ_VAL['###Z_3_IntWall_W_X'] =  0
	RQ_VAL['###Z_3_IntWall_W_Y'] =  0
	RQ_VAL['###Z_3_IntWall_W_Z'] =  0
	RQ_VAL['###Z_3_IntWall_W_L'] =  1.414*P
	RQ_VAL['###Z_3_IntWall_W_H'] =  H
	RQ_VAL['###Z_1_IntWall_N_X'] =  P
	RQ_VAL['###Z_1_IntWall_N_Y'] =  P
	RQ_VAL['###Z_1_IntWall_N_Z'] =  0
	RQ_VAL['###Z_1_IntWall_N_L'] =  L-2*P
	RQ_VAL['###Z_1_IntWall_N_H'] =  H
	RQ_VAL['###Z_1_IntWall_W_X'] =  0
	RQ_VAL['###Z_1_IntWall_W_Y'] =  0
	RQ_VAL['###Z_1_IntWall_W_Z'] =  0
	RQ_VAL['###Z_1_IntWall_W_L'] =  1.414*P
	RQ_VAL['###Z_1_IntWall_W_H'] =  H
	RQ_VAL['###Z_1_IntWall_E_X'] =  L
	RQ_VAL['###Z_1_IntWall_E_Y'] =  0
	RQ_VAL['###Z_1_IntWall_E_Z'] =  0
	RQ_VAL['###Z_1_IntWall_E_L'] =  1.414*P
	RQ_VAL['###Z_1_IntWall_E_H'] =  H
	RQ_VAL['###Z_2_IntWall_S_X'] =  0
	RQ_VAL['###Z_2_IntWall_S_Y'] =  0
	RQ_VAL['###Z_2_IntWall_S_Z'] =  0
	RQ_VAL['###Z_2_IntWall_S_L'] =  1.414*P
	RQ_VAL['###Z_2_IntWall_S_H'] =  H
	RQ_VAL['###Z_2_IntWall_W_X'] =  0
	RQ_VAL['###Z_2_IntWall_W_Y'] =  0
	RQ_VAL['###Z_2_IntWall_W_Z'] =  0
	RQ_VAL['###Z_2_IntWall_W_L'] =  W-2*P
	RQ_VAL['###Z_2_IntWall_W_H'] =  H
	RQ_VAL['###Z_2_IntWall_N_X'] =  0
	RQ_VAL['###Z_2_IntWall_N_Y'] =  W-2*P
	RQ_VAL['###Z_2_IntWall_N_Z'] =  0
	RQ_VAL['###Z_2_IntWall_N_L'] =  1.414*P
	RQ_VAL['###Z_2_IntWall_N_H'] =  H
	RQ_VAL['###Z_4_IntWall_S_X'] =  0
	RQ_VAL['###Z_4_IntWall_S_Y'] =  0
	RQ_VAL['###Z_4_IntWall_S_Z'] =  0
	RQ_VAL['###Z_4_IntWall_S_L'] =  1.414*P
	RQ_VAL['###Z_4_IntWall_S_H'] =  H
	RQ_VAL['###Z_4_IntWall_N_X'] =  P
	RQ_VAL['###Z_4_IntWall_N_Y'] =  W-P
	RQ_VAL['###Z_4_IntWall_N_Z'] =  0
	RQ_VAL['###Z_4_IntWall_N_L'] =  1.414*P
	RQ_VAL['###Z_4_IntWall_N_H'] =  H
	RQ_VAL['###Z_4_IntWall_E_X'] =  P
	RQ_VAL['###Z_4_IntWall_E_Y'] =  P
	RQ_VAL['###Z_4_IntWall_E_Z'] =  0
	RQ_VAL['###Z_4_IntWall_E_L'] =  W-2*P
	RQ_VAL['###Z_4_IntWall_E_H'] =  H
	
	RQ_VAL['###Z_C_R_X'] =  L-2*P
	RQ_VAL['###Z_C_R_Y'] =  0
	RQ_VAL['###Z_C_R_Z'] =  H
	RQ_VAL['###Z_C_R_L'] =  L-2*P
	RQ_VAL['###Z_C_R_W'] =  W-2*P
	
	RQ_VAL['###Z_C_F_X'] =  L-2*P
	RQ_VAL['###Z_C_F_Y'] =  0
	RQ_VAL['###Z_C_F_Z'] =  0
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
	print("RQ_VAL['###Z_4_Win_H'] =  West_Win_area/(W-2)",RQ_VAL['###Z_4_Win_H'] )
	RQ_VAL['###Z_4_Win_Z'] =  (H - RQ_VAL['###Z_4_Win_H'])/2
	
	#Overhang = 5
	RQ_VAL['###Shade_N'] = float(RQ_VAL['###Z_3_Win_H']) * math.tan(Overhang*3.14/180) 
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

	return RQ_VAL




# Multi Floor

def generate_co_MultiFloor(Orientation,Area,Ar,Wwr,glass,Overhang):
	
        zonemultiplier = Floors - 2;	# Top floor and ground floor minus 
        #STRUCTURAL REPRESENTATION

	P = 3.0; #Perimeter Depth for daylight
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


def FetchResutls():
    time.sleep(1)
    #os.system("clear")
    html = linecache.getline('Output/bTable.htm',37)
    m=re.findall(r"\d+\.\d+", html)
    print ("Total Energy =")
    #os.system("clear")
    print (m[0])    
    
    return (m[0])


def CleanFiles():
# # Delete all files
    os.system("rm -rf Output")
    #os.system("rm -rf expanded*")
    #os.system("rm -rf eplusout*")
    os.system("rm -rf b.idf")
    os.system("rm -rf sq*")
    os.system("rm -rf ep*") 
    os.system("mkdir Output")


def RunSimulations(filename):
    WeatherFilePath = 'WeatherData/' + WeatherFile
    #energyplus -w IND_Ahmedabad.426470_ISHRAE.epw -p ./Output/b -s C -x -m -r b_86.idf
    cmd_test = "/usr/local/bin/energyplus -w "+ WeatherFilePath+ " -p Output/b -s C -x -m -r "+filename 
    print (cmd_test)
    #os.system("rm -rf /Output")
    #os.system("mkdir /Output")
    os.system(cmd_test)




def GenerateTemplateMultiFloor(Schedule,CoolRoof,DayLightSensor,IntShades,HVAC):
    
    Schedule = "Office" # Other Options are "Retail" and "Institute"
    #DesignDay  Need to change with weather file selection 
    #CoolRoof="NO"  #Other Option "Yes"
    #DayLightSensor="ON"  #Other Option "OFF"
    #IntShades="OFF"  # Other Option "ON"
    HVAC="PTHP" #Other Options are "CentralWaterCooledChiller: CWC" and "CentralAirCooledChiller: CAC"

    f=open("MultiFloorTemplate.idf",'w')

    # Header file
    print "Header file"
    file_Header=open("MultiFloors/01_Header.idf","r")
    g_1=file_Header.read()
    f.write(g_1)
    file_Header.close()



    #DDY File
    print "DDY File"
    file_DDY=open("MultiFloors/02B_SizingWeatherFile.idf","r")
    g_2=file_DDY.read()
    f.write(g_2)
    file_DDY.close()
    
    # Schedule file
    print "Schedule file"
    
    if Schedule=="Office":
        file_Schedule_Office=open("MultiFloors/03A_Schedule_Office.idf","r")
        g_3=file_Schedule_Office.read()
        f.write(g_3)
        file_Schedule_Office.close()
    
    elif Schedule=="Retail":
        file_Schedule_Retail=open("MultiFloors/03B_Schedule_Retail.idf","r")
        g_3=file_Schedule_Retail.read()
        f.write(g_3)
        file_Schedule_Retail.close()
    
    else:
        file_Schedule_Institute=open("MultiFloors/03C_Schedule_Institute.idf","r")
        g_3=file_Schedule_Institute.read()
        f.write(g_3)
        file_Schedule_Institute.close()
    
    
    
    # Cool Roof
    print "Cool Roof file"
    
    if CoolRoof=="false":
        file_CoolRoof_Off=open("MultiFloors/04A_CoolRoof_OFF.idf","r")
        g_4=file_CoolRoof_Off.read()
        f.write(g_4)
        file_CoolRoof_Off.close()
    else:
        file_CoolRoof_On=open("MultiFloors/04B_CoolRoof_ON.idf","r")
        g_4=file_CoolRoof_On.read()
        f.write(g_4)
        file_CoolRoof_On.close()
    
    
    # Zones
    print "Zones"
    file_Zones=open("MultiFloors/05_Zones_MultiFloors.idf","r")
    g_5=file_Zones.read()
    f.write(g_5)
    file_Zones.close()
    
    
    # Gains
    print "Gains"
    file_Gains=open("MultiFloors/06_Gains.idf","r")
    g_6=file_Gains.read()
    f.write(g_6)
    file_Gains.close()
    
    
    # Daylight
    print "Daylight"
    
    if DayLightSensor=="true": 
        file_DayLight_ON=open("MultiFloors/07A_Daylight_ON.idf","r")
        g_7=file_DayLight_ON.read()
        f.write(g_7)
        file_DayLight_ON.close()
    else:
        file_DayLight_OFF=open("MultiFloors/07B_Daylight_OFF.idf","r")
        g_7=file_DayLight_OFF.read()
        f.write(g_7)
        file_DayLight_OFF.close()
    
    # Internal Shades
    print "Internal Shades"
    
    if IntShades=="OFF":
        file_IntShade_OFF=open("MultiFloors/08A_IntShade_OFF.idf","r")
        g_8=file_IntShade_OFF.read()
        f.write(g_8)
        file_IntShade_OFF.close()
    else:
        file_IntShade_ON=open("MultiFloors/08B_IntShade_ON_Solar.idf","r")
        g_8=file_IntShade_ON.read()
        f.write(g_8)
        file_IntShade_ON.close()

    # HVAC
    print "HVAC"
    
    if HVAC=="PTHP": 
        file_HVAC_PTHP=open("MultiFloors/09A_HVAC_PTHP.idf","r")
        g_9=file_HVAC_PTHP.read()
        f.write(g_9)
        file_HVAC_PTHP.close()
    elif HVAC=="CWC":
        file_HVAC=open("MultiFloors/09B_HVAC_CWC.idf","r")
        g_9=file_HVAC.read()
        f.write(g_9)
        file_HVAC.close()
    else:
    
        file_HVAC=open("MultiFloors/09C_HVAC_CAC.idf","r")
        g_9=file_HVAC.read()
        f.write(g_9)
        file_HVAC.close()
    
 
    # Economics
    print "Economics"
    file_Economics=open("MultiFloors/10_Economics.idf","r")
    g_10=file_Economics.read()
    f.write(g_10)
    file_Economics.close()
    
    
    # Output
    print "Output"
    file_Output=open("MultiFloors/11_Output.idf","r")
    g_11=file_Output.read()
    f.write(g_11)
    file_Output.close()
    
    
    f.close()
    
    print "Finish"
    


def GenerateTemplateSingleFloor(Schedule,CoolRoof,DayLightSensor,IntShades,HVAC):

    Schedule = "OFFICE" # Other Options are "Retail" and "Institute"
    #DesignDay  Need to change with weather file selection 
    CoolRoof="NO"  #Other Option "Yes"
    DayLightSensor="ON"  #Other Option "OFF"
    IntShades="OFF"  # Other Option "ON"
    HVAC="CWC" #Other Options are "CentralWaterCooledChiller: CWC" and "CentralAirCooledChiller: CAC"
    
    f=open("SingleFloorTemplate.idf",'w')
    
    # Header file
    print "Header file"
    file_Header=open("SingleFloor/01_Header.idf","r")
    g_1=file_Header.read()
    f.write(g_1)
    file_Header.close()
    
 
    #DDY File
    print "DDY File"
    file_DDY=open("SingleFloor/02B_Size_WeatherData.idf","r")
    g_2=file_DDY.read()
    f.write(g_2)
    file_DDY.close()
    
    # Schedule file
    print "Schedule file"
    
    if Schedule=="Office":
        file_Schedule_Office=open("SingleFloor/03A_Schedule_Office.idf","r")
        g_3=file_Schedule_Office.read()
        f.write(g_3)
        file_Schedule_Office.close()
    
    elif Schedule=="Retail":
        file_Schedule_Retail=open("SingleFloor/03B_Schedule_Retail.idf","r")
        g_3=file_Schedule_Retail.read()
        f.write(g_3)
        file_Schedule_Retail.close()
    
    else:
        file_Schedule_Institute=open("SingleFloor/03C_Schedule_Institute.idf","r")
        g_3=file_Schedule_Institute.read()
        f.write(g_3)
        file_Schedule_Institute.close()
    
    # Cool Roof
    print "Cool Roof file"
    
    if CoolRoof=="false":
        file_CoolRoof_Off=open("SingleFloor/04A_CoolRoof_OFF.idf","r")
        g_4=file_CoolRoof_Off.read()
        f.write(g_4)
        file_CoolRoof_Off.close()
    else:
        file_CoolRoof_On=open("SingleFloor/04B_CoolRoof_ON.idf","r")
        g_4=file_CoolRoof_On.read()
        f.write(g_4)
        file_CoolRoof_On.close()
    
  # Zones
    print "Zones"
    file_Zones=open("SingleFloor/05_Zones.idf","r")
    g_5=file_Zones.read()
    f.write(g_5)
    file_Zones.close()
    
    # Gains
    print "Gains"
    file_Gains=open("SingleFloor/06_Gains.idf","r")
    g_6=file_Gains.read()
    f.write(g_6)
    file_Gains.close()
    
   # Daylight
    print "Daylight"
    
    if DayLightSensor=="true": 
        file_DayLight_ON=open("SingleFloor/07A_Daylight_ON.idf","r")
        g_7=file_DayLight_ON.read()
        f.write(g_7)
        file_DayLight_ON.close()
    else:
        file_DayLight_OFF=open("SingleFloor/07B_Daylight_OFF.idf","r")
        g_7=file_DayLight_OFF.read()
        f.write(g_7)
        file_DayLight_OFF.close()
   
    
    # Internal Shades
    print "Internal Shades"
    
    if IntShades=="OFF":
        file_IntShade_OFF=open("SingleFloor/08A_IntShade_OFF.idf","r")
        g_8=file_IntShade_OFF.read()
        f.write(g_8)
        file_IntShade_OFF.close()
    else:
        file_IntShade_ON=open("SingleFloor/08A_IntShade_ON.idf","r")
        g_8=file_IntShade_ON.read()
        f.write(g_8)
        file_IntShade_ON.close()
    
   
    # HVAC
    print "HVAC"
    
    if HVAC=="PTHP": 
        file_HVAC_PTHP=open("SingleFloor/09A_HVAC_PTHP.idf","r")
        g_9=file_HVAC_PTHP.read()
        f.write(g_9)
        file_HVAC_PTHP.close()
    elif HVAC=="CWC":
        file_HVAC=open("SingleFloor/09B_HVAC_CWC.idf","r")
        g_9=file_HVAC.read()
        f.write(g_9)
        file_HVAC.close()
    else:
    
        file_HVAC=open("SingleFloor/09C_HVAC_CAC.idf","r")
        g_9=file_HVAC.read()
        f.write(g_9)
        file_HVAC.close()

    # Economics
    print "Economics"
    file_Economics=open("SingleFloor/10_Economics.idf","r")
    g_10=file_Economics.read()
    f.write(g_10)
    file_Economics.close()
 
    # Output
    print "Output"
    file_Output=open("SingleFloor/11_Output.idf","r")
    g_11=file_Output.read()
    f.write(g_11)
    file_Output.close()
   
    f.close()
    
    print "Finish"




def ProcessSingleFloor():
    GenerateTemplateSingleFloor(BuildingType,CoolRoof,DaylightCtrl,ShadingCtrl,HVAC_Type)
    filename ='b.idf'
    angle=Overhang
    RQ_VAL=generate_co_SingleFloor(Orientation,Area,Aspect_Ratio,Wwr,glass,angle);
    f=open('SingleFloorTemplate.idf');
    w=open(filename,'w');
    for line in f:
  		sets=re.findall(r'#.*?[,;]',line);
  		for j in sets:
 			j=j[:-1];
 			line=line.replace(j,str(RQ_VAL[j]));
    
  		w.write(line);
    w.close();



def ProcessMultiFloor():

    GenerateTemplateMultiFloor(BuildingType,CoolRoof,DaylightCtrl,ShadingCtrl,HVAC_Type)
    filename ='b.idf'
    angle=Overhang
    RQ_VAL=generate_co_MultiFloor(Orientation,Area,Aspect_Ratio,Wwr,glass,angle);
    f=open('MultiFloorTemplate.idf');
    w=open(filename,'w');
    for line in f:
  		sets=re.findall(r'#.*?[,;]',line);
  		for j in sets:
 			j=j[:-1];
 			line=line.replace(j,str(RQ_VAL[j]));
    
  		w.write(line);
    w.close();





# Main starts here

print "Number of Floors"
print Floors


if Floors == 1:

    ProcessSingleFloor()
    print "Finish single floor"

elif Floors == 2:
    #Second Floor model is not ready yet.
    Floors = 3
    ProcessMultiFloor()

else:

    ProcessMultiFloor()



# Run EnergyPlus
filename ='b.idf'
#RunSimulations(filename)

# # Fetch EnergySimualtion resutls

#FetchResutls()

#CleanFiles()

print ("Process Completed")

