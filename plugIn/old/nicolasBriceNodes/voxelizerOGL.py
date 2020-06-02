"""
delete "transform1";
flushUndo;


unloadPluginWithCheck( "C:/Users/crabs/Desktop/voxelizer2.py" );
loadPlugin( "C:/Users/crabs/Desktop/voxelizer2.py" );

createNode voxelizer;
if(!`objExists pSphereShape1`)
{
	polySphere -r 2 -sx 20 -sy 20 -ax 0 1 0 -cuv 2 -ch 1;

}
connectAttr -f pSphereShape1.outMesh voxelizer1.inMesh;
connectAttr -f pCube1.boundingBoxMinX voxelizer1.inBoundingBoxMinX;
connectAttr -f pCube1.boundingBoxMinY voxelizer1.inBoundingBoxMinY;
connectAttr -f pCube1.boundingBoxMinZ voxelizer1.inBoundingBoxMinZ;

connectAttr -f pCube1.boundingBoxMaxX voxelizer1.inBoundingBoxMaxX;
connectAttr -f pCube1.boundingBoxMaxY voxelizer1.inBoundingBoxMaxY;
connectAttr -f pCube1.boundingBoxMaxZ voxelizer1.inBoundingBoxMaxZ;
ToDo:
	-Making glCube (done)
	-Making grid from boundingBox (done)
	- transfering the mesh query to the draw def ([MODIF])
	-Querying intersections (def)
"""

import sys
import math
import maya.OpenMaya as om
import maya.OpenMayaMPx as omMPx
import maya.OpenMayaRender as omRender
import maya.OpenMayaUI as omUI

nodeTypeName = "voxelizer"
nodeTypeId = om.MTypeId(0x87579)

# -Hardware Render Utils
glRenderer = omRender.MHardwareRenderer.theRenderer()
glFT = glRenderer.glFunctionTable()

# HardWare texture manager
glTM = omRender.MHwTextureManager

########################################################################################
########################################################################################

class voxelizer(omMPx.MPxLocatorNode):
	blurg = om.MObject()
	def __init__(self):

		omMPx.MPxLocatorNode.__init__(self)

