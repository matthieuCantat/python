########################################################################################
'''
C:/Users/Cra/AppData/Local/Temp/Cra.20140629.1830.ma
delete "remapVectorNode1";
flushUndo;

unloadPluginWithCheck( "/u/rigstuff/PYTHON DEV/MAYA NODES/remapNode.py" );
loadPlugin( "/u/rigstuff/PYTHON DEV/MAYA NODES/remapNode.py"  );

createNode "remapNode";


'''


########################################################################################
import math, copy
import maya.OpenMaya as om
import maya.OpenMayaMPx as omMPx


nodeName = "remapVectorNode"
remapVectorNodeId = om.MTypeId(0x00181A51A)

########################################################################################
########################################################################################

class remapVectorNode(omMPx.MPxNode):

########################################################################################
########################################################################################

	def __init__(self):
		
		self.lastDistance = 0.0

		omMPx.MPxNode.__init__(self)

########################################################################################

	def compute(self, plug, dataBlock):

		pntAPos		= dataBlock.inputValue(self.pntAPosAttr).asFloat3()
		pntBPos		= dataBlock.inputValue(self.pntBPosAttr).asFloat3()
		
		maxHeight	= dataBlock.inputValue(self.maxHeightAttr).asFloat()		
		delta		= dataBlock.inputValue(self.deltaAttr).asFloat()
		
		vector = om.MVector(pntBPos[0] - pntAPos[0], pntBPos[1] - pntAPos[1], pntBPos[2] - pntAPos[2])
		distance = vector.length()	
		
		result = self.smoothStep(distance, (maxHeight-delta), maxHeight)
		result2 = 1-result

		self.outputHandle	= dataBlock.outputValue(self.outValueAAttr)
		self.outputHandle.setFloat(result)
		
		self.outputHandle	= dataBlock.outputValue(self.outValueBAttr)
		self.outputHandle.setFloat(result2)	
		
		self.lastDistance = copy.copy(distance)
		
		dataBlock.setClean(plug)

################################################################################
########################################################################################
	
	#smooth step fonction	
	def smoothStep(self, U, a, b):
	
		if U < a:
			return 0.0
		if U > b:
			return 1.0
	
		U = (U - a)/(b - a)
		return U * U * (3.0 - 2.0 * U)	
	
################################################################################
########################################################################################

def nodeCreator():
	return omMPx.asMPxPtr( remapVectorNode() )

########################################################################################
########################################################################################

def nodeInitializer():

	nAttr = om.MFnNumericAttribute()

	remapVectorNode.pntAPosAttr = nAttr.createPoint("pntAPos", "pntA")
	nAttr.setKeyable(True)
	nAttr.setStorable(True)
	nAttr.setWritable(True)

	remapVectorNode.pntBPosAttr = nAttr.createPoint("pntBPos", "pntB")
	nAttr.setKeyable(True)
	nAttr.setStorable(True)
	nAttr.setWritable(True)

	remapVectorNode.maxHeightAttr = nAttr.create("maxHeight", "max", om.MFnNumericData.kFloat, .5)
	nAttr.setKeyable(True)
	nAttr.setStorable(True)
	nAttr.setWritable(True)

	remapVectorNode.deltaAttr = nAttr.create("delta", "delta", om.MFnNumericData.kFloat, 0.1)
	nAttr.setKeyable(True)
	nAttr.setStorable(True)
	nAttr.setWritable(True)

	remapVectorNode.outValueAAttr = nAttr.create("outValueA", "outA", om.MFnNumericData.kFloat)
	nAttr.setWritable(False)
	
	remapVectorNode.outValueBAttr = nAttr.create("outValueB", "outB", om.MFnNumericData.kFloat)
	nAttr.setWritable(False)
	
	remapVectorNode.addAttribute(remapVectorNode.pntAPosAttr)
	remapVectorNode.addAttribute(remapVectorNode.pntBPosAttr)
	remapVectorNode.addAttribute(remapVectorNode.maxHeightAttr)
	remapVectorNode.addAttribute(remapVectorNode.deltaAttr)
	remapVectorNode.addAttribute(remapVectorNode.outValueAAttr)
	remapVectorNode.addAttribute(remapVectorNode.outValueBAttr)

	remapVectorNode.attributeAffects(remapVectorNode.pntAPosAttr, remapVectorNode.outValueAAttr)
	remapVectorNode.attributeAffects(remapVectorNode.pntBPosAttr, remapVectorNode.outValueAAttr)
	remapVectorNode.attributeAffects(remapVectorNode.maxHeightAttr, remapVectorNode.outValueAAttr)
	remapVectorNode.attributeAffects(remapVectorNode.deltaAttr, remapVectorNode.outValueAAttr)

	remapVectorNode.attributeAffects(remapVectorNode.pntAPosAttr, remapVectorNode.outValueBAttr)
	remapVectorNode.attributeAffects(remapVectorNode.pntBPosAttr, remapVectorNode.outValueBAttr)
	remapVectorNode.attributeAffects(remapVectorNode.maxHeightAttr, remapVectorNode.outValueBAttr)
	remapVectorNode.attributeAffects(remapVectorNode.deltaAttr, remapVectorNode.outValueBAttr)

########################################################################################
########################################################################################

def initializePlugin(mobject):
	mplugin = omMPx.MFnPlugin(mobject)
	try:
		mplugin.registerNode(nodeName, remapVectorNodeId, nodeCreator, nodeInitializer)
	except:
		sys.stderr.write("Failed to register node: $s\n" % nodeName)

########################################################################################
########################################################################################

def uninitializePlugin(mobject):
	mplugin = omMPx.MFnPlugin(mobject)
	try:
		mplugin.deregisterNode(remapVectorNodeId)
	except:
		sys.stderr.write("Failed to deregister node: $s\n" % nodeName)
