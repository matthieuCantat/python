


'''
________________________________________________ COORDS
API_convertCoordsByParentTransformation
API_getAllVertexCoords
    getNearestCoordsOnPlane
    getAlignCoords
    snapCoordOnPlane
    mirrorCoords
    getPointIntersectPlane
________________________________________________ ROTATION
API_findClosetEulerSolution                   # in trsClass
API_rotOffsetInsideEulerRot                   # in trsClass
________________________________________________ VECTOR
API_getVectorsRotDifference
API_getVectorsDistanceRapport
API_convertTripleVecteurToEulerRot            # in trsClass
API_convertEulerRotToTripleVecteur            # in trsClass
API_convert2CoordsToTripleVecteurOrient       # in trsClass
    get2VectorsNormal
    getSignScalaireProduct
________________________________________________ TRS
API_convertTRSValueToMMatrix                  # in trsClass
API_getParentedTRSvalue                       # in trsClass
API_getUnparentedTRSvalue                     # in trsClass
API_getTransformDifferenceBetweenSameGeometry # in trsClass
    mirrorTrsValue                            # in trsClass
    inverseTrsValueAxes                       # in trsClass
________________________________________________ BBreel
getTRSreelBB                     # in trsClass
getBBreelCoords
getBBreelPositions
getBBreelOrientation
getBBreelScale
convertTRSToReelBB               # in trsClass

________________________________________________ UTILS
API_getMDagPath
________________________________________________ CURVE
API_getClosestPointOnCurve      # in trsClass
API_getCurveULogicTrs           # in trsClass
API_getCurveUTrs
    getStraigtCurveCoords

________________________________________________ MAYA
API_growVerticesByEdge 
API_convertEdgeToVertices
API_convertVertexToEdges
________________________________________________ AUTRE
setAxisUp                       # in trsClass
getObjNameAndIndex
getTwoVerticesLength

API_getSortedDistancesIndexCoords
getfarestCoordsIndex
getClosestAxeFromVector  

'''






import math
import maya.cmds as mc
import maya.api.OpenMaya as ompy
import maya.OpenMaya as om 
import maya.OpenMayaAnim as oma


from . import utilsMath

print(' === import utilsMayaApi ===')

#==========================================================================================================================
#======================================================    COORDS    ======================================================
#==========================================================================================================================

#_____________________________________________________________________________________________________________________________________________________________________ convert coords by parent transformation

def API_convertCoordsByParentTransformation( baseCoords , trsValues , parentCoords ):

	'''
		give new coords when his father move to trsValue
	
		TRSValue = [ 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1 ]      TRS stand for Translate Rotate Scale
 
	'''
	newParentCoords  = [ parentCoords[0] + trsValues[0] , parentCoords[1] + trsValues[1] , parentCoords[2] + trsValues[2] ] 
	
	mEulerRot           = ompy.MEulerRotation( math.radians(trsValues[3]) , math.radians(trsValues[4]) , math.radians(trsValues[5]) ) 
	
	vChidrenParent   = [  baseCoords[0] - parentCoords[0]  ,  baseCoords[1] - parentCoords[1]  ,  baseCoords[2] - parentCoords[2]  ]
	vChidrenParentS  = ompy.MVector(  vChidrenParent[0] * trsValues[6]  ,  vChidrenParent[1] * trsValues[7]  ,  vChidrenParent[2] * trsValues[8]  )	
	vChidrenParentRS = vChidrenParentS.rotateBy(  mEulerRot  )
		
	newCoords = [  ( newParentCoords[0] + vChidrenParentRS.x )  ,  ( newParentCoords[1] + vChidrenParentRS.y )  ,  ( newParentCoords[2] + vChidrenParentRS.z )  ]	

	return newCoords

#_____________________________________________________________________________________________________________________________________________________________________ API_getAllVertexCoords

def API_getAllVertexCoords( nameMesh ):
 
	dagPath    = API_getMDagPath( nameMesh )	
	meshClass  = ompy.MFnMesh(dagPath)	
	pointArray = meshClass.getPoints( ompy.MSpace.kWorld )

	pointList = []	
	for i in range( 0 , len(pointArray) ):
		pointList.append( [pointArray[i][0], pointArray[i][1], pointArray[i][2]] )
		
	return pointList


	
#_____________________________________________________________________________________________________________________________________________________________________ getNearestCoordsOnPlane
				
def getNearestCoordsOnPlane( planeCoords , oldCoords , vDirection ):
	
	
	'''
		input vDirection is a MVector
		
		with oldcoords , a direction and the planeCoords find the point snap in the plan 
	
	
	'''
	
	
	vDirection.normalize()
	
	# on determine d de la formule du plan  2x + 3y + 7z +d = 0
	
	d = ( ( vDirection.x *  planeCoords[0][0] ) + ( vDirection.y *  planeCoords[0][1] ) + ( vDirection.z *  planeCoords[0][2] ) ) * -1 
	
	# on determine la distance entre le point de la ligne et le point de l'intersection
	
	dist = (   - ( vDirection.x * oldCoords[0] ) - ( vDirection.y * oldCoords[1] ) - ( vDirection.z * oldCoords[2] ) - d  ) / ( ( vDirection.x * vDirection.x ) + ( vDirection.y * vDirection.y ) + ( vDirection.z * vDirection.z )   ) 	
	
	# on determine les coordoonee de l'intersection
	
	iCoords = [  vDirection.x * dist + oldCoords[0] , vDirection.y * dist + oldCoords[1] , vDirection.z * dist + oldCoords[2] ] 
	
	return iCoords
    				
				
#_____________________________________________________________________________________________________________________________________________________________________ getAlignCoords				
				
def getAlignCoords( lineCoords , oldCoords ):
	
	'''
		with a line determine by lineCoords , convert oldCoords to new Coords snap on this line
	
	'''
	
	vectorRef       = ompy.MVector( ( lineCoords[1][0] - lineCoords[0][0] ) , ( lineCoords[1][1] - lineCoords[0][1] ) , ( lineCoords[1][2] - lineCoords[0][2] ) )
	vectorOldCoords = ompy.MVector( ( oldCoords[0]     - lineCoords[0][0] ) , ( oldCoords[1]     - lineCoords[0][1] ) , ( oldCoords[2]     - lineCoords[0][2] ) )
	angleA          = vectorRef.angle( vectorOldCoords )
		
	dist = math.cos( angleA ) * vectorOldCoords.length()
	
	vectorRef.normalize()
		
	newCoords = [  vectorRef.x * dist + lineCoords[0][0] , vectorRef.y * dist + lineCoords[0][1] , vectorRef.z * dist + lineCoords[0][2] ] 
	
	return newCoords
							
				
#_____________________________________________________________________________________________________________________________________________________________________ snapCoordOnPlane   # in trsClass	

