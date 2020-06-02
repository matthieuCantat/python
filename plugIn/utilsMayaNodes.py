
import maya.OpenMaya as om
import maya.OpenMayaMPx as ommpx
import maya.cmds as mc
import time


#______________________________________________________________ATTR
def nodeAttrToInt( DataBlock , NodeAttr ): 
	dataHandle  = DataBlock.inputValue( NodeAttr )
	valueInt = dataHandle.asInt()
	return valueInt

def nodeAttrToFloat( DataBlock , NodeAttr ): 
	dataHandle  = DataBlock.inputValue( NodeAttr )
	valueFloat = dataHandle.asFloat()
	return valueFloat

def nodeAttrToFloat3( DataBlock , NodeAttr ):                                            
    dataHandle      = DataBlock.inputValue( NodeAttr )
    dataHandleNum   = dataHandle.asFloat3()
    return [ dataHandleNum[0] , dataHandleNum[1] , dataHandleNum[2] ]      

def nodeAttrToEnumInt( DataBlock , NodeAttr ): 
	dataHandle  = DataBlock.inputValue( NodeAttr )
	valueInt = dataHandle.asInt()
	return valueInt

def nodeAttrToEnumStr( DataBlock , NodeAttr , values ): 
	dataHandle  = DataBlock.inputValue( NodeAttr )
	valueInt = dataHandle.asInt()
	return values[valueInt]

def nodeAttrToMVector( DataBlock , NodeAttr ): 
	dataHandle  = DataBlock.inputValue( NodeAttr )
	return dataHandle.asFloatVector()

def nodeAttrToMVectors( DataBlock , NodeAttr ): 
	dataHandle  = DataBlock.inputValue( NodeAttr )	
	arrayDataHandle = om.MArrayDataHandle(dataHandle )
	outMVectors = []   
	for i in range(0, arrayDataHandle.elementCount() ):
		if not( i == 0 ):arrayDataHandle.next() 
		dataHandle = arrayDataHandle.inputValue()
		outMVectors.append( dataHandle.asFloatVector() )

	return outMVectors

def nodeAttrToMStrings( DataBlock , NodeAttr ): 
	dataHandle  = DataBlock.inputValue( NodeAttr )	
	arrayDataHandle = om.MArrayDataHandle(dataHandle )
	outMString = []   
	for i in range(0, arrayDataHandle.elementCount() ):
		if not( i == 0 ):arrayDataHandle.next() 
		dataHandle = arrayDataHandle.inputValue()
		outMString.append( dataHandle.asString() )

	return outMString


def nodeAttrToIntArray( DataBlock , NodeAttr ): 
	dataHandle  = DataBlock.inputValue( NodeAttr )	
	arrayDataHandle = om.MArrayDataHandle(dataHandle )
	outIntArray = []   
	for i in range(0, arrayDataHandle.elementCount() ):
		if not( i == 0 ):arrayDataHandle.next() 
		dataHandle = arrayDataHandle.inputValue()
		outIntArray.append( dataHandle.asInt() )

	return outIntArray

def nodeAttrToFloatArray( DataBlock , NodeAttr ): 
	dataHandle  = DataBlock.inputValue( NodeAttr )	
	arrayDataHandle = om.MArrayDataHandle(dataHandle )
	outFloatArray = []   
	for i in range(0, arrayDataHandle.elementCount() ):
		if not( i == 0 ):arrayDataHandle.next() 
		dataHandle = arrayDataHandle.inputValue()
		outFloatArray.append( dataHandle.asFloat() )

	return outFloatArray



def nodeAttrToMatrixFloatList( DataBlock , NodeAttr  ):   

    dataHandle    = DataBlock.inputValue( NodeAttr )
    MFloatMatrixObj  = dataHandle.asFloatMatrix()
    worldMatrix       = MMatrixToNum(MFloatMatrixObj) 

    return worldMatrix


