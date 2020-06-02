
	
'''
#******************************************************** BUILD EXEMPLE 
import maya.cmds as mc

import python
from    python.projects.cute.assets.carrierShipD.rigPuppetCarrierShip_propulsor import *
reload( python.projects.cute.assets.carrierShipD.rigPuppetCarrierShip_propulsor)
mc.file( 'D:/mcantat_BDD/projects/cute/assets/carrierShipD/maya/scenes/carrierShipD_rigSkeleton.ma' , o = True , f = True  )
#=================================================
puppet = rigPuppetCarrierShip_propulsor()	
puppet.debug = 1
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
       
class rigPuppetCarrierShip_propulsor(rigPuppet):

	def __init__( self , **args ):
		rigPuppet.__init__( self , **args )

		#CLASSE TYPE
		self.classeType = 'rigPuppetPropulsor'
		#CLASSE BLUE PRINT - POS
		propulsorSlideLocs  = ['r_propulsorSlide0_JNT']
		propulsorRotLocs    = [x.encode('UTF8') for x in mc.ls('r_propulsorRot?_JNT'   , type = 'transform' )]
		propulsorPanelsLocs = [x.encode('UTF8') for x in mc.ls('r_propulsorPanel?0_JNT'       , type = 'transform' )]
		sideHoldLocs        = ['r_propulsorSideHold0_JNT']
		sideHoldWheelLocs   = ['r_propulsorSideHoldWheel0_JNT']
		sideHoldDampLocs    = ['r_propulsorSideHoldDamp0_JNT']
		miniReactorBLocs    = ['r_propulsorMiniReactorB0_JNT']
		miniReactorALocs    = ['r_propulsorMiniReactorA0_JNT']
		fireLocs            = ['r_propulsorFire0_JNT']
		backDampLocs        = [x.encode('UTF8') for x in mc.ls('r_propulsorBackDamp?_JNT'       , type = 'transform' )]		
		backDampSideLocs    = [x.encode('UTF8') for x in mc.ls('r_propulsorBackDampSide?_JNT'   , type = 'transform' )]
		dampFrontLocs       = [x.encode('UTF8') for x in mc.ls('r_propulsorDampFront?_JNT'     , type = 'transform' )]
		giroLocs            = ['r_propulsorGiro0_JNT']

		armDampTopRotLocs       = [x.encode('UTF8') for x in mc.ls('r_propulsorArmDampTopRot?_JNT'       , type = 'transform' )]
		armDampTopPistonLocs    = [x.encode('UTF8') for x in mc.ls('r_propulsorArmDampTopPiston?_JNT'    , type = 'transform' )]	
		armDampBottomRotLocs    = [x.encode('UTF8') for x in mc.ls('r_propulsorArmDampBottomRot?_JNT'    , type = 'transform' )]
		armDampBottomPistonLocs = [x.encode('UTF8') for x in mc.ls('r_propulsorArmDampBottomPiston?_JNT' , type = 'transform' )]

		slideDampTopLocs        = ['r_propulsorSlideDampTop0_JNT']
		slideDampBottomLocs     = ['r_propulsorSlideDampBottom0_JNT']
		armDampBottomOffsetLocs = ['r_propulsorArmDampBottomOffset0_JNT']

		sideWheelLocs       = ['r_propulsorSideWheel0_JNT']		


		#CLASSE BLUE PRINT
		self.Name.add( 'base' , baseName = 'prop'   )
		self.Name.add( 'root'         , ref = self.Name.base , baseNameAppend = 'root'        )
		self.Name.add( 'slide'         , ref = self.Name.base , baseNameAppend = 'slide'        )
		self.Name.add( 'rot'           , ref = self.Name.base , baseNameAppend = 'rot'          )
		self.Name.add( 'panelA'        , ref = self.Name.base , baseNameAppend = 'panelA'       )
		self.Name.add( 'panelB'        , ref = self.Name.base , baseNameAppend = 'panelB'       )
		self.Name.add( 'panelC'        , ref = self.Name.base , baseNameAppend = 'panelC'       )
		self.Name.add( 'panelD'        , ref = self.Name.base , baseNameAppend = 'panelD'       )
		self.Name.add( 'sideHold'      , ref = self.Name.base , baseNameAppend = 'sideHold'     )
		self.Name.add( 'sideHoldWheel' , ref = self.Name.base , baseNameAppend = 'sideHoldWheel')
		self.Name.add( 'sideHoldDamp'  , ref = self.Name.base , baseNameAppend = 'sideHoldDamp' )
		self.Name.add( 'miniReactorA'  , ref = self.Name.base , baseNameAppend = 'miniReactorA' )
		self.Name.add( 'miniReactorB'  , ref = self.Name.base , baseNameAppend = 'miniReactorB' )
		self.Name.add( 'backDamp'      , ref = self.Name.base , baseNameAppend = 'backDamp'     )
		self.Name.add( 'backDampSide'  , ref = self.Name.base , baseNameAppend = 'backDampSide' )
		self.Name.add( 'dampFront'     , ref = self.Name.base , baseNameAppend = 'dampFront'    )
		self.Name.add( 'fire'          , ref = self.Name.base , baseNameAppend = 'fire'         )
		self.Name.add( 'giro'          , ref = self.Name.base , baseNameAppend = 'giro'         )
		self.Name.add( 'armDampTopRot'      , ref = self.Name.base , baseNameAppend = 'armDampTopRot'      )	
		self.Name.add( 'armDampTopPiston'   , ref = self.Name.base , baseNameAppend = 'armDampTopPiston'   )
		self.Name.add( 'slideDampTop'       , ref = self.Name.base , baseNameAppend = 'slideDampTop'       )	
		self.Name.add( 'armDampBottomRot'   , ref = self.Name.base , baseNameAppend = 'armDampBottomRot'   )	
		self.Name.add( 'armDampBottomPiston', ref = self.Name.base , baseNameAppend = 'armDampBottomPiston')	
		self.Name.add( 'slideDampBottom'    , ref = self.Name.base , baseNameAppend = 'slideDampBottom'    )
		self.Name.add( 'armDampBottomOffset', ref = self.Name.base , baseNameAppend = 'armDampBottomOffset')
		self.Name.add( 'sideWheel'       , ref = self.Name.base , baseNameAppend = 'sideWheel'   )			
		#CLASSE BLUE PRINT - SUBRIG
		self.Slide         = rigCtrl( n = self.Name.slide         , pos = propulsorSlideLocs       , form = 'arrow2sides'     , colors = ['green'] , skeleton = True  , ctrlVisPriority = 1 , parent = self.Name.topNode , attrStates = [['tx']])
		self.Rot           = rigModuleArm(   n = self.Name.rot    , pos = propulsorRotLocs         , ik = True , fk = True , skeleton = True  , ctrlVisPriority = 0 , attrStates = [['rz']] )
		self.PanelA        = rigCtrl( n = self.Name.panelA        , pos = [propulsorPanelsLocs[0]] , form = 'arrow2SidesBend' , colors = ['red']    , ctrlVisPriority = 2 , parent = self.Name.topNode, attrStates = [['tx','ty','rz']] )
		self.PanelB        = rigCtrl( n = self.Name.panelB        , pos = [propulsorPanelsLocs[1]] , form = 'arrow2SidesBend' , colors = ['red']    , ctrlVisPriority = 2 , parent = self.Name.topNode, attrStates = [['tx','ty','rz']] )
		self.PanelC        = rigCtrl( n = self.Name.panelC        , pos = [propulsorPanelsLocs[2]] , form = 'arrow2SidesBend' , colors = ['red']    , ctrlVisPriority = 2 , parent = self.Name.topNode, attrStates = [['tx','ty','rz']] )
		self.PanelD        = rigCtrl( n = self.Name.panelD        , pos = [propulsorPanelsLocs[3]] , form = 'arrow2SidesBend' , colors = ['red']    , ctrlVisPriority = 2 , parent = self.Name.topNode, attrStates = [['tx','ty','rz']] )
		self.Fire          = rigCtrl( n = self.Name.fire          , pos = fireLocs                 , form = 'cylinder'        , colors = ['red']    , ctrlVisPriority = 1 , parent = self.Name.topNode)	
		self.SideHold      = rigCtrl( n = self.Name.sideHold      , pos = sideHoldLocs             , form = 'arrow2sides'     , colors = ['yellow'] , ctrlVisPriority = 2 , parent = self.Name.topNode, attrStates = [['tx']] )		
		self.SideHoldWheel = rigCtrl( n = self.Name.sideHoldWheel , pos = sideHoldWheelLocs        , form = 'circle'          , colors = ['yellow'] , ctrlVisPriority = 2 , parent = self.Name.topNode, attrStates = [['rz']] )
		self.SideHoldDamp  = rigCtrl( n = self.Name.sideHoldDamp  , pos = sideHoldDampLocs         , form = 'cylinder'        , colors = ['red']    , ctrlVisPriority = 2 , parent = self.Name.topNode, attrStates = [['tx','s']] )
		self.Giro          = rigCtrl( n = self.Name.giro          , pos = giroLocs                 , form = 'arrow2SidesBend' , colors = ['red']    , ctrlVisPriority = 6 , parent = self.Name.topNode , attrStates = [['rz']] )
		self.SubRigs      += [ self.Slide , self.Rot , self.PanelA , self.PanelB , self.PanelC , self.PanelD , self.Fire , self.SideHold , self.SideHoldWheel , self.SideHoldDamp , self.Giro ]
		self.SubRigsName  += [     'Slide',     'Rot',     'PanelA',     'PanelB',     'PanelC',     'PanelD',     'Fire',     'SideHold',     'SideHoldWheel',     'SideHoldDamp',     'Giro']

		self.RotDampTop       = rigCtrl(         n = self.Name.armDampTopRot       , pos = armDampTopRotLocs       , form = 'arrow2SidesBend' , colors = ['red'] , ctrlVisPriority = 2 , parent = self.Name.topNode, attrStates = [['rz']] )
		self.PistonDampTop    = rigModulePiston( n = self.Name.armDampTopPiston    , pos = armDampTopPistonLocs    , ctrlVisPriority = 10 , form = 'circle'          , colors = ['red'] , aim = 1 )
		self.SlideDampTop     = rigCtrl(         n = self.Name.slideDampTop        , pos = slideDampTopLocs        , form = 'arrow2sides'     , colors = ['red'] , ctrlVisPriority = 2 , parent = self.Name.topNode, attrStates = [['tx']] )
		self.OffsetDampBottom = rigCtrl(         n = self.Name.armDampBottomOffset , pos = armDampBottomOffsetLocs , form = 'arrow2sides'     , colors = ['red'] , ctrlVisPriority = 2 , parent = self.Name.topNode, attrStates = [['t']]  )	
		self.RotDampBottom    = rigCtrl(         n = self.Name.armDampBottomRot    , pos = armDampBottomRotLocs    , form = 'arrow2SidesBend' , colors = ['red'] , ctrlVisPriority = 2 , parent = self.Name.topNode, attrStates = [['rz']] )
		self.PistonDampBottom = rigModulePiston( n = self.Name.armDampBottomPiston , pos = armDampBottomPistonLocs , ctrlVisPriority = 10 , form = 'circle'          , colors = ['red'] , aim = 1 )
		self.SlideDampBottom  = rigCtrl(         n = self.Name.slideDampBottom     , pos = slideDampBottomLocs     , form = 'arrow2sides'     , colors = ['red'] , ctrlVisPriority = 2 , parent = self.Name.topNode, attrStates = [['tx']] )	
		self.SubRigs      += [ self.RotDampTop , self.PistonDampTop , self.SlideDampTop  , self.RotDampBottom , self.PistonDampBottom , self.SlideDampBottom , self.OffsetDampBottom  ]
		self.SubRigsName  += [     'RotDampTop',     'PistonDampTop',     'SlideDampTop' ,     'RotDampBottom',     'PistonDampBottom',     'SlideDampBottom',     'OffsetDampBottom' ]


		self.MiniReactorA  = rigCtrl( n = self.Name.miniReactorA , pos = miniReactorALocs , form = 'crossArrowBend' , colors = ['red'] , ctrlVisPriority = 3 , parent = self.Name.topNode , attrStates = [['r']] )
		self.MiniReactorB  = rigCtrl( n = self.Name.miniReactorB , pos = miniReactorBLocs , form = 'crossArrowBend' , colors = ['red'] , ctrlVisPriority = 3 , parent = self.Name.topNode , attrStates = [['r']] )
		self.SideWheel     = rigCtrl( n = self.Name.sideWheel    , pos = sideWheelLocs    , form = 'circle'         , colors = ['yellow'] , ctrlVisPriority = 2 , parent = self.Name.topNode, attrStates = [['rz']] )	
		self.SubRigs      += [ self.MiniReactorA , self.MiniReactorB , self.SideWheel  ]
		self.SubRigsName  += [ 'MiniReactorA'    , 'MiniReactorB'    ,     'SideWheel' ]

		self.BackDamp      = rigModuleChain( n = self.Name.backDamp     , pos = backDampLocs       , form = 'arrow2sidesBend' , colors = ['yellow'] , skeleton = True  , ctrlVisPriority = 2 , attrStates = [['rz']] )
		self.BackDampSide  = rigModuleChain( n = self.Name.backDampSide , pos = backDampSideLocs   , form = 'arrow2sidesBend' , colors = ['yellow'] , skeleton = True  , ctrlVisPriority = 2 , attrStates = [['rz']] )
		self.SubRigs      += [ self.BackDamp , self.BackDampSide ]
		self.SubRigsName  += [     'BackDamp',     'BackDampSide']

		self.DampFront     = rigModuleChain( n = self.Name.dampFront , pos = dampFrontLocs , form = 'arrow2sides' , colors = ['red'] , skeleton = True  , ctrlVisPriority = 2 , attrStates = [['tx'],['rz']] )
		self.SubRigs      += [ self.DampFront  ]
		self.SubRigsName  += [ 'DampFront'     ]
		#CLASSE BLUE PRINT - MIRROR
		#CLASSE BLUE PRINT - OTHER
		self.Attr.add( "giro"    , Name = self.Giro.Name.ctrl   , attrName = ["lightVisibility"] , attrType = ["intOnOff"] , attrValue = [1] )
		self.Attr.add( "fire"    , Name = self.Fire.Name.ctrl   , attrName = ["lightVisibility"] , attrType = ["intOnOff"] , attrValue = [1] )

		self.Link.add( 'SlideDampTop'    , Sources = [ self.SlideDampTop.outs[0]    ] , Destinations = [ self.PistonDampTop.ins[1]    ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )
		self.Link.add( 'SlideDampBottom' , Sources = [ self.SlideDampBottom.outs[0] ] , Destinations = [ self.PistonDampBottom.ins[1] ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )

		self.Link.add( 'paSpaceSideHold'      , Sources = [ self.Slide.outs[0] ] , Destinations = [ self.SideHold.ins[0]  ] , type = 'parentSpace'  , spaceDriver = self.SideHold.Name.ctrl               , spaceAttr = 'parentSpace' , spaceNames = ['slide'] )
		self.Link.add( 'paSpacePropulsorDamp' , Sources = [ self.Slide.outs[0] ] , Destinations = [ self.DampFront.ins[0] ] , type = 'parentSpace'  , spaceDriver = self.DampFront.Ctrl0.Name.ctrl    , spaceAttr = 'parentSpace' , spaceNames = ['slide'] )



		#CLASSE UTILS
		self.ins         = [ self.Rot.ins[1] ]
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


