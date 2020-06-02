


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


class dynTubeNode(ommpx.MPxNode):

    kPluginNodeTypeName = 'dynTubeNode'
    kPluginNodeId = om.MTypeId(0x00033450)

    # _________________________________ IN MATRIX    
    inputMatrixAAttr = None
    kInputMatrixAAttrName = 'inMatrixA'
    kInputMatrixAAttrLongName = 'inMatrixA'       
    
    inputMatrixBAttr = None
    kInputMatrixBAttrName = 'inMatrixB'
    kInputMatrixBAttrLongName = 'inMatrixB'      

    inputMatrixGAttr = None
    kInputMatrixGAttrName = 'inMatrixG'
    kInputMatrixGAttrLongName = 'inMatrixG'          
    
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
        
        
    def compute( self, plug , dataBlock ):
        
        outsAttr = [ self.outputTAttr , self.outputRAttr , self.outputSAttr ]                    
        if not ( plug in outsAttr ):
            return om.kUnknownParameter


        # _________________________________ IN MATRIX
        
        dataHandle     = dataBlock.inputValue( self.inputMatrixAAttr )
        floatMatrix    = dataHandle.asFloatMatrix()
        matrixA        = MMatrixToNum(floatMatrix) 

        dataHandle     = dataBlock.inputValue( self.inputMatrixBAttr )
        floatMatrix    = dataHandle.asFloatMatrix()
        matrixB        = MMatrixToNum(floatMatrix)         
        
        dataHandle     = dataBlock.inputValue( self.inputMatrixGAttr )
        floatMatrix    = dataHandle.asFloatMatrix()
        matrixG        = MMatrixToNum(floatMatrix)           
               
        
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
        
        dataHandle     = dataBlock.inputValue( self.inputNext4Attr )           
        self.slaveValue= dataHandle.asFloat3()          
        self.slaveValue= [ self.slaveValue[0] , self.slaveValue[1] , self.slaveValue[2] ]             
                    
        #_____________________________________________________________________________________COMPUTE
        
        gravityVector = [ 0 , gravity , 0 ]
               
        #_______________ DELTA TIME        
        incrEval      = 0.04
        self.nbrEval += incrEval
        
        curTime       = self.nbrEval       
        deltaTime     = curTime - self.lastTime         
        self.lastTime = curTime 
        
        #_______________ TRS  
        trsObj        = trsClass.trsClass()         
        masterATrs  = trsObj.createFromFloatMatrix( matrixA ) 
        masterBTrs  = trsObj.createFromFloatMatrix( matrixB )   
        matrixGTrs  = trsObj.createFromFloatMatrix( matrixG )    
        
        middleTrs = trsObj.getMiddleTrs( masterBTrs , inTrsValue = masterATrs )
          

        #_______________ CALCULATE F TENSION SELF COLLISION
        
        tensF = [0,0,0]         

        
        #_______________ DYNAMIC       
        curentFrame   = mc.currentTime( query = True )
        startFrame    = mc.playbackOptions( query = True , minTime = True )

        if( activate == 0 ) or ( curentFrame == startFrame ):
            
            self.nbrEval        = 0
            self.lastTime       = 0
            self.lastSpeed      = [ 0 , 0 , 0 ]       
            self.slaveValue     = middleTrs[0:3]

                
        else:
        	
            for i in range( 0 , 3 ):
                tensF[i] = - ( mass * gravityVector[i] ) + matrixGTrs[i] * ( 2 * elasticity )             	
                        
            # DYNAMIC
            for i in range( 0 , 3 ):
                self.slaveValue[i] , self.lastSpeed[i] = self.computeTubeDynamic( masterATrs[i] , masterBTrs[i] , self.slaveValue[i] , self.lastSpeed[i] , mass , elasticity , damping , gravityVector[i] , tensF[i] ,  deltaTime )         

        
        
        
        translate = self.slaveValue
        rotate    = [0,0,0]        
        scale     = [1,1,1] 
        
        #_____________________________________________________________________________________ OUT NEXT
 
        nodeName = self.name()  
        mc.undoInfo( swf = 0 )
        
        mc.setAttr( nodeName +'.'+ self.kInputNext1AttrName  , self.nbrEval  ) 
        mc.setAttr( nodeName +'.'+ self.kInputNext2AttrName  , self.lastTime  )        
        mc.setAttr( nodeName +'.'+ self.kInputNext3AttrName  , self.lastSpeed[0] ,  self.lastSpeed[1] ,  self.lastSpeed[2] , type = 'double3')            
        mc.setAttr( nodeName +'.'+ self.kInputNext4AttrName  , self.slaveValue[0] , self.slaveValue[1] , self.slaveValue[2] , type = 'double3')  
        
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
        
   
    #___________________________________________________________________________________________________________________________________________________________________________________  computeDynamicLimites
    
    def computeTubeDynamic( self , leadValueA , leadValueB , lastSlaveValue , lastSlaveSpeed , mass , elasticity , damping , gravity , tensionF , deltaTime ):

        #___________________INIT
        slaveValue = lastSlaveValue
        lastSpeed  = lastSlaveSpeed
        
        #__________________FIRST APROXIMATION            
        # ACCELERATION  
        elasticityAF   =  elasticity * ( leadValueA  - slaveValue )    
        elasticityBF   =  elasticity * ( leadValueB  - slaveValue )          
        frictionF      =  damping    * lastSpeed  * -1  
        gravityF       =  gravity    * mass       
        acceleration   =  ( elasticityAF + elasticityBF + frictionF + gravityF + tensionF ) / mass                 
        # EULER APPROXIMATION
        lastSpeed  = lastSpeed   + acceleration * deltaTime
        slaveValue = slaveValue  + lastSpeed    * deltaTime   
        # EXTRACT SLOPE         
        slopeA     = lastSpeed   * deltaTime

        #__________________SECOND APROXIMATION                 
        # ACCELERATION 
        elasticityAF  =  elasticity * ( leadValueA  - slaveValue )        
        elasticityBF  =  elasticity * ( leadValueB  - slaveValue )      
        frictionF     =  damping    * lastSpeed  * -1 
        gravityF      =  gravity    * mass         
        acceleration  =  ( elasticityAF + elasticityBF + frictionF + gravityF + tensionF ) / mass                           
        # EULER APPROXIMATION
        lastSpeed = lastSpeed + acceleration * deltaTime
        # EXTRACT SLOPE    
        slopeB    = lastSpeed * deltaTime
                   
        #__________________HEUN APPROXIMATION: 2 slope average         
        slaveValue    = slaveValue + ( slopeA + slopeB )/2          
                
        return slaveValue , lastSpeed             
        
        
        
    @classmethod
    def nodeCreator(cls):
        return ommpx.asMPxPtr(cls())


    @classmethod
    def nodeInitializer(cls):

        # _________________________________ IN MATRIX    

        nAttr = om.MFnMatrixAttribute() 
        
        cls.inputMatrixAAttr = nAttr.create(cls.kInputMatrixAAttrLongName, cls.kInputMatrixAAttrName , om.MFnNumericData.kFloat  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)
        cls.inputMatrixBAttr = nAttr.create(cls.kInputMatrixBAttrLongName, cls.kInputMatrixBAttrName , om.MFnNumericData.kFloat  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)        
        cls.inputMatrixGAttr = nAttr.create(cls.kInputMatrixGAttrLongName, cls.kInputMatrixGAttrName , om.MFnNumericData.kFloat  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)    
        
        
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
        
        #________________________________ OUT TRANSLATE
        nAttr = om.MFnNumericAttribute()         
        cls.outputTXAttr = nAttr.create( cls.kOutputTXAttrLongName , cls.kOutputTXAttrName , om.MFnNumericData.kDouble )      
        cls.outputTYAttr = nAttr.create( cls.kOutputTYAttrLongName , cls.kOutputTYAttrName , om.MFnNumericData.kDouble )     
        cls.outputTZAttr = nAttr.create( cls.kOutputTZAttrLongName , cls.kOutputTZAttrName , om.MFnNumericData.kDouble )             
 
        nAttr = om.MFnNumericAttribute()        
        cls.outputTAttr = nAttr.create( cls.kOutputTAttrLongName , cls.kOutputTAttrName , cls.outputTXAttr , cls.outputTYAttr , cls.outputTZAttr ) 
        nAttr.setWritable(False)
        nAttr.setStorable(False)  
        
        #________________________________ OUT ROTATE
        nAttr = om.MFnUnitAttribute()         
        cls.outputRXAttr = nAttr.create( cls.kOutputRXAttrLongName , cls.kOutputRXAttrName , om.MFnUnitAttribute.kAngle )      
        cls.outputRYAttr = nAttr.create( cls.kOutputRYAttrLongName , cls.kOutputRYAttrName , om.MFnUnitAttribute.kAngle )     
        cls.outputRZAttr = nAttr.create( cls.kOutputRZAttrLongName , cls.kOutputRZAttrName , om.MFnUnitAttribute.kAngle )             
 
        nAttr = om.MFnNumericAttribute()        
        cls.outputRAttr = nAttr.create( cls.kOutputRAttrLongName , cls.kOutputRAttrName , cls.outputRXAttr , cls.outputRYAttr , cls.outputRZAttr ) 
        nAttr.setWritable(False)
        nAttr.setStorable(False)
        
        #________________________________ OUT SCALE
        nAttr = om.MFnNumericAttribute()         
        cls.outputSXAttr = nAttr.create( cls.kOutputSXAttrLongName , cls.kOutputSXAttrName , om.MFnNumericData.kDouble )      
        cls.outputSYAttr = nAttr.create( cls.kOutputSYAttrLongName , cls.kOutputSYAttrName , om.MFnNumericData.kDouble )     
        cls.outputSZAttr = nAttr.create( cls.kOutputSZAttrLongName , cls.kOutputSZAttrName , om.MFnNumericData.kDouble ) 
        
        nAttr = om.MFnNumericAttribute()          
        cls.outputSAttr = nAttr.create(cls.kOutputSAttrLongName, cls.kOutputSAttrName , cls.outputSXAttr , cls.outputSYAttr , cls.outputSZAttr )
        nAttr.setWritable(False)
        nAttr.setStorable(False)

        
        #________________________________ ADD 
        cls.addAttribute(cls.inputMatrixAAttr )
        cls.addAttribute(cls.inputMatrixBAttr )
        cls.addAttribute(cls.inputMatrixGAttr )         
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
        cls.attributeAffects( cls.inputMatrixAAttr , cls.outputTAttr )
        cls.attributeAffects( cls.inputMatrixAAttr , cls.outputRAttr )
        cls.attributeAffects( cls.inputMatrixAAttr , cls.outputSAttr )
        
        cls.attributeAffects( cls.inputMatrixBAttr , cls.outputTAttr )
        cls.attributeAffects( cls.inputMatrixBAttr , cls.outputRAttr )
        cls.attributeAffects( cls.inputMatrixBAttr , cls.outputSAttr )
        
        cls.attributeAffects( cls.inputMatrixGAttr , cls.outputTAttr )
        cls.attributeAffects( cls.inputMatrixGAttr , cls.outputRAttr )
        cls.attributeAffects( cls.inputMatrixGAttr , cls.outputSAttr )         
          
        cls.attributeAffects( cls.inputTimeAttr , cls.outputTAttr )  
        cls.attributeAffects( cls.inputTimeAttr , cls.outputRAttr )  
        cls.attributeAffects( cls.inputTimeAttr , cls.outputSAttr )  

        cls.attributeAffects( cls.inputActivateAttr , cls.outputTAttr )  
        cls.attributeAffects( cls.inputActivateAttr , cls.outputRAttr ) 
        cls.attributeAffects( cls.inputActivateAttr , cls.outputSAttr ) 

        
