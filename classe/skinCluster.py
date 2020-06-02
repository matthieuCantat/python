'''
#******************************************************** BUILD EXEMPLE 
import maya.cmds as mc
import python
from python.classe.skinCluster import *
reload( python.classe.skinCluster)


reload( python.classe.readWriteInfo)

#CREATE
anim = skinCluster()	
anim.createFromSelection()
anim.delete()
anim.toObjs() 

anim.toObjs( inverse = True , startFrame = 1080 ) 

anim.getInfo() 
anim.getObjs() 
anim.getMatchObjs('l_reactorArmPropulsorHandle_CTRL') 

anim.toMatchSelection( mirror = 'X' , replace = True )

mc.select(anim.goMatchObjs('l_reactorArmPropulsorHandle_CTRL'))



#CREATE FROM FILE
anim.delete()
path = 'D:/mcantat_BDD/projects/cute/carrierShipD/maya/scenes/animCurves/test.xml'
anim.toFile( path , info = 'test test test 123 ultime' )

newAnim = animCurve()	
newAnim.createFromFile(path)
newAnim.toObjs()
newAnim.getInfo() 
newAnim.getObjs() 
newAnim.objsAttrs




'''


import maya.cmds as mc
import math
import copy


from . import coords as coordsClasse
from . import readWriteInfo
from ..utils import utilsMaya
from ..utils import utilsPython
from ..utils import utilsMath
from ..utils import utilsMayaApi
from .mayaClasse import *
from .trsBackUp import *
from .buildName import *

import maya.OpenMaya as om 
import maya.OpenMayaAnim as oma



