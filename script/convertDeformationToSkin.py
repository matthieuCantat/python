

'''
	name:  copySkinNurbsToMesh
	type:  RIGGING
	tag:   skin
	date:  01/01/2016	
	input: select 1 nurbs and 1 mesh

	convert the skin nurbs ( with his nurbs deformation ) to a skin for mesh.
	the nurbs must be freeze and skinned.
'''


import maya.cmds as mc
import maya.OpenMaya as om 
import maya.api.OpenMaya as ompy
import maya.OpenMayaAnim as oma
import time


#convertDefToSkin( 'pCube2' , 'pCube1')
#=========================================================================================================================================================    
#=============================================================================================================================================== MAIN PROC
#=========================================================================================================================================================


def convertDefToSkin( defMesh , skinMesh , joints = None ):

	moveVectors = [ [1 , 0 , 0] , [0 , 1 , 0] , [0 , 0 , 1] ]   

	if( joints == None ):
		joints = mc.ls(type='joint')


	baseCoords = API_getAllVertexCoords( defMesh )                                                                                  

	inf = {}                                                                                                                                                                                                                                                  
	for joint in joints:

		deltaAverage = [ 0 for i in range( 0 , len(baseCoords) ) ]                                                                                                           
		for vector in moveVectors:                                                                                            
			info = moveJoint( joint , vector , None )                                                                                                                                                                                           
			movedCoords = API_getAllVertexCoords( defMesh )                                                                                                                                                                                    
			moveJoint( joint , vector , info )                                                                                         
			delta = getDistanceArray( movedCoords , baseCoords )
			for i in range( 0 , len(deltaAverage) ):
				deltaAverage[i] += delta[i]

		for i in range( 0 , len(deltaAverage) ):
			deltaAverage[i] /= len( moveVectors )

		print( joint , deltaAverage )
		inf[joint] = convertDistanceToInfs( deltaAverage , 1 )                                                                           
			
		
	newSkinCluster = makeSkinCluster( skinMesh , joints , inf )		

	print( '===== DONE =====' )		



#=========================================================================================================================================================    
#===============================================================================================================================================      PROC
#=========================================================================================================================================================
    

def getNurbsAndMeshFromSelection():
	
	meshs , nurbs = [] , []
	
	selection = mc.ls( sl = True )
	
	for elem in selection:
		
		type = mc.nodeType( elem )
		
		if not ( type == 'transform'  ):
			continue

		childrens = mc.listRelatives( elem , c = True , s = True )
		
		type =  mc.nodeType( childrens[0] )
		
		if( type == 'mesh'):
			meshs.append( elem  ) 
		elif( type == 'nurbsSurface'):
			nurbs.append( elem ) 

	return [ nurbs , meshs ]












#------------------------------------------------------------------------------------------------------------------------------            // getSkinCluster 




def getSkinCluster( skinnedObjs ):	
	skinClusters = []
	for skinnedObj in skinnedObjs:

		objShapes = mc.listRelatives(skinnedObj, c=1, s=1)

		for objShape in objShapes:
			skinCluster = mc.listConnections(objShape, d=0, s=1, type="skinCluster")
			if( skinCluster == None ):
				continue
			skinClusters.append( skinCluster[0] )	

	return skinClusters	

	
def getJointMultipleSkins(skinnedObjs):

    allSkinJoints = []
    for skinnedObj in skinnedObjs:

        objShapes = mc.listRelatives(skinnedObj, c=1, s=1)

        for objShape in objShapes:
            skinClusters = mc.listConnections(objShape, d=0, s=1, type="skinCluster")

            id = mc.nodeType(skinClusters)
            if id == 'skinCluster':
                joints =  mc.skinCluster( skinClusters , q = True , inf = True  )

            skinJoints = arrayRemoveDuplicates(joints)
        allSkinJoints.extend(skinJoints)

    return allSkinJoints

	
#------------------------------------------------------------------------------------------------------------------------------            //  getJoints 



def arrayRemoveDuplicates(objs):
	list = []
	for obj in objs:
		if not obj in list:
			list.append(obj)

	return list



