
	
'''
#******************************************************** BUILD EXEMPLE 
import maya.cmds as mc
import python
from python.classe.rigPuppetQuadriped import *
reload( python.classe.rigPuppetQuadriped)
mc.file( 'D:/mcantat_BDD/projects/quadriped/quadriped_model01.ma' , o = True , f = True  )
#=================================================
puppet = rigPuppetQuadriped( ctrlScale = 15 )	
puppet.build()

'''

import maya.cmds as mc

from .rigPuppet import *  
from .rigCtrl import *  
from .rigModuleChain import *     
from .rigModuleArm import *    

       
class rigPuppetQuadriped(rigPuppet):

	def __init__( self , **args ):
		rigPuppet.__init__( self , **args )		
		#CLASSE TYPE
		self.classeType = 'rigPuppetHowie'
		#CLASSE BLUE PRINT
		globalLocs = [x.encode('UTF8') for x in mc.ls('pos_global?' , type = 'transform' )]
		bodyLocs   = [x.encode('UTF8') for x in mc.ls('pos_body?'   , type = 'transform' )]				
		pelvisLocs = [x.encode('UTF8') for x in mc.ls('pos_pelvis?' , type = 'transform' )]
		chestLocs  = [x.encode('UTF8') for x in mc.ls('pos_chest?'  , type = 'transform' )]		
		headLocs   = [x.encode('UTF8') for x in mc.ls('pos_head?'   , type = 'transform' )]

		spineLocs      = [x.encode('UTF8') for x in mc.ls('pos_spine?'      , type = 'transform' )]
		neckLocs       = [x.encode('UTF8') for x in mc.ls('pos_neck?'       , type = 'transform' )]
		tailLocs       = [x.encode('UTF8') for x in mc.ls('pos_tail?'       , type = 'transform' )]

		armPivLocs     = [x.encode('UTF8') for x in mc.ls('pos_armPiv?'     , type = 'transform' )]
		armLocs        = [x.encode('UTF8') for x in mc.ls('pos_arm?'        , type = 'transform' )]
		scapulaLocs    = [x.encode('UTF8') for x in mc.ls('pos_scapula?'    , type = 'transform' )]		
		handLocs       = [x.encode('UTF8') for x in mc.ls('pos_hand?'       , type = 'transform' )]		
		legLocs        = [x.encode('UTF8') for x in mc.ls('pos_leg?'        , type = 'transform' )]
		footLocs       = [x.encode('UTF8') for x in mc.ls('pos_foot?'       , type = 'transform' )]

		#SUBRIG
		self.Global = rigCtrl(        n = 'global' , pos = globalLocs , form = 'crossArrow' , colors = ['green']   , ctrlVisPriority = 1 , ctrlScale = self.ctrlScale*0.4 )
		self.Body   = rigCtrl(        n = 'body'   , pos = bodyLocs   , form = 'cube'       , colors = ['yellow']  , ctrlVisPriority = 1 , ctrlScale = self.ctrlScale*0.4 )
		self.Pelvis = rigCtrl(        n = 'pelvis' , pos = pelvisLocs , form = 'cube'       , colors = ['red']     , ctrlVisPriority = 1 , ctrlScale = self.ctrlScale*0.2 )
		self.Chest  = rigCtrl(        n = 'chest'  , pos = chestLocs  , form = 'cube'       , colors = ['red']     , ctrlVisPriority = 1 , ctrlScale = self.ctrlScale*0.2 )
		self.Head   = rigCtrl(        n = 'head'   , pos = headLocs   , form = 'cube'       , colors = ['red']     , ctrlVisPriority = 1 , ctrlScale = self.ctrlScale*0.2 )
		
		self.Spine  = rigModuleChain( n = 'spine'  , pos = spineLocs  , form = 'plane'      , colors = ['yellow']  , ctrlVisPriority = 1 , ctrlScale = self.ctrlScale*0.2 , skeleton = True  , aim = True)
		self.Neck   = rigModuleChain( n = 'neck'   , pos = neckLocs   , form = 'plane'      , colors = ['yellow']  , ctrlVisPriority = 2 , ctrlScale = self.ctrlScale*0.1 , skeleton = True  , aim = True)    
		self.Tail   = rigModuleChain( n = 'tail'   , pos = tailLocs   , form = 'circle'     , colors = ['yellow']  , ctrlVisPriority = 2 , ctrlScale = self.ctrlScale*0.05, skeleton = True  , aim = True)    
		
		self.SubRigs += [ self.Global , self.Body , self.Pelvis , self.Chest , self.Head , self.Spine , self.Neck , self.Tail ]

		self.ArmPiv  = rigCtrl(        n = 'armPiv'  , pos = armPivLocs  , form = 'cube'      , colors = ['red']     , ctrlVisPriority = 1 , ctrlScale = self.ctrlScale*0.2 )
		#self.Arm     = rigModuleArm(   n = 'arm'     , pos = armLocs     , ik = True          , skeleton = True      , ctrlVisPriority = 1 , ctrlScale = self.ctrlScale*0.15 )
		#self.Scapula = rigCtrl(        n = 'scapula' , pos = scapulaLocs , form = 'cube'      , colors = ['red']     , ctrlVisPriority = 1 , ctrlScale = self.ctrlScale*0.2 )		
		#self.Hand    = rigModuleChain( n = 'hand'    , pos = handLocs    , form = 'plane'     , colors = ['yellow']  , ctrlVisPriority = 1 , ctrlScale = self.ctrlScale*0.2 , skeleton = True  , aim = True)

		self.Leg    = rigModuleArm(   n = 'leg'    , pos = legLocs     , ik = True , skeleton = True                , ctrlVisPriority = 1 , ctrlScale = self.ctrlScale*0.15 ) 
		self.Foot   = rigModuleChain( n = 'foot'   , pos = footLocs    , form = 'plane'     , colors = ['yellow']   , ctrlVisPriority = 1 , ctrlScale = self.ctrlScale*0.2 , skeleton = True  , aim = True)

		#SUBRIG MIRROR
		args = {}
		args['value']             = [0,0,0 , 0,1,0 , 0,0,1]
		args['mode']              = 'mirror'
		args['pivot']             = [0,0,0 , 0,0,0 , 1,1,1]
		args['namePrefix']        = ['r','l']
		args['nameReplace']       = ['','']
		args['nameIncr']          = ''
		args['nameAdd']           = []
		args['noneMirrorAxe']     = 4

		self.ArmPivL  , self.ArmPivR  = self.ArmPiv.duplicate(  **args ) 
		#self.ArmL     , self.ArmR     = self.Arm.duplicate(     **args )    
		#self.ScapulaL , self.ScapulaR = self.Scapula.duplicate( **args )
		#self.HandL    , self.HandR    = self.Hand.duplicate(    **args )   
		self.LegL     , self.LegR     = self.Leg.duplicate(     **args )    
		self.FootL    , self.FootR    = self.Foot.duplicate(    **args ) 

		self.SubRigs += [ self.ArmPivL , self.ArmPivR ] #, self.ArmL , self.ArmR , self.ScapulaL , self.ScapulaR , self.HandL , self.HandR ]  
		self.SubRigs += [ self.LegL , self.LegR , self.FootL , self.FootR ]
		#PARENT								
		#LINK	
		self.Link.add( 'paRootGlobal'   , Sources = [ self.Root.outs[0]   ] , Destinations = [ self.Global.ins[0]                                            ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )
		self.Link.add( 'paGlobalBody'   , Sources = [ self.Global.outs[0] ] , Destinations = [ self.Body.ins[0]                                              ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )	
		self.Link.add( 'paBody'         , Sources = [ self.Body.outs[0]   ] , Destinations = [ self.Pelvis.ins[0] , self.Chest.ins[0] , self.Spine.ins[0]    ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )			
		self.Link.add( 'paPelvis'       , Sources = [ self.Pelvis.outs[0] ] , Destinations = [ self.Tail.ins[0] , self.LegL.ins[0]    , self.LegR.ins[0]     ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )
		self.Link.add( 'paSpine'        , Sources = [ self.Spine.outs[-1] ] , Destinations = [ self.Neck.ins[0] , self.ArmPivL.ins[0] , self.ArmPivR.ins[0]  ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )	
		self.Link.add( 'paNeck'         , Sources = [ self.Neck.outs[0]   ] , Destinations = [ self.Head.ins[0]                                              ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )			
		
		self.Link.add( 'paLegL'         , Sources = [ self.LegL.outs[4]  ] , Destinations = [ self.FootL.ins[0]  ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )		
		self.Link.add( 'paLegR'         , Sources = [ self.LegR.outs[4]  ] , Destinations = [ self.FootR.ins[0]  ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )			
		
		#self.Link.add( 'paArmPivL'      , Sources = [ self.ArmPivL.outs[0] ] , Destinations = [ self.ArmL.ins[0]      ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )
		#self.Link.add( 'paArmScapulaL'  , Sources = [ self.ArmL.outs[0]    ] , Destinations = [ self.ScapulaL.ins[0]  ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )	
		#self.Link.add( 'paArmHandL'     , Sources = [ self.ArmL.outs[4]    ] , Destinations = [ self.HandL.ins[0]     ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )		


		#self.Link.add( 'paArmPivR'      , Sources = [ self.ArmPivL.outs[0] ] , Destinations = [ self.ArmL.ins[0]      ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )
		#self.Link.add( 'paArmScapulaR'  , Sources = [ self.ArmL.outs[0]    ] , Destinations = [ self.ScapulaL.ins[0]  ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )	
		#self.Link.add( 'paArmHandR'     , Sources = [ self.ArmL.outs[4]    ] , Destinations = [ self.HandL.ins[0]     ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )					

		#PARENT	
		#CLASSE UTILS
		#CLASSE MODIF
		#INSTANCE MODIF
		name = args.get( 'n' , None )	
		if not( name == None ): self.Name.add( 'base' , copy = name ) 

		'''											
		if not( shape  == None ): self.CurveShape.add(  'ctrl'    , shape                 )
		if not( form   == None ): self.CurveShape.add(  'ctrl'    , { 'form'   : form   } )
		if not( colors == None ): self.CurveShape.add(  'ctrl'    , { 'colors' : colors } )	
		'''


	def postBuild( self ):
		pass