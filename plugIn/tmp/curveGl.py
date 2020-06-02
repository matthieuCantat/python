'''
#FOR TEST
import maya.cmds as mc
path = 'D:\mcantat_BDD\projects\code\maya\python\plugIn\curveGl.py'
mc.file( new = True , f = True )
mc.loadPlugin( path , qt = True )   
'''

import maya.OpenMaya as om
import maya.OpenMayaMPx as ommpx
import maya.cmds as mc
import maya.OpenMayaRender as omr
import time
import utilsMayaNodes as utils
import math
import copy

import python.utils.utilsMayaApi as utilsMayaApi

glRenderer = omr.MHardwareRenderer.theRenderer()
glFT = glRenderer.glFunctionTable()

class curveGl(ommpx.MPxLocatorNode):

    kPluginNodeTypeName = 'curveGl'
    kPluginNodeId = om.MTypeId(0x00033449)

    def __init__(self):
        #print('__init__')
        ommpx.MPxLocatorNode.__init__(self)                                                  
        self.coords        = []                                          
        self.thickness     = 1
        self.color         = [ 0.5 , 0.5 , 0.5 ]                 
        self.camPos        = [] 
        self.v2X           = []
        self.v2Y           = []

        self.distBg    = 500 
        self.distIncr  = 0.01

    def compute( self, plug , dataBlock ):
        print('compute')
        self.coords    = utils.nodeAttrToMVectors( dataBlock , self.attrInCoords      )
        self.thickness = utils.nodeAttrToFloat(    dataBlock , self.attrInThickness   )                  
        self.color     = utils.nodeAttrToMVector(  dataBlock , self.attrInColor       )  

        camMatrix        = utils.nodeAttrToMatrixFloatList( dataBlock , self.attrInCamMatrix )        
        #GET UNIT VECTOR
        self.camPos = om.MFloatVector( camMatrix[12] , camMatrix[13] , camMatrix[14] )         
        self.v2X    = om.MFloatVector( camMatrix[0] , camMatrix[1] , camMatrix[2] )
        self.v2Y    = om.MFloatVector( camMatrix[4] , camMatrix[5] , camMatrix[6] )

        utils.floatToNodeAttr( dataBlock , self.attrOutTrig , 0.0 )

    def draw(self, view, path, style, status):
        print('draw')
        view.beginGL()

        distBg = self.distBg
        #DRAW Curve    
        color = [ self.color.x , self.color.y , self.color.z , 1 ] 
        distBg -= self.distIncr
        for i in range( 1 , len( self.coords ) ):
            points = convertToPointsOnProjPlane( self.camPos , [ self.coords[i] , self.coords[i-1] ]   , self.v2X ,  self.v2Y , distBg )
            glDrawLine( glFT , points , self.thickness , color )

        view.endGL()        

    @classmethod
    def nodeCreator(cls):
        print('nodeCreator')
        return ommpx.asMPxPtr(cls())


    @classmethod
    def nodeInitializer(cls):
        print('nodeInitializer')
        nData = om.MFnNumericData()
        cData = om.MFnNurbsCurveData() 
        mData = om.MFnMeshData() 
        sData = om.MFnStringData()

        nAttr = om.MFnNumericAttribute()  
        eAttr = om.MFnEnumAttribute()
        mAttr = om.MFnMatrixAttribute()
        gAttr = om.MFnGenericAttribute()
        tAttr = om.MFnTypedAttribute()  
        sAttr = om.MFnTypedAttribute()

        # OUT ATTR    
        cls.attrInCamMatrix = mAttr.create( 'inCamMatrix' , 'inCamMatrix' ,  nData.kFloat  )    
        mAttr.setReadable(True) 
        mAttr.setStorable(True)
        mAttr.setConnectable(True)                   
        mAttr.setChannelBox(True) 

        cls.attrInCoords = nAttr.createPoint( 'coords' , 'coords' )    
        nAttr.setReadable(True) 
        nAttr.setStorable(True)
        nAttr.setConnectable(True)          
        nAttr.setArray(True)
        nAttr.isDynamic()     
        nAttr.setUsesArrayDataBuilder(True)

        cls.attrInThickness = nAttr.create( 'thickness', 'thickness' , nData.kFloat  )   
        nAttr.setReadable(True) 
        nAttr.setStorable(True)
        nAttr.setConnectable(True)          

        cls.attrInColor = nAttr.createPoint( 'color', 'color')   
        nAttr.setReadable(True) 
        nAttr.setStorable(True)
        nAttr.setConnectable(True)          

        cls.attrOutTrig = nAttr.create( 'outTrig', 'outTrig' , nData.kFloat  )   
        nAttr.setReadable(True) 
        nAttr.setStorable(True)
        nAttr.setConnectable(True)          

        cls.addAttribute(cls.attrInCamMatrix ) 
        cls.addAttribute(cls.attrInCoords )
        cls.addAttribute(cls.attrInThickness )          
        cls.addAttribute(cls.attrInColor )               
        cls.addAttribute(cls.attrOutTrig )            
        #INFLUENCE
        cls.attributeAffects(cls.attrInCamMatrix   , cls.attrOutTrig )
        cls.attributeAffects(cls.attrInCoords      , cls.attrOutTrig )
        cls.attributeAffects(cls.attrInThickness   , cls.attrOutTrig )          
        cls.attributeAffects(cls.attrInColor       , cls.attrOutTrig )                                                        
 
       
        
