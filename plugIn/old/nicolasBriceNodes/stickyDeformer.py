
"""delete "bb";
flushUndo;

unloadPluginWithCheck( "D:/Backup/C++/Python sources/collisionDeformer/collisionTestRaytrace.py" );
loadPlugin( "D:/Backup/C++/Python sources/collisionDeformer/collisionTestRaytrace.py" );

polySphere -ch on -o on -r 2 -n "bb";

deformer -typ stickyDeformer "bb";

connectAttr "bb1Shape.worldMesh[0]" "stickyDeformer1.targetMesh";
"""

"""
TO DO

get dagPath from MObject

creer une MSelectionList from dagPath
en tirer une MRichSelection
en tirer un MFnSingleIndeComp

getter les weights


softSelection = OpenMaya.MRichSelection()
OpenMaya.MGlobal.getRichSelection(softSelection)
selection = OpenMaya.MSelectionList()
softSelection.getSelection(selection)
pathDag = OpenMaya.MDagPath()
oComp = OpenMaya.MObject()
selection.getDagPath(0, pathDag, oComp)
fnComp = OpenMaya.MFnSingleIndexedComponent(oComp)

for i in range(fnComp.elementCount()):
  print fnComp.element(i), fnComp.weight(i).influence()
"""


import math, sys, copy
import maya.OpenMaya as om
import maya.OpenMayaAnim as omAnim
import maya.OpenMayaMPx as omMPx
from maya.mel import eval as meval
import time

########################################################################################
########################################################################################

kPluginNodeTypeName = "stickyDeformer"
stickyDeformerId = om.MTypeId(0x00150A51A)

########################################################################################
########################################################################################

# Node definition
class stickyDeformer(omMPx.MPxDeformerNode):

########################################################################################
########################################################################################

	def __init__(self):

		self.targetVectArray = om.MVectorArray()
		self.oldTargetPosArray = om.MPointArray()
		self.activePointssArray = om.MIntArray()
		self.activeVectArray = om.MVectorArray()
		self.newPoints = om.MPointArray()
		self.vtxNeighbArray = []
		self.hasBeenCollide = om.MIntArray()
		self.uvArray = om.MPointArray()
		self.faceIndexArray = om.MIntArray()
		
		self.vtxPolyIndex =om.MIntArray()
		self.vtxPerPoly = []
		self.fallOffActiveArray = om.MIntArray()
		
		self.deformed = 0
		self.collisionIndexArray = om.MIntArray()
		
		self.fallOffAttractArray = om.MIntArray()

		omMPx.MPxDeformerNode.__init__(self)

