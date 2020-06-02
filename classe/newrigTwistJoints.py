
import copy
import inspect
import types
import maya.cmds as mc
from ..utils import utilsMaya
from ..utils import utilsMath
from ..utils import utilsPython
from ..utils import utilsMayaApi
from . import trs
from . import readWriteInfo
from .rig import *
	
       
class rigTwistJoints(rig):

	'''
		simple utils rig
		with no ctrl for the animation

		in out attr
		top node
		scale
	'''	

	def __init__( self ):
		nameI = classeName.name()
		#UTILS
		self.utilsAttrToMirror = [ 'side' , 'buildTrs' , 'topNode' ]									
		#CLASSE
		self.classeType = 'rigTwistJoints'
		#INSTANCE	
		self.value      = None				
		self.side       = ''
		self.baseName   = 'default' 
		self.ins        = []
		self.outs       = []
		self.topNode    = ''  		
		#RIG ELEMENTS
		self.subRigObjs       = []					 							  		
		#SPACE       
		self.buildTrs         = []



	def buildRig( self ):
		# gather info
		self.buildTrs
		self.baseName
		self.topNode    = ''
		self.side       = ''
		# create setup
		#.....
		#.....
		#.....
		#.....
		#fill info
		self.ins        = []
		self.outs       = []
		
		return self	