def snapCoordsOnPlane( planeCoords , oldCoords ):   # in trsClass
	
	'''
		with a 3 coords plane and an old coords get the snapped version of oldCoords in plane
	
	'''
				
	vPlaneA      = ompy.MVector( ( planeCoords[1][0] - planeCoords[0][0] ) , ( planeCoords[1][1] - planeCoords[0][1] ) , ( planeCoords[1][2] - planeCoords[0][2] ) ) 
	vPlaneB      = ompy.MVector( ( planeCoords[2][0] - planeCoords[0][0] ) , ( planeCoords[2][1] - planeCoords[0][1] ) , ( planeCoords[2][2] - planeCoords[0][2] ) ) 		
	rawDir       = ompy.MVector( ( planeCoords[0][0] - oldCoords[0]      ) , ( planeCoords[0][1] - oldCoords[1]      ) , ( planeCoords[0][2] - oldCoords[2]      ) )	
	vPlaneNormal = get2VectorsNormal( vPlaneA , vPlaneB , rawDir )
	
	newCoords = getNearestCoordsOnPlane( planeCoords , oldCoords , vPlaneNormal ) 				
								
	return newCoords

		
#_____________________________________________________________________________________________________________________________________________________________________ mirrorCoord

def mirrorCoords( coords , planSymCoords  ):	
		
	coordsSym = []
	
	for coord in coords: 
		manipCoordsMiddle = snapCoordsOnPlane( planSymCoords , coord )   # in trsClass
		manipVtoSym       = [ ( manipCoordsMiddle[0] - coord[0] )*2 , ( manipCoordsMiddle[1] - coord[1] )*2 , ( manipCoordsMiddle[2] - coord[2] )*2 ]
		manipCoordsSym    = [ coord[0] + manipVtoSym[0]             , coord[1] + manipVtoSym[1]             , coord[2] + manipVtoSym[2]             ]		
		coordsSym.append(manipCoordsSym)
	
	return coordsSym		
		

#_____________________________________________________________________________________________________________________________________________________________________ getNearestCoordsOnPlane
def snapCoordsOnPlane( planeCoords , oldCoords ):   # in trsClass
	
	'''
		with a 3 coords plane and an old coords get the snapped version of oldCoords in plane
	
	'''
				
	vPlaneA      = ompy.MVector( ( planeCoords[1][0] - planeCoords[0][0] ) , ( planeCoords[1][1] - planeCoords[0][1] ) , ( planeCoords[1][2] - planeCoords[0][2] ) ) 
	vPlaneB      = ompy.MVector( ( planeCoords[2][0] - planeCoords[0][0] ) , ( planeCoords[2][1] - planeCoords[0][1] ) , ( planeCoords[2][2] - planeCoords[0][2] ) ) 		
	rawDir       = ompy.MVector( ( planeCoords[0][0] - oldCoords[0]      ) , ( planeCoords[0][1] - oldCoords[1]      ) , ( planeCoords[0][2] - oldCoords[2]      ) )	
	vPlaneNormal = get2VectorsNormal( vPlaneA , vPlaneB , rawDir )
	
	newCoords = getNearestCoordsOnPlane( planeCoords , oldCoords , vPlaneNormal ) 				
								
	return newCoords

	
#_____________________________________________________________________________________________________________________________________________________________________ getPointIntersectPlane	
def getPointIntersectPlane( planeCoords , oldPoint , vDir ):
	
	'''
		with a 3 coords plane and an old coords get the snapped version of oldCoords in plane
	
	'''
				
	nearestPlaneCoords = snapCoordsOnPlane( planeCoords , oldPoint )   # in trsClass
	
	vDirection = ompy.MVector( vDir[0] , vDir[1] , vDir[2] )
	vDirection.normalize()
	normal     = ompy.MVector( ( nearestPlaneCoords[0] - oldPoint[0] ) , ( nearestPlaneCoords[1] - oldPoint[1] ) , ( nearestPlaneCoords[2] - oldPoint[2] ) )

	angleVector = math.degrees( vDirection.angle(normal) )	
	dist        = abs( normal.length()  / math.cos(angleVector) )

	newCoords = [  vDirection.x * dist + oldPoint[0]  , vDirection.y * dist + oldPoint[1]  , vDirection.z * dist + oldPoint[2]  ]  
								
	return newCoords    
	
#==========================================================================================================================
#=====================================================    ROTATION    =====================================================
#==========================================================================================================================

#_____________________________________________________________________________________________________________________________________________________________________ find closet euler solution          # in trsClass	

def API_findClosetEulerSolution( rotValue , rotValueTarget ):              # in trsClass
	
	'''
		with the rotValue, it will find the closest XYZ rot to the target, but the orient stay the same of course 	
	'''
	
	eRotBase   = ompy.MEulerRotation( math.radians(rotValue[0]) , math.radians(rotValue[1]) , math.radians(rotValue[2]) )
	
	eRotTarget = ompy.MEulerRotation( math.radians(rotValueTarget[0]) , math.radians(rotValueTarget[1]) , math.radians(rotValueTarget[2]) )
	eRot = eRotBase.closestSolution(eRotTarget)
	
	return [  math.degrees(eRot.x) , math.degrees(eRot.y) , math.degrees(eRot.z) ]
	

	

#_____________________________________________________________________________________________________________________________________________________________________ rot offset inside euler rot   # in trsClass

def API_rotOffsetInsideEulerRot( parentRot , offset ):  # in trsClass
	
	'''
		offset euler rot inside an other euler rot. 
		As if we put the offset under parentRot. The result is the accumulation of the both
		
		can be replace by API_getUnparentedTRSvalue() same thing
	
	'''    
	parentTrs = [ 0 , 0 , 0 , parentRot[0] , parentRot[1] , parentRot[2] , 1 , 1 , 1 ]
	offsetTrs = [ 0 , 0 , 0 , offset[0]    , offset[1]    , offset[2]    , 1 , 1 , 1 ] 
	
	trs = API_getUnparentedTRSvalue( offsetTrs , parentTrs )  # in trsClass
	
	return trs[3:6]



#==========================================================================================================================
#======================================================    VECTOR    ======================================================
#==========================================================================================================================

#_____________________________________________________________________________________________________________________________________________________________________ get vectors rot difference	
  
def API_getVectorsRotDifference( vA , vB ):
	
	'''
		vA and vB are float array	
		get the ange between the two vectors in xyz euler rot degrees	
	'''
	
	
	mVectorA = ompy.MVector( vA[0] , vA[1] , vA[2] ) 
	mVectorB = ompy.MVector( vB[0] , vB[1] , vB[2] )
	
	qAngle = ompy.MQuaternion( mVectorA , mVectorB)
	eAngle = qAngle.asEulerRotation() 
	
	rot = [ math.degrees( eAngle[0] ) , math.degrees( eAngle[1] ) , math.degrees( eAngle[2] ) ]   
	
	return rot        
    
#_____________________________________________________________________________________________________________________________________________________________________ get vectors distance rapport	    
    
