

'''
import maya.cmds as mc
import python
from python.script.alignBetween2Vertices import *
reload(python.script.alignBetween2Vertices)
alignBetween2Vertices()



'''


import math	
import maya.cmds as mc
import maya.OpenMaya as om  

from ..utils import utilsMaya  
from ..utils import utilsMayaApi  
from ..utils import utilsPython          

	


#__________________________________________________________________________________________________________________________ main proc

def alignBetween2Vertices( uniform = True ):
	
	selection = mc.filterExpand( sm = 31 )
	
	if not( len( selection ) == 2 ):
		selection = selection_getIsolateVtx()
	
	vtxsToAlign = getVerticesBetween2Vertices( selection )
	
	vtxSelection = []
	vtxSelection.append( mc.xform( selection[0] , q = True , ws = True , t = True) )
	vtxSelection.append( mc.xform( selection[1] , q = True , ws = True , t = True) )	
		
	if( uniform == True ):
		vectorRef = om.MVector( ( vtxSelection[1][0] - vtxSelection[0][0] ) , ( vtxSelection[1][1] - vtxSelection[0][1] ) , ( vtxSelection[1][2] - vtxSelection[0][2] ) )
		distIncr = vectorRef.length()/(len(vtxsToAlign) - 1)
		vectorRef.normalize()
		vIncr = vectorRef*distIncr
		
	currentCoords = vtxSelection[0]

	for i in range( 0 , len(vtxsToAlign) ):
		coords = mc.xform( vtxsToAlign[i] , q = True , ws = True , t = True)
		if( uniform == True ):
			newCoords = currentCoords[:]
			currentCoords[0] += vIncr.x
			currentCoords[1] += vIncr.y
			currentCoords[2] += vIncr.z			
		else:
			newCoords = getAlignCoords( vtxSelection , coords )
		mc.xform( vtxsToAlign[i]  , ws = True , t = newCoords )
		
	print('DONE')




#__________________________________________________________________________________________________________________________ getVerticesBetween2Vertice3	



def getVerticesBetween2Vertices( vertices ):

	if not( len( vertices ) == 2 ):
		mc.error( 'it must be 2 vertices ( getMiddleVerticesBetween2Vertices )' )
		
	mainPath = []	
	pathsA     , pathsB     = [ [ vertices[0] ] ] , [ [ vertices[1] ] ]
	distancesA , distancesB = [ 0 ]	               , [ 0 ]
	
	lap = 0
	while( mainPath == [] ):

		# A ------------------------------------------------------------------
		pathDist = [ pathsA , distancesA ]		
		pathDist = getVerticesBetween2Vertices_growPath( pathDist )		
		pathsA , distancesA  = pathDist[0] , pathDist[1] 
	
		mainPath = getVerticesBetween2Vertices_getMainPath( pathsA , pathsB )

		if not( mainPath == [] ):
			break
		# B ------------------------------------------------------------------			
		pathDist = [ pathsB , distancesB ]		
		pathDist = getVerticesBetween2Vertices_growPath( pathDist )		
		pathsB , distancesB  = pathDist[0] , pathDist[1] 
			
		mainPath = getVerticesBetween2Vertices_getMainPath( pathsA , pathsB )
				
		lap += 1	
		if( lap > 500 ):
			mc.error('loop in getVerticesBetween2Vertices!')	
		
			
	return mainPath
	

	

#__________________________________________________________________________________________________________________________ getAlignCoords	
	




def getAlignCoords( lineCoords , oldCoords ):

	vectorRef       = om.MVector( ( lineCoords[1][0] - lineCoords[0][0] ) , ( lineCoords[1][1] - lineCoords[0][1] ) , ( lineCoords[1][2] - lineCoords[0][2] ) )
	vectorOldCoords = om.MVector( ( oldCoords[0]     - lineCoords[0][0] ) , ( oldCoords[1]     - lineCoords[0][1] ) , ( oldCoords[2]     - lineCoords[0][2] ) )
	angleA          = vectorRef.angle( vectorOldCoords )
		
	dist = math.cos( angleA ) * vectorOldCoords.length()
	
	vectorRef.normalize()
		
	newCoords = [  vectorRef.x * dist + lineCoords[0][0] , vectorRef.y * dist + lineCoords[0][1] , vectorRef.z * dist + lineCoords[0][2] ] 
	
	return newCoords	
	



