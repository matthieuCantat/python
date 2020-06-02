
'''
	name:  buildConstraintProxy                                                                                                                                                                                                                             		
	type:  RIGGING
	tag:   constraint
	date:  17/01/2017
	input: objs selected
	
	one master for one slaves

	the first half of the selection is the masters and the other half the slaves
	it get the coord of each obj and classe master slave by proximity 	


'''


import maya.cmds as mc
from ..utils import utilsMaya               


def buildConstraintProxy():
		                                                        		
	selection = mc.ls( sl = True )
	middleNbr = int( len(selection)/2 )
	
	masters = selection[0:middleNbr]
	slaves  = selection[middleNbr:len(selection)]
	
	utilsMaya.buildConstraintProximity( masters , slaves , types = [ 'parent' , 'scale' ] , maintainOffset = 1 , skipAttr = [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ] )
	
	mc.select( masters )
