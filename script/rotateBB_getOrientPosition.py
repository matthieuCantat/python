


import maya.cmds as mc
import maya.OpenMaya as om

#mc.loadPlugin( 'C:/Users/Matthieu/Desktop/Travail/code/maya/script/python/toolBox/mayaCommands/MC_getRotatedBBCoordsCmd_FINAL.py' , qt = True)



exec('import manipsUtils') in globals()
exec('reload (manipsUtils)') in globals()

			
#__________________________________________________________________________________________________________________________________          array Remove Duplicates 


def arrayRemoveDuplicates(objs):
    list = []
    for obj in objs:
        if not obj in list:
            list.append(obj)

    return list

#__________________________________________________________________________________________________________________________________          is In   


def isIn( terms , term1 ):
	
	for term in terms:
		if( term in term1 ):
			return 1
			
	return 0
#__________________________________________________________________________________________________________________________________          createLoc_modeSelection    


def createLoc_modeSelection( selection ):
	
	
	modeSelection = [ 'locator nul' , 'obj(s)' , 'component Mode' , 'component same Index Mode' , 'component same Index aim Mode' ]
	modeI = 0
	

	componentSuffix = [ '.vtx['  , '.cv['  , '.f['  , '.e['   ]
	nbrComponent , nbrObj , nbrBaseName  = 0 , 0 , 0 

	baseNames = []
	
	for elem in selection:		
		
		if(  isIn( componentSuffix , elem )  ):   nbrComponent    += 1			
		else:                                     nbrObj          += 1	  
		
		baseNames.append(   elem.split(".")[0]   )	
				    	
	baseNames = arrayRemoveDuplicates( baseNames )		
	nbrBaseName = len( baseNames )		

	
	if( len( selection ) == 0 ):	
		modeI = 0		
	else:	                                                                  
		if( nbrComponent == 0 ):               
			modeI = 1
		else:					                                                      
			if( nbrBaseName == 1 ) : 
				modeI = 2
			else:  		                                                                   
				if( nbrBaseName == nbrObj + 1  ):    
					modeI = 3
				else:
					modeI = 4	

	
	print( modeSelection[ modeI ] )					
					
		
	return modeI 
		
	
	
#__________________________________________________________________________________________________________________________________          pivot Obj 


def pivotObj( objName ):

	pivotCoords = [ 0 , 0 , 0 ]

	pivotCoords = mc.xform( objName, q = True  , ws = True , t = True ) 

	return pivotCoords

	
#__________________________________________________________________________________________________________________________________          orient Obj 


def orientObj( objName ):

	orient = [ 0 , 0 , 0 ]

	orient = mc.xform( objName, q = True  , ws = True , ro = True )  

	return orient

#__________________________________________________________________________________________________________________________________          convert To vtx


def convertTovtx( selection ):
	
	selectionVtx = []	
	
	componentToConvert = [  '.f['  , '.e['   ]	
	vertexTmp = []
	
	
	for elem in selection:
		
		if ( componentToConvert[0]  in elem ):
			
			vertexTmp = mc.polyListComponentConversion( elem ,  ff = True ,  tv = True )
			for v in vertexTmp:
				selectionVtx.append(v)
				
		elif ( componentToConvert[1]  in elem ):
			
			vertexTmp = mc.polyListComponentConversion( elem ,  fe = True ,  tv = True )
			for v in vertexTmp: 
				selectionVtx.append(v)
		else:
			selectionVtx.append(elem)
	
	
	return selectionVtx

#__________________________________________________________________________________________________________________________________          get Component Base Names


def getComponentBaseNames( selection ):

	baseNames = []

	for elem in selection:			
		baseNames.append(   elem.split(".")[0]   )	
		
		
	baseNames = arrayRemoveDuplicates( baseNames )	

	return baseNames[0]

	
#__________________________________________________________________________________________________________________________________          extract Index

	
def extractIndex( name ):

	iA = name.find('[') + 1
	iB = name.find(']') 
	
	index = name[ iA : iB ]
	
	return int(index)
	
	

#__________________________________________________________________________________________________________________________________          get Component Index 


