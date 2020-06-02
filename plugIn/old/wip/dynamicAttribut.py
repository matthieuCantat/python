



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


class dynamicAttribut(ommpx.MPxNode):

    kPluginNodeTypeName = 'dynamicAttribut'
    kPluginNodeId = om.MTypeId(0x00033445)

    
    inputTimeAttr = None
    kInputTimeAttrName = 'time'
    kInputTimeAttrLongName = 'time'
    
    # IN ATTR : MAIN
    input1Attr = None
    kInput1AttrName = 'activate'
    kInput1AttrLongName = 'activate'
 
    input2Attr = None
    kInput2AttrName = 'inValue'
    kInput2AttrLongName = 'inValue'   
    
    input3Attr = None
    kInput3AttrName = 'masse'
    kInput3AttrLongName = 'masse'       

    input4Attr = None
    kInput4AttrName = 'elasticity'
    kInput4AttrLongName = 'elasticity'       

    input5Attr = None
    kInput5AttrName = 'damping'
    kInput5AttrLongName = 'damping'  

    input6Attr = None
    kInput6AttrName = 'collision'
    kInput6AttrLongName = 'collision'      
    
    input7Attr = None
    kInput7AttrName = 'min'
    kInput7AttrLongName = 'minValue'    
  
    input8Attr = None
    kInput8AttrName = 'max'
    kInput8AttrLongName = 'maxValue'    

    input9Attr = None
    kInput9AttrName = 'elasticityC'
    kInput9AttrLongName = 'elasticityCollision'    

    input10Attr = None
    kInput10AttrName = 'dampingC'
    kInput10AttrLongName = 'dampingCollision'   
    
    # IN ATTR : SAVE NEXT EVAL

    input11Attr = None
    kInput11AttrName = 'nbrEval'
    kInput11AttrLongName = 'nbrEval'      

    input12Attr = None
    kInput12AttrName = 'lastTime'
    kInput12AttrLongName = 'lastTime'      

    input13Attr = None
    kInput13AttrName = 'lastSpeed'
    kInput13AttrLongName = 'lastSpeed'       

    input14Attr = None
    kInput14AttrName = 'slaveValue'
    kInput14AttrLongName = 'slaveValue'     
    
    # OUT ATTR         
    
    output = None
    kOutputAttrName = 'outValue'
    kOutputAttrLongName = 'outValue'
    
    
    def __init__(self):
    	
		ommpx.MPxNode.__init__(self)
		self.nbrEval     = 0
		self.lastTime    = 0
		self.lastSpeed   = 0		
		self.slaveValue  = 0
		
		self.reflexionOutVector = ompy.MVector( 0 , 0 , 0 )
        
    def compute( self, plug , dataBlock ):
    
		if not ( plug == self.outputAttr ):
			return om.kUnknownParameter			
				
		#_____________________________________________________________________________________ IN	


		dataHandle     = dataBlock.inputValue( self.inputTimeAttr )
		intime         = dataHandle.asFloat()			

		dataHandle     = dataBlock.inputValue( self.input1Attr )
		activate       = dataHandle.asInt()			
		
		dataHandle     = dataBlock.inputValue( self.input2Attr )
		leadValue      = dataHandle.asFloat()	                         
                        
		dataHandle     = dataBlock.inputValue( self.input3Attr )
		mass           = dataHandle.asFloat()			
                         
		dataHandle     = dataBlock.inputValue( self.input4Attr )
		elasticity     = dataHandle.asFloat()
                        
		dataHandle     = dataBlock.inputValue( self.input5Attr )
		damping        = dataHandle.asFloat()	
		
		dataHandle     = dataBlock.inputValue( self.input6Attr )
		collision      = dataHandle.asInt()		

		dataHandle     = dataBlock.inputValue( self.input7Attr )
		minValue       = dataHandle.asFloat()			
		
		dataHandle     = dataBlock.inputValue( self.input8Attr )
		maxValue       = dataHandle.asFloat()
		
		dataHandle     = dataBlock.inputValue( self.input9Attr )
		elasticityC    = dataHandle.asFloat()			

		dataHandle     = dataBlock.inputValue( self.input10Attr )
		dampingC       = dataHandle.asFloat()	
				
		dataHandle     = dataBlock.inputValue( self.input11Attr )
		self.nbrEval   = dataHandle.asFloat()
 		
		dataHandle     = dataBlock.inputValue( self.input12Attr ) 
		self.lastTime  = dataHandle.asFloat()                    
  
		dataHandle     = dataBlock.inputValue( self.input13Attr )
		self.lastSpeed = dataHandle.asFloat()		
		
		dataHandle     = dataBlock.inputValue( self.input14Attr )			
		self.slaveValue= dataHandle.asFloat()			
	
		#_____________________________________________________________________________________COMPUTE
		
		
		leadValueClamped = leadValue
		if( collision == 1 ):
			leadValueClamped = min( max( leadValue , minValue ) , maxValue )				
		#_______________ TIME 
		
		incrEval      = 0.04
		self.nbrEval += incrEval
		
		curTime       = self.nbrEval       
		deltaTime     = curTime - self.lastTime   		
		self.lastTime = curTime
		
		#_______________ 
	
		if ( intime == 0 ) or ( activate == 0):
			
			self.nbrEval      = 0
			self.lastTime     = 0
			self.lastSpeed    = 0		
			self.slaveValue   = leadValue
			
		else:
				
			#___________first aproximation	

			if( self.slaveValue < minValue ):
				limitValue = minValue
				isCollid   = collision
			elif( maxValue < self.slaveValue ):	
				limitValue = maxValue
				isCollid   = collision
			else:
				limitValue = 0	
				isCollid   = 0	
			
			# COMPUTE acceleration		
			elasticityF   = elasticity       * ( leadValueClamped   - self.slaveValue )
			elasticityCF  = elasticityC      * ( limitValue - self.slaveValue )			
			frictionF     = damping          * self.lastSpeed  * -1 			
			frictionCF    = dampingC         * self.lastSpeed  * -1
			acceleration  =   ( elasticityF  + frictionF  ) / mass  			
			accelerationC =   ( elasticityCF + frictionCF ) / mass 

			a = acceleration * ( 1 - isCollid ) + accelerationC * isCollid
			
			# EULER APPROXIMATION
			self.lastSpeed  = self.lastSpeed      + a                 * deltaTime
			self.slaveValue = self.slaveValue     + self.lastSpeed    * deltaTime	
			# EXTRACT SLOPE	    	
			slopeA = self.lastSpeed   * deltaTime
		    
			#___________second aproximation

			
			if( self.slaveValue < minValue ):
				limitValue = minValue
				isCollid   = collision
			elif( maxValue < self.slaveValue ):	
				limitValue = maxValue
				isCollid   = collision
			else:
				limitValue = 0	
				isCollid   = 0			
			
			# COMPUTE acceleration	  
			elasticityF   = elasticity       * ( leadValueClamped   - self.slaveValue )
			elasticityCF  = elasticityC      * ( limitValue - self.slaveValue )			
			frictionF     = damping          * self.lastSpeed  * -1 			
			frictionCF    = dampingC         * self.lastSpeed  * -1
			acceleration  =   ( elasticityF  + frictionF  ) / mass  			
			accelerationC =   ( elasticityCF + frictionCF ) / mass 

			a = acceleration * ( 1 - isCollid ) + accelerationC * isCollid
			
			# EULER APPROXIMATION
			self.lastSpeed    = self.lastSpeed    + a * deltaTime
			# EXTRACT SLOPE	   
			slopeB = self.lastSpeed    * deltaTime
		    
			#___________HEUN APPROXIMATION (moyenne des 2 slope)
		    
			self.slaveValue    = self.slaveValue    + ( slopeA + slopeB )/2

	
		
        
		#_____________________________________________________________________________________ OUT

		
		
		nodeName = self.name()	
		mc.undoInfo( swf = 0 )
		mc.setAttr( nodeName +'.'+ self.kInput11AttrName  , self.nbrEval    )
		mc.setAttr( nodeName +'.'+ self.kInput12AttrName  , self.lastTime   )		
		mc.setAttr( nodeName +'.'+ self.kInput13AttrName  , self.lastSpeed  )			
		mc.setAttr( nodeName +'.'+ self.kInput14AttrName  , self.slaveValue )						
		mc.undoInfo( swf = 1 )
		
		output     = self.slaveValue 				
		dataHandle = dataBlock.outputValue( self.outputAttr )		
		dataHandle.setFloat( output )	
			
		dataBlock.setClean( plug )        		

			
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
        
        cls.input1Attr = nAttr.create(cls.kInput1AttrLongName, cls.kInput1AttrName , om.MFnNumericData.kInt  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)
 
        nAttr = om.MFnNumericAttribute()   
        
        cls.input2Attr = nAttr.create(cls.kInput2AttrLongName, cls.kInput2AttrName , om.MFnNumericData.kFloat  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)
        
        nAttr = om.MFnNumericAttribute()   
        
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
        
        cls.input6Attr = nAttr.create(cls.kInput6AttrLongName, cls.kInput6AttrName , om.MFnNumericData.kInt  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)            
        
        nAttr = om.MFnNumericAttribute()   
        
        cls.input7Attr = nAttr.create(cls.kInput7AttrLongName, cls.kInput7AttrName , om.MFnNumericData.kFloat  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False) 
        
        nAttr = om.MFnNumericAttribute()   
        
        cls.input8Attr = nAttr.create(cls.kInput8AttrLongName, cls.kInput8AttrName , om.MFnNumericData.kFloat  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False) 
        
        nAttr = om.MFnNumericAttribute()   
        
        cls.input9Attr = nAttr.create(cls.kInput9AttrLongName, cls.kInput9AttrName , om.MFnNumericData.kFloat  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)         
        
        nAttr = om.MFnNumericAttribute()   
        
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
        
        cls.input13Attr = nAttr.create(cls.kInput13AttrLongName, cls.kInput13AttrName , om.MFnNumericData.kFloat  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)  

        nAttr = om.MFnNumericAttribute()   
        
        cls.input14Attr = nAttr.create(cls.kInput14AttrLongName, cls.kInput14AttrName , om.MFnNumericData.kFloat  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)  
        
		# OUTPUT
		       
        nAttr = om.MFnNumericAttribute() 
        
        cls.outputAttr = nAttr.create(cls.kOutputAttrLongName, cls.kOutputAttrName, om.MFnNumericData.kFloat )
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
        
        cls.addAttribute(cls.outputAttr )

        cls.attributeAffects( cls.input1Attr   , cls.outputAttr )        
        cls.attributeAffects( cls.input2Attr   , cls.outputAttr )
        cls.attributeAffects( cls.inputTimeAttr, cls.outputAttr )       
       
        
def initializePlugin(obj):
    plugin = ommpx.MFnPlugin( obj , 'matthieuCantat', '1.0', 'Any')
    try:
        plugin.registerNode( dynamicAttribut.kPluginNodeTypeName, dynamicAttribut.kPluginNodeId, dynamicAttribut.nodeCreator, dynamicAttribut.nodeInitializer)
    except:
        raise Exception('Failed to register node: {0}'.format(dynamicAttribut.kPluginNodeTypeName) )
   

def uninitializePlugin(obj):
    plugin = ommpx.MFnPlugin(obj)
    try:
        plugin.deregisterNode( dynamicAttribut.kPluginNodeId )
    except:
        raise Exception('Failed to unregister node: {0}'.format(dynamicAttribut.kPluginNodeTypeName) )

        
        
        
        
########################################################################################################################################################################################################        
########################################################################################################################################################################################################  PROC UTILS      
########################################################################################################################################################################################################        
        
      
        
        
        
        