########################################################################################
########################################################################################

	def deform( self, dataBlock, iter, matrix, index ):
		
		thisNode = self.thisMObject()
		
		# inputs
		env			   = omMPx.cvar.MPxDeformerNode_envelope
		envelopeValue = dataBlock.inputValue(env).asFloat()

		# get attributs that DON'T work in init def (??)
		#self.UcurrentTime = dataBlock.inputValue(self.currentTime)

		# get inMesh infos
		input  = omMPx.cvar.MPxDeformerNode_input
		hInput = dataBlock.inputArrayValue(input)
		hInput.jumpToArrayElement(index)

		inputGeom = omMPx.cvar.MPxDeformerNode_inputGeom
		groupId		 = omMPx.cvar.MPxDeformerNode_groupId

		hInputElement	 = hInput.inputValue()
		self.hInputGeom = hInputElement.child(inputGeom)

		inMesh	   = self.hInputGeom.asMesh()
		
		# Get target mesh

		targetMesh = dataBlock.inputValue(stickyDeformer.targetMesh).asMesh()
		
		hTargetMat = dataBlock.inputValue( stickyDeformer.targetMatrix )
		targetFloatMatValue = hTargetMat.asFloatMatrix()
		targetMatValue = self.floatMMatrixToMMatrix(hTargetMat.asFloatMatrix())
		
		if envelopeValue!=0 and not inMesh.isNull() and not targetMesh.isNull():

			inMeshFn = om.MFnMesh(inMesh)
			targetMeshFn = om.MFnMesh(targetMesh)

			# get target points coordinates
			targetPoints = om.MPointArray()
			targetMeshFn.getPoints(targetPoints, om.MSpace.kWorld)

			# get inMesh points coordinates 
			self.inMeshPoints = om.MPointArray()
			inMeshFn.getPoints(self.inMeshPoints,om.MSpace.kWorld)
			inMeshNormals = om.MFloatVectorArray()
			inMeshFn.getNormals(inMeshNormals)

			# keeping trace of deformed mesh points
			if self.newPoints.length() == 0:
				self.newPoints = copy.copy(self.inMeshPoints)
				
			# Initialize
			firstTimeTest = dataBlock.inputValue(stickyDeformer.firstTimeAtt).asShort()

			if self.vtxNeighbArray == []:
	
				self.initializeSelfVariables(inMesh, dataBlock)

			inMeshBB = om.MBoundingBox()
			inMeshBB = self.getBoundingBox( inMesh, 1)
										   
			targetBB = om.MBoundingBox()   
			targetBB = self.getBoundingBox( targetMesh, 1)
			
			searchVector = om.MVector()
			
			searchVector.x = targetBB.width(); searchVector.y = targetBB.height(); targetBB.z = targetBB.depth();
			searchVector.x += inMeshBB.width(); searchVector.y += inMeshBB.height(); searchVector.z += inMeshBB.depth();
			
			searchRadius = searchVector.length()
			searchRadius *= 2
			
			collisionMethod = dataBlock.inputValue(stickyDeformer.collisionMethod).asShort()
			hybridBlendValue = dataBlock.inputValue(stickyDeformer.hybridBlend).asFloat()

			collisionChek = 0

			collisionArray = om.MIntArray(self.inMeshPoints.length(), 0)

			stickyTest = dataBlock.inputValue(stickyDeformer.stickyness).asShort()

			self.mmAccelParams = targetMeshFn.autoUniformGridParams()

			meshIntersect = om.MMeshIntersector()
			meshIntersect.create(targetMesh, targetMatValue)
			
			fallOffValue = dataBlock.inputValue(stickyDeformer.fallOff).asDouble()
			
			moveTestArray = om.MIntArray() #[0]*self.inMeshPoints.length()
			
			globalCollision = 0
			globalSticky = 0
			
			while not iter.isDone():

				index = iter.index()
				
				raySource = om.MFloatPoint(self.inMeshPoints[index].x , self.inMeshPoints[index].y , self.inMeshPoints[index].z )
				rayDirection = om.MFloatVector(inMeshNormals[index])


				# MeshFn.allIntersections variables
				faceIds = None
				triIds = None
				idsSorted = True
				space = om.MSpace.kWorld
				maxParam = searchRadius/10
				tolerance = 1e-20

				#print searchRadius
				
				# testBothDirs = False
				testBothDirs = True
				accelParams = self.mmAccelParams
				sortHits = True
				hitPoints = om.MFloatPointArray()
				hitRayParams = om.MFloatArray()
				hitFaces = om.MIntArray()
				hitTriangles = None
				hitBary1s = None
				hitBary2s = None
				
				uvSet = None
				
				gotHit = 0
				
				try:
					gotHit = targetMeshFn.allIntersections( raySource,rayDirection, faceIds, triIds, idsSorted, space, maxParam, testBothDirs, accelParams,sortHits, hitPoints, hitRayParams, hitFaces, hitTriangles, hitBary1s, hitBary2s )
				except:
					print 'aie'
				
				collision = 0
				
				if gotHit:

					# getting hitsTrue
					collicionCheck = 1
					hitCount = hitPoints.length()
					signChange = 0
					hitPoint = om.MPoint(hitPoints[0].x, hitPoints[0].y, hitPoints[0].z)

					for i in range(hitCount-1):
						if hitRayParams[i] * hitRayParams[i+1] < 0:
							signChange = i
					
						else:
							signChange = -1000

					if hitCount ==2 and signChange+1 ==1 and signChange != -1000:
						collision = 1
					elif hitCount >2 and hitCount/(signChange+1) != 2 and signChange != -1000:
						collision = 1
						
					if collision == 1:
						
						globalCollision = 1
						
						closestPnt = om.MPoint()
						closestPntOnMesh = om.MPointOnMesh()
						
						meshIntersect.getClosestPoint(self.newPoints[index],closestPntOnMesh)
						
						closestPnt = closestPntOnMesh.getPoint()
						closestNormal = om.MVector(closestPntOnMesh.getNormal())
						faceIndex = closestPntOnMesh.faceIndex()
						
						resultPoint = om.MPoint()

						if collisionMethod == 0:
							# newPoint = raytrace hitPoint
							#print 'ray'
							resultPoint.x = hitPoint.x
							resultPoint.y = hitPoint.y
							resultPoint.z = hitPoint.z 
							
							# getting uv at collision points
						
							uvUtil = om.MScriptUtil()
							uvUtil.createFromList([0.0, 0.0], 2)
							uvPoint = uvUtil.asFloat2Ptr()		
							
							hitFaceUtil = om.MScriptUtil()
							hitFaceUtil.createFromInt(hitFaces[0])
							hitFace = hitFaceUtil.asIntPtr()	   
							
							targetMeshFn.getUVAtPoint(hitPoint, uvPoint, om.MSpace.kWorld, uvSet, hitFace) 

							u = om.MScriptUtil.getFloat2ArrayItem(uvPoint, 0, 0)
							v = om.MScriptUtil.getFloat2ArrayItem(uvPoint, 0, 1)
							
							self.uvArray[index].x = u
							self.uvArray[index].y = v
							self.faceIndexArray[index] = hitFaces[0]
							
						elif collisionMethod == 1:
							# newPoint = closestPoint
							#print 'closest'
											
							resultPoint = closestPnt * targetFloatMatValue 
							
							# getting uv at collision points
						
							uvUtil = om.MScriptUtil()
							uvUtil.createFromList([0.0, 0.0], 2)
							uvPoint = uvUtil.asFloat2Ptr() 
							
							hitFaceUtil = om.MScriptUtil()
							hitFaceUtil.createFromInt(faceIndex)
							hitFace = hitFaceUtil.asIntPtr()	   

							targetMeshFn.getUVAtPoint	(om.MPoint(resultPoint) , uvPoint, om.MSpace.kWorld, uvSet, hitFace) 

							u = om.MScriptUtil.getFloat2ArrayItem(uvPoint, 0, 0)
							v = om.MScriptUtil.getFloat2ArrayItem(uvPoint, 0, 1)
							
							self.uvArray[index].x = u
							self.uvArray[index].y = v
							self.faceIndexArray[index] = faceIndex
							
						elif collisionMethod == 2:
								
							#print 'hybrid'
							# newPoint = hybridTest
							
							closestPntTmp = closestPnt * targetFloatMatValue 
																														
							resultPoint.x = hitPoint.x + hybridBlendValue * ( closestPntTmp.x - hitPoint.x)
							resultPoint.y = hitPoint.y + hybridBlendValue * ( closestPntTmp.y - hitPoint.y)
							resultPoint.z = hitPoint.z + hybridBlendValue * ( closestPntTmp.z - hitPoint.z)	 
							
							#closestPnt = om.MPoint()
							#closestPntOnMesh = om.MPointOnMesh()	
							#
							#meshIntersect.getClosestPoint(resultPoint,closestPntOnMesh)
							#
							#closestPnt = closestPntOnMesh.getPoint()
							#resultPoint = closestPnt											
							
						self.newPoints[index].x +=	(resultPoint.x - self.newPoints[index].x )
						self.newPoints[index].y +=	(resultPoint.y - self.newPoints[index].y )
						self.newPoints[index].z +=	(resultPoint.z - self.newPoints[index].z )

						self.hasBeenCollide[index] = 1
						
						
						collideCheck = 0
						
						for i in xrange(self.collisionIndexArray.length()):
							
							if self.collisionIndexArray[i] == index:
								
								collideCheck = 1
								
						if collideCheck == 0:
							
							self.collisionIndexArray.append(index)
							self.deformed += 1
							
				if	collision == 0:
						
					self.newPoints[index].x = self.inMeshPoints[index].x
					self.newPoints[index].y = self.inMeshPoints[index].y
					self.newPoints[index].z = self.inMeshPoints[index].z 
				
				# keeping trace of collision
				moveTestArray.append(collision)
					
				if stickyTest == 1 and self.hasBeenCollide[index] == 1 and collision == 0:
					
					globalSticky = 1
					
					# getting pointAtuv

					u = self.uvArray[index].x
					v = self.uvArray[index].y
					
					uvUtil = om.MScriptUtil()
					uvUtil.createFromList([u, v], 2)
					uvPoint = uvUtil.asFloat2Ptr() 
					
					stickyPoint = om.MPoint()
					
					# try because sometimes uvPoint isn't correct...
					try:
						targetMeshFn.getPointAtUV( self.faceIndexArray[index], stickyPoint, uvPoint, om.MSpace.kObject, uvSet, 0.0)		
						
						curDist = self.inMeshPoints[index].distanceTo(stickyPoint)
						
						maxDist = dataBlock.inputValue(stickyDeformer.maxDistance).asDouble()
						
						if curDist < maxDist:
							
							self.newPoints[index].x	 = stickyPoint.x
							self.newPoints[index].y	 = stickyPoint.y
							self.newPoints[index].z	 = stickyPoint.z 
							
						else:
							
							self.newPoints[index].x = self.inMeshPoints[index].x
							self.newPoints[index].y = self.inMeshPoints[index].y
							self.newPoints[index].z = self.inMeshPoints[index].z 
							
							self.hasBeenCollide[index] = 0
							self.deformed -= 1
							self.fallOffAttractArray[index] = -1
						
							for i in xrange(self.collisionIndexArray.length()):
							
								if self.collisionIndexArray[i] == index:
								
									self.collisionIndexArray.remove(i)

					except:
						
						self.newPoints[index].x = self.inMeshPoints[index].x
						self.newPoints[index].y = self.inMeshPoints[index].y
						self.newPoints[index].z = self.inMeshPoints[index].z
						
					
				iter.next()
				

			iter.reset()
			
			if fallOffValue > 0.0 and self.deformed > 0 :#and globalSticky == 1:
				
				while not iter.isDone():

					index = iter.index()
					
					if self.hasBeenCollide[index] == 0:
							
						dist = 10000
						displaceVect = om.MVector()

						for i in xrange(self.collisionIndexArray.length()):
							
							indexTmp = self.collisionIndexArray[i]
								
							distTmp = self.inMeshPoints[index].distanceTo(self.inMeshPoints[indexTmp])
							
							attractIndex = None
							
							if distTmp < dist:
								
								dist = distTmp
									
								displaceVect = self.newPoints[indexTmp] - self.inMeshPoints[indexTmp]
								
								attractIndex = indexTmp

						magnitude = self.smoothStep( -dist, -fallOffValue, 0)
						magnitude = max(min(magnitude, 1), 0)
							
						displace = displaceVect.length()
						maxDist = 1
						
						if magnitude != 0.0:
							
							moveTestArray[index] = 1

						self.newPoints[index].x += ( displaceVect.x * magnitude )
						self.newPoints[index].y += ( displaceVect.y * magnitude )
						self.newPoints[index].z += ( displaceVect.z * magnitude )

					else:
						
						moveTestArray[index] = 0
						
					iter.next()
				
			iter.reset()
			
			smoothMethod = dataBlock.inputValue(self.smoothMethod).asShort()	
			
			if smoothMethod != 0:

				steps 			= dataBlock.inputValue(stickyDeformer.steps).asShort()
				relaxFactor1 	= dataBlock.inputValue(stickyDeformer.relaxFactor1Att).asDouble()
				relaxFactor2 	= dataBlock.inputValue(stickyDeformer.relaxFactor2Att).asDouble()
				
				if smoothMethod == 1:
					
					self.newPoints = self.laplacianMethod(self.newPoints.length(), self.newPoints, self.vtxNeighbArray, moveTestArray, relaxFactor1 , steps)
				
				if smoothMethod == 2:
					
					self.newPoints = self.taubinMethod(self.newPoints.length(), self.newPoints, self.vtxNeighbArray, moveTestArray, relaxFactor1, (relaxFactor2/100), steps)				
				
				if smoothMethod == 3:
					
					self.newPoints = self.bilateralMethod(self.newPoints.length(), self.newPoints, inMeshNormals, self.vtxNeighbArray, moveTestArray, relaxFactor1, relaxFactor2, steps)		
				
				while not iter.isDone():

					if moveTestArray[index] == 1 and self.hasBeenCollide[index] == 0:
						meshIntersect.getClosestPoint(self.newPoints[index],closestPntOnMesh)
								
						closestPnt 		= closestPntOnMesh.getPoint()
						closestNormal 	= om.MVector(closestPntOnMesh.getNormal())
						
						self.newPoints[index].x = closestPnt.x
						self.newPoints[index].y = closestPnt.y
						self.newPoints[index].z = closestPnt.z 
					
					iter.next()

			iter.setAllPositions(self.newPoints)
			
			collideArrayData	= om.MFnIntArrayData()
			collideArrayTmp		= collideArrayData.create(copy.copy(self.hasBeenCollide))
			collideOutputHandle = dataBlock.outputValue(stickyDeformer.collideArray)
			collideOutputHandle.setMObject( collideArrayTmp )

			uvArrayData 		= om.MFnPointArrayData()
			uvArrayTmp			= uvArrayData.create(copy.copy(self.uvArray))
			uvOutputHandle		= dataBlock.outputValue(stickyDeformer.uvArray)
			uvOutputHandle.setMObject( uvArrayTmp )

			facesArrayData		= om.MFnIntArrayData()
			faceArrayTmp		= facesArrayData.create(copy.copy(self.faceIndexArray))
			faceOutputHandle	= dataBlock.outputValue(stickyDeformer.faceIndexArray)
			faceOutputHandle.setMObject( faceArrayTmp )			

