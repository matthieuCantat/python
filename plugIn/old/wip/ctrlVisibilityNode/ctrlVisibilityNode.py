'''
TROP LOURD, 0.5 POUR 100 OBJS...



'''



import sys
import math
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
		
		
		#___getWorldMatrixSlaves  
      	
		matrixSlaves = []        	
		arrayDataHandle = dataBlock.inputArrayValue( self.input1Attr )	
		
		for i in range( arrayDataHandle.elementCount() ): 
			arrayDataHandle.jumpToArrayElement(i) 
			dataHandle = arrayDataHandle.inputValue()				
			matrixSlaves.append( floatMMatrixToMMatrix_(dataHandle.asFloatMatrix()) )	
			
		#___getBBlocalMatrixSlaves
			
		matrixBBSlaves    = []
		matrixBBSlavesTMP = []		
		arrayDataHandle = dataBlock.inputArrayValue( self.input2Attr )			
		nbrBBPoint = 8
		lap = 0

		
		for i in range( arrayDataHandle.elementCount() ):  
			arrayDataHandle.jumpToArrayElement(i)
		
			if( (i % nbrBBPoint) == 0 ) and not ( i == 0 ) :
				matrixBBSlaves.append( matrixBBSlavesTMP )
				matrixBBSlavesTMP = []
			
			dataHandle = arrayDataHandle.inputValue()			
			matrixBBSlavesTMP.append( floatMMatrixToMMatrix_(dataHandle.asFloatMatrix()) )
			
		matrixBBSlaves.append( matrixBBSlavesTMP )			
			
		#____getWorldMatrixMaster
		             
		dataHandle   = dataBlock.inputValue( self.input3Attr )
		matrixMaster = floatMMatrixToMMatrix_(dataHandle.asFloatMatrix())	

		
		#____getBBlocalMatrixMaster            
		
		matrixBBMaster = []
		arrayDataHandle = dataBlock.inputArrayValue( self.input4Attr )				
		
		for i in range( arrayDataHandle.elementCount() ): 
			arrayDataHandle.jumpToArrayElement(i) 			
			dataHandle = arrayDataHandle.inputValue()
			matrixBBMaster.append( floatMMatrixToMMatrix_(dataHandle.asFloatMatrix()) )		
			
		
			
		#_____________________________________________________________________________________COMPUTE
					
		#__ 1 __master Coords
		manipMasterCoords = []
	
		# 8 point du cube
		for i in range( 0 , nbrBBPoint ):
			matrixBBMasterTRSF = matrixBBMaster[i] * matrixMaster 	
			trsValue = convertMMatrixToTSRValue( MMatrixToNum(matrixBBMasterTRSF) )
			manipMasterCoords.append( [ trsValue[0] , trsValue[1] , trsValue[2] ] )

				
		#__ 2 __Slaves Coords
		manipSlavesCoords = []
		manipSlavesCoordsTmp = []
		
		for i in range( 0 , len( matrixSlaves ) ) :
			
			
			# point du centre
			trsValue = convertMMatrixToTSRValue( MMatrixToNum(matrixSlaves[i]) )			
			manipSlavesCoordsTmp.append( [ trsValue[0] , trsValue[1] , trsValue[2] ] )
			
			# 8 point du cube
			for p in range( 0 , nbrBBPoint ):
				matrixBBSlavesTRSF = matrixBBSlaves[i][p] * matrixSlaves[i]	
				trsValue = convertMMatrixToTSRValue( MMatrixToNum(matrixBBSlavesTRSF) )					
				manipSlavesCoordsTmp.append( [ trsValue[0] , trsValue[1] , trsValue[2] ] )

			manipSlavesCoords.append(manipSlavesCoordsTmp)
			manipSlavesCoordsTmp = []				
				
		#__ 3 __Compute			
		
		boolSlaves = []
		

		#masterVector
		upAB = om.MVector( ( manipMasterCoords[1][0] - manipMasterCoords[0][0] ) , ( manipMasterCoords[1][1] - manipMasterCoords[0][1] ) , ( manipMasterCoords[1][2] - manipMasterCoords[0][2] ) )      
		upAD = om.MVector( ( manipMasterCoords[3][0] - manipMasterCoords[0][0] ) , ( manipMasterCoords[3][1] - manipMasterCoords[0][1] ) , ( manipMasterCoords[3][2] - manipMasterCoords[0][2] ) )      
		upAA = om.MVector( ( manipMasterCoords[4][0] - manipMasterCoords[0][0] ) , ( manipMasterCoords[4][1] - manipMasterCoords[0][1] ) , ( manipMasterCoords[4][2] - manipMasterCoords[0][2] ) )      
				     
		dnCB = om.MVector( ( manipMasterCoords[5][0] - manipMasterCoords[6][0] ) , ( manipMasterCoords[5][1] - manipMasterCoords[6][1] ) , ( manipMasterCoords[5][2] - manipMasterCoords[6][2] ) )     
		dnCD = om.MVector( ( manipMasterCoords[7][0] - manipMasterCoords[6][0] ) , ( manipMasterCoords[7][1] - manipMasterCoords[6][1] ) , ( manipMasterCoords[7][2] - manipMasterCoords[6][2] ) )     
		dnCC = om.MVector( ( manipMasterCoords[2][0] - manipMasterCoords[6][0] ) , ( manipMasterCoords[2][1] - manipMasterCoords[6][1] ) , ( manipMasterCoords[2][2] - manipMasterCoords[6][2] ) )      
 				                                                                                                                                                                               
      		
		#SlaveVector
		
		for i in range( 0 , len( matrixSlaves ) ) :
			
			isIn = 0				
			for p in range( 0 , nbrBBPoint + 1 ):
		
				upCurrent = om.MVector( ( manipSlavesCoords[i][p][0] - manipMasterCoords[0][0] ) , ( manipSlavesCoords[i][p][1] - manipMasterCoords[0][1] ) , ( manipSlavesCoords[i][p][2] - manipMasterCoords[0][2] ) )     
				dnCurrent = om.MVector( ( manipSlavesCoords[i][p][0] - manipMasterCoords[6][0] ) , ( manipSlavesCoords[i][p][1] - manipMasterCoords[6][1] ) , ( manipSlavesCoords[i][p][2] - manipMasterCoords[6][2] ) )      

 				pScaleUpA =  upAB * upCurrent                                                                                                                                  
 				pScaleUpB =  upAD * upCurrent                                                                                                                                  
 				pScaleUpC =  upAA * upCurrent                                                                                                                                  
 				                                                                                                                                                                       
 				pScaleDnA =  dnCB * dnCurrent                                                                                                                                  
 				pScaleDnB =  dnCD * dnCurrent                                                                                                                                  
 				pScaleDnC =  dnCC * dnCurrent                                                                                                                                  
 				                                                                                                                                                                                                                                                                                                                              	                                                                                                                                                                               
				if ( 0 < pScaleUpA ) and ( 0 < pScaleUpB ) and ( 0 < pScaleUpC ) and ( 0 < pScaleDnA ) and ( 0 < pScaleDnB ) and ( 0 < pScaleDnC ):                                              
					isIn = 1
					break	 					
		

			boolSlaves.append(isIn) 
			

		#set output
		
		output = boolSlaves 
		
		
		arrayDataHandle = dataBlock.outputArrayValue( self.outputAttr )		
		arrayDataHandleBuild = arrayDataHandle.builder() 
	
		for i in range( len( output ) ):
			dataHandle = arrayDataHandleBuild.addElement(i)
			dataHandle.setDouble(output[i])

 			
		dataBlock.setClean( plug )        	
  
			
			
			
    @classmethod
    def nodeCreator(cls):
        return ommpx.asMPxPtr(cls())


    @classmethod
    def nodeInitializer(cls):

        nAttr = om.MFnMatrixAttribute()   
        
        cls.input1Attr = nAttr.create(cls.kInput1AttrLongName, cls.kInput1AttrName , om.MFnNumericData.kFloat )
        nAttr.setArray(True)        
        nAttr.setKeyable(True)        
        nAttr.setReadable(False)
        nAttr.setIndexMatters(False)
        nAttr.setDisconnectBehavior(om.MFnMatrixAttribute.kDelete)        
                
        cls.input2Attr = nAttr.create(cls.kInput2AttrLongName, cls.kInput2AttrName , om.MFnNumericData.kFloat  )
        nAttr.setArray(True)          
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)
        nAttr.setIndexMatters(False)
        nAttr.setDisconnectBehavior(om.MFnMatrixAttribute.kDelete)        
        
        cls.input3Attr = nAttr.create(cls.kInput3AttrLongName, cls.kInput3AttrName , om.MFnNumericData.kFloat  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)
 
              
        cls.input4Attr = nAttr.create(cls.kInput4AttrLongName, cls.kInput4AttrName , om.MFnNumericData.kFloat )
        nAttr.setArray(True)           
        nAttr.setKeyable(True)        
        nAttr.setReadable(False)
        nAttr.setIndexMatters(False)
        nAttr.setDisconnectBehavior(om.MFnMatrixAttribute.kDelete)               
        
        nAttr = om.MFnNumericAttribute() 
        
        cls.outputAttr = nAttr.create(cls.kOutputAttrLongName, cls.kOutputAttrName, om.MFnNumericData.kDouble)
        nAttr.setWritable(False)
        nAttr.setStorable(False)
        nAttr.setArray(True)
        nAttr.setIndexMatters(False)
        nAttr.setUsesArrayDataBuilder(True)
        nAttr.setDisconnectBehavior(ompy.MFnNumericAttribute.kDelete)          


        
        cls.addAttribute(cls.input1Attr)
        cls.addAttribute(cls.input2Attr)
        cls.addAttribute(cls.input3Attr)        
        cls.addAttribute(cls.input4Attr)   
        cls.addAttribute(cls.outputAttr)
        
        cls.attributeAffects(cls.input1Attr, cls.outputAttr)
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
