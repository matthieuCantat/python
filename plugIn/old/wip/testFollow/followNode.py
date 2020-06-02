


import sys
import math
import time
import maya.OpenMaya as om
import maya.api.OpenMaya as ompy
import maya.OpenMayaMPx as ommpx
import maya.cmds as mc


toolBox_mainPath = 'C:/Users/Matthieu/Desktop/Travail/code/maya/script/python/'        

import sys
sys.path.append( toolBox_mainPath )

import toolBox
import toolBox.utils.utilsMayaApi as utilsMayaApi
import toolBox.utils.classes.trsClass as trsClass


class followNode(ommpx.MPxNode):

    kPluginNodeTypeName = 'followNode'
    kPluginNodeId = om.MTypeId(0x00033451)

    # _________________________________ IN MATRIX    
    inputMatrixAttr = None
    kInputMatrixAttrName = 'inMatrix'
    kInputMatrixAttrLongName = 'inMatrix'           
    
    # _________________________________ IN DYN ATTR 
    
    inputTimeAttr = None
    kInputTimeAttrName = 'time'
    kInputTimeAttrLongName = 'time'
       
    inputActivateAttr = None
    kInputActivateAttrName = 'activate'
    kInputActivateAttrLongName = 'activate'
    
    input1Attr = None
    kInput1AttrName = 'masse'
    kInput1AttrLongName = 'masse'       

    input2Attr = None
    kInput2AttrName = 'elasticity'
    kInput2AttrLongName = 'elasticity'       

    input3Attr = None
    kInput3AttrName = 'damping'
    kInput3AttrLongName = 'damping'  
 
    input4Attr = None
    kInput4AttrName = 'gravity'
    kInput4AttrLongName = 'gravity'  
    
                                              
    # _________________________________ SAVE NEXT EVAL

    inputNext1Attr = None
    kInputNext1AttrName = 'nbrEval'
    kInputNext1AttrLongName = 'nbrEval'      

    inputNext2Attr = None
    kInputNext2AttrName = 'lastTime'
    kInputNext2AttrLongName = 'lastTime'      

    inputNext3Attr = None
    kInputNext3AttrName = 'lastSpeed'
    kInputNext3AttrLongName = 'lastSpeed'       

    inputNext4Attr = None
    kInputNext4AttrName = 'slaveValue'
    kInputNext4AttrLongName = 'slaveValue'     
    
    # _________________________________ OUT TRANSLATE    
    outputT = None
    kOutputTAttrName = 'outTran'
    kOutputTAttrLongName = 'outTranslate'    
    
    outputTX = None
    kOutputTXAttrName = 'outTranX'
    kOutputTXAttrLongName = 'outTranslateX'
    
    outputTY = None
    kOutputTYAttrName = 'outTranY'
    kOutputTYAttrLongName = 'outTranslateY'
 
    outputTZ = None
    kOutputTZAttrName = 'outTranZ'
    kOutputTZAttrLongName = 'outTranslateZ'    

    # _________________________________ OUT ROTATE    
    outputR = None
    kOutputRAttrName = 'outRot'
    kOutputRAttrLongName = 'outRotate'    
    
    outputRX = None
    kOutputRXAttrName = 'outRotX'
    kOutputRXAttrLongName = 'outRotateX'
    
    outputRY = None
    kOutputRYAttrName = 'outRotY'
    kOutputRYAttrLongName = 'outRotateY'
 
    outputRZ = None
    kOutputRZAttrName = 'outRotZ'
    kOutputRZAttrLongName = 'outRotateZ' 

    # _________________________________ OUT SCALE     
    outputS = None
    kOutputSAttrName = 'outSca'
    kOutputSAttrLongName = 'outScale'    
    
    outputSX = None
    kOutputSXAttrName = 'outScaX'
    kOutputSXAttrLongName = 'outScaleX'
    
    outputSY = None
    kOutputSYAttrName = 'outScaY'
    kOutputSYAttrLongName = 'outScaleY'
 
    outputSZ = None
    kOutputSZAttrName = 'outScaZ'
    kOutputSZAttrLongName = 'outScaleZ' 
    

    def __init__(self):        
        ommpx.MPxNode.__init__(self)
        self.nbrEval       = 0
        self.lastTime      = 0
        self.lastSpeed     = 0      
        self.slaveValue    = 0
        
        self.vGMiddle = [0,0,0]
        self.baseLengths = [ 1 for i in range(0,200) ]
        self.slavesValues = []
        
        
    def compute( self, plug , dataBlock ):
        
        outsAttr = [ self.outputTAttr , self.outputRAttr , self.outputSAttr ]                    
        if not ( plug in outsAttr ):
            return om.kUnknownParameter

        trsObj = trsClass.trsClass()   
        # _________________________________ IN MATRIX      
        masterTrs = []
        
        arrayDataHandle = om.MArrayDataHandle( dataBlock.inputValue( self.inputMatrixAttr ) )
        
        for i in range(arrayDataHandle.elementCount()-1):        
            arrayDataHandle.next()
            floatMatrix = (arrayDataHandle.inputValue()).asFloatMatrix()
            masterTrs.append( trsObj.createFromFloatMatrix(  MMatrixToNum(floatMatrix)  ) )  

        # _________________________________ IN DYN ATTR 
        
        dataHandle     = dataBlock.inputValue( self.inputTimeAttr )
        intime         = dataHandle.asFloat()           

        dataHandle     = dataBlock.inputValue( self.inputActivateAttr )
        activate       = dataHandle.asFloat()         
               
        dataHandle     = dataBlock.inputValue( self.input1Attr )
        mass           = dataHandle.asFloat()           
                         
        dataHandle     = dataBlock.inputValue( self.input2Attr )
        elasticity     = dataHandle.asFloat()
                        
        dataHandle     = dataBlock.inputValue( self.input3Attr )
        damping        = dataHandle.asFloat()   
        
        dataHandle     = dataBlock.inputValue( self.input4Attr )
        gravity        = dataHandle.asFloat()     

        # _________________________________ SAVE NEXT EVAL        
        
        dataHandle     = dataBlock.inputValue( self.inputNext1Attr )
        self.nbrEval   = dataHandle.asFloat()
        
        dataHandle     = dataBlock.inputValue( self.inputNext2Attr ) 
        self.lastTime  = dataHandle.asFloat()                    
  
        dataHandle     = dataBlock.inputValue( self.inputNext3Attr )
        self.lastSpeed = dataHandle.asFloat3()
        self.lastSpeed = [ self.lastSpeed[0] , self.lastSpeed[1] , self.lastSpeed[2] ]      
                          

        self.slavesValues = []
        
        arrayDataHandle = om.MArrayDataHandle( dataBlock.inputValue( self.inputNext4Attr )  )
        
        for i in range(arrayDataHandle.elementCount()-1):        
            arrayDataHandle.next()
            slaveValue = (arrayDataHandle.inputValue()).asFloat3()
            self.slavesValues.append( [ slaveValue[0] , slaveValue[1] , slaveValue[2] ] )   
        
        
        
        #_____________________________________________________________________________________COMPUTE
        
        gravityVector = [ 0 , gravity , 0 ]
               
        #_______________ DELTA TIME        
        incrEval      = 0.04
        self.nbrEval += incrEval
        
        curTime       = self.nbrEval       
        deltaTime     = curTime - self.lastTime         
        self.lastTime = curTime 
        
        #_______________ DYNAMIC       
        curentFrame   = mc.currentTime( query = True )
        startFrame    = mc.playbackOptions( query = True , minTime = True )

        if( activate == 0 ) or ( curentFrame == startFrame ):
            
            self.nbrEval        = 0
            self.lastTime       = 0
            self.lastSpeed      = [ 0 , 0 , 0 ]       
            
            self.slavesValues = []
            for i in range( 0 , len(masterTrs) ):
            	self.slavesValues.append( masterTrs[i][0:3] )
            	
            for i in range( 1 , len(masterTrs) ):
            	leadPos  = masterTrs[i-1]
            	slavePos = masterTrs[i]
            	baseLengths[i] = ompy.MVector( slavePos[0] - leadPos[0] , slavePos[1] - leadPos[1] , slavePos[2] - leadPos[2] ).length()
                
        else:
        	

            # FOLLOW DYN
            self.slaveValue[0] = inMatrices[0][0:3]
            
            for i in range( 1 , len(masterTrs) ):
            	leadPos  = self.slavesValues[i-1]
            	slavePos = self.slavesValues[i] 
            	
            	vLeadSlave       = ompy.MVector( slavePos[0] - leadPos[0] , slavePos[1] - leadPos[1] , slavePos[2] - leadPos[2] ) 
            	vLeadSlaveAdjust = vLeadSlave  * ( baseLengths[i] / vLeadSlave.length() )
            	slavePosNew      = [ leadPos[0] + vLeadSlaveAdjust.x , leadPos[1] + vLeadSlaveAdjust.y , leadPos[2] + vLeadSlaveAdjust.z ] 
            	
            	self.slavesValues[i] = slavePosNew
            	
            	
                
                
        
        
        translate = self.slaveValue
        rotate    = [0,0,0]        
        scale     = [1,1,1] 
        
        #_____________________________________________________________________________________ OUT NEXT
 
        nodeName = self.name()  
        mc.undoInfo( swf = 0 )
        
        mc.setAttr( nodeName +'.'+ self.kInputNext1AttrName  , self.nbrEval  ) 
        mc.setAttr( nodeName +'.'+ self.kInputNext2AttrName  , self.lastTime  )        
        #mc.setAttr( nodeName +'.'+ self.kInputNext3AttrName  , self.lastSpeed[0] ,  self.lastSpeed[1] ,  self.lastSpeed[2] , type = 'double3') 
        
        for i in range( 0 , len( self.slavesValues ) ):
        	mc.setAttr( nodeName +'.'+ self.kInputNext4AttrName + '[{0}]'.format(i)  , self.slavesValues[i][0] , self.slavesValues[i][1] , self.slavesValues[i][2] , type = 'double3')  
        
        mc.undoInfo( swf = 1 )        

        #_____________________________________________________________________________________COMPUTE OUT

        dataHandle = dataBlock.outputValue( self.outputTAttr )       
        dataHandle.set3Double( translate[0] , translate[1] , translate[2] )
        dataHandle.setClean()        
     
        dataHandle = dataBlock.outputValue( self.outputRAttr )       
        dataHandle.set3Double( math.radians(rotate[0]) , math.radians(rotate[1]) , math.radians(rotate[2]) )  
        dataHandle.setClean()    
        
        dataHandle = dataBlock.outputValue( self.outputSAttr )       
        dataHandle.set3Double( scale[0] , scale[1] , scale[2]  ) 
        dataHandle.setClean()            

        dataBlock.setClean( plug ) 
        
   
        
    @classmethod
    def nodeCreator(cls):
        return ommpx.asMPxPtr(cls())


    @classmethod
    def nodeInitializer(cls):

        # _________________________________ IN MATRIX    

        nAttr = om.MFnMatrixAttribute() 
        
        cls.inputMatrixAttr = nAttr.create(cls.kInputMatrixAttrLongName, cls.kInputMatrixAttrName , om.MFnNumericData.kFloat  )
        nAttr.setKeyable(True)
        nAttr.setArray(True)
        nAttr.setReadable(False)
        nAttr.setIndexMatters(False)
        nAttr.setDisconnectBehavior(om.MFnNumericAttribute.kDelete)        
        
        # _________________________________ IN DYN ATTR 

        nAttr = om.MFnNumericAttribute()   
        
        cls.inputTimeAttr = nAttr.create(cls.kInputTimeAttrLongName, cls.kInputTimeAttrName , om.MFnNumericData.kFloat  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)    
        cls.inputActivateAttr = nAttr.create(cls.kInputActivateAttrLongName, cls.kInputActivateAttrName , om.MFnNumericData.kFloat  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)  
        
        cls.input1Attr = nAttr.create(cls.kInput1AttrLongName, cls.kInput1AttrName , om.MFnNumericData.kFloat  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)        
        cls.input2Attr = nAttr.create(cls.kInput2AttrLongName, cls.kInput2AttrName , om.MFnNumericData.kFloat  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)         
        cls.input3Attr = nAttr.create(cls.kInput3AttrLongName, cls.kInput3AttrName , om.MFnNumericData.kFloat  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)         
        cls.input4Attr = nAttr.create(cls.kInput4AttrLongName, cls.kInput4AttrName , om.MFnNumericData.kFloat  )
        nAttr.setKeyable(True)  
        nAttr.setReadable(False)   
        
        # _________________________________ SAVE NEXT EVAL
        
        nAttr = om.MFnNumericAttribute() 
        
        cls.inputNext1Attr = nAttr.create(cls.kInputNext1AttrLongName, cls.kInputNext1AttrName , om.MFnNumericData.kFloat  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False) 
        cls.inputNext2Attr = nAttr.create(cls.kInputNext2AttrLongName, cls.kInputNext2AttrName , om.MFnNumericData.kFloat  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)   
        cls.inputNext3Attr = nAttr.create(cls.kInputNext3AttrLongName, cls.kInputNext3AttrName , om.MFnNumericData.k3Float  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)          
        cls.inputNext4Attr = nAttr.create(cls.kInputNext4AttrLongName, cls.kInputNext4AttrName , om.MFnNumericData.k3Float  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)   
        nAttr.setArray(True)    
        
        #________________________________ OUT TRANSLATE
        nAttr = om.MFnNumericAttribute()         
        cls.outputTXAttr = nAttr.create( cls.kOutputTXAttrLongName , cls.kOutputTXAttrName , om.MFnNumericData.kDouble )      
        cls.outputTYAttr = nAttr.create( cls.kOutputTYAttrLongName , cls.kOutputTYAttrName , om.MFnNumericData.kDouble )     
        cls.outputTZAttr = nAttr.create( cls.kOutputTZAttrLongName , cls.kOutputTZAttrName , om.MFnNumericData.kDouble )             
 
        nAttr = om.MFnNumericAttribute()        
        cls.outputTAttr = nAttr.create( cls.kOutputTAttrLongName , cls.kOutputTAttrName , cls.outputTXAttr , cls.outputTYAttr , cls.outputTZAttr ) 
        nAttr.setWritable(False)
        nAttr.setStorable(False)        
        nAttr.setArray(True)    
        
        #________________________________ OUT ROTATE
        nAttr = om.MFnUnitAttribute()         
        cls.outputRXAttr = nAttr.create( cls.kOutputRXAttrLongName , cls.kOutputRXAttrName , om.MFnUnitAttribute.kAngle )      
        cls.outputRYAttr = nAttr.create( cls.kOutputRYAttrLongName , cls.kOutputRYAttrName , om.MFnUnitAttribute.kAngle )     
        cls.outputRZAttr = nAttr.create( cls.kOutputRZAttrLongName , cls.kOutputRZAttrName , om.MFnUnitAttribute.kAngle )             
 
        nAttr = om.MFnNumericAttribute()        
        cls.outputRAttr = nAttr.create( cls.kOutputRAttrLongName , cls.kOutputRAttrName , cls.outputRXAttr , cls.outputRYAttr , cls.outputRZAttr ) 
        nAttr.setWritable(False)
        nAttr.setStorable(False)
        nAttr.setArray(True)
    
        
        #________________________________ OUT SCALE
        nAttr = om.MFnNumericAttribute()         
        cls.outputSXAttr = nAttr.create( cls.kOutputSXAttrLongName , cls.kOutputSXAttrName , om.MFnNumericData.kDouble )      
        cls.outputSYAttr = nAttr.create( cls.kOutputSYAttrLongName , cls.kOutputSYAttrName , om.MFnNumericData.kDouble )     
        cls.outputSZAttr = nAttr.create( cls.kOutputSZAttrLongName , cls.kOutputSZAttrName , om.MFnNumericData.kDouble ) 
        
        nAttr = om.MFnNumericAttribute()          
        cls.outputSAttr = nAttr.create(cls.kOutputSAttrLongName, cls.kOutputSAttrName , cls.outputSXAttr , cls.outputSYAttr , cls.outputSZAttr )
        nAttr.setWritable(False)
        nAttr.setStorable(False)        
        nAttr.setArray(True)   

        
        #________________________________ ADD 
        cls.addAttribute(cls.inputMatrixAttr )        
        cls.addAttribute(cls.inputTimeAttr ) 
        cls.addAttribute(cls.inputActivateAttr ) 
        cls.addAttribute(cls.input1Attr ) 
        cls.addAttribute(cls.input2Attr ) 
        cls.addAttribute(cls.input3Attr ) 
        cls.addAttribute(cls.input4Attr )         
        cls.addAttribute(cls.inputNext1Attr ) 
        cls.addAttribute(cls.inputNext2Attr )         
        cls.addAttribute(cls.inputNext3Attr ) 
        cls.addAttribute(cls.inputNext4Attr )        
        cls.addAttribute(cls.outputTAttr )        
        cls.addAttribute(cls.outputRAttr )
        cls.addAttribute(cls.outputSAttr ) 


        #__________________________________________________________ AFFECT MAIN 

        cls.attributeAffects( cls.inputMatrixAttr , cls.outputTAttr )
        cls.attributeAffects( cls.inputMatrixAttr , cls.outputRAttr )
        cls.attributeAffects( cls.inputMatrixAttr , cls.outputSAttr )              
          
        cls.attributeAffects( cls.inputTimeAttr , cls.outputTAttr )  
        cls.attributeAffects( cls.inputTimeAttr , cls.outputRAttr )  
        cls.attributeAffects( cls.inputTimeAttr , cls.outputSAttr )  

        cls.attributeAffects( cls.inputActivateAttr , cls.outputTAttr )  
        cls.attributeAffects( cls.inputActivateAttr , cls.outputRAttr ) 
        cls.attributeAffects( cls.inputActivateAttr , cls.outputSAttr ) 

        