########################################################################################
########################################################################################

	#Linear step fonction
	def linStep(self, U, a, b):
		return (U - a) * (1.0 / (b - a))
		
	#smooth step fonction	
	def smoothStep(self, U, a, b):

		if U < a:
			return 0.0
		if U > b:
			return 1.0

		U = (U - a)/(b - a)
		return U * U * (3.0 - 2.0 * U)
		
########################################################################################
########################################################################################		
		
	def getBoundingBox(self, pMeshObj, pBoundingBoxScale):
		''' Calculate a bounding box around the mesh's vertices. '''
		
		# Create the bounding box object we will populate with the points of the mesh.
		boundingBox = om.MBoundingBox()
		meshFn = om.MFnMesh( pMeshObj )
		pointArray = om.MPointArray()
		
		# Get the points of the mesh in its local coordinate space.
		meshFn.getPoints( pointArray, om.MSpace.kTransform )
	
		for i in range( 0, pointArray.length() ):
			point = pointArray[i]
			boundingBox.expand( point )
		
		# Expand the bounding box according to the scaling factor.
		newMinPoint = boundingBox.min() * pBoundingBoxScale
		newMaxPoint = boundingBox.max() * pBoundingBoxScale
		boundingBox.expand( newMinPoint )
		boundingBox.expand( newMaxPoint )
		
		return boundingBox
