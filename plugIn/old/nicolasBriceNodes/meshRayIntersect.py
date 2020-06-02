"""
closestPoint on Mesh


delete "meshRayIntersect1";
flushUndo;

unloadPluginWithCheck( "D:/C++/Python sources/meshRayIntersect.py" );
loadPlugin( "D:/C++/Python sources/meshRayIntersect.py"	 );

createNode "meshRayIntersect" -n "meshRayIntersect1";

connectAttr -f startShape.worldPosition[0] meshRayIntersect1.startPosition;
connectAttr -f targetShape.worldPosition[0] meshRayIntersect1.targetPosition;
connectAttr -f meshRayIntersect1.outPosition result.translate;
connectAttr -f meshShape.outMesh meshRayIntersect1.inMesh;


"""

########################################################################################
########################################################################################

import math, sys, copy
import maya.OpenMaya as om
import maya.OpenMayaAnim as omAnim
import maya.OpenMayaMPx as omMPx
import maya.cmds as cmds
import time

nodeName = "meshRayIntersect"
meshRayIntersectId = om.MTypeId(0x52533)

########################################################################################
########################################################################################

class meshRayIntersect(omMPx.MPxNode):

	
	# 'frameIteration' is there for further backward time scaling
	def __init__(self):
		
		# empty node's variables

		self.targetPos		= om.MObject()
		self.weight			= om.MObject()
		self.inMesh			= om.MObject()
		self.offset		   = om.MObject() 
		omMPx.MPxNode.__init__(self)
		
########################################################################################

	def compute(self, plug, dataBlock):
		
		thisNode = self.thisMObject()
		
		# node's attributs declaration
		self.startPos	= dataBlock.inputValue(self.startPosAttr).asFloat3()
		self.targetPos	= dataBlock.inputValue(self.targetPosAttr).asFloat3()
		self.weight		= dataBlock.inputValue(self.weightAttr).asDouble()
		self.offset		= dataBlock.inputValue(self.offsetAttr).asDouble()
		maxDist			= dataBlock.inputValue(self.maxDistAttr).asDouble()
		minDist			= dataBlock.inputValue(self.minDistAttr).asDouble()
		
		#refShape

		meshData	= dataBlock.inputValue(self.inMeshAttr).asMesh()
		plugInMesh	= om.MPlug( thisNode, self.inMeshAttr )
		
		if( plugInMesh.isConnected() == True):
			
			inMeshFn = om.MFnMesh(meshData)
			
			startPnt	= om.MPoint(self.startPos[0], self.startPos[1], self.startPos[2])
			targetPnt	= om.MPoint(self.targetPos[0], self.targetPos[1], self.targetPos[2])
			
			rayVect = targetPnt - startPnt
			
			#allIntersections variables declaration
			#ray is trace from rotate pivot along closest point's normal
			#hit point gives radius of the ball
			raySource			= om.MFloatPoint(startPnt.x, startPnt.y, startPnt.z)
			rayDirection		= om.MFloatVector(rayVect.x, rayVect.y, rayVect.z)
			faceIds				= None
			triIds				= None
			isSorted			= False
			maxParam			= 1000000000
			testBothDirections	= False
			accelParams			= inMeshFn.autoUniformGridParams()
			sortHits			= True
			hitPoints			= om.MFloatPointArray()
			hitRayParams		= om.MFloatArray()
			hitFaces			= om.MIntArray()
			hitTriangles		= om.MIntArray()
			hitBary1s			= om.MFloatArray()
			hitBary2s			= om.MFloatArray()
			tolerance			= 0.0001
		  
			#allIntersections method
			try:
				testHit = inMeshFn.allIntersections(raySource, rayDirection, faceIds, triIds, isSorted, om.MSpace.kWorld, maxParam, testBothDirections, accelParams, sortHits, hitPoints, hitRayParams, hitFaces, hitTriangles, hitBary1s, hitBary2s, tolerance )
			except:
				print 'aie'
				
			if testHit:
				
				#getting vectors
				hitPnt1 = hitPoints[0]
				
				distanceVect = om.MVector(om.MPoint(hitPnt1.x, hitPnt1.y, hitPnt1.z) - startPnt)
				distance	 = distanceVect.length()
				
				tagetDistVect	= om.MVector(om.MPoint(hitPnt1.x, hitPnt1.y, hitPnt1.z) - targetPnt)
				targetDistance	= tagetDistVect.length()

				tagetDistVect.normalize()
				
				if (distance > rayVect.length()) and (targetDistance > maxDist) and (maxDist != 0):
					
					hitPnt1 = targetPnt + (tagetDistVect * (maxDist))
					
				if (distance < rayVect.length()) and (targetDistance > minDist) and (minDist != 0):
					
					hitPnt1 = targetPnt + (tagetDistVect * (minDist))
					
			else:

				hitPnt1	 = targetPnt
				distance = 0
			
			# output variable
			self.posOutHandle	= dataBlock.outputValue(self.outPositionAttr)
			self.posOutHandle.set3Float(hitPnt1.x, hitPnt1.y, hitPnt1.z)
			
			self.distanceOutHandle	= dataBlock.outputValue(self.distanceAttr)
			self.distanceOutHandle.setDouble(distance)

		dataBlock.setClean(plug)															# set plug clean after compute 

########################################################################################
########################################################################################

def nodeCreator():
	return omMPx.asMPxPtr(meshRayIntersect())

########################################################################################
########################################################################################

