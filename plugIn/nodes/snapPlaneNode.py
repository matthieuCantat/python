



import sys
import math
import time
import maya.OpenMaya as om
import maya.api.OpenMaya as ompy
import maya.OpenMayaMPx as ommpx
import maya.cmds as mc


path = 'D:\mcantat_BDD\projects\code\maya'        

import sys
sys.path.append( path )

import python.classe.trsClass as trsClass

class snapPlane(ommpx.MPxNode):

    kPluginNodeTypeName = 'snapPlaneNode'
    kPluginNodeId = om.MTypeId(0x00033447)
   
    # IN ATTR : MAIN
    input0Attr = None
    kInput0AttrName = 'activate'
    kInput0AttrLongName = 'activate'

    input1Attr = None
    kInput1AttrName = 'worldMatrixA'
    kInput1AttrLongName = 'worldMatrixA' 

    input2Attr = None
    kInput2AttrName = 'worldMatrixB'
    kInput2AttrLongName = 'worldMatrixB' 
    
    input3Attr = None
    kInput3AttrName = 'worldMatrixC'
    kInput3AttrLongName = 'worldMatrixC' 
    
    input4Attr = None
    kInput4AttrName = 'worldMatrixD'
    kInput4AttrLongName = 'worldMatrixD' 

    input5Attr = None
    kInput5AttrName = 'worldMatrixFather'
    kInput5AttrLongName = 'worldMatrixFather'     
    



    outputT = None
    kOutputTAttrName = 'outTran'
    kOutputTAttrLongName = 'outTranslate' 
    
    outputR = None
    kOutputRAttrName = 'outRot'
    kOutputRAttrLongName = 'outRotate'     

    
    def __init__(self):
        
        ommpx.MPxNode.__init__(self)
        self.nbrEval       = 0
        self.lastTime      = 0
        
        self.lastSpeed     = [0,0,0,0,0,0,0,0,0]
        
        self.lastSpeedT     = [0,0,0]          
        self.lastSpeedR     = [0,0,0]  
        self.lastSpeedS     = [0,0,0]  

        self.slaveValue    = [0,0,0,0,0,0,1,1,1]  
        
        self.slaveTValue     = [0,0,0]          
        self.slaveRValue     = [0,0,0]  
        self.slaveSValue     = [1,1,1]   

    def compute( self, plug , dataBlock ):
    
     
    	outsAttr = [ self.outputTAttr , self.outputRAttr ]                    
        if not ( plug in outsAttr ):
            return om.kUnknownParameter                
        #_____________________________________________________________________________________ IN   
         

        dataHandle     = dataBlock.inputValue( self.input0Attr )
        activate       = dataHandle.asFloat()                 

        dataHandle        = dataBlock.inputValue( self.input1Attr )
        worldMFloatMatrix = dataHandle.asFloatMatrix()
        worldMatrixA      = MMatrixToNum(worldMFloatMatrix) 
  
        dataHandle        = dataBlock.inputValue( self.input2Attr )
        worldMFloatMatrix = dataHandle.asFloatMatrix()
        worldMatrixB      = MMatrixToNum(worldMFloatMatrix)         
        
        dataHandle        = dataBlock.inputValue( self.input3Attr )
        worldMFloatMatrix = dataHandle.asFloatMatrix()
        worldMatrixC      = MMatrixToNum(worldMFloatMatrix) 

        dataHandle        = dataBlock.inputValue( self.input4Attr )
        worldMFloatMatrix = dataHandle.asFloatMatrix()
        worldMatrixD      = MMatrixToNum(worldMFloatMatrix) 

        dataHandle       = dataBlock.inputValue( self.input5Attr )
        inMFloatMatrix   = dataHandle.asFloatMatrix()
        fatherMatrix     = MMatrixToNum(inMFloatMatrix)

                  
        
        #_____________________________________________________________________________________COMPUTE
        
        '''
        par convention on va dire que les points ABCD sont repartis de cette maniere:
        AB
        DC  ( vue de haut )
        avec AB devant CD derriere et qui se lit dans le sens des aiguille d'une montre
        
        '''
        
        
        trsObj = trsClass.trsClass() 
        
        
        #_______________ TRS       
        initTrsWorldA  = trsObj.createFromFloatMatrix( worldMatrixA ) 
        initTrsWorldB  = trsObj.createFromFloatMatrix( worldMatrixB )         
        initTrsWorldC  = trsObj.createFromFloatMatrix( worldMatrixC ) 
        initTrsWorldD  = trsObj.createFromFloatMatrix( worldMatrixD ) 
        fatherTrs      = trsObj.createFromFloatMatrix( fatherMatrix ) 
        
        #_______________ POSITION
        
        outPosition = [0,0,0]
        
        outPosition[0] = ( initTrsWorldA[0] + initTrsWorldB[0] + initTrsWorldC[0] + initTrsWorldD[0] ) / 4
        outPosition[1] = ( initTrsWorldA[1] + initTrsWorldB[1] + initTrsWorldC[1] + initTrsWorldD[1] ) / 4        
        outPosition[2] = ( initTrsWorldA[2] + initTrsWorldB[2] + initTrsWorldC[2] + initTrsWorldD[2] ) / 4        
        
        #_______________ ROTATION

        outRotation = [0,0,0] 
        
        # vector corner A
        vUpCornerA   = [0,1,0]
        vDirCornerA  = [ initTrsWorldA[0] - initTrsWorldD[0] , initTrsWorldA[1] - initTrsWorldD[1] ,  initTrsWorldA[2] - initTrsWorldD[2]  ]
        vSideCornerA = [ initTrsWorldB[0] - initTrsWorldA[0] , initTrsWorldB[1] - initTrsWorldA[1] ,  initTrsWorldB[2] - initTrsWorldA[2]  ]    
        
        # vector corner C
        vUpCornerC   = [0,1,0]
        vDirCornerC  = [ initTrsWorldB[0] - initTrsWorldC[0] , initTrsWorldB[1] - initTrsWorldC[1] ,  initTrsWorldB[2] - initTrsWorldC[2]  ]
        vSideCornerC = [ initTrsWorldC[0] - initTrsWorldD[0] , initTrsWorldC[1] - initTrsWorldD[1] ,  initTrsWorldC[2] - initTrsWorldD[2]  ]
        
        # moyenne
        vUpCorner    = [ ( vUpCornerA[0]   + vUpCornerC[0]   ) / 2 , ( vUpCornerA[1]   + vUpCornerC[1]   ) / 2 , ( vUpCornerA[2]   + vUpCornerC[2]   ) / 2   ] 
        vDirCorner   = [ ( vDirCornerA[0]  + vDirCornerC[0]  ) / 2 , ( vDirCornerA[1]  + vDirCornerC[1]  ) / 2 , ( vDirCornerA[2]  + vDirCornerC[2]  ) / 2   ] 
        vSideCorner  = [ ( vSideCornerA[0] + vSideCornerC[0] ) / 2 , ( vSideCornerA[1] + vSideCornerC[1] ) / 2 , ( vSideCornerA[2] + vSideCornerC[2] ) / 2   ] 
        
        # convert to rotation   
        trsObj.createFromTripleVectors( vDirCorner , vUpCorner , vSideCorner , accuracyOrder = [ 0 , 2 , 1 ] )
        outRotation = trsObj[3:6]
        
        #_____________________________________________________________________________________ OUT NODE                

        trsOut      = outPosition + outRotation + [1,1,1]       
        trsOutUnder = trsObj.parent( fatherTrs , inTrsValue = trsOut )


        dataHandle = dataBlock.outputValue( self.outputTAttr )      
        dataHandle.set3Float( trsOutUnder[0] , trsOutUnder[1] , trsOutUnder[2] )
        
        dataHandle = dataBlock.outputValue( self.outputRAttr )      
        dataHandle.set3Float( trsOutUnder[3] , trsOutUnder[4] , trsOutUnder[5] )
        
        dataBlock.setClean( plug ) 
        
        
    @classmethod
    def nodeCreator(cls):
        return ommpx.asMPxPtr(cls())


    @classmethod
    def nodeInitializer(cls):
        
        nAttr = om.MFnNumericAttribute()   
        
        cls.input0Attr = nAttr.create(cls.kInput0AttrLongName, cls.kInput0AttrName , om.MFnNumericData.kFloat  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)
        
        nAttr = om.MFnMatrixAttribute() 
        
        cls.input1Attr = nAttr.create(cls.kInput1AttrLongName, cls.kInput1AttrName , om.MFnNumericData.kFloat  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False) 
        
        nAttr = om.MFnMatrixAttribute() 
        
        cls.input2Attr = nAttr.create(cls.kInput2AttrLongName, cls.kInput2AttrName , om.MFnNumericData.kFloat  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)         

        nAttr = om.MFnMatrixAttribute() 
        
        cls.input3Attr = nAttr.create(cls.kInput3AttrLongName, cls.kInput3AttrName , om.MFnNumericData.kFloat  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)          

        nAttr = om.MFnMatrixAttribute() 
        
        cls.input4Attr = nAttr.create(cls.kInput4AttrLongName, cls.kInput4AttrName , om.MFnNumericData.kFloat  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False) 

        nAttr = om.MFnMatrixAttribute() 
        
        cls.input5Attr = nAttr.create(cls.kInput5AttrLongName, cls.kInput5AttrName , om.MFnNumericData.kFloat  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False) 

        
        nAttr = om.MFnNumericAttribute() 
        
        cls.outputTAttr = nAttr.create(cls.kOutputTAttrLongName, cls.kOutputTAttrName, om.MFnNumericData.k3Float )
        nAttr.setWritable(False)
        nAttr.setStorable(False)  

        nAttr = om.MFnNumericAttribute() 
        
        cls.outputRAttr = nAttr.create(cls.kOutputRAttrLongName, cls.kOutputRAttrName, om.MFnNumericData.k3Float )
        nAttr.setWritable(False)
        nAttr.setStorable(False)  
        
        
        
        cls.addAttribute(cls.input0Attr )
        cls.addAttribute(cls.input1Attr )
        cls.addAttribute(cls.input2Attr )        
        cls.addAttribute(cls.input3Attr )          
        cls.addAttribute(cls.input4Attr ) 
        cls.addAttribute(cls.input5Attr )     

        cls.addAttribute(cls.outputTAttr )          
        cls.addAttribute(cls.outputRAttr )  
        
        #INFLUENCE
        
        cls.attributeAffects( cls.input0Attr   , cls.outputRAttr )         
        cls.attributeAffects( cls.input1Attr   , cls.outputRAttr )                   
        cls.attributeAffects( cls.input2Attr   , cls.outputRAttr )           
        cls.attributeAffects( cls.input3Attr   , cls.outputRAttr )  
        cls.attributeAffects( cls.input4Attr   , cls.outputRAttr )
        cls.attributeAffects( cls.input5Attr   , cls.outputRAttr )

        cls.attributeAffects( cls.input0Attr   , cls.outputTAttr )         
        cls.attributeAffects( cls.input1Attr   , cls.outputTAttr )           
        cls.attributeAffects( cls.input2Attr   , cls.outputTAttr )
        cls.attributeAffects( cls.input3Attr   , cls.outputTAttr )       
        cls.attributeAffects( cls.input4Attr   , cls.outputTAttr )   
        cls.attributeAffects( cls.input5Attr   , cls.outputTAttr ) 
        
        
