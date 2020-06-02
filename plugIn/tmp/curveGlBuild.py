
#******************SOURCE******************
pythonFilePath = 'D:/mcantat_BDD/projects/code/maya/' 
import sys
sys.path.append( pythonFilePath )
#******************SOURCE******************


import maya.cmds as mc
import python
from python.plugIn.utilsMayaNodesBuild import *


cPlusPlusVersion = 0



path = 'D:\mcantat_BDD\projects\code\maya\python\plugIn/curveGl.py'
nodeType = 'curveGl'  
fileName = 'curveGl'


#NEW SCENE
clean( path , nodeType )    
mc.loadPlugin( path  )
newNode = mc.createNode( nodeType )  
#BUILD LOCATORS
print('=== BUILD TEST ===')
locs = createLocTest(  5 , separationLength = 5 )
cube = createCubeTest( [0,0,0] , parent = '' , returnTransform = True  )
#INPUT  
print('=== INPUT CONNECTIONS ===')    
mc.connectAttr( ( 'persp.worldMatrix' ) , ( newNode + '.inCamMatrix' ) )

for i in range(0,len(locs)):
	mc.connectAttr( ( locs[i] + '.translate' ) , ( newNode + '.coords[{}]'.format(i) ) )
	if( i%2 != 0 ):
		mc.setAttr( locs[i] + '.translateY' , 5 )

mc.connectAttr( ( newNode + '.outTrig' ) , ( cube + '.visibility' ) )

#OUTPUT
mc.setAttr( ( newNode + '.thickness') , 3.0 )
mc.setAttr( ( newNode + '.color') , 1,1,0 )

