########################################################################################
'''
C:/Users/Cra/AppData/Local/Temp/Cra.20140629.1830.ma
delete "equalDistNode1";
flushUndo;

unloadPluginWithCheck( "/u/rigstuff/PYTHON DEV/MAYA NODES/equalDistNode.py" );
loadPlugin( "/u/rigstuff/PYTHON DEV/MAYA NODES/equalDistNode.py"  );

createNode "equalDistNode";

connectAttr -f A.translate equalDistNode1.pntAPos;
connectAttr -f B.translate equalDistNode1.pntBPos;
connectAttr -f equalDistNode1.outPntA resA.translate;
connectAttr -f equalDistNode1.outPntB resB.translate;
connectAttr -f t1.translate equalDistNode1.targetInputPos[0];
connectAttr -f t2.translate equalDistNode1.targetInputPos[1];
connectAttr -f t3.translate equalDistNode1.targetInputPos[2];
connectAttr -f t4.translate equalDistNode1.targetInputPos[3];
connectAttr -f t5.translate equalDistNode1.targetInputPos[4];
connectAttr -f t6.translate equalDistNode1.targetInputPos[5];
connectAttr -f t7.translate equalDistNode1.targetInputPos[6];
connectAttr -f t8.translate equalDistNode1.targetInputPos[7];
connectAttr -f t9.translate equalDistNode1.targetInputPos[8];
connectAttr -f equalDistNode1.outProj res.translate ;
'''


########################################################################################
import math, copy
import maya.OpenMaya as om
import maya.OpenMayaMPx as omMPx


nodeName = "equalDistNode"
equalDistNodeId = om.MTypeId(0x00151A51A)

########################################################################################
########################################################################################

class equalDistNode(omMPx.MPxNode):

########################################################################################
########################################################################################

	def __init__(self):

		omMPx.MPxNode.__init__(self)

