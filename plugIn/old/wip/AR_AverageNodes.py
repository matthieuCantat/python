"""
-------------------------------------------------------------------------------
Creation Info:
Authors: Adam Mechtley http://adammechtley.com
    Ryan Trowbridge http://www.rtrowbridge.com/blog/
Date: 2011.06.09
Version: 1.0
Requires: Maya 8.5 or newer

Release Notes:
1.0 - 2011.06.09 - Initial release

Description:
This plug-in contains four different averaging nodes. It is intended to
demonstrate the basic parts of a custom dependency node, to demonstrate the use
of compound attributes, and to contrast plug arrays with array plugs.

Usage:
Add this file to your plug-in path and load it in Maya from the Plug-in Manager
(Window -> Settings/Preferences -> Plug-in Manager). You can then create the
nodes ar_averageDoubles, ar_averageArrayDoubles, ar_averageDoubleArray, and
ar_weightedAverageVectors.
-------------------------------------------------------------------------------
"""

import sys
# NOTE: sys.float_info was added in Python 2.6
# We hackishly append an attribute here for Maya 2009 and older
try: sys.float_info
except:
    class SysFloatInfoAttribute:
        epsilon = 2.2204460492503131e-16
    sys.float_info = SysFloatInfoAttribute()
import maya.OpenMaya as om
import maya.OpenMayaMPx as ommpx

# -----------------------------------------------------------------------------
# Node Definition
# -----------------------------------------------------------------------------
class AR_AverageDoublesNode(ommpx.MPxNode):
    """
    A node to compute the arithmetic mean of two doubles.
    """
    ## the name of the nodeType
    kPluginNodeTypeName = 'ar_averageDoubles'
    ## the unique MTypeId for the node
    kPluginNodeId = om.MTypeId(0x00033333)
    
    # input attributes
    ## first input number
    input1Attr = None
    kInput1AttrName = 'in1'
    kInput1AttrLongName = 'input1'
    ## second input number
    input2Attr = None
    kInput2AttrName = 'in2'
    kInput2AttrLongName = 'input2'
    
    # output attributes
    ## the arithmetic mean of in1 and in2
    output = None
    kOutputAttrName = 'out'
    kOutputAttrLongName = 'output'
    
    def __init__(self):
        ommpx.MPxNode.__init__(self)
    
    def compute(self, plug, dataBlock):
        """Compute the arithmetic mean of input 1 and input 2."""
        if (plug == AR_AverageDoublesNode.outputAttr):
            # get the incoming data
            dataHandle = om.MDataHandle(dataBlock.inputValue(AR_AverageDoublesNode.input1Attr))
            input1 = dataHandle.asDouble()
            dataHandle = om.MDataHandle(dataBlock.inputValue(AR_AverageDoublesNode.input2Attr))
            input2 = dataHandle.asDouble()
            # compute output
            output = (input1+input2)*0.5
            # set the outgoing plug
            dataHandle = om.MDataHandle(dataBlock.outputValue(AR_AverageDoublesNode.outputAttr))
            dataHandle.setDouble(output)
            dataBlock.setClean(plug)
        else: return om.kUnknownParameter
    
    @classmethod
    def nodeCreator(cls):
        return ommpx.asMPxPtr(cls())
    
    @classmethod
    def nodeInitializer(cls):
        # input attributes
        # first input number
        nAttr = om.MFnNumericAttribute()
        cls.input1Attr = nAttr.create(cls.kInput1AttrLongName, cls.kInput1AttrName, om.MFnNumericData.kDouble)
        nAttr.setKeyable(True)
        # second input number
        cls.input2Attr = nAttr.create(cls.kInput2AttrLongName, cls.kInput2AttrName, om.MFnNumericData.kDouble)
        nAttr.setKeyable(True)
        
        # ouput attributes
        # output number
        cls.outputAttr = nAttr.create(cls.kOutputAttrLongName, cls.kOutputAttrName, om.MFnNumericData.kDouble)
        nAttr.setWritable(False)
        nAttr.setStorable(False)
        
        # add the attributes
        cls.addAttribute(cls.input1Attr)
        cls.addAttribute(cls.input2Attr)
        cls.addAttribute(cls.outputAttr)
        
        # establish effects on output
        cls.attributeAffects(cls.input1Attr, cls.outputAttr)
        cls.attributeAffects(cls.input2Attr, cls.outputAttr)