########################################################################################
########################################################################################

	def floatMMatrixToMMatrix(self, fm):
		mat = om.MMatrix()
		om.MScriptUtil.createMatrixFromList ([
			fm(0,0),fm(0, 1),fm(0, 2),fm(0, 3),
			fm(1,0),fm(1, 1),fm(1, 2),fm(1, 3),
			fm(2,0),fm(2, 1),fm(2, 2),fm(2, 3),
			fm(3,0),fm(3, 1),fm(3, 2),fm(3, 3)], mat)
	
		return mat
				
########################################################################################
########################################################################################

	def laplacianMethod(self, vtxCount, noSmoothArray, vtxNeighborsArray, pntMoveTestArray, lambd, step):
	
		#- Do smoothing.
		#
		newPoints = om.MPointArray()
		currentPoint = om.MPoint()
		pointArrayTmp = om.MPointArray
	
		for s in xrange(step):
	
			if s == 0:
	
				pointArrayTmp = copy.copy(noSmoothArray)
	
			for i in xrange(vtxCount):
	
				moveTest = pntMoveTestArray[i];
				
				currentPoint = pointArrayTmp[i];
				neighbors = vtxNeighborsArray[i];
				
				# Calculate new position.
				#
				if moveTest == 1:
	
					weightedPoint = om.MPoint()
					WeightsIndex = 0
					weightSum = 0.0
					
					for j in xrange(neighbors.length()):
						
						neighborPoint = om.MPoint()
						neighborPoint = pointArrayTmp[neighbors[j]]
					
						neighbDist = neighborPoint - currentPoint
					
						weight = 1.0 / neighbDist.length()
						weightedPoint += neighbDist*weight
					
						weightSum += weight
	
					weightedPoint = weightedPoint / weightSum
					
					pointArrayTmp[i].x = (pointArrayTmp[i].x + (weightedPoint.x * lambd))
					pointArrayTmp[i].y = (pointArrayTmp[i].y + (weightedPoint.y * lambd))
					pointArrayTmp[i].z = (pointArrayTmp[i].z + (weightedPoint.z * lambd)) 
				
				if moveTest == 0:
			
					pointArrayTmp[i].x = currentPoint.x
					pointArrayTmp[i].y = currentPoint.y
					pointArrayTmp[i].z = currentPoint.z 
	
		return pointArrayTmp
	
	
	
