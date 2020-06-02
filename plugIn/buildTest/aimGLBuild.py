
pathPythonFiles = 'D:/mcantat_BDD/projects/code/maya/' 
#__________________________ NODE INFO
nodeType       = 'aimGL'  
useNodeCpp    = 1
highPoly      = 1
releaseMode   = 0
pathNodePython = 'NONE'
releaseFolder = ['Debug','Release']
pathNodeCpp    = 'D:\mcantat_BDD\projects\code\maya\c++\mayaNode\\aimGL\Build\{}\\aimGL.mll'.format( releaseFolder[releaseMode] )
#__________________________ BUILD TEST INFO
lodSuffixs = [ 'Low' , 'High' ]
pathBuildTest = 'D:/mcantat_BDD/projects/nodeTest/aimGLBuildTest.ma'

print( 'BUILD TEST __________________________ SOURCE')
import sys
sys.path.append( pathPythonFiles )
import python
import maya.cmds as mc
from python.plugIn.utilsMayaNodesBuild import *

pathNode   = [ pathNodePython , pathNodeCpp ][useNodeCpp]
if( mc.objExists("locator1") ):
    mc.file( new = True, f= True  )
    clean( pathNode , nodeType)
    mc.error("****CLEAN FOR RECOMPILING NODE*****")
    
print( 'BUILD TEST __________________________ PREPARE SCENE')

clean( pathNode , nodeType)
mc.file( pathBuildTest , i = True )

visTrigGeo = "pCube1"

print( 'BUILD TEST __________________________ LOAD NODE')
mc.loadPlugin( pathNode  )

print( 'BUILD TEST __________________________ CREATE NODE')
newNode = mc.createNode( nodeType ) 

print( 'BUILD TEST __________________________ CONNECT IN')
mc.connectAttr( 'locator1.worldMatrix[0]'  , '{}.orig'.format( newNode )  )
mc.connectAttr( 'locator2.worldMatrix[0]'  , '{}.target'.format( newNode )  )
mc.connectAttr( 'locator3.worldMatrix[0]'  , '{}.up'.format( newNode )  )


print( 'BUILD TEST __________________________ CONNECT OUT')
mc.connectAttr( ( newNode + '.outTrig' ) , ( visTrigGeo + '.visibility' ) )

print( 'BUILD TEST __________________________ SET ATTR')


print( 'BUILD TEST __________________________ DONE')
mc.select(newNode)



