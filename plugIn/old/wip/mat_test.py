"""
-------------------------------------------------------------------------------

-------------------------------------------------------------------------------
"""

import sys
import maya.OpenMaya as om
import maya.OpenMayaMPx as ommpx


# -----------------------------------------------------------------------------
# Node Definition
# -----------------------------------------------------------------------------
class mat_test(ommpx.MPxNode):

	
    kNodeName = 'mat_test'
    kPluginNodeId = om.MTypeId(0x52533)

    
    def __init__(self):
	self.sourcePos		= om.MObject()
	self.targetPos			= om.MObject()

	
        ommpx.MPxNode.__init__(self)
    
    def compute(self, plug, dataBlock):

	self.sourcePos	= dataBlock.inputValue(self.sourceAttr).asFloat3()
	self.targetPos	= dataBlock.inputValue(self.targetAttr).asFloat3()    	
    	
	#dataHandle = om.MDataHandle(dataBlock.inputValue(mat_test.sourceAttr))
	#self.sourcePos = dataHandle.asFloat3()
	#dataHandle = om.MDataHandle(dataBlock.inputValue(mat_test.targetAttr))
	#self.targetPos = dataHandle.asFloat3()

	startPnt	= om.MPoint(self.sourcePos[0], self.sourcePos[1], self.sourcePos[2])
	targetPnt	= om.MPoint(self.targetPos[0], self.targetPos[1], self.targetPos[2])	
	

	outPos = [ 0 , 0 , 0 ]
	outPos =[ ( startPnt.x - targetPnt.x ) / 2 , ( startPnt.y - targetPnt.x ) / 2 ,  ( startPnt.z - targetPnt.x ) / 2 ] 

	
	
	dataHandle = om.MDataHandle(dataBlock.outputValue(mat_test.outputAttr))
	dataHandle.asFloat3(outPos)
	dataBlock.setClean(plug)

    
    @classmethod
    def nodeCreator(cls):
        return ommpx.asMPxPtr(cls())
    
    @classmethod
    def nodeInitializer(cls):
    	
 	

	   	
    	# input
        nAttr = om.MFnNumericAttribute()
        mat_test.sourceAttr = nAttr.createPoint(  'sourceCoords'  , 'sCoords'  )
        nAttr.setKeyable(True)

        
        mat_test.targetAttr = nAttr.createPoint( 'targetCoords' , 'cCoords' )
        nAttr.setKeyable(True)
        nAttr.setReadable(True)
        nAttr.setChannelBox(True)
        nAttr.setHidden(False)

        # output
        
        mat_test.outputAttr = nAttr.createPoint( 'outCoords' , 'oCoords' )
        nAttr.setWritable(True)
        nAttr.setReadable(True)
        nAttr.setChannelBox(True)
        nAttr.setHidden(False)       
        

        mat_test.addAttribute(mat_test.sourceAttr)
        mat_test.addAttribute(mat_test.targetAttr)
        mat_test.addAttribute(mat_test.outputAttr)
   
        mat_test.attributeAffects(mat_test.sourceAttr, mat_test.outputAttr)
        mat_test.attributeAffects(mat_test.targetAttr, mat_test.outputAttr)


        
        
# -----------------------------------------------------------------------------
# Initialize
# -----------------------------------------------------------------------------
def initializePlugin(obj):
    plugin = ommpx.MFnPlugin( obj )
    try:
        plugin.registerNode(mat_test.kNodeName , mat_test.kPluginNodeId , mat_test.nodeCreator , mat_test.nodeInitializer)
    except:
        raise Exception('Failed to register node: %s'%mat_test.kNodeName)


# -----------------------------------------------------------------------------
# Uninitialize
# -----------------------------------------------------------------------------
def uninitializePlugin(obj):
    plugin = ommpx.MFnPlugin(obj)
    try:
        plugin.deregisterNode(mat_test.kPluginNodeId)
    except:
        raise Exception('Failed to unregister node: %s'%mat_test.kNodeName)


