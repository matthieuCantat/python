import maya.cmds as mc




def clean( path , nodeType):   
    print('=== NEW SCENE ===')
    mc.file( new = True , f = True )
    try:
        mc.unloadPlugin( nodeType , f = True ) 
    except:
        pass
    mc.file( new = True , f = True )    

    
def createLocTest( nbr , separationLength = 2 ):
    locators = []
    for i in range( 0 , nbr ):
        locTmp = mc.spaceLocator() 
        newLoc = locTmp[0]
        mc.setAttr( (newLoc + ".translateX") , ( i*separationLength ) )
        locators.append(newLoc)   
    return locators  


def createCubeTest( position , parent = '' , returnTransform = False  ):
    objTmp = mc.polyCube()   
    cube = objTmp[0]
    mc.setAttr(( cube + '.tx' ) , position[0] )
    mc.setAttr(( cube + '.ty' ) , position[1] )    
    mc.setAttr(( cube + '.tz' ) , position[2] ) 
    if not( parent == '' ): mc.parent(  cube , parent )       
    shape = mc.listRelatives( cube , c = True , s = True )
    if( returnTransform ):
        return cube    
    return shape[0]


def createPlaneTest( position , parent = '' , returnTransform = False ):
    objTmp = mc.polyPlane( sx = 5 , sy = 5 )
    cube = objTmp[0]
    mc.setAttr(( cube + '.tx' ) , position[0] )
    mc.setAttr(( cube + '.ty' ) , position[1] )    
    mc.setAttr(( cube + '.tz' ) , position[2] ) 
    if not( parent == '' ): mc.parent(  cube , parent )       
    shape = mc.listRelatives( cube , c = True , s = True )
    if( returnTransform ):
        return cube
    return shape[0]


def createSphereTest( position , parent = ''  , returnTransform = False ):
    objTmp = mc.polySphere( sx = 8 , sy = 8)   
    cube = objTmp[0]
    mc.setAttr(( cube + '.tx' ) , position[0] )
    mc.setAttr(( cube + '.ty' ) , position[1] )    
    mc.setAttr(( cube + '.tz' ) , position[2] ) 
    if not( parent == '' ): mc.parent(  cube , parent )       
    shape = mc.listRelatives( cube , c = True , s = True )
    if( returnTransform ):
        return cube    
    return shape[0]



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


def createCurveTest( name ,  parent = '' ):
    curveTrf = mc.createNode('transfrom' , n = name )    
    curveShape = mc.createNode('nurbsCurve' , parent = curveTrf )
    if not( parent == '' ): mc.parent(  curveTrf , parent )       
    return curveShape





import maya.cmds as mc

'''
createLocOnCoordsString( '0.270598 -0.92388 -0.270598 | 0 -0.92388 -0.382683')
createLocOnIndex( 'cage_GEO' , '| 0 1 8 | 0 1 8 | 0 1 8 | 0 1' )
'''


def stringToNumArray( string ):
    nums = [ "0" , "1" , "2" , "3" , "4" , "5" , "6" , "7" , "8" , "0" ]
    splitCoords = string.split(" ")
    coords = []
    for sCoords in splitCoords:
        isNum = 0
        for num in nums :
            if( num in sCoords):
                isNum = 1
                break
        
        if( isNum ):
            coords.append(float(sCoords))

    return coords
    
    
def createLocOnCoordsString( coordsString ):
    
    coords = stringToNumArray( coordsString )
    
    nbrElem = int( len(coords)/3 )
    
    print(coords)
    for i in range( 0 , nbrElem ):
        loc = mc.spaceLocator( n = 'test' )[0]
        print(i)
        mc.setAttr( loc + '.translateX' , coords[i*3+0] )
        mc.setAttr( loc + '.translateY' , coords[i*3+1] )
        mc.setAttr( loc + '.translateZ' , coords[i*3+2] )
        


def createLocOnIndex( mesh , coordsString ):
    indexes = stringToNumArray( coordsString )
    for i in range( 0 , len(indexes) ):
        loc = mc.spaceLocator( n = 'test' )[0]
        coords = mc.xform(  '{}.vtx[{}]'.format( mesh , indexes[i] ) , q = True  , t = True , ws = True )
        mc.setAttr( loc + '.translateX' , coords[0] )
        mc.setAttr( loc + '.translateY' , coords[1] )
        mc.setAttr( loc + '.translateZ' , coords[2] )

