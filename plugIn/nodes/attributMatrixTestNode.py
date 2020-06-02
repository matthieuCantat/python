
'''
#FOR TEST
import maya.cmds as mc
path = 'D:\mcantat_BDD\projects\code\maya\python\plugIn\dynamicTubeNode.py'
mc.file( new = True , f = True )
mc.loadPlugin( path , qt = True )   
'''

import sys
import math
import maya.OpenMaya as om
import maya.api.OpenMaya as ompy
import maya.OpenMayaMPx as ommpx
import maya.cmds as mc


class dynamicTube(ommpx.MPxNode):
	kPluginNodeTypeName = 'dynamicTube'
	kPluginNodeId = om.MTypeId(0x00033465)

	def __init__(self):
		ommpx.MPxNode.__init__(self)


	def compute( self, plug , dataBlock ): 
		
		#CHECK IF IT'S PLUG       
		outsAttrs = [ self.attrOutMatrices ]                    
		if not ( plug in outsAttrs ): return om.kUnknownParameter 

		#GET DATA 
		print('GET DATAMMatrix')  
		MatrixA    = self.utils_nodeAttrToMMatrix( dataBlock , self.attrInMatrixA    )
		MatrixB    = self.utils_nodeAttrToMMatrix( dataBlock , self.attrInMatrixB    )	
		print('GET DATAmatrices') 
		outMatricesBase   = self.utils_MMatricesBlend( MatrixA , MatrixB , samples  )
	  
		#CONVERT MATRICES TO COORDS
		print('CONVERT MATRICES TO COORDS') 		
		outPointsBase   = self.utils_MMatricesToMPoints( outMatricesBase  ) 

		#CONVERT COORDS TO MATRICES
		print('CONVERT COORDS TO MATRICES') 			
		outMatricesNew  = self.utils_MPointsToMMatrices( outPointsBase )

		#SET DATA
		print('SET DATA') 			   
		self.utils_MMatricesToNodeAttr( dataBlock , self.attrOutMatrices       , outMatricesNew) 

		print('SET CLEAN')		
		dataBlock.setClean( self.attrOutMatrices ) 
		dataBlock.setClean( plug ) 
		


	@classmethod
	def nodeCreator(cls):
		return ommpx.asMPxPtr(cls())



	@classmethod
	def nodeInitializer(cls):
		mNumData = om.MFnNumericData()
		# IN ATTR
		mAttr = om.MFnMatrixAttribute() 
		cls.attrInMatrixA = mAttr.create( 'inputMatrixA' , 'inputMatrixA' ,  mNumData.kFloat )
		mAttr.setChannelBox(True)
		mAttr.setKeyable(True)        
		mAttr.setReadable(True) 
		mAttr.setWritable(True)
		mAttr.setStorable(True)
		mAttr.setConnectable(True)         

		mAttr = om.MFnMatrixAttribute() 
		cls.attrInMatrixB = mAttr.create( 'inputMatrixB' , 'inputMatrixB' ,  mNumData.kFloat )
		mAttr.setChannelBox(True)
		mAttr.setKeyable(True)        
		mAttr.setReadable(True) 
		mAttr.setWritable(True)
		mAttr.setStorable(True)
		mAttr.setConnectable(True)         


		# OUT ATTR
		mAttr = om.MFnMatrixAttribute()          
		cls.attrOutMatrices = mAttr.create( 'outMatrices' , 'outMatrices' ,  mNumData.kFloat )    
		mAttr.setReadable(True) 
		mAttr.setStorable(True)
		mAttr.setConnectable(True) 
		mAttr.setArray(True) 
		mAttr.isDynamic()                    
		

		# ADD ATTR
		cls.addAttribute( cls.attrInMatrixA    )
		cls.addAttribute( cls.attrInMatrixB    )               
		cls.addAttribute( cls.attrOutMatrices  )

		#INFLUENCE
		cls.attributeAffects( cls.attrInMatrixA    , cls.attrOutMatrices )
		cls.attributeAffects( cls.attrInMatrixB    , cls.attrOutMatrices )

	def utils_nodeAttrToMMatrix( self , DataBlock , NodeAttr ): 
		dataHandle  = DataBlock.inputValue( NodeAttr )
		inFloatMatrix = dataHandle.asFloatMatrix()
		utils = om.MScriptUtil() #little hack
		inMatrix = om.MMatrix()
		utils.createMatrixFromList( utils_MMatrixToNum(inFloatMatrix), inMatrix )
		return inMatrix
	'''
	def utils_MMatrixToMPoint( self , Mmatrix ):
		trsf = om.MTransformationMatrix( Mmatrix )
		spaceInfo = om.MSpace()
		vec = trsf.getTranslation( spaceInfo.kWorld )
		return om.MPoint( vec )		
	'''

	def utils_nodeAttrToMMatrices( self , DataBlock , NodeAttr ): 
		arrayDataHandle = DataBlock.inputArrayValue( NodeAttr )
		outMMatrices = []   
		for i in range(0, arrayDataHandle.elementCount() ):
			dataHandle = arrayDataHandle.outputValue()
			outMMatrices.append( dataHandle.asMatrix() )
			arrayDataHandle.next() 
		return outMMatrices

	def utils_MMatricesToNodeAttr( self , DataBlock , NodeAttr  , Mmatices ):
		print('utils_MMatricesToNodeAttr')	               
		arrayDataHandle = DataBlock.outputArrayValue( NodeAttr )
		builder = om.MArrayDataBuilder(DataBlock, NodeAttr, len(Mmatices))		
		print(builder.elementCount())
		for i in range(0, len(Mmatices) ):
			handle = builder.addElement(i)
			print( builder.elementCount() , utils_MMatrixToNum(Mmatices[i]) )
			handle.setMMatrix( Mmatices[i] )
		
		arrayDataHandle.set(builder)
		arrayDataHandle.setAllClean()  	             	      

	def utils_nodeAttrToFloat( self , DataBlock , NodeAttr ): 
		dataHandle  = DataBlock.inputValue( NodeAttr )
		valueFloat = dataHandle.asFloat()
		return valueFloat

	def utils_nodeAttrToInt( self , DataBlock , NodeAttr ): 
		dataHandle  = DataBlock.inputValue( NodeAttr )
		valueInt = dataHandle.asInt()
		return valueInt

	def utils_MMatricesBlend( self , inMatrixA , inMatrixB , samples ):
		inMatrixAFloat = utils_MMatrixToNum( inMatrixA )
		inMatrixBFloat = utils_MMatrixToNum( inMatrixB )

		incr = []
		for i in range( 0 , len( inMatrixAFloat ) ):
			incr.append( (inMatrixBFloat[i] - inMatrixAFloat[i])/samples )
		#print( 'inMatrixAFloat' , inMatrixAFloat )
		#print( 'inMatrixAFloat' , inMatrixBFloat )		
		#print( 'incr' , incr )
		outMMatrices = []
		tmp = inMatrixAFloat 
		for i in range( samples ):
			for j in range( len(incr)):
				tmp[j] += incr[j]
			#print('tmp',tmp)
			outMMatrices.append( utils_numToMMatrix( tmp[:] ) )

		return outMMatrices


	def utils_MMatrixToMPoint( self , Mmatrix ):
		num = utils_MMatrixToNum( Mmatrix )
		return om.MPoint( num[12] , num[13] , num[14] )
	

	def utils_MPointToMMatrix( self , Mpoint ):
		num = [ 0.0,0,0,0 , 0,0,0,0 , 0,0,0,0 , Mpoint[0] , Mpoint[1] , Mpoint[2] , 0 ]
		return utils_numToMMatrix( num  )

	def utils_MMatricesToMPoints( self , MMatrices ):
		MPoints = []
		for matrix in MMatrices:
			MPoints.append( self.utils_MMatrixToMPoint( matrix ) )
		return MPoints

	def utils_MPointsToMMatrices( self , MPoints ):
		MMatrices = []
		for MPoint in MPoints:
			MMatrices.append( self.utils_MPointToMMatrix( MPoint ) )
		return MMatrices







