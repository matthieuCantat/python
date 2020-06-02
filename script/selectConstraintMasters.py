
'''
	name:  selectConstraintMasters
	type:  RIGGING
	tag:   constraint
	date:  17/01/2017	
	input: objs selected


'''


import maya.cmds as mc
from ..utils import utilsMaya               


def selectConstraintMasters():
		                                                        		
	selection = mc.ls( sl = True )
	masters = []
	for elem in selection:
		masters += utilsMaya.getConstraintMasters( elem )
		
	mc.select( masters )
