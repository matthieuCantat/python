
'''
	name:  testMaya
	type:  ALL
	tag:   utils
	date:  20/04/2016	
	input: ????

	area for testing script.
		
'''


import maya.cmds as mc
import maya.OpenMaya as ompy
import math
from ..utils import utilsMaya
from ..utils import utilsMayaApi
from ..utils import utilsPython
from ..buildManip import manipsClass
#from ..buildRigDoubleIk import pistonRigClass
from ...utils.classes import trsClass

def testMaya():

	
	skeleton    = [  'jointA'  , 'jointB'  , 'jointC'  , 'jointD' ]
	landmarks = [  'jointA_LOC'  , 'jointB_LOC'  , 'jointC_LOC'  , 'jointD_LOC' ]	
	camera       = 'camera1_CAM'
	
	
	#sketetonPosing( skeleton , camera , landmarks  )

	selection = mc.ls( sl=True )

	for elem in selection:
		buildXYZRotLimit( elem )



def buildXYZRotLimit( elem ):
	# BUILD
	mainGrp         = elem + '_rotLimit_GRP'
	locatorParent   = elem + '_rotLimitParent_LOC'
	locatorElemOrig = elem + '_rotLimitElem_ORIG'	
	locatorElem     = elem + '_rotLimitElem_LOC'

	rotLimitX = buildRotLimit( elem + 'X' )
	rotLimitY = buildRotLimit( elem + 'Y' )
	rotLimitZ = buildRotLimit( elem + 'Z' )
	mc.createNode( 'transform' , n = mainGrp         )
	mc.spaceLocator( n = locatorParent )
	mc.createNode( 'transform' , n = locatorElemOrig )		
	mc.spaceLocator( n = locatorElem   )	
	# PARENT
	mc.parent( locatorParent   , mainGrp )
	mc.parent( locatorElemOrig , locatorParent )	
	mc.parent( locatorElem     , locatorElemOrig )	
	mc.parent( rotLimitX[0]  , mainGrp )
	mc.parent( rotLimitY[0]  , mainGrp )
	mc.parent( rotLimitZ[0]  , mainGrp )
	# SETTING ATTR
	mc.setAttr( rotLimitX[1]  + '.rx' , -180 )
	mc.setAttr( rotLimitX[1]  + '.rz' , 90   )
	mc.setAttr( rotLimitX[2]  + '.rx' , -180 )
	mc.setAttr( rotLimitX[2]  + '.rz' , 90   )
	mc.setAttr( rotLimitZ[1]  + '.rx' , 90   )
	mc.setAttr( rotLimitZ[2]  + '.rx' , 90   )
	mc.setAttr( locatorParent + '.v'  , 0    )	
	# CNS
	mc.parentConstraint( locatorElemOrig , rotLimitX[1] , mo = True )
	mc.parentConstraint( locatorElemOrig , rotLimitY[1] , mo = True )
	mc.parentConstraint( locatorElemOrig , rotLimitZ[1] , mo = True )
	mc.parentConstraint( locatorElem   , rotLimitX[2] , mo = True )
	mc.parentConstraint( locatorElem   , rotLimitY[2] , mo = True )
	mc.parentConstraint( locatorElem   , rotLimitZ[2] , mo = True )	
	
	# PLACMENT

	elemParent = mc.listRelatives( elem , p = True )

	if( len( elemParent ) ==  1 ):
		mc.orientConstraint( elemParent[0] , locatorParent , mo = False )
		mc.pointConstraint( elem , locatorParent , mo = False )

	jointOrientAttr = [ 'jointOrientX' , 'jointOrientY' , 'jointOrientZ' ]
	rotAttr         = [ 'rotateX'      , 'rotateY'      , 'rotateZ'      ]	
	for i in range(0,3):
		if( mc.objExists( elem + '.' + jointOrientAttr[i]  ) ):
			valueTmp = mc.getAttr( elem + '.' + jointOrientAttr[i] )
			if not( valueTmp == 0 ):
				mc.setAttr( locatorElemOrig + '.' + rotAttr[i] , valueTmp )


	mc.parentConstraint( elem   , locatorElem , mo = False )		


	return [ mainGrp , locatorParent ]