def API_getVectorsDistanceRapport( vA , vB ):
	
	'''
	get the rapport between length of vector B and lenght of vector A:      vB.length()/vA.length() 
	vA and vB are float array
	'''
	
	mVectorADist = ompy.MVector( vA[0] , vA[1] , vA[2] ).length() 
	mVectorBDist = ompy.MVector( vB[0] , vB[1] , vB[2] ).length()
	
	distDiff = mVectorBDist / mVectorADist 
	
	return distDiff    
	
#_____________________________________________________________________________________________________________________________________________________________________ convert triple vecteur to euler rot   # in trsClass   


def API_convertTripleVecteurToEulerRot( vX , vY , vZ , accuracyOrder = [ 0 , 1 , 2 ] ):  # in trsClass
	
	'''
		input are array3 array3 array3
		with 3 vector, find the correct XYZ rotation corresponding
		
		[ 0 , 1 , 2 ] = [ X , Y , Z ]
		if you are not sure about the accuracy of the 3 vector, accuracyOrder give you a way to classe your vectors by the most accurate to the less 
		At default the X is the leader , the if Y is not accurate it ajuste by the X , and Z is praticely useless...
	'''

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
	
	matrix     = ompy.MMatrix(matrixValues)		
	matrixTrsf = ompy.MTransformationMatrix(matrix)
			
	rotEuler = matrixTrsf.rotation( )	
	rotXYZ = [ rotEuler.x , rotEuler.y , rotEuler.z ]

	for i in range( 0 , 3):
		rotXYZ[i] = math.degrees( rotXYZ[i] )
		

	if( accuracyOrder == [ 0 , 1 , 2 ] ):
		pass
	elif( accuracyOrder == [ 0 , 2 , 1 ] ):
		rotXYZ = API_rotOffsetInsideEulerRot( rotXYZ , [ -90 , 0 , 0  ] )  # in trsClass
		
	elif( accuracyOrder == [ 1 , 2 , 0 ] ):
		rotXYZ = API_rotOffsetInsideEulerRot( rotXYZ , [ -90 , 0 , 0  ] )  # in trsClass
		rotXYZ = API_rotOffsetInsideEulerRot( rotXYZ , [ 0 , 0 , -90 ] )   # in trsClass
		
	elif( accuracyOrder == [ 1 , 0 , 2 ] ):
		rotXYZ = API_rotOffsetInsideEulerRot( rotXYZ , [ 0 , 0 , -90  ] )  # in trsClass
		rotXYZ = API_rotOffsetInsideEulerRot( rotXYZ , [ 0 , 180 , 0  ] )  # in trsClass	
		
	elif( accuracyOrder == [ 2 , 0 , 1 ] ):
		rotXYZ = API_rotOffsetInsideEulerRot( rotXYZ , [ 90 , 0 , 0  ] )   # in trsClass
		rotXYZ = API_rotOffsetInsideEulerRot( rotXYZ , [ 0 , 90 , 0] )	     # in trsClass
		
	elif( accuracyOrder == [ 2 , 1 , 0 ] ):
		rotXYZ = API_rotOffsetInsideEulerRot( rotXYZ , [ 0 , 90 , 0] )     # in trsClass

                                                                                                                                                                                                                                                                                                                                                   
	return rotXYZ	

		
#_____________________________________________________________________________________________________________________________________________________________________ API_convertEulerRotToTripleVecteur   # in trsClass


def API_convertEulerRotToTripleVecteur( rotXYZ , rotOrder = [ 'X' , 'Y' , 'Z' ] ):    # in trsClass

	initCoords = [ [ 1 , 0 , 0 ] , [ 0 , 1 , 0 ] , [ 0 , 0 , 1 ] ]
	piv = [ 0 , 0 , 0 ]
	
	newCoords = initCoords
	for i in range( 0 , len(rotXYZ) ):
		newCoords = utilsMath.rotateCoords( newCoords , piv , rotOrder[i] , rotXYZ[i] )	
		
	return newCoords


#_____________________________________________________________________________________________________________________________________________________________________ API_convert2CoordsToTripleVecteurOrient  # in trsClass

def API_convert2CoordsToEulerOrient( coordsA , coordsB , vY  = [ 0 , 1 , 0 ] ):  # in trsClass

	MVectorX = ompy.MVector( ( coordsB[0] - coordsA[0] ) , ( coordsB[1] - coordsA[1] ) , ( coordsB[2] - coordsA[2] ) )

	'''	
	???
	if( coordsA[1] > coordsB[1] ):	
		MVectorX = MVectorX * -1
	'''
	
	vX  = [ MVectorX.x , MVectorX.y , MVectorX.z ]	
	vZ  = [ 1 , 0 , 0 ]
	
	rotXYZ = API_convertTripleVecteurToEulerRot( vX , vY , vZ )   # in trsClass
	
	
	return rotXYZ
 

#_____________________________________________________________________________________________________________________________________________________________________ get2VectorsNormal    
	    
def get2VectorsNormal( vectorA , vectorB , vectorMoyen ):
	
	'''
		input: que des MVector
		
		determine the normal of a plan represented by vectorA and vectorB
		vectorMoyen is to determine witch side of the plan the normal is
		
		output: que des MVector	
	'''
	
	
	
	normalx = ((vectorA.y)*(vectorB.z)-(vectorA.z)*(vectorB.y))
	normaly = ((vectorA.z)*(vectorB.x)-(vectorA.x)*(vectorB.z))
	normalz = ((vectorA.x)*(vectorB.y)-(vectorA.y)*(vectorB.x))
	
	vecteurNormal = ompy.MVector( normalx , normaly , normalz )
	
	coef = getSignScalaireProduct(vecteurNormal , vectorMoyen )
	
	vecteurNormal = ompy.MVector( normalx * coef , normaly * coef  , normalz * coef  )
	    
	     
	return vecteurNormal 

#_____________________________________________________________________________________________________________________________________________________________________ getSignScalaireProduct

def getSignScalaireProduct( vectorA , vectorRef ):
	
	'''
		input vectors must be MVector obj
		
		get the sign of the scalaire product between two vectors: 
		for simplify if the angle between the two is less than 90, it return 1 , more than 90 it return -1
	
	'''

	sign = math.copysign( 1 , vectorA * vectorRef ) 
	            
	return sign  



	
#==========================================================================================================================
#=======================================================    TRS     =======================================================
#==========================================================================================================================
		
#_____________________________________________________________________________________________________________________________________________________________________ convert TRS value to mMatrix   # in trsClass
	
def API_convertTRSValueToMMatrix( TRSValue ):   # in trsClass
	
	'''
		create a MTransformationMatrix with TRSValue. like if we create a transform with TRSValue in his attribute
		
		TRSValue = [ 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1 ]      TRS stand for Translate Rotate Scale		
	'''

	tMatrix = ompy.MTransformationMatrix()
	tMatrix.setTranslation( ompy.MVector( TRSValue[0]  , TRSValue[1] , TRSValue[2] ) , ompy.MSpace.kWorld )
	tMatrix.setRotation( ompy.MEulerRotation( math.radians(TRSValue[3]) , math.radians(TRSValue[4]) , math.radians(TRSValue[5]) )     )
	tMatrix.setScale( [ TRSValue[6] ,TRSValue[7] ,   TRSValue[8]  ]   , ompy.MSpace.kWorld  )
	tMatrix.setShear(   [ 0     ,   0     ,   0  ]   , ompy.MSpace.kWorld   )
	
	
	matrix = tMatrix.asMatrix()

	return matrix 	

