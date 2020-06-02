

'''
	name:  attrManager
	type:  RIGGING
	tag:   attr
	date:  06/11/2016	
	input: None
	----------------------------------------------------------
	UI for modify attr
	
'''


import sys	
import maya.cmds as mc	
import maya.mel as mel

from ..utils import utilsMaya
from ..utils import utilsPython



#__________________________________________________________________________________________________________________________ main proc

def attrManager():

	#try: print( attrManagerUIVar )
	#except: exec('attrManagerUIVar = attrManagerUI()') in globals()
	exec('attrManagerUIVar = attrManagerUI()') in globals()
	exec('attrManagerUIVar.mainUi()') in globals() 

class attrManagerUI():

	
	#______________________________________________________________________________________________________________________________________________________________________   INIT
	
	def __init__(self):	
		
		self.win ='attrManagerWindow'
		

		self.globalPath           = 'C:/Users/Matthieu/Desktop/Travail/code/maya/script/python/toolBox/tools/'
		self.variableNameInGlobal = 'toolBox.tools.attrManager.attrManager.attrManagerUIVar'	
		
		self.attrs            = []
		self.channelBoxAttrs  = []
		self.hideAttrs        = []
		self.lockAttrs        = []
		self.disKeyAttrs      = []

		
		self.channelboxLayoutDim   = [ 55 , 7 , 7 , 7 , 7 , 7  ]
		self.channelboxLayoutWidth = 205 
		
		self.hideLayoutDim = [ 15 , 80 ]
		self.hideLayoutWidth = 90


		self.cbScrollName = 'cbScrollAttr'
		self.hideScrollName	 =  'hideScrollAttr'		
		self.scrollBarThickness = 16
		self.scrollBarThickness = 16
		self.mainColumName = 'mainColumn'
		
		self.intervalSize = 5

		self.bothListLayoutName = 'bothListLayout' 
		
		self.attrCbColumnName   = 'attrCbColumn'
		self.attrHideColumnName = 'attrHideColumn'
		
		self.bgcStandard = 'bgc = [ 0.3 , 0.3 , 0.3 ]'
		self.bgcActif    = 'bgc = [ 0.7 , 0.4 , 0.4 ]'
		
		self.mainWidth = self.channelboxLayoutWidth +  self.hideLayoutWidth + self.scrollBarThickness * 2 + self.intervalSize * 2 + 20	
		self.mainHeight = 259
		
		
		self.whSideSpaceMainWin = [ 5 , 5 ]
		
		self.addAttrPanelName = 'addAttrPanel'
		
		
		self.channelBoxWinTitleName = 'channelBoxWinTitle' 
		self.hideWinTitleName       =  'hideWinTitle'
		self.mainButtonLayout = 'mainButtonLayout'
		
		self.textFieldAddAttrNames = [ 'tf_separator' , 'tf_enumOnOff' , 'tf_intOnOff' , 'tf_floatOnOff' , 'tf_float1'  ]	
		self.objs = []		


	#=========================================================================================================================================================================================		   		                  
	#======================================================================================================================================================================  
	#=========================================================================================================================================================================================	



	
	def UI_channelBoxWin( self ):
		
		mc.scrollLayout( self.cbScrollName , w = self.channelboxLayoutWidth + self.scrollBarThickness   ,  bgc = [ 0.2 , 0.2 , 0.2 ] , horizontalScrollBarThickness = self.scrollBarThickness , verticalScrollBarThickness = self.scrollBarThickness  , p = self.mainColumName  )
		mc.columnLayout( self.attrCbColumnName, w = self.channelboxLayoutWidth  , p = self.cbScrollName , bgc = [ 0.2 , 0.2 , 0.2 ]   )
			
		

	def UI_hideWin( self ):

		mc.scrollLayout( self.hideScrollName ,     bgc = [ 0.2 , 0.2 , 0.2 ] , horizontalScrollBarThickness = self.scrollBarThickness , verticalScrollBarThickness = self.scrollBarThickness , p = self.mainColumName  )
		mc.columnLayout( self.attrHideColumnName  , p = self.hideScrollName , bgc = [ 0.2 , 0.2 , 0.2 ]   )		
		
	
	def UI_addAttrPanel( self ):
		
		width = self.mainWidth - 30
		
		
		mc.rowColumnLayout( self.addAttrPanelName , nc = 1 , w = width , columnWidth = [ ( 1 , width )]  , p = self.mainColumName )

		dim = [ 32 , 32 , 31 ]
		

		mc.separator( height=20, style='in' , p = self.addAttrPanelName  )
		utilsMaya.buildUi_makeNiceBox( 'separatorBox'   , self.addAttrPanelName ,  width , 20  , [ 'mc.text( l = "Separator  " )' , 'mc.textField( "{0}" , tx = "EXTRA_ATTR" , bgc = [ 0.4 , 0.4 , 0.4 ] )'.format( self.textFieldAddAttrNames[0] ) , 'mc.button( l = "Create" , c = "{0}.createAttr(0)" )'.format( self.variableNameInGlobal) ] , dim  )			
		utilsMaya.buildUi_makeNiceBox( 'enumOnOffBox'   , self.addAttrPanelName ,  width , 20  , [ 'mc.text( l = "Enum ON OFF" )' , 'mc.textField( "{0}" , tx = "switch"     , bgc = [ 0.4 , 0.4 , 0.4 ] )'.format( self.textFieldAddAttrNames[1] ) , 'mc.button( l = "Create" , c = "{0}.createAttr(1)" )'.format( self.variableNameInGlobal) ] , dim  )			
		utilsMaya.buildUi_makeNiceBox( 'intOnOffBox '   , self.addAttrPanelName ,  width , 20  , [ 'mc.text( l = "Int ON OFF " )' , 'mc.textField( "{0}" , tx = "switch"     , bgc = [ 0.4 , 0.4 , 0.4 ] )'.format( self.textFieldAddAttrNames[2] ) , 'mc.button( l = "Create" , c = "{0}.createAttr(2)" )'.format( self.variableNameInGlobal) ] , dim  )	
		utilsMaya.buildUi_makeNiceBox( 'floatOnOffBox ' , self.addAttrPanelName ,  width , 20  , [ 'mc.text( l = "Float ON OFF " )' , 'mc.textField( "{0}" , tx = ""         , bgc = [ 0.4 , 0.4 , 0.4 ] )'.format( self.textFieldAddAttrNames[3] ) , 'mc.button( l = "Create" , c = "{0}.createAttr(3)" )'.format( self.variableNameInGlobal) ] , dim  )		
		utilsMaya.buildUi_makeNiceBox( 'floatBox    '   , self.addAttrPanelName ,  width , 20  , [ 'mc.text( l = "Float"       )' , 'mc.textField( "{0}" , tx = ""           , bgc = [ 0.4 , 0.4 , 0.4 ] )'.format( self.textFieldAddAttrNames[4] ) , 'mc.button( l = "Create" , c = "{0}.createAttr(4)" )'.format( self.variableNameInGlobal) ] , dim  )			
		
		
	def UI_channelBoxWinTitle( self ):
		
		mc.rowColumnLayout( self.channelBoxWinTitleName , nc = 1 , columnWidth = [ ( 1 , self.channelboxLayoutWidth + self.scrollBarThickness  )]  , p = self.mainColumName )		
		mc.text( 'toto' , l = ' CHANNEL BOX '  , h = 20 , p = self.channelBoxWinTitleName )

	def UI_hideWinTitle( self ):
		
		mc.rowColumnLayout( self.hideWinTitleName , nc = 1 , columnWidth = [ ( 1 , self.hideLayoutWidth + self.scrollBarThickness  )]  , p = self.mainColumName )		
		mc.text( 'toto' , l = ' HIDE '  , h = 20 , p = self.hideWinTitleName )

	
	def UI_mainButton( self ):
		
		width = self.mainWidth - 30
		
		mainButtonCmds = self.variableNameInGlobal + '.getSelectedObjCmds()'
		
		mc.rowColumnLayout( self.mainButtonLayout , nc = 1 , columnWidth = [ ( 1 , width )]  , p = self.mainColumName )		
		mc.button( 'toto' , l = ' SELECT OBJ ' , c = mainButtonCmds , bgc = [ 0.4 , 0.5 , 0.4 ]  , h = 20 , p = self.mainButtonLayout )		
		
		
		
	#______________________________________________________________________________________________________________________________________________ refreshUI_channelBox
	
	def refreshUI_channelBox( self ):
		
		# DELETE	
		try:
			mc.deleteUI( 'emptyText' )
		except:
			pass
					
		for i in range( 1 , len(self.attrs)):
			try:
				mc.deleteUI( 'commandBox%r' %i )
			except:
				break
		
		# CREATE
		
		if( len(self.channelBoxAttrs) == 0 ):
			mc.text( 'emptyText' , l = "---- empty ----" , p = self.attrCbColumnName , w = self.channelboxLayoutWidth , h = 20  )
			return 0			
				
		i = 1	
		for attr in self.channelBoxAttrs:



			bgcLock = self.bgcStandard 	
			bgcKeyable = self.bgcStandard 		
			
			if( attr in self.lockAttrs ):
				bgcLock    = 'bgc = [ 0.7 , 0.4 , 0.4 ]'
				
			if( attr in self.disKeyAttrs ):
				bgcKeyable   = 'bgc = [ 0.4 , 0.7 , 0.4 ]'				
				
			
			
					
			moveUpCmds      = self.variableNameInGlobal + '.moveInArrayCmds(   "{0}" , -1 )'.format( attr )              
			moveDwnCmds     = self.variableNameInGlobal + '.moveInArrayCmds(   "{0}" ,  1 )'.format( attr ) 
			setLockCmds     = self.variableNameInGlobal + '.setLockCmds(       "{0}"      )'.format( attr ) 
			setKeyableCmds  = self.variableNameInGlobal + '.setDisKeyableCmds( "{0}"      )'.format( attr ) 
			setHideCmds     = self.variableNameInGlobal + '.setHideCmds(       "{0}"      )'.format( attr ) 
			
			
			attrName         = ( 'mc.text(   l = "{0}" , ann = "{0}"  )  '.format( attr ) ) 		
			moveUp           = ( 'mc.button( l = "^"            , {0}  , c = \'{1}\' )'.format( self.bgcStandard , moveUpCmds)     ) 		
			moveDwn          = ( 'mc.button( l = "v"            , {0}  , c = \'{1}\' )'.format( self.bgcStandard , moveDwnCmds)    )		
			setLock          = ( 'mc.button( l = "L"            , {0}  , c = \'{1}\' )'.format( bgcLock          , setLockCmds)    ) 		
			setKeyable       = ( 'mc.button( l = "K"            , {0}  , c = \'{1}\' )'.format( bgcKeyable       , setKeyableCmds) ) 
			setHide          = ( 'mc.button( l = ">"            , {0}  , c = \'{1}\' )'.format( self.bgcStandard , setHideCmds)    )	
	
			utilsMaya.buildUi_makeNiceBox( 'commandBox%r' %i   , self.attrCbColumnName ,  self.channelboxLayoutWidth , 20  , [ attrName , moveUp , moveDwn , setLock , setKeyable , setHide ] , self.channelboxLayoutDim   )		
			i += 1

		
		return 1			

	#______________________________________________________________________________________________________________________________________ 	moveInArrayCmds

	def refreshUI_hide( self ):
		
		# DELETE	
		try:
			mc.deleteUI( 'emptyText2' )
		except:
			pass
					
		for i in range( 1 , len(self.attrs) ):
			try:
				mc.deleteUI( 'attrHideBox%r' %i )
			except:
				break
		
		# CREATE
		
		if( len(self.hideAttrs) == 0 ):
			mc.text( 'emptyText2' , l = "---- empty ----" , p = self.attrHideColumnName , w = self.hideLayoutWidth , h = 20  )
			return 0			
				
		i = 1	
		for attr in self.hideAttrs:
							
 
			setHideCmds     = self.variableNameInGlobal + '.setHideCmds(       "{0}"      )'.format( attr ) 
			
			setHide          = ( 'mc.button( l = "<"   , {0}  , c = \'{1}\' )'.format( self.bgcStandard , setHideCmds)    )				
			attrName         = ( 'mc.text(   l = "{0}" , ann = "{0}"  )  '.format( attr ) ) 		

	
			utilsMaya.buildUi_makeNiceBox( 'attrHideBox%r' %i   , self.attrHideColumnName ,  self.hideLayoutWidth * 2 , 20  , [ setHide , attrName ] , self.hideLayoutDim    )		
			i += 1

			
		return 1			


		
	#______________________________________________________________________________________________________________________________________ 	moveInArrayCmds
	def moveInArrayCmds(self , attr , iToMove ):
		
		self.channelBoxAttrs = utilsPython.moveInArray( self.channelBoxAttrs , attr , iToMove )
		self.refreshUI_channelBox()		
	
		
	#______________________________________________________________________________________________________________________________________ 	setLockCmds		
	def setLockCmds( self , attr ):
		
		if( attr in self.lockAttrs ):
			self.lockAttrs.remove(attr)
		else:
			self.lockAttrs.append(attr)
			
		self.refreshUI_channelBox()	
	
	#______________________________________________________________________________________________________________________________________ 	setDisKeyableCmds			
	def setDisKeyableCmds( self , attr ):
		
		if( attr in self.disKeyAttrs ):
			self.disKeyAttrs.remove(attr)
		else:
			self.disKeyAttrs.append(attr)
			
		self.refreshUI_channelBox()	

	#______________________________________________________________________________________________________________________________________ 	setHideCmds			
	def setHideCmds( self , attr ):
		
		if( attr in self.channelBoxAttrs ):
			self.channelBoxAttrs.remove(attr)
		else:
			self.channelBoxAttrs.append(attr)
	
		if( attr in self.hideAttrs ):
			self.hideAttrs.remove(attr)
		else:
			self.hideAttrs.append(attr)	
			
			
		self.refreshUI_hide()	
		self.refreshUI_channelBox()		

		
		
		
		
	#______________________________________________________________________________________________________________________________________ 	setHideCmds				
	def createAttr( self , index ):
		
		name     = mc.textField( self.textFieldAddAttrNames[index] , q = True , tx = True )
		attrType = self.textFieldAddAttrNames[index].split('tf_')[1]  
		
		for obj in self.objs:
			utilsMaya.addSpecialAttr( obj , name , attrType )

		self.getObjAttr()
		self.refreshUI_hide()	
		self.refreshUI_channelBox()				


	#______________________________________________________________________________________________________________________________________ 	mainButtonCmds		
	
	def getSelectedObjCmds( self ):
		
		selection = mc.ls( sl=True )
		
		self.objs = selection
		
		print( 'select:' , self.objs )
		
		self.getObjAttr()
		self.refreshUI_hide()	
		self.refreshUI_channelBox()			
		

	#______________________________________________________________________________________________________________________________________ 	mainButtonCmds		
	
	
	def getObjAttr(self):
		
		obj = self.objs[0]
		
		#_attr
		self.attrs            = mc.listAttr( obj )		
		
		#_cb
		cbKeyableAttr    = mc.listAttr( obj  , k = True  )
		cbNonkeyableAttr = mc.listAttr( obj  , k = False , v = True , cb = True )		
		
		cbAttrs = cbKeyableAttr
		
		if not ( cbNonkeyableAttr == None ):
			cbAttrs += cbNonkeyableAttr
			
		cbAttrs = list(set(cbAttrs))    		
		
		self.channelBoxAttrs  = mc.listAttr( obj  , k = True )
		
		#_hide		
		self.hideAttrs = self.attrs[:]
		
		for attr in self.channelBoxAttrs : 
			self.hideAttrs.remove(attr)
		
		#_lock
		self.lockAttrs = mc.listAttr( obj , l = True )
		if ( self.lockAttrs == None ):		
			self.lockAttrs = []
		
		#_diskeyable		
		self.disKeyAttrs     = self.attrs[:]
		keyAttrs             = mc.listAttr( obj , k = True )			
		for attr in keyAttrs : 
			self.disKeyAttrs.remove(attr)		
		
		print("=============================================================")
		print( "attr:"    ,len(self.attrs)           , self.attrs)
		print( "cb:"      ,len(self.channelBoxAttrs) , self.channelBoxAttrs)
		print( "hide:"    ,len(self.hideAttrs)	      , self.hideAttrs)	
		print( "lock:"    ,len(self.lockAttrs)	      , self.lockAttrs)	
		print( "diskey:"  ,len(self.disKeyAttrs)     , self.disKeyAttrs)  
		print("=============================================================")

	
	#=========================================================================================================================================================================================
	#==============================================================                    MAIN UI                      ===========================================================================
	#=========================================================================================================================================================================================		

	
	def mainUi(self):
	
		
		
		
		if( mc.windowPref( self.win , ex = True ) ):
			mc.windowPref( self.win , e = True , w = self.mainWidth , h = self.mainHeight  )
		
		if( mc.window( self.win , ex = True ) ):
			mc.deleteUI( self.win , wnd = True )
		
		 
		
		mc.window( self.win , w = self.mainWidth , h = self.mainHeight  , s = True ) 
		
		mc.formLayout( self.mainColumName , numberOfDivisions = 100 ,  bgc = [ 0.27 , 0.27 , 0.27 ]   )  #0.27

		
		
		self.UI_channelBoxWinTitle()
		self.UI_hideWinTitle()
		self.UI_channelBoxWin()
		self.UI_hideWin()		
		self.UI_addAttrPanel()
		self.UI_mainButton()


		mc.formLayout( self.mainColumName , e = True ,  af =[  ( self.channelBoxWinTitleName , 'top'    , self.whSideSpaceMainWin[1] )   , ( self.channelBoxWinTitleName     , 'left'   , self.whSideSpaceMainWin[0] )           ]   )		
		mc.formLayout( self.mainColumName , e = True ,  af =[  ( self.hideWinTitleName       , 'top'    , self.whSideSpaceMainWin[1] ) ] , ac =[ ( self.hideWinTitleName     , 'left'   , 0  , self.channelBoxWinTitleName )     ]   )		
		
		mc.formLayout( self.mainColumName , e = True ,  af =[  ( self.addAttrPanelName  , 'left'   , self.whSideSpaceMainWin[0]  )   ] , ac = [ (  self.addAttrPanelName    , 'bottom'    , 0 , self.mainButtonLayout  ) ]   )			
		mc.formLayout( self.mainColumName , e = True ,  af =[  ( self.cbScrollName      , 'left'   , self.whSideSpaceMainWin[0]  )   ] , ac = [ (  self.cbScrollName    , 'bottom'    , 0 , self.addAttrPanelName  )                                                                     ,( self.cbScrollName     , 'top'    , 0 ,  self.channelBoxWinTitleName ) ] ) 		
		mc.formLayout( self.mainColumName , e = True ,  af =[  ( self.hideScrollName    , 'right'   , self.whSideSpaceMainWin[0] )   ] , ac = [ (  self.hideScrollName  , 'bottom'    , 0 , self.addAttrPanelName  ) , (  self.hideScrollName  , 'left'      , 0 , self.cbScrollName   ) ,( self.hideScrollName   , 'top'    , 0 , self.hideWinTitleName  )       ] )	


		mc.formLayout( self.mainColumName , e = True ,  af =[  ( self.mainButtonLayout , 'bottom' , self.whSideSpaceMainWin[1] ) , ( self.mainButtonLayout , 'left'   , self.whSideSpaceMainWin[0] )     ]   )		
			
		
		mc.showWindow( self.win )
				
		self.refreshUI_channelBox()
		self.refreshUI_hide()
		
	
	
	
