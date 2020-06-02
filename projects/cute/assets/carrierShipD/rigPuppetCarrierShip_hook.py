
	
'''

##########################################
############### RIG PUPPET ###############
##########################################



#INIT
import maya.cmds as mc
import python
import python.classe.readWriteInfo as readWriteInfo
import python.utils.utilsRigPuppet as utilsRigPuppet
import python.utils.utilsMaya      as utilsMaya
import python.utils.utilsPython    as utilsPython

from    python.projects.cute.assets.carrierShipD.rigPuppetCarrierShip import *
reload( python.projects.cute.assets.carrierShipD.rigPuppetCarrierShip          )
reload( python.projects.cute.assets.carrierShipD.rigPuppetCarrierShip_damp     )
reload( python.projects.cute.assets.carrierShipD.rigPuppetCarrierShip_reactor  )
reload( python.projects.cute.assets.carrierShipD.rigPuppetCarrierShip_propulsor)
reload( python.projects.cute.assets.carrierShipD.rigPuppetCarrierShip_hook     )

reload(python.classe.readWriteInfo)
reload(python.utils.utilsRigPuppet)
reload(python.utils.utilsMaya )
reload(python.utils.utilsPython )

rwi = readWriteInfo.readWriteInfo()

pathRigBoundB   = 'D:/mcantat_BDD/projects/cute/assets/carrierShipD/maya/scenes/carrierShipD_rigBoundB.ma'
pathCtrlShape   = 'D:/mcantat_BDD/projects/cute/assets/carrierShipD/maya/scenes/carrierShipD_utils_ctrlShape.ma'
pathRigPuppet   = 'D:/mcantat_BDD/projects/cute/assets/carrierShipD/maya/scenes/carrierShipD_rigPuppet.ma'


driver = 'traj_CTRL'

####################################################################
rwi.mayaScene_load( pathRigBoundB , open = True  )
####################################################################


puppet = rigPuppetCarrierShip_hook( tubes = False )
puppet.printBuild = 1
toExec = puppet.build()
exec(toExec)

'''

import maya.cmds as mc

