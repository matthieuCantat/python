

import math
import maya.cmds         as mc
import maya.api.OpenMaya as ompy
from ..utils import utilsMath
from .mayaClasse import *

#from .. import utilsMayaApi


class trs(mayaClasse):
	
	def __init__(self , inValue = None):
		#super(self.__class__, self).__init__()
		mayaClasse.__init__(self)
		#UTILS
		self.utilsPositionWorldOrigine = [ 0 , 0 , 0 ]
		self.utilsUpVector             = [ 0 , 1 , 0 ]
		self.utilsTripleVectorsDefault = [ 1 , 0 , 0 , 0 , 1 , 0 , 0 , 0 , 1 ]
		self.utilsCubeCoordsDefault    = [ [-0.5,-0.5,-0.5] , [0.5,-0.5,-0.5] , [0.5,-0.5,0.5] , [-0.5,-0.5,0.5] , [-0.5,0.5,-0.5] , [0.5,0.5,-0.5] , [0.5,0.5,0.5] , [-0.5,0.5,0.5]  ]  		
		#CLASSE
		self.classeType       = 'trs'
		self.classeValueBase  = [ 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1 ]
		self.classeTrsValueUp = [ 0 , 1 , 0 , 0 , 0 , 0 , 1 , 1 , 1 ]		
		#INSTANCE			
		self.value      = self.classeValueBase
		self.value      = self.utils_overrideTrsValue( inValue )	

	#################################################################################################################################################################################		
	# IN ################################################################################################################################################################################# CREATE 
	################################################################################################################################################################################# 
	def createFromMayaObjCustom(  self , value , **args ): return self.createFromCustom( value , args )
	def createFromValuesCustom(   self , value , **args ): return self.createFromCustom( value , args )
	def createFromMayaObjsCustom( self , value , **args ): return self.createFromCustom( value , args )

	def createFromCustom( self , value , **args ):
		#ARGS
		toModif = args.get( 'toModif'  , [ 1 , 1 , 1 ] )
		uValue  = args.get( 'u'        , -1            )
		#VALUE TYPE
		isMayaObj , isArray , isCurve , arraySize = 0 , 0 , 0 , 0
		if( type(value) == types.ListType ):
			isMayaObj = mc.objExists(value[0])			
			isArray   = 1
			arraySize = len( value )
		else:
			isMayaObj = mc.objExists(value)
			if not( uValue == -1 ):
				isCurve = 1
		#GET VALUE
		if( isMayaObj ):
			if( isArray ): trsValue = self.createFromDifferenceBetweenGeometry( objs , **args )
			else:          
				if( isCurve ): trsValue = self.createFromCurve(        obj  , **args )
				else:          trsValue = self.createFromMayaObjSimple( obj , **args )
		else:
			if(   arraySize == 24 ): trsValue = self.createFromOrientedBoundingBox( values , **args )
			elif( arraySize == 16 ): trsValue = self.createFromFloatMatrix(         values , **args )
			elif( arraySize == 9  ): trsValue = self.createFromTripleVectors(       values , **args )
			elif( arraySize == 6  ): trsValue = self.createFromTwoVtxBarycentre(    values , **args )
			else:                    return 0			
		#MODIFY VALUE
		if( toModif[0] == 0  ): trsValue[0:3] = self.value[0:3] 
		if( toModif[1] == 0  ): trsValue[3:6] = self.value[3:6]
		if( toModif[2] == 0  ): trsValue[6:9] = self.value[6:9]
		return trsValue

		
	#################################################################################################################################################################################		
	# OUT ################################################################################################################################################################################ OUT
	################################################################################################################################################################################# 		
	def toMayaObjCustom( self , obj , trsValue ,  **args ): return self.toCustom( obj , trsValue , args  )
	def toValueCustom(   self , obj , trsValue ,  **args ): return self.toCustom( obj , trsValue , args  )

	def toCustom( self , obj = None , trsValue = None ,  **args  ):
		#ARGS
		worldSpace        = args.get( 'worldSpace'         , 0 )   
		getMMatrix        = args.get( 'MMatrix'            , 0 )
		getTripleVectors  = args.get( 'tripleVectors'      , 0 )
		getCube           = args.get( 'cube'               , 0 )
		distanceTrs       = args.get( 'distanceTrs'        , 0 )          		
		planAxis          = args.get( 'planAxis'           , 0 )
		closestAxisVector = args.get( 'closestAxisVector'  , 0 )
		visualize         = args.get( 'visualize'  , 0 )
		if( trsValue == None ):    trsValue = self.value
		isMayaObj = 0
		if( mc.objExists( obj ) ): 
			isMayaObj = 1

		#SET VALUE
		if( isMayaObj ): return self.toMayaObjSimple( obj , trsValue ,  worldSpace )
		else:						
			if not( getMMatrix        == 0 ): return self.toMMatrix(trsValue)			 
			if not( getTripleVectors  == 0 ): return self.toTripleVectors(trsValue)	
			if not( getCube           == 0 ): return self.toCubeCoords(trsValue)	
			if not( distanceTrs       == 0 ): return self.toDistance( distanceTrs , trsValue )	
			if not( planAxis          == 0 ): return self.toPlaneCoords( axeNormal , trsValue )
			if not( closestAxisVector == 0 ): return self.toClosestAxis( closestAxisVector , trsValue )	
			if not( visualize == 0 ):         return self.visualize( )

		
	#################################################################################################################################################################################		
	# MODIF ################################################################################################################################################################################# MODIF
	################################################################################################################################################################################# 		
	def modifyCustom( self ):	
		#ARGS
		inValue           = args.get( 'inValue'            , None          )  
		updateValue       = args.get( 'updateValue'        , 1             )  
		toModif           = args.get( 'toModif'            , [ 1 , 1 , 1 ] )  				

		trsValueFatherParent   = args.get( 'parent'               , 0 ) #[0,0,0,0,0,0,1,1,1]   
		trsValueFatherUnparent = args.get( 'unparent'             , 0 ) #[0,0,0,0,0,0,1,1,1]
		mirrorPlanCoords       = args.get( 'planSymCoords'        , 0 ) #[0,0,0,0,0,0,1,1,1]
		mirrorUnlockAxe        = args.get( 'unlockAxe'            , 2 )   
		mirrorRecomputeAxes    = args.get( 'recomputeAxes'        , 0 )
		offsetItselfTrs        = args.get( 'offsetItselfTrs'      , 0 ) #[0,0,0,0,0,0,1,1,1]  				    
		offsetParentTrs        = args.get( 'offsetParentTrs'      , 0 ) #[0,0,0,0,0,0,1,1,1]  
		offsetParentTrsUnder   = args.get( 'offsetParentTrsUnder' , 0 ) #[0,0,0,0,0,0,1,1,1]  	
		IntersectPlaneCoords   = args.get( 'IntersectPlaneCoords' , 0 ) #[0,0,0,0,0,0,1,1,1] 
		IntersectVectorDir     = args.get( 'IntersectVectorDir'   , 0 ) #[0,0,0]
		lineCoords             = args.get( 'lineCoords'           , 0 ) #[0,0,0,0,0,0] 		
		snapPlaneCoords        = args.get( 'snapPlaneCoords'      , 0 ) #[0,0,0,0,0,0,1,1,1] 
		curveName              = args.get( 'curveName'            , 0 ) #'toto_CRV'
		axisUp                 = args.get( 'axisUp'               , 0 )	#'X'
		inverseAxes            = args.get( 'inverseAxes'          , 0 ) #[0,0,0]				  			 			
		closetEulerRotation    = args.get( 'closetEulerRotation'  , 0 ) #[0,0,0]
		aimPoint               = args.get( 'aimPoint'             , 0 ) #[0,0,0]
		aimVector              = args.get( 'aimVector'            , 0 ) #[0,0,0] 
		aimAxe                 = args.get( 'aimAxe'               , None ) #[0,0,0]	
		middleTrsTarget        = args.get( 'middleTrsTarget'      , 0 ) #[0,0,0,0,0,0,1,1,1] 

		#MODIFY
		trsValue = self.utils_overrideTrsValue( inValue )

		if not( trsValueFatherParent   == 0 ): return self.parent(   trsValue , trsValueFatherParent   )
		if not( trsValueFatherUnparent == 0 ): return self.unParent( trsValue , trsValueFatherUnparent )	
		if not( mirrorPlanCoords       == 0 ): return self.mirror(   trsValue , mirrorPlanCoords , mirrorUnlockAxe , mirrorRecomputeAxes )
		if not( offsetItselfTrs        == 0 ): return self.offsetItself( offsetItselfTrs )
		if not( offsetParentTrs        == 0 ): return self.offsetParentTrs( offsetParentTrs , offsetParentTrsUnder )
		if not( IntersectPlaneCoords   == 0 ): return self.intersectPlane( IntersectPlaneCoords , IntersectVectorDir )		
		if not( lineCoords             == 0 ): return self.snapOnLine( lineCoords )
		if not( snapPlaneCoords        == 0 ): return self.snapOnPlane( snapPlaneCoords )
		if not( curveName              == 0 ): return self.snapOnCurve( curveName )
		if not( axisUp                 == 0 ): return self.setAxisUp( axisUp )
		if not( inverseAxes            == 0 ): return self.inverseAxes( inverseAxes )
		if not( closetEulerRotation    == 0 ): return self.convertRotToClosetEulerSolution( closetEulerRotation )
		if not( aimPoint               == 0 ): return self.aim( aimPoint , aimAxe )
		if not( aimVector              == 0 ): return self.setAim( aimVector , aimAxe )
		if not( middleTrsTarget        == 0 ): return self.getMiddleTrs( middleTrsTarget )
		'''
		if not( trsValueFather         == 0 ): return self.getTrsRotateAxeOriented( axeDirParent  , axeRotateParent , axeRotateChildren )
		if not( trsValueFather == 0 ): return self.projectAngle( trsOrigine , angleOffset , axe )
		'''
		childrenTrsValue = self.updateClassValue( trsValue , childrenTrsValue , updateValue , toModif )		

	def parent( self , trsValue , trsValueFather ):	
		matrix  = self.toMMatrix( trsValue       )	
		matrixP = self.toMMatrix( trsValueFather )		
		matrixP = matrixP.inverse()		
		mChild  = matrix * matrixP
		mtChild = ompy.MTransformationMatrix( mChild )
		trs     = mtChild.translation( ompy.MSpace.kWorld) + mtChild.rotationComponents() + mtChild.scale( ompy.MSpace.kWorld)
		trs[3:6]= [ math.degrees(trs[3]) , math.degrees(trs[4]) , math.degrees(trs[5]) ]	
		return trs	

	def unParent( self , trsValue , trsValueFather ):
		matrix  = self.toMMatrix( inValue = trsValue )				
		matrixP = self.toMMatrix( inValue = trsValueFather )			
		mChild  = matrix * matrixP
		mtChild = ompy.MTransformationMatrix( mChildren )
		trs     = mtChild.translation( ompy.MSpace.kWorld) + mtChild.rotationComponents() + mtChild.scale( ompy.MSpace.kWorld)
		trs[3:6]= [ math.degrees(trs[3]) , math.degrees(trs[4]) , math.degrees(trs[5]) ]	
		return trs	

	def mirror( self , trsValue , planSymCoords , unlockAxe = 2 , recomputeAxes = 0 ):	
		# GET TRIPLE VECTORS COORDS
		tripleOrientVector = self.toTripleVectors( trsValue )

		tripleOrientTrs = []			
		for i in range( 0 , len(tripleOrientVector), 3 ): 			
			tripleOrientTrs.append( [ tripleOrientVector[i+0] + trsValue[0] , tripleOrientVector[i+1] + trsValue[1] , tripleOrientVector[i+2] + trsValue[2] ] + trsValue[3:9]  )

		# GET COORDS ON PLANE
		trsMiddle = self.snapOnPlane( planSymCoords , inValue = trsValue , updateValue = 0 )

		# GET TRIPLE VECTORS COORDS ON PLANE		
		tripleOrientTrsMiddle = []
		for trs in tripleOrientTrs:
			tripleOrientTrsMiddle.append( self.snapOnPlane( planSymCoords , inValue = trs , updateValue = 0 ) ) 
			
		# GET VECTOR Normal->Symetrie
		manipVtoSym = [ ( trsMiddle[0] - trsValue[0] )*2 , ( trsMiddle[1] - trsValue[1] )*2 , ( trsMiddle[2] - trsValue[2] )*2 ]
		
		tripleOrientVToSym = []
		for i in range( 0 , len( tripleOrientTrsMiddle ) ):
			tmpVector =  [ ( tripleOrientTrsMiddle[i][0] - tripleOrientTrs[i][0] )*2 , ( tripleOrientTrsMiddle[i][1] - tripleOrientTrs[i][1] )*2 , ( tripleOrientTrsMiddle[i][2] - tripleOrientTrs[i][2] )*2 ]
			tripleOrientVToSym.append( tmpVector )
		
		#GET SYMETRIE COORD	
		manipCoordsSym = [ trsValue[0] + manipVtoSym[0] , trsValue[1] + manipVtoSym[1] , trsValue[2] + manipVtoSym[2] ]

		#GET SYMETRIE TRIPLE VECTORS COORDs
		tripleOrientTrsSym = []
		tripleOrientVectorSym = []		
		for i in range( 0 , len( tripleOrientTrs ) ):
			tripleOrientTrsSym =  [ tripleOrientTrs[i][0] + tripleOrientVToSym[i][0] , tripleOrientTrs[i][1] + tripleOrientVToSym[i][1] , tripleOrientTrs[i][2] + tripleOrientVToSym[i][2] ] 
			tripleOrientVectorSym.append( [ tripleOrientTrsSym[0] - manipCoordsSym[0] , tripleOrientTrsSym[1] - manipCoordsSym[1] , tripleOrientTrsSym[2] - manipCoordsSym[2] ]    )
			

		# set same side for mirror axes	
		outVectors = tripleOrientVectorSym	
		
		if( recomputeAxes == 1 ):
		
			closestAxis = self.toClosestAxis( tripleOrientTrs[i] , returnList = 0 , inValue = trsValue )

			for i in range( 0 , 3 ):
				vAxeMirror    = ompy.MVector( tripleOrientVectorSym[i][0] , tripleOrientVectorSym[i][1] , tripleOrientVectorSym[i][2] )			
				closestAxis   = self.toClosestAxis( tripleOrientVectorSym[i] , returnList = 0 , inValue = trsValue )
				signTmp = 1 
				if( closestAxis > 2 ):
					closestAxis -=  3
					signTmp      = -1
        	
				vAxeMirror    = vAxeMirror * signTmp
				outVectors[abs(closestAxis)] = [ vAxeMirror.x , vAxeMirror.y , vAxeMirror.z ] 
		
		# get rotation	
		rotSym = self.createFromTripleVectors( outVectors[0] , outVectors[1] , outVectors[2]  , unlockAxe = unlockAxe , updateValue = 0 )
		# get TRS			
		mirrorTrsValue =  manipCoordsSym[0:3] + rotSym[3:6] + trsValue[6:9]		
			
		return mirrorTrsValue		
	

	def offsetItself( self , trsValue , offsetTrs ):		
		return self.unParent( trsValue , offsetTrs )					
				
	def offsetParentTrs( self , trsValue ,  parentTrs , offsetTrsUnder ):
		newTrs = trsValue		
		#__________________________ TRANSFORM
		newParentTrs = [ parentTrs[i] + offsetTrsUnder[i] for i in range( 0 , 9 ) ]
		mEulerRot    = ompy.MEulerRotation( math.radians(offsetTrsUnder[3]) , math.radians(offsetTrsUnder[4]) , math.radians(offsetTrsUnder[5]) ) 
		
		vChidrenParent   = [  trsValue[0] - parentTrs[0]  ,  trsValue[1] - parentTrs[1]  ,  trsValue[2] - parentTrs[2]  ]
		vChidrenParentS  = ompy.MVector(  vChidrenParent[0] * offsetTrsUnder[6]  ,  vChidrenParent[1] * offsetTrsUnder[7]  ,  vChidrenParent[2] * offsetTrsUnder[8]  )	
		vChidrenParentRS = vChidrenParentS.rotateBy( mEulerRot )
			
		newTrs[0:3] = [  ( newParentTrs[0] + vChidrenParentRS.x )  ,  ( newParentTrs[1] + vChidrenParentRS.y )  ,  ( newParentTrs[2] + vChidrenParentRS.z )  ]	
	
		#__________________________ ROTATE
		tripleVectors = self.toTripleVectors( inValue = trsValue )
		
		for i in range( 0 , len(tripleVectors) , 3 ):
			mvAxe  = ompy.MVector(  tripleVectors[i+0] ,  tripleVectors[i+1]  ,  tripleVectors[i+2]  )
			mvAxe  = mvAxe.rotateBy(  mEulerRot  )
			tripleVectors[i] = [ mvAxe.x , mvAxe.y , mvAxe.z ]
		
		newRot = self.createFromTripleVectors( tripleVectors[0] , tripleVectors[1] , tripleVectors[2] , updateValue = 0 )	
		newTrs[3:6] = newRot[3:6]
	
		return newTrs
			
	def intersectPlane( self , trsValue , planeCoords , vectorDir ):		

		nearestPlaneCoords = self.snapOnPlane( trsValue , planeCoords )
		
		vDirection = ompy.MVector( vectorDir[0] , vectorDir[1] , vectorDir[2] )
		vDirection.normalize()
		normal     = ompy.MVector( ( nearestPlaneCoords[0] - trsValue[0] ) , ( nearestPlaneCoords[1] - trsValue[1] ) , ( nearestPlaneCoords[2] - trsValue[2] ) )
    	
		angleVector = math.degrees( vDirection.angle(normal) )	
		dist        = abs( normal.length()  / math.cos(angleVector) )
    	
		newCoords = [  vDirection.x * dist + trsValue[0]  , vDirection.y * dist + trsValue[1]  , vDirection.z * dist + trsValue[2]  ]  

		newTrs = newCoords + trsValue[3:9] 		
			
		return newTrs			
		
			
		
	#________________________________________________________________________________________________________________________________________________________________________________ snapOnLine	
	def snapOnLine( self , lineCoords , inValue = None , updateValue = 1 , toModif = [ 1 , 1 , 1 ] ):
		'''
			with a 2 coords plane and an old coords get the snapped version of oldCoords in plane
		
		'''			
		trsValue = self.utils_overrideTrsValue( inValue )

		vectorRef       = ompy.MVector( ( lineCoords[3] - lineCoords[0] ) , ( lineCoords[4] - lineCoords[1] ) , ( lineCoords[5] - lineCoords[2] ) )
		vectorOldCoords = ompy.MVector( ( trsValue[0]   - lineCoords[0] ) , ( trsValue[1] - lineCoords[1] ) , ( trsValue[2] - lineCoords[2] ) )
		angleA                  = vectorRef.angle( vectorOldCoords )
			
		dist = math.cos( angleA ) * vectorOldCoords.length()
		
		vectorRef.normalize()
			
		newCoords = [  vectorRef.x * dist + lineCoords[0][0] , vectorRef.y * dist + lineCoords[0][1] , vectorRef.z * dist + lineCoords[0][2] ] 
		newTrs = newCoords + trsValue[3:9] 

		newTrs = self.updateClassValue( trsValue , newTrs , updateValue , toModif )				
			
		return newTrs	
	
	#________________________________________________________________________________________________________________________________________________________________________________ snapOnPlane	
	
	def snapOnPlane( self , planeCoords , inValue = None , updateValue = 1 , toModif = [ 1 , 1 , 1 ] ):
		
		'''
			with a 3 coords plane and an old coords get the snapped version of oldCoords in plane
		
		'''
		trsValue = self.utils_overrideTrsValue( inValue )
			
		vPlaneA  =  [ ( planeCoords[3] - planeCoords[0] ) , ( planeCoords[4] - planeCoords[1] ) , ( planeCoords[5] - planeCoords[2] )  ] 
		vPlaneB  =  [ ( planeCoords[6] - planeCoords[0] ) , ( planeCoords[7] - planeCoords[1] ) , ( planeCoords[8] - planeCoords[2] )  ] 	
		rawDir   =  [ ( planeCoords[0] - trsValue[0]    ) , ( planeCoords[1] - trsValue[1]    ) , ( planeCoords[2] - trsValue[2]    )  ] 
		
		vPlaneNormal = self.get2VectorsNormal( vPlaneA , vPlaneB , rawDir )
		
		newCoords = self.getNearestCoordsOnPlane( planeCoords , trsValue[0:3] , vPlaneNormal ) 				
		
		newTrs = newCoords	+ trsValue[3:9]	
				
		newTrs = self.updateClassValue( trsValue , newTrs , updateValue , toModif )				
			
		return newTrs
			
	
		
	#________________________________________________________________________________________________________________________________________________________________________________ snapOnCurve		
	def snapOnCurve( self , curveName , inValue = None , updateValue = 1 , toModif = [ 1 , 1 , 1 ] ):	

		'''
			get a point on curveName witch is the closest of the given coords.
			it return [ [ coordX , coordY , coordZ ] , u ]
		'''
		trsValue = self.utils_overrideTrsValue( inValue )		
		
		pointApi = ompy.MPoint( trsValue[0] , trsValue[1] , trsValue[2] )
		curveApi = ompy.MFnNurbsCurve( self.getMDagPath( curveName ) )	
		closestPointInfo = curveApi.closestPoint(pointApi)

		u = closestPointInfo[1] 
		
		trsValue = self.createFromCurve( curveName , u , updateValue = 0 )	
			
		trsValue = self.updateClassValue( self.value , trsValue , updateValue , toModif )				
			
		return trsValue		 		
			 
			
		
	#________________________________________________________________________________________________________________________________________________________________________________ setAxisUp			
	def setAxisUp( self , axis , inValue = None , updateValue = 1 , toModif = [ 1 , 1 , 1 ] ):

		trsValue = self.utils_overrideTrsValue( inValue )

		# get actual AxisUp
		tripleVectors = self.toTripleVectors( inValue = trsValue )
		vectorValuesY = [ tripleVectors[1] , tripleVectors[1+3] , tripleVectors[i][1+6] ]			
		vectorValuesY.sort()
		actualAxisUp = [ i for i in range( 0 , 3 ) if( tripleVectors[i][1] == vectorValuesY[-1] ) ]
		
		# reset to Y UP 
		offset = [0,0,0,0,0,0,1,1,1]
		
		if( actualAxisUp[0] == 0):
			offset[3:6] = [ 0 , 0 , -90 ] 
		elif( actualAxisUp[0] == 2):
			offset[3:6] = [ 90 , 0 , 0 ] 		

		trsValue = self.offsetItself(  offset , inValue = trsValue , updateValue = 0 )		
		
		
		# change axe 		
		offset = [0,0,0,0,0,0,1,1,1]
		
		if( axis == 'X' ):
			offset[3:6] = [ 0 , 0 , 90 ]   	
		elif( axis == 'Z' ):
			offset[3:6] = [ -90 , 0 , 0 ]   				
		
		trsOffset = self.offsetItself(  offset , inValue = trsValue , updateValue = 0 )	
		
		trsOffset = self.updateClassValue( trsValue , trsOffset , updateValue , toModif )	
			
		return trsOffset 

	#________________________________________________________________________________________________________________________________________________________________________________ inverseAxes
	def inverseAxes( self , inverseAxes  , trsChoice = [ 0 , 1 , 0 ] , inValue = None , updateValue = 1 , toModif = [ 1 , 1 , 1 ] ):
	
		'''
			inverseAxes = [ 0 , 0 , 0 ] , represent X Y Z axes
			
			warning: you can only inverse 2 axes at the same time
		
		'''			
		trsValue = self.utils_overrideTrsValue( inValue )	
			
		newTrs = trsValue
		#translate
		if( trsChoice[0] ):
			for i in range( 0 , 3 ):
				newTrs[i] =  newTrs[i] * ( 1 - inverseAxes[i] ) - newTrs[i] * inverseAxes[i]  
			
		# rotate
		if( trsChoice[1] ):	
			
			offset = [0,0,0,0,0,0,1,1,1]
			
			if( inverseAxes == [ 0 , 0 , 0 ] ):
				pass
			elif( inverseAxes == [ 1 , 1 , 0 ]  ):
				offset[3:6] = [ 0 , 0 , 180 ]
			elif( inverseAxes == [ 1 , 0 , 1 ]  ):
				offset[3:6] = [ 0 , 180 , 0 ] 
			elif( inverseAxes == [ 0 , 1 , 1 ]  ):
				offset[3:6] = [ 180 , 0 , 0 ]		
			else:
				mc.error('you can only inverse 2 axes at the same time')
			
			newTrs = self.offsetItself(  offset , inValue = newTrs , updateValue = 0 )	
			
		#scale	
		if( trsChoice[2] ):	
			for i in range( 6 , 9 ):
				newTrs[i] =  newTrs[i] * ( 1 - inverseAxes[i-6] ) - newTrs[i] * inverseAxes[i-6]  

				
		newTrs = self.updateClassValue( trsValue , newTrs , updateValue , toModif )
		
		return newTrs				
		
	#________________________________________________________________________________________________________________________________________________________________________________ convertRotToClosetEulerSolution
	def convertRotToClosetEulerSolution( self , rotValueTarget , inValue = None , updateValue = 1 ):			
	
		'''
			with the rotValue, it will find the closest XYZ rot to the target, but the orient stay the same of course 	
		'''
		trsValue = self.utils_overrideTrsValue( inValue )	
			
		rotValue = trsValue[3:6]
		eRotBase   = ompy.MEulerRotation( math.radians(rotValue[0]) , math.radians(rotValue[1]) , math.radians(rotValue[2]) )
		
		eRotTarget = ompy.MEulerRotation( math.radians(rotValueTarget[0]) , math.radians(rotValueTarget[1]) , math.radians(rotValueTarget[2]) )
		eRot = eRotBase.closestSolution(eRotTarget)
		
		newRot = [ math.degrees(eRot.x) , math.degrees(eRot.y) , math.degrees(eRot.z) ]

		if( updateValue == 1 ):
			self.value[3:6] = newRot			

		return trsValue[0:3] + newRot + trsValue[6:9]

		
	#________________________________________________________________________________________________________________________________________________________________________________ projectAngle			
	def projectAngle( self , trsOrigine , angleOffset , axe , inValue = None , updateValue = 1  , toModif = [ 1 , 1 , 1 ] ):

		'''
			 	
		'''
		trsValue = self.utils_overrideTrsValue( inValue )	
		
		# INIT
		offsetTmp         = [ 0  , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1 ]
		offsetTmp[axe]    = 1
		trsAngleOffset    = [0,0,0] + angleOffset + [1,1,1]		
		vTargetOrig       = ompy.MVector( trsToProject[0] - trsOrigine[0]  , trsToProject[1] - trsOrigine[1] , trsToProject[2] - trsOrigine[2]   )
		
		vDirValues        = self.toTripleVectors( inValue = trsOrigine )[axe]
		vDir              = ompy.MVector( vDirValues[0] , vDirValues[1] , vDirValues[2] )

		# get Vector angle			
		trsAngleWorld     = self.offsetItself( trsAngleOffset  , inValue = trsOrigine , updateValue = 0 )
		trsAngleWorld[0:3]=  [0,0,0]		
		trsDir            = self.offsetItself( offsetTmp , inValue = trsAngleWorld   , updateValue = 0 )
		vAngle            = ompy.MVector( trsDir[0]  , trsDir[1] , trsDir[2] )
		
		# trs on vector dir
		
		angleTmp          = vDir.angle( vTargetOrig )				
		distTmp           = vTargetOrig.length() * math.cos( angleTmp )
		vTmp              = vDir * distTmp

		# trs on vector Angle	

		angleTmp          = vAngle.angle( vTmp )				
		distTmp           = distTmp / math.cos( angleTmp )
		vAngle.normalize()
		vCoords           = vAngle * distTmp

		
		# OUT		
		newTrs      = trsToProject[:] 
		newTrs[0:3] = [ vCoords.x + trsOrigine[0] , vCoords.y + trsOrigine[1] , vCoords.z + trsOrigine[2] ] 

		
		newTrs = self.updateClassValue( trsToProject , newTrs , updateValue , toModif )	
		
		return newTrs		
	
	#________________________________________________________________________________________________________________________________________________________________________________ setAim	

	
	def aim( self , point , aimAxe = None , inValue = None , updateValue = 1  , toModif = [ 1 , 1 , 1 ] ):
		trsValue = self.utils_overrideTrsValue( inValue )
		aimVector = [ point[0] - trsValue[0] , point[1] - trsValue[1] , point[2] - trsValue[2] ]
		print( trsValue , aimVector)
		newTrs = self.setAim( aimVector , aimAxe , trsValue , updateValue  , toModif )
		newTrs = self.updateClassValue( trsValue , newTrs , updateValue , toModif )	
		return newTrs				
		

	
	def setAim( self , aimVector , axeAim = None , inValue = None , updateValue = 1  , toModif = [ 1 , 1 , 1 ] ):

		trsValue = self.utils_overrideTrsValue( inValue )
		vectorUp = [ 0 , 1 , 0  ]		
		#GET AIM AXE
		if( axeAim == None ):			
			axeAim = self.toClosestAxis( aimVector , inValue = trsValue  )		
			if( 2 < axeAim ): axeAim -= 3
		#GET UP AXE				
		axes = self.toClosestAxis( vectorUp , returnList = True , inValue = trsValue  )
		axeUp = axes[0]			
		if( axeUp == axeAim )or( axeUp == (axeAim+3) ):
			axeUp = axes[1]

		if( axeUp > 2 ): axeUp -= 3
		#GET SIDE AXE			
		axis = [ 0 , 1 , 2 ]
		axis.remove( axeAim )
		axis.remove( axeUp  )
		axeSide = axis[0]
		#BUILD NEW TRS	
		tripleVector = self.toTripleVectors( inValue = trsValue )
		tripleVector[axeAim*3:axeAim*3+3] = aimVector
		trsTmp = self.createFromTripleVectors( tripleVector[0:3] , tripleVector[3:6] , tripleVector[6:9] , updateValue = 0 )		
		newTrs = trsValue[0:3] + trsTmp[3:6] + trsValue[6:9]		
		newTrs = self.updateClassValue( trsValue , newTrs , updateValue , toModif )	
		return newTrs				
		
		
	#________________________________________________________________________________________________________________________________________________________________________________ toPlaneCoords
	def getMiddleTrs( self , trsTarget , inValue = None  , updateValue = 1  , toModif = [ 1 , 1 , 1 ] ): 
		
		'''
			get the middle 
			position    = barycentre
			orientation = aim B--->A , but orient base influence by A
			scale       = represent by a box between A and B with value 1 for a side by default, scale base influence by A
			
		'''
		trsValue = self.utils_overrideTrsValue( inValue )
			
		middleTrs = [0,0,0,0,0,0,1,1,1]
		
		# POSITION
		middleTrs[0:3]  = [ ( trsValue[0] + trsTarget[0] ) / 2 , ( trsValue[1] + trsTarget[1] ) / 2 , ( trsValue[2] + trsTarget[2] ) / 2 ]
		
		# ROTATION

		vectorAim  = [ trsTarget[0] - trsValue[0] , trsTarget[1] - trsValue[1] , trsTarget[2] - trsValue[2]  ]
		axis       = self.toClosestAxis( vectorAim , inValue = trsValue  )		
		if( axis > 2 ):
			axisAim = axis - 3
		else:
			axisAim = axis
						
		vectorUp    = [ 0 , 1 , 0  ]
		axis = self.toClosestAxis( vectorUp , returnList = True , inValue = trsValue  )		
		if( axis[0] == axisAim ) or ( axis[0] == ( axisAim + 3 ) ):
			axisUp = axis[1]
		else:
			axisUp = axis[0]	
		
		if( axisUp > 2 ):
			axisUp -= 3
			
		axis = [ 0 , 1 , 2 ]
		axis.remove( axisAim )
		axis.remove( axisUp  )
		axisSide = axis[0]

		tripleVector = self.toTripleVectors( inValue = trsValue  )
		tripleVector[axisAim*3:axisAim*3+3] = vectorAim

		trsTmp = self.createFromTripleVectors( tripleVector[0:3] , tripleVector[3:6] , tripleVector[6:9] , accuracyOrder = [ axisAim ,  axisUp , axisSide ] , updateValue = 0 )

		middleTrs[3:6] = trsTmp[3:6]			


		# SCALE
		
		distanceAim = ompy.MVector( vectorAim[0] , vectorAim[1] , vectorAim[2] ).length()

		scaleTmp = trsValue[6:9] 
		scaleTmp[axisAim] = distanceAim 

		middleTrs[6:9] = scaleTmp
		
		newTrs = self.updateClassValue( trsValue , middleTrs , updateValue , toModif )
		
		return middleTrs 
					
		
		
	#________________________________________________________________________________________________________________________________________________________________________________ getTrsRotateAxeOriented	
	
	def getTrsRotateAxeOriented( self , axeDirParent  , axeRotateParent , axeRotateChildren , inValue = None , updateValue = 1  , toModif = [ 1 , 1 , 1 ] ):
		
		'''
		way to set properly limit collision manip in different Orientation
		axeAttr = [ 1 , 2 , 3 , -1 , -2 , -3 ]
					x	y   z   -x   -y  -z
		
		trsValue = parent value
		
		rotAxe = 1  axesTranPositiveWay = 2 ,  3 , -2 , -3 
		rotAxe = 2  axesTranPositiveWay = 3 ,  1 , -3 , -1  		
		rotAxe = 3  axesTranPositiveWay = 1 ,  2 , -1 , -2 			
		
		'''		
		axeTranList = [ [2,3,-2,-3] , [3,1,-3,-1] , [1,2,-1,-2] ]
		
		trsValue = self.utils_overrideTrsValue( inValue )
		parentTrs = trsValue
		
		vDirRef  = ompy.MVector( 1 , 0 , 0 )
		vUpRef   = ompy.MVector( 0 , 1 , 0 )
		vFreeRef = ompy.MVector( 0 , 0 , 1 )
		
		pVectors     = self.toTripleVectors( inValue = parentTrs )
		pVectorsObjs = [ ompy.MVector( pVectors[0] , pVectors[1] , pVectors[2] ) , ompy.MVector( pVectors[3] , pVectors[4] , pVectors[5] ) , ompy.MVector( pVectors[5] , pVectors[6] , pVectors[7] )  ]
		
		# GET OUTS VECTORS WITH AXE ROTATE CHILDREN
		'''
			avec parentTrs , axeDirParent et axeRotateParent parent , on trouve le triple vecteur correspondant au chidren
			par defaut on va prendre X en vDir et Y en vUp
		'''

		vDirRef   = pVectorsObjs[ abs(axeDirParent) - 1 ] #* math.copysign( 1 , axeDirParent  )		
	
		# get vUpRef
		axeDirIndex = axeTranList[ abs(axeRotateParent) - 1 ].index( axeDirParent )		
		axeUpIndex  = int( axeDirIndex + math.copysign( 1 , axeRotateParent ) )		
		axeUpIndex  = utilsMath.specialClamp( axeUpIndex , 0 , 4 )		
		axeUpParent = axeTranList[ abs(axeRotateParent) - 1 ][axeUpIndex]		
		vUpRef = pVectorsObjs[ abs(axeUpParent) - 1 ] * math.copysign( 1 , axeUpParent  )	
		
		# GET OUTS VECTORS WITH AXE ROTATE CHILDREN
		'''
			pour trois axes donne, et un axe/sens de rotation , on met le sens de rotation du fils entre le vDir et vUp	
		'''	

		inVectors  = [ vDirRef , vUpRef , vFreeRef ]  		
		outVectors = [ vDirRef , vUpRef , vFreeRef ]  		
		
		if( axeRotateChildren == 1 ): # X			
			axeDir  =  3 # Z
			axeUp   = -2 #-Y
			axeFree = axeRotateChildren
			
		elif( axeRotateChildren == 2 ): # Y
			axeDir  =  1 # X
			axeUp   =  3 # Z 
			axeFree = axeRotateChildren
			
		elif( axeRotateChildren == 3 ): # Z
			axeDir  = 1 # X
			axeUp   = 2 # Y 
			axeFree = axeRotateChildren
			
		elif( axeRotateChildren == -1 ): # -X
			axeDir  = -3 # Z
			axeUp   = 2 # Y
			axeFree = axeRotateChildren * -1
			
		elif( axeRotateChildren == -2 ): # -Y
			axeDir  = 1 # X
			axeUp   = -3 # Z
			axeFree = axeRotateChildren * -1 
			
		elif( axeRotateChildren == -3 ): # -Z
			axeDir  =  1 # X
			axeUp   = -2 # -Y 
			axeFree = axeRotateChildren * -1			
		
			
		outVectors[0]   = inVectors[abs(axeDir)  - 1 ] * math.copysign( 1 , axeDir  )
		outVectors[1]   = inVectors[abs(axeUp)   - 1 ] * math.copysign( 1 , axeUp   )
		outVectors[2]   = inVectors[abs(axeFree) - 1 ] * math.copysign( 1 , axeFree )			
		freeAxe         = abs( axeFree ) - 1
		freeAxe = 2 # il ne peut pas y avoir de free axe , tout les axes sont important		

		childrenTrs	= self.createFromTripleVectors( [ outVectors[0].x , outVectors[0].y , outVectors[0].z ] , [ outVectors[1].x , outVectors[1].y , outVectors[1].z ] , [ outVectors[2].x , outVectors[2].y , outVectors[2].z ] , unlockAxe = freeAxe , updateValue = 0 )

		
		# OUTPUT	
		newTrs = parentTrs[0:3] + childrenTrs[3:6] + parentTrs[6:9]
		newTrs = self.updateClassValue( trsValue , newTrs , updateValue , toModif )	

		
		return newTrs						
		
				
		
	#################################################################################################################################################################################		
	# SURCHARGE ################################################################################################################################################################################ SURCHARGE 
	#################################################################################################################################################################################
	
	#________________________________________________________________________________________________________________________________________________________________________________  print	
	def __repr__( self ):
		
		return repr(self.value)
	
	#________________________________________________________________________________________________________________________________________________________________________________  len	
	def  __len__( self ):
		
		return len(self.value)
		
		
	#________________________________________________________________________________________________________________________________________________________________________________ []	
	def __getitem__( self, index ): 
		
		return self.value[index] 	
		
	#________________________________________________________________________________________________________________________________________________________________________________ []=	
	def __setitem__ ( self, index , valeur ):
		
		self.value[index] = valeur		
		
	#________________________________________________________________________________________________________________________________________________________________________________ +
	def __add__( self, trsValueToAdd ):
					
		try:		
			for i in range( 0 , len( trsValueToAdd ) ):
				self.value[i] += trsValueToAdd[i]
		except:
			for i in range( 0 , len( self.value ) ):
				self.value[i] += trsValueToAdd
				
		return self.value 			
	
	#________________________________________________________________________________________________________________________________________________________________________________ -	
	def __sub__( self, trsValueToSubstract ):
			
		try:		
			for i in range( 0 , len( trsValueToSubstract ) ):
				self.value[i] -= trsValueToSubstract[i] 	
		except:
			for i in range( 0 , len( self.value ) ):
				self.value[i] -= trsValueToSubstract 
				
		return self.value 		
		
	#________________________________________________________________________________________________________________________________________________________________________________ *	
	def __mul__( self, trsValueToMult ):

		try:		
			for i in range( 0 , len( trsValueToMult ) ):
				self.value[i] *= trsValueToMult[i] 	
		except:
			for i in range( 0 , len( self.value ) ):
				self.value[i] *= trsValueToMult 	
							
		return self.value 
		
	#________________________________________________________________________________________________________________________________________________________________________________ /	
	def __truediv__( self, trsValueToDiv ):
		
		'''
			doesnt work - dont know why..,
		'''
		
		try:		
			for i in range( 0 , len( trsValueToDiv ) ):
				self.value[i] /= trsValueToDiv[i] 	
		except:
			for i in range( 0 , len( self.value ) ):
				self.value[i] /= trsValueToDiv 	
				
		return self.value 



	#################################################################################################################################################################################		
	################################################################################################################################################################################# UTILS
	################################################################################################################################################################################# 			
  
	def get2VectorsNormal( self , vectorA , vectorB , vMoyen ):
		normalx = ((vectorA[1])*(vectorB[2])-(vectorA[2])*(vectorB[1]))
		normaly = ((vectorA[2])*(vectorB[0])-(vectorA[0])*(vectorB[2]))
		normalz = ((vectorA[0])*(vectorB[1])-(vectorA[1])*(vectorB[0]))
		
		vecteurNormal = ompy.MVector( normalx   , normaly   , normalz   )
		vectorMoyen   = ompy.MVector( vMoyen[0] , vMoyen[1] , vMoyen[2] ) 
		
		coef = math.copysign( 1 , vecteurNormal*vectorMoyen )
		
		vecteurNormal = ompy.MVector( normalx * coef , normaly * coef  , normalz * coef  )
		    	     
		return [ vecteurNormal.x , vecteurNormal.y , vecteurNormal.z ] 		
			
	
	#________________________________________________________________________________________________________________________________________________________________________________ getNearestCoordsOnPlane
					
	def getNearestCoordsOnPlane( self , planeCoords , oldCoords , vDirection ):		
		'''		
			with oldcoords , a direction and the planeCoords find the point snap in the plan 	
		'''	
		mvDirection = ompy.MVector( vDirection[0] , vDirection[1] , vDirection[2] )
		mvDirection.normalize()
		vDirection = [ mvDirection.x , mvDirection.y , mvDirection.z ]
		
		# on determine d de la formule du plan  2x + 3y + 7z +d = 0
		
		d = ( ( vDirection[0] *  planeCoords[0] ) + ( vDirection[1] *  planeCoords[1] ) + ( vDirection[2] *  planeCoords[2] ) ) * -1 
		
		# on determine la distance entre le point de la ligne et le point de l'intersection
		
		dist = (   - ( vDirection[0] * oldCoords[0] ) - ( vDirection[1] * oldCoords[1] ) - ( vDirection[2] * oldCoords[2] ) - d  ) / ( ( vDirection[0] * vDirection[0] ) + ( vDirection[1] * vDirection[1] ) + ( vDirection[2] * vDirection[2] )   ) 	
		
		# on determine les coordoonee de l'intersection
		
		iCoords = [  vDirection[0] * dist + oldCoords[0] , vDirection[1] * dist + oldCoords[1] , vDirection[2] * dist + oldCoords[2] ] 
		
		return iCoords
	
	#________________________________________________________________________________________________________________________________________________________________________________ getMDagPath 
	
	def getMDagPath( self , obj ):	
		
		'''
		convert maya name into dagPath , very use to manipulate obj in API	
		'''
	
		selection = ompy.MSelectionList()
		selection.add( obj )
		
		dagPath= ompy.MDagPath()
		dagPath = selection.getDagPath( 0 )
		
		return dagPath	
		

	#________________________________________________________________________________________________________________________________________________________________________________ getBarycentre			
	
	def utils_getBarycentre( self , coords , nbrAxis = 3  ):
		barycentre = [0] * nbrAxis
		#ADD ALL COORDS TOGETHER
		for i in range( 0 , len( coords ) , nbrAxis):
			for j in range( 0 , nbrAxis ):
				barycentre[j] += coords[i+j]
		#DIVIDE WITH THE NBR OF POINTS
		nbrPoints = len( coords ) / nbrAxis
		for j in range( 0 , nbrAxis ):
			barycentre[j] /= nbrPoints
		#RETURN BARYCENTRE
		return barycentre	

			

	#________________________________________________________________________________________________________________________________________________________________________________ getBBreelCoords
	
	def getBBreelCoords( self , coords ):

		path = 'D:\mcantat_BDD\projects\code\maya\python\plugIn\getOrientedBoundingBox.py' 
		mc.loadPlugin( path , qt = True )	
		
		flattenCoords = [ c for coord in coords for c in coord ]
	
		reelBBCoords = mc.MC_getRotatedBBCoordsCmd( flattenCoords )
		
		reelBBCoords3 = []
		for i in range( 0 , len( reelBBCoords ) , 3 ):
			reelBBCoords3.append( [ reelBBCoords[i] , reelBBCoords[i+1] , reelBBCoords[i+2] ] )	
		
		return reelBBCoords3
	
	#________________________________________________________________________________________________________________________________________________________________________________ getOrientedBoundingBoxPosition
	
	def getOrientedBoundingBoxPosition( self , obbPoints ):
	
	
		baseA = obbPoints[0:3] 	
		baseB = obbPoints[3:6] 
		baseC = obbPoints[6:9]
		baseD = obbPoints[9:12]
		topA  = obbPoints[12:15]
		topB  = obbPoints[15:18]
		topC  = obbPoints[18:21]
		topD  = obbPoints[21:24]
	
		centreBBreel   = self.utils_getBarycentre( obbPoints )	
		
		centreBaseABCD = self.utils_getBarycentre( ( baseA + baseB + baseC + baseD ) )
		centreTopABCD  = self.utils_getBarycentre( ( topA + topB + topC + topD )  )
		
		centreCoteA  = self.utils_getBarycentre(  ( baseA + baseB + topA + topB ) )
		centreCoteB  = self.utils_getBarycentre(  ( baseB + baseC + topB + topC ) )
		centreCoteC  = self.utils_getBarycentre(  ( baseC + baseD + topC + topD ) )
		centreCoteD  = self.utils_getBarycentre(  ( baseD + baseA + topD + topA ) )
		               
		positions = [ centreBBreel , centreBaseABCD , centreTopABCD , centreCoteA , centreCoteB , centreCoteC , centreCoteD ]
	
		return positions     
	
	#________________________________________________________________________________________________________________________________________________________________________________ getOrientedBoundingBoxOrientation

	def getOrientedBoundingBoxOrientation( self , obbPoints ):
		
		baseB = obbPoints[3:6]
		baseD = obbPoints[9:12] 	
		baseC = obbPoints[0:3]
		topC  = obbPoints[12:15]
			
		vX = [  baseB[0] - baseC[0]  ,  baseB[1] - baseC[1]  ,  baseB[2] - baseC[2]  ]	
		vY = [   topC[0] - baseC[0]  ,   topC[1] - baseC[1]  ,   topC[2] - baseC[2]  ]
		vZ = [  baseD[0] - baseC[0]  ,  baseD[1] - baseC[1]  ,  baseD[2] - baseC[2]  ]
		    
		trs = self.createFromTripleVectors( vX , vY , vZ , updateValue = 0)    
		rotXYZ = trs[3:6]
		return rotXYZ   		
			
	#________________________________________________________________________________________________________________________________________________________________________________ getOrientedBoundingBoxOrientationScale
	
	def getOrientedBoundingBoxOrientationScale( self , obbPoints ):
		
		baseB = obbPoints[3:6]
		baseD = obbPoints[9:12] 	
		baseC = obbPoints[0:3]
		topC  = obbPoints[12:15]
	
		dX = ompy.MVector(   baseB[0] - baseC[0]  ,  baseB[1] - baseC[1]  ,  baseB[2] - baseC[2]  ).length()	
		dY = ompy.MVector(    topC[0] - baseC[0]  ,   topC[1] - baseC[1]  ,   topC[2] - baseC[2]  ).length()	
		dZ = ompy.MVector(   baseD[0] - baseC[0]  ,  baseD[1] - baseC[1]  ,  baseD[2] - baseC[2]  ).length()	
	
	    
		return [ dX , dY , dZ ] 
	
	#________________________________________________________________________________________________________________________________________________________________________________ getOrientedBoundingBoxOrientationScale			
	
	def updateClassValue( self , oldTrs , newTrs , updateValue ,  toModif ):
		
			
		oldTrs = oldTrs[:]
		
		if( toModif[0] == 1 ):
			oldTrs[0:3] = newTrs[0:3]
			
		if( toModif[1] == 1 ):
			oldTrs[3:6] = newTrs[3:6]		
		
		if( toModif[2] == 1 ):
			oldTrs[6:9] = newTrs[6:9]	


		if( updateValue == 1 )	:
			self.value = oldTrs
			
		return oldTrs


	def utils_overrideTrsValue( self , inValue ):

		if( inValue == None):
			trsValue = self.value
		else:
			trsValue = inValue	

		return trsValue		


		
		

	#################################################################################################################################################################################		
	# CREATE 2################################################################################################################################################################################# CREATE 
	################################################################################################################################################################################# 

	def createFromMayaObjSimple( self , obj , **args ):
		#ARGS
		worldSpace = args.get( 'worldSpace' , True  )
		#GET VALUE
		trsValue = []
		if( worldSpace == True ):
			worldValues = mc.xform( obj , q = True , t   = True , ws = True )
			pivValues   = mc.xform( obj , q = True , piv = True )	
			tValues     = [ ( worldValues[0] + pivValues[0] ) , ( worldValues[1] + pivValues[1] ) , ( worldValues[2] + pivValues[2] )  ]
						
			rValues = mc.xform( obj , q = True , ro = True , ws = True )
			sValues = mc.xform( obj , q = True , s = True  , ws = True )	
			
			trsValue = tValues + rValues + sValues 	
		else:
			for attr in self.utilsTrsAttrs:
				trsValue.append( mc.getAttr( obj + '.' + attr ) )

		return trsValue

	def createFromCurve( self , curveName , **args ):
		#ARGS
		u = args.get( 'u' , 0 )	
		#GET VALUE
		uInterval       = 0.022
		curveApi        = ompy.MFnNurbsCurve( self.getMDagPath( curveName ) )

		allUValueToCheck = [ i*uInterval for i in range( 0 , int(u/uInterval)) ]
		allUValueToCheck.append(u)
		upVectorLast = self.utilsUpVector 
		for uValue in allUValueToCheck:

			#GET TRS VALUE OF POINT ON CURVE			
			point     = curveApi.getPointAtParam( uValue , space= ompy.MSpace.kObject )
			dirVector = curveApi.tangent( uValue , space= ompy.MSpace.kObject )
			
			vX = [ dirVector.x , dirVector.y , dirVector.z ]
			vY = upVectorLast
			vZ = [ 1 , 1 , 1 ]				
			rValue = self.createFromTripleVectors( vX , vY , vZ , updateValue = 0 )[3:6]
			
			trsValueTmp = ( [ point.x , point.y , point.z ] + rValue + [ 1 , 1 , 1 ] )
			
			#GET NEXT UP VECTOR		
			trsValueUpUnder = self.unParent( trsValueTmp , inValue = self.classeTrsValueUp , updateValue = 0 )			
			
			vectorPointUp = ompy.MVector( ( trsValueUpUnder[0] - trsValueTmp[0] ) , ( trsValueUpUnder[1] - trsValueTmp[1] ) , ( trsValueUpUnder[2] - trsValueTmp[2] )  ).normalize()				
			upVectorLast = [ vectorPointUp.x , vectorPointUp.y , vectorPointUp.z ]	
				
		return trsValueTmp


	def createFromTwoVtxBarycentre( self , obbCoords , **args ):	
		tValue        = [ ( obbCoords[0] + obbCoords[3] )/2 , ( obbCoords[1] + obbCoords[4] )/2 , ( obbCoords[2] + obbCoords[5] )/2 ] 
		vX            = [ ( obbCoords[3] - obbCoords[0] )   , ( obbCoords[4] - obbCoords[1] )   , ( obbCoords[5] - obbCoords[2] ) ]
		vY            = [ 0 , 1 , 0 ]	
		vZ            = [ 1 , 0 , 0 ]	
		trsValue      = self.createFromTripleVectors( vX , vY , vZ , updateValue = 0  )			
		trsValue[0:3] = tValue 													
		return trsValue
			
	def createFromOrientedBoundingBox( self , obbCoords , **args ):
		position  = self.getOrientedBoundingBoxPosition(         obbCoords )[0]	
		rotation  = self.getOrientedBoundingBoxOrientation(      obbCoords )	
		scale     = self.getOrientedBoundingBoxOrientationScale( obbCoords )		
		trsValue  = position + rotation + scale
		return trsValue
				
	def createFromFloatMatrix( self , matrixValues , **args  ):	
		#GET VALUE		
		matrix     = ompy.MMatrix(matrixValues)		
		matrixTrsf = ompy.MTransformationMatrix(matrix)
		
		vTranslate   = matrixTrsf.translation( ompy.MSpace.kWorld )
		translateXYZ = [ vTranslate.x , vTranslate.y , vTranslate.z ]				
		rotEuler     = matrixTrsf.rotation()
		rotXYZ       = [  math.degrees(rotEuler.x) ,  math.degrees(rotEuler.y) ,  math.degrees(rotEuler.z) ]		
		scaleXYZ     = matrixTrsf.scale( ompy.MSpace.kWorld )
		
		trsValue = translateXYZ + rotXYZ + scaleXYZ 
		return trsValue	
		
	def createFromTripleVectors( self , tripleVector , **args):	
		#ARGS
		accuracyOrder = args.get( 'accuracyOrder' , [ 0 , 1 , 2 ]   )	
		unlockAxe     = args.get( 'unlockAxe'     , 2               )
		#GET VALUE						
		if( unlockAxe == 2 ):
			accuracyOrder = [ 0 , 1 , 2 ]
		elif(  unlockAxe == 1  ):
			accuracyOrder = [ 0 , 2 , 1 ]
		elif(  unlockAxe == 0  ):
			accuracyOrder = [ 1 , 2 , 0 ]				
    	
		vecteurX = ompy.MVector( tripleVector[0] , tripleVector[1] , tripleVector[2]  )
		vecteurY = ompy.MVector( tripleVector[3] , tripleVector[4] , tripleVector[5]  )
		vecteurZ = ompy.MVector( tripleVector[6] , tripleVector[7] , tripleVector[8]  )	
		vecteurX.normalize()	
		vecteurY.normalize()
		vecteurZ.normalize()
    	
		MVectors = [ vecteurX , vecteurY , vecteurZ ]	
			
		matrixValues  = ( MVectors[accuracyOrder[0]].x , MVectors[accuracyOrder[0]].y , MVectors[accuracyOrder[0]].z , 0  )
		matrixValues += ( MVectors[accuracyOrder[1]].x , MVectors[accuracyOrder[1]].y , MVectors[accuracyOrder[1]].z , 0  )
		matrixValues += ( MVectors[accuracyOrder[2]].x , MVectors[accuracyOrder[2]].y , MVectors[accuracyOrder[2]].z , 0  )
		matrixValues += (  0 , 0 , 0 , 0 )

		trsValue = self.createFromFloatMatrix( matrixValues , updateValue = 0 )
		trsValue[6:9] = [1,1,1]	
		
		#OFFSET
		offset     = [ [0,0,0,0,0,0,1,1,1] , [0,0,0,0,0,0,1,1,1] ] 		
		if( accuracyOrder == [ 0 , 1 , 2 ] ):
			pass
		elif( accuracyOrder == [ 0 , 2 , 1 ] ):			
			offset[0][3:6] = [ -90 , 0 , 0 ]		
		elif( accuracyOrder == [ 1 , 2 , 0 ] ):		
			offset[0][3:6] = [ -90 , 0 ,   0 ]
			offset[1][3:6] = [   0 , 0 , -90 ]

		trsValue   = self.offsetItself(  offset[0] , inValue = trsValue , updateValue = 0 )	
		trsValue   = self.offsetItself(  offset[1] , inValue = trsValue , updateValue = 0 )				
	                                                                                                                                                                                                                                                                                                                                               
		return trsValue

	def createFromDifferenceBetweenGeometry( self , objs , **args):			
		'''
			work with two same geometry. it return a TRS value
			TRSValue = [ 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1 ]      TRS stand for Translate Rotate Scale			
			if you apply the returned TRS value to the objA , the objA must supperpose the objB. ( objA and objB must be freeze )	
		'''	
		objA = objs[0]
		objB = objs[1]
		#GET VALUE						
		pivACoords = mc.xform( objA , q = True , piv = True , ws = True )
		pivACoords = pivACoords + [0,0,0,1,1,1]
			
		objACoords = []
		objACoords.append( mc.xform( objA + '.vtx[0]' , q = True , ws = True , t = True ) )
		objACoords.append( mc.xform( objA + '.vtx[1]' , q = True , ws = True , t = True ) )
		objACoords.append( mc.xform( objA + '.vtx[2]' , q = True , ws = True , t = True ) )
		
		objBCoords = []
		objBCoords.append( mc.xform( objB + '.vtx[0]' , q = True , ws = True , t = True ) )
		objBCoords.append( mc.xform( objB + '.vtx[1]' , q = True , ws = True , t = True ) )
		objBCoords.append( mc.xform( objB + '.vtx[2]' , q = True , ws = True , t = True ) )
		
		#COMPUTE TRANSFORM WITH VTX[0] AS PIVOT	
		translateDiff  = [ objBCoords[0][0] - objACoords[0][0] , objBCoords[0][1] - objACoords[0][1]  , objBCoords[0][2] - objACoords[0][2] ]
		
		vSA            = [ objACoords[1][0] - objACoords[0][0] , objACoords[1][1] - objACoords[0][1]  , objACoords[1][2] - objACoords[0][2] ]
		vSB            = [ objACoords[2][0] - objACoords[0][0] , objACoords[2][1] - objACoords[0][1]  , objACoords[2][2] - objACoords[0][2] ]
		
		vDA            = [ objBCoords[1][0] - objBCoords[0][0] , objBCoords[1][1] - objBCoords[0][1]  , objBCoords[1][2] - objBCoords[0][2] ]
		vDB            = [ objBCoords[2][0] - objBCoords[0][0] , objBCoords[2][1] - objBCoords[0][1]  , objBCoords[2][2] - objBCoords[0][2] ]

		TRSSource      = self.createFromTripleVectors( vSA , vSB , [ 0 , 1 , 0 ]  , updateValue = 0 , toModif = [0,1,0] )
		TRSDestination = self.createFromTripleVectors( vDA , vDB , [ 0 , 1 , 0 ]  , updateValue = 0 , toModif = [0,1,0] )

		TRSSourceInv = self.parent( TRSSource        , inValue = self.classeValueBase ,  updateValue = 0 )		
		TRSrotfinal  = self.unParent( TRSDestination , inValue = TRSSourceInv         , updateValue = 0 )	

		rotDiff = TRSrotfinal[3:6]
		
		scaleXDiff = ompy.MVector( vSA[0] , vSA[1] , vSA[2] ).length() / ompy.MVector( vDA[0] , vDA[1] , vDA[2] ).length()
		
		transformDiff = translateDiff + rotDiff + [ scaleXDiff , scaleXDiff , scaleXDiff ]
	
		#POSITION OF PIVOT OBJ B
		trsVtxAO = objACoords[0] + [0,0,0] + [1,1,1]	
		trsVtxBO = self.offsetParentTrs(  trsVtxAO , transformDiff , inValue = pivACoords , updateValue = 0 )

		#TRANSITION PIVOT A PIVOT B
		translateDiffPiv = [ trsVtxBO[0] - pivACoords[0] , trsVtxBO[1] - pivACoords[1] , trsVtxBO[2] - pivACoords[2] ]  	
		transformDiffPiv =  translateDiffPiv + rotDiff + [ scaleXDiff , scaleXDiff , scaleXDiff ]

		transformDiffPiv = self.updateClassValue( self.value , transformDiffPiv , updateValue , toModif )
			
		return transformDiffPiv		




	#################################################################################################################################################################################		
	# OUT 2 ################################################################################################################################################################################ OUT
	################################################################################################################################################################################# 		

	def visualize( self , name = '' , parent = '' ):
		#NAME
		defaultName = 'visuTrs_LOC'
		if( name == '' ):
			name = defaultNmae

		locTmp = mc.spaceLocator( n = name )[0]
		self.toMayaObjCustom( locTmp )
		if not ( parent == '' ):
			mc.parent( locTmp , parent )

		return locTmp


	def toMayaObjSimple( self , obj , trsValue ,  worldSpace ):						
		if( worldSpace == 0 ):
			for i in range( 0 , len(self.utilsTrsAttrs) ):
				mc.setAttr( obj + self.utilsTrsAttrs[i] , trsValue[i]  )
		else:
			mc.xform( obj , t  = trsValue[0:3] , ws = True )
			mc.xform( obj , ro = trsValue[3:6] , ws = True )			
			mc.xform( obj , s  = trsValue[6:9] , ws = True )




	def toMMatrix( self , trsValue ):			 
		tMatrix = ompy.MTransformationMatrix()
		tMatrix.setTranslation( ompy.MVector( trsValue[0]  , trsValue[1] , trsValue[2] ) , ompy.MSpace.kWorld )
		tMatrix.setRotation( ompy.MEulerRotation( math.radians(trsValue[3]) , math.radians(trsValue[4]) , math.radians(trsValue[5]) )     )
		tMatrix.setScale( [ trsValue[6] ,trsValue[7] ,   trsValue[8]  ]   , ompy.MSpace.kWorld  )
		tMatrix.setShear( [0 , 0 , 0] , ompy.MSpace.kWorld )
		matrix = tMatrix.asMatrix()
		return matrix 		
			
	def toTripleVectors( self , trsValue , axis = [ 'X' , 'Y' , 'Z' ] ):		
		newCoords = self.utilsTripleVectorsDefault
		for i in range( 0 , 3 ):
			newCoords = utilsMath.rotateCoords( newCoords , self.utilsPositionWorldOrigine , axis[i] , trsValue[3+i] )			
		return newCoords
		
	def toCubeCoords( self , trsValue ):
		return utilsMath.transformCoords( self.utilsCubeCoordsDefault , self.utilsPositionWorldOrigine  , trsValue , 'XYZ'  )	
				
	def toDistance( self , trsValueA , trsValue ):				
		return ompy.MVector( trsValueA[0] - trsValue[0] , trsValueA[1] - trsValue[1] , trsValueA[2] - trsValue[2] ).length()			
		
	def toPlaneCoords( self , axeNormal , trsValue ):
		coordsOffset  = [ [0,0,0] , [0,1,0] , [0,0,1]  ]	
		if( axeNormal == 0 ):
			coordsOffset = [ [0,0,0] , [0,1,0] , [0,0,1]  ]
		elif( axeNormal == 1 ):
			coordsOffset = [ [0,0,0] , [1,0,0] , [0,0,1]  ]
		elif( axeNormal == 2 ):
			coordsOffset = [ [0,0,0] , [1,0,0] , [0,1,0]  ]
					
		planeCoords = []		
		for coords in coordsOffset:
			planeCoords.append( self.offsetItself(  coords + [0,0,0,1,1,1] , inValue = trsValue , updateValue = 0 )[0:3] )	
		
		return planeCoords	
		
	def toClosestAxis( self , vector , trsValue ):				
		#BUILD VECTOR DIR
		mVectorDir = ompy.MVector( vector[0] , vector[1] , vector[2] )	
		mVectorDir.normalize()
		#BUILD TRIPLE VECTOR X2		
		tripleVectors    = self.toTripleVectors( inValue = trsValue )
		tripleVectorsInv = [ tripleVectors[0] * -1 , tripleVectors[1] * -1  , tripleVectors[2] * -1  ,  tripleVectors[3] * -1 , tripleVectors[4] * -1  , tripleVectors[5] * -1 ,  tripleVectors[6] * -1 , tripleVectors[7] * -1  , tripleVectors[8] * -1 ]  
		tripleVectorsX2 = tripleVectors + tripleVectorsInv 
		#COMPUTE SCALAR PRODUCT				
		scalaireProduct = []
		for i in range( 0 , 6*3 , 3 ):
			mVTMP = ompy.MVector( tripleVectorsX2[i+0] , tripleVectorsX2[i+1] , tripleVectorsX2[i+2] )
			scalaireProduct.append( mVTMP * mVectorDir ) 			
		#SORT SCALAR PRODUCT				
		sortTMP = scalaireProduct[:] 	
		sortTMP.sort()
		sortTMP.reverse()
		#GET SORTED AXE	
		sortedAxes = []
		for i in range( 0 , 6 ):		
			sortedAxes.append( scalaireProduct.index(sortTMP[i]) )
			
		return sortedAxes				