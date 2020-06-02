'''
#FOR TEST
import maya.cmds as mc
path = 'D:\mcantat_BDD\projects\code\maya\python\plugIn\curveNode.py'
mc.file( new = True , f = True )
mc.loadPlugin( path , qt = True )   
'''

import sys
import maya.OpenMaya as om
import maya.api.OpenMaya as ompy
import maya.OpenMayaMPx as ommpx
import maya.cmds as mc


class curveNode(ommpx.MPxNode):

    print('CURVE NODE')
    kPluginNodeTypeName = 'curveNode'
    kPluginNodeId = om.MTypeId(0x00033465)
    curveModes   = [ 'open' , 'close' , 'periodic' ]
    controlModes = [ 'cv' , 'ep' , 'hermite' ]
    # IN ATTR
    attrInMatrices = None
    attrInMatricesName = 'inputMatrix'
    attrInDegree = None
    attrInDegreeName = 'degree'    
    attrInCurveMode = None
    attrInCurveModeName = 'curveMode'
    attrInControlMode = None
    attrInControlModeName = 'controlMode'   
    attrInOffset = None
    attrInOffsetName = 'offset'       
    # OUT ATTR
    attrOutCurve = None
    attrOutCurveName = 'outCurve'
    attrOutLength = None
    attrOutLengthName = 'length'
   
    def __init__(self):
        print('-----INIT-----')
        ommpx.MPxNode.__init__(self)
        self.inputMatrices  = []
        self.degree       = 3
        self.curveMode    = 0
        self.curveModes   = [ 'open' , 'close' , 'periodic' ]
        self.controlMode  = 0
        self.controlModes = [ 'cv' , 'ep' , 'hermite' ]
        self.offset       = [0,0,0] 
        self.curveData    = None
        self.length       = 0         

    def compute( self, plug , dataBlock ): 
        #CHECK IF IT'S PLUG     
        print('1_plugCheck')   
    	outsAttrs = [ self.attrOutCurve , self.attrOutLength ]                    
        if not ( plug in outsAttrs ): return om.kUnknownParameter                        
        #GET DATA   
        print('2_getData')        
        arrayDataHandle = dataBlock.inputArrayValue( self.attrInMatrices )
        self.inputMatrices = []   
        for i in range(0, arrayDataHandle.elementCount() ):
            dataHandle = arrayDataHandle.outputValue()
            self.inputMatrices.append( arrayDataHandle.asMatrix() )
            arrayDataHandle.next()      

        dataHandle  = dataBlock.inputValue( self.attrInDegree )
        self.degree = dataHandle.asInt()                 
        dataHandle     = dataBlock.inputValue( self.attrInCurveMode )
        self.curveMode = dataHandle.asInt()               
        dataHandle       = dataBlock.inputValue( self.attrInControlMode )
        self.controlMode = dataHandle.asInt()   
        dataHandle  = dataBlock.inputValue( self.attrInOffset )
        self.offset = dataHandle.asFloat3()  

        dataHandle = dataBlock.outputValue( self.attrOutCurve )   
        curveDataHandle = dataHandle.asNurbsCuve()  

        dataHandle = dataBlock.outputValue( self.attrOutLength ) 
        lengthDataHandle = dataHandle.asFloat() 

        mNurbsCurveData = om.MFnNurbsCurveData()
        self.curveData  = mNurbsCurveData.create()                    
        #COMPUTE  
        #GET POINT FROM MATRIX
        print('3_extractPoint') 
        positions = om.MPointArray()
        for i in range( 0 , len(self.inputMatrices) ):
            mTrs = om.MTransformationMatrix(self.inputMatrices[i]) 
            mVector = mTrs.translation(om.MSpace.kWorld)
            mPoint = om.MPoint( mVector.x , mVector.y , mVector.z ) 
            positions.append( mPoint )
        #GET Knot
        print('4_computeKnot') 
        nbrKnot = len(positions) + degree - 1
        knotsValues = om.MDoubleArray()
        for i in range(0,3): knotsValues.append(0.0)
        for i in range(1,nbrKnot-5): knotsValues.append(i/(nbrKnot-5.0))
        for i in range(nbrKnot-3,nbrKnot): knotsValues.append(1.0)           
        #FILL ATTR
        fnCurve = om.MFnNurbsCurve()
        cvs = positions
        knots = knotsValues
        form = fnCurve.kOpen
        is2D = False
        rational = True
        #CREATE CURVE
        print('5_createAttr') 
        fnCurve.create(cvs, knots, degree, form, is2D, rational , self.curveData )
        #OUT
        print('6_out') 
        self.length = fnCurve.length()         
              

        curveDataHandle.set( self.curveData )      
        lengthDataHandle.setFloat( self.length )     
        dataBlock.setClean( self.attrOutCurve ) 
        dataBlock.setClean( self.attrOutLength ) 
        dataBlock.setClean( plug ) 
        
        
    @classmethod
    def nodeCreator(cls):
        return ommpx.asMPxPtr(cls())

    @classmethod
    def nodeInitializer(cls):
        print('-----nodeInitializer-----')
        mNumData = om.MFnNumericData()
        # IN ATTR
        mAttr = om.MFnMatrixAttribute() 
        cls.attrInMatrices = mAttr.create( cls.attrInMatricesName , cls.attrInMatricesName ,  mNumData.kFloat )
        mAttr.setChannelBox(True)
        mAttr.setKeyable(True)        
        mAttr.setReadable(True) 
        mAttr.setWritable(True)
        mAttr.setStorable(True)
        mAttr.setConnectable(True)         
        mAttr.setArray(True) 
        mAttr.isDynamic()

        mAttr = om.MFnNumericAttribute()    
        cls.attrInDegree = mAttr.create(cls.attrInDegreeName, cls.attrInDegreeName , mNumData.kInt  , 3.0 )
        mAttr.setChannelBox(True)
        mAttr.setKeyable(True)        
        mAttr.setReadable(True) 
        mAttr.setWritable(True)
        mAttr.setStorable(True)
        mAttr.setConnectable(True)      
        mAttr.setMin(1.0)    
        mAttr.setMax(3.0)    

        mAttr = om.MFnEnumAttribute()  
        cls.attrInCurveMode = mAttr.create(cls.attrInCurveModeName, cls.attrInCurveModeName  )
        mAttr.setChannelBox(True)
        mAttr.setKeyable(True)        
        mAttr.setReadable(True) 
        mAttr.setWritable(True)
        mAttr.setStorable(True)
        mAttr.setConnectable(True)        
        for i in range( 0 , len(cls.curveModes) ): mAttr.addField( cls.curveModes[i] , i )         
        
        mAttr = om.MFnEnumAttribute()             
        cls.attrInControlMode = mAttr.create(cls.attrInControlModeName, cls.attrInControlModeName )  
        mAttr.setChannelBox(True)
        mAttr.setKeyable(True)        
        mAttr.setReadable(True) 
        mAttr.setWritable(True)
        mAttr.setStorable(True)
        mAttr.setConnectable(True)     
        for i in range( 0 , len(cls.controlModes) ): mAttr.addField( cls.controlModes[i] , i )              
        
        mAttr = om.MFnNumericAttribute() 
        cls.attrInOffset = mAttr.createPoint(cls.attrInOffsetName, cls.attrInOffsetName )
        mAttr.setChannelBox(True)
        mAttr.setKeyable(True)        
        mAttr.setReadable(True) 
        mAttr.setWritable(True)
        mAttr.setStorable(True)
        mAttr.setConnectable(True)               
        
        # OUT ATTR
        mAttr = om.MFnGenericAttribute()   
        cls.attrOutCurve = mAttr.create(cls.attrOutCurveName, cls.attrOutCurveName )
        mData = om.MFnData()
        #mAttr.addDataType( mData.kNurbsCurve )   
        mAttr.setReadable(True) 
        mAttr.setStorable(True)
        mAttr.setConnectable(True)   
       
        mAttr = om.MFnNumericAttribute()          
        cls.attrOutLength = mAttr.create(cls.attrOutLengthName, cls.attrOutLengthName , mNumData.kFloat  )    
        mAttr.setReadable(True) 
        mAttr.setStorable(True)
        mAttr.setConnectable(True)             
        
        # ADD ATTR
        cls.addAttribute(cls.attrInMatrices )  
        cls.addAttribute(cls.attrInDegree )
        cls.addAttribute(cls.attrInCurveMode )          
        cls.addAttribute(cls.attrInControlMode ) 
        cls.addAttribute(cls.attrInOffset ) 
        cls.addAttribute(cls.attrOutCurve )    
        cls.addAttribute(cls.attrOutLength ) 
        
        #INFLUENCE
        cls.attributeAffects( cls.attrInMatrices    , cls.attrOutCurve )         
        cls.attributeAffects( cls.attrInDegree      , cls.attrOutCurve )           
        cls.attributeAffects( cls.attrInCurveMode   , cls.attrOutCurve )
        cls.attributeAffects( cls.attrInControlMode , cls.attrOutCurve )       
        cls.attributeAffects( cls.attrInOffset      , cls.attrOutCurve )   
        
        cls.attributeAffects( cls.attrInMatrices    , cls.attrOutLength )         
        cls.attributeAffects( cls.attrInDegree      , cls.attrOutLength )           
        cls.attributeAffects( cls.attrInCurveMode   , cls.attrOutLength )
        cls.attributeAffects( cls.attrInControlMode , cls.attrOutLength )       
        cls.attributeAffects( cls.attrInOffset      , cls.attrOutLength )   
             
       
        
def initializePlugin(obj):
    plugin = ommpx.MFnPlugin( obj , 'matthieuCantat', '1.0', 'Any')
    try:
        plugin.registerNode( curveNode.kPluginNodeTypeName, curveNode.kPluginNodeId, curveNode.nodeCreator, curveNode.nodeInitializer)
    except:
        raise Exception('Failed to register node: {0}'.format(curveNode.kPluginNodeTypeName) )
   

def uninitializePlugin(obj):
    plugin = ommpx.MFnPlugin(obj)
    try:
        plugin.deregisterNode( curveNode.kPluginNodeId )
    except:
        raise Exception('Failed to unregister node: {0}'.format(curveNode.kPluginNodeTypeName) )

        
        
        
        