def floatToNodeAttr( DataBlock , NodeAttr , value ): 
	dataHandle = DataBlock.outputValue( NodeAttr )
	dataHandle.setFloat(value)
	dataHandle.setClean()

def MVectorsToNodeAttr( DataBlock , NodeAttr  , Mvectors ):           
	builder = om.MArrayDataBuilder(DataBlock, NodeAttr, len(Mvectors))	
	for i in range(0, len(Mvectors) ):
		handle = builder.addElement(i)
		handle.setMFloatVector(Mvectors[i])			

	arrayDataHandle = DataBlock.outputArrayValue( NodeAttr )
	arrayDataHandle.set(builder)
	arrayDataHandle.setAllClean()



def MMatrixToNum( matrix ):
    return [  matrix(0,0) , matrix(0,1) , matrix(0,2) , matrix(0,3)  ,  matrix(1,0) , matrix(1,1) , matrix(1,2) , matrix(1,3)  ,  matrix(2,0) , matrix(2,1) , matrix(2,2) , matrix(2,3) ,  matrix(3,0) , matrix(3,1) , matrix(3,2) , matrix(3,3)  ]     






def nodeInstanceToFloat(  nodeInstance , attr  ):   
    plug = om.MPlug( nodeInstance.thisMObject() , attr )
    vec = plug.asFloat()
    return vec




def nodeInstanceToMVector(  nodeInstance , attr  ): 
    plug = om.MPlug( nodeInstance.thisMObject() , attr )    
    vec = vectorPlugValue(plug)
    return vec



def vectorPlugValue( plug ):
    if (plug.numChildren() == 3):
        rx = plug.child(0)
        ry = plug.child(1)
        rz = plug.child(2)
        x = rx.asFloat()
        y = ry.asFloat()
        z = rz.asFloat()
        result = om.MVector(x,y,z)
        return result
    else:
        Result = om.MVector(x,y,z)
        return result





            
#______________________________________________________________MATH

def clamp( min_value , max_value , my_value):
	return max(min(my_value, max_value), min_value)

def MVectorBlend( inMVectorA , inMVectorB , samples ):
	vAFloat = [ inMVectorA.x , inMVectorA.y , inMVectorA.z ]
	vBFloat = [ inMVectorB.x , inMVectorB.y , inMVectorB.z ]

	incr = []
	for i in range( 0 , len( vAFloat ) ):
		incr.append( (vBFloat[i] - vAFloat[i])/(samples+1) )

	outMVectors = []
	tmp = vAFloat 
	for i in range( samples ):
		for j in range( len(incr) ):
			tmp[j] += incr[j]

		outMVectors.append( om.MFloatVector( tmp[0] , tmp[1] , tmp[2]  ) )

	return outMVectors


def getBoundingBox( MFloatVectors ):
	minValue = -9999999999999999999999999999999999999999999999999999999999999999
	maxValue =  9999999999999999999999999999999999999999999999999999999999999999
	minPoint = om.MFloatVector( om.MPoint(maxValue , maxValue , maxValue) )
	maxPoint = om.MFloatVector( om.MPoint(minValue , minValue , minValue) )	
		
	size = len( MFloatVectors )
	for i in range( 0 , size ):
		if(  MFloatVectors[i].x < minPoint.x  ):
			minPoint.x = MFloatVectors[i].x
		if(  MFloatVectors[i].y < minPoint.y  ):
			minPoint.y = MFloatVectors[i].y
		if(  MFloatVectors[i].z < minPoint.z  ):
			minPoint.z = MFloatVectors[i].z

		if( maxPoint.x < MFloatVectors[i].x ):
			maxPoint.x = MFloatVectors[i].x
		if( maxPoint.y < MFloatVectors[i].y  ):
			maxPoint.y = MFloatVectors[i].y
		if( maxPoint.z < MFloatVectors[i].z  ):
			maxPoint.z = MFloatVectors[i].z
		
	return [ minPoint , maxPoint ]


