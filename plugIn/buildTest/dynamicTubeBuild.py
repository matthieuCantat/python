
#******************SOURCE******************
pythonFilePath = 'D:/mcantat_BDD/projects/code/maya/' 
import sys
sys.path.append( pythonFilePath )
#******************SOURCE******************


import maya.cmds as mc
import python
from python.plugIn.utilsMayaNodesBuild import *


cPlusPlusVersion = 1
nbrTest = 10



path = 'D:\mcantat_BDD\projects\code\maya\python\plugIn\dynamicTube.py'
nodeType = 'dynamicTube'  
fileName = 'dynamicTube'

if( cPlusPlusVersion == 1 ):
    path = 'D:\mcantat_BDD\Travail\code\maya\\node\c++\mayaNode\dynamicTube\Build\Debug\dynamicTube.mll'
    nodeType = 'dynamicTube'  
    fileName = 'dynamicTube'

#NEW SCENE
clean( path , nodeType)    
mc.loadPlugin( path  )
newNode = mc.createNode( nodeType )  
#BUILD LOCATORS
print('=== BUILD TEST ===')
inputMatrixObjsA = createCubeTest( [ 0 , 0 , 0 ] , returnTransform = True  )
inputMatrixObjsB = createCubeTest( [ nbrTest , 0 , 0 ] , returnTransform = True  )
planeCollision = createPlaneTest( [ 5 , -1 , 5 ] , returnTransform = True )
sphereCollision = createSphereTest( [ 7 , 0 , 7 ] , returnTransform = True )

outputMatrixObjs = []
for i in range( 0 , nbrTest ):
    outputMatrixObjs.append( createSphereTest( [ 0 , 0 , 0 ] , returnTransform = True ) )

#INPUT  
print('=== INPUT CONNECTIONS ===')    
mc.connectAttr( ( inputMatrixObjsA + '.translate' ) , ( newNode + '.inputPointA' ) )
mc.connectAttr( ( inputMatrixObjsB + '.translate' ) , ( newNode + '.inputPointB' ) )
mc.connectAttr( ( planeCollision + '.translate' )   , ( newNode + '.pointPlaneCollision' ) )
mc.connectAttr( ( sphereCollision + '.translate' ) , ( newNode + '.pointSphereCollision' ) )
mc.connectAttr( ( sphereCollision + '.scaleX' ) , ( newNode + '.raySphereCollision' ) )
#OUTPUT
print('=== OUTPUT CONNECTIONS ===')
mc.setAttr( 'dynamicTube1.nbrSamples', nbrTest)
for i in range( 0 , len(outputMatrixObjs) ):
    mc.connectAttr( ( newNode + '.outPoints['+str(i)+']' ) , ( outputMatrixObjs[i] + '.translate' ) )  
print('=== DONE ===')    

mc.setAttr( newNode + '.nbrLinkEval', 5)
mc.setAttr( newNode + '.momentumPastSample', 7)
mc.setAttr( newNode + '.momentumAverageSize', 7)
mc.setAttr( newNode + '.friction', 0.1)
mc.setAttr( newNode + '.mass', 0.01)
mc.setAttr( newNode + '.length', 1)
mc.setAttr( newNode + '.elasticity', 1)
mc.setAttr( newNode + '.repulsion', 1)
mc.setAttr( newNode + '.init', 1)
mc.setAttr( newNode + '.edgeLengthPower', 0)
mc.setAttr( newNode + '.addPower', 0)
mc.setAttr( newNode + '.smoothPower', 0)
mc.setAttr( newNode + '.relaxPower', 1)