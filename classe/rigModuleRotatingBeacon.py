'''
#******************************************************** BUILD EXEMPLE RIG CTRL
import maya.cmds as mc
import python
from python.classe.rigModuleRotatingBeacon import *
reload(python.classe.rigModuleRotatingBeacon)

mc.file( f = True , new = True )
#=================================================


#_________________________________BUILD
beaconA = rigModuleRotatingBeacon( n = 'cone' , pos = [ [2,0,0,45,45,0,1,1,1] ] )    
beaconA.printBuild = 1
toExec = beaconA.build()
exec(toExec)



#_________________________________MIRROR

args = {}
args['value']             = [0,0,0 , 0,1,0 , 0,0,1]
args['mode']              = 'mirror'
args['pivot']             = [0,0,0 , 0,0,0 , 1,1,1]
args['namePrefix']        = ['r','l']
args['nameReplace']       = ['toto','tata']
args['nameIncr']          = ''
args['nameAdd']           = []
args['noneMirrorAxe']     = 4

mirrored = beaconA.duplicate( **args )

for elem in mirrored:
    elem.build()

for elem in mirrored:
    elem.delete()
    

#_________________________________TRANSFORM
args = {}
args['value']             = [-2.36 , 2.876 , -2.247 , -23.629 , 18.578 , 33.015 , 1 , 1 , 1 , 5 ]
args['mode']              = 'transform'
args['pivot']             = [ 5 , 0 , -1 , 0 ,0,0 , 1 , 1 , 1 ]
args['namePrefix']        = ['','']
args['nameReplace']       = ['','']
args['nameIncr']          = 'A'
args['nameAdd']           = []
args['noneMirrorAxe']     = 4


duplicated = beaconA.duplicate( **args )

for elem in duplicated:
    elem.build()

for elem in duplicated:
    elem.delete()


'''

#ATTR
from .rigModule import *            
from .rigCtrl import *          
from .rigStretchyJoint import *     
from .rigLightCone import *     

