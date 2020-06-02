'''
#******************SOURCE******************
pythonFilePath = 'D:/mcantat_BDD/projects/code/maya/' 
import sys
sys.path.append( pythonFilePath )
#******************SOURCE******************


import maya.cmds as mc
import python
from python.plugIn.utilsMayaNodesBuild import *


cPlusPlusVersion = 0



path = 'D:\mcantat_BDD\projects\code\maya\python\plugIn/annotateDyn.py'
nodeType = 'annotateDyn'  
fileName = 'annotateDyn'


#NEW SCENE
clean( path , nodeType)    
mc.loadPlugin( path  )
newNode = mc.createNode( nodeType )  
#BUILD LOCATORS
print('=== BUILD TEST ===')
locs = createLocTest(  10 , separationLength = 2 )
cube = createCubeTest( [0,0,0] , parent = '' , returnTransform = True  )
#INPUT  
print('=== INPUT CONNECTIONS ===')    
mc.connectAttr( ( 'persp.worldMatrix' ) , ( newNode + '.inCamMatrix' ) )

mc.connectAttr( ( locs[0] + '.translate' ) , ( newNode + '.inVectors[0]' ) )
mc.connectAttr( ( locs[1] + '.translate' ) , ( newNode + '.inVectors[1]' ) )
mc.connectAttr( ( locs[2] + '.translate' ) , ( newNode + '.inSquares[0]' ) )
mc.connectAttr( ( locs[3] + '.translate' ) , ( newNode + '.inCircles[0]' ) )
mc.connectAttr( ( locs[4] + '.translate' ) , ( newNode + '.inTriangles[0]' ) )
mc.connectAttr( ( locs[5] + '.translate' ) , ( newNode + '.inTextPos' ) )
mc.connectAttr( ( locs[6] + '.translate' ) , ( newNode + '.inStars[0]' ) )
mc.connectAttr( ( locs[7] + '.translate' ) , ( newNode + '.inMotionTrail[0]' ) )
mc.connectAttr( ( locs[9] + '.translate' ) , ( newNode + '.inMotionTrail[1]' ) )

mc.connectAttr( ( newNode + '.outTrig' ) , ( cube + '.visibility' ) )

#OUTPUT

mc.setAttr( ( newNode + '.inVectorsSize[0]') , 0.5 )
mc.setAttr( ( newNode + '.inVectorsColor[0]') , 1,0,0 )
mc.setAttr( ( newNode + '.inVectorsName[0]') , 'momentum' , type = 'string' )

mc.setAttr( ( newNode + '.inSquaresSize[0]') , 1.0 )
mc.setAttr( ( newNode + '.inSquaresColor[0]') , 0,1,0 )
mc.setAttr( ( newNode + '.inSquaresName[0]') , 'PointA' , type = 'string' )

mc.setAttr( ( newNode + '.inCirclesSize[0]') , 10.0 )
mc.setAttr( ( newNode + '.inCirclesColor[0]') , 0,0,1 )
mc.setAttr( ( newNode + '.inCirclesName[0]') , 'PointB' , type = 'string' )

mc.setAttr( ( newNode + '.inTrianglesSize[0]') , 1.0 )
mc.setAttr( ( newNode + '.inTrianglesColor[0]') , 1,0,1 )
mc.setAttr( ( newNode + '.inTrianglesName[0]') , 'PointC' , type = 'string' )

mc.setAttr( ( newNode + '.inStarsSize[0]') , 1.0 )
mc.setAttr( ( newNode + '.inStarsColor[0]') , 1,1,0 )
mc.setAttr( ( newNode + '.inStarsName[0]') , 'STAR' , type = 'string' )


mc.setAttr( ( newNode + '.inMotionTrailSize[0]') , 1.0 )
mc.setAttr( ( newNode + '.inMotionTrailColor[0]') , 1,1,0 )
mc.setAttr( ( newNode + '.inMotionTrailName[0]') , 'MT' , type = 'string' )


mc.setAttr( ( newNode + '.inMotionTrailSize[1]') , 0.5 )
mc.setAttr( ( newNode + '.inMotionTrailColor[1]') , 1,0,1 )
mc.setAttr( ( newNode + '.inMotionTrailName[1]') , 'MT2' , type = 'string' )


'''










