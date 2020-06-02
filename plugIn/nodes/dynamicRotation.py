



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
import python.classe.trsBackUp as trsClass


class dynamicRotation(ommpx.MPxNode):

    kPluginNodeTypeName = 'dynamicRotation'
    kPluginNodeId = om.MTypeId(0x00033447)
    
    def __init__(self):
        
        ommpx.MPxNode.__init__(self)
        self.nbrEval       = 0
        self.lastTime      = 0
        self.lastSpeed     = 0      
        self.slaveValue    = 0
        self.minRotValues  = [-1000,-1000,-1000]
        self.maxRotValues  = [1000,1000,1000]
        self.leadCollision = None
        
        self.reflexionOutVector = ompy.MVector( 0 , 0 , 0 )
        
    def compute( self, plug , dataBlock ):
      
    	outsAttr = [ self.outputXAttr , self.outputYAttr , self.outputZAttr  ]                    
        if not ( plug in outsAttr ):
            return om.kUnknownParameter                    
        #_____________________________________________________________________________________ IN   


        dataHandle     = dataBlock.inputValue( self.inputTimeAttr )
        intime         = dataHandle.asFloat()           

        dataHandle     = dataBlock.inputValue( self.input1Attr )
        activate       = dataHandle.asFloat()         
        
        dataHandle       = dataBlock.inputValue( self.input2Attr )
        leadMFloatMatrix = dataHandle.asFloatMatrix()
        leadMatrix       = MMatrixToNum(leadMFloatMatrix) 

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

        dataHandle        = dataBlock.inputValue( self.input8Attr )
        self.minRotValues = dataHandle.asFloat3()           
        self.minRotValues = [ self.minRotValues[0] , self.minRotValues[1] , self.minRotValues[2] ]          
        
        dataHandle        = dataBlock.inputValue( self.input9Attr )
        self.maxRotValues = dataHandle.asFloat3() 
        self.maxRotValues = [ self.maxRotValues[0] , self.maxRotValues[1] , self.maxRotValues[2] ]  
        
        dataHandle     = dataBlock.inputValue( self.input10Attr )           
        distance       = dataHandle.asFloat()           
                
        dataHandle     = dataBlock.inputValue( self.input11Attr )
        self.nbrEval   = dataHandle.asFloat()
        
        dataHandle     = dataBlock.inputValue( self.input12Attr ) 
        self.lastTime  = dataHandle.asFloat()                    
  
        dataHandle     = dataBlock.inputValue( self.input13Attr )
        self.lastSpeed = dataHandle.asFloat3()
        self.lastSpeed = [ self.lastSpeed[0] , self.lastSpeed[1] , self.lastSpeed[2] ]      
        
        dataHandle     = dataBlock.inputValue( self.input14Attr )           
        self.slaveValue= dataHandle.asFloat3()          
        self.slaveValue= [ self.slaveValue[0] , self.slaveValue[1] , self.slaveValue[2] ]             
        
        dataHandle     = dataBlock.inputValue( self.input15Attr )           
        axeDirWay      = dataHandle.asInt()  
        
        dataHandle     = dataBlock.inputValue( self.input16Attr )
        ctrlTranslate  = dataHandle.asFloat3()           
        
        dataHandle     = dataBlock.inputValue( self.input17Attr )
        ctrlRotate     = dataHandle.asFloat3()  

        dataHandle     = dataBlock.inputValue( self.input18Attr )
        ctrlScale      = dataHandle.asFloat3()  
        
        dataHandle     = dataBlock.inputValue( self.input19Attr )
        follow         = dataHandle.asFloat()             
        
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
        origTrsWorld  = trsObj.createFromFloatMatrix( worldMatrix ) 
        
        ctrlTrsLocal  = [ ctrlTranslate[0] , ctrlTranslate[1] , ctrlTranslate[2] , ctrlRotate[0] , ctrlRotate[1] , ctrlRotate[2] , ctrlScale[0] , ctrlScale[1] , ctrlScale[2] ]
        ctrlTrsWorld  = trsObj.unParent( origTrsWorld , inTrsValue = ctrlTrsLocal  ) 
        
        ctrlTrsLocalClamped = ctrlTrsLocal[:]
        if not( collision == 0 ):
            for i in range(0,3):
                if not( i == axeDir ):
                    ctrlTrsLocalClamped[i+3] = max( min( ctrlTrsLocal[i+3] , self.maxRotValues[i] ), self.minRotValues[i] )        
                    
        ctrlTrsWorldClamped = trsObj.unParent( origTrsWorld , inTrsValue = ctrlTrsLocalClamped )

        offsetTrsBase         = [0,0,0,0,0,0,1,1,1]
        offsetTrsBase[axeDir] = distance * signDir           
        ctrlOffsetTrs         = trsObj.offsetItself( offsetTrsBase , inTrsValue = ctrlTrsWorldClamped  )  
        
        #_______________ DYNAMIC       
        curentFrame   = mc.currentTime( query = True )
        startFrame    = mc.playbackOptions( query = True , minTime = True )

        if( activate == 0 ) or ( curentFrame == startFrame ):
            
            self.nbrEval        = 0
            self.lastTime       = 0
            self.lastSpeed      = [ 0 , 0 , 0 ]       
            self.slaveValue     = ctrlOffsetTrs[0:3]
            self.leadCollision  = None 
            angleOut = self.angleCompute( axeDirWay , ctrlTrsWorld , ctrlOffsetTrs , self.slaveValue )
            
        else: 
                        
            # DYNAMIC
            for i in range( 0 , 3 ):
                self.slaveValue[i] , self.lastSpeed[i] = self.computeDynamic( ctrlOffsetTrs[i] , self.slaveValue[i] , self.lastSpeed[i] , mass , elasticity , damping , deltaTime )         

            # FOLLOW SYS                       
            if not( follow == 0 ):
                vToTarget       = ompy.MVector( self.slaveValue[0] - ctrlTrsWorldClamped[0] , self.slaveValue[1] - ctrlTrsWorldClamped[1] , self.slaveValue[2] - ctrlTrsWorldClamped[2] )               
                vFollow         = vToTarget * ( distance / vToTarget.length() )
                self.slaveValue = [ ctrlTrsWorldClamped[0] + vFollow.x , ctrlTrsWorldClamped[1] + vFollow.y , ctrlTrsWorldClamped[2] + vFollow.z ]
                
            # COLLISION           
            allAxesLimites    = [ [ 0 ,  2 , 1 ] , [ 2 , 1 ,  0 ] , [  1 , 0 , 2 ] ] 
            axeLimites        = allAxesLimites[axeDir]           
           
            if not( collision == 0 ):
                                    
                ctrlTrsWorldOrigOrient = ctrlTrsWorld[0:3] + origTrsWorld[3:6] + ctrlTrsWorld[6:9]              
                origOffsetTrs          = trsObj.offsetItself( offsetTrsBase , inTrsValue = ctrlTrsWorldOrigOrient   )               
                angleOutCollision      = self.angleCompute( axeDirWay , ctrlTrsWorldOrigOrient , origOffsetTrs , self.slaveValue+[0,0,0,1,1,1] )
                                
                # RECOMPUTE NEXT DYN:   slaveValue   lastSpeed 
                                        
                for i in range(0,3):
                    
                    if( i == axeDir ):
                        continue
                    
                    if( self.minRotValues[i] == 0 ) and ( self.maxRotValues[i] == 0 ):
                        planeCoords     = trsObj.toPlaneCoords( axeNormal = axeLimites[i] , inTrsValue = ctrlTrsWorldOrigOrient )
                        self.slaveValue = trsObj.snapOnPlane( planeCoords , inTrsValue = self.slaveValue+[0,0,0,1,1,1] )   
                        continue
                        
                    if( angleOutCollision[i] < self.minRotValues[i] ) or ( self.maxRotValues[i] < angleOutCollision[i] ):
                                         
                        if( angleOutCollision[i] < self.minRotValues[i] ):
                            limitRotValue = self.minRotValues 
                        elif( self.maxRotValues[i] < angleOutCollision[i] ):
                            limitRotValue = self.maxRotValues         
                                                
                        # plane coord corresponding to the limit
                
                        offsetTrsBase      = [0,0,0,0,0,0,1,1,1]
                        offsetTrsBase[i+3] = limitRotValue[i]                      
                        trsObj.offsetItself( offsetTrsBase , inTrsValue = ctrlTrsWorldOrigOrient  ) 
                        planeCoords      = trsObj.toPlaneCoords( axeNormal = axeLimites[i] )
                       
                        #slaveValue                               
                        self.slaveValue   = trsObj.snapOnPlane( planeCoords , inTrsValue = self.slaveValue+[0,0,0,1,1,1] )   
                        
                        #lastSpeed                       
                        mVectorA      = ompy.MVector( planeCoords[1][0] - planeCoords[0][0]  , planeCoords[1][1] - planeCoords[0][1]  , planeCoords[1][2] - planeCoords[0][2]  )
                        mVectorB      = ompy.MVector( planeCoords[2][0] - planeCoords[0][0]  , planeCoords[2][1] - planeCoords[0][1]  , planeCoords[2][2] - planeCoords[0][2]  )
                        mVectorMoyen  = ompy.MVector( origOffsetTrs[0]  - self.slaveValue[0] , origOffsetTrs[1]  - self.slaveValue[1] , origOffsetTrs[2]  - self.slaveValue[2] )
                        mVectorNormal = utilsMayaApi.get2VectorsNormal( mVectorA , mVectorB , mVectorMoyen )
                        
                        mlastSpeed    = ompy.MVector( self.lastSpeed[0] , self.lastSpeed[1] , self.lastSpeed[2] )                          
                                               
                        if( mVectorNormal * mlastSpeed < 0 ):
                            self.lastSpeed = self.getReflectVector( self.lastSpeed , planeCoords , collision )
                                          
               

            # OUT ANGLE  
            angleOut = self.angleCompute( axeDirWay , ctrlTrsWorld , ctrlOffsetTrs , self.slaveValue ) 
            
            angleOut = [ activate * angleOut[0] , activate * angleOut[1] , activate * angleOut[2] ]
            

        
        #_____________________________________________________________________________________ OUT

        
        
        nodeName = self.name()  
        mc.undoInfo( swf = 0 )
        mc.setAttr( nodeName +'.nbrEval'    , self.nbrEval    )
        mc.setAttr( nodeName +'.lastTime'   , self.lastTime   )       
        mc.setAttr( nodeName +'.lastSpeed'  ,  self.lastSpeed[0] ,  self.lastSpeed[1] ,  self.lastSpeed[2] , type = 'double3')            
        mc.setAttr( nodeName +'.slaveValue' , self.slaveValue[0] , self.slaveValue[1] , self.slaveValue[2] , type = 'double3')                        
        mc.undoInfo( swf = 1 )
    
        output     = angleOut[0]               
        dataHandle = dataBlock.outputValue( self.outputXAttr )       
        dataHandle.setFloat( output )
        
        output     = angleOut[1]               
        dataHandle = dataBlock.outputValue( self.outputYAttr )       
        dataHandle.setFloat( output )

        output     = angleOut[2]           
        dataHandle = dataBlock.outputValue( self.outputZAttr )      
        dataHandle.setFloat( output )

        
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
        
  
    #___________________________________________________________________________________________________________________________________________________________________________________  getMinMaxTranslateValues
    
    def getlimiteTranslateValue( self , axeDir , limiteRotValues , origTrsWorld , targetTrs ):

        # axe dir 
        signDir = 1
        if( 2 < axeDir ):
            signDir = -1
            axeDir -= 3         
        
        # axe dir       
        
        trsObj   = trsClass.trsClass()        
        distance = trsObj.toDistance( targetTrs , inTrsValue = origTrsWorld ) 
        
        # CONVERT TO ROT LIMIT
        limitRot = []      
        for i in range(0,3):
            rotationValue    = [0,0,0]
            rotationValue[i] = limiteRotValues[i]
            limitRot.append( rotationValue )       
        
        # CONVERT ROT TO TRANSLATE LIMIT        
        axeLimites = [ 0 , 2 , 1 ]
        
        limitCoords = [0,0,0]
        offsetTrsRotate    = [0,0,0,0,0,0,1,1,1]
        offsetTrsTranslate = [0,0,0,0,0,0,1,1,1]
        offsetTrsTranslate[axeDir] = distance * signDir
        
        for i in range( 0 , 3 ):
            offsetTrsRotate[3:6] = limitRot[i]
            trsObj.offsetItself( offsetTrsRotate , inTrsValue = origTrsWorld )
            trsObj.offsetItself( offsetTrsTranslate )            
            limitCoords[i] = ( trsObj.value[0:3] )   

        return limitCoords
        
    
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
        
    #___________________________________________________________________________________________________________________________________________________________________________________  angleCompute  
    
    def angleCompute( self , axeDir , oTrs , baseTrs , trs ):       

        axeDirSkip = [ [ 0 , 1 , 1 ] , [ 1 , 0 , 1 ] , [ 1 , 1 , 0 ]  ] 
        # vINIT
        
        way = 1
        if( 2 < axeDir ):
            axeDir -= 3
            way     = -1
        
        vBaseInitValue         = [0,0,0]
        vBaseInitValue[axeDir] = way
        vBaseInit   = ompy.MVector( vBaseInitValue[0]    ,  vBaseInitValue[1]    , vBaseInitValue[2]     )  
        
        # INVERSE ROTATION ORIGINE  
        eulerInit   = ompy.MEulerRotation( math.radians(oTrs[3]) , math.radians(oTrs[4]) , math.radians(oTrs[5]) )
        eulerInit.invertIt()        

        # vTARGET           
        vTarget   = ompy.MVector( trs[0]     - oTrs[0] ,  trs[1]     - oTrs[1] , trs[2]     - oTrs[2]  )        
        vTarget   = vTarget.rotateBy(eulerInit)

        # ANGLE BASE TARGET 
        rotQuat = ompy.MQuaternion( vBaseInit , vTarget )
        rotEuler = rotQuat.asEulerRotation()

        # ANGLE SKIP AXE        
        angleOut = [ rotEuler.x * axeDirSkip[axeDir][0] , rotEuler.y * axeDirSkip[axeDir][1] , rotEuler.z * axeDirSkip[axeDir][2]  ]
        
        # ANGLE OUT     
        angleOut = [ math.degrees(angleOut[0]) , math.degrees(angleOut[1]) , math.degrees(angleOut[2]) ]
        
        return angleOut             
        
        
    @classmethod
    def nodeCreator(cls):
        return ommpx.asMPxPtr(cls())


    @classmethod
    def nodeInitializer(cls):

        nAttr = om.MFnNumericAttribute()   
        
        cls.inputTimeAttr = nAttr.create( 'time' , 'time' , om.MFnNumericData.kFloat  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)    
        
        nAttr = om.MFnNumericAttribute()   
        
        cls.input1Attr = nAttr.create( 'activate' , 'activate' , om.MFnNumericData.kFloat  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)
 
        nAttr = om.MFnMatrixAttribute() 
        
        cls.input2Attr = nAttr.create( 'inMatrix' , 'inMatrix' , om.MFnNumericData.kFloat  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)
        
        nAttr = om.MFnMatrixAttribute() 
        
        cls.input3Attr = nAttr.create( 'worldMatrix',  'worldMatrix' , om.MFnNumericData.kFloat  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False) 
        
        nAttr = om.MFnNumericAttribute()   
        
        cls.input4Attr = nAttr.create( 'mass' , 'mass' , om.MFnNumericData.kFloat  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)        
        
        nAttr = om.MFnNumericAttribute()   
        
        cls.input5Attr = nAttr.create( 'elasticity' , 'elasticity' , om.MFnNumericData.kFloat  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)         
        
        nAttr = om.MFnNumericAttribute()   
        
        cls.input6Attr = nAttr.create( 'damping' , 'damping' , om.MFnNumericData.kFloat  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)         
       
        nAttr = om.MFnNumericAttribute()   
        
        cls.input7Attr = nAttr.create( 'collision' , 'collision' , om.MFnNumericData.kFloat  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)            
        
        nAttr = om.MFnNumericAttribute()   
        
        cls.input8Attr = nAttr.create( 'minValues' , 'minValues' , om.MFnNumericData.k3Float  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False) 
        
        nAttr = om.MFnNumericAttribute()   
        
        cls.input9Attr = nAttr.create( 'maxValues' , 'maxValues' , om.MFnNumericData.k3Float  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)   
        
        nAttr = om.MFnNumericAttribute()   
        
        cls.input10Attr = nAttr.create( 'distance' , 'distance' , om.MFnNumericData.kFloat  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)          

        nAttr = om.MFnNumericAttribute()   
        
        cls.input11Attr = nAttr.create( 'nbrEval' , 'nbrEval' , om.MFnNumericData.kFloat  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)  
        
        nAttr = om.MFnNumericAttribute()   
        
        cls.input12Attr = nAttr.create( 'lastTime' , 'lastTime' , om.MFnNumericData.kFloat  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)  


        nAttr = om.MFnNumericAttribute()   
        
        cls.input13Attr = nAttr.create( 'lastSpeed' , 'lastSpeed' , om.MFnNumericData.k3Float  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)  

        nAttr = om.MFnNumericAttribute()   
        
        cls.input14Attr = nAttr.create( 'slaveValue' , 'slaveValue' , om.MFnNumericData.k3Float  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)  
           
        nAttr = om.MFnNumericAttribute()   
        
        cls.input15Attr = nAttr.create( 'axeDir' , 'axeDir' , om.MFnNumericData.kInt  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False) 

        nAttr = om.MFnNumericAttribute()   
        
        cls.input16Attr = nAttr.create( 'ctrlTranslate' , 'ctrlTranslate' , om.MFnNumericData.k3Float  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False) 

        nAttr = om.MFnNumericAttribute()   
        
        cls.input17Attr = nAttr.create( 'ctrlRotate' , 'ctrlRotate' , om.MFnNumericData.k3Float  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False) 

        nAttr = om.MFnNumericAttribute()   
        
        cls.input18Attr = nAttr.create( 'ctrlScale' , 'ctrlScale' , om.MFnNumericData.k3Float  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)         

        nAttr = om.MFnNumericAttribute()   
        
        cls.input19Attr = nAttr.create( 'follow' , 'follow' , om.MFnNumericData.kFloat  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)    
        
        # OUTPUT
               
        nAttr = om.MFnNumericAttribute() 
        
        cls.outputXAttr = nAttr.create( 'outRotationX' , 'outRotationX' , om.MFnNumericData.kFloat )
        nAttr.setWritable(False)
        nAttr.setStorable(False)
        
        nAttr = om.MFnNumericAttribute() 
        
        cls.outputYAttr = nAttr.create( 'outRotationY' , 'outRotationY' , om.MFnNumericData.kFloat )
        nAttr.setWritable(False)
        nAttr.setStorable(False)
        
        nAttr = om.MFnNumericAttribute() 
        
        cls.outputZAttr = nAttr.create( 'outRotationZ' , 'outRotationZ', om.MFnNumericData.kFloat )
        nAttr.setWritable(False)
        nAttr.setStorable(False)             
        
        cls.addAttribute(cls.inputTimeAttr)  
        cls.addAttribute(cls.input1Attr )
        cls.addAttribute(cls.input2Attr )
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
        cls.addAttribute(cls.input13Attr)
        cls.addAttribute(cls.input14Attr)
        cls.addAttribute(cls.input15Attr)
        cls.addAttribute(cls.input16Attr)
        cls.addAttribute(cls.input17Attr)
        cls.addAttribute(cls.input18Attr)
        cls.addAttribute(cls.input19Attr )         
        
        cls.addAttribute(cls.outputXAttr )
        cls.addAttribute(cls.outputYAttr )     
        cls.addAttribute(cls.outputZAttr ) 
        
        cls.attributeAffects( cls.inputTimeAttr, cls.outputXAttr )         
        cls.attributeAffects( cls.input1Attr   , cls.outputXAttr )
        cls.attributeAffects( cls.input16Attr  , cls.outputXAttr )
        cls.attributeAffects( cls.input17Attr  , cls.outputXAttr )
        cls.attributeAffects( cls.input18Attr  , cls.outputXAttr )           
        cls.attributeAffects( cls.input3Attr   , cls.outputXAttr )
        cls.attributeAffects( cls.input8Attr   , cls.outputXAttr ) 
        cls.attributeAffects( cls.input9Attr   , cls.outputXAttr )                

        cls.attributeAffects( cls.inputTimeAttr, cls.outputYAttr )         
        cls.attributeAffects( cls.input1Attr   , cls.outputYAttr )        
        cls.attributeAffects( cls.input16Attr  , cls.outputYAttr )
        cls.attributeAffects( cls.input17Attr  , cls.outputYAttr )
        cls.attributeAffects( cls.input18Attr  , cls.outputYAttr )                
        cls.attributeAffects( cls.input3Attr   , cls.outputYAttr )  
        cls.attributeAffects( cls.input8Attr   , cls.outputYAttr ) 
        cls.attributeAffects( cls.input9Attr   , cls.outputYAttr )    
        
        cls.attributeAffects( cls.inputTimeAttr, cls.outputZAttr )         
        cls.attributeAffects( cls.input1Attr   , cls.outputZAttr )     
        cls.attributeAffects( cls.input16Attr  , cls.outputZAttr )
        cls.attributeAffects( cls.input17Attr  , cls.outputZAttr )
        cls.attributeAffects( cls.input18Attr  , cls.outputZAttr )               
        cls.attributeAffects( cls.input3Attr   , cls.outputZAttr ) 
        cls.attributeAffects( cls.input8Attr   , cls.outputZAttr ) 
        cls.attributeAffects( cls.input9Attr   , cls.outputZAttr )

        
        cls.attributeAffects( cls.input2Attr   , cls.outputXAttr )           
        cls.attributeAffects( cls.input2Attr   , cls.outputYAttr )           
        cls.attributeAffects( cls.input2Attr   , cls.outputZAttr )           
        
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
    