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
Wall_H = Height
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
wwr = Wwr
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
global Shade_Depth
Shade_Depth =float(sys.argv[18])
# Wwr = 0.4

# Aspect_Ratio = 2
Aspect_Ratio = float(sys.argv[19])




print ("AREA, Weatherfile, Orientation, OVerhang, WWR, AR, U-value glass, SHGC, and VLT, HVAC_Type")

print (Area, WeatherFile, Orientation, Overhang, Wwr, Aspect_Ratio, U_value, Shgc,Vlt,HVAC_Type)


# #cost fixed as of now
cost_glass = 5000
glass=(Shgc,Vlt,U_value,cost_glass)
# #glass=(0.1, 0.175, 3.1, 5000.0)

#///////////////////////////////////////////////////////////////////////////////////

#function to generate regular window type 

def Win_Coordinate(k,j,Win_S,Win_W_each,Win_H_each,i):
    Win_Number = k
    Win_X=j
    Win_Y=Win_S
    print "! Window ID=",k
    print "! X =","{0:.2f}".format(Win_X)
    print "! Y =","{0:.2f}".format(Win_S)
    f=open("WinShadeTemplate/Window_template.txt","r")
    text=f.read()
    
    text =  re.sub("Window_ID", i+str(k),text)
    text =  re.sub("Wall_ID", i,text)
    text =  re.sub("Win_X", str(round(Win_X,2)),text)
    text =  re.sub("Win_Z", str(Win_Y),text)
    text =  re.sub("Win_L", str(Win_W_each),text)
    text =  re.sub("Win_H", str(Win_H_each),text)
    print text
    
    f.close()
    
    WindowIDF.writelines("\n")
    WindowIDF.writelines(text)
    WindowIDF.writelines("\n")
	
	
    S=open("WinShadeTemplate/Shade_template.txt","r")
    Shade_text=S.read()
    
    Shade_text =  re.sub("Window_ID", i+str(k),Shade_text)
    Shade_text =  re.sub("Shade_ID", "shade_"+i+str(k),Shade_text)
    Shade_text =  re.sub("Shade_Depth", str(Shade_Depth),Shade_text)
    print Shade_text
    
    
    
    ShadeIDF.writelines("\n")
    ShadeIDF.writelines(Shade_text)
    ShadeIDF.writelines("\n")

    S.close()
   

def Wall_Win(i,Wall_H,Wall_W,Win_S,Win_W, Win_H):
    print i

    print("Wall Height=","{0:.2f}".format(Wall_H))
    print("Wall Width=","{0:.2f}".format(Wall_W))

    Wall_area=Wall_H*Wall_W
    Win_area=Wall_area*wwr
    Win_area_each= Win_W*Win_H

    #Win_W=Win_area/Win_H


    print("Window Area Sqm = Wall Area * WWR=","{0:.2f}".format(Win_area))
    #print("Calculated Window Width All =",Win_W)

  
   # Win_N=int(math.ceil(Wall_W/(Win_W+Win_Dist)))

    Win_N=int(math.ceil(Win_area/(Win_area_each)))
    

    

    Win_area_each_modified=Win_area/Win_N
    Win_W_each = Win_area_each_modified/Win_H
    Win_space=Wall_W-Win_W_each*Win_N
    Win_Dist=Win_space/(Win_N+1)
    print("Window Distance","{0:.2f}".format(Win_Dist))

    if Win_H + Win_S > Wall_H or Win_Dist<0:
        print "Windows does not fit, reduce WWR"
    
    else:
        print("Number of Windows=",Win_N)
        print("Calculated Window width each =","{0:.2f}".format(Win_W_each))
        j=0.1
        for k in range(Win_N):
            
            Win_Coordinate(k,j,Win_S,Win_W_each,Win_H,i)
            j=j+Win_W_each+Win_Dist
            




#////////////////////////////////////////////////////////////////////////////////////


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
    HVAC="PTHP" #Other Options are "CentralWaterCooledChiller: CWC" and "CentralAirCooledChiller: CAC"
    
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

#//////////////////////////////////////////////////////////////////////////////////////////////