def getComponentIndex( selectionVtx ):
	
	vIndex = []
	vIndexExpend = []
	
	for elem in selectionVtx:
		if( ':' in elem  ):
			
			vIndexExpend = mc.filterExpand( elem , ex = True , sm = 31 )
			for v in vIndexExpend:
				vIndex.append( extractIndex(v) )	
				
		elif( '.vtx' in elem  ):
			vIndex.append( extractIndex(elem) )		

						
			
	return vIndex
	

	
	
#__________________________________________________________________________________________________________________________________          grow Selection 


	
def growSelection( component ):
	  
	faces          = mc.polyListComponentConversion( component ,  fv = True ,  tf = True )
	growcomponents = mc.polyListComponentConversion( faces ,  ff = True ,  tv = True )  
	
	return growcomponents

	
	
#__________________________________________________________________________________________________________________________________          get Axe 2 Coords

def getaxe2Coords( coordsA , coordsB ):
	
	vInit = om.MVector(   ( coordsB[0] - coordsA[0] ) , ( coordsB[1] - coordsA[1] ) , ( coordsB[2] - coordsA[2] )   )
	
	rot90 = om.MEulerRotation(  0  ,  3.14955 / 2  ,  0  ,   om.MEulerRotation.kXYZ  )
	vDroit = vInit.rotateBy( rot90 )
	
	quatRot90 = om.MQuaternion( 3.14955 / 2 , vInit  ) 		
	vfinal    = vDroit.rotateBy(quatRot90 )
	
	return [ [ vInit.x , vInit.y , vInit.z ] , [ vDroit.x , vDroit.y , vDroit.z ] , [ vfinal.x , vfinal.y , vfinal.z ] ]






	
#=================================================================================================================================================================================
#===========================================================================================================================                 ROTATE BB PROCS               =======
#=================================================================================================================================================================================



#__________________________________________________________________________________________________________________________________          get All Vertex Coords 


def getAllVertexCoords(_nameMesh):
 
	# get the active selection
	selection = om.MSelectionList()
	selection.add(_nameMesh)
	iterSel = om.MItSelectionList(selection, om.MFn.kMesh)
 
	# go througt selection
	while not iterSel.isDone():
 
		# get dagPath
		dagPath = om.MDagPath()
		iterSel.getDagPath( dagPath )
 
		# create empty point array
		inMeshMPointArray = om.MPointArray()
 
		# create function set and get points in world space
		currentInMeshMFnMesh = om.MFnMesh(dagPath)
		currentInMeshMFnMesh.getPoints(inMeshMPointArray, om.MSpace.kWorld)
 
		# put each point to a list
		pointList = []
 
		for i in range( inMeshMPointArray.length() ) :
			
			pointList.append( [inMeshMPointArray[i][0], inMeshMPointArray[i][1], inMeshMPointArray[i][2]] )
 
		return pointList


#__________________________________________________________________________________________________________________________________          get Index Vertex Coords


def getIndexVertexCoords( vCoords , indexs ):

	if( len( indexs ) == 0 ):
		return vCoords
		
	coords = []
	
	for i in indexs:
		coords.append( vCoords[i] ) 
		
	return coords

	
	

#__________________________________________________________________________________________________________________________________          get Barycentre


def getBarycentre( *points ):
    
    sizePoints = len( points )    
    bCoords = [ 0.0 , 0.0 , 0.0 ]
    
    for point in points:
        bCoords[0] += point[0]
        bCoords[1] += point[1]
        bCoords[2] += point[2]

    bCoords = [ bCoords[0] / sizePoints , bCoords[1] / sizePoints , bCoords[2] / sizePoints  ]

    return bCoords

	
#__________________________________________________________________________________________________________________________________          convert Triple Vecteur To Euler Rot