def initializePlugin(obj):
    plugin = ommpx.MFnPlugin( obj , 'matthieuCantat', '1.0', 'Any')
    try:
        plugin.registerNode( dynTubeNode.kPluginNodeTypeName, dynTubeNode.kPluginNodeId, dynTubeNode.nodeCreator, dynTubeNode.nodeInitializer)
    except:
        raise Exception('Failed to register node: {0}'.format(dynTubeNode.kPluginNodeTypeName) )
   

def uninitializePlugin(obj):
    plugin = ommpx.MFnPlugin(obj)
    try:
        plugin.deregisterNode( dynTubeNode.kPluginNodeId )
    except:
        raise Exception('Failed to unregister node: {0}'.format(dynTubeNode.kPluginNodeTypeName) )

        


        
########################################################################################################################################################################################################        
########################################################################################################################################################################################################  PROC UTILS      
########################################################################################################################################################################################################        
        
  
def MMatrixToNum( matrix ):
    return [  matrix(0,0) , matrix(0,1) , matrix(0,2) , matrix(0,3)  ,  matrix(1,0) , matrix(1,1) , matrix(1,2) , matrix(1,3)  ,  matrix(2,0) , matrix(2,1) , matrix(2,2) , matrix(2,3) ,  matrix(3,0) , matrix(3,1) , matrix(3,2) , matrix(3,3)  ]     
        
 