def GenerateTemplateMultiFloorRegular(Schedule,CoolRoof,DayLightSensor,IntShades,HVAC):
    Schedule = "Office" # Other Options are "Retail" and "Institute"
    #DesignDay  Need to change with weather file selection 
    #CoolRoof="NO"  #Other Option "Yes"
    #DayLightSensor="ON"  #Other Option "OFF"
    #IntShades="OFF"  # Other Option "ON"
    HVAC="PTHP" #Other Options are "CentralWaterCooledChiller: CWC" and "CentralAirCooledChiller: CAC"

    f=open("MultiFloorTemplate.idf",'w')

    # Header file
    print "Header file"
    file_Header=open("MultiFloorsRegular/01_Header.idf","r")
    g_1=file_Header.read()
    f.write(g_1)
    file_Header.close()



    #DDY File
    print "DDY File"
    file_DDY=open("MultiFloorsRegular/02B_SizingWeatherFile.idf","r")
    g_2=file_DDY.read()
    f.write(g_2)
    file_DDY.close()
    
    # Schedule file
    print "Schedule file"
    
    if Schedule=="Office":
        file_Schedule_Office=open("MultiFloorsRegular/03A_Schedule_Office.idf","r")
        g_3=file_Schedule_Office.read()
        f.write(g_3)
        file_Schedule_Office.close()
    
    elif Schedule=="Retail":
        file_Schedule_Retail=open("MultiFloorsRegular/03B_Schedule_Retail.idf","r")
        g_3=file_Schedule_Retail.read()
        f.write(g_3)
        file_Schedule_Retail.close()
    
    else:
        file_Schedule_Institute=open("MultiFloorsRegular/03C_Schedule_Institute.idf","r")
        g_3=file_Schedule_Institute.read()
        f.write(g_3)
        file_Schedule_Institute.close()
    
    
    
    # Cool Roof
    print "Cool Roof file"
    
    if CoolRoof=="false":
        file_CoolRoof_Off=open("MultiFloorsRegular/04A_CoolRoof_OFF.idf","r")
        g_4=file_CoolRoof_Off.read()
        f.write(g_4)
        file_CoolRoof_Off.close()
    else:
        file_CoolRoof_On=open("MultiFloorsRegular/04B_CoolRoof_ON.idf","r")
        g_4=file_CoolRoof_On.read()
        f.write(g_4)
        file_CoolRoof_On.close()
    
    
    # Zones
    print "Zones"
    file_Zones=open("MultiFloorsRegular/05_Zones_MultiFloors.idf","r")
    g_5=file_Zones.read()
    f.write(g_5)
    file_Zones.close()
    
    
    # Gains
    print "Gains"
    file_Gains=open("MultiFloorsRegular/06_Gains.idf","r")
    g_6=file_Gains.read()
    f.write(g_6)
    file_Gains.close()
    
    
    # Daylight
    print "Daylight"
    
    if DayLightSensor=="true": 
        file_DayLight_ON=open("MultiFloorsRegular/07A_Daylight_ON.idf","r")
        g_7=file_DayLight_ON.read()
        f.write(g_7)
        file_DayLight_ON.close()
    else:
        file_DayLight_OFF=open("MultiFloorsRegular/07B_Daylight_OFF.idf","r")
        g_7=file_DayLight_OFF.read()
        f.write(g_7)
        file_DayLight_OFF.close()
    
    # Internal Shades
    print "Internal Shades"
    
    if IntShades=="OFF":
        file_IntShade_OFF=open("MultiFloorsRegular/08A_IntShade_OFF.idf","r")
        g_8=file_IntShade_OFF.read()
        f.write(g_8)
        file_IntShade_OFF.close()
    else:
        file_IntShade_ON=open("MultiFloorsRegular/08B_IntShade_ON_Solar.idf","r")
        g_8=file_IntShade_ON.read()
        f.write(g_8)
        file_IntShade_ON.close()

    # HVAC
    print "HVAC"
    
    if HVAC=="PTHP": 
        file_HVAC_PTHP=open("MultiFloorsRegular/09A_HVAC_PTHP.idf","r")
        g_9=file_HVAC_PTHP.read()
        f.write(g_9)
        file_HVAC_PTHP.close()
    elif HVAC=="CWC":
        file_HVAC=open("MultiFloorsRegular/09B_HVAC_CWC.idf","r")
        g_9=file_HVAC.read()
        f.write(g_9)
        file_HVAC.close()
    else:
    
        file_HVAC=open("MultiFloorsRegular/09C_HVAC_CAC.idf","r")
        g_9=file_HVAC.read()
        f.write(g_9)
        file_HVAC.close()
    
 
    # Economics
    print "Economics"
    file_Economics=open("MultiFloorsRegular/10_Economics.idf","r")
    g_10=file_Economics.read()
    f.write(g_10)
    file_Economics.close()
    
    
    # Output
    print "Output"
    file_Output=open("MultiFloorsRegular/11_Output.idf","r")
    g_11=file_Output.read()
    f.write(g_11)
    file_Output.close()
    
    
    f.close()
    
    print "Finish"
    


