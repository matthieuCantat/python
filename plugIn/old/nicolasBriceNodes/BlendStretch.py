"""

delete "BlendStretchDeformer1";
flushUndo;


unloadPluginWithCheck( "D:/Autorig/rig/BlendStretch.py" );
loadPlugin( "D:/Autorig/rig/BlendStretch.py" );

delete "createColorSet1";
BlendStretchDeformer;


connectAttr "compShape.outMesh" "BlendStretchDeformer1.compressionShape";
connectAttr "tensShape.outMesh" "BlendStretchDeformer1.tensionShape";
setAttr "BlendStretchDeformer1.stretchDeformation" 0;



"""
"""

	This node is a tension based stretch deformer.
	It's based on the face-vertices tension to push/pull points along their normal while vertex-edges stretch or compress.

	"buldge" is the mult factor for pushing/pulling points allong their normal
	"deformTest" switch the stertchDeformation state ON/OFF
	"colorTest" switch the colors display ON/OFF
	"colorFactor" is the mul factor for colors

	bellow the Node is the proc wich correctly sets the deformer.
	Select a mesh an exec BlendStretchDeformer;

TO DO:check for shape connections / get better colors control
sphere primitive performance

i7
deform = 42
color = 26
color+deform = 28

Octo
deform = 59
color = 39
color+deform = 36
"""
########################################################################################
########################################################################################

import math, sys, copy
import maya.OpenMaya as om
import maya.OpenMayaAnim as omAnim
import maya.OpenMayaMPx as omMPx
from maya.mel import eval as meval
import time

########################################################################################
########################################################################################

kPluginNodeTypeName = "BlendStretchDeformer"
BlendStretchDeformerId = om.MTypeId(0x001AA92B)

########################################################################################
########################################################################################

# Node definition
class BlendStretchDeformer(omMPx.MPxDeformerNode):


########################################################################################
########################################################################################


	def __init__(self):
		# Node definition
		self.thisNode  = om.MObject()

		# nodes's attributs

		self.deformTest				= om.MObject()
		self.stretchFactor			= om.MObject()
		self.blendTypeTest			= om.MObject()
		self.tensDeformTest			= om.MObject()
		self.compDeformTest			= om.MObject()
		self.tensionFactor			= om.MObject()
		self.compressionFactor		= om.MObject()
		self.tensionWeightArray		= om.MDoubleArray()
		self.compressionWeightArray = om.MDoubleArray()
		self.colorTest				= om.MObject()
		self.colorFactor			= om.MObject()

		# points variables
		# shape orig
		self.targetPoints  = om.MPointArray()			 # MPointArray for inMesh's vertices current position
		self.refPoints	   = om.MPointArray()			 # MPointArray for inMesh's vertices reference position
		self.normals	   = om.MFloatVectorArray()		 # MFloatVectorArray for each vertex normal
		self.refNormals	   = om.MFloatVectorArray()
		self.targetPos	   = None						 # MPoint for shapeorig's per vertex position
		self.vtxIter	   = None						 # Init proc MItMeshVertex variable
		self.neighborsPnts = []							 # array for per vertex neighbors index
		self.distRef	   = []							 # array for per vertex neighbors distance
		self.faceVertices  = om.MIntArray()				 # MIntArray for face-vertex index									  :[0, 1, 3, 2, 2, 3, 5, 4, 4, 5,...]
		self.prim		   = om.MIntArray()				 # MIntArray for polygones index corresponding to self.faceVertices		:[0, 0, 0, 0, 1, 1, 1, 1, 2, 2,...]
		self.resultPoints  = om.MPointArray()			 # MPointArray for vertex position

		# Tension shape
		self.tensionPoints = om.MPointArray()

		#compresion shape
		self.compressionPoints = om.MPointArray()

		# colors
		self.refColorArray = om.MColorArray()			 # MColorArray for per vertex color
		self.resultColors  = om.MColorArray()			 # MColorArray for face-vertices colors
		self.poly		   = om.MIntArray()				 # MIntArray for polygones
		
		self.pntWeight = om.MObject()					 # variable for vertex paint weight

		self.firstTime = 1								 # compute's init variable

		omMPx.MPxDeformerNode.__init__(self)

