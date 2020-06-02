########################################################################################
'''

delete "equalNode1";
flushUndo;

unloadPluginWithCheck( "/u/rigstuff/PYTHON DEV/MAYA NODES/equalNode.py" );
loadPlugin( "/u/rigstuff/PYTHON DEV/MAYA NODES/equalNode.py" );

createNode  "equalNode";

connectAttr -f locator1.translateY equalNode1.inputValues[0];
connectAttr -f locator2.translateY equalNode1.inputValues[1];
connectAttr -f locator3.translateY equalNode1.inputValues[2];

connectAttr -f equalNode1.outputValue locator4.translateY;

'''


########################################################################################

import maya.OpenMaya as om
import maya.OpenMayaMPx as omMPx


nodeName = "equalNode"
equalNodeId = om.MTypeId(0x00150A51A)

########################################################################################
########################################################################################

class equalNode(omMPx.MPxNode):

########################################################################################
########################################################################################

	def __init__(self):

		omMPx.MPxNode.__init__(self)

########################################################################################

	def compute(self, plug, dataBlock):

		hInputArray = dataBlock.inputArrayValue( self.inputsValsAttr )
		offsetValue = dataBlock.inputValue( self.offsetAttr ).asDouble()
		
		resultValue = None
		
		for i in xrange (hInputArray.elementCount()):
			
			hInputArray.jumpToElement(i)
			
			val = hInputArray.inputValue().asDouble();

			if (resultValue == None) or (val > resultValue):
				
				resultValue = val
				
		hOutputValue = dataBlock.outputValue(self.outputValAttr)
		hOutputValue.setDouble((resultValue + offsetValue))
		
		
		dataBlock.setClean(plug)
########################################################################################
########################################################################################

def nodeCreator():
	return omMPx.asMPxPtr( equalNode() )

########################################################################################
########################################################################################

def nodeInitializer():

	nAttr = om.MFnNumericAttribute()
	
	equalNode.inputsValsAttr = nAttr.create("inputValues", "inVals", om.MFnNumericData.kDouble)
	nAttr.setArray(True)
	nAttr.setKeyable(True)
	nAttr.setStorable(True)
	nAttr.setWritable(True)

	equalNode.offsetAttr = nAttr.create("offset", "offst", om.MFnNumericData.kDouble)
	nAttr.setKeyable(True)
	nAttr.setStorable(True)
	nAttr.setWritable(True)
	
	equalNode.outputValAttr = nAttr.create("outputValue", "outVal", om.MFnNumericData.kDouble)
	
	equalNode.addAttribute(equalNode.inputsValsAttr)
	equalNode.addAttribute(equalNode.offsetAttr)
	equalNode.addAttribute(equalNode.outputValAttr)
	
	equalNode.attributeAffects(equalNode.inputsValsAttr, equalNode.outputValAttr)
	equalNode.attributeAffects(equalNode.offsetAttr, equalNode.outputValAttr)
	
########################################################################################
########################################################################################
	
def initializePlugin(mobject):
	mplugin = omMPx.MFnPlugin(mobject)
	try:
		mplugin.registerNode(nodeName, equalNodeId, nodeCreator, nodeInitializer)
	except:
		sys.stderr.write("Failed to register node: $s\n" % nodeName)

########################################################################################
########################################################################################

def uninitializePlugin(mobject):
	mplugin = omMPx.MFnPlugin(mobject)
	try:
		mplugin.deregisterNode(equalNodeId)
	except:
		sys.stderr.write("Failed to deregister node: $s\n" % nodeName)

