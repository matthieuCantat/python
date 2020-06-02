

'''
	name:  snap
	type:  ALL
	tag:   utils
	date:  21/04/2016	
	input: obj and  obj or component

	snap the first object to the second
	
		
'''



import maya.cmds as mc
from .buildLocator import buildLocator



def snap():
	
	tAttrs = [ 'translateX' , 'translateY' , 'translateZ' ]
	rAttrs = [ 'rotateX'    , 'rotateY'    , 'rotateZ' ]
	
	axe = [ 'x' , 'y' , 'z' ]
	
	selection = mc.ls( sl = True )
	
	skipTranslate = []
	
	for i in range( 0 , 3 ):
		lock = mc.getAttr( ( selection[-1] + '.' + tAttrs[i] ) , l = True )
		if( lock ):
			skipTranslate.append( axe[i] )
			
	skipRotate = []
	
	for i in range( 0 , 3 ):
		lock = mc.getAttr( ( selection[-1] + '.' + rAttrs[i] ) , l = True )
		if( lock ):
			skipRotate.append( axe[i] )
			
		
	mc.select( cl = True )
	mc.select( selection[0:-1] )
	

	newLoc = buildLocator.buildLocator() 

	

	mc.delete( mc.parentConstraint( newLoc, selection[-1], st = skipTranslate , sr = skipRotate ) )
	mc.delete(newLoc)
	
	print('___DONE___')
		
		