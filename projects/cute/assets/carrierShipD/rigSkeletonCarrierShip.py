
'''




############################################################################ BUILD SKELETON
import maya.cmds as mc
import python
from    python.projects.cute.assets.carrierShipD.rigSkeletonCarrierShip import *
reload( python.projects.cute.assets.carrierShipD.rigSkeletonCarrierShip          )
reload( python.projects.cute.assets.carrierShipD.rigSkeletonCarrierShip_damp     )
reload( python.projects.cute.assets.carrierShipD.rigSkeletonCarrierShip_hook     )
reload( python.projects.cute.assets.carrierShipD.rigSkeletonCarrierShip_reactor  )
reload( python.projects.cute.assets.carrierShipD.rigSkeletonCarrierShip_propulsor)

#___________________________________________________________________________LOAD RIG BASE
from python.classe.readWriteInfo import *
reload(python.classe.readWriteInfo)
rwi = readWriteInfo()
rwi.mayaScene_load( 'D:/mcantat_BDD/projects/cute/assets/carrierShipD/maya/scenes/carrierShipD_rigBase.ma', open = True  )
#___________________________________________________________________________LOAD RIG BASE

#BUILD
puppet = rigSkeletonCarrierShip()	
puppet.printBuild = 1
toExec = puppet.build()
exec(toExec)


#CLEAN ROOT 
toKeep = ['all_GRP','rigPuppet_GRP','symPlane_reactor1','symPlane_hook1','symPlane_damp1']
rootElem = mc.ls("|*" , type = "transform")
rootElem = [ elem for elem in rootElem if not (elem in toKeep ) ]
mc.delete(rootElem)


#___________________________________________________________________________SAVE TO SKELETON
rwi.mayaScene_save( 'D:/mcantat_BDD/projects/cute/assets/carrierShipD/maya/scenes/carrierShipD_rigSkeleton.ma' )
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

from .rigSkeletonCarrierShip_reactor import *  
from .rigSkeletonCarrierShip_hook import *   
from .rigSkeletonCarrierShip_propulsor import *  
from .rigSkeletonCarrierShip_damp import * 


       
class rigSkeletonCarrierShip(rigPuppet):

	def __init__( self , **args ):
		rigPuppet.__init__( self , **args )
		#UTILS	
		#CLASSE
		self.classeType = 'rigSkeletonCarrierShip'
		self.doTubes = args.get( 'tubes' , None )
		#NAME
		self.Name.add( 'carrier' , baseName = self.classeType    , type = 'GRP' )			
		#INSTANCE_______________________________BLUEPRINT
		posLocs         = ['pos_pos1']
		trajLocs        = ['pos_traj1']
		bodyLocs        = ['pos_body1']
		reactorsLocs    = ['pos_reactors1']
		hooksPlugsLocs  = ['pos_hooksPlugs1']
		projsCenterLocs = ['pos_projsCenter1']
		projsFrontLocs  = ['pos_projsFront1']

		dampBaseLocs          = [x.encode('UTF8') for x in mc.ls('pos_dampBase?'        , type = 'transform' )]
		dampContactLocs       = ['pos_dampContact1']
		dampGiroLocs          = ['pos_dampGiro1']
		dampClosePanelALocs   = ['pos_dampClosePanelA1']
		dampClosePanelBLocs   = ['pos_dampClosePanelB1']

		giroLocs              = [x.encode('UTF8') for x in mc.ls('pos_giro?'       , type = 'transform' )]		
		projLocs              = [x.encode('UTF8') for x in mc.ls('pos_projRot*'    , type = 'transform' )]



		mirrorPlane            = [0,0,0 , 0,1,0 , 0,0,1 ]
		translateInfo          = [0,0, -0.823 , 0, -28.847,0 , 1,1,1 ]

		#CLASSE BLUE PRINT
		self.Name.add( 'pos'               , baseName = 'pos'           )
		self.Name.add( 'traj'              , baseName = 'traj'          )	
		self.Name.add( 'body'              , baseName = 'body'          )
		self.Name.add( 'reactors'          , baseName = 'reactors'      )
		self.Name.add( 'hooksPlugs'        , baseName = 'hooksPlugs'    )
		self.Name.add( 'projsCenter'       , baseName = 'projsCenter'   )
		self.Name.add( 'projsFront'        , baseName = 'projsFront'    )
		self.Name.add( 'reactor'           , baseName = 'reactor'       )
		self.Name.add( 'hook'              , baseName = 'hook'          )
		self.Name.add( 'propulsor'         , baseName = 'propulsor'     )
		self.Name.add( 'damp'              , baseName = 'damp'          )
		self.Name.add( 'rootB'             , baseName = 'damp'          )
		self.Name.add( 'coverSlide'        , baseName = 'damp'          )			
		self.Name.add( 'dampContact'       , ref = self.Name.damp , baseNameAppend = 'Contact'   )
		self.Name.add( 'dampBaseA'         , ref = self.Name.damp , baseNameAppend = 'BaseA'     )
		self.Name.add( 'dampBaseB'         , ref = self.Name.damp , baseNameAppend = 'BaseB'     )
		self.Name.add( 'dampBaseC'         , ref = self.Name.damp , baseNameAppend = 'BaseC'     )
		self.Name.add( 'dampGiro'          , ref = self.Name.damp , baseNameAppend = 'giro'      )
		self.Name.add( 'dampClosePanelA'   , ref = self.Name.damp , baseNameAppend = 'closePanelA' )
		self.Name.add( 'dampClosePanelB'   , ref = self.Name.damp , baseNameAppend = 'closePanelB' )

		self.Name.add( 'projector'  , baseName = 'projector' )
		self.Name.add( 'projectorA' , ref = self.Name.projector , baseNameAppend = 'A' )
		self.Name.add( 'projectorB' , ref = self.Name.projector , baseNameAppend = 'B' )
		self.Name.add( 'projectorC' , ref = self.Name.projector , baseNameAppend = 'C' )
		self.Name.add( 'projectorD' , ref = self.Name.projector , baseNameAppend = 'D' )
		self.Name.add( 'projectorE' , ref = self.Name.projector , baseNameAppend = 'E' )
		self.Name.add( 'projectorF' , ref = self.Name.projector , baseNameAppend = 'F' )

		self.Name.add( 'giro'       , baseName = 'giro' )	
		self.Name.add( 'giroA' , ref = self.Name.giro , baseNameAppend = 'A' )	
		self.Name.add( 'giroB' , ref = self.Name.giro , baseNameAppend = 'B' )	
		self.Name.add( 'giroC' , ref = self.Name.giro , baseNameAppend = 'C' )	
		self.Name.add( 'giroD' , ref = self.Name.giro , baseNameAppend = 'D' )	
		self.Name.add( 'giroE' , ref = self.Name.giro , baseNameAppend = 'E' )				

		#MAIN CTRLS
		print('MAIN CTRLS')
		self.Position    = rigSkeletonChain(  n = self.Name.pos         , pos = posLocs               , parent = self.Name.topNode      )			
		self.Traj        = rigSkeletonChain(  n = self.Name.traj        , pos = trajLocs              , parent = self.Position.outs[-1] )
		self.Body        = rigSkeletonChain(  n = self.Name.body        , pos = bodyLocs              , parent = self.Traj.outs[-1]     )
		self.Reactors    = rigSkeletonChain(  n = self.Name.reactors    , pos = reactorsLocs          , parent = self.Traj.outs[-1]     )
		self.HooksPlugs  = rigSkeletonChain(  n = self.Name.hooksPlugs  , pos = hooksPlugsLocs        , parent = self.Body.outs[-1]     )
		self.ProjsCenter = rigSkeletonChain(  n = self.Name.projsCenter , pos = projsCenterLocs       , parent = self.Body.outs[-1]     )
		self.ProjsFront  = rigSkeletonChain(  n = self.Name.projsFront  , pos = projsFrontLocs        , parent = self.Body.outs[-1]     )
		self.SubRigs     += [ self.Position  , self.Traj , self.Body , self.Reactors , self.HooksPlugs , self.ProjsCenter , self.ProjsFront  ]		
		self.SubRigsName += [     'Position'     , 'Traj'    , 'Body'    , 'Reactors'    , 'HooksPlugs'    , 'ProjsCenter'    , 'ProjsFront'  ]	

		#DAMP CTRLS
		print('DAMP CTRLS')
		self.DampRoot        = rigSkeletonChain(  n = self.Name.damp            , pos = dampContactLocs      , parent = self.Body.outs[-1]  )
		self.DampContact     = rigSkeletonChain(  n = self.Name.dampContact     , pos = dampContactLocs      , parent = self.DampRoot.outs[0]  )
		self.DampBaseA       = rigSkeletonChain(  n = self.Name.dampBaseA       , pos = [dampBaseLocs[0]]    , parent = self.DampRoot.outs[0]  )
		self.DampBaseB       = rigSkeletonChain(  n = self.Name.dampBaseB       , pos = [dampBaseLocs[1]]    , parent = self.DampRoot.outs[0]  )
		self.DampBaseC       = rigSkeletonChain(  n = self.Name.dampBaseC       , pos = [dampBaseLocs[2]]    , parent = self.DampRoot.outs[0]  )
		self.DampGiro        = rigSkeletonChain(  n = self.Name.dampGiro        , pos = dampGiroLocs         , parent = self.DampBaseC.outs[0] )
		self.DampClosePanelA = rigSkeletonChain(  n = self.Name.dampClosePanelA , pos = dampClosePanelALocs  , parent = self.DampRoot.outs[0] )
		self.DampClosePanelB = rigSkeletonChain(  n = self.Name.dampClosePanelB , pos = dampClosePanelBLocs  , parent = self.DampRoot.outs[0] )
		self.SubRigs     += [ self.DampRoot , self.DampContact , self.DampBaseA , self.DampBaseB , self.DampBaseC , self.DampGiro  , self.DampClosePanelA , self.DampClosePanelB ]		
		self.SubRigsName += [ 'DampRoot'    , 'DampContact'    , 'DampBaseA'    , 'DampBaseB'    , 'DampBaseC'    ,     'DampGiro' ,     'DampClosePanelA',     'DampClosePanelB']	

		#PROJECTOR CTRLS
		self.ProjectorA = rigSkeletonChain( n = self.Name.projectorA , pos = [projLocs[0]]  , parent = self.Body.outs[-1] )
		self.ProjectorB = rigSkeletonChain( n = self.Name.projectorB , pos = [projLocs[1]]  , parent = self.Body.outs[-1] )
		self.ProjectorC = rigSkeletonChain( n = self.Name.projectorC , pos = [projLocs[2]]  , parent = self.Body.outs[-1] )	
		self.ProjectorD = rigSkeletonChain( n = self.Name.projectorD , pos = [projLocs[3]]  , parent = self.Body.outs[-1] )	
		self.ProjectorE = rigSkeletonChain( n = self.Name.projectorE , pos = [projLocs[4]]  , parent = self.Body.outs[-1] )
		self.ProjectorF = rigSkeletonChain( n = self.Name.projectorF , pos = [projLocs[5]]  , parent = self.Body.outs[-1] )
		
		#GIRO CTRLS
		self.GiroA = rigSkeletonChain( n = self.Name.giroA , pos = [giroLocs[0]]  , parent = self.Body.outs[-1] )
		self.GiroB = rigSkeletonChain( n = self.Name.giroB , pos = [giroLocs[1]]  , parent = self.Body.outs[-1] )
		self.GiroC = rigSkeletonChain( n = self.Name.giroC , pos = [giroLocs[2]]  , parent = self.Body.outs[-1] )	
		self.GiroD = rigSkeletonChain( n = self.Name.giroD , pos = [giroLocs[3]]  , parent = self.Body.outs[-1] )	
		self.GiroE = rigSkeletonChain( n = self.Name.giroE , pos = [giroLocs[4]]  , parent = self.Body.outs[-1] )

		#SUBRIG
		print('SUBRIG')
		self.Reactor   = rigSkeletonCarrierShip_reactor(   n = self.Name.reactor   , parent = self.Body.outs[-1]  )
		self.Hook      = rigSkeletonCarrierShip_hook(      n = self.Name.hook      , parent = self.Body.outs[-1]  )
		self.Propulsor = rigSkeletonCarrierShip_propulsor( n = self.Name.propulsor , parent = self.Body.outs[-1]  )
		self.Damp      = rigSkeletonCarrierShip_damp(      n = self.Name.damp      , parent = self.DampContact.outs[-1]  )
		
		print('MIRROR HOOK')
		argsTransformHook = {}
		argsTransformHook['value']             = translateInfo
		argsTransformHook['mode']              = 'transform'
		argsTransformHook['pivot']             = [0,0,0 , 0,0,0 , 1,1,1]
		argsTransformHook['namePrefix']        = []
		argsTransformHook['nameReplace']       = []
		argsTransformHook['nameIncr']          = 'hook0'
		argsTransformHook['nameAdd']           = []
		argsTransformHook['noneMirrorAxe']     = 4

		argsTransformHook['debug'] = self.debug

		self.HookFront , self.HookBack    = self.Hook.duplicate( **argsTransformHook )

		print('MIRROR DAMP')
		argsMirrorZ = {}
		argsMirrorZ['value']             = 'symPlane_damp1'
		argsMirrorZ['mode']              = 'mirror'
		argsMirrorZ['pivot']             = [0,0,0 , 0,0,0 , 1,1,1]
		argsMirrorZ['namePrefix']        = []
		argsMirrorZ['nameReplace']       = []
		argsMirrorZ['nameIncr']          = 'damp0'
		argsMirrorZ['nameAdd']           = []
		argsMirrorZ['noneMirrorAxe']     = 4

		argsMirrorZ['debug'] = self.debug


		self.DampFront , self.DampBack  = self.Damp.duplicate( **argsMirrorZ )

		print('MIRROR ALL')
		
		argsMirrorX = {}
		argsMirrorX['value']             = [0,0,0 , 0,1,0 , 0,0,1]
		argsMirrorX['mode']              = 'mirror'
		argsMirrorX['pivot']             = [0,0,0 , 0,0,0 , 1,1,1]
		argsMirrorX['namePrefix']        = ['r','l']
		argsMirrorX['nameReplace']       = []
		argsMirrorX['nameIncr']          = ''
		argsMirrorX['nameAdd']           = []
		argsMirrorX['noneMirrorAxe']     = 4

		argsMirrorX['debug'] = self.debug

		rigsToDuplicate = []
		rigsToDuplicate.append( self.Reactor    )
		rigsToDuplicate.append( self.HookFront  )
		rigsToDuplicate.append( self.HookBack   )
		rigsToDuplicate.append( self.Propulsor  )
		rigsToDuplicate.append( self.DampFront  )
		rigsToDuplicate.append( self.DampBack   )

		rigsToDuplicate.append( self.ProjectorA   )
		rigsToDuplicate.append( self.ProjectorB   )
		rigsToDuplicate.append( self.ProjectorC   )
		rigsToDuplicate.append( self.ProjectorD   )
		rigsToDuplicate.append( self.ProjectorE   )
		rigsToDuplicate.append( self.ProjectorF   )

		rigsToDuplicate.append( self.GiroA   )
		rigsToDuplicate.append( self.GiroB   )
		rigsToDuplicate.append( self.GiroC   )
		rigsToDuplicate.append( self.GiroD   )
		rigsToDuplicate.append( self.GiroE   )


		print('duplicateRigs IN')
		duplicated = self.duplicateRigs( argsMirrorX , rigsToDuplicate )
		print('duplicateRigs OUT')

		self.ReactorR   , self.ReactorL   = duplicated[0][0] , duplicated[0][1]
		self.HookFrontR , self.HookFrontL = duplicated[1][0] , duplicated[1][1]
		self.HookBackR  , self.HookBackL  = duplicated[2][0] , duplicated[2][1]
		self.PropulsorR , self.PropulsorL = duplicated[3][0] , duplicated[3][1]
		self.DampFrontR , self.DampFrontL = duplicated[4][0] , duplicated[4][1]
		self.DampBackR  , self.DampBackL  = duplicated[5][0] , duplicated[5][1]

		self.ProjectorAR  , self.ProjectorAL  = duplicated[6][0]  , duplicated[6][1] 
		self.ProjectorBR  , self.ProjectorBL  = duplicated[7][0]  , duplicated[7][1] 		
		self.ProjectorCR  , self.ProjectorCL  = duplicated[8][0]  , duplicated[8][1] 
		self.ProjectorDR  , self.ProjectorDL  = duplicated[9][0]  , duplicated[9][1] 
		self.ProjectorER  , self.ProjectorEL  = duplicated[10][0] , duplicated[10][1]
		self.ProjectorFR  , self.ProjectorFL  = duplicated[11][0] , duplicated[11][1]

		self.GiroAR  , self.GiroAL = duplicated[12][0]  , duplicated[12][1]
		self.GiroBR  , self.GiroBL = duplicated[13][0]  , duplicated[13][1]
		self.GiroCR  , self.GiroCL = duplicated[14][0]  , duplicated[14][1]
		self.GiroDR  , self.GiroDL = duplicated[15][0]  , duplicated[15][1]
		self.GiroER  , self.GiroEL = duplicated[16][0]  , duplicated[16][1]

		self.SubRigs += [ self.ReactorL   , self.ReactorR   ]
		self.SubRigs += [ self.HookFrontL , self.HookFrontR ]
		self.SubRigs += [ self.HookBackL  , self.HookBackR  ]
		self.SubRigs += [ self.PropulsorL , self.PropulsorR ]
		self.SubRigs += [ self.DampFrontR , self.DampFrontL ]
		self.SubRigs += [ self.DampBackR  , self.DampBackL  ]		

		self.SubRigs += [ self.ProjectorAR  , self.ProjectorAL  ]	
		self.SubRigs += [ self.ProjectorBR  , self.ProjectorBL  ]			
		self.SubRigs += [ self.ProjectorCR  , self.ProjectorCL  ]	
		self.SubRigs += [ self.ProjectorDR  , self.ProjectorDL  ]
		self.SubRigs += [ self.ProjectorER  , self.ProjectorEL  ]				
		self.SubRigs += [ self.ProjectorFR  , self.ProjectorFL  ]

		self.SubRigs += [ self.GiroAR  , self.GiroAL ]
		self.SubRigs += [ self.GiroBR  , self.GiroBL ]
		self.SubRigs += [ self.GiroCR  , self.GiroCL ]
		self.SubRigs += [ self.GiroDR  , self.GiroDL ]
		self.SubRigs += [ self.GiroER  , self.GiroEL ]		

		self.SubRigsName += [ 'ReactorL'    , 'ReactorR'   ]
		self.SubRigsName += [ 'HookFrontL'  , 'HookFrontR' ]
		self.SubRigsName += [ 'HookBackL'   , 'HookBackR'  ]
		self.SubRigsName += [ 'PropulsorL'  , 'PropulsorR' ]
		self.SubRigsName += [ 'DampFrontR'  , 'DampFrontL' ]
		self.SubRigsName += [ 'DampBackR'   , 'DampBackL'  ]

		self.SubRigsName += [ 'ProjectorAR'  , 'ProjectorAL'  ]	
		self.SubRigsName += [ 'ProjectorBR'  , 'ProjectorBL'  ]			
		self.SubRigsName += [ 'ProjectorCR'  , 'ProjectorCL'  ]	
		self.SubRigsName += [ 'ProjectorDR'  , 'ProjectorDL'  ]
		self.SubRigsName += [ 'ProjectorER'  , 'ProjectorEL'  ]				
		self.SubRigsName += [ 'ProjectorFR'  , 'ProjectorFL'  ]

		self.SubRigsName += [ 'GiroAR'  , 'GiroAL' ]
		self.SubRigsName += [ 'GiroBR'  , 'GiroBL' ]
		self.SubRigsName += [ 'GiroCR'  , 'GiroCL' ]
		self.SubRigsName += [ 'GiroDR'  , 'GiroDL' ]
		self.SubRigsName += [ 'GiroER'  , 'GiroEL' ]		


		self.Attr.add( "DampGiro" , Name = self.DampGiro.outs[0] , attrName = ["lightVisibility"] , attrType = ["intOnOff"] , attrValue = [1] )
		
		for side in ['R','L']:
			for letter in ['A','B','C','D','E','F']:
				exec( 'self.Attr.add( "Projector{0}{1}" , Name = self.Projector{0}{1}.outs[0] , attrName = ["lightVisibility"] , attrType = ["intOnOff"] , attrValue = [1] )'.format(letter,side) )	
			
			for letter in ['A','B','C','D','E']:
				exec( 'self.Attr.add( "Giro{0}{1}" , Name = self.Giro{0}{1}.outs[0] , attrName = ["lightVisibility"] , attrType = ["intOnOff"] , attrValue = [1] )'.format(letter,side) )	


		#CLASSE UTILS
		#UPDATE
		name = args.get( 'n'   , None )	
		pos  = args.get( 'pos' , None )
		if not( name == None ): self.Name.add( 'base' , copy = name ) 
		if not( pos  == None ): pass


	def postBuild( self ):
		'''
		setupSwitchVisibilityModel( 'ALL_grp' , 'rigPuppetRoot_CTRL' , lods = ['low' , 'block' ] )

		attrNames = ['bodyCtrl'           , 'r_reactorCtrl'      ,'l_reactorCtrl'      ,  'r_hook0Ctrl'      , 'r_hook1Ctrl'      , 'l_hook0Ctrl'      , 'l_hook1Ctrl'    ]
		topNodes  = [['rigPuppetTop_GRP'] , ['r_reactorTop_GRP'] ,['l_reactorTop_GRP'] ,  ['r_hook0Top_GRP'] , ['r_hook1Top_GRP'] , ['l_hook0Top_GRP'] , ['l_hook1Top_GRP'] ]
		
		attrNames += [ 'l_propulsorCtrl'      , 'r_propulsorCtrl'      , 'dampCtrl']
		topNodes  += [ ['l_propulsorTop_GRP'] , ['r_propulsorTop_GRP'] , ['r_damp0Top_GRP' , 'r_damp1Top_GRP' , 'l_damp0Top_GRP' , 'l_damp1Top_GRP'] ]
		
		for i in range( 0 , len(attrNames) ):
			attr = self.Attr.utils_mayaAddSpecialAttr( 'rigPuppetRoot_CTRL' , attrNames[i] , 'int+' , 10 )
			for topNode in topNodes[i]:
				mc.connectAttr( attr , topNode + '.ctrlVis' )

		'''
		return ""