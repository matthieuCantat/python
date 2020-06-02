'''
version 1 trop lourd, 

version 2 les slaves ne bouge pas , trop lourd

version 3 les slaves ne bouge pas + un node par slaves

version 4 les slaves ne bouge pas + un node par slaves + optim

version 5 les slaves ne bouge pas + un node par slaves + optim + on allonge l init

version 6 les slaves ne bouge pas + un node par slaves + optim + on allonge l init + detection de distance


'''



import sys
import math
import time
import maya.OpenMaya as om
import maya.api.OpenMaya as ompy
import maya.OpenMayaMPx as ommpx
import maya.cmds as mc



def MMatrixToNum( matrix ):
	return [  matrix(0,0) , matrix(0,1) , matrix(0,2) , matrix(0,3)  ,  matrix(1,0) , matrix(1,1) , matrix(1,2) , matrix(1,3)  ,  matrix(2,0) , matrix(2,1) , matrix(2,2) , matrix(2,3) ,  matrix(3,0) , matrix(3,1) , matrix(3,2) , matrix(3,3)  ]   	



def numTofloatMMatrix( fm ):
	floatM = om.MFloatMatrix()
	om.MScriptUtil.createFloatMatrixFromList ([
		fm[0],fm[1],fm[2],fm[3],
		fm[4],fm[5],fm[6],fm[7],
		fm[8],fm[9],fm[10],fm[11],
		fm[12],fm[13],fm[14],fm[15]], floatM)
	return floatM
	
	
	
    
def convertMMatrixToTSRValue( matrixValues ):


	mtransChildren = ompy.MTransformationMatrix( ompy.MMatrix(matrixValues) )

	translate = mtransChildren.translation( ompy.MSpace.kWorld) 
	rotate    = mtransChildren.rotationComponents()
	scale     = mtransChildren.scale( ompy.MSpace.kWorld)
 	
	childrenTRSValue = [ translate[0] , translate[1] , translate[2] , math.degrees(rotate[0]) , math.degrees(rotate[1]) , math.degrees(rotate[2]) , scale[0] , scale[1] , scale[2] ]	

	return childrenTRSValue
			




#_____________________________________________________________________________________________________________________________________ getBarycentre

def getBarycentre( coords ):
	
	i = 0
	
	barycentre = [ 0 , 0 , 0 ]
	
	for i in range(0 , len(coords) , 3 ):
		barycentre[0] += coords[i + 0] 
		barycentre[1] += coords[i + 1]
		barycentre[2] += coords[i + 2]

	barycentre[0] /= len(coords)
	barycentre[1] /= len(coords)
	barycentre[2] /= len(coords)					
	
		
	return barycentre


#_____________________________________________________________________________________________________________________________________ extractBBRotCoordsAttr

def extractBBRotCoordsAttr( ctrl ):

	coords = []
	attr   = 'BBreelCoords_1'
	
	coordsString  = mc.getAttr ( ctrl + '.' + attr) 
	coordsStrings = coordsString.split(' ')
	

	for elem in coordsStrings:	
		try:coords.append( float(elem) )
		except:pass 		

	return coords

	
#_____________________________________________________________________________________________________________________________________ buildVisibilitySlavesLocs

def buildVisibilitySlavesLocs( ctrl ):
	
	nbrLocs = 8	
	
	axes  = [ 'X' , 'Y' , 'Z' ]	
	attrs = [ 'translate' , 'rotate' , 'scale' ]
	
	# coords
	
	coordsLocs = extractBBRotCoordsAttr( ctrl )


	# create loc
	locatorNames = []	
	
	j = 0
	
	
	for i in range( nbrLocs ):
	
		locatorName = '%s_slaveVisibility%r_loc' %( ctrl , i ) 
		mc.spaceLocator( n = locatorName )

		
		for axe in axes:
			mc.setAttr( ( locatorName + '.' + attrs[0] + axe ) , coordsLocs[j] )
			j += 1			
		
		
		mc.parent( locatorName , ctrl )		
		
		locatorNames.append( locatorName ) 
		
	
	return locatorNames
	

		

