

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
    
def createLocTest( nbr , separationLength = 2 ):
    locators = []
    for i in range( 0 , nbrCtrl ):
        locTmp = mc.spaceLocator() 
        newLoc = locTmp[0]
        mc.setAttr( (newLoc + ".translateX") , ( i*separationLength ) )
        locators.append(newLoc)   
    return locators  

def createCubeTest( position ):
    objTmp = mc.polyCube()   
    cube = objTmp[0]
    mc.setAttr(( cube + '.tx' ) , position[0] )
    mc.setAttr(( cube + '.ty' ) , position[1] )    
    mc.setAttr(( cube + '.tz' ) , position[2] )  
    return cube



path     = 'D:\mcantat_BDD\projects\code\maya\python\plugIn\curveNode.py'
nodeType = "curveNode"    
#NEW SCENE    
newNode = testNode_create( path , nodeType )
#BUILD LOCATORS
print('=== BUILD TEST ===')
inputMatrixObjs = createLocTest( nbr = 6 ) 
curveShape = mc.createNode('nurbsCurve') 
lengthObj = createCubeTest( [ 10 , 0 , 10 ] )
#INPUT  
print('=== INPUT CONNECTIONS ===')    
for i in range(0,len(inputMatrixObjs)):
    mc.connectAttr( ( inputMatrixObjs[i] + '.worldMatrix[0]' ) , ( newNode + '.inputMatrix[{}]'.format(i) ) )
#OUTPUT
print('=== OUTPUT CONNECTIONS ===')
mc.connectAttr( ( newNode + '.length' ) , ( lengthObj + '.ty' ) )    
mc.connectAttr( ( newNode + '.outCurve' ) , ( curveShape + '.create' ) )   
print('=== DONE ===')    