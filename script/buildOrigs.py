
'''
	name:  buildOrigs
	type:  RIGGING
	tag:   build
	date:  25/01/2015	
	input: a selected obj

	Build transform with the same space values than the selected obj.
	Put the selected obj under this transform
'''


import maya.cmds as mc
from ..utils import utils   


def buildOrigs(): 

	
	selection = mc.ls( sl = True )
	
	for elem in selection:
		utils.buildOrig( elem )
		
	mc.select(selection)