def getJoints( skinClusters ):
	
	allSkinJoints = []
	
	for skinCluster in skinClusters:	
		
		id = mc.nodeType( skinCluster )
		if id == 'skinCluster':
		    joints = mc.listConnections( skinCluster, s=1, c=0, d=0, type='joint')
		
		skinJoints = arrayRemoveDuplicates( joints )
		
		allSkinJoints.extend( skinJoints )
		
	return allSkinJoints


	
	
	return joints




    
    

#------------------------------------------------------------------------------------------------------------------------------             // getUvEquivalentToVertex 

def API_getMDagPath( obj ):	
	
	selection = ompy.MSelectionList()
	selection.add( obj )
	
	dagPath= ompy.MDagPath()
	dagPath = selection.getDagPath( 0 )
	
	return dagPath
	
	
def API_getAllVertexCoords( nameMesh ):
	dagPath    = API_getMDagPath( nameMesh )	
	meshClass  = ompy.MFnMesh(dagPath)	
	pointArray = meshClass.getPoints( ompy.MSpace.kWorld )

	pointList = []	
	for i in range( 0 , len(pointArray) ):
		pointList.append( [pointArray[i][0], pointArray[i][1], pointArray[i][2]] )
		
	return pointList

def API_meshClass( nameMesh ):	

	selection = om.MSelectionList()
	selection.add(nameMesh)
	
	dagPathMesh = om.MDagPath()
	selection.getDagPath( 0 , dagPathMesh )
	
	meshClass = om.MFnMesh(dagPathMesh)

	return meshClass
	

def API_getMeshPoints( meshClass ):	

	meshPoints = om.MPointArray()
	meshClass.getPoints( meshPoints, om.MSpace.kWorld)	

	return meshPoints
	


def API_nurbsSurfaceClass( nameNurbs ):	

	selection = om.MSelectionList()
	selection.add(nameNurbs)
	
	dagPathMesh = om.MDagPath()
	selection.getDagPath( 0 , dagPathMesh )
	
	nurbsClass = om.MFnNurbsSurface(dagPathMesh)

	return nurbsClass	
	
	

def API_convertToFloat( nbr_DoublePtr ):
	
	nbr_util = om.MScriptUtil( nbr_DoublePtr )		
	nbr_Float = nbr_util.asFloat() 
	
	return nbr_Float
 	
	
	
def getUvEquivalentToVertex( _mesh , _nurbs ):

	'''
	pour un mesh et plusieurs nurbs
	
	cette proc va associer chaque vertex du mesh a l'UV le plus proche
	
	ex:
	
	UVequi[ vtx ] [ 0 ] = nomDuNurbs
	UVequi[ vtx ] [ 1 ] = U
	UVequi[ vtx ] [ 2 ] = V
	'''		
	
	UVequi = []
	
	currentMesh = API_meshClass( _mesh )		
	meshPoints = API_getMeshPoints( currentMesh )

	#convertion double ptr	
	u_util = om.MScriptUtil()
	v_util = om.MScriptUtil()
	
	u_util.createFromDouble( 1.0 )
	v_util.createFromDouble( 1.0 )
	
	u = u_util.asDoublePtr()
	v = v_util.asDoublePtr()	
	#convertion double ptr
	
	
	pointNurbs = om.MPoint()

	closetNurbsUv = []
	
	
	for i in range( meshPoints.length() ) :	

		distNameUvs = {}
		distances = []
		
		for nurb in _nurbs:		

			currentNurbs      = API_nurbsSurfaceClass( nurb )      		
			closestPointNurbs = currentNurbs.closestPoint( meshPoints[i] , u , v )	
			
			
			distance          = closestPointNurbs.distanceTo( meshPoints[i] )
			distances.append( distance )
			
			u_float = API_convertToFloat(u)
			v_float = API_convertToFloat(v)
			
			distNameUvs[distance] = [ nurb , u_float , v_float ]

			
		distances.sort()
		UVequi.append( distNameUvs[ distances[0] ] )
		
	
	
	return UVequi	
	
	
	
	
	
	
	
