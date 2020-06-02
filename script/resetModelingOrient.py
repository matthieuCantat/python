'''
	name:  resetModelingOrient
	type:  MODELING
	tag:   orient
	date:  22/04/2016	
	input: selected geometry
	
	find the orient value of an obj base on his geometry
'''

#doit marcher pour modeling sous parent ayant des transform

import maya.cmds as mc
import maya.OpenMaya as om

from ..utils import utilsMaya
from ..utils import utilsPython
from .buildLocator import buildLocator


def resetModelingOrient():
	
	selection = mc.ls( sl = True )

	selectionVtx = utilsMaya.convertFaceEdgeTovtx( selection )	
	dicoIndexs   = utilsPython.getDictIndexsOfObjs(selectionVtx)
	
	#start   convert non-component obj into component
	for elem in selection:
		if not ( '.' in elem ):
			nbrVtx = mc.polyEvaluate( elem , vertex = True )
			mc.select( '{0}.vtx[0:{1}]'.format( elem , nbrVtx ) , add = True )
			mc.select( elem , d = True)			
	#end

	
	createdLocs  = buildLocator.buildLocator()
	
	attrs = [ 'translateX' , 'translateY' , 'translateZ' , 'rotateX' , 'rotateY' , 'rotateZ' ]	
	
	for i in range( 0 , len( dicoIndexs.keys() ) ):
		father = mc.listRelatives( dicoIndexs.keys()[i] , p = True )
		if not( father == None ):
			mc.parent( createdLocs[i] , father[0] )
		
		posRot = [] 
		for attr in attrs:
			posRot.append( mc.getAttr( createdLocs[i] + '.' + attr ) )
		
		resetObj( dicoIndexs.keys()[i] , posRot )
		mc.delete(createdLocs[i])
		
	mc.select(dicoIndexs.keys())

#====================================================================================================================================
#==================================================================================================================           other
#====================================================================================================================================


#__________________________________________________________________________________________________________________ resetObj

def resetObj( baseName , posRot ):
	
	defautRotateOrder = 0 	
	invRotateOrder = 5 	
	
	mc.xform( baseName , ws = True,  piv = posRot[0:3]  )
	
	mc.makeIdentity( baseName , a = True , t = True , r = True , s = True )
	
	mc.setAttr( ( baseName + '.rotateOrder' ) , invRotateOrder )
	
	
	mc.setAttr( ( baseName + '.rx'), ( posRot[3] * -1 )   )
	mc.setAttr( ( baseName + '.ry'), ( posRot[4] * -1 )   )
	mc.setAttr( ( baseName + '.rz'), ( posRot[5] * -1 )   )

	mc.makeIdentity( baseName , a = True , t = True , r = True , s = True )
		
	mc.setAttr( ( baseName + '.rotateOrder' ) , defautRotateOrder )

	
	mc.setAttr( ( baseName + '.rx'), ( posRot[3]  )   )
	mc.setAttr( ( baseName + '.ry'), ( posRot[4]  )   )
	mc.setAttr( ( baseName + '.rz'), ( posRot[5]  )   )


	
	