# -----------------------------------------------------------------------------
# Node Definition
# -----------------------------------------------------------------------------
class AR_AverageArrayDoublesNode(ommpx.MPxNode):
    """
    A node to compute the arithmetic mean of an array of double plugs.
    """
    ## the name of the nodeType
    kPluginNodeTypeName = 'ar_averageArrayDoubles'
    ## the unique MTypeId for the node
    kPluginNodeId = om.MTypeId(0x00033334)
    
    # input attributes
    ## input array
    inputAttr = None
    kInputAttrName = 'in'
    kInputAttrLongName = 'input'
    
    # output attributes
    ## the arithmetic mean of all the numbers in input array
    output = None
    kOutputAttrName = 'out'
    kOutputAttrLongName = 'output'
    
    def __init__(self):
        ommpx.MPxNode.__init__(self)
    
    def compute(self, plug, dataBlock):
        """Compute the arithmetic mean of all the items in input array."""
        if (plug == AR_AverageArrayDoublesNode.outputAttr):
            # get the incoming data
            arrayDataHandle = om.MArrayDataHandle(dataBlock.inputValue(AR_AverageArrayDoublesNode.inputAttr))
            # compute output
            output = 0.0
            try: output = (arrayDataHandle.inputValue()).asDouble()
            except: pass
            for i in range(arrayDataHandle.elementCount()-1):
                arrayDataHandle.next()
                output += (arrayDataHandle.inputValue()).asDouble()
            try: output /= arrayDataHandle.elementCount()
            except: pass
            """
            # an alternative approach using an MPlug; less efficient because MPlug is slower
            arrayPlug = om.MPlug(self.thisMObject(), AR_AverageArrayDoublesNode.inputAttr)
            output = 0.0
            for i in range(arrayPlug.numElements()):
                elementPlug = om.MPlug(arrayPlug[i]).asDouble() # index operator works with physical indices
                output += elementPlug.asDouble()
            try: output /= arrayPlug.numElements()
            except: pass
            """
            # set the outgoing plug
            dataHandle = om.MDataHandle(dataBlock.outputValue(AR_AverageArrayDoublesNode.outputAttr))
            dataHandle.setDouble(output)
            dataBlock.setClean(plug)
        else: return om.kUnknownParameter
    
    @classmethod
    def nodeCreator(cls):
        return ommpx.asMPxPtr(cls())
    
    @classmethod
    def nodeInitializer(cls):
        # input attributes
        # input array
        nAttr = om.MFnNumericAttribute()
        cls.inputAttr = nAttr.create(cls.kInputAttrLongName, cls.kInputAttrName, om.MFnNumericData.kDouble)
        nAttr.setKeyable(True)
        nAttr.setArray(True)
        nAttr.setReadable(False)
        nAttr.setIndexMatters(False)
        nAttr.setDisconnectBehavior(om.MFnNumericAttribute.kDelete)
        
        # ouput attributes
        # output number
        cls.outputAttr = nAttr.create(cls.kOutputAttrLongName, cls.kOutputAttrName, om.MFnNumericData.kDouble)
        nAttr.setWritable(False)
        nAttr.setStorable(False)
        
        # add the attributes
        cls.addAttribute(cls.inputAttr)
        cls.addAttribute(cls.outputAttr)
        
        # establish effects on output
        cls.attributeAffects(cls.inputAttr, cls.outputAttr)

# -----------------------------------------------------------------------------
# Node Definition
# -----------------------------------------------------------------------------
class AR_AverageDoubleArrayNode(ommpx.MPxNode):
    """
    A node to compute the arithmetic mean of a double array plug.
    """
    ## the name of the nodeType
    kPluginNodeTypeName = 'ar_averageDoubleArray'
    ## the unique MTypeId for the node
    kPluginNodeId = om.MTypeId(0x00033335)
    
    # input attributes
    ## input array
    inputAttr = None
    kInputAttrName = 'in'
    kInputAttrLongName = 'input'
    
    # output attributes
    ## the arithmetic mean of all the numbers in input array
    output = None
    kOutputAttrName = 'out'
    kOutputAttrLongName = 'output'
    
    def __init__(self):
        ommpx.MPxNode.__init__(self)
    
    def compute(self, plug, dataBlock):
        """Compute the arithmetic mean of all the items in input array."""
        if (plug == AR_AverageDoubleArrayNode.outputAttr):
            # get the incoming data
            dataHandle = om.MDataHandle(dataBlock.inputValue(AR_AverageDoubleArrayNode.inputAttr))
            doubleArrayFn = om.MFnDoubleArrayData(dataHandle.data())
            doubleArray = om.MDoubleArray(doubleArrayFn.array())
            # compute output
            output = 0.0
            for i in range(doubleArray.length()): output += doubleArray[i]
            try: output /= doubleArray.length()
            except: pass
            # set the outgoing plug
            dataHandle = om.MDataHandle(dataBlock.outputValue(AR_AverageDoubleArrayNode.outputAttr))
            dataHandle.setDouble(output)
            dataBlock.setClean(plug)
        else: return om.kUnknownParameter
    
    @classmethod
    def nodeCreator(cls):
        return ommpx.asMPxPtr(cls())
    
    @classmethod
    def nodeInitializer(cls):
        # input attributes
        # input array
        tAttr = om.MFnTypedAttribute()
        cls.inputAttr = tAttr.create(cls.kInputAttrLongName, cls.kInputAttrName, om.MFnData.kDoubleArray)
        tAttr.setKeyable(True)
        
        # ouput attributes
        # output number
        nAttr = om.MFnNumericAttribute()
        cls.outputAttr = nAttr.create(cls.kOutputAttrLongName, cls.kOutputAttrName, om.MFnNumericData.kDouble)
        nAttr.setWritable(False)
        nAttr.setStorable(False)
        
        # add the attributes
        cls.addAttribute(cls.inputAttr)
        cls.addAttribute(cls.outputAttr)
        
        # establish effects on output
        cls.attributeAffects(cls.inputAttr, cls.outputAttr)