#------------------------------------------------------------------------------------------------------------------------------             // getUVcoords 


def getUVcoords( UVequi ):
	
	'''
	a partir de UVequi

	UVequi[ vtx ] [ 0 ] = nomDuNurbs
	UVequi[ vtx ] [ 1 ] = U
	UVequi[ vtx ] [ 2 ] = V
	
	
	trouve les coordonnees XYZ de chaque UV
	
	UVcoords[ vtx ] = [ 0 , 0 , 0 ]
	
	'''

	UVcoords = []
	
	for i in range( 0 , len(UVequi) ):
		UVcoords.append( getUVNurbsXYZCoords(  UVequi[i][0]  ,  UVequi[i][1]  ,  UVequi[i][2]   ) )
	

	return UVcoords
	
	
	
	

def getUVNurbsXYZCoords( nurbsName , u , v ):
 

	selection = om.MSelectionList()
	selection.add( nurbsName )
	
	dagPathNurbs = om.MDagPath()	
	selection.getDagPath( 0 , dagPathNurbs )

 	currentNurbs = om.MFnNurbsSurface(dagPathNurbs)
 	point = om.MPoint()
 	coords = []

	currentNurbs.getPointAtParam( u , v , point , om.MSpace.kWorld )
	coords= [ point[0] , point[1], point[2] ]  
		

	return coords
		
	
	
	
	
#------------------------------------------------------------------------------------------------------------------------------             moveJoint 



#=====

def getJointsOneSkin(skinnedObj):

    objShapes = mc.listRelatives(skinnedObj, c=1, s=1)

    for objShape in objShapes:
        skinClusters = mc.listConnections(objShape, d=0, s=1, type="skinCluster")

        id = mc.nodeType(skinClusters)
        if id == 'skinCluster':
            joints = mc.listConnections(skinClusters, s=1, c=0, d=0, type='joint')
            skinJoints = arrayRemoveDuplicates(joints)

    return skinJoints

#========

def duplicateJoint(jointToDupli):
    newJoint = mc.joint(n=(jointToDupli + '_dupli'))
    mc.delete(mc.parentConstraint(jointToDupli, newJoint, mo=0))
    return newJoint


#=======


def getSkinClusterFromJoint( initJoint ):
    skinCLust = mc.listConnections( ( initJoint + '.lockInfluenceWeights' ) , s=0, d=1, type='skinCluster')
    skinClusters = arrayRemoveDuplicates( skinCLust )
    return skinClusters


#=====

def getNurbsFromSkin(skin):
    nurbsName = []
    shape = mc.listConnections(skin, s=0, d=1, sh=1, type='shape')
    transform = mc.listRelatives(shape[0], p=1, type='transform')
    nurbsName = transform

    return nurbsName

#==========

def addjointToSkinCluster( jointToAdd, skincluster ):

	mc.skinCluster( skincluster, e=1, dr=1, wt=0, ai = jointToAdd)


#========

def getCvs( nurbs ):	
	

	shape = mc.listRelatives( nurbs, c = 1, s = 1 )	

	numSpansU = mc.getAttr (shape[0] + '.spansU')
	degreeU   = mc.getAttr (shape[0] + '.degreeU')
	numSpansV = mc.getAttr (shape[0] + '.spansV')
	degreeV   = mc.getAttr (shape[0] + '.degreeV')
	
	numCVsU   = numSpansU + degreeU - 1
	numCVsV   = numSpansV + degreeV - 1
	
	numCVs = []
	numCVs.append(str(numCVsU))
	numCVs.append(str(numCVsV))
	
	return numCVs


#==========

def transferWeightSkinPerJnt( initJoint, transferJoint, nurbsName, skinClust, numberVtx):
	
    skinJoints = getJointsOneSkin( nurbsName )
    
    for skinJoint in skinJoints:
        mc.setAttr(skinJoint + '.liw', 1)


    mc.setAttr(initJoint + ".liw", 0)
    mc.setAttr(transferJoint + ".liw", 0)


    mc.skinPercent(str(skinClust), ( '%s.cv[0:%s][0:%s]' %( nurbsName , numberVtx[0] , numberVtx[1] ) ), transformValue=[(transferJoint, 1)])

    for skinJoint in skinJoints:
        mc.setAttr(skinJoint + '.liw', 0)

