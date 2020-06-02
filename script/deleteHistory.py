
'''
	name:  deleteHistory
	type:  ALL
	tag:   maya
	date:  01/01/2012	
	input: select objs

	delete history of maya
'''


import maya.cmds as mc


def deleteHistory(): 
	mc.DeleteHistory()