# -----------------------------------------------------------------------------
# Node Definition
# -----------------------------------------------------------------------------
class AR_WeightedAverageVectorsNode(ommpx.MPxNode):
    """
    A node to compute the mean of two vectors.
    """
    ## the name of the nodeType
    kPluginNodeTypeName = 'ar_weightedAverageVectors'
    ## the unique MTypeId for the node
    kPluginNodeId = om.MTypeId(0x00033336)
    
    # input attributes
    kInputVecAttrSuffix = 'V'
    kInputVecAttrLongSuffix = 'Vector'
    kInputWgtAttrSuffix = 'W'
    kInputWgtAttrLongSuffix = 'Weight'
    ## first input vector
    input1Attr = None
    input1VecAttr = None
    input1WgtAttr = None
    kInput1AttrName = 'in1'
    kInput1AttrLongName = 'input1'
    ## second input vector
    input2Attr = None
    input2VecAttr = None
    input2WgtAttr = None
    kInput2AttrName = 'in2'
    kInput2AttrLongName = 'input2'
    
    # output attributes
    ## the mean of in1 and in2
    outputAttr = None
    kOutputAttrName = 'out'
    kOutputAttrLongName = 'output'
    
    def __init__(self):
        ommpx.MPxNode.__init__(self)
    
    def compute(self, plug, dataBlock):
        """Compute the mean of input 1 and input 2."""
        if (plug == AR_WeightedAverageVectorsNode.outputAttr or
            (plug.isChild() and plug.parent()==AR_WeightedAverageVectorsNode.outputAttr)):
            # get the incoming data
            dataHandle = om.MDataHandle(dataBlock.inputValue(AR_WeightedAverageVectorsNode.input1VecAttr))
            input1Vector = dataHandle.asVector()
            dataHandle = om.MDataHandle(dataBlock.inputValue(AR_WeightedAverageVectorsNode.input1WgtAttr))
            input1Weight = dataHandle.asDouble()
            dataHandle = om.MDataHandle(dataBlock.inputValue(AR_WeightedAverageVectorsNode.input2VecAttr))
            input2Vector = dataHandle.asVector()
            dataHandle = om.MDataHandle(dataBlock.inputValue(AR_WeightedAverageVectorsNode.input2WgtAttr))
            input2Weight = dataHandle.asDouble()
            # compute output
            totalWeight = input1Weight+input2Weight
            if not abs(totalWeight) <= abs(totalWeight)*sys.float_info.epsilon:
                output = (input1Vector*input1Weight + input2Vector*input2Weight) / totalWeight
            else: output = (input1Vector+input2Vector)*0.5
            # set the outgoing plug
            dataHandle = om.MDataHandle(dataBlock.outputValue(AR_WeightedAverageVectorsNode.outputAttr))
            dataHandle.set3Double(output.x, output.y, output.z)
            dataBlock.setClean(plug)
        else: return om.kUnknownParameter
    
    @classmethod
    def nodeCreator(cls):
        return ommpx.asMPxPtr(cls())
    
    @classmethod
    def nodeInitializer(cls):
        # input attributes
        # first input vector
        nAttr = om.MFnNumericAttribute()
        cls.input1VecAttr = nAttr.create(cls.kInput1AttrLongName+cls.kInputVecAttrLongSuffix,
            cls.kInput1AttrName+cls.kInputVecAttrSuffix, om.MFnNumericData.k3Double)
        nAttr.setKeyable(True)
        # first input weight
        cls.input1WgtAttr = nAttr.create(cls.kInput1AttrLongName+cls.kInputWgtAttrLongSuffix,
            cls.kInput1AttrName+cls.kInputWgtAttrSuffix, om.MFnNumericData.kDouble, 0.5)
        nAttr.setKeyable(True)
        # first input compound
        cAttr = om.MFnCompoundAttribute()
        cls.input1Attr = cAttr.create(cls.kInput1AttrLongName, cls.kInput1AttrName)
        cAttr.addChild(cls.input1VecAttr)
        cAttr.addChild(cls.input1WgtAttr)
        # second input vector
        cls.input2VecAttr = nAttr.create(cls.kInput2AttrLongName+cls.kInputVecAttrLongSuffix,
            cls.kInput2AttrName+cls.kInputVecAttrSuffix, om.MFnNumericData.k3Double)
        nAttr.setKeyable(True)
        # second input weight
        cls.input2WgtAttr = nAttr.create(cls.kInput2AttrLongName+cls.kInputWgtAttrLongSuffix,
            cls.kInput2AttrName+cls.kInputWgtAttrSuffix, om.MFnNumericData.kDouble, 0.5)
        nAttr.setKeyable(True)
        # second input compound
        cls.input2Attr = cAttr.create(cls.kInput2AttrLongName, cls.kInput2AttrName)
        cAttr.addChild(cls.input2VecAttr)
        cAttr.addChild(cls.input2WgtAttr)
        
        # output attributes
        # output vector
        cls.outputAttr = nAttr.create(cls.kOutputAttrLongName, cls.kOutputAttrName, om.MFnNumericData.k3Double)
        #nAttr.setWritable(False)
        nAttr.setStorable(False)
        
        # add the attributes
        cls.addAttribute(cls.input1Attr)
        cls.addAttribute(cls.input2Attr)
        cls.addAttribute(cls.outputAttr)
        
        # establish effects on output
        cls.attributeAffects(cls.input1Attr, cls.outputAttr)
        cls.attributeAffects(cls.input2Attr, cls.outputAttr)

