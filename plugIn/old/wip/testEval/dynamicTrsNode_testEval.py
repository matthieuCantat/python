
'''

    BUG: lors d'un test de node avec TranstateXYZ RotateXYZ ScaleXYZ (9 attrs) attributs in et out, il y a souvent une difference entre les valeurs node out et les valeus in de l'obj slave ( corriger a l eval d apres)
         le bug apparait entre 3 et 6 attributs out
          
    Conclusion: 
    
    LE BUG ETAIT DU AU IF AU DEBUT DU COMPUTE:
    
    
        if not ( plug == self.outputTAttr ):
            return om.kUnknownParameter 

            
		plug est un parametre passer en argument , il represente le MObject MPlug
		
		il correspond a l attribut demande par le logiciel. ( en connection ou en get attr ) 
		
		Ici le logiciel renvoie une valeur seulement si c'est outputTAttr , les autres il renvoie rien. d'ou le bug d evaluation
		
		On a juste a mettre la liste des attrs out et on est bon!
		
		
    	outsAttr = [ self.outputTAttr , self.outputRAttr , self.outputSAttr ]                        
        if not ( plug in outsAttr ):
            return om.kUnknownParameter		



'''


import sys
import math
import time
import maya.OpenMaya as om
import maya.api.OpenMaya as ompy
import maya.OpenMayaMPx as ommpx
import maya.cmds as mc


toolBox_mainPath = 'C:/Users/Matthieu/Desktop/Travail/code/maya/script/python/'        

import sys
sys.path.append( toolBox_mainPath )

import toolBox
import toolBox.utils.utilsMayaApi as utilsMayaApi
import toolBox.utils.classes.trsClass as trsClass

