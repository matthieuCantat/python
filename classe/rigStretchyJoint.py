
'''
#******************************************************** BUILD EXEMPLE RIG CTRL
import maya.cmds as mc
import python
from python.classe.rigStretchyJoint import *
reload( python.classe.rigStretchyJoint)

mc.file( f = True , new = True )
#=================================================

#_________________________________BUILD
sjA = rigStretchyJoint( n = 'arm' , pos = [ [8,0,3,0,0,0,1,1,1] , [3,0,0,0,0,0,1,1,1] ]  , aim = True  )
sjA.printBuild = 1
toExec = sjA.build()
exec(toExec)

sjA.delete()

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

mirrored = sjA.duplicate( **args )

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


duplicated = sjA.duplicate( **args )

for elem in duplicated:
    elem.build()

for elem in duplicated:
    elem.delete()


#_________________________________REF
reload(python.classe.buildName)
from python.classe.buildName import *
from python.classe.buildPosition import *

Name = buildName( )
Name.add( 'base'        , baseName = 'leg'    )
Name.add( 'armB'        ,  ref = Name.base  , baseNameAppend = 'B'  )

Name.printInfo()

Pos = buildPosition()
Pos.add(  'masterA'      , [[5,0,-3,0,0,0,1,1,1]]  )
Pos.add(  'masterB'      , [[10,10,10,0,0,0,1,1,1]]  )

sjB = rigStretchyJoint( n = Name.armB , pos = [ Pos.masterA , Pos.masterB ] , aim = True  )	


sjA.Pos.printInfo()


sjB.build()

sjB.delete()


'''


import maya.cmds as mc
from ..utils import utilsMaya

