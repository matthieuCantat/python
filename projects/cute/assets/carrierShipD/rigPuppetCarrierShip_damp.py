
	
'''
#******************************************************** BUILD EXEMPLE 
import maya.cmds as mc

import python
from    python.projects.cute.assets.carrierShipD.rigPuppetCarrierShip_damp import *
reload( python.projects.cute.assets.carrierShipD.rigPuppetCarrierShip_damp)
mc.file( 'D:/mcantat_BDD/projects/cute/assets/carrierShipD/maya/scenes/carrierShipD_rigSkeleton.ma' , o = True , f = True  )
#=================================================
puppet = rigPuppetCarrierShip_damp()	
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
       
class rigPuppetCarrierShip_damp(rigPuppet):

	def __init__( self , **args ):
		rigPuppet.__init__( self , **args )

		#CLASSE TYPE
		self.classeType = 'rigPuppetDamp'
		#CLASSE BLUE PRINT - POS
		armLocs           = [x.encode('UTF8') for x in mc.ls('r_damp0Arm?_JNT'           , type = 'transform' )]
		ctrlPistonLocs    = [x.encode('UTF8') for x in mc.ls('r_damp0ArmPiston?_JNT'     , type = 'transform' )]
		pistonLocs        = [x.encode('UTF8') for x in mc.ls('r_damp0Piston?_JNT'        , type = 'transform' )]			
		secondaryMecaLocs = [x.encode('UTF8') for x in mc.ls('r_damp0SecondaryMeca??_JNT' , type = 'transform' )]
		secondaryDampLocs = ['r_damp0SecondaryRot0_JNT']	
		#CLASSE BLUE PRINT
		self.Name.add( 'base'           , baseName = 'damp'  )
		self.Name.add( 'root'           , ref = self.Name.base , baseNameAppend = 'root'            )
		self.Name.add( 'arm'            , ref = self.Name.base , baseNameAppend = 'arm'            )
		self.Name.add( 'ctrlPiston'     , ref = self.Name.base , baseNameAppend = 'ctrlPiston'      )
		self.Name.add( 'piston'         , ref = self.Name.base , baseNameAppend = 'piston'         )		
		self.Name.add( 'secondaryMecaA' , ref = self.Name.base , baseNameAppend = 'secondaryMecaA' )
		self.Name.add( 'secondaryMecaB' , ref = self.Name.base , baseNameAppend = 'secondaryMecaB' )				
		self.Name.add( 'secondaryDamp'  , ref = self.Name.base , baseNameAppend = 'secondaryRot'   )
		self.Name.add( 'dampAttach'     , ref = self.Name.base , baseNameAppend = 'attach'         )
		#CLASSE BLUE PRINT - SUBRIG
		self.Arm        = rigModuleArm(    n = self.Name.arm            , pos = armLocs                , ik = True , ctrlVisPriority = 10 , attrStates = [['rz']] )
		self.CtrlPiston = rigCtrl(         n = self.Name.ctrlPiston      , pos = [ctrlPistonLocs[0]]     , form = 'arrow2sidesBend'  , colors = ['red'] , ctrlVisPriority = 2  , parent = self.Name.topNode, attrStates = [['rz']] )
		self.Piston     = rigModulePiston( n = self.Name.piston         , pos = pistonLocs             , form = 'circle' , colors = ['red'] , aim = 1 , ctrlVisPriority = 10)	
		self.MecaA         = rigCtrl(     n = self.Name.secondaryMecaA , pos = [secondaryMecaLocs[0]] , form = 'arrow2sides'     , colors = ['green'] , ctrlVisPriority = 2  , parent = self.Name.topNode, attrStates = [['rz']] )
		self.MecaB         = rigCtrl(     n = self.Name.secondaryMecaB , pos = [secondaryMecaLocs[1]] , form = 'arrow2sides'     , colors = ['green'] , ctrlVisPriority = 2  , parent = self.Name.topNode, attrStates = [['rz']] )
		self.SecondaryDamp = rigCtrl(     n = self.Name.secondaryDamp  , pos = secondaryDampLocs      , form = 'arrow2sides'     , colors = ['yellow'] , ctrlVisPriority = 2 , parent = self.Name.topNode, attrStates = [['rz']] )

		self.SubRigs      += [ self.Arm , self.CtrlPiston , self.Piston , self.MecaA , self.MecaB , self.SecondaryDamp  ]
		self.SubRigsName  += [     'Arm',     'CtrlPiston',     'Piston'    , 'MecaA'    , 'MecaB'    , 'SecondaryDamp' ]

		#CLASSE BLUE PRINT - MIRROR
		#CLASSE BLUE PRINT - OTHER
		#self.Link.add( 'paRoot'         , Sources = [ self.Root.outs[0]          ] , Destinations = [ self.Slide.ins[0] , self.PropulsorDoor.ins[0]  ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )	
		self.Link.add( 'pistonA'      , Sources = [ self.CtrlPiston.outs[0]    ] , Destinations = [ self.Piston.ins[0] ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )	
		self.Link.add( 'pistonB'      , Sources = [ self.Arm.outs[1]           ] , Destinations = [ self.Piston.ins[1] ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )	


		#CLASSE UTILS
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