class dynamicRotation(ommpx.MPxNode):

    kPluginNodeTypeName = 'dynamicTrsNode_testEval'
    kPluginNodeId = om.MTypeId(0x00033449)

    # _________________________________ IN TRANSLATE    
    inputT = None
    kInputTAttrName = 'inTran'
    kInputTAttrLongName = 'inTranslate'       
    
    inputTX = None
    kInputTXAttrName = 'inTranX'
    kInputTXAttrLongName = 'inTranslateX'
    
    inputTY = None
    kInputTYAttrName = 'inTranY'
    kInputTYAttrLongName = 'inTranslateY'
 
    inputTZ = None
    kInputTZAttrName = 'inTranZ'
    kInputTZAttrLongName = 'inTranslateZ'    

    # _________________________________ IN ROTATE    
    inputR = None
    kInputRAttrName = 'inRot'
    kInputRAttrLongName = 'inRotate'    
    
    inputRX = None
    kInputRXAttrName = 'inRotX'
    kInputRXAttrLongName = 'inRotateX'
    
    inputRY = None
    kInputRYAttrName = 'inRotY'
    kInputRYAttrLongName = 'inRotateY'
 
    inputRZ = None
    kInputRZAttrName = 'inRotZ'
    kInputRZAttrLongName = 'inRotateZ' 
  
    # _________________________________ IN SCALE 
    inputS = None
    kInputSAttrName = 'inSca'
    kInputSAttrLongName = 'inScale'
    
    inputSX = None
    kInputSXAttrName = 'inScaX'
    kInputSXAttrLongName = 'inScaleX'
    
    inputSY = None
    kInputSYAttrName = 'inScaY'
    kInputSYAttrLongName = 'inScaleY'
 
    inputSZ = None
    kInputSZAttrName = 'inScaZ'
    kInputSZAttrLongName = 'inScaleZ' 

    # _________________________________ OUT TRANSLATE    
    outputT = None
    kOutputTAttrName = 'outTran'
    kOutputTAttrLongName = 'outTranslate'    
    
    outputTX = None
    kOutputTXAttrName = 'outTranX'
    kOutputTXAttrLongName = 'outTranslateX'
    
    outputTY = None
    kOutputTYAttrName = 'outTranY'
    kOutputTYAttrLongName = 'outTranslateY'
 
    outputTZ = None
    kOutputTZAttrName = 'outTranZ'
    kOutputTZAttrLongName = 'outTranslateZ'    

    # _________________________________ OUT ROTATE    
    outputR = None
    kOutputRAttrName = 'outRot'
    kOutputRAttrLongName = 'outRotate'    
    
    outputRX = None
    kOutputRXAttrName = 'outRotX'
    kOutputRXAttrLongName = 'outRotateX'
    
    outputRY = None
    kOutputRYAttrName = 'outRotY'
    kOutputRYAttrLongName = 'outRotateY'
 
    outputRZ = None
    kOutputRZAttrName = 'outRotZ'
    kOutputRZAttrLongName = 'outRotateZ' 

    # _________________________________ OUT SCALE     
    outputS = None
    kOutputSAttrName = 'outSca'
    kOutputSAttrLongName = 'outScale'    
    
    outputSX = None
    kOutputSXAttrName = 'outScaX'
    kOutputSXAttrLongName = 'outScaleX'
    
    outputSY = None
    kOutputSYAttrName = 'outScaY'
    kOutputSYAttrLongName = 'outScaleY'
 
    outputSZ = None
    kOutputSZAttrName = 'outScaZ'
    kOutputSZAttrLongName = 'outScaleZ' 
    

    def __init__(self):        
        ommpx.MPxNode.__init__(self)

    def compute( self, plug , dataBlock ):
    
    	
    	outsAttr = [ self.outputTAttr , self.outputRAttr , self.outputSAttr ]                               # <------------------------------ BUG !!!!                         
        if not ( plug in outsAttr ):
            return om.kUnknownParameter

        #_____________________________________________________________________________________COMPUTE IN
         
        dataHandle     = dataBlock.inputValue( self.inputTAttr )
        translate      = dataHandle.asDouble3()

        dataHandle     = dataBlock.inputValue( self.inputRAttr )
        rotate         = dataHandle.asDouble3()
        rotate         = [ math.degrees(rotate[0]) , math.degrees(rotate[1]) , math.degrees(rotate[2]) ]
        
        dataHandle     = dataBlock.inputValue( self.inputSAttr )
        scale          = dataHandle.asDouble3()        
        #_____________________________________________________________________________________COMPUTE
        
        #_____________________________________________________________________________________COMPUTE OUT

        dataHandle = dataBlock.outputValue( self.outputTAttr )       
        dataHandle.set3Double( translate[0] , translate[1] , translate[2] )
        dataHandle.setClean()        
     
        dataHandle = dataBlock.outputValue( self.outputRAttr )       
        dataHandle.set3Double( math.radians(rotate[0]) , math.radians(rotate[1]) , math.radians(rotate[2]) )  
        dataHandle.setClean()    
        
        dataHandle = dataBlock.outputValue( self.outputSAttr )       
        dataHandle.set3Double( scale[0] , scale[1] , scale[2]  ) 
        dataHandle.setClean()            

        dataBlock.setClean( plug ) 
        

    @classmethod
    def nodeCreator(cls):
        return ommpx.asMPxPtr(cls())


    @classmethod
    def nodeInitializer(cls):

 
        #________________________________ IN TRANSLATE
        nAttr = om.MFnNumericAttribute()         
        cls.inputTXAttr = nAttr.create( cls.kInputTXAttrLongName , cls.kInputTXAttrName , om.MFnNumericData.kDouble )      
        cls.inputTYAttr = nAttr.create( cls.kInputTYAttrLongName , cls.kInputTYAttrName , om.MFnNumericData.kDouble )     
        cls.inputTZAttr = nAttr.create( cls.kInputTZAttrLongName , cls.kInputTZAttrName , om.MFnNumericData.kDouble )             
 
        nAttr = om.MFnNumericAttribute()        
        cls.inputTAttr = nAttr.create( cls.kInputTAttrLongName , cls.kInputTAttrName , cls.inputTXAttr , cls.inputTYAttr , cls.inputTZAttr ) 
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)         
        
        #________________________________ IN ROTATE
        nAttr = om.MFnUnitAttribute()         
        cls.inputRXAttr = nAttr.create( cls.kInputRXAttrLongName , cls.kInputRXAttrName , om.MFnUnitAttribute.kAngle )      
        cls.inputRYAttr = nAttr.create( cls.kInputRYAttrLongName , cls.kInputRYAttrName , om.MFnUnitAttribute.kAngle )     
        cls.inputRZAttr = nAttr.create( cls.kInputRZAttrLongName , cls.kInputRZAttrName , om.MFnUnitAttribute.kAngle )             
 
        nAttr = om.MFnNumericAttribute()        
        cls.inputRAttr = nAttr.create( cls.kInputRAttrLongName , cls.kInputRAttrName , cls.inputRXAttr , cls.inputRYAttr , cls.inputRZAttr ) 
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)  

        #________________________________ IN SCALE
        nAttr = om.MFnNumericAttribute()         
        cls.inputSXAttr = nAttr.create( cls.kInputSXAttrLongName , cls.kInputSXAttrName , om.MFnNumericData.kDouble )      
        cls.inputSYAttr = nAttr.create( cls.kInputSYAttrLongName , cls.kInputSYAttrName , om.MFnNumericData.kDouble )     
        cls.inputSZAttr = nAttr.create( cls.kInputSZAttrLongName , cls.kInputSZAttrName , om.MFnNumericData.kDouble )             
 
        nAttr = om.MFnNumericAttribute()        
        cls.inputSAttr = nAttr.create( cls.kInputSAttrLongName , cls.kInputSAttrName , cls.inputSXAttr , cls.inputSYAttr , cls.inputSZAttr ) 
        nAttr.setKeyable(True)       
        nAttr.setReadable(False)  
        
        #________________________________ OUT TRANSLATE
        nAttr = om.MFnNumericAttribute()         
        cls.outputTXAttr = nAttr.create( cls.kOutputTXAttrLongName , cls.kOutputTXAttrName , om.MFnNumericData.kDouble )      
        cls.outputTYAttr = nAttr.create( cls.kOutputTYAttrLongName , cls.kOutputTYAttrName , om.MFnNumericData.kDouble )     
        cls.outputTZAttr = nAttr.create( cls.kOutputTZAttrLongName , cls.kOutputTZAttrName , om.MFnNumericData.kDouble )             
 
        nAttr = om.MFnNumericAttribute()        
        cls.outputTAttr = nAttr.create( cls.kOutputTAttrLongName , cls.kOutputTAttrName , cls.outputTXAttr , cls.outputTYAttr , cls.outputTZAttr ) 
        nAttr.setWritable(False)
        nAttr.setStorable(False)  
        
        #________________________________ OUT ROTATE
        nAttr = om.MFnUnitAttribute()         
        cls.outputRXAttr = nAttr.create( cls.kOutputRXAttrLongName , cls.kOutputRXAttrName , om.MFnUnitAttribute.kAngle )      
        cls.outputRYAttr = nAttr.create( cls.kOutputRYAttrLongName , cls.kOutputRYAttrName , om.MFnUnitAttribute.kAngle )     
        cls.outputRZAttr = nAttr.create( cls.kOutputRZAttrLongName , cls.kOutputRZAttrName , om.MFnUnitAttribute.kAngle )             
 
        nAttr = om.MFnNumericAttribute()        
        cls.outputRAttr = nAttr.create( cls.kOutputRAttrLongName , cls.kOutputRAttrName , cls.outputRXAttr , cls.outputRYAttr , cls.outputRZAttr ) 
        nAttr.setWritable(False)
        nAttr.setStorable(False)
        
        #________________________________ OUT SCALE
        nAttr = om.MFnNumericAttribute()         
        cls.outputSXAttr = nAttr.create( cls.kOutputSXAttrLongName , cls.kOutputSXAttrName , om.MFnNumericData.kDouble )      
        cls.outputSYAttr = nAttr.create( cls.kOutputSYAttrLongName , cls.kOutputSYAttrName , om.MFnNumericData.kDouble )     
        cls.outputSZAttr = nAttr.create( cls.kOutputSZAttrLongName , cls.kOutputSZAttrName , om.MFnNumericData.kDouble ) 
        
        nAttr = om.MFnNumericAttribute()          
        cls.outputSAttr = nAttr.create(cls.kOutputSAttrLongName, cls.kOutputSAttrName , cls.outputSXAttr , cls.outputSYAttr , cls.outputSZAttr )
        nAttr.setWritable(False)
        nAttr.setStorable(False)

        
        #________________________________ ADD         
        cls.addAttribute(cls.outputSAttr )        
        cls.addAttribute(cls.outputRAttr )
        cls.addAttribute(cls.outputTAttr ) 
        cls.addAttribute(cls.inputSAttr )
        cls.addAttribute(cls.inputRAttr )     
        cls.addAttribute(cls.inputTAttr )

        #__________________________________________________________ AFFECT MAIN 
        cls.attributeAffects( cls.inputTAttr , cls.outputTAttr )
        cls.attributeAffects( cls.inputRAttr , cls.outputRAttr )
        cls.attributeAffects( cls.inputSAttr , cls.outputSAttr )          
          
        
def initializePlugin(obj):
    plugin = ommpx.MFnPlugin( obj , 'matthieuCantat', '1.0', 'Any')
    try:
        plugin.registerNode( dynamicRotation.kPluginNodeTypeName, dynamicRotation.kPluginNodeId, dynamicRotation.nodeCreator, dynamicRotation.nodeInitializer)
    except:
        raise Exception('Failed to register node: {0}'.format(dynamicRotation.kPluginNodeTypeName) )
   

def uninitializePlugin(obj):
    plugin = ommpx.MFnPlugin(obj)
    try:
        plugin.deregisterNode( dynamicRotation.kPluginNodeId )
    except:
        raise Exception('Failed to unregister node: {0}'.format(dynamicRotation.kPluginNodeTypeName) )

        

    
 