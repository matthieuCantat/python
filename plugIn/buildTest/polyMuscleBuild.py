
pathPythonFiles = 'D:/mcantat_BDD/projects/code/maya/' 
#__________________________ NODE INFO
nodeType       = 'meshWrap'  
useNodeCpp    = 1
highPoly      = 1
releaseMode   = 1
pathNodePython = 'NONE'
releaseFolder = ['Debug','Release']
pathNodeCpp    = 'D:\mcantat_BDD\projects\code\maya\c++\mayaNode\meshWrap\Build\{}\meshWrap.mll'.format( releaseFolder[releaseMode] )
#__________________________ BUILD TEST INFO
lodSuffixs = [ 'Low' , 'High' ]
pathBuildTest = 'D:/mcantat_BDD/projects/nodeTest/meshWrapBuildTest{}.ma'.format(lodSuffixs[highPoly])

print( 'BUILD TEST __________________________ SOURCE')
import sys
sys.path.append( pathPythonFiles )
import python
import maya.cmds as mc
from python.plugIn.utilsMayaNodesBuild import *


if( mc.objExists("mesh_GEO") ):
    mc.file( new = True, f= True  )
    clean( pathNode , nodeType)
    mc.error("****CLEAN FOR RECOMPILING NODE*****")
    
print( 'BUILD TEST __________________________ PREPARE SCENE')
pathNode   = [ pathNodePython , pathNodeCpp ][useNodeCpp]
clean( pathNode , nodeType)
mc.file( pathBuildTest , i = True )

cage     = 'cage_GEO'
cageBase = 'cageBase_GEO'
mesh     = 'mesh_GEO'
meshBase = 'meshBase_GEO'

cageShape     = mc.listRelatives( cage     , c = True , s = True )[0]
cageBaseShape = mc.listRelatives( cageBase , c = True , s = True )[0]
meshShape     = mc.listRelatives( mesh     , c = True , s = True )[0]
meshBaseShape = mc.listRelatives( meshBase , c = True , s = True )[0]

print( 'BUILD TEST __________________________ LOAD NODE')
mc.loadPlugin( pathNode  )

print( 'BUILD TEST __________________________ CREATE NODE')
mc.select(mesh)
newNode = mc.deformer( type = nodeType )[0]  

print( 'BUILD TEST __________________________ CONNECT IN')
mc.connectAttr( ( cageShape      + '.worldMesh[0]' )  , ( newNode + '.cage'     ) )
mc.connectAttr( ( cageBaseShape  + '.worldMesh[0]' )  , ( newNode + '.cageBase' ) )
mc.connectAttr( ( meshBaseShape  + '.worldMesh[0]' )  , ( newNode + '.meshBase' ) )
print( 'BUILD TEST __________________________ CONNECT OUT')
#mc.connectAttr( ( newNode + '.outMesh' ) , ( meshShape + '.inMesh' ) )  

print( 'BUILD TEST __________________________ SET ATTR')
mc.setAttr( newNode + '.envelope', 1)
mc.setAttr( newNode + '.cache', 1)

print( 'BUILD TEST __________________________ DONE')
mc.select(newNode)
