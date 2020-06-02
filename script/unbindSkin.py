
'''
	name:  unbindSkin
	type:  RIGGING
	tag:   skin
	date:  02/01/2012	
	input: objs skined

	unbind Skin of maya
'''


import maya.cmds as mc


def unbindSkin():
	mc.DetachSkin()()