import maya.cmds as mc


def addAttrFloat( master , attrs ,values ):
	for i in range( 0 , len(attrs) ):
		mc.addAttr( master , ln = attrs[i], at = "double" , dv = values[i] )
		mc.setAttr( ( master + '.' + attrs[i] ) , e = True , keyable = True )


def addAttrStore( master , slaves , nbrMemorySlot ):
	attr    = 'slave'
	letters = ['A' , 'B' , 'C' , 'D' ]
	axes    = [ 'X' , 'Y' , 'Z' ]
	for slave in slaves:
		for i in range( 0 , nbrMemorySlot ):
			for axe in axes:
				attrToWrite = slave + letters[i] + axe
				mc.addAttr( master , ln = attrToWrite, at = "double" , dv = 0 )
				mc.setAttr( ( master + '.' + attrToWrite ) , e = True , keyable = True )
				


def addAttrPoint( master , attrs ):
	axis = [ 'X' , 'Y' , 'Z' ]
	for attr in attrs:
		mc.addAttr( master , ln = attr, at = "double3" )
		for axe in axis:
			mc.addAttr( master , ln = (attr+axe) , at = "double" , p = attr )
		mc.setAttr( ( master + '.' + attr ) , e = True , keyable = True )
		for axe in axis:
			mc.setAttr( ( master + '.' + (attr+axe) ) , e = True , keyable = True )



'''				
addAttrFloat( 'driver_GEO' , [ 'activate' , 'mass' , 'gravity' , 'friction' , 'attract' ] , [ 1 , 9.8 , 0.1 , 0.2 ] )				
addAttrStore( 'store' , ['slave'] , 2 )
addAttrPoint( 'visuStopEval' , ['pSim' , 'pSimStoreA' , 'pDriver' , 'vWeight' , 'vMomentum' , 'vFriction' , 'vAttractA' ] )
'''	



#******************SOURCE******************
pythonFilePath = 'D:/mcantat_BDD/projects/code/maya/' 
import sys
sys.path.append( pythonFilePath )
#******************SOURCE******************


def installAnnotationDyn( nodeName , camera ):

	path = 'D:\mcantat_BDD\projects\code\maya\python\plugIn/annotateDyn.py'
	nodeType = 'annotateDyn'  
	fileName = 'annotateDyn'
  
	mc.loadPlugin( path  )
	newNode = mc.createNode( nodeType , name = nodeName  )  
		#CONNECTION
	
	#CAM
	mc.connectAttr( ( camera + '.worldMatrix' ) , ( newNode + '.inCamMatrix' ) )
	#TRIGERRING
	cube = mc.polyCube( n = "visibilityTriggering" );
	mc.connectAttr( ( newNode + '.outTrig' ) , ( cube[0] + '.visibility' ) )
	#INFO
	mc.connectAttr( ( cube[0] + '.translate' ) , ( newNode + '.inTextPos' ) )
	return newNode






