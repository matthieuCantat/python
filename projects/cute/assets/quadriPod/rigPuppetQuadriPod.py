
	
'''





############################################################################ BUILD RIG PUPPET

import maya.cmds as mc
import python
from python.projects.cute.assets.quadriPod.rigPuppetQuadriPod import *
reload( python.projects.cute.assets.quadriPod.rigPuppetQuadriPod)

#____________________________________________________________________________LOAD SKELETON
from python.classe.readWriteInfo import *
reload(python.classe.readWriteInfo)
rwi = readWriteInfo()
rwi.mayaScene_load( 'D:/mcantat_BDD/projects/cute/assets/quadriPod/maya/scenes/quadriPod_rigBoundB.ma' , open = True )
#____________________________________________________________________________LOAD SKELETON

#BUILD
puppet = rigPuppetQuadriPod()	
puppet.debug = 1
toExec = puppet.build()
exec(toExec)

#____________________________________________________________________________LOAD SHAPE
from python.utils.utilsRigPuppet import *
reload( python.utils.utilsRigPuppet )
path = 'D:/mcantat_BDD/projects/cute/assets/quadriPod/maya/scenes/quadriPod_utils_ctrlShape.ma'
rigPuppet_importAndReplaceCtrlShape( path , adjustPosition = False )
#rwi.mayaScene_save( path )
#____________________________________________________________________________LOAD SHAPE


#CLEAN ROOT 
toKeep = ['rigPuppet_GRP']
rootElem = mc.ls("|*" , type = "transform")
rootElem = [ elem for elem in rootElem if not (elem in toKeep ) ]
mc.delete(rootElem)


#createSwitchVisibility
driver = 'traj_CTRL'
meshes = mc.ls('|rigPuppet_GRP|*_GEO')

from python.utils.utilsMaya import *

attr = addSpecialAttr( driver , 'ctrlVis'  , 'int+' , 9 , attrKeyable = False , attrCb  = True , attrLock  =  False )
mc.connectAttr( attr ,'rigPuppet_GRP.ctrlVis')

mc.setAttr( "pos0_JNT.v" , 0 )

pathSave = 'D:/mcantat_BDD/projects/cute/assets/quadriPod/maya/scenes/quadriPod_rigPuppet.ma'
addSpecialAttr( driver , 'path'  , 'string' , pathSave , attrKeyable = False , attrCb  = False , attrLock  =  False )

#____________________________________________________________________________SAVE TO RIG PUPPET
rwi.mayaScene_save( 'D:/mcantat_BDD/projects/cute/assets/quadriPod/maya/scenes/quadriPod_rigPuppet.ma' )
#____________________________________________________________________________SAVE TO RIG PUPPET



'''


import maya.cmds as mc

