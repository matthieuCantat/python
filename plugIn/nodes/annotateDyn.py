'''
#FOR TEST
import maya.cmds as mc
path = 'D:\mcantat_BDD\projects\code\maya\python\plugIn\annotateDyn.py'
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
import python.classe.trsBackUp as trsClass 

glRenderer = omr.MHardwareRenderer.theRenderer()
glFT = glRenderer.glFunctionTable()

class annotateDyn(ommpx.MPxLocatorNode):

    kPluginNodeTypeName = 'annotateDyn'
    kPluginNodeId = om.MTypeId(0x00033448)

    def __init__(self):
        #print('__init__')
        ommpx.MPxLocatorNode.__init__(self)                                                  
        self.vectors       = []                                          
        self.vectorsSize   = []
        self.vectorsColor  = []
        self.vectorsName   = []
        self.triangles     = []
        self.trianglesSize = []              
        self.trianglesColor= []                             
        self.squares       = []
        self.squaresSize   = []            
        self.squaresColor  = [] 
        self.circles       = []
        self.circlesSize   = []                
        self.circlesColor  = []                    
        self.camPos        = [] 
        self.v2X           = []
        self.v2Y           = []
        self.distProjInt = 1
        self.distIncr = 0.01
        self.motionTrailMaxMemory = 40
        self.pointO = om.MFloatVector(0.0,0.0,0.0)
        self.StorePoints = DynamicStore( arrayFill = [self.pointO,self.pointO,self.pointO,self.pointO] , maxIndex = self.motionTrailMaxMemory )
        self.motionTrailSizeLast = 0


    def compute( self, plug , dataBlock ):
        #print('compute')                                                  
        self.vectors            = utils.nodeAttrToMVectors(   dataBlock , self.attrInVectors      )                                            
        self.vectorsSize        = utils.nodeAttrToFloatArray( dataBlock , self.attrInVectorsSize  )
        self.vectorsColor       = utils.nodeAttrToMVectors(   dataBlock , self.attrInVectorsColor )
        self.vectorsName        = utils.nodeAttrToMStrings(   dataBlock , self.attrInVectorsName )        
        self.triangles          = utils.nodeAttrToMVectors(   dataBlock , self.attrInTriangles    )
        self.trianglesSize      = utils.nodeAttrToFloatArray( dataBlock , self.attrInTrianglesSize  )              
        self.trianglesColor     = utils.nodeAttrToMVectors(   dataBlock , self.attrInTrianglesColor )
        self.trianglesName      = utils.nodeAttrToMStrings(   dataBlock , self.attrInTrianglesName )                                      
        self.squares            = utils.nodeAttrToMVectors(   dataBlock , self.attrInSquares      )
        self.squaresSize        = utils.nodeAttrToFloatArray( dataBlock , self.attrInSquaresSize  )              
        self.squaresColor       = utils.nodeAttrToMVectors(   dataBlock , self.attrInSquaresColor )  
        self.squaresName        = utils.nodeAttrToMStrings(   dataBlock , self.attrInSquaresName  )          
        self.circles            = utils.nodeAttrToMVectors(   dataBlock , self.attrInCircles      )
        self.circlesSize        = utils.nodeAttrToFloatArray( dataBlock , self.attrInCirclesSize  )                  
        self.circlesColor       = utils.nodeAttrToMVectors(   dataBlock , self.attrInCirclesColor )  
        self.circlesName        = utils.nodeAttrToMStrings(   dataBlock , self.attrInCirclesName  )
        self.stars              = utils.nodeAttrToMVectors(   dataBlock , self.attrInStars      )
        self.starsSize          = utils.nodeAttrToFloatArray( dataBlock , self.attrInStarsSize  )                  
        self.starsColor         = utils.nodeAttrToMVectors(   dataBlock , self.attrInStarsColor )  
        self.starsName          = utils.nodeAttrToMStrings(   dataBlock , self.attrInStarsName  )

        self.motionTrail           = utils.nodeAttrToMVectors(   dataBlock , self.attrInMotionTrail      )
        self.motionTrailSize       = utils.nodeAttrToFloatArray( dataBlock , self.attrInMotionTrailSize  )                  
        self.motionTrailColor      = utils.nodeAttrToMVectors(   dataBlock , self.attrInMotionTrailColor )  
        self.motionTrailName       = utils.nodeAttrToMStrings(   dataBlock , self.attrInMotionTrailName  )
        self.motionTrailWorldSpace = utils.nodeAttrToInt(   dataBlock , self.attrInMotionTrailWorldSpace )
        self.motionTrailMaxMemory  = utils.nodeAttrToInt(   dataBlock , self.attrInMotionTrailMaxMemory  )

        self.pointTransparency       = utils.nodeAttrToFloat( dataBlock , self.attrInPointTransparency       )
        self.vectorTransparency      = utils.nodeAttrToFloat( dataBlock , self.attrInVectorTransparency      )
        self.motionTrailTransparency = utils.nodeAttrToFloat( dataBlock , self.attrInMotionTrailTransparency )
        self.motionTrailLinkTransparency = utils.nodeAttrToFloat( dataBlock , self.attrInMotionTrailLinkTransparency )

        self.textPos            = utils.nodeAttrToMVector(    dataBlock , self.attrInTextPos      )                    

        camMatrix          = utils.nodeAttrToMatrixFloatList( dataBlock , self.attrInCamMatrix )        
        #GET UNIT VECTOR
        self.camPos = om.MFloatVector( camMatrix[12] , camMatrix[13] , camMatrix[14] )         
        self.v2X    = om.MFloatVector( camMatrix[0] , camMatrix[1] , camMatrix[2] )
        self.v2Y    = om.MFloatVector( camMatrix[4] , camMatrix[5] , camMatrix[6] )


        for i in range( 0 , len(self.motionTrail) ):
            if not( self.motionTrail[i] == self.StorePoints[0][i] ):
                self.StorePoints.addFirst( self.motionTrail )
                break


        utils.floatToNodeAttr( dataBlock , self.attrOutTrig , 0.0 )



    def draw(self, view, path, style, status):
        #print('draw')
        view.beginGL()

        sizeAnnotation = 0.01
        sizeLine = 5
        sampleCircle = 60
        textIncr = 0.025
        textIncrLoadBar = 0.001   
        loadBarSize = 0.01     
        textShift = 2
        sizeIcone = 0.01
        dist = self.distProjInt 
        distBg = 500       
        textPos = convertToPointOnProjPlane( self.camPos , self.textPos  , self.v2X ,  self.v2Y , dist )


        #DRAW MOTION TRAIL LINK    
        index = 0
        for i in range( 1 , len( self.motionTrail ) ):
            color = [ 0.5 , 0.5 , 0.5 , self.motionTrailLinkTransparency ]                                 
            for j in range( 0 , self.StorePoints.maxIndex ):
                points = convertToPointsOnProjPlane( self.camPos , [ self.StorePoints[j][i] , self.StorePoints[j][i-1] ]   , self.v2X ,  self.v2Y , distBg )
                if( 0 < color[3] ):
                    glDrawLine( glFT , points , 0 , color )

        #DRAW MOTION TRAIL     
        index = 0
        for i in range( 0 , len( self.motionTrail ) ):
            distBg -= self.distIncr

            color = [ self.motionTrailColor[i].x , self.motionTrailColor[i].y , self.motionTrailColor[i].z , self.motionTrailTransparency  ]                                 
            for j in range( 1 , self.StorePoints.maxIndex ):
                points = convertToPointsOnProjPlane( self.camPos , [ self.StorePoints[j][i] , self.StorePoints[j-1][i] ]   , self.v2X ,  self.v2Y , distBg )
                if( 0 < color[3] ):
                    glDrawLine( glFT , points , sizeLine , color )

            #DRAW UI           
            view.drawText( self.motionTrailName[i] , om.MPoint(textPos) )
            textPos = textPos - self.v2Y * textIncr 




        #DRAW CRICLE
        for i in range( 0 , len( self.circles ) ):
            dist -= self.distIncr
            point = convertToPointOnProjPlane( self.camPos , self.circles[i]  , self.v2X ,  self.v2Y , dist )

            #COMPUTE RADIUS
            rPoint = self.circles[i] + self.v2X * self.circlesSize[i]
            rPointProj = convertToPointOnProjPlane( self.camPos , rPoint  , self.v2X ,  self.v2Y , dist )
            vRadiusProj = rPointProj - point 
            color = [ self.circlesColor[i].x , self.circlesColor[i].y , self.circlesColor[i].z , 1  ]
            if( 0 < color[3] ):
                glDrawCircle( glFT , point  , sampleCircle ,  self.v2X , self.v2Y , vRadiusProj.length() , color , sizeLine )

            #DRAW UI
            glDrawCircle( glFT , textPos  , sampleCircle , self.v2X , self.v2Y , sizeIcone , color , sizeLine  )        
            view.drawText( self.circlesName[i] , om.MPoint( textPos + self.v2X * sizeIcone * textShift ) )
            textPos = textPos - self.v2Y * textIncr 


        #DRAW SQUARE
        for i in range( 0 , len( self.squares ) ):
            dist -= self.distIncr
            point = convertToPointOnProjPlane( self.camPos , self.squares[i]   , self.v2X ,  self.v2Y , dist )
            color = [ self.squaresColor[i].x , self.squaresColor[i].y , self.squaresColor[i].z , self.pointTransparency  ]
            if( 0 < color[3] ):           
                glDrawSquare( glFT , point , self.v2X , self.v2Y , self.squaresSize[i] * sizeAnnotation , color )
            
            #DRAW UI
            glDrawSquare( glFT , textPos  , self.v2X , self.v2Y , sizeIcone , color )        
            view.drawText( self.squaresName[i] , om.MPoint( textPos + self.v2X * sizeIcone * textShift ) )
            textPos = textPos - self.v2Y * textIncr 

        #DRAW STAR
        for i in range( 0 , len( self.stars ) ):
            dist -= self.distIncr          
            point = convertToPointOnProjPlane( self.camPos , self.stars[i]   , self.v2X ,  self.v2Y , dist ) 
            color = [ self.starsColor[i].x , self.starsColor[i].y , self.starsColor[i].z , self.pointTransparency  ]
            if( 0 < color[3] ):                         
                glDrawStar( glFT , point  , self.v2X , self.v2Y , self.starsSize[i] * sizeAnnotation , color )

            #DRAW UI
            glDrawStar( glFT , textPos  , self.v2X , self.v2Y , sizeIcone , color )        
            view.drawText( self.starsName[i] , om.MPoint( textPos + self.v2X * sizeIcone * textShift ) )
            textPos = textPos - self.v2Y * textIncr 


        #DRAW TRIANGLE
        for i in range( 0 , len( self.triangles ) ):
            dist -= self.distIncr             
            point = convertToPointOnProjPlane( self.camPos , self.triangles[i]   , self.v2X ,  self.v2Y , dist )
            color = [ self.trianglesColor[i].x , self.trianglesColor[i].y , self.trianglesColor[i].z , self.pointTransparency  ]
            if( 0 < color[3] ):                        
                glDrawTriangle( glFT , point  , self.v2X , self.v2Y , self.trianglesSize[i] * sizeAnnotation , color )

            #DRAW UI
            glDrawTriangle( glFT , textPos  , self.v2X , self.v2Y , sizeIcone , color )        
            view.drawText( self.trianglesName[i] , om.MPoint( textPos + self.v2X * sizeIcone * textShift ) )
            textPos = textPos - self.v2Y * textIncr 

        #DRAW VECTOR      
        index = 0
        for i in range( 0 , len( self.vectors ) , 2 ):
            dist -= self.distIncr
            points = convertToPointsOnProjPlane( self.camPos , [ self.vectors[i] , self.vectors[i+1] ]   , self.v2X ,  self.v2Y , dist )
            color = [ self.vectorsColor[index].x , self.vectorsColor[index].y , self.vectorsColor[index].z , self.vectorTransparency  ] 
            if( 0 < color[3] ):                                 
                glDrawVector( glFT , points , self.camPos , self.v2X , self.v2Y , self.vectorsSize[index] * sizeAnnotation , sizeLine , color )

            #DRAW UI           
            view.drawText( self.vectorsName[index] , om.MPoint(textPos) )
            textPos = textPos - self.v2Y * textIncrLoadBar 
            glDrawLoadBar( glFT , textPos , (self.vectors[i+1] - self.vectors[i]).length() * loadBarSize  , self.v2X , self.v2Y , 3 , color )
            textPos = textPos - self.v2Y * textIncr

            index += 1
    
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

        cls.attrInVectors= nAttr.createPoint( 'inVectors' , 'inVectors' )    
        nAttr.setReadable(True) 
        nAttr.setStorable(True)
        nAttr.setConnectable(True)          
        nAttr.setArray(True)
        nAttr.isDynamic()     
        nAttr.setUsesArrayDataBuilder(True)

        cls.attrInVectorsSize = nAttr.create( 'inVectorsSize', 'inVectorsSize' , nData.kFloat  )   
        nAttr.setReadable(True) 
        nAttr.setStorable(True)
        nAttr.setConnectable(True)          
        nAttr.setArray(True)
        nAttr.isDynamic()     
        nAttr.setUsesArrayDataBuilder(True) 

        cls.attrInVectorsColor = nAttr.createPoint( 'inVectorsColor' , 'inVectorsColor' )   
        nAttr.setReadable(True) 
        nAttr.setStorable(True)
        nAttr.setConnectable(True)          
        nAttr.setArray(True)
        nAttr.isDynamic()     
        nAttr.setUsesArrayDataBuilder(True)         



        cls.attrInVectorsName = sAttr.create("inVectorsName", "inVectorsName", sData.kString)
        sAttr.setReadable(True) 
        sAttr.setStorable(True)
        sAttr.setConnectable(True)          
        sAttr.setArray(True)
        sAttr.isDynamic()     
        sAttr.setUsesArrayDataBuilder(True)      


        cls.attrInSquares = nAttr.createPoint( 'inSquares' , 'inSquares' )    
        nAttr.setReadable(True) 
        nAttr.setStorable(True)
        nAttr.setConnectable(True)          
        nAttr.setArray(True)
        nAttr.isDynamic()     
        nAttr.setUsesArrayDataBuilder(True)

        cls.attrInSquaresSize = nAttr.create( 'inSquaresSize', 'inSquaresSize' , nData.kFloat  )   
        nAttr.setReadable(True) 
        nAttr.setStorable(True)
        nAttr.setConnectable(True)          
        nAttr.setArray(True)
        nAttr.isDynamic()     
        nAttr.setUsesArrayDataBuilder(True) 

        cls.attrInSquaresColor = nAttr.createPoint( 'inSquaresColor', 'inSquaresColor' )    
        nAttr.setReadable(True) 
        nAttr.setStorable(True)
        nAttr.setConnectable(True)          
        nAttr.setArray(True)
        nAttr.isDynamic()     
        nAttr.setUsesArrayDataBuilder(True) 


        cls.attrInSquaresName = sAttr.create("inSquaresName", "inSquaresName", sData.kString)
        sAttr.setReadable(True) 
        sAttr.setStorable(True)
        sAttr.setConnectable(True)          
        sAttr.setArray(True)
        sAttr.isDynamic()     
        sAttr.setUsesArrayDataBuilder(True)    


        cls.attrInTriangles = nAttr.createPoint( 'inTriangles' , 'inTriangles' )    
        nAttr.setReadable(True) 
        nAttr.setStorable(True)
        nAttr.setConnectable(True)          
        nAttr.setArray(True)
        nAttr.isDynamic()     
        nAttr.setUsesArrayDataBuilder(True)

        cls.attrInTrianglesSize = nAttr.create( 'inTrianglesSize', 'inTrianglesSize' , nData.kFloat  )   
        nAttr.setReadable(True) 
        nAttr.setStorable(True)
        nAttr.setConnectable(True)          
        nAttr.setArray(True)
        nAttr.isDynamic()     
        nAttr.setUsesArrayDataBuilder(True) 

        cls.attrInTrianglesColor = nAttr.createPoint( 'inTrianglesColor', 'inTrianglesColor' )    
        nAttr.setReadable(True) 
        nAttr.setStorable(True)
        nAttr.setConnectable(True)          
        nAttr.setArray(True)
        nAttr.isDynamic()     
        nAttr.setUsesArrayDataBuilder(True) 


        cls.attrInTrianglesName = sAttr.create("inTrianglesName", "inTrianglesName", sData.kString)
        sAttr.setReadable(True) 
        sAttr.setStorable(True)
        sAttr.setConnectable(True)          
        sAttr.setArray(True)
        sAttr.isDynamic()     
        sAttr.setUsesArrayDataBuilder(True)  


        cls.attrInCircles = nAttr.createPoint( 'inCircles' , 'inCircles' )    
        nAttr.setReadable(True) 
        nAttr.setStorable(True)
        nAttr.setConnectable(True)          
        nAttr.setArray(True)
        nAttr.isDynamic()     
        nAttr.setUsesArrayDataBuilder(True)

        cls.attrInCirclesSize = nAttr.create( 'inCirclesSize', 'inCirclesSize' , nData.kFloat  )   
        nAttr.setReadable(True) 
        nAttr.setStorable(True)
        nAttr.setConnectable(True)          
        nAttr.setArray(True)
        nAttr.isDynamic()     
        nAttr.setUsesArrayDataBuilder(True) 

        cls.attrInCirclesColor = nAttr.createPoint( 'inCirclesColor', 'inCirclesColor')   
        nAttr.setReadable(True) 
        nAttr.setStorable(True)
        nAttr.setConnectable(True)          
        nAttr.setArray(True)
        nAttr.isDynamic()     
        nAttr.setUsesArrayDataBuilder(True)


        cls.attrInCirclesName = sAttr.create("inCirclesName", "inCirclesName", sData.kString)
        sAttr.setReadable(True) 
        sAttr.setStorable(True)
        sAttr.setConnectable(True)          
        sAttr.setArray(True)
        sAttr.isDynamic()     
        sAttr.setUsesArrayDataBuilder(True)  


        cls.attrInStars = nAttr.createPoint( 'inStars' , 'inStars' )    
        nAttr.setReadable(True) 
        nAttr.setStorable(True)
        nAttr.setConnectable(True)          
        nAttr.setArray(True)
        nAttr.isDynamic()     
        nAttr.setUsesArrayDataBuilder(True)

        cls.attrInStarsSize = nAttr.create( 'inStarsSize', 'inStarsSize' , nData.kFloat  )   
        nAttr.setReadable(True) 
        nAttr.setStorable(True)
        nAttr.setConnectable(True)          
        nAttr.setArray(True)
        nAttr.isDynamic()     
        nAttr.setUsesArrayDataBuilder(True) 

        cls.attrInStarsColor = nAttr.createPoint( 'inStarsColor', 'inStarsColor')   
        nAttr.setReadable(True) 
        nAttr.setStorable(True)
        nAttr.setConnectable(True)          
        nAttr.setArray(True)
        nAttr.isDynamic()     
        nAttr.setUsesArrayDataBuilder(True)


        cls.attrInStarsName = sAttr.create("inStarsName", "inStarsName", sData.kString)
        sAttr.setReadable(True) 
        sAttr.setStorable(True)
        sAttr.setConnectable(True)          
        sAttr.setArray(True)
        sAttr.isDynamic()     
        sAttr.setUsesArrayDataBuilder(True)  



        cls.attrInMotionTrail = nAttr.createPoint( 'inMotionTrails' , 'inMotionTrails' )    
        nAttr.setReadable(True) 
        nAttr.setStorable(True)
        nAttr.setConnectable(True)          
        nAttr.setArray(True)
        nAttr.isDynamic()     
        nAttr.setUsesArrayDataBuilder(True)

        cls.attrInMotionTrailSize = nAttr.create( 'inMotionTrailsSize', 'inMotionTrailsSize' , nData.kFloat  )   
        nAttr.setReadable(True) 
        nAttr.setStorable(True)
        nAttr.setConnectable(True)          
        nAttr.setArray(True)
        nAttr.isDynamic()     
        nAttr.setUsesArrayDataBuilder(True) 

        cls.attrInMotionTrailColor = nAttr.createPoint( 'inMotionTrailsColor', 'inMotionTrailsColor')   
        nAttr.setReadable(True) 
        nAttr.setStorable(True)
        nAttr.setConnectable(True)          
        nAttr.setArray(True)
        nAttr.isDynamic()     
        nAttr.setUsesArrayDataBuilder(True)


        cls.attrInMotionTrailName = sAttr.create("inMotionTrailsName", "inMotionTrailsName", sData.kString)
        sAttr.setReadable(True) 
        sAttr.setStorable(True)
        sAttr.setConnectable(True)          
        sAttr.setArray(True)
        sAttr.isDynamic()     
        sAttr.setUsesArrayDataBuilder(True)  


        cls.attrInMotionTrailWorldSpace = nAttr.create( 'inMotionTrailsWorldSpace', 'inMotionTrailsWorldSpace' , nData.kInt  )   
        nAttr.setReadable(True) 
        nAttr.setStorable(True)
        nAttr.setConnectable(True)          
        nAttr.setMin(0)  
        nAttr.setMax(1)                     
        nAttr.setDefault(1)  

        cls.attrInMotionTrailMaxMemory = nAttr.create( 'inMotionTrailsMaxMemory', 'inMotionTrailsMaxMemory' , nData.kInt  )   
        nAttr.setReadable(True) 
        nAttr.setStorable(True)
        nAttr.setConnectable(True)   
        nAttr.setMin(0)                   
        nAttr.setDefault(40)  

        cls.attrInTextPos = nAttr.createPoint( 'inTextPos', 'inTextPos')  
        nAttr.setReadable(True) 
        nAttr.setStorable(True)
        nAttr.setConnectable(True)

        cls.attrInPointTransparency = nAttr.create( 'inPointTransparency', 'inPointTransparency' , nData.kFloat  )   
        nAttr.setReadable(True) 
        nAttr.setStorable(True)
        nAttr.setConnectable(True)
        nAttr.setChannelBox(True)         
        nAttr.setMin(0.0)  
        nAttr.setMax(1.0)                     
        nAttr.setDefault(1.0)  

        cls.attrInVectorTransparency = nAttr.create( 'inVectorTransparency', 'inVectorTransparency' , nData.kFloat  )   
        nAttr.setReadable(True) 
        nAttr.setStorable(True)
        nAttr.setConnectable(True)           
        nAttr.setChannelBox(True)         
        nAttr.setMin(0.0)  
        nAttr.setMax(1.0)                     
        nAttr.setDefault(1.0) 

        cls.attrInMotionTrailTransparency = nAttr.create( 'inMTrailTransparency', 'inMTrailTransparency' , nData.kFloat  )   
        nAttr.setReadable(True) 
        nAttr.setStorable(True)
        nAttr.setConnectable(True)           
        nAttr.setChannelBox(True)         
        nAttr.setMin(0.0)  
        nAttr.setMax(1.0)                     
        nAttr.setDefault(1.0) 

        cls.attrInMotionTrailLinkTransparency = nAttr.create( 'inMTrailTransparency2', 'inMTrailTransparency2' , nData.kFloat  )   
        nAttr.setReadable(True) 
        nAttr.setStorable(True)
        nAttr.setConnectable(True)           
        nAttr.setChannelBox(True)         
        nAttr.setMin(0.0)  
        nAttr.setMax(1.0)                     
        nAttr.setDefault(1.0) 

        cls.attrOutTrig = nAttr.create( 'outTrig', 'outTrig' , nData.kFloat  )   
        nAttr.setReadable(True) 
        nAttr.setStorable(True)
        nAttr.setConnectable(True)          






        cls.addAttribute(cls.attrInCamMatrix )
        cls.addAttribute(cls.attrInVectors) 
        cls.addAttribute(cls.attrInVectorsSize )         
        cls.addAttribute(cls.attrInVectorsColor )
        cls.addAttribute(cls.attrInVectorsName )
        cls.addAttribute(cls.attrInSquares )   
        cls.addAttribute(cls.attrInSquaresSize )               
        cls.addAttribute(cls.attrInSquaresColor )
        cls.addAttribute(cls.attrInSquaresName )        
        cls.addAttribute(cls.attrInTriangles ) 
        cls.addAttribute(cls.attrInTrianglesSize ) 
        cls.addAttribute(cls.attrInTrianglesColor )
        cls.addAttribute(cls.attrInTrianglesName )                                         
        cls.addAttribute(cls.attrInCircles )
        cls.addAttribute(cls.attrInCirclesSize )          
        cls.addAttribute(cls.attrInCirclesColor )
        cls.addAttribute(cls.attrInCirclesName )   
        cls.addAttribute(cls.attrInStars )
        cls.addAttribute(cls.attrInStarsSize )          
        cls.addAttribute(cls.attrInStarsColor )
        cls.addAttribute(cls.attrInStarsName )  
        cls.addAttribute(cls.attrInMotionTrail )
        cls.addAttribute(cls.attrInMotionTrailSize )          
        cls.addAttribute(cls.attrInMotionTrailColor )
        cls.addAttribute(cls.attrInMotionTrailName ) 
        cls.addAttribute(cls.attrInMotionTrailWorldSpace ) 
        cls.addAttribute(cls.attrInMotionTrailMaxMemory ) 
        cls.addAttribute(cls.attrInTextPos )
        cls.addAttribute(cls.attrInPointTransparency )   
        cls.addAttribute(cls.attrInVectorTransparency ) 
        cls.addAttribute(cls.attrInMotionTrailTransparency )
        cls.addAttribute(cls.attrInMotionTrailLinkTransparency )                
        cls.addAttribute(cls.attrOutTrig )            
        #INFLUENCE
        cls.attributeAffects(cls.attrInCamMatrix      , cls.attrOutTrig )
        cls.attributeAffects(cls.attrInVectors        , cls.attrOutTrig ) 
        cls.attributeAffects(cls.attrInVectorsSize    , cls.attrOutTrig )         
        cls.attributeAffects(cls.attrInVectorsColor   , cls.attrOutTrig )
        cls.attributeAffects(cls.attrInVectorsName    , cls.attrOutTrig )
        cls.attributeAffects(cls.attrInSquares        , cls.attrOutTrig )   
        cls.attributeAffects(cls.attrInSquaresSize    , cls.attrOutTrig )               
        cls.attributeAffects(cls.attrInSquaresColor   , cls.attrOutTrig )
        cls.attributeAffects(cls.attrInSquaresName    , cls.attrOutTrig )        
        cls.attributeAffects(cls.attrInTriangles      , cls.attrOutTrig ) 
        cls.attributeAffects(cls.attrInTrianglesSize  , cls.attrOutTrig ) 
        cls.attributeAffects(cls.attrInTrianglesColor , cls.attrOutTrig )     
        cls.attributeAffects(cls.attrInTrianglesName  , cls.attrOutTrig )                                  
        cls.attributeAffects(cls.attrInCircles        , cls.attrOutTrig )
        cls.attributeAffects(cls.attrInCirclesSize    , cls.attrOutTrig )          
        cls.attributeAffects(cls.attrInCirclesColor   , cls.attrOutTrig )
        cls.attributeAffects(cls.attrInCirclesName    , cls.attrOutTrig )
        cls.attributeAffects(cls.attrInStars        , cls.attrOutTrig )
        cls.attributeAffects(cls.attrInStarsSize    , cls.attrOutTrig )          
        cls.attributeAffects(cls.attrInStarsColor   , cls.attrOutTrig )
        cls.attributeAffects(cls.attrInStarsName    , cls.attrOutTrig ) 
        cls.attributeAffects(cls.attrInMotionTrail        , cls.attrOutTrig )
        cls.attributeAffects(cls.attrInMotionTrailSize    , cls.attrOutTrig )          
        cls.attributeAffects(cls.attrInMotionTrailColor   , cls.attrOutTrig )
        cls.attributeAffects(cls.attrInMotionTrailName    , cls.attrOutTrig )  
        cls.attributeAffects(cls.attrInMotionTrailWorldSpace , cls.attrOutTrig ) 
        cls.attributeAffects(cls.attrInMotionTrailMaxMemory  , cls.attrOutTrig )               
        cls.attributeAffects(cls.attrInPointTransparency  , cls.attrOutTrig ) 
        cls.attributeAffects(cls.attrInVectorTransparency , cls.attrOutTrig )  
        cls.attributeAffects(cls.attrInMotionTrailTransparency , cls.attrOutTrig ) 
        cls.attributeAffects(cls.attrInMotionTrailLinkTransparency , cls.attrOutTrig )                                                
        cls.attributeAffects(cls.attrInTextPos        , cls.attrOutTrig )             
 
       
        
def initializePlugin(obj):
    print('initializePlugin')    
    plugin = ommpx.MFnPlugin( obj , 'matthieuCantat', '1.0', 'Any')
    try:
        plugin.registerNode( annotateDyn.kPluginNodeTypeName, annotateDyn.kPluginNodeId, annotateDyn.nodeCreator, annotateDyn.nodeInitializer, ommpx.MPxNode.kLocatorNode)
    except:
        raise Exception('Failed to register node: {0}'.format(annotateDyn.kPluginNodeTypeName) )
   

def uninitializePlugin(obj):
    print('uninitializePlugin')  
    plugin = ommpx.MFnPlugin(obj)
    try:
        plugin.deregisterNode( annotateDyn.kPluginNodeId )
    except:
        raise Exception('Failed to unregister node: {0}'.format(annotateDyn.kPluginNodeTypeName) )







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
         