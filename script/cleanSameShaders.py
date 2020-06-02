
'''
	name:  cleanSameShaders
	type:  AUTRE
	tag:   clean
	date:  15/10/2016	
	input: select 3 or 4 objs

	regoupe similar shaders in the scene
'''

from ..utils import utilsMaya 

def cleanSameShaders():
	utilsMaya.cleanSceneDupliShader()
	print('=== clean dupli shader ===')