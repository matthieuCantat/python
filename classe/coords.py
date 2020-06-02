import types

import maya.cmds as mc
import maya.OpenMaya as om
import maya.api.OpenMaya as ompy

from ..utils import utilsPython
from ..utils import utilsMath
from ..utils import utilsMayaApi
from .mayaClasse import *
from . import trsBackUp


class coords(mayaClasse):
	
	'''
_______________________________________CREATE	
createFromCoords
createFromObj
createFromObjs
_______________________________________MODIF
parent
unParent
mirror
offset
offsetParent	
snapOnPlane	
snapOnCurve
snapOnLine		
sortInit
sortReverse
sortByAxe
sortClosestPoint
sortClosestLine
sortClosestPlane
_______________________________________UPDATE ATTR
printAttrs
updateAttrPoints
initAttrIndexesInit
overrideCoords
_______________________________________SURCHARGE
_______________________________________OUT
toObj	
toObjs
toBarycentre
toBoundingBox
toBoundingBoxBarycentre
toOrientedBoundingBox
visualize
visualizePivot
visualizeBarycentre
visualizeBoundingBoxBarycentre
visualizeBoundingBox
visualizeOrientedBoundingBox
_______________________________________UTILS
utils_mayaNodeType	
utils_getCoordsMesh
utils_getCoordsCurve
utils_getCoordsSurface
utils_getBarycentre
utils_getBoundingBoxCoords
utils_getOrientedBoundingBoxCoords
utils_setCoordsMesh
utils_setCoordsCurve
utils_setCoordsSurface
utils_getNbrPointsMesh
utils_getNbrPointsCurve	
utils_getNbrPointsSurface
utils_boundingBoxToDiagonalLength
utils_buildVisuLocators
utils_buildVisuBoundingBox
utils_boundingBoxToCubePoints
utils_isCoordsClassInstance
utils_arrayCompareIsInf
utils_removeCoords
utils_getIndexes
utils_getDistance
utils_sortReturnIndex
utils_pointIndexToCoordsIndex		
utils_coordsToTrs
utils_trsToCoords
_______________________________________TO DO
getCoordsOneSidePlane *
getCoordsInsideCube *
getCoordsInsideVolume *
allOrientedBB proc *


	'''
	
	def __init__(self):

		self.type      = 'coords'
		self.debug    = 0	
		self.nbrAxis  = 3
		self.coords   = []
		self.points   = []
		self.pivot    = []
		self.barycentre = []	
		self.indexesInitCoords = []
		self.indexesInitPoints = []
		self.boundingBoxCoords       = []
		self.boundingBoxPoints       = []				
		self.boundingBoxBarycentre   = []				
		self.orientedBoundingBoxCoords = []
		self.orientedBoundingBoxPoints = []
		self.trs = trsBackUp.trs()

	#__________________________________________________________________________________________________________ FILL
	def createFromCoords( self , coords , worldSpace = True ):
		self.coords = coords
		self.initAttrIndexesInit()			
		self.updateAttrPoints()
		return 1

	def createFromObj( self , obj , worldSpace = True ):

		objType = self.utils_mayaNodeType( obj )
		if(   objType in ['mesh'   ,'meshShape'   ] ): self.coords = self.utils_getCoordsMesh( obj , worldSpace )				
		elif( objType in ['curve'  ,'curveShape'  ] ): self.coords = self.utils_getCoordsCurve( obj , worldSpace )
		elif( objType in ['surface','surfaceShape'] ): self.coords = self.utils_getCoordsNurbs( obj , worldSpace )				
		else:                                          self.coords = self.trs.createFromObj( obj , worldSpace )[0:3]
			
		self.initAttrIndexesInit()			
		self.updateAttrPoints()
		return self.coords

	def createFromObjs( self , objs , worldSpace = True ):
		coords = []
		for obj in objs:
			coords += self.createFromObj( obj , worldSpace )

		self.coords = coords
		self.initAttrIndexesInit()			
		self.updateAttrPoints()
		return self.coords

	#__________________________________________________________________________________________________________ GET	
	def toBarycentre( self , overrideCoords = None ):
		self.overrideCoords( overrideCoords )
		self.barycentre = self.utils_getBarycentre( self.coords , self.nbrAxis )
		return self.barycentre

	def toBoundingBox( self , overrideCoords = None ):	
		self.overrideCoords( overrideCoords )
		self.boundingBoxCoords = self.utils_getBoundingBoxCoords( self.coords , self.nbrAxis )	
		self.updateAttrPoints()
		return self.boundingBoxCoords 

	def toBoundingBoxBarycentre( self , overrideCoords = None ):
		self.overrideCoords( overrideCoords )
		self.toBoundingBox()
		self.boundingBoxBarycentre = self.utils_getBarycentre( self.boundingBoxCoords , self.nbrAxis )
		return self.boundingBoxBarycentre

	def toBoundingBoxScale( self , overrideCoords = None ):
		self.overrideCoords( overrideCoords )
		self.toBoundingBox()
		return utilsMath.getBBscale( self.boundingBoxCoords )
	
	def toBoundingBoxDiagonalLength( self , overrideCoords = None ):
		self.overrideCoords( overrideCoords )
		self.toBoundingBox()
		return utilsMath.getBBscaleLength( self.boundingBoxCoords )


	def toOrientedBoundingBox( self , overrideCoords = None ):
		self.overrideCoords( overrideCoords )
		self.orientedBoundingBoxCoords = self.utils_getOrientedBoundingBoxCoords( self.coords , self.nbrAxis )
		self.updateAttrPoints()
		return self.orientedBoundingBoxCoords


	#__________________________________________________________________________________________________________ visualize	
	def visualize( self , name = '' , parent = '' , colorRamp = [ 1.0 , 0 , 0 , 0 , 0 , 1.0  ]   ):
		return self.utils_buildVisuLocators( (name + '_coords_')  , self.coords , parent , self.coords , colorRamp )

	def visualizePivot( self , name = '' , parent = '' ):
		return self.utils_buildVisuLocators( (name + '_pivot_LOC')  ,  self.pivot , parent , self.coords )

	def visualizeBarycentre( self , name = '' , parent = '' ):
		return self.utils_buildVisuLocators( (name + '_barycentre_LOC')  ,  self.barycentre , parent , self.coords )

	def visualizeBoundingBoxBarycentre( self , name = '' , parent = '' ):
		return self.utils_buildVisuLocators( (name + '_boundingBoxBarycentre_LOC')  ,  self.boundingBoxBarycentre , parent , self.coords )

	def visualizeBoundingBox( self , name = '' , parent = '' ):
		return self.utils_buildVisuBoundingBox( (name + '_boundingBox')  ,  self.boundingBoxCoords , parent )
				
	def visualizeOrientedBoundingBox( self , name = '' , parent = '' ):
		return self.utils_buildVisuBoundingBox( (name + '_orientedBoundingBox')  ,  self.orientedBoundingBoxCoords , parent  )
		
	#__________________________________________________________________________________________________________ Sort	

	def sortInit( self ):
		coordsTmp = self.coords[:]
		for i in range( 0 , len(self.indexesInitCoords) ):
			coordsTmp[self.indexesInitCoords[i]] = self.coords[i]
		self.coords = coordsTmp
		self.initAttrIndexesInit()		
		self.updateAttrPoints()


	def sortReverse( self , overrideCoords = None ):
		self.overrideCoords( overrideCoords )
		#INIT
		coordsInv  = []
		indexesInv = []		
		for i in range( len(self.indexesInitCoords) - self.nbrAxis , -1 , self.nbrAxis * -1 ):
			for j in range( 0 , self.nbrAxis ):
				coordsInv.append( self.coords[i+j] )
				indexesInv.append( self.indexesInitCoords[i+j])

		self.coords = coordsInv
		self.indexesInitCoords = indexesInv
		self.updateAttrPoints()
		return self.coords


	def sortByAxe( self , axeOrder = [0,1,2] ,  inv = False , overrideCoords = None ):
		self.overrideCoords( overrideCoords )
		#INIT
		coordsSorted  = []
		indexesSorted = []		
		#RESET TO DEFAUT COORDS
		minValues = [999999999999999999999999999999999999999999999999999] * self.nbrAxis
		coordsTmp = self.coords[:]
		while not( len(coordsSorted) == len(self.coords) ):

			minValuesTmp = minValues
			for i in range( 0 , len(coordsTmp) , 3 ):
				if( self.utils_arrayCompareIsInf( coordsTmp[ i : i+self.nbrAxis ] , minValuesTmp , axeOrder ) ):
					minValuesTmp = coordsTmp[ i : i+self.nbrAxis ]
		
			coordsSorted += minValuesTmp
			indexesSorted += self.utils_getIndexes( self.coords , minValuesTmp )
			coordsTmp = self.utils_removeCoords( coordsTmp , minValuesTmp )

		#UPDATE
		self.coords = coordsSorted	
		self.indexesInitCoords = indexesSorted
		self.updateAttrPoints()

		if( inv == True ):
			self.sortReverse()	

		return self.coords	


	def sortClosestPoint( self , point = [0,0,0] ,  inv = False , overrideCoords = None ):
		self.overrideCoords( overrideCoords )		
		#GET DISTANCES 
		distances = []
		for i in range( 0 , len(self.coords) , self.nbrAxis ):
			distances.append( self.utils_getDistance( point , self.coords[i:i+self.nbrAxis] ) )
		#SORT DISTANCES & INDEX
		distancesSortedIndexes = self.utils_sortReturnIndex(distances)
		coordsSortedIndexes = self.utils_pointIndexToCoordsIndex( distancesSortedIndexes , self.nbrAxis )
		#GET SORTED COORDS
		coordsSorted = []
		indexesSorted = []
		for i in coordsSortedIndexes:
			coordsSorted.append( self.coords[i] )
			indexesSorted.append( self.indexesInitCoords[i])
		#UPDATE
		self.coords = coordsSorted	
		self.indexesInitCoords = indexesSorted
		self.updateAttrPoints()

		if( inv == True ):
			self.sortReverse()

		return self.coords		


	def sortClosestLine( self , points = [0,0,0,1,0,0] , inv = False , overrideCoords = None ):
		self.overrideCoords( overrideCoords )		
		#GET COORDS SNAP
		coordsSnaped = []
		for i in range( 0 , len(self.coords) , self.nbrAxis ):
			self.trs.value = self.utils_coordsToTrs( self.coords[i:i+self.nbrAxis] )
			self.trs.snapOnLine( [ points[0:3] , points[3:6] ])
			coordsSnaped += self.utils_trsToCoords( self.trs.value , self.nbrAxis ) 
		#GET DISTANCES
		distances = []
		for i in range( 0 , len(self.coords) , self.nbrAxis ):
			distances.append( self.utils_getDistance( coordsSnaped[i:i+self.nbrAxis] , self.coords[i:i+self.nbrAxis] ) )
		#SORT DISTANCES & INDEX
		distancesSortedIndexes = self.utils_sortReturnIndex(distances)
		coordsSortedIndexes = self.utils_pointIndexToCoordsIndex( distancesSortedIndexes , self.nbrAxis )
		#GET SORTED COORDS
		coordsSorted = []
		indexesSorted = []
		for i in coordsSortedIndexes:
			coordsSorted.append( self.coords[i] )
			indexesSorted.append( self.indexesInitCoords[i])
		#UPDATE
		self.coords = coordsSorted	
		self.indexesInitCoords = indexesSorted
		self.updateAttrPoints()

		if( inv == True ):
			self.sortReverse()		

		return self.coords

	def sortClosestPlane( self , points = [0,0,0,1,0,0,0,0,1] , inv = False , overrideCoords = None ):
		self.overrideCoords( overrideCoords )
		#GET COORDS SNAP
		coordsSnaped = []
		for i in range( 0 , len(self.coords) , self.nbrAxis ):
			self.trs.value = self.coordsToTrs( self.coords[i:i+self.nbrAxis] )
			self.trs.snapOnPlane( [ points[0:3] , points[3:6] , points[6:9] ])
			coordsSnaped += self.trsToCoords( self.trs.value , self.nbrAxis ) 
		#GET DISTANCES
		distances = []
		for i in range( 0 , len(self.coords) , self.nbrAxis ):
			distances.append( self.utils_getDistance( coordsSnaped[i:i+self.nbrAxis] , self.coords[i:i+self.nbrAxis] ) )
		#SORT DISTANCES & INDEX
		distancesSortedIndexes = self.utils_sortReturnIndex(distances)
		coordsSortedIndexes = self.utils_pointIndexToCoordsIndex( distancesSortedIndexes , self.nbrAxis )
		#GET SORTED COORDS
		coordsSorted = []
		indexesSorted = []
		for i in coordsSortedIndexes:
			coordsSorted.append( self.coords[i] )
			indexesSorted.append( self.indexesInitCoords[i])
		#UPDATE
		self.coords = coordsSorted	
		self.indexesInitCoords = indexesSorted
		self.updateAttrPoints()

		if( inv == True ):
			self.sortReverse()	

		return self.coords	


	#__________________________________________________________________________________________________________ GET SPECIAL COORDS	
	def getCoordsOneSidePlane( self , points = [0,0,0 , 1,0,0 , 0,0,1 , 0,0,1 ] , inv = False ):
		return 0
	def getCoordsInsideCube( self , points = [0,0,0 , 1,0,0 , 0,0,1 , 0,0,1 , 0,0,1 , 0,0,1 , 0,0,1 , 0,0,1] , inv = False ):
		return 0
	def getCoordsInsideVolume( self , points = [ [0,0,0 , 1,0,0 , 0,0,1 , 0,0,1 ] , [0,0,0 , 1,0,0 , 0,0,1 , 0,0,1 ] ], inv = False ):
		return 0

	#__________________________________________________________________________________________________________ PARENT
	def parent( self , trsValueFather , overrideCoords = None ):
		self.overrideCoords( overrideCoords )
		coordsParented = []
		for i in range( 0 , len(self.coords) , self.nbrAxis ):
			self.trs.parent( trsValueFather , inTrsValue = self.utils_coordsToTrs( self.coords[i:i+self.nbrAxis] ) )
			coordsParented += self.utils_trsToCoords( self.trs.value , self.nbrAxis )

		self.coords = coordsParented
		return self.coords

	def unParent( self , trsValueFather , overrideCoords = None ):
		self.overrideCoords( overrideCoords )
		coordsUnparented = []
		for i in range( 0 , len(self.coords) , self.nbrAxis ):
			self.trs.unParent( trsValueFather , inTrsValue = self.utils_coordsToTrs( self.coords[i:i+self.nbrAxis] ) )
			coordsUnparented += self.utils_trsToCoords( self.trs.value , self.nbrAxis )

		self.coords = coordsUnparented
		return self.coords

	def offset( self , trsOffset , pivCoords , rotateAxeOrder = ['X','Y','Z'], overrideCoords = None ):
		self.overrideCoords( overrideCoords )
		
		if( self.coords == [[]] ):
			return [[]]

		self.coords = utilsMath.transformCoords( self.coords , pivCoords , trsOffset , rotateAxeOrder ) 
		
		return self.coords		

	def offsetParent( self , trsValueFather , trsValueOffset , overrideCoords = None ):
		self.overrideCoords( overrideCoords )
		coordsOffseted = []
		for i in range( 0 , len(self.coords) , self.nbrAxis ):
			self.trs.offsetParentTrs( trsValueFather , trsValueOffset , inTrsValue = self.utils_coordsToTrs( self.coords[i:i+self.nbrAxis] ) )
			coordsOffseted += self.utils_trsToCoords( self.trs.value , self.nbrAxis )

		self.coords = coordsOffseted
		return self.coords


	
	def transform( self , value , pivot , iter ):

		Trs      = trsBackUp.trs()
		TrsPivot = trsBackUp.trs( pivot )			
	
		for i in range(0,iter):
		    Trs.offsetTrs( pivot , value )
		    TrsPivot.offsetItself( pivot , value )
		    pivot = TrsPivot.value

		self.offset( Trs.value , [0,0,0,0,0,0,1,1,1] )


	#__________________________________________________________________________________________________________ SNAP
	def snapOnVolume( self ):
		return 0

	def snapOnPlane( self , planeCoords , overrideCoords = None ):
		self.overrideCoords( overrideCoords )
		coordsSnaped = []
		for i in range( 0 , len(self.coords) , self.nbrAxis ):
			self.trs.snapOnPlane( planeCoords , inTrsValue = self.utils_coordsToTrs( self.coords[i:i+self.nbrAxis] ) )
			coordsSnaped += self.utils_trsToCoords( self.trs.value , self.nbrAxis )

		self.coords = coordsSnaped
		return self.coords

	def snapOnLine( self , lineCoords , overrideCoords = None ):
		self.overrideCoords( overrideCoords )
		coordsSnaped = []
		for i in range( 0 , len(self.coords) , self.nbrAxis ):
			self.trs.snapOnLine( lineCoords , inTrsValue = self.utils_coordsToTrs( self.coords[i:i+self.nbrAxis] ) )
			coordsSnaped += self.utils_trsToCoords( self.trs.value , self.nbrAxis )

		self.coords = coordsSnaped
		return self.coords
	#__________________________________________________________________________________________________________ SNAP
	def mirror( self , planSymCoords , overrideCoords = None ):

		if( type( planSymCoords )  in [ types.StringType , types.UnicodeType ] )and( mc.objExists(planSymCoords) ):
			Coords = coords( )
			Coords.createFromObj(planSymCoords)
			planSymCoords = Coords.coords[0:9]
		

		self.overrideCoords( overrideCoords )
		coordsMirrored = []
		for i in range( 0 , len(self.coords) , self.nbrAxis ):
			self.trs.mirror( planSymCoords , inValue = self.utils_coordsToTrs( self.coords[i:i+self.nbrAxis] ) )
			coordsMirrored += self.utils_trsToCoords( self.trs.value , self.nbrAxis )

		self.coords = coordsMirrored
		return self.coords



	#__________________________________________________________________________________________________________ toObj

	def toObj( self , obj , worldSpace = True , overrideCoords = None ):

		self.overrideCoords( overrideCoords )
		firstIndex = 0

		objType = self.utils_mayaNodeType( obj )

		if(   objType in ['mesh'   ,'meshShape'   ] ): 
			self.utils_setCoordsMesh( self.coords[firstIndex:] , obj , worldSpace )	
			firstIndex += self.utils_getNbrPointsMesh(obj) * self.nbrAxis	
		elif( objType in ['curve'  ,'curveShape'  ] ):
			self.utils_setCoordsCurve( self.coords[firstIndex:] , obj , worldSpace )
			firstIndex += self.utils_getNbrPointsCurve(obj) * self.nbrAxis	
		elif( objType in ['surface','surfaceShape'] ): 
			self.utils_setCoordsNurbs( self.coords[firstIndex:] , obj , worldSpace )	
			firstIndex += self.utils_getNbrPointsSurface(obj) * self.nbrAxis
		else:
			self.trs.createFromObj( obj , worldSpace )                                         
			self.trs[0:3] = self.coords[ firstIndex : (firstIndex+self.nbrAxis) ]
			self.trs.toObj( obj , worldSpace )
				
		return 1	

	def toObjs( self , objs , worldSpace = True , overrideCoords = None ):
		for obj in objs:
			self.toObj( obj )		
		return 1	

	#__________________________________________________________________________________________________________ UPDATE ATTR
	def initAttrIndexesInit( self ):
		self.indexesInitCoords = []
		for i in range( 0 , len(self.coords) ):
			self.indexesInitCoords.append(i)

	def updateAttrPoints( self ):
		self.points = []
		for i in range( 0 , len( self.coords ) , self.nbrAxis ):
			self.points.append( [ self.coords[i+0] , self.coords[i+1] , self.coords[i+2] ] )

		self.boundingBoxPoints = []
		for i in range( 0 , len( self.boundingBoxCoords ) , self.nbrAxis ):
			self.boundingBoxPoints.append( [ self.boundingBoxCoords[i+0] , self.boundingBoxCoords[i+1] , self.boundingBoxCoords[i+2] ] )

		self.orientedBoundingBoxPoints = []
		for i in range( 0 , len( self.orientedBoundingBoxCoords ) , self.nbrAxis ):
			self.orientedBoundingBoxPoints.append( [ self.orientedBoundingBoxCoords[i+0] , self.orientedBoundingBoxCoords[i+1] , self.orientedBoundingBoxCoords[i+2] ] )						

		self.indexesInitPoints = []
		for i in range( 0 , len( self.indexesInitCoords ) , self.nbrAxis ):
			self.indexesInitPoints += [ self.indexesInitCoords[i] ]						

	def overrideCoords( self , inCoords ):
		coords = self.coords
		if not( inCoords == None ):
			coords = inCoords
			self.createFromCoords(coords)
		return coords

	def printAttrs( self , title = '' ):

		print('START_____________________________ ' + title)
		print('**********ATTRS***********')
		print( 'nbrAxis            : ' , self.nbrAxis              )
		print( 'coords             : ' , self.coords               )
		print( 'len(coords)        : ' , len(self.coords)          ) 
		print( 'points             : ' , self.points               )
		print( 'len(points)        : ' , len(self.points)          )
		print( 'indexesInitCoords  : ' , self.indexesInitCoords    )	
		print( 'indexesInitPoints  : ' , self.indexesInitPoints    )		 
		print( 'pivot              : ' , self.pivot                )
		print( 'barycentre         : ' , self.barycentre           )
		print( 'boundingBoxCoords  : ' , self.boundingBoxCoords    )
		print( 'boundingBoxPoints  : ' , self.boundingBoxPoints    )
		print( 'boundingBoxBarycentre  : ' , self.boundingBoxBarycentre   )
		print( 'orientedBoundingBoxCoords  : ' , self.orientedBoundingBoxCoords   )
		print( 'orientedBoundingBoxPoints  : ' , self.orientedBoundingBoxPoints   )
		print('END________________________________ ' + title)
		
	#__________________________________________________________________________________________________________ OVERLOAD	
	def  __len__( self ):		
		return len(self.points)
		
	def __getitem__( self, index ): 	
		return self.points[index] 	
		
	def __setitem__ ( self, index , value ):		
		self.points[index] = value		
		indexCoords = index * self.nbrAxis
		self.coords[indexCoords:indexCoords+self.nbrAxis] = value
		self.updateAttrPoints()
		
	def __add__( self, values ):
		if( (type(values) == types.IntType) or (type(values) == types.FloatType ) ):
			for i in range( 0 , len( self.coords ) ):
				self.coords[i] += values
		elif( self.utils_isCoordsClassInstance(values) ):
			sizes = [ len(self.coords[i]) , len(values.coords[i]) ]
			sizes.sort()
			for i in range( 0 , sizes[0] ):
				self.coords[i] += values.coords[i]				
		elif( len(values) == self.nbrAxis ):
			for i in range( 0 , len( self.coords ) , self.nbrAxis ):
				self.coords[i+0] += values[0]
				self.coords[i+1] += values[1]
				self.coords[i+2] += values[2]
		elif( self.nbrAxis < len(values) ):
			for i in range( 0 , len( self.coords ) , self.nbrAxis ):
				self.coords[i+0] += values[i+0]
				self.coords[i+1] += values[i+1]
				self.coords[i+2] += values[i+2]
		self.updateAttrPoints()
		return self


	def __iadd__(self, values):
		return self + values

	def __sub__( self, values ):
		if( (type(values) == types.IntType) or (type(values) == types.FloatType ) ):
			for i in range( 0 , len( self.coords ) ):
				self.coords[i] -= values
		elif( self.utils_isCoordsClassInstance(values) ):
			sizes = [ len(self.coords[i]) , len(values.coords[i]) ]
			sizes.sort()
			for i in range( 0 , sizes[0] ):
				self.coords[i] -= values.coords[i]				
		elif( len(values) == self.nbrAxis ):
			for i in range( 0 , len( self.coords ) , self.nbrAxis ):
				self.coords[i+0] -= values[0]
				self.coords[i+1] -= values[1]
				self.coords[i+2] -= values[2]
		elif( self.nbrAxis < len(values) ):
			for i in range( 0 , len( self.coords ) , self.nbrAxis ):
				self.coords[i+0] -= values[i+0]
				self.coords[i+1] -= values[i+1]
				self.coords[i+2] -= values[i+2]

		self.updateAttrPoints()
		return self
		
	def __isub__(self, values):
		return self - values


	def __mul__( self, values ):
		if( (type(values) == types.IntType) or (type(values) == types.FloatType ) ):
			for i in range( 0 , len( self.coords ) ):
				self.coords[i] *= values
		elif( self.utils_isCoordsClassInstance(values) ):
			sizes = [ len(self.coords[i]) , len(values.coords[i]) ]
			sizes.sort()
			for i in range( 0 , sizes[0] ):
				self.coords[i] *= values.coords[i]				
		elif( len(values) == self.nbrAxis ):
			for i in range( 0 , len( self.coords ) , self.nbrAxis ):
				self.coords[i+0] *= values[0]
				self.coords[i+1] *= values[1]
				self.coords[i+2] *= values[2]
		elif( self.nbrAxis < len(values) ):
			for i in range( 0 , len( self.coords ) , self.nbrAxis ):
				self.coords[i+0] *= values[i+0]
				self.coords[i+1] *= values[i+1]
				self.coords[i+2] *= values[i+2]

		self.updateAttrPoints()
		return self

	def __imul__(self, values):
		return self * values

		
	def __truediv__( self, values ):
		if( (type(values) == types.IntType) or (type(values) == types.FloatType ) ):
			for i in range( 0 , len( self.coords ) ):
				self.coords[i] /= values
		elif( self.utils_isCoordsClassInstance(values) ):
			sizes = [ len(self.coords[i]) , len(values.coords[i]) ]
			sizes.sort()
			for i in range( 0 , sizes[0] ):
				self.coords[i] /= values.coords[i]				
		elif( len(values) == self.nbrAxis ):
			for i in range( 0 , len( self.coords ) , self.nbrAxis ):
				self.coords[i+0] /= values[0]
				self.coords[i+1] /= values[1]
				self.coords[i+2] /= values[2]
		elif( self.nbrAxis < len(values) ):
			for i in range( 0 , len( self.coords ) , self.nbrAxis ):
				self.coords[i+0] /= values[i+0]
				self.coords[i+1] /= values[i+1]
				self.coords[i+2] /= values[i+2]

		self.updateAttrPoints()
		return self

	def __itruediv__(self, values):
		return self / values		

	def append( self , values ):
		self.coords += values
		if( (type(values) == types.IntType) or (type(values) == types.FloatType ) ):
			pass
		if( self.utils_isCoordsClassInstance(values) ):
			self.coords += values.coords			
		else:
				self.coords += values

		self.updateAttrPoints()


	#__________________________________________________________________________________________________________UTILS


	def utils_mayaNodeType( self , obj ):

		if( mc.nodeType(obj) == 'mesh' ):
			return 'meshShape'
		elif( mc.nodeType(obj) == 'nurbsCurve' ):
			return 'curveShape'
		elif( mc.nodeType(obj) == 'nurbsSurface' ):
			return 'surfaceShape'
		elif( mc.nodeType(obj) == 'locator' ):
			return 'locatorShape'			
		elif( mc.nodeType(obj) == 'transform' ):

			childrens = mc.listRelatives( obj , c = True , s = True )

			if( len(childrens) == 0 ):
				return 'transform'
			elif( mc.nodeType( childrens[0] ) == 'mesh' ):
				return 'mesh'
			elif( mc.nodeType( childrens[0] ) == 'nurbsCurve' ):
				return 'curve'
			elif( mc.nodeType( childrens[0] ) == 'nurbsSurface' ):
				return 'surface'
			elif( mc.nodeType( childrens[0] ) == 'locator' ):
				return 'locator'

		return 'other'

	def utils_getCoordsMesh( self , mesh , worldSpace = True ):
		#INIT MESH CLASS
		dagPath    = utilsMayaApi.API_getMDagPath( mesh )	
		meshClass  = ompy.MFnMesh(dagPath)	
		#GET COORDS
		if( worldSpace ):
			pointArray = meshClass.getPoints( ompy.MSpace.kWorld )
		else:
			pointArray = meshClass.getPoints( ompy.MSpace.kObject )
		#MODIF ARRAY
		coords = []	
		for i in range( 0 , len(pointArray) ):
			coords += [ pointArray[i][0] , pointArray[i][1], pointArray[i][2] ]

		return coords

	def utils_getCoordsCurve( self , curve , worldSpace = True ):
		#INFO:   CVs = spans + degree  , knot = CVs + degree - 1			
		coords = []
		#CONVERT CURVE INTO SHAPES
		childrensTmp = parentsToChildrens( [ curve ] , includeParents = True );
		shapes       = filterType( childrensTmp , [ 'nurbsCurve' ] )    		
		#GET COORDS
		for shape in shapes:		
			nbrSpans  = mc.getAttr( shape + '.spans' ) 
			degree    = mc.getAttr( shape + '.degree' )  	
			nbrCvs    = nbrSpans + degree  
		
			shapeCoords = []
			for i in range( 0 , nbrCvs ):
				cvCoords  = mc.xform( '{0}.cv[{1}]'.format( shape , i ), q = True , t = True , ws = worldSpace  )
				shapeCoords += cvCoords    
		
			coords += shapeCoords

		return coords	
	'''
	def utils_getCoordsSurface( self , surface , worldSpace = True  ):
		#INFO:   CVs = spans + degree  , knot = CVs + degree - 1	
		coords = []
		#CONVERT NURBS INTO SHAPES
		childrensTmp = utilsMaya.getAllChildrens( [ surface ] , includeParents = True );
		shapes       = utilsMaya.filterType( childrensTmp , [ 'nurbsSurface' ] )    		
		#GET COORDS
		for shape in shapes:		
			nbrSpansU  = mc.getAttr( shape + '.spansU' ) 
			degreeU    = mc.getAttr( shape + '.degreeU' )  	
			nbrCvsU    = nbrSpansU + degreeU  

			nbrSpansV  = mc.getAttr( shape + '.spansV' ) 
			degreeV    = mc.getAttr( shape + '.degreeV' )  	
			nbrCvsV    = nbrSpansV + degreeV  			
		
			shapeCoords = []
			for u in range( 0 , nbrCvsU ):
				for v in range( 0 , nbrCvsV ):
					cvCoords  = mc.xform( '{0}.cv[{1}][{2}]'.format( shape , u , v ), q = True , t = True , ws = worldSpace  )
					shapeCoords += cvCoords    
		
			allCoords += shapeCoords

		return allCoords	
	'''
	def utils_getBarycentre( self , coords , nbrAxis ):
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

	def utils_getBoundingBoxCoords( self , coords , nbrAxis ):
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
		boundingBoxCoords = maxValues + minValues 	
		return boundingBoxCoords	

	def utils_getOrientedBoundingBoxCoords( self , coords , nbrAxis ):
		plugInPath = 'D:\mcantat_BDD\projects\code\maya\python\plugIn\toOrientedBoundingBox.py' 
		mc.loadPlugin( plugInPath , qt = True )	
		orientedBoundingBoxCoords = mc.getReelBBCoordsCmds( coords )
		return orientedBoundingBoxCoords


	def utils_setCoordsMesh( self , coords , obj , worldSpace = True ):
		nbrPoints = mc.polyEvaluate( obj , v = True )
		lap = 0
		for i in range( 0 , len(coords) , 3 ):
			if( nbrPoints <= lap ):
				return 0
			mc.xform( "{0}.vtx[{1}]".format( obj , lap ) , t = coords[i:(i+3)] , ws = worldSpace   )
			lap += 1			
		return 1

	def utils_setCoordsCurve( self , coords , obj , worldSpace = True ):
		nbrPoints = self.utils_getNbrPointsCurve( obj )
		lap = 0
		for i in range( 0 , len(coords) , 3 ):
			if( nbrPoints <= lap ):
				return 0
			mc.xform( "{0}.cv[{1}]".format( obj , lap ) , t = coords[i:(i+3)] , ws = worldSpace   )
			lap += 1			
		return 1

	def utils_setCoordsSurface( self , coords , obj , worldSpace = True ):
		return 0

	def utils_getNbrPointsMesh( self , obj ):
		return mc.polyEvaluate( obj , v = True )

	def utils_getNbrPointsCurve( self , obj ):
		#INFO:   CVs = spans + degree  , knot = CVs + degree - 1	
		nbrSpans  = mc.getAttr( obj + '.spans' ) 
		degree    = mc.getAttr( obj + '.degree' )  
		return nbrSpans + degree 

	def utils_getNbrPointsSurface( self , obj ):
		#INFO:   CVs = spans + degree  , knot = CVs + degree - 1	
		nbrSpansU  = mc.getAttr( obj + '.spansU' ) 
		degreeU    = mc.getAttr( obj + '.degreeU' )  
		nbrSpansV  = mc.getAttr( obj + '.spansV' ) 
		degreeV    = mc.getAttr( obj + '.degreeV' )  		
		return ( nbrSpansU + degreeU ) * ( nbrSpansV + degreeV )

	def utils_boundingBoxToDiagonalLength( self , boundingBox ):

		if( len(boundingBox) == 6 ):
			return self.utils_getDistance( boundingBox[0:3] , boundingBox[3:6] )
		if( len(boundingBox) == 4 ):
			return self.utils_getDistance( boundingBox[0:2] , boundingBox[2:4] )

		return -1

	def utils_buildVisuLocators( self , name , coords , parent , allCoords , colorRamp = [ 1.0 , 0 , 0 , 0 , 0 , 1.0  ]  ):
		#INIT
		rgbStart = colorRamp[0:3]
		rgbEnd   = colorRamp[3:6]
		boundingBoxDiagIdealScaleDefaut = 65
		#COMPUTE SCALE
		boundingBox     = self.utils_getBoundingBoxCoords( allCoords , 3 )
		boundingBoxDiag = self.utils_boundingBoxToDiagonalLength( boundingBox )
		scale           = boundingBoxDiag / boundingBoxDiagIdealScaleDefaut
		#BUILD GRP
		toReturn = []
		if( 3 < len(coords) ):
			groupName = name + '_GRP'
			groupName = mc.createNode( 'transform' , n = groupName )
			if not ( parent == '' ):
				mc.parent( groupName , parent )
			parent = groupName
			toReturn.append(groupName)
		#BUILD
		lap = 0
		rgbTmp = rgbStart
		nbrPoints = len( coords ) / 3
		rgbIncr = [ (rgbEnd[0] - rgbStart[0])/nbrPoints , (rgbEnd[1] - rgbStart[1])/nbrPoints , (rgbEnd[2] - rgbStart[2])/nbrPoints ]
		for i in range( 0 , len( coords ) , 3 ):
			#BUILD
			self.trs.value = [ coords[i+0] , coords[i+1] , coords[i+2] , 0 , 0 , 0 , scale , scale , scale ]
			locTmp = self.trs.visualize( '{0}_{1}'.format( name , lap ), parent )
			toReturn.append(locTmp)
			lap += 1
			#COLOR
			mc.setAttr( "{}.overrideEnabled".format( locTmp ) , 1 );	
			mc.setAttr( "{}.overrideRGBColors".format( locTmp ) , 1 );
			mc.setAttr( "{}.overrideColorRGB".format( locTmp ) , rgbTmp[0] , rgbTmp[1] , rgbTmp[2] , type = 'double3' );
			rgbTmp = [ rgbTmp[0] + rgbIncr[0] , rgbTmp[1] + rgbIncr[1]  , rgbTmp[2] + rgbIncr[2]  ]			

		return toReturn
	
	def utils_buildVisuBoundingBox( self , name  , boundingBoxCoords , parent = '' ):
		barycentre = self.utils_getBarycentre( boundingBoxCoords , 3 )
		cube = mc.polyCube( n = name )

		if( len(boundingBoxCoords) == 6 ):
			boundingBoxCoords = self.utils_boundingBoxToCubePoints( boundingBoxCoords )

		self.trs.createFromOrientedBoundingBox( boundingBoxCoords )
		self.trs.toObj( cube[0] )

		if not( parent == '' ):
			mc.parent( cube[0] , parent )


	def utils_boundingBoxToCubePoints( self , boundingBoxCoords ):

		bb = [ boundingBoxCoords[0:3] , boundingBoxCoords[3:6] ]

		cubePoints  = [ bb[0][0] , bb[0][1] , bb[0][2] , bb[1][0] , bb[0][1] , bb[0][2] , bb[1][0] , bb[0][1] , bb[1][2] , bb[0][0] , bb[0][1] , bb[1][2]  ]
		cubePoints += [ bb[0][0] , bb[1][1] , bb[0][2] , bb[1][0] , bb[1][1] , bb[0][2] , bb[1][0] , bb[1][1] , bb[1][2] , bb[0][0] , bb[1][1] , bb[1][2]  ]

		return cubePoints


	def utils_isCoordsClassInstance( self , value ):

		if( type(values) == types.InstanceType ):
			#GET CLASS NAME
			modules = str(values.__class__).split('.')
			className = modules[0]
			if( 1 < len(modules) ):
				className = modules[-1] 

			if( className == 'coords'):
				return 1

		return 0



	def utils_arrayCompareIsInf( self , coordsA , coordsB , axeOrder ):

		coordsAModif = []
		coordsBModif = []
		for i in axeOrder:
			coordsAModif.append( coordsA[i])
			coordsBModif.append( coordsB[i])

		if( coordsAModif < coordsBModif ):
			return True
		else:
			return False

	def utils_removeCoords( self , coords , toRemove ):

		for i in range( 0 , len( coords ) ,  len(toRemove) ):
			if( coords[i:i+len(toRemove)] == toRemove ):
				for j in range( 0 , len(toRemove) ):
					coords.pop(i)
				return coords

		return coords

	def utils_getIndexes( self , array , value ):
		
		indexes = [ 0 , 0 , 0 ]
		sizeValue = len(value)

		for i in range( 0 , len(array) , sizeValue ):
			if( array[i:i+sizeValue] == value ):
				indexes = range( i , i+sizeValue )

		return indexes

	def utils_getDistance( self , pointA , pointB ):

		if( len( pointA ) == 1 ):
			distance = om.MVector( pointB[0] - pointA[0] , 0 , 0 ).length()
		elif( len( pointA ) == 2 ):
			distance = om.MVector( pointB[0] - pointA[0] , pointB[1] - pointA[1] , 0 ).length()
		elif( len( pointA ) == 3 ):
			distance = om.MVector( pointB[0] - pointA[0] , pointB[1] - pointA[1] , pointB[2] - pointA[2] ).length()

		return distance

	def utils_sortReturnIndex( self , values ):
		indexesSorted = []
		#INIT
		indexes = range( 0 , len(values) )
		minValue = 9999999999999999999999999999999999999999999999999999999999999
		valuesToRemove  = values[:]
		#SORT
		while not( len(valuesToRemove) == 0 ):
			minValueTmp = minValue
			for i in range( 0 , len(valuesToRemove) ):
				valueTmp = valuesToRemove[i]
				if( valueTmp < minValueTmp ):
					minValueTmp = valueTmp
					minValueIndex = indexes[i]

			valuesToRemove.remove(minValueTmp)
			indexes.remove( minValueIndex )
			indexesSorted.append( minValueIndex )

		return indexesSorted


	def utils_pointIndexToCoordsIndex( self , pointIndex , nbrAxis ):

		coordsIndexes = []
		for i in range( 0 , len(pointIndex) ):
			for j in range( 0 , nbrAxis ):
				coordsIndexes.append( pointIndex[i]*nbrAxis + j ) 

		return coordsIndexes

	def utils_coordsToTrs( self , coords ):
		trs = [0.0,0.0,0.0,0.0,0.0,0.0,1.1,1.1,1.1] 
		trs[0:len(coords)] = coords
		return trs

	def utils_trsToCoords( self , trs , nbrAxis ):
		return trs[0:nbrAxis]