#_____________________________________________________________________________________________________________________________________________________________________ get parented TRS value      # in trsClass
	
def API_getParentedTRSvalue( TRSValue , parentTRSValue  ):      # in trsClass
	
	'''
		act as if trsValue is a transform node and we parent it to parentTRSValue.
		the New trsValue is return
	
		TRSValue = [ 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1 ]      TRS stand for Translate Rotate Scale
	'''

	matrixP = API_convertTRSValueToMMatrix( parentTRSValue )  # in trsClass
	matrixP = matrixP.inverse()
	
	matrixG = API_convertTRSValueToMMatrix( TRSValue )   # in trsClass
	
	mChildren = matrixG * matrixP
	
	mtransChildren = ompy.MTransformationMatrix( mChildren )

	translate = mtransChildren.translation( ompy.MSpace.kWorld) 
	rotate    = mtransChildren.rotationComponents()
	scale     = mtransChildren.scale( ompy.MSpace.kWorld)
 	
	childrenTRSValue = [ translate[0] , translate[1] , translate[2] , math.degrees(rotate[0]) , math.degrees(rotate[1]) , math.degrees(rotate[2]) , scale[0] , scale[1] , scale[2] ]	

	return childrenTRSValue


#_____________________________________________________________________________________________________________________________________________________________________ get unparented TRS value   # in trsClass	

def API_getUnparentedTRSvalue( TRSValue , parentTRSValue  ):   # in trsClass

	'''
		act as if trsValue is a transform node under parentTRSValue and we place it in the world.
		the New trsValue is return
	
		TRSValue = [ 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1 ]      TRS stand for Translate Rotate Scale
	'''	
	
	
	matrixP = API_convertTRSValueToMMatrix( parentTRSValue )  # in trsClass
	
	matrixG = API_convertTRSValueToMMatrix( TRSValue )    # in trsClass
	
	mChildren = matrixG * matrixP
	
	mtransChildren = ompy.MTransformationMatrix( mChildren )

	translate = mtransChildren.translation( ompy.MSpace.kWorld) 
	rotate    = mtransChildren.rotationComponents()
	scale     = mtransChildren.scale( ompy.MSpace.kWorld)
 	
	childrenTRSValue = [ translate[0] , translate[1] , translate[2] , math.degrees(rotate[0]) , math.degrees(rotate[1]) , math.degrees(rotate[2]) , scale[0] , scale[1] , scale[2] ]	

	return childrenTRSValue	
	
				
		
#_____________________________________________________________________________________________________________________________________________________________________ find same geometry transform difference   # in trsClass

def API_getTransformDifferenceBetweenSameGeometry( objA , objB ):   # in trsClass
	
	'''
		work with two same geometry. it return a TRS value
		TRSValue = [ 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1 ]      TRS stand for Translate Rotate Scale
		
		if you apply the returned TRS value to the objA , the objA must supperpose the objB. ( objA and objB must be freeze )	
	'''	
	
	pivACoords = mc.xform( objA , q = True , piv = True , ws = True )	
		
	objACoords = []
	objACoords.append( mc.xform( objA + '.vtx[0]' , q = True , ws = True , t = True ) )
	objACoords.append( mc.xform( objA + '.vtx[1]' , q = True , ws = True , t = True ) )
	objACoords.append( mc.xform( objA + '.vtx[2]' , q = True , ws = True , t = True ) )
	
	objBCoords = []
	objBCoords.append( mc.xform( objB + '.vtx[0]' , q = True , ws = True , t = True ) )
	objBCoords.append( mc.xform( objB + '.vtx[1]' , q = True , ws = True , t = True ) )
	objBCoords.append( mc.xform( objB + '.vtx[2]' , q = True , ws = True , t = True ) )
	
	# compute the transformation if vtx[0] were the pivot point
	
	translateDiff = [ objBCoords[0][0] - objACoords[0][0] , objBCoords[0][1] - objACoords[0][1]  , objBCoords[0][2] - objACoords[0][2] ]
	
	vSA            = [ objACoords[1][0] - objACoords[0][0] , objACoords[1][1] - objACoords[0][1]  , objACoords[1][2] - objACoords[0][2] ]
	vSB            = [ objACoords[2][0] - objACoords[0][0] , objACoords[2][1] - objACoords[0][1]  , objACoords[2][2] - objACoords[0][2] ]
	
	vDA            = [ objBCoords[1][0] - objBCoords[0][0] , objBCoords[1][1] - objBCoords[0][1]  , objBCoords[1][2] - objBCoords[0][2] ]
	vDB            = [ objBCoords[2][0] - objBCoords[0][0] , objBCoords[2][1] - objBCoords[0][1]  , objBCoords[2][2] - objBCoords[0][2] ]
	
	#rotDiff       = API_getVectorsRotDifference( vA , vB )
	####################
	rotS = API_convertTripleVecteurToEulerRot( vSA , vSB , [ 0 , 1 , 0 ] )  # in trsClass
	rotD = API_convertTripleVecteurToEulerRot( vDA , vDB , [ 0 , 1 , 0 ] )  # in trsClass
	
	
	TRSSource      = [ 0 , 0 , 0 , rotS[0] , rotS[1]  , rotS[2] , 1 , 1 , 1 ] 
	TRSDestination = [ 0 , 0 , 0 , rotD[0] , rotD[1]  , rotD[2] , 1 , 1 , 1 ] 
	TRSpiv         = [ 0 , 0 , 0 , 0 , 0  , 0 , 1 , 1 , 1 ] 
		
	TRSSourceInv = API_getParentedTRSvalue( TRSpiv , TRSSource )             # in trsClass  
	TRSrotfinal  = API_getUnparentedTRSvalue( TRSSourceInv , TRSDestination )# in trsClass
	
	rotDiff = TRSrotfinal[3:6]
	####################
	
	scaleXDiff    = API_getVectorsDistanceRapport( vSA , vDA )    
	
	transformDiff = translateDiff + rotDiff + [ scaleXDiff , scaleXDiff , scaleXDiff ]

	# compute the position of objB pivot like if it was the same the objA

	pivBCoords = API_convertCoordsByParentTransformation( pivACoords , transformDiff , objACoords[0] )

	# calcule de la translation entre pivA et pivB
	
	translateDiffPiv = [ pivBCoords[0] - pivACoords[0] , pivBCoords[1] - pivACoords[1] , pivBCoords[2] - pivACoords[2] ]  	
	transformDiffPiv =  translateDiffPiv + rotDiff + [ scaleXDiff , scaleXDiff , scaleXDiff ]
	
	return transformDiffPiv 