########################################################################################
########################################################################################

	def makeGlCube(self, _position, _size, _depth):

		positionX = _position.x
		positionY = _position.y
		positionZ = _position.z

		#top plane
		glFT.glBegin(omRender.MGL_QUADS)
		glFT.glTexCoord2f(0.0, 0.0)
		glFT.glNormal3f( 0, -1.0, 0 )
		glFT.glVertex3f((positionX - (1.0 * _size)) , (positionY + (1.0 * _size)) , (positionZ - (1.0 * _size)) )

		glFT.glTexCoord2f(1.0, 0.0)
		glFT.glNormal3f( 0, -1.0, 0 )
		glFT.glVertex3f((positionX + (1.0 * _size)) , (positionY + (1.0 * _size)) , (positionZ - (1.0 * _size)) )

		glFT.glTexCoord2f(0.0, 1.0)
		glFT.glNormal3f( 0, -1.0, 0 )
		glFT.glVertex3f((positionX + (1.0 * _size)) , (positionY + (1.0 * _size)) , (positionZ + (1.0 * _size)) )

		glFT.glTexCoord2f(1.0, 1.0)
		glFT.glNormal3f( 0, -1.0, 0 )
		glFT.glVertex3f((positionX - (1.0 * _size)) , (positionY + (1.0 * _size)) , (positionZ + (1.0 * _size)) )


		#bottom plane
		glFT.glNormal3f( 0, -1.0, 0 )
		glFT.glVertex3f((positionX - (1.0 * _size)) , (positionY - (1.0 * _size)) , (positionZ - (1.0 * _size)) )

		glFT.glNormal3f( 0, -1.0, 0 )
		glFT.glVertex3f((positionX + (1.0 * _size)) , (positionY - (1.0 * _size)) , (positionZ - (1.0 * _size)) )

		glFT.glNormal3f( 0, -1.0, 0 )
		glFT.glVertex3f((positionX + (1.0 * _size)) , (positionY - (1.0 * _size)) , (positionZ + (1.0 * _size)) )

		glFT.glNormal3f( 0, -1.0, 0 )
		glFT.glVertex3f((positionX - (1.0 * _size)) , (positionY - (1.0 * _size)) , (positionZ + (1.0 * _size)) )

		#front plane

		glFT.glNormal3f( 0, 0, 1.0 )
		glFT.glTexCoord2d(0,1);
		glFT.glVertex3f((positionX - (1.0 * _size)) , (positionY - (1.0 * _size)) , (positionZ + (1.0)* _size))

		glFT.glTexCoord2d(0,0)
		glFT.glNormal3f( 0, 0, 1.0 )
		glFT.glVertex3f((positionX + (1.0 * _size)) , (positionY - (1.0 * _size)) , (positionZ + (1.0)* _size))

		glFT.glTexCoord2d(1,0)
		glFT.glNormal3f( 0, 0, 1.0 )
		glFT.glVertex3f((positionX + (1.0 * _size)) , (positionY + (1.0 * _size)) , (positionZ + (1.0)* _size))

		glFT.glTexCoord2d(1,1)
		glFT.glNormal3f( 0, 0, 1.0 )
		glFT.glVertex3f((positionX - (1.0 * _size)) , (positionY + (1.0 * _size)) , (positionZ + (1.0 * _size)) )


		#back plane
		glFT.glNormal3f( 0, 0, 1.0 )
		glFT.glVertex3f((positionX - (1.0 * _size)) , (positionY - (1.0 * _size)) , (positionZ - (1.0 * _size)) )

		glFT.glNormal3f( 0, 0, 1.0 )
		glFT.glVertex3f((positionX + (1.0 * _size)) , (positionY - (1.0 * _size)) , (positionZ - (1.0 * _size)) )

		glFT.glNormal3f( 0, 0, 1.0 )
		glFT.glVertex3f((positionX + (1.0 * _size)) , (positionY + (1.0 * _size)) , (positionZ - (1.0 * _size)) )

		glFT.glNormal3f( 0, 0, 1.0 )
		glFT.glVertex3f((positionX - (1.0 * _size)) , (positionY + (1.0 * _size)) , (positionZ - (1.0 * _size)) )

		#left plane
		glFT.glNormal3f( -1.0, 0, 0 )
		glFT.glVertex3f((positionX + (1.0 * _size)) , (positionY - (1.0 * _size)) , (positionZ + (1.0 * _size)) )

		glFT.glNormal3f( -1.0, 0, 0 )
		glFT.glVertex3f((positionX + (1.0 * _size)) , (positionY + (1.0 * _size)) , (positionZ + (1.0 * _size)) )

		glFT.glNormal3f( -1.0, 0, 0 )
		glFT.glVertex3f((positionX + (1.0 * _size)) , (positionY + (1.0 * _size)) , (positionZ - (1.0 * _size)) )

		glFT.glNormal3f( -1.0, 0, 0 )
		glFT.glVertex3f((positionX + (1.0 * _size)) , (positionY - (1.0 * _size)) , (positionZ - (1.0 * _size)) )

		#right plane
		glFT.glNormal3f( -1.0, 0, 0 )
		glFT.glVertex3f((positionX - (1.0 * _size)) , (positionY - (1.0 * _size)) , (positionZ + (1.0 * _size)) )

		glFT.glNormal3f( -1.0, 0, 0 )
		glFT.glVertex3f((positionX - (1.0 * _size)) , (positionY + (1.0 * _size)) , (positionZ + (1.0 * _size)) )

		glFT.glNormal3f( -1.0, 0, 0 )
		glFT.glVertex3f((positionX - (1.0 * _size)) , (positionY + (1.0 * _size)) , (positionZ - (1.0 * _size)) )

		glFT.glNormal3f( -1.0, 0, 0 )
		glFT.glVertex3f((positionX - (1.0 * _size)) , (positionY - (1.0 * _size)) , (positionZ - (1.0 * _size)) )

		glFT.glEnd()

		if _depth == 0:
			glFT.glDisable(omRender.MGL_DEPTH_TEST)

		# -Wireframe Lines

