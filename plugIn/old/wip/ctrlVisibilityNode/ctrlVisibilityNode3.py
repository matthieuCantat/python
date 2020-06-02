'''
version 1 trop lourd, 

version 2 les slaves ne bouge pas , trop lourd

version 3 les slaves ne bouge pas + un node par slaves



'''



import sys
import math
import time
import maya.OpenMaya as om
import maya.api.OpenMaya as ompy
import maya.OpenMayaMPx as ommpx


def MMatrixToNum( matrix ):
	return [  matrix(0,0) , matrix(0,1) , matrix(0,2) , matrix(0,3)  ,  matrix(1,0) , matrix(1,1) , matrix(1,2) , matrix(1,3)  ,  matrix(2,0) , matrix(2,1) , matrix(2,2) , matrix(2,3) ,  matrix(3,0) , matrix(3,1) , matrix(3,2) , matrix(3,3)  ]   	


def floatMMatrixToMMatrix_(fm):
	mat = om.MMatrix()
	om.MScriptUtil.createMatrixFromList ([
		fm(0,0),fm(0, 1),fm(0, 2),fm(0, 3),
		fm(1,0),fm(1, 1),fm(1, 2),fm(1, 3),
		fm(2,0),fm(2, 1),fm(2, 2),fm(2, 3),
		fm(3,0),fm(3, 1),fm(3, 2),fm(3, 3)], mat)
	return mat

    
def convertMMatrixToTSRValue( matrixValues ):


	mtransChildren = ompy.MTransformationMatrix( ompy.MMatrix(matrixValues) )

	translate = mtransChildren.translation( ompy.MSpace.kWorld) 
	rotate    = mtransChildren.rotationComponents()
	scale     = mtransChildren.scale( ompy.MSpace.kWorld)
 	
	childrenTRSValue = [ translate[0] , translate[1] , translate[2] , math.degrees(rotate[0]) , math.degrees(rotate[1]) , math.degrees(rotate[2]) , scale[0] , scale[1] , scale[2] ]	

	return childrenTRSValue
			
	