def getBarycentre( MFloatVectors ):
	x = 0.0
	y = 0.0
	z = 0.0
	size = len( MFloatVectors )
	for i in range( 0 , size ):
		x += MFloatVectors[i].x
		y += MFloatVectors[i].y
		z += MFloatVectors[i].z	

	x /= size
	y /= size
	z /= size					
	return om.MFloatVector( om.MPoint(x , y , z) )


def cumulateDistance( MFloatVectors , MFloatVector ):

	distance = 0 
	for i in range( 0 , len(MFloatVectors) ):
		vTmp = MFloatVectors[i] - MFloatVector 
		distance += vTmp.length() 

	return distance	 	



#______________________________________________________________TOPOLOGY INFO

def getTopologyNeighbourIndexes( MeshFn , linkComponent , linkExpand  ):

	tnIndexes = []
	mItVtx    = om.MItMeshVertex(MeshFn)

	for i in range( 0 , mItVtx.count() ):
		if( linkComponent == 'edge' ):
			tnIndexes.append( growVertexByEdge( MeshFn , i  ) )
		elif( linkComponent == 'face' ):
			tnIndexes.append( growVertexByFace( MeshFn , i  ) )				
		mItVtx.next()

	return tnIndexes



def getTopologyNeighbourLenghts( MVectors , topologyNeighbourIndexes  ):
	topologyNeighbourBaseLenghts = []
	for i in range( 0 , len( MVectors ) ):
		tmp = []
		for ni in topologyNeighbourIndexes[i]:
			vTmp = MVectors[ni] - MVectors[i] 
			tmp.append( vTmp.length() )
		topologyNeighbourBaseLenghts.append( tmp )

	return topologyNeighbourBaseLenghts



def vertexToEdges( MFnMesh , iVtx ):

	mItVtx    = om.MItMeshVertex(MFnMesh)
	edgeIndex = om.MIntArray()
	vtxPos    = []	
	
	while not mItVtx.isDone():
		if( mItVtx.index() == iVtx ):
			mItVtx.getConnectedEdges( edgeIndex )
			break
		mItVtx.next()
		
	edgeIndexesInt = []		
	for i in range( 0 , edgeIndex.__len__() ):
		edgeIndexesInt.append( edgeIndex[i] )
	    
	return edgeIndexesInt

def edgeToVertices( MFnMesh , iEdge ):
	
	mItVtx    = om.MItMeshVertex(MFnMesh)

	vtxNum = []	
	while not mItVtx.isDone():
		iEdgesConnected = om.MIntArray()
		mItVtx.getConnectedEdges(iEdgesConnected)
		iEdgesConnectedInt = [ iEdgesConnected[i] for i in range( 0 , iEdgesConnected.length() )]

		if( iEdge in iEdgesConnectedInt ):			
			vtxNum.append( mItVtx.index() )
		mItVtx.next()

			
	iVtx = []
	for i in range( 0 , len(vtxNum) ):
		iVtx.append( vtxNum[i] )
	    	
	return iVtx
	


def vertexToFaces( MFnMesh , iVtx ):

	mItVtx    = om.MItMeshVertex(MFnMesh)
	faceIndex = om.MIntArray()
	vtxPos    = []	
	
	while not mItVtx.isDone():
		if( mItVtx.index() == iVtx ):
			mItVtx.getConnectedFaces( faceIndex )
			break
		mItVtx.next()
		
	faceIndexesInt = []		
	for i in range( 0 , faceIndex.__len__() ):
		faceIndexesInt.append( faceIndex[i] )
	    
	return faceIndexesInt


def faceToVertices( MFnMesh , iFace ):
	
	mItVtx    = om.MItMeshVertex(MFnMesh)

	vtxNum = []	
	while not mItVtx.isDone():

		iFacesConnected = om.MIntArray()
		mItVtx.getConnectedFaces(iFacesConnected)
		iFacesConnectedInt = [ iFacesConnected[i] for i in range( 0 , iFacesConnected.length() )]

		if( iFace in iFacesConnectedInt ):			
			vtxNum.append( mItVtx.index() )
		mItVtx.next()
			
	iVtx = []
	for i in range( 0 , len(vtxNum) ):
		iVtx.append( vtxNum[i] )
	    	
	return iVtx



