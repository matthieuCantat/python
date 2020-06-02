
'''
	name:  snapVerticesOnVirtualPlane
	type:  MODELING
	tag:   vertex
	date:  15/08/2016	
	input: 3 vtx ref and x vtx
	
	first time it take 3 vertices for calculate the plane
	the x vertex for snap
	with nothing selected it erease the plane and start to the first time
'''





import maya.cmds as mc
import maya.OpenMaya as om
import math
from ..utils import utilsBin
from ..utils import utilsMayaApi


global customTmpHotkeyVar

def snapVerticesOnVirtualPlane():


	nameSpaceInMaya = 'toolBox.tools.snapVerticesOnVirtualPlane.snapVerticesOnVirtualPlane'
	
	global customTmpHotkeyVar	
	customTmpHotkeyVar = utilsBin.customTmpHotkeyManager()
	customTmpHotkeyVar.addHotkey( 'savePlaneCoords' , 'c' , 'ctrl' , 'alignToolVar = {0}.alignTool();alignToolVar.saveCoords()'.format(nameSpaceInMaya) )
	customTmpHotkeyVar.addHotkey( 'snapToPlane'     , 'v' , 'ctrl' , 'alignToolVar.doIt()' )
	customTmpHotkeyVar.nameSpace = nameSpaceInMaya	
	customTmpHotkeyVar.doIt()
	




			
#___________________________________________________________________________________________ aligneTool



class alignTool():

	def __init__(self):		
		self.refCoords     = [ [0,0,0] , [0,0,0] ]
		self.refCoordsBase = [ [0,0,0] , [0,0,0] ]	



	def saveCoords( self ):    		
		selection = mc.filterExpand( sm = 31 )
		
		if(  len(selection) == 2 ):
			coordsA = mc.xform( selection[0] , q = True , t = True , ws = True )
			coordsB = mc.xform( selection[1] , q = True , t = True , ws = True )			
			self.refCoords = [ coordsA , coordsB ]
			print( 'save 2 ref coords : line mode' )

		elif(  len(selection) == 3 ):
			coordsA = mc.xform( selection[0] , q = True , t = True , ws = True )
			coordsB = mc.xform( selection[1] , q = True , t = True , ws = True )
			coordsC = mc.xform( selection[2] , q = True , t = True , ws = True )			
			self.refCoords = [ coordsA , coordsB , coordsC ]
			print( 'save 3 ref coords : plane mode' )			
		else:
			mc.error( 'you must select 2 or 3 objs' )

			
			
	def doIt( self ):
		
		selection = mc.filterExpand( sm = 31 )
		
		if( self.refCoords == self.refCoordsBase ):
			mc.error( 'you must save coords' )			
		else:
			
			for elem in selection:
				oldCoords = mc.xform( elem , q = True , t = True , ws = True )
				
				if( len( self.refCoords ) == 2 ):
					newCoords = utilsMayaApi.getAlignCoords( self.refCoords , oldCoords )
				else:
					
					newCoords = utilsMayaApi.snapCoordsOnPlane( self.refCoords , oldCoords )
					
				
				mc.xform( elem , t = newCoords , ws = True )
			