#==========

'''
def moveJoint( nurbs , joint , distance, direction, reset):

	mc.select(cl=1)
	
	valuesTranslate = mc.xform( joint, q=1, ws=1, t=1 )
	vectorDirection = om.MVector( direction[0], direction[1], direction[2] )
	vectorDirection.normalize()
	
	if reset == 0:
		newValueTxResetOn = valuesTranslate[0] + ( vectorDirection.x * distance )
		newValueTyResetOn = valuesTranslate[1] + ( vectorDirection.y * distance )
		newValueTzResetOn = valuesTranslate[2] + ( vectorDirection.z * distance )
		
		
		jointDupli = duplicateJoint( joint )
		
		skinClusters = getSkinClusterFromJoint( joint )
		
		for skinCluster in skinClusters:
			        	
			shapeTmp   = mc.listConnections( skinCluster, s=0, d=1, sh=1, type='shape')
			skinSlaves = mc.listRelatives( shapeTmp , p = 1)
			

			if( skinSlaves[0] in nurbs ):
				
				nbrCvs = getCvs( skinSlaves[0] ) 
				addjointToSkinCluster( jointDupli, skinCluster )    			
				transferWeightSkinPerJnt( joint , jointDupli , skinSlaves[0]  , skinCluster , nbrCvs )
				
				
				
		mc.xform(  jointDupli , ws=1 , t=( newValueTxResetOn, newValueTyResetOn, newValueTzResetOn )   )   

     	
    	    	
	if reset == 1:
	
		newValueTxResetOn = valuesTranslate[0] - (vectorDirection.x * distance)
		newValueTyResetOn = valuesTranslate[1] - (vectorDirection.y * distance)
		newValueTzResetOn = valuesTranslate[2] - (vectorDirection.z * distance)
		
		
		skinClusters = getSkinClusterFromJoint(joint)
		jointDupli = joint + '_dupli'
		
		for skinCluster in skinClusters:
			
			shapeTmp   = mc.listConnections( skinCluster, s=0, d=1, sh=1, type='shape' )
			skinSlaves = mc.listRelatives( shapeTmp, p = 1 )
			
			if( skinSlaves[0] in nurbs ):  
				
				nbrCvs = getCvs( skinSlaves[0] )
				mc.xform( jointDupli , ws=1 , t = ( newValueTxResetOn, newValueTyResetOn, newValueTzResetOn ) )
				transferWeightSkinPerJnt( jointDupli , joint , skinSlaves[0] , skinCluster, nbrCvs)
		
		mc.delete(jointDupli)


	return valuesTranslate 
'''




