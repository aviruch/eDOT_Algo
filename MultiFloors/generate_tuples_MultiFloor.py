import math
import re
import itertools
import sys

#### define static params ######
floors = 10;

zonemultiplier = floors - 2;


#Area in square meter
Area=1000.0;
Height=3.0;

def load_params_ranges(filename):
	f=open(filename,'r');
	params_dict={};
	for line in f:
		line=line.replace('\r\n','');
		line=line.replace('\n','');
		line=line.replace(';','');
		line=line.split(',');
		token=line[0];
		if token:
			values=line[1:];
			values=[float(i) for i in values];
			params_dict[token]=values;
	print params_dict;
	return params_dict;

def modify_params(params_dict):
	cost=params_dict['cost_glass'];
	U_value=params_dict['U_value'];
	shgc=params_dict['Shgc'];
	Vlt=params_dict['Vlt'];
	glass_dict=[];
	try:
		for i in range(len(shgc)):
			glass=(shgc[i],Vlt[i],U_value[i],cost[i]);
			glass_dict.append(glass);
	except:
		raise ValueError;
	params_dict.pop('cost_glass',None);
	params_dict.pop('U_value',None);
	params_dict.pop('Shgc',None);
	params_dict.pop('Vlt',None);
	params_dict['glass']=glass_dict;

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

def generate_idf(param,filename):
	Aspect_Ratio= param['Aspect_Ratio'];
	Wwr= 1.0*param['Wwr'] / 100;
	Orientation = param['Orientation'];
	#breadth=math.sqrt(float(Area)/float(Aspect_Ratio));
	#length=Aspect_Ratio*breadth;
	
	#length,breadth = breadth,length

	angle= param['Overhang'];
	glass= param['Glass'];
	
	#window_height=Wwr*Height;
	#overhang_depth=math.tan(angle*3.14/180) * window_height;
	
	RQ_VAL=generate_co(Orientation,Area,Aspect_Ratio,Wwr,glass,angle);


	f=open('MultiFloorTemplate.idf');
	w=open(filename,'w');
	for line in f:
		sets=re.findall(r'#.*?[,;]',line);
		for j in sets:
			j=j[:-1];
			line=line.replace(j,str(RQ_VAL[j]));

		w.write(line);
	w.close();

def generate_combinations(params):
	combinations = itertools.product(params['Orientation'],params['Wwr'],params['glass'],params['Aspect_Ratio'],params['Overhang']);
	f=open('details.txt','w');
	sys.stdout=f;
	count=1;
	print "Index Orientation WWR Glass Aspect_Ratio Overhang "
	for i in combinations:
		print count,i[0],i[1],i[2],i[3],i[4]
		param={};
		param['Aspect_Ratio'] = i[3]
		param['Wwr'] = i[1]
		param['Orientation'] = i[0] 
		param['Overhang'] = i[4]
		param['Glass'] = i[2] 
		filename = 'IDF/file_'+str(count) +'.idf' ;
		generate_idf(param,filename);
		count=count+1
		print i;
	sys.stdout=1;

print "start"
params=load_params_ranges('params.txt');
print "Done load ranges"
modify_params(params);
print "modifiy params"
generate_combinations(params)
print "combination generatedd"

