"""
    This node is a sphere rolling Node.
    It's based on the "damped mass-spring" differential equation computed with the Heun's ODE solving method
    It needs a polySphere, nurbs surface and a locator to work.
    
    bellow is there to show how the node should be connected.
    
    
    createNode "rollingNode";

    connectAttr -f locatorShape1.worldPosition[0] rollingNode1.targetPosition;
    connectAttr -f nurbsTorusShape1.local rollingNode1.inRefShape;
    connectAttr -f pSphereShape1.outMesh rollingNode1.ballShape;
    connectAttr -f rollingNode1.outPosition pSphere1.translate;

    select -r locator1 ;

"""

########################################################################################
########################################################################################

import math, copy
import maya.OpenMaya as om
import maya.OpenMayaMPx as omMPx

nodeName = "rollingNode"
rollingNodeId = om.MTypeId(0x51243)

########################################################################################
########################################################################################

class rollingNode(omMPx.MPxNode):

    # empty node's variables
    weight             = om.MObject()
    heightOffest       = 0.0

    targetPos          = om.MPoint()        #to store the current locator's position
    lastTargetPosition = om.MPoint()        #to store the last locator's position 
                                            
    clstPnt            = om.MPoint()        #to store the current locator's closest point
    lastClstPnt        = om.MPoint()        #to store the last locator's closest point
                                            
    lastParamU         = 0.0                #to store the last surface's closest point U param 
    lastParamV         = 0.0                #to store the last surface's closest point V param

    quater             = om.MQuaternion()   

    outPosition        = [0.0, 0.0, 0.0]

    firstTime          = 1                  #first time test variable

########################################################################################
########################################################################################

    def compute(self, plug, dataBlock):

        thisNode = self.thisMObject()
        
        # node's attributs declaration
        self.targetPos    = dataBlock.inputValue(rollingNode.targetPos).asFloat3()
        self.weight       = dataBlock.inputValue(rollingNode.weight).asFloat()
        self.heightOffest = dataBlock.inputValue(rollingNode.offset).asFloat()

        #refShape
        inRefShapeData = dataBlock.inputValue(rollingNode.inRefShape).asNurbsSurface()
        plugInRefShape = om.MPlug( thisNode, self.inRefShape )

        ballShapeData  = dataBlock.inputValue(rollingNode.ballShape).asMesh()
        plugInBallShape = om.MPlug( thisNode, self.ballShape )

        
        if( plugInRefShape.isConnected() == True and  plugInBallShape.isConnected()):
            
            #declaring shapes fonctions
            inRefShapeFn = om.MFnNurbsSurface(inRefShapeData)
            ballShapeFn  = om.MFnMesh(ballShapeData)

            #we get ball's transform by outPosition attribute's plug
            thisNodePlug     = om.MPlug(thisNode, rollingNode.outPosition)
            plugArr          = om.MPlugArray()

            thisNodePlug.connectedTo(plugArr, False, True)
            ballPlug      = plugArr[0]
            ballNode      = ballPlug.node()
            ballTransform = om.MFnTransform(ballNode)
            
            #getting transform rotation pivot
            ballPivotTmp = ballTransform.rotatePivot(om.MSpace.kObject)
            ballPivot    = om.MFloatPoint(ballPivotTmp.x,ballPivotTmp.y,ballPivotTmp.z)

#########################################

            #MScriptUtils for getting U and V paramters from MFnNurbsSurface.closestPoint
            #U parameter
            paramUtemp    = om.MScriptUtil()
            paramUtemp.createFromDouble(0.0)

            paramU  = paramUtemp.asDoublePtr()
            
            #V parameter
            paramVtemp = om.MScriptUtil()
            paramVtemp.createFromDouble(0.0)

            paramV = paramVtemp.asDoublePtr()

            #Closest point from handle to refSurface
            targetPnt    = om.MPoint(self.targetPos[0], self.targetPos[1], self.targetPos[2])
            self.clstPnt = inRefShapeFn.closestPoint(targetPnt, paramU, paramV, True, 0.001, om.MSpace.kWorld)
            
            #we get doubles from MScripUtils
            u = paramUtemp.getDouble(paramU)
            v = paramUtemp.getDouble(paramV)

            #first init of global variables
            if (self.firstTime == 1):
                self.lastClstPnt        = copy.copy(self.clstPnt)
                self.lastParamU         = copy.copy(u)
                self.lastParamV         = copy.copy(v)
                self.lastTargetPosition = copy.copy(targetPnt)
                pivotPnt                = copy.copy(targetPnt)
                self.firstTime          = 0

#########################################

            #getting point from last U, V parameters, to compare with current closest point
            inRefShapeFn.getPointAtParam(self.lastParamU, self.lastParamV, self.lastClstPnt, om.MSpace.kWorld)

            #vectors: normal / displacement / rotation axis vector
            
            #normal vector at closest point
            normalVect   = inRefShapeFn.normal(u, v, om.MSpace.kObject)
            
            #displacement vector
            displaceVect = self.lastClstPnt - self.clstPnt
            
            #rotation axis
            rotationAxis = displaceVect ^ normalVect

            #displacement
            displace     = displaceVect.length()
            
            #raytrace position/direction from closest point
            rayNormal = self.clstPnt + normalVect