from .....classe.rigPuppet import *  
from .....classe.rigCtrl import *  
from .....classe.rigModuleChain import *     
from .....classe.rigModuleArm import *    
from .....classe.rigModulePiston import *  
from .....classe.rigModuleTube import * 

       
class rigPuppetCarrierShip_hook(rigPuppet):

	def __init__( self , **args ):
		rigPuppet.__init__( self , **args )
		#CLASSE TYPE
		self.classeType = 'rigPuppetHook'
		self.doTubes      = args.get( 'tubes'      , True )
		self.doProjectors = args.get( 'projectors' , True )
		self.doGiros      = args.get( 'giros'      , True )
		#CLASSE BLUE PRINT - POS
		
		
		rootBLocs              = [x.encode('UTF8') for x in mc.ls('r_hook0Offset?_JNT'         , type = 'joint' )]
		armCoverLocs           = [x.encode('UTF8') for x in mc.ls('r_hook0ArmCover?_JNT'       , type = 'joint' )]		
		armCoverSideLocs       = [x.encode('UTF8') for x in mc.ls('r_hook0ArmCover?Left_JNT'   , type = 'joint' )]

		armCoverDampALocs      = [x.encode('UTF8') for x in mc.ls('r_hook0ArmCoverDampA?_JNT'     , type = 'transform' )]
		armCoverDampBLocs      = [x.encode('UTF8') for x in mc.ls('r_hook0ArmCoverDampB?_JNT'     , type = 'transform' )]
		armCoverSideDampALocs  = [x.encode('UTF8') for x in mc.ls('r_hook0ArmCoverDampA?Left_JNT' , type = 'transform' )]
		armCoverSideDampBLocs  = [x.encode('UTF8') for x in mc.ls('r_hook0ArmCoverDampB?Left_JNT' , type = 'transform' )]

		coverNoseLocs          = [x.encode('UTF8') for x in mc.ls('r_hook0CoverNose?_JNT'         , type = 'transform' )]
		coverNoseDampLocs      = [x.encode('UTF8') for x in mc.ls('r_hook0CoverNoseDamp?_JNT'     , type = 'transform' )]

		coverLocs              = [x.encode('UTF8') for x in mc.ls('r_hook0Cover?_JNT'          , type = 'joint' )]
		innerCoverLocs         = [x.encode('UTF8') for x in mc.ls('r_hook0InnerCover?_JNT'     , type = 'joint' )]
		pistonSlideLocs        = ['r_hook0PistonSlide0_JNT']
		
		pistonUpLocs           = [x.encode('UTF8') for x in mc.ls('r_hook0PistonUp?Left_JNT'   , type = 'joint' )]		
		pistonDownLocs         = [x.encode('UTF8') for x in mc.ls('r_hook0PistonDown?Left_JNT' , type = 'joint' )]	
		middleLocs             = ['r_hook0Middle0_JNT']
		
		armOffsetLocs          = [x.encode('UTF8') for x in mc.ls('r_hook0ArmBase?_JNT'        , type = 'joint' )]
		armLocs                = [x.encode('UTF8') for x in mc.ls('r_hook0Arm?_JNT'            , type = 'joint' )]
		pistonArmOffsetLocs    = [x.encode('UTF8') for x in mc.ls('r_hook0PistonArmOffset?_JNT' , type = 'joint' )]



		middleSpaceArmLocs     = [x.encode('UTF8') for x in mc.ls('r_hook0MiddleSpaceArm?_JNT'     , type = 'joint' )]
		holderLocs             = [x.encode('UTF8') for x in mc.ls('r_hook0Holder?_JNT'             , type = 'joint' )]
		holderSideLocs         = [x.encode('UTF8') for x in mc.ls('r_hook0Holder?Left_JNT'         , type = 'joint' )]
		#holderSecondaryLocs   = [x.encode('UTF8') for x in mc.ls('r_hook0HolderSecondary?_JNT'    , type = 'joint' )]
		holder1SpacePistonLocs = [x.encode('UTF8') for x in mc.ls('r_hook0Holder1SpacePiston?_JNT' , type = 'joint' )]
		holder3SpacePistonLocs = [x.encode('UTF8') for x in mc.ls('r_hook0Holder3SpacePiston?_JNT' , type = 'joint' )]		
			
		plugSlideLocs          = ['r_hook0PlugSlide0_JNT']
		plugLocs               = ['r_hook0Plug0_JNT']
		plugDampALocs          = [x.encode('UTF8') for x in mc.ls('r_hook0PlugDampA?_JNT'      , type = 'joint' )]	
		plugDampBLocs          = [x.encode('UTF8') for x in mc.ls('r_hook0PlugDampB?_JNT'      , type = 'joint' )]		
		plugMiddleLocs         = [x.encode('UTF8') for x in mc.ls('r_hook0PlugMiddle?_JNT'     , type = 'joint' )]	
		plugGrabLocs           = [x.encode('UTF8') for x in mc.ls('r_hook0PlugGrab?Left_JNT'   , type = 'joint' )]
		giroCoverLocs         = [ 'r_hook0GiroCover0_JNT' ] 
		GiroArmLocs            = [ 'r_hook0GiroArm0_JNT' ] 

		rotHolderLocs          = ['r_hook0RotHolder0Left_JNT']
		rotHolderDownLocs      = ['r_hook0RotHolderDown0_JNT']
		pressureHolderLocs     = ['r_hook0PressureHolder0Left_JNT']
		slideHolderLocs        = ['r_hook0SlideHolder0Left_JNT']	
				
		if( self.doTubes ):
			tubeCoverALocs            = [x.encode('UTF8') for x in mc.ls('r_hook0TubeCoverA?_JNT'          , type = 'joint' )]
			tubeCoverHangALocs        = [x.encode('UTF8') for x in mc.ls('r_hook0TubeCoverHangA?_JNT'      , type = 'joint' )]
			tubeCoverStraightALocs    = [x.encode('UTF8') for x in mc.ls('r_hook0TubeCoverStraightA?_JNT'  , type = 'joint' )]
			tubeCoverBLocs            = [x.encode('UTF8') for x in mc.ls('r_hook0TubeCoverB?_JNT'          , type = 'joint' )]
			tubeCoverHangBLocs        = [x.encode('UTF8') for x in mc.ls('r_hook0TubeCoverHangB?_JNT'      , type = 'joint' )]
			tubeCoverStraightBLocs    = [x.encode('UTF8') for x in mc.ls('r_hook0TubeCoverStraightB?_JNT'  , type = 'joint' )]
	
			tubeArmBackLocs           = [x.encode('UTF8') for x in mc.ls('r_hook0TubeArmBack?_JNT'         , type = 'joint' )]
			tubeArmBackHangLocs       = [x.encode('UTF8') for x in mc.ls('r_hook0TubeArmBackHang?_JNT'     , type = 'joint' )]
			tubeArmBackStraightLocs   = [x.encode('UTF8') for x in mc.ls('r_hook0TubeArmBackStraight?_JNT' , type = 'joint' )]
	
			tubeMiddleALocs           = [x.encode('UTF8') for x in mc.ls('r_hook0TubeMiddleA?_JNT'         , type = 'joint' )]
			tubeMiddleHangALocs       = [x.encode('UTF8') for x in mc.ls('r_hook0TubeMiddleHangA?_JNT'     , type = 'joint' )]		
			tubeMiddleStraightALocs   = [x.encode('UTF8') for x in mc.ls('r_hook0TubeMiddleStraightA?_JNT' , type = 'joint' )]		
			tubeMiddleBLocs           = [x.encode('UTF8') for x in mc.ls('r_hook0TubeMiddleB?_JNT'         , type = 'joint' )]
			tubeMiddleHangBLocs       = [x.encode('UTF8') for x in mc.ls('r_hook0TubeMiddleHangB?_JNT'     , type = 'joint' )]
			tubeMiddleStraightBLocs   = [x.encode('UTF8') for x in mc.ls('r_hook0TubeMiddleStraightB?_JNT' , type = 'joint' )]
	
			tubeArmALocs              = [x.encode('UTF8') for x in mc.ls('r_hook0TubeArmA?_JNT'            , type = 'joint' )]
			tubeArmHangALocs          = [x.encode('UTF8') for x in mc.ls('r_hook0TubeArmHangA?_JNT'        , type = 'joint' )]
			tubeArmStraightALocs      = [x.encode('UTF8') for x in mc.ls('r_hook0TubeArmStraightA?_JNT'    , type = 'joint' )]
			tubeArmBLocs              = [x.encode('UTF8') for x in mc.ls('r_hook0TubeArmB?_JNT'            , type = 'joint' )]		
			tubeArmHangBLocs          = [x.encode('UTF8') for x in mc.ls('r_hook0TubeArmHangB?_JNT'        , type = 'joint' )]
			tubeArmStraightBLocs      = [x.encode('UTF8') for x in mc.ls('r_hook0TubeArmStraightB?_JNT'    , type = 'joint' )]		
	
			tubeArmSmallLocs          = [x.encode('UTF8') for x in mc.ls('r_hook0TubeArmSmall?_JNT'        , type = 'joint' )]		
			tubeArmSideSmallLocs      = [x.encode('UTF8') for x in mc.ls('r_hook0TubeArmSmall?Left_JNT'    , type = 'joint' )]
	
			tubePlugSmallLocs         = [x.encode('UTF8') for x in mc.ls('r_hook0TubePlugSmall?_JNT'       , type = 'joint' )]		
			tubePlugSideSmallLocs     = [x.encode('UTF8') for x in mc.ls('r_hook0TubePlugSmall?Left_JNT'   , type = 'joint' )]



		mirrorPlane            = 'symPlane_hook1'		
		#CLASSE BLUE PRINT
		self.Name.add( 'base'             , baseName = 'hook' )

		#self.Name.add( 'root'             , ref = self.Name.base , baseNameAppend = 'root'          )
		self.Name.add( 'rootB'            , ref = self.Name.base , baseNameAppend = 'offset'        )

		self.Name.add( 'armCover'         , ref = self.Name.base , baseNameAppend = 'armCover'        )
		self.Name.add( 'armCoverSide'     , ref = self.Name.base , baseNameAppend = 'armCover'        )

		self.Name.add( 'armCoverDampA'     , ref = self.Name.base , baseNameAppend = 'armCoverDampA'        )
		self.Name.add( 'armCoverDampB'     , ref = self.Name.base , baseNameAppend = 'armCoverDampB'        )
		self.Name.add( 'armCoverSideDampA' , ref = self.Name.base , baseNameAppend = 'armCoverDampA'        )
		self.Name.add( 'armCoverSideDampB' , ref = self.Name.base , baseNameAppend = 'armCoverDampB'        )

		self.Name.add( 'coverNose'     , ref = self.Name.base , baseNameAppend = 'coverNose'        )
		self.Name.add( 'coverNoseDamp' , ref = self.Name.base , baseNameAppend = 'coverNoseDamp'    )


		self.Name.add( 'cover'            , ref = self.Name.base , baseNameAppend = 'cover'        )
		self.Name.add( 'innerCover'       , ref = self.Name.base , baseNameAppend = 'innerCover'        )			
		self.Name.add( 'pistonSlide'      , ref = self.Name.base , baseNameAppend = 'pistonSlide'        )
		
		self.Name.add( 'pistonUp'         , ref = self.Name.base , baseNameAppend = 'pistonUp'        )
		self.Name.add( 'pistonDown'       , ref = self.Name.base , baseNameAppend = 'pistonDown'        )
		self.Name.add( 'middle'           , ref = self.Name.base , baseNameAppend = 'middle'        )

		self.Name.add( 'armOffset'        , ref = self.Name.base , baseNameAppend = 'armBase'        )
		self.Name.add( 'arm'              , ref = self.Name.base , baseNameAppend = 'arm'           )
		self.Name.add( 'pistonArmOffset'  , ref = self.Name.base , baseNameAppend = 'pistonArmOffset')
		
		self.Name.add( 'middleSpaceArm'     , ref = self.Name.base , baseNameAppend = 'middleSpaceArm'    )
		self.Name.add( 'holder'             , ref = self.Name.base , baseNameAppend = 'holder'          )
		self.Name.add( 'holderSide'         , ref = self.Name.base , baseNameAppend = 'holder'          )
		#self.Name.add( 'holderSecondary'   , ref = self.Name.base , baseNameAppend = 'holderSecondary' )
		self.Name.add( 'holder1SpacePiston' , ref = self.Name.base , baseNameAppend = 'holder1SpacePiston' )
		self.Name.add( 'holder3SpacePiston' , ref = self.Name.base , baseNameAppend = 'holder3SpacePiston' )

		self.Name.add( 'plugSlide'        , ref = self.Name.base , baseNameAppend = 'plugSlide'        )
		self.Name.add( 'plug'             , ref = self.Name.base , baseNameAppend = 'plug'             )
		self.Name.add( 'plugDampA'        , ref = self.Name.base , baseNameAppend = 'plugDampA'        )
		self.Name.add( 'plugDampB'        , ref = self.Name.base , baseNameAppend = 'plugDampB'        )			
		self.Name.add( 'plugMiddle'       , ref = self.Name.base , baseNameAppend = 'plugMiddle'        )
		self.Name.add( 'plugGrab'         , ref = self.Name.base , baseNameAppend = 'plugGrab'        )	

		self.Name.add( 'rotHolder'        , ref = self.Name.base , baseNameAppend = 'rotLock'        )
		self.Name.add( 'rotHolderDown'    , ref = self.Name.base , baseNameAppend = 'rotLockDown'    )
		self.Name.add( 'pressureHolder'   , ref = self.Name.base , baseNameAppend = 'pressureLock'   )
		self.Name.add( 'slideHolder'      , ref = self.Name.base , baseNameAppend = 'slideLock'      )

		self.Name.add( 'giroCover'       , ref = self.Name.base , baseNameAppend = 'giroCover'        )
		self.Name.add( 'giroArm'          , ref = self.Name.base , baseNameAppend = 'giroArm'           )

		if( self.doTubes ):
			self.Name.add( 'tubeCoverA'          , ref = self.Name.base , baseNameAppend = 'tubeCoverA'          )
			self.Name.add( 'tubeCoverHangA'      , ref = self.Name.base , baseNameAppend = 'tubeCoverHangA'      )
			self.Name.add( 'tubeCoverStraightA'  , ref = self.Name.base , baseNameAppend = 'tubeCoverStraightA'  )
			self.Name.add( 'tubeCoverB'          , ref = self.Name.base , baseNameAppend = 'tubeCoverB'          )
			self.Name.add( 'tubeCoverHangB'      , ref = self.Name.base , baseNameAppend = 'tubeCoverHangB'      )		
			self.Name.add( 'tubeCoverStraightB'  , ref = self.Name.base , baseNameAppend = 'tubeCoverStraightB'  )	
	
			self.Name.add( 'tubeArmBack'         , ref = self.Name.base , baseNameAppend = 'tubeArmBack'         )
			self.Name.add( 'tubeArmBackHang'     , ref = self.Name.base , baseNameAppend = 'tubeArmBackHang'     )
			self.Name.add( 'tubeArmBackStraight' , ref = self.Name.base , baseNameAppend = 'tubeArmBackStraight' )	
	
			self.Name.add( 'tubeMiddleA'         , ref = self.Name.base , baseNameAppend = 'tubeMiddleA'         )
			self.Name.add( 'tubeMiddleHangA'     , ref = self.Name.base , baseNameAppend = 'tubeMiddleHangA'     )
			self.Name.add( 'tubeMiddleStraightA' , ref = self.Name.base , baseNameAppend = 'tubeMiddleStraightA' )		
			self.Name.add( 'tubeMiddleB'         , ref = self.Name.base , baseNameAppend = 'tubeMiddleB'         )
			self.Name.add( 'tubeMiddleHangB'     , ref = self.Name.base , baseNameAppend = 'tubeMiddleHangB'     )			
			self.Name.add( 'tubeMiddleStraightB' , ref = self.Name.base , baseNameAppend = 'tubeMiddleStraightB' )
	
			self.Name.add( 'tubeArmA'            , ref = self.Name.base , baseNameAppend = 'tubeArmA'            )
			self.Name.add( 'tubeArmHangA'        , ref = self.Name.base , baseNameAppend = 'tubeArmHangA'        )	
			self.Name.add( 'tubeArmStraightA'    , ref = self.Name.base , baseNameAppend = 'tubeArmStraightA'    )	
			self.Name.add( 'tubeArmB'            , ref = self.Name.base , baseNameAppend = 'tubeArmB'            )
			self.Name.add( 'tubeArmHangB'        , ref = self.Name.base , baseNameAppend = 'tubeArmHangB'        )
			self.Name.add( 'tubeArmStraightB'    , ref = self.Name.base , baseNameAppend = 'tubeArmStraightB'    )	
	
			self.Name.add( 'tubeArmSmall'        , ref = self.Name.base , baseNameAppend = 'tubeArmSmall'        )	
			self.Name.add( 'tubeArmSideSmall'    , ref = self.Name.base , baseNameAppend = 'tubeArmSmall'    )
	
			self.Name.add( 'tubePlugSmall'       , ref = self.Name.base , baseNameAppend = 'tubePlugSmall'       )	
			self.Name.add( 'tubePlugSideSmall'   , ref = self.Name.base , baseNameAppend = 'tubePlugSmall'   )	


		#CLASSE BLUE PRINT - SUBRIG
		#self.Root           = rigCtrl(        n = self.Name.root  , pos = [[0,0,0,0,0,0,1,1,1]]      , ctrlVisPriority = 0 , form = 'crossArrow'      , colors = ['green'] , parent = self.Name.topNode ) 	
		self.RootB          = rigModuleChain( n = self.Name.rootB         , pos = rootBLocs          , ctrlVisPriority = 1 , form = 'crossArrow'      , colors = ['green']  , attrStates = [['t','r']] )
		self.SubRigs       += [ self.RootB ]
		self.SubRigsName   += [ 'RootB'    ]

		self.ArmCover       = rigModuleArm(   n = self.Name.armCover      , pos = armCoverLocs       , ctrlVisPriority = 10 , ik = True , attrStates = [['rz']] )
		self.ArmCoverSide   = rigModuleArm(   n = self.Name.armCoverSide  , pos = armCoverSideLocs   , ctrlVisPriority = 10 , ik = True , attrStates = [['rz']] )
		self.Cover          = rigCtrl(        n = self.Name.cover         , pos = coverLocs          , ctrlVisPriority = 1 , form = 'crossArrow'      , colors = ['green'] , parent = self.Name.topNode , attrStates = [['rz']] )
		self.InnerCover     = rigModuleChain( n = self.Name.innerCover    , pos = innerCoverLocs     , ctrlVisPriority = 2 , form = 'arrow2sidesBend' , colors = ['red']    , attrStates = [ ['rz'], ['tx','rz'] ]  )
		self.PistonSlide    = rigCtrl(        n = self.Name.pistonSlide   , pos = pistonSlideLocs    , ctrlVisPriority = 2 , form = 'arrow2sides'     , colors = ['red']   , parent = self.Name.topNode , attrStates = [['rz','tx']])			
		
		self.CoverNose          = rigModulePiston( n = self.Name.coverNose         , pos = coverNoseLocs          , ctrlVisPriority = 10 , form = 'circle'          , colors = ['red'] , aim = 1 )	
		self.DampCoverNose      = rigModulePiston( n = self.Name.coverNoseDamp     , pos = coverNoseDampLocs      , ctrlVisPriority = 10 , form = 'circle'          , colors = ['red'] , aim = 1 )	

		self.DampArmCoverA      = rigModulePiston( n = self.Name.armCoverDampA     , pos = armCoverDampALocs     , ctrlVisPriority = 10 , form = 'circle'          , colors = ['red'] , aim = 1 )	
		self.DampArmCoverB      = rigModulePiston( n = self.Name.armCoverDampB     , pos = armCoverDampBLocs     , ctrlVisPriority = 10 , form = 'circle'          , colors = ['red'] , aim = 1 )	
		self.DampArmCoverASide  = rigModulePiston( n = self.Name.armCoverSideDampA , pos = armCoverSideDampALocs , ctrlVisPriority = 10 , form = 'circle'          , colors = ['red'] , aim = 1 )	
		self.DampArmCoverBSide  = rigModulePiston( n = self.Name.armCoverSideDampB , pos = armCoverSideDampBLocs , ctrlVisPriority = 10 , form = 'circle'          , colors = ['red'] , aim = 1 )	

		self.SubRigs           += [ self.ArmCover , self.Cover , self.InnerCover , self.PistonSlide , self.DampArmCoverA , self.DampArmCoverB , self.CoverNose , self.DampCoverNose ]
		self.SubRigsName       += [     'ArmCover',     'Cover',     'InnerCover',     'PistonSlide',     'DampArmCoverA',     'DampArmCoverB',     'CoverNose',     'DampCoverNose']
    

		self.PistonUpSide   = rigModulePiston( n = self.Name.pistonUp     , pos = pistonUpLocs       , ctrlVisPriority = 10 , form = 'circle'          , colors = ['red'] , aim = 1 )	
		self.PistonDownSide = rigModulePiston( n = self.Name.pistonDown   , pos = pistonDownLocs     , ctrlVisPriority = 10 , form = 'circle'          , colors = ['red'] , aim = 1 )
		self.Middle         = rigCtrl(         n = self.Name.middle       , pos = middleLocs         , ctrlVisPriority = 1 , form = 'arrow2sidesBend' , colors = ['red']  , parent = self.Name.topNode  , attrStates = [['rz']] )			
		self.SubRigs       += [ self.Middle ]
		self.SubRigsName   += [ 'Middle'    ]

		self.ArmOffset       = rigModuleChain(    n = self.Name.armOffset       , pos = armOffsetLocs      , ctrlVisPriority = 2 , form = 'arrow2sides' , colors = ['red'] , attrStates = [ ['t','r'] , ['rz'] ]	 ) 
		self.Arm             = rigModuleArm(      n = self.Name.arm             , pos = armLocs            , ctrlVisPriority = 1 , ik = True , fk = True , attrStates = [['rz']] ) 
		self.PistonArmOffset = rigModulePiston(   n = self.Name.pistonArmOffset , pos = pistonArmOffsetLocs, ctrlVisPriority = 10 , form = 'circle'          , colors = ['red'] , aim = 1 )
		self.GiroArm         = rigCtrl(           n = self.Name.giroArm         , pos = GiroArmLocs        , form = 'arrow2SidesBend' , colors = ['red'] , ctrlVisPriority = 6 , parent = self.Name.topNode , attrStates = [['rz']] )
		self.SubRigs           += [ self.ArmOffset , self.Arm , self.PistonArmOffset , self.GiroArm ] 
		self.SubRigsName       += [     'ArmOffset',     'Arm',     'PistonArmOffset',     'GiroArm'] 

		self.MiddleSpaceArm     = rigModuleArm(    n = self.Name.middleSpaceArm     , pos = middleSpaceArmLocs  , ctrlVisPriority = 10 , ik = True , trsv = False  )
		self.Holder             = rigModuleChain(  n = self.Name.holder             , pos = holderLocs          , ctrlVisPriority = 1 , form = 'arrow2sidesBend' , colors = ['yellow'] , attrStates = [ ['rz'], ['tx'] , ['rz'] ] )
		self.HolderSide         = rigModuleChain(  n = self.Name.holderSide         , pos = holderSideLocs      , ctrlVisPriority = 2 , form = 'arrow2sidesBend' , colors = ['yellow']  , attrStates = [['rz']] )
		self.Holder1SpacePiston = rigModulePiston( n = self.Name.holder1SpacePiston , pos = holder1SpacePistonLocs , ctrlVisPriority = 10 , form = 'circle'          , colors = ['red'] , aim = 1  , attrStates = [['']] )
		self.Holder3SpacePiston = rigModulePiston( n = self.Name.holder3SpacePiston , pos = holder3SpacePistonLocs , ctrlVisPriority = 10 , form = 'circle'          , colors = ['red'] , aim = 1  , attrStates = [['']] )
		self.GiroCover         = rigCtrl(         n = self.Name.giroCover         , pos = giroCoverLocs         , form = 'arrow2SidesBend' , colors = ['red'] , ctrlVisPriority = 6 , parent = self.Name.topNode , attrStates = [['rz']] )
		self.SubRigs           += [ self.MiddleSpaceArm , self.Holder  , self.Holder1SpacePiston  , self.Holder3SpacePiston  , self.GiroCover ]
		self.SubRigsName       += [     'MiddleSpaceArm',     'Holder' ,     'Holder1SpacePiston' ,     'Holder3SpacePiston' ,     'GiroCover']
    
		self.PlugSlide    = rigCtrl(         n = self.Name.plugSlide      , pos = plugSlideLocs    , ctrlVisPriority = 1  , form = 'arrow2sides'     , colors = ['red']   , parent = self.Name.topNode , attrStates = [['tx']] )	
		self.Plug         = rigCtrl(         n = self.Name.plug           , pos = plugLocs         , ctrlVisPriority = 1  , form = 'crossArrow'      , colors = ['red']   , parent = self.Name.topNode , attrStates = [['r']] )	
		self.PlugDampA    = rigModulePiston( n = self.Name.plugDampA      , pos = plugDampALocs    , ctrlVisPriority = 10 , form = 'circle'          , colors = ['red']   , aim = 1  , attrStates = [['']] )
		self.PlugDampB    = rigModulePiston( n = self.Name.plugDampB      , pos = plugDampBLocs    , ctrlVisPriority = 10 , form = 'circle'          , colors = ['red']   , aim = 1  , attrStates = [['']] )
		self.PlugMiddle   = rigModuleChain(  n = self.Name.plugMiddle     , pos = plugMiddleLocs     , ctrlVisPriority = 1 , form = 'circle'          , colors = ['green']  , attrStates = [['rz']] )
		self.PlugGrabSide = rigModuleChain(  n = self.Name.plugGrab       , pos = plugGrabLocs       , ctrlVisPriority = 2 , form = 'arrow2sidesBend' , colors = ['green']  , attrStates = [['rz']] )
		self.SubRigs           += [ self.PlugSlide , self.Plug , self.PlugDampA , self.PlugDampB , self.PlugMiddle ]
		self.SubRigsName       += [     'PlugSlide',     'Plug',     'PlugDampA',     'PlugDampB',     'PlugMiddle']


		self.RotHolderSide      = rigCtrl( n = self.Name.rotHolder        , pos = rotHolderLocs      , ctrlVisPriority = 2 , form = 'arrow2sidesBend' , colors = ['red'] , parent = self.Name.topNode , attrStates = [['rz']] )	
		self.RotHolderDown      = rigCtrl( n = self.Name.rotHolderDown    , pos = rotHolderDownLocs  , ctrlVisPriority = 2 , form = 'arrow2sidesBend' , colors = ['red'] , parent = self.Name.topNode , attrStates = [['rz']] )	
		self.PressureHolderSide = rigCtrl( n = self.Name.pressureHolder   , pos = pressureHolderLocs , ctrlVisPriority = 2 , form = 'arrow2sides'     , colors = ['red'] , parent = self.Name.topNode , attrStates = [['tx']] )	
		self.SlideHolderSide    = rigCtrl( n = self.Name.slideHolder      , pos = slideHolderLocs    , ctrlVisPriority = 2 , form = 'arrow2sides'     , colors = ['red'] , parent = self.Name.topNode , attrStates = [['tx']] )	
		self.SubRigs           += [  self.RotHolderDown ]
		self.SubRigsName       += [  'RotHolderDown'    ]


		if( self.doTubes ):
			self.TubeCoverA          = rigModuleArm(    n = self.Name.tubeCoverA          , pos = tubeCoverALocs          , ik = True , pv = True , ctrlVisPriority = 8 ,  attrStates = [['']] )
			self.TubeCoverHangA      = rigCtrl(         n = self.Name.tubeCoverHangA      , pos = tubeCoverHangALocs                              , ctrlVisPriority = 3 ,  attrStates = [['t','r']] , parent = self.Name.topNode)
			self.TubeCoverStraightA  = rigModulePiston( n = self.Name.tubeCoverStraightA  , pos = tubeCoverStraightALocs                          , ctrlVisPriority = 8 ,  attrStates = [['']] )
			self.TubeCoverB          = rigModuleArm(    n = self.Name.tubeCoverB          , pos = tubeCoverBLocs          , ik = True , pv = True , ctrlVisPriority = 8 ,  attrStates = [['']] )
			self.TubeCoverHangB      = rigCtrl(         n = self.Name.tubeCoverHangB      , pos = tubeCoverHangBLocs                              , ctrlVisPriority = 3 ,  attrStates = [['t','r']] , parent = self.Name.topNode)		
			self.TubeCoverStraightB  = rigModulePiston( n = self.Name.tubeCoverStraightB  , pos = tubeCoverStraightBLocs                          , ctrlVisPriority = 8 ,  attrStates = [['']] )
	
			self.TubeArmBack         = rigModuleArm(    n = self.Name.tubeArmBack         , pos = tubeArmBackLocs         , ik = True , pv = True , ctrlVisPriority = 8 ,  attrStates = [['']] )
			self.TubeArmBackHang     = rigCtrl(         n = self.Name.tubeArmBackHang     , pos = tubeArmBackHangLocs                             , ctrlVisPriority = 3 ,  attrStates = [['t','r']] , parent = self.Name.topNode)
			self.TubeArmBackStraight = rigModulePiston( n = self.Name.tubeArmBackStraight , pos = tubeArmBackStraightLocs                         , ctrlVisPriority = 8 ,  attrStates = [['']] )
	
			self.TubeMiddleA         = rigModuleArm(    n = self.Name.tubeMiddleA         , pos = tubeMiddleALocs         , ik = True , pv = True , ctrlVisPriority = 8 ,  attrStates = [['']] )				
			self.TubeMiddleHangA     = rigCtrl(         n = self.Name.tubeMiddleHangA     , pos = tubeMiddleHangALocs                             , ctrlVisPriority = 3 ,  attrStates = [['t','r']] , parent = self.Name.topNode)
			self.TubeMiddleStraightA = rigModulePiston( n = self.Name.tubeMiddleStraightA , pos = tubeMiddleStraightALocs                         , ctrlVisPriority = 8 ,  attrStates = [['']] )
			self.TubeMiddleB         = rigModuleArm(    n = self.Name.tubeMiddleB         , pos = tubeMiddleBLocs         , ik = True , pv = True , ctrlVisPriority = 8 ,  attrStates = [['']] )
			self.TubeMiddleHangB     = rigCtrl(         n = self.Name.tubeMiddleHangB     , pos = tubeMiddleHangBLocs                             , ctrlVisPriority = 3 ,  attrStates = [['t','r']] , parent = self.Name.topNode)
			self.TubeMiddleStraightB = rigModulePiston( n = self.Name.tubeMiddleStraightB , pos = tubeMiddleStraightBLocs                         , ctrlVisPriority = 8 , attrStates = [['']] )
	
			self.TubeArmA           = rigModuleArm(     n = self.Name.tubeArmA             , pos = tubeArmALocs           , ik = True , pv = True , ctrlVisPriority = 8 ,  attrStates = [['']] )
			self.TubeArmHangA       = rigCtrl(          n = self.Name.tubeArmHangA         , pos = tubeArmHangALocs                               , ctrlVisPriority = 3 ,  attrStates = [['t','r']] , parent = self.Name.topNode)
			self.TubeArmStraightA   = rigModulePiston(  n = self.Name.tubeArmStraightA     , pos = tubeArmStraightALocs                           , ctrlVisPriority = 8 ,  attrStates = [['']] )
			self.TubeArmB           = rigModuleArm(     n = self.Name.tubeArmB             , pos = tubeArmBLocs           , ik = True , pv = True , ctrlVisPriority = 8 ,  attrStates = [['']] )
			self.TubeArmHangB       = rigCtrl(          n = self.Name.tubeArmHangB         , pos = tubeArmHangBLocs                               , ctrlVisPriority = 3 ,  attrStates = [['t','r']] , parent = self.Name.topNode)
			self.TubeArmStraightB   = rigModulePiston(  n = self.Name.tubeArmStraightB     , pos = tubeArmStraightBLocs                           , ctrlVisPriority = 8 ,  attrStates = [['']] )
	
			self.TubeArmSmall       = rigModuleArm(     n = self.Name.tubeArmSmall         , pos = tubeArmSmallLocs       , ik = True , pv = True , ctrlVisPriority = 8 ,  attrStates = [['']] )
			self.TubeArmSmallSide   = rigModuleArm(     n = self.Name.tubeArmSideSmall     , pos = tubeArmSideSmallLocs   , ik = True , pv = True , ctrlVisPriority = 8 ,  attrStates = [['']] )
	
			self.TubePlugSmall      = rigModuleArm(     n = self.Name.tubePlugSmall        , pos = tubePlugSmallLocs      , ik = True , pv = True , ctrlVisPriority = 8 ,  attrStates = [['']] )
			self.TubePlugSmallSide  = rigModuleArm(     n = self.Name.tubePlugSideSmall    , pos = tubePlugSideSmallLocs  , ik = True , pv = True , ctrlVisPriority = 8 ,  attrStates = [['']] )
	
			self.SubRigs     += [ self.TubeCoverA , self.TubeCoverHangA , self.TubeCoverStraightA , self.TubeCoverB , self.TubeCoverHangB , self.TubeCoverStraightB ]
			self.SubRigsName += [     'TubeCoverA',     'TubeCoverHangA',     'TubeCoverStraightA',     'TubeCoverB',     'TubeCoverHangB',     'TubeCoverStraightB']
				
			self.SubRigs     += [ self.TubeArmBack , self.TubeArmBackHang , self.TubeArmBackStraight ]
			self.SubRigsName += [     'TubeArmBack',     'TubeArmBackHang',     'TubeArmBackStraight']
	
			self.SubRigs     += [ self.TubeMiddleA , self.TubeMiddleHangA , self.TubeMiddleStraightA , self.TubeMiddleB , self.TubeMiddleHangB , self.TubeMiddleStraightB ]
			self.SubRigsName += [     'TubeMiddleA',     'TubeMiddleHangA',     'TubeMiddleStraightA',     'TubeMiddleB',     'TubeMiddleHangB',     'TubeMiddleStraightB']
	
			self.SubRigs     += [ self.TubeArmA , self.TubeArmHangA , self.TubeArmStraightA , self.TubeArmB , self.TubeArmHangB , self.TubeArmStraightB ]
			self.SubRigsName += [     'TubeArmA',     'TubeArmHangA',     'TubeArmStraightA',     'TubeArmB',     'TubeArmHangB',     'TubeArmStraightB']
	
			self.SubRigs     += [ self.TubeArmSmall , self.TubePlugSmall ]
			self.SubRigsName += [     'TubeArmSmall'    , 'TubePlugSmall']


		#CLASSE BLUE PRINT - MIRROR
		args = {}
		args['value']             = mirrorPlane
		args['mode']              = 'mirror'
		args['pivot']             = [0,0,0 , 0,0,0 , 1,1,1]
		args['namePrefix']        = ['','']
		args['nameReplace']       = ['','']
		args['nameIncr']          = ''
		args['nameAdd']           = [ 'Left' , 'Right' ]
		args['noneMirrorAxe']     = 4
		args['debug']             = self.debug


		rigsToDuplicate = []
		rigsToDuplicate.append( self.ArmCoverSide      )
		rigsToDuplicate.append( self.DampArmCoverASide )
		rigsToDuplicate.append( self.DampArmCoverBSide )
		rigsToDuplicate.append( self.PistonUpSide      )
		rigsToDuplicate.append( self.PistonDownSide    )
		rigsToDuplicate.append( self.HolderSide        )
		rigsToDuplicate.append( self.PlugGrabSide      )
		rigsToDuplicate.append( self.RotHolderSide     )
		rigsToDuplicate.append( self.PressureHolderSide)
		rigsToDuplicate.append( self.SlideHolderSide   )
		rigsToDuplicate.append( self.TubeArmSmallSide  )
		rigsToDuplicate.append( self.TubePlugSmallSide )			


		duplicated = self.duplicateRigs( args , rigsToDuplicate )

		self.ArmCoverL       , self.ArmCoverR       = duplicated[0][0]  , duplicated[0][1]
		self.DampArmCoverAL  , self.DampArmCoverAR  = duplicated[1][0]  , duplicated[1][1]
		self.DampArmCoverBL  , self.DampArmCoverBR  = duplicated[2][0]  , duplicated[2][1]
		self.PistonUpL       , self.PistonUpR       = duplicated[3][0]  , duplicated[3][1]
		self.PistonDownL     , self.PistonDownR     = duplicated[4][0]  , duplicated[4][1]
		self.HolderL         , self.HolderR         = duplicated[5][0]  , duplicated[5][1]
		self.PlugGrabL       , self.PlugGrabR       = duplicated[6][0]  , duplicated[6][1]
		self.RotHolderL      , self.RotHolderR      = duplicated[7][0]  , duplicated[7][1]	
		self.PressureHolderL , self.PressureHolderR = duplicated[8][0]  , duplicated[8][1]		
		self.SlideHolderL    , self.SlideHolderR    = duplicated[9][0]  , duplicated[9][1]
		self.TubeArmSmallL   , self.TubeArmSmallR   = duplicated[10][0] , duplicated[10][1]		
		self.TubePlugSmallL  , self.TubePlugSmallR  = duplicated[11][0] , duplicated[11][1]

		self.SubRigs     += [ self.ArmCoverL       , self.ArmCoverR       ]
		self.SubRigs     += [ self.DampArmCoverAL  , self.DampArmCoverAR  ]
		self.SubRigs     += [ self.DampArmCoverBL  , self.DampArmCoverBR  ]
		self.SubRigs     += [ self.PistonUpL       , self.PistonUpR       ]
		self.SubRigs     += [ self.PistonDownL     , self.PistonDownR     ]
		self.SubRigs     += [ self.HolderL         , self.HolderR         ]
		self.SubRigs     += [ self.PlugGrabL       , self.PlugGrabR       ]
		self.SubRigs     += [ self.RotHolderL      , self.RotHolderR      ]
		self.SubRigs     += [ self.PressureHolderL , self.PressureHolderR ]
		self.SubRigs     += [ self.SlideHolderL    , self.SlideHolderR    ]
		self.SubRigs     += [ self.TubeArmSmallL   , self.TubeArmSmallR   ]
		self.SubRigs     += [ self.TubePlugSmallL  , self.TubePlugSmallR  ]

		self.SubRigsName += [ 'ArmCoverL'       , 'ArmCoverR'       ]
		self.SubRigsName += [ 'DampArmCoverAL'  , 'DampArmCoverAR'  ]
		self.SubRigsName += [ 'DampArmCoverBL'  , 'DampArmCoverBR'  ]
		self.SubRigsName += [ 'PistonUpL'       , 'PistonUpR'       ]
		self.SubRigsName += [ 'PistonDownL'     , 'PistonDownR'     ]
		self.SubRigsName += [ 'HookHolderL'     , 'HookHolderR'     ]
		self.SubRigsName += [ 'PlugGrabL'       , 'PlugGrabR'       ]
		self.SubRigsName += [ 'RotHolderL'      , 'RotHolderR'      ]
		self.SubRigsName += [ 'PressureHolderL' , 'PressureHolderR' ]
		self.SubRigsName += [ 'SlideHolderL'    , 'SlideHolderR'    ]
		self.SubRigsName += [ 'TubeArmSmallL'   , 'TubeArmSmallR'   ]
		self.SubRigsName += [ 'TubePlugSmallL'  , 'TubePlugSmallR'  ]		


		if( self.doTubes ):
			self.Attr.add( 'TubeCoverHangA'  , Name = self.TubeCoverHangA.Name.ctrl  , attrName = ['straighten'] , attrType = ['floatOnOff'] , attrValue = [0] , attrKeyable = [True] )
			self.Attr.add( 'TubeCoverHangB'  , Name = self.TubeCoverHangB.Name.ctrl  , attrName = ['straighten'] , attrType = ['floatOnOff'] , attrValue = [0] , attrKeyable = [True] )
			self.Attr.add( 'TubeArmBackHang' , Name = self.TubeArmBackHang.Name.ctrl , attrName = ['straighten'] , attrType = ['floatOnOff'] , attrValue = [0] , attrKeyable = [True] )
			self.Attr.add( 'TubeMiddleHangA' , Name = self.TubeMiddleHangA.Name.ctrl , attrName = ['straighten'] , attrType = ['floatOnOff'] , attrValue = [0] , attrKeyable = [True] )
			self.Attr.add( 'TubeMiddleHangB' , Name = self.TubeMiddleHangB.Name.ctrl , attrName = ['straighten'] , attrType = ['floatOnOff'] , attrValue = [0] , attrKeyable = [True] )
			self.Attr.add( 'TubeArmHangA'    , Name = self.TubeArmHangA.Name.ctrl    , attrName = ['straighten'] , attrType = ['floatOnOff'] , attrValue = [0] , attrKeyable = [True] )
			self.Attr.add( 'TubeArmHangB'    , Name = self.TubeArmHangB.Name.ctrl    , attrName = ['straighten'] , attrType = ['floatOnOff'] , attrValue = [0] , attrKeyable = [True] )


		self.Attr.add( "GiroArm"    , Name = self.GiroArm.Name.ctrl    , attrName = ["lightVisibility"] , attrType = ["intOnOff"] , attrValue = [1] )
		self.Attr.add( "GiroCover" , Name = self.GiroCover.Name.ctrl , attrName = ["lightVisibility"] , attrType = ["intOnOff"] , attrValue = [1] )

		self.Link.add( 'paArmCover'          , Sources = [ self.RootB.outs[0]              ] , Destinations = [ self.ArmCover.ins[1]    , self.ArmCoverL.ins[1]   , self.ArmCoverR.ins[1]          ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 , clear = True )	
		self.Link.add( 'paMiddle'            , Sources = [ self.Middle.outs[0]             ] , Destinations = [ self.PistonUpL.ins[1]   , self.PistonUpR.ins[1]                                    ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )
		self.Link.add( 'paPistonsDown'       , Sources = [ self.PlugMiddle.outs[1]         ] , Destinations = [ self.PistonDownL.ins[1] , self.PistonDownR.ins[1] , self.Holder3SpacePiston.ins[1] ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )
		self.Link.add( 'middleSpaceArm'      , Sources = [ self.PlugSlide.outs[0]          ] , Destinations = [ self.MiddleSpaceArm.ins[1]                                                         ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )
		self.Link.add( 'Holder1SpacePiston1' , Sources = [ self.Holder3SpacePiston.outs[0] ] , Destinations = [ self.Holder1SpacePiston.ins[1]                                                     ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )
		self.Link.add( 'plugDamp'            , Sources = [ self.Plug.outs[0]               ] , Destinations = [ self.PlugDampA.ins[1] , self.PlugDampB.ins[1]                                      ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )
		self.Link.add( 'PistonArmOffset'     , Sources = [ self.Arm.outs[0]                ] , Destinations = [ self.PistonArmOffset.ins[1]                                                        ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )

		self.Link.add( 'CoverNose'           , Sources = [ self.RootB.outs[0]              ] , Destinations = [ self.CoverNose.ins[1]                                       ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )
		self.Link.add( 'DampArmCoverA'       , Sources = [ self.ArmCover.outs[1]           ] , Destinations = [ self.DampArmCoverA.ins[1]                                   ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )
		self.Link.add( 'DampArmCoverB'       , Sources = [ self.ArmCover.outs[0]           ] , Destinations = [ self.DampArmCoverB.ins[1]	                                ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )
		self.Link.add( 'DampArmCoverAL'      , Sources = [ self.ArmCoverL.outs[1]          ] , Destinations = [ self.DampArmCoverAL.ins[1]                                  ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )
		self.Link.add( 'DampArmCoverBL'      , Sources = [ self.ArmCoverL.outs[0]          ] , Destinations = [ self.DampArmCoverBL.ins[1]                                  ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )		
		self.Link.add( 'DampArmCoverAR'      , Sources = [ self.ArmCoverR.outs[1]          ] , Destinations = [ self.DampArmCoverAR.ins[1]                                  ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )
		self.Link.add( 'DampArmCoverBR'      , Sources = [ self.ArmCoverR.outs[0]          ] , Destinations = [ self.DampArmCoverBR.ins[1]	                                ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )


		if( self.doTubes ):
			self.Link.add( 'tubeInnerCover'    , Sources = [ self.InnerCover.outs[0]     ] , Destinations = [ self.TubeCoverA.ins[0]   , self.TubeCoverStraightA.ins[0]  , self.TubeCoverB.ins[0]         , self.TubeCoverStraightB.ins[0] ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )				
			self.Link.add( 'tubeArm1A'         , Sources = [ self.Arm.outs[0]            ] , Destinations = [ self.TubeCoverA.ins[1]   , self.TubeCoverStraightA.ins[1]  , self.TubeCoverB.ins[1]         , self.TubeCoverStraightB.ins[1] ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )	
			self.Link.add( 'tubeArm1B'         , Sources = [ self.Arm.outs[1]            ] , Destinations = [ self.TubeArmSmall.ins[1] , self.TubeArmSmallL.ins[1]       , self.TubeArmSmallR.ins[1]                                       ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )			  
			self.Link.add( 'tubeArm1C'         , Sources = [ self.Arm.outs[1]            ] , Destinations = [ self.TubeArmBack.ins[1]  , self.TubeArmBackStraight.ins[1]                                                                   ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )	
			self.Link.add( 'tubeHolder1'       , Sources = [ self.Holder.outs[1]         ] , Destinations = [ self.TubeMiddleB.ins[1]  , self.TubeMiddleStraightB.ins[1]                                                                   ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )	
			self.Link.add( 'tubeMiddle'        , Sources = [ self.Middle.outs[0]         ] , Destinations = [ self.TubeMiddleA.ins[1]  , self.TubeMiddleStraightA.ins[1]                                                                   ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )	
			self.Link.add( 'tubePlugSlide'     , Sources = [ self.PlugSlide.outs[0]      ] , Destinations = [ self.TubeArmA.ins[1]     , self.TubeArmStraightA.ins[1]    , self.TubeArmB.ins[1]           , self.TubeArmStraightB.ins[1]   ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )	
			self.Link.add( 'tubeRotHolderDown' , Sources = [ self.RotHolderDown.outs[0]  ] , Destinations = [ self.TubePlugSmall.ins[1]   ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )	
			self.Link.add( 'tubeRotHolderL'    , Sources = [ self.RotHolderL.outs[0]     ] , Destinations = [ self.TubePlugSmallL.ins[1]  ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )	
			self.Link.add( 'tubeRotHolderR'    , Sources = [ self.RotHolderR.outs[0]     ] , Destinations = [ self.TubePlugSmallR.ins[1]  ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )	
	
			self.Link.add( 'TubeCoverHangA'    , Sources = [ self.TubeCoverA.outs[0]     ] , Destinations = [ self.TubeCoverHangA.ins[0]  ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 , skipAxes = [0,0,0,1,1,1,0,0,0] )	
			self.Link.add( 'TubeCoverHangB'    , Sources = [ self.TubeCoverB.outs[0]     ] , Destinations = [ self.TubeCoverHangB.ins[0]  ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 , skipAxes = [0,0,0,1,1,1,0,0,0] )	
			self.Link.add( 'TubeArmBackHang'   , Sources = [ self.TubeArmBack.outs[0]    ] , Destinations = [ self.TubeArmBackHang.ins[0] ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 , skipAxes = [0,0,0,1,1,1,0,0,0] )	
			self.Link.add( 'TubeMiddleHangA'   , Sources = [ self.TubeMiddleStraightA.outs[0] ] , Destinations = [ self.TubeMiddleHangA.ins[0] ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 , skipAxes = [0,0,0,1,1,1,0,0,0] )	
			self.Link.add( 'TubeMiddleHangB'   , Sources = [ self.TubeMiddleB.outs[0]    ] , Destinations = [ self.TubeMiddleHangB.ins[0] ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 , skipAxes = [0,0,0,1,1,1,0,0,0] )	
			self.Link.add( 'TubeArmHangA'      , Sources = [ self.TubeArmA.outs[0]       ] , Destinations = [ self.TubeArmHangA.ins[0]    ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 , skipAxes = [0,0,0,1,1,1,0,0,0] )	
			self.Link.add( 'TubeArmHangB'      , Sources = [ self.TubeArmB.outs[0]       ] , Destinations = [ self.TubeArmHangB.ins[0]    ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 , skipAxes = [0,0,0,1,1,1,0,0,0] )	


		self.Link.add( 'paSpaceArmOffset' , Sources = [ self.Cover.outs[0]                                   ] , Destinations = [ self.ArmOffset.ins[0] ] , type = 'parentSpace'  , spaceDriver = self.ArmOffset.Ctrl0.Name.ctrl , spaceAttr = 'parentSpace' , spaceNames = ['cover'] )	
		self.Link.add( 'paSpaceMiddle'    , Sources = [ self.MiddleSpaceArm.outs[0]     , self.Cover.outs[0] ] , Destinations = [ self.Middle.ins[0]    ] , type = 'parentSpace'  , spaceDriver = self.Middle.Name.ctrl          , spaceAttr = 'parentSpace' , spaceNames = ['arm','cover'] )	
		self.Link.add( 'paSpaceHolder0'   , Sources = [ self.Holder1SpacePiston.outs[0] , self.RootB.outs[0] ] , Destinations = [ self.Holder.ins[0]    ] , type = 'orientSpace'  , spaceDriver = self.Holder.Ctrl0.Name.ctrl    , spaceAttr = 'parentSpace' , spaceNames = ['middle','root'] )	
		self.Link.add( 'paSpaceHolder1'   , Sources = [ self.Holder1SpacePiston.outs[1]                      ] , Destinations = [ self.Holder.ins[1]    ] , type = 'parentSpace'  , spaceDriver = self.Holder.Ctrl1.Name.ctrl    , spaceAttr = 'parentSpace' , spaceNames = ['middle'] )
		self.Link.add( 'paSpaceHolder3'   , Sources = [ self.Holder3SpacePiston.outs[0]                      ] , Destinations = [ self.Holder.ins[2]    ] , type = 'parentSpace'  , spaceDriver = self.Holder.Ctrl2.Name.ctrl    , spaceAttr = 'parentSpace' , spaceNames = ['middle'] )


		#CLASSE UTILS
		#CLASSE UTILS
		self.ins   = [ self.RootB.ins[0] , self.Arm.ins[1]  , self.Arm.ins[0] ]
		self.outs  = []			
		#CLASSE MODIF
		#INSTANCE MODIF
		name = args.get( 'n'   , None )	
		pos  = args.get( 'pos' , None )
		if not( name == None ): self.Name.add( 'base' , copy = name ) 
		if not( pos  == None ): pass

		'''											
		if not( shape  == None ): self.CurveShape.add(  'ctrl'    , shape                 )
		if not( form   == None ): self.CurveShape.add(  'ctrl'    , { 'form'   : form   } )
		if not( colors == None ): self.CurveShape.add(  'ctrl'    , { 'colors' : colors } )	
		'''