########################################################################################
########################################################################################

	def mageGlContour(self, _position, _size, _wireframe):
		if _wireframe != 0:

			glFT.glLineWidth(_wireframe)

			glFT.glBegin(omRender.MGL_LINES)

			positionX = _position.x
			positionY = _position.y
			positionZ = _position.z

			#top line
			glFT.glVertex3f((positionX - (1.0 * _size)) , (positionY + (1.0 * _size)) , (positionZ - (1.0 * _size)) )
			glFT.glVertex3f((positionX + (1.0 * _size)) , (positionY + (1.0 * _size)) , (positionZ - (1.0 * _size)) )

			glFT.glVertex3f((positionX + (1.0 * _size)) , (positionY + (1.0 * _size)) , (positionZ + (1.0 * _size)) )
			glFT.glVertex3f((positionX - (1.0 * _size)) , (positionY + (1.0 * _size)) , (positionZ + (1.0 * _size)) )

			glFT.glVertex3f((positionX + (1.0 * _size)) , (positionY + (1.0 * _size)) , (positionZ - (1.0 * _size)) )
			glFT.glVertex3f((positionX + (1.0 * _size)) , (positionY + (1.0 * _size)) , (positionZ + (1.0)		   * _size))

			glFT.glVertex3f((positionX - (1.0 * _size)) , (positionY + (1.0 * _size)) , (positionZ - (1.0 * _size)) )
			glFT.glVertex3f((positionX - (1.0 * _size)) , (positionY + (1.0 * _size)) , (positionZ + (1.0 * _size)) )

			#bottom line
			glFT.glVertex3f((positionX - (1.0 * _size)) , (positionY - (1.0 * _size)) , (positionZ - (1.0 * _size)) )
			glFT.glVertex3f((positionX + (1.0 * _size)) , (positionY - (1.0 * _size)) , (positionZ - (1.0 * _size)) )

			glFT.glVertex3f((positionX + (1.0 * _size)) , (positionY - (1.0 * _size)) , (positionZ + (1.0 * _size)) )
			glFT.glVertex3f((positionX - (1.0 * _size)) , (positionY - (1.0 * _size)) , (positionZ + (1.0 * _size)) )

			glFT.glVertex3f((positionX + (1.0 * _size)) , (positionY - (1.0 * _size)) , (positionZ - (1.0 * _size)) )
			glFT.glVertex3f((positionX + (1.0 * _size)) , (positionY - (1.0 * _size)) , (positionZ + (1.0 * _size)) )

			glFT.glVertex3f((positionX - (1.0 * _size)) , (positionY - (1.0 * _size)) , (positionZ - (1.0 * _size)) )
			glFT.glVertex3f((positionX - (1.0 * _size)) , (positionY - (1.0 * _size)) , (positionZ + (1.0 * _size)) )

			#front line
			glFT.glVertex3f((positionX + (1.0 * _size)) , (positionY + (1.0 * _size)) , (positionZ + (1.0 * _size)) )
			glFT.glVertex3f((positionX + (1.0 * _size)) , (positionY - (1.0 * _size)) , (positionZ + (1.0 * _size)) )

			glFT.glVertex3f((positionX - (1.0 * _size)) , (positionY + (1.0 * _size)) , (positionZ + (1.0 * _size)) )
			glFT.glVertex3f((positionX - (1.0 * _size)) , (positionY - (1.0 * _size)) , (positionZ + (1.0 * _size)) )

			#front line
			glFT.glVertex3f((positionX + (1.0 * _size)) , (positionY + (1.0 * _size)) , (positionZ - (1.0 * _size)) )
			glFT.glVertex3f((positionX + (1.0 * _size)) , (positionY - (1.0 * _size)) , (positionZ - (1.0 * _size)) )

			glFT.glVertex3f((positionX - (1.0 * _size)) , (positionY + (1.0 * _size)) , (positionZ - (1.0 * _size)) )
			glFT.glVertex3f((positionX - (1.0 * _size)) , (positionY - (1.0 * _size)) , (positionZ - (1.0 * _size)) )

			glFT.glEnd()

