'''

 
 
 
 

import python
import python.classe.trsBackUp as trs 
reload( python.classe.trsBackUp )

Trs      = trs.trs()
TrsPivot = trs.trs()

toMove = [-2.895 ,0.854  ,3.382  , 0,      0,0 , 1,1,1 ]
pivot  = [ 0     , 1.477 , 3.271 , 0,      0,0 , 1,1,1 ]
value  = [ 0     ,     0 ,-2.972 , 0,-36.235,0 , 1,1,1 ]

Trs.value      = toMove
TrsPivot.value = pivot

for i in range(0,7):
    Trs.offsetTrs( pivot , value )
    TrsPivot.offsetItself( pivot , value )
    pivot = TrsPivot.value
    print(i)
    print( 'obj' , Trs.value)
    print( 'pivot' , pivot)
    
    
 
'''



import math
import maya.cmds         as mc
import maya.api.OpenMaya as ompy
import maya.OpenMaya as om
from ..utils import utilsMath
from .mayaClasse import *
import types

#from .. import utilsMayaApi


class trs(mayaClasse):
	
	'''	
		_______________________________________ATTR	
	value
	_______________________________________CREATE	
	createFromObj
	createFromOrientedBoundingBoxCoords
	createFromCurve
	createFromFloatMatrix
	createFromTripleVectors
	createFromDifferenceBetweenGeometry	
	_______________________________________MODIF	
	parent
	unParent
	mirror
	offsetItself
	offsetParentTrs	?
	intersectPlane
	snapOnPlane	
	snapOnCurve
	snapOnLine	
	setAxisUp
	inverseAxes
	convertRotToClosetEulerSolution	
	projectAngle	?
	aim
	setAim
	getMiddleTrs	
	getTrsRotateAxeOriented	
	blendArray
	_______________________________________SURCHARGE
	len() a) [] + - * /	
	_______________________________________OUT	
	visualize	
	toObj	
	toMMatrix
	toTripleVectors
	toCubeCoords	
	toDistance
	toPlaneCoords
	toClosestAxis	
	_______________________________________UTILS
	get2VectorsNormal
	getNearestCoordsOnPlane
	getMDagPath
	utils_getBarycentre	
	getBBreelCoords	
	getOrientedBoundingBoxPosition	
	getOrientedBoundingBoxOrientation
	getOrientedBoundingBoxOrientationScale	
	updateClassValue	
	'''                       


	def __init__(self , inValue = None ):
		mayaClasse.__init__(self )
		#UTILS	
		#CLASSE
		self.classeType = 'trs'
		self.classeValueBase  = [ 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1 ]		
		#INSTANCE			
		self.value = self.classeValueBase
		if not( inValue == None ):
			if( type(inValue) == types.StringType ) and ( mc.objExists(inValue) ):
				self.createFromObj(inValue)
			else:
				self.value = self.utils_overrideTrsValue( inValue )	

	#################################################################################################################################################################################		
	# CREATE ################################################################################################################################################################################# CREATE 
	################################################################################################################################################################################# 

	def createFromObj( self , obj , updateValue = 1 , **args ):
		#ARGS
		worldSpace = args.get( 'worldSpace' , True          )
		toModif    = args.get( 'toModif'    , [ 1 , 1 , 1 ] )


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
			

		trsValue = self.updateClassValue( self.value , trsValue , updateValue , toModif )
		
		return trsValue
		
		
	#________________________________________________________________________________________________________________________________________________________________________________ createFromOrientedBoundingBoxCoords
	def createFromOrientedBoundingBox( self , obbCoords , updateValue = 1  , toModif = [ 1 , 1 , 1 ] ):
		
		#____________________________________ two vtx		
		if( len( obbCoords ) == 2 ):
			
			tValue =  [ ( obbCoords[0][0] + obbCoords[1][0] )/2 , ( obbCoords[0][1] + obbCoords[1][1] )/2 , ( obbCoords[0][2] + obbCoords[1][2] )/2 ] 
			#rValue = utilsMayaApi.API_convert2CoordsToEulerOrient( [ obbCoords[0] , obbCoords[1] ])	

			vX  = [ ( obbCoords[1][0] - obbCoords[0][0] ) , ( obbCoords[1][1] - obbCoords[0][1] ) , ( obbCoords[1][2] - obbCoords[0][2] ) ]
			vY  = [ 0 , 1 , 0 ]	
			vZ  = [ 1 , 0 , 0 ]
			
			trsValue      = self.createFromTripleVectors( vX , vY , vZ , updateValue = 0  )			
			trsValue[0:3] = tValue 						
	
				
		#____________________________________ many vtx		
		else:
				
			position  = self.getOrientedBoundingBoxPosition(         obbCoords )[0]	
			rotation  = self.getOrientedBoundingBoxOrientation(      obbCoords )	
			scale     = self.getOrientedBoundingBoxOrientationScale( obbCoords )		
			
			trsValue = position + rotation + scale
		
		
		trsValue = self.updateClassValue( self.value , trsValue , updateValue , toModif )			
			
		return trsValue
			
	#________________________________________________________________________________________________________________________________________________________________________________ createFromCurve		
	def createFromCurve( self ,  curveName , u , updateValue = 1 , toModif = [ 1 , 1 , 1 ] ):
		
	
		'''
			API_getCurveULogicTrs
			
			return a TRSvalue cooresponding to curveName's tangeant at u value
    	
			TRSValue = [ 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1 ]      TRS stand for Translate Rotate Scale
			
			To be sure that the tangeant have the right orientation , it works with special algorithms:
			Each time you ask a tangeant at u, it start at 0 and "walk" to u with an step of uInterval. At each step it compute the right orient based on the last one.
			At u(0) it take the world orient as reference , and u( n + uInterval ) take the orientation of u( n ).
						
		'''
		
		uInterval = 0.022
		upVector = [ 0 , 1 , 0 ]
		curveApi  = ompy.MFnNurbsCurve( self.getMDagPath( curveName ) )
		
		trsValueUp = [ 0 , 1 , 0 , 0 , 0 , 0 , 1 , 1 , 1 ]
		trsValueUpUnder = []  	
		
		allUValueToCheck = [ i*uInterval for i in range( 0 , int(u/uInterval)) ]
		allUValueToCheck.append(u)
		
		for uValue in allUValueToCheck:
			
			# get trs value of point on curve
			
			point     = curveApi.getPointAtParam( uValue , space= ompy.MSpace.kObject )
			dirVector = curveApi.tangent( uValue , space= ompy.MSpace.kObject )
			
			tValue = [ point.x , point.y , point.z ]
			sValue = [ 1 , 1 , 1 ]
			
			vX = [ dirVector.x , dirVector.y , dirVector.z ]
			vY = upVector
			vZ = [ 1 , 1 , 1 ]		
			
			rValue = self.createFromTripleVectors( vX , vY , vZ , updateValue = 0 )[3:6]
			#rValue = utilsMayaApi.API_convertTripleVecteurToEulerRot( vX , vY , vZ)   #AUTOREF
			

			trsValueTmp = ( tValue + rValue + sValue )
			
			# get next up vector
			
			trsValueUpUnder = self.unParent( trsValueTmp , inValue = trsValueUp , updateValue = 0 )			
			#trsValueUpUnder = utilsMayaApi.API_getUnparentedTRSvalue( trsValueUp , trsValue )	 #AUTOREF
			
			vectorPointUp = ompy.MVector( ( trsValueUpUnder[0] - trsValueTmp[0] ) , ( trsValueUpUnder[1] - trsValueTmp[1] ) , ( trsValueUpUnder[2] - trsValueTmp[2] )  ).normalize()				
			upVector = [ vectorPointUp.x , vectorPointUp.y , vectorPointUp.z ]	
				
			

		trsValueTmp = self.updateClassValue( self.value , trsValueTmp , updateValue , toModif )				
			
		return trsValueTmp

	#________________________________________________________________________________________________________________________________________________________________________________ createFromFloatMatrix			
		
	def createFromFloatMatrix( self , matrixValues , updateValue = 1 , toModif = [ 1 , 1 , 1 ] ):	
		
		matrix     = ompy.MMatrix(matrixValues)		
		matrixTrsf = ompy.MTransformationMatrix(matrix)
		
		vTranslate   = matrixTrsf.translation( ompy.MSpace.kWorld )
		translateXYZ = [ vTranslate.x , vTranslate.y , vTranslate.z ]				
		rotEuler     = matrixTrsf.rotation()
		rotXYZ       = [  math.degrees(rotEuler.x) ,  math.degrees(rotEuler.y) ,  math.degrees(rotEuler.z) ]		
		scaleXYZ     = matrixTrsf.scale( ompy.MSpace.kWorld )
		

		trsValue = translateXYZ + rotXYZ + scaleXYZ 
		

		trsValue = self.updateClassValue( self.value , trsValue , updateValue , toModif )	
		
		return trsValue	
		
	#________________________________________________________________________________________________________________________________________________________________________________ createFromTripleVectors

	def createFromTripleVectors( self ,  vX , vY , vZ , accuracyOrder = [ 0 , 1 , 2 ] , unlockAxe = 2 , updateValue = 1 , toModif = [ 1 , 1 , 1 ] ):

		'''
			input are array3 array3 array3
			with 3 vector, find the correct XYZ rotation corresponding
			
			ACCURACY ORDER DOESNT WORK , the orient finale is correst BUT IT MESSE UP THE AXES OF THE FINAL RESULT exemple = [0,2,1] take vZ as vY !!!
			
			[ 0 , 1 , 2 ] = [ X , Y , Z ]
			if you are not sure about the accuracy of the 3 vector, accuracyOrder give you a way to classe your vectors by the most accurate to the less 
			At default the X is the leader , the if Y is not accurate it ajuste by the X , and Z is praticely useless...
			
		'''

		if( unlockAxe == 2 ):
			accuracyOrder = [ 0 , 1 , 2 ]
		elif(  unlockAxe == 1  ):
			accuracyOrder = [ 0 , 2 , 1 ]
		elif(  unlockAxe == 0  ):
			accuracyOrder = [ 1 , 2 , 0 ]				
    	
		vecteurX = ompy.MVector( vX[0] , vX[1] , vX[2]  )
		vecteurY = ompy.MVector( vY[0] , vY[1] , vY[2]  )
		vecteurZ = ompy.MVector( vZ[0] , vZ[1] , vZ[2]  )	
		
		vecteurX.normalize()	
		vecteurY.normalize()
		vecteurZ.normalize()
    	
		MVectors = [ vecteurX , vecteurY , vecteurZ ]	
			
		matrixValues  = ( MVectors[accuracyOrder[0]].x , MVectors[accuracyOrder[0]].y , MVectors[accuracyOrder[0]].z , 0  )
		matrixValues += ( MVectors[accuracyOrder[1]].x , MVectors[accuracyOrder[1]].y , MVectors[accuracyOrder[1]].z , 0  )
		matrixValues += ( MVectors[accuracyOrder[2]].x , MVectors[accuracyOrder[2]].y , MVectors[accuracyOrder[2]].z , 0  )
		matrixValues += (  0 , 0 , 0 , 0 )

		trsToOffset = self.createFromFloatMatrix( matrixValues , updateValue = 0 )	
		
		##################################
		trsToOffset[6:9] = [1,1,1] 		                                            #<--------- ON REMET LE SCALE A 1 , pas besoin pour le triples vector , a voir!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
		##################################
		
		
		
		offset     = [ [0,0,0,0,0,0,1,1,1] , [0,0,0,0,0,0,1,1,1] ] 	
		
		if( accuracyOrder == [ 0 , 1 , 2 ] ):
			pass
		elif( accuracyOrder == [ 0 , 2 , 1 ] ):
			
			offset[0][3:6] = [ -90 , 0 , 0 ]		
		
		elif( accuracyOrder == [ 1 , 2 , 0 ] ):
			
			offset[0][3:6] = [ -90 , 0 ,   0 ]
			offset[1][3:6] = [   0 , 0 , -90 ]
		'''
		elif( accuracyOrder == [ 1 , 0 , 2 ] ):
			
			offset[0][3:6] = [ 0 ,   0 , -90  ]
			offset[1][3:6] = [ 0 , 180 ,   0  ]
			
		elif( accuracyOrder == [ 2 , 0 , 1 ] ):
			
			offset[0][3:6] = [ 90 ,  0 , 0  ]
			offset[1][3:6] = [  0 , 90 , 0  ]			
			
		elif( accuracyOrder == [ 2 , 1 , 0 ] ):
			
			offset[0][3:6] = [ 0 , 90 , 0 ]				
			#rotXYZ = utilsMayaApi.API_rotOffsetInsideEulerRot( rotXYZ , [ 0 , 90 , 0] )          #AUTOREF
    	'''
		trsToOffset   = self.offsetItself(  offset[0] , inValue = trsToOffset , updateValue = 0 )	
		trsOffset     = self.offsetItself(  offset[1] , inValue = trsToOffset , updateValue = 0 )				
  	                                                                                                                                                                                                                                                                                                                                               


		trsOffset = self.updateClassValue( self.value , trsOffset , updateValue , toModif )
			
		return trsOffset


	def utils_trsFromPosTripleVectorsApi( self , position , vecX , vecY , vecZ  ):
		trsValue = [0,0,0 , 0,0,0 , 1,1,1]	

		matrix  = [ vecX[0]     , vecX[1]     , vecX[2]     , 0 ]
		matrix += [ vecY[0]     , vecY[1]     , vecY[2]     , 0 ]
		matrix += [ vecZ[0]     , vecZ[1]     , vecZ[2]     , 0 ]
		matrix += [ position[0] , position[1] , position[2] , 0 ]

		outPosition = [ position[0] , position[1] , position[2] ] 

		Matrix  = ompy.MMatrix(matrix)

		TMatrix = ompy.MTransformationMatrix(Matrix)

		eRot    = TMatrix.rotation()
		outRotation = [ math.degrees(eRot.x) , math.degrees(eRot.y) , math.degrees(eRot.z) ]

		outScale    = TMatrix.scale( ompy.MSpace.kObject)	

		trsValue = outPosition + outRotation + outScale


		#DEBUG
		return trsValue



	#________________________________________________________________________________________________________________________________________________________________________________ createFromDifferenceBetweenGeometry
	
	def createFromDifferenceBetweenGeometry( self , objA , objB  , updateValue = 1 , toModif = [ 1 , 1 , 1 ] ):	
		
		'''
			work with two same geometry. it return a TRS value
			TRSValue = [ 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1 ]      TRS stand for Translate Rotate Scale
			
			if you apply the returned TRS value to the objA , the objA must supperpose the objB. ( objA and objB must be freeze )	
		'''	

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
		
		# compute the transformation if vtx[0] were the pivot point
		
		translateDiff  = [ objBCoords[0][0] - objACoords[0][0] , objBCoords[0][1] - objACoords[0][1]  , objBCoords[0][2] - objACoords[0][2] ]
		
		vSA            = [ objACoords[1][0] - objACoords[0][0] , objACoords[1][1] - objACoords[0][1]  , objACoords[1][2] - objACoords[0][2] ]
		vSB            = [ objACoords[2][0] - objACoords[0][0] , objACoords[2][1] - objACoords[0][1]  , objACoords[2][2] - objACoords[0][2] ]
		
		vDA            = [ objBCoords[1][0] - objBCoords[0][0] , objBCoords[1][1] - objBCoords[0][1]  , objBCoords[1][2] - objBCoords[0][2] ]
		vDB            = [ objBCoords[2][0] - objBCoords[0][0] , objBCoords[2][1] - objBCoords[0][1]  , objBCoords[2][2] - objBCoords[0][2] ]
		
		####################

		TRSSource      = self.createFromTripleVectors( vSA , vSB , [ 0 , 1 , 0 ]  , updateValue = 0 , toModif = [0,1,0] )
		TRSDestination = self.createFromTripleVectors( vDA , vDB , [ 0 , 1 , 0 ]  , updateValue = 0 , toModif = [0,1,0] )
		TRSpiv         = [ 0 , 0 , 0 , 0 , 0  , 0 , 1 , 1 , 1 ] 
		
		TRSSourceInv = self.parent( TRSSource , inValue = TRSpiv ,  updateValue = 0 )		
		TRSrotfinal  = self.unParent( TRSDestination , inValue = TRSSourceInv , updateValue = 0 )	

		rotDiff = TRSrotfinal[3:6]
		####################
		
		scaleXDiff = ompy.MVector( vSA[0] , vSA[1] , vSA[2] ).length() / ompy.MVector( vDA[0] , vDA[1] , vDA[2] ).length()
		
		transformDiff = translateDiff + rotDiff + [ scaleXDiff , scaleXDiff , scaleXDiff ]
	
		# compute the position of objB pivot like if it was the same the objA

		trsVtxAO = objACoords[0] + [0,0,0] + [1,1,1]	
		trsVtxBO = self.offsetParentTrs(  trsVtxAO , transformDiff , inValue = pivACoords , updateValue = 0 )


		
		# calcule de la translation entre pivA et pivB
		
		translateDiffPiv = [ trsVtxBO[0] - pivACoords[0] , trsVtxBO[1] - pivACoords[1] , trsVtxBO[2] - pivACoords[2] ]  	
		transformDiffPiv =  translateDiffPiv + rotDiff + [ scaleXDiff , scaleXDiff , scaleXDiff ]


		transformDiffPiv = self.updateClassValue( self.value , transformDiffPiv , updateValue , toModif )
			
		return transformDiffPiv		
		
		
	#################################################################################################################################################################################		
	# MODIF ################################################################################################################################################################################# MODIF
	################################################################################################################################################################################# 		
		

	#________________________________________________________________________________________________________________________________________________________________________________ parent	
	def parent( self , trsValueFather , inValue = None ,  updateValue = 1 , toModif = [ 1 , 1 , 1 ] ):	
		
		'''
			act as if trsValue is a transform node and we parent it to trsValueFather.
			the New trsValue is return
		
			TRSValue = [ 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1 ]      TRS stand for Translate Rotate Scale
		'''
		trsValue = self.utils_overrideTrsValue( inValue )		
			
		matrixP = self.toMMatrix( inValue = trsValueFather )		
		#matrixP = utilsMayaApi.API_convertTRSValueToMMatrix( trsValueFather )          #AUTOREF
		matrixP = matrixP.inverse()
		
		matrixG = self.toMMatrix( inValue = trsValue )		
		#matrixG = utilsMayaApi.API_convertTRSValueToMMatrix( trsValue )          #AUTOREF
		
		mChildren = matrixG * matrixP
		
		mtransChildren = ompy.MTransformationMatrix( mChildren )
	
		translate = mtransChildren.translation( ompy.MSpace.kWorld) 
		rotate    = mtransChildren.rotationComponents()
		scale     = mtransChildren.scale( ompy.MSpace.kWorld)
	 	
		childrenTrsValue = [ translate[0] , translate[1] , translate[2] , math.degrees(rotate[0]) , math.degrees(rotate[1]) , math.degrees(rotate[2]) , scale[0] , scale[1] , scale[2] ]	
	

		childrenTrsValue = self.updateClassValue( trsValue , childrenTrsValue , updateValue , toModif )			
			
		return childrenTrsValue	
	
	#________________________________________________________________________________________________________________________________________________________________________________ unParent	
	def unParent( self , trsValueFather , inValue = None , updateValue = 1 , toModif = [ 1 , 1 , 1 ] ):	
	
		'''
			act as if trsValue is a transform node under parentTRSValue and we place it in the world.
			the New trsValue is return
		
			TRSValue = [ 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1 ]      TRS stand for Translate Rotate Scale
		'''	
		trsValue = self.utils_overrideTrsValue( inValue )			
			
		matrixP = self.toMMatrix( inValue = trsValueFather )			
		#matrixP = utilsMayaApi.API_convertTRSValueToMMatrix( trsValueFather )         #AUTOREF
		matrixG = self.toMMatrix( inValue = trsValue )		
		#matrixG = utilsMayaApi.API_convertTRSValueToMMatrix( trsValue )         #AUTOREF
		
		mChildren = matrixG * matrixP
		
		mtransChildren = ompy.MTransformationMatrix( mChildren )
	
		translate = mtransChildren.translation( ompy.MSpace.kWorld) 
		rotate    = mtransChildren.rotationComponents()
		scale     = mtransChildren.scale( ompy.MSpace.kWorld)
	 	
		childrenTRSValue = [ translate[0] , translate[1] , translate[2] , math.degrees(rotate[0]) , math.degrees(rotate[1]) , math.degrees(rotate[2]) , scale[0] , scale[1] , scale[2] ]	

			
		childrenTRSValue = self.updateClassValue( trsValue , childrenTRSValue , updateValue , toModif )
		
		return childrenTRSValue		



	#________________________________________________________________________________________________________________________________________________________________________________ mirror	
	def mirror( self , planSymCoords , noneMirrorAxe = 4 ,  inValue = None ,  updateValue = 1 , toModif = [ 1 , 1 , 1 ] ):	
		
		trsValue = self.utils_overrideTrsValue( inValue )

		# GET TRIPLE VECTORS COORDS
		tripleOrientVector = self.toTripleVectors( inValue = trsValue )

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
			

		outVectors = tripleOrientVectorSym	


		#****************************************************FOR ROTATION AND SCALE
		'''
		noneMirrorAxe = -1 no reorient
		noneMirrorAxe = 0 axe x is adjusted ---> mirror: rX & tY tZ  
		noneMirrorAxe = 1 axe y is adjusted ---> mirror: rY & tX tZ
		noneMirrorAxe = 2 axe z is adjusted ---> mirror: rZ & tX tY
		noneMirrorAxe = 3 axe perpendicular to mirrorPlane is adjusted    ---> mirror: rPerp & t? t?		
		noneMirrorAxe = 4 axe ? is adjusted and the other two are inverse ---> mirror: rPara1 & rPara2 (FOR ROTATE)
		'''

		mirrorTrsValue = trsValue[:]
		#For a matrix with no scale negatif...
		if( noneMirrorAxe == 0 ):
			#...axe x is adjusted:  mirror: rX & tY tZ 
			outVectors[0][0] *= -1
			outVectors[0][1] *= -1
			outVectors[0][2] *= -1
			#OUT
			rotSym = self.createFromTripleVectors( outVectors[0] , outVectors[1] , outVectors[2]  , updateValue = 0 )	
			mirrorTrsValue =  manipCoordsSym[0:3] + rotSym[3:6] + trsValue[6:9]

		elif( noneMirrorAxe == 1 ):
			#...axe y is adjusted ---> mirror: rY & tX tZ
			outVectors[1][0] *= -1
			outVectors[1][1] *= -1
			outVectors[1][2] *= -1
			#OUT
			rotSym = self.createFromTripleVectors( outVectors[0] , outVectors[1] , outVectors[2]  , updateValue = 0 )	
			mirrorTrsValue =  manipCoordsSym[0:3] + rotSym[3:6] + trsValue[6:9]

		elif( noneMirrorAxe == 2 ):
			#...axe z is adjusted ---> mirror: rZ & tX tY
			outVectors[2][0] *= -1
			outVectors[2][1] *= -1
			outVectors[2][2] *= -1
			#OUT
			rotSym = self.createFromTripleVectors( outVectors[0] , outVectors[1] , outVectors[2]  , updateValue = 0 )	
			mirrorTrsValue =  manipCoordsSym[0:3] + rotSym[3:6] + trsValue[6:9]

		elif( noneMirrorAxe == 3 ):
			#...axe perpendicular to mirrorPlane is adjusted ---> mirror: rPerp & t? t?

			# find the Closest axe to the plane
			vPlaneNormal = om.MVector( manipVtoSym[0] , manipVtoSym[1] , manipVtoSym[1] )
			# find the Closest axe to the plane
			closestAxe = 0
			dotMax = 0
			for i in range( 0 , 3 ):
				vAxe = om.MVector( outVectors[i][0] , outVectors[i][1] , outVectors[i][2] )
				dotTmp = abs( vAxe*vPlaneNormal )
				if( dotMax < dotTmp ):
					dotMax = dotTmp
					closestAxe = i

			# -1 that axe
			outVectors[closestAxe][0] *= -1
			outVectors[closestAxe][1] *= -1
			outVectors[closestAxe][2] *= -1 
			#OUT
			rotSym = self.createFromTripleVectors( outVectors[0] , outVectors[1] , outVectors[2]  , updateValue = 0 )	
			mirrorTrsValue =  manipCoordsSym[0:3] + rotSym[3:6] + trsValue[6:9]
	
		elif( noneMirrorAxe == 4 ):
			#...axe ? is adjusted and the other two are inverse ---> mirror: rPara1 & rPara2 (NICE FOR ROTATION)
			outVectors[0][0] *= -1
			outVectors[0][1] *= -1
			outVectors[0][2] *= -1 	

			outVectors[1][0] *= -1
			outVectors[1][1] *= -1
			outVectors[1][2] *= -1 	

			outVectors[2][0] *= -1
			outVectors[2][1] *= -1
			outVectors[2][2] *= -1 
			#OUT
			rotSym = self.createFromTripleVectors( outVectors[0] , outVectors[1] , outVectors[2]  , updateValue = 0 )	
			mirrorTrsValue =  manipCoordsSym[0:3] + rotSym[3:6] + trsValue[6:9]				
		else:
			#...no scale adjustement no reorient
			mirrorTrsValue = self.utils_trsFromPosTripleVectorsApi( manipCoordsSym[0:3] , outVectors[0] , outVectors[1] , outVectors[2]  )	





		mirrorTrsValue = self.updateClassValue( trsValue , mirrorTrsValue , updateValue , toModif )			
		return mirrorTrsValue		
		

		
	#________________________________________________________________________________________________________________________________________________________________________________ offsetItself			
	#DOESNT WORK WITH TRANSLATE
	def offsetItself( self , offsetTrs , inValue = None , updateValue = 1 , toModif = [ 1 , 1 , 1 ] ):

		'''
			offset euler rot inside an other euler rot. 
			As if we put the offset under parentRot. The result is the accumulation of the both
			
			can be replace by API_getUnparentedTRSvalue() same thing
		
		'''   

		trsValue = self.utils_overrideTrsValue( inValue )				
					
		offsetTrsWorld  = self.unParent( offsetTrs , inValue = trsValue , updateValue = 0 )				
		#offsetTrsWorld = utilsMayaApi.API_getUnparentedTRSvalue( offsetTrs , parentTrs )    #AUTOREF 

		offsetTrsWorld = self.updateClassValue( trsValue , offsetTrsWorld , updateValue , toModif )			
						
		return offsetTrsWorld


	#________________________________________________________________________________________________________________________________________________________________________________ offsetParentTrs
	def offsetParentTrs(  self , parentTrs , offsetTrsUnder  , inValue = None , updateValue = 1 , toModif = [ 1 , 1 , 1 ] ):
	
		'''
			give new coords when his father move to trsValue
		
			TRSValue = [ 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1 ]      TRS stand for Translate Rotate Scale
	 
		'''
		trsValue = self.utils_overrideTrsValue( inValue )	

		newTrs = trsValue		
		#__________________________ TRANSFORM

		newParentTrs = []
		for i in range( 0 , 9 ):
			newParentTrs.append( parentTrs[i] + offsetTrsUnder[i] )
	
		mEulerRot = ompy.MEulerRotation( math.radians(offsetTrsUnder[3]) , math.radians(offsetTrsUnder[4]) , math.radians(offsetTrsUnder[5]) ) 
		
		vChidrenParent   = [  trsValue[0] - parentTrs[0]  ,  trsValue[1] - parentTrs[1]  ,  trsValue[2] - parentTrs[2]  ]
		vChidrenParentS  = ompy.MVector(  vChidrenParent[0] * offsetTrsUnder[6]  ,  vChidrenParent[1] * offsetTrsUnder[7]  ,  vChidrenParent[2] * offsetTrsUnder[8]  )	
		vChidrenParentRS = vChidrenParentS.rotateBy(  mEulerRot  )
			
		newTrs[0:3] = [  ( newParentTrs[0] + vChidrenParentRS.x )  ,  ( newParentTrs[1] + vChidrenParentRS.y )  ,  ( newParentTrs[2] + vChidrenParentRS.z )  ]	
	
		#__________________________ ROTATE
		
		tripleVectors = self.toTripleVectors( inValue = trsValue )
		
		for i in range( 0 , len(tripleVectors) , 3 ):
			mvAxe  = ompy.MVector(  tripleVectors[i+0] ,  tripleVectors[i+1]  ,  tripleVectors[i+2]  )
			mvAxe  = mvAxe.rotateBy(  mEulerRot  )
			tripleVectors[i:i+3] = [ mvAxe.x , mvAxe.y , mvAxe.z ]
		
		newRot = self.createFromTripleVectors( tripleVectors[0:3] , tripleVectors[3:6] , tripleVectors[6:9] , updateValue = 0 )	

		newTrs[3:6] = newRot[3:6]
	
		#__________________________ SCALE
		#...

		newTrs = self.updateClassValue( trsValue , newTrs , updateValue , toModif )				
			
		return newTrs
			
	#________________________________________________________________________________________________________________________________________________________________________________ offsetParentTrs
	def offsetTrs(  self , trsPivot , offsetTrs , inValue = None , updateValue = 1 , toModif = [ 1 , 1 , 1 ] ):
	
		'''
			give new coords when his father move to trsValue
		
			TRSValue = [ 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1 ]      TRS stand for Translate Rotate Scale
	 
		'''
		trsValue = self.utils_overrideTrsValue( inValue )	

		newTrs = trsValue		
		#__________________________ TRANSFORM
		trsPivotOffseted = self.offsetItself( trsPivot , inValue = offsetTrs , updateValue = 0 )

		newTrs[0] += trsPivotOffseted[0] - trsPivot[0]
		newTrs[1] += trsPivotOffseted[1] - trsPivot[1]
		newTrs[2] += trsPivotOffseted[2] - trsPivot[2]

	
		mEulerRot = ompy.MEulerRotation( math.radians(offsetTrs[3]) , math.radians(offsetTrs[4]) , math.radians(offsetTrs[5]) ) 

		vChidrenParent   = [ newTrs[0] - trsPivotOffseted[0]  ,  newTrs[1] - trsPivotOffseted[1]  ,  newTrs[2] - trsPivotOffseted[2]  ]
		vChidrenParentS  = ompy.MVector(  vChidrenParent[0] * offsetTrs[6]  ,  vChidrenParent[1] * offsetTrs[7]  ,  vChidrenParent[2] * offsetTrs[8]  )	
		vChidrenParentRS = vChidrenParentS.rotateBy(  mEulerRot  )

		newTrs[0:3] = [  ( trsPivotOffseted[0] + vChidrenParentRS.x )  ,  ( trsPivotOffseted[1] + vChidrenParentRS.y )  ,  ( trsPivotOffseted[2] + vChidrenParentRS.z )  ]	

		#__________________________ ROTATE

		tripleVectors = self.toTripleVectors( inValue = trsValue )
		
		for i in range( 0 , len(tripleVectors) , 3 ):
			mvAxe  = ompy.MVector(  tripleVectors[i+0] ,  tripleVectors[i+1]  ,  tripleVectors[i+2]  )
			mvAxe  = mvAxe.rotateBy(  mEulerRot  )
			tripleVectors[i:i+3] = [ mvAxe.x , mvAxe.y , mvAxe.z ]
		
		newRot = self.createFromTripleVectors( tripleVectors[0:3] , tripleVectors[3:6] , tripleVectors[6:9] , updateValue = 0 )	

		newTrs[3:6] = newRot[3:6]
	
		#__________________________ SCALE
		#...

		newTrs = self.updateClassValue( trsValue , newTrs , updateValue , toModif )				
			
		return newTrs
			
	#________________________________________________________________________________________________________________________________________________________________________________ intersectPlane		
	def intersectPlane( self , planeCoords , vectorDir , inValue = None , updateValue = 1 , toModif = [ 1 , 1 , 1 ]  ):		
		
		trsValue = self.utils_overrideTrsValue( inValue )

		nearestPlaneCoords = self.snapOnPlane( planeCoords , inValue = trsValue , updateValue = 0  )
		
		vDirection = ompy.MVector( vectorDir[0] , vectorDir[1] , vectorDir[2] )
		vDirection.normalize()
		normal     = ompy.MVector( ( nearestPlaneCoords[0] - trsValue[0] ) , ( nearestPlaneCoords[1] - trsValue[1] ) , ( nearestPlaneCoords[2] - trsValue[2] ) )
    	
		angleVector = math.degrees( vDirection.angle(normal) )	
		dist        = abs( normal.length()  / math.cos(angleVector) )
    	
		newCoords = [  vDirection.x * dist + trsValue[0]  , vDirection.y * dist + trsValue[1]  , vDirection.z * dist + trsValue[2]  ]  

		newTrs = newCoords + trsValue[3:9] 
		
		newTrs = self.updateClassValue( trsValue , newTrs , updateValue , toModif )				
			
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

	
	def aim( self , point , aimAxe = 0 , inValue = None , updateValue = 1  , toModif = [ 1 , 1 , 1 ] ):
		# if aimAxe = 2 there is no aim going on... to fixe

		trsValue = self.utils_overrideTrsValue( inValue )
		aimVector = [ point[0] - trsValue[0] , point[1] - trsValue[1] , point[2] - trsValue[2] ]
		newTrs = self.setAim( aimVector , aimAxe , trsValue , updateValue  , toModif )
		newTrs = self.updateClassValue( trsValue , newTrs , updateValue , toModif )	
		return newTrs				
		

	
	def setAim( self , aimVector , aimAxe = 0 , inValue = None , updateValue = 1  , toModif = [ 1 , 1 , 1 ] ):

		trsValue = self.utils_overrideTrsValue( inValue )
		vectorUp = [ 0 , 1 , 0  ]		
		#GET AIM AXE
		if( aimAxe == None ):			
			aimAxe = self.toClosestAxis( aimVector , inValue = trsValue  )		
			if( 2 < aimAxe ): aimAxe -= 3
		#GET UP AXE				
		axes = self.toClosestAxis( vectorUp , returnList = True , inValue = trsValue  )
		axeUp = axes[0]			
		if( axeUp == aimAxe )or( axeUp == (aimAxe+3) ):
			axeUp = axes[1]

		if( axeUp > 2 ): axeUp -= 3
		#GET SIDE AXE			
		axis = [ 0 , 1 , 2 ]
		axis.remove( aimAxe )
		axis.remove( axeUp  )
		axeSide = axis[0]
		#BUILD NEW TRS			
		tripleVector = self.toTripleVectors( inValue = trsValue )
		tripleVector[aimAxe*3:aimAxe*3+3] = aimVector
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
		
	#________________________________________________________________________________________________________________________________________________________________________________ getTrsRotateAxeOriented	
	
	def blendArray( self , trsArray  , includeCurrent = 1 , inValue = None , updateValue = 1  , toModif = [ 1 , 1 , 1 ] ):
					
		if( includeCurrent ):
			trsArray.append(self.value)

		outTrs = [0,0,0,0,0,0,1,1,1]
		for i in range( 0,len(trsArray) ):
			for j in range( 0,len(trsArray[i]) ):
				outTrs[j] += trsArray[i][j]

		for j in range( 0,6 ):
			outTrs[j] /= len(trsArray)

		for j in range( 0,3 ):
			outTrs[6+j] -= 1
			outTrs[6+j] /= len(trsArray)
			outTrs[6+j] += 1

		self.value = outTrs
		return outTrs

	def overshoot( self , trsTarget , mult ):

		vTarget = ompy.MVector( trsTarget[0]-self.value[0] , trsTarget[1]-self.value[1] , trsTarget[2]-self.value[2] )
		vTarget *= mult	

		self.value[0] += vTarget.x
		self.value[1] += vTarget.y
		self.value[2] += vTarget.z



	#################################################################################################################################################################################		
	# SURCHARGE ################################################################################################################################################################################ SURCHARGE 
	#################################################################################################################################################################################
	'''
	#________________________________________________________________________________________________________________________________________________________________________________  print	
	def __repr__( self ):
		
		return repr(self.value)
	'''	
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
	################################################################################################################################################################################# OUT
	################################################################################################################################################################################# 		
	

	def visualize( self , name = '' , parent = '' ):

		#NAME
		defaultName = 'visuTrs_LOC'
		if( name == '' ):
			name = defaultNmae

		locTmp = mc.spaceLocator( n = name )[0]
		self.toObj( locTmp )
		if not ( parent == '' ):
			mc.parent( locTmp , parent )

		return locTmp

	
	#________________________________________________________________________________________________________________________________________________________________________________ toObj
	def toObj( self , obj , worldSpace = 0 , inValue = None ):
	
		'''
			TRSValue = [ 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1 ]      TRS stand for Translate Rotate Scale	
		'''
		trsValue = self.utils_overrideTrsValue( inValue )

		if( worldSpace == 0 ):
			for i in range( 0 , len(self.utilsTrsAttrs) ):
				mc.setAttr( ( obj + '.' + self.utilsTrsAttrs[i] ) , trsValue[i]  )
		else:
			mc.xform( obj , t  = trsValue[0:3] , ws = True )
			mc.xform( obj , ro = trsValue[3:6] , ws = True )			
			mc.xform( obj , s  = trsValue[6:9] , ws = True )				 

	#________________________________________________________________________________________________________________________________________________________________________________ toObj
	def toObjCmds( self , obj , worldSpace = 0 , inValue = None ):
		buildCmds = ''
	
		'''
			TRSValue = [ 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1 ]      TRS stand for Translate Rotate Scale	
		'''
		trsValue = self.utils_overrideTrsValue( inValue )

		if( worldSpace == 0 ):
			for i in range( 0 , len(self.utilsTrsAttrs) ):
				buildCmds += 'mc.setAttr( "{}.{}" , {} )\n'.format( obj , self.utilsTrsAttrs[i] , trsValue[i] )
		else:
			buildCmds += 'mc.xform( "{}" , t  = {} , ws = True )\n'.format( obj , trsValue[0:3] )
			buildCmds += 'mc.xform( "{}" , ro = {} , ws = True )\n'.format( obj , trsValue[3:6] )
			buildCmds += 'mc.xform( "{}" , s  = {} , ws = True )\n'.format( obj , trsValue[6:9] )
				 
		return buildCmds

	#________________________________________________________________________________________________________________________________________________________________________________ toMMatrix			 
	def toMMatrix( self  , inValue = None ):			 
			 
		'''
			create a MTransformationMatrix with TRSValue. like if we create a transform with TRSValue in his attribute
			
			TRSValue = [ 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1 ]      TRS stand for Translate Rotate Scale		
		'''
		trsValue = self.utils_overrideTrsValue( inValue )

		TRSValue = trsValue
		tMatrix = ompy.MTransformationMatrix()
		tMatrix.setTranslation( ompy.MVector( TRSValue[0]  , TRSValue[1] , TRSValue[2] ) , ompy.MSpace.kWorld )
		tMatrix.setRotation( ompy.MEulerRotation( math.radians(TRSValue[3]) , math.radians(TRSValue[4]) , math.radians(TRSValue[5]) ) )
		tMatrix.setScale( [ TRSValue[6] ,TRSValue[7] ,   TRSValue[8]  ]   , ompy.MSpace.kWorld  )
		tMatrix.setShear(   [ 0     ,   0     ,   0  ]   , ompy.MSpace.kWorld   )
		
		
		matrix = tMatrix.asMatrix()
		
		return matrix 		
		
		
	#________________________________________________________________________________________________________________________________________________________________________________ toTripleVectors				

	def toTripleVectors( self , axis = [ 'X' , 'Y' , 'Z' ] , inValue = None ):
		
		trsValue = self.utils_overrideTrsValue( inValue )	
	
		MMatrix = self.toMMatrix( inValue = trsValue )
		tripleVectors = [ MMatrix[i+j] for i in [0,4,8] for j in range(0,3) ]
		return tripleVectors 

		'''
		rotValue = trsValue[3:6]
		
		initCoords = [ 1 , 0 , 0 , 0 , 1 , 0 , 0 , 0 , 1 ]
		piv = [ 0 , 0 , 0 ]
				
		newCoords = initCoords
		for i in range( 0 , len(rotValue) ):
			newCoords = utilsMath.rotateCoords( newCoords , piv , axis[i] , rotValue[i] )	
		return newCoords		
		'''


		
	#________________________________________________________________________________________________________________________________________________________________________________ toCubeCoords			
	def toCubeCoords( self  , sortByFace = 0 , inValue = None ):

		trsValue = self.utils_overrideTrsValue( inValue )

		reelBBCoords = [ [-0.5,-0.5,-0.5] , [0.5,-0.5,-0.5] , [0.5,-0.5,0.5] , [-0.5,-0.5,0.5] , [-0.5,0.5,-0.5] , [0.5,0.5,-0.5] , [0.5,0.5,0.5] , [-0.5,0.5,0.5]  ]  
		
		reelBBCoords = utilsMath.transformCoords( reelBBCoords , [ 0 , 0 , 0 ]  , trsValue , 'XYZ'  )
		
		facesCoords = []
		if( sortByFace == 1 ):
			facesCoords.append( [ reelBBCoords[0] , reelBBCoords[1] , reelBBCoords[2] , reelBBCoords[3] ] ) 
			facesCoords.append( [ reelBBCoords[0] , reelBBCoords[1] , reelBBCoords[5] , reelBBCoords[4] ] ) 
			facesCoords.append( [ reelBBCoords[1] , reelBBCoords[2] , reelBBCoords[6] , reelBBCoords[5] ] ) 
			facesCoords.append( [ reelBBCoords[2] , reelBBCoords[3] , reelBBCoords[7] , reelBBCoords[6] ] )
			facesCoords.append( [ reelBBCoords[3] , reelBBCoords[0] , reelBBCoords[4] , reelBBCoords[7] ] ) 
			facesCoords.append( [ reelBBCoords[4] , reelBBCoords[5] , reelBBCoords[6] , reelBBCoords[7] ] )

			reelBBCoords = facesCoords   			
			
		return reelBBCoords
				
	#________________________________________________________________________________________________________________________________________________________________________________ toDistance
	def toDistance( self , trsValueA , inValue = None):
		
		trsValue = self.utils_overrideTrsValue( inValue )
			
		distance = ompy.MVector( trsValueA[0] - trsValue[0] , trsValueA[1] - trsValue[1] , trsValueA[2] - trsValue[2] ).length()	
		
		return distance
		
	#________________________________________________________________________________________________________________________________________________________________________________ toPlaneCoords
	def toPlaneCoords( self , axeNormal , inValue = None):
		
		trsValue = self.utils_overrideTrsValue( inValue )
			
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
		
	#________________________________________________________________________________________________________________________________________________________________________________ toPlaneCoords
	def toClosestAxis( self , vector , returnList = 0 , inValue = None):	
		
		trsValue = self.utils_overrideTrsValue( inValue )	
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
			
		if( returnList == 1 ):	
			return sortedAxes
		else:
			return sortedAxes[0]			


			
			
			
			
	#################################################################################################################################################################################		
	################################################################################################################################################################################# UTILS
	################################################################################################################################################################################# 			



		
	#________________________________________________________________________________________________________________________________________________________________________________ get2VectorsNormal    
		    
	def get2VectorsNormal( self , vectorA , vectorB , vMoyen ):
		
		'''
			determine the normal of a plan represented by vectorA and vectorB
			vectorMoyen is to determine witch side of the plan the normal is
		'''
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


		
		
	#ADD
	def unParentBis( self , trsValue , trsValueFather ):
		matrix  = self.toMMatrix( inValue = trsValue )				
		matrixP = self.toMMatrix( inValue = trsValueFather )			
		mChild  = matrix * matrixP
		mtChild = ompy.MTransformationMatrix( mChildren )
		trs     = mtChild.translation( ompy.MSpace.kWorld) + mtChild.rotationComponents() + mtChild.scale( ompy.MSpace.kWorld)
		trs[3:6]= [ math.degrees(trs[3]) , math.degrees(trs[4]) , math.degrees(trs[5]) ]	
		return trs	

	def offsetItselfBis( self , trsValue , offsetTrs ):		
		return self.unParent( trsValue , offsetTrs )			
	
	
	def utils_MMatrixToNum( self, MMatrix ):
		return [  MMatrix(0,0) , MMatrix(0,1) , MMatrix(0,2) , MMatrix(0,3)  ,  MMatrix(1,0) , MMatrix(1,1) , MMatrix(1,2) , MMatrix(1,3)  ,  MMatrix(2,0) , MMatrix(2,1) , MMatrix(2,2) , MMatrix(2,3) ,  MMatrix(3,0) , MMatrix(3,1) , MMatrix(3,2) , MMatrix(3,3)  ]     
	
	
	def utils_numToMMatrix( self, num ):
		inMatrix = om.MMatrix()
		utils = om.MScriptUtil()
		utils.createMatrixFromList( num, inMatrix )
		return inMatrix