#__________________________________________________________________________________________________________________________ getVerticesBetween2Vertices_growPath



def getVerticesBetween2Vertices_growPath( pathDists ):


	pathsA       = pathDists[0] 
	distancesA   = pathDists[1] 	
	pathsAdd     = []
	distancesAdd = []
		
	for path in pathsA:
		
		vtxsExpend = utilsMayaApi.API_growVerticesByEdge( [ path[-1] ] , 0 )	
		
		for vtx in vtxsExpend:
			if( vtx in utilsPython.convertArrayToFlatArray( pathsA ) ):
				continue
				
			dist = utilsMayaApi.getTwoVerticesLength( path[-1] , vtx )				
			pathsAdd.append( path + [vtx]  )								
			distancesAdd.append( dist )
		
	pathsA       = pathsAdd
	distancesA   = distancesAdd
	pathsAdd     = []
	distancesAdd = []	
	iToRemove    = []
	
	for iA in range( 0 , len( pathsA ) ):
		distA = distancesA[iA]
		for iB in range( 0 , len( pathsA ) ):
			distB = distancesA[iB]
			if( pathsA[iA][-1] == pathsA[iB][-1] ):
				if(distA < distB):
					iToRemove.append(iA)
	
	for i in range( 0 ,  len(pathsA ) ):
		if( i in iToRemove):
			continue
		pathsAdd.append( pathsA[i])	
		distancesAdd.append( distancesA[i])				
	
	pathsA     = pathsAdd
	distancesA = distancesAdd	
	
	pathDists = [ pathsA , distancesA ]

	return pathDists

#__________________________________________________________________________________________________________________________ getVerticesBetween2Vertices_getMainPath

def getVerticesBetween2Vertices_getMainPath( pathsA , pathsB ):

	mainPath = []	
	
	for iA in range( 0 , len(pathsA)):
		for iB in range( 0 , len( pathsB ) ):
			for elemA in pathsA[iA]:
				if( elemA in pathsB[iB] ):
					mainPath = pathsA[iA] + list(reversed(pathsB[iB]))
					break

	return mainPath					








########################################################################################################


def convertArrayToFlatArray( array , maxlevel = 999999 ):
	
	'''
		flatten array to the minimum possible ( = down to one index)
		keep entire world for string
	'''
	currentLevel = 1
	flattenArray = array

	while not( maxlevel == currentLevel ):
		
		
		flattenArray = []
		
		sizeArray = len(array)
		noChangeLap = 0
		
		for elem in array:
			
			if( list == type( elem ) ):
				for e in elem:			
					flattenArray.append( e )
			else:
					flattenArray.append( elem )	
					noChangeLap += 1
							
		
		if( noChangeLap == sizeArray ):
			return flattenArray
				
		array = flattenArray
		currentLevel += 1
			
			
	return flattenArray	
	

def API_getMDagPath( obj ):	
	
	'''
	convert maya name into dagPath , very use to manipulate obj in API	
	'''

	selection = ompy.MSelectionList()
	selection.add( obj )
	
	dagPath= ompy.MDagPath()
	dagPath = selection.getDagPath( 0 )
	
	return dagPath
	

import re

def getObjNameAndIndex( componentName ):

	testIndex = re.search( '(?<=\[)(?P<vtxNum>[\d]+)(?=\])', str(componentName) )

	if testIndex:
		index = int(testIndex.group('vtxNum'))
		obj = componentName.split('.')[0]
	else:
		return

	return [ obj , index ]