def convertTripleVecteurToEulerRot( vX , vY , vZ):

	vecteurX = om.MVector( vX[0] , vX[1] , vX[2]  )
	vecteurY = om.MVector( vY[0] , vY[1] , vY[2]  )
	vecteurZ = om.MVector( vZ[0] , vZ[1] , vZ[2]  )	
	
	vecteurX.normalize()	
	vecteurY.normalize()
	vecteurZ.normalize()	
	
	
	matrixValues = ( vecteurX.x , vecteurX.y , vecteurX.z , 0 , vecteurY.x , vecteurY.y , vecteurY.z , 0 , vecteurZ.x , vecteurZ.y , vecteurZ.z , 0 , 0 , 0 , 0 , 0 )
	matrix = om.MMatrix()
	
	matrix_util = om.MScriptUtil()
	matrix_util.createMatrixFromList( matrixValues , matrix ) 	
	
	matrixTrsf = om.MTransformationMatrix(matrix)

	rotEuler = matrixTrsf.eulerRotation( )	

	rotXYZ = [ rotEuler.x , rotEuler.y , rotEuler.z ]
	
	#conversion en degres
	
	for i in range( 0 , 3):
		rotXYZ[i] = ( rotXYZ[i] / ( 2 * 3.14 ) ) * 360

	
	return rotXYZ		


	
	
#__________________________________________________________________________________________________________________________________          get Position BBreel
	
def getPositionBBreel( _reelBBPoint ):


	baseA = _reelBBPoint[0] 	
	baseB = _reelBBPoint[1] 
	baseC = _reelBBPoint[2]
	baseD = _reelBBPoint[3]
	topA  = _reelBBPoint[4]
	topB  = _reelBBPoint[5]
	topC  = _reelBBPoint[6]
	topD  = _reelBBPoint[7]

	centreBBreel   = getBarycentre( baseA , baseB , baseC , baseD , topA , topB , topC , topD )		
	centreBaseABCD = getBarycentre( baseA , baseB , baseC , baseD )
	centreTopABCD  = getBarycentre( topA  , topB  , topC  , topD  )
	centreCoteA    = getBarycentre( baseA , baseB , topA  , topB  )
	centreCoteB    = getBarycentre( baseB , baseC , topB  , topC  )
	centreCoteC    = getBarycentre( baseC , baseD , topC  , topD  )
	centreCoteD    = getBarycentre( baseD , baseA , topD  , topA  )
	
	positions = [ centreBBreel , centreBaseABCD , centreTopABCD , centreCoteA , centreCoteB , centreCoteC , centreCoteD ]

	return positions     
            

#__________________________________________________________________________________________________________________________________          get Orientation BBreel

	
	
def getOrientationBBreel( _reelBBPoint ):
	
	baseB = _reelBBPoint[1]
	baseD = _reelBBPoint[3] 	
	baseC = _reelBBPoint[2]
	topC  = _reelBBPoint[6]


	vX = [  baseC[0] - baseD[0]  ,  baseC[1] - baseD[1]  ,  baseC[2] - baseD[2]  ]
	vY = [   topC[0] - baseC[0]  ,   topC[1] - baseC[1]  ,   topC[2] - baseC[2]  ]
	vZ = [  baseC[0] - baseB[0]  ,  baseC[1] - baseB[1]  ,  baseC[2] - baseB[2]  ]
	
	
	rotXYZ = convertTripleVecteurToEulerRot( vX  , vY , vZ )    
    
	return rotXYZ    
	
	
	
	
#__________________________________________________________________________________________________________________________________          get Scale BBreel	
	

	
def getScaleBBreel( rotBBCoords ):
	
	baseB = rotBBCoords[1]
	baseD = rotBBCoords[3] 	
	baseC = rotBBCoords[2]
	topC  = rotBBCoords[6]

	vX = om.MVector(  baseC[0] - baseD[0]  ,  baseC[1] - baseD[1]  ,  baseC[2] - baseD[2]   ).length()	
	vY = om.MVector(   topC[0] - baseC[0]  ,   topC[1] - baseC[1]  ,   topC[2] - baseC[2]   ).length()
	vZ = om.MVector(  baseC[0] - baseB[0]  ,  baseC[1] - baseB[1]  ,  baseC[2] - baseB[2]   ).length()
	
	return [ vX , vY , vZ ]	

#__________________________________________________________________________________________________________________________________          array 3by3 To Flat
		
def array_3by3ToFlat( arrays ):
	
	flattenList = []
	
	for array in arrays:
		for a in array:
			flattenList.append(a)
			
	return flattenList  
	
