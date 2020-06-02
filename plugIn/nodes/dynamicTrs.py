'''
#FOR TEST
import maya.cmds as mc
path = 'D:\mcantat_BDD\projects\code\maya\python\plugIn\dynamicTubeNodeOptim2.py'
mc.file( new = True , f = True )
mc.loadPlugin( path , qt = True )   
'''

import maya.OpenMaya as om
import maya.OpenMayaMPx as ommpx
import maya.cmds as mc
import time
import utilsMayaNodes as utils

import python.utils.utilsMayaApi as utilsMayaApi
import python.classe.trsBackUp as trsClass


class dynamicTrs(ommpx.MPxNode):

    kPluginNodeTypeName = 'dynamicTrs'
    kPluginNodeId = om.MTypeId(0x00033449)

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
        intime           = utils.nodeAttrToFloat(           dataBlock , self.attrInTime  )          
        activate         = utils.nodeAttrToFloat(           dataBlock , self.attrInActivate  )                 
        worldMatrix      = utils.nodeAttrToMatrixFloatList( dataBlock , self.attrInMatrix  )   
        mass             = utils.nodeAttrToFloat(           dataBlock , self.attrInMass  )            
        elasticity       = utils.nodeAttrToFloat(           dataBlock , self.attrInElasticity  ) 
        damping          = utils.nodeAttrToFloat(           dataBlock , self.attrInDamping  ) 
        collision        = utils.nodeAttrToFloat(           dataBlock , self.attrInCollision  ) 
        collisionMatrix  = utils.nodeAttrToMatrixFloatList( dataBlock , self.attrInCollisionMatrix  )        
        hitSphereSize    = utils.nodeAttrToFloat(           dataBlock , self.attrInCollisionSphereSize  )         
        fatherMatrix     = utils.nodeAttrToMatrixFloatList( dataBlock , self.attrInMatrixFather  )  
        self.nbrEval     = utils.nodeAttrToFloat(           dataBlock , self.attrInNbrEval  )         
        self.lastTime    = utils.nodeAttrToFloat(           dataBlock , self.attrInLastTime  )               
        self.lastSpeedT  = utils.nodeAttrToFloat3(          dataBlock , self.attrInLastSpeedT  )                                            
        self.lastSpeedR  = utils.nodeAttrToFloat3(          dataBlock , self.attrInLastSpeedR  )      
        self.lastSpeedS  = utils.nodeAttrToFloat3(          dataBlock , self.attrInLastSpeedS  )      
        self.slaveTValue = utils.nodeAttrToFloat3(          dataBlock , self.attrInSlaveT  )   
        self.slaveRValue = utils.nodeAttrToFloat3(          dataBlock , self.attrInSlaveR  )          
        self.slaveSValue = utils.nodeAttrToFloat3(          dataBlock , self.attrInSlaveS  )                 
        axeDirWay        = utils.nodeAttrToInt(             dataBlock , self.attrInAxeDir  )        
        
        #_____________________________________________________________________________________COMPUTE
        #_______________ DELTA TIME        
        incrEval      = 0.04
        self.nbrEval += incrEval
        
        curTime       = self.nbrEval       
        deltaTime     = curTime - self.lastTime         
        self.lastTime = curTime 
        
        #_______________ TRS  
        trsObj = trsClass.trsClass()              
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
        mc.setAttr( nodeName +'.nbrEval'  , self.nbrEval    )
        mc.setAttr( nodeName +'.lastTime' , self.lastTime   )  
        
        mc.setAttr( nodeName +'.lastSpeedT' ,  self.lastSpeedT[0] ,  self.lastSpeedT[1] ,  self.lastSpeedT[2] , type = 'double3')   
        mc.setAttr( nodeName +'.lastSpeedR' ,  self.lastSpeedR[0] ,  self.lastSpeedR[1] ,  self.lastSpeedR[2] , type = 'double3') 
        mc.setAttr( nodeName +'.lastSpeedS' ,  self.lastSpeedS[0] ,  self.lastSpeedS[1] ,  self.lastSpeedS[2] , type = 'double3') 
        
        mc.setAttr( nodeName +'.slaveTValue' , self.slaveTValue[0] , self.slaveTValue[1] , self.slaveTValue[2] , type = 'double3')  
        mc.setAttr( nodeName +'.slaveRValue' , self.slaveRValue[0] , self.slaveRValue[1] , self.slaveRValue[2] , type = 'double3')  
        mc.setAttr( nodeName +'.slaveSValue' , self.slaveSValue[0] , self.slaveSValue[1] , self.slaveSValue[2] , type = 'double3')          
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
        nData = om.MFnNumericData()
        cData = om.MFnNurbsCurveData() 
        mData = om.MFnMeshData() 

        nAttr = om.MFnNumericAttribute()  
        eAttr = om.MFnEnumAttribute()
        mAttr = om.MFnMatrixAttribute()
        gAttr = om.MFnGenericAttribute()
        tAttr = om.MFnTypedAttribute()  
    
        cls.attrInTime = nAttr.create( 'time' , 'time' , nData.kFloat  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)    
        
        cls.attrInActivate = nAttr.create('activate', 'activate' , nData.kFloat  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)

        cls.attrInMatrix = mAttr.create( 'worldMatrix' , 'worldMatrix'  , nData.kFloat  )
        mAttr.setKeyable(True)       
        mAttr.setReadable(False) 

        cls.attrInMass = nAttr.create( 'mass' , 'mass'  , nData.kFloat  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)        

        cls.attrInElasticity = nAttr.create( 'elasticity' , 'elasticity' , nData.kFloat  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)         

        cls.attrInDamping = nAttr.create( 'damping' , 'damping' , nData.kFloat  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)         

        cls.attrInCollision = nAttr.create( 'collision' , 'collision' , nData.kFloat  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)            

        cls.attrInCollisionMatrix = mAttr.create( 'collisionMatrix' , 'collisionMatrix' , nData.kFloat  )
        mAttr.setKeyable(True)       
        mAttr.setReadable(False) 

        cls.attrInCollisionSphereSize = nAttr.create('hitSphereSize', 'hitSphereSize' , nData.kFloat  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)            

        cls.attrInMatrixFather = mAttr.create('worldMatrixFather', 'worldMatrixFather' , nData.kFloat  )
        mAttr.setKeyable(True)       
        mAttr.setReadable(False)          

        cls.attrInNbrEval = nAttr.create( 'nbrEval' , 'nbrEval'  , nData.kFloat  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)  

        cls.attrInLastTime = nAttr.create( 'lastTime', 'lastTime'  , nData.kFloat  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)  

        cls.attrInLastSpeedT = nAttr.create( 'lastSpeedT', 'lastSpeedT' , nData.k3Float  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)  

        cls.attrInLastSpeedR = nAttr.create( 'lastSpeedR', 'lastSpeedR' , nData.k3Float  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False) 

        cls.attrInLastSpeedS = nAttr.create( 'lastSpeedS', 'lastSpeedS' , nData.k3Float  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)         

        cls.attrInSlaveT = nAttr.create( 'slaveTValue' , 'slaveTValue' , nData.k3Float  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)  

        cls.attrInSlaveR = nAttr.create( 'slaveRValue', 'slaveRValue' , nData.k3Float  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False) 

        cls.attrInSlaveS = nAttr.create( 'slaveSValue', 'slaveSValue' , nData.k3Float  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)         

        cls.attrInAxeDir = nAttr.create( 'axeDir', 'axeDir' , nData.kInt  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False) 
        
        #_________________________________________________ OUTPUT
        
        cls.outputTXAttr = nAttr.create('outTranslateX', 'outTranslateX', nData.kFloat )
        nAttr.setWritable(False)
        nAttr.setStorable(False)

        cls.outputTYAttr = nAttr.create('outTranslateY', 'outTranslateY', nData.kFloat )
        nAttr.setWritable(False)
        nAttr.setStorable(False)

        cls.outputTZAttr = nAttr.create('outTranslateZ', 'outTranslateZ', nData.kFloat )
        nAttr.setWritable(False)
        nAttr.setStorable(False)             

        cls.outputRXAttr = nAttr.create('outRotateX', 'outRotateX', nData.kFloat )
        nAttr.setWritable(False)
        nAttr.setStorable(False)

        cls.outputRYAttr = nAttr.create('outRotateY', 'outRotateY', nData.kFloat )
        nAttr.setWritable(False)
        nAttr.setStorable(False)

        cls.outputRZAttr = nAttr.create('outRotateZ', 'outRotateZ', nData.kFloat )
        nAttr.setWritable(False)
        nAttr.setStorable(False)    

        cls.outputSXAttr = nAttr.create('outScaleX', 'outScaleX', nData.kFloat )
        nAttr.setWritable(False)
        nAttr.setStorable(False)

        cls.outputSYAttr = nAttr.create('outScaleY', 'outScaleY', nData.kFloat )
        nAttr.setWritable(False)
        nAttr.setStorable(False)
 
        cls.outputSZAttr = nAttr.create('outScaleZ', 'outScaleZ', nData.kFloat )
        nAttr.setWritable(False)
        nAttr.setStorable(False)  


        cls.addAttribute(cls.attrInTime)  
        cls.addAttribute(cls.attrInActivate )
        cls.addAttribute(cls.attrInMatrix )          
        cls.addAttribute(cls.attrInMass ) 
        cls.addAttribute(cls.attrInElasticity ) 
        cls.addAttribute(cls.attrInDamping )    
        cls.addAttribute(cls.attrInCollision ) 
        cls.addAttribute(cls.attrInCollisionMatrix )
        cls.addAttribute(cls.attrInCollisionSphereSize )          
        cls.addAttribute(cls.attrInMatrixFather)              
        cls.addAttribute(cls.attrInNbrEval)
        cls.addAttribute(cls.attrInLastTime)        
        cls.addAttribute(cls.attrInLastSpeedT)
        cls.addAttribute(cls.attrInLastSpeedR)
        cls.addAttribute(cls.attrInLastSpeedS)        
        cls.addAttribute(cls.attrInSlaveT)
        cls.addAttribute(cls.attrInSlaveR)
        cls.addAttribute(cls.attrInSlaveS)        
        cls.addAttribute(cls.attrInAxeDir)     

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
        cls.attributeAffects( cls.attrInTime                 , cls.outputTXAttr )         
        cls.attributeAffects( cls.attrInActivate             , cls.outputTXAttr )           
        cls.attributeAffects( cls.attrInMatrix               , cls.outputTXAttr )
        cls.attributeAffects( cls.attrInCollisionMatrix      , cls.outputTXAttr )       
        cls.attributeAffects( cls.attrInCollisionSphereSize  , cls.outputTXAttr )   
        cls.attributeAffects( cls.attrInMatrixFather         , cls.outputTXAttr ) 
        
        cls.attributeAffects( cls.attrInTime                , cls.outputTYAttr )         
        cls.attributeAffects( cls.attrInActivate            , cls.outputTYAttr )                        
        cls.attributeAffects( cls.attrInMatrix              , cls.outputTYAttr )
        cls.attributeAffects( cls.attrInCollisionMatrix     , cls.outputTYAttr )
        cls.attributeAffects( cls.attrInCollisionSphereSize , cls.outputTYAttr )        
        cls.attributeAffects( cls.attrInMatrixFather        , cls.outputTYAttr )
        
        cls.attributeAffects( cls.attrInTime                , cls.outputTZAttr )         
        cls.attributeAffects( cls.attrInActivate            , cls.outputTZAttr )                    
        cls.attributeAffects( cls.attrInMatrix              , cls.outputTZAttr )          
        cls.attributeAffects( cls.attrInCollisionMatrix     , cls.outputTZAttr )   
        cls.attributeAffects( cls.attrInCollisionSphereSize , cls.outputTZAttr )
        cls.attributeAffects( cls.attrInMatrixFather        , cls.outputTZAttr )
        
        cls.attributeAffects( cls.attrInTime                , cls.outputRXAttr )         
        cls.attributeAffects( cls.attrInActivate            , cls.outputRXAttr )        
        cls.attributeAffects( cls.attrInMatrix              , cls.outputRXAttr )               
        cls.attributeAffects( cls.attrInCollisionMatrix     , cls.outputRXAttr )   
        cls.attributeAffects( cls.attrInCollisionSphereSize , cls.outputRXAttr ) 
        cls.attributeAffects( cls.attrInMatrixFather        , cls.outputRXAttr )
        
        cls.attributeAffects( cls.attrInTime                , cls.outputRYAttr )         
        cls.attributeAffects( cls.attrInActivate            , cls.outputRYAttr )                       
        cls.attributeAffects( cls.attrInMatrix              , cls.outputRYAttr )     
        cls.attributeAffects( cls.attrInCollisionMatrix     , cls.outputRYAttr )   
        cls.attributeAffects( cls.attrInCollisionSphereSize , cls.outputRYAttr )
        cls.attributeAffects( cls.attrInMatrixFather        , cls.outputRYAttr )
        
        cls.attributeAffects( cls.attrInTime                , cls.outputRZAttr )         
        cls.attributeAffects( cls.attrInActivate            , cls.outputRZAttr )                   
        cls.attributeAffects( cls.attrInMatrix              , cls.outputRZAttr )           
        cls.attributeAffects( cls.attrInCollisionMatrix     , cls.outputRZAttr )  
        cls.attributeAffects( cls.attrInCollisionSphereSize , cls.outputRZAttr )
        cls.attributeAffects( cls.attrInMatrixFather        , cls.outputRZAttr )
        
        cls.attributeAffects( cls.attrInTime                , cls.outputSXAttr ) 
        cls.attributeAffects( cls.attrInActivate            , cls.outputSXAttr )
        cls.attributeAffects( cls.attrInMatrix              , cls.outputSXAttr )
        cls.attributeAffects( cls.attrInCollisionMatrix     , cls.outputSXAttr ) 
        cls.attributeAffects( cls.attrInCollisionSphereSize , cls.outputSXAttr )
        cls.attributeAffects( cls.attrInMatrixFather        , cls.outputSXAttr )
        
        cls.attributeAffects( cls.attrInTime                , cls.outputSYAttr ) 
        cls.attributeAffects( cls.attrInActivate            , cls.outputSYAttr )  
        cls.attributeAffects( cls.attrInMatrix              , cls.outputSYAttr )         
        cls.attributeAffects( cls.attrInCollisionMatrix     , cls.outputSYAttr ) 
        cls.attributeAffects( cls.attrInCollisionSphereSize , cls.outputSYAttr )
        cls.attributeAffects( cls.attrInMatrixFather        , cls.outputSYAttr )
        
        cls.attributeAffects( cls.attrInTime                , cls.outputSZAttr ) 
        cls.attributeAffects( cls.attrInActivate            , cls.outputSZAttr ) 
        cls.attributeAffects( cls.attrInMatrix              , cls.outputSZAttr )  
        cls.attributeAffects( cls.attrInCollisionMatrix     , cls.outputSZAttr )                
        cls.attributeAffects( cls.attrInCollisionSphereSize , cls.outputSZAttr )        
        cls.attributeAffects( cls.attrInMatrixFather        , cls.outputSZAttr )
       
        
def initializePlugin(obj):
    plugin = ommpx.MFnPlugin( obj , 'matthieuCantat', '1.0', 'Any')
    try:
        plugin.registerNode( dynamicTrs.kPluginNodeTypeName, dynamicTrs.kPluginNodeId, dynamicTrs.nodeCreator, dynamicTrs.nodeInitializer)
    except:
        raise Exception('Failed to register node: {0}'.format(dynamicTrs.kPluginNodeTypeName) )
   

def uninitializePlugin(obj):
    plugin = ommpx.MFnPlugin(obj)
    try:
        plugin.deregisterNode( dynamicTrs.kPluginNodeId )
    except:
        raise Exception('Failed to unregister node: {0}'.format(dynamicTrs.kPluginNodeTypeName) )

        
        
        
        