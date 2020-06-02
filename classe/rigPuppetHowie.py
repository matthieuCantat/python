
	
'''
#******************************************************** BUILD EXEMPLE 
import maya.cmds as mc
import python
from python.classe.rigPuppetHowie import *
reload( python.classe.rigPuppetHowie)
mc.file( 'D:/mcantat_BDD/projects/flyAway/howie/maya/scenes/howie_rig.ma' , o = True , f = True  )
#=================================================
puppet = rigPuppetHowie( ctrlScale = 15 )	
puppet.printBuild = 1
toExec = puppet.build()
exec(toExec)

'''

import maya.cmds as mc

from .rigPuppet import *  
from .rigCtrl import *  
from .rigModuleChain import *     
from .rigModuleArm import *    

       
class rigPuppetHowie(rigPuppet):

	def __init__( self , **args ):
		rigPuppet.__init__( self , **args )		
		#CLASSE TYPE
		self.classeType = 'rigPuppetHowie'
		#CLASSE BLUE PRINT
		centerLocs = [x.encode('UTF8') for x in mc.ls('pos_center*' , type = 'transform' )]
		pelvisLocs = [x.encode('UTF8') for x in mc.ls('pos_pelvis*' , type = 'transform' )]
		headLocs   = [x.encode('UTF8') for x in mc.ls('pos_head*'   , type = 'transform' )]
		spineLocs  = [x.encode('UTF8') for x in mc.ls('pos_spine*'  , type = 'transform' )]
		neckLocs   = [x.encode('UTF8') for x in mc.ls('pos_neck*'   , type = 'transform' )]
		tailLocs   = [x.encode('UTF8') for x in mc.ls('pos_tail*'   , type = 'transform' )]
		armLocs    = [x.encode('UTF8') for x in mc.ls('pos_arm*'    , type = 'transform' )]
		legLocs    = [x.encode('UTF8') for x in mc.ls('pos_leg*'    , type = 'transform' )]
		self.CurveShape.add(  'root' , value = { 'form' : 'crossArrow' , 'colors' : ['green'] , 'axe' : 'y' , 'offset' : [0,0,0,0,0,0,1,1,1] , 'scale' : self.ctrlScale*1 }  )
		#SUBRIG
		self.Root   = rigCtrl(        n = 'root'   , pos = [ [0,0,0 , 0,0,0 , 1,1,1] ] , shape = self.CurveShape.root , joint = None , offset = None , ctrlVisPriority = 0  , parent = self.Name.ctrlGrp ) 	
		self.Center = rigCtrl(        n = 'center' , pos = centerLocs , form = 'crossArrow' , colors = ['green']  , ctrlVisPriority = 1 , ctrlScale = self.ctrlScale*0.4 , parent = self.Name.ctrlGrp )
		self.Pelvis = rigCtrl(        n = 'pelvis' , pos = pelvisLocs , form = 'cube'       , colors = ['red']    , ctrlVisPriority = 1 , ctrlScale = self.ctrlScale*0.2 , parent = self.Name.ctrlGrp )
		self.Head   = rigCtrl(        n = 'head'   , pos = headLocs   , form = 'cube'       , colors = ['red']    , ctrlVisPriority = 1 , ctrlScale = self.ctrlScale*0.2 , parent = self.Name.ctrlGrp )
		self.Spine  = rigModuleChain( n = 'spine'  , pos = spineLocs  , form = 'plane'      , colors = ['yellow'] , ctrlVisPriority = 1 , ctrlScale = self.ctrlScale*0.2 , skeleton = True  , aim = True)
		self.Neck   = rigModuleChain( n = 'neck'   , pos = neckLocs   , form = 'plane'      , colors = ['yellow'] , ctrlVisPriority = 2 , ctrlScale = self.ctrlScale*0.1 , skeleton = True  , aim = True)    
		self.Tail   = rigModuleChain( n = 'tail'   , pos = tailLocs   , form = 'circle'     , colors = ['yellow'] , ctrlVisPriority = 2 , ctrlScale = self.ctrlScale*0.05, skeleton = True  , aim = True)    
		self.Arm    = rigModuleArm(   n = 'arm'    , pos = armLocs    , ik = True , skeleton = True               , ctrlVisPriority = 1 , ctrlScale = self.ctrlScale*0.15 )
		self.Leg    = rigModuleArm(   n = 'leg'    , pos = legLocs    , ik = True , skeleton = True               , ctrlVisPriority = 1 , ctrlScale = self.ctrlScale*0.15 )  
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

		self.ArmL , self.ArmR = self.Arm.duplicate( **args )
		self.LegL , self.LegR = self.Leg.duplicate( **args )
		#PARENT								
		#LINK	
		self.Link.add( 'paRootCenter'   , Sources = [ self.Root.outs[0]   ] , Destinations = [ self.Center.ins[0]                  ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )
		self.Link.add( 'paCenterPelvis' , Sources = [ self.Center.outs[0] ] , Destinations = [ self.Pelvis.ins[0]                  ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )	
		self.Link.add( 'paPelvisSpine'  , Sources = [ self.Pelvis.outs[0] ] , Destinations = [ self.Spine.ins[0]                   ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )			
		self.Link.add( 'paSpineNeck'    , Sources = [ self.Spine.outs[4]  ] , Destinations = [ self.Neck.ins[0]                    ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )
		self.Link.add( 'paSpineHead'    , Sources = [ self.Spine.outs[-1] ] , Destinations = [ self.Head.ins[0]                    ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )	
		self.Link.add( 'paPelvisTail'   , Sources = [ self.Pelvis.outs[0] ] , Destinations = [ self.Tail.ins[0]                    ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )			
		self.Link.add( 'paSpineArms'    , Sources = [ self.Spine.outs[4]  ] , Destinations = [ self.ArmL.ins[0] , self.ArmR.ins[0] ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )		
		self.Link.add( 'paPelvisLegs'   , Sources = [ self.Pelvis.outs[0] ] , Destinations = [ self.LegL.ins[0] , self.LegR.ins[0] ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )	
		#PARENT
		#self.Parent.add( 'modelStore' , Name = ['howie_mesh'] , parent = self.Name.modelGrp )			
		#CLASSE UTILS
		self.SubRigs += [ self.Root , self.Center , self.Pelvis , self.Spine , self.Neck , self.Tail , self.Head , self.ArmL , self.ArmR , self.LegL , self.LegR  ]
		#CLASSE MODIF
		#INSTANCE MODIF
		name = args.get( 'n' , None )	
		if not( name == None ): self.Name.add( 'base' , copy = name ) 

		'''											
		if not( shape  == None ): self.CurveShape.add(  'ctrl'    , shape                 )
		if not( form   == None ): self.CurveShape.add(  'ctrl'    , { 'form'   : form   } )
		if not( colors == None ): self.CurveShape.add(  'ctrl'    , { 'colors' : colors } )	
		'''