class skinCluster(mayaClasse):
	
	'''
	#________________________________________________________________CREATE
	createFromCurve
	createFromCurves
	createFromSelection
	createFromFile
	#________________________________________________________________MODIF
	modify
	copy
	mirror
	delete
	#________________________________________________________________OUT
	toCurve
	toSelectedCurve	
	toSaveFile
	selectionToFile
	printAttrs
	#________________________________________________________________UTILS	
	utils_rotateCoordsWithAxeOrient
	utils_separateCoords
	utils_mergeCoords
	utils_buildCurveShape
	utils_getCurveShapeCoords
	utils_getKnotIndexes
	'''
	
	def __init__(self):

		self.type      = 'animCurve'
		self.debug     = 0		
		#CURVE INFO	
		self.filePath  = ''	
		self.info      = ''
		self.nodes       = []
		self.objsAttrs   = []
		self.times       = []
		self.values      = []
		self.tLock       = []
		self.tWeightLock = []
		self.tInType     = []
		self.tInX        = []
		self.tInY        = []
		self.tOutType    = []
		self.tOutX       = []
		self.tOutY       = []
		self.breakdown   = []
		self.others      = []


	def printAttrs( self , title = '' , printInfo = 1 ):
		if( printInfo == 1 ):
			print('START_____________________________ ' + title)
			print('**********ATTRS***********')
			for i in range(0,len(self.objsAttrs )):
				print( '{} {}'.format( self.objsAttrs[i] , self.values[i] ) )
			print('END________________________________ ' + title)

	#________________________________________________________________CREATE

	def createFromObjs( self , objs , worldSpace = False , convertConstraint = False ):
		print('animCurve createFromObjs')
		self.meshs    = []
		self.vtxNbr   = []
		self.joints   = []
		self.vertices = []
		self.weights  = []

		for obj in objs:

			shapes     = mc.listRelatives( obj , c = True , s =  True , f = True)
			skinInput = None
			for shape in shapes:
				skinInput  = mc.listConnections( shape , s = True , d = False , t = "skinCluster" )
				if not( skinInput == None ): break

			vtxNbr     = mc.polyEvaluate(  obj , v = True )
			contraints = utilsMaya.getConstraintMasters( obj , constraintTypesFilter = [ 'parentConstraint' ] )
			
			if not( skinInput == None ):
				dataSkin = getSkinWeights(skinInput[0])

				mesh = dataSkin.keys()[0]
				joints = dataSkin[mesh].keys()

				vertices = []
				weights  = []
				for joint in joints:
					vertices.append( dataSkin[mesh][joint][0] )
					weights.append(  dataSkin[mesh][joint][1] )

				self.meshs.append(    obj      )
				self.vtxNbr.append(   vtxNbr   )
				self.joints.append(   joints   )
				self.vertices.append( vertices )
				self.weights.append(  weights  )
			
			elif(convertConstraint == True) and ( 0 < len(contraints) ):
				vtxNbr        = mc.polyEvaluate(  obj , v = True )
				vtxIndexList  = range(0,vtxNbr)
				vtxWeightList = [1]*vtxNbr
				self.meshs.append(    obj               )
				self.vtxNbr.append(   vtxNbr            )
				self.joints.append(   [ contraints[0] ] )
				self.vertices.append( [ vtxIndexList  ] )
				self.weights.append(  [ vtxWeightList ] )
			else:
				print('\tskinCluster.createFromObjs: SKIP ---> {} '.format(obj) )


		return 1
		

	def createFromSelection( self ):
		selection = mc.ls(sl=True)
		self.createFromObjs( selection )
		return 1

	def createFromFile( self , filePath , latest = 1 ):
		print('animCurve createFromFile')
		self.filePath = filePath
		#GET INFO FROM FILE				
		ReadWriteInfo = readWriteInfo.readWriteInfo()
		ReadWriteInfo.createFromFile( self.filePath , latest = latest)				
		dictSkin = ReadWriteInfo.dict	
		#FILL CLASS ATTR
		self.meshs    = [ key for key in dictSkin.keys() ]
		self.vtxNbr   = []
		self.joints   = []
		self.vertices = []
		self.weights  = []


		for mesh in self.meshs:
			self.vtxNbr.append(   dictSkin[mesh][0] )
			self.joints.append(   dictSkin[mesh][1] )  
			self.vertices.append( dictSkin[mesh][2] )      
			self.weights.append(  dictSkin[mesh][3] )       
    

		self.printAttrs( 'createFromFile' , self.debug )				
		return 1		


	#________________________________________________________________MODIF

	def delete(self):
		mc.delete(self.nodes)


	#________________________________________________________________OUT
	def toFile( self , filePath , info = None , incr = 1 , clearOldVar = 1):
		print('animCurve toFile')
		self.filePath = filePath
		#GET INFO FROM FILE				
		ReadWriteInfo = readWriteInfo.readWriteInfo()

		dictSkin = {}
		for i in range(0,len(self.meshs)):
			key = self.meshs[i]
			dictSkin[key] = []
			dictSkin[key].append( self.vtxNbr      [i] )
			dictSkin[key].append( self.joints      [i] )
			dictSkin[key].append( self.vertices    [i] )
			dictSkin[key].append( self.weights     [i] )

		#SAVE DICO IN FILE
		ReadWriteInfo.dict = dictSkin			
		ReadWriteInfo.toFile( self.filePath , incr = incr , clearOldVar = clearOldVar )

		self.printAttrs( 'toFile' , self.debug )		
		return 1

	def getInfo( self ):
		return self.info

	def getRange( self ):

		min = 999999999999999999999999.0
		max = -99999999999999999999999.0

		for i in range(len(self.times)):
			for j in range(len(self.times[i])):
				if(       self.times[i][j] < min ): min = self.times[i][j]
				if( max < self.times[i][j]       ): max = self.times[i][j]

		return [ min , max ]

	def getObjs( self ):
		objs = []
		for i in range(0,len(self.objsAttrs)):
			objs.append( self.objsAttrs[i].split('.')[0] )

		objs = list(set(objs))
		return objs

	def selectObjs( self ):
		mc.select(self.getObjs())

	def getNodes( self ):
		return self.nodes

	def getMatchObjs( self , objToMatch ):
		objs = self.getObjs()

		Names = buildName()
		convertedObjs = Names.convertNamesToMatchExemple( objs , objToMatch )

		return convertedObjs


	def toObjs( self , **args ):

		dataSkin = {}
		for i in range(0,len(self.meshs)):
			mesh = self.meshs[i]
			dataSkin[mesh] = {}
			for j in range(0,len(self.joints[i])):
				joint = self.joints[i][j]
				dataSkin[mesh][joint] = [[],[]]
				dataSkin[mesh][joint][0] = self.vertices[i][j]
				dataSkin[mesh][joint][1] = self.weights [i][j]

		for i in range(0,len(self.meshs)):

			skip = 0
			if not( mc.objExists(self.meshs[i]) ):
				print('skinCluster.toObjs - SKIP SKINNING - MESH doesnt exists - {}'.format(self.meshs[i]) )
				skip = 1

			joints = dataSkin[self.meshs[i]].keys()
			for joint in joints:
				if not( mc.objExists(joint) ):
					print('skinCluster.toObjs - SKIP SKINNING - JOINT doesnt exists - {}'.format(joint) )
					skip = 1

			if( skip ):continue

			skinInput = mc.listConnections( self.meshs[i] , s = True , d = False , t = "skinCluster" )
			if( skinInput == None ):
				mesh   = self.meshs[i]
				joints = dataSkin[self.meshs[i]].keys()
				mc.select( joints )
				skinInput = mc.skinCluster( joints, mesh , normalizeWeights = 1 , bindMethod = 0 , includeHiddenSelections = True , maximumInfluences = 4 , toSelectedBones = True )

				setSkinWeights(skinInput[0],dataSkin)
			else:
				setSkinWeights(skinInput[0],dataSkin)


	def combineData( self , newMeshName ):
		
		combinedMeshs  = [newMeshName]
		combinedVtxNbr = [0]
		combinedJoints   = [[]]
		combinedVertices = [[]]
		combinedWeights  = [[]]			
		#CONVERT INDEX 
		offset = 0
		verticesOffseted = copy.deepcopy(self.vertices)

		for i in range( 0 , len(self.meshs) ):
			for j in range( 0 , len(self.joints[i]) ):
				for k in range( 0 , len(self.vertices[i][j]) ):
					verticesOffseted[i][j][k] = self.vertices[i][j][k] + offset

			vtxNbr = self.vtxNbr[i]
			offset = offset + vtxNbr
			combinedVtxNbr[0] += vtxNbr


		#MERGE SIMILAR JOINTS	
		for i in range( 0 , len(self.meshs) ):
			for j in range( 0 , len(self.joints[i]) ):
				
				iJoint = len(combinedJoints[0])
				if( self.joints[i][j] in combinedJoints[0] ):
					iJoint = combinedJoints[0].index(self.joints[i][j])
				else:
					combinedJoints[0].append( self.joints[i][j] )
					combinedVertices[0].append( [] )
					combinedWeights[0].append(  [] )

				combinedVertices[0][iJoint] += verticesOffseted[i][j]
				combinedWeights[0][iJoint]  += self.weights[i][j]

		#OVERRIDE VALUES
		self.meshs    = combinedMeshs
		self.vtxNbr   = combinedVtxNbr
		self.joints   = combinedJoints
		self.vertices = combinedVertices
		self.weights  = combinedWeights		

	def toCombinedObj( self , name ):
		oldMeshes = self.meshs[:]
		self.combineData(name)

		newMesh = mc.polyUnite( oldMeshes )[0]
		mc.DeleteHistory(newMesh)
		mc.rename(newMesh,name)
		self.toObjs()	
		return name

	def toMatchObjs( self , objToMatch , **args ):
		args['matchObjName'] = objToMatch	
		self.toObjs( **args )
		return 1    

	def toMatchSelection( self , **args ):
		args['matchObjName'] = mc.ls(sl=True)[0]	
		self.toObjs( **args )
		return 1    

	def toSelection( self  , **args ):	
		args['objsToFilter'] = mc.ls( sl = True )	
		self.toObjs( **args )	
		return 1




	#________________________________________________________________UTILS