#_____________________________________________________________________________________________________________________________________________________________________ convert vertex to edges
		
def API_convertVertexToEdges(vtxName):
	
	'''
		with the vertex's name give the edges associate
	'''
			
	vtxObj , vtxNum = getObjNameAndIndex( vtxName )	

	# Iterate over all the mesh vertices and get position of required vtx		
		
	pathDg    = API_getMDagPath(vtxObj)
	
	mItVtx    = ompy.MItMeshVertex(pathDg)
	edgeIndex = ompy.MIntArray()
	vtxPos    = []	
	
	while not mItVtx.isDone():
		if( mItVtx.index() == vtxNum ):
			edgeIndex = mItVtx.getConnectedEdges()
			break
		mItVtx.next()
		
		
	edgeNames = []		
	for i in range( 0 , edgeIndex.__len__() ):
		edgeNames.append( vtxObj + '.e[{0}]'.format(edgeIndex[i]) )
	    
	
	return edgeNames

#_____________________________________________________________________________________________________________________________________________________________________ convert edge to vertices


def API_convertEdgeToVertices(edgeName):
	
	'''
		with the edge's name give the two vertices associate
	'''

	edgeObj , edgeNum = getObjNameAndIndex( edgeName )			
		
	# Iterate over all the mesh vertices and get position of required vtx		
		
	pathDg    = API_getMDagPath(edgeObj)	
	mItVtx    = ompy.MItMeshVertex(pathDg)

	vtxNum = []	
	while not mItVtx.isDone():
		if mItVtx.connectedToEdge(edgeNum):			
			vtxNum.append( mItVtx.index() ) 
		mItVtx.next()
		
		
	vtxNames = []
	for i in range( 0 , len(vtxNum) ):
		vtxNames.append( edgeObj + '.vtx[{0}]'.format(vtxNum[i]) )
	    	
	return vtxNames

#_____________________________________________________________________________________________________________________________________________________________________ grow vertices by edge
		
def API_growVerticesByEdge( verticesBase , keepVerticesBase = 1 ):

	'''	
	Grow selection of a list a vertices. Yse keepVerticesBase = 0 for removing the input vertices	
	'''
	
	edgesGrow    = []
	
	for vtx in verticesBase:
		edgesGrow += API_convertVertexToEdges( vtx )

	edgesGrow    = list(set(edgesGrow))	
	verticesGrow = []
	
	for edge in edgesGrow:
		verticesGrow += API_convertEdgeToVertices( edge )		
		
	verticesGrow = list(set(verticesGrow))	

	
	
	if( keepVerticesBase == 0 ):	
		for v in verticesBase:
			try:verticesGrow.remove(v)
			except:pass

	return verticesGrow 	


#_____________________________________________________________________________________________________________________________________________________________________ getTwoVerticesLength
def getTwoVerticesLength( vtxA , vtxB ):

	coordA = mc.xform( vtxA , q = True , ws = True , t = True )
	coordB = mc.xform( vtxB      , q = True , ws = True , t = True )
	dist   = om.MVector( coordB[0] - coordA[0] , coordB[1] - coordA[1] , coordB[2] - coordA[2] ).length() 

	return dist 	
	

def selection_getIsolateVtx( maxConnectionAllowed = 1):
	'''
	when you select a edge of vtx, it will return the two oposite points
	usefull for tubes a

	'''
	isolateVtx = []

	selection = mc.filterExpand( sm = 31 )
	for i in range( 0 , len(selection) ):
		vtxNeighBourgs = utilsMayaApi.API_growVerticesByEdge( [ selection[i] ] , 0 )

		sharedNeighBourgCount = 0
		for j in range( 0 , len(vtxNeighBourgs) ):
			if( vtxNeighBourgs[j] in selection ):
				sharedNeighBourgCount += 1

		if( sharedNeighBourgCount <= maxConnectionAllowed ):
			isolateVtx.append(selection[i])
	
	return isolateVtx