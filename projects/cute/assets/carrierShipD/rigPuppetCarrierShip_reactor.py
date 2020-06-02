
	
'''
#******************************************************** BUILD EXEMPLE 
import maya.cmds as mc

import python
from    python.projects.cute.assets.carrierShipD.rigPuppetCarrierShip_reactor import *
reload( python.projects.cute.assets.carrierShipD.rigPuppetCarrierShip_reactor)
mc.file( 'D:/mcantat_BDD/projects/cute/assets/carrierShipD/maya/scenes/carrierShipD_rigSkeleton.ma' , o = True , f = True  )
#=================================================
puppet = rigPuppetCarrierShip_reactor( tubes = False )	
puppet.debug = 1
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

class rigPuppetCarrierShip_reactor(rigPuppet):

	def __init__( self , **args ):
		rigPuppet.__init__( self , **args )
		#CLASSE TYPE
		self.classeType = 'rigPuppetReactor'
		self.doTubes      = args.get( 'tubes'      , True )
		self.doProjectors = args.get( 'projectors' , True )
		self.doGiros      = args.get( 'giros'      , True )
		#CLASSE BLUE PRINT - POS
		propulsorRootLocs      = [x.encode('UTF8') for x in mc.ls('r_reacOffset?_JNT'    , type = 'joint' )]
		coverRootLocs          = ['r_reacCoverRoot0_JNT']
		coverSideLocs          = ['r_reacCoverSide0Left_JNT']
		burnPanelsLocs         = ['r_reacBurnPanels0_JNT']
		coverSlideLocs         = ['r_reacCoverSlide0Left_JNT']
		airCompressorLocs      = ['r_reacAirCompressorMain0_JNT']
		pistonSlideLocs        = ['r_reacPistonSlide0_JNT']
		fireLocs               = ['r_reacFire0_JNT'       ]
		burnPanelRightALocs    = [x.encode('UTF8') for x in mc.ls('r_reacBurnPanelA?Left_JNT'    , type = 'joint' )]
		burnPanelRightBLocs    = [x.encode('UTF8') for x in mc.ls('r_reacBurnPanelB?Left_JNT'    , type = 'joint' )]
		airCompressorRightLocs = [x.encode('UTF8') for x in mc.ls('r_reacAirCompressor?Left_JNT' , type = 'joint' )]
		armPropuplsorLocs      = [x.encode('UTF8') for x in mc.ls('r_reacArmPropulsor?_JNT'      , type = 'joint' )]
		armCoverLocs           = [x.encode('UTF8') for x in mc.ls('r_reacArmCoverMiddle?_JNT'    , type = 'joint' )]		
		armCoverRightLocs      = [x.encode('UTF8') for x in mc.ls('r_reacArmCover?Left_JNT'      , type = 'joint' )]
		
		armCoverDampALocs      = [x.encode('UTF8') for x in mc.ls('r_reacArmCoverDampA?_JNT'     , type = 'transform' )]
		armCoverDampBLocs      = [x.encode('UTF8') for x in mc.ls('r_reacArmCoverDampB?_JNT'     , type = 'transform' )]
		armCoverSideDampALocs  = [x.encode('UTF8') for x in mc.ls('r_reacArmCoverDampA?Left_JNT' , type = 'transform' )]
		armCoverSideDampBLocs  = [x.encode('UTF8') for x in mc.ls('r_reacArmCoverDampB?Left_JNT' , type = 'transform' )]

		coverDampSideLocs      = [x.encode('UTF8') for x in mc.ls('r_reacCoverDamp?Left_JNT'     , type = 'transform' )]

		pistonUpLocs           = [x.encode('UTF8') for x in mc.ls('r_reacPistonUp?Left_JNT'      , type = 'joint' )]		
		pistonDownLocs         = [x.encode('UTF8') for x in mc.ls('r_reacPistonDown?Left_JNT'    , type = 'joint' )]		
		giroLocs               = ['r_reacGiro0_JNT']

		if( self.doTubes ):
			tubeCoreALocs            = [x.encode('UTF8') for x in mc.ls('r_reacTubeCoreA?_JNT'            , type = 'joint' )]
			tubeCoreHangALocs        = [x.encode('UTF8') for x in mc.ls('r_reacTubeCoreHangA?_JNT'        , type = 'joint' )]		
			tubeCoreStraightALocs    = [x.encode('UTF8') for x in mc.ls('r_reacTubeCoreStraightA?_JNT'    , type = 'joint' )]			
			tubeCoreBLocs            = [x.encode('UTF8') for x in mc.ls('r_reacTubeCoreB?_JNT'            , type = 'joint' )]
			tubeCoreHangBLocs        = [x.encode('UTF8') for x in mc.ls('r_reacTubeCoreHangB?_JNT'        , type = 'joint' )]
			tubeCoreStraightBLocs    = [x.encode('UTF8') for x in mc.ls('r_reacTubeCoreStraightB?_JNT'    , type = 'joint' )]
			tubePistonALocs          = [x.encode('UTF8') for x in mc.ls('r_reacTubePistonA?_JNT'          , type = 'joint' )]
			tubePistonHangALocs      = [x.encode('UTF8') for x in mc.ls('r_reacTubePistonHangA?_JNT'      , type = 'joint' )]		
			tubePistonStraightALocs  = [x.encode('UTF8') for x in mc.ls('r_reacTubePistonStraightA?_JNT'  , type = 'joint' )]
			tubeArmSmallLocs         = [x.encode('UTF8') for x in mc.ls('r_reacTubeArmSmall?_JNT'         , type = 'joint' )]
			tubeArmSmallSideLocs     = [x.encode('UTF8') for x in mc.ls('r_reacTubeArmSmall?Left_JNT'     , type = 'joint' )]
						

		mirrorPlane            = 'symPlane_reactor1'

		#CLASSE BLUE PRINT
		self.Name.add( 'base'              , baseName = 'reac' )
		self.Name.add( 'rootB'             , ref = self.Name.base , baseNameAppend = 'offset'          )
		self.Name.add( 'coverSlide'        , ref = self.Name.base , baseNameAppend = 'coverSlide'    )
		self.Name.add( 'coverRoot'         , ref = self.Name.base , baseNameAppend = 'coverRoot'     )
		self.Name.add( 'cover'             , ref = self.Name.base , baseNameAppend = 'cover'         )
		self.Name.add( 'coverSide'         , ref = self.Name.base , baseNameAppend = 'coverSide'     )
		self.Name.add( 'armCoverMiddle'    , ref = self.Name.base , baseNameAppend = 'armCoverMiddle')
		self.Name.add( 'armCover'          , ref = self.Name.base , baseNameAppend = 'armCover'      )

		self.Name.add( 'armCoverDampA'     , ref = self.Name.base , baseNameAppend = 'armCoverDampA'        )
		self.Name.add( 'armCoverDampB'     , ref = self.Name.base , baseNameAppend = 'armCoverDampB'        )
		self.Name.add( 'armCoverSideDampA' , ref = self.Name.base , baseNameAppend = 'armCoverDampA'        )
		self.Name.add( 'armCoverSideDampB' , ref = self.Name.base , baseNameAppend = 'armCoverDampB'        )	

		self.Name.add( 'coverDampSide'     , ref = self.Name.base , baseNameAppend = 'coverDamp'         )	

		self.Name.add( 'armPropulsor'      , ref = self.Name.base , baseNameAppend = 'armPropulsor'  )
		self.Name.add( 'pistonSlide'       , ref = self.Name.base , baseNameAppend = 'pistonSlide'   )
		self.Name.add( 'pistonUp'          , ref = self.Name.base , baseNameAppend = 'pistonUp'      )
		self.Name.add( 'pistonDown'        , ref = self.Name.base , baseNameAppend = 'pistonDown'    )
		self.Name.add( 'burnPanels'        , ref = self.Name.base , baseNameAppend = 'burnPanels'       )
		self.Name.add( 'airCompressorMain' , ref = self.Name.base , baseNameAppend = 'airCompressorMain')
		self.Name.add( 'burnPanelA'        , ref = self.Name.base , baseNameAppend = 'burnPanelA'       )
		self.Name.add( 'burnPanelB'        , ref = self.Name.base , baseNameAppend = 'burnPanelB'       )
		self.Name.add( 'airCompressor'     , ref = self.Name.base , baseNameAppend = 'airCompressor'    )
		self.Name.add( 'fire'              , ref = self.Name.base , baseNameAppend = 'fire'             )
		self.Name.add( 'giro'              , ref = self.Name.base , baseNameAppend = 'giro'             )

		if( self.doTubes ):
			self.Name.add( 'tubeCoreA'           , ref = self.Name.base , baseNameAppend = 'tubeCoreA'           )
			self.Name.add( 'tubeCoreHangA'       , ref = self.Name.base , baseNameAppend = 'tubeCoreHangA'       )
			self.Name.add( 'tubeCoreStraightA'   , ref = self.Name.base , baseNameAppend = 'tubeCoreStraightA'   )
			self.Name.add( 'tubeCoreB'           , ref = self.Name.base , baseNameAppend = 'tubeCoreB'           )
			self.Name.add( 'tubeCoreHangB'       , ref = self.Name.base , baseNameAppend = 'tubeCoreHangB'       )		
			self.Name.add( 'tubeCoreStraightB'   , ref = self.Name.base , baseNameAppend = 'tubeCoreStraightB'   )
			self.Name.add( 'tubePistonA'         , ref = self.Name.base , baseNameAppend = 'tubePistonA'         )
			self.Name.add( 'tubePistonHangA'     , ref = self.Name.base , baseNameAppend = 'tubePistonHangA'     )
			self.Name.add( 'tubePistonStraightA' , ref = self.Name.base , baseNameAppend = 'tubePistonStraightA' )		
			self.Name.add( 'tubeArmSmall'        , ref = self.Name.base , baseNameAppend = 'tubeArmSmall'        )
			self.Name.add( 'tubeArmSmallSide'    , ref = self.Name.base , baseNameAppend = 'tubeArmSmall'    )	
	
		#CLASSE BLUE PRINT - SUBRIG
		self.ReactorRoot = rigModuleChain(  n = self.Name.rootB      , pos = propulsorRootLocs , form = 'crossArrow'      , colors = ['green']  , ctrlVisPriority = 0 , parent = self.Name.topNode , attrStates = [['t','r']] )
		self.CoverSlide  = rigCtrl(         n = self.Name.coverSlide , pos = coverSlideLocs    , form = 'arrow2sidesBend' , colors = ['red']    , ctrlVisPriority = 0 , parent = self.Name.topNode , attrStates = [['rz']] )	
		self.SubRigs     += [ self.ReactorRoot ]
		self.SubRigsName += [ 'ReactorRoot'    ]		
		
		self.CoverRoot    = rigCtrl(      n = self.Name.coverRoot          , pos = coverRootLocs          , form = 'cube'            , colors = ['yellow']  , ctrlVisPriority = 0 , parent = self.Name.topNode , attrStates = [['rz']] )	
		self.CoverSide    = rigCtrl(      n = self.Name.coverSide          , pos = coverSideLocs          , form = 'arrow2sidesBend' , colors = ['red']     , ctrlVisPriority = 0 , parent = self.Name.topNode , attrStates = [['rz']] )	
		self.ArmCover     = rigModuleArm( n = self.Name.armCoverMiddle     , pos = armCoverLocs           , ik = True , ctrlVisPriority = 10 , attrStates = [['rz']] )	
		self.ArmCoverSide = rigModuleArm( n = self.Name.armCover           , pos = armCoverRightLocs      , ik = True , ctrlVisPriority = 10 , attrStates = [['rz']] )			
		self.Giro         = rigCtrl(      n = self.Name.giro               , pos = giroLocs               , form = 'arrow2SidesBend' , colors = ['red']    , ctrlVisPriority = 6 , parent = self.Name.topNode , attrStates = [['rz']] )
		
		self.DampArmCoverA      = rigModulePiston( n = self.Name.armCoverDampA     , pos = armCoverDampALocs     , ctrlVisPriority = 10 , form = 'circle'          , colors = ['red'] , aim = 1 )	
		self.DampArmCoverB      = rigModulePiston( n = self.Name.armCoverDampB     , pos = armCoverDampBLocs     , ctrlVisPriority = 10 , form = 'circle'          , colors = ['red'] , aim = 1 )	
		self.DampArmCoverASide  = rigModulePiston( n = self.Name.armCoverSideDampA , pos = armCoverSideDampALocs , ctrlVisPriority = 10 , form = 'circle'          , colors = ['red'] , aim = 1 )	
		self.DampArmCoverBSide  = rigModulePiston( n = self.Name.armCoverSideDampB , pos = armCoverSideDampBLocs , ctrlVisPriority = 10 , form = 'circle'          , colors = ['red'] , aim = 1 )	

		self.DampCoverSide      = rigModulePiston( n = self.Name.coverDampSide     , pos = coverDampSideLocs     , ctrlVisPriority = 10 , form = 'circle'          , colors = ['red'] , aim = 1 )	

		self.SubRigs           += [  self.CoverRoot  , self.ArmCover , self.Giro , self.DampArmCoverA , self.DampArmCoverB ]
		self.SubRigsName       += [      'CoverRoot' ,     'ArmCover',     'Giro',     'DampArmCoverA',     'DampArmCoverB']		
     

		self.ArmPropulsor = rigModuleArm(    n = self.Name.armPropulsor , pos = armPropuplsorLocs      , ik = True , fk = True , skeleton = True  , ctrlVisPriority = 0 , attrStates = [['rz']] )	
		self.PistonSlide  = rigCtrl(         n = self.Name.pistonSlide  , pos = pistonSlideLocs        , form = 'arrow2sides'         , colors = ['red']  , ctrlVisPriority = 0 , parent = self.Name.topNode , attrStates = [['tx']] )
		self.PistonUp     = rigModulePiston( n = self.Name.pistonUp     , pos = pistonUpLocs           , form = 'circle' , colors = ['red'] , aim = 1 , ctrlVisPriority = 10)	
		self.PistonDown   = rigModulePiston( n = self.Name.pistonDown   , pos = pistonDownLocs         , form = 'circle' , colors = ['red'] , aim = 1 , ctrlVisPriority = 10)	
		self.SubRigs     += [ self.ArmPropulsor , self.PistonSlide ]	
		self.SubRigsName += [ 'ArmPropulsor'    , 'PistonSlide'    ]	

		self.BurnPanels        = rigCtrl(        n = self.Name.burnPanels         , pos = burnPanelsLocs         , form = 'cylinder'         , colors = ['yellow'] , ctrlVisPriority = 1 , parent = self.Name.topNode , attrStates = [['rz']] )
		self.Fire              = rigCtrl(        n = self.Name.fire               , pos = fireLocs               , form = 'cylinder'         , colors = ['red']    , ctrlVisPriority = 1 , parent = self.Name.topNode  )
		self.AirCompressor     = rigCtrl(        n = self.Name.airCompressorMain  , pos = airCompressorLocs      , form = 'arrow2SidesBend'  , colors = ['yellow'] , parent = self.Name.topNode                       , attrStates = [['rz']] )
		self.BurnPanelA        = rigModuleChain( n = self.Name.burnPanelA         , pos = burnPanelRightALocs    , form = 'plane'            , colors = ['red'] , skeleton = True  , ctrlVisPriority = 1              , attrStates = [['rz']] )	
		self.BurnPanelB        = rigModuleChain( n = self.Name.burnPanelB         , pos = burnPanelRightBLocs    , form = 'sphere'           , colors = ['red'] , skeleton = True  , ctrlVisPriority = 1              , attrStates = [['rz']] )		
		self.AirCompressorSide = rigModuleChain( n = self.Name.airCompressor      , pos = airCompressorRightLocs , form = 'circle'           , colors = ['red'] , skeleton = True  , ctrlVisPriority = 1              , attrStates = [['rz']] )	
		self.SubRigs     += [ self.BurnPanels , self.Fire ,  self.AirCompressor ]
		self.SubRigsName += [ 'BurnPanels'    ,     'Fire',      'AirCompressor'    ]

		if( self.doTubes ):
			self.TubeCoreA           = rigModuleArm(    n = self.Name.tubeCoreA           , pos = tubeCoreALocs           , ik = True , pv = True , ctrlVisPriority = 8 ,  attrStates = [['']] )
			self.TubeCoreHangA       = rigCtrl(         n = self.Name.tubeCoreHangA       , pos = tubeCoreHangALocs                               , ctrlVisPriority = 3 ,  attrStates = [['t','r']] , parent = self.Name.topNode)		
			self.TubeCoreStraightA   = rigModulePiston( n = self.Name.tubeCoreStraightA   , pos = tubeCoreStraightALocs                           , ctrlVisPriority = 8 ,  attrStates = [['']] )
			self.TubeCoreB           = rigModuleArm(    n = self.Name.tubeCoreB           , pos = tubeCoreBLocs           , ik = True , pv = True , ctrlVisPriority = 8 ,  attrStates = [['']] )
			self.TubeCoreHangB       = rigCtrl(         n = self.Name.tubeCoreHangB       , pos = tubeCoreHangBLocs                               , ctrlVisPriority = 3 ,  attrStates = [['t','r']] , parent = self.Name.topNode)		
			self.TubeCoreStraightB   = rigModulePiston( n = self.Name.tubeCoreStraightB   , pos = tubeCoreStraightBLocs                           , ctrlVisPriority = 8 ,  attrStates = [['']] )
	
			self.TubePistonA         = rigModuleArm(    n = self.Name.tubePistonA         , pos = tubePistonALocs         , ik = True , pv = True , ctrlVisPriority = 8 ,  attrStates = [['']] )    
			self.TubePistonHangA     = rigCtrl(         n = self.Name.tubePistonHangA     , pos = tubePistonHangALocs                             , ctrlVisPriority = 3 ,  attrStates = [['t','r']] , parent = self.Name.topNode)		
			self.TubePistonStraightA = rigModulePiston( n = self.Name.tubePistonStraightA , pos = tubePistonStraightALocs                         , ctrlVisPriority = 8 ,  attrStates = [['']] )    
	
			self.TubeArmSmall        = rigModuleArm(    n = self.Name.tubeArmSmall        , pos = tubeArmSmallLocs        , ik = True , pv = True , ctrlVisPriority = 8 ,  attrStates = [['']] )
			self.TubeArmSmallSide    = rigModuleArm(    n = self.Name.tubeArmSmallSide    , pos = tubeArmSmallSideLocs    , ik = True , pv = True , ctrlVisPriority = 8 ,  attrStates = [['']] )
	
			self.SubRigs     += [ self.TubeCoreA , self.TubeCoreHangA , self.TubeCoreStraightA , self.TubeCoreB , self.TubeCoreHangB , self.TubeCoreStraightB ]
			self.SubRigsName += [     'TubeCoreA',     'TubeCoreHangA',     'TubeCoreStraightA',     'TubeCoreB',     'TubeCoreHangB',     'TubeCoreStraightB']
				
			self.SubRigs     += [ self.TubePistonA , self.TubePistonHangA , self.TubePistonStraightA ]
			self.SubRigsName += [     'TubePistonA',     'TubePistonHangA',     'TubePistonStraightA']
	
			self.SubRigs     += [ self.TubeArmSmall ]
			self.SubRigsName += [     'TubeArmSmall']

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
		rigsToDuplicate.append( self.CoverSide         )
		rigsToDuplicate.append( self.CoverSlide        )
		rigsToDuplicate.append( self.ArmCoverSide      )
		rigsToDuplicate.append( self.DampArmCoverASide )
		rigsToDuplicate.append( self.DampArmCoverBSide )
		rigsToDuplicate.append( self.DampCoverSide     )
		rigsToDuplicate.append( self.PistonUp          )
		rigsToDuplicate.append( self.PistonDown        )
		rigsToDuplicate.append( self.BurnPanelA        )
		rigsToDuplicate.append( self.BurnPanelB        )
		rigsToDuplicate.append( self.AirCompressorSide )
		rigsToDuplicate.append( self.TubeArmSmallSide  )

		duplicated = self.duplicateRigs( args , rigsToDuplicate )

		self.CoverSideL         , self.CoverSideR         = duplicated[0][0]  , duplicated[0][1]
		self.CoverSlideL        , self.CoverSlideR        = duplicated[1][0]  , duplicated[1][1]
		self.ArmCoverL          , self.ArmCoverR          = duplicated[2][0]  , duplicated[2][1]
		self.DampArmCoverAL     , self.DampArmCoverAR     = duplicated[3][0]  , duplicated[3][1]
		self.DampArmCoverBL     , self.DampArmCoverBR     = duplicated[4][0]  , duplicated[4][1]
		self.DampCoverL         , self.DampCoverR         = duplicated[5][0]  , duplicated[5][1]
		self.PistonUpL          , self.PistonUpR          = duplicated[6][0]  , duplicated[6][1]
		self.PistonDownL        , self.PistonDownR        = duplicated[7][0]  , duplicated[7][1]
		self.BurnPanelAL        , self.BurnPanelAR        = duplicated[8][0]  , duplicated[8][1]
		self.BurnPanelBL        , self.BurnPanelBR        = duplicated[9][0]  , duplicated[9][1]
		self.AirCompressorSideL , self.AirCompressorSideR = duplicated[10][0] , duplicated[10][1]
		self.TubeArmSmallL      , self.TubeArmSmallR      = duplicated[11][0] , duplicated[11][1]

		self.SubRigs     += [ self.CoverSideL         , self.CoverSideR         ]
		self.SubRigs     += [ self.CoverSlideL        , self.CoverSlideR        ]
		self.SubRigs     += [ self.ArmCoverL          , self.ArmCoverR          ]
		self.SubRigs     += [ self.DampArmCoverAL     , self.DampArmCoverAR     ]
		self.SubRigs     += [ self.DampArmCoverBL     , self.DampArmCoverBR     ]
		self.SubRigs     += [ self.DampCoverL         , self.DampCoverR         ]
		self.SubRigs     += [ self.PistonUpL          , self.PistonUpR          ]
		self.SubRigs     += [ self.PistonDownL        , self.PistonDownR        ]
		self.SubRigs     += [ self.BurnPanelAL        , self.BurnPanelAR        ]
		self.SubRigs     += [ self.BurnPanelBL        , self.BurnPanelBR        ]
		self.SubRigs     += [ self.AirCompressorSideL , self.AirCompressorSideR ]
		self.SubRigs     += [ self.TubeArmSmallL      , self.TubeArmSmallR      ]

		self.SubRigsName += [     'CoverSideL'         ,     'CoverSideR'         ]
		self.SubRigsName += [     'CoverSlideL'        ,     'CoverSlideR'        ]
		self.SubRigsName += [     'ArmCoverL'          ,     'ArmCoverR'          ]
		self.SubRigsName += [     'DampArmCoverAL'     ,     'DampArmCoverAR'     ]
		self.SubRigsName += [     'DampArmCoverBL'     ,     'DampArmCoverBR'     ]
		self.SubRigsName += [     'DampCoverL'         ,     'DampCoverR'         ]
		self.SubRigsName += [     'PistonUpL'          ,     'PistonUpR'          ]
		self.SubRigsName += [     'PistonDownL'        ,     'PistonDownR'        ]
		self.SubRigsName += [     'BurnPanelAL'        ,     'BurnPanelAR'        ]
		self.SubRigsName += [     'BurnPanelBL'        ,     'BurnPanelBR'        ]
		self.SubRigsName += [     'AirCompressorSideL' ,     'AirCompressorSideR' ]
		self.SubRigsName += [     'TubeArmSmallL'      ,     'TubeArmSmallR'      ]		
	


		##CLASSE BLUE PRINT - OTHER
		if( self.doTubes ):		
			self.Attr.add( 'TubeCoreHangA'   , Name = self.TubeCoreHangA.Name.ctrl   , attrName = ['straighten'] , attrType = ['floatOnOff'] , attrValue = [0] , attrKeyable = [True] )
			self.Attr.add( 'TubeCoreHangB'   , Name = self.TubeCoreHangB.Name.ctrl   , attrName = ['straighten'] , attrType = ['floatOnOff'] , attrValue = [0] , attrKeyable = [True] )
			self.Attr.add( 'TubePistonHangA' , Name = self.TubePistonHangA.Name.ctrl , attrName = ['straighten'] , attrType = ['floatOnOff'] , attrValue = [0] , attrKeyable = [True] )

		self.Attr.add( "giro"    , Name = self.Giro.Name.ctrl   , attrName = ["lightVisibility"] , attrType = ["intOnOff"] , attrValue = [1] )
		self.Attr.add( "fire"    , Name = self.Fire.Name.ctrl   , attrName = ["lightVisibility"] , attrType = ["intOnOff"] , attrValue = [1] )
		

		self.Link.add( 'paArmCover' , Sources = [ self.ReactorRoot.outs[0]    ] , Destinations = [ self.ArmCover.ins[1]  , self.ArmCoverR.ins[1] , self.ArmCoverL.ins[1]                        ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )	
		self.Link.add( 'paPistons'  , Sources = [ self.ArmPropulsor.outs[2] ] , Destinations = [ self.PistonUpR.ins[1] , self.PistonUpL.ins[1]     , self.PistonDownR.ins[1]  , self.PistonDownL.ins[1] ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )					

		self.Link.add( 'DampArmCoverA'       , Sources = [ self.ArmCover.outs[1]           ] , Destinations = [ self.DampArmCoverA.ins[1]                                   ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )
		self.Link.add( 'DampArmCoverB'       , Sources = [ self.ArmCover.outs[0]           ] , Destinations = [ self.DampArmCoverB.ins[1]	                                ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )
		self.Link.add( 'DampArmCoverAL'      , Sources = [ self.ArmCoverL.outs[1]          ] , Destinations = [ self.DampArmCoverAL.ins[1]                                  ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )
		self.Link.add( 'DampArmCoverBL'      , Sources = [ self.ArmCoverL.outs[0]          ] , Destinations = [ self.DampArmCoverBL.ins[1]                                  ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )		
		self.Link.add( 'DampArmCoverAR'      , Sources = [ self.ArmCoverR.outs[1]          ] , Destinations = [ self.DampArmCoverAR.ins[1]                                  ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )
		self.Link.add( 'DampArmCoverBR'      , Sources = [ self.ArmCoverR.outs[0]          ] , Destinations = [ self.DampArmCoverBR.ins[1]	                                ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )

		self.Link.add( 'DampCoverL'          , Sources = [ self.CoverRoot.outs[0]             ] , Destinations = [ self.DampCoverL.ins[1]	                                ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )
		self.Link.add( 'DampCoverR'          , Sources = [ self.CoverRoot.outs[0]             ] , Destinations = [ self.DampCoverR.ins[1]	                                ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )


		self.Link.add( 'tubeArmOffset'     , Sources = [ self.ArmPropulsor.outs[2]   ] , Destinations = [ self.TubeCoreA.ins[1]    , self.TubeCoreStraightA.ins[1]   , self.TubeCoreB.ins[1] , self.TubeCoreStraightB.ins[1] ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )	
		self.Link.add( 'tubePistonUpR'     , Sources = [ self.PistonUpL.outs[0]      ] , Destinations = [ self.TubePistonA.ins[1]  , self.TubePistonStraightA.ins[1]                                                         ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )			  
		self.Link.add( 'tubeArm0'          , Sources = [ self.ArmPropulsor.outs[1]   ] , Destinations = [ self.TubeArmSmall.ins[1] , self.TubeArmSmallL.ins[1]       , self.TubeArmSmallR.ins[1]                             ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )	

		if( self.doTubes ):	
			self.Link.add( 'TubeCoreHangA'   , Sources = [ self.TubeCoreA.outs[0]   ] , Destinations = [ self.TubeCoreHangA.ins[0]   ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 , skipAxes = [0,0,0,1,1,1,0,0,0] )	
			self.Link.add( 'TubeCoreHangB'   , Sources = [ self.TubeCoreB.outs[0]   ] , Destinations = [ self.TubeCoreHangB.ins[0]   ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 , skipAxes = [0,0,0,1,1,1,0,0,0] )	
			self.Link.add( 'TubePistonHangA' , Sources = [ self.TubePistonA.outs[0] ] , Destinations = [ self.TubePistonHangA.ins[0] ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 , skipAxes = [0,0,0,1,1,1,0,0,0] )	


		self.Link.add( 'paSpaceArm' , Sources = [ self.CoverRoot.outs[0] ] , Destinations = [ self.ArmPropulsor.ins[0] ] , type = 'parentSpace'  , spaceDriver = self.ArmPropulsor.Root.Name.ctrl    , spaceAttr = 'parentSpace' , spaceNames = ['cover'] )



		#CLASSE UTILS
		self.ins         = [ self.ReactorRoot.ins[0] , self.ArmPropulsor.ins[1] , self.ArmPropulsor.ins[0] ]
		self.outs        = []		
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


