

Sytesm Argument must be in order Area(sqm), Weatherfile, BuildingType, HvacType, Daylight, CoolRoof, IntShadeCtrl, Floors, WindowType, 
WWR, WindowHeight,WindowWidthP,SillHeight,GlassU, SHGC, VLT, Orientation, OverHangDegree, OverHangDepth, AR, RoofInsulation, WallInsulation. 



Sample input

test 1
python MainFile_v6.py 1000 IND_Ahmedabad.426470_ISHRAE.epw Office PTHP ON OFF OnHighSolar 10 Strip 0.5 0 0 0 0.351 0.5 0.2 0 30 0 2 0 0

test 2
python MainFile_v6.py 1000 IND_Ahmedabad.426470_ISHRAE.epw Office CWC ON OFF OnHighSolar 10 Strip 0.5 0 0 0 0.351 0.5 0.2 0 30 0 2 0 0


python MainFile_v4.py Area:1000 Weatherfile:IND_Ahmedabad.426470_ISHRAE.epw BuildignType:Office Hvac_Type:PTHP Daylight:ON 
CoolRoof:OFF IntShadeCtrl:OnHighSolar Floors:10 WindowType:Strip WWR:0.5 WindowHeight:NA WindowWidhtP:NA SillHeight:NA
GlassU:0.351 SHGC:0.5 VLT:0.2 Orientation:0 OverHangDegree:30 OverHangDepth:NA AR:2 RoofInsulation:0 WallInsulation:0


energyplus -w IND_Ahmedabad.426470_ISHRAE.epw -p ./Output/b -s C -x -m -r b_86.idf




python MainFile_v6.py 1000 IND_Ahmedabad.426470_ISHRAE.epw Office PTHP true false OnHighSolar 10 Strip 0.5 0 0 0 0.351 0.5 0.2 0 30 2 0 0

python MainFile_v9_local.py 1000 IND_Ahmedabad.426470_ISHRAE.epw Office PTHP true false OnHighSolar 10 Strip 0.5 0 0 0 0.351 0.5 0.2 0 30 2 0 0


Test Case for Regular window

python MainFile_v10_local.py 1000 IND_Ahmedabad.426470_ISHRAE.epw Office PTHP true false OnHighSolar 1 Regular 0.5 1 1 1 0.351 0.5 0.2 0 0 2 0 0