########################################################################################

	def compute(self, plug, dataBlock):

		# - Getting input values
		#
		pi = 3.14159265359
		hTargetInputArray	= dataBlock.inputArrayValue( self.targetInputsPosAttr )

		pntAPos		= dataBlock.inputValue( self.pntAPosAttr ).asFloat3()
		pntBPos		= dataBlock.inputValue( self.pntBPosAttr ).asFloat3()
		NormalPos	= dataBlock.inputValue( self.upVectorAttr ).asFloat3()
		frontPos	= dataBlock.inputValue( self.frontVectorAttr ).asFloat3()
		
		pntAOffsetValue	 = dataBlock.inputValue( self.pntAOffsetAttr ).asDouble()
		pntBOffsetValue	 = dataBlock.inputValue( self.pntBOffsetAttr ).asDouble()

		# - Getting inputs positions/vectors
		#
		pntA		= om.MPoint(pntAPos[0], pntAPos[1], pntAPos[2])
		pntB		= om.MPoint(pntBPos[0], pntBPos[1], pntBPos[2])
		
		upVector	= om.MVector(NormalPos[0], NormalPos[1], NormalPos[2])
		upVector.normalize()
		
		frontVect	 = pntA - pntB #om.MVector(frontPos[0], frontPos[1], frontPos[2])
		#frontVect.normalize()		 
		# - Base vector and distance
		#
		abVector   = pntB - pntA
		abDistance = abVector.length()

		# - Init vars
		#
		aTargetVector = om.MVector()
		bTargetVector = om.MVector()

		aTargetDistance = 0.0
		bTargetDistance = 0.0

		resultTargetPnt = om.MPoint()
		resultDistance	= 0.0

		test = 0
		testI = 0

		elementsCount = hTargetInputArray.elementCount()
		
		heightPntArray	= om.MPointArray(2, om.MPoint(0.0,0.0,0.0))
		heightArray		= om.MFloatArray(2, 99)
		elemArray		= om.MIntArray(2, 99)
		
		# - Finding targets side
		#
		
		frontHeightPntArray = om.MPointArray()
		frontHeightArray	= om.MFloatArray()
		frontElemArray		= om.MIntArray(2, 99)
		
		backHeightPntArray = om.MPointArray()
		backHeightArray	   = om.MFloatArray()
		backElemArray	   = om.MIntArray(2, 99)

		
		for i in xrange (elementsCount):
			
			hTargetInputArray.jumpToElement(i)
		
			target		= hTargetInputArray.inputValue().asFloat3()
			targetPnt	= om.MPoint(target[0], target[1], target[2])
			
			aTargetDistance = targetPnt.distanceTo(pntA)
			
			aTargetVector = targetPnt - pntA
			bTargetVector = targetPnt - pntB
			
			# - compute target to base height
			#
			
			
			angleRef = aTargetVector.angle(abVector)
			height	 = math.sin(angleRef) * aTargetDistance

			if targetPnt.y >= 0:
				hx = 1
			else:
				hx =  -1
			
			height *= hx
			
			# - Testing height direction
			#
			#if targetPnt.y < 0:
			#	height = 0.0
				
			projPntTmp = targetPnt + (-upVector * height * hx)
			
			vect = projPntTmp - om.MPoint((pntB.x + pntA.x)/2,(pntB.y + pntA.y)/2,(pntB.z + pntA.z)/2)
			dirAngle = frontVect.angle(vect)

			tmpPnt = copy.copy(targetPnt)
			heightTmp = copy.copy(height)
			
			if dirAngle < 1:
				frontHeightPntArray.append(tmpPnt)
				frontHeightArray.append(heightTmp)
				
				
			if dirAngle > 1:
				backHeightPntArray.append(tmpPnt)				 
				backHeightArray.append(heightTmp)

		totalHeightPntArray = [frontHeightPntArray, backHeightPntArray]
		totalHeightArray	= [frontHeightArray, backHeightArray]
		totalElemArray		= [frontElemArray, backElemArray]
		
		# - Finding the two first highest targets of each Side
		#
		resultFrontProjPnt = om.MPoint()
		resultFrontHeight = 0
		
		resultBackProjPnt = om.MPoint()
		resultBackHeight = 0
		
		testS = 0
		
		#print backHeightArray.length()
		
		for s in xrange (2):
			#- s=0 front
			#- s=1 back

			targetsArray = totalHeightPntArray[testS]
			#elemArray = totalElemArray[s]
			targetsHeightArray = totalHeightArray[testS]
			
			
			for n in xrange(2):
				
				resultDistance = 0.0
				test = 0	
				
				for z in xrange(targetsArray.length()):
					
					if (z != elemArray[0]):
						
						height		= targetsHeightArray[z]
						targetPnt	= targetsArray[z]
			
						if (test == 0) or (height > resultDistance):
							
							resultDistance	= copy.copy(height)
							resultTargetPnt = copy.copy(targetPnt)
							
							heightArray.set(resultDistance, n)
							heightPntArray.set(resultTargetPnt, n)
							
							testI = copy.copy(z)

							elemArray.set(testI, n)
							
							test = 1				
			
			#computing le projPnt for each side
			
			# - Project the targets on base
			#
			
			heightPnt1	= heightPntArray[0]
			height1		= heightArray[0]
			projPnt1	= heightPnt1 + (-upVector * height1)
			
			heightPnt2	= heightPntArray[1]
			height2		= heightArray[1]
			projPnt2	= heightPnt2 + (-upVector * height2)
			
			#Cosin interpolation ////// test
			height1Test = [heightPnt1.x,heightPnt1.y,heightPnt1.z] 

			height2Test = [heightPnt2.x,heightPnt2.y,heightPnt2.z]

				
			projPnt = om.MPoint()

			if height1 == 0.0:
				ratio2 = 0
				
			else:
				ratio2 = height2/height1
			vect2 = projPnt2 - projPnt1
			
			
			#abDistance
			
			abSemiDistance = abDistance/2
			
			heightDistance = vect2.length()
			interTargetDist = abDistance/(elementsCount-1)
			resDistance = heightDistance / abSemiDistance
			
			resDistance2 = height1/abSemiDistance
			
			if height1 >= 1:
				a1 = 0.88
			if height1 < 1:
				a1 = 0.65
				
			b1 = 1
			U1 = ratio2
			interInterp = (U1 - a1) * (1.0 / (b1 - a1))
			interInterp = max(min(interInterp, 1), 0)
			
			a2 = interTargetDist
			b2 = abSemiDistance
			U2 = heightDistance
			
			totalInterp = (U2 - a2) * (1.0 / (b2 - a2))
			totalInterp = max(min(totalInterp, 1), 0)
			
			projPnt = (projPnt1) + ((vect2/2)*interInterp*(1-totalInterp)) + ((vect2/2)*totalInterp)			
			#s= 1
			if testS == 0:
				resultFrontHeight = copy.copy(height1)
				resultFrontProjPnt = copy.copy(projPnt)
				
			
			if testS == 1:
				resultBackHeight = copy.copy(height1)
				resultBackProjPnt = copy.copy(projPnt)
				
			testS = 1
		# - Project the targets on base
		#
		
		'''
		if resultFrontHeight > resultBackHeight:
			
			projPnt1 = resultFrontProjPnt
			height1	 = resultFrontHeight
			
			projPnt2 = resultBackProjPnt
			height2	 = resultBackHeight
			
		else:				 
			projPnt1 = resultBackProjPnt
			height1	 = resultBackHeight
			
			projPnt2 = resultFrontProjPnt
			height2	 = resultFrontHeight  

		projPnt = om.MPoint()

		vect2 = projPnt2 - projPnt1
		ratio2 = height2/height1

		heightDistance = vect2.length()
		interTargetDist = abDistance/(elementsCount-1)
		resDistance = heightDistance / abDistance
		
		resDistance2 = height1/abDistance

		a1 = 0
		b1 = 1
		U1 = ratio2
		interInterp = (U1 - a1) * (1.0 / (b1 - a1))
		interInterp = max(min(interInterp, 1), 0)
		
		a2 = interTargetDist
		b2 = abDistance
		U2 = heightDistance
		
		totalInterp = (U2 - a2) * (1.0 / (b2 - a2))
		totalInterp = max(min(totalInterp, 1), 0)
		
		projPnt = (projPnt1) + ((vect2/2)*interInterp)
		
		resultTargetPnt = height1
		
		heightProjPnt = projPnt + (upVector * height1)
		
		# - Project the target on base
		#
		#projPnt = resultTargetPnt + (-upVector * heightArray[0])

		##################################################################

		# - Compute A and B positions for closest target
		#
		
		
		aToTargetProjVect = projPnt - pntA
		bToTargetProjVect = projPnt - pntB

		aToTargetProjDist = aToTargetProjVect.length()
		bToTargetProjDist = bToTargetProjVect.length()

		balanceRatioA	= aToTargetProjDist / abDistance
		balanceRatioB	= bToTargetProjDist / abDistance

		targetVect = heightProjPnt - projPnt

		targetDist = targetVect.length()

		linStepA = (balanceRatioB) * (1.0 / (.5 ))
		linStepA = max(min(linStepA, 1), -1)

		linStepB = (balanceRatioA) * (1.0 / (.5 ))
		linStepB = max(min(linStepB, 1), -1)

		# - Adding up mov when centering
		#

		linStepBb = (linStepB * pi)
		linStepAa = (linStepA * pi)

		aResultPnt = pntA + (targetVect * (linStepA))
		bResultPnt = pntB + (targetVect * (linStepB))

		aDistVect = aResultPnt - pntA
		bDistVect = bResultPnt - pntB

		aDist = aDistVect.length()
		bDist = bDistVect.length()

		aDistVect.normalize()
		bDistVect.normalize()'''

		# - computing result a et b positions

		#aResultPnt += (bDistVect * ((bDist)/(aDist + .0001)) * (math.sin(linStepBb)/2))
		#bResultPnt += (aDistVect * ((aDist)/(bDist + .0001)) * (math.sin(linStepAa)/2))
		
		
		aResultPnt = pntA + (upVector * resultFrontHeight * pntAOffsetValue)
		bResultPnt = pntB + (upVector * resultBackHeight * pntBOffsetValue)
		
		aResultDist = om.MVector(aResultPnt - pntA).length()
		bResultDist = om.MVector(bResultPnt - pntB).length()

		abResultVect = bResultPnt - aResultPnt
		abResultVect.normalize()

		#projPnt2	 = testPnt
		#aResultPnt	 = resultFrontProjPnt
		#bResultPnt	 = resultBackProjPnt
		# - Setting outputs
		#
		hOutputAPnt = dataBlock.outputValue(self.outPntAAttr)
		hOutputAPnt.set3Float(aResultPnt.x, aResultPnt.y, aResultPnt.z)

		hOutputBPnt = dataBlock.outputValue(self.outPntBAttr)
		hOutputBPnt.set3Float(bResultPnt.x, bResultPnt.y, bResultPnt.z)

		hOutputProjPnt = dataBlock.outputValue(self.outProjAttr)
		hOutputProjPnt.set3Float(projPnt.x, projPnt.y, projPnt.z)
		
		hOutputProj2Pnt = dataBlock.outputValue(self.outProjAttr2)
		hOutputProj2Pnt.set3Float(projPnt.x, projPnt.y, projPnt.z)
		
		dataBlock.setClean(plug)
