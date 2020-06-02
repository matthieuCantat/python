"""
	This node is a polygonal motion blur
	It uses the quadratic interpolation method
	You must connect the maya scene time1.outTime in the node's current time attribut.

	the principle is based on the interpolation of 3 positions in time (current/position at previous compute/positions at compute -2):

	strength : affects the "tail" length
	weight		   : affects the percent of the deformation
	
	For each interpolation method : px
	you must connect time1.outTime in blurDeformer.currentTime to make this node work.

		
		These attributs affect only while the node is in "hermite interpolation" mode
		
		Tension: 1 is high, 0 normal, -1 is low
		Bias: positive is towards first segment, 0 is even, negative is towards the other

"""

########################################################################################
########################################################################################

import math, sys, copy
import maya.OpenMaya as om
import maya.OpenMayaAnim as omAnim
import maya.OpenMayaMPx as omMPx
from maya.mel import eval as meval
import time

########################################################################################
########################################################################################

kPluginNodeTypeName = "blurDeformer"
blurDeformerId = om.MTypeId(0x0010A52B)

########################################################################################
########################################################################################

# Node definition
class blurDeformer(omMPx.MPxDeformerNode):

	# Node definition
	thisNode	= om.MObject()

	# nodes's attributs
	strength	  = om.MObject()
	interpType	  = 0
	hBias		  = om.MObject()
	hTension	  = om.MObject()
	currentTime	  = om.MObject()

	# points variables
	targetPoints   = om.MPointArray()			# MPointArray of shapeorig's vertices position
	lastPoints1	   = om.MPointArray()			# MPointArray of vertices position at compute -1
	lastPoints2	   = om.MPointArray()			# MPointArray of vertices position at compute -2
	lastPoints3	   = om.MPointArray()			# MPointArray of vertices position at compute -3

	targetPos	   = om.MPoint()				# MPoint of shapeorig's per vertex position
	pt1			   = om.MPoint()				# MPoint of per vertex position at compute -1
	pt2			   = om.MPoint()				# MPoint of per vertex position at compute -2
	pt3			   = om.MPoint()				# MPoint of per vertex position at compute -3
	normals		   = om.MFloatVectorArray()		# MFloatVectorArray of vertice's normal
	
	posTmp		   = [0.0, 0.0, 0.0]			# tmp vertex position variable

	pntWeight	   = om.MObject()				# variable for per vertex paint weight
	
	# Vector variables
	dotProdVect	   = om.MVector()
	vectFactor	   = om.MVector()
	interpBetween  = 0.0

	firstTime	   = 1						   # compute's init variable

	lastTime	   = 0						   # frame at previous compute

	# empty variables creation for first run
	
	UcurrentTime   = 0
	envelopeHandle = None
	hInputGeom	   = None

########################################################################################
########################################################################################

	# first compute init proc
	def initializeSelfVariables(self, dataBlock, envelope):

		# first and only MPlug attribut's declaration at first run (faster compute because variables are not re-created at each compute but only query)

		self.thisNode  = self.thisMObject()

		self.envelopeHandle = dataBlock.inputValue( envelope )			# Some of the internal deformer node's attributs do not provide MPlug fonction

		self.lastPoints1.copy( self.targetPoints )						# Variable init at first run with Target points coordinates
		self.lastPoints2.copy( self.targetPoints )						# Variable init at first run with Target points coordinates
		self.lastPoints3.copy( self.targetPoints )						# Variable init at first run with Target points coordinates

		print "First init"

########################################################################################
########################################################################################

	def __init__(self):
		omMPx.MPxDeformerNode.__init__(self)

