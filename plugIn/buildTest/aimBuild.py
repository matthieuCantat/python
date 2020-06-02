
pathPythonFiles = 'D:/mcantat_BDD/projects/code/maya/' 
#__________________________ NODE INFO
nodeType       = 'aim'  
useNodeCpp    = 1
highPoly      = 1
releaseMode   = 0
pathNodePython = 'NONE'
releaseFolder = ['Debug','Release']
pathNodeCpp    = 'D:\mcantat_BDD\projects\code\maya\c++\mayaNode\\aim\Build\{}\\aim.mll'.format( releaseFolder[releaseMode] )
#__________________________ BUILD TEST INFO
lodSuffixs = [ 'Low' , 'High' ]
pathBuildTest = 'D:/mcantat_BDD/projects/nodeTest/aimBuildTest.ma'

print( 'BUILD TEST __________________________ SOURCE')
import sys
sys.path.append( pathPythonFiles )
import python
import maya.cmds as mc
from python.plugIn.utilsMayaNodesBuild import *


if( mc.objExists("target") ):
    mc.file( new = True, f= True  )
    clean( pathNode , nodeType)
    clean( pathNodeB , nodeTypeB)
    mc.error("****CLEAN FOR RECOMPILING NODE*****")
    
print( 'BUILD TEST __________________________ PREPARE SCENE')
pathNode   = [ pathNodePython , pathNodeCpp ][useNodeCpp]
clean( pathNode , nodeType)
mc.file( pathBuildTest , i = True )

print( 'BUILD TEST __________________________ LOAD NODE')
mc.loadPlugin( pathNode  )

print( 'BUILD TEST __________________________ CREATE NODE')
newNode = mc.createNode( nodeType ) 

print( 'BUILD TEST __________________________ CONNECT IN')

slave = 'joint2'
target = 'target'
up = 'up'

mc.connectAttr( slave + '.parentMatrix[0]'      , newNode+'.origParent' , f = True )
mc.connectAttr( slave + '.translate'            , newNode+'.origTranslate'   , f = True )
mc.connectAttr( slave + '.rotatePivotTranslate' , newNode+'.origRotatePivotTranslate'   , f = True )
mc.connectAttr( slave + '.rotatePivot'          , newNode+'.origRotatePivot'   , f = True )
mc.connectAttr( slave + '.jointOrient'          , newNode+'.origJointOrient'   , f = True )
mc.setAttr( newNode+'.origRotate'          , mc.getAttr(slave + '.rotate' )[0][0], mc.getAttr(slave + '.rotate' )[0][1], mc.getAttr(slave + '.rotate' )[0][2] , type = "double3"   )
mc.connectAttr( slave + '.rotateAxis'           , newNode+'.origRotateAxis'   , f = True )
mc.connectAttr( slave + '.rotateOrder'          , newNode+'.origRotateOrder'   , f = True )

mc.connectAttr( target+'.worldMatrix[0]' , newNode+'.target' , f = True )
mc.connectAttr( up+'.worldMatrix[0]'     , newNode+'.up'     , f = True )

print( 'BUILD TEST __________________________ CONNECT OUT')
mc.connectAttr( newNode+'.outRotation' , slave + '.rotate'  , f = True )

print( 'BUILD TEST __________________________ SET ATTR')

print( 'BUILD TEST __________________________ DONE')
mc.select(newNode)







pathPythonFiles = 'D:/mcantat_BDD/projects/code/maya/' 
#__________________________ NODE INFO
nodeTypeB       = 'glDraw'  
useNodeCpp    = 1
highPoly      = 1
releaseMode   = 0
pathNodePython = 'NONE'
releaseFolder = ['Debug','Release']
pathNodeCpp    = 'D:\mcantat_BDD\projects\code\maya\c++\mayaNode\glDraw\Build\{}\glDraw.mll'.format( releaseFolder[releaseMode] )
#__________________________ BUILD TEST INFO
lodSuffixs = [ 'Low' , 'High' ]
pathBuildTest = 'D:/mcantat_BDD/projects/nodeTest/glDrawBuildTest.ma'


print( 'BUILD TEST __________________________ PREPARE SCENE')
pathNodeB   = [ pathNodePython , pathNodeCpp ][useNodeCpp]

camera = "persp"
visTrigGeo = "pCube1"

print( 'BUILD TEST __________________________ LOAD NODE')
mc.loadPlugin( pathNodeB  )

print( 'BUILD TEST __________________________ CREATE NODE')
drawNode = mc.createNode( nodeTypeB ) 

print( 'BUILD TEST __________________________ CONNECT IN')
mc.connectAttr( ( camera + '.worldMatrix[0]' )  , '{}.camMatrix'.format( drawNode )  )
mc.connectAttr( ( newNode + '.outDraw' )  , '{}.inDraw'.format( drawNode )  )

print( 'BUILD TEST __________________________ CONNECT OUT')
mc.connectAttr( ( drawNode + '.outTrig' ) , ( visTrigGeo + '.visibility' ) )

print( 'BUILD TEST __________________________ SET ATTR')

print( 'BUILD TEST __________________________ DONE')
mc.select(drawNode)