#_____________________________________________________________________________________________________________________________________ getMatrixBBMaster		


def getMatrixBBMaster(masterManips):
	
	#as float matrix
	
	matrixBBMaster = []
	
	for manip in masterManips:
		bbLocators = buildVisibilitySlavesLocs( manip )
				
		for loc in bbLocators:
			matrixNum =  mc.getAttr(( loc + '.matrix') ) 
			matrixBBMaster.append( numTofloatMMatrix( matrixNum ) )				
			
		mc.delete(bbLocators)
		
	return matrixBBMaster
		
#_____________________________________________________________________________________________________________________________________ getMatrixBBMaster		


def getBBSlavesCoords( slaveManip ):
	
	BBSlavesCoords = []
	
	
	coords = extractBBRotCoordsAttr( slaveManip )
	
	for i in range( 0 , len(coords) , 3):
		BBSlavesCoords.append( [ coords[i] , coords[i+1] , coords[i+2] ] )

			
	return BBSlavesCoords


#_____________________________________________________________________________________________________________________________________ NODE	
	

class ctrlVisibilityNode(ommpx.MPxNode):

    kPluginNodeTypeName = 'ctrlVisibilityNode'
    kPluginNodeId = om.MTypeId(0x00033445)

    
    input3Attr = None
    kInput3AttrName = 'inM'
    kInput3AttrLongName = 'inputMasterMatrix'

    
    output = None
    kOutputAttrName = 'out'
    kOutputAttrLongName = 'outputSlavesBool'
    
    
    def __init__(self):
		ommpx.MPxNode.__init__(self)
		print('________INIT_________')
		selection    = mc.ls( sl = True )
		
		if( len(selection) < 2 ):
			mc.error('must select at least 2 manips')
		
		print(selection)
		masterManips = selection[0:( len(selection)-1 )]        
		slaveManip   = selection[-1]
		
		
		self.matrixBBMaster = getMatrixBBMaster(masterManips)     
		self.BBSlavesCoords = getBBSlavesCoords(slaveManip)
		
		

		
	#_______________________________________________________________________________________________________________________________________________________________________ compute
        
    def compute( self, plug , dataBlock ):
    
		if not ( plug == self.outputAttr ):
			return om.kUnknownParameter			
				
		#_____________________________________________________________________________________GET ATTR
		timeEval = [] 
		timeEval.append( time.clock() )
		

		#_1___ World Matrix Master 1
		             
		dataHandle   = dataBlock.inputValue( self.input3Attr )
		matrixMaster = dataHandle.asFloatMatrix()	



		#_____________________________________________________________________________________COMPUTE
		
		timeEval.append( time.clock() )		
					
		#_1___ get master Coords
		
		manipMasterCoords = []
		nbrBBPoint = 8


		
		for i in range( 0 , nbrBBPoint ):
			matrixBBMasterTRSF = self.matrixBBMaster[i] * matrixMaster 	
			trsValue = convertMMatrixToTSRValue( MMatrixToNum(matrixBBMasterTRSF) )
			manipMasterCoords.append( [ trsValue[0] , trsValue[1] , trsValue[2] ] )


		#_2___ get master Vectors
		
		upAB = om.MVector( ( manipMasterCoords[1][0] - manipMasterCoords[0][0] ) , ( manipMasterCoords[1][1] - manipMasterCoords[0][1] ) , ( manipMasterCoords[1][2] - manipMasterCoords[0][2] ) )      
		upAD = om.MVector( ( manipMasterCoords[3][0] - manipMasterCoords[0][0] ) , ( manipMasterCoords[3][1] - manipMasterCoords[0][1] ) , ( manipMasterCoords[3][2] - manipMasterCoords[0][2] ) )      
		upAA = om.MVector( ( manipMasterCoords[4][0] - manipMasterCoords[0][0] ) , ( manipMasterCoords[4][1] - manipMasterCoords[0][1] ) , ( manipMasterCoords[4][2] - manipMasterCoords[0][2] ) )      
		
		
		trsValueBarycentre = convertMMatrixToTSRValue( MMatrixToNum(matrixMaster) )		
		vectorDist = [ upAB.length() , upAD.length() , upAA.length() ]
		vectorDist.sort()
		masterRayon = vectorDist[-1] / 2 
		
		isNear = 0
		for coords in self.BBSlavesCoords:
			dist = om.MVector(  (coords[0] - trsValueBarycentre[0]) , (coords[1] - trsValueBarycentre[1]) , (coords[2] - trsValueBarycentre[2]) ).length()
			
			if( dist < masterRayon ):
				isNear = 1
				continue
		
		isIn = 0	
		
		if( isNear == 1 ):	
	
			dnCB = om.MVector( ( manipMasterCoords[5][0] - manipMasterCoords[6][0] ) , ( manipMasterCoords[5][1] - manipMasterCoords[6][1] ) , ( manipMasterCoords[5][2] - manipMasterCoords[6][2] ) )     
			dnCD = om.MVector( ( manipMasterCoords[7][0] - manipMasterCoords[6][0] ) , ( manipMasterCoords[7][1] - manipMasterCoords[6][1] ) , ( manipMasterCoords[7][2] - manipMasterCoords[6][2] ) )     
			dnCC = om.MVector( ( manipMasterCoords[2][0] - manipMasterCoords[6][0] ) , ( manipMasterCoords[2][1] - manipMasterCoords[6][1] ) , ( manipMasterCoords[2][2] - manipMasterCoords[6][2] ) ) 			
				
								                                                                                                                                                                               
    			
			#_3___ find if each point is in manip
    		
						
			for p in range( 0 , nbrBBPoint  ):
			
				upCurrent = om.MVector( ( self.BBSlavesCoords[p][0] - manipMasterCoords[0][0] ) , ( self.BBSlavesCoords[p][1] - manipMasterCoords[0][1] ) , ( self.BBSlavesCoords[p][2] - manipMasterCoords[0][2] ) )     
				dnCurrent = om.MVector( ( self.BBSlavesCoords[p][0] - manipMasterCoords[6][0] ) , ( self.BBSlavesCoords[p][1] - manipMasterCoords[6][1] ) , ( self.BBSlavesCoords[p][2] - manipMasterCoords[6][2] ) )      
											
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

		'''
		print('eval compute ================================')
		print('getAttr : %f , %f /100 '%( timediff[0] , timediff[0] / timediff[3] * 100) )		
		print('compute : %f , %f /100 '%( timediff[1] , timediff[1] / timediff[3] * 100) )
		print('setAttr : %f , %f /100 '%( timediff[2] , timediff[2] / timediff[3] * 100) )
		print('total   : %f , %f /100 '%( timediff[3] , timediff[3] / timediff[3] * 100) )
		'''
			
			
    @classmethod
    def nodeCreator(cls):
        return ommpx.asMPxPtr(cls())


    @classmethod
    def nodeInitializer(cls):

   
        
        nAttr = om.MFnMatrixAttribute()   
        
        cls.input3Attr = nAttr.create(cls.kInput3AttrLongName, cls.kInput3AttrName , om.MFnNumericData.kFloat  )
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)
 
  
        nAttr = om.MFnNumericAttribute() 
        
        cls.outputAttr = nAttr.create(cls.kOutputAttrLongName, cls.kOutputAttrName, om.MFnNumericData.kDouble)
        nAttr.setWritable(False)
        nAttr.setStorable(False)
     
  
        cls.addAttribute(cls.input3Attr)         
        cls.addAttribute(cls.outputAttr)
        
        cls.attributeAffects(cls.input3Attr, cls.outputAttr)

        
        

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
