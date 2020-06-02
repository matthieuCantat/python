
import maya.OpenMayaMPx as ommpx
import maya.OpenMaya as om
import math
import time
import copy



#######################################################################################################	
########################################  procs   #####################################################
#######################################################################################################


#-------------------------------------------------------------------------------------------------- getBoundingBox




def getBoundingBox( _vertexCoords ):
	
	x , y , z = [] , [] , []
	
	for coord in _vertexCoords:
		x.append( coord[0] )
		y.append( coord[1] )		
		z.append( coord[2] )
		
	x.sort()		
	y.sort()		
	z.sort()	

	minMaxCoords = [ x[0] , y[0] , z[0] , x[-1] , y[-1] , z[-1] ]

	return minMaxCoords



def getBoundingBox2D( _vertexCoords ):
	
	x , y  = [] , [] 
	
	for coord in _vertexCoords:
		x.append( coord[0] )
		y.append( coord[1] )		
		
	x.sort()		
	y.sort()		

	minMaxCoords = [ x[0] , y[0]  , x[-1] , y[-1]  ]

	return minMaxCoords


		
	
	
#-------------------------------------------------------------------------------------------------- rotateAllVertex	
		


def rotateAllVertex( _vertexCoords , _pivotCoords , axe , _rotValue ):
 
    # find Index list
	
	dicoAxe  = { 'X' : [ 1 , 2 , 0 ]  ,  'Y' : [ 0 , 2 , 1 ]   ,  'Z' : [ 0 , 1 , 2 ] }	
	i = dicoAxe[ axe ]
	
	if( axe == 'Y' ):
		_rotValue *= -1    

    # calcule Rot
    
	rotRad = math.radians(_rotValue)
	
	newVertexCoords = []
	
	for coord in _vertexCoords:
		
		newCoord = [ 0 , 0 , 0 ]
		
		newCoord[ i[0] ] = math.cos( rotRad ) * ( coord[i[0]] - _pivotCoords[i[0]] )     -     math.sin( rotRad ) * ( coord[i[1]] - _pivotCoords[i[1]] )     +     _pivotCoords[i[0]]        
		newCoord[ i[1] ] = math.sin( rotRad ) * ( coord[i[0]] - _pivotCoords[i[0]] )     +     math.cos( rotRad ) * ( coord[i[1]] - _pivotCoords[i[1]] )     +     _pivotCoords[i[1]]              
		newCoord[ i[2] ] = coord[i[2]] 
		    
		newVertexCoords.append( newCoord )
		
		    
	return newVertexCoords



def rotateAllVertex2D( _vertexCoords , _pivotCoords , axe , _rotValue ):
 
	if( axe == 'Y' ):
		_rotValue *= -1    
		
	# calcule Rot		
		
	rotRad = math.radians(_rotValue)
	
	newVertexCoords = []
	
	for coord in _vertexCoords:
		
		newCoord = [ 0 , 0 ]
		
		newCoord[ 0 ] = math.cos( rotRad ) * ( coord[0] - _pivotCoords[0] )     -     math.sin( rotRad ) * ( coord[1] - _pivotCoords[1] )     +     _pivotCoords[0]        
		newCoord[ 1 ] = math.sin( rotRad ) * ( coord[0] - _pivotCoords[0] )     +     math.cos( rotRad ) * ( coord[1] - _pivotCoords[1] )     +     _pivotCoords[1]              
		    
		newVertexCoords.append( newCoord )
		
		    
	return newVertexCoords



#-------------------------------------------------------------------------------------------------- getLengthDiagoBB

    
def getLengthDiagoBB( _bbCoords, axe ):
	
	dicoAxe  = { 'X' : [ 0 , 1 , 1 ]   ,  'Y' : [ 1 , 0 , 1 ]   ,  'Z' : [ 1 , 1 , 0 ] }	
	skipAxes = dicoAxe[ axe ]
	
	
	bbMin = [ _bbCoords[0] , _bbCoords[1] , _bbCoords[2] ]    
	bbMax = [ _bbCoords[3] , _bbCoords[4] , _bbCoords[5] ]
	
	bbDiagLength = om.MVector( (bbMax[0] - bbMin[0]) * skipAxes[0]  , (bbMax[1] - bbMin[1]) * skipAxes[1] , (bbMax[2] - bbMin[2]) * skipAxes[2] ).length()   
	  
	return bbDiagLength   
    