def initializePlugin(obj):
    print('initializePlugin')    
    plugin = ommpx.MFnPlugin( obj , 'matthieuCantat', '1.0', 'Any')
    try:
        plugin.registerNode( curveGl.kPluginNodeTypeName, curveGl.kPluginNodeId, curveGl.nodeCreator, curveGl.nodeInitializer, ommpx.MPxNode.kLocatorNode)
    except:
        raise Exception('Failed to register node: {0}'.format(curveGl.kPluginNodeTypeName) )
   

def uninitializePlugin(obj):
    print('uninitializePlugin')  
    plugin = ommpx.MFnPlugin(obj)
    try:
        plugin.deregisterNode( curveGl.kPluginNodeId )
    except:
        raise Exception('Failed to unregister node: {0}'.format(curveGl.kPluginNodeTypeName) )







###############################################################################################################
###############################################################################################################
###############################################################################################################
###############################################################################################################
###############################################################################################################
###############################################################################################################









def glDrawSquare( glFT , point , v2X , v2Y , size , color ):
    squarePoints = getSquarePoint( point , v2X , v2Y , size )
    # PRE GL
    glFT.glEnable(omr.MGL_BLEND)
    #START BUILD
    glFT.glBegin(omr.MGL_QUADS)

    if( len(color) == 3 ):
        glFT.glColor3f(color[0], color[1], color[2])
    elif( len(color) == 4  ):
        glFT.glColor4f(color[0], color[1], color[2] ,  color[3])

    for sPoint in squarePoints:             
        glFT.glVertex3f( sPoint.x , sPoint.y , sPoint.z ) 

    #END BUILD
    glFT.glEnd()
    # PRE GL
    glFT.glDisable(omr.MGL_BLEND) 



def glDrawTriangle2( glFT , triPoints , v2X , v2Y , color ):

    # PRE GL
    glFT.glEnable(omr.MGL_BLEND)
    #START BUILD
    glFT.glBegin(omr.MGL_TRIANGLES)

    if( len(color) == 3 ):
        glFT.glColor3f(color[0], color[1], color[2])
    elif( len(color) == 4  ):
        glFT.glColor4f(color[0], color[1], color[2] ,  color[3])

    for tPoint in triPoints:             
        glFT.glVertex3f( tPoint.x , tPoint.y , tPoint.z ) 

    #END BUILD
    glFT.glEnd()
    # PRE GL
    glFT.glDisable(omr.MGL_BLEND) 