from .....classe.rigPuppet import *  
from .....classe.rigCtrl import *  
from .....classe.rigModuleChain import *     
from .....classe.rigModuleArm import *    
from .....classe.rigModulePiston import *  
from .....classe.rigModuleProjector import *
from .....classe.rigModuleRotatingBeacon import *


       
class rigPuppetQuadriPod(rigPuppet):

	def __init__( self , **args ):
		rigPuppet.__init__( self , **args )
		#UTILS	
		#CLASSE

		self.classeType = 'rigPuppetQuadriPod'
		#NAME
		self.Name.add( 'quadri' , baseName = self.classeType    , type = 'GRP' )			
		#INSTANCE_______________________________BLUEPRINT
		posLocs         = ['pos0_JNT']
		trajLocs        = ['traj0_JNT']
		bodyLocs        = ['body0_JNT']
		feetsLocs       = ['feets0_JNT']
		rampLocs        = ['ramp0_JNT']
		fanLocs         = ['fan0_JNT']
		pumpLocs        = [x.encode('UTF8') for x in mc.ls('pump?0_JNT' , type = 'joint' )]

		rampHolderLocs         = ['r_rampHolder0_JNT']
		rampPistonLocs         = [x.encode('UTF8') for x in mc.ls('r_rampPiston?_JNT'         , type = 'joint' )]
		topDamperLocs          = [x.encode('UTF8') for x in mc.ls('r_topDamper?0_JNT'         , type = 'joint' )]
		rampHolderSupportALocs = [x.encode('UTF8') for x in mc.ls('r_rampHolderSupportA?_JNT' , type = 'joint' )]		
		rampHolderSupportBLocs = [x.encode('UTF8') for x in mc.ls('r_rampHolderSupportB?_JNT' , type = 'joint' )]

		tubeRampPistonLocs     = [x.encode('UTF8') for x in mc.ls('r_tubeRampPiston?_JNT'    , type = 'joint' )]
		tubeReserveLocs        = [x.encode('UTF8') for x in mc.ls('tubeReserve?_JNT'         , type = 'joint' )]

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
		self.Position = rigCtrl(  n = self.Name.pos    , pos = posLocs  , form = 'plane'       , colors = ['yellow'] , ctrlVisPriority = 2  , parent  = self.Name.topNode )
		self.Traj     = rigCtrl(  n = self.Name.traj  , pos = trajLocs  , form = 'crossArrow'  , colors = ['yellow'] , ctrlVisPriority = 2  , parent  = self.Name.topNode , attrStates = [['t','r']] )
		self.Body     = rigCtrl(  n = self.Name.body  , pos = bodyLocs  , form = 'crossArrow'  , colors = ['green']  , ctrlVisPriority = 2  , parent  = self.Name.topNode , attrStates = [['t','r']] )
		self.Feets    = rigCtrl(  n = self.Name.feets , pos = feetsLocs , form = 'circle'      , colors = ['red']    , ctrlVisPriority = 2  , parent  = self.Name.topNode , attrStates = [['t','r']] )

		self.Ramp  = rigCtrl(  n = self.Name.ramp   , pos = rampLocs      , form = 'arrow2sidesBend'  , colors = ['red']  , ctrlVisPriority = 2  , parent  = self.Name.topNode , attrStates = [['rz']] )
		self.Fan   = rigCtrl(  n = self.Name.fan    , pos = fanLocs       , form = 'arrow2sidesBend'  , colors = ['red']  , ctrlVisPriority = 2  , parent  = self.Name.topNode , attrStates = [['rz']] )
		self.PumpA = rigCtrl(  n = self.Name.pumpA  , pos = [pumpLocs[0]] , form = 'arrow2sides'      , colors = ['red']  , ctrlVisPriority = 2  , parent  = self.Name.topNode , attrStates = [['tx']] )
		self.PumpB = rigCtrl(  n = self.Name.pumpB  , pos = [pumpLocs[1]] , form = 'arrow2sides'      , colors = ['red']  , ctrlVisPriority = 2  , parent  = self.Name.topNode , attrStates = [['tx']] )

		self.TubeReserve = rigCtrl( n = self.Name.tubeReserve  , pos =  tubeReserveLocs  , form = 'sphere'  , colors = ['red']  , ctrlVisPriority = 3  , parent  = self.Name.topNode , attrStates = [['t']] )

		self.SubRigs     += [ self.Position , self.Traj , self.Body , self.Feets , self.Ramp , self.Fan , self.PumpA , self.PumpB , self.TubeReserve  ]		
		self.SubRigsName += [     'Position' ,    'Traj',     'Body',     'Feets',     'Ramp',     'Fan',     'PumpA',     'PumpB',     'TubeReserve' ]	

		#SIDES CTRLS
		self.RampHolder  = rigCtrl(         n = self.Name.rampHolder  , pos = rampHolderLocs      , form = 'arrow2sidesBend'  , colors = ['red'] , modif = True , ctrlVisPriority = 2  , parent  = self.Name.topNode , attrStates = [['rz']])
		self.RampPiston  = rigModulePiston( n = self.Name.rampPiston  , pos = rampPistonLocs      , form = 'circle'           , colors = ['red']           , ctrlVisPriority = 2  , attrStates = [['']])
		self.TopDamperA  = rigCtrl(         n = self.Name.topDamperA  , pos = [topDamperLocs[0]]  , form = 'arrow2sides'      , colors = ['red']           , ctrlVisPriority = 2  , parent  = self.Name.topNode , attrStates = [['tx']] )
		self.TopDamperB  = rigCtrl(         n = self.Name.topDamperB  , pos = [topDamperLocs[1]]  , form = 'arrow2sides'      , colors = ['red']           , ctrlVisPriority = 2  , parent  = self.Name.topNode , attrStates = [['tx']] )
		self.TopDamperC  = rigCtrl(         n = self.Name.topDamperC  , pos = [topDamperLocs[2]]  , form = 'arrow2sides'      , colors = ['red']           , ctrlVisPriority = 2  , parent  = self.Name.topNode , attrStates = [['tx']] )
		self.RampHolderSupportA = rigModulePiston( n = self.Name.rampHolderSupportA  , pos = rampHolderSupportALocs , form = 'circle'      , colors = ['red']  , ctrlVisPriority = 2  , attrStates = [['']])
		self.RampHolderSupportB = rigModulePiston( n = self.Name.rampHolderSupportB  , pos = rampHolderSupportBLocs , form = 'circle'      , colors = ['red']  , ctrlVisPriority = 2  , attrStates = [['']])

		self.TubeRampPiston     = rigModuleArm( n = self.Name.tubeRampPiston , pos = tubeRampPistonLocs , ik = True , pv = True , ctrlVisPriority = 8 ,  attrStates = [['']] )

		#SUBRIG
		self.Leg = rigPuppetQuadriPod_leg(   n = self.Name.leg   , ctrlVisPriority = 1  )

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
		self.SubRigs += [ self.TubeRampPistonR     , self.TubeRampPistonL ]	


		self.SubRigsName += [ 'RampHolderR'  , 'RampHolderL'  ]
		self.SubRigsName += [ 'RampPistonR'  , 'RampPistonL'  ]
		self.SubRigsName += [ 'TopDamperAR'  , 'TopDamperAL'  ]
		self.SubRigsName += [ 'TopDamperBR'  , 'TopDamperBL'  ]
		self.SubRigsName += [ 'TopDamperCR'  , 'TopDamperCL'  ]
		self.SubRigsName += [ 'RampHolderSupportAR'  , 'RampHolderSupportAL'  ]
		self.SubRigsName += [ 'RampHolderSupportBR'  , 'RampHolderSupportBL'  ]
		self.SubRigsName += [ 'LegFrontR'    , 'LegFrontL' ]
		self.SubRigsName += [ 'LegBackR'     , 'LegBackL'  ]
		self.SubRigsName += [ 'TubeRampPistonR'     , 'TubeRampPistonL'  ]

		#LINKS
		self.Link.add( 'feets'           , Sources = [ self.Feets.outs[0]        ] , Destinations = [ self.LegFrontR.ins[1] , self.LegFrontL.ins[1] , self.LegBackR.ins[1] , self.LegBackL.ins[1] ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )	

		self.Link.add( 'ramp'            , Sources = [ self.Ramp.outs[0]         ] , Destinations = [ self.RampPistonR.ins[1] , self.RampPistonL.ins[1] , self.RampHolderSupportAR.ins[1] , self.RampHolderSupportBR.ins[1] , self.RampHolderSupportAL.ins[1] , self.RampHolderSupportBL.ins[1] ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )	
		self.Link.add( 'bodyRamp'        , Sources = [ self.Body.outs[0]         ] , Destinations = [ self.RampHolderR.ins[1] , self.RampHolderL.ins[1] ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 , skipAxes = [0,0,0 , 1,1,1 , 0,0,0] )	
		self.Link.add( 'rampHolderR'     , Sources = [ self.RampHolderR.outs[0]  ] , Destinations = [ self.RampHolderSupportAR.ins[0] , self.RampHolderSupportBR.ins[0] ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )	
		self.Link.add( 'rampHolderL'     , Sources = [ self.RampHolderL.outs[0]  ] , Destinations = [ self.RampHolderSupportAL.ins[0] , self.RampHolderSupportBL.ins[0] ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1  )	
		self.Link.add( 'TubeRampPistonR' , Sources = [ self.RampPistonR.outs[0]  ] , Destinations = [ self.TubeRampPistonR.ins[1] ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )	
		self.Link.add( 'TubeRampPistonL' , Sources = [ self.RampPistonL.outs[0]  ] , Destinations = [ self.TubeRampPistonL.ins[1] ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )	
		#CLASSE UTILS

		#UPDATE
		name = args.get( 'n'   , None )	
		pos  = args.get( 'pos' , None )
		if not( name == None ): self.Name.add( 'base' , copy = name ) 
		if not( pos  == None ): pass


       
class rigPuppetQuadriPod_leg(rigPuppet):

	def __init__( self , **args ):
		rigPuppet.__init__( self , **args )
		#UTILS	
		#CLASSE
		self.classeType = 'rigPuppetQuadriPodLeg'
		#NAME
		self.Name.add( 'base'            , baseName = self.classeType )		
		#INSTANCE_______________________________BLUEPRINT
		legLocs                = [x.encode('UTF8') for x in mc.ls('r_leg0Base?_JNT'     , type = 'joint' )]
		legPistonALocs         = [x.encode('UTF8') for x in mc.ls('r_leg0PistonA?_JNT'  , type = 'joint' )]
		legPistonBLocs         = [x.encode('UTF8') for x in mc.ls('r_leg0PistonB?_JNT'  , type = 'joint' )]
		legPistonCLocs         = [x.encode('UTF8') for x in mc.ls('r_leg0PistonC?_JNT'  , type = 'joint' )]

		legToeLocs             = [x.encode('UTF8') for x in mc.ls('r_leg0ToeA?_JNT'     , type = 'joint' )]

		tubeALocs         = [x.encode('UTF8') for x in mc.ls('r_leg0TubeA?_JNT'            , type = 'joint' )]
		tubeBRightLocs    = [x.encode('UTF8') for x in mc.ls('r_leg0TubeBRight?_JNT'       , type = 'joint' )]
		tubeBLeftLocs     = [x.encode('UTF8') for x in mc.ls('r_leg0TubeBLeft?_JNT'        , type = 'joint' )]
		tubeCLocs         = [x.encode('UTF8') for x in mc.ls('r_leg0TubeC?_JNT'            , type = 'joint' )]
		
		tubePistonALocs   = [x.encode('UTF8') for x in mc.ls('r_leg0TubePistonA?_JNT'      , type = 'joint' )]
		tubePistonBLocs   = [x.encode('UTF8') for x in mc.ls('r_leg0TubePistonB?_JNT'      , type = 'joint' )]
		tubePistonCLocs   = [x.encode('UTF8') for x in mc.ls('r_leg0TubePistonC?_JNT'      , type = 'joint' )]
														
		tubeToeLocs       = [x.encode('UTF8') for x in mc.ls('r_leg0TubeToeA?_JNT'          , type = 'joint' )]


		#NAME
		self.Name.add( 'base'            , baseName = self.classeType )
		self.Name.add( 'leg'             , ref = self.Name.base      , baseNameAppend = 'Base'    )
		self.Name.add( 'legPiston'       , ref = self.Name.base      , baseNameAppend = 'Piston'  )
		self.Name.add( 'legPistonA'      , ref = self.Name.legPiston , baseNameAppend = 'A'   )
		self.Name.add( 'legPistonB'      , ref = self.Name.legPiston , baseNameAppend = 'B'   )
		self.Name.add( 'legPistonC'      , ref = self.Name.legPiston , baseNameAppend = 'C'   )
		
		self.Name.add( 'legToe'          , ref = self.Name.base      , baseNameAppend = 'Toe'  )			

		self.Name.add( 'tubeA'           , ref = self.Name.base      , baseNameAppend = 'tubeA' )
		self.Name.add( 'tubeBRight'      , ref = self.Name.base      , baseNameAppend = 'tubeBRight' )	
		self.Name.add( 'tubeBLeft'       , ref = self.Name.base      , baseNameAppend = 'tubeBLeft'  )			
		self.Name.add( 'tubeC'           , ref = self.Name.base      , baseNameAppend = 'tubeC' )	

		self.Name.add( 'tubePistonA'     , ref = self.Name.base      , baseNameAppend = 'tubePistonA' )
		self.Name.add( 'tubePistonB'     , ref = self.Name.base      , baseNameAppend = 'tubePistonB' )	
		self.Name.add( 'tubePistonC'     , ref = self.Name.base      , baseNameAppend = 'tubePistonC' )		
		
		self.Name.add( 'legToe'          , ref = self.Name.base      , baseNameAppend = 'Toe'     )
		self.Name.add( 'tubeToe'         , ref = self.Name.base      , baseNameAppend = 'tubeToe' )		

		#LEG CTRLS
		self.Leg        = rigModuleArm(    n = self.Name.leg         , pos = legLocs        , fk = True  , ik = True  , ctrlVisPriority = 3  , attrStates = [ ['t','r'] , ['rz'] ]	 )
		self.LegPistonA = rigModulePiston( n = self.Name.legPistonA  , pos = legPistonALocs , form = 'circle' , colors = ['red']  , ctrlVisPriority = 2  , attrStates = [['']])
		self.LegPistonB = rigModulePiston( n = self.Name.legPistonB  , pos = legPistonBLocs , form = 'circle' , colors = ['red']  , ctrlVisPriority = 2  , attrStates = [['']])
		self.LegPistonC = rigModulePiston( n = self.Name.legPistonC  , pos = legPistonCLocs , form = 'circle' , colors = ['red']  , ctrlVisPriority = 2  , attrStates = [['']])

		self.SubRigs     += [ self.Leg  , self.LegPistonA , self.LegPistonB  , self.LegPistonC ]
		self.SubRigsName += [ 'Leg'     , 'LegPistonA'    , 'LegPistonB'     , 'LegPistonC'    ]

		self.TubeA      = rigModuleArm( n = self.Name.tubeA      , pos = tubeALocs       , ik = True , pv = True , ctrlVisPriority = 8 ,  attrStates = [['']] )
		self.TubeBRight = rigModuleArm( n = self.Name.tubeBRight , pos = tubeBRightLocs  , ik = True , pv = True , ctrlVisPriority = 8 ,  attrStates = [['']] )
		self.TubeBLeft  = rigModuleArm( n = self.Name.tubeBLeft  , pos = tubeBLeftLocs   , ik = True , pv = True , ctrlVisPriority = 8 ,  attrStates = [['']] )
		self.TubeC      = rigModuleArm( n = self.Name.tubeC      , pos = tubeCLocs       , ik = True , pv = True , ctrlVisPriority = 8 ,  attrStates = [['']] )

		self.TubePistonA = rigModuleArm( n = self.Name.tubePistonA  , pos = tubePistonALocs , ik = True , pv = True , ctrlVisPriority = 8 ,  attrStates = [['']] )
		self.TubePistonB = rigModuleArm( n = self.Name.tubePistonB  , pos = tubePistonBLocs , ik = True , pv = True , ctrlVisPriority = 8 ,  attrStates = [['']] )
		self.TubePistonC = rigModuleArm( n = self.Name.tubePistonC  , pos = tubePistonCLocs , ik = True , pv = True , ctrlVisPriority = 8 ,  attrStates = [['']] )

		self.SubRigs     += [ self.TubeA  , self.TubeBRight , self.TubeBLeft  , self.TubeC ]
		self.SubRigsName += [     'TubeA' ,     'TubeBRight',     'TubeBLeft' ,     'TubeC']

		self.SubRigs     += [ self.TubePistonA  , self.TubePistonB , self.TubePistonC ]
		self.SubRigsName += [     'TubePistonA' ,     'TubePistonB',     'TubePistonC']

		#TOE CTRLS
		self.Toe     = rigModuleChain(  n = self.Name.legToe  , pos = legToeLocs  , form = 'plane' , colors = ['red']  , ctrlVisPriority = 5 , trsv = False , attrStates = [['rz']])
		self.TubeToe = rigModuleArm(    n = self.Name.tubeToe , pos = tubeToeLocs , ik = True , pv = True , ctrlVisPriority = 8 ,  attrStates = [['']] )


		argsToeRotation = {}
		argsToeRotation['value']             = [0,0,0 , 0,90,0 , 1,1,1 , 4]
		argsToeRotation['mode']              = 'transform'
		argsToeRotation['pivot']             = [ -1.506 , -0.019 , 1.588 , 0,0,0 , 1,1,1]
		argsToeRotation['namePrefix']        = []
		argsToeRotation['nameReplace']       = []
		argsToeRotation['nameIncr']          = 'toeA'
		argsToeRotation['nameAdd']           = []
		argsToeRotation['noneMirrorAxe']     = 4
		argsToeRotation['debug']             = self.debug		
				
		self.Toe1     , self.Toe2     , self.Toe3     , self.Toe4     = self.Toe.duplicate(     **argsToeRotation )
		self.TubeToe1 , self.TubeToe2 , self.TubeToe3 , self.TubeToe4 = self.TubeToe.duplicate( **argsToeRotation )

		self.SubRigs     += [ self.Toe1  , self.Toe2 , self.Toe3  , self.Toe4 ]
		self.SubRigsName += [     'Toe1' ,     'Toe2',     'Toe3' ,     'Toe4']

		self.SubRigs     += [ self.TubeToe1  , self.TubeToe2 , self.TubeToe3  , self.TubeToe4 ]
		self.SubRigsName += [     'TubeToe1' ,     'TubeToe2',     'TubeToe3' ,     'TubeToe4']

		#LINKS
		self.Link.add( 'leg0' , Sources = [ self.Leg.outs[0] ] , Destinations = [ self.LegPistonA.ins[1]                          ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )	
		self.Link.add( 'leg2' , Sources = [ self.Leg.outs[2] ] , Destinations = [ self.LegPistonB.ins[1] , self.LegPistonC.ins[1] ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )	


		self.Link.add( 'TubeA'       , Sources = [ self.Leg.outs[0]        ] , Destinations = [ self.TubeA.ins[1]       ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )	
		self.Link.add( 'TubeBRight'  , Sources = [ self.Leg.outs[1]        ] , Destinations = [ self.TubeBRight.ins[1]  ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )	
		self.Link.add( 'TubeBLeft'   , Sources = [ self.Leg.outs[1]        ] , Destinations = [ self.TubeBLeft.ins[1]   ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )	
		self.Link.add( 'TubeC'       , Sources = [ self.Leg.outs[0]        ] , Destinations = [ self.TubeC.ins[1]       ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )	
		self.Link.add( 'TubePistonA' , Sources = [ self.LegPistonA.outs[0] ] , Destinations = [ self.TubePistonA.ins[1] ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )	
		self.Link.add( 'TubePistonB' , Sources = [ self.LegPistonB.outs[0] ] , Destinations = [ self.TubePistonB.ins[1] ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )			
		self.Link.add( 'TubePistonC' , Sources = [ self.LegPistonC.outs[0] ] , Destinations = [ self.TubePistonC.ins[1] ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )	

		self.Link.add( 'tubeToe1' , Sources = [ self.Toe1.outs[1] ] , Destinations = [ self.TubeToe1.ins[1] ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )	
		self.Link.add( 'tubeToe2' , Sources = [ self.Toe2.outs[1] ] , Destinations = [ self.TubeToe2.ins[1] ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )	
		self.Link.add( 'tubeToe3' , Sources = [ self.Toe3.outs[1] ] , Destinations = [ self.TubeToe3.ins[1] ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )	
		self.Link.add( 'tubeToe4' , Sources = [ self.Toe4.outs[1] ] , Destinations = [ self.TubeToe4.ins[1] ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )	




		#CLASSE UTILS
		self.ins   = [ self.Leg.ins[0]  , self.Leg.ins[1] , self.LegPistonA.ins[0] ]
		self.outs  = []			
		#CLASSE MODIF
		#INSTANCE MODIF
		name = args.get( 'n'   , None )	
		pos  = args.get( 'pos' , None )
		if not( name == None ): self.Name.add( 'base' , copy = name ) 
		if not( pos  == None ): pass