def filterType( dagObjs , types ):

	filteredObjs = []
	
	for elem in dagObjs:
		for type in types:
			if( mc.nodeType(elem) == type ): 	
				filteredObjs.append(elem)	

	return utilsPython.removeDuplicate(filteredObjs)



def parentsToChildrens( parents , includeParents = False , returnLongName = False ):
	allSceneObj = mc.ls( l = True , r = True );	
	#GET LONG NAME OF PARENT
	parentsLongName = []
	for parent in parents:
		parentsLongName.append( getLongName( parent ) );	    
	#GET CHILDRENS
   	childrensLongName = []
	for obj in allSceneObj:
		for parent in parentsLongName:	    
			if(  len(parent) <= len(obj)  ) and ( obj[0:(len(parent)+1)] == (parent+'|') ):
				childrensLongName.append(obj)    
   	#REMOVE DUPLICATE
   	childrensLongName = utilsPython.removeDuplicate(childrensLongName)   
   	#REMOVE PARENTS
   	if( includeParents == True ):
   		childrensLongName += parentsLongName 
   	#REMOVE PARENTS
   	childrens = childrensLongName
   	if( returnLongName == False ):
		childrens = []
		for children in childrensLongName:
			childrens.append( getShortName( children ) )	
	return childrens
	


def getLongName( shortName ):
    return mc.ls( shortName , l = True , r = True)[0];
    
def getShortName( longName ):
    return mc.ls( longName , l = False , r = True)[0];