def GenerateTemplateSingleFloorRegular(Schedule,CoolRoof,DayLightSensor,IntShades,HVAC):
    Schedule = "OFFICE" # Other Options are "Retail" and "Institute"
    #DesignDay  Need to change with weather file selection 
    CoolRoof="NO"  #Other Option "Yes"
    DayLightSensor="ON"  #Other Option "OFF"
    IntShades="OFF"  # Other Option "ON"
    HVAC="PTHP" #Other Options are "CentralWaterCooledChiller: CWC" and "CentralAirCooledChiller: CAC"
    
    f=open("SingleFloorTemplate.idf",'w')
    
    # Header file
    print "Header file"
    file_Header=open("SingleFloorRegular/01_Header.idf","r")
    g_1=file_Header.read()
    f.write(g_1)
    file_Header.close()
    
 
    #DDY File
    print "DDY File"
    file_DDY=open("SingleFloorRegular/02B_Size_WeatherData.idf","r")
    g_2=file_DDY.read()
    f.write(g_2)
    file_DDY.close()
    
    # Schedule file
    print "Schedule file"
    
    if Schedule=="Office":
        file_Schedule_Office=open("SingleFloorRegular/03A_Schedule_Office.idf","r")
        g_3=file_Schedule_Office.read()
        f.write(g_3)
        file_Schedule_Office.close()
    
    elif Schedule=="Retail":
        file_Schedule_Retail=open("SingleFloorRegular/03B_Schedule_Retail.idf","r")
        g_3=file_Schedule_Retail.read()
        f.write(g_3)
        file_Schedule_Retail.close()
    
    else:
        file_Schedule_Institute=open("SingleFloorRegular/03C_Schedule_Institute.idf","r")
        g_3=file_Schedule_Institute.read()
        f.write(g_3)
        file_Schedule_Institute.close()
    
    # Cool Roof
    print "Cool Roof file"
    
    if CoolRoof=="false":
        file_CoolRoof_Off=open("SingleFloorRegular/04A_CoolRoof_OFF.idf","r")
        g_4=file_CoolRoof_Off.read()
        f.write(g_4)
        file_CoolRoof_Off.close()
    else:
        file_CoolRoof_On=open("SingleFloorRegular/04B_CoolRoof_ON.idf","r")
        g_4=file_CoolRoof_On.read()
        f.write(g_4)
        file_CoolRoof_On.close()
    
  # Zones
    print "Zones"
    file_Zones=open("SingleFloorRegular/05_Zones.idf","r")
    g_5=file_Zones.read()
    f.write(g_5)
    file_Zones.close()
    
    # Gains
    print "Gains"
    file_Gains=open("SingleFloorRegular/06_Gains.idf","r")
    g_6=file_Gains.read()
    f.write(g_6)
    file_Gains.close()
    
   # Daylight
    print "Daylight"
    
    if DayLightSensor=="true": 
        file_DayLight_ON=open("SingleFloorRegular/07A_Daylight_ON.idf","r")
        g_7=file_DayLight_ON.read()
        f.write(g_7)
        file_DayLight_ON.close()
    else:
        file_DayLight_OFF=open("SingleFloorRegular/07B_Daylight_OFF.idf","r")
        g_7=file_DayLight_OFF.read()
        f.write(g_7)
        file_DayLight_OFF.close()
   
    
    # Internal Shades
    print "Internal Shades"
    
    if IntShades=="OFF":
        file_IntShade_OFF=open("SingleFloorRegular/08A_IntShade_OFF.idf","r")
        g_8=file_IntShade_OFF.read()
        f.write(g_8)
        file_IntShade_OFF.close()
    else:
        file_IntShade_ON=open("SingleFloorRegular/08A_IntShade_ON.idf","r")
        g_8=file_IntShade_ON.read()
        f.write(g_8)
        file_IntShade_ON.close()
    
   
    # HVAC
    print "HVAC"
    
    if HVAC=="PTHP": 
        file_HVAC_PTHP=open("SingleFloorRegular/09A_HVAC_PTHP.idf","r")
        g_9=file_HVAC_PTHP.read()
        f.write(g_9)
        file_HVAC_PTHP.close()
    elif HVAC=="CWC":
        file_HVAC=open("SingleFloorRegular/09B_HVAC_CWC.idf","r")
        g_9=file_HVAC.read()
        f.write(g_9)
        file_HVAC.close()
    else:
    
        file_HVAC=open("SingleFloorRegular/09C_HVAC_CAC.idf","r")
        g_9=file_HVAC.read()
        f.write(g_9)
        file_HVAC.close()

    # Economics
    print "Economics"
    file_Economics=open("SingleFloorRegular/10_Economics.idf","r")
    g_10=file_Economics.read()
    f.write(g_10)
    file_Economics.close()
 
    # Output
    print "Output"
    file_Output=open("SingleFloorRegular/11_Output.idf","r")
    g_11=file_Output.read()
    f.write(g_11)
    file_Output.close()
   
    f.close()
    
    print "Finish"