########################################################################################
########################################################################################

	def deform( self, dataBlock, iter, matrix, index ):

		# inputs
		envelope = omMPx.cvar.MPxDeformerNode_envelope

		# get inMesh infos
		input  = omMPx.cvar.MPxDeformerNode_input
		hInput = dataBlock.inputArrayValue(input)
		hInput.jumpToArrayElement(index)

		inputGeom = omMPx.cvar.MPxDeformerNode_inputGeom
		groupId			   = omMPx.cvar.MPxDeformerNode_groupId

		hInputElement	   = hInput.inputValue()
		self.hInputGeom = hInputElement.child(inputGeom)

		inMesh		   = self.hInputGeom.asMesh()
		inMeshFn = om.MFnMesh(inMesh)

		# get target points coordinates and normals
		inMeshFn.getPoints(self.targetPoints,om.MSpace.kWorld)
		inMeshFn.getVertexNormals(True, self.normals, om.MSpace.kWorld)

		# test first time
		if self.firstTime ==1:

			self.initializeSelfVariables(dataBlock, envelope)
			self.firstTime = 0

		# get node's attributs
		envelopeValue			= self.envelopeHandle.asFloat()
		self.UcurrentTime		= dataBlock.inputValue(self.currentTime)
		self.strength			= dataBlock.inputValue(blurDeformer.strength).asFloat()
		self.interpType			= dataBlock.inputValue(blurDeformer.blurInterpolationType).asShort()
		self.meshRepartition	= dataBlock.inputValue(blurDeformer.meshRepartition).asShort()
		self.hBias				= dataBlock.inputValue(blurDeformer.hermiteBias).asFloat()
		self.hTension			= dataBlock.inputValue(blurDeformer.hermiteTension).asFloat()
		self.posTmp				= [0.0, 0.0, 0.0]

		if envelopeValue!=0:

			# deform's variables

			startTime		  = omAnim.MAnimControl.animationStartTime().value() # get time range start frame
			frameTime		  = self.UcurrentTime.asInt()
			currentTime				= frameTime/250										  # Don't know why frameTime is 250 time the node's attribute

			if currentTime != startTime and currentTime != self.lastTime:

				while not iter.isDone():

					# get per vertex Positions in time, normal and paint weight
					self.targetPos	= self.targetPoints[iter.index()]
					self.pt1		= self.lastPoints1[iter.index()]
					self.pt2		= self.lastPoints2[iter.index()]
					self.pt3		= self.lastPoints3[iter.index()]
					normal			= self.normals[iter.index()]
					self.pntWeight	= self.weightValue( dataBlock, index, iter.index())

					# displacement/vectors
					displacement = self.pt1.distanceTo(self.targetPos)			  # displacement length

					# displacement direction vector
					displVect = om.MFloatVector(self.targetPos - self.pt1)
					displVect.normalize()
					normal.normalize()
					
					# dot product of vertex's normal and displacement vector
					self.dotProdVect = displVect * -normal
					
					# clamping dotProduct
					self.vectFactor = max(min((1-self.dotProdVect/((2/self.strength)/self.strength)), 1), -1)
					
					# mesh interpolation selection
					if self.meshRepartition == 0: 
						self.interpBetween = self.linStep(self.vectFactor, -1, 1)
					
					else: 
						self.interpBetween = self.smoothStep(self.vectFactor, -1, 1)

						
					# blur deformation selection
					interp = 0
					if self.interpType > 1:
						interp = 1
						[self.comp1(i, self.interpType) for i in xrange(3)]

					else:
						interp = 0
						self.comp2( self.interpType)

						
					# finalPoint calculation
					tmpPos	 = om.MPoint(self.posTmp[0], self.posTmp[1], self.posTmp[2]) + ((om.MVector(self.targetPos - self.pt1) * self.interpBetween ) * (interp))
					finalPos = om.MPoint( (tmpPos.x * self.pntWeight) + (self.targetPos.x * (1 - self.pntWeight)), (tmpPos.y * self.pntWeight) + (self.targetPos.y * (1 - self.pntWeight)), (tmpPos.z * self.pntWeight) + (self.targetPos.z * (1 - self.pntWeight)) )

					self.lastPoints1[iter.index()].x = finalPos.x
					self.lastPoints1[iter.index()].y = finalPos.y
					self.lastPoints1[iter.index()].z = finalPos.z

					iter.next()

				iter.setAllPositions(self.lastPoints1)
				self.lastPoints3.copy( self.lastPoints2)
				self.lastPoints2.copy( self.lastPoints1)
				self.lastPoints1.copy( self.targetPoints)
				self.lastTime = copy.copy(currentTime)

			else:

				iter.setAllPositions(self.targetPoints)				# if CurrentTime = startTime or CurrentTime = lastTime we just move the points
				self.lastPoints3.copy( self.targetPoints)
				self.lastPoints2.copy( self.targetPoints)
				self.lastPoints1.copy( self.targetPoints)
				self.lastTime = copy.copy(currentTime)

########################################################################################
########################################################################################
	# blur interpolations procs
	
	def comp2(self, interp):
		
		if interp == 0:
			self.posTmp = self.linearInterpolation(self.pt1, self.targetPos, self.interpBetween)

		elif interp == 1:
			self.posTmp = self.quadraticInterpolation(self.pt2, self.pt1, self.targetPos, self.interpBetween)

	def comp1(self, i, interp):

		posVxt = [0.0, 0.0, 0.0]

		if interp == 2:
			self.posTmp[i] = self.cubicInterpolation(self.pt3[i], self.pt2[i], self.pt1[i], self.targetPos[i], self.interpBetween)

		elif interp == 3:
			self.posTmp[i] = self.CatmullRomInterpolation(self.pt3[i], self.pt2[i], self.pt1[i], self.targetPos[i], self.interpBetween)

		elif interp == 4:
			self.posTmp[i] = self.HermiteInterpolation(self.pt3[i], self.pt2[i], self.pt1[i], self.targetPos[i], self.interpBetween, self.hTension, self.hBias)
		

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