def moveJoint( joint , direction, reset = None ):

	mc.select(cl=1)
	
	valuesTranslate = mc.xform( joint, q=1, ws=1, t=1 )
	vectorDirection = om.MVector( direction[0], direction[1], direction[2] )
	vectorDirection.normalize()
	
	if( reset == None ):
		#GET INFO
		connectionsDest   = mc.listConnections( joint , c = True , p = True ,s = False , d = True )
		connectionsDest = None
		if( connectionsDest == None ):connectionsDest = [] 
		connectionsSource = mc.listConnections( joint , c = True , p = True ,s = True  , d = False )
		if( connectionsSource == None ):connectionsSource = [] 
		childrens         = mc.listRelatives( joint , c = True )
		if( childrens == None ):childrens = [] 
		lockTranslate = []
		lockTranslate.append( mc.getAttr( joint + '.translateX' ,   l = True  ) )
		lockTranslate.append( mc.getAttr( joint + '.translateY' ,   l = True  ) )
		lockTranslate.append( mc.getAttr( joint + '.translateZ' ,   l = True  ) )
		#DISCONNECT
		for i in range( 0 , len( connectionsDest ) , 2 ):
			mc.disconnectAttr( connectionsDest[i] , connectionsDest[i+1] )
		for i in range( 0 , len( connectionsSource ) , 2 ):
			mc.disconnectAttr( connectionsSource[i+1] , connectionsSource[i] )
		#UNPARENT CHILDREN
		if( len(childrens) ):mc.parent(  childrens , w = True )
		#UNLOCK TRANSLATE
		if(lockTranslate[0]): mc.setAttr( joint + '.translateX' , l = False )
		if(lockTranslate[1]): mc.setAttr( joint + '.translateY' , l = False )
		if(lockTranslate[2]): mc.setAttr( joint + '.translateZ' , l = False )					
		#MOVE JOINT
		newValueTxResetOn = valuesTranslate[0] + vectorDirection.x 
		newValueTyResetOn = valuesTranslate[1] + vectorDirection.y 
		newValueTzResetOn = valuesTranslate[2] + vectorDirection.z
		mc.xform(  joint , ws=1 , t=( newValueTxResetOn, newValueTyResetOn, newValueTzResetOn )   )
		#return INFO
		return [ connectionsDest , connectionsSource , childrens , lockTranslate ]		 
	else:
		newValueTxResetOn = valuesTranslate[0] - vectorDirection.x 
		newValueTyResetOn = valuesTranslate[1] - vectorDirection.y 
		newValueTzResetOn = valuesTranslate[2] - vectorDirection.z 			
		mc.xform(  joint , ws=1 , t=( newValueTxResetOn, newValueTyResetOn, newValueTzResetOn )   )
		#get INFO
		connectionsDest   = reset[0]
		connectionsSource = reset[1] 
		childrens         = reset[2] 
		lockTranslate     = reset[3] 		
		#CONNECT
		for i in range( 0 , len( connectionsDest ) , 2 ):
			mc.connectAttr( connectionsDest[i] , connectionsDest[i+1] )
		for i in range( 0 , len( connectionsSource ) , 2 ):
			mc.connectAttr( connectionsSource[i+1] , connectionsSource[i] )
		#PARENT
		if( len(childrens) ):mc.parent( childrens , joint )
		#LOCK TRANSLATE
		if(lockTranslate[0]): mc.setAttr( joint + '.translateX' , l = True )
		if(lockTranslate[1]): mc.setAttr( joint + '.translateY' , l = True )
		if(lockTranslate[2]): mc.setAttr( joint + '.translateZ' , l = True )
		return None	











def moveJoint_OLD( joint , distance , vectorOrient , reset ):
	
	'''
	
	a partir d'une distance , d'un vecteur de direction et d'un bool
	
	deplacement d'un joint selon une distance et un vecteur de direction
	
	
	'''

	valuesTranslate = mc.xform( joint, q=1, ws=1, t=1)
	vectorDirection = om.MVector(vectorOrient[0], vectorOrient[1], vectorOrient[2])
	vectorDirection.normalize()
	
	if reset == 0:
		newValueTxResetOn = valuesTranslate[0] + (vectorDirection.x * distance)
		newValueTyResetOn = valuesTranslate[1] + (vectorDirection.y * distance)
		newValueTzResetOn = valuesTranslate[2] + (vectorDirection.z * distance)
	
	if reset == 1:
	
		newValueTxResetOn = valuesTranslate[0] - (vectorDirection.x * distance)
		newValueTyResetOn = valuesTranslate[1] - (vectorDirection.y * distance)
		newValueTzResetOn = valuesTranslate[2] - (vectorDirection.z * distance)
	
	mc.xform( joint, ws=1, t = (newValueTxResetOn, newValueTyResetOn, newValueTzResetOn) )	
	

	return 1


	
	
	


#------------------------------------------------------------------------------------------------------------------------------             // getDistanceArray 



def getDistanceArray( aCoords , bCoords ):
	
	'''
		a partir de deux array de coords		
		return un array de distance entre aCoords et bCoords
	'''

	distances = []
	
	for i in range( 0 , len( aCoords ) ):
		distances.append(    om.MVector( ( aCoords[i][0] - bCoords[i][0] ) , ( aCoords[i][1] - bCoords[i][1] ) , ( aCoords[i][2] - bCoords[i][2] ) ).length()      )
	

	return distances	
	
		