########################################################################################
########################################################################################

	def deform( self, dataBlock, iter, matrix, index ):

		self.thisNode  = self.thisMObject()

		# get inMesh infos
		input  = omMPx.cvar.MPxDeformerNode_input
		hInput = dataBlock.inputArrayValue(input)
		hInput.jumpToArrayElement(index)

		# get attributs data
		self.deformTest		   = dataBlock.inputValue(BlendStretchDeformer.stretchDeformation).asShort()
		self.blendTypeTest	   = dataBlock.inputValue(BlendStretchDeformer.blendType).asShort()
		self.tensDeformTest	   = dataBlock.inputValue(BlendStretchDeformer.tensionDeformation).asShort()
		self.compDeformTest	   = dataBlock.inputValue(BlendStretchDeformer.compressionDeformation).asShort()
		self.colorTest		   = dataBlock.inputValue(BlendStretchDeformer.colorMap).asShort()
		self.stretchFactor	   = dataBlock.inputValue(BlendStretchDeformer.stretchFactor).asFloat()
		self.tensionFactor	   = dataBlock.inputValue(BlendStretchDeformer.tensionFactor).asFloat()
		self.compressionFactor = dataBlock.inputValue(BlendStretchDeformer.compressionFactor).asFloat()
		self.colorFactor	   = dataBlock.inputValue(BlendStretchDeformer.colorFactor).asFloat()

		# envelope
		env			   = omMPx.cvar.MPxDeformerNode_envelope
		envelope = dataBlock.inputValue(env).asFloat()

########################################################################################

		# input meshOrig
		inputGeom	  = omMPx.cvar.MPxDeformerNode_inputGeom
		hInputElement = hInput.inputValue()
		hInputGeom	  = hInputElement.child(inputGeom)
		inMesh		  = hInputGeom.asMesh()
		inMeshFn	  = om.MFnMesh(inMesh)

########################################################################################

		# output mesh
		outputGeom = omMPx.cvar.MPxDeformerNode_outputGeom
		hOutput	   = dataBlock.outputArrayValue(outputGeom)
		outMesh	   = hOutput.outputValue().asMesh()
		outMeshFn  = om.MFnMesh( outMesh)

########################################################################################

		# get target points coordinates /Normals
		inMeshFn.getPoints(self.targetPoints,om.MSpace.kObject)
		inMeshFn.getVertexNormals(False, self.normals, om.MSpace.kObject)

		# test first time
		if self.firstTime ==1:

			self.initializeSelfVariables(dataBlock, envelope, inMesh, inMeshFn)
			self.firstTime = 0

########################################################################################

		# Tension mesh data
		tensionShapeConnect = 0
		tensionShapeData	= dataBlock.inputValue(BlendStretchDeformer.tensionShape).asMesh()
		tensionPlugTest = om.MPlug(self.thisNode, BlendStretchDeformer.tensionShape)

		if tensionPlugTest.isConnected():

			tensionShapeFn		= om.MFnMesh(tensionShapeData)
			tensionShapeFn.getPoints(self.tensionPoints, om.MSpace.kObject)
			tensionShapeConnect = 1
		else:
			self.tensionPoints = copy.copy(self.refPoints)

		# Compression mesh data
		compressionShapeConnect = 0
		compressionShapeData  = dataBlock.inputValue(BlendStretchDeformer.compressionShape).asMesh()
		compressionPlugTest = om.MPlug(self.thisNode, BlendStretchDeformer.compressionShape)
		
		if compressionPlugTest.isConnected():
            
			compressionShapeFn		= om.MFnMesh(compressionShapeData)
			compressionShapeFn.getPoints(self.compressionPoints, om.MSpace.kObject)
			compressionShapeConnect = 1
		else:
			self.compressionPoints = copy.copy(self.refPoints)
			
########################################################################################

		# Getting the children (tension/compression) attributes of the compound attribute "blenStretchWeights"
		arrayDataHandle = dataBlock.inputArrayValue(BlendStretchDeformer.blendStretchWeights)

		# Correspond to BlendStretchDeformer.blendStretchWeights.blendStretchWeights[0]
		arrayDataHandle.jumpToArrayElement(0)

		tensElem = arrayDataHandle.inputValue().child(BlendStretchDeformer.tensionWeight)
		hTensElem = tensElem.data()
		tensionWeightArray= om.MFnDoubleArrayData(hTensElem).array()

		compElem = arrayDataHandle.inputValue().child(BlendStretchDeformer.compressionWeight)
		hCompElem = compElem.data()
		compressionWeightArray = om.MFnDoubleArrayData(hCompElem).array()