def growVertexByEdge( MfnMesh , iVtx  , keepVerticesBase = 0 ):

	verticesBase = [ iVtx ]

	edgesGrow = vertexToEdges( MfnMesh , iVtx )
	edgesGrow    = list(set(edgesGrow))	
	
	verticesGrow = []	
	for edge in edgesGrow:
		verticesGrow += edgeToVertices( MfnMesh , edge )			
	verticesGrow = list(set(verticesGrow))	

	if( keepVerticesBase == 0 ):	
		for v in verticesBase:
			try:verticesGrow.remove(v)
			except:pass

	return verticesGrow 	         

def growVertexByFace( MfnMesh , iVtx  , keepVerticesBase = 0 ):

	verticesBase = [ iVtx ]

	facesGrow = vertexToFaces( MfnMesh , iVtx )
	facesGrow    = list(set(facesGrow))	
	
	verticesGrow = []	
	for face in facesGrow:
		verticesGrow += faceToVertices( MfnMesh , face )			
	verticesGrow = list(set(verticesGrow))	

	if( keepVerticesBase == 0 ):	
		for v in verticesBase:
			try:verticesGrow.remove(v)
			except:pass

	return verticesGrow 	         




#______________________________________________________________FORCES

def getAttractForce( MVpoint , MVdriver  , repulsion = 0 , triggerDist = 0 , power = 1 , overrideLength = None ,  globalIter = 1 ): 
	bigNbr = 99999999999999999
	if( repulsion == 0 ): 
		v = MVdriver - MVpoint
		l = clamp(0,bigNbr, v.length() - triggerDist ) * power / globalIter
	else:                 
		v = MVpoint - MVdriver
		l = clamp(0,bigNbr, triggerDist - v.length() ) * power / globalIter
	
	if not( overrideLength == None ): 
		l = overrideLength

	v.normalize()
	v *= l
	return v


def applyTopologyEdgeLength( inPoints , fixeIndexes , envelope , attractForce , repulseForce , globalIter , topologyNeighbourIndexes , topologyNeighbourBaseLenghts ):
	tnIs = topologyNeighbourIndexes
	tnLs = topologyNeighbourBaseLenghts

	if( envelope == 0 ):
		return inPoints

	outPoints = inPoints[:]
	for e in range( 0 , globalIter ):

		tmpPoints = outPoints[:]
		for i in range( 0 , len( outPoints ) ):	

			if( i in fixeIndexes ):
				continue

			for tnI , tnL in zip(tnIs[i] , tnLs[i]):
				#COMPUTE FORCES
				vAttract = getAttractForce( tmpPoints[i] , tmpPoints[tnI] , triggerDist = tnL , power = attractForce , globalIter = globalIter , repulsion = 0  )					
				vRepulse = getAttractForce( tmpPoints[i] , tmpPoints[tnI] , triggerDist = tnL , power = repulseForce , globalIter = globalIter  , repulsion = 1  )		
				#APPLY FORCES
				tmpPoints[i]   = tmpPoints[i]   + vAttract/2 + vRepulse/2
				tmpPoints[tnI] = tmpPoints[tnI] - vAttract/2 - vRepulse/2
	
		outPoints = tmpPoints[:] 

	
	for i in range( 0 , len(outPoints) ):
		outPoints[i] = outPoints[i] * envelope + inPoints[i] * ( 1 - envelope )

	return outPoints