def initializePlugin(obj):
    plugin = ommpx.MFnPlugin( obj , 'matthieuCantat', '1.0', 'Any')
    try:
        plugin.registerNode( followNode.kPluginNodeTypeName, followNode.kPluginNodeId, followNode.nodeCreator, followNode.nodeInitializer)
    except:
        raise Exception('Failed to register node: {0}'.format(followNode.kPluginNodeTypeName) )
   

def uninitializePlugin(obj):
    plugin = ommpx.MFnPlugin(obj)
    try:
        plugin.deregisterNode( followNode.kPluginNodeId )
    except:
        raise Exception('Failed to unregister node: {0}'.format( followNode.kPluginNodeTypeName ) )

        


        
########################################################################################################################################################################################################        
########################################################################################################################################################################################################  PROC UTILS      
########################################################################################################################################################################################################        
        
  
def MMatrixToNum( matrix ):
    return [  matrix(0,0) , matrix(0,1) , matrix(0,2) , matrix(0,3)  ,  matrix(1,0) , matrix(1,1) , matrix(1,2) , matrix(1,3)  ,  matrix(2,0) , matrix(2,1) , matrix(2,2) , matrix(2,3) ,  matrix(3,0) , matrix(3,1) , matrix(3,2) , matrix(3,3)  ]     
        
 