def glDrawTriangle( glFT , point , v2X , v2Y , size , color ):

    triPoints = getTrianglePoint( point , v2X , v2Y , size )
    # PRE GL
    glFT.glEnable(omr.MGL_BLEND)
    #START BUILD
    glFT.glBegin(omr.MGL_TRIANGLES)

    if( len(color) == 3 ):
        glFT.glColor3f(color[0], color[1], color[2])
    elif( len(color) == 4  ):
        glFT.glColor4f(color[0], color[1], color[2] ,  color[3])

    for tPoint in triPoints:             
        glFT.glVertex3f( tPoint.x , tPoint.y , tPoint.z ) 

    #END BUILD
    glFT.glEnd()
    # PRE GL
    glFT.glDisable(omr.MGL_BLEND) 

def glDrawStar( glFT , point , v2X , v2Y , size , color ):

    starPoints = getStarPoint( point , v2X , v2Y , size )
    # PRE GL
    glFT.glEnable(omr.MGL_BLEND)
    #START BUILD
    glFT.glBegin(omr.MGL_POLYGON)

    if( len(color) == 3 ):
        glFT.glColor3f(color[0], color[1], color[2])
    elif( len(color) == 4  ):
        glFT.glColor4f(color[0], color[1], color[2] ,  color[3])

    for sPoint in starPoints:             
        glFT.glVertex3f( sPoint.x , sPoint.y , sPoint.z ) 

    #END BUILD
    glFT.glEnd()
    # PRE GL
    glFT.glDisable(omr.MGL_BLEND) 


def glDrawLoadBar( glFT , point , length , v2X , v2Y , size , color ):

    # PRE GL
    glFT.glEnable(omr.MGL_BLEND)
    glFT.glPushAttrib( omr.MGL_LINE_BIT ) 
    glFT.glLineWidth( size )     
    #START BUILD
    glFT.glBegin(omr.MGL_LINES) 

    if( len(color) == 3 ):
        glFT.glColor3f(color[0], color[1], color[2])
    elif( len(color) == 4  ):
        glFT.glColor4f(color[0], color[1], color[2] ,  color[3])

                
    glFT.glVertex3f( point.x , point.y , point.z ) 
    glFT.glVertex3f( point.x + v2X.x * length , point.y + v2X.y * length , point.z + v2X.z * length )
    #END BUILD
    glFT.glEnd()
    # PRE GL
    glFT.glDisable(omr.MGL_BLEND) 
    glFT.glPopAttrib()

def glDrawCircle( glFT , point , nbrSample , v2X , v2Y , size , color , line ):
    circlePoints = getCirclePoint( point , nbrSample , v2X , v2Y , size )
    # PRE GL
    glFT.glEnable(omr.MGL_BLEND)
    #START BUILD
    if( 0 < line ):
        glFT.glPushAttrib( omr.MGL_LINE_BIT )
        glFT.glLineWidth( line )            
        glFT.glBegin(omr.MGL_LINES)    
    else:
        glFT.glBegin(omr.MGL_POLYGON)

    if( len(color) == 3 ):
        glFT.glColor3f(color[0], color[1], color[2])
    elif( len(color) == 4  ):
        glFT.glColor4f(color[0], color[1], color[2] ,  color[3])

    for cPoint in circlePoints:             
        glFT.glVertex3f( cPoint.x , cPoint.y , cPoint.z ) 

    #END BUILD
    glFT.glEnd()
    # PRE GL
    glFT.glDisable(omr.MGL_BLEND) 
    if( 0 < line ):
        glFT.glPopAttrib()


