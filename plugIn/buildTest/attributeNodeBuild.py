

import maya.cmds as mc



def testNode_create( path , nodeType ):   
    print('=== NEW SCENE ===')
    mc.file( new = True , f = True )
    mc.unloadPlugin( nodeType , f = True ) 
    print('=== LOAD PLUGIN ===') 
    mc.loadPlugin( path  )
    print('=== CREATE NODE ===')
    newNode = mc.createNode( nodeType )     
    return newNode
   
def createTestLocs( baseName , nbr , separationLength = 2 , parent = '' ):
    locators = []
    for i in range( 0 , nbr ):
        locTmp = mc.spaceLocator( n = ( baseName + str(i) ) ) 
        newLoc = locTmp[0]
        mc.setAttr( (newLoc + ".translateX") , ( i*separationLength ) )
        locators.append(newLoc) 
        if not( parent == '' ): mc.parent(  newLoc , parent )  
    return locators  

def createTestCubes( baseName , nbr , separationLength = 2 , parent = '' ):
    cubes = []
    for i in range( 0 , nbr ):
        objTmp = mc.polyCube( n = ( baseName + str(i) ) )   
        cube = objTmp[0]
        mc.setAttr( (cube + ".translateX") , ( i*separationLength ) )
        cubes.append(cube) 
        if not( parent == '' ): mc.parent(  cube , parent )  
    return cubes  


def createCubeTest( position , parent = '' ):
    objTmp = mc.polyCube()   
    cube = objTmp[0]
    mc.setAttr(( cube + '.tx' ) , position[0] )
    mc.setAttr(( cube + '.ty' ) , position[1] )    
    mc.setAttr(( cube + '.tz' ) , position[2] ) 
    if not( parent == '' ): mc.parent(  cube , parent )       
    return cube

def createCurveTest( name ,  parent = '' ):
    curveTrf = mc.createNode('transfrom' , n = name )    
    curveShape = mc.createNode('nurbsCurve' , parent = curveTrf )
    if not( parent == '' ): mc.parent(  curveTrf , parent )       
    return curveShape


path     = 'D:/mcantat_BDD/projects/code/maya/python/plugIn/attributeNode.py'
nodeType = "attributeNode"    
#NEW SCENE    
newNode = testNode_create( path , nodeType )
#BUILD LOCATORS
print('=== BUILD TEST ===')
inputGrp = mc.createNode( "transform" , n = "input" )
inputMatrixObjs = createTestLocs( "inputMatrices" , 6 , parent = inputGrp )
curveShape = createCurveTest( 'inputCurve' ,  parent = inputGrp )
lengthObj = createCubeTest( [ 0 , 0 , 0 ] , parent = inputGrp )
#INPUT  
print('=== INPUT CONNECTIONS ===')    
for i in range(0,len(inputMatrixObjs)):
    mc.connectAttr( ( inputMatrixObjs[i] + '.worldMatrix[0]' ) , ( newNode + '.matrices[{}]'.format(i) ) )
#BUILD LOCATORS
print('=== BUILD TEST ===')
outputGrp = mc.createNode( "transform" , n = "output" )
outputMatrixObjs = createTestCubes( "outputMatrices" , 6 , parent = outputGrp )
outputCurveShape = createCurveTest( 'outputCurve' ,  parent = inputGrp )
lengthObj = createCubeTest( [ 0 , 0 , 0 ] , parent = inputGrp )    
#OUTPUT
print('=== OUTPUT CONNECTIONS ===')
for i in range(0,len(outputMatrixObjs)):
    decomposeMatrixTmp = mc.createNode("decomposeMatrix")
    mc.connectAttr( ( newNode + '.outMatrices[{}]'.format(i) ) , (decomposeMatrixTmp + '.inputMatrix' ) )    
    mc.connectAttr( ( decomposeMatrixTmp + '.outputTranslate' ) , ( outputMatrixObjs[i] + '.translate' ) )
print('=== DONE ===')    
