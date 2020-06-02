
	
'''
#******************************************************** BUILD EXEMPLE 
import maya.cmds as mc

import python
from    python.projects.cute.assets.carrierShipD.rigSkeletonCarrierShip_reactor import *
reload( python.projects.cute.assets.carrierShipD.rigSkeletonCarrierShip_reactor)
mc.file( 'D:/mcantat_BDD/projects/cute/assets/carrierShipD/maya/scenes/carrierShipD_rigBase5.ma' , o = True , f = True  )
#=================================================
puppet = rigSkeletonCarrierShip_reactor( tubes = False )	
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

class rigSkeletonCarrierShip_reactor(rigPuppet):

	def __init__( self , **args ):
		rigPuppet.__init__( self , **args )
		#CLASSE TYPE
		self.classeType = 'rigSkeletonReactor'
		self.doTubes = args.get( 'tubes' , None )
		#CLASSE BLUE PRINT - POS
		propulsorLocs          = ['pos_propulsor']
		propulsorRootLocs      = [x.encode('UTF8') for x in mc.ls('pos_reactorRoot?'    , type = 'transform' )]
		coverRootLocs          = ['pos_cacheRoot1']
		coverSideLocs          = ['pos_cacheRight1']
		burnPanelsLocs         = ['pos_burnPanels']
		coverSlideLocs         = ['pos_reactorSlideRight1']
		airCompressorLocs      = ['pos_airCompressor']
		pistonSlideLocs        = ['pos_pistonTopSlide1']
		fireLocs               = ['pos_reactorFire']
		burnPanelRightALocs    = [x.encode('UTF8') for x in mc.ls('pos_burnPanelRightA?'    , type = 'transform' )]
		burnPanelRightBLocs    = [x.encode('UTF8') for x in mc.ls('pos_burnPanelRightB?'    , type = 'transform' )]
		airCompressorRightLocs = [x.encode('UTF8') for x in mc.ls('pos_airCompressorRight?' , type = 'transform' )]
		armPropuplsorLocs      = [x.encode('UTF8') for x in mc.ls('pos_reactorArm?'         , type = 'transform' )]
		armCoverLocs           = [x.encode('UTF8') for x in mc.ls('pos_cacheArmMain?'       , type = 'transform' )]		
		armCoverRightLocs      = [x.encode('UTF8') for x in mc.ls('pos_cacheArmRight?'      , type = 'transform' )]
		
		armCoverDampALocs      = [x.encode('UTF8') for x in mc.ls('pos_reactorCoverArmDampA?'     , type = 'transform' )]
		armCoverDampBLocs      = [x.encode('UTF8') for x in mc.ls('pos_reactorCoverArmDampB?'     , type = 'transform' )]
		armCoverSideDampALocs  = [x.encode('UTF8') for x in mc.ls('pos_reactorCoverArmSideDampA?' , type = 'transform' )]
		armCoverSideDampBLocs  = [x.encode('UTF8') for x in mc.ls('pos_reactorCoverArmSideDampB?' , type = 'transform' )]

		coverDampSideLocs      = [x.encode('UTF8') for x in mc.ls('pos_reactorCoverDampSide?'     , type = 'transform' )]

		pistonUpLocs           = [x.encode('UTF8') for x in mc.ls('pos_pistonUpRight?'      , type = 'transform' )]		
		pistonDownLocs         = [x.encode('UTF8') for x in mc.ls('pos_pistonDownRight?'    , type = 'transform' )]		
		giroLocs               = ['pos_reactorGiro1']

		tubeCoreALocs            = [x.encode('UTF8') for x in mc.ls('pos_reactorCoreTubeA?'            , type = 'transform' )]
		tubeCoreHangALocs        = [x.encode('UTF8') for x in mc.ls('pos_reactorCoreTubeHangA?'        , type = 'transform' )]	
		tubeCoreStraightALocs    = [x.encode('UTF8') for x in mc.ls('pos_reactorCoreTubeStraightA?'    , type = 'transform' )]			
		tubeCoreBLocs            = [x.encode('UTF8') for x in mc.ls('pos_reactorCoreTubeB?'            , type = 'transform' )]
		tubeCoreHangBLocs        = [x.encode('UTF8') for x in mc.ls('pos_reactorCoreTubeHangB?'        , type = 'transform' )]
		tubeCoreStraightBLocs    = [x.encode('UTF8') for x in mc.ls('pos_reactorCoreTubeStraightB?'    , type = 'transform' )]
		tubePistonALocs          = [x.encode('UTF8') for x in mc.ls('pos_reactorPistonTubeA?'          , type = 'transform' )]
		tubePistonHangALocs      = [x.encode('UTF8') for x in mc.ls('pos_reactorPistonTubeHangA?'      , type = 'transform' )]
		tubePistonStraightALocs  = [x.encode('UTF8') for x in mc.ls('pos_reactorPistonTubeStraightA?'  , type = 'transform' )]
		tubeArmSmallLocs         = [x.encode('UTF8') for x in mc.ls('pos_reactorArmTubeSmall?'         , type = 'transform' )]
		tubeArmSmallSideLocs     = [x.encode('UTF8') for x in mc.ls('pos_reactorArmTubeSmallSideLeft?' , type = 'transform' )]

		mirrorPlane            = 'symPlane_reactor1'

		#CLASSE BLUE PRINT
		self.Name.add( 'base'              , baseName = 'reac' )
		self.Name.add( 'root'              , ref = self.Name.base , baseNameAppend = 'root'            )
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
		self.Name.add( 'fire'              , ref = self.Name.base , baseNameAppend = 'fire'             )
		self.Name.add( 'airCompressorMain' , ref = self.Name.base , baseNameAppend = 'airCompressorMain')
		self.Name.add( 'burnPanelA'        , ref = self.Name.base , baseNameAppend = 'burnPanelA'       )
		self.Name.add( 'burnPanelB'        , ref = self.Name.base , baseNameAppend = 'burnPanelB'       )
		self.Name.add( 'airCompressor'     , ref = self.Name.base , baseNameAppend = 'airCompressor'    )
		self.Name.add( 'giro'              , ref = self.Name.base , baseNameAppend = 'giro'             )

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
		parent  = args.get( 'parent' , self.Name.topNode  )

		self.ReactorRoot        = rigSkeletonChain( n = self.Name.rootB            , pos = propulsorRootLocs      , parent = parent ) 
		self.CoverSlide         = rigSkeletonChain( n = self.Name.coverSlide       , pos = coverSlideLocs         , parent = self.ReactorRoot.outs[-2] ) 
		self.SubRigs           += [ self.ReactorRoot ]
		self.SubRigsName       += [     'ReactorRoot']		
		      
		self.CoverRoot          = rigSkeletonChain( n = self.Name.coverRoot        , pos = coverRootLocs          , parent = self.ReactorRoot.outs[-1] ) 
		self.Cover              = rigSkeletonChain( n = self.Name.cover            , pos = coverRootLocs          , parent = self.CoverRoot.outs[-1]   )
		self.CoverSide          = rigSkeletonChain( n = self.Name.coverSide        , pos = coverSideLocs          , parent = self.CoverRoot.outs[-1]   )
		self.ArmCover           = rigSkeletonChain( n = self.Name.armCoverMiddle   , pos = armCoverLocs           , parent = self.Cover.outs[-1]       ) 
		self.ArmCoverSide       = rigSkeletonChain( n = self.Name.armCover         , pos = armCoverRightLocs      , parent = self.Cover.outs[-1]       ) 
		self.Giro               = rigSkeletonChain( n = self.Name.giro             , pos = giroLocs               , parent = self.Cover.outs[-1]       )
		
		self.DampArmCoverA      = rigSkeletonChain( n = self.Name.armCoverDampA     , pos = armCoverDampALocs     , parent = self.ReactorRoot.outs[-1] )
		self.DampArmCoverB      = rigSkeletonChain( n = self.Name.armCoverDampB     , pos = armCoverDampBLocs     , parent = self.Cover.outs[-1] )
		self.DampArmCoverASide  = rigSkeletonChain( n = self.Name.armCoverSideDampA , pos = armCoverSideDampALocs , parent = self.ReactorRoot.outs[-1] )
		self.DampArmCoverBSide  = rigSkeletonChain( n = self.Name.armCoverSideDampB , pos = armCoverSideDampBLocs , parent = self.Cover.outs[-1] )

		self.DampCoverSide      = rigSkeletonChain( n = self.Name.coverDampSide     , pos = coverDampSideLocs     , parent = self.ReactorRoot.outs[-1] )

		self.SubRigs           += [ self.Cover , self.CoverRoot  , self.ArmCover , self.Giro , self.DampArmCoverA , self.DampArmCoverB ]
		self.SubRigsName       += [     'Cover',     'CoverRoot' ,     'ArmCover',     'Giro',     'DampArmCoverA',     'DampArmCoverB']		
     
		self.ArmPropulsor      = rigSkeletonChain( n = self.Name.armPropulsor      , pos = armPropuplsorLocs      , parent = self.ReactorRoot.outs[-1] )
		self.PistonSlide       = rigSkeletonChain( n = self.Name.pistonSlide       , pos = pistonSlideLocs        , parent = self.Cover.outs[-1]       )
		self.PistonUp          = rigSkeletonChain( n = self.Name.pistonUp          , pos = pistonUpLocs           , parent = self.PistonSlide.outs[-1] )
		self.PistonDown        = rigSkeletonChain( n = self.Name.pistonDown        , pos = pistonDownLocs         , parent = self.PistonSlide.outs[-1] )
		self.SubRigs          += [ self.ArmPropulsor , self.PistonSlide ]	
		self.SubRigsName      += [ 'ArmPropulsor'    , 'PistonSlide'    ]	

		self.BurnPanels        = rigSkeletonChain( n = self.Name.burnPanels        , pos = burnPanelsLocs         , parent = self.ArmPropulsor.outs[-1]  )
		self.AirCompressor     = rigSkeletonChain( n = self.Name.airCompressorMain , pos = airCompressorLocs      , parent = self.ArmPropulsor.outs[-1]  )
		self.BurnPanelA        = rigSkeletonChain( n = self.Name.burnPanelA        , pos = burnPanelRightALocs    , parent = self.BurnPanels.outs[-1]    )
		self.BurnPanelB        = rigSkeletonChain( n = self.Name.burnPanelB        , pos = burnPanelRightBLocs    , parent = self.BurnPanels.outs[-1]    )	
		self.Fire              = rigSkeletonChain( n = self.Name.fire              , pos = fireLocs               , parent = self.BurnPanels.outs[-1]    )	
		self.AirCompressorSide = rigSkeletonChain( n = self.Name.airCompressor     , pos = airCompressorRightLocs , parent = self.AirCompressor.outs[-1] )
		self.SubRigs          += [ self.BurnPanels , self.AirCompressor , self.Fire  ]
		self.SubRigsName      += [ 'BurnPanels'    , 'AirCompressor'    ,     'Fire' ]



		self.TubeCoreA           = rigSkeletonChain( n = self.Name.tubeCoreA           , pos = tubeCoreALocs           , parent = self.ReactorRoot.outs[-1] )
		self.TubeCoreHangA       = rigSkeletonChain( n = self.Name.tubeCoreHangA       , pos = tubeCoreHangALocs       , parent = self.ReactorRoot.outs[-1] )
		self.TubeCoreStraightA   = rigSkeletonChain( n = self.Name.tubeCoreStraightA   , pos = tubeCoreStraightALocs   , parent = self.ReactorRoot.outs[-1] )
		self.TubeCoreB           = rigSkeletonChain( n = self.Name.tubeCoreB           , pos = tubeCoreBLocs           , parent = self.ReactorRoot.outs[-1] )
		self.TubeCoreHangB       = rigSkeletonChain( n = self.Name.tubeCoreHangB       , pos = tubeCoreHangBLocs       , parent = self.ReactorRoot.outs[-1] )
		self.TubeCoreStraightB   = rigSkeletonChain( n = self.Name.tubeCoreStraightB   , pos = tubeCoreStraightBLocs   , parent = self.ReactorRoot.outs[-1] )

		self.TubePistonA         = rigSkeletonChain( n = self.Name.tubePistonA         , pos = tubePistonALocs         , parent = self.Cover.outs[-1]       )
		self.TubePistonHangA     = rigSkeletonChain( n = self.Name.tubePistonHangA     , pos = tubePistonHangALocs     , parent = self.Cover.outs[-1]       )
		self.TubePistonStraightA = rigSkeletonChain( n = self.Name.tubePistonStraightA , pos = tubePistonStraightALocs , parent = self.Cover.outs[-1]       )

		self.TubeArmSmall        = rigSkeletonChain( n = self.Name.tubeArmSmall        , pos = tubeArmSmallLocs        , parent = self.ArmPropulsor.outs[0] )
		self.TubeArmSmallSide    = rigSkeletonChain( n = self.Name.tubeArmSmallSide    , pos = tubeArmSmallSideLocs    , parent = self.ArmPropulsor.outs[0] )

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

		args['debug'] = self.debug

		
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
		self.Attr.add( "giro"    , Name = self.Giro.outs[0]    , attrName = ["lightVisibility"] , attrType = ["intOnOff"] , attrValue = [1] )
		self.Attr.add( "fire"    , Name = self.Fire.outs[0]    , attrName = ["lightVisibility"] , attrType = ["intOnOff"] , attrValue = [1] )
		

		#CLASSE UTILS
		self.ins         = [ self.ArmPropulsor.ins[1] , self.ArmPropulsor.ins[0] ]
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


