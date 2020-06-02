
#******************SOURCE******************
pythonFilePath = 'D:/mcantat_BDD/projects/code/maya/' 
import sys
sys.path.append( pythonFilePath )
#******************SOURCE******************

'''
cPlusPlusVersion = 1
#FOR TEST
import maya.cmds as mc

path     = 'D:/mcantat_BDD/projects/code/maya/python/plugIn/dynamicSkin.py'
nodeType = 'dynamicSkin'

if( cPlusPlusVersion == 1 ):
    path = 'D:\mcantat_BDD\Travail\code\maya\\node\c++\mayaNode\dynamicSkin\Build\Debug\dynamicSkin.mll'
    nodeType = 'dynamicSkin'  
    fileName = 'dynamicSkin'


mc.file( new = True , f = True )
mc.loadPlugin( path , qt = True )   
'''



import maya.cmds as mc
import python
from python.plugIn.utilsMayaNodesBuild import *



cPlusPlusVersion = 1


path     = 'D:/mcantat_BDD/projects/code/maya/python/plugIn/dynamicSkin.py'
nodeType = 'dynamicSkin'

if( cPlusPlusVersion == 1 ):
    path = 'D:\mcantat_BDD\Travail\code\maya\\node\c++\mayaNode\dynamicSkin\Build\Debug\dynamicSkin.mll'
    nodeType = 'dynamicSkin'  
    fileName = 'dynamicSkin'


#NEW SCENE    
clean( path , nodeType)    
mc.loadPlugin( path  )
#BUILD LOCATORS
print('=== BUILD TEST ===')
inputGrp = mc.createNode( 'transform' , n = 'input' )
inBase = createPlaneTest( [ -5 , 0 , 2 ] , parent = inputGrp )
outMesh = createPlaneTest( [ 0 , 0 , 0 ] , parent = inputGrp )
#NEW SCENE    
mc.select( outMesh )
mc.cluster()
mc.select( outMesh )
newNode = mc.deformer(  type = nodeType )[0]     
#INPUT  
print('=== INPUT CONNECTIONS ===')   
mc.connectAttr( ( inBase + '.outMesh' ) , ( newNode + '.inBaseMesh' ) )
#mc.connectAttr( ( newNode + '.outputGeometry[0]' ) , ( outMesh + '.inMesh' ) , f = True )
#BUILD LOCATORS 

mc.deformerWeights('clusterTestWeight.xml', im=True, deformer='cluster1', path = 'D:/mcantat_BDD/projects/test/dynamics/')



mc.setAttr( newNode + '.envelope', 1 );
mc.setAttr( newNode + '.cache', 0 );
mc.setAttr( newNode + '.momentumPastSample', 1 );
mc.setAttr( newNode + '.momentumAverageSize', 1 );
mc.setAttr( newNode + '.friction', 1 );
mc.setAttr( newNode + '.mass', 0 );
mc.setAttr( newNode + '.bindElasticity', 1 );
mc.setAttr( newNode + '.pressure', 0 );
mc.setAttr( newNode + '.topoType', 0 );
mc.setAttr( newNode + '.nbrLinkEval', 1 );
mc.setAttr( newNode + '.linkElasticity', 1 );
mc.setAttr( newNode + '.linkRepulsion', 1 );
mc.setAttr( newNode + '.modeTopo', 3 );