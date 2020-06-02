
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

class space2d(mayaClasse):
	
	'''
	#_________________________________________________________________CREATE
	createFromCamera
	#_________________________________________________________________OUT
	convertCoords3dTo2d
	convertCoords2dTo3d	
	#_________________________________________________________________UTILS
	utils_getProjectionPlaneCoords
	utils_rotateCoords	
	utils_projectCoordsOnPlane
	utils_getLinePlaneIntersectionPoint
	utils_getClosestPointOnPlane
	utils_get2VectorsNormal
	utils_convertCoords3dToWorld2d
	'''

	def __init__(self):
		self.Coords = coords.coords()
		self.distanceCamCanvas = 10
		self.projectionTR = [ 0 , 0 , 0 , 0 , 0 , 0 ]

		self.canvas3d = [ 0 , 0 , 0 ,  0 , 0 , 0  ,  0 , 0 , 0  ,  0 , 0 , 0 ]
		self.canvas2d = [ 0 , 0     ,  0 , 0      ,  0 , 0      ,  0 , 0     ]		
		self.origine3d     = [ 0 , 0 , 0 ]
		self.origine2d     = [ 0 , 0 ]	
		self.dimention3d   = [ 1 , 1 ]
		self.dimention2d   = [ 1 , 1 ]		
		self.unit3d  = [ 0 , 0 , 0 ,  0 , 0 , 0 ]
		self.unit2d  = [ 1 , 0     ,  0 , 1     ]					


	#_________________________________________________________________CREATE
	def createFromCamera( self , camera ):
		#BASE CAMERA INFO
		self.projectionTR[0:3] = mc.camera( camera , q = True , position = True )
		self.projectionTR[3:6] = mc.camera( camera , q = True , rotation = True )			
		#GET SQUARE COORDS
		projectionAngle	      = [0,0]
		orthographicDimention = [0,0]
		isOrthographic = mc.camera( camera , q = True , orthographic = True )
		if( isOrthographic ):
			width   = mc.camera( camera , q = True , orthographicWidth = True )/2				
			heigth  = mc.camera( camera , q = True , orthographicWidth = True )/2	
			orthographicDimention = [ width , heigth ]			
		else:
			horizontalAngle = mc.camera( camera , q = True , horizontalFieldOfView = True )			
			verticalAngle   = mc.camera( camera , q = True , verticalFieldOfView = True )
			projectionAngle = [ horizontalAngle , verticalAngle ]

		overrideRatio = mc.getAttr( 'defaultResolution.deviceAspectRatio')		
		self.canvas3d = self.utils_getProjectionPlaneCoords( self.projectionTR , '-z' , self.distanceCamCanvas , projectionAngle , orthographicDimention , overrideRatio  )
	
		#GET ORIGINE
		self.origine3d   = self.canvas3d[9:12]
		#GET DIMENTION
		world2d_vectorX = om.MVector( self.canvas3d[6] - self.canvas3d[9] , self.canvas3d[7] - self.canvas3d[10] , self.canvas3d[8] - self.canvas3d[11]  )
		world2d_vectorY = om.MVector( self.canvas3d[0] - self.canvas3d[9] , self.canvas3d[1] - self.canvas3d[10] , self.canvas3d[2] - self.canvas3d[11]  )
		self.dimention3d = [ world2d_vectorX.length() , world2d_vectorY.length() ]			
		#GET vectorBase
		world2d_vectorX.normalize()
		world2d_vectorY.normalize()
		self.unit3d = [ world2d_vectorX.x , world2d_vectorX.y , world2d_vectorX.z , world2d_vectorY.x , world2d_vectorY.y , world2d_vectorY.z ]		
		#GET 2D VERSION
		self.canvas2d = [ 0 , self.dimention3d[1]     ,  self.dimention3d[0]  , self.dimention3d[1]       ,  self.dimention3d[0] , 0      ,  0 , 0     ]	
		self.origine2d     = [ 0 , 0 ]	
		self.dimention2d   = [ world2d_vectorX.length() , world2d_vectorY.length() ]				
		self.unit2d  = [ 1 , 0     ,  0 , 1   ]	


	#_________________________________________________________________OUT

	def to2d( self , coords3d ):
		coords2d = []
		for i in range( 0 , len(coords3d) , 3 ):
			coord3dOnPlane = self.utils_projectCoordsOnPlane( coords3d[i:i+3] , self.canvas3d[0:9] , self.projectionTR[0:3]  )
			coord2d        = self.utils_convertCoords3dToWorld2d( self.origine3d , self.unit3d , coord3dOnPlane )
			coords2d += coord2d
		return coords2d

	def to3d( self , coords2d ):
		coords3d = []
		for i in range( 0 , len(coords2d) , 2 ):
			coord3d = self.origine3d[:]
			coord3d[0] += self.unit3d[0] * coords2d[0] + self.unit3d[3] * coords2d[1]   
			coord3d[1] += self.unit3d[1] * coords2d[0] + self.unit3d[4] * coords2d[1]
			coord3d[2] += self.unit3d[2] * coords2d[0] + self.unit3d[5] * coords2d[1]
			coords3d   += coord3d
		return coords3d

	#_________________________________________________________________UTILS

	def utils_getProjectionPlaneCoords( self , projectionTR , axeDir = '-z' , distanceCameraPlane = 10 , projectionAngle = [ 45 , 45 ] , orthographicDimention = [0,0] , overrideRatio = None  ):
		axis = [ 'x' , 'y' , 'x' ] 	
		#INIT INFO
		dictAxeDirToTripleVector = {}
		dictAxeDirToTripleVector['x']  = [ 1,0,0 , 0,1,0 , 0,0, 1]
		dictAxeDirToTripleVector['y']  = [ 1,0,0 , 0,1,0 , 0,0, 1]
		dictAxeDirToTripleVector['z']  = [-1,0,0 , 0,1,0 , 0,0, 1]
		dictAxeDirToTripleVector['-x'] = [-1,0,0 , 0,1,0 , 0,0,-1]
		dictAxeDirToTripleVector['-y'] = [-1,0,0 , 0,1,0 , 0,0, 1]
		dictAxeDirToTripleVector['-z'] = [ 1,0,0 , 0,1,0 , 0,0,-1]	
		dictAxeDirToAxeDirIndex  = { 'x':0 , 'y':1 , 'z':2 , '-x':0 , '-y':1 , '-z':2 }
		dictAxeDirToAxeUpIndex   = { 'x':1 , 'y':2 , 'z':1 , '-x':1 , '-y':2 , '-z':1 }
		dictAxeDirToAxeSideIndex = { 'x':2 , 'y':0 , 'z':0 , '-x':2 , '-y':0 , '-z':0 }
		#GET AXIS INFO		
		tripleVector = dictAxeDirToTripleVector[axeDir]
		axeDirIndex  = dictAxeDirToAxeDirIndex[axeDir]
		axeUpIndex   = dictAxeDirToAxeUpIndex[axeDir]
		axeSideIndex = dictAxeDirToAxeSideIndex[axeDir] 		
		#GET VECTEUR PROJECTION DIR							
		for i in range( 0 , 3 ):
			tripleVector = self.utils_rotateCoords( tripleVector , [ 0 , 0 , 0 ] , axis[i] , projectionTR[i+3] )		
		vProjectionDir = [ tripleVector[axeDirIndex*3] , tripleVector[axeDirIndex*3+1]  , tripleVector[axeDirIndex*3+2] ]
		#GET PROJECTION PLANE CENTER
		projPlaneCenter = [ projectionTR[0] + vProjectionDir[0]*distanceCameraPlane , projectionTR[1] + vProjectionDir[1]*distanceCameraPlane , projectionTR[2] + vProjectionDir[2]*distanceCameraPlane ]	
		print('projPlaneCenter' , projPlaneCenter)
		#GET WIDTH HEIGTH VALUE
		canvasHalfWidth  = abs( math.tan( math.radians( projectionAngle[0] /2) ) * distanceCameraPlane )
		canvasHalfHeight = abs( math.tan( math.radians( projectionAngle[1] /2) ) * distanceCameraPlane )
		if not( orthographicDimention == [0,0] ):
			canvasHalfWidth  = orthographicDimention[0]
			canvasHalfHeight = orthographicDimention[1]					
		#GET WIDTH HEIGTH VALUE
		if not( overrideRatio == None ):
			canvasHalfHeight = canvasHalfWidth / overrideRatio
		# GET VECTOR CENTER-SIDE & VECTOR CENTER-TOP  !!!
		vCenterSide  = [ tripleVector[axeSideIndex*3] * canvasHalfWidth  , tripleVector[axeSideIndex*3+1] * canvasHalfWidth  , tripleVector[axeSideIndex*3+2] * canvasHalfWidth  ] 
		vCenterTop   = [ tripleVector[axeUpIndex*3]   * canvasHalfHeight , tripleVector[axeUpIndex*3+1]   * canvasHalfHeight , tripleVector[axeUpIndex*3+2]   * canvasHalfHeight ] 		
		print('vCenterSide' , vCenterSide)
		print('vCenterTop'  , vCenterTop )		
		#COMPUTE FOUR CORNER
		cornerA =  [ projPlaneCenter[0] - vCenterSide[0] + vCenterTop[0] , projPlaneCenter[1] - vCenterSide[1] + vCenterTop[1] , projPlaneCenter[2] - vCenterSide[2] + vCenterTop[2] ]
		cornerB =  [ projPlaneCenter[0] + vCenterSide[0] + vCenterTop[0] , projPlaneCenter[1] + vCenterSide[1] + vCenterTop[1] , projPlaneCenter[2] + vCenterSide[2] + vCenterTop[2] ]
		cornerC =  [ projPlaneCenter[0] + vCenterSide[0] - vCenterTop[0] , projPlaneCenter[1] + vCenterSide[1] - vCenterTop[1] , projPlaneCenter[2] + vCenterSide[2] - vCenterTop[2] ]
		cornerD =  [ projPlaneCenter[0] - vCenterSide[0] - vCenterTop[0] , projPlaneCenter[1] - vCenterSide[1] - vCenterTop[1] , projPlaneCenter[2] - vCenterSide[2] - vCenterTop[2] ]
		return cornerA + cornerB + cornerC + cornerD

	@staticmethod
	def utils_rotateCoords( coords , piv , axe , value ):	
		#GET INDEX ORDER 
		dictAxe  = { 'x' : [ 1 , 2 , 0 ]  ,  'y' : [ 0 , 2 , 1 ]   ,  'z' : [ 0 , 1 , 2 ] }	
		io       = dictAxe[ axe ]
		#EXCEPTION		
		if( axe == 'y' ): value *= -1    		
		#COMPUTE ROTATION			
		rotRad = math.radians(value)	
		newVertexCoords = []	
		for i in range( 0 , len(coords) , 3 ):	
			newCoord = [ 0 , 0 , 0 ]	
			newCoord[ io[0] ] = math.cos( rotRad ) * ( coords[ i+io[0] ] - piv[ io[0] ] )  -  math.sin( rotRad ) * ( coords[ i+io[1] ] - piv[ io[1] ] )  +  piv[ io[0] ]        
			newCoord[ io[1] ] = math.sin( rotRad ) * ( coords[ i+io[0] ] - piv[ io[0] ] )  +  math.cos( rotRad ) * ( coords[ i+io[1] ] - piv[ io[1] ] )  +  piv[ io[1] ]              
			newCoord[ io[2] ] = coords[ i+io[2] ] 		
			newVertexCoords += newCoord
					    
		return newVertexCoords






	def utils_projectCoordsOnPlane( self , coords , planeCoords , origine ):
		lineCoords = [ origine[0] , origine[1] , origine[2] , coords[0] , coords[1] , coords[2] ]
		intersectPoint = self.utils_getLinePlaneIntersectionPoint( lineCoords , planeCoords ) 
		return intersectPoint

	def utils_getLinePlaneIntersectionPoint( self , lineCoords , planeCoords ):
		#GET CLOSEST POINT
		closestPointPlane = self.utils_getClosestPointOnPlane( lineCoords[0:3] , planeCoords )
		print( 'lineCoords'        , lineCoords        )
		print( 'planeCoords'       , planeCoords       )
		print( 'closestPointPlane' , closestPointPlane )
		#GET ANGLE CLOSEST POINT PLANE - lineO - lineEND	
		vPlaneLineO = om.MVector( closestPointPlane[0] - lineCoords[0] , closestPointPlane[1] - lineCoords[1] , closestPointPlane[2] - lineCoords[2] )
		vline = om.MVector( lineCoords[3] - lineCoords[0] , lineCoords[4] - lineCoords[1] , lineCoords[5] - lineCoords[2] ) 
		dotPoduct = math.copysign( 1 , vline*vPlaneLineO )
		vline *= dotPoduct
		angle = vline.angle(vPlaneLineO)
		print( 'angle' , angle )
		#DISTANCE CLOSEST POINT PLANE
		distClosestPointPlane = vPlaneLineO.length()
		#TRIGO: GET DISTANCE LINE ORIGINE - INTERSECTION POINT
		distLineOInter  = abs(distClosestPointPlane / math.cos(angle) )
		#GET INTERSECTION POINT
		vline.normalize()	
		vline *= distLineOInter 	
		intersectionPoint = [ vline.x + lineCoords[0] , vline.y + lineCoords[1] , vline.z + lineCoords[2] ]
		print( 'intersectionPoint' , intersectionPoint )
		return intersectionPoint

	def utils_getClosestPointOnPlane( self , coords , planeCoords ):
		#GET PLANE NORMAL
		planVectorA      =  [ ( planeCoords[3] - planeCoords[0] ) , ( planeCoords[4] - planeCoords[1] ) , ( planeCoords[5] - planeCoords[2] )  ] 
		planVectorB      =  [ ( planeCoords[6] - planeCoords[0] ) , ( planeCoords[7] - planeCoords[1] ) , ( planeCoords[8] - planeCoords[2] )  ] 	
		normalDir        =  [ ( planeCoords[0] - coords[0]    )   , ( planeCoords[1] - coords[1]    )   , ( planeCoords[2] - coords[2]      )  ] 			
		vPlaneNormal = self.utils_get2VectorsNormal( planVectorA , planVectorB , normalDir  )
		#GET d OF THE PLAN EQUATION  2x + 3y + 7z +d = 0	
		d = ( ( vPlaneNormal[0] *  planeCoords[0] ) + ( vPlaneNormal[1] *  planeCoords[1] ) + ( vPlaneNormal[2] *  planeCoords[2] ) ) * -1 
		#GET DIST BETWEEN POINT AND PLANE
		dist = (  - ( vPlaneNormal[0] * coords[0] ) - ( vPlaneNormal[1] * coords[1] ) - ( vPlaneNormal[2] * coords[2] ) - d  ) / ( ( vPlaneNormal[0] * vPlaneNormal[0] ) + ( vPlaneNormal[1] * vPlaneNormal[1] ) + ( vPlaneNormal[2] * vPlaneNormal[2] )   ) 		
		#GET INTERSECT COORDS		
		iCoords = [  vPlaneNormal[0] * dist + coords[0] , vPlaneNormal[1] * dist + coords[1] , vPlaneNormal[2] * dist + coords[2] ] 
		return iCoords
	
	@staticmethod	
	def utils_get2VectorsNormal( vectorA , vectorB , vDir ):
		#GET NORMAL
		normalx = ((vectorA[1])*(vectorB[2])-(vectorA[2])*(vectorB[1]))
		normaly = ((vectorA[2])*(vectorB[0])-(vectorA[0])*(vectorB[2]))
		normalz = ((vectorA[0])*(vectorB[1])-(vectorA[1])*(vectorB[0]))
		vecteurNormal = ompy.MVector( normalx   , normaly   , normalz   )
		#GET MODIF IT WITH VECTOR DIR
		vectorDirection   = ompy.MVector( vDir[0] , vDir[1] , vDir[2] ) 	
		coef = math.copysign( 1 , vecteurNormal*vectorDirection )		
		vecteurNormal = ompy.MVector( vecteurNormal.x * coef , vecteurNormal.y * coef  , vecteurNormal.z * coef  )
		return [ vecteurNormal.x , vecteurNormal.y , vecteurNormal.z ] 		
			 

	@staticmethod	
	def utils_convertCoords3dToWorld2d( origine , unitVectors , coords ):
		#GET UNIT VECTORS
		vUnitX = om.MVector( unitVectors[0] , unitVectors[1] , unitVectors[2] )
		vUnitY = om.MVector( unitVectors[3] , unitVectors[4] , unitVectors[5] )
		#COORDS ORIGINE INFO
		vCoordsO = om.MVector( coords[0] - origine[0] , coords[1] - origine[1] , coords[2] - origine[2] )
		distCoordsO = vCoordsO.length()
		# COODS ORIGINE UNIT INFO
		angeCoordsOX = vCoordsO.angle(vUnitX)
		angeCoordsOY = vCoordsO.angle(vUnitY)
		# GET 2D UNIT VALUE
		xValue = distCoordsO * math.sin(angeCoordsOY)
		yValue = distCoordsO * math.sin(angeCoordsOX)
		return [ xValue , yValue ]


