
'''
	name:  buildConstaintOneMaster
	type:  RIGGING
	tag:   constraint
	date:  01/01/2014	
	input: two or more objs selected

	one master for many slaves:
	master--->slave --->slave --->slave  
'''


import maya.cmds as mc
from ..utils import utilsMaya               


def buildConstaintOneMaster():
		                                                        		
	selection = mc.ls( sl = True )		
	masters = utilsMaya.buildConstraint( selection , [ 'parent' , 'scale' ] , 'oneMaster' )		
	mc.select( masters )
	                               
	
	                                                                                                                                                                                                                              		