########################################################################################
		
		if envelope!=0:

			# deform's variables
			while not iter.isDone():

				index = iter.index()

				# get per vertex Position / normal / paint weight
				self.targetPos	  = self.targetPoints[iter.index()]
				self.pntWeight	  = self.weightValue( dataBlock, index, iter.index())
				tensionWeight	  = tensionWeightArray[iter.index()]
				compressionWeight = compressionWeightArray[iter.index()]
				normal			  = om.MVector(self.normals[iter.index()])
				refNormal		  = om.MVector(self.refNormals[iter.index()])
				pntTmp			  = om.MObject()
				
				# iter temp variables
				vtxColor = om.MColor()
				tension	 = 0.0

				# get vertex neighbors
				neighborList = len(self.neighborsPnts[index])

				# for each
				for i in xrange(neighborList):

					# get index
					neighborPos = self.neighborsPnts[index][i]

					# get current distance
					distCur = self.targetPos.distanceTo(self.targetPoints[neighborPos])

					# get tension
					distResTmp = distCur/self.distRef[index][i]
					tension += distResTmp

				# average tension
				tension /= neighborList

				# get vertex current position


				if self.deformTest == 1:
					# Get result position
					pntTmp = self.refPoints[index] + ( self.targetPoints[index] - self.refPoints[index] )
					pntTmp = pntTmp + (((normal * (1-tension)) * self.pntWeight * self.stretchFactor))

				if self.deformTest == 0:
					# Get result position
					pntTmp = copy.copy(self.targetPoints[index])

				if self.tensDeformTest == 1 and tension > 1 and tensionWeight > 0:
					# Get result position
					normalQuat = refNormal.rotateTo(normal)
					delta = self.tensionPoints[index] - self.refPoints[index]
					delta = delta.rotateBy(normalQuat)
					pntTmp = (pntTmp + (delta * ((tension-1) * self.tensionFactor * tensionWeight )))

				if self.compDeformTest == 1 and tension < 1 and compressionWeight > 0:
					# Get result position
					normalQuat = refNormal.rotateTo(normal)
					delta = self.compressionPoints[index] - self.refPoints[index]
					delta = delta.rotateBy(normalQuat)
					pntTmp = (pntTmp + (delta * ((1-tension) * self.compressionFactor * compressionWeight)))

				if self.colorTest == 1 and self.pntWeight > 0 and tension != 1:
					# Get color per vertex
					clampedR = max(min(((tension-1)*(self.colorFactor*2)), 1), 0)
					clampedB = max(min(((1-tension)*(self.colorFactor*2)), 1), 0)
					vtxColor.set(om.MColor.kRGB, clampedR, 0.0, clampedB, 1)
					self.refColorArray.set(copy.copy(vtxColor), index)

				#pntTmp = pntTmp * matrix
				self.resultPoints.append(pntTmp)

				iter.next()

			# Set positions
			iter.setAllPositions(self.resultPoints)

			if self.colorTest == 1:

				colorSetName = "BstretchColorSet"

				for i in self.faceVertices:
					# Get face-vertex colors
					self.resultColors.set(self.refColorArray[i], i)

				# Set colors
				outMeshFn.setFaceVertexColors(self.resultColors, self.prim, self.faceVertices)
				outMeshFn.assignColors(self.faceVertices, colorSetName)

			# Clear arrays
			self.resultPoints.clear()
			self.targetPoints.clear()

