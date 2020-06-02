"""

"""

import math, sys, copy
import maya.OpenMaya as om
import maya.OpenMayaAnim as omAnim
import maya.OpenMayaMPx as omMPx
from maya.mel import eval as meval
import time

kPluginNodeTypeName = "simpleBlendShape"
simpleBlendShapeId = om.MTypeId(0x0010A52B)

# Node definition
class simpleBlendShape(omMPx.MPxDeformerNode):

	print("---------------node++++++++++++")

	def __init__(self):
		print("INIT_START")
		omMPx.MPxDeformerNode.__init__(self)
		print("INIT_END")
		'''
	def compute( self, plug , dataBlock ):
		print("compute_START")
		omMPx.MPxDeformerNode.compute( self, plug , dataBlock )
		print("compute_END")
	'''
	def deform( self, dataBlock, iter, matrix, index ):

		print('deform_START')
		envelope  = omMPx.cvar.MPxGeometryFilter_envelope
		input     = omMPx.cvar.MPxGeometryFilter_input
		inputGeom = omMPx.cvar.MPxGeometryFilter_inputGeom
		groupId   = omMPx.cvar.MPxGeometryFilter_groupId
		#INPUT
		print('1_ENVELOPE')
		henvelope = dataBlock.inputValue(envelope)
		envelope = henvelope.asFloat()
		#HANDLE
		print('2_OUT MESH INPUT')		
		hInput = dataBlock.inputArrayValue(input)
		hInput.jumpToArrayElement(index)
		hInputElement   = hInput.inputValue()
		self.hInputGeom = hInputElement.child(inputGeom)	
		inMesh          = self.hInputGeom.asMesh()
		inMeshFn        = om.MFnMesh(inMesh)
		print('3_IN TARGET INPUT')
		hInputTarget   = dataBlock.inputValue(self.inTargetMesh)
		inTargetMesh   = hInputTarget.asMesh()
		inTargetMeshFn = om.MFnMesh(inTargetMesh)		
		print('3_IN BASE INPUT')
		hInputBase    = dataBlock.inputValue(self.inBaseMesh)
		inBaseMesh    = hInputBase.asMesh()
		inBaseMeshFn  = om.MFnMesh(inBaseMesh)						
		#GET OUT MESH POINTS
		print('4_GET POINTS INFO')
		self.outBasePoints = om.MPointArray()	
		inMeshFn.getPoints( self.outBasePoints , om.MSpace.kWorld )			
		self.targetPoints = om.MPointArray()
		inTargetMeshFn.getPoints( self.targetPoints , om.MSpace.kWorld )
		self.basePoints = om.MPointArray()
		inBaseMeshFn.getPoints( self.basePoints , om.MSpace.kWorld )	
		self.outPoints = om.MPointArray()	
		#DEFORM	
		print('5_DEFORM')
		p = self.outBasePoints	
		t = self.targetPoints	
		b = self.basePoints	
		e = envelope 								
		while not iter.isDone():
			i = iter.index()
			vDelta = ( t[i] - b[i] )
			vDeltaEnv = om.MVector( e * ( vDelta.x + p[i].x ), e * (vDelta.y  + p[i].y) , e * (vDelta.z  + p[i].z) )
			pBaseEnv =  om.MPoint( (1 - e) * p[i].x , (1 - e) * p[i].y  , (1 - e) * p[i].z )
			#self.outPoints.append( pBaseEnv + vDeltaEnv )
			iter.setPosition(pBaseEnv + vDeltaEnv)
			iter.next()

		#OUT
		print('5_OUT')			
		#iter.setAllPositions(self.outPoints)		  # if CurrentTime = startTime we just move the points
		print('deform_END')

		return True

def nodeCreator():
	return omMPx.asMPxPtr( simpleBlendShape() )

def nodeInitializer():
	print('nodeInitializer_START')
	gAttr = om.MFnGenericAttribute()
	simpleBlendShape.inTargetMesh = gAttr.create( "inTargetMesh", "inTarget")
	gAttr.addDataAccept( om.MFnData.kMesh )
	gAttr.setKeyable(True)

	simpleBlendShape.inBaseMesh = gAttr.create( "inBaseMesh", "inBase")
	gAttr.addDataAccept( om.MFnData.kMesh )
	gAttr.setKeyable(True)

	nAttr = om.MFnNumericAttribute()
	simpleBlendShape.weight = nAttr.create("weight", "wt", om.MFnNumericData.kFloat, 1)
	nAttr.setMin(0.0)
	nAttr.setKeyable(True)

	simpleBlendShape.addAttribute( simpleBlendShape.inTargetMesh )
	simpleBlendShape.addAttribute(simpleBlendShape.inBaseMesh)
	simpleBlendShape.addAttribute(simpleBlendShape.weight)

	outputGeom = omMPx.cvar.MPxGeometryFilter_outputGeom
	simpleBlendShape.attributeAffects(simpleBlendShape.inTargetMesh, outputGeom )
	simpleBlendShape.attributeAffects(simpleBlendShape.inBaseMesh, outputGeom )
	simpleBlendShape.attributeAffects(simpleBlendShape.weight, outputGeom )
	print('nodeInitializer_END')


def initializePlugin(mobject):
	mplugin = omMPx.MFnPlugin(mobject)
	try:
		mplugin.registerNode( kPluginNodeTypeName, simpleBlendShapeId, nodeCreator, nodeInitializer, omMPx.MPxNode.kDeformerNode )
	except:
		sys.stderr.write( "Failed to register node: %s\n" % kPluginNodeTypeName )

def uninitializePlugin(mobject):
	mplugin = omMPx.MFnPlugin(mobject)
	try:
		mplugin.deregisterNode( simpleBlendShapeId )
	except:
		sys.stderr.write( "Failed to unregister node: %s\n" % kPluginNodeTypeName )
        
        