def applyTopologyRelax( inPoints , fixeIndexes , envelope , attractForce , repulseForce , globalIter , topologyNeighbourIndexes , topologyNeighbourBaseLenghts ):
	tnIs = topologyNeighbourIndexes
	tnLs = topologyNeighbourBaseLenghts

	if( envelope == 0 ):
		return inPoints

	outPoints = inPoints[:]
	for e in range( 0 , globalIter ):

		tmpPoints = outPoints[:]
		for i in range( 0 , len( outPoints ) ):	

			if( i in fixeIndexes ):
				continue

			barycentre  = outPoints[i]   
			nbrToDivide = 1  	

			for tnI , tnL in zip(tnIs[i] , tnLs[i]):
				#COMPUTE FORCES
				vAttract = getAttractForce( outPoints[i] , outPoints[tnI] , triggerDist = tnL , power = attractForce , globalIter = globalIter , repulsion = 0  )					
				vRepulse = getAttractForce( outPoints[i] , outPoints[tnI] , triggerDist = tnL , power = repulseForce , globalIter = globalIter  , repulsion = 1  )		
				#APPLY FORCES
				if not( attractForce == 0 ):
					barycentre = barycentre + tmpPoints[i] + vAttract
					nbrToDivide += 1
				if not( repulseForce == 0 ):	
					barycentre = barycentre + tmpPoints[i] + vRepulse
					nbrToDivide += 1

			tmpPoints[i] = barycentre / nbrToDivide

		outPoints = tmpPoints[:] 

	for i in range( 0 , len(outPoints) ):
		outPoints[i] = outPoints[i] * envelope + inPoints[i] * ( 1 - envelope )

	return outPoints


def applyTopologyAdd( inPoints , fixeIndexes , envelope , attractForce , repulseForce , globalIter , topologyNeighbourIndexes , topologyNeighbourBaseLenghts ):
	tnIs = topologyNeighbourIndexes
	tnLs = topologyNeighbourBaseLenghts

	if( envelope == 0 ):
		return inPoints

	outPoints = inPoints[:]
	for e in range( 0 , globalIter ):
		tmpPoints = outPoints[:]

		for i in range( 0 , len( outPoints ) ):

			if( i in fixeIndexes ):
				continue

			for tnI , tnL in zip(tnIs[i] , tnLs[i]):
				#COMPUTE FORCES
				vAttract = getAttractForce( outPoints[i] , outPoints[tnI] , triggerDist = tnL , power = attractForce , globalIter = globalIter , repulsion = 0  )					
				vRepulse = getAttractForce( outPoints[i] , outPoints[tnI] , triggerDist = tnL , power = repulseForce , globalIter = globalIter  , repulsion = 1  )		
				#APPLY FORCES
				print( vAttract.x , vAttract.y , vAttract.z , )
				tmpPoints[i] = tmpPoints[i] + vAttract + vRepulse

	
		outPoints = tmpPoints[:] 

	for i in range( 0 , len(outPoints) ):
		xTmp = outPoints[i].x * envelope + inPoints[i].x * ( 1 - envelope )
		yTmp = outPoints[i].y * envelope + inPoints[i].y * ( 1 - envelope )
		zTmp = outPoints[i].z * envelope + inPoints[i].z * ( 1 - envelope )
		outPoints[i] = om.MFloatPoint( xTmp , yTmp , zTmp )

	return outPoints


def applyTopologySmooth( inPoints , fixeIndexes , envelope , globalIter , topologyNeighbourIndexes , topologyNeighbourBaseLenghts  ): 	
	tnIs = topologyNeighbourIndexes
	tnLs = topologyNeighbourBaseLenghts

	if( envelope == 0 ):
		return inPoints

	outPoints = inPoints[:]
	for e in range( 0 , globalIter ):
		tmpPoints = outPoints[:]

		for i in range( 0 , len( outPoints ) ):

			if( i in fixeIndexes ):
				continue

			barycentre  = outPoints[i]   
			nbrToDivide = 1  	

			for tnI , tnL in zip(tnIs[i] , tnLs[i]):
				#COMPUTE FORCES
				#APPLY FORCES
				barycentre = barycentre + tmpPoints[tnI]
				nbrToDivide += 1

			tmpPoints[i] = barycentre / nbrToDivide
	
		outPoints = tmpPoints[:] 

	for i in range( 0 , len(outPoints) ):
		outPoints[i] = outPoints[i] * envelope + inPoints[i] * ( 1 - envelope )

	return outPoints


