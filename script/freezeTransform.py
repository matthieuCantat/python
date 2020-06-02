

'''
	name:  freezeTransform
	type:  ALL
	tag:   maya
	date:  01/01/2012	
	input: select objs

	freeze Transform of maya
'''



import maya.cmds as mc

def freezeTransform():
	mc.makeIdentity( apply = True , t = 1 , r = 1 , s = 1 , n = 0 , pn = 1 )