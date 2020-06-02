
import math

import maya.cmds as mc
import maya.OpenMaya as om
import maya.api.OpenMaya as ompy

from ..utils import utilsMaya
from ..utils import utilsPython
from ..utils import utilsMath
from ..utils import utilsMayaApi

from . import trs
from . import coords

class boundingBox2d(mayaClasse):
	
	'''
	#_________________________________________________________________ATTRS
	ratio
	area
	#_________________________________________________________________CREATE
	createFromCoords
	createFromBoundingBoxCoords
	createFromPositionDimention
	createFromSquareCoords
	createFromPositionVector
	createFromPositionAngleDistance
	#_________________________________________________________________MODIF
	grow( incr , boundingBoxsToAvoid , boundingBoxToStayInside )
	#_________________________________________________________________OUT
	isIn( boundingBox2d )
	isOut( boundingBox2d )	
	divide()
	isValide
	#_________________________________________________________________UTILS
	'''

	def __init__(self):

		self.vX = om.MVector( 1 , 0 , 0 )
		self.vY = om.MVector( 1 , 1 , 0 )

		self.ratio = 0
		self.area = 0
		self.width = 1 
		self.heigth = 1		
		self.squareCoords       = [ 0,0 , 0,1 , 1,1 , 1,0 ]	
		self.squareMiddleCoords = [ 0,0  , 0,0.5 , 0,1 , 0.5,1 , 1,1 , 1,0.5 , 1,0 , 0.5,0 ]			
		self.boundingBoxCoords  = [ 0,0 , 1,1 ]	

		self.pointVector  = [ 0,0 , 1,1 ]
		self.pointAngleDistance  = [ 0,0 , 315 , math.sqrt(2) ]		

		self.debug = 0

	#_________________________________________________________________CREATE
	def createFromObj( self , obj , bbOrigineIndex = None ):
		bbCoords = mc.xform( obj , q = True , boundingBox = True)
		boundingBoxCoords2d = [ bbCoords[2] , bbCoords[1] , bbCoords[5] , bbCoords[4] ]
		self.createFromBoundingBoxCoords( boundingBoxCoords2d , bbOrigineIndex )

	def createFromCoords( self , coords , bbOrigineIndex = None ):
		boundingBoxCoords = self.utils_getBoundingBoxCoords( coords , 2 )
		self.createFromBoundingBoxCoords( boundingBoxCoords , bbOrigineIndex )

	def createFromBoundingBoxCoords( self , boundingBoxCoords , bbOrigineIndex = None ):
		bb = boundingBoxCoords
		self.boundingBoxCoords = bb	
		self.squareCoords = [ bb[0],bb[1] , bb[0],bb[3] , bb[2],bb[3] , bb[2],bb[1]  ]
		self.squareMiddleCoords = [ bb[0],bb[1] , bb[0],(bb[1]+bb[3])/2 , bb[0],bb[3] , (bb[0]+bb[2])/2,bb[3] , bb[2],bb[3] , bb[2],(bb[1]+bb[3])/2 , bb[2],bb[1] , (bb[2]+bb[0])/2,bb[1]  ]	
		self.width = bb[2]-bb[0] 
		self.heigth = bb[3]-bb[1] 				
		self.area = self.width * self.heigth
		self.ratio = None
		if not( self.area == 0 ):
			self.ratio = self.width / self.heigth	

		squareCoordsTmp = self.squareCoords + self.squareCoords[0:4]
		if not ( bbOrigineIndex == None ):
			#GET POINT VECTOR			
			bbOrigineCoords   = [ squareCoordsTmp[bbOrigineIndex*2] , squareCoordsTmp[bbOrigineIndex*2+1] ]
			bbDirCoords       = [ squareCoordsTmp[bbOrigineIndex*2+4] , squareCoordsTmp[bbOrigineIndex*2+1+4] ]
			self.pointVector  =  bbOrigineCoords + [ bbDirCoords[0]-bbOrigineCoords[0] , bbDirCoords[1]-bbOrigineCoords[1] ]		
			#GET POINT ANGLE DISTANCE
			self.pointAngleDistance  = self.pointVector[0:2] + self.vectorToAngleDistance(self.pointVector[2:4])	


	def createFromSquareCoords( self , squareCoords , bbOrigineIndex = None ):
		boundingBoxCoords = self.utils_getBoundingBoxCoords( squareCoords , 2 )
		self.createFromBoundingBoxCoords( boundingBoxCoords , bbOrigineIndex )


	def createFromPointVector( self , pointVector ):
		#GET ATTR	
		coords = pointVector[0:2] + [ pointVector[0] + pointVector[2] , pointVector[1] + pointVector[3] ]
		boundingBoxCoords = self.utils_getBoundingBoxCoords( coords , 2 )			
		self.createFromBoundingBoxCoords( boundingBoxCoords )
		#GET pointAngleDistance
		self.pointVector = pointVector
		self.pointAngleDistance = pointVector[0:2] + self.vectorToAngleDistance( pointVector[2:4] )


	def createFromPointAngleDistance( self , pointAngleDistance ):
		#GET ATTR				
		vectorBase = [ self.vX.x , self.vX.y  ]
		vectorRotated = [ math.cos( math.radians(pointAngleDistance[2]) ) , math.sin( math.radians(pointAngleDistance[2]) ) ]	
		vectorDistance = [ vectorRotated[0] * pointAngleDistance[3] ,  vectorRotated[1] * pointAngleDistance[3]  ]	
		self.createFromPointVector( pointAngleDistance[0:2] + vectorDistance )


	
	#_________________________________________________________________MODIF
	def grow( self , incr , blockBoundingBox2ds , canvasBoundingBox2ds , keepRatio = 0 ):	
		iterLimit      = 100
		iterActual     = 0
		stop           = 0
		collision      = 0

		vectorIncr = self.utils_resizeVector( self.pointVector[2:4] , incr )
		oldArea = self.area		
		if( self.debug == 1 ):
			print( 'collision' , collision )
			self.visualize('grow {}'.format(iterActual) )

		while( stop == 0 ):
			pointVectorStart = self.pointVector[:]
			#self.printAttrs('grow {}'.format(iterActual) )
			self.pointVector[2] += vectorIncr[0]	
			self.pointVector[3] += vectorIncr[1]						
			self.createFromPointVector( self.pointVector )

			for bbBlock in blockBoundingBox2ds:
				if( self.isIn(bbBlock) ):
					cornerPoint = [ self.pointVector[0] + self.pointVector[2] , self.pointVector[1] + self.pointVector[3] ]	
					#GET AXE INDEX COLLISION
					collideEdge  = self.getCollideEdge( bbBlock , vectorIncr )
					vEdge = [ collideEdge[2] - collideEdge[0] , collideEdge[3] - collideEdge[1] ]
					if( abs(vEdge[0]) < abs(vEdge[1]) ): vectorIncr[0] = 0
					else:                                vectorIncr[1] = 0					
					#GET CLOSEST POINT
					cornerPoint = [ self.pointVector[0] + self.pointVector[2] , self.pointVector[1] + self.pointVector[3] ]
					closestPoints = self.utils_getClosestPointOnLine( cornerPoint , collideEdge )
					self.pointVector = self.pointVector[0:2] + [ closestPoints[0] - self.pointVector[0] ,  closestPoints[1] - self.pointVector[1] ]
					self.createFromPointVector( self.pointVector )												
									
			for bbCanvas in canvasBoundingBox2ds:
				if( self.isOut(bbCanvas) ):	
					cornerPoint = [ self.pointVector[0] + self.pointVector[2] , self.pointVector[1] + self.pointVector[3] ]	
					#GET AXE INDEX COLLISION
					closestEdge  = self.getCollideEdge( bbCanvas , vectorIncr  )
					vEdge = [ closestEdge[2] - closestEdge[0] , closestEdge[3] - closestEdge[1] ]
					if( abs(vEdge[0]) < abs(vEdge[1]) ): vectorIncr[0] = 0
					else:                                vectorIncr[1] = 0					
					#GET CLOSEST POINT
					cornerPoint = [ self.pointVector[0] + self.pointVector[2] , self.pointVector[1] + self.pointVector[3] ]
					closestPoints = self.utils_getClosestPointOnLine( cornerPoint , closestEdge )
					self.pointVector = self.pointVector[0:2] + [ closestPoints[0] - self.pointVector[0] ,  closestPoints[1] - self.pointVector[1] ]
					self.createFromPointVector( self.pointVector )	

			pointVectorEnd = self.pointVector[:]

			if( keepRatio ):
				if( vectorIncr[0] == 0 ) or ( vectorIncr[1] == 0 ) or ( pointVectorStart == pointVectorEnd) or ( iterLimit < iterActual ) or ( self.area	< oldArea ):
					stop = 1
			else:
				if( vectorIncr == [0,0] ) or ( pointVectorStart == pointVectorEnd) or ( iterLimit < iterActual ) or ( self.area	< oldArea ):
					stop = 1

			iterActual += 1
			if( self.debug == 1 ):
				print( oldArea , 'vs' , self.area	)
				print( 'collision' , collision )
				self.visualize('grow {}'.format(iterActual) )			

	def snapPointToTheClosestSide( self , toSnap , boundingBox2d ):
		closestCoords = self.utils_getClosestPoint( toSnap , boundingBox2d.squareCoords , 2)

		vSnapClosest = [ closestCoords[0] - toSnap[0] , closestCoords[1] - toSnap[1] ]
		if( abs(vSnapClosest[0]) < abs(vSnapClosest[1]) ):
			toSnap[0] = closestCoords[0]
		else:
			toSnap[1] = closestCoords[1]

		return toSnap

	def getClosestPoint( self , point ):
		closestPointsOnSegment = []
		squareCoords = self.squareCoords + self.squareCoords[0:2]
		for i in range( 0 , len(squareCoords) - 2 , 2 ):
			edgeCoords = [ squareCoords[i+0] , squareCoords[i+1] ,  squareCoords[i+2] , squareCoords[i+3] ]
			closestPointsOnSegment += self.utils_getClosestPointOnSegment( point , edgeCoords )

		closestPoints = self.utils_sortByClosestPoint( closestPointsOnSegment , point , 2 ) 	
		return closestPoints[0:2]	


	def getClosestEdgeFromCoords( self , point ):

		squareCoords = self.squareCoords + self.squareCoords[0:2]
		distances = []
		distanceToEdge = {}
		edgesCoords = []
		for i in range( 0 , len(squareCoords) - 2 , 2 ):
			edgeCoords = [ squareCoords[i+0] , squareCoords[i+1] ,  squareCoords[i+2] , squareCoords[i+3] ]
			edgesCoords += edgeCoords
			pointOnEdge =  self.utils_getClosestPointOnSegment( point , edgeCoords ) 
			distance = om.MVector( pointOnEdge[0] - point[0] , pointOnEdge[1] - point[1] , 0 ).length()
			distances.append( distance )

		distancesSorted = distances[:]
		distancesSorted.sort()
		#GET CLOSEST EDGE INDEX
		ci = distances.index(distancesSorted[0])*4
		return [ edgesCoords[ci+0], edgesCoords[ci+1], edgesCoords[ci+2], edgesCoords[ci+3] ]

	def getClosestEdgeFromSegment( self , segment ):

		squareCoords = self.squareCoords + self.squareCoords[0:2]
		distances = []
		distanceToEdge = {}
		edgesCoords = []
		for i in range( 0 , len(squareCoords) - 2 , 2 ):
			edgeCoords = [ squareCoords[i+0] , squareCoords[i+1] ,  squareCoords[i+2] , squareCoords[i+3] ]
			edgesCoords += edgeCoords
			pointOnEdge =  self.utils_getClosestPointOnSegment( point , edgeCoords ) 
			distance = om.MVector( pointOnEdge[0] - point[0] , pointOnEdge[1] - point[1] , 0 ).length()
			distances.append( distance )

		distancesSorted = distances[:]
		distancesSorted.sort()
		#GET CLOSEST EDGE INDEX
		ci = distances.index(distancesSorted[0])*4
		return [ edgesCoords[ci+0], edgesCoords[ci+1], edgesCoords[ci+2], edgesCoords[ci+3] ]


	def getClosestEdge( self , boundingBox2d ):
		squareCoordsA = self.squareCoords + self.squareCoords[0:2]
		squareCoordsB = boundingBox2d.squareCoords + boundingBox2d.squareCoords[0:2]		
		distances = []
		distanceToEdge = {}
		edgesCoords = []
		for i in range( 0 , len(squareCoordsA) - 2 , 2 ):
			for j in range( 0 , len(squareCoordsB) - 2 , 2 ):		
				edgeA              = [ squareCoordsA[i+0] , squareCoordsA[i+1] , squareCoordsA[i+2] , squareCoordsA[i+3] ]				
				edgeB              = [ squareCoordsB[j+0] , squareCoordsB[j+1] , squareCoordsB[j+2] , squareCoordsB[j+3] ]	
				if ( edgeA[0] - edgeA[2] ==  edgeB[0] - edgeB[2] ) or ( edgeA[1] - edgeA[3] ==  edgeB[1] - edgeB[3]  ):  	
					projAOnB =  self.utils_getClosestPointOnLine( edgeA[0:2] , edgeB ) 	+ self.utils_getClosestPointOnLine( edgeA[2:4] , edgeB )
					distanceProjA = [ 0 , 0 ] 	
					distanceProjA[0] = om.MVector( projAOnB[0] - edgeA[0] , projAOnB[1] - edgeA[1] , 0 ).length()
					distanceProjA[1] = om.MVector( projAOnB[2] - edgeA[2] , projAOnB[3] - edgeA[3] , 0 ).length()
					distances.append(min(distanceProjA))
					edgesCoords += edgeB

		distancesSorted = distances[:]
		distancesSorted.sort()
		#GET CLOSEST EDGE INDEX
		ci = distances.index(distancesSorted[0])*4
		return [ edgesCoords[ci+0], edgesCoords[ci+1], edgesCoords[ci+2], edgesCoords[ci+3] ]

	def getCollideEdge( self , boundingBox2d , vDirection):
		bigNbr = 9999999999999999999999999999999999999999999999999999999999999999999999999.9
		cornerPoint   = [ self.pointVector[0] + self.pointVector[2] , self.pointVector[1] + self.pointVector[3] ]	
		#GET EDGE VECTOR AND POINT OF boundingBox2d
		vEdges = []
		points = []
		squareCoordsA = boundingBox2d.squareCoords + boundingBox2d.squareCoords[0:2]
		for i in range( 0 , len(squareCoordsA) - 2 , 2 ):	
				points += [ squareCoordsA[i+0] , squareCoordsA[i+1] ]
				vEdges += [ squareCoordsA[i+2] - squareCoordsA[i+0] , squareCoordsA[i+3] - squareCoordsA[i+1] ]				
		#GET LINE MOVING COEF
		if( vDirection[0] == 0 ):

			#GET POINT EDGE COLLISION
			pointEdgeCollision = []
			for i in range( 0 , len(vEdges) , 2 ):
				if( vEdges[i+0] == 0 ):
					pointEdgeCollisionX = bigNbr
					pointEdgeCollisionY = bigNbr			
				else:
					pointEdgeCollisionX = cornerPoint[0]
					pointEdgeCollisionY = points[i+1] 				
				pointEdgeCollision += [ pointEdgeCollisionX , pointEdgeCollisionY ]		

		elif( vDirection[1] == 0 ):

			#GET POINT EDGE COLLISION
			pointEdgeCollision = []
			for i in range( 0 , len(vEdges) , 2 ):
				if( vEdges[i+0] == 0 ):
					pointEdgeCollisionX = points[i+0]
					pointEdgeCollisionY = cornerPoint[1] 			
				else:
					pointEdgeCollisionX = bigNbr
					pointEdgeCollisionY = bigNbr				
				pointEdgeCollision += [ pointEdgeCollisionX , pointEdgeCollisionY ]	

		else:
			mLineCoefDir    = vDirection[1] / vDirection[0]
			mLineCoefOffset = cornerPoint[1] - mLineCoefDir * cornerPoint[0]  	
			#GET POINT EDGE COLLISION
			pointEdgeCollision = []
			for i in range( 0 , len(vEdges) , 2 ):
				if( vEdges[i+0] == 0 ):
					pointEdgeCollisionX = points[i+0]
					pointEdgeCollisionY = points[i+0] * mLineCoefDir + mLineCoefOffset 			
				else:
					pointEdgeCollisionX = ( points[i+1] - mLineCoefOffset ) / mLineCoefDir
					pointEdgeCollisionY = points[i+1] 				
				pointEdgeCollision += [ pointEdgeCollisionX , pointEdgeCollisionY ]				
	
		#GET DISTANCE CORNER === POINT EDGE COLLISON
		distances = []
		for i in range( 0 , len(pointEdgeCollision) , 2 ):
			distances.append( om.MVector( pointEdgeCollision[i] - cornerPoint[0] , pointEdgeCollision[i+1] - cornerPoint[1] , 0 ).length() )
		#GETT EDGE COLLISON			
		distancesSorted = distances[:]
		distancesSorted.sort()
		ci = distances.index(distancesSorted[0])*2

		return [ squareCoordsA[ci+0], squareCoordsA[ci+1], squareCoordsA[ci+2], squareCoordsA[ci+3] ]
		



	#_________________________________________________________________OUT
	def isIn( self , boundingBox2d ):
		for i in range( 0 , len( self.squareMiddleCoords ) , 2 ):
			if( self.utils_isInBoundingBox( boundingBox2d.boundingBoxCoords , self.squareMiddleCoords[i:i+2] ) == 1 ):
				return 1
		for i in range( 0 , len( boundingBox2d.squareMiddleCoords ) , 2 ):
			if( self.utils_isInBoundingBox( self.boundingBoxCoords , boundingBox2d.squareMiddleCoords[i:i+2] ) == 1 ):
				return 1
		return 0
	def isOut( self , boundingBox2d ):
		for i in range( 0 , len( self.squareMiddleCoords ) , 2 ):
			if( self.utils_isOutBoundingBox( boundingBox2d.boundingBoxCoords , self.squareMiddleCoords[i:i+2] ) == 1 ):
				return 1
		return 0

	def divide( nbr ):
		pass
	def isValide(  boundingBox2d ):
		pass

	def printAttrs( self , title = '' ):
		print('START_____________________________ ' + title)
		print('**********ATTRS***********')
		print( 'width              : ' , self.width               )
		print( 'heigth             : ' , self.heigth              )				
		print( 'ratio              : ' , self.ratio               )
		print( 'area               : ' , self.area                )
		print( 'squareCoords       : ' , self.squareCoords        ) 
		print( 'boundingBoxCoords  : ' , self.boundingBoxCoords   )
		print( 'pointVector        : ' , self.pointVector         )
		print( 'pointAngleDistance : ' , self.pointAngleDistance  )	
		print('END________________________________ ' + title)


	def visualize( self , name ):
		barycentre = [ (self.boundingBoxCoords[0] + self.boundingBoxCoords[2])/2.0 , (self.boundingBoxCoords[1] + self.boundingBoxCoords[3])/2.0]
		width  = self.width
		heigth = self.heigth
		planeName = mc.polyPlane( n = name , w = width , h = heigth , sx = 1 , sy = 1  , ax = [ -1 ,0 ,0 ] , cuv = 2 , ch = 1 )	
		mc.setAttr(( planeName[0] + '.translateZ') , barycentre[0] )
		mc.setAttr(( planeName[0] + '.translateY') , barycentre[1] )
		return planeName
	
	#_________________________________________________________________UTILS


	def vectorToAngleDistance( self , vector ):
		mayaVector = om.MVector( vector[0] , vector[1] , 0 )
		angle = math.degrees( mayaVector.angle( self.vX ) )

		if( mayaVector* self.vY < 0 ):
			angle = 360 - angle

		return [ angle , mayaVector.length() ]

	@staticmethod
	def utils_resizeVector( vector , newSize ):
		vectorResize = []
		if( len(vector) == 2 ):
			mayaVector = om.MVector( vector[0] , vector[1] , 0 )
			mayaVector.normalize()
			mayaVector *= newSize 
			vectorResize = [ mayaVector.x , mayaVector.y ]
		elif( len(vector) == 3 ):
			mayaVector = om.MVector( vector[0] , vector[1] , vector[2] )
			mayaVector.normalize()
			mayaVector *= newSize 
			vectorResize = [ mayaVector.x , mayaVector.y , mayaVector.z ]
		return vectorResize

	@staticmethod
	def utils_getBoundingBoxCoords( coords , nbrAxis ):
		#INIT MIN & MAX VALUE
		customValueHigh =  999999999999999999999999999999999999999999999999999999999999999999999
		customValueLow  = -999999999999999999999999999999999999999999999999999999999999999999999
		maxValues = [ customValueLow  ] * nbrAxis 
		minValues = [ customValueHigh ] * nbrAxis 
		#COMPUTE MIN & MAX 
		for i in range( 0 , len( coords ) , nbrAxis ):
			for j in range( 0 , nbrAxis):
				if( maxValues[j] < coords[i+j] ):
					maxValues[j] = coords[i+j]
				if( coords[i+j] < minValues[j] ):
					minValues[j] = coords[i+j]
		#RETURN BOUNDING BOX COORDS
		boundingBoxCoords =  minValues + maxValues 	
		return boundingBoxCoords	

	@staticmethod
	def utils_sortByClosestPoint( coords , refCoords , nbrAxis):
		distances = []
		for i in range( 0 , len(coords) , nbrAxis ):
			#GET VECTOR
			vCoordsToRef = [0,0,0]
			for j in range(  0 , nbrAxis ):
				vCoordsToRef[j] = coords[i+j] - refCoords[j] 
			#GET DISTANCE
			distance = om.MVector( vCoordsToRef[0] , vCoordsToRef[1] , vCoordsToRef[2] ).length() 
			#STORE IT
			distances.append( distance )
		#SORT
		distancesSorted = distances[:]
		distancesSorted.sort()
		#GET CLOSEST POINT INDEX
		closestCoordsIndex = []
		for dist in distancesSorted:
			closestCoordsIndex.append( distances.index(distancesSorted[0])*nbrAxis)
		#GET CLOSEST POINT COORDS
		closestCoords = []
		for i in closestCoordsIndex:
			for j in range(  0 , nbrAxis ):
				closestCoords.append( coords[i+j] ) 	
		
		return closestCoords

	@staticmethod
	def utils_getClosestPoint( coords , refCoords , nbrAxis ):
		distances = []
		for i in range( 0 , len(coords) , nbrAxis ):
			#GET VECTOR
			vCoordsToRef = [0,0,0]
			for j in range(  0 , nbrAxis ):
				vCoordsToRef[j] = coords[i+j]-refCoords[j] 
			#GET DISTANCE
			distance = om.MVector( vCoordsToRef[0] , vCoordsToRef[1] , vCoordsToRef[2] ).length() 
			#STORE IT
			distances.append( distance )
		#SORT
		distancesSorted = distances[:]
		distancesSorted.sort()
		#GET CLOSEST POINT INDEX
		closestCoordsIndex = distances.index(distancesSorted[0])*nbrAxis
		#GET CLOSEST POINT COORDS
		closestCoords = [0,0,0]
		for j in range(  0 , nbrAxis ):
			closestCoords[j] = coords[closestCoordsIndex+j] 		
		
		return closestCoords

	@staticmethod
	def utils_isInBoundingBox( bbCoords , coords ):
		if(  bbCoords[0] < coords[0] < bbCoords[2] ) and (  bbCoords[1] < coords[1] < bbCoords[3] ):
			return 1
		else:
			return 0


	def utils_isOutBoundingBox( self , bbCoords , coords ):
		if(  bbCoords[0] <= coords[0] <= bbCoords[2] ) and (  bbCoords[1] <= coords[1] <= bbCoords[3] ):
			return 0
		else:
			return 1



	def utils_getClosestPointOnLine( self , coords , lineCoords  ):	
		#GET LINE NORMAL
		vLine           = [ ( lineCoords[2] - lineCoords[0] ) , ( lineCoords[3] - lineCoords[1] ) ]  
		vDir            = [ ( lineCoords[0] - coords[0] )  , ( lineCoords[1] - coords[1] ) ] 			
		vNormal         = self.utils_getVectorNormal( vLine , vDir )
		#GET y OF THE LINE EQUATION  2x + y = 0	
		iCoords = [ 0.0 , 0.0 ]			
		if(   vLine[0] == 0 ): return [ lineCoords[0] , coords[1] ]
		elif( vLine[1] == 0 ): return [ coords[0] , lineCoords[1] ] 							
		x = vLine[0]/vLine[1] 
		y = lineCoords[1] - ( (vLine[0]/vLine[1]) *  lineCoords[0] )
		xBis = vNormal[0]/vNormal[1] 
		yBis = coords[1] - ( xBis *  coords[0] )		
		#GET INTERSECT COORDS	
		iCoords = [ 0.0 , 0.0 ]	
		iCoords[0] = ( yBis - y )/( x - xBis ) 
		iCoords[1] = iCoords[0] * x + y  
		#CLAMP EVERYTHING
		return iCoords




	def utils_getClosestPointOnSegment( self , coords , lineCoords ):
		#GET LINE NORMAL
		vLine           = [ ( lineCoords[2] - lineCoords[0] ) , ( lineCoords[3] - lineCoords[1] ) ]  
		vDir            = [ ( lineCoords[0] - coords[0] )  , ( lineCoords[1] - coords[1] ) ] 			
		vNormal         = self.utils_getVectorNormal( vLine , vDir )
		#GET y OF THE LINE EQUATION  2x + y = 0	
		iCoords = [ 0.0 , 0.0 ]			
		if(   vLine[0] == 0 ): 
			iCoords = [ lineCoords[0] , coords[1] ]
			if( iCoords[1] < min( lineCoords[1] , lineCoords[3] ) ): iCoords[1] = min( lineCoords[1] , lineCoords[3] )
			if( max( lineCoords[1] , lineCoords[3] ) < iCoords[1] ): iCoords[1] = max( lineCoords[1] , lineCoords[3] )						 
			return iCoords	
		elif( vLine[1] == 0 ): 
			iCoords = [ coords[0] , lineCoords[1] ] 
			if( iCoords[0] < min( lineCoords[0] , lineCoords[2] ) ): iCoords[0] = min( lineCoords[0] , lineCoords[2] )
			if( max( lineCoords[0] , lineCoords[2] ) < iCoords[0] ): iCoords[0] = max( lineCoords[0] , lineCoords[2] )
			return iCoords								

		x = vLine[0]/vLine[1] 
		y = lineCoords[1] - ( (vLine[0]/vLine[1]) *  lineCoords[0] )
		xBis = vNormal[0]/vNormal[1] 
		yBis = coords[1] - ( xBis *  coords[0] )		
		#GET INTERSECT COORDS	
		iCoords = [ 0.0 , 0.0 ]	
		iCoords[0] = ( yBis - y )/( x - xBis ) 
		iCoords[1] = iCoords[0] * x + y  
		#CLAMP EVERYTHING
		if( lineCoords[0] < iCoords[0] < lineCoords[2] ) and ( lineCoords[1] < iCoords[1] < lineCoords[3] ):   return iCoords
		elif( lineCoords[2] < iCoords[0] < lineCoords[0] ) and ( lineCoords[3] < iCoords[1] < lineCoords[1] ): return iCoords
		elif( lineCoords[0] < iCoords[0] ) and ( lineCoords[1] < iCoords[1] ):			                       return lineCoords[2:4]
		else:			                                                                                       return lineCoords[0:2]	



	@staticmethod
	def utils_getVectorNormal( vectorA , vDir ):
		#GET NORMAL
		vecteurNormal = ompy.MVector( vectorA[1] * -1 , vectorA[0] , 0 )
		#GET MODIF IT WITH VECTOR DIR
		vectorDirection   = ompy.MVector( vDir[0] , vDir[1] , 0 ) 	
		coef = math.copysign( 1 , vecteurNormal*vectorDirection )		
		vecteurNormal = ompy.MVector( vecteurNormal.x * coef , vecteurNormal.y * coef  , 0 )
		vecteurNormal.normalize()
		return [ vecteurNormal.x , vecteurNormal.y , vecteurNormal.z ] 		
			 




