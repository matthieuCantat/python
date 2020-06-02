

'''


pathPythonFiles = 'D:/mcantat_BDD/projects/code/maya/' 
#__________________________ NODE INFO
nodeType       = 'getFrontOfChainSculpt'  
useNodeCpp    = 1
highPoly      = 1
releaseMode   = 0
pathNodePython = 'NONE'
releaseFolder = ['Debug','Release']
pathNodeCpp    = 'D:\mcantat_BDD\projects\code\maya\c++\mayaNode\\getFrontOfChainSculpt\Build\{}\\getFrontOfChainSculpt.mll'.format( releaseFolder[releaseMode] )
#__________________________ BUILD TEST INFO
pathNode   = [ pathNodePython , pathNodeCpp ][useNodeCpp]
mc.loadPlugin( pathNode  )


mc.getFrontOfChainSculpt( "sculpt" , "deform" , "base") 


'''


pathPythonFiles = 'D:/mcantat_BDD/projects/code/maya/' 
#__________________________ NODE INFO
nodeType       = 'getFrontOfChainSculpt'  
useNodeCpp    = 1
highPoly      = 1
releaseMode   = 0
pathNodePython = 'NONE'
releaseFolder = ['Debug','Release']
pathNodeCpp    = 'D:\mcantat_BDD\projects\code\maya\c++\mayaNode\\getFrontOfChainSculpt\Build\{}\\getFrontOfChainSculpt.mll'.format( releaseFolder[releaseMode] )
#__________________________ BUILD TEST INFO
lodSuffixs = [ 'Low' , 'High' ]
pathBuildTest = 'D:/mcantat_BDD/projects/nodeTest/getFrontOfChainSculptBuildTest.ma'

print( 'BUILD TEST __________________________ SOURCE')
import sys
sys.path.append( pathPythonFiles )
import python
import maya.cmds as mc
from python.plugIn.utilsMayaNodesBuild import *


if( mc.objExists("sculpt") ):
    mc.file( new = True, f= True  )
    clean( pathNode , nodeType)
    mc.error("****CLEAN FOR RECOMPILING NODE*****")
    
print( 'BUILD TEST __________________________ PREPARE SCENE')
pathNode   = [ pathNodePython , pathNodeCpp ][useNodeCpp]
clean( pathNode , nodeType)
mc.file( pathBuildTest , i = True )

print( 'BUILD TEST __________________________ LOAD NODE')
mc.loadPlugin( pathNode  )

print( 'BUILD TEST __________________________ CREATE NODE')
mc.getFrontOfChainSculpt( "sculpt" , "deform" , "base") 
