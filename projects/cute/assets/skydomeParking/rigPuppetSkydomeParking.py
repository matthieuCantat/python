
	
'''





############################################################################ BUILD RIG PUPPET

import maya.cmds as mc
import python
from python.projects.cute.assets.skydomeParking.rigPuppetSkydomeParking import *
reload( python.projects.cute.assets.skydomeParking.rigPuppetSkydomeParking)

#____________________________________________________________________________LOAD SKELETON
from python.classe.readWriteInfo import *
reload(python.classe.readWriteInfo)
rwi = readWriteInfo()
rwi.mayaScene_load( 'D:/mcantat_BDD/projects/cute/assets/skydomeParking/maya/scenes/skydomeParking_rigBoundB.ma' , open = True )
#____________________________________________________________________________LOAD SKELETON


#BUILD
puppet = rigPuppetSkydomeParking()	
puppet.debug = 1
toExec = puppet.build()
exec(toExec)


#____________________________________________________________________________LOAD SHAPE
from python.utils.utilsRigPuppet import *
reload( python.utils.utilsRigPuppet )
path = 'D:/mcantat_BDD/projects/cute/assets/skydomeParking/maya/scenes/skydomeParking_utils_ctrlShape.ma'
rigPuppet_importAndReplaceCtrlShape( path , adjustPosition = False )
#rwi.mayaScene_save( path )
#____________________________________________________________________________LOAD SHAPE

mc.connectAttr( "pos_CTRL.vp2" , "pos0_JNT.vp2" )
mc.connectAttr( "pos_CTRL.arnold" , "pos0_JNT.arnold" )

#CLEAN ROOT 
toKeep = ['rigPuppet_GRP']
rootElem = mc.ls("|*" , type = "transform")
rootElem = [ elem for elem in rootElem if not (elem in toKeep ) ]
mc.delete(rootElem)


#____________________________________________________________________________SAVE TO RIG PUPPET
from python.classe.readWriteInfo import *
reload(python.classe.readWriteInfo)
rwi = readWriteInfo()
rwi.mayaScene_save( 'D:/mcantat_BDD/projects/cute/assets/skydomeParking/maya/scenes/skydomeParking_rigPuppet.ma' )
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


       
class rigPuppetSkydomeParking(rigPuppet):

	def __init__( self , **args ):
		rigPuppet.__init__( self , **args )
		#UTILS	
		#CLASSE

		self.classeType = 'rigSkydomeParking'
		#NAME
		self.Name.add( 'cam' , baseName = self.classeType    , type = 'GRP' )			
		#INSTANCE_______________________________BLUEPRINT
		posLocs           = ['pos0_JNT' ]
		trajLocs          = ['traj0_JNT']
		bodyLocs          = ['body0_JNT']
		sunLocs           = ['sun0_JNT' ]
		#NAME
		self.Name.add( 'pos'   , baseName = 'pos'    )
		self.Name.add( 'traj'  , baseName = 'traj'   )	
		self.Name.add( 'body'  , baseName = 'body'   )
		self.Name.add( 'sun'   , baseName = 'sun'    )		
		#MAIN CTRLS
		self.Position      = rigCtrl(  n = self.Name.pos   , pos = posLocs   , form = 'plane'       , colors = ['green']  , ctrlVisPriority = 2  , parent  = self.Name.topNode )
		self.Traj          = rigCtrl(  n = self.Name.traj  , pos = trajLocs  , form = 'crossArrow'  , colors = ['yellow'] , ctrlVisPriority = 2  , parent  = self.Name.topNode , attrStates = [['t','r']] )
		self.Body          = rigCtrl(  n = self.Name.body  , pos = bodyLocs  , form = 'plane'       , colors = ['red']    , ctrlVisPriority = 2  , parent  = self.Name.topNode , attrStates = [['t','r']] )

		self.Sun = rigCtrl(  n = self.Name.sun  , pos = sunLocs  , form = 'arrow2sidesBend'  , colors = ['red']  , ctrlVisPriority = 4  , parent  = self.Name.topNode , attrStates = [['r']] )

		self.SubRigs     += [ self.Position , self.Traj , self.Body , self.Sun ]		
		self.SubRigsName += [     'Position' ,    'Traj',     'Body',     'Sun']	

		#LINKS
		self.Attr.add( 'vp2'    , Name = self.Position.outs[0] , attrName = ['vp2']     , attrType = ['intOnOff'] , attrValue = [1] )	
		self.Attr.add( 'arnold' , Name = self.Position.outs[0] , attrName = ['arnold']  , attrType = ['intOnOff'] , attrValue = [0] )			
		#CLASSE UTILS

		#UPDATE
		name = args.get( 'n'   , None )	
		pos  = args.get( 'pos' , None )
		if not( name == None ): self.Name.add( 'base' , copy = name ) 
		if not( pos  == None ): pass
