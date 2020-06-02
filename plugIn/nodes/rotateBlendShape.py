"""

"""

import math, sys, copy
import maya.OpenMaya as om
import maya.OpenMayaAnim as omAnim
import maya.OpenMayaMPx as omMPx
from maya.mel import eval as meval
import time

kPluginNodeTypeName = "rotateBlendShape"
rotateBlendShapeId = om.MTypeId(0x0010A52B)

# Node definition
class rotateBlendShape(omMPx.MPxDeformerNode):

	def __init__(self):
		omMPx.MPxDeformerNode.__init__(self)


	def deform( self, dataBlock, iter, matrix, index ):

		envelope  = omMPx.cvar.MPxGeometryFilter_envelope
		input     = omMPx.cvar.MPxGeometryFilter_input
		inputGeom = omMPx.cvar.MPxGeometryFilter_inputGeom
		groupId   = omMPx.cvar.MPxGeometryFilter_groupId
		#HANDLE ENVELOPE
		henvelope = dataBlock.inputValue(envelope)
		envelope = henvelope.asFloat()

		#HANDLE MESH
		hInput = dataBlock.inputArrayValue(input)
		hInput.jumpToArrayElement(index)
		hInputElement   = hInput.inputValue()
		self.hInputGeom = hInputElement.child(inputGeom)	
		inMesh          = self.hInputGeom.asMesh()
		inMeshFn        = om.MFnMesh(inMesh)

		hInputTarget   = dataBlock.inputValue(self.inTargetMesh)
		inTargetMesh   = hInputTarget.asMesh()
		inTargetMeshFn = om.MFnMesh(inTargetMesh)			

		hInputBase    = dataBlock.inputValue(self.inBaseMesh)
		inBaseMesh    = hInputBase.asMesh()
		inBaseMeshFn  = om.MFnMesh(inBaseMesh)
		
		#HANDLE MATRIX
		dataHandleA  = dataBlock.inputValue( self.attrInMatrix )
		inFloatMatrix = dataHandleA.asFloatMatrix()
		utils = om.MScriptUtil() #little hack
		inMatrix = om.MMatrix()
		utils.createMatrixFromList ( MMatrixToNum(inFloatMatrix), inMatrix)

		dataHandleB  = dataBlock.inputValue( self.attrInMatrixBase )
		inFloatMatrixBase = dataHandleB.asFloatMatrix() 
		inMatrixBase = om.MMatrix()
		utils.createMatrixFromList ( MMatrixToNum(inFloatMatrixBase), inMatrixBase) 

		#GET MESH POINTS
		self.outBasePoints = om.MPointArray()	
		inMeshFn.getPoints( self.outBasePoints , om.MSpace.kWorld )		

		self.targetPoints = om.MPointArray()
		inTargetMeshFn.getPoints( self.targetPoints , om.MSpace.kWorld )

		self.basePoints = om.MPointArray()
		inBaseMeshFn.getPoints( self.basePoints , om.MSpace.kWorld )

		self.outPoints = om.MPointArray()
		#COMPUTE ROTATION
		inMatrixBase = inMatrixBase.inverse()
		deltaMatrix =  inMatrix * inMatrixBase
		trsMatrix = om.MTransformationMatrix( deltaMatrix )
		rotQuad = trsMatrix.rotation()

		#DEFORM	
		p = self.outBasePoints	
		t = self.targetPoints	
		b = self.basePoints	
		e = envelope 								
		while not iter.isDone():
			i = iter.index()
			vDelta = ( t[i] - b[i] )
			vDelta = vDelta.rotateBy(rotQuad) 
			vDeltaEnv = om.MVector( e * ( vDelta.x + p[i].x ), e * (vDelta.y  + p[i].y) , e * (vDelta.z  + p[i].z) )
			pBaseEnv =  om.MPoint( (1 - e) * p[i].x , (1 - e) * p[i].y  , (1 - e) * p[i].z )
			#self.outPoints.append( pBaseEnv + vDeltaEnv )
			iter.setPosition(pBaseEnv + vDeltaEnv)
			iter.next()


		return True

