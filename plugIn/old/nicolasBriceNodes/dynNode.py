"""
    This node is a dyn output Node.
    It's based on the "damped mass-spring" differential equation computed with the Heun's ODE solving method
    
    The inputs can be used independantly with any float data.
    The corresponding output is an approximation of de "DMP" equation at the given time.

    TO DO:
    Add matrix mult + attr in order to choose the matrix in wich you want the node to evaluate
    It actualy works in worldSpace.
    
    delete "r_chenille_dyn";
flushUndo;

unloadPluginWithCheck( "D:/C++/Python sources/dynNode.py" );
loadPlugin( "D:/C++/Python sources/dynNode.py"  );

createNode "dynNode" -n "r_chenille_dyn";

connectAttr "r_chenille_dyn.outPosition" "r_chenilleDyn_skn.translate";
connectAttr "r_chenilleDyn.translate" "r_chenille_dyn.targetPosition";
connectAttr "time1.outTime" "r_chenille_dyn.currentTime";
"""

########################################################################################
########################################################################################

import math, sys, copy
import maya.OpenMaya as om
import maya.OpenMayaAnim as omAnim
import maya.OpenMayaMPx as omMPx
import maya.cmds as cmds
import time

nodeName = "dynNode"
dynNodeId = om.MTypeId(0x52843)

########################################################################################
########################################################################################

class dynNode(omMPx.MPxNode):

	
	# 'frameIteration' is there for further backward time scaling
	def __init__(self):
	    
	    # empty node's variables
	    self.currentTime		= om.MObject()		   # (node's attributs)
	    self.stiffness		= om.MObject()
	    self.weight			= om.MObject()
	    self.dampingRatio	= om.MObject()
	    
	    self.targetPos		= [0.0, 0.0, 0.0]
	    self.outPosition		= [0.0, 0.0, 0.0]
	    self.outVelocity		= [0.0, 0.0, 0.0]
	    self.lastPos			= [0.0, 0.0, 0.0]
	    self.lastVel			= [0.0, 0.0, 0.0]
	    self.lastTime		= 0.0
	    self.lastUpdate		= 0.0	 
	    self.h				= 1
	    self.firstTime		= 1
	    self.frameIteration	= 1	
	    
	    omMPx.MPxNode.__init__(self)
	    
########################################################################################

	def compute(self, plug, dataBlock):

		# node's attributs declaration         
		self.targetPos		= dataBlock.inputValue(self.targetPosAttr).asFloat3()
		self.dampingRatio	= dataBlock.inputValue(self.dampingRatioAttr).asFloat()
		self.stiffness		= dataBlock.inputValue(self.stiffnessAttr).asFloat()
		self.weight			= dataBlock.inputValue(self.weightAttr).asFloat()
		currentTime			= dataBlock.inputValue(self.currentTimeAttr).asInt()

		# time variables
		self.startTime		= omAnim.MAnimControl.animationStartTime().value()			  # get time range start frame

		# output variable
		self.outputHandle	= dataBlock.outputValue(self.outPositionAttr)

		if currentTime != self.startTime and currentTime != self.lastTime:

			deltaTime = abs(currentTime - self.lastTime)

			if deltaTime > 1.0 or deltaTime < -1.0:										   #it should always be 1 or -1, else compute will be very hazardous
				deltaTime = 1.0															   # that's why we clamp it :)
																						   
				self.h = deltaTime/self.frameIteration									   # it should be 1 as well (this attribut's for futur integration of backward time scaling)
																						   # (backward time scaling doesn't work with Heun's ODE solver)
																						   
			[self.comp(i) for i in xrange(3)]											   # the actual method needs per axis compute (0, 1, 2) = (x, y, z)

			self.outputHandle.set3Float(self.lastPos[0], self.lastPos[1], self.lastPos[2]) # set the output position 

		else:
			self.lastVel			= [0.0, 0.0, 0.0]
			self.outputHandle.set3Float(self.targetPos[0], self.targetPos[1], self.targetPos[2])


		self.lastTime = copy.copy(currentTime)
		dataBlock.setClean(plug)															# set plug clean after compute 