def nodeInitializer():
   
	nAttr = om.MFnNumericAttribute()
	meshRayIntersect.startPosAttr = nAttr.createPoint("startPosition", "startpos")
	nAttr.setKeyable(True)

	meshRayIntersect.targetPosAttr = nAttr.createPoint("targetPosition", "targPos")
	nAttr.setKeyable(True)
	
	meshRayIntersect.maxDistAttr = nAttr.create("maxDistance", "maxDist", om.MFnNumericData.kDouble, 0)
	nAttr.setKeyable(True)
	nAttr.setMin(0.0)

	meshRayIntersect.minDistAttr = nAttr.create("minDistance", "minDist", om.MFnNumericData.kDouble, 0)
	nAttr.setKeyable(True)
	nAttr.setMin(0.0)
	
	meshRayIntersect.offsetAttr = nAttr.create("offset", "offs", om.MFnNumericData.kDouble, 0)
	nAttr.setKeyable(True)
	
	gAttr = om.MFnGenericAttribute()
	meshRayIntersect.inMeshAttr = gAttr.create( "inMesh", "inMh")
	gAttr.addDataAccept( om.MFnData.kMesh )
	
	meshRayIntersect.weightAttr = nAttr.create("weight", "wt", om.MFnNumericData.kDouble, 1)
	nAttr.setMin(0.0)
	nAttr.setKeyable(True)

	meshRayIntersect.outPositionAttr = nAttr.createPoint("outPosition", "outPos")
	nAttr.setWritable(False)
   
	meshRayIntersect.outOrientAttr = nAttr.createPoint("outOrient", "outOri")
	nAttr.setWritable(False)
   
	meshRayIntersect.distanceAttr = nAttr.create("resultDistance", "resdist", om.MFnNumericData.kDouble, 1)
	#nAttr.setWritable(False)
	nAttr.setReadable(True)
	nAttr.setChannelBox(True)
	nAttr.setHidden(False)
	
	meshRayIntersect.addAttribute(meshRayIntersect.startPosAttr)
	meshRayIntersect.addAttribute(meshRayIntersect.targetPosAttr)
	meshRayIntersect.addAttribute(meshRayIntersect.maxDistAttr)
	meshRayIntersect.addAttribute(meshRayIntersect.minDistAttr)
	meshRayIntersect.addAttribute(meshRayIntersect.offsetAttr)
	meshRayIntersect.addAttribute(meshRayIntersect.inMeshAttr)
	meshRayIntersect.addAttribute(meshRayIntersect.weightAttr)
	meshRayIntersect.addAttribute(meshRayIntersect.outPositionAttr)
	meshRayIntersect.addAttribute(meshRayIntersect.outOrientAttr)
	meshRayIntersect.addAttribute(meshRayIntersect.distanceAttr)

	
	meshRayIntersect.attributeAffects(meshRayIntersect.startPosAttr, meshRayIntersect.outPositionAttr)
	meshRayIntersect.attributeAffects(meshRayIntersect.targetPosAttr, meshRayIntersect.outPositionAttr)
	meshRayIntersect.attributeAffects(meshRayIntersect.targetPosAttr, meshRayIntersect.distanceAttr)
	
	meshRayIntersect.attributeAffects(meshRayIntersect.startPosAttr, meshRayIntersect.outOrientAttr)
	meshRayIntersect.attributeAffects(meshRayIntersect.targetPosAttr, meshRayIntersect.outOrientAttr)
	meshRayIntersect.attributeAffects(meshRayIntersect.targetPosAttr, meshRayIntersect.distanceAttr)
	
	meshRayIntersect.attributeAffects(meshRayIntersect.inMeshAttr, meshRayIntersect.outPositionAttr)
	meshRayIntersect.attributeAffects(meshRayIntersect.inMeshAttr, meshRayIntersect.outOrientAttr)		
	meshRayIntersect.attributeAffects(meshRayIntersect.inMeshAttr, meshRayIntersect.distanceAttr)
	
	meshRayIntersect.attributeAffects(meshRayIntersect.offsetAttr, meshRayIntersect.outPositionAttr)	
	meshRayIntersect.attributeAffects(meshRayIntersect.offsetAttr, meshRayIntersect.outOrientAttr)		
	meshRayIntersect.attributeAffects(meshRayIntersect.offsetAttr, meshRayIntersect.distanceAttr)		

	meshRayIntersect.attributeAffects(meshRayIntersect.maxDistAttr, meshRayIntersect.outPositionAttr)
	meshRayIntersect.attributeAffects(meshRayIntersect.maxDistAttr, meshRayIntersect.outOrientAttr)
	meshRayIntersect.attributeAffects(meshRayIntersect.maxDistAttr, meshRayIntersect.distanceAttr)

	meshRayIntersect.attributeAffects(meshRayIntersect.minDistAttr, meshRayIntersect.outPositionAttr)
	meshRayIntersect.attributeAffects(meshRayIntersect.minDistAttr, meshRayIntersect.outOrientAttr)
	meshRayIntersect.attributeAffects(meshRayIntersect.minDistAttr, meshRayIntersect.distanceAttr)
	
########################################################################################
########################################################################################
	
def initializePlugin(mobject):
	mplugin = omMPx.MFnPlugin(mobject)
	try:
		mplugin.registerNode(nodeName, meshRayIntersectId, nodeCreator, nodeInitializer)
	except:
		sys.stderr.write("Failed to register node: $s\n" % nodeName)

########################################################################################
########################################################################################

def uninitializePlugin(mobject):
	mplugin = omMPx.MFnPlugin(mobject)
	try:
		mplugin.deregisterNode(meshRayIntersectId)
	except:
		sys.stderr.write("Failed to deregister node: $s\n" % nodeName)