#_____________________________________________________________________________________________________________________________________________________________________ mirrorTrsValue  # in trsClass



def mirrorTrsValue( trsValue , planSymCoords  ):  # in trsClass	
		
		#COORDS_get coords			
		manipCoords = trsValue[0:3]
			
		tripleOrientVector = API_convertEulerRotToTripleVecteur(  trsValue[3:6] )  # in trsClass
		
		tripleOrientCoords = []			
		for v in tripleOrientVector: 			
			tripleOrientCoords.append( [ v[0] + manipCoords[0] , v[1] + manipCoords[1] , v[2] + manipCoords[2] ] )

			
		#COORDS_get coords	on symPlane	
								
		manipCoordsMiddle = snapCoordsOnPlane( planSymCoords , manipCoords )  # in trsClass
		
		tripleOrientCoordsMiddle = []
		for c in tripleOrientCoords:
			tripleOrientCoordsMiddle.append( snapCoordsOnPlane( planSymCoords , c ) )  # in trsClass
		
		#COORDS_get vector to sym
		
		manipVtoSym = [ ( manipCoordsMiddle[0] - manipCoords[0] )*2 , ( manipCoordsMiddle[1] - manipCoords[1] )*2 , ( manipCoordsMiddle[2] - manipCoords[2] )*2 ]
		
		tripleOrientVToSym = []
		for i in range( 0 , len( tripleOrientCoordsMiddle ) ):
			tmpVector =  [ ( tripleOrientCoordsMiddle[i][0] - tripleOrientCoords[i][0] )*2 , ( tripleOrientCoordsMiddle[i][1] - tripleOrientCoords[i][1] )*2 , ( tripleOrientCoordsMiddle[i][2] - tripleOrientCoords[i][2] )*2 ]
			tripleOrientVToSym.append( tmpVector )
		
		#COORDS_sym coords
		
		manipCoordsSym = [ manipCoords[0] + manipVtoSym[0] , manipCoords[1] + manipVtoSym[1] , manipCoords[2] + manipVtoSym[2] ]
		
		tripleOrientCoordsSym = []
		tripleOrientVectorSym = []		
		for i in range( 0 , len( tripleOrientCoords ) ):
			tripleOrientCoordsSym =  [ tripleOrientCoords[i][0] + tripleOrientVToSym[i][0] , tripleOrientCoords[i][1] + tripleOrientVToSym[i][1] , tripleOrientCoords[i][2] + tripleOrientVToSym[i][2] ] 
			tripleOrientVectorSym.append( [ tripleOrientCoordsSym[0] - manipCoordsSym[0] , tripleOrientCoordsSym[1] - manipCoordsSym[1] , tripleOrientCoordsSym[2] - manipCoordsSym[2] ]    )
				
		# get priority order
		'''
			when you make a mirror of the axe, you have the direction of axe, but not the direction/way.
			the first triple orient vertor must have the same direction of the second
		'''
		for i in range( 0 , len(tripleOrientVector) ):
			vOrient    = ompy.MVector( tripleOrientVector[i][0]    , tripleOrientVector[i][1]    , tripleOrientVector[i][2]    )
			vOrientsym = ompy.MVector( tripleOrientVectorSym[i][0] , tripleOrientVectorSym[i][1] , tripleOrientVectorSym[i][2] )				
		
			sign = getSignScalaireProduct( vOrient , vOrientsym )
			tripleOrientVectorSym[i] = [ tripleOrientVectorSym[i][0] * sign , tripleOrientVectorSym[i][1] * sign , tripleOrientVectorSym[i][2] * sign ] 
		
		
			
		# get rotation			
		rotSym = API_convertTripleVecteurToEulerRot( tripleOrientVectorSym[0] , tripleOrientVectorSym[1] , tripleOrientVectorSym[2] )  # in trsClass
		
		# get TRS			
		mirrorTrsValue =  manipCoordsSym + rotSym + trsValue[6:9]
		
		return mirrorTrsValue
  


#_____________________________________________________________________________________________________________________________________________________________________ find same geometry transform difference

def inverseTrsValueAxes( trsValue , inverseAxes  , trsChoice = [ 0 , 1 , 0 ] ):  # in trsClass
	
	'''
		inverseAxes = [ 0 , 0 , 0 ] , represent X Y Z axes
		
		warning: you can only inverse 2 axes at the same time
	
	'''
	
	#translate
	if( trsChoice[0] ):
		for i in range( 0 , 3 ):
			trsValue[i] =  trsValue[i] * ( 1 - inverseAxes[i] ) - trsValue[i] * inverseAxes[i]  

	# rotate
	if( trsChoice[1] ):	
		if( inverseAxes == [ 0 , 0 , 0 ] ):
			pass
		elif( inverseAxes == [ 1 , 1 , 0 ]  ):
			trsValue[3:6] = API_rotOffsetInsideEulerRot( trsValue[3:6] , [ 0 , 0 , 180 ] )   # in trsClass
		elif( inverseAxes == [ 1 , 0 , 1 ]  ):
			trsValue[3:6] = API_rotOffsetInsideEulerRot( trsValue[3:6] , [ 0 , 180 , 0 ] )   # in trsClass
		elif( inverseAxes == [ 0 , 1 , 1 ]  ):
			trsValue[3:6] = API_rotOffsetInsideEulerRot( trsValue[3:6] , [ 180 , 0 , 0 ] )   # in trsClass		
		else:
			mc.error('you can only inverse 2 axes at the same time')
		

	#scale	
	if( trsChoice[2] ):	
		for i in range( 6 , 9 ):
			trsValue[i] =  trsValue[i] * ( 1 - inverseAxes[i-6] ) - trsValue[i] * inverseAxes[i-6]  
	
		
	return trsValue				
		

	
	
	
	
#==========================================================================================================================
#======================================================     BB REEL    ====================================================
#==========================================================================================================================

#_____________________________________________________________________________________________________________________________________________________________________ getTRSreelBB # in trsClass

def getTRSreelBB( baseName , indexs ):   # in trsClass
	
	
	allCoords = API_getAllVertexCoords( baseName )
	coords    = []	
	for i in indexs:
		coords.append( allCoords[i] )
	
	reelBBCoords = getBBreelCoords( coords )
		
	position  = getBBreelPositions(reelBBCoords)	
	rotation  = getBBreelOrientation(reelBBCoords)	
	scale     = getBBreelScale(reelBBCoords)	
	
	return  position[0] + rotation + scale  
	
	
#_____________________________________________________________________________________________________________________________________________________________________ getBBreelCoords

def getBBreelCoords( coords ):
	
	import maya.cmds as mc	
	mc.loadPlugin( 'D:/mcantat_BDD/projects/code/maya/python/plugIn/commands/getOrientedBoundingBox.py' , qt = True )	
	
	
	flattenCoords = [ c for coord in coords for c in coord ]

	reelBBCoords = mc.getReelBBCoordsCmds( flattenCoords )
	
	reelBBCoords3 = []
	for i in range( 0 , len( reelBBCoords ) , 3 ):
		reelBBCoords3.append( [ reelBBCoords[i] , reelBBCoords[i+1] , reelBBCoords[i+2] ] )	
	
	return reelBBCoords3

