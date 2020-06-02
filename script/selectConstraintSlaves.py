
'''
	name:  selectConstraintSlaves
	type:  RIGGING
	tag:   constraint
	date:  17/01/2017	
	input: objs selected


'''


import maya.cmds as mc
from ..utils import utilsMaya               


def selectConstraintSlaves():
		                                                        		
	selection = mc.ls( sl = True )
	slaves = []
	for elem in selection:
		slaves += utilsMaya.getConstraintSlaves( elem )
		
	mc.select( slaves )
	                               
	
	                                                                                                                                                                                                                              		