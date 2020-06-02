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
    kPluginNodeId = om.MTypeId(0x00033333)

    
    def __init__(self):
        ommpx.MPxNode.__init__(self)
    
    def compute(self, plug, dataBlock):

	dataHandle = om.MDataHandle(dataBlock.inputValue(mat_test.sourceAttr))
	sourcePos = dataHandle.asFloat3()
	dataHandle = om.MDataHandle(dataBlock.inputValue(mat_test.targetAttr))
	targetPos = dataHandle.asFloat3()
	#dataHandle = om.MDataHandle(dataBlock.inputValue(mat_test.inMeshAttr))
	#inMesh = dataHandle.asMesh()	


	outPos =[ ( targetPos[0] - sourcePos[0] ) / 2 , ( targetPos[1] - sourcePos[1] ) / 2 ,  ( targetPos[1] - sourcePos[1] ) / 2 ] 

	
	
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
        cls.sourceAttr = nAttr.createPoint(  'sourceCoords'  , 'sCoords'  )
        nAttr.setKeyable(False)

        cls.targetAttr = nAttr.createPoint( 'targetCoords' , 'cCoords' )
        nAttr.setKeyable(False)
        
        mAttr = om.MFnGenericAttribute()
        cls.inMeshAttr = mAttr.create( 'inMesh' , 'inM' )
        mAttr.addDataAccept(om.MFnData.KMesh)

        # output
        
        cls.outputAttr = nAttr.createPoint( 'outCoords' , 'oCoords' )
        nAttr.setWritable(False)
       
        

        cls.addAttribute(cls.sourceAttr)
        cls.addAttribute(cls.targetAttr)
        #cls.addAttribute(cls.inMeshAttr)
        cls.addAttribute(cls.outputAttr)
        
        
        cls.attributeAffects(cls.sourceAttr, cls.outputAttr)
        cls.attributeAffects(cls.targetAttr, cls.outputAttr)
        #cls.attributeAffects(cls.inMeshAttr, cls.outputAttr)

        
        
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