def sketetonPosing( skeleton , camera , landmarks ):
	
	print('_________________________________________ START')
	objTrs = trsClass.trsClass()
	
	print('_________________________________________ GET INFO')
	skeletonDist = []
	for i  in range( 0 , len( skeleton ) ):
		trsTmp = objTrs.createFromObj( skeleton[0] )
		objTrs.createFromObj( skeleton[1] )
		skeletonDist.append( objTrs.toDistance( trsTmp ) )
		
	cameraTrs = objTrs.createFromObj( camera )
		
	landmarkTrs = []
	for loc  in landmarks :
		landmarkTrs.append( objTrs.createFromObj( loc ) )

		
	print('_________________________________________ END')
	
	
			
	return 1



def buildRotLimit( baseName ):

	print('rotLimit__________________ START')

	grpMain         = baseName + '_rotLimit_GRP'
	grpWorld        = baseName + '_toWorld_GRP'
	grpParent       = baseName + '_toCnsParent_GRP'	
	grpChild        = baseName + '_toCnsChildren_GRP'

	limitAreaOrig   = baseName + '_limitArea_ORIG'
	limitArea       = baseName + '_limitArea_SURF'

	grpAim          = baseName + '_outValueAim_GRP'
	valueLocMax     = baseName + '_max_LOC'
	valueLocMin     = baseName + '_min_LOC'

	curveBuildExt   = baseName + '_ext_CRV'	
	curveBuildInt   = baseName + '_int_CRV'		

	folMax          = baseName + '_max_FOL'	
	folMin          = baseName + '_min_FOL'

	arrow           = baseName + '_arrow_SURF'	
	posDir          = baseName + '_posDir_CRV'		
	arrowOrig       = baseName + '_arrow_ORIG'		
	expName         = baseName + '_limiteAreaRot_EXP'	


	print('rotLimit__________________ CREATE HIERARCHY')

	elemsName   = [  grpMain    ,  grpWorld   ,  grpParent  ,  grpChild   ,  limitAreaOrig  ,  grpAim     , arrowOrig   ,  valueLocMax ,  valueLocMin ]       
	elemsType   = [ 'transform' , 'transform' , 'transform' , 'transform' , 'transform'     , 'transform' , 'transform' , 'locator'    , 'locator'    ]
	elemsFather = [ ''          ,  grpMain    ,  grpMain    ,  grpMain    ,  grpParent      ,  grpParent  , grpChild    ,  grpAim      ,  grpAim      ] 
	
	utilsMaya.createDagNodes( elemsType , elemsName , elemsFather )
				
	print('rotLimit__________________ CREATE CURVES')

	mc.circle( n = curveBuildExt, c = (0,0,0), nr = (0,1,0), sw = 360, r = 1, d = 3, ut = 0, tol = 0.01, s = 8, ch = 1 )
	mc.circle( n = curveBuildInt, c = (0,0,0), nr = (0,1,0), sw = 360, r = 1, d = 3, ut = 0, tol = 0.01, s = 8, ch = 1 )

	mc.parent( curveBuildExt , grpWorld )
	mc.parent( curveBuildInt , grpWorld )

	print('rotLimit__________________ CREATE LIMITE AREA')	

	mc.loft( curveBuildExt, curveBuildInt, n = limitArea, ch = 1, u = 1, c = 0, ar = 1, d = 3, ss = 1, rn = 0, po = 0, rsn = True  )
	mc.parent( limitArea, limitAreaOrig )

	print('rotLimit__________________ CREATE ARROW')

	curvesTmp = [ 'buildRotLimitTMP1_CRV' , 'buildRotLimitTMP2_CRV' ]
	mc.curve( n = curvesTmp[0], d = 1, p = ( ( 0, 0, 0 ) , ( 0.25, 0,  0.13 ) ) , k = (0,1) )	
	mc.curve( n = curvesTmp[1], d = 1, p = ( ( 0, 0, 0 ) , ( 0.25, 0, -0.13 ) ) , k = (0,1) )	
	mc.loft( curvesTmp[0], curvesTmp[1], n = arrow, ch = 1, u = 1, c = 0, ar = 1, d = 3, ss = 1, rn = 0, po = 0, rsn = True  )
	mc.delete( curvesTmp )

	mc.parent( arrow, arrowOrig )

	mc.setAttr( arrow + '.tx' , 1 )


	print('rotLimit__________________ CREATE FOLLICLE')

	utilsMaya.buildFollicle( limitArea , n = folMax , u = 1 , v = 0 ) 
	utilsMaya.buildFollicle( limitArea , n = folMin , u = 0 , v = 0 ) 

	mc.parent( folMax , grpWorld )
	mc.parent( folMin , grpWorld )	

	print('rotLimit__________________ CREATE POSDIR')

	mc.curve( n = posDir , d = 1 , p = ( (0.016,0,0.050) , (-0.016,0,0.050) , (-0.016,0,0.016) , (-0.050,0,0.016) , ( -0.050,0,-0.016 ) , ( -0.016,0,-0.016 ) , ( -0.016,0,-0.050 ) , ( 0.016,0,-0.050 ) , ( 0.016,0,-0.016 ) , ( 0.050,0,-0.016 ) , ( 0.050,0,0.016 ) , ( 0.016,0,0.016 ) , ( 0.016,0,0.050 ) , ( 0.016,0,0.050 )   ) , k = ( 0,1,2,3,4,5,6,7,8,9,10,11,12,13 ) )
	mc.setAttr( posDir + '.tx' , -0.5 )
	mc.parent( posDir , folMax )




	print('rotLimit__________________ LIMITE AREA ATTR')

	attrToHide = [ 'translateX' , 'translateY' , 'translateZ' , 'rotateX' , 'rotateZ' , 'scaleX' , 'scaleY' , 'scaleZ' , 'visibility' ]
	
	for attr in attrToHide:
		mc.setAttr( limitArea + '.' + attr , cb = False , l = True , k = False )

	attrNames  = [ 'areaSize'  , 'EXTRA_ATTR', 'overrideMode', 'max'    , 'min'    , 'LIMIT_OUT' , 'maxOut'     , 'minOut'   , 'VISU'      , 'extShape'  , 'intShape'  , 'arrowSize' ]
	attrTypes  = [ 'float1Pos' , 'separator' , 'intOnOff'    , 'float1' , 'float1' , 'separator' , 'floatRead' , 'floatRead' , 'separator' , 'float1Pos' , 'float1Pos' , 'float1Pos' ]
	attrValues = [  0          ,  None       ,  0            ,  0       , 0        , None        , 0           , 0           , None        ,  1.1        , 0.9         , 1           ]	 
	objs       = [ limitArea for i in range( 0 , len(attrNames) ) ]

	utilsMaya.addSpecialAttrs( objs , attrNames , attrTypes , attrValues = attrValues )


	print('rotLimit__________________ MAKE CONNECTIONS')

	mc.connectAttr( valueLocMax + '.rotateY' , limitArea + '.maxOut' )
	mc.connectAttr( valueLocMin + '.rotateY' , limitArea + '.minOut' )

	mc.connectAttr( limitArea + '.extShape' , curveBuildExt + '.scaleX' )
	mc.connectAttr( limitArea + '.extShape' , curveBuildExt + '.scaleY' )
	mc.connectAttr( limitArea + '.extShape' , curveBuildExt + '.scaleZ' )		

	mc.connectAttr( limitArea + '.intShape' , curveBuildInt + '.scaleX' )
	mc.connectAttr( limitArea + '.intShape' , curveBuildInt + '.scaleY' )
	mc.connectAttr( limitArea + '.intShape' , curveBuildInt + '.scaleZ' )	

	mc.connectAttr( limitArea + '.extShape' , arrowOrig + '.scaleX' )
	mc.connectAttr( limitArea + '.extShape' , arrowOrig + '.scaleY' )
	mc.connectAttr( limitArea + '.extShape' , arrowOrig + '.scaleZ' )	

	mc.connectAttr( limitArea + '.arrowSize' , arrow + '.scaleX' )
	mc.connectAttr( limitArea + '.arrowSize' , arrow + '.scaleY' )
	mc.connectAttr( limitArea + '.arrowSize' , arrow + '.scaleZ' )

	print('rotLimit__________________ MAKE EXRPESSIONS')


	curveBuildExtShape    = mc.listRelatives( curveBuildExt, s = True, c = True )
	curveBuildExtMakeNode = mc.listConnections( curveBuildExtShape[0] + '.create' , s = True , d = False , )
	
	curveBuildIntShape    = mc.listRelatives( curveBuildInt, s = True, c = True )
	curveBuildIntMakeNode = mc.listConnections( curveBuildIntShape[0] + '.create' , s = True , d = False , )
	
	exp  = ''
	exp += '\n' + 'float $limitAreaRotCompensateOffset = -90;' 	
	exp += '\n' + '//_____________________________________________________________INS'
	exp += '\n' + 'int $overrideMode    = {0}.overrideMode;'.format( limitArea )
	exp += '\n' + 'float $max           = {0}.max;     '.format( limitArea )
	exp += '\n' + 'float $min           = {0}.min;     '.format( limitArea )
	exp += '\n' + 'float $limitAreaRot  = {0}.rotateY; '.format( limitArea )
	exp += '\n' + 'float $limitAreaSize = {0}.areaSize;'.format( limitArea )
	exp += '\n' + '//_____________________________________________________________COMPUTE'
	exp += '\n' + ''
	exp += '\n' + 'float $limitAreaRotCompensate  = $limitAreaSize / 2 * -1  + $limitAreaRotCompensateOffset;'
	exp += '\n' + 'float $limitAreaFatherRot      = 0;'
	exp += '\n' + ''
	exp += '\n' + 'if( $overrideMode == 1 )'
	exp += '\n' + '{	'
	exp += '\n' + '	$limitAreaSize           = abs( $max - $min );	'
	exp += '\n' + '	$limitAreaRotCompensate  = $min + $limitAreaRotCompensateOffset;	'
	exp += '\n' + '	$limitAreaFatherRot      = $limitAreaRot * -1;	'
	exp += '\n' + '}'
	exp += '\n' + '//_____________________________________________________________OUTS'
	exp += '\n' + '{0}.sweep = clamp( 0.01 , 99999999 , $limitAreaSize);'.format( curveBuildExtMakeNode[0] )
	exp += '\n' + '{0}.sweep = clamp( 0.01 , 99999999 , $limitAreaSize);'.format( curveBuildIntMakeNode[0] )
	exp += '\n' + '{0}.rotateY = $limitAreaRotCompensate;'.format( curveBuildExt )
	exp += '\n' + '{0}.rotateY = $limitAreaRotCompensate;'.format( curveBuildInt )
	exp += '\n' + '{0}.rotateY = $limitAreaFatherRot;'.format( limitAreaOrig )

	utilsMaya.buildSimpleExpression( expName , exp )

	print('rotLimit__________________ MAKE CONSTRAINTS')

	mc.aimConstraint( folMax , valueLocMax , mo = True , aimVector = (0,0,-1), upVector = (0,1,0), worldUpType = "vector", worldUpVector = (0,1,0) )
	mc.aimConstraint( folMin , valueLocMin , mo = True , aimVector = (0,0,1), upVector = (0,1,0), worldUpType = "vector", worldUpVector = (0,1,0) )


	print('rotLimit__________________ SET DEFAUT VALUE')	

	mc.setAttr( limitArea + '.areaSize' , 360 )
	mc.setAttr( limitArea + '.rotateY'  , 0   )
	mc.setAttr( limitArea + '.max'      , 180  )
	mc.setAttr( limitArea + '.min'      , -180  )



	print('rotLimit__________________ CLEAN')



	mc.setAttr( grpWorld + '.visibility' , 0 )
	mc.setAttr( grpAim   + '.visibility' , 0 )

	mc.setAttr( arrow   + '.overrideEnabled'     , 1 )
	mc.setAttr( arrow   + '.overrideDisplayType' , 2 )	
	mc.setAttr( posDir   + '.overrideEnabled'     , 1 )
	mc.setAttr( posDir   + '.overrideDisplayType' , 2 )



	print('rotLimit__________________ END')

	return [ grpMain , grpParent , grpChild ] 













