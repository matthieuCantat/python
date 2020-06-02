
import sys
import os
import maya.cmds as mc	
import maya.mel as mel
import math

#new
print('import begin')
import toolBox
import toolBox.utils.utils as utils
reload(utils)
import toolBox.utils.utilsPython as utilsPython
print('import end')




class toolBoxUI():


	def __init__(self):	
		
		#___name___
		
		self.win             = 'toolBoxWindow'
		self.dockWin         = 'toolBoxWindowDock'			
		self.winTitle        = 'TOOL BOX'		
		self.mainColumName   = 'mainColumn'	
		self.toolGridName    = 'toolGrid'	
		self.scrollName      = 'scollToolGrid'
		self.searchFieldName = 'searchToolField'
		self.toolStatsfileBaseName = 'toolsStatistics'
		self.toolPrefFileBaseName  = 'toolBoxPref'	
		
		#___display___	
		
		self.categories = [ 'ALL' , 'MODELING' , 'RIGGING' , 'AUTRE' ]		
		self.categorieIndex = 0
		
		self.toolSort =  [ 'tag' , 'alpha' , 'date' , 'useDate' , 'useNbr' ]  
		self.toolSortIndex = 0		
				
		self.layoutModes = [ 'tableau' , 'list' ]		
		self.layoutModesIndex = 0

		self.dockingMode = [ 'none' , 'left' , 'right' , 'top' , 'bottom' ]
		self.dockingModeIndex = 0
		self.dockingModeIndexLast = 0

		self.helpModeIndex = 0
		
		#___position main___
		
		self.positionWin       = [ 300 , 300 ]
		self.positionWinDefaut = [ 300 , 300 ]	

		#___size main___
		
		self.whMainWin     = [ 296 , 316 ]		
		self.whMainWinMin  = [ 136 , 144 ]			
		self.whMainWinMax  = [ 999999 , 705 ]	
		
		self.whdockingTableauDefaut = [ [ 296 , 316 ] , [ 136 , 705 ] , [ 136 , 705 ] ,  [ 1296 , 156.0 ] , [ 1296 , 156.0 ] ]
		self.whdockingListDefaut    = [ [ 236 , 316 ] , [ 400 , 705 ] , [ 236 , 705 ] ,  [ 1296 , 156.0 ] , [ 1296 , 156.0 ] ]

		self.whMainWinMinTableau  = [ 136 , 144 ]			
		self.whMainWinMaxTableau  = [ 999999 , 705 ]	
		
		self.whMainWinMinList  = [ 236 , 144 ]			
		self.whMainWinMaxList  = [ 999999 , 705 ]	
		
		#___size case___
		
		self.nbrWHCases = [ 0 , 0 ]
		self.whCase     = [ 0 , 0 ]

		self.whCaseTableauDefault = [ 40 , 40 ]
		self.whCaseListDefault    = [ 180 , 40 ]

		#___size autre___
		
		self.whSideSpaceMainWin = [ 20 , 20 ]
		self.hSearchBar         = 20
		self.scrollBarThickness = 16		
		
		#___path___	
		
		arrayPath             = __file__.split('\\')
		self.selfPath         = '/'.join(arrayPath[0:-1]) + '/'	
		self.toolPathRelative = 'tools/'
		self.toolStatsPath    = self.selfPath 
		self.toolPrefPath     = self.selfPath
 		
		#___tool___	
		
		self.newToolsList   = [ elem    for elem in os.listdir( self.selfPath + self.toolPathRelative )    if not( '.' in elem ) ]	
		self.allToolsInfo   = {}
		self.toolsOnScreen  = []
		self.toolStatsInfo  = {}
		
		#___autre___
		
		self.firstLaunch = 1		
		self.searchFilter    = ''	
		
		self.getAllToolsInfo()
		self.applyPref()
		
	#______________________________________________________________________________________________________________________________________________________________________   toolBoxUi
	
	
	def toolBoxUi( self ):


		
		# gather info for layout
		
		self.getToolsOnScreen()
		self.resizeAndAjust()
		self.savePref()	
		
		# delete

		if( self.firstLaunch == 1):
			
			uiToDelete = [ self.win , self.win + 'Bis'	,   self.dockWin , self.dockWin + 'Bis' ]
			
			for uiName in uiToDelete:
				try:
					mc.deleteUI(uiName)
				except:
					pass			
		else:	
			mc.evalDeferred('import maya.cmds as mc') 			
			mc.evalDeferred('if(mc.window( "{0}" , ex = True )): mc.deleteUI( "{0}" )'.format(self.win)) 
			mc.evalDeferred('if(mc.dockControl( "{0}" , ex = True )): mc.deleteUI( "{0}" )'.format(self.dockWin))				
			if( self.win[-3:-1] == 'Bi' ):
				self.win     = self.win.split('Bis')[0]
				self.dockWin = self.dockWin.split('Bis')[0]				
			else:	
				self.win     = self.win + 'Bis'	
				self.dockWin = self.dockWin + 'Bis'						
		

			
		# build
		
		if( self.firstLaunch == 0):	
			self.winTitle = self.categories[self.categorieIndex] 
				

				
		mc.window( self.win  , wh = self.whMainWin , s = True , t = self.winTitle , topLeftCorner = self.positionWin )  
		mc.windowPref( self.win  , e = True , wh = self.whMainWin , topLeftCorner = self.positionWin )	

		mc.formLayout( self.mainColumName , numberOfDivisions = 100 ,  bgc = [ 0.27 , 0.27 , 0.27 ]   )  #0.27
		
		self.canvasPopupMenu()
	
		mc.textField( self.searchFieldName , bgc = [ 0.35 , 0.35 , 0.35 ] , h = self.hSearchBar , tx = self.searchFilter , cc = 'import maya.cmds as mc; toolBoxWindow.searchFilter = mc.textField( toolBoxWindow.searchFieldName , q = True , tx = True );toolBoxWindow.toolBoxUi()' )
		
		mc.scrollLayout( self.scrollName , horizontalScrollBarThickness = self.scrollBarThickness , verticalScrollBarThickness = self.scrollBarThickness , p = self.mainColumName  )
		self.scrollToolsPopupMenu()		
		self.gridListTools()
	
		mc.formLayout( self.mainColumName , e = True ,  af =[  (  self.searchFieldName , 'top'    , self.whSideSpaceMainWin[1] ) , ( self.searchFieldName , 'right'   , self.whSideSpaceMainWin[0] ) , ( self.searchFieldName , 'left'   , self.whSideSpaceMainWin[0]  )   ]   , ac = [  ] ) 		
		mc.formLayout( self.mainColumName , e = True ,  af =[  (  self.scrollName      , 'bottom' , self.whSideSpaceMainWin[1] ) , ( self.scrollName      , 'right'   , self.whSideSpaceMainWin[0] ) , ( self.scrollName      , 'left'   , self.whSideSpaceMainWin[0]  )   ]   , ac = [ (  self.scrollName , 'top'    , 0 , self.searchFieldName  ) ] )

	
		if not ( self.dockingMode[self.dockingModeIndex] == 'none'):
			mc.dockControl( self.dockWin , l = self.winTitle , content = self.win , area = self.dockingMode[self.dockingModeIndex] )
		else:
			mc.showWindow( self.win )
				

		self.firstLaunch = 0	
		
	#______________________________________________________________________________________________________________________________________________________________________   gridListTools
		
	def gridListTools( self ):

		
		mc.gridLayout( self.toolGridName ,  numberOfColumns = self.nbrWHCases[0] , cellWidthHeight = self.whCase , bgc = [ 0.27 , 0.27 , 0.27 ] , p = self.scrollName  )
		
		if( self.layoutModes[self.layoutModesIndex] == 'tableau'):
			for tool in self.toolsOnScreen:	
				mc.symbolButton(  ( tool + '_button' )   , c = self.allToolsInfo[tool]['cmds']  , i = self.allToolsInfo[tool]['icons'] , p = self.toolGridName  )
			
		else:
			for tool in self.toolsOnScreen:

				if( self.helpModeIndex == 1):
					toolNameListCmds = 'mc.button( l = "{0}" , c = \'toolBoxWindow.showHelpWindow("{0}")\' , bgc = [ 0.3 , 0.4 , 0.3] )'.format(tool) 
				else:
					toolNameListCmds = 'mc.text( l = "{0}" )'.format(tool)  
					
				toolLine = [ 'mc.symbolButton( ( "{0}_button" ) , c = "{1}" , i = ( "{2}" ) , w = {3[0]} , h = {3[1]}   )'.format( tool , self.allToolsInfo[tool]['cmds'] , self.allToolsInfo[tool]['icons'] , self.whCaseTableauDefault  ) , toolNameListCmds ]				
				utils.buildUi_makeNiceBox( ( tool + '_niceBox' ) , self.toolGridName, layoutWidth =  self.whCaseListDefault[0]  , casesHeight = self.whCaseListDefault[1] , caseCommands = toolLine  , caseWidthPercent = [ 21 , 76 ]  )	 #[ 21 , 76 ] 
				mc.setParent(self.toolGridName)
	
				
				
	
	#______________________________________________________________________________________________________________________________________________________________________   canvasPopupMenu
		
	def canvasPopupMenu(self):
		
		mc.popupMenu(  mm = True )

		mc.menuItem( l = 'dockingLeft'     , rp  = 'W' , c = 'toolBoxWindow.nextDockingMode("left")   ;toolBoxWindow.toolBoxUi();'  )
		mc.menuItem( l = 'dockingRight'    , rp  = 'E' , c = 'toolBoxWindow.nextDockingMode("right")  ;toolBoxWindow.toolBoxUi();'  )
		mc.menuItem( l = 'dockingTop'      , rp  = 'N' , c = 'toolBoxWindow.nextDockingMode("top")    ;toolBoxWindow.toolBoxUi();'  )
		mc.menuItem( l = 'dockingBottom'   , rp  = 'S' , c = 'toolBoxWindow.nextDockingMode("bottom") ;toolBoxWindow.toolBoxUi();'  )		
				
	#______________________________________________________________________________________________________________________________________________________________________   nextDockingMode
	
	def nextDockingMode( self , orient ):
			
		lastDockingIndex = self.dockingModeIndex 
		self.dockingModeIndex = self.dockingMode.index(orient)

		if( 0 < lastDockingIndex < 3 ) and ( 0 < self.dockingModeIndex < 3 ):
			self.dockingModeIndex = 0
	
		if( 2 < lastDockingIndex < 5 ) and ( 2 < self.dockingModeIndex < 5 ):
			self.dockingModeIndex = 0
			
	#______________________________________________________________________________________________________________________________________________________________________   nextToolSort			
			
	def nextToolSort( self , mode ):
			
		self.toolSortIndex = self.toolSort.index(mode)

	#______________________________________________________________________________________________________________________________________________________________________   scrollToolsPopupMenu		
		
	def scrollToolsPopupMenu( self ):
		mc.popupMenu( mm = True )
		
		mc.menuItem( l = 'tableau/list'    , rp  = 'N' , c = "toolBoxWindow.nextLayout(1)    ;toolBoxWindow.toolBoxUi();" ) 
		mc.menuItem( l = 'next Categorie'  , rp  = 'E' , c = "toolBoxWindow.nextType(1)      ;toolBoxWindow.toolBoxUi();" )
		mc.menuItem( l = 'resize'          , rp  = 'S' , c = "toolBoxWindow.toolBoxUi();"                                 )
		mc.menuItem( l = 'prev Categorie'  , rp  = 'W' , c = "toolBoxWindow.nextType(-1)     ;toolBoxWindow.toolBoxUi();" )
		mc.menuItem( l = 'help mode'       , rp  = 'NW', c = "toolBoxWindow.nextHelp(1)      ;toolBoxWindow.toolBoxUi();" )

		
		mc.menuItem( l = 'classement'    , rp  = 'NE' , c = '' , sm = True  )	
		
		mc.menuItem( l = 'alphabetique'      , rp  = 'N' , c = 'toolBoxWindow.nextToolSort("alpha")   ;toolBoxWindow.toolBoxUi();' ) 
		mc.menuItem( l = 'recement utilise'  , rp  = 'E' , c = 'toolBoxWindow.nextToolSort("useDate") ;toolBoxWindow.toolBoxUi();' ) 
		mc.menuItem( l = 'tag'               , rp  = 'S' , c = 'toolBoxWindow.nextToolSort("tag")     ;toolBoxWindow.toolBoxUi();' ) 
		mc.menuItem( l = 'dateCreation'      , rp  = 'W' , c = 'toolBoxWindow.nextToolSort("date")    ;toolBoxWindow.toolBoxUi();' ) 
		mc.menuItem( l = 'populaire'         , rp  = 'NW', c = 'toolBoxWindow.nextToolSort("useNbr")  ;toolBoxWindow.toolBoxUi();' )
		
	#______________________________________________________________________________________________________________________________________________________________________   nextLayout			
	def nextLayout( self , incr ):
		self.layoutModesIndex += incr	
		self.layoutModesIndex = utils.specialClamp( self.layoutModesIndex , 0 , len( self.layoutModes) )
	#______________________________________________________________________________________________________________________________________________________________________   nextType	
	def nextType( self , incr ):
		self.categorieIndex += incr	
		self.categorieIndex = utils.specialClamp( self.categorieIndex , 0 , len( self.categories) )				
	#______________________________________________________________________________________________________________________________________________________________________   nextHelp
	def nextHelp( self , incr ):
		self.helpModeIndex += incr	
		self.helpModeIndex = utils.specialClamp( self.helpModeIndex , 0 , 2 )			
		
	#______________________________________________________________________________________________________________________________________________________________________   resizeAndAjust	
	
	def resizeAndAjust( self ):

		
		# get win position
		
		if( self.dockingModeIndex == 0):
			if( self.dockingModeIndexLast == self.dockingModeIndex ):
				if(mc.window( self.win  , ex = True )):
					self.positionWin[0] = mc.window( self.win  , q = True , topEdge = True )
					self.positionWin[1] = mc.window( self.win  , q = True , leftEdge = True )
			else:	
				self.positionWin = self.positionWinDefaut[:]

		
		# get size window
		
		if( self.firstLaunch == 0):
			if( self.dockingModeIndexLast == self.dockingModeIndex ):
			
				if( mc.window( self.win  , ex = True ) ):
					self.whMainWin[0] = mc.window( self.win , q = True , w = True  )
					self.whMainWin[1] = mc.window( self.win , q = True , h = True  )				
				
				if( mc.dockControl( self.dockWin , ex = True ) ):
					self.whMainWin[0] = mc.dockControl( self.dockWin , q = True , w = True  )
					self.whMainWin[1] = mc.dockControl( self.dockWin , q = True , h = True  )	
			
			else:
				if( self.layoutModes[self.layoutModesIndex] == 'tableau'):				
					self.whMainWin = self.whdockingTableauDefaut[self.dockingModeIndex][:]
				else:
					self.whMainWin = self.whdockingListDefaut[self.dockingModeIndex][:]
					
				self.dockingModeIndexLast = self.dockingModeIndex
			

	
		# get whCase and min max
		
		if( self.layoutModes[self.layoutModesIndex] == 'tableau'):
			self.whCase = self.whCaseTableauDefault
			self.whMainWinMax = self.whMainWinMaxTableau[:]
			self.whMainWinMin = self.whMainWinMinTableau[:] 
		else:
			self.whCase = self.whCaseListDefault 		
			self.whMainWinMax = self.whMainWinMaxList[:]
			self.whMainWinMin = self.whMainWinMinList[:] 
							
		# clamp
	
		
		self.whMainWin[0] = min( self.whMainWinMax[0] , self.whMainWin[0] )
		self.whMainWin[1] = min( self.whMainWinMax[1] , self.whMainWin[1] )
		
		self.whMainWin[0] = max( self.whMainWinMin[0] , self.whMainWin[0] )
		self.whMainWin[1] = max( self.whMainWinMin[1] , self.whMainWin[1] )		
		

			
		# get Width nbr of case and adjust mainWin
		
		self.nbrWHCases[0] = math.ceil( ( self.whMainWin[0] - self.whSideSpaceMainWin[0] * 2 - self.scrollBarThickness ) / self.whCase[0] )
		self.nbrWHCases[0] = min( self.nbrWHCases[0] , len( self.toolsOnScreen) )
		
		self.whMainWin[0]  = self.nbrWHCases[0] * self.whCase[0] + self.whSideSpaceMainWin[0] * 2 + self.scrollBarThickness
		
		# get height nbr of case and adjust mainWin 
		
		self.nbrWHCases[1] = math.ceil( len( self.toolsOnScreen ) / self.nbrWHCases[0] )
		self.whMainWin[1]  = self.nbrWHCases[1] * self.whCase[1] + self.whSideSpaceMainWin[1] * 2 + self.hSearchBar  + self.scrollBarThickness

		
		# clamp
		self.whMainWin[0] = min( self.whMainWinMax[0] , self.whMainWin[0] )
		self.whMainWin[1] = min( self.whMainWinMax[1] , self.whMainWin[1] )
		
		self.whMainWin[0] = max( self.whMainWinMin[0] , self.whMainWin[0] )
		self.whMainWin[1] = max( self.whMainWinMin[1] , self.whMainWin[1] )
		
		
		

			
	
	#______________________________________________________________________________________________________________________________________________________________________   getToolsOnScreen	

		
	def getToolsOnScreen( self ):
		
	
		toolsFiltered = []
		
		filtre = self.categories[ self.categorieIndex ]
		search = self.searchFilter  
		
		for tool in self.allToolsInfo.keys():	
			
			toolType = self.allToolsInfo[tool]['type']
			
			if( filtre in toolType ) or ( 'ALL' in toolType ) or (filtre == 'ALL'):			
				if( search in tool.lower() ) or ( search == '' ):
					toolsFiltered.append(tool) 
	
		#sort allToolsInfoFiltered 
		
		toolsFilterSort = []
		
		#self.toolSort =  [ 'tag' , 'alpha' , 'date' , 'useDate' , 'useNbr' ]  
		
		if( self.toolSort[self.toolSortIndex] == 'tag' ):
			
			for type in self.categories:
				sameTypeTool = []
				sameTypeTags = []
				
				for tool in toolsFiltered:
					toolType = self.allToolsInfo[tool]['type']
					toolTag  = self.allToolsInfo[tool]['tag']
					
					if( type == toolType ):
						sameTypeTool.append(tool)
						sameTypeTags.append(toolTag)
						sameTypeTags = list(set(sameTypeTags))
						
        	
				for tag in sameTypeTags:
					for stool in sameTypeTool:
						toolTag  = self.allToolsInfo[stool]['tag']
						if( tag == toolTag):
							toolsFilterSort.append(stool)

		elif( self.toolSort[self.toolSortIndex] == 'date' ):
			
			rawDates = []
			for tool in toolsFiltered:
				rawDates.append( self.allToolsInfo[tool]['date'] )			
				
				
			rawDates = list(set(rawDates))	
			datesSorted = utils.sortDates(rawDates)

			datesSorted.reverse()
			for date in datesSorted:
				for tool in toolsFiltered:
					if( self.allToolsInfo[tool]['date'] == date ):
						toolsFilterSort.append(tool)
						
		elif( self.toolSort[self.toolSortIndex] == 'useDate' ):
					
			rawDates = []
			for tool in toolsFiltered:
				rawDates.append( self.allToolsInfo[tool]['useDate'] )			
				
			arrayDates = []	
			for stringDate in rawDates:
				arrayDate = utilsPython.convertArrayStringToArray(stringDate)
				if not( arrayDate in arrayDates ):
					arrayDates.append(arrayDate)
			
			arrayDates.sort()
			arrayDates.reverse()
			datesSorted = arrayDates

			
			for date in datesSorted:
				for tool in toolsFiltered:
					if( self.allToolsInfo[tool]['useDate'] ==str(date) ):
						toolsFilterSort.append(tool)
						
						
		elif( self.toolSort[self.toolSortIndex] == 'useNbr' ):
			
			rawUseNbr = []
			for tool in toolsFiltered:
				rawUseNbr.append( self.allToolsInfo[tool]['useNbr'] )
			
			
			useNbrSorted = list(set(rawUseNbr))
			useNbrSorted.sort()
			useNbrSorted.reverse()
			
				
			for nbr in useNbrSorted:
				for tool in toolsFiltered:
					if( self.allToolsInfo[tool]['useNbr'] == nbr ):
						toolsFilterSort.append(tool)					
			
		else:
			toolsFilterSort  = toolsFiltered
			toolsFilterSort.sort()
						
		self.toolsOnScreen = toolsFilterSort

		
	#______________________________________________________________________________________________________________________________________________________________________   getAllToolsInfo	
		
	def getAllToolsInfo( self ):
		
		# read toolStatsInfo XML
		utils.createXmlDicoVar( self.toolStatsfileBaseName , self.toolStatsPath ) 		
		self.toolStatsInfo = utils.readXmlDicoVar( self.toolStatsfileBaseName , self.toolStatsPath ) 
		
			
		# self.allToolsInfo[ tool ] = { path: , icons: , categorie: , tag: , description: , date: , useDate: , useNbr: } 		
		
		for tool in self.newToolsList:
			print('import {0}'.format(tool) )
			exec( 'import toolBox.tools.{0}.{0} as {0}'.format(tool)  ) in globals()
			exec( 'reload( toolBox.tools.{0}.{0})'.format(tool)  ) in globals() 
			moduleDocInfo = self.extractInfoFromToolModule( tool ) 		
			self.allToolsInfo[ tool ] = { 'path': '' , 'icons': '' , 'cmds' : '' , 'type': '' , 'tag': '' , 'description': '' , 'input':'' , 'date': '' , 'useDate': '' , 'useNbr': '' } 
		
			self.allToolsInfo[ tool ]['path']         = self.selfPath + self.toolPathRelative + tool + '/'  
			self.allToolsInfo[ tool ]['icons']        = self.allToolsInfo[ tool ]['path'] + tool + '.jpg' 			
			self.allToolsInfo[ tool ]['type']         = moduleDocInfo['type'] 	
			self.allToolsInfo[ tool ]['tag']          = moduleDocInfo['tag'] 	 	
			self.allToolsInfo[ tool ]['date']         = moduleDocInfo['date']

			self.allToolsInfo[ tool ]['input']        = moduleDocInfo['input'] 						
			#self.allToolsInfo[ tool ]['description']  = '\\n'.join(moduleDocInfo['descrition'].split('\n')) # remplace tous les '\n' par des '\\n'
			self.allToolsInfo[ tool ]['description']  = moduleDocInfo['descrition'].split('\n')
			
			#new
			try:
				self.allToolsInfo[ tool ]['useDate']          = self.toolStatsInfo[ tool ][0]	 	
				self.allToolsInfo[ tool ]['useNbr']           = self.toolStatsInfo[ tool ][1]
			except:
				self.allToolsInfo[ tool ]['useDate']          = '[0,0,0,0,0,0]' 	
				self.allToolsInfo[ tool ]['useNbr']           = '0'				
			#new
			
			
			importDossier = 'toolBox.tools.'+ tool +'.'+ tool 
			mainProc = tool + '()'	 			
			self.allToolsInfo[ tool ]['cmds']  =  ( 'toolBoxWindow.toolStats_writeOneUse(\'{0}\');'.format(tool) + 'reload(' + importDossier + ');' + importDossier + '.' + mainProc )	
			#reload('toolBox.tools.{0}.{0}'.format(tool) )

	#______________________________________________________________________________________________________________________________________________________________________   extractInfoFromToolModule	
			
	def extractInfoFromToolModule( self , moduleName ):
		
		'''
		extract from doc and convert the info into a dictionary
		name: -----
		type: -----
		date: -----
		input:-----
		-----------------
		-----------------
		----------------
		'''

		exec('lines = '+ moduleName +'.__doc__.split(\'\\n\')')
		dicoInfo = { 'name':'' , 'type':'' , 'tag':'' , 'date':'' , 'input':'' , 'descrition':'' }
	
		for i in range( 0 , len(lines) ):
			
		    matchKey = 0
		    for k in dicoInfo.keys() :
		        if( k in lines[i] )and(':' in lines[i]):
		            dicoInfo[k] = lines[i].split(':')[1].strip()
		            matchKey = 1
		
		    if( matchKey == 0 ) and ( len(lines[i]) > 2 ):
		        dicoInfo['descrition'] += lines[i].strip() + '\n'
	        
		return dicoInfo	
		
	#______________________________________________________________________________________________________________________________________________________________________   toolStats_writeOneUse	
			
	def toolStats_writeOneUse( self , toolName ):

		#self.toolStatsInfo  = {}				
						
		try:
			oldUseNbr = int( self.toolStatsInfo[toolName][1] )
		except:
			oldUseNbr = 0
		
		newUseNbr = oldUseNbr + 1
		
		newUseDate = utilsPython.getActualTimeArray()
		
		self.toolStatsInfo[toolName] = [ str(newUseDate) , str(newUseNbr) ]
		
		utils.writeXmlDicoVar( self.toolStatsfileBaseName , self.toolStatsPath , self.toolStatsInfo )

	#______________________________________________________________________________________________________________________________________________________________________   savePref
	
	
	def savePref( self ):

		# make a dict		
		dictPref = { 'position' : self.positionWin , 'size' : self.whMainWin , 'nbrCase' : self.nbrWHCases , 'sizeCase' : self.whCase  }
		dictPref.update( { 'type' : [self.categorieIndex] , 'sort' : [self.toolSortIndex] , 'layout' : [self.layoutModesIndex] , 'docking' : [self.dockingModeIndex] , 'dockingLast' : [self.dockingModeIndexLast] } )
		
		# write XML
		utils.createXmlDicoVar( self.toolPrefFileBaseName , self.toolPrefPath ) 		
		utils.writeXmlDicoVar( self.toolPrefFileBaseName , self.toolPrefPath , dictPref )
		'''
		# position / Size
		self.positionWin       = [ 300 , 300 ]		
		self.whMainWin         = [ 296 , 316 ]					
		self.nbrWHCases        = [ 0 , 0 ]
		self.whCase            = [ 0 , 0 ]
		
		# display		
		self.categorieIndex       = 0
		self.toolSortIndex        = 0		
		self.layoutModesIndex     = 0
		self.dockingModeIndex     = 0
		self.dockingModeIndexLast = 0	
		'''				

	
	def applyPref( self ):	
	
		# read toolStatsInfo XML
		utils.createXmlDicoVar( self.toolPrefFileBaseName , self.toolPrefPath ) 		
		dictPref = utils.readXmlDicoVar( self.toolPrefFileBaseName , self.toolPrefPath ) 	

		# position / Size
		self.positionWin       = [ float(dictPref['position'][0]	),float(dictPref['position'][1]	)]
		self.whMainWin         = [ float(dictPref['size'][0]		),float(dictPref['size'][1]		)]			
		self.nbrWHCases        = [ float(dictPref['nbrCase'][0]	),float(dictPref['nbrCase'][1]	)]
		self.whCase            = [ float(dictPref['sizeCase'][0]	),float(dictPref['sizeCase'][1]	)]
		                    
		# display		
		self.categorieIndex       = int( dictPref['type'][0]	   )
		self.toolSortIndex        = int( dictPref['sort'][0]		)
		self.layoutModesIndex     = int( dictPref['layout'][0]	   )
		self.dockingModeIndex     = int( dictPref['docking'][0]	   )
		self.dockingModeIndexLast = int( dictPref['dockingLast'][0])		

		
		
		
	def showHelpWindow( self , tool ):
		
		helpWin          = 'tb_helpWindow'
		formLayoutName   = 'tb_helpFormLayout'
		descritionColumn = 'tb_helpDescritionColumn'
		title            = 'tb_helpToolName'
		inputText        = 'tb_helpInputName'
		
		wInterSpace = 5
		wMiddleColumn = 300
		
		if( mc.window( helpWin , ex = True) ):
			mc.deleteUI(helpWin)

		
		mc.window( helpWin , wh = [ ( wMiddleColumn + wInterSpace * 2 )  , 120 ] , s = True , t = 'tool info' )		
		mc.formLayout( formLayoutName , numberOfDivisions = 100 ,  bgc = [ 0.27 , 0.27 , 0.27 ]   )  #0.27
		
		mc.text( title , l = tool , h = 30 , w = wMiddleColumn ,  bgc = [ 0.3 , 0.4 , 0.3] )
		mc.text( inputText ,  l = self.allToolsInfo[ tool ]['input'] , w = wMiddleColumn )

		mc.columnLayout( descritionColumn , w = wMiddleColumn    )
		
		mc.text( l = '-'*200  )		
		for line in self.allToolsInfo[ tool ]['description']:
			mc.text( l = line  )
		
			
		mc.formLayout( formLayoutName , e = True ,  af =[ ( title             , 'right'   , wInterSpace ) , ( title            , 'left'   , wInterSpace ) , (  title            , 'top'    , wInterSpace)  ]   , ac = [  ] ) 		
		mc.formLayout( formLayoutName , e = True ,  af =[ ( inputText         , 'right'   , wInterSpace ) , ( inputText        , 'left'   , wInterSpace )                                                  ]   , ac = [ (  inputText        , 'top'    , wInterSpace , title  ) ] )
		mc.formLayout( formLayoutName , e = True ,  af =[ ( descritionColumn  , 'right'   , wInterSpace ) , ( descritionColumn , 'left'   , wInterSpace ) , (  descritionColumn , 'bottom' , wInterSpace)  ]   , ac = [ (  descritionColumn , 'top'    , wInterSpace , inputText  ) ] )		
		
		mc.showWindow(helpWin)  			












		