def initializePlugin(obj):
    plugin = ommpx.MFnPlugin( obj , 'matthieuCantat', '1.0', 'Any')
    try:
        plugin.registerNode( snapPlane.kPluginNodeTypeName, snapPlane.kPluginNodeId, snapPlane.nodeCreator, snapPlane.nodeInitializer)
    except:
        raise Exception('Failed to register node: {0}'.format(snapPlane.kPluginNodeTypeName) )
   

def uninitializePlugin(obj):
    plugin = ommpx.MFnPlugin(obj)
    try:
        plugin.deregisterNode( snapPlane.kPluginNodeId )
    except:
        raise Exception('Failed to unregister node: {0}'.format(snapPlane.kPluginNodeTypeName) )

        
        
        
        
########################################################################################################################################################################################################        
########################################################################################################################################################################################################  PROC UTILS      
########################################################################################################################################################################################################        
        
  
def MMatrixToNum( matrix ):
    return [  matrix(0,0) , matrix(0,1) , matrix(0,2) , matrix(0,3)  ,  matrix(1,0) , matrix(1,1) , matrix(1,2) , matrix(1,3)  ,  matrix(2,0) , matrix(2,1) , matrix(2,2) , matrix(2,3) ,  matrix(3,0) , matrix(3,1) , matrix(3,2) , matrix(3,3)  ]     