########################################################################################
########################################################################################

	def createVoxelsPos(self, _mesh, _size, _bBoxMin, _bBoxMax ):

		xmin = _bBoxMin.x
		ymin = _bBoxMin.y
		zmin = _bBoxMin.z
		xmax = _bBoxMax.x
		ymax = _bBoxMax.y
		zmax = _bBoxMax.z

		voxelSize = _size/2

		# -Center --> Cote (demie longueur)
		xDist = (xmax-xmin)
		yDist = (ymax-ymin)
		zDist = (zmax-zmin)

		# -Nombre de voxels par demie longueur
		xNum = math.ceil(((xDist/_size)/2))
		yNum = math.ceil(((yDist/_size)/2))
		zNum = math.ceil(((zDist/_size)/2))

		voxPosArray = om.MPointArray()
		
		# -Create Voxel Positions for given size
		for x in range(int(xNum)):
			xPos    = (_size/2.0 + (_size  * (x))) + (xmax+xmin)/2
			xNegPos = -(_size/2.0 + (_size * (x))) + (xmax+xmin)/2

			for y in range(int(yNum)):
				yPos    = (_size/2.0 + (_size * (y))) + (ymax+ymin)/2
				yNegPos = -(_size/2.0 + (_size * (y))) + (ymax+ymin)/2

				for z in range(int(zNum)):
					zPos    = (_size/2.0 + (_size * (z))) + (zmax+zmin)/2
					zNegPos = -(_size/2.0 + (_size * (z))) + (zmax+zmin)/2
					
					# -For each axis, in negative and positive direction
					pos    = om.MPoint(xPos, yPos, zPos)
					negPos = om.MPoint(xNegPos, yNegPos, zNegPos)

					posY    = om.MPoint(xNegPos, yPos, zNegPos)
					posNegY = om.MPoint(xPos, yNegPos, zPos)

					posZ    = om.MPoint(xNegPos, yPos, zPos)
					posNegZ = om.MPoint(xPos, yNegPos, zNegPos)

					posXZ    = om.MPoint(xPos, yPos, zNegPos)
					posNegXZ = om.MPoint(xNegPos, yNegPos, zPos)

					voxPosArray.append(pos)
					voxPosArray.append(negPos)
					voxPosArray.append(posY)
					voxPosArray.append(posNegY)
					voxPosArray.append(posZ)
					voxPosArray.append(posNegZ)
					voxPosArray.append(posXZ)
					voxPosArray.append(posNegXZ)

		return voxPosArray

########################################################################################
########################################################################################

	def findClosestPoints(self, _position, _meshNode, _size):

		pathToMesh = om.MDagPath()
		om.MDagPath.getAPathTo(_meshNode, pathToMesh)

		inclusiveMatrix = pathToMesh.inclusiveMatrix()

		meshIntersect = om.MMeshIntersector()
		meshIntersect.create(_meshNode, inclusiveMatrix )

		# Result avtive (or not) voxels
		activeVoxelsArray = om.MIntArray()
		
		closestPnt = om.MPoint()
		closestPntOnMesh = om.MPointOnMesh()
		
		for i in range(_position.length()):

			meshIntersect.getClosestPoint(_position[i], closestPntOnMesh)

			center = _position[i]

			closestPnt = closestPntOnMesh.getPoint()

			if (abs(closestPnt.x - center.x) <= _size) and (abs(closestPnt.y - center.y) <= _size) and (abs(closestPnt.z - center.z) <= _size):
				activeVoxelsArray.append(1)
			else:
				activeVoxelsArray.append(0)

		return activeVoxelsArray