########################################################################################
########################################################################################
	
	def taubinMethod(self, vtxCount, noSmoothArray, vtxNeighborsArray, pntMoveTestArray, lambd, mu, step):
	
		# Do smoothing.
		# 
		newPoints = om.MPointArray()
		currentPoint = om.MPoint()
		pointArrayTmp = om.MPointArray()
	
		factors = [0]*2
		factors[0] = lambd
		factors[1] = 1 / (mu - (1/(lambd)))
		
		for q in xrange( step ):
	
			for s in xrange(2):
	
				if q == 0:
					
					pointArrayTmp= copy.copy(noSmoothArray)
					
	
				for i in xrange(vtxCount):
	
					moveTest = pntMoveTestArray[i]
					
					currentPoint = pointArrayTmp[i]
					neighbors = vtxNeighborsArray[i]
					
					# Calculate new position.
					#
					if moveTest == 1:
	
						weightedPoint = om.MPoint()
	
						for j in xrange(neighbors.length()):
	
							neighborPoint = om.MPoint()
							neighborPoint = pointArrayTmp[neighbors[j]]
							
							neighbDist = currentPoint - neighborPoint
							
							weight = 1.0 / neighbDist.length()
							weightedPoint += neighbDist
	
						pointArrayTmp[i].x = currentPoint.x + ((weightedPoint.x / neighbors.length()) * factors[s] )
						pointArrayTmp[i].y = currentPoint.y + ((weightedPoint.y / neighbors.length()) * factors[s] )
						pointArrayTmp[i].z = currentPoint.z + ((weightedPoint.z / neighbors.length()) * factors[s] )
					
					if moveTest == 0:
						
						pointArrayTmp[i].x = currentPoint.x
						pointArrayTmp[i].y = currentPoint.y
						pointArrayTmp[i].z = currentPoint.z
	
		return pointArrayTmp
	
	
