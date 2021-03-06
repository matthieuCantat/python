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

	
#_____________________________________________________________________________________________________________________________________ buildVisibilitySlavesLocs

def buildVisibilitySlavesLocs( ctrl ):
	
	nbrLocs = 8	
	
	axes  = [ 'X' , 'Y' , 'Z' ]	
	attrs = [ 'translate' , 'rotate' , 'scale' ]
	
	# coords
	
	coordsLocs = extractBBRotCoordsAttr( ctrl )


	# create loc
	locatorNames = []	
	
	j = 0
	
	
	for i in range( nbrLocs ):
	
		locatorName = '%s_slaveVisibility%r_loc' %( ctrl , i ) 
		mc.spaceLocator( n = locatorName )

		
		for axe in axes:
			mc.setAttr( ( locatorName + '.' + attrs[0] + axe ) , coordsLocs[j] )
			j += 1			
		
		
		mc.parent( locatorName , ctrl )		
		
		locatorNames.append( locatorName ) 
		
	
	return locatorNames
	

#_____________________________________________________________________________________________________________________________________ ctrlVisibilityNode_setUp


def ctrlVisibilityNode_setUp(  masterManips , slaveManips ):
	

	mc.loadPlugin( '/u/mcantat/Sandbox/script/ctrlVisibilityNode/ctrlVisibilityNode.py' , qt = True)
	nodeName = mc.createNode("ctrlVisibilityNode")		    
	
	
	#connectIn
	mLap = 0
	
	for manip in masterManips:
		mc.connectAttr( ('%s.worldMatrix[0]'%( manip ) ) , ( '%s.inputMasterMatrix'%( nodeName ) ) )
		bbLocators = buildVisibilitySlavesLocs( manip )
		
		for loc in bbLocators:
			mc.setAttr( ( nodeName + '.inputMasterBBmatrix[%r]'%(mLap) ) , mc.getAttr( loc + '.matrix') , type = 'matrix' )
			mLap += 1			
		
		mc.delete(bbLocators)		
		
	sLap = 0
	i = 0
		
	for manip in slaveManips:
		print( ' %s  %r / %r ' %(manip,i,len(slaveManips)) )
		mc.connectAttr( ( '%s.worldMatrix[0]' %( manip ) ), ( '%s.inputSlavesMatrix[%r]' %( nodeName , i ) ) )	
		bbLocators = buildVisibilitySlavesLocs( manip )    
		i += 1
		for loc in bbLocators:
			mc.setAttr( ( nodeName + '.inputSlavesBBMatrix[%r]'%(sLap) ) , mc.getAttr( loc + '.matrix') , type = 'matrix' )			
			sLap += 1		
			
		mc.delete(bbLocators)				
		
		
	#connectOut	
	for i in range(len(slaveManips)):		
		mc.connectAttr( ( '%s.outputSlavesBool[%r]' %( nodeName , i ) ), ( '%s.object_display' %( slaveManips[i] ) ) )			
		
		
		
#_____________________________________________________________________________________________________________________________________ ctrlVisibilitySys_create		
		
		
	

def ctrlVisibilitySys_create():
	
	
	selection = mc.ls( sl = True )
	
	bbManips = findBBmanips()
	
	for elem in selection :
		bbManips.remove(elem)
		
	ctrlVisibilityNode_setUp( selection , bbManips[0:100] )	 #<----------------

	
	
ctrlVisibilitySys_create()



'''


import sys


sys.path.append('/u/mcantat/Sandbox/script/ctrlVisibilityNode/')


/u/mcantat/Sandbox/script/ctrlVisibilityNode/ctrlVisibilityNode_SetUp.py

import ctrlVisibilityNode_SetUp as cv 

'''
