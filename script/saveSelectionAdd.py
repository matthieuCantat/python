

'''
	name:  saveSelectionAdd
	type:  ALL
	tag:   utils
	date:  20/04/2016	
	input: select objs

	save the selection into a variable
'''


import maya.cmds as mc
global toolBoxSelectionSave	

def saveSelectionAdd():
	global toolBoxSelectionSave	
	toolBoxSelectionSave = mc.ls( sl = True )
	#toolBoxWindow.modifUI_sectionSaveTool(toolBoxSelectionSave)