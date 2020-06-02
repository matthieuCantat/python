
'''
	name:  paralleleEdgeTool
	type:  MODELING
	tag:   edge
	date:  27/07/2016	
	input: x edge of an obj
	
	take the first edge as reference. 
	the make the others parallele at the first
'''


import maya.cmds as mc
import maya.OpenMaya as om
import math
from ..utils import utilsMaya

def paralleleEdgeTool():


	nameSpaceInMaya = 'toolBox.tools.paralleleEdgeTool.paralleleEdgeTool'
	
	global customTmpHotkeyVar	
	customTmpHotkeyVar = utilsMaya.customTmpHotkeyManager()
	customTmpHotkeyVar.addHotkey( 'saveEdgeCoords' , 'c' , 'ctrl' , 'paralleleEdgeToolVar = {0}.paralleleTool();paralleleEdgeToolVar.saveCoords()'.format(nameSpaceInMaya) )
	customTmpHotkeyVar.addHotkey( 'makeParalleleEdge'     , 'v' , 'ctrl' , 'paralleleEdgeToolVar.doIt()' )
	customTmpHotkeyVar.nameSpace = nameSpaceInMaya	
	customTmpHotkeyVar.doIt()

	'''
	
	try: print( paralleleEdgeToolVar )
	except: exec('paralleleEdgeToolVar = paralleleEdgeTool.paralleleTool()') in globals()
	
	paralleleEdgeToolVar.doIt()
	
	if( paralleleEdgeToolVar.refCoords == [ [0,0,0] , [0,0,0] ] ):
		mc.symbolButton( 'paralleleEdgeTool_button' , e = True ,  i = ( self.iconPath + 'paralleleEdgeTool.jpg' )   )
	else:
		mc.symbolButton( 'paralleleEdgeTool_button' , e = True ,  i = ( self.iconPath + 'paralleleEdgeTool1.jpg' )   )
		
	'''	

class paralleleTool():

	def __init__(self):		
		self.refCoords     = [ [0,0,0] , [0,0,0] ]
		self.refCoordsBase = [ [0,0,0] , [0,0,0] ]	

		
	def getParallelePointCoords( self , originCoords , directionVector , dist ):
		
		newCoords = [0,0,0]
		
		
		newCoords[0] = directionVector.x * dist + originCoords[0]
		newCoords[1] = directionVector.y * dist + originCoords[1]
		newCoords[2] = directionVector.z * dist + originCoords[2]	
		
		return newCoords		
		
		
		

	def getAlignCoords( self , lineCoords , oldCoords ):
	
		vectorRef       = om.MVector( ( lineCoords[1][0] - lineCoords[0][0] ) , ( lineCoords[1][1] - lineCoords[0][1] ) , ( lineCoords[1][2] - lineCoords[0][2] ) )
		vectorOldCoords = om.MVector( ( oldCoords[0]         - lineCoords[0][0] ) , ( oldCoords[1]         - lineCoords[0][1] ) , ( oldCoords[2]         - lineCoords[0][2] ) )
		angleA          = vectorRef.angle( vectorOldCoords )
			
		dist = math.cos( angleA ) * vectorOldCoords.length()
		
		vectorRef.normalize()
			
		newCoords = [  vectorRef.x * dist + lineCoords[0][0] , vectorRef.y * dist + lineCoords[0][1] , vectorRef.z * dist + lineCoords[0][2] ] 
		
		return newCoords
				
				

	def saveCoords(self):
		
		selection = mc.filterExpand( sm = 32 )
						
		if(  len(selection) == 1 ):
			
			verticesRef = utilsMaya.API_getVerticesOfEdge( selection[0] )	
			coordsA = mc.xform( verticesRef[0] , q = True , t = True , ws = True )
			coordsB = mc.xform( verticesRef[1] , q = True , t = True , ws = True )	
			self.refCoords = [ coordsA , coordsB ]
			print('record 1 edge ref')

			
		else:
			mc.error( 'you must select 1 edge de reference' )		
	    
    	
	def doIt( self ):
		
		selection = mc.filterExpand( sm = 32 )

			
		if( self.refCoords == self.refCoordsBase ) :
			mc.error( 'you must select save coords' )
                                                                                                                              
		else:
			
			vectorRef = om.MVector( self.refCoords[1][0] - self.refCoords[0][0] , self.refCoords[1][1] - self.refCoords[0][1] , self.refCoords[1][2] - self.refCoords[0][2] )
			
			for elem in selection:

				vertices  = utilsMaya.API_getVerticesOfEdge( elem )					
				coordsA = mc.xform( vertices[0] , q = True , t = True , ws = True )
				coordsB = mc.xform( vertices[1] , q = True , t = True , ws = True )

				paralleleCoords = self.getParallelePointCoords( coordsA , vectorRef , 1 )	
				newCoords = self.getAlignCoords( [ coordsA , paralleleCoords ] , coordsB )

				mc.xform( vertices[1]  , t = newCoords , ws = True )
				print('doIt')

	
				
				