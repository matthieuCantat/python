

import math
import maya.cmds         as mc
import maya.api.OpenMaya as ompy
from ..utils import utilsMath
from .mayaClasse import *

#from .. import utilsMayaApi


class vector(mayaClasse):
	
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


	def __init__(self , **args ):
		mayaClasse.__init__(self )
		#UTILS	
		#CLASSE
		self.classeType = 'vector'	
		#INSTANCE			
		self.value      = [0,0,0]

		#MODIF
        updateValue = args.get( 'updateValue' , 1             ) 
        toModif     = args.get( 'toModif'     , [ 1 , 1 , 1 ] )
        inValue     = args.get( 'inValue'     , None          )


		def dot( self , vector ):
			pass

		def cross( self , vector ):
			pass        	
		
		def length( self ):
			pass

		def normalize( self ):
			pass        				