#__________________________________________________________________________________________________________________________________          array Flat To 3by3 


def array_flatTo3by3( flatArray ):	
	
	array3by3 = []
	tmp       = []	
	
	for e in flatArray:
		tmp.append( e )
		if( len( tmp ) == 3 ):
			array3by3.append( tmp )
			tmp = []

	return array3by3

#__________________________________________________________________________________________________________________________________          get mesh Coords	

	
def getmeshCoords( baseName , indexs ):

	
	allCoords   = getAllVertexCoords( baseName )
	coords      = getIndexVertexCoords( allCoords , indexs )
	coords      = array_3by3ToFlat( coords)	
	
	
	return coords	
	
	
#=================================================================================================================================================================================
#===========================================================================================================================                 MAIN PROC                     =======
#=================================================================================================================================================================================
	



#__________________________________________________________________________________________________________________________________          get Coords To Process	


def getCoordsToProcess( selection ):

	coordsToProcess = []
	
	indexs          = []	
	mode            = createLoc_modeSelection( selection ) 

	
	if( mode == 0 ):
		coordsToProcess = []
							
	if( mode == 1 ):
		for elem in selection:
			coordsToProcess    =   getmeshCoords( elem , indexs )

			

	if( mode == 2 ) or ( mode == 3 ):
		
		baseName     = getComponentBaseNames( selection )		
		selectionVtx = convertTovtx( selection )
		indexs       = getComponentIndex( selectionVtx )

		
		if( len( indexs ) == 1 ):
			
			extraComponents = growSelection( selection[0] )
			selectionVtx    = convertTovtx( extraComponents) 
			indexs          = getComponentIndex( selectionVtx )	
			
			coordsToProcess     = getmeshCoords( baseName , indexs )


						
		elif( len( indexs ) == 2 ):
			
			coordsA = pivotObj( baseName + '.vtx[%r]' %( indexs[0] )  )
			coordsB = pivotObj( baseName + '.vtx[%r]' %( indexs[1] )  )	
			
			pos = getBarycentre( coordsA , coordsB  )
			p2Vectors = getaxe2Coords( coordsA , coordsB )		
			p2Orient = convertTripleVecteurToEulerRot( p2Vectors[0] , p2Vectors[1] , p2Vectors[2] ) 
			
			coordsToProcess     = getmeshCoords( baseName , indexs )
							
		else:
			
			coordsToProcess     = getmeshCoords( baseName , indexs )
       
		
	#if( mode == 3 ):	
	#if( mode == 4 ):	
		

	return coordsToProcess 
	






def getCoordsToProcess_02( obj , indexs ):

	coordsToProcess = []
	
	indexs          = []	
	mode            = createLoc_modeSelection( selection ) 

	
	if( obj == '' ) and ( indexs == [] ):
		return []
							
	if( obj == '' ) and ( indexs == [] ):
		return getmeshCoords( elem , indexs )

			

	if( mode == 2 ) or ( mode == 3 ):
		
		baseName     = getComponentBaseNames( selection )		
		selectionVtx = convertTovtx( selection )
		indexs       = getComponentIndex( selectionVtx )

		
		if( len( indexs ) == 1 ):
			
			extraComponents = growSelection( selection[0] )
			selectionVtx    = convertTovtx( extraComponents) 
			indexs          = getComponentIndex( selectionVtx )	
			
			coordsToProcess     = getmeshCoords( baseName , indexs )


						
		elif( len( indexs ) == 2 ):
			
			coordsA = pivotObj( baseName + '.vtx[%r]' %( indexs[0] )  )
			coordsB = pivotObj( baseName + '.vtx[%r]' %( indexs[1] )  )	
			
			pos = getBarycentre( coordsA , coordsB  )
			p2Vectors = getaxe2Coords( coordsA , coordsB )		
			p2Orient = convertTripleVecteurToEulerRot( p2Vectors[0] , p2Vectors[1] , p2Vectors[2] ) 
			
			coordsToProcess     = getmeshCoords( baseName , indexs )
							
		else:
			
			coordsToProcess     = getmeshCoords( baseName , indexs )
       
		
	#if( mode == 3 ):	
	#if( mode == 4 ):	
		

	return coordsToProcess 





	
