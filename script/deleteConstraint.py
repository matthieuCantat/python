
'''
	name:  deleteConstraint
	type:  RIGGING
	tag:   constraint
	date:  03/01/2012	
	input: select objs

	delete constraints of maya
'''

import maya.cmds as mc 


def deleteConstraint():
	#mc.DeleteConstraints()
	
	selection = mc.ls( sl = True )
	
	for elem in selection:
		constraints = mc.listRelatives( elem , c = True , typ = [ 'parentConstraint' ,'scaleConstraint' ,'pointConstraint' ,'orientConstraint' ,'aimConstraint' ] )
		mc.delete( constraints )