'''




	def getCollisionEdges( self , boundingBox2d , returnOutsideEdges = 0 ):
		collisionEdges = []
		#GET COLLISION POINTS
		if( returnOutsideEdges == 0 ): 
			BBaCollisionPoints  = self.getInsideCollisionPoints( boundingBox2d ) #[0,1,2,3]
			BBbCollisionPoints =  boundingBox2d.getInsideCollisionPoints( self ) #[0,1,2,3]			
		else:                         
			BBaCollisionPoints  = self.getOutsideCollisionPoints( boundingBox2d ) #[0,1,2,3]
			BBbCollisionPoints =  boundingBox2d.getOutsideCollisionPoints( self ) #[0,1,2,3]		
		#GET COLLISION POINTS
		BBaCollisionEdges = self.pointsIndexToEdgeIndex(collisionPoints) 
		BBbCollisionEdges = boundingBox2d.pointsIndexToEdgeIndex(BBbCollisionPoints)
		#EXCEPTION
		if( len(BBaCollisionPoints) == 1 ) and( len(BBbCollisionPoints) == 1 ):	
			pointA = self.pointsIndexToCoords(BBaCollisionPoints) 	
			pointB = boundingBox2d.pointsIndexToCoords(BBbCollisionPoints) 	
			vectorAB = [ pointA[0] - pointB[0] , pointA[1] - pointB[2] ]
			BBaCollisionEdges = vectorAB
			BBbCollisionEdges = boundingBox2d.pointsIndexToEdgeIndex(BBbCollisionPoints)

		collisionEdges = []
		for toStayOut in boundingBoxToStayOut:
			if( self.isIn( toStayOut ) ):
				collisionEdges.append( self.getCollisionEdge( toAvoid ) )
		for toStayIn in boundingBoxToStayIns:
			if( self.isOut( toStayIn ) ):
				collisionEdges.append( self.getCollisionEdge( toStayIn ) )

		collisionEdges = list(set(collisionEdges))
		return collisionEdges


	def utils_getClosestPointOnSegmentOld( self , coords , lineCoords ):
		#GET LINE NORMAL
		vLine           = [ ( lineCoords[2] - lineCoords[0] ) , ( lineCoords[3] - lineCoords[1] ) ]  
		vDir            = [ ( lineCoords[0] - coords[0] )  , ( lineCoords[1] - coords[1] ) ] 			
		vNormal         = self.utils_getVectorNormal( vLine , vDir )
		#GET y OF THE LINE EQUATION  2x + y = 0	
		if(   vLine[0] == 0 ): x = 0
		elif( vLine[1] == 0 ): x , y = 1 , 0
		else: 
			x = vLine[0]/vLine[1] 
			y = lineCoords[1] - ( (vLine[0]/vLine[1]) *  lineCoords[0] )

		if(   vNormal[0] == 0 ): xBis = 0
		elif( vNormal[1] == 0 ): xBis = 1
		else: xBis = vNormal[0]/vNormal[1] 
		yBis = coords[1] - ( xBis *  coords[0] )		
		#GET INTERSECT COORDS	
		iCoords = [ 0.0 , 0.0 ]	
		iCoords[0] = ( yBis - y )/( x - xBis ) 
		iCoords[1] = iCoords[0] * x + y  
		#CLAMP EVERYTHING
		print( 'iCoords' , iCoords )
		if( lineCoords[0] < iCoords[0] < lineCoords[2] ) and ( lineCoords[1] < iCoords[1] < lineCoords[3] ):				
			return iCoords
		elif( lineCoords[2] < iCoords[0] < lineCoords[0] ) and ( lineCoords[3] < iCoords[1] < lineCoords[1] ):				
			return iCoords
		elif( lineCoords[0] < iCoords[0] ) and ( lineCoords[1] < iCoords[1] ):			
			return lineCoords[2:4]
		else:			
			return lineCoords[0:2]			

'''