########################################################################################
########################################################################################

	def draw(self, view, path, style, status):

		# - Getting attributes

		thisNode = self.thisMObject()

		shadedPlug = om.MPlug(thisNode, self.shaded)
		shadedTest = shadedPlug.asFloat()
		
		wirePlug = om.MPlug( thisNode, self.wireframe )
		frameWidtht = wirePlug.asFloat()

		diffusePlug = om.MPlug( thisNode, self.diffuse )
		diffuseVal = diffusePlug.asFloat()

		ambientPlug = om.MPlug( thisNode, self.ambient )
		ambientVal = ambientPlug.asFloat()

		specularPlug = om.MPlug( thisNode, self.specular )
		specularVal = specularPlug.asFloat()

		depthPlug = om.MPlug( thisNode, self.depth )
		depthVal = depthPlug.asInt()

		sizePlug = om.MPlug( thisNode, self.voxelsSize )
		sizeVal = sizePlug.asFloat()

		textPlug = om.MPlug( thisNode, self.texture)

		texturePlugTest = textPlug.isConnected()

		inMeshPlug = om.MPlug( thisNode, self.inMesh )

		inBoundingBoxMinPlug = om.MPlug( thisNode, self.inBoundingBoxMin )
		inboundingBoxMaxPlug = om.MPlug( thisNode, self.inBoundingBoxMax )
		
		if inMeshPlug.isConnected():
			"""
			# On recupere le MObject du textureFile connecte
			textPlugs =om.MPlugArray()
			textPlug.connectedTo(textPlugs, 1, 0)
			textNodePlug = textPlugs[0]
			textNode = textNodePlug.node()


			if texturePlugTest :

				#hTexture = glTM.kHwTextureUnknown

				texturePath = "C:\Users\crabs\Desktop\bb.jpg" #omRender.MRenderUtil.exactFileTextureName(textNode)
				#glTM.registerTextureFile(texturePath, hTexture )

				print "bla"
				image = om.MImage()
				image.readFromTextureNode(textNode, om.MImage.kUnknown )

				imageInfo = om.MImageFileInfo()
				imageInfo.width(512)
				imageInfo.height(512)
				imageInfo.channels(3)
				imageInfo.numberOfImages(1)
				imageInfo.imageType(om.MImageFileInfo.kImageTypeColor )
				imageInfo.hardwareType(om.MImageFileInfo.kHwTexture2D)
				imageInfo.hasAlpha(0)
				imageInfo.hasMipMaps(0)

				glFT.glTexImage2D(omRender.MGL_TEXTURE_2D, 0, omRender.MGL_RGB, 512, 512, 0, omRender.MGL_RGB, omRender.MGL_UNSIGNED_BYTE, image.pixels())

				glTM.glBind( textNode, om.MImageFileInfo.kHwTextureUnknown, om.MImageFileInfo.kImageTypeColor )
				glFT.glEnable(omRender.MGL_TEXTURE_2D)"""
			

			view.beginGL()
			glFT.glEnable(omRender.MGL_LIGHTING)
			glFT.glPushAttrib(omRender.MGL_CURRENT_BIT)
			glFT.glPushAttrib( omRender.MGL_ALL_ATTRIB_BITS)
			#glFT.glEnable(omRender.MGL_BLEND)
			#glFT.glEnable(omRender.MGL_DEPTH_TEST)
			glFT.glEnable(omRender.MGL_LIGHTING)
			glFT.glEnable(omRender.MGL_LIGHT0)
			glFT.glEnable(omRender.MGL_NORMALIZE)
			glFT.glEnable(omRender.MGL_COLOR_MATERIAL)

			glFT.glColorMaterial(omRender.MGL_FRONT_AND_BACK, omRender.MGL_AMBIENT)
			glFT.glColor4f( ambientVal, ambientVal, ambientVal, 1.0 )

			glFT.glColorMaterial(omRender.MGL_FRONT_AND_BACK, omRender.MGL_DIFFUSE)
			glFT.glColor4f( diffuseVal, diffuseVal, diffuseVal, 1.0 )

			glFT.glColorMaterial(omRender.MGL_FRONT_AND_BACK, omRender.MGL_SPECULAR)
			glFT.glColor4f( specularVal, specularVal, specularVal, 1 )

			glFT.glColorMaterial(omRender.MGL_FRONT_AND_BACK, omRender.MGL_SHININESS)
			glFT.glColor4f( specularVal, specularVal, specularVal, 1 )

			# Getting mesh obj
			#inMeshObj = inMeshPlug.asMDataHandle().asMesh()

			# Getting boundingbox
			inBoundingBoxMin = inBoundingBoxMinPlug.asMDataHandle().asFloat3()
			inboundingBoxMax = inboundingBoxMaxPlug.asMDataHandle().asFloat3()
			
			inboundingBoxMinPnt = om.MPoint(inBoundingBoxMin[0], inBoundingBoxMin[1], inBoundingBoxMin[2])
			inboundingBoxMaxPnt = om.MPoint(inboundingBoxMax[0], inboundingBoxMax[1], inboundingBoxMax[2])
		   
			# Filtering voxelPntArray. Voxel intersected by the input mesh

			connects = om.MPlugArray()
			inMeshPlug.connectedTo(connects, 1, 1)
			connect = connects[0]
			
			# Creating the grid. voxelPntArray is the center voxel position array
			voxelPntArray = self.createVoxelsPos(connect.node(), sizeVal, inboundingBoxMinPnt, inboundingBoxMaxPnt)

			activeVoxelsArray = self.findClosestPoints(voxelPntArray, connect.node(), sizeVal/2)

			#print activeVoxelsArray.length()
			# Drawing Active voxels
			for v in range(voxelPntArray.length()):

				activeTest = activeVoxelsArray[v]
				#print status
				if activeTest and ( (style != omUI.M3dView.kWireFrame) or ((style == omUI.M3dView.kWireFrame) and shadedTest)) :

					self.makeGlCube(voxelPntArray[v], sizeVal/2, depthVal)

			glFT.glDisable(omRender.MGL_LIGHT0)
			glFT.glDisable(omRender.MGL_LIGHTING);
			glFT.glDisable(omRender.MGL_COLOR_MATERIAL)
			#glFT.glDisable(omRender.MGL_NORMALIZE)

			for v in range(voxelPntArray.length()):

				activeTest = activeVoxelsArray[v]

				if (activeTest and	(style == omUI.M3dView.kWireFrame)) or (activeTest and	(frameWidtht > 0)):

						
					if status == omUI.M3dView.kActive:
						glFT.glColor4f(1, 1, 1, 1.0)
					
					if status == omUI.M3dView.kLead:
						glFT.glColor4f(.25, 1, .5, 1.0)
						
					if status == omUI.M3dView.kDormant:
						glFT.glColor4f(0, 0, 0.4, 1.0)
					
					self.mageGlContour(voxelPntArray[v], sizeVal/2, frameWidtht)


			glFT.glLineWidth(1.0)
			#glFT.glEnable(omRender.MGL_LIGHTING)
			#glFT.glEnable(omRender.MGL_LIGHT0)
			#glFT.glDisable(omRender.MGL_DEPTH_TEST)
			glFT.glDisable(omRender.MGL_BLEND)
			glFT.glPopAttrib()
			view.endGL()