def linkExpressionToAnnotation( expressionName , annotationNode , toVisualizeInfo , modeDriver , startCumulateVariable):

	exp = mc.expression( expressionName , q = True  , s = True )
	exp += ('\n                                                                                                                 ');
	exp += ('\n                                                                                                                 ');
	exp += ('\n                                                                                                                 ');
	exp += ('\n                                                                                                                 ');
	exp += ('\n//****************************************************************                                               ');
	exp += ('\n//*****************************VISU*******************************                                               ');
	exp += ('\n//****************************************************************                                               ');
	exp += ('\n//GATHER INFO MODE                                                                                               ');
	exp += ('\nfloat $mode = {}.mode;'.format( modeDriver ) );
	exp += ('\nfloat $mA = clamp( 0, 1 , 1 - abs( $mode -  0 ) ) ; //GET                                                        ');
	exp += ('\nfloat $mB = clamp( 0, 1 , 1 - abs( $mode -  1 ) ) ; //COMPUTE                                                    ');
	exp += ('\nfloat $mC = clamp( 0, 1 , 1 - abs( $mode -  2 ) ) ; //APPLY                                                      ');
	exp += ('\nfloat $mD = clamp( 0, 1 , 1 - abs( $mode -  3 ) ) ; //APPLYCUMULATE                                              ');
	exp += ('\n                                                                                                                 ');
	exp += ('\nvector $vValue;                                                                                                  ');
	exp += ('\nvector $pStart;                                                                                                  ');
	exp += ('\nfloat $size ;                                                                                                    ');
	exp += ('\nvector $color ;                                                                                                  ');
	exp += ('\nstring $name;                                                                                                    ');
	exp += ('\nvector $pStartCumulate = {};'.format( startCumulateVariable ) );
	exp += ('\n                                                                                                                 ');
	exp += ('\n//_____________________OUT POINT                                                                                 ');
	
	index = {}
	for info in toVisualizeInfo:
		#GET ATTR
		variable = info[0]
		attrType = info[1][0].capitalize() + info[1][1:] + 's'
		name     = info[2]
		size     = info[3]
		color    = info[4]
		variableStart = ''

		if( attrType in index.keys() ):
			index[attrType] +=1
		else:
			index[attrType] = 0

		isVector = 0
		print(info , len(info))		
		if( 5 < len(info) ):
			isVector = 1
			variableStart = info[5]	

		#BUILD EXP	
		if( isVector == 0 ):
			exp += ('\n$name   = "{}";                                                       '.format( name     ) );
			exp += ('\n$vValue = {};                                                         '.format( variable ) );
			exp += ('\n$size   = {};                                                         '.format( size     ) );
			exp += ('\n$color  = << {0} , {1} , {2} >>;                                      '.format( info[4][0] , info[4][1] , info[4][2] ) );
			exp += ('\nsetAttr( "{0}.in{1}[{2}]"      , $vValue.x , $vValue.y , $vValue.z ); '.format( annotationNode , attrType , index[attrType] ) );
			exp += ('\nsetAttr( "{0}.in{1}Color[{2}]" , $color.x  , $color.y  , $color.z  ); '.format( annotationNode , attrType , index[attrType] ) );
			exp += ('\nsetAttr( "{0}.in{1}Size[{2}]"  , $size );                             '.format( annotationNode , attrType , index[attrType] ) );
			exp += ('\nsetAttr  "{0}.in{1}Name[{2}]" -type "string"  $name ;                 '.format( annotationNode , attrType , index[attrType] ) );
			exp += ('\n                                                                      ');
			exp += ('\n                                                                      ');
		else:	
			exp += ('\n$name   = "{}";                                                      '.format( name     ) );
			exp += ('\n$pStart = {0} * $mA + {0} * $mB + {0} * $mC + $pStartCumulate * $mD;    '.format( variableStart ) );
			exp += ('\n$vValue = {};                                                        '.format( variable ) );
			exp += ('\n$size   = {};                                                        '.format( size    ) );
			exp += ('\n$color  = << {0} , {1} , {2} >>;                                     '.format( info[4][0] , info[4][1] , info[4][2] ) );
			exp += ('\nsetAttr( "{0}.in{1}[{2}]"      , $pStart.x             , $pStart.y             , $pStart.z             );  '.format( annotationNode , attrType , index[attrType]*2   ) );
			exp += ('\nsetAttr( "{0}.in{1}[{2}]"      , $pStart.x + $vValue.x , $pStart.y + $vValue.y , $pStart.z + $vValue.z );  '.format( annotationNode , attrType , index[attrType]*2+1 ) );
			exp += ('\nsetAttr( "{0}.in{1}Color[{2}]" , $color.x              , $color.y              , $color.z               ); '.format( annotationNode , attrType , index[attrType]     ) );
			exp += ('\nsetAttr( "{0}.in{1}Size[{2}]"  , $size );                                                                  '.format( annotationNode , attrType , index[attrType]     ) );
			exp += ('\nsetAttr  "{0}.in{1}Name[{2}]"  -type "string"  $name ;                                                     '.format( annotationNode , attrType , index[attrType]     ) );
			exp += ('\n                                                                     ');
			exp += ('\n                                                                     ');
			exp += ('\n$pStartCumulate = $pStartCumulate + {};                              '.format( variable) );
			exp += ('\n                                                                     ');
			exp += ('\n                                                                     ');
	
	
	
	mc.expression( expressionName  , e = True , s = exp  , o = '' , ae=  1 , uc = 'all'  )



