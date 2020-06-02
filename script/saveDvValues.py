
'''
	name:  saveDvValues
	type:  AUTRE
	tag:   dv
	date:  15/10/2016	
	input: selected Objs

	with the manipulable attrs of objs. write new attrs dv_someting for storing actual attrs.
	if attr already exist, change only the value on it
	
	
'''

import maya.cmds as mc
from ..utils import utilsMaya

def saveDvValues():
	
	selection = mc.ls(sl=True)
	
	for elem in selection:	
		manipulableAttrs = utilsMaya.getManipulableAttr(elem)
		utilsMaya.writeCustomDv( elem , manipulableAttrs )
		
	print('=== save Defaut Values ===')