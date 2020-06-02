
'''
	name:  setToDvValue
	type:  AUTRE
	tag:   dv
	date:  15/10/2016	
	input: selected Objs
	
	set the attr to it dv value
	its define by an attribute named dv_something in the obj

	
'''
import maya.cmds as mc
from ..utils import utilsMaya 

def setToDvValues():
	selection = mc.ls(sl=True)
	for elem in selection:
		utilsMaya.setToCustomDv(elem)
		
	print('=== Apply Defaut Values ===')