def glDrawVector( glFT , points , camPoint ,  v2X , v2Y , sizeArrow ,sizeLine , color ):
    vectorPoints = getVectorPoint( points , camPoint , v2X , v2Y , sizeArrow )
    glDrawTriangle2( glFT ,[ vectorPoints[1] , vectorPoints[2] , vectorPoints[3] ] , v2X , v2Y , color )      
    # PRE GL
    glFT.glEnable(omr.MGL_BLEND)
    glFT.glPushAttrib( omr.MGL_LINE_BIT ) 
    glFT.glLineWidth( sizeLine )   
    #START BUILD
    glFT.glBegin(omr.MGL_LINES)
    if( len(color) == 3 ):
        glFT.glColor3f(color[0], color[1], color[2])
    elif( len(color) == 4  ):
        glFT.glColor4f(color[0], color[1], color[2] ,  color[3])

    glFT.glVertex3f( vectorPoints[0].x , vectorPoints[0].y , vectorPoints[0].z )
    glFT.glVertex3f( vectorPoints[1].x , vectorPoints[1].y , vectorPoints[1].z )

    glFT.glEnd()
    # PRE GL       
    glFT.glDisable(omr.MGL_BLEND) 
    glFT.glPopAttrib()


def glDrawLine( glFT , points , sizeLine , color ):
 
    # PRE GL
    if( 0 < sizeLine ):
        glFT.glPushAttrib( omr.MGL_LINE_BIT ) 
        glFT.glLineWidth( sizeLine ) 
    glFT.glEnable(omr.MGL_BLEND)          
    #START BUILD
    glFT.glBegin(omr.MGL_LINES)
    if( len(color) == 3 ):
        glFT.glColor3f(color[0], color[1], color[2])
    elif( len(color) == 4  ):
        glFT.glColor4f(color[0], color[1], color[2] ,  color[3])

    glFT.glVertex3f( points[0].x , points[0].y , points[0].z )
    glFT.glVertex3f( points[1].x , points[1].y , points[1].z )

    glFT.glEnd()
    # PRE GL
    glFT.glDisable(omr.MGL_BLEND)    
    if( 0 < sizeLine ):     
        glFT.glPopAttrib()          



def getSquarePoint( point , v2X , v2Y , size ):
    squarePoints = []
    squarePoints.append( point+(-v2X+v2Y)*size )
    squarePoints.append( point+( v2X+v2Y)*size )
    squarePoints.append( point+( v2X-v2Y)*size )
    squarePoints.append( point+(-v2X-v2Y)*size )
    return squarePoints



def getTrianglePoint( point , v2X , v2Y , size ):
    trianglePoints = []
    trianglePoints.append( point+(v2Y)*size )
    trianglePoints.append( point+( v2X-v2Y)*size )
    trianglePoints.append( point+(-v2X-v2Y)*size )
    return trianglePoints

'''
def getStarPoint( point , v2X , v2Y , size ):
    starPoints = []
    starPoints.append( point+( v2X * -0.349 + v2Y * -0.5  )*size )
    starPoints.append( point+( v2X * 0      + v2Y * 0.492 )*size )
    starPoints.append( point+( v2X *  0.349 + v2Y * -0.5  )*size )
    starPoints.append( point+( v2X * -0.505 + v2Y * 0.103 )*size )
    starPoints.append( point+( v2X *  0.505 + v2Y * 0.103 )*size )
    starPoints.append( point+( v2X * -0.349 + v2Y * -0.5  )*size )            
    return starPoints
'''

def getStarPoint( point , v2X , v2Y , size ):
    starPoints = []
    starPoints.append( point+( v2X *  0     + v2Y * -0.254)*size )      
    starPoints.append( point+( v2X * -0.349 + v2Y * -0.5   )*size )
    starPoints.append( point+( v2X * -0.21  + v2Y * -0.105 )*size )
    starPoints.append( point+( v2X * -0.505 + v2Y * 0.103  )*size )
    starPoints.append( point+( v2X * -0.137 + v2Y * 0.103  )*size )
    starPoints.append( point+( v2X * 0      + v2Y * 0.492  )*size )
    starPoints.append( point+( v2X *  0.137 + v2Y * 0.103  )*size )
    starPoints.append( point+( v2X *  0.505 + v2Y * 0.103  )*size )
    starPoints.append( point+( v2X *  0.21  + v2Y * -0.105 )*size )
    starPoints.append( point+( v2X *  0.349 + v2Y * -0.5   )*size )
    starPoints.append( point+( v2X *  0     + v2Y * -0.254)*size )            
    return starPoints