def getLengthDiagoBB2D( _bbCoords ):
	
	
	bbMin = [ _bbCoords[0] , _bbCoords[1]  ]    
	bbMax = [ _bbCoords[2] , _bbCoords[3]  ]

	vDiag = [ ( bbMax[0] - bbMin[0] ) , ( bbMax[1] - bbMin[1] ) ] 
	diagLength =  distance2D( vDiag )
	  
	return diagLength   

	
#-------------------------------------------------------------------------------------------------- getRapportSidesBB	


def getRapportSidesBB( _bbCoords , axe ):

		
	x = _bbCoords[3] - _bbCoords[0]     
	y = _bbCoords[4] - _bbCoords[1]  
	z = _bbCoords[5] - _bbCoords[2]    
	
	
	if( axe == "X" ):
	 	if( y < z ):
	 		diffSides = y / z
	 	else:	
	 		diffSides = z / y
	    
	elif( axe == "Y" ):
	 	if( x < z ):
	 		diffSides = x / z
	 	else:	
	 		diffSides = z / x
	  	
	elif( axe == "Z" ):
	    if( x < y ):
	    	diffSides = x / y
	    else:	
	    	diffSides = y / x
	
		    	
		  
	return diffSides       
    



def getRapportSidesBB2D( _bbCoords ):
		
	x = _bbCoords[2] - _bbCoords[0]     
	y = _bbCoords[3] - _bbCoords[1]  

	if( x < y ):
		diffSides = x / y
	else:	
		diffSides = y / x
	    
	return diffSides       
    


    
#-------------------------------------------------------------------------------------------------- getMaxAngleCoord	

		
		
		
def getMaxAngleCoord_2( coords , coordOrigine , coordRef , skipCoords ):


	# get for each vertex angle et distances
	
	newCoord = [0,0]
	angles = []
	anglesSorted = []
	
	vecteurRef = [ coordRef[0] - coordOrigine[0] , coordRef[1] - coordOrigine[1] ]

	for coord in coords:
		vecteurTest = [ (coord[0] - coordOrigine[0] ) , ( coord[1] - coordOrigine[1] ) ]

		if(  distance2D(vecteurTest) == 0  ):
			angle = 0
		else:		
			angle = angle2D( vecteurRef , vecteurTest ) 

		angles.append( angle )
		anglesSorted.append( angle )

	# get max angle(s)
	
	anglesSorted.sort()
	anglesSorted.reverse()
	
	
	angleMax = anglesSorted[0] 
	
	# get max angle / min dist coords
	dico = {}
	distances = []
	
	for i in range( 0 , len(coords) ):
		if( angles[i] == angleMax ):
			vecteurTest = [ ( coords[i][0] - coordOrigine[0] ) , ( coords[i][1] - coordOrigine[1] ) ]
			distance = distance2D(vecteurTest)
			distances.append( distance )
			dico[distance] = coords[i]
			
	distances.sort()
	newCoord = dico[ distances[-1] ]
	


	if ( newCoord in skipCoords ):
		return 0
	else:
		return newCoord 
		

		
		
#-------------------------------------------------------------------------------------------------- getVertexSilhouette_3	




def getVertexSilhouette_4( coords ):
	

		
	# get pivot coords

	distances = []
	vCoords = []
	
	bbCoords =  getBoundingBox2D( coords )
	pivCoords = getBarycentreBBcoords2D( bbCoords )

		
	#find farest point

	dico = {}
	distances = []
	farestCoord = []
	
	for coord in coords:
		distance = distance2D( [ coord[0] - pivCoords[0] , coord[1] - pivCoords[1] ] ) 
		distances.append( distance )
		dico[distance] = coord 
				
	distances.sort()
	distances.reverse()
	
	farestCoord = dico[distances[0]]

	
	#find silhouetteCoords

	silhouetteCoords = []

	coordO = farestCoord
	coordRef = pivCoords
	skipCoords = [coordO]
	newCoord = [0,0]
	
	lap = 0

	
	while not( newCoord  == 0 ):
		
		newCoord = getMaxAngleCoord_2( coords , coordO , coordRef , skipCoords  )

		if not(newCoord == 0):

			skipCoords.append(newCoord)
			coordRef = coordO
			coordO = newCoord




	silhouetteCoords = skipCoords
	

	return silhouetteCoords	



	

