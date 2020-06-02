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

nodeName = "deltaToMaskNode"
dynNodeId = om.MTypeId(0x58843)

########################################################################################
########################################################################################

class deltaToMaskNode(omMPx.MPxNode):

	
	# 'frameIteration' is there for further backward time scaling
	def __init__(self):

	    
	    omMPx.MPxNode.__init__(self)
	    
########################################################################################

	def compute(self, plug, dataBlock):

		dataBlock.setClean(plug)															# set plug clean after compute 

########################################################################################
########################################################################################

def nodeCreator():
	return omMPx.asMPxPtr(deltaToMaskNode())

########################################################################################
########################################################################################

def nodeInitializer():
	
	deltaToMaskNode.compressionShape = gAttr.create("compressionShape", "tenShape")
	gAttr.addDataAccept( om.MFnData.kMesh )
	
	deltaToMaskNode.tensionShape = gAttr.create("tensionShape", "tenShape")
	gAttr.addDataAccept( om.MFnData.kMesh )

	
	deltaToMaskNode.addAttribute(deltaToMaskNode.compressionShape)
		
	deltaToMaskNode.addAttribute(deltaToMaskNode.tensionShape)
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

