
	
'''
#******************************************************** BUILD EXEMPLE 
import maya.cmds as mc

import python
from    python.projects.cute.assets.carrierShipD.rigSkeletonCarrierShip_hook import *
reload( python.projects.cute.assets.carrierShipD.rigSkeletonCarrierShip_hook)
mc.file( 'D:/mcantat_BDD/projects/cute/assets/carrierShipD/maya/scenes/carrierShipD_rigBase5.ma' , o = True , f = True  )
#=================================================
puppet = rigSkeletonCarrierShip_hook( tubes = False )
puppet.printBuild = 1
toExec = puppet.build()
exec(toExec)

'''

import maya.cmds as mc

from .....classe.rigPuppet import *  
from .....classe.rigSkeletonChain import *     


       
class rigSkeletonCarrierShip_hook(rigPuppet):

	def __init__( self , **args ):
		rigPuppet.__init__( self , **args )
		#CLASSE TYPE
		self.classeType = 'rigSkeletonHook'
		self.doTubes = args.get( 'tubes' , None )
		#CLASSE BLUE PRINT - POS
		rootBLocs              = [x.encode('UTF8') for x in mc.ls('pos_hookRoot?'         , type = 'transform' )]
		
		armCoverLocs           = [x.encode('UTF8') for x in mc.ls('pos_armCover?'         , type = 'transform' )]		
		armCoverSideLocs       = [x.encode('UTF8') for x in mc.ls('pos_armCoverSide?'     , type = 'transform' )]

		armCoverDampALocs      = [x.encode('UTF8') for x in mc.ls('pos_hookCoverArmDampA?'     , type = 'transform' )]
		armCoverDampBLocs      = [x.encode('UTF8') for x in mc.ls('pos_hookCoverArmDampB?'     , type = 'transform' )]
		armCoverSideDampALocs  = [x.encode('UTF8') for x in mc.ls('pos_hookCoverArmSideDampA?' , type = 'transform' )]
		armCoverSideDampBLocs  = [x.encode('UTF8') for x in mc.ls('pos_hookCoverArmSideDampB?' , type = 'transform' )]

		coverNoseLocs          = [x.encode('UTF8') for x in mc.ls('pos_hookCoverNose?'    , type = 'transform' )]
		coverNoseDampLocs      = [x.encode('UTF8') for x in mc.ls('pos_hookCoverNoseDamp?', type = 'transform' )]

		coverLocs              = [x.encode('UTF8') for x in mc.ls('pos_hookCover?'        , type = 'transform' )]
		innerCoverLocs         = [x.encode('UTF8') for x in mc.ls('pos_innerCover?'     , type = 'transform' )]
		pistonSlideLocs        = ['pos_pistonSlide1']

		pistonUpLocs           = [x.encode('UTF8') for x in mc.ls('pos_pistonUp?'         , type = 'transform' )]		
		pistonDownLocs         = [x.encode('UTF8') for x in mc.ls('pos_pistonDwn?'        , type = 'transform' )]	
		middleLocs             = ['pos_middle1']

		armOffsetLocs          = [x.encode('UTF8') for x in mc.ls('pos_hookArmOffset?'    , type = 'transform' )]
		armLocs                = [x.encode('UTF8') for x in mc.ls('pos_hookArm?'          , type = 'transform' )]
		pistonArmOffsetLocs    = [x.encode('UTF8') for x in mc.ls('pos_pistonArmOffset?'  , type = 'transform' )]


		middleSpaceArmLocs     = [x.encode('UTF8') for x in mc.ls('pos_middleSpaceArm?'     , type = 'transform' )]
		holderLocs             = [x.encode('UTF8') for x in mc.ls('pos_hookHolder?'         , type = 'transform' )]
		holderSideLocs         = [x.encode('UTF8') for x in mc.ls('pos_hookHolderSide?'     , type = 'transform' )]
		holder1SpacePistonLocs = [x.encode('UTF8') for x in mc.ls('pos_holder1SpacePiston?' , type = 'transform' )]
		holder3SpacePistonLocs = [x.encode('UTF8') for x in mc.ls('pos_holder3SpacePiston?' , type = 'transform' )]		


		plugSlideLocs          = ['pos_plugSlide1']
		plugLocs               = ['pos_plug1'     ]
		plugDampALocs          = [x.encode('UTF8') for x in mc.ls('pos_plugDampA?'       , type = 'transform' )]	
		plugDampBLocs          = [x.encode('UTF8') for x in mc.ls('pos_plugDampB?'       , type = 'transform' )]	
		plugMiddleLocs         = [x.encode('UTF8') for x in mc.ls('pos_plugHook?'        , type = 'transform' )]	
		plugGrabLocs           = [x.encode('UTF8') for x in mc.ls('pos_plugSideHook?'    , type = 'transform' )]

		rotHolderLocs          = ['pos_rotHolderR1']
		rotHolderDownLocs      = ['pos_rotHolderD1']
		pressureHolderLocs     = ['pos_pressureHolderR1']
		slideHolderLocs        = ['pos_slideHolderR1']	

		plugGrabLocs           = [x.encode('UTF8') for x in mc.ls('pos_plugSideHook?'      , type = 'transform' )]
		giroCoverLocs         = [ 'pos_hookGiro1' ] 
		GiroArmLocs            = [ 'pos_hookGiro2' ] 

		tubeCoverALocs            = [x.encode('UTF8') for x in mc.ls('pos_hookCoverTubeA?'          , type = 'transform' )]
		tubeCoverHangALocs        = [x.encode('UTF8') for x in mc.ls('pos_hookCoverTubeHangA?'      , type = 'transform' )]
		tubeCoverStraightALocs    = [x.encode('UTF8') for x in mc.ls('pos_hookCoverTubeStraightA?'  , type = 'transform' )]
		tubeCoverBLocs            = [x.encode('UTF8') for x in mc.ls('pos_hookCoverTubeB?'          , type = 'transform' )]
		tubeCoverHangBLocs        = [x.encode('UTF8') for x in mc.ls('pos_hookCoverTubeHangB?'      , type = 'transform' )]
		tubeCoverStraightBLocs    = [x.encode('UTF8') for x in mc.ls('pos_hookCoverTubeStraightB?'  , type = 'transform' )]

		tubeArmBackLocs           = [x.encode('UTF8') for x in mc.ls('pos_hookArmTubeBack?'         , type = 'transform' )]
		tubeArmBackHangLocs       = [x.encode('UTF8') for x in mc.ls('pos_hookArmTubeBackHang?'     , type = 'transform' )]
		tubeArmBackStraightLocs   = [x.encode('UTF8') for x in mc.ls('pos_hookArmTubeBackStraight?' , type = 'transform' )]

		tubeMiddleALocs           = [x.encode('UTF8') for x in mc.ls('pos_hookMiddleTubeA?'         , type = 'transform' )]
		tubeMiddleHangALocs       = [x.encode('UTF8') for x in mc.ls('pos_hookMiddleTubeHangA?'     , type = 'transform' )]		
		tubeMiddleStraightALocs   = [x.encode('UTF8') for x in mc.ls('pos_hookMiddleTubeStraightA?' , type = 'transform' )]		
		tubeMiddleBLocs           = [x.encode('UTF8') for x in mc.ls('pos_hookMiddleTubeB?'         , type = 'transform' )]
		tubeMiddleHangBLocs       = [x.encode('UTF8') for x in mc.ls('pos_hookMiddleTubeHangB?'     , type = 'transform' )]
		tubeMiddleStraightBLocs   = [x.encode('UTF8') for x in mc.ls('pos_hookMiddleTubeStraightB?' , type = 'transform' )]

		tubeArmALocs              = [x.encode('UTF8') for x in mc.ls('pos_hookArmTubeA?'            , type = 'transform' )]
		tubeArmHangALocs          = [x.encode('UTF8') for x in mc.ls('pos_hookArmTubeHangA?'        , type = 'transform' )]
		tubeArmStraightALocs      = [x.encode('UTF8') for x in mc.ls('pos_hookArmTubeStraightA?'    , type = 'transform' )]
		tubeArmBLocs              = [x.encode('UTF8') for x in mc.ls('pos_hookArmTubeB?'            , type = 'transform' )]	
		tubeArmHangBLocs          = [x.encode('UTF8') for x in mc.ls('pos_hookArmTubeHangB?'        , type = 'transform' )]	
		tubeArmStraightBLocs      = [x.encode('UTF8') for x in mc.ls('pos_hookArmTubeStraightB?'    , type = 'transform' )]		
		
		tubeArmSmallLocs          = [x.encode('UTF8') for x in mc.ls('pos_hookArmTubeSmall?'        , type = 'transform' )]		
		tubeArmSideSmallLocs      = [x.encode('UTF8') for x in mc.ls('pos_hookArmTubeSideSmall?'    , type = 'transform' )]

		tubePlugSmallLocs         = [x.encode('UTF8') for x in mc.ls('pos_hookPlugTubeSmall?'       , type = 'transform' )]		
		tubePlugSideSmallLocs     = [x.encode('UTF8') for x in mc.ls('pos_hookPlugTubeSmallSide?'   , type = 'transform' )]


		mirrorPlane            = 'symPlane_hook1'		
		#CLASSE BLUE PRINT
		self.Name.add( 'base'             , baseName = 'hook' )

		self.Name.add( 'root'             , ref = self.Name.base , baseNameAppend = 'root'          )
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
		self.Name.add( 'arm'              , ref = self.Name.base , baseNameAppend = 'arm'            )
		self.Name.add( 'pistonArmOffset'  , ref = self.Name.base , baseNameAppend = 'pistonArmOffset')
		
		self.Name.add( 'middleSpaceArm'   , ref = self.Name.base , baseNameAppend = 'middleSpaceArm'           )
		self.Name.add( 'holder'           , ref = self.Name.base , baseNameAppend = 'holder'        )
		self.Name.add( 'holderSide'       , ref = self.Name.base , baseNameAppend = 'holder'        )
		self.Name.add( 'holder1SpacePiston', ref = self.Name.base , baseNameAppend = 'holder1SpacePiston'   )
		self.Name.add( 'holder3SpacePiston', ref = self.Name.base , baseNameAppend = 'holder3SpacePiston'   )

		self.Name.add( 'plugSlide'        , ref = self.Name.base , baseNameAppend = 'plugSlide'        )
		self.Name.add( 'plug'             , ref = self.Name.base , baseNameAppend = 'plug'             )
		self.Name.add( 'plugDampA'        , ref = self.Name.base , baseNameAppend = 'plugDampA'        )
		self.Name.add( 'plugDampB'        , ref = self.Name.base , baseNameAppend = 'plugDampB'        )
		self.Name.add( 'plugMiddle'       , ref = self.Name.base , baseNameAppend = 'plugMiddle'       )
		self.Name.add( 'plugGrab'         , ref = self.Name.base , baseNameAppend = 'plugGrab'         )	

		self.Name.add( 'rotHolder'        , ref = self.Name.base , baseNameAppend = 'rotHolder'        )
		self.Name.add( 'rotHolderDown'    , ref = self.Name.base , baseNameAppend = 'rotHolderDown'        )
		self.Name.add( 'pressureHolder'   , ref = self.Name.base , baseNameAppend = 'pressureHolder'        )
		self.Name.add( 'slideHolder'      , ref = self.Name.base , baseNameAppend = 'slideHolder'        )

		self.Name.add( 'giroCover'        , ref = self.Name.base , baseNameAppend = 'giroCover'        )
		self.Name.add( 'giroArm'          , ref = self.Name.base , baseNameAppend = 'giroArm'           )

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
		parent  = args.get( 'parent' , self.Name.topNode  )

		self.RootB              = rigSkeletonChain( n = self.Name.rootB          , pos = rootBLocs , parent = parent ) 
		self.SubRigs           += [ self.RootB ]
		self.SubRigsName       += [ 'RootB'    ]
    
		self.Cover              = rigSkeletonChain( n = self.Name.cover          , pos = coverLocs        , parent = self.RootB.outs[-1] )
		self.InnerCover         = rigSkeletonChain( n = self.Name.innerCover     , pos = innerCoverLocs   , parent = self.Cover.outs[-1] )		
		self.PistonSlide        = rigSkeletonChain( n = self.Name.pistonSlide    , pos = pistonSlideLocs  , parent = self.Cover.outs[-1] )
		self.ArmCover           = rigSkeletonChain( n = self.Name.armCover       , pos = armCoverLocs     , parent = self.Cover.outs[-1] )
		self.ArmCoverSide       = rigSkeletonChain( n = self.Name.armCoverSide   , pos = armCoverSideLocs , parent = self.Cover.outs[-1] )					
		
		self.CoverNose          = rigSkeletonChain( n = self.Name.coverNose         , pos = coverNoseLocs     , parent = self.Cover.outs[-1] )
		self.DampCoverNose      = rigSkeletonChain( n = self.Name.coverNoseDamp     , pos = coverNoseDampLocs , parent = self.Cover.outs[-1] )

		self.DampArmCoverA      = rigSkeletonChain( n = self.Name.armCoverDampA     , pos = armCoverDampALocs     , parent = self.RootB.outs[0] )
		self.DampArmCoverB      = rigSkeletonChain( n = self.Name.armCoverDampB     , pos = armCoverDampBLocs     , parent = self.CoverNose.outs[0] )
		self.DampArmCoverASide  = rigSkeletonChain( n = self.Name.armCoverSideDampA , pos = armCoverSideDampALocs , parent = self.RootB.outs[0] )
		self.DampArmCoverBSide  = rigSkeletonChain( n = self.Name.armCoverSideDampB , pos = armCoverSideDampBLocs , parent = self.Cover.outs[-1] )


		self.SubRigs           += [ self.ArmCover , self.Cover , self.InnerCover , self.PistonSlide , self.DampArmCoverA , self.DampArmCoverB , self.CoverNose , self.DampCoverNose ]
		self.SubRigsName       += [     'ArmCover',     'Cover',     'InnerCover',     'PistonSlide',     'DampArmCoverA',     'DampArmCoverB',     'CoverNose',     'DampCoverNose']
    
		self.PistonUpSide       = rigSkeletonChain( n = self.Name.pistonUp       , pos = pistonUpLocs     , parent = self.PistonSlide.outs[-1]  )
		self.Middle             = rigSkeletonChain( n = self.Name.middle         , pos = middleLocs       , parent = self.RootB.outs[-1]        )				
		self.SubRigs           += [ self.Middle ] 
		self.SubRigsName       += [     'Middle'] 
     
		self.ArmOffset          = rigSkeletonChain( n = self.Name.armOffset      , pos = armOffsetLocs      , parent = self.RootB.outs[-1]     )			
		self.Arm                = rigSkeletonChain( n = self.Name.arm            , pos = armLocs            , parent = self.ArmOffset.outs[-1] )
		self.PistonArmOffset    = rigSkeletonChain( n = self.Name.pistonArmOffset, pos = pistonArmOffsetLocs, parent = self.ArmOffset.outs[-1] )
		self.GiroArm            = rigSkeletonChain( n = self.Name.giroArm        , pos = GiroArmLocs        , parent = self.Arm.outs[1]        )		
		self.SubRigs           += [ self.ArmOffset , self.Arm , self.PistonArmOffset , self.GiroArm ] 
		self.SubRigsName       += [     'ArmOffset',     'Arm',     'PistonArmOffset',     'GiroArm'] 
     
		self.MiddleSpaceArm     = rigSkeletonChain( n = self.Name.middleSpaceArm     , pos = middleSpaceArmLocs     , parent = self.ArmOffset.outs[-1] )
		self.Holder             = rigSkeletonChain( n = self.Name.holder             , pos = holderLocs             , parent = self.Cover.outs[-1]     )	
		self.Holder1SpacePiston = rigSkeletonChain( n = self.Name.holder1SpacePiston , pos = holder1SpacePistonLocs , parent = self.Cover.outs[-1]     )					
		self.Holder3SpacePiston = rigSkeletonChain( n = self.Name.holder3SpacePiston , pos = holder3SpacePistonLocs , parent = self.Middle.outs[-1]    )					
		self.HolderSide         = rigSkeletonChain( n = self.Name.holderSide         , pos = holderSideLocs         , parent = self.Holder.outs[-1]    )
		self.PistonDownSide     = rigSkeletonChain( n = self.Name.pistonDown         , pos = pistonDownLocs         , parent = self.Holder.outs[-1]    )
		self.GiroCover          = rigSkeletonChain( n = self.Name.giroCover          , pos = giroCoverLocs          , parent = self.Cover.outs[-1]     )		
		self.SubRigs           += [ self.MiddleSpaceArm , self.Holder  , self.Holder1SpacePiston  , self.Holder3SpacePiston  , self.GiroCover ]
		self.SubRigsName       += [     'MiddleSpaceArm',     'Holder' ,     'Holder1SpacePiston' ,     'Holder3SpacePiston' ,     'GiroCover']
    
		self.PlugSlide          = rigSkeletonChain( n = self.Name.plugSlide      , pos = plugSlideLocs    , parent = self.Arm.outs[1]         ) 	
		self.Plug               = rigSkeletonChain( n = self.Name.plug           , pos = plugLocs         , parent = self.PlugSlide.outs[-1]  ) 
		self.PlugDampA          = rigSkeletonChain( n = self.Name.plugDampA      , pos = plugDampALocs    , parent = self.Arm.outs[1]         )	
		self.PlugDampB          = rigSkeletonChain( n = self.Name.plugDampB      , pos = plugDampBLocs    , parent = self.Arm.outs[1]         )	
		self.PlugMiddle         = rigSkeletonChain( n = self.Name.plugMiddle     , pos = plugMiddleLocs   , parent = self.Plug.outs[-1]       )
		self.PlugGrabSide       = rigSkeletonChain( n = self.Name.plugGrab       , pos = plugGrabLocs     , parent = self.PlugMiddle.outs[-1] )
		self.SubRigs           += [ self.PlugSlide , self.Plug , self.PlugDampA , self.PlugDampB , self.PlugMiddle ]
		self.SubRigsName       += [     'PlugSlide',     'Plug',     'PlugDampA',     'PlugDampB',     'PlugMiddle']

		self.RotHolderSide      = rigSkeletonChain( n = self.Name.rotHolder      , pos = rotHolderLocs      , parent = self.Plug.outs[-1]     )	
		self.RotHolderDown      = rigSkeletonChain( n = self.Name.rotHolderDown  , pos = rotHolderDownLocs  , parent = self.Plug.outs[-1]    )	
		self.PressureHolderSide = rigSkeletonChain( n = self.Name.pressureHolder , pos = pressureHolderLocs , parent = self.Plug.outs[-1]     )	
		self.SlideHolderSide    = rigSkeletonChain( n = self.Name.slideHolder    , pos = slideHolderLocs    , parent = self.Plug.outs[-1]     )	
		self.SubRigs           += [  self.RotHolderDown ]
		self.SubRigsName       += [  'RotHolderDown'    ]


		self.TubeCoverA          = rigSkeletonChain( n = self.Name.tubeCoverA          , pos = tubeCoverALocs           , parent = self.Cover.outs[-1]     )
		self.TubeCoverHangA      = rigSkeletonChain( n = self.Name.tubeCoverHangA      , pos = tubeCoverHangALocs       , parent = self.Cover.outs[-1]     )
		self.TubeCoverStraightA  = rigSkeletonChain( n = self.Name.tubeCoverStraightA  , pos = tubeCoverStraightALocs   , parent = self.Cover.outs[-1]     )
		self.TubeCoverB          = rigSkeletonChain( n = self.Name.tubeCoverB          , pos = tubeCoverBLocs           , parent = self.Cover.outs[-1]     )
		self.TubeCoverHangB      = rigSkeletonChain( n = self.Name.tubeCoverHangB      , pos = tubeCoverHangBLocs       , parent = self.Cover.outs[-1]     )
		self.TubeCoverStraightB  = rigSkeletonChain( n = self.Name.tubeCoverStraightB  , pos = tubeCoverStraightBLocs   , parent = self.Cover.outs[-1]     )

		self.TubeArmBack         = rigSkeletonChain( n = self.Name.tubeArmBack         , pos = tubeArmBackLocs          , parent = self.RootB.outs[-1]     )
		self.TubeArmBackHang     = rigSkeletonChain( n = self.Name.tubeArmBackHang     , pos = tubeArmBackHangLocs      , parent = self.RootB.outs[-1]     )
		self.TubeArmBackStraight = rigSkeletonChain( n = self.Name.tubeArmBackStraight , pos = tubeArmBackStraightLocs  , parent = self.RootB.outs[-1]     )

		self.TubeMiddleA         = rigSkeletonChain( n = self.Name.tubeMiddleA         , pos = tubeMiddleALocs          , parent = self.Holder.outs[2]     )				
		self.TubeMiddleHangA     = rigSkeletonChain( n = self.Name.tubeMiddleHangA     , pos = tubeMiddleHangALocs      , parent = self.Holder.outs[2]     )
		self.TubeMiddleStraightA = rigSkeletonChain( n = self.Name.tubeMiddleStraightA , pos = tubeMiddleStraightALocs  , parent = self.Holder.outs[2]     )
		self.TubeMiddleB         = rigSkeletonChain( n = self.Name.tubeMiddleB         , pos = tubeMiddleBLocs          , parent = self.Middle.outs[-1]    )
		self.TubeMiddleHangB     = rigSkeletonChain( n = self.Name.tubeMiddleHangB     , pos = tubeMiddleHangBLocs      , parent = self.Middle.outs[-1]    )
		self.TubeMiddleStraightB = rigSkeletonChain( n = self.Name.tubeMiddleStraightB , pos = tubeMiddleStraightBLocs  , parent = self.Middle.outs[-1]    )

		self.TubeArmA           = rigSkeletonChain( n = self.Name.tubeArmA             , pos = tubeArmALocs             , parent = self.Arm.outs[1]     )
		self.TubeArmHangA       = rigSkeletonChain( n = self.Name.tubeArmHangA         , pos = tubeArmHangALocs         , parent = self.Arm.outs[1]     )
		self.TubeArmStraightA   = rigSkeletonChain( n = self.Name.tubeArmStraightA     , pos = tubeArmStraightALocs     , parent = self.Arm.outs[1]     )
		self.TubeArmB           = rigSkeletonChain( n = self.Name.tubeArmB             , pos = tubeArmBLocs             , parent = self.Arm.outs[1]     )
		self.TubeArmHangB       = rigSkeletonChain( n = self.Name.tubeArmHangB         , pos = tubeArmHangBLocs         , parent = self.Arm.outs[1]     )
		self.TubeArmStraightB   = rigSkeletonChain( n = self.Name.tubeArmStraightB     , pos = tubeArmStraightBLocs     , parent = self.Arm.outs[1]     )

		self.TubeArmSmall       = rigSkeletonChain( n = self.Name.tubeArmSmall         , pos = tubeArmSmallLocs         , parent = self.Arm.outs[0]     )
		self.TubeArmSmallSide   = rigSkeletonChain( n = self.Name.tubeArmSideSmall     , pos = tubeArmSideSmallLocs     , parent = self.Arm.outs[0]     )

		self.TubePlugSmall      = rigSkeletonChain( n = self.Name.tubePlugSmall        , pos = tubePlugSmallLocs        , parent = self.Plug.outs[-1]     )
		self.TubePlugSmallSide  = rigSkeletonChain( n = self.Name.tubePlugSideSmall    , pos = tubePlugSideSmallLocs    , parent = self.Plug.outs[-1]     )

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

		args['debug'] = self.debug

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



		self.Attr.add( "GiroArm"    , Name = self.GiroArm.outs[0]    , attrName = ["lightVisibility"] , attrType = ["intOnOff"] , attrValue = [1] )
		self.Attr.add( "GiroCover" , Name = self.GiroCover.outs[0] , attrName = ["lightVisibility"] , attrType = ["intOnOff"] , attrValue = [1] )

		#CLASSE UTILS
		#CLASSE UTILS
		self.ins   = []
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