#-------------------------------------------------------------------------------------------------- findSameElemIndex		
	
	
def findSameElemIndex( elems ):

	indexs = range( 0 , len(elems) )

	sameIndexSort = []	
		
	while not ( len( indexs ) == 0 ):
		
		lap = 0
		sameIndex = []
		
		for i in indexs:
			
			if( lap == 0):
				ref = elems[i]
				
			if( elems[i] == ref):
				sameIndex.append(i)

				
			lap += 1
							
		
		sameIndexSort.append( sameIndex )
		
		for i in sameIndex:
			indexs.remove( i )
		
	return sameIndexSort

	
	
#-------------------------------------------------------------------------------------------------- findnonRoundCoef		


				
		

def findnonRoundCoef_2( coords):

	
	# find all vector
	
	vectors = []
	
	vectors.append(   [ ( coords[-1][0] - coords[0][0] ) , ( coords[-1][1] - coords[0][1] ) ]    )
		
	for i in range( 0 , len(coords)  ):
		vectors.append(   [ ( coords[i][0] - coords[ i-1 ][0] ) , ( coords[i][1] - coords[ i-1 ][1] ) ]    )		
	# find Perimetre
	
	perimetre = 0.0	
	
	
	for vector in vectors:	
		perimetre += distance2D(vector)	
	
	# vectorRef

	vectorRefA = [ 1 , 0 ] 	
	vectorRefB = [ 0 , 1 ] 
	
	# find angle
	
	angles = []
	
	for vector in vectors:
		if( vector == [0,0] ):
			vector = [ 0,000000001 , 0]		
		angleA = round( angle2D( vector , vectorRefA ) , 4 )			
		angleB = round( angle2D( vector , vectorRefB ) , 4 )			
		angles.append( [angleA , angleB] )
		
	# add vector distance for the same angle	
		
	sameElemIndexs = findSameElemIndex(angles)
	distances = []
	
	
	for sameElemIndex in sameElemIndexs :
		
		distance = 0
		
		for i in sameElemIndex:
			distance += distance2D(vectors[i])

		distances.append( distance )	
	
	distances.sort()	
	distances.reverse()
	
	coef = distances[0] / perimetre
	
	
	return coef 
	
				
			
	
			
		
#-------------------------------------------------------------------------------------------------- getAxeToCalculeLocalBB_3		 	
	 	




def getAxeToCalculeLocalBB_4( _coords ,_bbcoords , skipAxes ):

   
        #le calcule de la reelBB se fait axe par axe.
        #On peut avoir des resultats differents selon l'ordre des axe dans le calcule
        
        
        #le meilleur ordre, c'est de partir de l axe ou la BB de l'objet est le moins carre au plus carre.( plus grand rapport au plus petit ) 
   
    axeOrder = []
    
    worldAxes = [ 'X' , 'Y' , 'Z' ]
    alldiff = []
    
    for a in worldAxes :   	
		if( a in skipAxes ):
			alldiff.append( -1234 )
			continue    		
		
		coord2D = convertTo2D( _coords , a  )
		coordSilhouetteMesh = getVertexSilhouette_4( coord2D  ) 
		diffAire =  findnonRoundCoef_2( coordSilhouetteMesh )
		alldiff.append(diffAire)
    	

    alldiffSorted = copy.copy(alldiff)	
    alldiffSorted.sort()
    alldiffSorted.reverse()

    
  
    for i in range(0 , 3 )  :
 
        if( alldiffSorted[i] == -1234 ):
        	continue
 
        elif( alldiffSorted[i] == alldiff[0]  ):
            axeOrder.append( "X" )

        elif( alldiffSorted[i] == alldiff[1]  ):
            axeOrder.append( "Y" )

        elif( alldiffSorted[i] == alldiff[2]  ):
            axeOrder.append( "Z" )      
 
    return axeOrder[0]	

	 	


	 	
