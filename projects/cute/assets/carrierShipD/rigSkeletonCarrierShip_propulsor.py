
	
'''
#******************************************************** BUILD EXEMPLE 
import maya.cmds as mc

import python
from    python.projects.cute.assets.carrierShipD.rigSkeletonCarrierShip_propulsor import *
reload( python.projects.cute.assets.carrierShipD.rigSkeletonCarrierShip_propulsor)
mc.file( 'D:/mcantat_BDD/projects/cute/assets/carrierShipD/maya/scenes/carrierShipD_rigBase5.ma' , o = True , f = True  )
#=================================================
puppet = rigSkeletonCarrierShip_propulsor()	
puppet.printBuild = 1
toExec = puppet.build()
exec(toExec)


from python.classe.curveShape import *
reload( python.classe.curveShape)
curve = curveShape()	
curve.replaceSameNameFile('D:\mcantat_BDD\projects\cute\carrierShipD\maya\scenes\carrierShipD_saveCtrlShapes.ma')


'''

import maya.cmds as mc

from .....classe.rigPuppet import *  
from .....classe.rigCtrl import *  
from .....classe.rigModuleChain import *     
from .....classe.rigModuleArm import *    
from .....classe.rigModulePiston import *   
       
class rigSkeletonCarrierShip_propulsor(rigPuppet):

	def __init__( self , **args ):
		rigPuppet.__init__( self , **args )

		#CLASSE TYPE
		self.classeType = 'rigPuppetPropulsor'
		#CLASSE BLUE PRINT - POS
		propulsorSlideLocs      = ['pos_propulsorSlide1']
		propulsorRotLocs        = [x.encode('UTF8') for x in mc.ls('pos_propulsorRot?'   , type = 'transform' )]
		propulsorPanelsLocs     = [x.encode('UTF8') for x in mc.ls('pos_propulsorPanels?'   , type = 'transform' )]
		sideHoldLocs            = ['pos_sideHold1']
		sideHoldWheelLocs       = ['pos_sideHoldWheel1']
		sideHoldDampLocs        = ['pos_sideHoldDamp1']
		miniReactorBLocs        = ['pos_miniReactorB1']
		miniReactorALocs        = ['pos_miniReactorA1']
		fireLocs                = ['pos_propulsorFire']
		backDampLocs            = [x.encode('UTF8') for x in mc.ls('pos_backDamp?'       , type = 'transform' )]		
		backDampSideLocs        = [x.encode('UTF8') for x in mc.ls('pos_backDampSide?'   , type = 'transform' )]
		dampFrontLocs           = [x.encode('UTF8') for x in mc.ls('pos_propulsorDampFront?'     , type = 'transform' )]
		giroLocs                = ['pos_propulsorGiro1']
		armDampTopLocs          = [x.encode('UTF8') for x in mc.ls('pos_armDampTop?'     , type = 'transform' )]
		armDampBottomLocs       = [x.encode('UTF8') for x in mc.ls('pos_armDampBottom?'  , type = 'transform' )]
		slideDampTopLocs        = ['pos_slideDampTop1']
		slideDampBottomLocs     = ['pos_slideDampBottom1']
		armDampBottomOffsetLocs = ['pos_armDampBottomOffset1']
		sideWheelLocs           = ['pos_sideWheel1']		
		#CLASSE BLUE PRINT
		self.Name.add( 'base' , baseName = 'prop'   )
		self.Name.add( 'root'            , ref = self.Name.base , baseNameAppend = 'root'            )
		self.Name.add( 'slide'           , ref = self.Name.base , baseNameAppend = 'slide'           )
		self.Name.add( 'rot'             , ref = self.Name.base , baseNameAppend = 'rot'             )
		self.Name.add( 'panelA'          , ref = self.Name.base , baseNameAppend = 'panelA'          )
		self.Name.add( 'panelB'          , ref = self.Name.base , baseNameAppend = 'panelB'          )
		self.Name.add( 'panelC'          , ref = self.Name.base , baseNameAppend = 'panelC'          )
		self.Name.add( 'panelD'          , ref = self.Name.base , baseNameAppend = 'panelD'          )
		self.Name.add( 'sideHold'        , ref = self.Name.base , baseNameAppend = 'sideHold'        )
		self.Name.add( 'sideHoldWheel'   , ref = self.Name.base , baseNameAppend = 'sideHoldWheel'   )
		self.Name.add( 'sideHoldDamp'    , ref = self.Name.base , baseNameAppend = 'sideHoldDamp'    )
		self.Name.add( 'miniReactorA'    , ref = self.Name.base , baseNameAppend = 'miniReactorA'    )
		self.Name.add( 'miniReactorB'    , ref = self.Name.base , baseNameAppend = 'miniReactorB'    )
		self.Name.add( 'backDamp'        , ref = self.Name.base , baseNameAppend = 'backDamp'        )
		self.Name.add( 'backDampSide'    , ref = self.Name.base , baseNameAppend = 'backDampSide'    )
		self.Name.add( 'dampFront'       , ref = self.Name.base , baseNameAppend = 'dampFront'       )
		self.Name.add( 'fire'            , ref = self.Name.base , baseNameAppend = 'fire'            )
		self.Name.add( 'giro'            , ref = self.Name.base , baseNameAppend = 'giro'            )
		self.Name.add( 'armDampTopRot'      , ref = self.Name.base , baseNameAppend = 'armDampTopRot'      )	
		self.Name.add( 'armDampTopPiston'   , ref = self.Name.base , baseNameAppend = 'armDampTopPiston'   )
		self.Name.add( 'slideDampTop'       , ref = self.Name.base , baseNameAppend = 'slideDampTop'       )	
		self.Name.add( 'armDampBottomRot'   , ref = self.Name.base , baseNameAppend = 'armDampBottomRot'   )	
		self.Name.add( 'armDampBottomPiston', ref = self.Name.base , baseNameAppend = 'armDampBottomPiston')	
		self.Name.add( 'slideDampBottom'    , ref = self.Name.base , baseNameAppend = 'slideDampBottom'    )
		self.Name.add( 'armDampBottomOffset', ref = self.Name.base , baseNameAppend = 'armDampBottomOffset')
		self.Name.add( 'sideWheel'       , ref = self.Name.base , baseNameAppend = 'sideWheel'   )			
		#CLASSE BLUE PRINT - SUBRIG
		parent  = args.get( 'parent' , self.Name.topNode  )
		
		self.Root          = rigSkeletonChain( n = self.Name.root          , pos = [[0,0,0,0,0,0,1,1,1]] , parent = parent  )
		self.Slide         = rigSkeletonChain( n = self.Name.slide         , pos = propulsorSlideLocs    , parent = self.Root.outs[-1]    )
		self.Rot           = rigSkeletonChain( n = self.Name.rot           , pos = propulsorRotLocs      , parent = self.Slide.outs[0]    )
		self.PanelA        = rigSkeletonChain( n = self.Name.panelA        , pos = [propulsorPanelsLocs[0]] , parent = self.Rot.outs[1]      )
		self.PanelB        = rigSkeletonChain( n = self.Name.panelB        , pos = [propulsorPanelsLocs[1]] , parent = self.Rot.outs[1]      )
		self.PanelC        = rigSkeletonChain( n = self.Name.panelC        , pos = [propulsorPanelsLocs[2]] , parent = self.Rot.outs[1]      )
		self.PanelD        = rigSkeletonChain( n = self.Name.panelD        , pos = [propulsorPanelsLocs[3]] , parent = self.Rot.outs[1]      )		
		self.Fire          = rigSkeletonChain( n = self.Name.fire          , pos = fireLocs              , parent = self.Rot.outs[2] )		
		self.SideHold      = rigSkeletonChain( n = self.Name.sideHold      , pos = sideHoldLocs          , parent = self.Root.outs[-1]     )	
		self.SideHoldWheel = rigSkeletonChain( n = self.Name.sideHoldWheel , pos = sideHoldWheelLocs     , parent = self.SideHold.outs[0] )
		self.SideHoldDamp  = rigSkeletonChain( n = self.Name.sideHoldDamp  , pos = sideHoldDampLocs      , parent = self.SideHold.outs[0] )
		self.Giro          = rigSkeletonChain( n = self.Name.giro          , pos = giroLocs              , parent = self.SideHold.outs[0] )
		self.SubRigs      += [ self.Root , self.Slide , self.Rot , self.PanelA , self.PanelB , self.PanelC , self.PanelD , self.Fire , self.SideHold , self.SideHoldWheel , self.SideHoldDamp , self.Giro ]
		self.SubRigsName  += [     'Root',     'Slide',     'Rot',     'PanelA',     'PanelB',     'PanelC',     'PanelD',     'Fire',     'SideHold',     'SideHoldWheel',     'SideHoldDamp',     'Giro']

		self.RotDampTop    = rigSkeletonChain( n = self.Name.armDampTopRot     , pos = [armDampTopLocs[0]] , parent = self.SideHold.outs[0]    )
		self.PistonDampTop = rigSkeletonChain( n = self.Name.armDampTopPiston  , pos = armDampTopLocs[1:]  , parent = self.RotDampTop.outs[-1] )
		self.SlideDampTop  = rigSkeletonChain( n = self.Name.slideDampTop      , pos = slideDampTopLocs    , parent = self.Rot.outs[1]         )
		self.OffsetDampBottom = rigSkeletonChain( n = self.Name.armDampBottomOffset  , pos = armDampBottomOffsetLocs , parent = self.Root.outs[-1]   )		
		self.RotDampBottom    = rigSkeletonChain( n = self.Name.armDampBottomRot     , pos = [armDampBottomLocs[0]]    , parent = self.OffsetDampBottom.outs[-1]   )
		self.PistonDampBottom = rigSkeletonChain( n = self.Name.armDampBottomPiston  , pos = armDampBottomLocs[1:]     , parent = self.RotDampBottom.outs[-1] )
		self.SlideDampBottom  = rigSkeletonChain( n = self.Name.slideDampBottom      , pos = slideDampBottomLocs       , parent = self.Rot.outs[1]         )
		self.SubRigs      += [ self.RotDampTop , self.PistonDampTop , self.SlideDampTop  , self.OffsetDampBottom , self.RotDampBottom , self.PistonDampBottom , self.SlideDampBottom ]
		self.SubRigsName  += [     'RotDampTop',     'PistonDampTop',     'SlideDampTop' ,     'OffsetDampBottom',     'RotDampBottom',     'PistonDampBottom',     'SlideDampBottom']

		self.MiniReactorA  = rigSkeletonChain( n = self.Name.miniReactorA  , pos = miniReactorALocs      , parent = self.Root.outs[-1]    )	
		self.MiniReactorB  = rigSkeletonChain( n = self.Name.miniReactorB  , pos = miniReactorBLocs      , parent = self.Root.outs[-1]    )	
		self.SideWheel     = rigSkeletonChain( n = self.Name.sideWheel     , pos = sideWheelLocs         , parent = self.SideHold.outs[0]    )		
		self.SubRigs      += [ self.MiniReactorA , self.MiniReactorB , self.SideWheel  ]
		self.SubRigsName  += [ 'MiniReactorA'    , 'MiniReactorB'    ,     'SideWheel' ]

		self.BackDamp      = rigSkeletonChain( n = self.Name.backDamp      , pos = backDampLocs          , parent = self.Root.outs[-1]    )
		self.BackDampSide  = rigSkeletonChain( n = self.Name.backDampSide  , pos = backDampSideLocs      , parent = self.Root.outs[-1]    )
		self.SubRigs      += [ self.BackDamp , self.BackDampSide ]
		self.SubRigsName  += [     'BackDamp'    , 'BackDampSide'    ]

		self.DampFront     = rigSkeletonChain( n = self.Name.dampFront     , pos = dampFrontLocs         , parent = self.Root.outs[-1]    )
		self.SubRigs      += [ self.DampFront  ]
		self.SubRigsName  += [ 'DampFront'     ]
		#CLASSE BLUE PRINT - MIRROR
		self.Attr.add( "giro"    , Name = self.Giro.outs[0]    , attrName = ["lightVisibility"] , attrType = ["intOnOff"] , attrValue = [1] )
		self.Attr.add( "fire"    , Name = self.Fire.outs[0]    , attrName = ["lightVisibility"] , attrType = ["intOnOff"] , attrValue = [1] )

		#CLASSE UTILS
		self.ins         = [ self.Root.ins[0] , self.Rot.ins[1] , self.Rot.ins[0] ]
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


