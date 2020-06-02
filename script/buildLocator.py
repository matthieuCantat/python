
'''
	name:  buildLocator
	type:  ALL
	tag:   build
	date:  21/04/2016	
	input: select objs

	create locator on selected obj
	if transform, make locator oriented like transform
	if vertex, make locator oriented localBB mode
	if face or edge, convert to vertex.
'''





import maya.cmds as mc

from ..utils import utilsMaya
from ..utils import utilsPython
from ..utils import utilsMayaApi
from ..utils import utilsMath




	


def buildLocator():
	
	selection = mc.ls( sl = True ) 

	if( len(selection) == 0 ):
		return [ utilsMaya.buildSimpleLoc( 'nul' , [ 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1 ]  ) ]				
	
		
	selectionVtx = utilsMaya.convertFaceEdgeTovtx( selection )	
	print( 'selectionVtx:   ' ,selectionVtx)
	dicoIndexs   = utilsPython.getDictIndexsOfObjs(selectionVtx)
	print( 'dicoIndexs:   ' ,dicoIndexs)
	
	
	listObjs = dicoIndexs.keys()
	listObjsSorted = []
	for elem in selection:	
		for obj in listObjs:
			if( obj in elem ):
				listObjsSorted.append( obj )
				break
	
	print( 'listObjsSorted:  ' , listObjsSorted )				
				
	createdLocs = []
	
	for baseName in listObjsSorted: 
	
		#____________________________________ no componente	
		if( len( dicoIndexs[baseName] ) == 0 ):
			trsValue = utilsMaya.getWorldTrsValue( baseName )					
						
		#____________________________________ one vtx	
		elif( len( dicoIndexs[baseName] ) == 1 ):
	
			tValue = mc.xform( selection[0] , q = True , t = True , ws = True )
			
			# pour rotate
			extraComponents = growSelection( selection )
			indexs          = utilsPython.getArrayIndexsOfObjs( extraComponents )
			posRot          = utilsMayaApi.getTRSreelBB( baseName , indexs )
			# pour rotate
			
			trsValue    = tValue + posRot[3:6]  + [ 1 , 1 , 1 ]  	 					
	
			
		#____________________________________ two vtx		
		elif( len( dicoIndexs[baseName] ) == 2 ):
			
			coordsA = mc.xform( '{0}.vtx[{1}]'.format( baseName , dicoIndexs[baseName][0] ) , q = True , t = True , ws = True ) 
			coordsB = mc.xform( '{0}.vtx[{1}]'.format( baseName , dicoIndexs[baseName][1] ) , q = True , t = True , ws = True ) 
			
			tValue    = utilsMath.getBarycentre( [ coordsA , coordsB ] )
			rValue = utilsMayaApi.API_convert2CoordsToEulerOrient( coordsA , coordsB )	
						
			trsValue = tValue + rValue + [ 1 , 1 , 1 ]  						
	
				
		#____________________________________ many vtx		
		else:
	
			if( isAimConfiguration( baseName , dicoIndexs[baseName] ) == 1 ):
				trsValue = aimPosRot( baseName , dicoIndexs[baseName] )
			else:
				trsValue = utilsMayaApi.getTRSreelBB( baseName , dicoIndexs[baseName] )				
	

		loc = utilsMaya.buildSimpleLoc( baseName , trsValue  )	
		compensateScaleWithLocalScale( loc )
		createdLocs.append( loc )
	

	return createdLocs 	
	
	
#====================================================================================================================================
#==================================================================================================================           other
#====================================================================================================================================


#_______________________________________________________________________________________________________________________ isAimConfiguration
def isAimConfiguration( baseName , indexs ):

	coef = 5
	
	allCoords = utilsMayaApi.API_getAllVertexCoords( baseName )
	
	coords    = []	
	for i in indexs:
		coords.append( allCoords[i] )
	
		
	distances = utilsMayaApi.API_getSortedDistancesIndexCoords( coords , 0 )

	
	if( distances[0] < coef * distances[1] ):
		return 0
	else:
		return 1
	
	


#_______________________________________________________________________________________________________________________ aimPosRot

def aimPosRot( baseName , indexs ):
	
	allCoords = utilsMayaApi.API_getAllVertexCoords( baseName )
	iMax      = utilsMayaApi.getfarestCoordsIndex( allCoords , indexs )
	indexs.remove( iMax )

	TRSvalue = utilsMayaApi.getTRSreelBB( baseName , indexs )
	
	rValue = utilsMayaApi.API_convert2CoordsToEulerOrient( allCoords[iMax] , TRSvalue[0:3] )	

	return TRSvalue[0:3] + rValue	+ TRSvalue[6:9]
		


#_______________________________________________________________________________________________________________________ growSelection
	
def growSelection( component ):
	  
	faces = mc.polyListComponentConversion( component ,  fv = True ,  tf = True )
	growcomponents = mc.polyListComponentConversion( faces ,  ff = True ,  tv = True )  
	
	return growcomponents


#_______________________________________________________________________________________________________________________ compensateScaleWithLocalScale	
def compensateScaleWithLocalScale( loc ):
	
	attrs = [ 'scale' , 'localScale' ]
	axes = ['X' , 'Y' , 'Z' ]

	value = 0.0
	for axe in axes:
		value = 1.0 / mc.getAttr( loc + '.' + attrs[0] + axe ) 
		mc.setAttr( ( loc + '.' + attrs[1] + axe ) , value )
		
	return 1
	
	
			
			