#__________________________________________________________________________________________________________________________________          get RotatedBBCoords	

def getRotatedBBCoords( coords ):
	
	rotBBCoords = mc.MC_getRotatedBBCoordsCmd( coords )

	rotBBCoords = array_flatTo3by3( rotBBCoords )
	
	return rotBBCoords	
	
	
#__________________________________________________________________________________________________________________________________          get TRSValue From RotBBCoords


def getTRSValueFromRotBBCoords( rotBBCoords , position  ):
	
	
	rotation    = getOrientationBBreel(rotBBCoords)
	scale       = getScaleBBreel(rotBBCoords)		
	positions   = getPositionBBreel(rotBBCoords) 	


	return [ positions[position][0] , positions[position][1] , positions[position][2] , rotation[0] , rotation[1] , rotation[2] , scale[0] , scale[1] , scale[2] ] 			
			

	
	
	
	
	
	
	
	
		
#_________________________________________________________________________________________________________________________________________________________________________  getBBCoordRef			
		
		
		
def getBBCoordRef(  obj , indexs , autoPosition , autoOrient , autoScale ):
	

	manipPiv    =   manipsUtils.findPivot( obj )

	if( manipsUtils.isMesh( obj ) == 1 ):
		coordsToProcess = getmeshCoords( obj , indexs )	
		
	elif( manipsUtils.isGroupMesh( obj ) == 1 ):		
		allMshinGrp = manipsUtils.getAllChildrenMsh( obj )
		coordsToProcess = []
		for msh in allMshinGrp:
			coordsToProcess += getmeshCoords( msh , indexs )
	else:
		autoPosition = 0 
		autoOrient   = 0			
		autoScale    = 0				

		
	if( autoOrient == 1 ): 
		
		rotBBCoords     = getRotatedBBCoords( coordsToProcess )
				
		if( autoPosition == 0 ):
			
			baryCentre  = manipsUtils.getBarycentre( rotBBCoords )				
			diff        = [ manipPiv[0] - baryCentre[0] , manipPiv[1] - baryCentre[1] , manipPiv[2] - baryCentre[2]   ]				
			rotBBCoords = manipsUtils.transformCoords( rotBBCoords ,  [ 0 , 0 , 0 ]  , [ diff[0] , diff[1] , diff[2] , 0 , 0 , 0 , 1 , 1 , 1 ] , 'XYZ'  )
		
		if( autoScale == 0 ):				
			rotBBCoords = resetScale( rotBBCoords )

	else:

		position = manipPiv
		scale = [ 1 , 1 , 1 ]
		
		if( autoPosition == 1 ) or ( len(indexs) > 0 ):			
			position     = manipsUtils.getBBbarycentre( coordsToProcess )
			
		if( autoScale == 1 ): 				
			scale       = manipsUtils.getBBscale( coordsToProcess )

		rotBBCoords     = manipsUtils.getCubeCoords(  [ position[0] , position[1] , position[2] , 0 , 0 , 0 , scale[0] , scale[1] , scale[2] ]   )		

		
	return rotBBCoords			
		
						
	
	
	
#_______________________________________________________________________________________________________________________________________________________________________________  reset Scale

			
def resetScale( coords ):
	
	offset = getTRSValueFromRotBBCoords( coords , 0 )
	cubeCoords = manipsUtils.getCubeCoords( [ offset[0] , offset[1] , offset[2] , offset[3] , offset[4] , offset[5] , 1 , 1 , 1 ]  )		
		
	return cubeCoords 				

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
'''



import sys

sys.path.append( '/u/mcantat/Sandbox/script/toolBox/autoManips/' )

exec('import rotateBB_getOrientPosition') in globals()
exec('reload (rotateBB_getOrientPosition)') in globals()
import rotateBB_getOrientPosition as rBB

coordsToProcess = rBB.getCoordsToProcess( ['pCube1']  )

rotBBCoords     = rBB.getRotatedBBCoords( coordsToProcess )	

posRotScale = rBB.getTRSValueFromRotBBCoords( rotBBCoords , 0 )

'''



	
	
	
	