#-------------------------------------------------------------------------------------------------- convertBBcoordsToCubePoints			 
	
def convertBBcoordsToCubePoints( _bbCoords ):
    
    baseA = [ _bbCoords[0] , _bbCoords[1] , _bbCoords[2] ]
    baseB = [ _bbCoords[3] , _bbCoords[1] , _bbCoords[2] ]    
    baseC = [ _bbCoords[3] , _bbCoords[1] , _bbCoords[5] ]        
    baseD = [ _bbCoords[0] , _bbCoords[1] , _bbCoords[5] ]            
                                                      
    topA  = [ _bbCoords[0] , _bbCoords[4] , _bbCoords[2] ]    
    topB  = [ _bbCoords[3] , _bbCoords[4] , _bbCoords[2] ]        
    topC  = [ _bbCoords[3] , _bbCoords[4] , _bbCoords[5] ]    
    topD  = [ _bbCoords[0] , _bbCoords[4] , _bbCoords[5] ]    

    cubePoints  = [ baseA , baseB , baseC , baseD , topA , topB , topC , topD ]     
    
    return cubePoints
    
    
#-------------------------------------------------------------------------------------------------- getBarycentre	 

def getBarycentre( points ):
	

    sizePoints = len( points )    
    bCoords = [ 0.0 , 0.0 , 0.0 ]
    
    for point in points:
        bCoords[0] += point[0]
        bCoords[1] += point[1]
        bCoords[2] += point[2]

    bCoords = [ bCoords[0] / sizePoints , bCoords[1] / sizePoints , bCoords[2] / sizePoints  ]

    return bCoords
	    
    
    
#-------------------------------------------------------------------------------------------------- getBarycentreBBcoords	   
    
def getBarycentreBBcoords( _bbCoords ):
	
	pivCoords = [ 0 , 0 , 0 ]
	
	pivCoords[0] = ( _bbCoords[0] + _bbCoords[3] )/2
	pivCoords[1] = ( _bbCoords[1] + _bbCoords[4] )/2	
	pivCoords[2] = ( _bbCoords[2] + _bbCoords[5] )/2
	
	return pivCoords

    
def getBarycentreBBcoords2D( _bbCoords ):
	
	pivCoords = [ 0 , 0 ]
	
	pivCoords[0] = ( _bbCoords[0] + _bbCoords[2] )/2
	pivCoords[1] = ( _bbCoords[1] + _bbCoords[3] )/2	

	
	return pivCoords


    
 #-------------------------------------------------------------------------------------------------- getCircleAxes	
		
def getCircleAxes( _coords , _pivCoords ):

	circleAxes = []
	axes = [ 'X' , 'Y' , 'Z' ]
	
	rotValue = 0 
	incr = 20 
	target = 360  

	for axe in axes :
		
		diff = 0.01	
		
		bbCoords = getBoundingBox( _coords )	
		oldDiag = getLengthDiagoBB(  bbCoords  , axe ) + getRapportSidesBB(  bbCoords  , axe )  
		diagRef = oldDiag
		diag = oldDiag  
		i = 0	
		
		
		while( abs( oldDiag - diag ) < ( diff * diagRef ) ):
		
			oldDiag = diag
			rotValue = i
			
			rotCoords = rotateAllVertex( _coords , _pivCoords , axe ,  rotValue  ) 
			bbCoords = getBoundingBox( rotCoords )  
			diag = getLengthDiagoBB(  bbCoords  , axe ) + getRapportSidesBB(  bbCoords  , axe )  

			       		       
			i += incr       
			if( i > target ):
				circleAxes.append(axe)
				diff = 0

	
	return circleAxes     
		
	

 #-------------------------------------------------------------------------------------------------- getRotValueReelBB		
	

	
	