def getCirclePoint( point , nbrSample , v2X , v2Y , radius ):
 
    maxAngle = 2 * math.pi
    incrAngle = maxAngle / nbrSample 
    angle = 0
    circlePoints = []
    while( angle < maxAngle ):
        x = math.cos( angle + incrAngle ) * radius
        y = math.sin( angle + incrAngle ) * radius
        vRadius = v2X * x + v2Y * y    
        circlePoints.append( point + vRadius )
        angle += incrAngle    

    return circlePoints



def getVectorPoint( points , camPoint , v2X , v2Y , size ):
    vectorPoints = []
    vectorPoints.append( points[0] )
    vectorPoints.append( points[1] )

    vectorA = points[0] - points[1]
    vectorB = camPoint - points[1]
    vectorPerp = vectorA^vectorB
    vectorA.normalize()
    vectorPerp.normalize()

    pointsArrowSideA = points[1] + vectorA * size + vectorPerp * size
    pointsArrowSideB = points[1] + vectorA * size - vectorPerp * size

    vectorPoints.append( pointsArrowSideA )
    vectorPoints.append( pointsArrowSideB )    
    return vectorPoints






def convertToPointsOnProjPlane( pointO , points , v2X ,  v2Y , distance ):
    iPoints = []
    for point in points:
        iPoints.append( convertToPointOnProjPlane( pointO , point , v2X ,  v2Y , distance ) )
    return iPoints





def convertToPointOnProjPlane( pointO , point , v2X ,  v2Y , distance ):

    vectorTmp = om.MFloatVector( point.x - pointO.x , point.y - pointO.y , point.z - pointO.z )
    vectorTmp.normalize()
    pointTmp = pointO + vectorTmp * distance

    planeCoords = [ pointTmp.x , pointTmp.y , pointTmp.z , pointTmp.x + v2X.x , pointTmp.y + v2X.y , pointTmp.z + v2X.z  , pointTmp.x + v2Y.x , pointTmp.y + v2Y.y , pointTmp.z + v2Y.z ]
    lineCoords  = [ pointO.x , pointO.y , pointO.z , point.x , point.y , point.z ]
    iPoint = utils_getLinePlaneIntersectionPoint( lineCoords , planeCoords )

    return om.MFloatVector( iPoint[0] , iPoint[1] , iPoint[2] )




def utils_getLinePlaneIntersectionPoint( lineCoords , planeCoords ):
    #GET CLOSEST POINT
    closestPointPlane = utils_getClosestPointOnPlane( lineCoords[0:3] , planeCoords )
    #GET ANGLE CLOSEST POINT PLANE - lineO - lineEND    
    vPlaneLineO = om.MVector( closestPointPlane[0] - lineCoords[0] , closestPointPlane[1] - lineCoords[1] , closestPointPlane[2] - lineCoords[2] )
    vline = om.MVector( lineCoords[3] - lineCoords[0] , lineCoords[4] - lineCoords[1] , lineCoords[5] - lineCoords[2] ) 
    dotPoduct = math.copysign( 1 , vline*vPlaneLineO )
    vline *= dotPoduct
    angle = vline.angle(vPlaneLineO)
    #DISTANCE CLOSEST POINT PLANE
    distClosestPointPlane = vPlaneLineO.length()
    #TRIGO: GET DISTANCE LINE ORIGINE - INTERSECTION POINT
    distLineOInter  = abs(distClosestPointPlane / math.cos(angle) )
    #GET INTERSECTION POINT
    vline.normalize()   
    vline *= distLineOInter     
    intersectionPoint = [ vline.x + lineCoords[0] , vline.y + lineCoords[1] , vline.z + lineCoords[2] ]
    return intersectionPoint