########################################################################################
########################################################################################

	# Compute proc for list comprehension

	def comp(self, i):
		
		deltaPos = self.lastPos[i]-self.targetPos[i]

		# ODE solver call
		r = self.heun(deltaPos, self.lastVel[i], self.h)

		self.lastPos[i] = self.weight*r[0] + self.targetPos[i]
		self.lastVel[i] = r[1]	

########################################################################################
########################################################################################

	# acceleration proc
	def accel(self, x, v):

		accel = -self.stiffness*x - (2.0 * self.dampingRatio * math.sqrt(self.stiffness))*v
		return accel

########################################################################################
########################################################################################

	# ODE solver
	def heun(self, x, v, h):

		x1 = x								# Heun's ODE method seems to be a very good one, 2nd order, fast and reliable
		v1 = v								# Runge-Kutta 2nd order is good also, 4th order ODE solvers are much more precise but much more slower
		a1 = self.accel(x1, v1)

		x2 = x + v1*h
		v2 = v + a1*h
		a2 = self.accel(x2, v2)

		xf = x + (h/2.0)*(v1 + v2)
		vf = v + (h/2.0)*(a1 + a2)
		return xf, vf

########################################################################################
########################################################################################

def nodeCreator():
	return omMPx.asMPxPtr(dynNode())

########################################################################################
########################################################################################

def nodeInitializer():
	uAttr = om.MFnUnitAttribute()
	dynNode.currentTimeAttr = uAttr.create("currentTime", "time", om.MFnUnitAttribute.kTime, 1.0)
	uAttr.setKeyable(True)
   
	nAttr = om.MFnNumericAttribute()
	dynNode.targetPosAttr = nAttr.createPoint("targetPosition", "targPos")
	nAttr.setKeyable(True)

	nAttr = om.MFnNumericAttribute()
	dynNode.weightAttr = nAttr.create("weight", "wt", om.MFnNumericData.kFloat, 1)
	nAttr.setMin(0.0)
	nAttr.setKeyable(True)
   
	nAttr = om.MFnNumericAttribute()
	dynNode.stiffnessAttr = nAttr.create("stiffness", "stiff", om.MFnNumericData.kFloat, 0.2)
	nAttr.setMin(0.0)
	nAttr.setKeyable(True)
   
	nAttr = om.MFnNumericAttribute()
	dynNode.dampingRatioAttr = nAttr.create("dampingRatio", "dr", om.MFnNumericData.kFloat, 0.2)
	nAttr.setMin(0.0)
	nAttr.setMax(1.0)
	nAttr.setKeyable(True)
   
	nAttr = om.MFnNumericAttribute()
	dynNode.outPositionAttr = nAttr.createPoint("outPosition", "outPos")
	nAttr.setWritable(False)
   
	nAttr = om.MFnNumericAttribute()
	dynNode.outVelocityAttr = nAttr.createPoint("outVelocity", "outVel")
	nAttr.setWritable(False)
   
   
	dynNode.addAttribute(dynNode.currentTimeAttr)
	dynNode.addAttribute(dynNode.targetPosAttr)
	dynNode.addAttribute(dynNode.stiffnessAttr)
	dynNode.addAttribute(dynNode.weightAttr)
	dynNode.addAttribute(dynNode.dampingRatioAttr)
	dynNode.addAttribute(dynNode.outPositionAttr)
	dynNode.addAttribute(dynNode.outVelocityAttr)
   
	dynNode.attributeAffects(dynNode.currentTimeAttr, dynNode.outPositionAttr)
	dynNode.attributeAffects(dynNode.targetPosAttr, dynNode.outPositionAttr)

########################################################################################
########################################################################################
	
def initializePlugin(mobject):
	mplugin = omMPx.MFnPlugin(mobject)
	try:
		mplugin.registerNode(nodeName, dynNodeId, nodeCreator, nodeInitializer)
	except:
		sys.stderr.write("Failed to register node: $s\n" % nodeName)

########################################################################################
########################################################################################

def uninitializePlugin(mobject):
	mplugin = omMPx.MFnPlugin(mobject)
	try:
		mplugin.deregisterNode(dynNodeId)
	except:
		sys.stderr.write("Failed to deregister node: $s\n" % nodeName)

