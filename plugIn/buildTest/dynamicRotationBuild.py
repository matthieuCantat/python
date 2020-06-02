
#******************SOURCE******************
pythonFilePath = 'D:/mcantat_BDD/projects/code/maya/' 
import sys
sys.path.append( pythonFilePath )
#******************SOURCE******************


import maya.cmds as mc
import python
from python.plugIn.utilsMayaNodesBuild import *


cPlusPlusVersion = 0

path = 'D:\mcantat_BDD\projects\code\maya\python\plugIn\dynamicRotationLimit.py'
nodeType = "dynamicRotation"  
fileName = "dynamicRotation"

if( cPlusPlusVersion == 1 ):
    path = 'D:\mcantat_BDD\Travail\code\maya\\node\c++\mayaNode\dynamicTube\Build\Debug\dynamicTrs.mll'
    nodeType = "dynamicRotation"  
    fileName = "dynamicRotationLimit"

#NEW SCENE
clean( path , nodeType )    
mc.loadPlugin( path  )
newNode = mc.createNode( nodeType )  
#BUILD LOCATORS
print('=== BUILD TEST ===')
locs = createTestLocs( 'driver' ,1 )
cube = createCubeTest( [ 0 , 0 , 0 ] , returnTransform = True )


#INPUT  
print('=== INPUT CONNECTIONS ===')    
mc.connectAttr( ( locs[0] + '.worldMatrix' ) , ( newNode + '.worldMatrix' ) )
mc.connectAttr( ('time1.outTime' ) , ( newNode + '.time' ) )
#OUTPUT
print('=== OUTPUT CONNECTIONS ===')

for axe in ['X','Y','Z']:
    mc.connectAttr( ( newNode + '.outTranslate' + axe ) , ( cube + '.translate' + axe ) )
    mc.connectAttr( ( newNode + '.outRotate' + axe ) , ( cube + '.rotate' + axe ) )
    mc.connectAttr( ( newNode + '.outScale' + axe ) , ( cube + '.scale' + axe ) )
print('=== DONE ===')    

mc.setAttr( newNode + '.activate'  , 1)
mc.setAttr( newNode + '.mass'     , 0.1)
mc.setAttr( newNode + '.elasticity', 0.1)
mc.setAttr( newNode + '.damping'   , 0.1)
mc.setAttr( newNode + '.collision' , 0)