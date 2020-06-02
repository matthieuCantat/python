
'''
	name:  buildConstaint2by2
	type:  RIGGING
	tag:   constraint
	date:  01/01/2014	
	input: two or more objs selected

	one master for one slave:
	master--->slave master--->slave 
'''

import maya.cmds as mc
from ..utils import utilsMaya           

	
                                                                                                
def buildConstaint2by2( ):     
		                                                               		
	selection = mc.ls( sl = True )		
	masters = utilsMaya.buildConstraint( selection , [ 'parent' , 'scale' ] , '2by2' )		
	mc.select( masters )