from .rig import *	

       
class rigStretchyJoint(rig):

	def __init__( self , **args ):
		rig.__init__( self , **args )

		#CLASSE TYPE
		self.classeType = 'rigStretchyJoint'

		#CLASSE BLUE PRINT	
		self.Name.add( 'base' , baseName = self.classeType )
		self.Pos.add(  'A'    , replace = [ -1,0,0,0,0,0,1,1,1 ] )
		self.Pos.add(  'B'    , replace = [ 1,0,0,0,0,0,1,1,1  ] )	

		self.Name.add( 'topNode' , ref = self.Name.base , type = 'GRP'  )	
		self.Name.add( 'offsetA'      , ref = self.Name.base  , baseNameAppend = 'offsetA' , type =	'GRP' , parent = self.Name.topNode )
		self.Name.add( 'offsetB'      , ref = self.Name.base  , baseNameAppend = 'offsetB' , type =	'GRP' , parent = self.Name.topNode )			
		self.Name.add( 'masterA'      , ref = self.Name.base  , baseNameAppend = 'masterA' , type =	'GRP' , parent = self.Name.offsetA )
		self.Name.add( 'masterB'      , ref = self.Name.base  , baseNameAppend = 'masterB' , type =	'GRP' , parent = self.Name.offsetB )
		self.Name.add( 'jointA'       , ref = self.Name.base  , baseNameAppend = 'A'       , type =	'JNT' , parent = self.Name.topNode )
		self.Name.add( 'jointB'       , ref = self.Name.base  , baseNameAppend = 'B'       , type =	'JNT' , parent = self.Name.jointA  )
			
		self.Name.add( 'ikHandle'     , ref = self.Name.base , baseNameAppend = '' , type = 'ikHandle' )
		self.Name.add( 'ikEffector'   , ref = self.Name.base , baseNameAppend = '' , type = 'ikEffector' )
		
		self.Name.add( 'distDim'      , ref = self.Name.base  , baseNameAppend = 'Dist'    , type =	''     )										
		self.Name.add( 'stretchNodes' , ref = self.Name.base  , baseNameAppend = 'Stretchy', type =	''     )	

		self.Attr.add( 'topNode' , Name = self.Name.topNode , attrName = ['distance'      , 'distanceBase'  , 'stretch'       ]  , attrType = [ 'float'      , 'float'      , 'float'     ]  , attrValue = [0,1,0] )
		self.Attr.add( 'topNode' , Name = self.Name.topNode , attrName = ['stretchBlendX' , 'stretchBlendY' , 'stretchBlendZ' ]  , attrType = [ 'floatOnOff' , 'floatOnOff' , 'floatOnOff']  , attrValue = [0,0,0] )
		self.Attr.add( 'jointA'  , Name = self.Name.jointA )

		self.Pos.add( 'masterA' , Name = self.Name.masterA , replace = self.Pos.A      )
		self.Pos.add( 'masterB' , Name = self.Name.masterB , replace = self.Pos.B      )		
		self.Pos.add( 'offsetA' , Name = self.Name.offsetA , replace = self.Pos.masterA      )		
		self.Pos.add( 'offsetB' , Name = self.Name.offsetB , replace = self.Pos.masterB      )	
		self.Pos.add( 'jointA'  , Name = self.Name.jointA  , replace = self.Pos.masterA     )
		self.Pos.add( 'jointB'  , Name = self.Name.jointB  , replace = self.Pos.masterB      )	

		'''
		self.Dag.add( 'offsetA' , Name = self.Name.offsetA  , type = 'transform' )			
		self.Dag.add( 'offsetB' , Name = self.Name.offsetB  , type = 'transform' )
		self.Dag.add( 'masterA' , Name = self.Name.masterA  , type = 'transform' )
		self.Dag.add( 'masterB' , Name = self.Name.masterB  , type = 'transform' )	
		self.Dag.add( 'jointA'  , Name = self.Name.jointA   , type = 'joint'     )
		self.Dag.add( 'jointB'  , Name = self.Name.jointB   , type = 'joint'     )

		self.Parent.add( 'offsetA' , Name = self.Name.offsetA , parent = self.Name.topNode  )			
		self.Parent.add( 'offsetB' , Name = self.Name.offsetB , parent = self.Name.topNode  )
		self.Parent.add( 'masterA' , Name = self.Name.masterA , parent = self.Name.offsetA  )
		self.Parent.add( 'masterB' , Name = self.Name.masterB , parent = self.Name.offsetB  )	
		self.Parent.add( 'jointA'  , Name = self.Name.jointA  , parent = self.Name.masterA  )
		self.Parent.add( 'jointB'  , Name = self.Name.jointB  , parent = self.Name.jointA   )				
		'''
		self.doPv = args.get( 'doPv' , 0 )

		ikSolvers = ['ikSCsolver','ikRPsolver']
		self.Link.add( 'ik'      , Sources = [ self.Name.ikHandle , self.Name.ikEffector ]  , Destinations = [self.Name.jointA , self.Name.jointB]                                                     , type = ikSolvers[self.doPv] , parents = [self.Name.topNode , None ] )		
		self.Link.add( 'stretch' , Sources = [ self.Name.masterA  , self.Name.masterB    ]  , Destinations = [self.Attr.topNode.distance , self.Attr.topNode.distanceBase, self.Attr.topNode.stretch ] , type = 'stretch'            , parents = [self.Name.topNode ]        )		
		self.Link.add( 'blendX'   , Sources = [ 1 , self.Attr.topNode.stretch ,  self.Attr.topNode.stretchBlendX ]  , Destinations = [self.Attr.jointA.scaleX ] , type = 'blend'  )		
		self.Link.add( 'blendY'   , Sources = [ 1 , self.Attr.topNode.stretch ,  self.Attr.topNode.stretchBlendY ]  , Destinations = [self.Attr.jointA.scaleY ] , type = 'blend'  )		
		self.Link.add( 'blendZ'   , Sources = [ 1 , self.Attr.topNode.stretch ,  self.Attr.topNode.stretchBlendZ ]  , Destinations = [self.Attr.jointA.scaleZ ] , type = 'blend'  )		

		self.Link.add( 'ikCns'      , Sources = [ self.Name.masterA , self.Name.masterB ] , Destinations = [ self.Name.jointA , self.Name.ikHandle ] , type = 'parent' , operation = '2by2' , maintainOffset = 1 )


		#CLASSE UTILS
		self.SubRigs = []
		self.ins     = [self.Name.masterA , self.Name.masterB ]
		self.outs    = [self.Name.jointA  , self.Name.jointB ]

		#CLASSE MODIF
		#INSTANCE MODIF
		name       = args.get( 'n'      , None )	
		pos        = args.get( 'pos'    , None )			
		parent     = args.get( 'parent' , None )
		self.doAim = args.get( 'aim'    , True )
		
		if not( name == None ): self.Name.add( 'base', copy = name ) 
		if not( pos  == None ):
			self.Pos.add( 'A' , replace = pos[0] )
			self.Pos.add( 'B' , replace = pos[1] )	
		if not( parent == None ): self.Name.add('topNode' , parent = parent )		
		if ( self.doAim ):
			self.Pos.add( 'A' , aim = self.Pos.B )
			self.Pos.add( 'masterB' , orient = self.Pos.A )

			
	def postBuild( self ):	
		return ''
	'''							
		#print(' GET NAMES ')
		jointA           = self.Name.jointA.str()
		jointB           = self.Name.jointB.str()
		ikHandle         = self.Name.ikHandle.str()
		masterA          = self.Name.masterA.str()
		masterB          = self.Name.masterB.str()
		distDim          = self.Name.distDim.str()
		stretchNodes     = self.Name.stretchNodes.str()
		topNode          = self.Name.topNode.str()
		attrDistance     = self.Attr.topNode.distance.str()
		attrDistanceBase = self.Attr.topNode.distanceBase.str()
		attrStretchX     = self.Attr.topNode.stretchX.str()
		attrStretchY     = self.Attr.topNode.stretchY.str()
		attrStretchZ     = self.Attr.topNode.stretchZ.str()		

		#print(' BUILD IK SYSTEME ')
		if( self.doRpSolver ): mc.ikHandle( sj = jointA , ee = jointB , sol = 'ikRPsolver' , n = ikHandle ) 
		else:                  mc.ikHandle( sj = jointA , ee = jointB , sol = 'ikSCsolver' , n = ikHandle ) 
		mc.parent( ikHandle , masterB )
		mc.setAttr( ikHandle + '.visibility' , 0 )	
	
		#print(' BUILD DISTANCE DIMENSION SYS ')		
		distDimElems = utilsMaya.buildDistDimensionSys( distDim , masterA , masterB , attrDistance )
		mc.parent( distDimElems[0] , topNode )	
		mc.setAttr( attrDistanceBase , mc.getAttr( attrDistance ) , l = True )
		mc.setAttr( distDimElems[0] + '.visibility' , 0 )

		#print(' BUILD STRETCH SYS	NODES ')				
		dObj      = attrDistance
		dBase     = attrDistanceBase	
		scaleX    = masterA +'.'+ 'scaleX'  		
		stretch   = [ attrStretchX , attrStretchY , attrStretchZ ]
		outScale  = [ jointA +'.'+ 'scaleX' , jointA +'.'+ 'scaleY' , jointA + '.' + 'scaleZ' ] 

		netWorkAttrs     = []
		netWorkNodeTypes = []					
		netWorkAttrs.append(       [ dObj , dBase , scaleX    , [1,stretch[0]] , outScale[0] ]    )
		netWorkNodeTypes.append(   [ None , '/'   , '/'       , 'blend'        , None        ]    )	
		netWorkAttrs.append(       [ None , None  , None      , [1,stretch[1]] , outScale[1] ]    )
		netWorkNodeTypes.append(   [ None , None  , None      , 'blend'        , None        ]    )	
		netWorkAttrs.append(       [ None , None  , None      , [1,stretch[2]] , outScale[2] ]    )
		netWorkNodeTypes.append(   [ None , None  , None      , 'blend'        , None        ]    )	
	
		stretchNodes = utilsMaya.buildNodeNetWork( stretchNodes , netWorkAttrs , netWorkNodeTypes )
	'''	