def convertConstraintToSkin( objs ):
	
	vectexCount = []
	joints      = []
	for i in range( len(objs) ):
		contraints = getConstraintMasters( objs[i] , constraintTypesFilter = [ 'parentConstraint' , 'scaleConstraint'  ] , deleteConstraint = 1 )
		if( len(contraints) == 0 ):mc.error( 'convertConstraintToSkin: no constraint on --> {} '.format(objs[i]) )
		joints.append( contraints[0] )
		vectexCount.append( mc.polyEvaluate(  objs[i] , v = True ) )		

	if( len(objs) == 1 ): newMesh = objs[0]
	else:                 newMesh = mc.polyUnite( objs )[0]
	mc.DeleteHistory(newMesh)	

	mc.select( joints )
	skinClusterNode = mc.skinCluster( joints,  newMesh , normalizeWeights = 1 , ignoreHierarchy = True , includeHiddenSelections = True , maximumInfluences = 4 , toSelectedBones = True )[0]

	currentVtx = 0
	vertJointWeightData = []
	for i in range( len(objs)):
		for j in range( currentVtx , currentVtx + vectexCount[i] ):
			vertJointWeightData.append(    ( '{}.vtx[{}]'.format(newMesh,j) , [(joints[i], 1.0)] )    )
		currentVtx += vectexCount[i]

	utilsMayaApi.setSkinWeights( skinClusterNode, vertJointWeightData )	

	return newMesh