################################################################################
########################################################################################
	
	# Catmull-Rom interpolation 
	def CatmullRomInterpolation(self, p0, p1, p2, p3, U):

		U2 = U*U
		a0 = -0.5*p0+1.5*p1-1.5*p2+0.5*p3
		a1 = p0-2.5*p1+2*p2-0.5*p3
		a2 = -0.5*p0+0.5*p2
		a3 = p1

		interpPnt = a0*U*U2+a1*U2+a2*U+a3

		return interpPnt
		
################################################################################
########################################################################################

def nodeCreator():
	return omMPx.asMPxPtr( equalDistNode() )

########################################################################################
########################################################################################

def nodeInitializer():

	nAttr = om.MFnNumericAttribute()

	equalDistNode.pntAPosAttr = nAttr.createPoint("pntAPos", "pntA")
	nAttr.setKeyable(True)
	nAttr.setStorable(True)
	nAttr.setWritable(True)

	equalDistNode.pntBPosAttr = nAttr.createPoint("pntBPos", "pntB")
	nAttr.setKeyable(True)
	nAttr.setStorable(True)
	nAttr.setWritable(True)

	equalDistNode.upVectorAttr = nAttr.createPoint("upVector", "upVect")
	nAttr.setKeyable(True)
	nAttr.setStorable(True)
	nAttr.setWritable(True)

	equalDistNode.frontVectorAttr = nAttr.createPoint("frontVector", "frontVect")
	nAttr.setKeyable(True)
	nAttr.setStorable(True)
	nAttr.setWritable(True)
	
	equalDistNode.targetInputsPosAttr = nAttr.createPoint("targetInputPos", "targIn")
	nAttr.setArray(True)
	nAttr.setKeyable(True)
	nAttr.setStorable(True)
	nAttr.setWritable(True)

	equalDistNode.pntAOffsetAttr = nAttr.create("pntAOffset", "offstA", om.MFnNumericData.kDouble, 1.0)
	nAttr.setKeyable(True)
	nAttr.setStorable(True)
	nAttr.setWritable(True)

	equalDistNode.pntBOffsetAttr = nAttr.create("pntBOffset", "offstB", om.MFnNumericData.kDouble, 1.0)
	nAttr.setKeyable(True)
	nAttr.setStorable(True)
	nAttr.setWritable(True)

	equalDistNode.outPntAAttr = nAttr.createPoint("outPntA", "outA")

	equalDistNode.outPntBAttr = nAttr.createPoint("outPntB", "outB")

	equalDistNode.outProjAttr = nAttr.createPoint("outProj", "outP")
	
	equalDistNode.outProjAttr2 = nAttr.createPoint("outProj2", "outP2")
	
	equalDistNode.addAttribute(equalDistNode.pntAPosAttr)
	equalDistNode.addAttribute(equalDistNode.pntBPosAttr)
	equalDistNode.addAttribute(equalDistNode.upVectorAttr)
	equalDistNode.addAttribute(equalDistNode.frontVectorAttr)
	equalDistNode.addAttribute(equalDistNode.targetInputsPosAttr)
	equalDistNode.addAttribute(equalDistNode.pntAOffsetAttr)
	equalDistNode.addAttribute(equalDistNode.pntBOffsetAttr)
	equalDistNode.addAttribute(equalDistNode.outPntAAttr)
	equalDistNode.addAttribute(equalDistNode.outPntBAttr)
	equalDistNode.addAttribute(equalDistNode.outProjAttr)
	equalDistNode.addAttribute(equalDistNode.outProjAttr2)

	equalDistNode.attributeAffects(equalDistNode.pntAPosAttr, equalDistNode.outPntAAttr)
	equalDistNode.attributeAffects(equalDistNode.pntAOffsetAttr, equalDistNode.outPntAAttr)
	equalDistNode.attributeAffects(equalDistNode.pntBOffsetAttr, equalDistNode.outPntAAttr)
	equalDistNode.attributeAffects(equalDistNode.pntBPosAttr, equalDistNode.outPntAAttr)
	equalDistNode.attributeAffects(equalDistNode.upVectorAttr, equalDistNode.outPntAAttr)
	equalDistNode.attributeAffects(equalDistNode.frontVectorAttr, equalDistNode.outPntAAttr)
	equalDistNode.attributeAffects(equalDistNode.targetInputsPosAttr, equalDistNode.outPntAAttr)

	equalDistNode.attributeAffects(equalDistNode.pntAPosAttr, equalDistNode.outPntBAttr)
	equalDistNode.attributeAffects(equalDistNode.pntBPosAttr, equalDistNode.outPntBAttr)
	equalDistNode.attributeAffects(equalDistNode.pntAOffsetAttr, equalDistNode.outPntBAttr)
	equalDistNode.attributeAffects(equalDistNode.pntBOffsetAttr, equalDistNode.outPntBAttr)
	equalDistNode.attributeAffects(equalDistNode.upVectorAttr, equalDistNode.outPntBAttr)
	equalDistNode.attributeAffects(equalDistNode.frontVectorAttr, equalDistNode.outPntBAttr)
	equalDistNode.attributeAffects(equalDistNode.targetInputsPosAttr, equalDistNode.outPntBAttr)

	equalDistNode.attributeAffects(equalDistNode.pntAPosAttr, equalDistNode.outProjAttr)
	equalDistNode.attributeAffects(equalDistNode.pntBPosAttr, equalDistNode.outProjAttr)
	equalDistNode.attributeAffects(equalDistNode.pntAOffsetAttr, equalDistNode.outProjAttr)
	equalDistNode.attributeAffects(equalDistNode.pntBOffsetAttr, equalDistNode.outProjAttr)
	equalDistNode.attributeAffects(equalDistNode.upVectorAttr, equalDistNode.outProjAttr)
	equalDistNode.attributeAffects(equalDistNode.frontVectorAttr, equalDistNode.outProjAttr)
	equalDistNode.attributeAffects(equalDistNode.targetInputsPosAttr, equalDistNode.outProjAttr)
	
	equalDistNode.attributeAffects(equalDistNode.pntAPosAttr, equalDistNode.outProjAttr2)
	equalDistNode.attributeAffects(equalDistNode.pntBPosAttr, equalDistNode.outProjAttr2)
	equalDistNode.attributeAffects(equalDistNode.upVectorAttr, equalDistNode.outProjAttr2)
	equalDistNode.attributeAffects(equalDistNode.targetInputsPosAttr, equalDistNode.outProjAttr2)
########################################################################################
########################################################################################

def initializePlugin(mobject):
	mplugin = omMPx.MFnPlugin(mobject)
	try:
		mplugin.registerNode(nodeName, equalDistNodeId, nodeCreator, nodeInitializer)
	except:
		sys.stderr.write("Failed to register node: $s\n" % nodeName)

########################################################################################
########################################################################################

def uninitializePlugin(mobject):
	mplugin = omMPx.MFnPlugin(mobject)
	try:
		mplugin.deregisterNode(equalDistNodeId)
	except:
		sys.stderr.write("Failed to deregister node: $s\n" % nodeName)
