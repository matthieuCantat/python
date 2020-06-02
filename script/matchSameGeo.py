
'''
	name:  matchSameGeo
	type:  MODELING
	tag:   clean
	date:  15/10/2016	
	input: select 3 or 4 objs

	-DONT WORK-
	Build a arm in rig.
	the first 3 obj is the shoulder - elbow - wrist
	the 4th is pole vector (facultatif)
'''

import maya.cmds as mc
from ..utils import utilsMaya
from ..utils import utilsMayaApi


def matchSameGeo():
	
	selection = mc.ls(sl=True)
	
	for i in range( 0 , len(selection) , 2 ):
		trsValue = utilsMayaApi.API_getTransformDifferenceBetweenSameGeometry( selection[i] , selection[i+1] )
		utilsMaya.setTRSValueToObj( selection[i]  , trsValue )