#_____________________________________________________________________________________________________________________________________________________________________ getBBreelPositions	
	
def getBBreelPositions( BBPoints ):


	baseA = BBPoints[0] 	
	baseB = BBPoints[1] 
	baseC = BBPoints[2]
	baseD = BBPoints[3]
	topA  = BBPoints[4]
	topB  = BBPoints[5]
	topC  = BBPoints[6]
	topD  = BBPoints[7]

	centreBBreel   = utilsMath.getBarycentre( [ baseA , baseB , baseC , baseD , topA , topB , topC , topD ] )	
	
	centreBaseABCD = utilsMath.getBarycentre( [ baseA , baseB , baseC , baseD ] )
	centreTopABCD  = utilsMath.getBarycentre( [ topA , topB  , topC  , topD ]  )
	
	centreCoteA  = utilsMath.getBarycentre(  [ baseA , baseB  , topA  , topB ] )
	centreCoteB  = utilsMath.getBarycentre(  [ baseB , baseC  , topB  , topC ] )
	centreCoteC  = utilsMath.getBarycentre(  [ baseC , baseD  , topC  , topD ] )
	centreCoteD  = utilsMath.getBarycentre(  [ baseD , baseA  , topD  , topA ] )
	               
	positions = [ centreBBreel , centreBaseABCD , centreTopABCD , centreCoteA , centreCoteB , centreCoteC , centreCoteD ]

	return positions     

#_____________________________________________________________________________________________________________________________________________________________________ getBBreelOrientation


def getBBreelOrientation( BBPoints ):
	
	baseB = BBPoints[1]
	baseD = BBPoints[3] 	
	baseC = BBPoints[0]
	topC  = BBPoints[4]
		
	vX = [  baseB[0] - baseC[0]  ,  baseB[1] - baseC[1]  ,  baseB[2] - baseC[2]  ]	
	vY = [   topC[0] - baseC[0]  ,   topC[1] - baseC[1]  ,   topC[2] - baseC[2]  ]
	vZ = [  baseD[0] - baseC[0]  ,  baseD[1] - baseC[1]  ,  baseD[2] - baseC[2]  ]

    
	rotXYZ = API_convertTripleVecteurToEulerRot( vX , vY , vZ )    # in trsClass 
    
	return rotXYZ   		

	

	
#_____________________________________________________________________________________________________________________________________________________________________ getBBreelScale

def getBBreelScale( BBPoints ):
	
	baseB = BBPoints[1]
	baseD = BBPoints[3] 	
	baseC = BBPoints[0]
	topC  = BBPoints[4]

	dX = ompy.MVector(   baseB[0] - baseC[0]  ,  baseB[1] - baseC[1]  ,  baseB[2] - baseC[2]  ).length()	
	dY = ompy.MVector(    topC[0] - baseC[0]  ,   topC[1] - baseC[1]  ,   topC[2] - baseC[2]  ).length()	
	dZ = ompy.MVector(   baseD[0] - baseC[0]  ,  baseD[1] - baseC[1]  ,  baseD[2] - baseC[2]  ).length()	

    
	return [ dX , dY , dZ ] 

#_____________________________________________________________________________________________________________________________________________________________________ convertTRSToReelBB    # in trsClass


def convertTRSToReelBB( trsValue ):   # in trsClass
	
	reelBBCoords = [ [-0.5,-0.5,-0.5] , [0.5,-0.5,-0.5] , [0.5,-0.5,0.5] , [-0.5,-0.5,0.5] , [-0.5,0.5,-0.5] , [0.5,0.5,-0.5] , [0.5,0.5,0.5] , [-0.5,0.5,0.5]  ]  # <---- ordre a revoir
	
	reelBBCoords = utilsMath.transformCoords( reelBBCoords , [ 0 , 0 , 0 ]  , trsValue , 'XYZ'  )
	
	return reelBBCoords
		

	
#==========================================================================================================================
#======================================================     UTILS    ======================================================
#==========================================================================================================================

#_____________________________________________________________________________________________________________________________________________________________________get mDagPath 

def API_getMDagPath( obj ):	
	
	'''
	convert maya name into dagPath , very use to manipulate obj in API	
	'''

	selection = ompy.MSelectionList()
	selection.add( obj )
	
	dagPath= ompy.MDagPath()
	dagPath = selection.getDagPath( 0 )
	
	return dagPath
	
	
#==========================================================================================================================
#======================================================     CURVE    ======================================================
#==========================================================================================================================

#_____________________________________________________________________________________________________________________________________________________________________ get closest point on curve    # in trsClass  

def API_getClosestPointOnCurve( curveName , pointCoords ):	    # in trsClass
	
	'''
		get a point on curveName witch is the closest of the given coords.
		it return [ [ coordX , coordY , coordZ ] , u ]
	'''
	
	pointApi = ompy.MPoint( pointCoords[0] , pointCoords[1] , pointCoords[2] )
	curveApi = ompy.MFnNurbsCurve( API_getMDagPath( curveName ) )	
	closestPointInfo = curveApi.closestPoint(pointApi)
	
	coords = [ closestPointInfo[0].x , closestPointInfo[0].y , closestPointInfo[0].z ]
	u = closestPointInfo[1] 
	
	return [ coords , u ] 
		
#_____________________________________________________________________________________________________________________________________________________________________ get curve u TRS

def API_getCurveUTrs( curveName , u ):
	
	'''
		return a TRSvalue cooresponding to curveName's tangeant at u value
		it works only with algorithms of maya
		
		TRSValue = [ 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1 ]      TRS stand for Translate Rotate Scale		
	
	'''
    
	curveApi = ompy.MFnNurbsCurve( API_getMDagPath( curveName ) )
	dirVector = curveApi.tangent( u , space= ompy.MSpace.kObject )
	normalVector = curveApi.normal( u , space= ompy.MSpace.kObject )
	point = curveApi.getPointAtParam( u , space= ompy.MSpace.kObject )

	vX = [ dirVector.x , dirVector.y , dirVector.z ]
	vY = [ normalVector.x , normalVector.y , normalVector.z ]
	vZ = [ 1 , 1 , 1 ]

	tValue = [ point.x , point.y , point.z ]		
	rValue = API_convertTripleVecteurToEulerRot( vX , vY , vZ)  # in trsClass
	
	trsValue = ( tValue + rValue + [ 1 , 1 , 1 ] )
	
	return trsValue	

#_____________________________________________________________________________________________________________________________________________________________________ get curve u logic TRS      # in trsClass
	
