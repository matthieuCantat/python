'''
	name:  resetControlsValue
	type:  RIGGING
	tag:   value
	date:  25/01/2015	
	input: selected objs
	
	Clean values of an obj by transfering them to his parent
'''

import sys
import maya.cmds as mc
from ..utils import utilsMaya             



def resetControlsValue():
	
	selection = mc.ls( sl = True )                 
	
	for elem in selection:		
		utilsMaya.resetControlValue( elem )                                                              