# -----------------------------------------------------------------------------
# Initialize
# -----------------------------------------------------------------------------
def initializePlugin(obj):
    plugin = ommpx.MFnPlugin(obj, 'Adam Mechtley & Ryan Trowbridge', '1.0', 'Any')
    try:
        plugin.registerNode(AR_AverageDoublesNode.kPluginNodeTypeName, AR_AverageDoublesNode.kPluginNodeId, AR_AverageDoublesNode.nodeCreator, AR_AverageDoublesNode.nodeInitializer)
    except:
        raise Exception('Failed to register node: %s'%AR_AverageDoublesNode.kPluginNodeTypeName)
    try:
        plugin.registerNode(AR_AverageArrayDoublesNode.kPluginNodeTypeName, AR_AverageArrayDoublesNode.kPluginNodeId, AR_AverageArrayDoublesNode.nodeCreator, AR_AverageArrayDoublesNode.nodeInitializer)
    except:
        raise Exception('Failed to register node: %s'%AR_AverageArrayDoublesNode.kPluginNodeTypeName)
    try:
        plugin.registerNode(AR_AverageDoubleArrayNode.kPluginNodeTypeName, AR_AverageDoubleArrayNode.kPluginNodeId, AR_AverageDoubleArrayNode.nodeCreator, AR_AverageDoubleArrayNode.nodeInitializer)
    except:
        raise Exception('Failed to register node: %s'%AR_AverageDoubleArrayNode.kPluginNodeTypeName)
    try:
        plugin.registerNode(AR_WeightedAverageVectorsNode.kPluginNodeTypeName, AR_WeightedAverageVectorsNode.kPluginNodeId, AR_WeightedAverageVectorsNode.nodeCreator, AR_WeightedAverageVectorsNode.nodeInitializer)
    except:
        raise Exception('Failed to register node: %s'%AR_WeightedAverageVectorsNode.kPluginNodeTypeName)

# -----------------------------------------------------------------------------
# Uninitialize
# -----------------------------------------------------------------------------
def uninitializePlugin(obj):
    plugin = ommpx.MFnPlugin(obj)
    try:
        plugin.deregisterNode(AR_AverageDoublesNode.kPluginNodeId)
    except:
        raise Exception('Failed to unregister node: %s'%AR_AverageDoublesNode.kPluginNodeTypeName)
    try:
        plugin.deregisterNode(AR_AverageArrayDoublesNode.kPluginNodeId)
    except:
        raise Exception('Failed to unregister node: %s'%AR_AverageArrayDoublesNode.kPluginNodeTypeName)
    try:
        plugin.deregisterNode(AR_AverageDoubleArrayNode.kPluginNodeId)
    except:
        raise Exception('Failed to unregister node: %s'%AR_AverageDoubleArrayNode.kPluginNodeTypeName)
    try:
        plugin.deregisterNode(AR_WeightedAverageVectorsNode.kPluginNodeId)
    except:
        raise Exception('Failed to unregister node: %s'%AR_WeightedAverageVectorsNode.kPluginNodeTypeName)

