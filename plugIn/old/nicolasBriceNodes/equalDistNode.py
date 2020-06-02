########################################################################################
'''

delete "equalDistNode1";
flushUndo;

unloadPluginWithCheck( "/u/rigstuff/PYTHON DEV/MAYA NODES/equalDistNode.py );
loadPlugin( "/u/rigstuff/PYTHON DEV/MAYA NODES/equalDistNode.py"  );

createNode "equalDistNode";

connectAttr -f A.translate equalDistNode1.pntAPos;
connectAttr -f B.translate equalDistNode1.pntBPos;
connectAttr -f equalDistNode1.outPntA resA.translate;
connectAttr -f equalDistNode1.outPntB resB.translate;
connectAttr -f t1.translate equalDistNode1.targetInputPos[0];
connectAttr -f t2.translate equalDistNode1.targetInputPos[1];
connectAttr -f t3.translate equalDistNode1.targetInputPos[2];
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
		hTargetInputArray		= dataBlock.inputArrayValue( self.targetInputsPosAttr )

		pntAPos				   = dataBlock.inputValue( self.pntAPosAttr ).asFloat3()
		pntBPos				   = dataBlock.inputValue( self.pntBPosAttr ).asFloat3()
		NormalPos		   = dataBlock.inputValue( self.NormalPosAttr ).asFloat3()

		pntAOffsetValue		   = dataBlock.inputValue( self.pntAOffsetAttr ).asDouble()
		pntBOffsetValue		   = dataBlock.inputValue( self.pntBOffsetAttr ).asDouble()

		# - Getting inputs positions
		#
		pntA		= om.MPoint(pntAPos[0], pntAPos[1], pntAPos[2])
		pntB		= om.MPoint(pntBPos[0], pntBPos[1], pntBPos[2])
		NormalPnt	  = om.MPoint(NormalPos[0], NormalPos[1], NormalPos[2])

		# - Base vector and distance
		#
		abVector = pntB - pntA
		abDistance = abVector.length()

		# - Up vector
		#
		upVector = om.MVector(0.0, 1.0, 0.0)#NormalPnt - pntA

		# - Init vars
		#
		aTargetVector = om.MVector()
		bTargetVector = om.MVector()

		aTargetDistance = 0.0
		bTargetDistance = 0.0

		resultTargetPnt = om.MPoint()
		resultDistance	= 0.0

		resultTargetPnt2 = om.MPoint()
		resultDistance2	 = 0.0
		resultBaseProj2	 = None
		
		aResultTargetDistance = 0.0
		bResultTargetDistance = 0.0

		test = 0
	   
		testI = 0
	   
		# - Finding closest target
		#
		for i in xrange (hTargetInputArray.elementCount()):

			hTargetInputArray.jumpToElement(i)

			target				= hTargetInputArray.inputValue().asFloat3()
			targetPnt		= om.MPoint(target[0], target[1], target[2])

			aTargetDistance = targetPnt.distanceTo(pntA)

			aTargetVector = targetPnt - pntA
			bTargetVector = targetPnt - pntB

			# - compute target to base height
			#
			heigth	= 0.0
		   
			angleRef = aTargetVector.angle(abVector)
			height = math.sin(angleRef) * aTargetDistance

			# - Keeping the longest
			#

			if (test == 0) or (height > resultDistance):

				resultDistance	= copy.copy(height)
				resultTargetPnt = copy.copy(targetPnt)

				testI = i

				test = 1
	   
		testJ = 0
		test = 0

 
		# - Project the target on base
		#
		projPnt = resultTargetPnt + (-upVector * resultDistance)

		##################################################################

		# - Compute A and B positions for closest target
		#
	   
		aToTargetProjVect = projPnt - pntA
		bToTargetProjVect = projPnt - pntB

		aToTargetProjDist = aToTargetProjVect.length()
		bToTargetProjDist = bToTargetProjVect.length()

		balanceRatioA		= aToTargetProjDist / abDistance
		balanceRatioB		= bToTargetProjDist / abDistance

		targetVect = resultTargetPnt - projPnt

		targetDist = targetVect.length()
	   
		linStepA  = (balanceRatioB) * (1.0 / (.5 ))
		linStepA = max(min(linStepA, 1), -1)

		linStepB  = (balanceRatioA) * (1.0 / (.5 ))
		linStepB = max(min(linStepB, 1), -1)

		# - Adding up mov when centering
		#
		pi = 3.14159265359
	   
		linStepBb = (linStepB * pi)
		linStepAa = (linStepA * pi)

		aResultPnt = pntA + (targetVect * (linStepA))
		bResultPnt = pntB + (targetVect * (linStepB))

		aDistVect = aResultPnt - pntA
		bDistVect = bResultPnt - pntB
	   
		aDist = aDistVect.length()
		bDist = bDistVect.length()
	   
		aDistVect.normalize()
		bDistVect.normalize()
		
		# - computing result a et b positions
		
		aResultPnt += (bDistVect * ((bDist)/(aDist + .0001)) * (math.sin(linStepBb)/2))
		bResultPnt += (aDistVect * ((aDist)/(bDist + .0001)) * (math.sin(linStepAa)/2))
		
		aResultDist = om.MVector(aResultPnt - pntA).length()
		bResultDist = om.MVector(bResultPnt - pntB).length()

		abResultVect = bResultPnt - aResultPnt
		abResultVect.normalize()
	   
		heightTest = 0
		
		# - Finding second closest target
		#
		stopCount = 0
		if (hTargetInputArray.elementCount() > 1 ):
			for j in xrange (hTargetInputArray.elementCount()):
				   
				if (j != testI):
					   
					hTargetInputArray.jumpToElement(j)
					
					target2		= hTargetInputArray.inputValue().asFloat3()
					targetPnt2	= om.MPoint(target2[0], target2[1], target2[2])
					
					aTargetDistance2 = targetPnt2.distanceTo(pntA)
					
					aTargetVector2 = targetPnt2 - pntA
					bTargetVector2 = targetPnt2 - pntB
					
					# - compute target to base height
					#
					heigth2	 = 99999.9
					
					angleRef2 = aTargetVector2.angle(abVector)
					height2 = math.sin(angleRef2) * aTargetDistance2
					
					# - Keeping the longest
					#
					# ------------
					baseProjPnt2 = targetPnt2 + (-upVector * height2)
					targetVect2 = targetPnt2 - baseProjPnt2
					targetVect2.normalize()
					# ------------
					
					# - Finding intersection between baseToTarget vect and aToB vect
					#
					r1= aResultPnt
					r2= baseProjPnt2
					e1= abResultVect
					e2= targetVect2
					
					u = e1*e2
					
					if u!=1 :
					   
						v = r2-r1
					   
						t1 = v*e1
						t2 = v*e2
						dist = (t2-u*t1)/(u*u-1)
						
						#intersection point is given by le distance (dist) at wich he is on the baseToTarget line
						#
						projPntTmp = baseProjPnt2 + (targetVect2 * dist) 
					   
						
						projVect			= projPntTmp - baseProjPnt2
						projLength			= projVect.length()
					   
						targetVect2Length	= height2
					   
						height2 = targetVect2Length - projLength
						#print height2
						
					if (test == 0) or (height2 > resultDistance2):
						
						targetTest = 1
						
						resultDistance2	 = copy.copy(height2)
						resultTargetPnt2 = copy.copy(targetPnt2)
						tragetVectDef	 = copy.copy(targetVect2)
						projPnt			 = copy.copy(projPntTmp)
						resultBaseProj2	 = copy.copy(baseProjPnt2)
					
						testJ = j
						test = 1



		# - Compute A and B positions for second closest target
		#
		
		aToTargetProjVect2 = resultBaseProj2 - pntA
		bToTargetProjVect2 = resultBaseProj2 - pntB
		
		aToTargetProjDist2 = aToTargetProjVect2.length()
		bToTargetProjDist2 = bToTargetProjVect2.length()
		
		balanceRatioA2		 = aToTargetProjDist2 / abDistance
		balanceRatioB2		 = bToTargetProjDist2 / abDistance	 
																 
																 
		#######################################
		#######TO DO											 
		##														 
																 
		linStepA2  = (balanceRatioB2) * (1.0 / (.5 ))			 
		linStepA2 = max(min(linStepA2, 1), -1)					 
																 
		linStepB2  = (balanceRatioA2) * (1.0 / (.5 ))			 
		linStepB2 = max(min(linStepB2, 1), -1)					 
																 
		heigthLinStep = max(min(0, 1000000), (resultDistance2))	 
																 
		if (linStepA2<1):
			linStepA2 = 0
			
		if (linStepB2<1):
			linStepB2 = 0	
			
		aResultPnt += (upVector * heigthLinStep * linStepA2 / balanceRatioB2)	 
		bResultPnt += (upVector * heigthLinStep * linStepB2 / balanceRatioA2)
		
		print linStepA2
		print linStepB2
		# - Setting outputs
		#
		hOutputAPnt = dataBlock.outputValue(self.outPntAAttr)
		hOutputAPnt.set3Float(aResultPnt.x, aResultPnt.y, aResultPnt.z)
		
		hOutputBPnt = dataBlock.outputValue(self.outPntBAttr)
		hOutputBPnt.set3Float(bResultPnt.x, bResultPnt.y, bResultPnt.z)
		
		hOutputAPnt = dataBlock.outputValue(self.outProjAttr)
		hOutputAPnt.set3Float(projPnt.x, projPnt.y, projPnt.z)
		
		dataBlock.setClean(plug)
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

	equalDistNode.NormalPosAttr = nAttr.createPoint("normalPos", "normPos")
	nAttr.setKeyable(True)
	nAttr.setStorable(True)
	nAttr.setWritable(True)

	equalDistNode.targetInputsPosAttr = nAttr.createPoint("targetInputPos", "targIn")
	nAttr.setArray(True)
	nAttr.setKeyable(True)
	nAttr.setStorable(True)
	nAttr.setWritable(True)

	equalDistNode.pntAOffsetAttr = nAttr.create("pntAOffset", "offstA", om.MFnNumericData.kDouble)
	nAttr.setKeyable(True)
	nAttr.setStorable(True)
	nAttr.setWritable(True)

	equalDistNode.pntBOffsetAttr = nAttr.create("pntBOffset", "offstB", om.MFnNumericData.kDouble)
	nAttr.setKeyable(True)
	nAttr.setStorable(True)
	nAttr.setWritable(True)

	equalDistNode.outPntAAttr = nAttr.createPoint("outPntA", "outA")

	equalDistNode.outPntBAttr = nAttr.createPoint("outPntB", "outB")

	equalDistNode.outProjAttr = nAttr.createPoint("outProj", "outP")

	equalDistNode.addAttribute(equalDistNode.pntAPosAttr)
	equalDistNode.addAttribute(equalDistNode.pntBPosAttr)
	equalDistNode.addAttribute(equalDistNode.NormalPosAttr)
	equalDistNode.addAttribute(equalDistNode.targetInputsPosAttr)
	equalDistNode.addAttribute(equalDistNode.pntAOffsetAttr)
	equalDistNode.addAttribute(equalDistNode.pntBOffsetAttr)
	equalDistNode.addAttribute(equalDistNode.outPntAAttr)
	equalDistNode.addAttribute(equalDistNode.outPntBAttr)
	equalDistNode.addAttribute(equalDistNode.outProjAttr)


	equalDistNode.attributeAffects(equalDistNode.pntAPosAttr, equalDistNode.outPntAAttr)
	equalDistNode.attributeAffects(equalDistNode.pntBPosAttr, equalDistNode.outPntAAttr)
	equalDistNode.attributeAffects(equalDistNode.NormalPosAttr, equalDistNode.outPntAAttr)
	equalDistNode.attributeAffects(equalDistNode.targetInputsPosAttr, equalDistNode.outPntAAttr)

	equalDistNode.attributeAffects(equalDistNode.pntAPosAttr, equalDistNode.outPntBAttr)
	equalDistNode.attributeAffects(equalDistNode.pntBPosAttr, equalDistNode.outPntBAttr)
	equalDistNode.attributeAffects(equalDistNode.NormalPosAttr, equalDistNode.outPntBAttr)
	equalDistNode.attributeAffects(equalDistNode.targetInputsPosAttr, equalDistNode.outPntBAttr)

	equalDistNode.attributeAffects(equalDistNode.pntAPosAttr, equalDistNode.outProjAttr)
	equalDistNode.attributeAffects(equalDistNode.pntBPosAttr, equalDistNode.outProjAttr)
	equalDistNode.attributeAffects(equalDistNode.NormalPosAttr, equalDistNode.outProjAttr)
	equalDistNode.attributeAffects(equalDistNode.targetInputsPosAttr, equalDistNode.outProjAttr)
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
