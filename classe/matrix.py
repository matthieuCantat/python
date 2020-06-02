

import math
import maya.cmds         as mc
import maya.api.OpenMaya as ompy
from ..utils import utilsMath
from .mayaClasse import *

#from .. import utilsMayaApi


class matrix(mayaClasse):
	
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
		self.classeType = 'matrix'	
		#INSTANCE			
		self.value      = [1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1]	
		#MODIF
        updateValue = args.get( 'updateValue' , 1             ) 
        toModif     = args.get( 'toModif'     , [ 1 , 1 , 1 , 1 ] )
        inValue     = args.get( 'inValue'     , None          )

	def setRow( self , rowNum , vector , **args ):
	def setVectorX( self , rowNum , vector , **args ):
	def setVectorY( self , rowNum , vector , **args ):
	def setVectorZ( self , rowNum , vector , **args ):
	def setPosition( self , rowNum , vector , **args ):
    #CREATE
	def createFromMatrix( self , matrix , **args ):
	def createFromObj( self , mayaObjName , **args ):
	def createFromCoords( self , coords , **args ):
	def createFromCurve( self , mayaCurveName , value , upVector , distanceMode = 0 , inverse = 0 , **args ):
	def createFromTRS( self , TRS , **args ):

    # MODIFY
    def orthogonize( self , vectorNum , **args  ):
    def orthogonizeRow( self , vectorNum , **args  ):

    def normalize( self , vectorNum , **args  ):
    def normalizeRow( self , vectorNum , **args  ):

    def inverse( self , vectorNum , **args  ):
    def inverseAxes( self , inverseAxes ,  **args ):
    def swapAxes( self , inverseAxes ,  **args ):

    # TRANSFORM
	def transform(    self , matrixTrsf , **args ):
	def transformTRS( self , TRS        , **args ):

	def parent(          self , matrixFather  , **args ):	
	def unParent(        self , matrixFather  , **args ):	
	def offsetItself(    self , offsetTrs , **args ):
	def offsetParentTrs( self , parentTrs , offsetTrsUnder  ,  **args ):

	def mirror( self , planSymCoords , unlockAxe = 2 , recomputeAxes = 0 , **args ):	

	def intersectPlan( self , planeCoords , vectorDir , **args  ):		
	def intersectMesh( self , meshName    , vectorDir , **args  ):

	def snapOnLine( self  , lineCoords  , **args ):
	def snapOnPlane( self , planeCoords , **args ):
	def snapOnCurve( self , curveName   , **args ):
	def snapOnMesh( self  , meshName    , **args ):

	def aim(    self , matrix    , axeAim = 0 , axeUp = 1 , upVector = [ 0 , 1 , 0 ] , **args ):
	def setAim( self , vectorAim , axeAim = 0 , axeUp = 1 , upVector = [ 0 , 1 , 0 ] , **args ):

	def blend( self , trsTarget , value = 0.5 , distanceMode = 0 , **args ): 

	def projectAngle( self , trsOrigine , angleOffset , axe ,  updateValue = 1  , toModif = [ 1 , 1 , 1 ] ):

    # OUT
	def toVector( self , obj , worldSpace = 0 , **args ):
	def toMVector( self , obj , worldSpace = 0 , **args ):
	def toPoint( self , obj , worldSpace = 0 , **args ):	
	def toMPoint( self , obj , worldSpace = 0 , **args ):	
	def toTrs( self , obj , worldSpace = 0 , **args ):	
	def toObj( self , obj , worldSpace = 0 , **args ):
	def toMMatrix( self  , **args ):	
	def toRotation( self , rotValueTarget ,  updateValue = 1 ):	#	def getTrsRotateAxeOriented( self , axeDirParent  , axeRotateParent , axeRotateChildren ,  updateValue = 1  , toModif = [ 1 , 1 , 1 ] ):		 
	def toCubeCoords( self  , sortByFace = 0 , **args ):
	def toDistance( self , matrixTarget , **args):
	def toPlaneCoords( self , axeNormal , **args):
	def toClosestAxis( self , vector , returnList = 0 , **args):	
	def toGlRepresentation( self , name = '' , parent = '' ):
	def toPrint()

			
			
	#################################################################################################################################################################################		
	################################################################################################################################################################################# UTILS
	################################################################################################################################################################################# 			


	def utils_perpendicularizeVector( self , vector , vectoRefA , vectorRefB ):
		vectorPerp = vectoRefA.cross(vectorRefB)
		dotPoduct  = vector.dot(vectorPerp)
		vectorOut  = vectorOut.normalize() * vector.length() * sign(dotPoduct)
		return vectorOut


    def utils_getOtherVectorMatrixIndexes( self , indexe ):
		#TO ADJUST INDEX     
		otherIndexes = [ None , None ]       
        if( indexe == 0):
        	otherIndexes = [ 1 , 2 ]    
        elif(indexe == 1):
        	otherIndexes = [ 0 , 2 ]  
        elif(indexe == 2):
        	otherIndexes = [ 0 , 1 ]   

        return otherIndexes   



	def utils_getBoundingBoxCoords( self , coords , **args ):
		nbrAxis = args.get( 'nbrAxis' , 3  ) 
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

	def utils_getBarycentre( self , coords , **args ):
		nbrAxis = args.get( 'nbrAxis' , 3  ) 

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

	def utils_getOrientedBoundingBoxCoords( self , coords ):
		plugInPath = 'D:\mcantat_BDD\projects\code\maya\python\plugIn\toOrientedBoundingBox.py' 
		mc.loadPlugin( plugInPath , qt = True )	
		orientedBoundingBoxCoords = mc.getReelBBCoordsCmds( coords )
		return orientedBoundingBoxCoords

		
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


		
		
		