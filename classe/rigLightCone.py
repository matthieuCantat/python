
'''
#******************************************************** BUILD EXEMPLE RIG CTRL
import maya.cmds as mc
import python
from python.classe.rigLightCone import *
reload(python.classe.rigLightCone)
reload(python.classe.rigStretchyJoint)


mc.file( f = True , new = True )
#=================================================


#_________________________________BUILD

coneA = rigLightCone( n = 'cone' , pos = [ [3,0,0,0,0,0,1,1,1] , [5,0,4,0,0,0,1,1,1] ] , form = 'cube' , colors = [17] )    
coneA.printBuild = 1
toExec = coneA.build()
exec(toExec)


coneA.delete()

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

mirrored = coneA.duplicate( **args )

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


duplicated = coneA.duplicate( **args )

for elem in duplicated:
    elem.build()

for elem in duplicated:
    elem.delete()
    

'''

#ATTR


from .rig import *            
from .rigCtrl import *          
from .rigStretchyJoint import *
import maya.OpenMaya as om     


class rigLightCone( rig ):

	def __init__( self , **args ):
		rig.__init__( self , **args )

		#CLASSE TYPE
		self.classeType = 'rigLightCone'

		#CLASSE BLUE PRINT
		
		self.Name.add( 'base'    , baseName = self.classeType      )
		self.Name.add( 'topNode' , ref = self.Name.base , baseNameAppend = 'top' , type = 'GRP'  )	
		self.Pos.add(  'A'       , replace  = [ 1,0,0,0,0,0,1,1,1] )
		self.Pos.add(  'B'       , replace  = [-1,0,0,0,0,0,1,1,1] )
		 
		self.Name.add( 'stretchyA'   , ref = self.Name.base , baseNameAppend = 'StretchyA'   , type = ''     )	
		
		attrsName  = [ 'sizeStart' , 'sizeEnd' , 'keepProportion'  , 'offset' , 'intensity' , 'colorR'  , 'colorG'  , 'colorB' ]
		attrsType  = [ 'float'     , 'float'    , 'floatOnOff'     , 'float'  , 'float'     , 'float'   , 'float'   , 'float'  ]		
		attrsValue = [   0.05      ,     1      ,     0            ,   2      ,  1          ,    1      , 0.821     ,  0.39    ]
		self.Attr.add(  'topNode'  , Name = self.Name.topNode , attrName = attrsName , attrType = attrsType , attrValue = attrsValue )
		
		self.StretchyA = rigStretchyJoint( n = self.Name.stretchyA , pos = [self.Pos.A , self.Pos.B ] , aim = True , parent = self.Name.topNode  )				
		

		self.Link.add( 'stretchX' , Sources = [1]                                , Destinations = [ self.StretchyA.Attr.topNode.stretchBlendX ] , type = 'normal' , operation = 'oneMaster' )		
		self.Link.add( 'stretchY' , Sources = [self.Attr.topNode.keepProportion] , Destinations = [ self.StretchyA.Attr.topNode.stretchBlendY ] , type = 'normal' , operation = 'oneMaster' )		
		self.Link.add( 'stretchZ' , Sources = [self.Attr.topNode.keepProportion] , Destinations = [ self.StretchyA.Attr.topNode.stretchBlendZ ] , type = 'normal' , operation = 'oneMaster' )		


		self.Name.add( 'cone'        , ref = self.Name.base , baseNameAppend = 'cone'          )
		
		coneSources  = [ self.StretchyA.Name.jointA , self.StretchyA.Name.jointB ]
		coneSources += [ self.Attr.topNode.sizeStart , self.Attr.topNode.sizeEnd , self.Attr.topNode.keepProportion , self.Attr.topNode.offset ]
		coneSources += [ self.Attr.topNode.intensity , self.Attr.topNode.colorR , self.Attr.topNode.colorG , self.Attr.topNode.colorB ]

		self.Link.add( 'cone'    , Sources = coneSources , Destinations = [ self.Name.cone ] , type = 'coneGeometry' , parents = [self.Name.topNode] )		

		#self.Link.add( 'offset'   , Sources = [self.Attr.topNode.offset        ] , Destinations = [ self.StretchyA.Attr.jointB.translateX ] , type = 'coneGeometry' , parents = [self.Name.TopNode] )		



		#CLASSE UTILS
		self.SubRigs     = [ self.StretchyA ]
		self.SubRigsName = [ 'StretchyA' ]
		self.ins     = self.StretchyA.ins
		self.outs    = self.StretchyA.outs
		self.Name.masterA = self.StretchyA.Name.masterA
		self.Name.masterB = self.StretchyA.Name.masterB	
		
		#CLASSE MODIF
		
		#INSTANCE MODIF
		name       = args.get( 'n'       , None )	
		pos        = args.get( 'pos'     , None )	
		self.aim   = args.get( 'aim'     , None )	
		parent     = args.get( 'parent'  , None )		
		
		if not( name == None ):  self.Name.add( 'base' , copy = name ) 
		if not( pos  == None ): 
			self.Pos.add( 'A' , replace = pos[0] )
			self.Pos.add( 'B' , replace = pos[1] )
		if( self.aim ):
			self.Pos.add(  'masterA' , aim = self.Pos.B )	
			self.Pos.add(  'masterB' , aim = self.Pos.A )	

		if not( parent == None ):self.Name.add(       'topNode'  , parent = parent )     


		