#------------------------------------------------------------------------------------------------------------------------------             // convertDistanceToInfs 


def convertDistanceToInfs( UVdists , distMove ):
		
	'''
		de la dist entre uv et des la distance de deplacement du joint	
		return un array d'influence (  UVdist / distMove )
	'''
	infs = []
	
	for d in UVdists:
		infs.append( d / distMove ) 

	return infs	
   
	
	
	
	
#------------------------------------------------------------------------------------------------------------------------------             // makeSkinCluster 


def makeSkinCluster(  mesh , joints , inf ):
	
	'''
		create simple skin cluster + inf
	'''
	
	newSkinClusterNode = mc.skinCluster( joints, mesh , mi = len(joints) )
	
	
	WeightDate = convertInfToWeightDate( mesh , joints , inf  )
	setSkinWeights( newSkinClusterNode[0] ,  WeightDate )
	
	'''
	
	nbrVertex = mc.polyEvaluate( mesh , v = True )
	
	influencesList = []
	
	for i in range( 0 , nbrVertex):
		for joint in joints :
			influencesList.append( [ joint , inf[joint][i] ]  )
			
		mc.skinPercent( newSkinClusterNode[0], ( '%s.vtx[%r]' %( mesh , i ) ) , transformValue = influencesList )	

	'''
	
	return newSkinClusterNode		
	

def convertInfToWeightDate( mesh , joints , inf  ):

	nbrVertex = mc.polyEvaluate( mesh , v = True )
	WeightDate = []

	for i in range( 0 , nbrVertex ):
		jointAndWeight = []
		for joint in joints:
			jointAndWeight.append( ( joint , inf[joint][i] ) )
	
		WeightDate.append( ( '%s.vtx[%r]' %( mesh , i) , jointAndWeight ) )


	return WeightDate

	
	
	
	
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
		    	
		
	
	
	
	
#------------------------------------------------------------------------------------------------------------------------------             // makeSkinCluster 

	
	
def printRapport( timeValues ):	
	
	selectionEtJoints = timeValues[1] - timeValues[0]
	UVequiVertex      = timeValues[2] - timeValues[1]	
	UVcoords          = timeValues[3] - timeValues[2]		
	moveGetDistInf    = timeValues[4] - timeValues[3]		
	makeSkinCluster   = timeValues[5] - timeValues[4]
	ALL               = timeValues[5] - timeValues[0]
	
	print( '=======================================================================' )
	print( '==================== CONVERT SKIN NURBS TO MESH =======================' )	
	print( '=======================================================================' )
	print(' ')
	print( ' selectionEtJoints :   %f   ----->  %f  ' %( selectionEtJoints , ( selectionEtJoints / ALL *100 )  ) )
	print( ' UVequiVertex      :   %f   ----->  %f  ' %( UVequiVertex      , ( UVequiVertex      / ALL *100 )  ) )
	print( ' UVcoords          :   %f   ----->  %f  ' %( UVcoords          , ( UVcoords          / ALL *100 )  ) )
	print( ' moveGetDistInf    :   %f   ----->  %f  ' %( moveGetDistInf    , ( moveGetDistInf    / ALL *100 )  ) )
	print( ' makeSkinCluster   :   %f   ----->  %f  ' %( makeSkinCluster   , ( makeSkinCluster   / ALL *100 )  ) )
	print( ' ALL               :   %f   ----->  %f  ' %( ALL               , ( ALL               / ALL *100 )  ) )
	print(' ')
	print( '=======================================================================' )
	print( '==================== CONVERT SKIN NURBS TO MESH =======================' )	
	print( '=======================================================================' )
	print(' ')	
	
	
	
	
	
	

	
	
'''	



import sys

sys.path.append( '/u/mcantat/Sandbox/script/convertSkinNurbsToMesh' )



exec('import copySkinNurbsToMesh') in globals()
exec('reload (copySkinNurbsToMesh)') in globals()


copySkinNurbsToMesh.copySkinCurvToMesh()



'''
