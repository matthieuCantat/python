

import maya.cmds as mc



def clean( path , nodeType):   
    print('=== NEW SCENE ===')
    mc.file( new = True , f = True )
    mc.unloadPlugin( nodeType , f = True ) 
    print('=== LOAD PLUGIN ===') 
    mc.loadPlugin( path  )
     
   
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
    shape = mc.listRelatives( cube , c = True , s = True )
    return shape[0]

def createCurveTest( name ,  parent = '' ):
    curveTrf = mc.createNode('transfrom' , n = name )    
    curveShape = mc.createNode('nurbsCurve' , parent = curveTrf )
    if not( parent == '' ): mc.parent(  curveTrf , parent )       
    return curveShape


path     = 'D:/mcantat_BDD/projects/code/maya/python/plugIn/simpleBlendShape.py'
nodeType = "simpleBlendShape"    
#NEW SCENE    
newNode = clean( path , nodeType)
#BUILD LOCATORS
print('=== BUILD TEST ===')
inputGrp = mc.createNode( "transform" , n = "input" )
inTarget = createCubeTest( [ -5 , 0 , 0 ] , parent = inputGrp )
inBase = createCubeTest( [ -5 , 0 , 2 ] , parent = inputGrp )
outMesh = createCubeTest( [ 0 , 0 , 0 ] , parent = inputGrp )
#NEW SCENE    
mc.select( outMesh )
newNode = mc.deformer(  type = nodeType )   
#INPUT  
print('=== INPUT CONNECTIONS ===')    
mc.connectAttr( ( inTarget + '.outMesh' ) , ( newNode + '.inTargetMesh' ) )
mc.connectAttr( ( inBase + '.outMesh' ) , ( newNode + '.inBaseMesh' ) )
mc.connectAttr( ( newNode + '.outputGeometry[0]' ) , ( outMesh + '.inMesh' ) , f = True )
#BUILD LOCATORS 