class rigModuleRotatingBeacon( rigModule ):

	def __init__( self , **args ):
		rigModule.__init__( self , **args )
		#CLASSE TYPE
		self.classeType = 'rigModuleRotatingBeacon'
		
		#CLASSE BLUE PRINT
		self.Name.add( 'base'   , baseName = self.classeType )
		self.Pos.add( 'masterA' , replace  = [0,0,0,0,0,0,1,1,1] )	

		self.Name.add( 'ctrl'       , ref = self.Name.base , baseNameAppend = 'ctrl'        )
		self.Name.add( 'lightConeA' , ref = self.Name.base , baseNameAppend = 'lightConeA'  )	
		self.Name.add( 'lightConeB' , ref = self.Name.base , baseNameAppend = 'lightConeB'  )

		self.Pos.add( 'lightConeA' , append = [{'replace': self.Pos.masterA } , {'addLocal': [ 10,0,0,0,0,0,1,1,1] }] )
		self.Pos.add( 'lightConeB' , append = [{'replace': self.Pos.masterA } , {'addLocal': [-10,0,0,0,0,0,1,1,1] }] ) 

		self.CurveShape.add(  'ctrl'  , value = { 'form' : 'cylinder' , 'colors' : [13] , 'axe' : 'x' , 'offset' : [0,0,0,0,0,0,1,1,1] }  )

		self.Ctrl       = rigCtrl(      n = self.Name.ctrl       , pos = [ self.Pos.masterA ] , joint = True , ctrlScale = self.ctrlScale , parent = self.Name.ctrlGrp )
		self.LightConeA = rigLightCone( n = self.Name.lightConeA , pos = [ self.Pos.masterA , self.Pos.lightConeA ]  , parent = self.Name.skeletonGrp)
		self.LightConeB = rigLightCone( n = self.Name.lightConeB , pos = [ self.Pos.masterA , self.Pos.lightConeB ]  , parent = self.Name.skeletonGrp)

		self.Link.add(  'lightConeA' , Sources = [ self.Ctrl.Name.joint ]  , Destinations = [ self.LightConeA.Name.masterA , self.LightConeA.Name.masterB  ] , type = 'parent' , operation = 'oneMaster' ,  maintainOffset = 1 )
		self.Link.add(  'lightConeB' , Sources = [ self.Ctrl.Name.joint ]  , Destinations = [ self.LightConeB.Name.masterB                                 ] , type = 'parent' , operation = 'oneMaster' ,  maintainOffset = 1 )		

		attrNames  = [ 'sinusoidale','sinSpeed' , 'sinAmplitude' , 'sinOffset' , 'linear'    , 'linearSpeed' , 'linearOffset'   ]
		attrTypes  = [ 'separator'  ,'float'    , 'float'        , 'float'    , 'separator'  , 'float'       , 'float'         ]
		attrValues = [  None        , 0         , 0              , 0           ,  None       , 0             , 0                ]
		self.Attr.add(  'ctrl' , Name = self.Ctrl.Name.ctrl , attrName = attrNames , attrType = attrTypes , attrValue = attrValues )

		for letter in [ 'A' , 'B' ]:
			attrsName  = [ 'lightConeShape' + letter , 'intensity' + letter , 'colorR' + letter  , 'colorG' + letter  , 'colorB' + letter  , 'sizeStart' + letter , 'sizeEnd' + letter , 'keepProportion' + letter , 'offset' + letter ]
			attrsType  = [ 'separator'               , 'float'     , 'float'  , 'float'  , 'float'  , 'float'    , 'float'   , 'floatOnOff'     , 'float' ]		
			attrsValue = [  None                     ,  1          ,    1      , 0.821     ,  0.39     ,   0.05      ,     1      ,     1            ,   2      ]
			self.Attr.add(  'topNode'  , Name = self.Ctrl.Name.ctrl , attrName = attrsName , attrType = attrsType , attrValue = attrsValue )

		attrsName  = [ 'intensity' , 'colorR' , 'colorG' , 'colorB' , 'sizeStart' , 'sizeEnd' , 'keepProportion' , 'offset' ]
		for attr in attrsName:
			exec( "self.Link.add( '{0}{1}' , Sources = [ self.Attr.topNode.{0}{1} ]  , Destinations = [ self.LightConeA.Attr.topNode.{0} ] , type = 'simple' , operation = 'oneMaster' )".format( attr , "A" )	)
			exec( "self.Link.add( '{0}{1}' , Sources = [ self.Attr.topNode.{0}{1} ]  , Destinations = [ self.LightConeB.Attr.topNode.{0} ] , type = 'simple' , operation = 'oneMaster' )".format( attr , "B" )		)

		self.Attr.add(  'joint'     , Name = self.Ctrl.Name.joint )
		self.Link.add( 'timeRotation' , Sources = [ self.Attr.ctrl.sinSpeed , self.Attr.ctrl.sinAmplitude , self.Attr.ctrl.sinOffset , self.Attr.ctrl.linearSpeed, self.Attr.ctrl.linearOffset , 10 ]  , Destinations = [self.Attr.joint.rotateY ] , type = 'timeRotation'  )		

		#CLASSE UTILS
		self.SubRigs     = [ self.Ctrl , self.LightConeA , self.LightConeB ]
		self.SubRigsName = [ 'Ctrl'    , 'LightConeA'    , 'LightConeB'    ]
		self.ins         = self.Ctrl.ins
		self.outs        = [ self.Ctrl.outs[0]    ]
		self.outsToCtrls = [[self.Ctrl.Name.ctrl] ]				
		#CLASSE MODIF
		#INSTANCE MODIF
		name       = args.get( 'n'     , None )	
		pos        = args.get( 'pos'   , None )
		shape      = args.get( 'shape' , None )
		form       = args.get( 'form'  , None )	
		colors     = args.get( 'colors'  , None )	
		aim        = args.get( 'aim'  , None )						
		#UPDATE
		if not( name   == None ): self.Name.add( 'base'   , copy    = name   ) 
		if not( pos    == None ): self.Pos.add( 'masterA' , replace = pos[0] )		
		if not( shape  == None ): self.CurveShape.add(  'ctrl'    , value = shape                 )
		if not( form   == None ): self.CurveShape.add(  'ctrl'    , value = { 'form'   : form   } )
		if not( colors == None ): self.CurveShape.add(  'ctrl'    , value = { 'colors' : colors } )	
		
		constraintOuts = args.get( 'constraintOuts' , True )	
		if not( pos == None ) and( type(pos[0]) == types.StringType ):
			if( mc.objExists(pos[0]) == True ):

				if( constraintOuts ):
					for i in range( 0 , len(pos) ):
						self.Name.add(  'out{}'.format(i) , copy = pos[i] , objExists = True )
						self.Link.add(  'out{}'.format(i)      , Sources = [ self.outs[i] ] , Destinations = [ eval('self.Name.out{}'.format(i) )  ] , type = 'parent' , operation = 'oneMaster'  )					
						self.Link.add(  'outScale{}'.format(i) , Sources = [ self.outs[i] ] , Destinations = [ eval('self.Name.out{}'.format(i) )  ] , type = 'scale'  , operation = 'oneMaster'  )

				fathers = mc.listRelatives( pos[0] , p = True )
				if not( fathers == None ):		
					self.Name.add(  'in0' , copy = fathers[0] , objExists = True )		
					self.Link.add(  'in0' , Sources = [eval('self.Name.in0' )] , Destinations = [ self.ins[0] ] , type = 'parent' , operation = 'oneMaster'  )					


		#attrsName  = [ 'intensity' , 'colorR'  , 'colorG'  , 'colorB'  , 'sizeStart' , 'sizeEnd' , 'keepProportion' , 'offset' ]
		#attrsType  = [ 'float'    , 'float'  , 'float'  , 'float'  , 'float'    , 'float'   , 'floatOnOff'     , 'float' ]		
		#attrsValue = [  1          ,    1      , 0.821     ,  0.39     ,   0.05      ,     1      ,     1            ,   0      ]
		#self.Attr.add(  'ctrlB'  , self.CtrlB.Name.ctrl , attrsName , attrsType , attrsValue )
	
		#self.Link.add( self.Attr.ctrlB.sizeStart      , self.Attr.StretchyA.scale , type = 'simple' )
		#self.Link.add( self.Attr.ctrlB.sizeEnd        , self.Attr.StretchyB.scale , type = 'simple' )
		#self.Link.add( self.Attr.ctrlB.keepProportion , self.Attr.stretchy.jointCtrl   , type = 'simple' )
		
		'''
		# CONNECT DISTANCE OFFSET
		vectorAim = [  self.buildTrs[0][0] - self.buildTrs[1][0] , self.buildTrs[0][1] - self.buildTrs[1][1] , self.buildTrs[0][2] - self.buildTrs[1][2] ]	
		signAxes = utilsMayaApi.getAxesSignFromVector(  end.buildTrs[0]  ,  vectorAim )
		utilsMaya.buildOffsetConnection( end.ctrl + '.' +  self.offsetDistanceAttr    ,     end.multiOrig + '.translateX'     ,     offsetAttrs = [ [ '*' , signAxes[0] * -1 ] ]     )
		'''	
		
	def postBuild( self ):

		'''
		# EXP			
		expContent = ''
		
		expContent += '\n' + 'float $linearMult = 100;'		
		expContent += '\n' + ''	
		expContent += '\n' + '// GET ATTR'	
		expContent += '\n' + ''	
		expContent += '\n' + 'float $time = time;'	
		expContent += '\n' + ''	
		expContent += '\n' + 'float $linearSpeed  = {0}.linearSpeed;'.format( self.Ctrl.Name.ctrl.str() )	
		expContent += '\n' + 'float $linearOffset = {0}.linearOffset;'.format( self.Ctrl.Name.ctrl.str()  )		
		expContent += '\n' + ''	
		expContent += '\n' + 'float $sinSpeed     = {0}.sinSpeed;'.format( self.Ctrl.Name.ctrl.str()  )	
		expContent += '\n' + 'float $sinAmplitude = {0}.sinAmplitude;'.format( self.Ctrl.Name.ctrl.str()  )		
		expContent += '\n' + 'float $sinOffset    = {0}.sinOffset;'.format( self.Ctrl.Name.ctrl.str()  )		
		expContent += '\n' + ''	
		expContent += '\n' + ''	
		expContent += '\n' + '// LINEAR ROT'	
		expContent += '\n' + ''	
		expContent += '\n' + 'float $linearRot =  ( $linearSpeed * $time + $linearOffset ) * $linearMult ;'	
		expContent += '\n' + ''			
		expContent += '\n' + '// SINUSOIDAL ROT'
		expContent += '\n' + ''	
		expContent += '\n' + 'float $sinRot =  sin( $sinSpeed * $time + $linearOffset ) * $sinAmplitude ;'
		expContent += '\n' + ''	
		expContent += '\n' + '// TOTAL'	
		expContent += '\n' + ''	
		expContent += '\n' + '{0}.rotateY = $linearRot + $sinRot ;'.format( self.Ctrl.Name.joint.str()  )		
		expContent += '\n' + ''	

		expressionName = self.Name.base.str() + '_EXP'
		utilsMaya.buildSimpleExpression( expressionName , expContent )
		self.alls.append(expressionName)		
		
		
		# SET ATTR
		#mc.setAttr( self.LightConeA.manipGrp + '.visibility' , 0)	
		#mc.setAttr( self.LightConeB.manipGrp + '.visibility' , 0)					
		mc.setAttr( self.Attr.topNode.skeletonRef.str() , 2)			
		'''
		return ''