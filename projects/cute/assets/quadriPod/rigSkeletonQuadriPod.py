
'''




############################################################################ BUILD SKELETON
import maya.cmds as mc
import python
from python.projects.cute.assets.quadriPod.rigSkeletonQuadriPod import *
reload( python.projects.cute.assets.quadriPod.rigSkeletonQuadriPod)
#___________________________________________________________________________LOAD RIG BASE
from python.classe.readWriteInfo import *
reload(python.classe.readWriteInfo)
rwi = readWriteInfo()
rwi.mayaScene_load( 'D:/mcantat_BDD/projects/cute/assets/quadriPod/maya/scenes/quadriPod_rigBase.ma' , open = True )
#___________________________________________________________________________LOAD RIG BASE

import python.utils.utilsMaya as utilsMaya
utilsMaya.setSceneUnitToMeter()


#BUILD
puppet = rigSkeletonQuadriPod()
puppet.printBuild = 1	
toExec = puppet.build()
exec(toExec)


#CLEAN ROOT 
toKeep = ['rigPuppet_GRP','all_GRP']
rootElem = mc.ls("|*" , type = "transform")
rootElem = [ elem for elem in rootElem if not (elem in toKeep ) ]
mc.delete(rootElem)


#___________________________________________________________________________SAVE TO SKELETON
rwi.mayaScene_save( 'D:/mcantat_BDD/projects/cute/assets/quadriPod/maya/scenes/quadriPod_rigSkeleton.ma' )
#___________________________________________________________________________SAVE TO SKELETON







'''

	


import maya.cmds as mc