'''
# SPRING
nodeName = 'visu'
cam = 'visu_CAM'

toVisualize = []
toVisualize.append( ['$pSim'    , 'motionTrail' ,'SIM'      , 0 , [0.8,0.8,0.3]       ] )
toVisualize.append( ['$pDriver' , 'motionTrail' ,'DRIVER'   , 0 , [0.3,0.2,0.8]       ] )

toVisualize.append( ['$pSim'    , 'star' ,'SIM'    , 4 , [1,1,0]             ] )
toVisualize.append( ['$pSimA'   , 'star' ,'SIM -1'   , 3.5 , [0.8,0.8,0]           ] )
toVisualize.append( ['$pSimB'   , 'star' ,'SIM -2'   , 2 , [0.7,0.7,0]           ] )

toVisualize.append( ['$pDriver' , 'triangle' ,'DRIVER'   , 1 , [0,0,1]           ] )

toVisualize.append( ['$vWeight'          , 'vector'   ,'WEIGHT'           , 0.7 , [0,0,1]   , '$pSim' ] )
toVisualize.append( ['$vMomentum'        , 'vector'   ,'MOMENTUM'         , 0.7 , [1,0,0]   , '$pSim' ] )
toVisualize.append( ['$vFriction'        , 'vector'   ,'FRICTION'         , 0.7 , [0.6,0,0] , '$pSim' ] )
toVisualize.append( ['$vAttractA'        , 'vector'   ,'ATTRACT'          , 0.7 , [1,0,1]   , '$pSim' ] )
toVisualize.append( ['$vCollisionPlane'  , 'vector'   ,'COLLISION PLANE'  , 0.7 , [0,1,0]   , '$pSim' ] )
toVisualize.append( ['$vCollisionSphere' , 'vector'   ,'COLLISION SPHERE' , 0.7 , [0,1,1]   , '$pSim' ] )

installAnnotationDyn( nodeName , cam )
linkExpressionToAnnotation( 'simpleDyn_EXP' , 'visu' , toVisualize , 'driver_GEO' , '$pSimA' )
'''



