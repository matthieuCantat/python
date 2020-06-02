
'''
#FOR TEST
import maya.cmds as mc
path = 'D:\mcantat_BDD\projects\code\maya\python\plugIn\dynamicSkin.py'
mc.file( new = True , f = True )
mc.loadPlugin( path , qt = True )   
'''


import math, sys, copy
import maya.OpenMaya as om
import maya.OpenMayaAnim as omAnim
import maya.OpenMayaMPx as omMPx
from maya.mel import eval as meval
import time
import utilsMayaNodes as utils

kPluginNodeTypeName = "dynamicSkin"
dynamicSkinId = om.MTypeId(0x0010A52B)

# Node definition
class dynamicSkin(omMPx.MPxDeformerNode):

	def __init__(self):
		omMPx.MPxDeformerNode.__init__(self)
		self.vGravity = om.MFloatVector( 0 , -9.8 , 0 )
		self.inPoints = []
		self.inNormals = []
		self.basePoints = []
		self.outPoints = []
		self.StorePoints = None
		self.nbrPoints = 0
		#FILL TOPOLOGY INFO
		self.topologyNeighbourIndexes = []
		self.topologyNeighbourBaseLenghts = []
		self.topologyNeighbourLock = []
		#VOLUME
		self.baseDistanceCumulate = 0

	def deform( self, dataBlock, iter, matrix, index ):

		envelope  = omMPx.cvar.MPxGeometryFilter_envelope
		input     = omMPx.cvar.MPxGeometryFilter_input
		inputGeom = omMPx.cvar.MPxGeometryFilter_inputGeom
		groupId   = omMPx.cvar.MPxGeometryFilter_groupId

		#___________________________GET ATTR	
		envelope            = utils.nodeAttrToFloat(   dataBlock , envelope  )
		cache               = utils.nodeAttrToInt(     dataBlock , self.attrInCache  )
		momentumPastSample  = utils.nodeAttrToInt(     dataBlock , self.attrInMomentumPastSample   )
		momentumAverageSize = utils.nodeAttrToInt(     dataBlock , self.attrInMomentumAverageSize   )
		momentumMaxMemory   = momentumPastSample + momentumAverageSize + 1		 
		friction            = utils.nodeAttrToFloat(   dataBlock , self.attrInFriction   )
		mass                = utils.nodeAttrToFloat(   dataBlock , self.attrInMass       )    
		bindElasticity      = utils.nodeAttrToFloat(   dataBlock , self.attrInBindElasticity )
		pressure            = utils.nodeAttrToFloat(   dataBlock , self.attrInPressure )		
		topoMode            = utils.nodeAttrToEnumStr( dataBlock , self.attrInTopoMode  , self.topoMode )	
		topoType            = utils.nodeAttrToEnumStr( dataBlock , self.attrInTopoType  , self.topoType )
		recomputeLink       = utils.nodeAttrToInt(     dataBlock , self.attrInRecomputeLink    ) 	 		
		nbrLinkEval         = utils.nodeAttrToInt(     dataBlock , self.attrInNbrLinkEval    ) 
		linkElasticity      = utils.nodeAttrToFloat(   dataBlock , self.attrInLinkElasticity  )
		linkRepulsion       = utils.nodeAttrToFloat(   dataBlock , self.attrInLinkRepulsion  )

		#GET INPUT GEOMETRY
		hInput = dataBlock.inputArrayValue(input)
		hInput.jumpToArrayElement(index)
		hInputElement   = hInput.inputValue()
		self.hInputGeom = hInputElement.child(inputGeom)	
		inMesh          = self.hInputGeom.asMesh()
		inMeshFn        = om.MFnMesh(inMesh)

		handle       = dataBlock.inputValue(self.inBaseMesh)
		inBaseMesh   = handle.asMesh()
		inBaseMeshFn =  om.MFnMesh(inBaseMesh)
			
		#GET IN POINTS
		inMPointsArray = om.MFloatPointArray()	
		inMeshFn.getPoints( inMPointsArray , om.MSpace.kWorld )		

		self.inPoints = []
		for i in range( 0 , inMPointsArray.length() ):
			self.inPoints.append( om.MFloatVector(inMPointsArray[i]) )

		#GET BASE POINTS		
		baseMPointsArray = om.MFloatPointArray()
		inBaseMeshFn.getPoints( baseMPointsArray , om.MSpace.kWorld )

		self.basePoints = []
		for i in range( 0 , baseMPointsArray.length() ):
			self.basePoints.append( om.MFloatVector(baseMPointsArray[i]) )

		#GET NBR POINTS
		self.nbrPoints = inMPointsArray.length()
		#GET IN NORMALS
		inMVectorArray = om.MFloatVectorArray()	
		inMeshFn.getNormals( inMVectorArray , om.MSpace.kWorld )		
								
		self.inNormals = []
		for i in range( 0 , inMVectorArray.length() ):
			self.inNormals.append( inMVectorArray[i] )


		#___________________________DEFORM	
		if( cache == 0 ):
			#POINT INFO					
 			self.outPoints   = self.inPoints
			self.StorePoints = utils.DynamicStore( arrayFill = self.inPoints , maxIndex = momentumMaxMemory ) 
			#TOPOLOGY INFO
			linkExpand = 1
			self.topologyNeighbourIndexes     = utils.getTopologyNeighbourIndexes( inBaseMesh , topoType , linkExpand  )
			self.topologyNeighbourBaseLenghts = utils.getTopologyNeighbourLenghts( self.basePoints , self.topologyNeighbourIndexes  )
			self.topologyNeighbourLock = [ 0 for i in range( 0 , len(self.topologyNeighbourIndexes) ) ] 
			#VOLUME INFO
			baseBB = utils.getBoundingBox(self.basePoints)				
			baseBBbarycentre = utils.getBarycentre(baseBB)	 
			self.baseDistanceCumulate = utils.cumulateDistance(self.basePoints , baseBBbarycentre)	 
		else:

			#___________________________________FORCES
			#VOLUME
			inBBbarycentre = om.MFloatVector( 0 , 0 , 0 )
			lPressurePerVtx = 0
			if not( pressure == 0 ):
				inBB   = sutils.getBoundingBox(self.inPoints)
				outBB  = utils.getBoundingBox(self.outPoints)							 
				inBBbarycentre   = utils.getBarycentre(inBB)	 
				outBBbarycentre   = utils.getBarycentre(outBB)		 
				outDistanceCumulate   = utils.cumulateDistance(self.outPoints , outBBbarycentre)			
				deltaDistanceCumulate = outDistanceCumulate - self.baseDistanceCumulate
				lPressurePerVtx = deltaDistanceCumulate / self.nbrPoints  

			#MOMENTUM
			vMomentums = []
			while not iter.isDone():
				i = iter.index()
				vMomentum = om.MFloatVector( 0 , 0 , 0 )
				for ia in range( 0 , momentumAverageSize + 1 ):
					indexStore = momentumPastSample + ia 
					vMomentum += self.StorePoints[indexStore][i] - self.StorePoints[indexStore+1][i]
				vMomentum = vMomentum / ( momentumAverageSize + 1 )
				vMomentums.append(vMomentum)
				iter.next()

			#APPLY FORCES
			outPointsForces = []
			for i in range( 0 , len( self.outPoints ) ):
				p  = self.outPoints[i]
				bp = self.inPoints[i]
				n  = self.inNormals[i]

				#MOMENTUM 
				p = p + vMomentums[i] 
				#FRICTION
				vFriction = vMomentums[i] * -1 * friction
				p         = p + vFriction
				#GRAVITY
				wG  = utils.clamp ( 0,1 , self.vGravity*n ) 
				vG  = self.vGravity * wG * mass 
				p   = p + vG 				
				#BIND
				vBind = utils.getAttractForce( p , bp ,  power = bindElasticity  ) 
				p = p + vBind;	
				#ATMOSPHERIc PRESSURE 
				vPressure = utils.getAttractForce( p , inBBbarycentre , overrideLength = lPressurePerVtx )
				vPressure = vPressure * pressure  
				p = p + vPressure;					

				outPointsForces.append( p )			


			#debug
			self.topologyNeighbourIndexes[21] = []	

			#___________________________________TOPOLOGY
			self.topologyNeighbourIndexes , self.topologyNeighbourLock = utils.topologyNeighbourIndexesReorder( outPointsForces , self.topologyNeighbourIndexes, self.topologyNeighbourBaseLenghts ,  self.topologyNeighbourLock ) 	
			outPointsTopo = outPointsForces[:]

			tnIs = self.topologyNeighbourIndexes
			tnLs = self.topologyNeighbourBaseLenghts
			for e in range( 0 , nbrLinkEval ):
				outPointsTopoTmp = outPointsTopo[:]
				#FOR EACH POINT
				for i in range( 0 , len( self.outPoints ) ):								
					barycentre  = outPointsTopo[i]   
					nbrToDivide = 1  	
					#FOR EACH TOPO LINK
					for tnI , tnL in zip(tnIs[i] , tnLs[i]):
						#COMPUTE FORCES
						if( recomputeLink == 1 ): point = outPointsTopoTmp[i]	
						else:                     point = outPointsTopo[i]
						vAttract = utils.getAttractForce( point , outPointsTopo[tnI] , triggerDist = tnL , power = linkElasticity , globalIter = nbrLinkEval , repulsion = 0  )					
						vRepulse = utils.getAttractForce( point , outPointsTopo[tnI] , triggerDist = tnL , power = linkRepulsion , globalIter = nbrLinkEval  , repulsion = 1  )					
						#APPLY FORCES
						if( topoMode == 'add' ):
							outPointsTopoTmp[i] = outPointsTopoTmp[i] + vAttract + vRepulse

						if( topoMode == 'edgeLength' ):
							outPointsTopoTmp[i]   = outPointsTopoTmp[i]   + vAttract/2 + vRepulse/2
							outPointsTopoTmp[tnI] = outPointsTopoTmp[tnI] - vAttract/2 - vRepulse/2

						if( topoMode == 'relax' ):
							if not( linkElasticity == 0 ):
								barycentre = barycentre + outPointsTopoTmp[i] + vAttract
								nbrToDivide += 1
							if not( linkRepulsion == 0 ):	
								barycentre = barycentre + outPointsTopoTmp[i] + vRepulse
								nbrToDivide += 1

						if( topoMode == 'smooth' ):	
							barycentre = barycentre + outPointsTopoTmp[tnI]
							nbrToDivide += 1

					if( topoMode == 'relax' )or( topoMode == 'smooth' ):
						outPointsTopoTmp[i] = barycentre / nbrToDivide


									
				
				outPointsTopo = outPointsTopoTmp[:] 	




			#___________________________________OUT
			iter.reset()
			outPoints = outPointsTopo[:]
			while not iter.isDone():
				i = iter.index()
				outPoints[i] = outPoints[i]  * envelope + self.inPoints[i] * ( 1.0 - envelope )
				iter.setPosition(om.MPoint(outPoints[i]))
				iter.next()


			#STORE MATRICES FOR THE NEXT EVAL	
			self.StorePoints.addFirst( self.outPoints )
			self.outPoints       = outPoints[:]




		return True



	@classmethod
	def nodeCreator(cls):
		print( 'nodeCreator' , cls )
		return omMPx.asMPxPtr( cls() )

	@classmethod
	def nodeInitializer(cls):
		print( 'nodeInitializer' , cls )
		nData = om.MFnNumericData()
		cData = om.MFnNurbsCurveData() 
		mData = om.MFnMeshData() 
	
		nAttr = om.MFnNumericAttribute()  
		eAttr = om.MFnEnumAttribute()
		mAttr = om.MFnMatrixAttribute()
		gAttr = om.MFnGenericAttribute()
		tAttr = om.MFnTypedAttribute()  
	
	
		mNumData = om.MFnNumericData()
		# IN ATTR
		cls.inBaseMesh = gAttr.create( "inBaseMesh", "inBase" )
		gAttr.addDataAccept( om.MFnData.kMesh )
		gAttr.setKeyable(True)
	
		cls.attrInCache = nAttr.create( 'cache' , 'cache' , nData.kInt , 0 )
		nAttr.setKeyable(True)        
		nAttr.setChannelBox(True)      
		nAttr.setMin(0)            
		nAttr.setMax(1)

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
		
		cls.attrInBindElasticity = nAttr.create( 'bindElasticity' , 'bindElasticity' , nData.kFloat  , 0.6 )
		nAttr.setKeyable(True)        
		nAttr.setChannelBox(True)      
		nAttr.setMin(0.0)               
		nAttr.setMax(1.0) 

		cls.attrInPressure = nAttr.create( 'pressure' , 'pressure' , nData.kFloat  , 0.0 )
		nAttr.setKeyable(True)        
		nAttr.setChannelBox(True)      
		nAttr.setMin(0.0)               
		nAttr.setMax(1.0) 		

		cls.topoMode = [ 'add' , 'edgeLength' , 'relax' , 'smooth' ]
		cls.attrInTopoMode = eAttr.create( 'modeTopo' , 'modeTopo' )
		for i in range( 0 , len(cls.topoMode) ): eAttr.addField( cls.topoMode[i] , i )             
		eAttr.setKeyable(True)          
		eAttr.setChannelBox(True)  

		cls.topoType = [ 'edge' , 'face' , 'volume']
		cls.attrInTopoType = eAttr.create( 'topoType' , 'topoType' )
		for i in range( 0 , len(cls.topoType) ): eAttr.addField( cls.topoType[i] , i )             
		eAttr.setKeyable(True)          
		eAttr.setChannelBox(True)  

		cls.attrInRecomputeLink = nAttr.create( 'recomputeLink' , 'recomputeLink' , nData.kInt  , 0 )
		nAttr.setKeyable(True)        
		nAttr.setChannelBox(True)        
		nAttr.setMin(0)    
		nAttr.setMax(1) 


		cls.attrInNbrLinkEval = nAttr.create( 'nbrLinkEval' , 'nbrLinkEvalclamp' , nData.kInt  , 5.0 )
		nAttr.setKeyable(True)        
		nAttr.setChannelBox(True)        
		nAttr.setMin(0)    
		nAttr.setMax(20) 

		cls.attrInLinkElasticity = nAttr.create( 'linkElasticity' , 'linkElasticity' , nData.kFloat  , 0.6 )
		nAttr.setKeyable(True)        
		nAttr.setChannelBox(True)     
		nAttr.setMin(0.0)   		
		nAttr.setMax(1.0)

		cls.attrInLinkRepulsion = nAttr.create( 'linkRepulsion' , 'linkRepulsion' , nData.kFloat  , 0.6 )
		nAttr.setKeyable(True)        
		nAttr.setChannelBox(True)     
		nAttr.setMin(0.0)            
		nAttr.setMax(1.0)		


		cls.addAttribute( cls.inBaseMesh        )
		cls.addAttribute( cls.attrInCache        )
		cls.addAttribute( cls.attrInMomentumPastSample )
		cls.addAttribute( cls.attrInMomentumAverageSize )		
		cls.addAttribute( cls.attrInFriction        )
		cls.addAttribute( cls.attrInMass            )
		cls.addAttribute( cls.attrInBindElasticity  )
		cls.addAttribute( cls.attrInPressure )
		cls.addAttribute( cls.attrInTopoType    )		
		cls.addAttribute( cls.attrInRecomputeLink    )				
		cls.addAttribute( cls.attrInNbrLinkEval     )
		cls.addAttribute( cls.attrInLinkElasticity      )	
		cls.addAttribute( cls.attrInLinkRepulsion       )
		cls.addAttribute( cls.attrInTopoMode       )	

		outputGeom = omMPx.cvar.MPxGeometryFilter_outputGeom
		cls.attributeAffects( cls.inBaseMesh        , outputGeom )
		cls.attributeAffects( cls.attrInCache       , outputGeom )
		cls.attributeAffects( cls.attrInMomentumPastSample       , outputGeom )		
		cls.attributeAffects( cls.attrInMomentumAverageSize       , outputGeom )			
		cls.attributeAffects( cls.attrInFriction    , outputGeom )
		cls.attributeAffects( cls.attrInMass        , outputGeom )
		cls.attributeAffects( cls.attrInBindElasticity  , outputGeom )
		cls.attributeAffects( cls.attrInPressure  , outputGeom )	
		cls.attributeAffects( cls.attrInTopoMode   , outputGeom )		
		cls.attributeAffects( cls.attrInTopoType   , outputGeom )
		cls.attributeAffects( cls.attrInRecomputeLink   , outputGeom )					
		cls.attributeAffects( cls.attrInNbrLinkEval , outputGeom )
		cls.attributeAffects( cls.attrInLinkElasticity   , outputGeom )
		cls.attributeAffects( cls.attrInLinkRepulsion   , outputGeom )



def initializePlugin(mobject):
	mplugin = omMPx.MFnPlugin(mobject)
	try:
		mplugin.registerNode( kPluginNodeTypeName, dynamicSkinId, dynamicSkin.nodeCreator, dynamicSkin.nodeInitializer, omMPx.MPxNode.kDeformerNode )
	except:
		sys.stderr.write( "Failed to register node: %s\n" % kPluginNodeTypeName )

def uninitializePlugin(mobject):
	mplugin = omMPx.MFnPlugin(mobject)
	try:
		mplugin.deregisterNode( dynamicSkinId )
	except:
		sys.stderr.write( "Failed to unregister node: %s\n" % kPluginNodeTypeName )
        
        

