
'''
	name:  deleteAllNameSpace
	type:  AUTRE
	tag:   clean
	date:  15/10/2016	
	input: none

	delete all the namespaces of the curent scene
'''


from ..utils import utilsMaya


def deleteAllNameSpace():
	utilsMaya.deleteAllNamespace()
	print('=== delete all namespaces ===')