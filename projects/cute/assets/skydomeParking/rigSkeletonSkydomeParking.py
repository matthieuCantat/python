
'''







############################################################################ BUILD SKELETON
import maya.cmds as mc
import python
from python.projects.cute.assets.skydomeParking.rigSkeletonSkydomeParking import *
reload( python.projects.cute.assets.skydomeParking.rigSkeletonSkydomeParking)
#___________________________________________________________________________LOAD RIG BASE
from python.classe.readWriteInfo import *
reload(python.classe.readWriteInfo)
rwi = readWriteInfo()
rwi.mayaScene_load( 'D:/mcantat_BDD/projects/cute/assets/skydomeParking/maya/scenes/skydomeParking_rigBase.ma' , open = True )
#___________________________________________________________________________LOAD RIG BASE

import python.utils.utilsMaya as utilsMaya
utilsMaya.setSceneUnitToMeter()


#BUILD
puppet = rigSkeletonSkydomeParking()
puppet.printBuild = 1	
toExec = puppet.build()
exec(toExec)


#CLEAN ROOT 
toKeep = ['rigPuppet_GRP','all_GRP']
rootElem = mc.ls("|*" , type = "transform")
rootElem = [ elem for elem in rootElem if not (elem in toKeep ) ]
mc.delete(rootElem)


#___________________________________________________________________________SAVE TO SKELETON
rwi.mayaScene_save( 'D:/mcantat_BDD/projects/cute/assets/skydomeParking/maya/scenes/skydomeParking_rigSkeleton.ma' )
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


       
class rigSkeletonSkydomeParking(rigPuppet):

	def __init__( self , **args ):
		rigPuppet.__init__( self , **args )
		#UTILS	
		#CLASSE
		self.classeType = 'rigSkeletonSkydomeParking'
		#NAME
		self.Name.add( 'quadri' , baseName = self.classeType    , type = 'GRP' )			
		#INSTANCE_______________________________BLUEPRINT
		posLocs           = ['pos_pos1' ]
		trajLocs          = ['pos_traj1']
		bodyLocs          = ['pos_body1']
		sunLocs           = ['pos_sun1']
		#NAME
		self.Name.add( 'pos'   , baseName = 'pos'    )
		self.Name.add( 'traj'  , baseName = 'traj'   )	
		self.Name.add( 'body'  , baseName = 'body'   )
		self.Name.add( 'sun'   , baseName = 'sun'  )			
		#MAIN CTRLS
		self.Position = rigSkeletonChain( n = self.Name.pos , pos = posLocs  , parent = self.Name.topNode )
		self.Traj     = rigSkeletonChain( n = self.Name.traj  , pos = trajLocs  , parent = self.Position.outs[-1]  )
		self.Body     = rigSkeletonChain( n = self.Name.body  , pos = bodyLocs  , parent = self.Traj.outs[-1] )

		self.Sun     = rigSkeletonChain( n = self.Name.sun , pos = sunLocs  , parent = self.Body.outs[-1] )


		self.SubRigs     += [ self.Position , self.Traj , self.Body , self.Sun  ]		
		self.SubRigsName += [     'Position' ,    'Traj',     'Body', 	  'Sun' ]	

		#Attrs CTRLS
		self.Attr.add( 'vp2'    , Name = self.Position.outs[0] , attrName = ['vp2']     , attrType = ['intOnOff']    , attrValue = [0] )	
		self.Attr.add( 'arnold' , Name = self.Position.outs[0] , attrName = ['arnold']  , attrType = ['intOnOff'] , attrValue = [1] )			
		#CLASSE UTILS

		#UPDATE
		name = args.get( 'n'   , None )	
		pos  = args.get( 'pos' , None )
		if not( name == None ): self.Name.add( 'base' , copy = name ) 
		if not( pos  == None ): pass


       