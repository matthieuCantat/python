



'''
	name:  buildManip
	type:  RIGGING
	tag:   manip
	date:  21/04/2016	
	input: none

	lauch the UI for placing manipulator
'''

import sys	
import maya.cmds as mc	
import maya.mel as mel

from ..utils import utilsBin
from ..utils import utilsPython
from . import buildLocator
from ..utils.classe import buildRigClassManip



def buildManip(): 
	#try: print( buildManipUIVar )
	#except: exec('buildManipUIVar = buildManipUI()') in globals()
	exec('buildManipUIVar = buildManipUI()') in globals()
	exec('buildManipUIVar.mainUi()') in globals() 

class buildManipUI():

	
	#______________________________________________________________________________________________________________________________________________________________________   INIT
	
	def __init__(self):	
		


		self.globalPath           =  utilsPython.getActualPath()	
		pathSplitTmp = self.globalPath.split('/' )
		self.toolBoxPath  = '/'.join( pathSplitTmp[0: len(pathSplitTmp) - 2 ] ) + '/'		
		
		self.variableNameInGlobal = 'toolBox.tools.buildManip.buildManip.buildManipUIVar'

		self.CurveFormBank = utilsBin.curveFormBank()
		
		self.baseName           = None
		self.orient             = None
		self.pivotButtonValue   = 0  		
		self.shapeForm          = 'loc'
		self.shapeAxe           = 1 
		self.indexColor         = 13
		self.manipOptions       = [ 'position' , 'orient' , 'scale' , 'joint' , 'visibility' , 'constraint' , 'root' , 'animSet' ]		
		self.optionChoice       = [ 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1  ]  
		
		

	#=========================================================================================================================================================================================		   		                  
	#======================================================================================================================================================================  UI manip General
	#=========================================================================================================================================================================================	
	
	
	def UI_manipGeneral( self, UIparent ):
		
		
		panels =  [ 'bmUI_general' , 'bmUI_baseName' , 'bmUI_setOrient' ,  'bmUI_pivotManip'  ]	
		
		mc.frameLayout( panels[0]  , li = 80 ,  cll = 1 ,  w = 262 ,  bgc = [ 0.23 , 0.23 , 0.24 ]  ,   label = 'General' , p = UIparent  , cc = self.variableNameInGlobal + '.resizeMainWindow()' , ec = self.variableNameInGlobal + '.resizeMainWindow()' )
		
		# declaration du form
		
		form = mc.formLayout( numberOfDivisions = 100 ,  bgc = [ 0.27 , 0.27 , 0.27 ]  ) 
				
		# declaration des elements
		
		self.UI_manipGeneral_baseName(   panels[1] , form  )
		self.UI_manipGeneral_setOrient(  panels[2] , form  )	
		self.UI_manipGeneral_pivotManip( panels[3] , form  )			
				
		# ajout des elements dans le 
		
		mc.formLayout( form , e = True ,  af =[  ( panels[1] , 'top'    , 5 )  , ( panels[1] , 'left'   , 10  )   ]   , ac = [                                                                                            ] )  # baseName 	                                      
		mc.formLayout( form , e = True ,  af =[  ( panels[2] , 'left'   , 10 ) , ( panels[2] , 'bottom' , 5 )    ]   , ac = [  ( panels[2] , 'top'  ,  5  ,  panels[1] )                                                ] )  # setOrient	                   			                          
		mc.formLayout( form , e = True ,  af =[  ( panels[3] , 'top'   ,  5 )  , ( panels[3] , 'right' ,  3  )    ]   , ac = [                                                                                            ] )  # pivotManip 	                                          
	

	#_______________________________________________________________________________________________________________________________________________________________________ UI_manipGeneral_baseName
	def UI_manipGeneral_baseName( self , name , parent ):
	
			
		mc.rowColumnLayout( name , nc = 3 , columnWidth = [ ( 1 , 60 ) , ( 2 , 5 ) , ( 3 , 110 ) ]  , p = parent )
		mc.text( l = 'Basename:')			
		mc.text( l = ' ')	
		mc.textField( 'bmUI_baseNameField' , bgc = [ 0.4 , 0.4 , 0.4 ] , cc = ( self.variableNameInGlobal + '.getBaseName()' )  , ec = ( self.variableNameInGlobal + '.applyBaseName()' )  )
		
	def getBaseName( self ):
		self.baseName = mc.textField( 'bmUI_baseNameField' ,  q = True , tx = True )

	def applyBaseName(self):
		
		self.getBaseName()
		selection = mc.ls( sl = True )			
		
		for elem in selection:
			manip = buildRigClassManip.manip()
			manip.fillAttrFromRig(elem , masterRig = 0 )	
			manip.changeBaseName(self.baseName)		
		
		
	
	#_______________________________________________________________________________________________________________________________________________________________________ UI_manipGeneral_setOrient		
	def UI_manipGeneral_setOrient( self , name , parent ):
				
		mc.rowColumnLayout( name , nc = 3 , columnWidth = [ ( 1 , 60 ) , ( 2 , 5 ) , ( 3 , 110 ) ]  , p = parent )
		mc.button( l = 'setOrient' ,  bgc = [ 0.4 , 0.4 , 0.4 ] , c = ( '{0}.getSetOrient()'.format(self.variableNameInGlobal) ) )			
		mc.text( l = ' ')	
		mc.text( 'setOrientText' , l = '   None   ' )	    

		
	def getSetOrient( self ):
		selection = mc.ls(sl=True)
		
		if( len(selection) == 0 ):
			self.orient	= None
			mc.text(  'setOrientText' , e = True ,  l = ' None ' )				
		else:
			
			locators = buildLocator.buildLocator()
			self.orient	 = mc.getAttr( locators[0] + '.rotate' )[0]
			mc.delete(locators)
			mc.select(selection)
			mc.text(  'setOrientText' , e = True ,  l = '{0[0]:.2f}  {0[1]:.2f}  {0[2]:.2f} '.format(self.orient) )	

		
	#_______________________________________________________________________________________________________________________________________________________________________ UI_manipGeneral_pivotManip
	def UI_manipGeneral_pivotManip( self , name , parent ):
	
		
		iconePivotDossier = 'tools/buildManip/icon/pivot/'
			
		mc.rowColumnLayout( name , nc = 3 , columnWidth = [ ( 1 , 5 ) , ( 2 , 50 ) , ( 3 , 5 ) ]  , p = parent )
		
		mc.text( l = ' ')	
		mc.shelfButton( 'pivotButton'       , w = 50 , h = 50 , i = ( self.toolBoxPath + iconePivotDossier + 'pivot0.jpg'    )  , c = ( self.variableNameInGlobal + '.changePivotButton();' )  )      
		mc.text( l = ' ')				
	

	#_______________________________________________________________________________________________________________________________________________________________________ changePivotButton		
	def changePivotButton( self ):

		iconPivotDossier = 'tools/buildManip/icon/pivot/'
		iconPivotPath    = self.toolBoxPath + iconPivotDossier
		
		
		self.pivotButtonValue += 1
		
		if( self.pivotButtonValue > 6 ):
			self.pivotButtonValue = 0

		#_UI				
		mc.shelfButton( 'pivotButton' , e = True , i = ( iconPivotPath + 'pivot' + str( self.pivotButtonValue )  + '.jpg' ) )
		
		#_SCENE
		print( 'change pivot of selected manip! --->{0}'.format(self.pivotButtonValue) )
		selection = mc.ls( sl = True )			
		
		for elem in selection:
			manip = buildRigClassManip.manip()
			manip.fillAttrFromRig(elem , masterRig = 0 )		
			manip.changePivot( self.pivotButtonValue )	
		   
		mc.select(selection)		
		
	#=========================================================================================================================================================================================		   		                  
	#======================================================================================================================================================================  UI manip Shape
	#=========================================================================================================================================================================================	

	def UI_manipShape( self, UIparent ):
		
		
		panels =  [ 'bmUI_manipShape' , 'bmUI_manipShapeForm' , 'bmUI_manipShapeAxe' ,  'bmUI_manipShapeColor' ]	
		
		mc.frameLayout( panels[0]  , li = 80 ,  cll = 1 ,  w = 262 ,  bgc = [ 0.23 , 0.23 , 0.24 ]  ,   label = 'Shape' , p = UIparent  , cc = self.variableNameInGlobal + '.resizeMainWindow()' , ec = self.variableNameInGlobal + '.resizeMainWindow()')
		
		# declaration du form
		
		form = mc.formLayout( numberOfDivisions = 100 ,  bgc = [ 0.27 , 0.27 , 0.27 ]  ) 
				
		# declaration des elements
		
		self.UI_manipShape_form(  panels[1]  , form )
		self.UI_manipShape_axe(   panels[2]  , form )				
		self.UI_manipShape_color( panels[3]  , form )  	
			
		# ajout des elements dans le 
		
		mc.formLayout( form , e = True ,  af =[  ( panels[1] , 'top'    , 5  ) , ( panels[1] , 'left'   , 10   )   ]   , ac = [                                                                                             ] )  # manipShapeForm	                                      
		mc.formLayout( form , e = True ,  af =[  ( panels[2] , 'top'    , 5  )                                     ]   , ac = [  ( panels[2] , 'left'  ,  10  ,  panels[1] )                                                ] )  # manipShapeAxe 	                   			                          
		mc.formLayout( form , e = True ,  af =[  ( panels[3] , 'left'   , 10 ) ,( panels[3] , 'bottom'   , 10 )    ]   , ac = [  ( panels[3] , 'top'   ,  5   ,  panels[1] )                                                ] )  # manipShapeColor 	                                          

	
		
	#_______________________________________________________________________________________________________________________________________________________________________ UI_manipShape_form		
	def UI_manipShape_form( self , name , parent ):
	
		iconePivotDossier = 'buildManip/icon/shape/'
			
		mc.rowColumnLayout( name , nc = 3 , columnWidth = [ ( 1 , 120 ) , ( 2 , 10 ) , ( 3 , 50 ) ]  , p = parent )

		#---------------------------------------		
		mc.rowColumnLayout(  nc = 1 , w = 120)
		mc.text( l = ' ' , h = 15 )
		
		mc.optionMenu( 'formList' , w = 120 , cc = self.variableNameInGlobal + '.changeShapeFormIcon()')
		
		for form in self.CurveFormBank.formNames:
			mc.menuItem( l = form )
			
		mc.menuItem( l = '>> ADD <<' )
		
		mc.text( l = ' ' , h = 15 )
		mc.setParent(name)	
		#---------------------------------------
		
		mc.text( l = ' ')
		curentForm = mc.optionMenu( 'formList' , q = True , v = True )				
		mc.shelfButton( 'formPicture' , w = 50 , h = 50 , i = ( self.CurveFormBank.pathPictures + curentForm + '.jpg'     )  , c = self.variableNameInGlobal + '.applyShapeForm()' ) 
		
		
	#_______________________________________________________________________________________________________________________________________________________________________ changeShapeFormIcon				
	def changeShapeFormIcon(self):
		
		curentForm        = mc.optionMenu( 'formList' , q = True , v = True )
		self.shapeForm    = curentForm 
		curentFormPicture = curentForm + '.jpg'
		
		if not( curentFormPicture in self.CurveFormBank.formPictures ):
			if( curentForm == '>> ADD <<' ):
				curentForm      = 'add'
				self.shapeForm = curentForm 
			else:
				curentForm = 'noPicture'
			
		mc.shelfButton( 'formPicture'       , e = True , i = ( self.CurveFormBank.pathPictures + curentForm + '.jpg'    )  ) 		

	#_______________________________________________________________________________________________________________________________________________________________________ changeShapeFormIcon				
	def applyShapeForm(self):
		if( self.shapeForm == 'add'):
			self.CurveFormBank.saveSelectedForm()
		else:
			selection = mc.ls( sl = True )
			print('selection ----->' , selection)			
			
			for elem in selection:
				manip = buildRigClassManip.manip()
				manip.fillAttrFromUI(self)	
				manip.fillAttrFromRig(elem , masterRig = 0 )	
				manip.changeShapeForm( self.shapeForm )	

			mc.select(selection)




		
	#_______________________________________________________________________________________________________________________________________________________________________ UI_manipShape_axe					
	def UI_manipShape_axe( self , name , parent ):
	
		
		iconeAxeDossier   = 'tools/buildManip/icon/shapeRot/'
			
		mc.rowColumnLayout( name , nc = 3 , columnWidth = [ ( 1 , 1 ) , ( 2 , 50 ) , ( 3 , 1 ) ]  , p = parent )
		
		mc.text( l = ' ')	
		mc.shelfButton( 'bmUI_manipShapeAxeButton' , w = 50 , h = 50 , i = ( self.toolBoxPath + iconeAxeDossier   + 'manipAxe1.jpg' )  , c = ( self.variableNameInGlobal + '.changeShapeAxeButton()' )  )      
		mc.text( l = ' ')				
					
	#_______________________________________________________________________________________________________________________________________________________________________ changeShapeAxeButton		
	def changeShapeAxeButton(self):
	

		iconAxeDossier   = 'tools/buildManip/icon/shapeRot/'
		iconAxePath      = self.toolBoxPath + iconAxeDossier	
		
		self.shapeAxe += 1
		
		if( self.shapeAxe > 2 ):
			self.shapeAxe = 0
		
		#_UI	
		mc.shelfButton( 'bmUI_manipShapeAxeButton' , e = True , i = ( iconAxePath + 'manipAxe' + str( self.shapeAxe )  + '.jpg' )  )    
		
		print('change shape axe selection  ------> {0}'.format(self.shapeAxe) )
		
		
		selection = mc.ls( sl = True )			
		
		for elem in selection:
			manip = buildRigClassManip.manip()
			manip.fillAttrFromRig(elem , masterRig = 0 )
			manip.shapeForm = self.shapeForm		
			manip.changeShapeAxe( self.shapeAxe )	

		mc.select(selection)




		
		
	#_______________________________________________________________________________________________________________________________________________________________________ UI_manipShape_color				
	def UI_manipShape_color( self , name , parent ):
	
	
		# w = 240	
		rows      = 2
		columns   = 16 
		cellHeigh = 19 
		cellWidth = 15
		
		mc.palettePort( name ,      dim = [ columns , rows  ]   ,    width = (columns * cellWidth)    ,    height = (rows * cellHeigh)    , transparent = 0 , topDown = True , colorEditable = False , setCurCell = 0  , p = parent  )	
		mc.palettePort( name , e = True , cc = ( self.variableNameInGlobal + '.changeShapeColorButton()' ) )	
		
		for i  in range( 1 , 32 ):	
			componentColors = mc.colorIndex( i , q = True )	
			mc.palettePort(   name ,  e = True ,  rgbValue = [ i , componentColors[0] , componentColors[1] , componentColors[2] ]   )
			
		mc.palettePort(       name ,  e = True ,  rgbValue = [ 0 , 0.6 , 0.6 , 0.6 ]   )

	#_______________________________________________________________________________________________________________________________________________________________________ changeShapeColorButton				
	def changeShapeColorButton(self):		

		#_UI			
		self.indexColor = mc.palettePort( 'bmUI_manipShapeColor' , query=True , scc = True ) 
		
		selection = mc.ls( sl = True )			
		
		for elem in selection:
			manip = buildRigClassManip.manip()
			manip.fillAttrFromRig(elem , masterRig = 0 )		
			manip.changeColor( self.indexColor )	
		
	
		
	#=========================================================================================================================================================================================		   		                  
	#======================================================================================================================================================================  UI manip Option
	#=========================================================================================================================================================================================	

	def UI_manipOption( self, UIparent ):
		
		
		panels =  [ 'AM_manipOption' , 'AM_colorPanel' , 'AM_shapePanel' , 'AM_createManipButton' ,  'AM_pivotRotateManip' ,  'AM_optionVisButton' ,  'AM_option'   ]	
		
		mc.frameLayout( panels[0]  , li = 80 ,  cll = 1 ,  w = 262 ,  bgc = [ 0.23 , 0.23 , 0.24 ]  ,   label = 'Option' , p = UIparent  , cc = self.variableNameInGlobal + '.resizeMainWindow()' , ec = self.variableNameInGlobal + '.resizeMainWindow()')

		
		icoOptionDossier = 'tools/buildManip/icon/option/'
		icoOptionPath = self.toolBoxPath + icoOptionDossier   
		
		manipOptionsAnnotation = [ 'auto pivot' , 'auto orient' , 'adjust shape to obj' , 'Make Jo' , 'Connect vis' , 'constra' , 'Parent to root' ,  'add to animSet'  ]	
		nbrOptions = len( self.manipOptions ) 
		sizeIcone = 34 
		
		mc.rowColumnLayout( 'optionPanel' , nc = 6  )
		
	
		for i in range( 0 , nbrOptions ):
	
			activeName = 'Off'
			if( self.optionChoice[i] == 1 ):
				activeName = 'On'
				
			mc.shelfButton( ('AM_' + self.manipOptions[i] + '_ITRB' ) , w = sizeIcone , h = sizeIcone , ann = manipOptionsAnnotation[i]   ) 
			mc.shelfButton( ('AM_' + self.manipOptions[i] + '_ITRB' ) , e = True , c = ( self.variableNameInGlobal + '.changeOptionButton(%r)'%(i) ) ,  i = ( icoOptionPath + 'optionAM_' + self.manipOptions[i] + activeName + '.jpg')  ) 
			

	#______________________________________________________________________________________________________________________________________________________________________  changeOptionButton
	
	def changeOptionButton( self , index ):
	

		activeNames     =  [ 'Off' , 'On' ]
		icoOptionDossier =  'tools/buildManip/icon/option/' 	
		icoOptionPath    =  self.globalPath + icoOptionDossier
		nbrOptions       =  len( self.manipOptions )	
		
		if( self.optionChoice[ index ] == 1 ):
			self.optionChoice[ index ] = 0
		else:
			self.optionChoice[ index ] = 1
			
	
		for i in range( 0 , nbrOptions ):
			mc.shelfButton(  ('AM_' + self.manipOptions[i] + '_ITRB' ) , e = True , i = ( icoOptionPath + 'optionAM_' + self.manipOptions[i] + activeNames[ self.optionChoice[i] ] + '.jpg') )		
	



	#=========================================================================================================================================================================================		   		                  
	#======================================================================================================================================================================  AUTRE
	#=========================================================================================================================================================================================				
			
			
	def resizeMainWindow(self):

		# self.variableNameInGlobal + '.resizeMainWindow()
		
		general  = 1 - mc.frameLayout( 'bmUI_general'     , q = True ,  cl = True )
		shape    = 1 - mc.frameLayout( 'bmUI_manipShape'  , q = True ,  cl = True )		
		option   = 1 - mc.frameLayout( 'AM_manipOption'   , q = True ,  cl = True )
		
		base = 107
		
		hGeneral = base + 62 * general + 112 * shape + 70 * option
		
		mc.window( 'buildManipWindow'   , e = True ,  h = hGeneral )
		

		
		
	def createManipButton(self):

		
		manipObj = buildRigClassManip.manip()
		manipObj.fillAttrFromUI(self)
		print(manipObj.orient)		
		manipObj.createFromSelection()
		print(manipObj.orient)
		
		if not( self.baseName == '' ) and not( self.baseName == None ):
			manipObj.changeBaseName(self.baseName)
			
		
	
		print('=========================')
		print( '     CREATE MANIP       ')
		print( 'baseName : ' , self.baseName  )
		print( 'orient   : ' , self.orient  )
		print( 'pivot    : ' , self.pivotButtonValue)
		print( 'Form     : ' , self.shapeForm )		
		print( 'axe      : ' , self.shapeAxe )			
		print( 'color    : ' , self.indexColor )	
		print( 'option   : ' , self.optionChoice )	  
		print('=========================')
		
	#=========================================================================================================================================================================================
	#==============================================================                    MAIN UI                      ===========================================================================
	#=========================================================================================================================================================================================		

	
	def mainUi(self):
	
		win ='buildManipWindow'
		
		
		if( mc.windowPref( win , ex = True ) ):
			mc.windowPref( win , e = True , w = 280 , h = 200 )
		
		if( mc.window( win , ex = True ) ):
			mc.deleteUI( win , wnd = True )
		
		 
		 
		
		mc.window( win , w = 280 , h = 200 , s = True ) 
		
		mainColumName = 'mainColumn'	
		mc.columnLayout( mainColumName , columnAttach = [ 'both' , 10 ] , rowSpacing = 0 , columnWidth = 280 , bgc = [ 0.27 , 0.27 , 0.27 ]  )
		
		mc.text( l = '' , h = 1  , p = mainColumName)
		self.UI_manipGeneral( mainColumName )
		self.UI_manipShape(   mainColumName )
		self.UI_manipOption(  mainColumName )
		mc.text( l = '' , h = 5 , p = mainColumName)		
		mc.button( l = 'CREATE MANIP' , bgc = [ 0.5 , 0.3 , 0.3 ] , p = mainColumName , c = self.variableNameInGlobal + '.createManipButton()' )
		mc.text( l = '' , h = 10 , p = mainColumName)
		
			
		
				
		mc.showWindow( win )
	
	







