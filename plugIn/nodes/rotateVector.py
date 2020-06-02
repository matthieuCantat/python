'''
#FOR TEST
import maya.cmds as mc
path = 'D:\mcantat_BDD\projects\code\maya\python\plugIn\rotateVector.py'
mc.file( new = True , f = True )
mc.loadPlugin( path , qt = True )   
'''

import sys
import math
import maya.OpenMaya as om
import maya.api.OpenMaya as ompy
import maya.OpenMayaMPx as ommpx
import maya.cmds as mc


class rotateVector(ommpx.MPxNode):

    kPluginNodeTypeName = 'rotateVector'
    kPluginNodeId = om.MTypeId(0x00033465)

    # IN ATTR
    attrInMatrix = None
    attrInMatrixName = 'inputMatrix'
    attrInMatrixBase = None
    attrInMatrixBaseName = 'inputMatrixBase'    
    attrInVector = None
    attrInVectorName = 'inputVector'
    # OUT ATTR
    attrOutVector = None
    attrOutVectorName = 'outputVector'
   
    def __init__(self):
        ommpx.MPxNode.__init__(self)
        self.inputMatrices  = []


    def compute( self, plug , dataBlock ): 
        #CHECK IF IT'S PLUG       
        outsAttrs = [ self.attrOutVector ]                    
        if not ( plug in outsAttrs ): return om.kUnknownParameter                        
        #GET DATA   
        dataHandleA  = dataBlock.inputValue( self.attrInMatrix )
        inFloatMatrix = dataHandleA.asFloatMatrix()
        utils = om.MScriptUtil() #little hack
        inMatrix = om.MMatrix()
        utils.createMatrixFromList ( MMatrixToNum(inFloatMatrix), inMatrix)

        dataHandleB  = dataBlock.inputValue( self.attrInMatrixBase )
        inFloatMatrixBase = dataHandleB.asFloatMatrix() 
        inMatrixBase = om.MMatrix()
        utils.createMatrixFromList ( MMatrixToNum(inFloatMatrixBase), inMatrixBase)  

        dataHandle  = dataBlock.inputValue( self.attrInVector )
        inVector = dataHandle.asFloat3()  

        outDataHandle = dataBlock.outputValue( self.attrOutVector )   
        outVector = dataHandle.asFloat3()                    
        #COMPUTE 
        inMatrixBase = inMatrixBase.inverse()
        deltaMatrix =  inMatrix * inMatrixBase
        trsMatrix = om.MTransformationMatrix( deltaMatrix )
        rotQuad = trsMatrix.rotation()

        inMVector = om.MVector( inVector[0] , inVector[1] , inVector[2] )
        outMVector = inMVector.rotateBy(rotQuad)

        outVector = [ outMVector.x , outMVector.y , outMVector.z ] 

        #OUT  
        outDataHandle.set3Float( outVector[0] , outVector[1] , outVector[2] )      
        dataBlock.setClean( self.attrOutVector ) 
        dataBlock.setClean( plug ) 
        
        
    @classmethod
    def nodeCreator(cls):
        return ommpx.asMPxPtr(cls())

    @classmethod
    def nodeInitializer(cls):
        print('-----nodeInitializer-----')
        mNumData = om.MFnNumericData()
        # IN ATTR
        mAttr = om.MFnMatrixAttribute() 
        cls.attrInMatrix = mAttr.create( cls.attrInMatrixName , cls.attrInMatrixName ,  mNumData.kFloat )
        mAttr.setChannelBox(True)
        mAttr.setKeyable(True)        
        mAttr.setReadable(True) 
        mAttr.setWritable(True)
        mAttr.setStorable(True)
        mAttr.setConnectable(True)         


        mAttr = om.MFnMatrixAttribute() 
        cls.attrInMatrixBase = mAttr.create( cls.attrInMatrixBaseName , cls.attrInMatrixBaseName ,  mNumData.kFloat )
        mAttr.setChannelBox(True)
        mAttr.setKeyable(True)        
        mAttr.setReadable(True) 
        mAttr.setWritable(True)
        mAttr.setStorable(True)
        mAttr.setConnectable(True)         


        mAttr = om.MFnNumericAttribute() 
        cls.attrInVector = mAttr.createPoint(cls.attrInVectorName, cls.attrInVectorName )
        mAttr.setChannelBox(True)
        mAttr.setKeyable(True)        
        mAttr.setReadable(True) 
        mAttr.setWritable(True)
        mAttr.setStorable(True)
        mAttr.setConnectable(True)               
        
        # OUT ATTR
        mAttr = om.MFnNumericAttribute()          
        cls.attrOutVector = mAttr.createPoint(cls.attrOutVectorName, cls.attrOutVectorName  )    
        mAttr.setReadable(True) 
        mAttr.setStorable(True)
        mAttr.setConnectable(True)             
        
        # ADD ATTR
        cls.addAttribute(cls.attrInMatrix )  
        cls.addAttribute(cls.attrInMatrixBase )
        cls.addAttribute(cls.attrInVector )          
        cls.addAttribute(cls.attrOutVector ) 
        
        #INFLUENCE
        cls.attributeAffects( cls.attrInMatrix     , cls.attrOutVector )         
        cls.attributeAffects( cls.attrInMatrixBase , cls.attrOutVector )           
        cls.attributeAffects( cls.attrInVector     , cls.attrOutVector )

             
       
        
def initializePlugin(obj):
    plugin = ommpx.MFnPlugin( obj , 'matthieuCantat', '1.0', 'Any')
    try:
        plugin.registerNode( rotateVector.kPluginNodeTypeName, rotateVector.kPluginNodeId, rotateVector.nodeCreator, rotateVector.nodeInitializer)
    except:
        raise Exception('Failed to register node: {0}'.format(rotateVector.kPluginNodeTypeName) )
   

def uninitializePlugin(obj):
    plugin = ommpx.MFnPlugin(obj)
    try:
        plugin.deregisterNode( rotateVector.kPluginNodeId )
    except:
        raise Exception('Failed to unregister node: {0}'.format(rotateVector.kPluginNodeTypeName) )

        
        
        
def MMatrixToNum( matrix ):
    return [  matrix(0,0) , matrix(0,1) , matrix(0,2) , matrix(0,3)  ,  matrix(1,0) , matrix(1,1) , matrix(1,2) , matrix(1,3)  ,  matrix(2,0) , matrix(2,1) , matrix(2,2) , matrix(2,3) ,  matrix(3,0) , matrix(3,1) , matrix(3,2) , matrix(3,3)  ]     
            