#/////////////////////////////////////////////////////////////////////////////////////////////


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


#////////////////////////////////////////////////////////////////////////////////////////////////////
def ProcessSingleFloorRegular():
    GenerateTemplateSingleFloorRegular(BuildingType,CoolRoof,DaylightCtrl,ShadingCtrl,HVAC_Type)
    filename ='temp.idf'
    #print HAVC_Type
    angle=40 #Dummy Variable for flow of code
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



def ProcessMultiFloorRegular():

    GenerateTemplateMultiFloorRegular(BuildingType,CoolRoof,DaylightCtrl,ShadingCtrl,HVAC_Type)
    filename ='temp.idf'
    angle=40 #Dummy Variable for flow of code
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

#//////////////////////////////////////////////////////////////////////////////////////////////////

def ProcessSingleFloorRegular_2():    

    area = Area
    AR = Aspect_Ratio
    B_W= math.sqrt(area/AR)
    
    B_L= AR * B_W
    
    
    B_H=3.0
    Wall_H=B_H
    print("Building Lenght =","{0:.2f}".format(B_L))
    print("Building Width =","{0:.2f}".format(B_W))
    
    print "For Example you can enter Example window width 1.8 m"
    Win_W = WindowWidthP
    #Win_S = float(input('Sill Height (m): '))
    
    print "For Example you can enter Example window width 0.75 m"
    Win_S = SilHeight
    #Win_S = 0.75 # Fixed sill height 0.75 m
    
    print "For Example you can enter window height 1.5 m"
    Win_H = WindowHeight
    
    Win_Lintel = Wall_H-Win_S-Win_H
    
    wwr_max= (Win_H)/Wall_H
    
    print "Maximum allowed WWR is - ",wwr_max
    
    wwr = Wwr
    
    if wwr<wwr_max or wwr == wwr_max:
    
    
        Wall=["Front_Wall", "Back_Wall","Left_Wall", "Right_Wall"]
        
        Wall_dict={}
        
        l=[]
        l.append(B_L)
        l.append(B_L)
        l.append(B_W)
        l.append(B_W)
        
        
        #WindowIDF=open("Window_IDF.idf",'w+')
        #ShadeIDF=open("Shade_IDF.idf",'w+')
        
        #Front Wall
        
        print "\n\n"
        
        Wall_Win("N_Wall",Wall_H,B_L,Win_S,Win_W, Win_H)
        
        
        #Back Wall
        
        print "\n\n"
        Wall_Win("S_Wall",Wall_H,B_L,Win_S,Win_W, Win_H)
        
        #Left Wall
        print "\n\n"
        Wall_Win("E_Wall",Wall_H,B_W,Win_S,Win_W, Win_H)
        
        #Right Wall
        print "\n\n"
        Wall_Win("W_Wall",Wall_H,B_W,Win_S,Win_W, Win_H)
        
        WindowIDF.close()
        ShadeIDF.close()
        
        # Merge files 
        
        s=open("temp.idf",'r')
        t=open("Window_IDF.idf",'r')     
        v=open("Shade_IDF.idf",'r')
        u=open("b.idf",'w')
        
        text1=s.read()
        text2=t.read()
        text3=v.read()
        
        u.write(text1)
        u.write(text2)
        u.write(text3)
    
    
        s.close()
        t.close()
        u.close()
        v.close()
    
    else:
        print "WWR condtion failed"
    
    





#/////////////////////////////////////////////////////////////////////////////////////////////////////



# Main starts here

if WindowType == "Regular":
#////////////////////////////////
    WindowIDF=open("Window_IDF.idf",'w+')
    ShadeIDF=open("Shade_IDF.idf",'w+')
    
    if Floors == 1:
    
        ProcessSingleFloorRegular()
        ProcessSingleFloorRegular_2()
        print "Finish single floor"
    
    elif Floors == 2:
        #Second Floor model is not ready yet.
        Floors = 3
        ProcessMultiFloorRegular()
    
    else:
    
        ProcessMultiFloorRegular()

    # Run EnergyPlus
    filename ='b.idf'
    #RunSimulations(filename)
    
    # # Fetch EnergySimualtion resutls
    
    #FetchResutls()
    
    #CleanFiles()
    
    WindowIDF.close()
    ShadeIDF.close()    
    print ("Process Completed")


#//////////////////////////////////////////////////////
else:
    #//////////////WindowType == "Strip" /////////////////
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

#//////////////////////////////////////////////////
