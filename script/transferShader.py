

'''
	name:  transferShader
	type:  MODELING
	tag:   shader
	date:  01/09/2016	
	input: two or more obj/face

	find the shader of the first elem and apply to the second	
'''


import maya.cmds as mc
from ..utils import utilsBin
from ..utils import utilsMaya
global customTmpHotkeyVar


def transferShader():
	
	nameSpaceInMaya = 'toolBox.tools.transferShader.transferShader'
	
	global customTmpHotkeyVar	
	customTmpHotkeyVar = utilsBin.customTmpHotkeyManager()
	customTmpHotkeyVar.addHotkey( 'saveShader'  , 'c' , 'ctrl' , 'transferShader_savedShader = {0}.transferShader_saveShader()'.format(nameSpaceInMaya) )
	customTmpHotkeyVar.addHotkey( 'applyShader' , 'v' , 'ctrl' , '{0}.transferShader_applyShader(transferShader_savedShader)'.format(nameSpaceInMaya)   )
	customTmpHotkeyVar.nameSpace = nameSpaceInMaya	
	customTmpHotkeyVar.doIt()

#___________________________________________________________________________________________ transferShader_saveShader	
def transferShader_saveShader():
	selection = mc.ls(sl=True)
	shaders = utilsMaya.getShadersOfObj(selection)
	return shaders
	
	
#___________________________________________________________________________________________ transferShader_applyShader	
def transferShader_applyShader(shaders):	
	
	selection = mc.ls(sl=True)
	utilsMaya.setShaderToObj( shaders[0] , selection )	
	return 1
