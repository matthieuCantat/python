


'''

#******************************************************** BUILD EXEMPLE RIG CTRL
import maya.cmds as mc
import python
from python.classe.rigModuleArm import *
reload(python.classe.rigModuleArm)



mc.file( f = True , new = True )
#=================================================
#_________________________________BUILD

armA = rigModuleArm( n = 'arm' , fk = True , ik = True , offset = True  )    
toExec = armA.build()
exec(toExec)

mc.setAttr("armTop_GRP.skeletonVis" , 1 )
mc.setAttr("armTop_GRP.ctrlVis" , 20 )


armA.delete()

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

mirrored = armA.duplicate( **args )

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


duplicated = armA.duplicate( **args )

for elem in duplicated:
    elem.build()

for elem in duplicated:
    elem.delete()



'''


import maya.cmds as mc
import maya.api.OpenMaya as ompy

from ..utils import utilsMath
from ..utils import utilsPython
from ..utils import utilsMaya
from ..utils import utilsMayaApi
from ..utils import utilsBin

#ATTR
from .rigModule import *            
from .rigCtrl import *          
from .rigStretchyJoint import *         
from .rigModuleChain import *
from .rigStretchyJoint import *   

class rigModuleArm( rigModule ):

	def __init__( self , **args ):
		rigModule.__init__( self , **args )

		self.doOffset       = args.get( 'offset'       , 0 )
		self.doFk           = args.get( 'fk'           , 0 )
		self.doIk           = args.get( 'ik'           , 0 )
		self.doPv           = args.get( 'pv'           , 0 )
		self.doPvOrient     = args.get( 'pvOrient'     , 0 )
		self.doStretch      = args.get( 'stretch'      , 0 ) 
		self.doSkeleton     = args.get( 'skeleton'     , 0 )			
		self.doMiddleOffset = args.get( 'middleOffset' , 0 )
		self.doIkCollision  = args.get( 'ikCollision'  , 0 )	
		self.doFkDynamic    = args.get( 'fkDyn'        , 0 )	
		name                = args.get( 'n'            , None )	
		pos                 = args.get( 'pos'          , None )
		self.attrStates     = args.get( 'attrStates'   , None )
		

		#CLASSE TYPE
		self.classeType = 'rigModuleArm'

		#SPECIAL
		self.ikSysAttr       = [ 'distance' , 'distanceBase' ]
		self.holdRotAttrType = 'floatOnOff'

		#CLASSE BLUE PRINT
		self.Name.add( 'base'  , baseName = self.classeType )

		self.Pos.add( 'A' , replace = [0,0,-2 , 0,0,0 , 1,1,1 ] )
		self.Pos.add( 'B' , replace = [4,0,-6 , 0,0,0 , 1,1,1 ] )
		self.Pos.add( 'C' , replace = [8,0,-2 , 0,0,0 , 1,1,1 ] )	

		self.Pos.add( 'aimAB' , append = [ {'replace': self.Pos.A } , {'aim': self.Pos.B } ] )
		self.Pos.add( 'aimBC' , append = [ {'replace': self.Pos.B } , {'aim': self.Pos.C } ] )
		self.Pos.add( 'aimAC' , append = [ {'replace': self.Pos.A } , {'aim': self.Pos.C } ] )

		#ROOT
		self.Name.add(       'root'   , ref = self.Name.base , baseNameAppend = 'root'      )
		self.Pos.add(        'root'   , replace = self.Pos.A                                )
		self.CurveShape.add( 'root'   , value = { 'form' : 'plane' , 'colors' : [14] , 'axe' : 'z' , 'scale' : self.ctrlScale*1   }  )
		
		self.Root = rigCtrl( n = self.Name.root , pos = [ self.Pos.root ] , shape = self.CurveShape.root , ctrlVisPriority = 0 , parent = self.Name.ctrlGrp , s = False ) 	
		
		#CLASSE UTILS
		self.SubRigs     += [ self.Root         ]
		self.SubRigsName += [ 'Root'            ]
		self.outs         = [ self.Root.outs[0] ]
		self.ins          = [ self.Root.ins[0]  ]
		outsRoot          = [ self.Root.outs[0] ]

		if( self.doOffset ):
			self.Name.add(       'offset' , ref = self.Name.base , baseNameAppend = 'offset' )
			self.Pos.add(        'offset' , replace = self.Pos.A               )
			self.CurveShape.add( 'offset' , value = { 'form' : 'crossArrow' , 'colors' : [14] , 'axe' : 'z' , 'scale' : self.ctrlScale*1   }  )		
			
			self.Offset= rigCtrl( n = self.Name.offset , parent = self.Name.ctrlGrp , pos = [ self.Pos.offset ] , shape = self.CurveShape.offset , ctrlVisPriority = 1 , modif = 1 , s = False) 		
			
			self.Link.add(       'offset' , Sources = outsRoot , Destinations = [ self.Offset.ins[0] ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )					

			#CLASSE UTILS
			self.SubRigs     += [ self.Offset         ]
			self.SubRigsName += [ 'Offset'            ]
			self.outs         = [ self.Offset.outs[0] ]
			self.ins         += [ self.Offset.ins[1]  ]
			outsRoot          = [ self.Offset.outs[0] ]

		#SKELETON
		self.Name.add(   'joints' , ref = self.Name.base  , baseNameAppend = 'out' )				
		
		self.Joints = rigSkeletonChain( n = self.Name.joints ,  pos = [ self.Pos.aimAB , self.Pos.aimBC , self.Pos.C ] , aim = True , parent = self.Name.skeletonGrp ) 
		
		self.Link.add(   'joint0' , Sources = outsRoot , Destinations = [ self.Joints.ins[0] ] , type = 'point' , operation = 'oneMaster' , maintainOffset = 1 )					

		#CLASSE UTILS
		self.SubRigs     += [ self.Joints ]
		self.SubRigsName += [ 'Joints'    ]
		self.outs         = self.Joints.outs
		self.outsToCtrls  = [ [self.Root.outs[0]] ]*len(self.Joints.outs)


		if( self.doFk ):
			self.Name.add(       'fk' , ref = self.Name.base , baseNameAppend = 'manipsFk'  )							
			self.CurveShape.add( 'fk' , value = { 'form' : 'circle' , 'colors' : [17] , 'axe' : 'x' , 'scale' : self.ctrlScale*0.5 }  )				
			
			self.Fk = rigModuleChain( n = self.Name.fk , pos = [ self.Pos.aimAB , self.Pos.aimBC , self.Pos.C ] , shape = self.CurveShape.fk     , ctrlVisPriority = 1 , attrStates = self.attrStates )		
			
			self.Link.add(       'fk' , Sources = outsRoot                , Destinations = [ self.Fk.ins[0]  ]       , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )			
			self.Link.add( 'joint0'   , Sources = [ self.Fk.outs[0]     ] , Destinations = [ self.Joints.outs[0] ]   , type = 'parent'   )
			self.Link.add( 'joint1'   , Sources = [ self.Fk.outs[1]     ] , Destinations = [ self.Joints.outs[1] ]   , type = 'orient'   )
			self.Link.add( 'joint2'   , Sources = [ self.Fk.outs[2]     ] , Destinations = [ self.Joints.outs[2] ]   , type = 'orient'   ) 			
			#CLASSE UTILS
			self.SubRigs     += [ self.Fk  ]
			self.SubRigsName += [ 'Fk'     ]
			self.outsToCtrls  = [[self.Fk.Name.ctrl0] ,[self.Fk.Name.ctrl1] ,[self.Fk.Name.ctrl2] , [self.Root.Name.ctrl ] ] 
					

		if( self.doIk ):
			#CLASSE BLUE PRINT
			self.Name.add( 'handle'              , ref = self.Name.base , baseNameAppend = 'handle'         , type = ''         )
			self.Name.add( 'handleBase'          , ref = self.Name.base , baseNameAppend = 'handleBase'     , type = ''         )
			self.Name.add( 'ikHandle'            , ref = self.Name.base , baseNameAppend = ''               , type = 'ikHandle' )
			self.Name.add( 'ikEffector'          , ref = self.Name.base , baseNameAppend = ''               , type = 'ikEffector' )
			
			self.CurveShape.add(  'handle'     , value = { 'form' : 'cube'   , 'colors' : [13] , 'axe' : 'x' , 'scale' : self.ctrlScale*0.5 }  )
			self.CurveShape.add(  'handleBase' , value = { 'form' : 'cube'   , 'colors' : [13] , 'axe' : 'x' , 'scale' : self.ctrlScale*0.5 }  )

			self.Handle     = rigCtrl(  n = self.Name.handle     , pos = [ self.Pos.C     ] , shape = self.CurveShape.handle     , ctrlVisPriority = 0  , parent = self.Name.ctrlGrp , s = False) 	
			self.HandleBase = rigCtrl(  n = self.Name.handleBase , pos = [ self.Pos.aimAC ] , shape = self.CurveShape.handleBase , ctrlVisPriority = 0  , parent = self.Name.ctrlGrp , s = False) 	

			ikSolvers = ['ikSCsolver','ikRPsolver']
			self.Link.add( 'ik'    , Sources = [ self.Name.ikHandle , self.Name.ikEffector ]     , Destinations = self.Joints.outs[0:3]                       , type = ikSolvers[self.doPv] , parents = [self.Name.rigGrp , None ] )		
	
			self.Link.add( 'handle'     , Sources = outsRoot                    , Destinations = [ self.Handle.ins[0]     ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )	
			self.Link.add( 'handleBase' , Sources = outsRoot                    , Destinations = [ self.HandleBase.ins[0] ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )							
			self.Link.add( 'joint0'     , Sources = [ self.HandleBase.outs[0] ] , Destinations = [ self.Joints.outs[0] ]    , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1  )			
			self.Link.add( 'joint2'     , Sources = [ self.Handle.outs[0]     ] , Destinations = [ self.Joints.outs[2] ]    , type = 'orient' , operation = 'oneMaster' , maintainOffset = 0  )       
			
			if( ikSolvers[self.doPv] == 'ikSCsolver' ):
				self.Link.add( 'ikCnsPoint'       , Sources = [ self.Handle.outs[0]                           ] , Destinations = [ self.Name.ikHandle         ] , type = 'point'       , operation = 'oneMaster' , maintainOffset = 1 )			
				self.Link.add( 'ikCnsOrient'      , Sources = [ self.HandleBase.outs[0] , self.Handle.outs[0] ] , Destinations = [ self.Name.ikHandle         ] , type = 'orientSpace' , spaceDriver = self.Handle.Name.ctrl , spaceAttr = 'orientDriver' , spaceNames = ['base','handle'] , spaceValue = 0 , operation = 'oneMaster' , maintainOffset = 0 )			      
			else:
				self.Link.add( 'ikCns'        , Sources = [ self.Handle.outs[0]                           ] , Destinations = [ self.Name.ikHandle ] , type = 'parent'       , operation = 'oneMaster' , maintainOffset = 1 )			

			#CLASSE UTILS
			self.SubRigs     += [ self.Handle , self.HandleBase ]
			self.SubRigsName += [ 'Handle'    , 'HandleBase'    ]
			self.ins         += [  self.Handle.ins[0] , self.HandleBase.ins[0] ]		 
			self.outs        += [  self.Handle.outs[0]          ]
			self.outsToCtrls += [ [self.Handle.Name.ctrl]       ] 


			if( self.doPv ):			
				self.Name.add(       'pv' , ref = self.Name.base , baseNameAppend = 'pv' , type = ''  )	
				self.Pos.add(        'pv' , append = [ { 'replace': self.Pos.A } , {'blend': self.Pos.C } , {'orient': self.Pos.aimAC } , {'overshoot': [self.Pos.B , 1.3 ] } ]   )
				self.CurveShape.add( 'pv' , value = { 'form' : 'sphere' , 'colors' : [6]  , 'axe' : 'x' , 'scale' : self.ctrlScale*0.2 }  )
				
				self.Pv = rigCtrl(  n = self.Name.pv  , pos = [ self.Pos.pv ] , shape = self.CurveShape.pv , ctrlVisPriority = 0  , parent = self.Name.ctrlGrp  , r = False , s = False) 	   					 				
				
				self.Link.add(   'pvIn'  , Sources = outsRoot            , Destinations = [ self.Pv.ins[0]     ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )	
				self.Link.add(   'pvOut' , Sources = [ self.Pv.outs[0] ] , Destinations = [ self.Name.ikHandle ] , type = 'poleVector' ,  maintainOffset = 0 )		

				#CLASSE UTILS
				self.SubRigs     += [ self.Pv  ]
				self.SubRigsName += [ 'Pv'     ]

				if( self.doPvOrient ):
					self.Name.add( 'pvOrient_IkSys'      , ref = self.Name.base , baseNameAppend = 'pvOrient_IkSys' , type = ''         )		
					self.Name.add( 'followWrist_reverse' , ref = self.Name.base , baseNameAppend = 'followWrist'    , type = 'reverse'  )
					self.Name.add( 'transLoc'            , ref = self.Name.base , baseNameAppend = 'transmission'   , type = ''         )	
					self.Link.add( 'paPvSwitch'         , Sources = [ self.HandleBase.Name.ctrl , self.StretchyPv.Name.jointA ] , Destinations = [ self.Pv.Name.topNode         ] , type = 'parent' ,  maintainOffset = 1 )	

					pvAttrs      = [ 'followHandle' ] 
					pvAttrsType  = [ 'floatOnOff'   ] 		
					pvAttrsValue = [  1             ] 
					self.Attr.add(  'pv'     , Name = self.Pv.Name.ctrl       , attrName = pvAttrs     , attrType = pvAttrsType     , attrValue = pvAttrsValue     )
			

			if( self.doFk ):
				self.Attr.add( 'Ctrl2'     , Name = self.Fk.Ctrl2.Name.ctrl , attrName = ['holdRot']  , attrType = ['floatOnOff']   , attrValue = [1] )
				self.Attr.add( 'root'      , Name = self.Root.Name.ctrl     , attrName = ['IK']       , attrType = ['intOnOff']     , attrValue = [0] , attrKeyable = [False]  )
				self.Attr.add( 'ikHandle'  , Name = self.Name.ikHandle      , attrName = ['ikBlend']  , attrType = ['float']        , attrValue = [1] )
			
				self.Link.add( 'ikSwitch'    , Sources = [ self.Attr.root.IK ]   , Destinations = [ self.Attr.ikHandle.ikBlend , self.Handle.Name.ctrl , self.HandleBase.Name.ctrl  ] , type = 'simple' )			
				self.Link.add( 'ikSwitchInv' , Sources = [ self.Attr.root.IK ]   , Destinations = [  self.Fk.Ctrl0.Name.ctrl                                                        ] , type = 'inverse01' )			
				
				self.Link.add( 'joint0'     , Sources = [ self.Fk.outs[0] , self.HandleBase.outs[0] ] , Destinations = [ self.Joints.outs[0] ] , type = 'parentSpace'  , spaceDriver = self.Root.Name.ctrl , spaceAttr = 'IK' , clear = True )  
				self.Link.add( 'joint2'     , Sources = [ self.Fk.outs[2] , self.Handle.outs[0]     ] , Destinations = [ self.Joints.outs[2] ] , type = 'orientSpace'  , spaceDriver = self.Root.Name.ctrl , spaceAttr = 'IK' , clear = True , maintainOffset = 0 )       	      
				
				if( self.doPv ):
					self.Link.add( 'ikSwitchPv'    , Sources = [ self.Attr.root.IK ] , Destinations = [ self.Pv.Name.ctrl  ] , type = 'simple' )			


			if( self.doStretch ):
				self.Name.add( 'stretchExp'          , ref = self.Name.base , baseNameAppend = 'stretch'        , type = 'EXP'      )
				self.StretchyPv = rigStretchyJoint( n = self.Name.pvOrient_IkSys , pos = [ self.Pos.aimAB , self.Pos.C ] , aim = True  )
				self.Parent.add( 'stretchyPvStore' , Name = self.StretchyPv.Name.topNode                                                       , parent = self.Name.rigGrp  )	
				self.Link.add( 'paRootStretchPv0'   , Sources = [ self.HandleBase.Name.ctrl   ]                             , Destinations = [ self.StretchyPv.Name.masterA ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )		
				self.Link.add( 'paHandleStretchPv1' , Sources = [ self.Handle.Name.ctrl ]                                   , Destinations = [ self.StretchyPv.Name.masterB ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )		

			
				handleAttrs      = [ 'stretchUP'  , 'stretchDwn' , 'reduceClapping' ] 
				handleAttrsType  = [ 'floatOnOff' , 'floatOnOff' , 'floatOnOff'     ] 		
				handleAttrsValue = [  1           ,    0         ,    1             ] 			
				self.Attr.add(  'handle' , Name = self.Handle.Name.ctrl   , attrName = handleAttrs , attrType = handleAttrsType , attrValue = handleAttrsValue )
			
	
				#CLASSE UTILS
				self.SubRigs     += [ self.StretchyPv ]
				self.SubRigsName += [ 'StretchyPv'     ]

			
		if( self.doMiddleOffset ):
			
			#CLASSE BLUE PRINT			
			self.Name.add( 'offsetMiddle'        , ref = self.Name.base , baseNameAppend = 'offsetMiddle'        )	
			self.Name.add( 'offsetMiddleA'       , ref = self.Name.base , baseNameAppend = 'offsetMiddleA'       )	
			self.Name.add( 'offsetMiddleB'       , ref = self.Name.base , baseNameAppend = 'offsetMiddleB'       )
			self.Name.add( 'middleOrient_IkSys'  , ref = self.Name.base , baseNameAppend = 'middleOrient_IkSys'  )	
			self.Name.add( 'middleOrientA_IkSys' , ref = self.Name.base , baseNameAppend = 'middleOrientA_IkSys' )	
			self.Name.add( 'middleOrientB_IkSys' , ref = self.Name.base , baseNameAppend = 'middleOrientB_IkSys' )	
			self.Name.add( 'endA'                , ref = self.Name.base , baseNameAppend = 'endA'                )	 
			self.Name.add( 'endB'                , ref = self.Name.base , baseNameAppend = 'endB'                )				

			self.Pos.add( 'middleA'  , append = [ {'replace': self.Pos.B } , {'orient': self.Pos.aimAB } ]  )
			self.Pos.add( 'middleB'  , append = [ {'replace': self.Pos.B } , {'orient': self.Pos.aimAC } ]  )
			self.Pos.add( 'middleC'  , append = [ {'replace': self.Pos.B } , {'orient': self.Pos.aimBC } ]  )

			self.CurveShape.add(  'middle'    , value = { 'form' : 'plane' , 'colors' : [6]  , 'axe' : 'x' , 'offset' : [0,0,0,0,0,0,1,1,1] , 'scale' : self.ctrlScale*0.4 }  )
			self.CurveShape.add(  'middleSide', value = { 'form' : 'arrow' , 'colors' : [6]  , 'axe' : 'x' , 'offset' : [0,0,0,0,0,0,1,1,1] , 'scale' : self.ctrlScale*0.3 }  )

			self.Middle  = rigCtrl( n = self.Name.offsetMiddle  , pos = [ self.Pos.middleB ]  , shape = self.CurveShape.middle      , joint = self.doJoint , offset = self.doOffset , ctrlVisPriority = 2  )
			self.MiddleA = rigCtrl( n = self.Name.offsetMiddleA , pos = [ self.Pos.middleA ]  , shape = self.CurveShape.middleSide  , joint = self.doJoint , offset = self.doOffset , ctrlVisPriority = 3  )        
			self.MiddleB = rigCtrl( n = self.Name.offsetMiddleB , pos = [ self.Pos.middleC ]  , shape = self.CurveShape.middleSide  , joint = self.doJoint , offset = self.doOffset , ctrlVisPriority = 3  )  
			self.StretchyMiddle  = rigStretchyJoint( n = self.Name.middleOrient_IkSys  , pos = [ self.Pos.A  , self.Pos.C ] , aim = True , rpSolver = True ) 
			self.StretchyMiddleA = rigStretchyJoint( n = self.Name.middleOrientA_IkSys , pos = [ self.Pos.A  , self.Pos.B ] , aim = True  )
			self.StretchyMiddleB = rigStretchyJoint( n = self.Name.middleOrientB_IkSys , pos = [ self.Pos.B  , self.Pos.C ] , aim = True  ) 
			self.StretchyEndA = rigStretchyJoint( n = self.Name.endA   , pos = [ self.Pos.A  , self.Pos.B ] , aim = True  )
			self.StretchyEndB = rigStretchyJoint( n = self.Name.endB   , pos = [ self.Pos.C  , self.Pos.B ] , aim = True  )

			self.Parent.add( 'middleStore'         , Name = [self.Middle.Name.topNode , self.MiddleA.Name.topNode , self.MiddleB.Name.topNode ] , parent = self.Name.ctrlGrp )
			self.Parent.add( 'stretchyMiddleStore' , Name = [self.StretchyMiddle.Name.topNode , self.StretchyMiddleA.Name.topNode , self.StretchyMiddleB.Name.topNode , self.StretchyEndA.Name.topNode , self.StretchyEndB.Name.topNode ], parent = self.Name.rigGrp )

			self.Link.add( 'pvPvHandle'       , Sources = [ self.Pv.outs[0]                  ] , Destinations = [ self.StretchyMiddle.Name.ikHandle] , type = 'poleVector' , operation = 'oneMaster' ,  maintainOffset = 0 )	
			self.Link.add( 'poCtrl1Middle'    , Sources = [ self.Fk.Ctrl1.outs[0]            ] , Destinations = [ self.Middle.Name.topNode         ] , type = 'point'      , operation = 'oneMaster' ,  maintainOffset = 1 )	
			self.Link.add( 'poMiddleMiddleA'  , Sources = [ self.Middle.outs[0]              ] , Destinations = [ self.MiddleA.Name.topNode        ] , type = 'point'      , operation = 'oneMaster' ,  maintainOffset = 1 )	
			self.Link.add( 'poMiddleAMiddleB' , Sources = [ self.MiddleA.outs[0]             ] , Destinations = [ self.MiddleB.Name.topNode        ] , type = 'point'      , operation = 'oneMaster' ,  maintainOffset = 1 )				
			self.Link.add( 'oSMiddleMiddle'   , Sources = [ self.StretchyMiddle.Name.jointA  ] , Destinations = [ self.Middle.Name.topNode         ] , type = 'orient'     , operation = 'oneMaster' ,  maintainOffset = 1 )	
			self.Link.add( 'oSMiddleAMiddleA' , Sources = [ self.StretchyMiddleA.Name.jointA ] , Destinations = [ self.MiddleA.Name.topNode        ] , type = 'orient'     , operation = 'oneMaster' ,  maintainOffset = 1 )	
			self.Link.add( 'oSMiddleBMiddleB' , Sources = [ self.StretchyMiddleB.Name.jointA ] , Destinations = [ self.MiddleB.Name.topNode        ] , type = 'orient'     , operation = 'oneMaster' ,  maintainOffset = 1 )	
	
			self.Link.add( 'poFkSMiddle'  , Sources = [ self.Fk.Ctrl0.outs[0] , self.Fk.Ctrl2.outs[0] ] , Destinations = [ self.StretchyMiddle.Name.masterA  , self.StretchyMiddle.Name.masterB  ]  , type = 'point'  , operation = '2by2' ,  maintainOffset = 1 )	
			self.Link.add( 'poFkSMiddleA' , Sources = [ self.Fk.Ctrl0.outs[0] , self.Middle.outs[0]   ] , Destinations = [ self.StretchyMiddleA.Name.masterA , self.StretchyMiddleA.Name.masterB ]  , type = 'point'  , operation = '2by2' ,  maintainOffset = 1 )	
			self.Link.add( 'poFkSMiddleB' , Sources = [ self.MiddleA.outs[0]  , self.Fk.Ctrl2.outs[0] ] , Destinations = [ self.StretchyMiddleB.Name.masterA , self.StretchyMiddleB.Name.masterB ]  , type = 'point'  , operation = '2by2' ,  maintainOffset = 1 )	
			self.Link.add( 'poFkSEndA'    , Sources = [ self.Fk.Ctrl0.outs[0] , self.MiddleB.outs[0]  ] , Destinations = [ self.StretchyEndA.Name.masterA    , self.StretchyEndA.Name.masterB    ]  , type = 'point'  , operation = '2by2' ,  maintainOffset = 1 )	
			self.Link.add( 'poFkSEndB'    , Sources = [ self.Fk.Ctrl2.outs[0] , self.MiddleB.outs[0]  ] , Destinations = [ self.StretchyEndB.Name.masterA    , self.StretchyEndB.Name.masterB    ]  , type = 'point'  , operation = '2by2' ,  maintainOffset = 1 )	
			
			#CLASSE UTILS
			self.SubRigs     += [ self.Middle , self.MiddleA , self.MiddleB , self.StretchyMiddle , self.StretchyMiddleA , self.StretchyMiddleB , self.StretchyEndA  , self.StretchyEndB ] 	
			self.SubRigsName += [ 'Middle'    , 'MiddleA'    , 'MiddleB'    , 'StretchyMiddle'    , 'StretchyMiddleA'    , 'StretchyMiddleB'    , 'StretchyEndA'     , 'StretchyEndB'    ] 						
			self.outs[1:4]    = [ self.StretchyEndA.outs[0] , self.MiddleB.outs[0] , self.Fk.outs[2] ]
		

		if ( self.doIkCollision )and ( self.doIk ):
			self.Name.add( 'collisionIk' , ref = self.Name.base , baseNameAppend = 'collisionIk' )			
			#snapPlaneObj = rigSnapPlane( self.Name.collisionIk  , self.collisionIkTrs , isSubRig = 1   , buildTrsDupli = self.buildTrsDupliNull[0:6]  ) 
			#self.SubRigs += [ snapPlaneObj ]
	

		#INSTANCE MODIF


		#UTILS	
		#CLASSE
		
		#SKELETON
		#self.Parent.add( [self.Root.Name.topNode       ] , self.Name.skeletonGrp )
		#self.Parent.add( [self.Fk.Ctrl0.Name.topNode ] , self.Root.Name.joint  )	
		#self.Link.add(   [ self.Root.Name.ctrl       ] , [ self.Root.Name.joint ] , type = 'parent' , operation = 'oneMaster' ,  maintainOffset = 1 )		


		'''
		# CALCUL  5 COLLISION IK TRS
		
		trsObj.getMiddleTrs( trsAimLastManip , inTrsValue = self.buildTrs[2] )
		facesTmp = trsObj.toCubeCoords( sortByFace = 1 )
		
		faceCenterY = []
		for i in range( 0 , 6 ):
			faceCenterY.append( utilsMath.getBarycentre( facesTmp[i] )[1] )
			
		faceCenterYSorted = faceCenterY[:]	
		faceCenterYSorted.sort()
		downFaceIndex = faceCenterY.index( faceCenterYSorted[0] )
		
		downFaceCoords = facesTmp[ downFaceIndex ]
		downFaceCenter = utilsMath.getBarycentre( facesTmp[ downFaceIndex ] )
		
		self.collisionIkTrs = []
		self.collisionIkTrs.append(  downFaceCoords[0] + trsObj[3:6] + [1,1,1]  )  
		self.collisionIkTrs.append(  downFaceCoords[1] + trsObj[3:6] + [1,1,1]  )  
		self.collisionIkTrs.append(  downFaceCoords[2] + trsObj[3:6] + [1,1,1]  ) 			
		self.collisionIkTrs.append(  downFaceCoords[3] + trsObj[3:6] + [1,1,1]  ) 
		self.collisionIkTrs.append(  downFaceCenter    + trsObj[3:6] + [1,1,1]  )		

		'''
						
		#UPDATE
		if not( name == None ): self.Name.add( 'base' , copy = name ) 
		if not( pos  == None ): 
			self.Pos.add( 'A'    , replace = pos[0] )
			self.Pos.add( 'B'    , replace = pos[1] )	
			self.Pos.add( 'C'    , replace = pos[2] )
			if( 3 < len(pos)  ): self.Pos.add( 'root' , replace = pos[3] )
			if( 4 < len(pos)  ): self.Pos.add( 'pv'   , replace = pos[4] )
		
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


		'''											
		if not( shape  == None ): self.CurveShape.add(  'ctrl'    , shape                 )
		if not( form   == None ): self.CurveShape.add(  'ctrl'    , { 'form'   : form   } )
		if not( colors == None ): self.CurveShape.add(  'ctrl'    , { 'colors' : colors } )	
		'''


	def postBuild( self ):

		if ( self.doIk ):
			#BUILD			
			'''	
			ikJointsGrp = mc.createNode( 'transform' , n = self.Name.ikJoint.str() + '_GRP' )
			mc.parent( ikJointsGrp , self.Name.rigGrp.str() )
			utilsMaya.buildConstraint( [ self.Root.outs[0].str()  , ikJointsGrp  ] , [ 'parent' , 'scale' ] , 'oneMaster' , 1 )			    	
			# IK___________CREATE JOINT
			ikJoints = [ self.Name.ikJoint.str() + 'A' , self.Name.ikJoint.str() + 'B' , self.Name.ikJoint.str() + 'C' ]
			ikJointsPos = [ self.Pos.aimAB.value() , self.Pos.aimBC.value() , self.Pos.C.value() ]
			mc.select( cl = True )
			mc.joint( n = ikJoints[0] , p = ikJointsPos[0][0:3] , o = ikJointsPos[0][3:6]  )
			mc.select( cl = True )
			mc.joint( n = ikJoints[1] , p = ikJointsPos[1][0:3] , o = ikJointsPos[1][3:6]  )
			mc.select( cl = True )
			mc.joint( n = ikJoints[2] , p = ikJointsPos[2][0:3] , o = ikJointsPos[2][3:6]  )
			mc.parent( ikJoints[0] , ikJointsGrp )
			mc.parent( ikJoints[1] , ikJoints[0] )
			mc.parent( ikJoints[2] , ikJoints[1] )
	
			self.utils_prepareJointForIk( ikJoints )
			# IK___________CREATE JOINT TRANSFER
			ikJointsTransfer = [ self.Name.ikJoint.str() + 'TransferA' , self.Name.ikJoint.str() + 'TransferB' , self.Name.ikJoint.str() + 'TransferC' ]
			mc.select( cl = True )
			mc.joint( n = ikJointsTransfer[0] , p = ikJointsPos[0][0:3] , o = ikJointsPos[0][3:6]  )
			mc.select( cl = True )
			mc.joint( n = ikJointsTransfer[1] , p = ikJointsPos[1][0:3] , o = ikJointsPos[1][3:6]  )
			mc.select( cl = True )
			mc.joint( n = ikJointsTransfer[2] , p = ikJointsPos[2][0:3] , o = ikJointsPos[2][3:6]  )
			mc.parent( ikJointsTransfer[0] , ikJointsGrp )
			mc.parent( ikJointsTransfer[1] , ikJointsTransfer[0] )
			mc.parent( ikJointsTransfer[2] , ikJointsTransfer[1] )
	
			self.utils_prepareJointForIk( ikJointsTransfer )
			utilsMaya.buildConstraint( [ ikJoints[0]  , ikJointsTransfer[0] ] , [ 'parent' ] , 'oneMaster' , 1 )	
			utilsMaya.buildConstraint( [ ikJoints[1]  , ikJointsTransfer[1] ] , [ 'parent' ] , 'oneMaster' , 1 )		
			utilsMaya.buildConstraint( [ ikJoints[2]  , ikJointsTransfer[2] ] , [ 'parent' ] , 'oneMaster' , 1 )				    	

			# IK___________CREATE SOLVER
			ikSolvers = ['ikSCsolver','ikRPsolver']				
			mc.ikHandle( sj = self.Joints.outs[0].str() , ee = self.Joints.outs[2].str() , sol = ikSolvers[self.doPv] , n = self.Name.handleIkSolver.str() )
			mc.parent( self.Name.handleIkSolver.str() , self.Name.rigGrp.str()  )
			utilsMaya.buildConstraint( [ self.Handle.outs[0].str()      , self.Name.handleIkSolver.str()  ] , [ 'parent' , 'scale' ] , 'oneMaster' , 1 )			   
			utilsMaya.buildConstraint( [ self.HandleBase.outs[0].str()  , self.Joints.ins[0].str()        ] , [ 'parent'  ] , 'oneMaster' , 1 )	
			
			if( self.doPv ):
				mc.poleVectorConstraint( self.Pv.Name.ctrl.str() , self.Name.handleIkSolver.str() )		
			''' 	
			# IK___________PV ORIENT SYSTEME
			if( self.doPvOrient ):			
				constraintCreated = mc.listRelatives( self.Pv.Name.topNode.str() , c = True , type = 'parentConstraint' )	
				
				mc.createNode( 'reverse' , n = self.Name.followWrist_reverse.str()  )
				mc.connectAttr(  self.Attr.pv.followHandle.str() , self.Name.followWrist_reverse.str() + '.inputX' )	
				
				mc.connectAttr(   self.Name.followWrist_reverse.str() + '.outputX' ,  constraintCreated[0] + '.' + self.HandleBase.Name.ctrl.str()  + 'W0' )			
				mc.connectAttr(   self.Attr.pv.followHandle.str()                  ,  constraintCreated[0] + '.' + self.StretchyPv.Name.jointA.str() + 'W1' )			
			
			'''
			# IK___________FK LINK	
			utilsMaya.buildConnections(  [ ikJointsTransfer[0]  , self.Fk.Ctrl0.Name.topNode.str()  ] , [ 'translate','rotate' ] , [ 'translate','rotate' ] , 'oneMaster'  )		
			utilsMaya.buildConnections(  [ ikJointsTransfer[1]  , self.Fk.Ctrl1.Name.topNode.str()  ] , [ 'translate','rotate' ] , [ 'translate','rotate' ] , 'oneMaster'  )		
			utilsMaya.buildConnections(  [ ikJointsTransfer[2]  , self.Fk.Ctrl2.Name.topNode.str()  ] , [ 'translate','rotate' ] , [ 'translate','rotate' ] , 'oneMaster'  )		
			
			#FK HOLD ROTATIONS
			utilsMaya.buildConstraint( [ self.Handle.Name.ctrl.str()  , ikJoints[2]  ] , [  'orient'  ] , 'oneMaster' , 1 )
			constraintCreated = mc.listRelatives( ikJoints[2] , c = True , type = 'orientConstraint' )	
			mc.connectAttr( self.Attr.Ctrl2.holdRot.str() , constraintCreated[0] + '.' + self.Handle.Name.ctrl.str() + 'W0' )
			'''
			if( self.doStretch ):
				# IK___________STRETCH EXPRESSION	
				stretchAxes = [0,0,0] #only work with x axis
		
				pA = self.Pos.A.value()
				pB = self.Pos.B.value()
				pC = self.Pos.C.value()				
				distanceMax = 0
				distanceMax += ompy.MVector( pB[0] - pA[0] , pB[1] - pA[1]  , pB[2] - pA[2] ).length()
				distanceMax += ompy.MVector( pC[0] - pB[0] , pC[1] - pB[1]  , pC[2] - pB[2] ).length()
												
				stretchExp = '\n\n'		
				stretchExp += '\n' +   '\n'
				stretchExp += '\n' +   'float $rapport = {0}/{1} / {2}.scaleX;'.format( self.StretchyPv.Attr.topNode.distance.str() , distanceMax , self.Fk.Name.topNode.str() ) 
				stretchExp += '\n' +   'float $scaleValue = 1;'
				stretchExp += '\n' +   '\n'
				stretchExp += '\n' +   'if( $rapport > 1 )'
				stretchExp += '\n' +   '{'
				stretchExp += '\n' +   '	$scaleValue = $rapport * {0} + ( 1 - {0} );'.format( self.Attr.handle.stretchUP.str()  )
				stretchExp += '\n' +   '}else{'
				stretchExp += '\n' +   '	$scaleValue = $rapport * {0} + ( 1 - {0} );'.format( self.Attr.handle.stretchDwn.str() )
				stretchExp += '\n' +   '}'
				stretchExp += '\n' +   '\n'
				stretchExp += '\n' +   '//_______________________________________________________________________________reduce claping____START'
				stretchExp += '\n' +   '\n'
				stretchExp += '\n' +   'float $scaleReduceClapping = 0.1 ;'
				stretchExp += '\n' +   'float $distanceReduceClapping[] = { 0.75 , 0.85 , 1.0 };'
				stretchExp += '\n' +   'float $mult =  0;'		
				stretchExp += '\n' +   '\n'		
				stretchExp += '\n' +   'if( $rapport <  $distanceReduceClapping[1] )'
				stretchExp += '\n' +   '{'				
				stretchExp += '\n' +   '	$mult = ( clamp( $distanceReduceClapping[0] , $distanceReduceClapping[1] , $rapport ) - $distanceReduceClapping[0] ) / ( $distanceReduceClapping[1] - $distanceReduceClapping[0] );'		
				stretchExp += '\n' +   '}else{'		
				stretchExp += '\n' +   '	$mult = 1 - ( clamp( $distanceReduceClapping[1] , $distanceReduceClapping[2] , $rapport ) - $distanceReduceClapping[1] ) / ( $distanceReduceClapping[2] - $distanceReduceClapping[1] );'				
				stretchExp += '\n' +   '}'		
				stretchExp += '\n' +   '\n'		
				stretchExp += '\n' +   'if( ( $rapport <  $distanceReduceClapping[0] )||( $rapport >  $distanceReduceClapping[2] ) )'				
				stretchExp += '\n' +   '{'				
				stretchExp += '\n' +   '	$mult = 0;'
				stretchExp += '\n' +   '}'		
				stretchExp += '\n' +   '\n'		
				stretchExp += '\n' +   'float $reduceClappingValue = $scaleValue - {0} * $scaleReduceClapping * $mult;'.format( self.Attr.handle.reduceClapping.str() )		
				stretchExp += '\n' +   '\n'				
				stretchExp += '\n' +   '//_______________________________________________________________________________reduce claping____END'		
				stretchExp += '\n' +   '\n'	
				stretchExp += '\n' +   '{0}.scaleX = $reduceClappingValue;'.format( ikJoints[0] )	
				stretchExp += '\n' +   '{0}.scaleX = $reduceClappingValue;'.format( ikJoints[1] )	
						     
				#utilsMaya.buildSimpleExpression( self.Name.stretchExp.str() , stretchExp )
        
		'''
		# IK COLLISION
		if( self.ikCollision == 1 ): 			
			mc.parent( snapPlaneObj.mainGrp , self.ikRigGrp )
			utilsMaya.buildConstraint( [ handle.ctrl   , snapPlaneObj.subRigObjs[0].ins[0] , snapPlaneObj.subRigObjs[1].ins[0] , snapPlaneObj.subRigObjs[2].ins[0] , snapPlaneObj.subRigObjs[3].ins[0] ] , [ 'parent' , 'scale' ] , 'oneMaster' , 1 )
			utilsMaya.buildConstraint( [ snapPlaneObj.outs[0] , handle.skn ] , [ 'parent' , 'scale' ] , 'oneMaster' , 1 )
		'''
		#TRANS LOCATOR
		'''		
		transLocNames = [ self.Name.transLocs.str() + 'A' , self.Name.transLocs.str() + 'B' , self.Name.transLocs.str() + 'C' ]
		utilsMaya.buildSimpleLoc( transLocNames[0] , self.Pos.aimAB.value() )
		utilsMaya.buildSimpleLoc( transLocNames[1] , self.Pos.aimBC.value() )
		utilsMaya.buildSimpleLoc( transLocNames[2] , self.Pos.C.value()     )									
		mc.parent( transLocNames[0] , self.Name.rigGrp.str() )	
		mc.parent( transLocNames[1] , transLocNames[0] )
		mc.parent( transLocNames[2] , transLocNames[1] )

		utilsMaya.buildConstraint( [ ikGrp       , transLocNames[0] ] , [  'scale' ] , 'oneMaster' , 1 )
		utilsMaya.buildConstraint( [ ikJoints[0] , transLocNames[0] ] , [ 'parent' ] , 'oneMaster' , 1 )
		utilsMaya.buildConstraint( [ ikJoints[1] , transLocNames[1] ] , [ 'parent' ] , 'oneMaster' , 1 )
		utilsMaya.buildConstraint( [ ikJoints[2] , transLocNames[2] ] , [ 'parent' ] , 'oneMaster' , 1 )
		'''	

		#SOMETHING TO DO WITH CONSTRAINT ?
		'''
			add a fonction to link to link the result constraint to an other attr , of place a usefull node inbetween like a multiply divide
		'''
		#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! revisite first the IK sys, create a chain in parrallele instead of the FK joints!!!!!!!!!!!!!!!!!!!!!!!!!
		


		'''
		pA = self.Pos.masterC.value()
		pB = self.Pos.masterD.value()
		vector = om.MVector( pA[0] - pB[0] , pA[1] - pB[1] , pA[2] - pB[2] )
		dist   = vector.length()
		mc.setAttr( self.Attr.ctrlTarget.offset.str()  , dist )		
		# SET ATTR
		mc.setAttr( self.StretchyRotB.Name.topNode.str() + '.visibility' , 0)	
		mc.setAttr( self.StretchyRotA.Name.topNode.str() + '.visibility' , 0)					
		mc.setAttr( self.Attr.topNode.skeletonRef.str() , 2)		
	
		'''	

		return ''

	def utils_prepareJointForIk( self , ikJoints ):

		for joint in ikJoints :
			utils_jointOrientToRotation( joint )
			utils_rotationToPrefAngle( joint )



def utils_jointOrientToRotation( joint ):
	#CREATE AND PLACE TRSF
	trsfTmp = mc.createNode( 'transform' , n = 'utils_jointOrientToRotation_' + joint )
	father  = mc.listRelatives( joint , p = True )
	mc.parent( trsfTmp , father )
	mc.delete( mc.parentConstraint( joint , trsfTmp) )
	#CLEAN JOINT
	for axe in ['X','Y','Z']:
		mc.setAttr( '{}.jointOrient{}'.format( joint , axe) , 0 )
		mc.setAttr( '{}.rotate{}'.format( joint , axe) , mc.getAttr( '{}.rotate{}'.format( trsfTmp , axe) ) )
	mc.delete( trsfTmp )


def utils_rotationToJointOrient( joint ):
	pass

def utils_rotationToPrefAngle( joint ):
	for axe in ['X','Y','Z']:
		mc.setAttr( '{}.preferredAngle{}'.format( joint , axe) , mc.getAttr( '{}.rotate{}'.format( joint , axe) ) )
