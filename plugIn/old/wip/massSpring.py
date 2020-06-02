



import sys
import math
import time
import maya.OpenMaya as om
import maya.api.OpenMaya as ompy
import maya.OpenMayaMPx as ommpx
import maya.cmds as mc




class massSpringNode(ommpx.MPxNode):

    kPluginNodeTypeName = 'massSpringNode'
    kPluginNodeId = om.MTypeId(0x00033445)

    
    inputTimeAttr = None
    kInputTimeAttrName = 'time'
    kInputTimeAttrLongName = 'time'
    
    # IN ATTR : MAIN
    input1Attr = None
    kInput1AttrName = 'pos'
    kInput1AttrLongName = 'position'
 
    input2Attr = None
    kInput2AttrName = 'activate'
    kInput2AttrLongName = 'activate'   
    
    input3Attr = None
    kInput3AttrName = 'masse'
    kInput3AttrLongName = 'masse'       

    input4Attr = None
    kInput4AttrName = 'elasticity'
    kInput4AttrLongName = 'elasticity'       

    input5Attr = None
    kInput5AttrName = 'damping'
    kInput5AttrLongName = 'damping'  

    # IN ATTR : SAVE NEXT EVAL

    input6Attr = None
    kInput6AttrName = 'nbrEval'
    kInput6AttrLongName = 'nbrEval'      

    input7Attr = None
    kInput7AttrName = 'lastTime'
    kInput7AttrLongName = 'lastTime'      

    input8Attr = None
    kInput8AttrName = 'lastSpeed'
    kInput8AttrLongName = 'lastSpeed'       

    input9Attr = None
    kInput9AttrName = 'slavePos'
    kInput9AttrLongName = 'slavePos'     
    
    # OUT ATTR         
    
    output = None
    kOutputAttrName = 'outPos'
    kOutputAttrLongName = 'outPosition'
    
    
    def __init__(self):
    	
		ommpx.MPxNode.__init__(self)
		self.nbrEval   = 0
		self.lastTime  = 0
		self.lastSpeed = [0,0,0]		
		self.slavePos  = [0,0,0]
        
    def compute( self, plug , dataBlock ):
    
		if not ( plug == self.outputAttr ):
			return om.kUnknownParameter			
				
		#_____________________________________________________________________________________ IN	

		dataHandle     = dataBlock.inputValue( self.inputTimeAttr )
		intime         = dataHandle.asFloat()			
             
		dataHandle     = dataBlock.inputValue( self.input1Attr )
		pos            = dataHandle.asFloat3()	
                          
		dataHandle     = dataBlock.inputValue( self.input2Attr )
		activate       = dataHandle.asInt()	
                        
		dataHandle     = dataBlock.inputValue( self.input3Attr )
		mass           = dataHandle.asFloat()			
                         
		dataHandle     = dataBlock.inputValue( self.input4Attr )
		elasticity     = dataHandle.asFloat()
                        
		dataHandle     = dataBlock.inputValue( self.input5Attr )
		damping        = dataHandle.asFloat()
                        
		dataHandle     = dataBlock.inputValue( self.input6Attr )
		self.nbrEval   = dataHandle.asFloat()
 		
		dataHandle     = dataBlock.inputValue( self.input7Attr ) 
		self.lastTime  = dataHandle.asFloat()                    
  
		dataHandle     = dataBlock.inputValue( self.input8Attr )
		self.lastSpeed = dataHandle.asFloat3()		
		self.lastSpeed = [ self.lastSpeed[0] , self.lastSpeed[1] , self.lastSpeed[2] ]
		
		dataHandle     = dataBlock.inputValue( self.input9Attr )			
		self.slavePos  = dataHandle.asFloat3()	
		self.slavePos = [ self.slavePos[0] , self.slavePos[1] , self.slavePos[2] ]			
	
		#_____________________________________________________________________________________COMPUTE

		#_______________ TIME EVAL
		
		incrEval      = 0.04
		self.nbrEval += incrEval

		#_______________ INPUT
		
		curTime       = self.nbrEval       
		deltaTime     = curTime - self.lastTime   		
		self.lastTime = curTime
				
		#_______________ INIT CONDITION
		
		target = [ pos[0] - self.slavePos[0] , pos[1] - self.slavePos[1]  , pos[2] - self.slavePos[2]  ]

		if ( intime == 0 ) or ( activate == 0):
			
			self.nbrEval   = 0
			self.lastTime  = 0
			self.lastSpeed = [0,0,0]		
			target         = [0,0,0] 
			self.slavePos  = pos
			
		else:
		
			for i in range( 0 , 3 ):
				
				#___________first aproximation	
				
				# COMPUTE acceleration
				a = ( elasticity * target[i]  - damping * self.lastSpeed[i] ) / mass 
				# EULER APPROXIMATION
				self.lastSpeed[i] = self.lastSpeed[i] + a                 * deltaTime
				self.slavePos[i]  = self.slavePos[i]  + self.lastSpeed[i] * deltaTime	
				# EXTRACT SLOPE	    	
				slopeA = self.lastSpeed[i] * deltaTime
		    	
				#___________second aproximation
				
				# COMPUTE acceleration	  
				target[i] =  pos[i] - self.slavePos[i]
				a = ( elasticity * target[i]  - damping * self.lastSpeed[i] )/  mass 
				# EULER APPROXIMATION
				self.lastSpeed[i] = self.lastSpeed[i] + a * deltaTime
				# EXTRACT SLOPE	   
				slopeB = self.lastSpeed[i] * deltaTime
		    	
				#___________HEUN APPROXIMATION (moyenne des 2 slope)
		    	
				self.slavePos[i] = self.slavePos[i] + ( slopeA + slopeB )/2

		#_____________________________________________________________________________________ OUT
	
		nodeName = self.name()		
		mc.setAttr( nodeName +'.'+ self.kInput6AttrName  , self.nbrEval     )
		mc.setAttr( nodeName +'.'+ self.kInput7AttrName  , self.lastTime   )		
		mc.setAttr( nodeName +'.'+ self.kInput8AttrName  , self.lastSpeed[0] , self.lastSpeed[1] , self.lastSpeed[2]  ,type = 'float3' )			
		mc.setAttr( nodeName +'.'+ self.kInput9AttrName  , self.slavePos[0]  , self.slavePos[1]  , self.slavePos[2]   ,type = 'float3' )						
				
		output = self.slavePos 				
		dataHandle = dataBlock.outputValue( self.outputAttr )		
		dataHandle.set3Float(output[0] , output[1] , output[2] )	
			
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
        
        cls.input1Attr = nAttr.create(cls.kInput1AttrLongName, cls.kInput1AttrName , om.MFnNumericData.k3Float  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)
 
        nAttr = om.MFnNumericAttribute()   
        
        cls.input2Attr = nAttr.create(cls.kInput2AttrLongName, cls.kInput2AttrName , om.MFnNumericData.kInt  )
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
        
        cls.input6Attr = nAttr.create(cls.kInput6AttrLongName, cls.kInput6AttrName , om.MFnNumericData.kFloat  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)            
        
        nAttr = om.MFnNumericAttribute()   
        
        cls.input7Attr = nAttr.create(cls.kInput7AttrLongName, cls.kInput7AttrName , om.MFnNumericData.kFloat  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False) 
        
        nAttr = om.MFnNumericAttribute()   
        
        cls.input8Attr = nAttr.create(cls.kInput8AttrLongName, cls.kInput8AttrName , om.MFnNumericData.k3Float  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False) 
        
        nAttr = om.MFnNumericAttribute()   
        
        cls.input9Attr = nAttr.create(cls.kInput9AttrLongName, cls.kInput9AttrName , om.MFnNumericData.k3Float  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)         
        
    
		# OUTPUT
		       
        nAttr = om.MFnNumericAttribute() 
        
        cls.outputAttr = nAttr.create(cls.kOutputAttrLongName, cls.kOutputAttrName, om.MFnNumericData.k3Float )
        nAttr.setWritable(False)
        nAttr.setStorable(False)

 
        
        cls.addAttribute(cls.inputTimeAttr)  
        cls.addAttribute(cls.input1Attr)
        cls.addAttribute(cls.input2Attr) 
        cls.addAttribute(cls.input3Attr) 
        cls.addAttribute(cls.input4Attr) 
        cls.addAttribute(cls.input5Attr) 
        cls.addAttribute(cls.input6Attr) 
        cls.addAttribute(cls.input7Attr) 
        cls.addAttribute(cls.input8Attr)
        cls.addAttribute(cls.input9Attr)
                
        cls.addAttribute(cls.outputAttr )
        
        cls.attributeAffects( cls.input1Attr   , cls.outputAttr )
        cls.attributeAffects( cls.inputTimeAttr, cls.outputAttr )       
       
        
def initializePlugin(obj):
    plugin = ommpx.MFnPlugin( obj , 'matthieuCantat', '1.0', 'Any')
    try:
        plugin.registerNode( massSpringNode.kPluginNodeTypeName, massSpringNode.kPluginNodeId, massSpringNode.nodeCreator, massSpringNode.nodeInitializer)
    except:
        raise Exception('Failed to register node: {0}'.format(massSpringNode.kPluginNodeTypeName) )
   

def uninitializePlugin(obj):
    plugin = ommpx.MFnPlugin(obj)
    try:
        plugin.deregisterNode( massSpringNode.kPluginNodeId )
    except:
        raise Exception('Failed to unregister node: {0}'.format(massSpringNode.kPluginNodeTypeName) )