#########################################

            #allIntersections variables declaration
            #ray is trace from rotate pivot along closest point's normal
            #hit point gives radius of the ball
            raySource           = om.MFloatPoint(ballPivot.x,ballPivot.y,ballPivot.z)
            rayDirection        = om.MFloatVector(rayNormal.x,rayNormal.y,rayNormal.z)
            faceIds             = None
            triIds              = None
            isSorted            = False
            maxParam            = 1000000000
            testBothDirections  = False
            accelParams         = ballShapeFn.autoUniformGridParams()
            sortHits            = True
            hitPoints           = om.MFloatPointArray()
            hitRayParams        = om.MFloatArray()
            hitFaces            = om.MIntArray()
            hitTriangles        = om.MIntArray()
            hitBary1s           = om.MFloatArray()
            hitBary2s           = om.MFloatArray()
            tolerance           = 0.0001
          
            #allIntersections method
            ballShapeFn.allIntersections(raySource, rayDirection, faceIds, triIds, isSorted, om.MSpace.kWorld, maxParam, testBothDirections, accelParams, sortHits, hitPoints, hitRayParams, hitFaces, hitTriangles, hitBary1s, hitBary2s, tolerance )
          
            #getting vectors
            hitPnt1 = hitPoints[0]

#########################################

            #getting the radius * ball's transform matrix
            hitVectTmp = raySource - hitPnt1
            hitVect    = om.MVector(hitVectTmp)
            ballMatrix = ballTransform.transformation().asMatrix()
            hitVect   *= ballMatrix
            radius     = hitVect.length()
           
            #print radius           

            #getting perimeter
            pi    = 3.14159625
            perim = 2*pi*radius
           
            #rolling angle
            rollDeg = ( 360 / perim) * displace
            rollRad = math.radians(rollDeg) * self.weight

            #rotation Components
            quatNew       = self.quater.setAxisAngle(rotationAxis, rollRad)
            
            #setting the ball's transform rotation
            ballTransform.rotateBy(quatNew, om.MSpace.kTransform)
           
#########################################  

            #seting pivot position
            pivotVect = normalVect * (radius + self.heightOffest)
            pivotPnt  = self.clstPnt + pivotVect

#########################################

            self.lastTargetPosition = copy.copy(targetPnt)
            self.lastParamU         = copy.copy(u)
            self.lastParamV         = copy.copy(v)
            self.lastClstPnt        = copy.copy(self.clstPnt)


        # output variable
            self.outputHandle    = dataBlock.outputValue(rollingNode.outPosition)
            self.outputHandle.set3Float(pivotPnt.x, pivotPnt.y, pivotPnt.z)

        dataBlock.setClean(plug)

########################################################################################
########################################################################################

def nodeCreator():
    return omMPx.asMPxPtr(rollingNode())

########################################################################################
########################################################################################

def nodeInitializer():

    #inputs
    nAttr = om.MFnGenericAttribute()
    rollingNode.inRefShape = nAttr.create("inRefShape", "inRef")
    nAttr.addDataAccept( om.MFnData.kNurbsSurface )

    nAttr = om.MFnGenericAttribute()
    rollingNode.ballShape = nAttr.create("ballShape", "ballSurf")
    nAttr.addDataAccept( om.MFnData.kNurbsSurface )
    nAttr.addDataAccept( om.MFnData.kMesh )

    nAttr = om.MFnNumericAttribute()
    rollingNode.targetPos = nAttr.createPoint("targetPosition", "targPos")
    nAttr.setKeyable(True)
    
    nAttr = om.MFnNumericAttribute()
    rollingNode.offset = nAttr.create("offset", "of", om.MFnNumericData.kFloat, 0)
    nAttr.setKeyable(True)
    
    nAttr = om.MFnNumericAttribute()
    rollingNode.weight = nAttr.create("weight", "wt", om.MFnNumericData.kFloat, 1)
    nAttr.setKeyable(True)


    nAttr = om.MFnMessageAttribute()
    rollingNode.blurg = nAttr.create("blurg", "rb")

    rollingNode.addAttribute(rollingNode.inRefShape)
    rollingNode.addAttribute(rollingNode.ballShape)
    rollingNode.addAttribute(rollingNode.targetPos)
    rollingNode.addAttribute(rollingNode.offset)
    rollingNode.addAttribute(rollingNode.weight)

    #outputs
    nAttr = om.MFnNumericAttribute()
    rollingNode.outPosition = nAttr.createPoint("outPosition", "outPos")
    nAttr.setWritable(False)

    rollingNode.addAttribute(rollingNode.outPosition)

    #affects
    rollingNode.attributeAffects(rollingNode.inRefShape, rollingNode.outPosition)
    rollingNode.attributeAffects(rollingNode.targetPos, rollingNode.outPosition)
    rollingNode.attributeAffects(rollingNode.weight, rollingNode.outPosition)
    rollingNode.attributeAffects(rollingNode.offset, rollingNode.outPosition)
    
########################################################################################
########################################################################################

def initializePlugin(mobject):
    mplugin = omMPx.MFnPlugin(mobject)
    try:
        mplugin.registerNode(nodeName, rollingNodeId, nodeCreator, nodeInitializer)
    except:
        sys.stderr.write("Failed to register node: $s\n" % nodeName)

########################################################################################
########################################################################################

def uninitializePlugin(mobject):
    mplugin = omMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterNode(rollingNodeId)
    except:
        sys.stderr.write("Failed to deregister node: $s\n" % nodeName)
