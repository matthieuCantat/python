



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


import python.utils.utilsMayaApi as utilsMayaApi
import python.classe.trsClass as trsClass


class dynamicRotation(ommpx.MPxNode):

    kPluginNodeTypeName = 'dynamicTrsNode'
    kPluginNodeId = om.MTypeId(0x00033446)

    
    inputTimeAttr = None
    kInputTimeAttrName = 'time'
    kInputTimeAttrLongName = 'time'
    
    # IN ATTR : MAIN
    inputAttr = None
    kInput1AttrName = 'activate'
    kInput1AttrLongName = 'activate'

    input3Attr = None
    kInput3AttrName = 'worldMatrix'
    kInput3AttrLongName = 'worldMatrix' 
    
    input4Attr = None
    kInput4AttrName = 'masse'
    kInput4AttrLongName = 'masse'       

    input5Attr = None
    kInput5AttrName = 'elasticity'
    kInput5AttrLongName = 'elasticity'       

    input6Attr = None
    kInput6AttrName = 'damping'
    kInput6AttrLongName = 'damping'  

    input7Attr = None
    kInput7AttrName = 'collision'
    kInput7AttrLongName = 'collision'      
       
    input8Attr = None
    kInput8AttrName = 'collisionMatrix'
    kInput8AttrLongName = 'collisionMatrix'  

    input9Attr = None
    kInput9AttrName = 'hitSphereSize'
    kInput9AttrLongName = 'hitSphereSize'  
   
    input10Attr = None
    kInput10AttrName = 'worldMatrixFather'
    kInput10AttrLongName = 'worldMatrixFather'        
 
    input15Attr = None
    kInput15AttrName = 'axeDir'
    kInput15AttrLongName = 'axeDir' 
    
    
    # IN ATTR : SAVE NEXT EVAL

    input11Attr = None
    kInput11AttrName = 'nbrEval'
    kInput11AttrLongName = 'nbrEval'      

    input12Attr = None
    kInput12AttrName = 'lastTime'
    kInput12AttrLongName = 'lastTime'      

    input13TAttr = None
    kInput13TAttrName = 'lastSpeedT'
    kInput13TAttrLongName = 'lastSpeedT'       

    input13RAttr = None
    kInput13RAttrName = 'lastSpeedR'
    kInput13RAttrLongName = 'lastSpeedR'   

    input13SAttr = None
    kInput13SAttrName = 'lastSpeedS'
    kInput13SAttrLongName = 'lastSpeedS'       
    
    
    input14TAttr = None
    kInput14TAttrName = 'slaveTValue'
    kInput14TAttrLongName = 'slaveTValue'     

    input14RAttr = None
    kInput14RAttrName = 'slaveRValue'
    kInput14RAttrLongName = 'slaveRValue'   
    
    input14SAttr = None
    kInput14SAttrName = 'slaveSValue'
    kInput14SAttrLongName = 'slaveSValue'       
    
    # OUT ATTR___________________________TRANSLATE         
    outputTX = None
    kOutputTXAttrName = 'outTranX'
    kOutputTXAttrLongName = 'outTranslateX'
    
    outputTY = None
    kOutputTYAttrName = 'outTranY'
    kOutputTYAttrLongName = 'outTranslateY'
 
    outputTZ = None
    kOutputTZAttrName = 'outTranZ'
    kOutputTZAttrLongName = 'outTranslateZ'    
    
    # OUT ATTR___________________________ROTATE           
    outputRX = None
    kOutputRXAttrName = 'outRotX'
    kOutputRXAttrLongName = 'outRotateX'
    
    outputRY = None
    kOutputRYAttrName = 'outRotY'
    kOutputRYAttrLongName = 'outRotateY'
 
    outputRZ = None
    kOutputRZAttrName = 'outRotZ'
    kOutputRZAttrLongName = 'outRotateZ' 
    
    # OUT ATTR___________________________SCALE     
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
        
        self.lastSpeed     = [0,0,0,0,0,0,0,0,0]
        
        self.lastSpeedT     = [0,0,0]          
        self.lastSpeedR     = [0,0,0]  
        self.lastSpeedS     = [0,0,0]  

        self.slaveValue    = [0,0,0,0,0,0,1,1,1]  
        
        self.slaveTValue     = [0,0,0]          
        self.slaveRValue     = [0,0,0]  
        self.slaveSValue     = [1,1,1]   

    def compute( self, plug , dataBlock ):  
            
    	outsAttr = [ self.outputTXAttr , self.outputTYAttr , self.outputTZAttr , self.outputRXAttr , self.outputRYAttr , self.outputRZAttr , self.outputSXAttr , self.outputSYAttr , self.outputSZAttr ]                    
        if not ( plug in outsAttr ):
            return om.kUnknownParameter                        
        #_____________________________________________________________________________________ IN   


        dataHandle     = dataBlock.inputValue( self.inputTimeAttr )
        intime         = dataHandle.asFloat()           

        dataHandle     = dataBlock.inputValue( self.input1Attr )
        activate       = dataHandle.asFloat()                 

        dataHandle       = dataBlock.inputValue( self.input3Attr )
        worldMFloatMatrix = dataHandle.asFloatMatrix()
        worldMatrix       = MMatrixToNum(worldMFloatMatrix) 
        
        dataHandle     = dataBlock.inputValue( self.input4Attr )
        mass           = dataHandle.asFloat()           
                         
        dataHandle     = dataBlock.inputValue( self.input5Attr )
        elasticity     = dataHandle.asFloat()
                        
        dataHandle     = dataBlock.inputValue( self.input6Attr )
        damping        = dataHandle.asFloat()   
        
        dataHandle     = dataBlock.inputValue( self.input7Attr )
        collision      = dataHandle.asFloat()        

        
        dataHandle       = dataBlock.inputValue( self.input8Attr )
        inMFloatMatrix   = dataHandle.asFloatMatrix()
        collisionMatrix  = MMatrixToNum(inMFloatMatrix)
        
        dataHandle     = dataBlock.inputValue( self.input9Attr )
        hitSphereSize  = dataHandle.asFloat()          
        
        dataHandle       = dataBlock.inputValue( self.input10Attr )
        inMFloatMatrix   = dataHandle.asFloatMatrix()
        fatherMatrix     = MMatrixToNum(inMFloatMatrix)

        dataHandle     = dataBlock.inputValue( self.input11Attr )
        self.nbrEval   = dataHandle.asFloat()
        
        dataHandle     = dataBlock.inputValue( self.input12Attr ) 
        self.lastTime  = dataHandle.asFloat()                    
  
        dataHandle      = dataBlock.inputValue( self.input13TAttr )
        dataHandleNum   = dataHandle.asFloat3()
        self.lastSpeedT = [ dataHandleNum[0] , dataHandleNum[1] , dataHandleNum[2] ]      

        dataHandle      = dataBlock.inputValue( self.input13RAttr )
        dataHandleNum   = dataHandle.asFloat3()
        self.lastSpeedR = [ dataHandleNum[0] , dataHandleNum[1] , dataHandleNum[2] ]    
        
        dataHandle      = dataBlock.inputValue( self.input13SAttr )
        dataHandleNum   = dataHandle.asFloat3()
        self.lastSpeedS = [ dataHandleNum[0] , dataHandleNum[1] , dataHandleNum[2] ]            

        
        dataHandle       = dataBlock.inputValue( self.input14TAttr )           
        dataHandleNum    = dataHandle.asFloat3()          
        self.slaveTValue = [ dataHandleNum[0] , dataHandleNum[1] , dataHandleNum[2] ]             

        dataHandle       = dataBlock.inputValue( self.input14RAttr )           
        dataHandleNum    = dataHandle.asFloat3()          
        self.slaveRValue = [ dataHandleNum[0] , dataHandleNum[1] , dataHandleNum[2] ] 

        dataHandle       = dataBlock.inputValue( self.input14SAttr )           
        dataHandleNum    = dataHandle.asFloat3()          
        self.slaveSValue = [ dataHandleNum[0] , dataHandleNum[1] , dataHandleNum[2] ]         
        
        
        dataHandle     = dataBlock.inputValue( self.input15Attr )           
        axeDirWay      = dataHandle.asInt()  
                  
        
        #_____________________________________________________________________________________COMPUTE
        trsObj = trsClass.trsClass() 
        
        #_______________ SIGN AXE         
        signDir = 1
        axeDir  = axeDirWay
        if( 2 < axeDir ):
            signDir = -1
            axeDir -= 3 
            
        #_______________ DELTA TIME        
        incrEval      = 0.04
        self.nbrEval += incrEval
        
        curTime       = self.nbrEval       
        deltaTime     = curTime - self.lastTime         
        self.lastTime = curTime 
        
        #_______________ TRS       
        initTrsWorld  = trsObj.createFromFloatMatrix( worldMatrix ) 
        
        # COLLISION INIT
        
        leadTrsWorld = initTrsWorld 
        
        if not( collision == 0 ):
                        
            # get vector normal + plane coords
            axeNormal = 0
            trsObj.createFromFloatMatrix( collisionMatrix )
        
            vectorNormal  = trsObj.toTripleVectors()[axeNormal]
            mVectorNormal = ompy.MVector( vectorNormal[0] , vectorNormal[1] , vectorNormal[2] ) 
            mVectorNormal.normalize()
            vContact = mVectorNormal * hitSphereSize            
            
            planeCoords   = trsObj.toPlaneCoords( axeNormal )             
                                
            # RECOMPUTE LEAD : leadTrsWorld
            snapOnPlane    = trsObj.snapOnPlane( planeCoords , inTrsValue = initTrsWorld )               
            vSnapInit      = ompy.MVector( initTrsWorld[0]   - snapOnPlane[0] , initTrsWorld[1]   - snapOnPlane[1] , initTrsWorld[2]   - snapOnPlane[2] )
            
            if( vSnapInit.length() <= hitSphereSize ) or ( mVectorNormal * vSnapInit <= 0 ):
                leadTrsWorld = [ snapOnPlane[0] + vContact.x , snapOnPlane[1] + vContact.y , snapOnPlane[2] + vContact.z ] + leadTrsWorld[3:9]        

        
        #_______________ DYNAMIC       
        curentFrame   = mc.currentTime( query = True )
        startFrame    = mc.playbackOptions( query = True , minTime = True )

        if( activate == 0 ) or ( curentFrame == startFrame ):
            
            self.nbrEval        = 0
            self.lastTime       = 0  
            
            self.slaveTValue    = leadTrsWorld[0:3]                  
            self.slaveRValue    = leadTrsWorld[3:6]    
            self.slaveSValue    = leadTrsWorld[6:9] 
            
            self.lastSpeedT = [0,0,0]
            self.lastSpeedR = [0,0,0]
            self.lastSpeedS = [0,0,0]
            
            self.slaveValue = self.slaveTValue + self.slaveRValue + self.slaveSValue
            self.lastSpeed  = self.lastSpeedT + self.lastSpeedR + self.lastSpeedS            
            trsOut          = leadTrsWorld
            
        else: 
                        
            # DYNAMIC
            self.slaveValue = self.slaveTValue + self.slaveRValue + self.slaveSValue
            self.lastSpeed  = self.lastSpeedT + self.lastSpeedR + self.lastSpeedS
            
            for i in range( 0 , 9 ):
                self.slaveValue[i] , self.lastSpeed[i] = self.computeDynamic( leadTrsWorld[i] , self.slaveValue[i] , self.lastSpeed[i] , mass , elasticity , damping , deltaTime )   
                           
                        
            # activate modulation
            for i in range( 0 , 9 ):            	
            	self.slaveValue[i] =  self.slaveValue[i] * activate + leadTrsWorld[i] * ( 1 - activate )
            	
            # out
            
            self.slaveTValue = self.slaveValue[0:3]                  
            self.slaveRValue = self.slaveValue[3:6]    
            self.slaveSValue = self.slaveValue[6:9]
            
            self.lastSpeedT = self.lastSpeed[0:3]
            self.lastSpeedR = self.lastSpeed[3:6]
            self.lastSpeedS = self.lastSpeed[6:9]
            
            # COLLISION                   
           
            if not( collision == 0 ):
                                              
                # RECOMPUTE NEXT DYN:   slaveValue   lastSpeed  
                snapOnPlane    = trsObj.snapOnPlane( planeCoords , inTrsValue = self.slaveValue )
                vSnapSlave     = ompy.MVector( self.slaveValue[0] - snapOnPlane[0] , self.slaveValue[1] - snapOnPlane[1] , self.slaveValue[2] - snapOnPlane[2] ) 
                
                if( vSnapSlave.length() <= hitSphereSize ) or ( mVectorNormal * vSnapSlave <= 0 ): 
                    self.slaveValue = [ snapOnPlane[0] + vContact.x , snapOnPlane[1] + vContact.y , snapOnPlane[2] + vContact.z ] + self.slaveValue[6:9]                    
                    #self.slaveValue = snapOnPlane 
                    
                    mLastSpeed    = ompy.MVector( self.lastSpeed[0] , self.lastSpeed[1] , self.lastSpeed[2] )                     
                    if( mVectorNormal * mLastSpeed < 0 ):                 
                        self.lastSpeed = self.getReflectVector( self.lastSpeed , planeCoords , collision )                
            
            self.slaveTValue = self.slaveValue[0:3]                     
            self.lastSpeedT  = self.lastSpeed[0:3]
            
            trsOut = self.slaveTValue + self.slaveRValue + self.slaveSValue                                          
        
        #_____________________________________________________________________________________ OUT NEXT EXAL       
        
        nodeName = self.name()  
        mc.undoInfo( swf = 0 )
        mc.setAttr( nodeName +'.'+ self.kInput11AttrName  , self.nbrEval    )
        mc.setAttr( nodeName +'.'+ self.kInput12AttrName  , self.lastTime   )  
        
        mc.setAttr( nodeName +'.'+ self.kInput13TAttrName  ,  self.lastSpeedT[0] ,  self.lastSpeedT[1] ,  self.lastSpeedT[2] , type = 'double3')   
        mc.setAttr( nodeName +'.'+ self.kInput13RAttrName  ,  self.lastSpeedR[0] ,  self.lastSpeedR[1] ,  self.lastSpeedR[2] , type = 'double3') 
        mc.setAttr( nodeName +'.'+ self.kInput13SAttrName  ,  self.lastSpeedS[0] ,  self.lastSpeedS[1] ,  self.lastSpeedS[2] , type = 'double3') 
        
        mc.setAttr( nodeName +'.'+ self.kInput14TAttrName  , self.slaveTValue[0] , self.slaveTValue[1] , self.slaveTValue[2] , type = 'double3')  
        mc.setAttr( nodeName +'.'+ self.kInput14RAttrName  , self.slaveRValue[0] , self.slaveRValue[1] , self.slaveRValue[2] , type = 'double3')  
        mc.setAttr( nodeName +'.'+ self.kInput14SAttrName  , self.slaveSValue[0] , self.slaveSValue[1] , self.slaveSValue[2] , type = 'double3')          
        mc.undoInfo( swf = 1 )
    
        #_____________________________________________________________________________________ OUT NODE                

        fatherTrs   = trsObj.createFromFloatMatrix( fatherMatrix )         
        trsOutUnder = trsObj.parent( fatherTrs , inTrsValue = trsOut )

        
        dataHandle = dataBlock.outputValue( self.outputTXAttr )       
        dataHandle.setFloat( trsOutUnder[0] )
             
        dataHandle = dataBlock.outputValue( self.outputTYAttr )       
        dataHandle.setFloat( trsOutUnder[1] )
        
        dataHandle = dataBlock.outputValue( self.outputTZAttr )      
        dataHandle.setFloat( trsOutUnder[2] )

        dataHandle = dataBlock.outputValue( self.outputRXAttr )      
        dataHandle.setFloat( trsOutUnder[3] )
        
        dataHandle = dataBlock.outputValue( self.outputRYAttr )      
        dataHandle.setFloat( trsOutUnder[4] )
        
        dataHandle = dataBlock.outputValue( self.outputRZAttr )      
        dataHandle.setFloat( trsOutUnder[5] )

        dataHandle = dataBlock.outputValue( self.outputSXAttr )      
        dataHandle.setFloat( trsOutUnder[6] )

        dataHandle = dataBlock.outputValue( self.outputSYAttr )      
        dataHandle.setFloat( trsOutUnder[7] )

        dataHandle = dataBlock.outputValue( self.outputSZAttr )      
        dataHandle.setFloat( trsOutUnder[8] )
        
        dataBlock.setClean( plug ) 
        
       
    #___________________________________________________________________________________________________________________________________________________________________________________  getMinMaxTranslateValues
    
    def getReflectVector( self , vector , planeCoords , collisionWeight ):
        
        vectorReset = [ planeCoords[0][0] * -1 , planeCoords[0][1] * -1 , planeCoords[0][2] * -1 ]
        
        for i in range( 0 , 3 ):
            for j in range( 0 , 3 ):
                planeCoords[i][j] += vectorReset[j]
        
        
        
        trsObj  = trsClass.trsClass()
        trsObj.value = vector + [0,0,0,1,1,1]
        trsObj.mirror( planeCoords )
        
        trsObj * collisionWeight
        
        reflectVector = trsObj.value[0:3]

        
        return reflectVector
         
 
    #___________________________________________________________________________________________________________________________________________________________________________________  computeDynamicLimites
    
    def computeDynamic( self , leadValue , lastSlaveValue , lastSlaveSpeed , mass , elasticity , damping , deltaTime ):

        #___________________INIT
        slaveValue = lastSlaveValue
        lastSpeed  = lastSlaveSpeed
        
        #__________________FIRST APROXIMATION            
        # ACCELERATION  
        elasticityF  =    elasticity * ( leadValue  - slaveValue )    
        frictionF    =       damping * lastSpeed  * -1                           
        acceleration  =  (elasticityF + frictionF) / mass                 
        # EULER APPROXIMATION
        lastSpeed  = lastSpeed   + acceleration * deltaTime
        slaveValue = slaveValue  + lastSpeed    * deltaTime   
        # EXTRACT SLOPE         
        slopeA     = lastSpeed   * deltaTime

        #__________________SECOND APROXIMATION                 
        # ACCELERATION    
        elasticityF  =    elasticity * ( leadValue  - slaveValue )      
        frictionF    =       damping * lastSpeed  * -1                             
        acceleration  =  (elasticityF + frictionF) / mass                           
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

        nAttr = om.MFnNumericAttribute()   
        
        cls.inputTimeAttr = nAttr.create(cls.kInputTimeAttrLongName, cls.kInputTimeAttrName , om.MFnNumericData.kFloat  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)    
        
        nAttr = om.MFnNumericAttribute()   
        
        cls.input1Attr = nAttr.create(cls.kInput1AttrLongName, cls.kInput1AttrName , om.MFnNumericData.kFloat  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)
        
        nAttr = om.MFnMatrixAttribute() 
        
        cls.input3Attr = nAttr.create(cls.kInput3AttrLongName, cls.kInput3AttrName , om.MFnNumericData.kFloat  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False) 
        
        nAttr = om.MFnNumericAttribute()   
        
        cls.input4Attr = nAttr.create(cls.kInput4AttrLongName, cls.kInput4AttrName , om.MFnNumericData.kFloat  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)        
        
        nAttr = om.MFnNumericAttribute()   
        
        cls.input5Attr = nAttr.create(cls.kInput5AttrLongName, cls.kInput5AttrName , om.MFnNumericData.kFloat  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)         
        
        nAttr = om.MFnNumericAttribute()   
        
        cls.input6Attr = nAttr.create(cls.kInput6AttrLongName, cls.kInput6AttrName , om.MFnNumericData.kFloat  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)         
       
        nAttr = om.MFnNumericAttribute()   
        
        cls.input7Attr = nAttr.create(cls.kInput7AttrLongName, cls.kInput7AttrName , om.MFnNumericData.kFloat  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)            
        
        
        nAttr = om.MFnMatrixAttribute() 
        
        cls.input8Attr = nAttr.create(cls.kInput8AttrLongName, cls.kInput8AttrName , om.MFnNumericData.kFloat  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False) 
        
        nAttr = om.MFnNumericAttribute()   
        
        cls.input9Attr = nAttr.create(cls.kInput9AttrLongName, cls.kInput9AttrName , om.MFnNumericData.kFloat  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)            
        
        nAttr = om.MFnMatrixAttribute() 
        
        cls.input10Attr = nAttr.create(cls.kInput10AttrLongName, cls.kInput10AttrName , om.MFnNumericData.kFloat  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)          

        nAttr = om.MFnNumericAttribute()   
        
        cls.input11Attr = nAttr.create(cls.kInput11AttrLongName, cls.kInput11AttrName , om.MFnNumericData.kFloat  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)  
        
        nAttr = om.MFnNumericAttribute()   
        
        cls.input12Attr = nAttr.create(cls.kInput12AttrLongName, cls.kInput12AttrName , om.MFnNumericData.kFloat  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)  


        nAttr = om.MFnNumericAttribute()   
        
        cls.input13TAttr = nAttr.create(cls.kInput13TAttrLongName, cls.kInput13TAttrName , om.MFnNumericData.k3Float  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)  

        nAttr = om.MFnNumericAttribute()   
        
        cls.input13RAttr = nAttr.create(cls.kInput13RAttrLongName, cls.kInput13RAttrName , om.MFnNumericData.k3Float  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False) 

        nAttr = om.MFnNumericAttribute()   
        
        cls.input13SAttr = nAttr.create(cls.kInput13SAttrLongName, cls.kInput13SAttrName , om.MFnNumericData.k3Float  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)         
        
        
        nAttr = om.MFnNumericAttribute()   
        
        cls.input14TAttr = nAttr.create(cls.kInput14TAttrLongName, cls.kInput14TAttrName , om.MFnNumericData.k3Float  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)  

        nAttr = om.MFnNumericAttribute()   
        
        cls.input14RAttr = nAttr.create(cls.kInput14RAttrLongName, cls.kInput14RAttrName , om.MFnNumericData.k3Float  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False) 

        nAttr = om.MFnNumericAttribute()   
        
        cls.input14SAttr = nAttr.create(cls.kInput14SAttrLongName, cls.kInput14SAttrName , om.MFnNumericData.k3Float  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)         
        
        
        nAttr = om.MFnNumericAttribute()   
        
        cls.input15Attr = nAttr.create(cls.kInput15AttrLongName, cls.kInput15AttrName , om.MFnNumericData.kInt  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False) 
        
        
        # OUTPUT______________________TRANSLATE
               
        nAttr = om.MFnNumericAttribute() 
        
        cls.outputTXAttr = nAttr.create(cls.kOutputTXAttrLongName, cls.kOutputTXAttrName, om.MFnNumericData.kFloat )
        nAttr.setWritable(False)
        nAttr.setStorable(False)
        
        nAttr = om.MFnNumericAttribute() 
        
        cls.outputTYAttr = nAttr.create(cls.kOutputTYAttrLongName, cls.kOutputTYAttrName, om.MFnNumericData.kFloat )
        nAttr.setWritable(False)
        nAttr.setStorable(False)
        
        nAttr = om.MFnNumericAttribute() 
        
        cls.outputTZAttr = nAttr.create(cls.kOutputTZAttrLongName, cls.kOutputTZAttrName, om.MFnNumericData.kFloat )
        nAttr.setWritable(False)
        nAttr.setStorable(False)             

        # OUTPUT______________________ROTATE
               
        nAttr = om.MFnNumericAttribute() 
        
        cls.outputRXAttr = nAttr.create(cls.kOutputRXAttrLongName, cls.kOutputRXAttrName, om.MFnNumericData.kFloat )
        nAttr.setWritable(False)
        nAttr.setStorable(False)
        
        nAttr = om.MFnNumericAttribute() 
        
        cls.outputRYAttr = nAttr.create(cls.kOutputRYAttrLongName, cls.kOutputRYAttrName, om.MFnNumericData.kFloat )
        nAttr.setWritable(False)
        nAttr.setStorable(False)
        
        nAttr = om.MFnNumericAttribute() 
        
        cls.outputRZAttr = nAttr.create(cls.kOutputRZAttrLongName, cls.kOutputRZAttrName, om.MFnNumericData.kFloat )
        nAttr.setWritable(False)
        nAttr.setStorable(False)    

        # OUTPUT______________________SCALE
               
        nAttr = om.MFnNumericAttribute() 
        
        cls.outputSXAttr = nAttr.create(cls.kOutputSXAttrLongName, cls.kOutputSXAttrName, om.MFnNumericData.kFloat )
        nAttr.setWritable(False)
        nAttr.setStorable(False)
        
        nAttr = om.MFnNumericAttribute() 
        
        cls.outputSYAttr = nAttr.create(cls.kOutputSYAttrLongName, cls.kOutputSYAttrName, om.MFnNumericData.kFloat )
        nAttr.setWritable(False)
        nAttr.setStorable(False)
        
        nAttr = om.MFnNumericAttribute() 
        
        cls.outputSZAttr = nAttr.create(cls.kOutputSZAttrLongName, cls.kOutputSZAttrName, om.MFnNumericData.kFloat )
        nAttr.setWritable(False)
        nAttr.setStorable(False)  


        
        cls.addAttribute(cls.inputTimeAttr)  
        cls.addAttribute(cls.input1Attr )
        cls.addAttribute(cls.input3Attr )          
        cls.addAttribute(cls.input4Attr ) 
        cls.addAttribute(cls.input5Attr ) 
        cls.addAttribute(cls.input6Attr )    
        cls.addAttribute(cls.input7Attr ) 
        cls.addAttribute(cls.input8Attr )
        cls.addAttribute(cls.input9Attr )          
        cls.addAttribute(cls.input10Attr)              
        cls.addAttribute(cls.input11Attr)
        cls.addAttribute(cls.input12Attr)        
        cls.addAttribute(cls.input13TAttr)
        cls.addAttribute(cls.input13RAttr)
        cls.addAttribute(cls.input13SAttr)        
        cls.addAttribute(cls.input14TAttr)
        cls.addAttribute(cls.input14RAttr)
        cls.addAttribute(cls.input14SAttr)        
        cls.addAttribute(cls.input15Attr)     

        cls.addAttribute(cls.outputTXAttr )
        cls.addAttribute(cls.outputTYAttr )     
        cls.addAttribute(cls.outputTZAttr ) 
        cls.addAttribute(cls.outputRXAttr )
        cls.addAttribute(cls.outputRYAttr )     
        cls.addAttribute(cls.outputRZAttr )         
        cls.addAttribute(cls.outputSXAttr )
        cls.addAttribute(cls.outputSYAttr )     
        cls.addAttribute(cls.outputSZAttr ) 
        
        #INFLUENCE

        cls.attributeAffects( cls.inputTimeAttr, cls.outputTXAttr )         
        cls.attributeAffects( cls.input1Attr   , cls.outputTXAttr )           
        cls.attributeAffects( cls.input3Attr   , cls.outputTXAttr )
        cls.attributeAffects( cls.input8Attr   , cls.outputTXAttr )       
        cls.attributeAffects( cls.input9Attr   , cls.outputTXAttr )   
        cls.attributeAffects( cls.input10Attr  , cls.outputTXAttr ) 
        
        cls.attributeAffects( cls.inputTimeAttr, cls.outputTYAttr )         
        cls.attributeAffects( cls.input1Attr   , cls.outputTYAttr )                        
        cls.attributeAffects( cls.input3Attr   , cls.outputTYAttr )
        cls.attributeAffects( cls.input8Attr   , cls.outputTYAttr )
        cls.attributeAffects( cls.input9Attr   , cls.outputTYAttr )        
        cls.attributeAffects( cls.input10Attr  , cls.outputTYAttr )
        
        cls.attributeAffects( cls.inputTimeAttr, cls.outputTZAttr )         
        cls.attributeAffects( cls.input1Attr   , cls.outputTZAttr )                    
        cls.attributeAffects( cls.input3Attr   , cls.outputTZAttr )          
        cls.attributeAffects( cls.input8Attr   , cls.outputTZAttr )   
        cls.attributeAffects( cls.input9Attr   , cls.outputTZAttr )
        cls.attributeAffects( cls.input10Attr  , cls.outputTZAttr )
        
        cls.attributeAffects( cls.inputTimeAttr, cls.outputRXAttr )         
        cls.attributeAffects( cls.input1Attr   , cls.outputRXAttr )        
        cls.attributeAffects( cls.input3Attr   , cls.outputRXAttr )               
        cls.attributeAffects( cls.input8Attr   , cls.outputRXAttr )   
        cls.attributeAffects( cls.input9Attr   , cls.outputRXAttr ) 
        cls.attributeAffects( cls.input10Attr  , cls.outputRXAttr )
        
        cls.attributeAffects( cls.inputTimeAttr, cls.outputRYAttr )         
        cls.attributeAffects( cls.input1Attr   , cls.outputRYAttr )                       
        cls.attributeAffects( cls.input3Attr   , cls.outputRYAttr )     
        cls.attributeAffects( cls.input8Attr   , cls.outputRYAttr )   
        cls.attributeAffects( cls.input9Attr   , cls.outputRYAttr )
        cls.attributeAffects( cls.input10Attr  , cls.outputRYAttr )
        
        cls.attributeAffects( cls.inputTimeAttr, cls.outputRZAttr )         
        cls.attributeAffects( cls.input1Attr   , cls.outputRZAttr )                   
        cls.attributeAffects( cls.input3Attr   , cls.outputRZAttr )           
        cls.attributeAffects( cls.input8Attr   , cls.outputRZAttr )  
        cls.attributeAffects( cls.input9Attr   , cls.outputRZAttr )
        cls.attributeAffects( cls.input10Attr  , cls.outputRZAttr )
        
        cls.attributeAffects( cls.inputTimeAttr, cls.outputSXAttr ) 
        cls.attributeAffects( cls.input1Attr   , cls.outputSXAttr )
        cls.attributeAffects( cls.input3Attr   , cls.outputSXAttr )
        cls.attributeAffects( cls.input8Attr   , cls.outputSXAttr ) 
        cls.attributeAffects( cls.input9Attr   , cls.outputSXAttr )
        cls.attributeAffects( cls.input10Attr  , cls.outputSXAttr )
        
        cls.attributeAffects( cls.inputTimeAttr, cls.outputSYAttr ) 
        cls.attributeAffects( cls.input1Attr   , cls.outputSYAttr )  
        cls.attributeAffects( cls.input3Attr   , cls.outputSYAttr )         
        cls.attributeAffects( cls.input8Attr   , cls.outputSYAttr ) 
        cls.attributeAffects( cls.input9Attr   , cls.outputSYAttr )
        cls.attributeAffects( cls.input10Attr  , cls.outputSYAttr )
        
        cls.attributeAffects( cls.inputTimeAttr, cls.outputSZAttr ) 
        cls.attributeAffects( cls.input1Attr   , cls.outputSZAttr ) 
        cls.attributeAffects( cls.input3Attr   , cls.outputSZAttr )  
        cls.attributeAffects( cls.input8Attr   , cls.outputSZAttr )                
        cls.attributeAffects( cls.input9Attr   , cls.outputSZAttr )        
        cls.attributeAffects( cls.input10Attr  , cls.outputSZAttr )
       
        
