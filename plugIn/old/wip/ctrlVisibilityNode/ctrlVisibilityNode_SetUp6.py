import maya.cmds as mc

#_____________________________________________________________________________________________________________________________________ findBBmanips


def findBBmanips():

	BBmanips = []
	BBattr   = 'BBreelCoords_1'
	manips   = mc.ls( '*_ctrl' , r = 1 , typ = 'transform' )

	for manip in manips :
	    if( mc.objExists( manip + '.' + BBattr ) ):
	        BBmanips.append( manip )  

	return BBmanips 



#_____________________________________________________________________________________________________________________________________ getBarycentre

def getBarycentre( coords ):
	
	i = 0
	
	barycentre = [ 0 , 0 , 0 ]
	
	for i in range(0 , len(coords) , 3 ):
		barycentre[0] += coords[i + 0] 
		barycentre[1] += coords[i + 1]
		barycentre[2] += coords[i + 2]

	barycentre[0] /= len(coords)
	barycentre[1] /= len(coords)
	barycentre[2] /= len(coords)					
	
		
	return barycentre


#_____________________________________________________________________________________________________________________________________ extractBBRotCoordsAttr

def extractBBRotCoordsAttr( ctrl ):

	coords = []
	attr   = 'BBreelCoords_1'
	
	coordsString  = mc.getAttr ( ctrl + '.' + attr) 
	coordsStrings = coordsString.split(' ')
	

	for elem in coordsStrings:	
		try:coords.append( float(elem) )
		except:pass 		

	return coords

	

#_____________________________________________________________________________________________________________________________________ ctrlVisibilityNode_setUp


def ctrlVisibilityNode_setUp(  masterManips , slaveManips ):
	
	
	mc.loadPlugin( '/u/mcantat/Sandbox/script/ctrlVisibilityNode/ctrlVisibilityNode6.py' , qt = True)
	i = 0
	
	for slaveManip in slaveManips :
		
		mc.select( cl = True )
		mc.select( masterManips )
		mc.select( slaveManip , add = True )
		
		print( ' %s  %r / %r ' %(slaveManip,i,len(slaveManips)) )
		
		nodeName = mc.createNode("ctrlVisibilityNode" , ss= True)
				
		for manip in masterManips:
			mc.connectAttr( ('%s.worldMatrix[0]'%( manip ) ) , ( '%s.inputMasterMatrix'%( nodeName ) ) )
	
		mc.connectAttr( ( '%s.outputSlavesBool' %( nodeName ) ), ( '%s.object_display' %( slaveManip ) ) )			
		
		
		
#_____________________________________________________________________________________________________________________________________ ctrlVisibilitySys_create		
		
		
	

def ctrlVisibilitySys_create():
	
	
	masterManip = mc.ls( sl = True )
	
	slaveManip = findBBmanips()
	
	for elem in masterManip :
		slaveManip.remove(elem)
		
	ctrlVisibilityNode_setUp( masterManip , slaveManip )	 #<----------------

	
	
ctrlVisibilitySys_create()



'''


import sys


sys.path.append('/u/mcantat/Sandbox/script/ctrlVisibilityNode/')


/u/mcantat/Sandbox/script/ctrlVisibilityNode/ctrlVisibilityNode_SetUp.py

import ctrlVisibilityNode_SetUp as cv 

'''
