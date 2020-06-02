
	
'''




############################################################################ BUILD RIG PUPPET

import maya.cmds as mc
import python
from python.projects.cute.assets.camera.rigPuppetCamera import *
reload( python.projects.cute.assets.camera.rigPuppetCamera)

#____________________________________________________________________________LOAD SKELETON
from python.classe.readWriteInfo import *
reload(python.classe.readWriteInfo)
rwi = readWriteInfo()
rwi.mayaScene_load( 'D:/mcantat_BDD/projects/cute/assets/camera/maya/scenes/camera_rigBoundB.ma' , open = True )
#____________________________________________________________________________LOAD SKELETON


#BUILD
puppet = rigPuppetCamera()	
puppet.debug = 1
toExec = puppet.build()
exec(toExec)


#____________________________________________________________________________LOAD SHAPE
from python.utils.utilsRigPuppet import *
reload( python.utils.utilsRigPuppet )
path = 'D:/mcantat_BDD/projects/cute/assets/camera/maya/scenes/camera_utils_ctrlShape.ma'
rigPuppet_importAndReplaceCtrlShape( path , adjustPosition = False )
#rwi.mayaScene_save( path )
#____________________________________________________________________________LOAD SHAPE

mc.connectAttr( "traj_CTRL.clipPlaneVis" , "pos0_JNT.clipPlaneVis" )
mc.connectAttr( "traj_CTRL.shotRangeMin" , "pos0_JNT.shotRangeMin" )
mc.connectAttr( "traj_CTRL.shotRangeMax" , "pos0_JNT.shotRangeMax" )
mc.connectAttr( "traj_CTRL.rimLight" , "pos0_JNT.rimLight" )

#CLEAN ROOT 
toKeep = ['rigPuppet_GRP']
rootElem = mc.ls("|*" , type = "transform")
rootElem = [ elem for elem in rootElem if not (elem in toKeep ) ]
mc.delete(rootElem)


#____________________________________________________________________________SAVE TO RIG PUPPET
from python.classe.readWriteInfo import *
reload(python.classe.readWriteInfo)
rwi = readWriteInfo()
rwi.mayaScene_save( 'D:/mcantat_BDD/projects/cute/assets/camera/maya/scenes/camera_rigPuppet.ma' )
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


       
class rigPuppetCamera(rigPuppet):

	def __init__( self , **args ):
		rigPuppet.__init__( self , **args )
		#UTILS	
		#CLASSE

		self.classeType = 'rigCamera'
		#NAME
		self.Name.add( 'cam' , baseName = self.classeType    , type = 'GRP' )			
		#INSTANCE_______________________________BLUEPRINT
		posLocs           = ['pos0_JNT' ]
		trajLocs          = ['traj0_JNT']
		bodyLocs          = ['body0_JNT']
		nearClipPlaneLocs = ['nearClipPlane0_JNT']
		farClipPlaneLocs  = ['farClipPlane0_JNT' ]
		#NAME
		self.Name.add( 'pos'   , baseName = 'pos'    )
		self.Name.add( 'traj'  , baseName = 'traj'   )	
		self.Name.add( 'body'  , baseName = 'body'   )
		self.Name.add( 'nearClipPlane' , baseName = 'nearClipPlane'  )
		self.Name.add( 'farClipPlane'  , baseName = 'farClipPlane'   )			
		#MAIN CTRLS
		self.Position      = rigCtrl(  n = self.Name.pos   , pos = posLocs   , form = 'plane'       , colors = ['green']  , ctrlVisPriority = 2  , parent  = self.Name.topNode )
		self.Traj          = rigCtrl(  n = self.Name.traj  , pos = trajLocs  , form = 'crossArrow'  , colors = ['yellow'] , ctrlVisPriority = 2  , parent  = self.Name.topNode , attrStates = [['t','r']] )
		self.Body          = rigCtrl(  n = self.Name.body  , pos = bodyLocs  , form = 'plane'       , colors = ['red']    , ctrlVisPriority = 2  , parent  = self.Name.topNode , attrStates = [['t','r']] )

		self.NearClipPlane = rigCtrl(  n = self.Name.nearClipPlane  , pos = nearClipPlaneLocs  , form = 'plane'  , colors = ['red']  , ctrlVisPriority = 4  , parent  = self.Name.topNode , attrStates = [['tx']] )
		self.FarClipPlane  = rigCtrl(  n = self.Name.farClipPlane   , pos = farClipPlaneLocs   , form = 'plane'  , colors = ['red']  , ctrlVisPriority = 4  , parent  = self.Name.topNode , attrStates = [['tx']] )

		self.SubRigs     += [ self.Position , self.Traj , self.Body , self.NearClipPlane , self.FarClipPlane  ]		
		self.SubRigsName += [     'Position' ,    'Traj',     'Body',     'NearClipPlane',     'FarClipPlane' ]	

		#LINKS
		self.Attr.add( 'clipPlaneVis'  , Name = self.Traj.Name.ctrl      , attrName = ['clipPlaneVis']   , attrType = ['intOnOff'] , attrValue = [0]       )
		self.Attr.add( 'shotRangeMin'  , Name = self.Traj.Name.ctrl      , attrName = ['shotRangeMin']   , attrType = ['int'] , attrValue = [1001]       )			
		self.Attr.add( 'shotRangeMax'  , Name = self.Traj.Name.ctrl      , attrName = ['shotRangeMax']   , attrType = ['int'] , attrValue = [1200]       )	
		self.Attr.add( 'rimLight'      , Name = self.Traj.Name.ctrl      , attrName = ['rimLight']       , attrType = ['intOnOff'] , attrValue = [0]     )
		#CLASSE UTILS

		#UPDATE
		name = args.get( 'n'   , None )	
		pos  = args.get( 'pos' , None )
		if not( name == None ): self.Name.add( 'base' , copy = name ) 
		if not( pos  == None ): pass