def getRotValueReelBB_2( _coords , _pivCoords , axe ):
    
	rotValue = 0   
	rotIncr = 22.5          # 22.5 
	rotIncrTarget = 0.1      #0.1
	divideByLap = 2

	i = 1
	loop = 0	

	coord2D = convertTo2D( _coords , axe  )
	
	bbCoords = getBoundingBox2D( coord2D )
	oldValue = getLengthDiagoBB2D( bbCoords ) + getRapportSidesBB2D( bbCoords ) 
		
	doPosIncr = 1
	doNegIncr = 1	
	
	while( rotIncr > rotIncrTarget ):
	    
		
		if( doPosIncr ):
		
			# + Rot         
			rotCoords = rotateAllVertex2D( coord2D , _pivCoords , axe , ( rotValue + rotIncr) ) 				
			bbCoords = getBoundingBox2D( rotCoords )		
			posValue = getLengthDiagoBB2D( bbCoords ) + getRapportSidesBB2D( bbCoords )  
      
		if( doNegIncr ):	

			# - Rot        
			rotCoords = rotateAllVertex2D( coord2D , _pivCoords , axe , ( rotValue - rotIncr) )			
			bbCoords = getBoundingBox2D( rotCoords )			
			negValue = getLengthDiagoBB2D( bbCoords ) + getRapportSidesBB2D( bbCoords )  

		
		
		doPosIncr = 1
		doNegIncr = 1		
		
		# result
		     
		if( posValue < negValue ):
			rotValue += rotIncr			
			if( oldValue < posValue):
				doPosIncr = 0
			
			oldValue = posValue
		else:
			rotValue -= rotIncr 			
			if( oldValue < negValue):				
				doNegIncr = 0	
				
			oldValue = negValue
				
				 

		rotIncr = rotIncr / divideByLap
			
		#garde fou	
		i += 1				 
		if( i > 100 ):
			error("LOOP")

	return rotValue



	
	
	
	
	
	
def distance2D( vecteurA ):
	
	distance = math.sqrt( math.pow( vecteurA[0] , 2 ) + math.pow( vecteurA[1] , 2 )  )
	
	return distance


def angle2D( vecteurA , vecteurB ):
	
	pi = 3.14159
	
	distA = math.sqrt( math.pow( vecteurA[0] , 2 ) + math.pow( vecteurA[1] , 2 ) ) 
	distB = math.sqrt( math.pow( vecteurB[0] , 2 ) + math.pow( vecteurB[1] , 2 ) )
	 
	
	produitScalaire =  vecteurA[0] * vecteurB[0] + vecteurA[1] * vecteurB[1]  
	
	firstOp =  produitScalaire / ( distA * distB )
	
	if( 1 < firstOp ):
		firstOp = 1
	
	if( firstOp < -1 ):
		firstOp = -1
		
	angleV = math.acos( firstOp ) * 360 / (pi * 2)
	
	return angleV

	
def convertTo2D( coords , axe ):
	
	coords2D = []

	dicoAxe  = { 'X' : [ 1 , 2 ]   ,  'Y' : [ 0 , 2 ]   ,  'Z' : [ 0 , 1 ] }	
	iAxes = dicoAxe[ axe ]	
	
	for coord in coords:
		coords2D.append( [ coord[ iAxes[0] ] , coord[ iAxes[1] ] ] )
	
	
	return coords2D 
	
	

	
#######################################################################################################	
########################################  COMPUTE   ###################################################
#######################################################################################################



	
	
