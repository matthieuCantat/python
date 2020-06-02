'''

import python
from python.classe.rig import *
from python.classe.rigCtrl import *
from python.classe.rigSkeletonChain import *
from python.classe.rigStretchyJoint import *

from python.classe.rigModule import *
from python.classe.rigModuleArm import *
from python.classe.rigModuleChain import *
from python.classe.rigModulePiston import *
from python.classe.rigModuleProjector import *
from python.classe.rigModuleRotatingBeacon import *

from python.classe.rigPuppet import *
from python.classe.rigPuppetCarrierShip import *
from python.classe.rigPuppetCarrierShip_backPropulsor import *
from python.classe.rigPuppetCarrierShip_frontReactor import *
from python.classe.rigPuppetCarrierShip_sideHook import *
from python.classe.rigPuppetHowie import *

reload( python.classe.rig)
reload( python.classe.rigCtrl)
reload( python.classe.rigSkeletonChain)
reload( python.classe.rigStretchyJoint)

reload( python.classe.rigModule)
reload( python.classe.rigModuleArm)
reload( python.classe.rigModuleChain)
reload( python.classe.rigModulePiston)
reload( python.classe.rigModuleProjector)
reload( python.classe.rigModuleRotatingBeacon)

reload( python.classe.rigPuppet)
reload( python.classe.rigPuppetCarrierShip)
reload( python.classe.rigPuppetCarrierShip_backPropulsor)
reload( python.classe.rigPuppetCarrierShip_frontReactor)
reload( python.classe.rigPuppetCarrierShip_sideHook)
reload( python.classe.rigPuppetHowie)

#******************************************************** BUILD EXEMPLE RIG CTRL
import maya.cmds as mc
import python
from python.classe.rigCtrl import *
from python.classe.mayaRig import *
reload(python.classe.mayaClasse)
reload(python.classe.mayaObject)
reload(python.classe.mayaRig)
reload(python.classe.rigCtrl)
#=================================================


manipA = mayaObject()

manipA = mayaRig()


manipA = rigCtrl( )	

manipA = rigCtrl( n = 'manipA' , pos = [5,0,3,0,0,0,1,1,1] , form = 'cube' , colors = [13] )	

# REF

from python.classe.buildName import *
reload(python.classe.buildName)
from python.classe.buildCurveShape import *
reload(python.classe.buildCurveShape)
from python.classe.buildPosition import *
reload(python.classe.buildPosition)

Name = buildName( )
Name.setBaseName('manip')
Name.add( 'manipB'        , appendBaseName = 'B'    )

Pos = buildPosition()
Pos.add(  'manipB'      , [5,0,-3,0,0,0,1,1,1]  )

cShape = buildCurveShape()
cShape.add(  'manipB' , form = 'sphere'   , colors = [13] , axe = 'x' , offset = [0,0,0,0,0,0,1,1,1]   )

manipB = rigCtrl( n = Name.manipB , pos = [ Pos.manipB ] , shape = CurveShape.manipB )	


print('____________________MODIF')
print('____________________BUILD')
manipA.build()
manipB.build()




TO IMPROVE:
-mirror orientation
-name suffix incr to fix
-documentation/presentation
-add other rig and modules

'''

from .mayaObject import *

class rig(mayaObject):

	def __init__( self , **args ):
		mayaObject.__init__( self , **args )
		#UTILS			
		#CLASSE
		self.classeType = 'rig'
		self.depthLevel = 0															
		#INSTANCE_______________________________BLUEPRINT
		self.Name.add( 'base'    , baseName = self.classeType )			
		#INSTANCE_______________________________INFO
		self.ins        = []
		self.insAnim    = []
		self.outs       = []
		self.ctrls      = []
		self.ctrlsDupli = []

	def buildMayaObject( self ):
		self.buildMayaRig()

	def buildMayaRig( self ):
		pass