def initializePlugin(obj):
    plugin = ommpx.MFnPlugin( obj , 'matthieuCantat', '1.0', 'Any')
    try:
        plugin.registerNode( dynamicRotation.kPluginNodeTypeName, dynamicRotation.kPluginNodeId, dynamicRotation.nodeCreator, dynamicRotation.nodeInitializer)
    except:
        raise Exception('Failed to register node: {0}'.format(dynamicRotation.kPluginNodeTypeName) )
   

def uninitializePlugin(obj):
    plugin = ommpx.MFnPlugin(obj)
    try:
        plugin.deregisterNode( dynamicRotation.kPluginNodeId )
    except:
        raise Exception('Failed to unregister node: {0}'.format(dynamicRotation.kPluginNodeTypeName) )

        
        
        
        
########################################################################################################################################################################################################        
########################################################################################################################################################################################################  PROC UTILS      
########################################################################################################################################################################################################        
        
  
def MMatrixToNum( matrix ):
    return [  matrix(0,0) , matrix(0,1) , matrix(0,2) , matrix(0,3)  ,  matrix(1,0) , matrix(1,1) , matrix(1,2) , matrix(1,3)  ,  matrix(2,0) , matrix(2,1) , matrix(2,2) , matrix(2,3) ,  matrix(3,0) , matrix(3,1) , matrix(3,2) , matrix(3,3)  ]     

    
    
def API_getMDagPath( obj ): 
    
    '''
    convert maya name into dagPath , very use to manipulate obj in API  
    '''

    selection = ompy.MSelectionList()
    selection.add( obj )
    
    dagPath= ompy.MDagPath()
    dagPath = selection.getDagPath( 0 )
    
    return dagPath    