########################################################################################
########################################################################################

	# first compute init proc
	def initializeSelfVariables(self, dataBlock, envelope, inMesh, inMeshFn):


		# filling all the ref arrays
		############################
		
		# Get reference Normals
		inMeshFn.getVertexNormals(False, self.refNormals, om.MSpace.kObject)

		# get face-vertices
		polyNum = inMeshFn.numPolygons()
		polyVertices = om.MIntArray()
		num = 0

		for i in xrange(polyNum):

			self.poly.append(i)
			inMeshFn.getPolygonVertices(i, polyVertices)

			for j in xrange(polyVertices.length()):

				self.faceVertices.append(polyVertices[j])
				self.prim.append(i)
				
		# Init color for each face-vertex
		for i in range(self.faceVertices.length()):
			self.resultColors.append(om.MColor(1, 1, 1, 1))

		# DataHandle to outputArray attribute
		refPointsDataHandle = dataBlock.inputValue(BlendStretchDeformer.outputPtArray).data()

		# this node have a typedAttribute "outputArray" that keeps the per vertex neighbors distance between saves
		# If it is empty then fill it
		# If it isn't then copy it to a temp array "array"
		
		try:
			pointArrayData = om.MFnPointArrayData(refPointsDataHandle)

			print "------- STRETCH DEFORMER INIT -------"

		except:
			
			# Initialize refPoints array 
			pointArrayTmp	= om.MPointArray()
			pointArrayData	= om.MFnPointArrayData()
			arrayTmp		= pointArrayData.create(copy.copy(self.targetPoints))
			outputHandle	= dataBlock.outputValue(BlendStretchDeformer.outputPtArray)
			outputHandle.setMObject( arrayTmp )

			for i in range(self.targetPoints.length()):


				self.compressionWeightArray.append(1.0)
				self.tensionWeightArray.append(1.0)
				
			#################################################################################
			# Initialize custom paintable attributes										#
			# BlendStretchDeformer.tensionWeight and BlendStretchDeformer.compressionWeight #
			#################################################################################
			
			doubleArrayData			= om.MFnDoubleArrayData()
			arrayObjectTmp			 = doubleArrayData.create(copy.copy(self.tensionWeightArray))
			
			# Declare a attribute plug
			tensPlug = om.MPlug(self.thisNode, BlendStretchDeformer.tensionWeight)
		   
			# Get tension attribute via its parent Attribut
			tensPlug.selectAncestorLogicalIndex( 0, BlendStretchDeformer.blendStretchWeights )
			
			# Construct a MDataHandle from it
			tensHandle = tensPlug.constructHandle(dataBlock)
			
			# Set it
			tensHandle.setMObject(arrayObjectTmp)
			tensPlug.setMDataHandle(tensHandle)
			tensPlug.destructHandle(tensHandle)

			# Same job for the Compression
			doubleArrayData2 = om.MFnDoubleArrayData()
			arrayObjectTmp2	 = doubleArrayData2.create(copy.copy(self.compressionWeightArray))
			
			compPlug		 = om.MPlug(self.thisNode, BlendStretchDeformer.compressionWeight)
			compPlug.selectAncestorLogicalIndex( 0, BlendStretchDeformer.blendStretchWeights )
			compHandle = compPlug.constructHandle(dataBlock)
			compHandle.setMObject(arrayObjectTmp2)
			compPlug.setMDataHandle(compHandle)
			compPlug.destructHandle(compHandle)		  

			print "------- FIRST STRETCH DEFORMER INIT -------"


		# getting pointArrayData
		array = pointArrayData.array()

		for i in range(array.length()):

			self.refPoints.append(array[i])
			self.refColorArray.append(om.MColor(1, 1, 1, 1))

		# Mesh iterator declaration
		self.vtxIter = om.MItMeshVertex(inMesh)

		# getting neghbors points
		while not self.vtxIter.isDone():

			# getting per vertex neighbors to fill self.neighborsPnts
			vtxNeighbArray = om.MIntArray()

			index = self.vtxIter.index()
			self.vtxIter.getConnectedVertices(vtxNeighbArray)

			self.neighborsPnts.append(vtxNeighbArray)

			curdDistList  = []
			# for each neighbor get the distance from current vertex
			for i in range(vtxNeighbArray.length()):

				curPtn = self.neighborsPnts[index][i]
				curdDistList.append(self.refPoints[index].distanceTo(self.refPoints[curPtn]))

			self.distRef.append(copy.copy(curdDistList))

			self.vtxIter.next()





########################################################################################
################################################################################################################################################################################

def nodeCreator():
	return omMPx.asMPxPtr( BlendStretchDeformer() )

########################################################################################
########################################################################################

