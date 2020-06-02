'''
#FOR TEST
import maya.cmds as mc
path = 'D:\mcantat_BDD\projects\code\maya\python\plugIn/templateNode.py'
mc.file( new = True , f = True )
mc.loadPlugin( path , qt = True )   
node = mc.createNode( "templateNode")
'''

import sys
import maya.OpenMaya as om
import maya.api.OpenMaya as ompy
import maya.OpenMayaMPx as ommpx
import maya.cmds as mc


class templateNode(ommpx.MPxNode):

    kPluginNodeTypeName = 'templateNode'
    kPluginNodeId = om.MTypeId(0x00033467)

    @classmethod
    def nodeCreator(cls):
        return ommpx.asMPxPtr(cls())

    @classmethod
    def nodeInitializer(cls):
        cls.curveModes = [ 'open' , 'close' , 'periodic' ] 
        nData = om.MFnNumericData()
        cData = om.MFnNurbsCurveData() 
        mData = om.MFnMeshData() 

        nAttr = om.MFnNumericAttribute()  
        eAttr = om.MFnEnumAttribute()
        mAttr = om.MFnMatrixAttribute()
        gAttr = om.MFnGenericAttribute()
        tAttr = om.MFnTypedAttribute()                 

        # INPUT ATTRIBUT                   default: Readable Writable Storable Connectable                                 
        cls.aInPoint = nAttr.createPoint( 'point' , 'point' )
        nAttr.setKeyable(True)        
        nAttr.setChannelBox(True)        
     
        # OUTPUT ATTRIBUT                                     
        cls.aOutPoint = nAttr.createPoint( 'outPoint' , 'outPoint' )
        nAttr.setChannelBox(True) 
                        
        # ADD ATTR               
        cls.addAttribute(cls.aInPoint     )     
        cls.addAttribute(cls.aOutPoint    )
        #INFLUENCE         
        cls.attributeAffects( cls.aInPoint    , cls.aOutPoint    )

    def __init__(self):
        ommpx.MPxNode.__init__(self)
      

    def compute( self, plug , dataBlock ): 

        #CHECK IF AN OUT ATTR IS REQUESTED  
        outsAttrs = [self.aOutPoint  ]                    
        if not ( plug in outsAttrs ): 
            return om.kUnknownParameter  

        #GET DATA   
        pointInHandle = dataBlock.inputValue( self.aInPoint )
        pointInValue  = pointInHandle.asFloat3()  

        #COMPUTE     
        print('point    : {} {} {}'.format( pointInValue[0] , pointInValue[1] , pointInValue[2] ) )     

        #OUT            
        pointOutHandle = dataBlock.outputValue( self.aOutPoint )      
        pointOutHandle.set3Float( pointInValue[0] , pointInValue[1] , pointInValue[2] )

        #SET THE OUT ATTR CLEAN
        dataBlock.setClean( self.aOutPoint ) 
        
             
       
        
def initializePlugin(obj):
    plugin = ommpx.MFnPlugin( obj , 'matthieuCantat', '1.0', 'Any')
    try:
        plugin.registerNode( templateNode.kPluginNodeTypeName, templateNode.kPluginNodeId, templateNode.nodeCreator, templateNode.nodeInitializer)
    except:
        raise Exception('Failed to register node: {0}'.format(templateNode.kPluginNodeTypeName) )
   

def uninitializePlugin(obj):
    plugin = ommpx.MFnPlugin(obj)
    try:
        plugin.deregisterNode( templateNode.kPluginNodeId )
    except:
        raise Exception('Failed to unregister node: {0}'.format(templateNode.kPluginNodeTypeName) )

        
        
        
        