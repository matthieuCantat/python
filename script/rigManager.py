

'''
	name:  mirrorManip
	type:  RIGGING
	tag:   manip
	date:  06/11/2016	
	input: selected manip
	----------------------------------------------------------
	mirror manip
	
'''

from ..classe import rigManagerClass


#__________________________________________________________________________________________________________________________ main proc

def rigManager():

	exec('rigManagerVar = rigManagerClass.rigManager() ') in globals()
	exec('rigManagerVar.variableNameInGlobal = "toolBox.tools.rigManager.rigManager.rigManagerVar"') in globals()
	exec('rigManagerVar.mainUi()') in globals()
	