########################################################################################
########################################################################################
	
	def bilateralMethod(self, vtxCount, noSmoothArray, normalsArray, vtxNeighborsArray, pntMoveTestArray, lambd, mu, step):
	
		# Do smoothing.
		# 
		newPoints = om.MPointArray()
		currentPoint = om.MPoint()
		currentNormal = om.MVector()
		pointArrayTmp = om.MPointArray()
	
		for q in xrange(step):
		
			if q == 0:
	
				pointArrayTmp.copy(noSmoothArray)
	
	
	
			for i in xrange(vtxCount):
	
				moveTest = pntMoveTestArray[i]
				
				currentPoint = pointArrayTmp[i]
				currentNormal = normalsArray[i]
				neighbors = vtxNeighborsArray[i]
				
				# Calculate new position.
				#
				if moveTest == 1:
	
	
					currentNormal.normalize()
	
					sum = 0.0
					normalizer = 0.0
					
					for j in xrange(neighbors.length()):
	
						neighborPoint = om.MPoint()
						neighborPoint = pointArrayTmp[neighbors[j]]
						
						E = neighborPoint - currentPoint
	
						t = E.length()
	
						h = E.x*currentNormal.x + E.y*currentNormal.y + E.z*currentNormal.z
						omegaC = math.exp(-t*t/(2.0*lambd*mu))
						omegaS = math.exp(-t*t/(2.0*lambd*lambd))
	
						sum += omegaC*omegaS*h
						normalizer += omegaC*omegaS
	
					pointArrayTmp[i].x = currentPoint.x + currentNormal.x*( sum/normalizer )
					pointArrayTmp[i].y = currentPoint.y + currentNormal.y*( sum/normalizer )
					pointArrayTmp[i].z = currentPoint.z + currentNormal.z*( sum/normalizer )
				if moveTest == 0:
						
					pointArrayTmp[i].x = currentPoint.x
					pointArrayTmp[i].y = currentPoint.y
					pointArrayTmp[i].z = currentPoint.z
					
		return pointArrayTmp
	
	
			
########################################################################################
########################################################################################
	
	def initializeSelfVariables(self, oInputGeom, dataBlock):
	
	
		#self.thisNode	= self.thisMObject()
		
		# declaring node for global var
		#
		# filling all the ref arrays
		#
		# Get reference Normals
	
		# Mesh iterator declaration
		vtxIter = om.MItMeshVertex(oInputGeom)
	
		# getting neghbors points
		while not vtxIter.isDone():
	
			# getting per vertex neighbors to fill self.neighborsPnts
			vtxNeighbArrayTmp = om.MIntArray()
		
			index = vtxIter.index()
			vtxIter.getConnectedVertices(vtxNeighbArrayTmp)
	
			self.vtxNeighbArray.append(vtxNeighbArrayTmp)
		
			curdDistList = om.MDoubleArray()
	
			# for each neighbor get the distance from current vertex
			test1 = self.inMeshPoints[index]
	
			for m in xrange(vtxNeighbArrayTmp.length()):
	
				curPtn = vtxNeighbArrayTmp[m]
				test2 = om.MPoint(self.inMeshPoints[curPtn])
				test = test1.distanceTo(test2)
				curdDistList.append(test)
	
			self.fallOffAttractArray.append(-1)
			self.fallOffActiveArray.append(0)
				
			vtxIter.next()
			
		
		
		collideArrayTmp = dataBlock.inputValue(stickyDeformer.collideArray).data()
		uvArrayTmp = dataBlock.inputValue(stickyDeformer.uvArray).data()
		faceIndexArrayTmp = dataBlock.inputValue(stickyDeformer.faceIndexArray).data() 
		
		try:
			collideDataTmp = om.MFnIntArrayData(collideArrayTmp)
			self.hasBeenCollide = collideDataTmp.array()
			
			print '### Init ###'
		except:
			 
			for i in xrange(self.inMeshPoints.length()):
				
				self.hasBeenCollide.append(0)
				
			print '### First Init ###'
				
		try:
			uvDataTmp = om.MFnPointArrayData(uvArrayTmp)
			self.uvArray = uvDataTmp.array()
			
			print '### UV Init ###'
		except:
			 
			for i in xrange(self.inMeshPoints.length()):
				
				poinTmp = om.MPoint(0, 0, 0, 0)
				self.uvArray.append(poinTmp)
				
			print '### First UV Init ###'
			
		try:
			faceIndexDataTmp = om.MFnIntArrayData(faceIndexArrayTmp)
			self.faceIndexArray = faceIndexDataTmp.array()
			
			print '### FaceIndex Init ###'
		except:
			 
			for i in xrange(self.inMeshPoints.length()):
				
				self.faceIndexArray.append(0)
				
			print '### First FaceIndex Init ###'
			
		# Getting poly
		
		polyIter = om.MItMeshPolygon(oInputGeom)
		
		while not polyIter.isDone():
			
			index = polyIter.index()
			
			self.vtxPolyIndex.append(index)
			array = om.MIntArray()
			polyIter.getVertices(array)
			self.vtxPerPoly.append(array)
			
			polyIter.next()