from .....classe.rigPuppet import *  
from .....classe.rigCtrl import *  
from .....classe.rigModuleChain import *     
from .....classe.rigModuleArm import *    
from .....classe.rigModulePiston import *  
from .....classe.rigModuleProjector import *
from .....classe.rigModuleRotatingBeacon import *


       
class rigSkeletonQuadriPod(rigPuppet):

	def __init__( self , **args ):
		rigPuppet.__init__( self , **args )
		#UTILS	
		#CLASSE
		self.classeType = 'rigSkeletonQuadriPod'
		#NAME
		self.Name.add( 'quadri' , baseName = self.classeType    , type = 'GRP' )			
		#INSTANCE_______________________________BLUEPRINT
		posLocs         = ['pos_pos1' ]
		trajLocs        = ['pos_traj1']
		bodyLocs        = ['pos_body1']
		feetsLocs       = ['pos_feets1']
		rampLocs        = ['pos_ramp1']
		fanLocs         = ['pos_fan1']
		pumpLocs        = [x.encode('UTF8') for x in mc.ls('pos_pump?'        , type = 'transform' )]

		rampHolderLocs         = ['pos_rampHolder1']
		rampPistonLocs         = [x.encode('UTF8') for x in mc.ls('pos_rampPiston?'          , type = 'transform' )]
		topDamperLocs          = [x.encode('UTF8') for x in mc.ls('pos_topDamper?'           , type = 'transform' )]
		rampHolderSupportALocs = [x.encode('UTF8') for x in mc.ls('pos_rampHolderSupportA?'  , type = 'transform' )]		
		rampHolderSupportBLocs = [x.encode('UTF8') for x in mc.ls('pos_rampHolderSupportB?'  , type = 'transform' )]

		tubeRampPistonLocs   = [x.encode('UTF8') for x in mc.ls('pos_TubeRampPiston?'   , type = 'transform' )]
		tubeReserveLocs      = [x.encode('UTF8') for x in mc.ls('pos_tubeReserve?'      , type = 'transform' )]

		#NAME
		self.Name.add( 'pos'   , baseName = 'pos'    )
		self.Name.add( 'traj'  , baseName = 'traj'   )	
		self.Name.add( 'body'  , baseName = 'body'   )
		self.Name.add( 'feets' , baseName = 'feets'  )
		self.Name.add( 'ramp'  , baseName = 'ramp'   )
		self.Name.add( 'fan'   , baseName = 'fan'    )
		self.Name.add( 'pump'  , baseName = 'pump'   )
		self.Name.add( 'pumpA' , ref = self.Name.pump , baseNameAppend = 'A'   )
		self.Name.add( 'pumpB' , ref = self.Name.pump , baseNameAppend = 'B'   )

		self.Name.add( 'rampHolder'        , baseName = 'rampHolder'         )
		self.Name.add( 'rampPiston'        , baseName = 'rampPiston'         )
		self.Name.add( 'topDamper'         , baseName = 'topDamper'          )
		self.Name.add( 'topDamperA'        , ref = self.Name.topDamper , baseNameAppend = 'A'   )
		self.Name.add( 'topDamperB'        , ref = self.Name.topDamper , baseNameAppend = 'B'   )
		self.Name.add( 'topDamperC'        , ref = self.Name.topDamper , baseNameAppend = 'C'   )
		self.Name.add( 'rampHolderSupportA', baseName = 'rampHolderSupportA' )
		self.Name.add( 'rampHolderSupportB', baseName = 'rampHolderSupportB' )

		self.Name.add( 'tubeRampPiston', baseName = 'tubeRampPiston' )
		self.Name.add( 'tubeReserve'   , baseName = 'tubeReserve'    )

		self.Name.add( 'leg', baseName = 'leg' )

		#MAIN CTRLS
		self.Position = rigSkeletonChain( n = self.Name.pos , pos = posLocs  , parent = self.Name.topNode )
		self.Traj  = rigSkeletonChain( n = self.Name.traj  , pos = trajLocs  , parent = self.Position.outs[-1]  )
		self.Body  = rigSkeletonChain( n = self.Name.body  , pos = bodyLocs  , parent = self.Traj.outs[-1] )
		self.Feets = rigSkeletonChain( n = self.Name.feets , pos = feetsLocs , parent = self.Traj.outs[-1] )

		self.Ramp  = rigSkeletonChain( n = self.Name.ramp   , pos = rampLocs      , parent = self.Body.outs[-1] )
		self.Fan   = rigSkeletonChain( n = self.Name.fan    , pos = fanLocs       , parent = self.Body.outs[-1] )
		self.PumpA = rigSkeletonChain( n = self.Name.pumpA  , pos = [pumpLocs[0]] , parent = self.Body.outs[-1] )
		self.PumpB = rigSkeletonChain( n = self.Name.pumpB  , pos = [pumpLocs[1]] , parent = self.Body.outs[-1] )

		self.TubeReserve = rigSkeletonChain( n = self.Name.tubeReserve  , pos =  tubeReserveLocs  , parent = self.Body.outs[-1] )

		self.SubRigs     += [ self.Position , self.Traj , self.Body , self.Feets , self.Ramp , self.Fan , self.PumpA , self.PumpB , self.TubeReserve  ]		
		self.SubRigsName += [     'Position' ,    'Traj',     'Body',     'Feets',     'Ramp',     'Fan',     'PumpA',     'PumpB',     'TubeReserve' ]	

		#SIDES CTRLS
		self.RampHolder         = rigSkeletonChain( n = self.Name.rampHolder         , pos = rampHolderLocs         , parent = self.Ramp.outs[-1] )
		self.RampPiston         = rigSkeletonChain( n = self.Name.rampPiston         , pos = rampPistonLocs         , parent = self.Body.outs[-1] )	
		self.TopDamperA         = rigSkeletonChain( n = self.Name.topDamperA         , pos = [topDamperLocs[0]]     , parent = self.Body.outs[-1] )
		self.TopDamperB         = rigSkeletonChain( n = self.Name.topDamperB         , pos = [topDamperLocs[1]]     , parent = self.Body.outs[-1] )
		self.TopDamperC         = rigSkeletonChain( n = self.Name.topDamperC         , pos = [topDamperLocs[2]]     , parent = self.Body.outs[-1] )
		self.RampHolderSupportA = rigSkeletonChain( n = self.Name.rampHolderSupportA , pos = rampHolderSupportALocs , parent = self.Ramp.outs[-1] )
		self.RampHolderSupportB = rigSkeletonChain( n = self.Name.rampHolderSupportB , pos = rampHolderSupportBLocs , parent = self.Ramp.outs[-1] )

		self.TubeRampPiston     = rigSkeletonChain( n = self.Name.tubeRampPiston     , pos = tubeRampPistonLocs , parent = self.Body.outs[-1] )

		#SUBRIG
		self.Leg   = rigSkeletonQuadriPod_leg(   n = self.Name.leg   , ctrlVisPriority = 1 , parent = self.Body.outs[-1] )

		#MIRROR
		argsMirrorZ = {}
		argsMirrorZ['value']             = [0,0,0 , 0,1,0 , 1,0,0]
		argsMirrorZ['mode']              = 'mirror'
		argsMirrorZ['pivot']             = [0,0,0 , 0,0,0 , 1,1,1]
		argsMirrorZ['namePrefix']        = []
		argsMirrorZ['nameReplace']       = []
		argsMirrorZ['nameIncr']          = 'leg0'
		argsMirrorZ['nameAdd']           = []
		argsMirrorZ['noneMirrorAxe']     = 4
		argsMirrorZ['debug']             = self.debug

		self.LegFront  , self.LegBack     = self.Leg.duplicate( **argsMirrorZ )

		argsMirrorX = {}
		argsMirrorX['value']             = [0,0,0 , 0,1,0 , 0,0,1]
		argsMirrorX['mode']              = 'mirror'
		argsMirrorX['pivot']             = [0,0,0 , 0,0,0 , 1,1,1]
		argsMirrorX['namePrefix']        = ['r','l']
		argsMirrorX['nameReplace']       = ['','']
		argsMirrorX['nameIncr']          = ''
		argsMirrorX['nameAdd']           = []
		argsMirrorX['noneMirrorAxe']     = 4
		argsMirrorX['debug']             = self.debug
		

		rigsToDuplicate = []
		rigsToDuplicate.append( self.RampHolder         )
		rigsToDuplicate.append( self.RampPiston         )
		rigsToDuplicate.append( self.TopDamperA         )
		rigsToDuplicate.append( self.TopDamperB         )
		rigsToDuplicate.append( self.TopDamperC         )
		rigsToDuplicate.append( self.RampHolderSupportA )
		rigsToDuplicate.append( self.RampHolderSupportB )
		rigsToDuplicate.append( self.LegFront           )
		rigsToDuplicate.append( self.LegBack            )
		rigsToDuplicate.append( self.TubeRampPiston     )

		print('duplicateRigs IN')
		duplicated = self.duplicateRigs( argsMirrorX , rigsToDuplicate )
		print('duplicateRigs OUT')

		self.RampHolderR         , self.RampHolderL          = duplicated[0][0] , duplicated[0][1]
		self.RampPistonR         , self.RampPistonL          = duplicated[1][0] , duplicated[1][1]
		self.TopDamperAR         , self.TopDamperAL          = duplicated[2][0] , duplicated[2][1]
		self.TopDamperBR         , self.TopDamperBL          = duplicated[3][0] , duplicated[3][1]
		self.TopDamperCR         , self.TopDamperCL          = duplicated[4][0] , duplicated[4][1]
		self.RampHolderSupportAR , self.RampHolderSupportAL  = duplicated[5][0] , duplicated[5][1]
		self.RampHolderSupportBR , self.RampHolderSupportBL  = duplicated[6][0] , duplicated[6][1]
		self.LegFrontR           , self.LegFrontL            = duplicated[7][0] , duplicated[7][1]
		self.LegBackR            , self.LegBackL             = duplicated[8][0] , duplicated[8][1]
		self.TubeRampPistonR     , self.TubeRampPistonL      = duplicated[9][0] , duplicated[9][1]

		self.SubRigs += [ self.RampHolderR  , self.RampHolderL ]
		self.SubRigs += [ self.RampPistonR  , self.RampPistonL ]
		self.SubRigs += [ self.TopDamperAR  , self.TopDamperAL ]
		self.SubRigs += [ self.TopDamperBR  , self.TopDamperBL ]
		self.SubRigs += [ self.TopDamperCR  , self.TopDamperCL ]		
		self.SubRigs += [ self.RampHolderSupportAR  , self.RampHolderSupportAL ]
		self.SubRigs += [ self.RampHolderSupportBR  , self.RampHolderSupportBL ]		
		self.SubRigs += [ self.LegFrontR    , self.LegFrontL ]
		self.SubRigs += [ self.LegBackR     , self.LegBackL ]
		self.SubRigs += [ self.TubeRampPistonR , self.TubeRampPistonL ]	


		self.SubRigsName += [ 'RampHolderR'  , 'RampHolderL'  ]
		self.SubRigsName += [ 'RampPistonR'  , 'RampPistonL'  ]
		self.SubRigsName += [ 'TopDamperAR'  , 'TopDamperAL'  ]
		self.SubRigsName += [ 'TopDamperBR'  , 'TopDamperBL'  ]
		self.SubRigsName += [ 'TopDamperCR'  , 'TopDamperCL'  ]
		self.SubRigsName += [ 'RampHolderSupportAR'  , 'RampHolderSupportAL'  ]
		self.SubRigsName += [ 'RampHolderSupportBR'  , 'RampHolderSupportBL'  ]
		self.SubRigsName += [ 'LegFrontR'    , 'LegFrontL'  ]
		self.SubRigsName += [ 'LegBackR'     , 'LegBackL'  ]
		self.SubRigsName += [ 'TubeRampPistonR' , 'TubeRampPistonL' ]	


		#CLASSE UTILS

		#UPDATE
		name = args.get( 'n'   , None )	
		pos  = args.get( 'pos' , None )
		if not( name == None ): self.Name.add( 'base' , copy = name ) 
		if not( pos  == None ): pass


       
