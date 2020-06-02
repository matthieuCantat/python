
	
'''
#******************************************************** BUILD EXEMPLE 
import maya.cmds as mc

import python
from    python.projects.cute.assets.carrierShipD.rigSkeletonCarrierShip_damp import *
reload( python.projects.cute.assets.carrierShipD.rigSkeletonCarrierShip_damp)
mc.file( 'D:/mcantat_BDD/projects/cute/assets/carrierShipD/maya/scenes/carrierShipD_rigBase5.ma' , o = True , f = True  )
#=================================================
puppet = rigSkeletonCarrierShip_damp()	
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
       
class rigSkeletonCarrierShip_damp(rigPuppet):

	def __init__( self , **args ):
		rigPuppet.__init__( self , **args )

		#CLASSE TYPE
		self.classeType = 'rigPuppetDamp'
		#CLASSE BLUE PRINT - POS
		armLocs           = [x.encode('UTF8') for x in mc.ls('pos_dampArm?'           , type = 'transform' )]
		armPistonLocs     = [x.encode('UTF8') for x in mc.ls('pos_dampArmPiston?'     , type = 'transform' )]
		pistonLocs        = [x.encode('UTF8') for x in mc.ls('pos_dampPiston?'        , type = 'transform' )]			
		secondaryMecaLocs = [x.encode('UTF8') for x in mc.ls('pos_secondaryDampMeca?' , type = 'transform' )]
		secondaryDampLocs = ['pos_secondaryDampRot1']		
		#CLASSE BLUE PRINT
		self.Name.add( 'base'           , baseName = 'damp'  )
		self.Name.add( 'root'           , ref = self.Name.base , baseNameAppend = 'root'            )
		self.Name.add( 'arm'            , ref = self.Name.base , baseNameAppend = 'arm'            )
		self.Name.add( 'armPiston'      , ref = self.Name.base , baseNameAppend = 'armPiston'      )
		self.Name.add( 'piston'         , ref = self.Name.base , baseNameAppend = 'piston'         )		
		self.Name.add( 'secondaryMecaA' , ref = self.Name.base , baseNameAppend = 'secondaryMecaA' )
		self.Name.add( 'secondaryMecaB' , ref = self.Name.base , baseNameAppend = 'secondaryMecaB' )				
		self.Name.add( 'secondaryDamp'  , ref = self.Name.base , baseNameAppend = 'secondaryRot'   )
		self.Name.add( 'dampAttach'     , ref = self.Name.base , baseNameAppend = 'attach'         )

		#CLASSE BLUE PRINT - SUBRIG
		parent  = args.get( 'parent' , self.Name.topNode  )

		self.Attach        = rigSkeletonChain( n = self.Name.dampAttach     , pos = [armLocs[-1]]               , parent = parent   )	
		self.Arm           = rigSkeletonChain( n = self.Name.arm            , pos = armLocs                     , parent = self.Attach.outs[0]    )
		self.ArmPiston     = rigSkeletonChain( n = self.Name.armPiston      , pos = armPistonLocs               , parent = self.Attach.outs[0]    )
		self.Piston        = rigSkeletonChain( n = self.Name.piston         , pos = pistonLocs                  , parent = self.ArmPiston.outs[2] )	
		self.MecaA         = rigSkeletonChain( n = self.Name.secondaryMecaA , pos = [secondaryMecaLocs[0]]      , parent = self.Attach.outs[0]    )
		self.MecaB         = rigSkeletonChain( n = self.Name.secondaryMecaB , pos = [secondaryMecaLocs[1]]      , parent = self.Attach.outs[0]    )
		self.SecondaryDamp = rigSkeletonChain( n = self.Name.secondaryDamp  , pos = secondaryDampLocs           , parent = self.Attach.outs[0]    )
		
		self.SubRigs      += [  self.Arm , self.ArmPiston , self.Piston , self.MecaA , self.MecaB , self.SecondaryDamp , self.Attach ]
		self.SubRigsName  += [   'Arm'   , 'ArmPiston'    , 'Piston'    , 'MecaA'    , 'MecaB'    , 'SecondaryDamp'    , 'Attach'    ]

		#CLASSE BLUE PRINT - MIRROR
		#CLASSE BLUE PRINT - OTHER
		#CLASSE UTILS
		#CLASSE MODIF
		#INSTANCE MODIF
		name    = args.get( 'n'      , None )	
		pos     = args.get( 'pos'    , None )
		if not( name == None ): self.Name.add( 'base' , copy = name ) 
		if not( pos  == None ): pass

		'''											
		if not( shape  == None ): self.CurveShape.add(  'ctrl'    , shape                 )
		if not( form   == None ): self.CurveShape.add(  'ctrl'    , { 'form'   : form   } )
		if not( colors == None ): self.CurveShape.add(  'ctrl'    , { 'colors' : colors } )	
		'''