def initializePlugin(obj):
	plugin = ommpx.MFnPlugin( obj , 'matthieuCantat', '1.0', 'Any')
	try:
		plugin.registerNode( dynamicTube.kPluginNodeTypeName, dynamicTube.kPluginNodeId, dynamicTube.nodeCreator, dynamicTube.nodeInitializer)
	except:
		raise Exception('Failed to register node: {0}'.format(dynamicTube.kPluginNodeTypeName) )
   

def uninitializePlugin(obj):
	plugin = ommpx.MFnPlugin(obj)
	try:
		plugin.deregisterNode( dynamicTube.kPluginNodeId )
	except:
		raise Exception('Failed to unregister node: {0}'.format(dynamicTube.kPluginNodeTypeName) )

        
        
        
def utils_MMatrixToNum( MMatrix ):
	return [  MMatrix(0,0) , MMatrix(0,1) , MMatrix(0,2) , MMatrix(0,3)  ,  MMatrix(1,0) , MMatrix(1,1) , MMatrix(1,2) , MMatrix(1,3)  ,  MMatrix(2,0) , MMatrix(2,1) , MMatrix(2,2) , MMatrix(2,3) ,  MMatrix(3,0) , MMatrix(3,1) , MMatrix(3,2) , MMatrix(3,3)  ]     


def utils_numToMMatrix( num ):
	inMatrix = om.MMatrix()
	utils = om.MScriptUtil()
	utils.createMatrixFromList( num, inMatrix )
	return inMatrix


