"""

delete "slidingCluster1";
flushUndo;

unloadPluginWithCheck( "/u/dm2/Users/nicolasb/Sandbox/Labo/scripts/slidingCluster.py" );
loadPlugin( "/u/dm2/Users/nicolasb/Sandbox/Labo/scripts/slidingCluster.py" );

select pPlane1;
deformer -type "slidingCluster";


connectAttr -f locator1.worldMatrix[0] slidingCluster1.matrix;
connectAttr -f locator1.parentInverseMatrix slidingCluster1.bindPreMatrix;


select -r locator1 ;

This node is a cluster


"""
import math, sys, array, copy
import maya.OpenMaya as om
import maya.OpenMayaAnim as omAnim
import maya.OpenMayaMPx as omMPx
from maya.mel import eval as meval
import time

kPluginNodeTypeName = "slidingCluster"

slidingClusterDeformerId = om.MTypeId(0x0010A51B)

# Node definition
class slidingCluster(omMPx.MPxDeformerNode):

	#node's variables
	thisNode		 = om.MObject()
	weight			 = om.MObject()
	positions		 = om.MPointArray()
	vecNormal		 = om.MVector() 
	closestMPtn		 = om.MPointOnMesh()

	#empty variables creation for first run
	envelopeHandle	= None
	hInputGeom		= None
	firstTime		= 1

	def __init__(self):
		omMPx.MPxDeformerNode.__init__(self)

	def deform( self, dataBlock, iter, matrix, index ):

		#inputs
		envelope = omMPx.cvar.MPxDeformerNode_envelope

		parentMatrix	  = dataBlock.inputValue(self.matrix).asMatrix()
		parentInvMatrix	  = dataBlock.inputValue(self.bindPreMatrix).asMatrix()
		refMatrix		  = parentInvMatrix * parentMatrix
		
		input  = omMPx.cvar.MPxDeformerNode_input
		hInput = dataBlock.inputArrayValue(input)
		hInput.jumpToArrayElement(index)

		inputGeom  = omMPx.cvar.MPxDeformerNode_inputGeom
		groupId	   = omMPx.cvar.MPxDeformerNode_groupId

		hInputElement	= hInput.inputValue()
		self.hInputGeom = hInputElement.child(inputGeom)

		inMesh	 = self.hInputGeom.asMesh()
		inRawMeshFn = om.MFnMesh(inMesh)

        smoothOptions	= om.MMeshSmoothOptions()
		smoothOptions.setDivisions( smoothLevel )
		smoothOptions.setSmoothness( 1 )
		#
		# get smooth mesh from inputGeom
		smoothGeom	   = om.MObject( oInputGeom )
		om.MFnMesh( oInputGeom ).generateSmoothMesh( smoothGeom, smoothOptions )
		#
		# get FnMesh from smooth mesh	
		#
		# get FnMesh from smooth mesh	
		#fnMesh			= om.MFnMesh( smoothGeom )
		smoothMesh	   = smoothGeom.asMesh()

		
		intersector = om.MMeshIntersector()
		intersector.create(smoothGeom)
		
		positions		 = om.MPointArray()

		#test first time
		if self.firstTime == 1:

			self.initializeSelfVariables(dataBlock, envelope)
			inRawMeshFn.getPoints(positions,om.MSpace.kObject)
			self.firstTime = 0			

		envelopeValue	  = self.envelopeHandle.asFloat()	

		#compute
		if envelopeValue!=0:
			
			#compute's variables
			#weight = self.weight.asFloat()

			iter.allPositions(positions)

			while not iter.isDone():

				iIndex	   = iter.index()
				pntWeight  = self.weightValue( dataBlock, index, iIndex)
				pos		   = positions[iIndex]
				 
				posDisp			  = pos * refMatrix

				vDisp	   = pos - posDisp

				
				
				inRawMeshFn.getVertexNormal(iter.index(), False, self.vecNormal, om.MSpace.kWorld)
				 
				planeDum = om.MPlane()
				planeDum.setPlane(self.vecNormal, 0.0)
				
				distance = planeDum.directedDistance( vDisp )
				
				ptOnPlane = (self.vecNormal * distance)
				
				
				vecMove = vDisp-ptOnPlane




				closestMPtn = om.MPointOnMesh()

				intersector.getClosestPoint((pos-vecMove), self.closestMPtn)

				closestPtn = om.MPoint(self.closestMPtn.getPoint())
				
				vecMove = pos-closestPtn

				pos = (pos - (vecMove* pntWeight * envelopeValue ))

				
				
				positions[iIndex].x = pos[0]
				positions[iIndex].y = pos[1]
				positions[iIndex].z = pos[2]

				iter.next()

			iter.setAllPositions(positions)

	def initializeSelfVariables(self, dataBlock, envelope):

		om.MGlobal.executeCommand( "makePaintable -attrType multiFloat -sm deformer slidingCluster weights;" )

		self.thisNode		   = self.thisMObject()		  
		self.envelopeHandle	   = dataBlock.inputValue( envelope )
		self.weight			   = om.MPlug(self.thisNode, slidingCluster.weight)
		self.firstTime = 0

		print "First init"
	  
def nodeCreator():
	return omMPx.asMPxPtr( slidingCluster() )


def nodeInitializer():


	gAttr = om.MFnMatrixAttribute()
	slidingCluster.bindPreMatrix = gAttr.create( "bindPreMatrix", "bpm")

	gAttr = om.MFnMatrixAttribute()
	slidingCluster.matrix = gAttr.create( "matrix", "mx")

	outputGeom = omMPx.cvar.MPxDeformerNode_outputGeom

	slidingCluster.addAttribute( slidingCluster.matrix )
	slidingCluster.addAttribute( slidingCluster.bindPreMatrix )
	
	slidingCluster.attributeAffects( slidingCluster.matrix, outputGeom )
	slidingCluster.attributeAffects( slidingCluster.bindPreMatrix, outputGeom )
	
def initializePlugin(mobject):
	mplugin = omMPx.MFnPlugin(mobject)
	try:
		mplugin.registerNode( kPluginNodeTypeName, slidingClusterDeformerId, nodeCreator, nodeInitializer, omMPx.MPxNode.kDeformerNode )
	except:
		sys.stderr.write( "Failed to register node: %s\n" % kPluginNodeTypeName )

def uninitializePlugin(mobject):
	mplugin = omMPx.MFnPlugin(mobject)
	try:
		mplugin.deregisterNode( slidingClusterDeformerId )
	except:
		sys.stderr.write( "Failed to unregister node: %s\n" % kPluginNodeTypeName )
