
'''
	name:  setCustomAxisOrientation
	type:  MODELING
	tag:   utils
	date:  23/04/2016	
	input: select components

	Compute an orientation with the selected component
	Apply the orientation in the gizmo
	Also lauch a scipt job via UI for fixing this orient	
'''


#TO DO :
#modifier le script locator pour que le locator soit Y up



import maya.cmds as mc
import sys
import math
import maya.mel as mel
from ..script import buildLocator
from ..utils import utilsMaya   


def setCustomAxisOrientation():

	'''
	TENTATIVE DE PATH DE L ISOLATE SELECTION ----
	
	#fix: isolateSelection   part1	
	viewSelectedSets = mc.ls( '*ViewSelectedSet' , type = 'objectSet' )
	isolatedObjs     = []
	panelName = ''
	
	for set in viewSelectedSets:
		isolatedObjs  = mc.sets( set , q = True )
		
		if( len(isolatedObjs) == 0 ):
		    continue
		 
		panelName = set.split( 'ViewSelectedSet' )[0]
		break
	#fix: isolateSelection   part1	
	
	'''
	
	
	selection = mc.ls( sl = True )
	locators = buildLocator.buildLocator()

	if( len( locators ) > 1 ):
		mc.delete(locators)
		mc.error( 'marche pas avec plusieurs obj' )
		
	rot    = [ 0 , 0 , 0]
	rotRad = [ 0 , 0 , 0]

	
	rot[0] = mc.getAttr( locators[0] + '.rotateX' )	
	rot[1] = mc.getAttr( locators[0] + '.rotateY' )
	rot[2] = mc.getAttr( locators[0] + '.rotateZ' )
	
	rotRad[0] = math.radians( rot[0] )  
	rotRad[1] = math.radians( rot[1] )
	rotRad[2] = math.radians( rot[2] )
	
	mc.delete(locators)
	mc.select(selection)
	
	if( len(selection) == 0 ):
		return 0
	
	if( '.' in selection[0] ):
		i = selection[0].index('.')
		selection[0] = selection[0][0:i]



	#changement orientation	

		
	mel.eval('changeSelectMode -component;' )
	mc.hilite( selection[0]  , r = True )

	mc.manipScaleContext(  'Scale'  , e = True , mode = 6 , orientAxes = rotRad )	
	mc.manipRotateContext( 'Rotate' , e = True , mode = 3 , orientAxes = rotRad )	
	mc.manipMoveContext(   'Move'   , e = True  , mode = 6 , orientAxes = rotRad )

	#fix gizmo au centre du monde
	mc.setToolTo( 'RotateSuperContext')
	mc.setToolTo( 'scaleSuperContext' )
	mc.setToolTo( 'moveSuperContext'  )

	'''
	TENTATIVE DE PATH DE L ISOLATE SELECTION ----
		
	
	#fix: isolateSelection   part2	
	
	print( isolatedObjs )
	print( panelName )
	
	mc.refresh()

	if( len( isolatedObjs ) > 0 ):		
		mc.isolateSelect( panelName , s = False )
		for obj in isolatedObjs:
			mc.isolateSelect( panelName , ado = obj  )

	mc.isolateSelect( panelName , rdo = '|polySurface115.f[58]')
	mc.isolateSelect( panelName , u = True  )			
	mc.isolateSelect( panelName , s = True  )	
	
	'''
	
	#fix: scriptJob pour les changement de selection	

	exec( 'maintainCustomOrientationSJW = scriptJobWindow()' ) in globals()
	exec( 'maintainCustomOrientationSJW.UI()' ) in globals()	
	


	return 1	
	


	
	
class scriptJobWindow():

	def __init__(self):	
		
		self.mainWindow      = 'maintainCustomOrientationUI'		
		self.winLabel        = "MAINTAIN CUSTOM ORIENATION"
		self.scriptJobEvent  = 'SelectionChanged' 
		self.nameSpaceInMaya = 'python.script.setCustomAxisOrientation.maintainCustomOrientationSJW'
		
	def UI(self):
		
		mainColumName = 'mainColumnMCO'                      
		
		closeCmd = 'import maya.cmds as mc ;mc.deleteUI(\'maintainCustomOrientationUI\')'
	
		if( mc.window( self.mainWindow  , ex = True ) ):
			mc.deleteUI( self.mainWindow  , wnd = True )
			
		mc.window( self.mainWindow  , w = 180 , h = 30  , rtf = True , t = 'scriptJobWin' )
		mc.columnLayout( mainColumName , bgc = [ 0.27 , 0.27 , 0.27 ]  )
		utilsMaya.buildUi_makeNiceBox( 'title'     , mainColumName  , layoutWidth =  200  , casesHeight = 30 , caseCommands = [ 'mc.text("'+ self.winLabel + '" , bgc = [ 0.2 , 0.2 , 0.2 ] )'  ] , caseWidthPercent = [ 95 ]  )		
		utilsMaya.buildUi_makeNiceBox( 'closeCtrl' , mainColumName  , layoutWidth =  200  , casesHeight = 30 , caseCommands = [ 'mc.text(" delect Script job ----->")' , 'mc.button( "CLOSE" , c = "%s" , bgc = [ 0.7 , 0.3 , 0.3 ] )' %( closeCmd )  ] , caseWidthPercent = [ 60 , 30 ]  )	
		
		mc.showWindow( self.mainWindow  )
		
	
		mc.scriptJob(  p = self.mainWindow , event = [ self.scriptJobEvent  , '%s.scriptJobCmds()' %(self.nameSpaceInMaya)  ]  )
	
	
	def scriptJobCmds(self):
		
		mc.manipScaleContext(  'Scale'  , e = True , mode = 6  )	
		mc.manipRotateContext( 'Rotate' , e = True , mode = 3  )	
		mc.manipMoveContext(   'Move'   , e = True , mode = 6  )

		#fix: isolateSelection 
		viewSelectedSets = mc.ls( '*ViewSelectedSet' , type = 'objectSet' )
		isolatedObjs     = []
		panelName = ''
		
		for set in viewSelectedSets:
			isolatedObjs  = mc.sets( set , q = True )
			
			if( len(isolatedObjs) == 0 ):
			    continue
			 
			panelName = set.split( 'ViewSelectedSet' )[0]
			mc.isolateSelect( panelName , s = False  )				
			mc.isolateSelect( panelName , s = True  )				
			break	

	
'''
appel de proc:


import sys
sys.path.append( 'C:\Users\Matthieu\Desktop\Travail\WIP\script\jedit' )

exec('import setCustomAxisOrientation') in globals()
exec('reload (setCustomAxisOrientation)') in globals()

setCustomAxisOrientation.setCustomAxisOrientation()

'''
	
	
	
	