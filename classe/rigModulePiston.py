
'''
#******************************************************** BUILD EXEMPLE RIG CTRL
import maya.cmds as mc
import python
from python.classe.rigModulePiston import *
reload(python.classe.rigModulePiston)

mc.file( f = True , new = True )
#=================================================


#_________________________________BUILD

pistonA = rigModulePiston( n = 'arm' , pos = [ [5,0,3,0,0,0,1,1,1] , [2,0,0,0,0,0,1,1,1] ] , form = 'cylinder' , colors = [17] , aim = 1 )	
pistonA.build()


pistonA.delete()


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

mirrored = pistonA.duplicate( **args )

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


duplicated = pistonA.duplicate( **args )

for elem in duplicated:
    elem.build()

for elem in duplicated:
    elem.delete()

'''

from .rigModule import *        	
from .rigCtrl import *          
from .rigStretchyJoint import * 	


class rigModulePiston( rigModule ):

	def __init__( self , **args ):
		rigModule.__init__( self , **args )

		#CLASSE TYPE
		self.classeType = 'rigModulePiston'

		#CLASSE BLUE PRINT
		self.Name.add( 'base'      , baseName = self.classeType )
		self.Pos.add( 'masterA' , replace = [ 1,0,0,0,0,0,1,1,1] )
		self.Pos.add( 'masterB' , replace = [-1,0,0,0,0,0,1,1,1] )
		self.CurveShape.add( 'ctrl' , value = { 'form' : 'cylinder' , 'colors' : [13] , 'axe' : 'x' , 'offset' : [0,0,0,0,0,0,1,1,1] }  )

		self.Name.add( 'ctrlA'     , ref = self.Name.base , baseNameAppend = 'OffsetA'    )
		self.Name.add( 'ctrlB'     , ref = self.Name.base , baseNameAppend = 'OffsetB'    )
		self.Name.add( 'stretchyA' , ref = self.Name.base , baseNameAppend = 'StretchyA'  )	
		self.Name.add( 'stretchyB' , ref = self.Name.base , baseNameAppend = 'stretchyB'  )								

		self.CtrlA = rigCtrl( n = self.Name.ctrlA , pos = [ self.Pos.masterA ] , shape = self.CurveShape.ctrl , ctrlScale = self.ctrlScale*1 , parent = self.Name.ctrlGrp )		
		self.CtrlB = rigCtrl( n = self.Name.ctrlB , pos = [ self.Pos.masterB ] , shape = self.CurveShape.ctrl , ctrlScale = self.ctrlScale*1 , parent = self.CtrlA.outs[0] )		

		self.StretchyA = rigStretchyJoint( n = self.Name.stretchyA , pos = [self.Pos.masterA , self.Pos.masterB ] , parent = self.Name.skeletonGrp )	
		self.StretchyB = rigStretchyJoint( n = self.Name.stretchyB , pos = [self.Pos.masterB , self.Pos.masterA ] , parent = self.Name.skeletonGrp )			
		
		#self.Parent.add( 'StretchyA' , Name = self.StretchyA.Name.topNode , parent = self.Name.skeletonGrp )		
		#self.Parent.add( 'StretchyB' , Name = self.StretchyB.Name.topNode , parent = self.Name.skeletonGrp )

		self.Link.add( 'CtrlA' , Sources = [ self.CtrlA.Name.ctrl ]  , Destinations = [ self.StretchyA.Name.masterA , self.StretchyB.Name.masterB ] , type = 'parent' , operation = 'oneMaster' )
		self.Link.add( 'CtrlB' , Sources = [ self.CtrlB.Name.ctrl ]  , Destinations = [ self.StretchyA.Name.masterB , self.StretchyB.Name.masterA ] , type = 'parent' , operation = 'oneMaster' )		

		#CLASSE UTILS
		self.SubRigs     = [ self.CtrlA , self.CtrlB , self.StretchyA , self.StretchyB ]
		self.SubRigsName = [ 'CtrlA'    , 'CtrlB'    , 'StretchyA'    , 'StretchyB'    ]
		self.ins         = [ self.CtrlA.ins[0]      , self.CtrlB.ins[0]      ]
		self.outs        = [ self.StretchyA.outs[0] , self.StretchyB.outs[0] ]
		self.outsToCtrls = [[self.CtrlA.Name.ctrl]  ,[self.CtrlB.Name.ctrl]  ]
		#CLASSE MODIF
		
		#INSTANCE MODIF
		name       = args.get( 'n'     , None )	
		pos        = args.get( 'pos'   , None )
		shape      = args.get( 'shape' , None )
		form       = args.get( 'form'  , None )	
		colors     = args.get( 'colors'  , None )	
		aim        = args.get( 'aim'  , None )						
		#UPDATE
		if not( name == None ): self.Name.add( 'base' , copy = name ) 
		if not( pos  == None ): 
			self.Pos.add( 'masterA' , replace = pos[0] )
			self.Pos.add( 'masterB' , replace = pos[1] )
		if( aim ):
			self.Pos.add(  'masterA' , aim = pos[1] )	
			self.Pos.add(  'masterB' , aim = pos[0] )				
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


	def buildRig( self ):
		pass			



