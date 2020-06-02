"""
    This node is a jiggle deformer wich uses the Heun's ODE solving method
    You can change the ODE solving method in the "def heun"
    You must connect the maya scene time1.outTime in the node's current time attribut.

    TO DO:
    Add matrix mult + attr in order to choose the matrix in wich you want the node to evaluate
    It actualy works in worldSpace.
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

kPluginNodeTypeName = "jiggleDeformer"
jiggleDeformerId = om.MTypeId(0x0010A52B)

########################################################################################
########################################################################################

# Node definition
class jiggleDeformer(omMPx.MPxDeformerNode):

	# Node definition
	thisNode	= om.MObject()

	# nodes's attributs
	stiffness		= om.MObject()
	weight			= om.MObject()
	dampingRatio	= om.MObject()
	frameIterations = om.MObject()
	currentTime = om.MObject()

	# points variables

	targetPoints = om.MPointArray()		 # MPointArray of shapeorig's vertices position
	lastPoints	 = om.MPointArray()		 # MPointArray of vertices position at previous compute 
	lastVel		 = om.MFloatPointArray() # MPointArray of vertices velocity at previous compute
	
	targetPos	 = om.MPoint()			 # MPoint of shapeorig's per vertex position
	lastPosition = om.MPoint()			 # MPoint of per vertex position at previous compute
	vel			 = om.MPoint()			 # MPoint of per vertex velocity at previous compute

	positionTmp	 = [0.0,0.0,0.0]		 # tmp variable for per vertex position
	velTmp		 = [0.0,0.0,0.0]		 # tmp variable for per vertex velocity
										 
	pntWeight	 = om.MObject()			 # variable for per vertex paint weight
										 
	lastTime	 = 0					 # frame at previous compute
	h			 = 1					 # delatTime
	firstTime	 = 1					 # compute's init variable

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

		# global command to make node paintable
		om.MGlobal.executeCommand( "makePaintable -attrType multiFloat -sm deformer jiggleDeformer weights;" )

		self.envelopeHandle = dataBlock.inputValue( envelope )	  # Some of the internal deformer node's attributs do not provide MPlug fonction

		self.lastPoints.copy( self.targetPoints )				  # Variable init at first run with Target points coordinates
		velfloatTmp		  = om.MFloatPoint (0.0,0.0,0.0)
		self.lastVel	  = om.MFloatPointArray(self.targetPoints.length(), velfloatTmp)
		self.dampingRatio = dataBlock.inputValue(jiggleDeformer.dampingRatio)
		self.stiffness	  = om.MPlug(self.thisNode, jiggleDeformer.stiffness)
		self.weight		  = om.MPlug(self.thisNode, jiggleDeformer.weight)

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
		groupId   = omMPx.cvar.MPxDeformerNode_groupId

		hInputElement   = hInput.inputValue()
		self.hInputGeom = hInputElement.child(inputGeom)

		inMesh   = self.hInputGeom.asMesh()
		inMeshFn = om.MFnMesh(inMesh)

		# get target points coordinates
		inMeshFn.getPoints(self.targetPoints,om.MSpace.kWorld)

		# test first time
		if self.firstTime ==1:
			
			self.initializeSelfVariables(dataBlock, envelope)
			self.firstTime = 0

		# get attributs that DON'T work in init def (??)
		envelopeValue = self.envelopeHandle.asFloat()
		self.UcurrentTime = dataBlock.inputValue(self.currentTime)

		if envelopeValue!=0:

			# deform's variables

			startTime	   = omAnim.MAnimControl.animationStartTime().value() # get time range start frame
			frameTime	   = self.UcurrentTime.asInt()
			currentTime	   = frameTime/250									  # Don't know why frameTime is 250 time the node's attribut
			frameIteration = 1												  # optionnal frame iteration

			if currentTime != startTime and currentTime != self.lastTime:				 

				deltaTime = abs(currentTime - self.lastTime)				 #it should always be 1 or -1, else compute will be very hazardous

				if	 deltaTime > 1.0 or deltaTime < -1.0:					 # that's why we clamp it :)
					 deltaTime = 1.0

				self.h = deltaTime/frameIteration							 # it should be 1 as well (this attribut's for futur integration of backward time scaling)
																			 # (backward time scaling doesn't work with Heun's ODE solver)
				while not iter.isDone():

					# get per vertex Position
					self.targetPos	  = self.targetPoints[iter.index()]
					self.lastPosition = self.lastPoints[iter.index()]
					self.vel		  = self.lastVel[iter.index()]
					self.pntWeight	  = self.weightValue( dataBlock, index, iter.index())

					[self.comp(i) for i in xrange(3)]	# the actual method needs per axis compute (0, 1, 2) = (x, y, z) 

					# set each new vertex velocity (only usefull for next compute)	
					self.lastVel[iter.index()].x = self.velTmp[0]
					self.lastVel[iter.index()].y = self.velTmp[1]
					self.lastVel[iter.index()].z = self.velTmp[2]

					# set each new vertex position
					self.lastPoints[iter.index()].x = self.positionTmp[0]
					self.lastPoints[iter.index()].y = self.positionTmp[1]
					self.lastPoints[iter.index()].z = self.positionTmp[2]

					iter.next()

				iter.setAllPositions(self.lastPoints)

			else:

				iter.setAllPositions(self.targetPoints)		  # if CurrentTime = startTime we just move the points
				self.lastPoints .copy( self.targetPoints )	  # avoids shape from poping when moving it at start frame then playing

			self.lastTime = copy.copy(currentTime)			  # copying current frame as last compute's frame for next compute

########################################################################################
########################################################################################

    # Compute proc for list comprehension
	def comp(self, i):

		weight	 = self.weight.asFloat()
		deltaPos = self.lastPosition[i]-self.targetPos[i]

		# solver call
		reslut = self.heun(deltaPos, self.vel[i], self.h)	 # result[0] returns the computed position / result[1] returns the computed velocity

		self.positionTmp[i] = (self.pntWeight * weight) * reslut[0] + self.targetPos[i]
		self.velTmp[i]		= reslut[1]

########################################################################################
########################################################################################

	# acceleration proc
	def accel(self, x, v):

		dampingRatioValue = self.dampingRatio.asFloat()
		stiffnessValue	  = self.stiffness.asFloat()
        	accel             = -stiffnessValue*x - (2.0 * dampingRatioValue * math.sqrt(stiffnessValue))*v

		return accel

########################################################################################
########################################################################################

	# ODE solver
	def heun(self, x, v, h):

		x1 = x								# Heun's ODE solver method seems to be a very good one, 2nd order ( enhanced euler method), fast and reliable
		v1 = v								# Runge-Kutta 2nd order is good also, 4th order solvers are much more precise but much more slower
		a1 = self.accel(x1, v1)             # 1st order ODE solvers are not precise and stable enougth to be used

		x2 = x + v1*h
		v2 = v + a1*h
		a2 = self.accel(x2, v2)

		xf = x + (h/2.0)*(v1 + v2)
		vf = v + (h/2.0)*(a1 + a2)
		return xf, vf

########################################################################################
########################################################################################

def nodeCreator():
	return omMPx.asMPxPtr( jiggleDeformer() )

########################################################################################
########################################################################################

# initializer
def nodeInitializer():

	gAttr = om.MFnGenericAttribute()
	jiggleDeformer.inMesh = gAttr.create( "inMesh", "inMsh")
	gAttr.addDataAccept( om.MFnData.kMesh )

	uAttr = om.MFnUnitAttribute()
	jiggleDeformer.currentTime = uAttr.create("currentTime", "time", om.MFnUnitAttribute.kTime, 1.0)
	uAttr.setKeyable(True)

	nAttr = om.MFnNumericAttribute()
	jiggleDeformer.weight = nAttr.create("weight", "wt", om.MFnNumericData.kFloat, 1)
	nAttr.setMin(0.0)
	nAttr.setKeyable(True)

	nAttr = om.MFnNumericAttribute()
	jiggleDeformer.stiffness = nAttr.create("stiffness", "stiff", om.MFnNumericData.kFloat, 0.2)
	nAttr.setMin(0.0)
	nAttr.setKeyable(True)

	nAttr = om.MFnNumericAttribute()
	jiggleDeformer.dampingRatio = nAttr.create("dampingRatio", "dr", om.MFnNumericData.kFloat, 0.2)
	nAttr.setMin(0.0)
	nAttr.setMax(1.0)
	nAttr.setKeyable(True)

	nAttr = om.MFnNumericAttribute()
	jiggleDeformer.eulerChk = nAttr.create("euler", "eu", om.MFnNumericData.kInt, 0)
	nAttr.setMin(0)
	nAttr.setMax(1)
	nAttr.setKeyable(True)

	nAttr = om.MFnNumericAttribute()
	jiggleDeformer.frameIterations = nAttr.create("frameIterations", "frameIter", om.MFnNumericData.kFloat, 1)
	nAttr.setMin(1)
	nAttr.setMax(5)
	nAttr.setChannelBox(True)


	jiggleDeformer.addAttribute( jiggleDeformer.inMesh )
	jiggleDeformer.addAttribute(jiggleDeformer.currentTime)
	jiggleDeformer.addAttribute(jiggleDeformer.stiffness)
	jiggleDeformer.addAttribute(jiggleDeformer.weight)
	jiggleDeformer.addAttribute(jiggleDeformer.dampingRatio)
	jiggleDeformer.addAttribute(jiggleDeformer.eulerChk)
	jiggleDeformer.addAttribute(jiggleDeformer.frameIterations)

	outputGeom = omMPx.cvar.MPxDeformerNode_outputGeom

	jiggleDeformer.attributeAffects(jiggleDeformer.inMesh, outputGeom )
	jiggleDeformer.attributeAffects(jiggleDeformer.currentTime, outputGeom )

########################################################################################
########################################################################################

# initialize the script plug-in
def initializePlugin(mobject):
	mplugin = omMPx.MFnPlugin(mobject)
	try:
		mplugin.registerNode( kPluginNodeTypeName, jiggleDeformerId, nodeCreator, nodeInitializer, omMPx.MPxNode.kDeformerNode )
	except:
		sys.stderr.write( "Failed to register node: %s\n" % kPluginNodeTypeName )

########################################################################################
########################################################################################

# uninitialize the script plug-in
def uninitializePlugin(mobject):
	mplugin = omMPx.MFnPlugin(mobject)
	try:
		mplugin.deregisterNode( jiggleDeformerId )
	except:
		sys.stderr.write( "Failed to unregister node: %s\n" % kPluginNodeTypeName )
        
        