def rebindWithIncrMesh( skinnedMeshBaseName ):
	skinnedMesh = mc.ls( skinnedMeshBaseName + "*" , type = "transform" )[-1]
	shape = mc.listRelatives( skinnedMesh , c = True , s = True )[0]
	skinClusterNode = mc.listConnections( shape + '.inMesh' , s = True , d = False )[0]
	joints = mc.listConnections( skinClusterNode + '.matrix' , s = True , d = False , type = 'joint' )
	
	mc.setAttr( skinClusterNode + '.envelope' , 0 )
	newMesh = mc.duplicate( skinnedMesh )[0]
	mc.select( joints )
	mc.skinCluster( joints,  newMesh , toSelectedBones = True )
	mc.copySkinWeights( skinnedMesh , newMesh , noMirror = True , surfaceAssociation = 'closestPoint' , influenceAssociation  = 'closestJoint' )   
	mc.setAttr( skinnedMesh + '.visibility' , 0 )


	
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
	
	


	
def getSkinWeights( skinCluster ):	
	# dataSkin[shape][joint][0] ---> indexes
	# dataSkin[shape][joint][1] ---> weights
	dataSkin = {} 
	#convert the vertex component names into vertex indices

	shape  = mc.skinCluster( skinCluster , q = True , g = True )[0]
	obj    = mc.listRelatives(shape,p=True)[0]
	vtxNbr = mc.polyEvaluate( obj , v = True )
	joints = mc.skinCluster( skinCluster , q = True , weightedInfluence = True )

	idxJointWeight = []
	for i in range(0,vtxNbr):	
		idxJointWeight.append( (i,[]) )
	    
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
	
	dataSkin[obj] = {}
	for i in range(0,vtxNbr):	   
		#we need to use the api to query the physical indices used    
		weightsP.selectAncestorLogicalIndex( i, weightListObj )  
		weightsP.getExistingArrayAttributeIndices( tmpIntArray )
		
		weightFmtStr = baseFmtStr % i +'.weights[%d]'
		
		#at this point using the api or mel to set the data is a moot point...  we have the strings already so just use mel      	
		for j in range(0,len(joints)):
			infIdx = jApiIndices[ joints[j] ]
			weight = mc.getAttr( weightFmtStr % infIdx )	 
			if( 0 < weight ):
				if not( joints[j] in dataSkin[obj].keys() ):
					dataSkin[obj][joints[j]] = [[i],[weight]]
				else:
					dataSkin[obj][joints[j]][0].append(i)
					dataSkin[obj][joints[j]][1].append(weight)

	return dataSkin
	
	
def setSkinWeights( skinCluster, dataSkin ):	
	# dataSkin[shape][joint][0] ---> indexes
	# dataSkin[shape][joint][1] ---> weights
	shape  = mc.skinCluster( skinCluster , q = True , g = True )[0]
	obj    = mc.listRelatives(shape,p=True)[0]
	vtxNbr = mc.polyEvaluate( obj , v = True )
	skinFn = API_skinClusterClass( skinCluster )
	
	#construct a dict mapping joint names to joint indices    
	jApiIndices = {}  
	_tmp = om.MDagPathArray()    
	skinFn.influenceObjects( _tmp )    
	
	for n in range( _tmp.length() ):
		jApiIndices[ str( _tmp[n].partialPathName() ) ] = skinFn.indexForInfluenceObject( _tmp[n] )    	
		
	#GET PLUGS
	weightListP   = skinFn.findPlug( "weightList" )        
	weightListObj = weightListP.attribute()        
	weightsP      = skinFn.findPlug( "weights" )
	
	#CLEAN out any existing skin data
	tmpIntArray = om.MIntArray() 
	for i in range( 0 , vtxNbr ):
		weightsP.selectAncestorLogicalIndex( i, weightListObj )  
		weightsP.getExistingArrayAttributeIndices( tmpIntArray )

		for n in range( tmpIntArray.length() ):   
			wAttr = '{}.weightList[{}].weights[{}]'.format(skinCluster,i,tmpIntArray[n]) 	
			mc.removeMultiInstance( wAttr )

	#SET DATA
	for joint in dataSkin[obj].keys():
		for i in range( len(dataSkin[obj][joint][0]) ):
			index  = dataSkin[obj][joint][0][i]
			weight = dataSkin[obj][joint][1][i]

			wAttr = '{}.weightList[{}].weights[{}]'.format(skinCluster,index,jApiIndices[ joint ])
			mc.setAttr( wAttr, weight )	

	


		
