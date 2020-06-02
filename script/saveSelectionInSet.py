
'''
	name:  saveSelectionInSet
	type:  ALL
	tag:   set
	date:  16/01/2017	
	input: selected Objs

	save selection in a set created for the occasion
	
	
'''

import maya.cmds as mc
from ..utils import utilsMaya

def saveSelectionInSet():
	
	setName = 'rigManagerTmpSet'
	'''
	if( mc.objExists(setName) == 1 ):
		mc.delete( setName )
		
	'''
	
	mc.sets( n = setName )		
	