########################################################################################
########################################################################################

def nodeCreator():
	return omMPx.asMPxPtr(voxelizer())

def nodeInitializer():

	nAttr = om.MFnNumericAttribute()
	gAttr = om.MFnGenericAttribute()

	voxelizer.shaded = nAttr.create("shaded", "sh", om.MFnNumericData.kInt, 1)
	nAttr.setMin(0)
	nAttr.setMax(1)
	nAttr.setKeyable(True)

	voxelizer.wireframe = nAttr.create("wireframe", "wf", om.MFnNumericData.kInt, 1)
	nAttr.setMin(0)
	nAttr.setMax(10)
	nAttr.setKeyable(True)

	voxelizer.diffuse = nAttr.create("diffuse", "dif", om.MFnNumericData.kFloat, 0.5)
	nAttr.setMin(0.0)
	nAttr.setMax(1.0)
	nAttr.setKeyable(True)

	voxelizer.ambient = nAttr.create("ambient", "amb", om.MFnNumericData.kFloat, 0.5)
	nAttr.setMin(0.0)
	nAttr.setMax(1.0)
	nAttr.setKeyable(True)

	voxelizer.specular = nAttr.create("specular", "spec", om.MFnNumericData.kFloat, 0)
	nAttr.setMin(0.0)
	nAttr.setMax(1.0)
	nAttr.setKeyable(True)

	voxelizer.depth = nAttr.create("depth", "dp", om.MFnNumericData.kInt, 1)
	nAttr.setMin(0)
	nAttr.setMax(1)
	nAttr.setKeyable(True)

	voxelizer.voxelsSize = nAttr.create("voxelsSize", "size", om.MFnNumericData.kFloat, 1.0)
	nAttr.setMin(0.0001)
	nAttr.setKeyable(True)
	
	voxelizer.inBoundingBoxMin = nAttr.createPoint("inBoundingBoxMin", "bbMin")
	nAttr.setKeyable(True)

	voxelizer.inBoundingBoxMax = nAttr.createPoint("inBoundingBoxMax", "bbMax")
	nAttr.setKeyable(True)

	voxelizer.texture = gAttr.create("texture", "text")
	gAttr.addDataAccept( om.MFnData.kAny )
	gAttr.setKeyable(True)

	voxelizer.inMesh = gAttr.create("inMesh", "iMsh")
	gAttr.addDataAccept( om.MFnData.kMesh )

	voxelizer.addAttribute(voxelizer.shaded)
	voxelizer.addAttribute(voxelizer.wireframe)
	voxelizer.addAttribute(voxelizer.diffuse)
	voxelizer.addAttribute(voxelizer.ambient)
	voxelizer.addAttribute(voxelizer.specular)
	voxelizer.addAttribute(voxelizer.depth)
	voxelizer.addAttribute(voxelizer.texture)
	voxelizer.addAttribute(voxelizer.inMesh)
	voxelizer.addAttribute(voxelizer.voxelsSize)
	voxelizer.addAttribute(voxelizer.inBoundingBoxMin)
	voxelizer.addAttribute(voxelizer.inBoundingBoxMax)

########################################################################################
########################################################################################

def initializePlugin(obj):
	plugin = omMPx.MFnPlugin(obj)
	try:
		plugin.registerNode(nodeTypeName, nodeTypeId, nodeCreator, nodeInitializer, omMPx.MPxNode.kLocatorNode)
	except:
		sys.stderr.write( "Failed to register node: %s" % nodeTypeName)

def uninitializePlugin(obj):
	plugin = omMPx.MFnPlugin(obj)
	try:
		plugin.deregisterNode(nodeTypeId)
	except:
		sys.stderr.write( "Failed to deregister node: %s" % nodeTypeName)