def getLocalBB( coords ):
	
	
	
	
	#findPivot

	bbCoords  = getBoundingBox( coords )
	pivCoords = getBarycentreBBcoords( bbCoords )     

	
	#getAllRotations + Coord Non Orient

	nbrLap = 4  #4
	
	axeOrder = []
	allRot   = []
	skipAxe  = []
	

	for i in range( 0 , nbrLap ):
		
		if( len( skipAxe ) == 3 ):
			skipAxe = []
			

		bbCoords = getBoundingBox( coords )	
		axe      = getAxeToCalculeLocalBB_4( coords, bbCoords , skipAxe )
		rot      = getRotValueReelBB_2( coords , pivCoords , axe ) 		
		coords   = rotateAllVertex( coords , pivCoords , axe , rot )
			
		
		skipAxe.append(  axe )
		axeOrder.append( axe )		
		allRot.append(   rot )
	

	

	
	#find CoordsBB Non Orient		
	
	bbcoordsRot = getBoundingBox( coords )	
	pointCube =  convertBBcoordsToCubePoints( bbcoordsRot )
	
	

	

	#find Coords BB Orient (orientBB)	
	
	allRot.reverse()
	axeOrder.reverse()

	for i in range( 0 , nbrLap ):
		pointCube = rotateAllVertex( pointCube , pivCoords , axeOrder[i] , ( allRot[i] * -1 ) )

	
	
		
	#findAxisOriented ------------------------------------------
	
	axis = [ 'X' , 'Y' , 'Z' ]
	dicoVectorAxis = { 'X' : om.MVector( 1 , 0 , 0 ) , 'Y' : om.MVector( 0 , 1 , 0 ) , 'Z' : om.MVector( 0 , 0 , 1) }	
	dicoVectorAxisOrient = {}
	
	for axe in axis:
		vecteur = dicoVectorAxis[ axe ] 
		for i in range( 0 , nbrLap ):
			angle = om.MQuaternion( math.radians( allRot[i] * -1 )  , dicoVectorAxis[ axeOrder[i] ] )
			vecteur = vecteur.rotateBy( angle )
		
		dicoVectorAxisOrient[ axe ] =  vecteur 	


	#findCircleAxe
	
	circleAxes = []

	circleAxes = getCircleAxes( coords , pivCoords )

		
	#reset circle Axe
	
	eulerCoordsToReset = []
	pivCoords = getBarycentre( pointCube )
	
	for i in range( 0 , nbrLap ):
		if( axeOrder[i] in circleAxes ):
			angleQuat = om.MQuaternion( math.radians( allRot[i] )   , dicoVectorAxisOrient[ axeOrder[i] ] )   
			angleEuler = angleQuat.asEulerRotation()
			eulerRot = [ math.degrees(angleEuler.x) , math.degrees(angleEuler.y) , math.degrees(angleEuler.z) ]
		
			for i in range( 0 , 3 ):
				pointCube = rotateAllVertex( pointCube , pivCoords , axis[i] , eulerRot[i] )	
				
	


	return pointCube



#######################################################################################################	
########################################  CLASS   ###################################################
#######################################################################################################
			


class MC_getRotatedBBCoordsCmd(ommpx.MPxCommand):
	
	'''
	argument doit etre une liste double simple 
	
	'''


	kPluginCmdName = 'MC_getRotatedBBCoordsCmd'
	
	
	
	def __init__(self):
		ommpx.MPxCommand.__init__(self)

		
	

		
		
		
	def doIt(self, args):
		
		# get array in args
		
		mArray = om.MDoubleArray()		
		util = om.MScriptUtil()		
		
		util.createFromInt(0)
		pInt = util.asUintPtr()		
		mArray  = args.asDoubleArray( pInt )

		# get coords in args	
		
		coords = []
		pCoords = []
		
		for i in range( 0 , mArray.length() ):
			pCoords.append( mArray[i] )
			
			if( len( pCoords ) == 3 ):
				coords.append( pCoords )
				pCoords = []

				
		# compute
		
		resultArray = om.MDoubleArray()	 
		
		rotatedBBCoords = getLocalBB( coords ) 

		for i in range( 0 , len( rotatedBBCoords ) ):
			for j in range(0 , len( rotatedBBCoords[i] ) ):
				resultArray.append( rotatedBBCoords[i][j] )
				
			

			
		self.setResult( resultArray )
		
	
	@classmethod
	def cmdCreator(cls):
		return ommpx.asMPxPtr(cls())


		

   
    
		
		
		
		

		
def initializePlugin(obj):
	plugin = ommpx.MFnPlugin( obj , 'matthieuCantat' , '1.0' , 'Any' )

	try:
		plugin.registerCommand( MC_getRotatedBBCoordsCmd.kPluginCmdName , MC_getRotatedBBCoordsCmd.cmdCreator   )
		
	except:
		raise Exception( 'Failed to register command ' )




def uninitializePlugin(obj):
	
	plugin = ommpx.MFnPlugin( obj , 'matthieuCantat' , '1.0' , 'Any' )

	try:
		plugin.deregisterCommand( MC_getRotatedBBCoordsCmd.kPluginCmdName  )
		
	except:
		raise Exception( 'Failed to deregister command ' )