'''
# PLANE
nodeName = 'visu'
cam = 'visu_CAM'

toVisualize = []
toVisualize.append( ['$pSlave25'    , 'motionTrail' ,'SIM'      , 0 , [0.8,0.8,0.3]       ] )
#toVisualize.append( ['$pDriver' , 'motionTrail' ,'DRIVER'   , 0 , [0.3,0.2,0.8]       ] )

toVisualize.append( ['$pSlave25'    , 'star' ,'SIM'       , 4 , [1,1,0]       ] )
toVisualize.append( ['$pSlaveA25'   , 'star' ,'SIM -1'    , 3.5 , [0.9,0.9,0]             ] )
toVisualize.append( ['$pSlaveB25'   , 'star' ,'SIM -2'   , 3.5 , [0.8,0.8,0]           ] )
toVisualize.append( ['$pSlaveC25'   , 'star' ,'SIM -3'   , 2 , [0.7,0.7,0]           ] )

toVisualize.append( ['$pDriverA25' , 'triangle' ,'DRIVER A'   , 0.7 , [0,0,1]           ] )
toVisualize.append( ['$pDriverB25' , 'triangle' ,'DRIVER B'   , 0.7 , [0,0,1]           ] )
toVisualize.append( ['$pDriverC25' , 'triangle' ,'DRIVER C'   , 0.7 , [0,0,1]           ] )
toVisualize.append( ['$pDriverD25' , 'triangle' ,'DRIVER D'   , 0.7 , [0,0,1]           ] )

toVisualize.append( ['$vWeight25'          , 'vector'   ,'WEIGHT'           , 0.7 , [0,0,1]   , '$pSlave25' ] )
toVisualize.append( ['$vMomentum25'        , 'vector'   ,'MOMENTUM'         , 0.7 , [1,0,0]   , '$pSlave25' ] )
toVisualize.append( ['$vFriction25'        , 'vector'   ,'FRICTION'         , 0.7 , [0.6,0,0] , '$pSlave25' ] )
toVisualize.append( ['$vAttractA25'        , 'vector'   ,'ATTRACT A'          , 0.7 , [1,0,1]   , '$pSlave25' ] )
toVisualize.append( ['$vAttractB25'        , 'vector'   ,'ATTRACT B'          , 0.7 , [1,0,1]   , '$pSlave25' ] )
toVisualize.append( ['$vAttractC25'        , 'vector'   ,'ATTRACT C'          , 0.7 , [1,0,1]   , '$pSlave25' ] )
toVisualize.append( ['$vAttractD25'        , 'vector'   ,'ATTRACT D'          , 0.7 , [1,0,1]   , '$pSlave25' ] )
toVisualize.append( ['$vCollisionA25'      , 'vector'   ,'COLLISION A'  , 0.7 , [0,1,0]   , '$pSlave25' ] )
toVisualize.append( ['$vCollisionB25'      , 'vector'   ,'COLLISION B' , 0.7 , [0,1,1]   , '$pSlave25' ] )

installAnnotationDyn( nodeName , cam )
linkExpressionToAnnotation( 'ropeDyn_EXP' , 'visu' , toVisualize , 'driver' , '$pSlaveA25' )
'''



'''
# FOLLOW
nodeName = 'visu'
cam = 'visu_CAM'

toVisualize = []
toVisualize.append( ['$pSim'    , 'star' ,'SIM'       , 4 , [1,1,0]       ] )
toVisualize.append( ['$pSimA'   , 'star' ,'SIM -1'    , 3.5 , [0.9,0.9,0]             ] )
toVisualize.append( ['$pSimB'   , 'star' ,'SIM -2'   , 3.5 , [0.8,0.8,0]           ] )


toVisualize.append( ['$pDriver' , 'triangle' ,'DRIVER '   , 0.7 , [0,0,1]           ] )


toVisualize.append( ['$vWeight'          , 'vector'   ,'WEIGHT'           , 0.7 , [0,0,1]   , '$pSim' ] )
toVisualize.append( ['$vMomentum'        , 'vector'   ,'MOMENTUM'         , 0.7 , [1,0,0]   , '$pSim' ] )
toVisualize.append( ['$vFriction'        , 'vector'   ,'FRICTION'         , 0.7 , [0.6,0,0] , '$pSim' ] )
toVisualize.append( ['$vAttractA'        , 'vector'   ,'ATTRACT'          , 0.7 , [1,0,1]   , '$pSim' ] )
toVisualize.append( ['$vCollisionPlane'      , 'vector'   ,'COLLISION A'  , 0.7 , [0,1,0]   , '$pSim' ] )
toVisualize.append( ['$vCollisionSphere'      , 'vector'   ,'COLLISION B' , 0.7 , [0,1,1]   , '$pSim' ] )

installAnnotationDyn( nodeName , cam )
linkExpressionToAnnotation( 'followDyn_EXP' , 'visu' , toVisualize , 'driver_GEO' , '$pSimA' )
'''








