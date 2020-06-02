	
'''

import python
from python.script.animDynamicTool import *
reload(python.script.animDynamicTool )

mc.file( 'D:/mcantat_BDD/projects/test/animDynamicTool01.ma' , o = True , f = True )

animDynamicTool( ['pCube1' , 'pCube2'] )

'''


import maya.cmds as mc
import maya.OpenMaya as om
from ..plugIn import utilsMayaNodes as utils

def animDynamicTool( slaves ):

	mass     = 0
	friction = 0.01
	attract  = 0.95
	repulse  = 0.9
	fixPointIndex   = [0]
	topologyNeighbourIndexes     = [[],[0]]	
	topologyNeighbourBaseLenghts = [[],[6.711]] 

	startFrame = int(mc.playbackOptions( q = True , min = True ))
	endFrame   = int(mc.playbackOptions( q = True , max = True ))

	attributes  = ["translateX","translateY","translateZ"]

	vGravity = om.MFloatVector(0,-1,0)

	#INIT
	mc.currentTime(startFrame)

	outPoints = []
	for i in range( 0 , len(slaves) ):	
		position = mc.xform( slaves[i] , ws = True , t = True , q = True )
		outPoints.append( om.MFloatPoint( position[0] , position[1] , position[2] ) )

	StorePoints = utils.DynamicStore( arrayFill = outPoints , maxIndex = 3 )


	#COMPUTE
	for f in range( startFrame , endFrame ):
		mc.currentTime(f)

		for i in range( 0 , len(slaves) ):		
			if( i in fixPointIndex ):
				position = mc.xform( slaves[i] , ws = True , t = True , q = True )
				outPoints[i] = om.MFloatPoint( position[0] , position[1] , position[2] ) 


		# COMPUTE FORCE / NEW POSITION
		for i in range( 0 , len(slaves) ):
			if( i in fixPointIndex ):continue

			vMomentum = StorePoints[0][i] - StorePoints[1][i]
			vWeight   = vGravity * mass
			vFriction = vMomentum * -1.0 * friction
			print( 'vMomentum' , vMomentum.x , vMomentum.y , vMomentum.z )

			outPoints[i] = outPoints[i] + vMomentum + vWeight + vFriction


		attractIter     = 1
		attractEnvelope = 1
		outPoints       = utils.applyTopologyAdd( outPoints , fixPointIndex , attractEnvelope , attract , repulse , attractIter , topologyNeighbourIndexes , topologyNeighbourBaseLenghts )

		StorePoints.addFirst( outPoints )

		#ADD KEY
		for i in range( 0 , len(slaves) ):
			if( i in fixPointIndex ):continue

			trsfTmp = mc.createNode( 'transform' , n = 'animDynamicTool_trsfTmp' )
			mc.setAttr( trsfTmp + '.translateX' , outPoints[i].x )
			mc.setAttr( trsfTmp + '.translateY' , outPoints[i].y )
			mc.setAttr( trsfTmp + '.translateZ' , outPoints[i].z )

			constrTmp = mc.parentConstraint( trsfTmp , slaves[i] , mo = 0)

			mc.setKeyframe( slaves[i] , v = mc.getAttr( slaves[i] + '.translateX') , at = '.translateX'  )
			mc.setKeyframe( slaves[i] , v = mc.getAttr( slaves[i] + '.translateY') , at = '.translateY'  )
			mc.setKeyframe( slaves[i] , v = mc.getAttr( slaves[i] + '.translateZ') , at = '.translateZ'  )
			mc.delete(constrTmp)

'''
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

'''