class ctrlVisibilityNode(ommpx.MPxNode):

    kPluginNodeTypeName = 'ctrlVisibilityNode'
    kPluginNodeId = om.MTypeId(0x00033445)
    
    input1Attr = None
    kInput1AttrName = 'inSM'
    kInput1AttrLongName = 'inputSlavesMatrix'
        
    input2Attr = None
    kInput2AttrName = 'inSBBm'
    kInput2AttrLongName = 'inputSlavesBBMatrix'
  
    input3Attr = None
    kInput3AttrName = 'inM'
    kInput3AttrLongName = 'inputMasterMatrix'

    input4Attr = None
    kInput4AttrName = 'inMBB'
    kInput4AttrLongName = 'inputMasterBBmatrix'    
    
    output = None
    kOutputAttrName = 'out'
    kOutputAttrLongName = 'outputSlavesBool'
    
    
    def __init__(self):
        ommpx.MPxNode.__init__(self)

        
        

		
	#_______________________________________________________________________________________________________________________________________________________________________ compute
        
    def compute( self, plug , dataBlock ):
    
		if not ( plug == self.outputAttr ):
			return om.kUnknownParameter			
				
		#_____________________________________________________________________________________GET ATTR
		timeEval = [] 
		timeEval.append( time.clock() )
		
		
		#_1___ World Matrix Master 1
		             
		dataHandle   = dataBlock.inputValue( self.input3Attr )
		matrixMaster = floatMMatrixToMMatrix_( dataHandle.asFloatMatrix() )	

		
		#_2___ BB Matrix Master 8            
		
		matrixBBMaster = []
		arrayDataHandle = dataBlock.inputArrayValue( self.input4Attr )				
		
		for i in range( arrayDataHandle.elementCount() ): 
			arrayDataHandle.jumpToArrayElement(i) 			
			dataHandle = arrayDataHandle.inputValue()
			matrixBBMaster.append( floatMMatrixToMMatrix_( dataHandle.asFloatMatrix() ) )		
			
	
		#_3___ BB Matrix Slave 8 
               
		BBSlavesCoords  = []	
		arrayDataHandle = dataBlock.inputArrayValue( self.input2Attr )			

		
		for i in range( arrayDataHandle.elementCount() ):  
			arrayDataHandle.jumpToArrayElement(i)				
			dataHandle = arrayDataHandle.inputValue()			
			BBSlavesCoords.append( dataHandle.asFloat3() )
			
			
		#_____________________________________________________________________________________COMPUTE
		
		timeEval.append( time.clock() )		
					
		#_1___ get master Coords
		
		manipMasterCoords = []
		nbrBBPoint = 8

		for i in range( 0 , nbrBBPoint ):
			matrixBBMasterTRSF = matrixBBMaster[i] * matrixMaster 	
			trsValue = convertMMatrixToTSRValue( MMatrixToNum(matrixBBMasterTRSF) )
			manipMasterCoords.append( [ trsValue[0] , trsValue[1] , trsValue[2] ] )

			
		#_2___ get master Vectors
		
		upAB = om.MVector( ( manipMasterCoords[1][0] - manipMasterCoords[0][0] ) , ( manipMasterCoords[1][1] - manipMasterCoords[0][1] ) , ( manipMasterCoords[1][2] - manipMasterCoords[0][2] ) )      
		upAD = om.MVector( ( manipMasterCoords[3][0] - manipMasterCoords[0][0] ) , ( manipMasterCoords[3][1] - manipMasterCoords[0][1] ) , ( manipMasterCoords[3][2] - manipMasterCoords[0][2] ) )      
		upAA = om.MVector( ( manipMasterCoords[4][0] - manipMasterCoords[0][0] ) , ( manipMasterCoords[4][1] - manipMasterCoords[0][1] ) , ( manipMasterCoords[4][2] - manipMasterCoords[0][2] ) )      
				     
		dnCB = om.MVector( ( manipMasterCoords[5][0] - manipMasterCoords[6][0] ) , ( manipMasterCoords[5][1] - manipMasterCoords[6][1] ) , ( manipMasterCoords[5][2] - manipMasterCoords[6][2] ) )     
		dnCD = om.MVector( ( manipMasterCoords[7][0] - manipMasterCoords[6][0] ) , ( manipMasterCoords[7][1] - manipMasterCoords[6][1] ) , ( manipMasterCoords[7][2] - manipMasterCoords[6][2] ) )     
		dnCC = om.MVector( ( manipMasterCoords[2][0] - manipMasterCoords[6][0] ) , ( manipMasterCoords[2][1] - manipMasterCoords[6][1] ) , ( manipMasterCoords[2][2] - manipMasterCoords[6][2] ) ) 			
			
							                                                                                                                                                                               
      		
		#_3___ find if each point is in manip

		isIn = 0				
		for p in range( 0 , nbrBBPoint  ):
		
			upCurrent = om.MVector( ( BBSlavesCoords[p][0] - manipMasterCoords[0][0] ) , ( BBSlavesCoords[p][1] - manipMasterCoords[0][1] ) , ( BBSlavesCoords[p][2] - manipMasterCoords[0][2] ) )     
			dnCurrent = om.MVector( ( BBSlavesCoords[p][0] - manipMasterCoords[6][0] ) , ( BBSlavesCoords[p][1] - manipMasterCoords[6][1] ) , ( BBSlavesCoords[p][2] - manipMasterCoords[6][2] ) )      
										
			pScaleUpA =  upAB * upCurrent                                                                                                                                  
			pScaleUpB =  upAD * upCurrent                                                                                                                                  
			pScaleUpC =  upAA * upCurrent                                                                                                                                  
			                                                                                                                                                                       
			pScaleDnA =  dnCB * dnCurrent                                                                                                                                  
			pScaleDnB =  dnCD * dnCurrent                                                                                                                                  
			pScaleDnC =  dnCC * dnCurrent                                                                                                                                  
			            
						
			if ( 0 < pScaleUpA ) and ( 0 < pScaleUpB ) and ( 0 < pScaleUpC ) and ( 0 < pScaleDnA ) and ( 0 < pScaleDnB ) and ( 0 < pScaleDnC ):                                              
				isIn = 1
				break	 					
		

			
		#_____________________________________________________________________________________SET ATTR
		timeEval.append( time.clock() )
		
		output = isIn 				
		dataHandle = dataBlock.outputValue( self.outputAttr )		
		dataHandle.setDouble(output)	
			
		dataBlock.setClean( plug )        	
  
		timeEval.append( time.clock() )	

		#eval
		timediff    = []
		timediff.append( timeEval[0] - timeEval[1] )
		timediff.append( timeEval[1] - timeEval[2] )
		timediff.append( timeEval[2] - timeEval[3] )
		timediff.append( timeEval[0] - timeEval[3] )
		
		print('eval compute ================================')
		print('getAttr : %f , %f /100 '%( timediff[0] , timediff[0] / timediff[3] * 100) )
		print('compute : %f , %f /100 '%( timediff[1] , timediff[1] / timediff[3] * 100) )
		print('setAttr : %f , %f /100 '%( timediff[2] , timediff[2] / timediff[3] * 100) )
		print('total   : %f , %f /100 '%( timediff[3] , timediff[3] / timediff[3] * 100) )
		
			
			
    @classmethod
    def nodeCreator(cls):
        return ommpx.asMPxPtr(cls())


    @classmethod
    def nodeInitializer(cls):

        nAttr = om.MFnNumericAttribute()   
  
            
        cls.input2Attr = nAttr.create(cls.kInput2AttrLongName, cls.kInput2AttrName , om.MFnNumericData.k3Float  )
        nAttr.setArray(True)          
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)
 
        
        nAttr = om.MFnMatrixAttribute()   
        
        cls.input3Attr = nAttr.create(cls.kInput3AttrLongName, cls.kInput3AttrName , om.MFnNumericData.kFloat  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)
 
              
        cls.input4Attr = nAttr.create(cls.kInput4AttrLongName, cls.kInput4AttrName , om.MFnNumericData.kFloat )
        nAttr.setArray(True)           
        nAttr.setKeyable(True)        
        nAttr.setReadable(False)
           
        
        nAttr = om.MFnNumericAttribute() 
        
        cls.outputAttr = nAttr.create(cls.kOutputAttrLongName, cls.kOutputAttrName, om.MFnNumericData.kDouble)
        nAttr.setWritable(False)
        nAttr.setStorable(False)
     


        
        #cls.addAttribute(cls.input1Attr)
        cls.addAttribute(cls.input2Attr)
        cls.addAttribute(cls.input3Attr)        
        cls.addAttribute(cls.input4Attr)   
        cls.addAttribute(cls.outputAttr)
        
        #cls.attributeAffects(cls.input1Attr, cls.outputAttr)
        cls.attributeAffects(cls.input2Attr, cls.outputAttr)        
        cls.attributeAffects(cls.input3Attr, cls.outputAttr)
        cls.attributeAffects(cls.input4Attr, cls.outputAttr)
        
        

def initializePlugin(obj):
    plugin = ommpx.MFnPlugin( obj , 'leCantit', '1.0', 'Any')
    try:
        plugin.registerNode(ctrlVisibilityNode.kPluginNodeTypeName, ctrlVisibilityNode.kPluginNodeId, ctrlVisibilityNode.nodeCreator, ctrlVisibilityNode.nodeInitializer)
    except:
        raise Exception('Failed to register node: %s'%ctrlVisibilityNode.kPluginNodeTypeName)
   

def uninitializePlugin(obj):
    plugin = ommpx.MFnPlugin(obj)
    try:
        plugin.deregisterNode(ctrlVisibilityNode.kPluginNodeId)
    except:
        raise Exception('Failed to unregister node: %s'%ctrlVisibilityNode.kPluginNodeTypeName)
