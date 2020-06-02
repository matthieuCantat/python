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


class attributeNode(ommpx.MPxNode):

    kPluginNodeTypeName = 'attributeNode'
    kPluginNodeId = om.MTypeId(0x00033467)

    @classmethod
    def nodeCreator(cls):
        return ommpx.asMPxPtr(cls())

    @classmethod
    def nodeInitializer(cls):
        cls.curveModes = [ 'open' , 'close' , 'periodic' ] 
        nData = om.MFnNumericData()
        cData = om.MFnNurbsCurveData() 
        mData = om.MFnMeshData() 

        nAttr = om.MFnNumericAttribute()  
        eAttr = om.MFnEnumAttribute()
        mAttr = om.MFnMatrixAttribute()
        gAttr = om.MFnGenericAttribute()
        tAttr = om.MFnTypedAttribute()                 

        # INPUT ATTRIBUT                   default: Readable Writable Storable Connectable
        cls.aInInt = nAttr.create( 'int' , 'int' , nData.kInt  , 3.0 )
        nAttr.setMin(1.0)    
        nAttr.setMax(3.0)         
        nAttr.setKeyable(True)          
        nAttr.setChannelBox(True)           

        cls.aInEnum = eAttr.create( 'enum' , 'enum' )
        for i in range( 0 , len(cls.curveModes) ): 
            eAttr.addField( cls.curveModes[i] , i )             
        eAttr.setKeyable(True)          
        eAttr.setChannelBox(True)             
                          
        cls.aInPoint = nAttr.createPoint( 'point' , 'point' )
        nAttr.setKeyable(True)        
        nAttr.setChannelBox(True)        

        cls.aInMatrix = mAttr.create( 'matrix' , 'matrix' ,  nData.kFloat )
        mAttr.setKeyable(True)        
        mAttr.setChannelBox(True)   

        cls.aInMatrices = mAttr.create( 'matrices' , 'matrices' ,  nData.kFloat )
        mAttr.setKeyable(True)        
        mAttr.setChannelBox(True)  
        mAttr.setArray(True) 
        mAttr.isDynamic() 
 
        cls.aInCurve = tAttr.create( 'curve' , 'curve' , cData.kNurbsCurve )
        tAttr.setKeyable(True)        
        tAttr.setChannelBox(True)        

        cls.aInMesh = tAttr.create( 'mesh' , 'mesh' , mData.kMesh )
        tAttr.setKeyable(True)        
        tAttr.setChannelBox(True)        

        cls.aInGeo = gAttr.create( 'geo' , 'geo')
        gAttr.addDataAccept(cData.kNurbsCurve)
        gAttr.addDataAccept(mData.kMesh)        
        gAttr.setKeyable(True)        
        gAttr.setChannelBox(True)        

        # OUTPUT ATTRIBUT                   default: Readable Writable Storable Connectable     warning: keyable error in output 
        cls.aOutInt = nAttr.create( 'outInt' , 'outInt' , nData.kInt  , 3.0 )
        nAttr.setChannelBox(True)        

        cls.aOutEnum = eAttr.create( 'outEnum' , 'outEnum' )
        eAttr.setChannelBox(True)                
                     
        cls.aOutPoint = nAttr.createPoint( 'outPoint' , 'outPoint' )
        nAttr.setChannelBox(True) 
                        
        cls.aOutMatrix = mAttr.create( 'outMatrix' , 'outMatrix' ,  nData.kFloat )      
        mAttr.setChannelBox(True)   
                        
        cls.aOutMatrices = mAttr.create( 'outMatrices' , 'outMatrices' ,  nData.kFloat )      
        mAttr.setChannelBox(True)  
        mAttr.setArray(True) 
        mAttr.isDynamic()    

        cls.aOutCurve = tAttr.create( 'outCurve' , 'outCurve' , cData.kNurbsCurve )    
        tAttr.setChannelBox(True) 

        cls.aOutMesh = tAttr.create( 'outMesh' , 'outMesh' , mData.kMesh )     
        tAttr.setChannelBox(True)        

        cls.aOutGeo = gAttr.create( 'outGeo' , 'outGeo' )
        gAttr.addDataAccept(cData.kNurbsCurve)
        gAttr.addDataAccept(mData.kMesh)                  
        gAttr.setChannelBox(True)    

        # ADD ATTR     
        cls.addAttribute(cls.aInInt       )
        cls.addAttribute(cls.aInEnum      )          
        cls.addAttribute(cls.aInPoint     ) 
        cls.addAttribute(cls.aInMatrix    )        
        cls.addAttribute(cls.aInMatrices  )    
        cls.addAttribute(cls.aInCurve     ) 
        cls.addAttribute(cls.aInMesh      )         
        cls.addAttribute(cls.aInGeo       )  

        cls.addAttribute(cls.aOutInt      )
        cls.addAttribute(cls.aOutEnum     )          
        cls.addAttribute(cls.aOutPoint    )
        cls.addAttribute(cls.aOutMatrix   )        
        cls.addAttribute(cls.aOutMatrices )     
        cls.addAttribute(cls.aOutCurve    )  
        cls.addAttribute(cls.aOutMesh     )  
        cls.addAttribute(cls.aOutGeo      ) 

        #INFLUENCE
        cls.attributeAffects( cls.aInInt      , cls.aOutInt      )         
        cls.attributeAffects( cls.aInEnum     , cls.aOutEnum     )           
        cls.attributeAffects( cls.aInPoint    , cls.aOutPoint    )
        cls.attributeAffects( cls.aInMatrix   , cls.aOutMatrix   )
        cls.attributeAffects( cls.aInMatrices , cls.aOutMatrices )
        cls.attributeAffects( cls.aInCurve    , cls.aOutCurve    )
        cls.attributeAffects( cls.aInMesh     , cls.aOutMesh     )
        cls.attributeAffects( cls.aInGeo      , cls.aOutGeo      )

    def __init__(self):
        ommpx.MPxNode.__init__(self)
      

    def compute( self, plug , dataBlock ): 

        #CHECK IF AN OUT ATTR IS REQUESTED  
    	outsAttrs = [ self.aOutInt , self.aOutEnum , self.aOutPoint , self.aOutMatrix , self.aOutMatrices , self.aOutCurve , self.aOutMesh , self.aOutGeo ]                    
        if not ( plug in outsAttrs ): 
            return om.kUnknownParameter  

        #GET DATA   
        intInHandle  = dataBlock.inputValue( self.aInInt )
        intInValue   = intInHandle.asInt() 

        enumInHandle = dataBlock.inputValue( self.aInEnum )
        enumInValue  = enumInHandle.asInt()   

        pointInHandle = dataBlock.inputValue( self.aInPoint )
        pointInValue  = pointInHandle.asFloat3()  

        matrixInHandle = dataBlock.inputValue( self.aInMatrix )
        matrixInValue  = matrixInHandle.asMatrix()          

        matricesInHandle = dataBlock.inputArrayValue( self.aInMatrices )
        matricesInValue  = []   
        for i in range(0, matricesInHandle.elementCount() ):
            tmpHandle = matricesInHandle.outputValue()
            matricesInValue.append( tmpHandle.asMatrix() )
            matricesInHandle.next()      
        '''
        curveInHandle = dataBlock.inputValue( self.aInCurve )   
        MobjTmp       = curveInHandle.asNurbsCurve()
        curveInValue  = om.MFnNurbsCurve(MobjTmp)  

        meshInHandle = dataBlock.inputValue( self.aInMesh )  
        MobjTmp      = meshInHandle.asMesh() 
        meshInValue  = om.MFnMesh(MobjTmp)    
        '''
        #COMPUTE 
        print('======================================')
        print('1 - int      : {}'.format(intInValue ) )
        print('2 - enum     : {}'.format(enumInValue) )        
        print('3 - point    : {} {} {}'.format( pointInValue[0] , pointInValue[1] , pointInValue[2] ) )      
        print('4 - matrix   : {}'.format( matrixInValue.det4x4() ) )                  
        print('5 - matrices : {} elements'.format( len(matricesInValue) ) )              
        #print('6 - curve    : {} degree {} cvs'.format( curveInValue.degree , curveInValue.numCVs  ) )  
        #print('7 - mesh     : {} vtx {} face'.format( meshInValue.numVertices , meshInValue.numPolygons ) )  
        print('======================================')        
        
        #OUT            
        intOutHandle = dataBlock.outputValue( self.aOutInt )       
        intOutHandle.setInt( intInValue )
                     
        enumOutHandle = dataBlock.outputValue( self.aOutEnum )       
        enumOutHandle.setInt( enumInValue )
     
        pointOutHandle = dataBlock.outputValue( self.aOutPoint )      
        pointOutHandle.set3Float( pointInValue[0] , pointInValue[1] , pointInValue[2] )


        #SET THE OUT ATTR CLEAN
        dataBlock.setClean( self.aOutInt ) 
        dataBlock.setClean( self.aOutEnum ) 
        dataBlock.setClean( self.aOutPoint ) 
        
             
       
        
def initializePlugin(obj):
    plugin = ommpx.MFnPlugin( obj , 'matthieuCantat', '1.0', 'Any')
    try:
        plugin.registerNode( attributeNode.kPluginNodeTypeName, attributeNode.kPluginNodeId, attributeNode.nodeCreator, attributeNode.nodeInitializer)
    except:
        raise Exception('Failed to register node: {0}'.format(attributeNode.kPluginNodeTypeName) )
   

def uninitializePlugin(obj):
    plugin = ommpx.MFnPlugin(obj)
    try:
        plugin.deregisterNode( attributeNode.kPluginNodeId )
    except:
        raise Exception('Failed to unregister node: {0}'.format(attributeNode.kPluginNodeTypeName) )

        
        
        
        