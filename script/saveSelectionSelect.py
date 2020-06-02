'''
	name:  saveSelectionSelect
	type:  ALL
	tag:   utils
	date:  20/04/2016
	input: select objs

	select the selection saved into a variable
'''



from .saveSelectionAdd import saveSelectionAdd

import maya.cmds as mc

def saveSelectionSelect():
	mc.select( saveSelectionAdd.toolBoxSelectionSave , add = True )