class rigSkeletonQuadriPod_leg(rigPuppet):

	def __init__( self , **args ):
		rigPuppet.__init__( self , **args )
		#UTILS	
		#CLASSE
		self.classeType = 'leg'
		#NAME
		self.Name.add( 'base'            , baseName = self.classeType )		
		#INSTANCE_______________________________BLUEPRINT
		legLocs           = [x.encode('UTF8') for x in mc.ls('pos_leg?'                 , type = 'transform' )]
		legPistonLocs     = [x.encode('UTF8') for x in mc.ls('pos_legPiston?'           , type = 'transform' )]
		legToeLocs        = [x.encode('UTF8') for x in mc.ls('pos_legToe?'              , type = 'transform' )]
	
		tubeALocs         = [x.encode('UTF8') for x in mc.ls('pos_TubeLegA?'            , type = 'transform' )]
		tubeBRightLocs    = [x.encode('UTF8') for x in mc.ls('pos_TubeLegBRight?'       , type = 'transform' )]
		tubeBLeftLocs     = [x.encode('UTF8') for x in mc.ls('pos_TubeLegBLeft?'        , type = 'transform' )]
		tubeCLocs         = [x.encode('UTF8') for x in mc.ls('pos_TubeLegC?'            , type = 'transform' )]
		
		tubePistonALocs   = [x.encode('UTF8') for x in mc.ls('pos_TubeLegPistonA?'      , type = 'transform' )]
		tubePistonBLocs   = [x.encode('UTF8') for x in mc.ls('pos_TubeLegPistonB?'      , type = 'transform' )]
		tubePistonCLocs   = [x.encode('UTF8') for x in mc.ls('pos_TubeLegPistonC?'      , type = 'transform' )]
														
		tubeToeLocs       = [x.encode('UTF8') for x in mc.ls('pos_tubeLegToe?'          , type = 'transform' )]

		#NAME
		self.Name.add( 'base'            , baseName = self.classeType )
		self.Name.add( 'leg'             , ref = self.Name.base      , baseNameAppend = 'Base'    )
		self.Name.add( 'legPiston'       , ref = self.Name.base      , baseNameAppend = 'Piston'  )
		self.Name.add( 'legPistonA'      , ref = self.Name.legPiston , baseNameAppend = 'A'   )
		self.Name.add( 'legPistonB'      , ref = self.Name.legPiston , baseNameAppend = 'B'   )
		self.Name.add( 'legPistonC'      , ref = self.Name.legPiston , baseNameAppend = 'C'   )

		self.Name.add( 'tubeA'           , ref = self.Name.base      , baseNameAppend = 'tubeA' )
		self.Name.add( 'tubeBRight'      , ref = self.Name.base      , baseNameAppend = 'tubeBRight' )	
		self.Name.add( 'tubeBLeft'       , ref = self.Name.base      , baseNameAppend = 'tubeBLeft'  )			
		self.Name.add( 'tubeC'           , ref = self.Name.base      , baseNameAppend = 'tubeC' )	

		self.Name.add( 'tubePistonA'     , ref = self.Name.base      , baseNameAppend = 'tubePistonA' )
		self.Name.add( 'tubePistonB'     , ref = self.Name.base      , baseNameAppend = 'tubePistonB' )	
		self.Name.add( 'tubePistonC'     , ref = self.Name.base      , baseNameAppend = 'tubePistonC' )		
		
		self.Name.add( 'legToe'          , ref = self.Name.base      , baseNameAppend = 'Toe'     )
		self.Name.add( 'tubeToe'         , ref = self.Name.base      , baseNameAppend = 'tubeToe' )			
		#SUBRIG

		#LEG CTRLS
		parent  = args.get( 'parent' , self.Name.topNode  )

		self.Leg        = rigSkeletonChain( n = self.Name.leg         , pos = legLocs            , parent = parent           )
		self.LegPistonA = rigSkeletonChain( n = self.Name.legPistonA  , pos = legPistonLocs[0:2] , parent = parent           )
		self.LegPistonB = rigSkeletonChain( n = self.Name.legPistonB  , pos = legPistonLocs[2:4] , parent = self.Leg.outs[0] )
		self.LegPistonC = rigSkeletonChain( n = self.Name.legPistonC  , pos = legPistonLocs[4:6] , parent = self.Leg.outs[1] )

		self.TubeA      = rigSkeletonChain( n = self.Name.tubeA      , pos = tubeALocs       , parent = parent           )
		self.TubeBRight = rigSkeletonChain( n = self.Name.tubeBRight , pos = tubeBRightLocs  , parent = self.Leg.outs[0] )
		self.TubeBLeft  = rigSkeletonChain( n = self.Name.tubeBLeft  , pos = tubeBLeftLocs   , parent = self.Leg.outs[0] )
		self.TubeC      = rigSkeletonChain( n = self.Name.tubeC      , pos = tubeCLocs       , parent = parent )

		self.TubePistonA = rigSkeletonChain( n = self.Name.tubePistonA  , pos = tubePistonALocs , parent = parent           )
		self.TubePistonB = rigSkeletonChain( n = self.Name.tubePistonB  , pos = tubePistonBLocs , parent = self.Leg.outs[0] )
		self.TubePistonC = rigSkeletonChain( n = self.Name.tubePistonC  , pos = tubePistonCLocs , parent = self.Leg.outs[1] )

		self.SubRigs     += [ self.Leg  , self.LegPistonA , self.LegPistonB  , self.LegPistonC ]
		self.SubRigsName += [     'Leg' ,     'LegPistonA',     'LegPistonB' ,     'LegPistonC']

		self.SubRigs     += [ self.TubeA  , self.TubeBRight , self.TubeBLeft  , self.TubeC ]
		self.SubRigsName += [     'TubeA' ,     'TubeBRight',     'TubeBLeft' ,     'TubeC']

		self.SubRigs     += [ self.TubePistonA  , self.TubePistonB , self.TubePistonC ]
		self.SubRigsName += [     'TubePistonA' ,     'TubePistonB',     'TubePistonC']

		#TOE CTRLS
		self.Toe     = rigSkeletonChain( n = self.Name.legToe  , pos = legToeLocs  , parent = self.Leg.outs[2]    )
		self.TubeToe = rigSkeletonChain( n = self.Name.tubeToe , pos = tubeToeLocs , parent = self.Leg.outs[2]    )

		#MIRROR
		toeRotation = {}
		toeRotation['value']             = [0,0,0 , 0,90,0 , 1,1,1 , 4]
		toeRotation['mode']              = 'transform'
		toeRotation['pivot']             = [ -1.506 , -0.019 , 1.588 , 0,0,0 , 1,1,1]
		toeRotation['namePrefix']        = []
		toeRotation['nameReplace']       = []
		toeRotation['nameIncr']          = 'toeA'
		toeRotation['nameAdd']           = []
		toeRotation['noneMirrorAxe']     = 4

		self.Toe1     , self.Toe2     , self.Toe3     , self.Toe4     = self.Toe.duplicate(     **toeRotation )
		self.TubeToe1 , self.TubeToe2 , self.TubeToe3 , self.TubeToe4 = self.TubeToe.duplicate( **toeRotation )

		self.SubRigs     += [ self.Toe1  , self.Toe2 , self.Toe3  , self.Toe4 ]
		self.SubRigsName += [     'Toe1' ,     'Toe2',     'Toe3' ,     'Toe4']

		self.SubRigs     += [ self.TubeToe1  , self.TubeToe2 , self.TubeToe3  , self.TubeToe4 ]
		self.SubRigsName += [     'TubeToe1' ,     'TubeToe2',     'TubeToe3' ,     'TubeToe4']

		#LINKS
		'''
		self.Link.add( 'paRootA' , Sources = [ self.Root.outs[0] ] , Destinations = [ self.Leg.ins[0]     ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )	

		self.Link.add( 'paRootB' , Sources = [ self.Root.outs[0] ] , Destinations = [ self.Leg.ins[0] , self.LegPistonA.ins[0]        ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )	
		self.Link.add( 'paLegA' , Sources = [ self.Leg.outs[1] ] , Destinations = [ self.LegPistonA.ins[1] , self.LegPistonB.ins[0] ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )	
		self.Link.add( 'paLegB' , Sources = [ self.Leg.outs[2] ] , Destinations = [ self.LegPistonC.ins[0]                          ], type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )	
		self.Link.add( 'paLegC' , Sources = [ self.Leg.outs[3] ] , Destinations = [ self.LegPistonB.ins[1] , self.LegPistonC.ins[1] ], type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )	
		self.Link.add( 'paToe'  , Sources = [ self.Leg.outs[3] ] , Destinations = [ self.Toe1.ins[0] , self.Toe2.ins[0] , self.Toe3.ins[0] , self.Toe4.ins[0] ], type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )	
		'''		
		#CLASSE UTILS
		self.ins = []
		self.outs = []		
		#CLASSE MODIF
		#INSTANCE MODIF
		name = args.get( 'n'   , None )	
		pos  = args.get( 'pos' , None )
		if not( name == None ): self.Name.add( 'base' , copy = name ) 
		if not( pos  == None ): pass

