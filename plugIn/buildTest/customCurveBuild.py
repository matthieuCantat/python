
pathPythonFiles = 'D:/mcantat_BDD/projects/code/maya/' 
#__________________________ NODE INFO
nodeType       = 'customCurve'  
useNodeCpp    = 1
highPoly      = 1
releaseMode   = 0
pathNodePython = 'NONE'
releaseFolder = ['Debug','Release']
pathNodeCpp    = 'D:\mcantat_BDD\projects\code\maya\c++\mayaNode\customCurve\Build\{}\customCurve.mll'.format( releaseFolder[releaseMode] )
#__________________________ BUILD TEST INFO
lodSuffixs = [ 'Low' , 'High' ]
pathBuildTest = 'D:/mcantat_BDD/projects/nodeTest/customCurveBuildTest.ma'

print( 'BUILD TEST __________________________ SOURCE')
import sys
sys.path.append( pathPythonFiles )
import python
import maya.cmds as mc
from python.plugIn.utilsMayaNodesBuild import *


if( mc.objExists("locator1") ):
    mc.file( new = True, f= True  )
    clean( pathNode , nodeType)
    mc.error("****CLEAN FOR RECOMPILING NODE*****")
    
print( 'BUILD TEST __________________________ PREPARE SCENE')
pathNode   = [ pathNodePython , pathNodeCpp ][useNodeCpp]
clean( pathNode , nodeType)
mc.file( pathBuildTest , i = True )

drivers    = mc.ls( "locator*" , type = "transform" )
curve      = mc.curve( n = "curveOut" , d = 3 , p=[(0, 0, 0), (1, 0, 0), (2, 0, 0), (3, 0, 0)] , k=[ 0 , 0 , 0 , 1 , 1 , 1 ] ) ;
curveShape = mc.listRelatives( curve , s = True , c = True )[0]

print( 'BUILD TEST __________________________ LOAD NODE')
mc.loadPlugin( pathNode  )

print( 'BUILD TEST __________________________ CREATE NODE')
newNode = mc.createNode( nodeType ) 

print( 'BUILD TEST __________________________ CONNECT IN')
for i in range( 0 , len( drivers ) ) :
	mc.connectAttr( ( drivers[i] + '.worldMatrix[0]' )  , '{}.matrices[{}]'.format( newNode , i)  )

print( 'BUILD TEST __________________________ CONNECT OUT')
mc.connectAttr( ( newNode + '.curve' ) , ( curveShape + '.create' ) )  

print( 'BUILD TEST __________________________ SET ATTR')
mc.setAttr( newNode + '.mode'     , 0)
mc.setAttr( newNode + '.degree'   , 3)
mc.setAttr( newNode + '.isClose'  , 0)
mc.setAttr( newNode + '.offsetAxe', 1)
mc.setAttr( newNode + '.offset'   , 0)

print( 'BUILD TEST __________________________ DONE')
mc.select(newNode)



mc.setAttr( "curveShape1.lineWidth" , 5)