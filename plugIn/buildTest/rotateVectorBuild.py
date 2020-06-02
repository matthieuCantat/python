

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
    for i in range( 0 , nbr ):
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



path     = "D:\mcantat_BDD\projects\code\maya\python\plugIn\\rotateVector.py"
nodeType = "rotateVector"    
#NEW SCENE    
newNode = testNode_create( path , nodeType )
#BUILD LOCATORS
print('=== BUILD TEST ===')
inputMatrixObjs = createLocTest( nbr = 4 ) 
#INPUT  
print('=== INPUT CONNECTIONS ===')    
mc.connectAttr( ( inputMatrixObjs[0] + '.worldMatrix[0]' ) , ( newNode + '.inputMatrix' ) )
mc.connectAttr( ( inputMatrixObjs[1] + '.worldMatrix[0]' ) , ( newNode + '.inputMatrixBase' ) )
mc.connectAttr( ( inputMatrixObjs[2] + '.translate' ) , ( newNode + '.inputVector' ) )
#OUTPUT
print('=== OUTPUT CONNECTIONS ===')
mc.connectAttr( ( newNode + '.outputVector' ) , ( inputMatrixObjs[3] + '.translate' ) )
print('=== DONE ===')    