#####################################################################################
########################Interpolation algorithms#####################################
#####################################################################################

	# Linear interpomation
	def linearInterpolation(self, p0, p1, U):
		interpPnt = p0+((p1-p0)*U)

		return interpPnt

	# quadratic interpolation
	def quadraticInterpolation(self, p0, p1, p2, U):

		edgeA	  = om.MPoint(p0 + ((p1-p0) * U))
		edgeB	  = om.MPoint(p1 + ((p2-p1) * U))
		interpPnt = om.MPoint(edgeA + (edgeB - edgeA) * U)

		return interpPnt

	# Catmull-Rom interpolation 
	def CatmullRomInterpolation(self, p0, p1, p2, p3, U):

		U2 = U*U
		a0 = -0.5*p0+1.5*p1-1.5*p2+0.5*p3
		a1 = p0-2.5*p1+2*p2-0.5*p3
		a2 = -0.5*p0+0.5*p2
		a3 = p1

		interpPnt = a0*U*U2+a1*U2+a2*U+a3

		return interpPnt
	
	# cubic interpolation	
	def cubicInterpolation(self, p0, p1, p2, p3, U):
		
		U2 = U*U
		a0 = (p3-p2-p0+p1)
		a1 = (p0-p1-a0)
		a2 = (p2-p0)
		a3 = p1

		interpPnt = a0*U*U2+a1*U2+a2*U+a3

		return interpPnt

	# Hermite interpolation
	def HermiteInterpolation(self, p0, p1, p2, p3, U, tension, bias):

		U2 = U * U
		U3 = U2 * U
		m0 = (p1-p0)*(1+bias)*(1-tension)/2
		m0 += (p2-p1)*(1-bias)*(1-tension)/2
		m1 = (p2-p1)*(1+bias)*(1-tension)/2
		m1 += (p3-p2)*(1-bias)*(1-tension)/2
		a0 = 2*U3 - 3*U2 + 1
		a1 = U3 - 2*U2 + U
		a2 = U3 - U2
		a3 = -2*U3 + 3*U2

		interpPnt = (a0*p1+a1*m0+a2*m1+a3*p2)

		return interpPnt
		
########################################################################################
########################################################################################

def nodeCreator():
	return omMPx.asMPxPtr( blurDeformer() )

########################################################################################
########################################################################################

# initializer
def nodeInitializer():

	#attributs creation
	uAttr = om.MFnUnitAttribute()
	eAttr = om.MFnEnumAttribute()
	nAttr = om.MFnNumericAttribute()

	blurDeformer.currentTime = uAttr.create("currentTime", "time", om.MFnUnitAttribute.kTime, 1.0)
	uAttr.setKeyable(True)

	blurDeformer.strength = nAttr.create("strength", "stren", om.MFnNumericData.kFloat, 1)
	nAttr.setMin(0.00000001)
	nAttr.setKeyable(True)

	blurDeformer.blurInterpolationType = eAttr.create("blurInterpolationType", "blurInterpType", 0)
	eAttr.addField('linear', 0)
	eAttr.addField('quadratic', 1)
	eAttr.addField('Cubic', 2)
	eAttr.addField('Catmull-Rom', 3)
	eAttr.addField('Hermite', 4)
	eAttr.setKeyable(True)

	blurDeformer.meshRepartition = eAttr.create("meshRepartition", "meshRep", 0)
	eAttr.addField('linear', 0)
	eAttr.addField('smooth', 1)
	eAttr.setKeyable(True)
	
	
	blurDeformer.hermiteTension = nAttr.create("hermiteTension", "hTension", om.MFnNumericData.kFloat, 0)
	nAttr.setMin(-1.0)
	nAttr.setMax(1.0)
	nAttr.setKeyable(True)

	blurDeformer.hermiteBias = nAttr.create("hermiteBias", "hBias", om.MFnNumericData.kFloat, 0)
	nAttr.setKeyable(True)

	blurDeformer.addAttribute(blurDeformer.currentTime)
	blurDeformer.addAttribute(blurDeformer.blurInterpolationType)
	blurDeformer.addAttribute(blurDeformer.meshRepartition)
	blurDeformer.addAttribute(blurDeformer.strength)
	blurDeformer.addAttribute(blurDeformer.hermiteTension)
	blurDeformer.addAttribute(blurDeformer.hermiteBias)

	outputGeom = omMPx.cvar.MPxDeformerNode_outputGeom

	blurDeformer.attributeAffects(blurDeformer.currentTime, outputGeom )
	
	# global command to make node paintable
	om.MGlobal.executeCommand( "makePaintable -attrType multiFloat -sm deformer blurDeformer weights;" )
	
########################################################################################
########################################################################################

# initialize the script plug-in
def initializePlugin(mobject):
	mplugin = omMPx.MFnPlugin(mobject)
	try:
		mplugin.registerNode( kPluginNodeTypeName, blurDeformerId, nodeCreator, nodeInitializer, omMPx.MPxNode.kDeformerNode )
	except:
		sys.stderr.write( "Failed to register node: %s\n" % kPluginNodeTypeName )

########################################################################################
########################################################################################

# uninitialize the script plug-in
def uninitializePlugin(mobject):
	mplugin = omMPx.MFnPlugin(mobject)
	try:
		mplugin.deregisterNode( blurDeformerId )
	except:
		sys.stderr.write( "Failed to unregister node: %s\n" % kPluginNodeTypeName )


mel = '''
global proc polyBlurDeformer()
{
	string $sel[] = `ls -sl -tr`;
	for($obj in $sel)
	{
		select $obj;
		string $deformer[] = `deformer -type "blurDeformer"`;
		connectAttr "time1.outTime" ($deformer[0] + ".currentTime");
	}
}'''

meval( mel )