def utils_getClosestPointOnPlane( coords , planeCoords ):
    #GET PLANE NORMAL
    planVectorA      =  [ ( planeCoords[3] - planeCoords[0] ) , ( planeCoords[4] - planeCoords[1] ) , ( planeCoords[5] - planeCoords[2] )  ] 
    planVectorB      =  [ ( planeCoords[6] - planeCoords[0] ) , ( planeCoords[7] - planeCoords[1] ) , ( planeCoords[8] - planeCoords[2] )  ]    
    normalDir        =  [ ( planeCoords[0] - coords[0]    )   , ( planeCoords[1] - coords[1]    )   , ( planeCoords[2] - coords[2]      )  ]            
    vPlaneNormal = utils_get2VectorsNormal( planVectorA , planVectorB , normalDir  )
    #GET d OF THE PLAN EQUATION  2x + 3y + 7z +d = 0    
    d = ( ( vPlaneNormal[0] *  planeCoords[0] ) + ( vPlaneNormal[1] *  planeCoords[1] ) + ( vPlaneNormal[2] *  planeCoords[2] ) ) * -1 
    #GET DIST BETWEEN POINT AND PLANE
    dist = (  - ( vPlaneNormal[0] * coords[0] ) - ( vPlaneNormal[1] * coords[1] ) - ( vPlaneNormal[2] * coords[2] ) - d  ) / ( ( vPlaneNormal[0] * vPlaneNormal[0] ) + ( vPlaneNormal[1] * vPlaneNormal[1] ) + ( vPlaneNormal[2] * vPlaneNormal[2] )   )        
    #GET INTERSECT COORDS       
    iCoords = [  vPlaneNormal[0] * dist + coords[0] , vPlaneNormal[1] * dist + coords[1] , vPlaneNormal[2] * dist + coords[2] ] 
    return iCoords


def utils_get2VectorsNormal( vectorA , vectorB , vDir ):
    #GET NORMAL
    normalx = ((vectorA[1])*(vectorB[2])-(vectorA[2])*(vectorB[1]))
    normaly = ((vectorA[2])*(vectorB[0])-(vectorA[0])*(vectorB[2]))
    normalz = ((vectorA[0])*(vectorB[1])-(vectorA[1])*(vectorB[0]))
    vecteurNormal = om.MVector( normalx   , normaly   , normalz   )
    #GET MODIF IT WITH VECTOR DIR
    vectorDirection   = om.MVector( vDir[0] , vDir[1] , vDir[2] )     
    coef = math.copysign( 1 , vecteurNormal*vectorDirection )       
    vecteurNormal = om.MVector( vecteurNormal.x * coef , vecteurNormal.y * coef  , vecteurNormal.z * coef  )
    return [ vecteurNormal.x , vecteurNormal.y , vecteurNormal.z ]      




#______________________________________________________________DynamicStore

class DynamicStore():

    def __init__(self , arrayFill , maxIndex ):
        self.maxIndex = maxIndex 

        self.storeValues = []
        for i in range( 0 , self.maxIndex + 1 ) : 
            self.storeValues.append( arrayFill )


    def __getitem__( self, index ): 
        return self.storeValues[index]

    def addFirst( self , valueToAdd):
        #ONLY WORK WITH M FLOAT VECTOR

        #SHIFT ALL THE VALUES
        for i in range( len(self.storeValues) , 0 , -1 ):
            if( i <= self.maxIndex ):
                self.storeValues[i] = self.storeValues[i-1][:]
            
        #MFLOAT VECTOR
        valueToAddCopy = []
        for value in valueToAdd:
            valueToAddCopy.append( om.MFloatVector(value) )

        #ADDValue
        self.storeValues[0] = valueToAddCopy
         