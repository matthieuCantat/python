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


class dynamicTube(ommpx.MPxNode):
	kPluginNodeTypeName = 'dynamicTube'
	kPluginNodeId = om.MTypeId(0x00033465)

	def __init__(self):
		ommpx.MPxNode.__init__(self)
		self.outPoints = []
		self.outPointsStoreA = []
		self.outPointsStoreB = []
		#FILL TOPOLOGY INFO
		self.topologyNeighbourIndexes = []
		self.topologyNeighbourBaseLenghts = []
		self.StorePoints = None
		self.vGravity = om.MFloatVector( 0 , -9.8 , 0 )	
		self.raySlave = 1	

	def compute( self, plug , dataBlock ): 
		#CHECK IF IT'S PLUG       
		outsAttrs = [ self.attrOutPoints ]                    
		if not ( plug in outsAttrs ): return om.kUnknownParameter 
		#GET DATA 
		timeGetDataA = time.clock() 		
		PointA              = utils.nodeAttrToMVector(  dataBlock , self.attrInPointA     )
		PointB              = utils.nodeAttrToMVector(  dataBlock , self.attrInPointB     )	  
		samples             = utils.nodeAttrToInt(     dataBlock , self.attrInNbrSamples )
		nbrLinkEval         = utils.nodeAttrToInt(      dataBlock , self.attrInNbrLinkEval    )
		momentumPastSample  = utils.nodeAttrToInt(      dataBlock , self.attrInMomentumPastSample   )
		momentumAverageSize = utils.nodeAttrToInt(      dataBlock , self.attrInMomentumAverageSize   )
		momentumMaxMemory   = momentumPastSample + momentumAverageSize + 1		 				
		friction            = utils.nodeAttrToFloat(    dataBlock , self.attrInFriction   )
		mass                = utils.nodeAttrToFloat(    dataBlock , self.attrInMass       )
		length              = utils.nodeAttrToFloat(    dataBlock , self.attrInLength     )        
		elasticity          = utils.nodeAttrToFloat(    dataBlock , self.attrInElasticity ) 
		repulsion           = utils.nodeAttrToFloat(    dataBlock , self.attrInRepulsion  ) 
		init                = utils.nodeAttrToInt(      dataBlock , self.attrInInit  ) 
		edgeLengthPower     = utils.nodeAttrToFloat(    dataBlock , self.attrInEdgeLengthPower ) 
		addPower            = utils.nodeAttrToFloat(    dataBlock , self.attrInAddPower        ) 
		relaxPower          = utils.nodeAttrToFloat(    dataBlock , self.attrInRelaxPower      ) 
		smoothPower         = utils.nodeAttrToFloat(    dataBlock , self.attrInSmoothPower     ) 									
		pointPlaneCollision = utils.nodeAttrToMVector(  dataBlock , self.attrInPointPlaneCollision ) 
		pointSphereCollision= utils.nodeAttrToMVector(  dataBlock , self.attrInPointSphereCollision  ) 	
		raySphereCollision  = utils.nodeAttrToFloat(    dataBlock , self.attrInRaySphereCollision  ) 	
		outPointsBis        = utils.nodeAttrToMVectors( dataBlock , self.attrOutPoints  )
						
		if( init == 1 ):
			#POINT			
			self.outPoints   = utils.MVectorBlend( PointA , PointB , samples  )
			#MOMENTUM					 
			self.StorePoints = utils.DynamicStore( arrayFill = self.outPoints , maxIndex = momentumMaxMemory )
			#FILL TOPOLOGY INFO
			self.topologyNeighbourIndexes = [[1]]
			self.topologyNeighbourIndexes += [ [i-1,i+1] for i in range( 1 , samples +1 ) ]
			self.topologyNeighbourIndexes += [ [samples]]		
			self.topologyNeighbourBaseLenghts = [ [ length for i in indexes ] for indexes in self.topologyNeighbourIndexes ] 
		else:
			#MOMENTUM
			vMomentums = []
			for i in range( 0 , len(self.outPoints) ):
				vMomentum = om.MFloatVector( 0 , 0 , 0 )
				for ia in range( 0 , momentumAverageSize + 1 ):
					indexStore = momentumPastSample + ia 
					vMomentum += self.StorePoints[indexStore][i] - self.StorePoints[indexStore+1][i]
				vMomentum = vMomentum / ( momentumAverageSize + 1 )
				vMomentums.append(vMomentum)
			#___________________________________________________________DYNAMIC COMPUTE START	
			#startFrame = mc.playbackOptions( q = True , min = True )
			#FORCES
			outPoints = self.outPoints[:]
			vWeight   = self.vGravity * mass
			for i in range( 0 , len(outPoints) ):
				vFriction = vMomentums[i] * -1 * friction;
				outPoints[i] = outPoints[i] + vMomentums[i] + vFriction + vWeight	

			#LINKS
			points      = [PointA] + outPoints +  [PointB]
			fixeIndexes = [ 0 , len(points) - 1 ]
			points = utils.applyTopologyEdgeLength( points , fixeIndexes , edgeLengthPower , elasticity , repulsion , nbrLinkEval , self.topologyNeighbourIndexes , self.topologyNeighbourBaseLenghts )
			points = utils.applyTopologyAdd(        points , fixeIndexes , addPower        , elasticity , repulsion , nbrLinkEval , self.topologyNeighbourIndexes , self.topologyNeighbourBaseLenghts )
			points = utils.applyTopologyRelax(      points , fixeIndexes , relaxPower      , elasticity , repulsion , nbrLinkEval , self.topologyNeighbourIndexes , self.topologyNeighbourBaseLenghts )
			points = utils.applyTopologySmooth(     points , fixeIndexes , smoothPower     , nbrLinkEval , self.topologyNeighbourIndexes , self.topologyNeighbourBaseLenghts )

			outPoints = points[1:len(points)-1]

			#COLLISION GROUND
			for i in range( 0 , len( outPoints ) ):
				if( outPoints[i].y < pointPlaneCollision.y + self.raySlave ):
					outPoints[i].y = pointPlaneCollision.y + self.raySlave

			#COLLISION SPHERE
			for i in range( 0 , len( outPoints ) ):			
				vRepulse = utils.getAttractForce( outPoints[i] , pointSphereCollision , triggerDist = raySphereCollision + self.raySlave , power = 1 , globalIter = 1  , repulsion = 1  )	
				outPoints[i] = outPoints[i] + vRepulse	

			#___________________________________________________________DYNAMIC COMPUTE END 

			#STORE MATRICES FOR THE NEXT EVAL	
			self.StorePoints.addFirst( self.outPoints )
			self.outPoints       = outPoints[:]
	
		#SET DATA		
		utils.MVectorsToNodeAttr( dataBlock , self.attrOutPoints , self.outPoints)
		dataBlock.setClean( self.attrOutPoints ) 
		dataBlock.setClean( plug ) 

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

		# IN ATTR
		cls.attrInPointA = nAttr.createPoint( 'inputPointA' , 'inputPointA' )
		nAttr.setKeyable(True)                 
		nAttr.setChannelBox(False) 

		cls.attrInPointB = nAttr.createPoint( 'inputPointB' , 'inputPointB' )
		nAttr.setKeyable(True)          
		nAttr.setChannelBox(False) 

		cls.attrInNbrSamples = nAttr.create( 'nbrSamples' , 'nbrSamples' , nData.kInt  , 10.0 )
		nAttr.setKeyable(True)        
		nAttr.setChannelBox(True)        
		nAttr.setMin(1.0)    
		
		cls.attrInNbrLinkEval = nAttr.create( 'nbrLinkEval' , 'nbrLinkEval' , nData.kInt  , 5.0 )
		nAttr.setKeyable(True)        
		nAttr.setChannelBox(True)        
		nAttr.setMin(1.0)    

		cls.attrInMomentumPastSample = nAttr.create( 'momentumPastSample' , 'momentumPastSample' , nData.kInt , 1 )	
		nAttr.setKeyable(True)        
		nAttr.setChannelBox(True)        
		nAttr.setMin(0)    
		nAttr.setMax(7)  

		cls.attrInMomentumAverageSize = nAttr.create( 'momentumAverageSize' , 'momentumAverageSize' , nData.kInt  , 0 )
		nAttr.setKeyable(True)        
		nAttr.setChannelBox(True)        
		nAttr.setMin(0)    		
		nAttr.setMax(7)  
		
		cls.attrInFriction = nAttr.create( 'friction' , 'friction' , nData.kFloat  , 0.01 )
		nAttr.setKeyable(True)        
		nAttr.setChannelBox(True)        
		nAttr.setMin(0.0)    
		nAttr.setMax(1.0) 
		
		cls.attrInMass = nAttr.create( 'mass' , 'mass' , nData.kFloat  , 0.1 )
		nAttr.setKeyable(True)        
		nAttr.setChannelBox(True)      
		nAttr.setMin(0.0)    
		
		cls.attrInLength = nAttr.create( 'length' , 'length' , nData.kFloat  , 1.0 )
		nAttr.setKeyable(True)        
		nAttr.setChannelBox(True)      
		nAttr.setMin(0.0)    
		
		cls.attrInElasticity = nAttr.create( 'elasticity' , 'elasticity' , nData.kFloat  , 0.6 )
		nAttr.setKeyable(True)        
		nAttr.setChannelBox(True)      
		nAttr.setMin(0.0)               
		nAttr.setMax(1.0) 

		cls.attrInRepulsion = nAttr.create( 'repulsion' , 'repulsion' , nData.kFloat  , 0.6 )
		nAttr.setKeyable(True)        
		nAttr.setChannelBox(True)     
		nAttr.setMin(0.0)            
		nAttr.setMax(1.0) 

		cls.attrInInit = nAttr.create( 'init' , 'init' , nData.kInt , 1 )
		nAttr.setKeyable(True)        
		nAttr.setChannelBox(True)      
		nAttr.setMin(0)            
		nAttr.setMax(1)

		cls.attrInEdgeLengthPower = nAttr.create( 'edgeLengthPower' , 'edgeLengthPower' , nData.kFloat  , 0 )
		nAttr.setKeyable(True)        
		nAttr.setChannelBox(True)     
		nAttr.setMin(0.0)   
		nAttr.setMax(1.0) 

		cls.attrInAddPower = nAttr.create( 'addPower' , 'addPower' , nData.kFloat  , 0 )
		nAttr.setKeyable(True)        
		nAttr.setChannelBox(True)     
		nAttr.setMin(0.0)   
		nAttr.setMax(1.0) 

		cls.attrInRelaxPower = nAttr.create( 'relaxPower' , 'relaxPower' , nData.kFloat  , 0 )
		nAttr.setKeyable(True)        
		nAttr.setChannelBox(True)     
		nAttr.setMin(0.0)   
		nAttr.setMax(1.0) 

		cls.attrInSmoothPower = nAttr.create( 'smoothPower' , 'smoothPower' , nData.kFloat  , 0 )
		nAttr.setKeyable(True)        
		nAttr.setChannelBox(True)     
		nAttr.setMin(0.0)   
		nAttr.setMax(1.0) 		

		cls.attrInPointPlaneCollision = nAttr.createPoint( 'pointPlaneCollision' , 'pointPlaneCollision' )
		nAttr.setKeyable(True)                 
		nAttr.setChannelBox(False) 

		cls.attrInPointSphereCollision = nAttr.createPoint( 'pointSphereCollision' , 'pointSphereCollision' )
		nAttr.setKeyable(True)                 
		nAttr.setChannelBox(False) 

		cls.attrInRaySphereCollision = nAttr.create( 'raySphereCollision' , 'raySphereCollision' , nData.kFloat  , 1 )
		nAttr.setKeyable(True)        
		nAttr.setChannelBox(True)     
		nAttr.setMin(0.0)   						

		# OUT ATTR      
		cls.attrOutPoints = nAttr.createPoint( 'outPoints' , 'outPoints' )    
		nAttr.setReadable(True) 
		nAttr.setStorable(True)
		nAttr.setConnectable(True) 		    
		nAttr.setArray(True)    
		nAttr.setUsesArrayDataBuilder(True)                
	
		# ADD ATTR
		cls.addAttribute( cls.attrInPointA     )
		cls.addAttribute( cls.attrInPointB     )
		cls.addAttribute( cls.attrInNbrSamples )
		cls.addAttribute( cls.attrInNbrLinkEval)
		cls.addAttribute( cls.attrInMomentumPastSample )		
		cls.addAttribute( cls.attrInMomentumAverageSize )		
		cls.addAttribute( cls.attrInFriction   )
		cls.addAttribute( cls.attrInMass       )
		cls.addAttribute( cls.attrInLength     )
		cls.addAttribute( cls.attrInElasticity )  
		cls.addAttribute( cls.attrInRepulsion  )    
		cls.addAttribute( cls.attrInInit       )
		cls.addAttribute( cls.attrInEdgeLengthPower)
		cls.addAttribute( cls.attrInAddPower)
		cls.addAttribute( cls.attrInRelaxPower)
		cls.addAttribute( cls.attrInSmoothPower	)		                		
		cls.addAttribute( cls.attrOutPoints     )
		cls.addAttribute( cls.attrInPointPlaneCollision ) 
		cls.addAttribute( cls.attrInPointSphereCollision )
		cls.addAttribute( cls.attrInRaySphereCollision )

		#INFLUENCE
		cls.attributeAffects( cls.attrInPointA     , cls.attrOutPoints )
		cls.attributeAffects( cls.attrInPointB     , cls.attrOutPoints )
		cls.attributeAffects( cls.attrInNbrSamples , cls.attrOutPoints )
		cls.attributeAffects( cls.attrInNbrLinkEval, cls.attrOutPoints )
		cls.attributeAffects( cls.attrInMomentumPastSample       , cls.attrOutPoints )		
		cls.attributeAffects( cls.attrInMomentumAverageSize       , cls.attrOutPoints )				
		cls.attributeAffects( cls.attrInFriction   , cls.attrOutPoints )
		cls.attributeAffects( cls.attrInMass       , cls.attrOutPoints )
		cls.attributeAffects( cls.attrInLength     , cls.attrOutPoints )
		cls.attributeAffects( cls.attrInElasticity , cls.attrOutPoints )              
		cls.attributeAffects( cls.attrInRepulsion  , cls.attrOutPoints )        
		cls.attributeAffects( cls.attrInInit       , cls.attrOutPoints )
		cls.attributeAffects( cls.attrInEdgeLengthPower       , cls.attrOutPoints )		
		cls.attributeAffects( cls.attrInAddPower       , cls.attrOutPoints )		
		cls.attributeAffects( cls.attrInRelaxPower       , cls.attrOutPoints )
		cls.attributeAffects( cls.attrInSmoothPower       , cls.attrOutPoints )
		cls.attributeAffects( cls.attrInPointPlaneCollision , cls.attrOutPoints ) 
		cls.attributeAffects( cls.attrInPointSphereCollision, cls.attrOutPoints  )
		cls.attributeAffects( cls.attrInRaySphereCollision , cls.attrOutPoints )


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

        

