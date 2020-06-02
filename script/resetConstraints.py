
'''
	name:  resetConstraints
	type:  RIGGING
	tag:   constraint
	date:  01/01/2014	
	input: select objs

	reset to 0 values of a obj under constraints.
'''

import maya.cmds as mc
from ..utils import utilsMaya                

	

def resetConstraints():   
	
	selection = mc.ls( sl = True )
	                                      
	for elem in selection:		
		utilsMaya.resetConstraint( elem )                                                                                                        
	    