def nodeCreator():
	return omMPx.asMPxPtr( rotateBlendShape() )

def nodeInitializer():
	mNumData = om.MFnNumericData()
	# IN ATTR
	mAttr = om.MFnMatrixAttribute() 
	rotateBlendShape.attrInMatrix = mAttr.create( 'inputMatrix' , 'inputMatrix' ,  mNumData.kFloat )
	mAttr.setChannelBox(True)
	mAttr.setKeyable(True)        
	mAttr.setReadable(True) 
	mAttr.setWritable(True)
	mAttr.setStorable(True)
	mAttr.setConnectable(True)         

	mAttr = om.MFnMatrixAttribute() 
	rotateBlendShape.attrInMatrixBase = mAttr.create( 'inputMatrixBase' , 'inputMatrixBase' ,  mNumData.kFloat )
	mAttr.setChannelBox(True)
	mAttr.setKeyable(True)        
	mAttr.setReadable(True) 
	mAttr.setWritable(True)
	mAttr.setStorable(True)
	mAttr.setConnectable(True)         

	gAttr = om.MFnGenericAttribute()
	rotateBlendShape.inTargetMesh = gAttr.create( "inTargetMesh", "inTarget")
	gAttr.addDataAccept( om.MFnData.kMesh )
	gAttr.setKeyable(True)

	rotateBlendShape.inBaseMesh = gAttr.create( "inBaseMesh", "inBase")
	gAttr.addDataAccept( om.MFnData.kMesh )
	gAttr.setKeyable(True)

	nAttr = om.MFnNumericAttribute()
	rotateBlendShape.weight = nAttr.create("weight", "wt", om.MFnNumericData.kFloat, 1)
	nAttr.setMin(0.0)
	nAttr.setKeyable(True)

	rotateBlendShape.addAttribute( rotateBlendShape.attrInMatrix     )
	rotateBlendShape.addAttribute( rotateBlendShape.attrInMatrixBase )
	rotateBlendShape.addAttribute( rotateBlendShape.inTargetMesh     )
	rotateBlendShape.addAttribute( rotateBlendShape.inBaseMesh       )
	rotateBlendShape.addAttribute( rotateBlendShape.weight           )

	outputGeom = omMPx.cvar.MPxGeometryFilter_outputGeom
	rotateBlendShape.attributeAffects(rotateBlendShape.attrInMatrix     , outputGeom )	
	rotateBlendShape.attributeAffects(rotateBlendShape.attrInMatrixBase , outputGeom )	
	rotateBlendShape.attributeAffects(rotateBlendShape.inTargetMesh     , outputGeom )
	rotateBlendShape.attributeAffects(rotateBlendShape.inBaseMesh       , outputGeom )
	rotateBlendShape.attributeAffects(rotateBlendShape.weight           , outputGeom )


def initializePlugin(mobject):
	mplugin = omMPx.MFnPlugin(mobject)
	try:
		mplugin.registerNode( kPluginNodeTypeName, rotateBlendShapeId, nodeCreator, nodeInitializer, omMPx.MPxNode.kDeformerNode )
	except:
		sys.stderr.write( "Failed to register node: %s\n" % kPluginNodeTypeName )

def uninitializePlugin(mobject):
	mplugin = omMPx.MFnPlugin(mobject)
	try:
		mplugin.deregisterNode( rotateBlendShapeId )
	except:
		sys.stderr.write( "Failed to unregister node: %s\n" % kPluginNodeTypeName )
        
        

        
        
def MMatrixToNum( matrix ):
    return [  matrix(0,0) , matrix(0,1) , matrix(0,2) , matrix(0,3)  ,  matrix(1,0) , matrix(1,1) , matrix(1,2) , matrix(1,3)  ,  matrix(2,0) , matrix(2,1) , matrix(2,2) , matrix(2,3) ,  matrix(3,0) , matrix(3,1) , matrix(3,2) , matrix(3,3)  ]     
            