# initializer
def nodeInitializer():
	#thisNode = self.thisMObject()
	nAttr = om.MFnNumericAttribute()
	eAttr = om.MFnEnumAttribute()
	tAttr = om.MFnTypedAttribute()
	gAttr = om.MFnGenericAttribute()
	cAttr = om.MFnCompoundAttribute()

	BlendStretchDeformer.stretchDeformation = eAttr.create("stretchDeformation", "strtchDdef", 1)
	eAttr.addField('OFF', 0)
	eAttr.addField('ON', 1)
	eAttr.setKeyable(True)

	BlendStretchDeformer.stretchFactor = nAttr.create("stretchFactor", "strtchFact", om.MFnNumericData.kFloat, 1)
	nAttr.setKeyable(True)

	BlendStretchDeformer.blendType = eAttr.create("blendType", "blendType", 0)
	eAttr.addField('Freeze', 0)
	eAttr.addField('Interactive', 1)
	eAttr.setKeyable(True)

	BlendStretchDeformer.tensionDeformation = eAttr.create("tensionDeformation", "tensDeform", 1)
	eAttr.addField('OFF', 0)
	eAttr.addField('ON', 1)
	eAttr.setKeyable(True)

	BlendStretchDeformer.tensionFactor = nAttr.create("tensionFactor", "tensFact", om.MFnNumericData.kFloat, 1)
	nAttr.setKeyable(True)

	BlendStretchDeformer.compressionDeformation = eAttr.create("compressionDeformation", "compDeform", 1)
	eAttr.addField('OFF', 0)
	eAttr.addField('ON', 1)
	eAttr.setKeyable(True)

	BlendStretchDeformer.compressionFactor = nAttr.create("compressionFactor", "compFact", om.MFnNumericData.kFloat, 1)
	nAttr.setKeyable(True)

	BlendStretchDeformer.colorFactor = nAttr.create("colorFactor", "colorFact", om.MFnNumericData.kFloat, 1)
	nAttr.setKeyable(True)

	BlendStretchDeformer.colorMap = eAttr.create("colorMap", "cm", 0)
	eAttr.addField('OFF', 0)
	eAttr.addField('ON', 1)
	eAttr.setKeyable(True)

	BlendStretchDeformer.tensionShape = gAttr.create("tensionShape", "tenShape")
	gAttr.addDataAccept( om.MFnData.kMesh )

	BlendStretchDeformer.compressionShape = gAttr.create("compressionShape", "compShape")
	gAttr.addDataAccept( om.MFnData.kMesh )

	# This attribute keeps the refence distances between each point and his neighbors
	BlendStretchDeformer.outputPtArray = tAttr.create("outputPtArray", "opa", om.MFnPointArrayData.kPointArray)
	tAttr.setStorable(1)
	tAttr.setKeyable(0)
	tAttr.setHidden(1)

	# Those two attributes are the children of the compound attribute blendStretchWeights
	BlendStretchDeformer.tensionWeight = tAttr.create("tensionWeight", "tensWgt", om.MFnDoubleArrayData.kDoubleArray)
	tAttr.setStorable(1)
	tAttr.setHidden(0)
	#tAttr.setArray(1)

	BlendStretchDeformer.compressionWeight = tAttr.create("compressionWeight", "compWgt", om.MFnDoubleArrayData.kDoubleArray)
	tAttr.setStorable(1)
	tAttr.setHidden(0)
	#tAttr.setArray(1)
	
	# Compound attribute
	BlendStretchDeformer.blendStretchWeights = cAttr.create("blendStretchWeights", "bsWgts")
	cAttr.setArray(1)
	cAttr.addChild(BlendStretchDeformer.tensionWeight)
	cAttr.addChild(BlendStretchDeformer.compressionWeight)
	cAttr.setReadable(1)
	cAttr.setUsesArrayDataBuilder(1)


	BlendStretchDeformer.addAttribute(BlendStretchDeformer.stretchDeformation)
	BlendStretchDeformer.addAttribute(BlendStretchDeformer.stretchFactor)
	BlendStretchDeformer.addAttribute(BlendStretchDeformer.blendType)
	BlendStretchDeformer.addAttribute(BlendStretchDeformer.tensionDeformation)
	BlendStretchDeformer.addAttribute(BlendStretchDeformer.compressionDeformation)
	BlendStretchDeformer.addAttribute(BlendStretchDeformer.tensionFactor)
	BlendStretchDeformer.addAttribute(BlendStretchDeformer.compressionFactor)
	BlendStretchDeformer.addAttribute(BlendStretchDeformer.colorFactor)
	BlendStretchDeformer.addAttribute(BlendStretchDeformer.colorMap)
	BlendStretchDeformer.addAttribute(BlendStretchDeformer.tensionShape)
	BlendStretchDeformer.addAttribute(BlendStretchDeformer.compressionShape)
	BlendStretchDeformer.addAttribute(BlendStretchDeformer.outputPtArray)
	BlendStretchDeformer.addAttribute(BlendStretchDeformer.blendStretchWeights)

	outputGeom = omMPx.cvar.MPxDeformerNode_outputGeom

	BlendStretchDeformer.attributeAffects(BlendStretchDeformer.stretchDeformation, outputGeom )
	BlendStretchDeformer.attributeAffects(BlendStretchDeformer.stretchFactor, outputGeom )
	BlendStretchDeformer.attributeAffects(BlendStretchDeformer.colorMap, outputGeom )
	BlendStretchDeformer.attributeAffects(BlendStretchDeformer.blendType, outputGeom )
	BlendStretchDeformer.attributeAffects(BlendStretchDeformer.tensionDeformation, outputGeom )
	BlendStretchDeformer.attributeAffects(BlendStretchDeformer.compressionDeformation, outputGeom )
	BlendStretchDeformer.attributeAffects(BlendStretchDeformer.tensionFactor, outputGeom )
	BlendStretchDeformer.attributeAffects(BlendStretchDeformer.compressionFactor, outputGeom )
	BlendStretchDeformer.attributeAffects(BlendStretchDeformer.colorFactor, outputGeom )
	BlendStretchDeformer.attributeAffects(BlendStretchDeformer.tensionShape, outputGeom )
	BlendStretchDeformer.attributeAffects(BlendStretchDeformer.compressionShape, outputGeom )
	BlendStretchDeformer.attributeAffects(BlendStretchDeformer.tensionWeight, outputGeom )
	BlendStretchDeformer.attributeAffects(BlendStretchDeformer.compressionWeight, outputGeom )


   
	om.MGlobal.executeCommand( "makePaintable -attrType multiFloat -sm deformer BlendStretchDeformer weights;" )
	om.MGlobal.executeCommand( "makePaintable -attrType doubleArray -sm deformer BlendStretchDeformer tensionWeight;" )
	om.MGlobal.executeCommand( "makePaintable -attrType doubleArray -sm deformer BlendStretchDeformer compressionWeight;" )
