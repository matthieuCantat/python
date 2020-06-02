



'''
	name:  autoManipUI
	type:  RIGGING
	tag:   manip
	date:  21/04/2016	
	input: none

	lauch the UI for placing manipulator
'''

import sys	
import maya.cmds as mc	
import maya.mel as mel
from ..utils import utilsPython


def autoManip(): 
	try: print( autoManipUIVar )
	except: exec('autoManipUIVar = autoManipUI()') in globals()

	exec('autoManipUIVar.mainUi()') in globals() 

class autoManipUI():

	
	#______________________________________________________________________________________________________________________________________________________________________   INIT
	
	def __init__(self):	
		

		self.globalPath           = 'C:/Users/Matthieu/Desktop/Travail/code/maya/script/python/toolBox/tools/'
		
		self.globalPath           =  utilsPython.getActualPath()	
		pathSplitTmp             = self.globalPath.split('/' )
		self.toolBoxPath       = '/'.join( pathSplitTmp[0: len(pathSplitTmp) - 2 ] ) + '/'				
		
		self.variableNameInGlobal = 'toolBox.tools.autoManip.autoManip.autoManipUIVar'
		
		self.indexColor           = 13
		
		self.manipShapeNames      = ['Cube', 'Sphere', 'Cylindre', 'Loc', 'ArrowA', 'ArrowB', 'ArrowC', 'ArrowD', 'ArrowE', 'Smiley', 'Oeil', 'Plane', 'Circle' , 'None']
		self.shapeChoice          = [ 1 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ] 
		self.shapeName            = 'Cube' 
		                          
		self.pivotButtonValue     = 0  
		self.shapeAxe             = 1 
		                          
		self.manipOptions         = [ 'position' , 'orient' , 'scale' , 'joint' , 'visibility' , 'constraint' , 'root' , 'animSet' ]		
		self.optionChoice         = [ 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1  ]  
		                          
		self.optionVis            = 0 
			


		# load manip class
		sys.path.append( self.globalPath + 'autoManip/' )
		exec('import manipsClass' ) in globals()  
		exec('reload(manipsClass)') in globals() 
		
   




		

	#=========================================================================================================================================================================================
	#==============================================================                 MANIP CREATOR                  ===========================================================================
	#=========================================================================================================================================================================================



	#=========================================================================================================================================================================================
	#======================================================================================================================================================================   BUILD UI   =====
	#=========================================================================================================================================================================================
	

	#______________________________________________________________________________________________________________________________________________________________________   manip Creator
	
	def UI_manipCreator( self, UIparent ):
		
		
		panels =  [ 'AM_manipCreator' , 'AM_colorPanel' , 'AM_shapePanel' , 'AM_createManipButton' ,  'AM_pivotRotateManip' ,  'AM_optionVisButton' ,  'AM_option'   ]	
		
		mc.frameLayout( panels[0]  , li = 100 ,  cll = 0 ,  w = 275 ,  bgc = [ 0.45 , 0.35 , 0.35 ] ,   label = 'MANIP' , p = UIparent )
		
		# declaration du form
		
		form = mc.formLayout( numberOfDivisions = 100 ,  bgc = [ 0.27 , 0.27 , 0.27 ]  ) 
				
		# declaration des elements
		
		self.UI_manipCreator_colorPanel(  panels[1]  ,     form  )
		self.UI_manipCreator_shapeChoice( panels[2]  ,     form  )	
		toto = mc.button(                 panels[3]  , p = form     , bgc = [ 0.5 , 0.7 , 0.5 ] ,  h = 30  ,  w = 125   ,  c = ( self.variableNameInGlobal + '.manipCreator_createManipButton()' )  , l = '  CREATE MANIP  '  )				
		self.UI_manipCreator_editPivAndShape(  panels[4]  ,     form  )  	
		mc.button(                         panels[5]  , p = form     , w = 10  ,  c = ( self.variableNameInGlobal + '.manipCreator_hideOptionPanel()' )   , l = '>'  ) 	
		self.UI_manipCreator_optionPanel(            panels[6]  ,     form  )		
		
		
		# ajout des elements dans le 
		
		mc.formLayout( form , e = True ,  af =[  ( panels[1] , 'top'    , 10 ) , ( panels[1] , 'left'   , 10  )   ]   , ac = [                                                                                            ] )  # AM_colorPanel 	                                      
		mc.formLayout( form , e = True ,  af =[  ( panels[2] , 'left'   , 10 )                                    ]   , ac = [  ( panels[2] , 'top'  ,  10  ,  panels[1] )                                                ] )  # AM_shapePanel 	                   			                          
		mc.formLayout( form , e = True ,  af =[  ( panels[3] , 'left'   , 10 ) , ( panels[3] , 'bottom' , 10  )   ]   , ac = [  ( panels[3] , 'top'  ,  10  ,  panels[2] )                                                ] )  # AM_createManipButton 	                                          
		mc.formLayout( form , e = True ,  af =[  ( panels[4] , 'bottom' , 10 )                                    ]   , ac = [  ( panels[4] , 'top'  ,  10  ,  panels[2] ) , ( panels[4] , 'left' ,  10  ,  panels[3] )   ] )  # AM_pivotRotateManip 	
		mc.formLayout( form , e = True ,  af =[  ( panels[5] , 'top'    , 10 ) , ( panels[5] , 'bottom' , 10  )   ]   , ac = [  ( panels[5] , 'left' ,  10  ,  panels[2] )                                                ] )  # AM_optionVisButton	
		mc.formLayout( form , e = True ,  af =[  ( panels[6] , 'top'    , 10 ) , ( panels[6] , 'bottom' , 10  )   ]   , ac = [  ( panels[6] , 'left' ,  0   ,  panels[5] )                                                ] )  # AM_option	
		   		                  
	
		
		
		
	#______________________________________________________________________________________________________________________________________________________________________   color Panel
	
	def UI_manipCreator_colorPanel( self, panelColorName , parent ):
	
		# w = 240	
		rows      = 2
		columns   = 16 
		cellHeigh = 19 
		cellWidth = 15
		
		mc.palettePort( panelColorName ,      dim = [ columns , rows  ]   ,    width = (columns * cellWidth)    ,    height = (rows * cellHeigh)    , transparent = 0 , topDown = True , colorEditable = False , setCurCell = 0  , p = parent  )	
		mc.palettePort( panelColorName , e = True , cc = ( self.variableNameInGlobal + '.manipCreator_changeShapeColorButton()' ) )	
		
		for i  in range( 1 , 32 ):	
			componentColors = mc.colorIndex( i , q = True )	
			mc.palettePort(   panelColorName ,  e = True ,  rgbValue = [ i , componentColors[0] , componentColors[1] , componentColors[2] ]   )
			
		mc.palettePort(       panelColorName ,  e = True ,  rgbValue = [ 0 , 0.6 , 0.6 , 0.6 ]   )
		
		
	
	
	#______________________________________________________________________________________________________________________________________________________________________   shape Choice
	
	def UI_manipCreator_shapeChoice(  self , name , parent ):
	
		# w = 238
				
		icoShapeDossier = 'tools/autoManip/icon/shape/'
		icoShapePath    = self.toolBoxPath + icoShapeDossier
		sizeIcone       = 34 		
		nbrShape        = len( self.manipShapeNames )
		
		mc.rowColumnLayout(   name   , numberOfRows = 2  , rowHeight = ( [ 1 , sizeIcone ] , [ 2 , sizeIcone ] ) , p = parent    )
		mc.iconTextRadioCollection( name + 'rc' ) 
		
		for i in range( 0 , nbrShape ): 
			
			activeName = 'Off'
			if( self.shapeChoice[i] == 1 ):
				activeName = 'On'	
				
			mc.iconTextRadioButton(  ('AM_' + self.manipShapeNames[i] + '_ITRB' ) , w = sizeIcone , h = sizeIcone  , cl = (name + 'rc')   )         	
			mc.iconTextRadioButton(  ('AM_' + self.manipShapeNames[i] + '_ITRB' ) , e = True      , onc = ( self.variableNameInGlobal + '.manipCreator_changeShapeFormButton(%r)'%(i) )      ,      i = ( icoShapePath + 'manip' + self.manipShapeNames[i] + activeName + '.jpg')  )
							   
	

	
	#______________________________________________________________________________________________________________________________________________________________________   edit Piv And Shape
	
	
	def UI_manipCreator_editPivAndShape( self , name , parent ):
	
		
		iconeAxeDossier   = 'tools/autoManip/icon/shapeRot/'
		iconePivotDossier = 'tools/autoManip/icon/pivot/'
			
		mc.rowColumnLayout( name , nc = 3 , columnWidth = [ ( 1 , 50 ) , ( 2 , 5 ) , ( 3 , 50 ) ]  , p = parent )   
			
		mc.shelfButton( 'pivotButton'       , w = 50 , h = 50 , i = ( self.toolBoxPath + iconePivotDossier + 'pivot0.jpg'    )  , c = ( 'print("tata");' + self.variableNameInGlobal + '.manipCreator_changePivotButton();print("toto")' )  )      
		mc.text( l = ' ' ) 	
		mc.shelfButton( 'orientShapeButton' , w = 50 , h = 50 , i = ( self.toolBoxPath + iconeAxeDossier   + 'manipAxe1.jpg' )  , c = ( self.variableNameInGlobal + '.manipCreator_changeShapeAxeButton()' )  )     			
			
	
	
	
	#______________________________________________________________________________________________________________________________________________________________________   option panel
	
	def UI_manipCreator_optionPanel(  self , name , parent ):


		icoOptionDossier = 'tools/autoManip/icon/option/'
		icoOptionPath = self.toolBoxPath + icoOptionDossier   
		
		manipOptionsAnnotation = [ 'auto pivot' , 'auto orient' , 'adjust shape to obj' , 'Make Jo' , 'Connect vis' , 'constra' , 'Parent to root' ,  'add to animSet'  ]	
		nbrOptions = len( self.manipOptions ) 
		sizeIcone = 34 
		
		mc.columnLayout( name , columnAttach = ['both' , 0 ] , rowSpacing = 0 , columnWidth = 80 , p = parent , vis = 0  ) 
		mc.text( bgc = [ 0.2 , 0.2 , 0.2 ] , l = 'OPTION:' )
		
		mc.gridLayout( numberOfColumns = 2 , cellWidthHeight = [ 40 , 40 ] )  
	    	
	
		for i in range( 0 , nbrOptions ):
	
			activeName = 'Off'
			if( self.optionChoice[i] == 1 ):
				activeName = 'On'
				
			mc.shelfButton( ('AM_' + self.manipOptions[i] + '_ITRB' ) , w = sizeIcone , h = sizeIcone , ann = manipOptionsAnnotation[i]   ) 
			mc.shelfButton( ('AM_' + self.manipOptions[i] + '_ITRB' ) , e = True , c = ( self.variableNameInGlobal + '.manipCreator_changeOptionButton(%r)'%(i) ) ,  i = ( icoOptionPath + 'optionAM_' + self.manipOptions[i] + activeName + '.jpg')  ) 
			


			
			
			
	#=========================================================================================================================================================================================
	#======================================================================================================================================================================   COMMANDS   =====
	#=========================================================================================================================================================================================

	
	
	
	#______________________________________________________________________________________________________________________________________________________________________   change Shape Color Button

	
	def manipCreator_changeShapeColorButton( self ):

		#_UI			
		self.indexColor = mc.palettePort( 'AM_colorPanel' , query=True , scc = True ) 
		
		#_SCENE

		selection = mc.ls( sl = True )
		
		for elem in selection:

				try:
					manip = manipsClass.manip( elem )
					manip.setShapeColor( self.indexColor )					
				except:
					pass
								
		
		mc.select( selection )		

	
		
		
	#______________________________________________________________________________________________________________________________________________________________________   change Shape Form Button		
		
	def manipCreator_changeShapeFormButton( self , index ):

		
		self.shapeChoice  =  [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ]  	
		activeNames     =  [ 'Off' , 'On' ]
		icoShapeDossier =  'tools/autoManip/icon/shape/' 	
		icoShapePath    =  self.toolBoxPath + icoShapeDossier
		nbrShapes       =  len( self.manipShapeNames )	
		
		self.shapeChoice[ index ] = 1
		
		self.shapeName = self.manipShapeNames[ index ]

		#_UI			
		for i in range( 0 , nbrShapes ):
			mc.iconTextRadioButton(  ('AM_' + self.manipShapeNames[i] + '_ITRB' ) , e = True , i = ( icoShapePath + 'manip' + self.manipShapeNames[i] + activeNames[self.shapeChoice[i]] + '.jpg') )		
	
		#_SCENE

		selection = mc.ls( sl = True )
		
		for elem in selection:				
			try:
				manip = manipsClass.manip( elem )
				manip.setShapeForm( self.shapeName )					
			except:
				pass				
	
				
		mc.select( selection )


		
	#______________________________________________________________________________________________________________________________________________________________________   change Pivot Button	
	
	
	def manipCreator_changePivotButton( self ):

		iconPivotDossier = '/autoManip/icon/pivot/'
		iconPivotPath    = self.toolBoxPath + iconPivotDossier
		
		
		self.pivotButtonValue += 1
		
		if( self.pivotButtonValue > 6 ):
			self.pivotButtonValue = 0

		#_UI				
		mc.shelfButton( 'pivotButton' , e = True , i = ( iconPivotPath + 'pivot' + str( self.pivotButtonValue )  + '.jpg' ) )
		
		#_SCENE

		selection = mc.ls( sl = True )
			
		for elem in selection:				
			try:
				manip = manipsClass.manip( elem )
				manip.rBB_setPivot( self.pivotButtonValue )					
			except:
				pass					
							
		mc.select( selection )

		
	#______________________________________________________________________________________________________________________________________________________________________   change Shape Axe Button		
		
	def manipCreator_changeShapeAxeButton(self):
	

		iconAxeDossier   = '/autoManip/icon/shapeRot/'
		iconAxePath      = self.toolBoxPath + iconAxeDossier	
		
		self.shapeAxe += 1
		
		if( self.shapeAxe > 3 ):
			self.shapeAxe = 1
		
		#_UI	
		mc.shelfButton( 'orientShapeButton' , e = True , i = ( iconAxePath + 'manipAxe' + str( self.shapeAxe )  + '.jpg' )  )    
		
		#_SCENE
		manip = manipsClass.manip()	

		selection = mc.ls( sl = True )
		
		
		for elem in selection:				
			try:
				manip = manipsClass.manip( elem )
				manip.setShapeAxe( self.shapeAxe )					
			except:
				pass		

		mc.select( selection )	
		
	#______________________________________________________________________________________________________________________________________________________________________   create Manip Button	
	
	def manipCreator_createManipButton( self ):

		selection = mc.ls( sl = True )
		manip = manipsClass.manip()		
		manip.toolBox_createManips( self , selection )		
			

		
	#______________________________________________________________________________________________________________________________________________________________________   hide Option Panel	
	
	def manipCreator_hideOptionPanel( self ):
	

		if( self.optionVis == 0):
			self.optionVis = 1
		else:
			self.optionVis = 0		
		
	 	
		mc.columnLayout( 'AM_option'       , e = True ,  vis =  self.optionVis               )  
		mc.frameLayout(  'AM_manipCreator' , e = True ,  w   = ( 275 + 80 * self.optionVis ) ) 		
		mc.window(       'AutoManipWindow' , e = True ,  w   = ( 295 + 80 * self.optionVis ) )
		
		
		
	#______________________________________________________________________________________________________________________________________________________________________   change Option Button	
	
	def manipCreator_changeOptionButton( self , index ):
	

		activeNames     =  [ 'Off' , 'On' ]
		icoOptionDossier =  '/autoManip/icon/option/' 	
		icoOptionPath    =  self.toolBoxPath + icoOptionDossier
		nbrOptions       =  len( self.manipOptions )	
		
		if( self.optionChoice[ index ] == 1 ):
			self.optionChoice[ index ] = 0
		else:
			self.optionChoice[ index ] = 1
			
	
		for i in range( 0 , nbrOptions ):
			mc.shelfButton(  ('AM_' + self.manipOptions[i] + '_ITRB' ) , e = True , i = ( icoOptionPath + 'optionAM_' + self.manipOptions[i] + activeNames[ self.optionChoice[i] ] + '.jpg') )		
	






		
	
	#=========================================================================================================================================================================================
	#==============================================================                    MAIN UI                      ===========================================================================
	#=========================================================================================================================================================================================		
		
	
	#______________________________________________________________________________________________________________________________________________________________________   toolBox Ui
	
	def mainUi(self):
	
		win ='AutoManipWindow'
		
		
		if( mc.windowPref( win , ex = True ) ):
			mc.windowPref( win , e = True , w = 295 , h = 200 )
		
		if( mc.window( win , ex = True ) ):
			mc.deleteUI( win , wnd = True )
		
		 
		 
		
		mc.window( win , w = 295 , h = 200 , s = True ) 
		
		mainColumName = 'mainColumn'	
		mc.columnLayout( mainColumName , columnAttach = [ 'both' , 10 ] , rowSpacing = 0 , columnWidth = 275 , bgc = [ 0.27 , 0.27 , 0.27 ]  )
		
		mc.text( l = '' , h = 1  , p = mainColumName)
		self.UI_manipCreator( mainColumName )
		mc.text( l = '' , h = 10 , p = mainColumName)
			
		
				
		mc.showWindow( win )
	
	







