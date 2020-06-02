
import math
import copy

import maya.cmds as mc
import maya.OpenMaya as om
import maya.api.OpenMaya as ompy

from ..utils import utilsMaya
from ..utils import utilsPython
from ..utils import utilsMath
from ..utils import utilsMayaApi

from . import trs
from . import coords
from . import boundingBox2d

class layout2dGenerator(mayaClasse):
	
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

		self.bb2d           = boundingBox2d.boundingBox2d()
		self.canvas         = []
		self.blocks         = []
		self.pictures       = []		
		self.newBlockSize   = []
		self.vectorGrowBase = [ 0 , 1 ]
		self.growIncr       = 0.25
		self.debug  = 0
	#_________________________________________________________________CREATE

	def createCanvasFromObjs( self , objs ):
		bb2d  = boundingBox2d.boundingBox2d()
		self.canvas = []
		for obj in objs:
			bb2d.createFromObj( obj )
			self.canvas.append( copy.copy(bb2d) )


	def createBlockFromObjs( self , objs ):
		bb2d  = boundingBox2d.boundingBox2d()
		self.blocks = []
		for obj in objs:
			bb2d.createFromObj( obj )
			self.blocks.append( copy.copy(bb2d) )

	def createPicturesFromObjs( self , objs ):
		bb2d  = boundingBox2d.boundingBox2d()
		self.pictures = []
		for obj in objs:
			bb2d.createFromObj( obj )
			self.pictures.append( copy.copy(bb2d) )

	def getAllLayoutPoints( self ):
		points = []
		for block in self.blocks:
			points += block.squareCoords
		for canva in self.canvas:
			points += canva.squareCoords

		return points



	#_________________________________________________________________MODIF

	def keepRatioGrowFromPoint( self , bb2d , point ):

		angle       = 0
		distMin     = 1
		#EXTRACT FOUR VECTOR
		bb = bb2d.squareCoords
		vbb = om.MVector( bb[0] - bb[4] , bb[1] - bb[5] , 0 )					
		vbb.normalize()
		bbVectors = [ vbb.x , vbb.y , vbb.x , vbb.y*-1 , vbb.x*-1 , vbb.y , vbb.x*-1 , vbb.y*-1 ]

		bb2dGrown = []
		for i in range( 0 , 4 ):
			skip = 0
			#CREATE BB
			vector = [ bbVectors[i*2] * distMin , bbVectors[i*2+1] * distMin ]
			self.bb2d.createFromPointVector( point + vector )
			#SKIP IF IT'S IN BLOCKS OR OUT OF THE CANVAS
			for block in self.blocks:
				if( self.bb2d.isIn(block) ):
					skip = 1
			for canva in self.canvas:
				if( self.bb2d.isOut(canva) ):
					skip = 1

			if( skip == 1 ):
				continue

			self.bb2d.grow( self.growIncr , self.blocks , self.canvas , keepRatio = 1 )	
			bb2dGrown.append( copy.copy(self.bb2d) )

		return bb2dGrown
	

	#_________________________________________________________________MODIF

	def multiDirectionGrowFromPoint( self , point , interval = 22.5 ):

		vector      = self.vectorGrowBase
		nbrInterval = int( 360 / interval)
		angle       = 0
		distMin     = 1
		#GET BB GROW
		angleToAvoid = [ 0 , 90 , 180 , 270 ]
		bb2dGrown = []
		for i in range( 0 , nbrInterval ):
			skip = 0
			#AVOID STRAIGHT ANGLE			
			if( angle in angleToAvoid ):
				angle += 10
			#CREATE BB
			vector = [ math.cos(math.radians(angle)) * distMin , math.sin(math.radians(angle))  * distMin]
			self.bb2d.createFromPointVector( point + vector )
			#SKIP IF IT'S IN BLOCKS OR OUT OF THE CANVAS
			for block in self.blocks:
				if( self.bb2d.isIn(block) ):
					skip = 1
			for canva in self.canvas:
				if( self.bb2d.isOut(canva) ):
					skip = 1

			angleOld = copy.copy(angle) 
			angle += interval

			if( skip == 1 ):
				continue
			#GROW
			'''
			if( self.debug == 85 ) and ( 230 < angleOld  ):
				self.bb2d.debug = 1
				self.bb2d.grow( self.growIncr , self.blocks , self.canvas )
				mc.error()
			'''

			self.bb2d.grow( self.growIncr , self.blocks , self.canvas , keepRatio = 0 )
			#print( self.bb2d.visualize( 'point{}_angle{}'.format( self.debug , int(angleOld) ) ) , point )			
			bb2dGrown.append( copy.copy(self.bb2d) )
		self.debug += 1

		return bb2dGrown
	


	def keepRatioGrowFromPoints( self , bb2d , points ):
		possibleBBs = []
		for i in range( 0 , len(points) , 2 ):
			possibleBBs += self.keepRatioGrowFromPoint( bb2d , points[i:i+2] )
		return possibleBBs


	def setBbOnFreeSpace( self , bbToPlace ):
		points = self.getAllLayoutPoints()
		allpossibleBB = self.keepRatioGrowFromPoints( bbToPlace , points )			
		bestBB = self.getBestBoundingBox2d(allpossibleBB)
		return bestBB
	

	def setBbsOnFreeSpace( self , bbsToPlace ):
		bbsPlaced = []
		stop = 0
		for bbToPlace in bbsToPlace:
			bb = self.setBbOnFreeSpace( bbToPlace )			
			bbsPlaced.append( bb )
			self.blocks.append( bb )			

		return bbsPlaced


	def multiDirectionGrowFromPoints( self , points ):
		possibleBBs = []
		for i in range( 0 , len(points) , 2 ):
			possibleBBs += self.multiDirectionGrowFromPoint( points[i:i+2] )
		return possibleBBs
	
	def getBBFromFreeSpace( self ):
		points = self.getAllLayoutPoints()
		allBBs = self.multiDirectionGrowFromPoints(points)			
		bestBB = self.getBestBoundingBox2d(allBBs)
		return bestBB

	def fillFreeSpaceWithBB( self ):
		maxIter = 50
		curIter = 0

		freeSpaceBB = []
		stop = 0
		while( stop == 0 ):
			#print( 'lap' , curIter , len(self.blocks) )
			bb = self.getBBFromFreeSpace()
			#bb.visualize('toto{}_'.format(curIter))			
			#OUT
			if( bb == None ) or ( maxIter < curIter ):
				stop = 1
			else:
				freeSpaceBB.append( bb )
				self.blocks.append( bb )

			curIter += 1 

		return freeSpaceBB


	#_________________________________________________________________UTILS
	def sortBoundingBoxByArea( self , boundingBox2ds ):
		#GET INFO
		bbAreas = []
		for i in range( 0 , len(boundingBox2ds) ):
			bbAreas.append( boundingBox2ds[i].area ) 

		bbAreasSorted = bbAreas[:]
		bbAreasSorted.sort()
		#SORT
		boundingBox2dsSorted = []
		for i in range( 0 , len(bbAreasSorted) ):
			index = bbAreas.index( bbAreasSorted[i] )
			boundingBox2dsSorted.append( boundingBox2ds[index])

		return boundingBox2dsSorted

	def getBestBoundingBox2d( self , boundingBox2ds ):
		if(len(boundingBox2ds) == 0 ):
			return None

		boundingBox2dsSorted = self.sortBoundingBoxByArea( boundingBox2ds)
		boundingBox2dsSorted.reverse()

		minRatio = 0.04
		bestBB = boundingBox2dsSorted[0] 
		for bb in boundingBox2dsSorted:
			if( minRatio < bb.ratio ):
				bestBB = bb
				break

		return boundingBox2dsSorted[0]