########################################################################################
########################################################################################

# initialize the script plug-in
def initializePlugin(mobject):
	mplugin = omMPx.MFnPlugin(mobject)
	try:
		mplugin.registerNode( kPluginNodeTypeName, BlendStretchDeformerId, nodeCreator, nodeInitializer, omMPx.MPxNode.kDeformerNode )
	except:
		sys.stderr.write( "Failed to register node: %s\n" % kPluginNodeTypeName )

########################################################################################
########################################################################################

# uninitialize the script plug-in
def uninitializePlugin(mobject):
	mplugin = omMPx.MFnPlugin(mobject)
	try:
		mplugin.deregisterNode( BlendStretchDeformerId )
	except:
		sys.stderr.write( "Failed to unregister node: %s\n" % kPluginNodeTypeName )


mel = '''
global proc BlendStretchDeformer()
{
	string $sel[] = `ls -sl -tr`;
	for($obj in $sel)
	{
		string $BlendStretchDeformer[] = `cluster $obj`;

		polyColorSet -create -clamped 1 -rpt RGBA -colorSet "BstretchColorSet" $obj;

		delete $BlendStretchDeformer[0];
		string $BlendStretchDeformer[] = `deformer -type "BlendStretchDeformer" $obj`;
		setAttr ($obj + ".displayColors") 0;
		connectAttr -f ($BlendStretchDeformer[0] + ".colorMap") ($obj + ".displayColors");
	}
	
	


}'''

meval( mel )