########################################################################################
########################################################################################

# initializer
def nodeInitializer():

	nAttr = om.MFnNumericAttribute()
	gAttr = om.MFnGenericAttribute()
	uAttr = om.MFnUnitAttribute()
	mAttr = om.MFnMatrixAttribute()
	eAttr = om.MFnEnumAttribute()
	tAttr = om.MFnTypedAttribute()
	
	stickyDeformer.firstTimeAtt = nAttr.create( "firstTimev", "ft", om.MFnNumericData.kShort, 1)
	nAttr.setStorable(False)
	nAttr.setHidden(True)
	
	stickyDeformer.targetMesh = gAttr.create( "targetMesh", "tMsh")
	gAttr.addDataAccept( om.MFnData.kMesh )

	stickyDeformer.currentTime = uAttr.create("currentTime", "time", om.MFnUnitAttribute.kTime, 1.0)
	uAttr.setKeyable(True)

	stickyDeformer.weight = nAttr.create("weight", "wt", om.MFnNumericData.kFloat, 1)
	nAttr.setMin(0.0)
	nAttr.setKeyable(True)

	stickyDeformer.collisionMethod = eAttr.create("collisionMethod", "method", 0)
	eAttr.addField('rayTrace', 0)
	eAttr.addField('closestPoint', 1)
	eAttr.addField('hybridBlending', 2)
	eAttr.setKeyable(True)
	
	stickyDeformer.hybridBlend = nAttr.create("hybridBlend", "hb", om.MFnNumericData.kFloat, .5)
	nAttr.setMin(0.0)
	nAttr.setMax(1.0)
	nAttr.setKeyable(True)
	
	stickyDeformer.stickyness = nAttr.create("stickyness", "sticky", om.MFnNumericData.kShort, 1)
	nAttr.setMin(0)
	nAttr.setMax(1)
	nAttr.setKeyable(True)	
	
	stickyDeformer.maxDistance = nAttr.create("maxDistance", "maxDist", om.MFnNumericData.kDouble, 0.5)
	nAttr.setMin(0.001)
	nAttr.setKeyable(True)	
	
	stickyDeformer.smoothMethod = eAttr.create("smoothMethod", "sm", 0)
	eAttr.addField('OFF', 0)
	eAttr.addField('Laplacian', 1)
	eAttr.addField('Taubin', 2)
	eAttr.addField('Bilateral', 3)
	eAttr.setKeyable(True)
	
	stickyDeformer.steps = nAttr.create("steps", "steps", om.MFnNumericData.kShort, 1)
	nAttr.setMin(False)
	nAttr.setKeyable(True)	
	
	stickyDeformer.relaxFactor1Att = nAttr.create("relaxFactor1", "reFact1", om.MFnNumericData.kDouble, 0.1)
	nAttr.setMin(0.001)
	nAttr.setMax(.999)
	nAttr.setKeyable(True)

	stickyDeformer.relaxFactor2Att = nAttr.create("relaxFactor2", "reFact2", om.MFnNumericData.kDouble, .999)
	nAttr.setMin(0.001)
	nAttr.setMax(.999)
	nAttr.setKeyable(True)
	
	stickyDeformer.targetMatrix = mAttr.create("targetMatrix", "targMatr", om.MFnNumericData.kFloat )
	
	stickyDeformer.collideArray = tAttr.create("collideArray", "collArray", om.MFnIntArrayData.kIntArray)
	tAttr.setStorable(True)
	tAttr.setKeyable(False)
	tAttr.setHidden(True)

	stickyDeformer.uvArray = tAttr.create("uvArray", "uvA", om.MFnPointArrayData.kPointArray)
	tAttr.setStorable(True)
	tAttr.setKeyable(False)
	tAttr.setHidden(True)
	
	stickyDeformer.faceIndexArray = tAttr.create("faceIndexArray", "fvA", om.MFnIntArrayData.kIntArray)
	tAttr.setStorable(True)
	tAttr.setKeyable(False)
	tAttr.setHidden(True)
	
	stickyDeformer.fallOff = nAttr.create("fallOff", "fall", om.MFnNumericData.kDouble, 0.00000001)
	nAttr.setMin(0.00000001)
	nAttr.setKeyable(True)

	stickyDeformer.addAttribute(stickyDeformer.firstTimeAtt )
	stickyDeformer.addAttribute(stickyDeformer.targetMesh )
	stickyDeformer.addAttribute(stickyDeformer.currentTime)
	stickyDeformer.addAttribute(stickyDeformer.targetMatrix)
	stickyDeformer.addAttribute(stickyDeformer.collisionMethod)
	stickyDeformer.addAttribute(stickyDeformer.hybridBlend)
	stickyDeformer.addAttribute(stickyDeformer.stickyness)
	stickyDeformer.addAttribute(stickyDeformer.maxDistance)
	stickyDeformer.addAttribute(stickyDeformer.smoothMethod)
	stickyDeformer.addAttribute(stickyDeformer.steps)
	stickyDeformer.addAttribute(stickyDeformer.relaxFactor1Att)
	stickyDeformer.addAttribute(stickyDeformer.relaxFactor2Att)
	stickyDeformer.addAttribute(stickyDeformer.fallOff)
	stickyDeformer.addAttribute(stickyDeformer.weight)
	stickyDeformer.addAttribute(stickyDeformer.collideArray)
	stickyDeformer.addAttribute(stickyDeformer.uvArray)
	stickyDeformer.addAttribute(stickyDeformer.faceIndexArray)

	outputGeom = omMPx.cvar.MPxDeformerNode_outputGeom

	stickyDeformer.attributeAffects(stickyDeformer.firstTimeAtt, outputGeom )
	stickyDeformer.attributeAffects(stickyDeformer.targetMesh, outputGeom )
	stickyDeformer.attributeAffects(stickyDeformer.currentTime, outputGeom )
	stickyDeformer.attributeAffects(stickyDeformer.collisionMethod, outputGeom )
	stickyDeformer.attributeAffects(stickyDeformer.hybridBlend, outputGeom )
	stickyDeformer.attributeAffects(stickyDeformer.stickyness, outputGeom )
	stickyDeformer.attributeAffects(stickyDeformer.maxDistance, outputGeom )
	stickyDeformer.attributeAffects(stickyDeformer.smoothMethod, outputGeom )
	stickyDeformer.attributeAffects(stickyDeformer.steps, outputGeom )
	stickyDeformer.attributeAffects(stickyDeformer.relaxFactor1Att, outputGeom )
	stickyDeformer.attributeAffects(stickyDeformer.relaxFactor2Att, outputGeom )
	stickyDeformer.attributeAffects(stickyDeformer.fallOff, outputGeom )
	stickyDeformer.attributeAffects(stickyDeformer.targetMatrix, outputGeom )
	stickyDeformer.attributeAffects(stickyDeformer.weight, outputGeom )

	
########################################################################################
########################################################################################

def nodeCreator():
	return omMPx.asMPxPtr( stickyDeformer() )


#######################################################################################
########################################################################################

# initialize the script plug-in
def initializePlugin(mobject):
	mplugin = omMPx.MFnPlugin(mobject)
	try:
		mplugin.registerNode( kPluginNodeTypeName, stickyDeformerId, nodeCreator, nodeInitializer, omMPx.MPxNode.kDeformerNode )
	except:
		sys.stderr.write( "Failed to register node: %s\n" % kPluginNodeTypeName )

########################################################################################
########################################################################################

# uninitialize the script plug-in
def uninitializePlugin(mobject):
	mplugin = omMPx.MFnPlugin(mobject)
	try:
		mplugin.deregisterNode( stickyDeformerId )
	except:
		sys.stderr.write( "Failed to unregister node: %s\n" % kPluginNodeTypeName )