def API_getCurveULogicTrs( curveName , u ):         # in trsClass
	
	'''
		return a TRSvalue cooresponding to curveName's tangeant at u value

		TRSValue = [ 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1 ]      TRS stand for Translate Rotate Scale
		
		To be sure that the tangeant have the right orientation , it works with special algorithms:
		Each time you ask a tangeant at u, it start at 0 and "walk" to u with an step of uInterval. At each step it compute the right orient based on the last one.
		At u(0) it take the world orient as reference , and u( n + uInterval ) take the orientation of u( n ).
					
	'''
	
	uInterval = 0.022
	upVector = [ 0 , 1 , 0 ]
	curveApi  = ompy.MFnNurbsCurve( API_getMDagPath( curveName ) )
	
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
				
		rValue = API_convertTripleVecteurToEulerRot( vX , vY , vZ)  # in trsClass
		
		trsValue = ( tValue + rValue + sValue )
		
		# get next up vector
		
		trsValueUpUnder = API_getUnparentedTRSvalue( trsValueUp , trsValue ) # in trsClass	
		vectorPointUp = ompy.MVector( ( trsValueUpUnder[0] - trsValue[0] ) , ( trsValueUpUnder[1] - trsValue[1] ) , ( trsValueUpUnder[2] - trsValue[2] )  ).normalize()				
		upVector = [ vectorPointUp.x , vectorPointUp.y , vectorPointUp.z ]	
			
		
	return trsValue  
	
	
	
	
#_____________________________________________________________________________________________________________________________________________________________________ getStraigtCurveCoords

def getStraigtCurveCoords( curveCoords ):
	
	degree       = 3
	nbrCvs       = len( curveCoords ) 
	nbrIntervals = nbrCvs - 1
	
	firstCvCoords = curveCoords[0]
	lastCvCoords  = curveCoords[-1]
	    
	dirVector = ompy.MVector( lastCvCoords[0] - firstCvCoords[0] , lastCvCoords[1] - firstCvCoords[1] , lastCvCoords[2] - firstCvCoords[2] )
	lenVector = dirVector.length()
	dirVector.normalize()    
	lenBtwCvs = lenVector / nbrIntervals
	
	straigtCurveCoords = [ firstCvCoords ]
	newCoord = firstCvCoords[:] 
	
	for i in range( 0 , nbrIntervals ):
		newCoord[0] += dirVector.x * lenBtwCvs
		newCoord[1] += dirVector.y * lenBtwCvs 
		newCoord[2] += dirVector.z * lenBtwCvs                 
		straigtCurveCoords.append( newCoord[:] )     
	 
	return straigtCurveCoords   
	
	
	
#==========================================================================================================================
#======================================================     MAYA     ======================================================
#==========================================================================================================================

#_____________________________________________________________________________________________________________________________________________________________________ convert vertex to edges
		
def API_convertVertexToEdges(vtxName):
	
	'''
		with the vertex's name give the edges associate
	'''
			
	vtxObj , vtxNum = getObjNameAndIndex( vtxName )	

	# Iterate over all the mesh vertices and get position of required vtx		
		
	pathDg    = API_getMDagPath(vtxObj)
	
	mItVtx    = ompy.MItMeshVertex(pathDg)
	edgeIndex = ompy.MIntArray()
	vtxPos    = []	
	
	while not mItVtx.isDone():
		if( mItVtx.index() == vtxNum ):
			edgeIndex = mItVtx.getConnectedEdges()
			break
		mItVtx.next()
		
		
	edgeNames = []		
	for i in range( 0 , edgeIndex.__len__() ):
		edgeNames.append( vtxObj + '.e[{0}]'.format(edgeIndex[i]) )
	    
	
	return edgeNames

#_____________________________________________________________________________________________________________________________________________________________________ convert edge to vertices


def API_convertEdgeToVertices(edgeName):
	
	'''
		with the edge's name give the two vertices associate
	'''

	edgeObj , edgeNum = getObjNameAndIndex( edgeName )			
		
	# Iterate over all the mesh vertices and get position of required vtx		
		
	pathDg    = API_getMDagPath(edgeObj)	
	mItVtx    = ompy.MItMeshVertex(pathDg)

	vtxNum = []	
	while not mItVtx.isDone():
		if mItVtx.connectedToEdge(edgeNum):			
			vtxNum.append( mItVtx.index() ) 
		mItVtx.next()
		
		
	vtxNames = []
	for i in range( 0 , len(vtxNum) ):
		vtxNames.append( edgeObj + '.vtx[{0}]'.format(vtxNum[i]) )
	    	
	return vtxNames

#_____________________________________________________________________________________________________________________________________________________________________ grow vertices by edge
		
def API_growVerticesByEdge( verticesBase , keepVerticesBase = 1 ):

	'''	
	Grow selection of a list a vertices. Yse keepVerticesBase = 0 for removing the input vertices	
	'''
	
	edgesGrow    = []
	
	for vtx in verticesBase:
		edgesGrow += API_convertVertexToEdges( vtx )

	edgesGrow    = list(set(edgesGrow))	
	verticesGrow = []
	
	for edge in edgesGrow:
		verticesGrow += API_convertEdgeToVertices( edge )		
		
	verticesGrow = list(set(verticesGrow))	

	
	
	if( keepVerticesBase == 0 ):	
		for v in verticesBase:
			try:verticesGrow.remove(v)
			except:pass

	return verticesGrow 	


#==========================================================================================================================
#======================================================     AUTRE    ======================================================
#==========================================================================================================================

#_____________________________________________________________________________________________________________________________________________________________________ set axis up

def setAxisUp( rotValue , axis ):     # in trsClass
	
 		
	if( axis == 'X' ):
		rotValue = API_rotOffsetInsideEulerRot( rotValue , 'XYZ' , [ 0 , 0 , 90 ] )  # in trsClass
	
	elif( axis == 'Z' ):
		rotValue = API_rotOffsetInsideEulerRot( rotValue , 'XYZ' , [ -90 , 0 , 0 ] )	 # in trsClass	

		
	return rotValue 	

#_____________________________________________________________________________________________________________________________________________________________________ get objName And index

import re

def getObjNameAndIndex( componentName ):

	testIndex = re.search( '(?<=\[)(?P<vtxNum>[\d]+)(?=\])', str(componentName) )

	if testIndex:
		index = int(testIndex.group('vtxNum'))
		obj = componentName.split('.')[0]
	else:
		return

	return [ obj , index ]


	
#_____________________________________________________________________________________________________________________________________________________________________ getTwoVerticesLength
def getTwoVerticesLength( vtxA , vtxB ):

	coordA = mc.xform( vtxA , q = True , ws = True , t = True )
	coordB = mc.xform( vtxB      , q = True , ws = True , t = True )
	dist   = om.MVector( coordB[0] - coordA[0] , coordB[1] - coordA[1] , coordB[2] - coordA[2] ).length() 

	return dist 	
	
	
	
	

#_____________________________________________________________________________________________________________________________________________________________________ API_getSortedDistancesIndexCoords
def API_getSortedDistancesIndexCoords( coords , i ):

	distances = []
	
	for c in coords:		
		distance = ompy.MVector(   ( c[0] - coords[i][0] ) , ( c[1] - coords[i][1] ) , ( c[2] - coords[i][2] )    ).length()
		distances.append( distance )
		
	distances.sort()
	distances.reverse()
	
	return distances
		