#______________________________________________________________DynamicStore

class DynamicStore():

	def __init__(self , arrayFill , maxIndex ):
		self.maxIndex = maxIndex 

		self.storeValues = []
		for i in range( 0 , self.maxIndex + 1 ) : 
			self.storeValues.append( arrayFill )

	def __getitem__( self, index ): 
		return self.storeValues[index]

	def addFirst( self , valueToAdd):
		#SHIFT ALL THE VALUES
		for i in range( len(self.storeValues) , 0 , -1 ):
			if( i <= self.maxIndex ):
				self.storeValues[i] = self.storeValues[i-1][:]
			
		#ADDValue
		self.storeValues[0] = valueToAdd




#__________________________________________________________ TEST



def getWeightPriority( points , basePoints ):

	distances = []
	distanceMax = 0

	for i in range( 0 , len(points) ):
		vTmp = points[i] - basePoints[i]
		distances.append(vTmp.length())
		if( distanceMax < vTmp.length() ):
			distanceMax = vTmp.length()

	weights = [ distances[i]/distanceMax for i in range( 0 , len(distances) ) ]
	return weights 


def getMomentumWeightPriority( vMomentums , pointIndex , neighbourgIndexes ):

	pointMomentum     = vMomentums[pointIndex]
	neighbourgMomentums = [ vMomentums[i] for i in neighbourgIndexes ]
	allMomentums = [ pointMomentum ] + neighbourgMomentums

	distance = 0
	distanceMax = 0
	for vMomentum in allMomentums:
		distance += vMomentum.length()
		if( distanceMax < vMomentum.length() ):
			distanceMax = vMomentum.length() 

	weights = []
	for vMomentum in neighbourgMomentums:
		if( distanceMax == 0 ):
			weights.append( 1 )
		else:
			weights.append( vMomentum.length() /distanceMax )
	return weights
			

def topologyNeighbourIndexesReorder( points , topologyNeighbourIndexes, topologyNeighbourBaseLenghts ,  topologyNeighbourLock ):
	
	topologyNeighbourIndexesOut = topologyNeighbourIndexes[:]
	topologyNeighbourLockOut    = topologyNeighbourLock[:]

	for i in range( 0 , len(points) ):
		pMs = [ points[indexe] for indexe in topologyNeighbourIndexes[i] ]		 			
		lMs = topologyNeighbourBaseLenghts[i]
		lock     = topologyNeighbourLock[i]

		#NEW ORDER
		if( lock == 0 ):
			distances = []
			for im in range( 0 , len(pMs) ):
				vtmp = pMs[im] - points[i] 
				distances.append( vtmp.length() )
			
			distancesSorted = distances[:]
			distancesSorted.sort()	

			indexesSorted = []
			indexesIn = range( 0 , len(distances) )
			for d in distancesSorted:
				for iIn in indexesIn:
					if( d == distances[iIn] ):
						indexesSorted.append(iIn)
						indexesIn.remove(iIn)
						break

			indexesOut = [topologyNeighbourIndexes[i][ni] for ni in indexesSorted ]	
			topologyNeighbourIndexesOut[i] = indexesOut
		else:
			topologyNeighbourIndexesOut[i] = topologyNeighbourIndexes[i]

		# LOCK
		lockTolerence = 0.05
		distance = 0
		distanceBase = 0
		for im in range( 0 , len(pMs) ):
			vtmp = pMs[im] - points[i] 
			distance += vtmp.length()
			distanceBase += lMs[im]

		if( distance < distanceBase + distanceBase*lockTolerence ):
			lock = 0
		else:
			lock = 1

		topologyNeighbourLockOut[i] = lock



	debugIndexQuery = 16			
	#print( topologyNeighbourLockOut[debugIndexQuery] , topologyNeighbourIndexesOut[debugIndexQuery] )


	return topologyNeighbourIndexesOut , topologyNeighbourLockOut