#_____________________________________________________________________________________________________________________________________________________________________ getfarestCoordsIndex
def getfarestCoordsIndex( coords , indexBase ):
	
	dicoDistCoords = {}
	distances = []


	for i in  indexBase :
		
		distance = ompy.MVector(   ( coords[i][0] - coords[0][0] ) , ( coords[i][1] - coords[0][1] ) , ( coords[i][2] - coords[0][2] )    ).length()
		dicoDistCoords[ distance ] = i	
		distances.append( distance )
		
	distances.sort()
	
	distances.reverse()

	return dicoDistCoords[distances[0]]

	
	

#_____________________________________________________________________________________________________________________________________________________________________ getClosestAxeFromVector
		
def getClosestAxeFromVector( trsValue , vector ):
	
	'''
		give the closest axe to a vector for an obj . axe = X , Y or Z 
		
		vector = [ 0 , 0 , 0 ]
	
	'''
	
	mainVector = ompy.MVector( vector[0] , vector[1] , vector[2] )
	
	vectorsXYZ = API_convertEulerRotToTripleVecteur( trsValue[3:6] )   # in trsClass
	
	vectorX =  ompy.MVector( vectorsXYZ[0][0] , vectorsXYZ[0][1] , vectorsXYZ[0][2] ) 
	vectorY =  ompy.MVector( vectorsXYZ[1][0] , vectorsXYZ[1][1] , vectorsXYZ[1][2] ) 	
	vectorZ =  ompy.MVector( vectorsXYZ[2][0] , vectorsXYZ[2][1] , vectorsXYZ[2][2] ) 
		
	dotProducts = [ abs(mainVector * vectorX) , abs(mainVector * vectorY) , abs(mainVector * vectorZ) ]
	dotProductsDico = { dotProducts[0] : 'X' , dotProducts[1] : 'Y' , dotProducts[2] : 'Z' }
	dotProducts.sort()
	dotProducts.reverse()
	

	return dotProductsDico[dotProducts[0]]		
	


#_____________________________________________________________________________________________________________________________________________________________________ getClosestAxeFromVector
		
def getAxesSignFromVector( trsValue , vector ):
	
	'''
		give the closest axe to a vector for an obj . axe = X , Y or Z 
		
		vector = [ 0 , 0 , 0 ]
	
	'''
	
	mainVector = ompy.MVector( vector[0] , vector[1] , vector[2] )
	
	vectorsXYZ = API_convertEulerRotToTripleVecteur( trsValue[3:6] )   # in trsClass
	
	vectorX =  ompy.MVector( vectorsXYZ[0][0] , vectorsXYZ[0][1] , vectorsXYZ[0][2] ) 
	vectorY =  ompy.MVector( vectorsXYZ[1][0] , vectorsXYZ[1][1] , vectorsXYZ[1][2] ) 	
	vectorZ =  ompy.MVector( vectorsXYZ[2][0] , vectorsXYZ[2][1] , vectorsXYZ[2][2] ) 
		
	dotProducts = [ math.copysign( 1 , (mainVector * vectorX) ) , math.copysign( 1 , (mainVector * vectorY) ) , math.copysign( 1 , (mainVector * vectorZ) ) ]	

	return dotProducts	







	
	
def API_skinClusterClass( skinClusterName  ):
   

	allSkins = om.MItDependencyNodes( om.MFn.kSkinClusterFilter )

	
	i = 1
	while not allSkins.isDone():
	       
		skinObj = allSkins.thisNode() 
		actualName = om.MFnDependencyNode(skinObj).name() 
		
		if( actualName  == skinClusterName ):
			skin = oma.MFnSkinCluster( skinObj )
			break
		

		 
		allSkins.next()         
		i+=1        
		if( i > 300 ):
			break
	
	return skin	
	
	

# ===================================================	
# find in :   http://www.macaronikazoo.com/?p=417	 
# ===================================================		
	
	
def setSkinWeights( skinCluster, vertJointWeightData ):	

	'''
	vertJointWeightData is a list of 2-tuples containing the vertex component name, and a list of 2-tuples
	containing the joint name and weight.  ie it looks like this:
	[ ('someMesh.vtx[0]', [('joint1', 0.25), 'joint2', 0.75)]) , ('someMesh.vtx[1]', [('joint1', 0.2), 'joint2', 0.7, 'joint3', 0.1)]), ... ]
	
	'''	
	#convert the vertex component names into vertex indices
	idxJointWeight = []
	
	for vert, jointsAndWeights in vertJointWeightData:
		idx = int( vert[ vert.rindex( '[' )+1:-1 ] )    	
		idxJointWeight.append( (idx, jointsAndWeights) )
	    
	#get an MObject for the skin cluster node
   
	skinFn = API_skinClusterClass( skinCluster )
	
	#construct a dict mapping joint names to joint indices    
	jApiIndices = {}  
	_tmp = om.MDagPathArray()    
	skinFn.influenceObjects( _tmp )    
	
	for n in range( _tmp.length() ):
		jApiIndices[ str( _tmp[n].partialPathName() ) ] = skinFn.indexForInfluenceObject( _tmp[n] )    	
		
	
	weightListP = skinFn.findPlug( "weightList" )        
	weightListObj = weightListP.attribute()        
	weightsP = skinFn.findPlug( "weights" )
	
	tmpIntArray = om.MIntArray()    
	baseFmtStr = str( skinCluster ) +'.weightList[%d]'  #pre build this string: fewer string ops == faster-ness!
	
	for vertIdx, jointsAndWeights in idxJointWeight:    
		#we need to use the api to query the physical indices used    
		weightsP.selectAncestorLogicalIndex( vertIdx, weightListObj )  
		weightsP.getExistingArrayAttributeIndices( tmpIntArray )
		
		weightFmtStr = baseFmtStr % vertIdx +'.weights[%d]'
		
		#clear out any existing skin data - and awesomely we cannot do this with the api - so we need to use a weird ass mel command
		
		for n in range( tmpIntArray.length() ):    	
			mc.removeMultiInstance( weightFmtStr % tmpIntArray[n] )
			
		#at this point using the api or mel to set the data is a moot point...  we have the strings already so just use mel        	
		for joint, weight in jointsAndWeights:
			if weight:
				infIdx = jApiIndices[ joint ]
				mc.setAttr( weightFmtStr % infIdx, weight )	         	
		    	
		
	

def getDistanceBetweenObjs( objA , objB ):
	coordsA = mc.xform( objA , q = True , t=True , ws = True)
	coordsB = mc.xform( objB , q = True , t=True , ws = True)	

	vDiff = ompy.MVector( coordsA[0] - coordsB[0] , coordsA[1] - coordsB[1] , coordsA[2] - coordsB[2] )
	return vDiff.length()



