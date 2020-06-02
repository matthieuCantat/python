

'''
	name:  constraintManager
	type:  RIGGING
	tag:   constraint
	date:  07/11/2016	
	input: selected manip
	----------------------------------------------------------
	mirror manip
	
'''
import sys	
import maya.cmds as mc	
import maya.mel as mel

from ..utils import utilsMaya


#__________________________________________________________________________________________________________________________ main proc

def constraintManager():

	#try: print( constraintManagerUIVar )
	#except: exec('constraintManagerUIVar = constraintManagerUI()') in globals()
	exec('constraintManagerUIVar = constraintManagerUI()') in globals()
	exec('constraintManagerUIVar.mainUi()') in globals() 

class constraintManagerUI():

	
	#______________________________________________________________________________________________________________________________________________________________________   INIT
	
	def __init__(self):	
		
		self.win ='constraintManagerWindow'
		
		arrayPath             = __file__.split('\\')
		self.selfPath         = '/'.join(arrayPath[0:-1]) + '/'	
		self.toolPathRelative = 'constraintManager/'
		
		print(  'path '  , self.selfPath )
		
		self.globalPath   = self.selfPath 
		self.variableNameInGlobal = 'toolBox.tools.constraintManager.constraintManager.constraintManagerUIVar'
		self.modulPathInGlobal = 'toolBox.tools.constraintManager'
		
		
		self.ui_cbType      = [ 'cbParent' , 'cbPoint' , 'cbOrient' , 'cbScale' , 'cbAim' , 'cbPv' , 'cbVis'      ]
		self.constraintType = [ 'parent'   , 'point'   , 'orient'   , 'scale'   , 'aim'   , 'pv'   , 'visibility' ]
		self.typeValues     = [ 1 , 0 , 0 , 1 , 0 , 0 , 1 ]

		self.ui_rbSelection   = [ 'rbOneMaster' , 'rb2by2' , 'rbDefaut' ]
		self.rbSelectionLabel = [ 'oneMaster'   , '2by2'   , 'defaut'   ]
		self.rbSelectionValue = [ 1 , 0 , 0 ]
		

		self.ui_skipAttrChoice = [ 'ui_skipTX' , 'ui_skipTY' , 'ui_skipTZ' , 'ui_skipRX' , 'ui_skipRY' , 'ui_skipRZ' , 'ui_skipSX' , 'ui_skipSY' , 'ui_skipSZ' ]
		self.ui_skipAttrValue  = [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ]		
		
		self.mainHeight = [ 177 , 266 ]
		self.mainHeightIndex = 0		
		
		# load manip class
		#sys.path.append( self.globalPath + 'buildManip/' )
		#exec('import manipsClass' ) in globals()  
		#exec('reload(manipsClass)') in globals() 
		


	#=========================================================================================================================================================================================		   		                  
	#======================================================================================================================================================================  
	#=========================================================================================================================================================================================	
	
	#_______________________________________________________________________________________________________________________________________ UI_constraintType
	def UI_constraintType( self, UIparent ):
		
		
		name = 'ui_columnType'

		
		mc.rowColumnLayout( name , nc = 4 , columnWidth = [ ( 1 , 70 ) , ( 2 , 70 ) , ( 3 , 70 ) , ( 4 , 70 ) ]  , p = UIparent )
		
		for i in range( 0 , len(self.ui_cbType) ):
			mc.checkBox( self.ui_cbType[i]  , label = self.constraintType[i] ,  v = self.typeValues[i] , p = name )

		
		
	def getConstraintType(self):
		
		for i in range( 0 , len(self.ui_cbType) ):
			self.typeValues[i] = mc.checkBox( self.ui_cbType[i]  , q = True , v = True )		
		
	#_______________________________________________________________________________________________________________________________________ UI_selectionManager
	def UI_selectionManager( self , UIparent ):

		
		name = 'ui_selectionManager'
		
		mc.rowColumnLayout( name , nc = 3 , columnWidth = [ ( 1 , 90 ) , ( 2 , 90 ) , ( 3 , 90 ) ]  , p = UIparent )
		
		mc.radioCollection()
		for i in range( 0 , len( self.ui_rbSelection ) ):		
			mc.radioButton( self.ui_rbSelection[i] , label = self.rbSelectionLabel[i] , sl = self.rbSelectionValue[i] )
		
			
	def getSelectionManager(self):
		
		for i in range( 0 , len(self.ui_rbSelection) ):
			self.rbSelectionValue[i] = mc.radioButton( self.ui_rbSelection[i]  , q = True , sl = True )				

	#_______________________________________________________________________________________________________________________________________ UI_skipAttr
	def UI_skipAttr( self , UIparent ):
		
		nameColumn = 'skipAttrColumn'
		nameGrid   = 'skipAttrGrid'
		
		mc.columnLayout( nameColumn , p = UIparent , columnAttach = [ 'both' , 10 ] , rowSpacing = 0 , columnWidth = 100 , bgc = [ 0.27 , 0.27 , 0.27 ]  )
		mc.text( l = 'SKIP ATTR' , p = nameColumn , w = 60  )
		
		
		
		mc.gridLayout( nameGrid , p = nameColumn , cw = 15 , ch = 15  , nr = 4 , nc = 4 )
		
		
		mc.text(l=''  , p = nameGrid )
		mc.text(l='X' , p = nameGrid )
		mc.text(l='Y' , p = nameGrid )
		mc.text(l='Z' , p = nameGrid )
		                        
		textTRS = [ 'T' , 'R' , 'S' ]
		
		for lap in range( 0 , 3 ):
			mc.text( l = textTRS[lap] , p = nameGrid  )
			for i in range( 0 , 3 ):
				mc.checkBox( self.ui_skipAttrChoice[ lap*3 + i ] , v = self.ui_skipAttrValue[ lap*3 + i ] , l = '' , p = nameGrid  )



	def getSkipAttr(self):
		
		for i in range( 0 , len(self.ui_skipAttrChoice) ):
			self.ui_skipAttrValue[i] = mc.checkBox( self.ui_skipAttrChoice[i]  , q = True , v = True )		


			
	def makeCns(self):

		self.getSelectionManager()
		self.getConstraintType()
		self.getSkipAttr()		
		
		
		#___ get
		objs  = mc.ls(sl = True ) 	
		
		mode  = self.rbSelectionLabel[ self.rbSelectionValue.index(1)] 

		types = []
		for i in range( 0 , len(self.constraintType) ):
			
			if( self.constraintType[i] == 'visibility' ):
				if( self.typeValues[i] == 1 ):
					utilsMaya.buildConnections( objs , ['object_display'] , ['visibility'] , mode )				
			elif( self.typeValues[i] == 1 ):
				types.append( self.constraintType[i] )
		
		#___ build
		masters = utilsMaya.buildConstraint( objs , types , mode , 1 , self.ui_skipAttrValue )

					
		mc.select( masters )
			


		
	def toolGrid( self , UIparent ):
	
		toolList = [ 'buildConstaint2by2' , 'buildConstaintOneMaster' , 'buildConstraintProxy' , 'deleteConstraint' , 'resetConstraints' , 'selectConstraintMasters' , 'selectConstraintSlaves'  ]
		
		toolGridName = 'toolGridLayout'
		
		mc.gridLayout( toolGridName ,  numberOfColumns = 5 , cellWidthHeight = [ 50 , 50 ] , bgc = [ 0.27 , 0.27 , 0.27 ] , p = UIparent  )
		
		for tool in toolList:
			
			exec( 'import {0}.{1}.{1}'.format( self.modulPathInGlobal , tool)  ) in globals()
			cmds = (  '{0}.{1}.{1}.{1}()'.format( self.modulPathInGlobal , tool))
			path = ( self.globalPath + '/' +tool + '/' + tool + '.jpg' ) 
			
			mc.symbolButton(  ( tool + '_button' )   , c = cmds  , i = path , ann = tool ,  p = toolGridName  )                               
	
		
		
	#=========================================================================================================================================================================================
	#==============================================================                    MAIN UI                      ===========================================================================
	#=========================================================================================================================================================================================		

	
	def mainUi(self):
	
		
		
		if( mc.windowPref( self.win , ex = True ) ):
			mc.windowPref( self.win , e = True , w = 280 , h = self.mainHeight[0] )
		
		if( mc.window( self.win , ex = True ) ):
			mc.deleteUI( self.win , wnd = True )
		
		 
		
		mc.window( self.win , w = 280 , h = self.mainHeight[0] , s = True ) 
		
		mainColumName = 'mainColumn'	
		mc.columnLayout( mainColumName , columnAttach = [ 'both' , 10 ] , rowSpacing = 0 , columnWidth = 280 , bgc = [ 0.27 , 0.27 , 0.27 ]  )
		
		mc.text( l = '' , h = 10  , p = mainColumName)
		mc.separator( height=20, style='in', p = mainColumName  )		
		self.UI_constraintType(mainColumName)
		mc.separator( height=20, style='in' , p = mainColumName )
		self.UI_selectionManager(mainColumName)
		mc.separator( height=20, style='in', p = mainColumName  )
		
		mc.rowColumnLayout( 'rowSkipName' , nc = 2 , columnWidth = [ ( 1 , 90 ) , ( 2 , 170 )  ]  , p = mainColumName )	
		self.UI_skipAttr('rowSkipName')	

		makeCnsCmds  = self.variableNameInGlobal + '.makeCns()' 
		
		mc.columnLayout( 'buttonColumn' , p = 'rowSkipName' , columnAttach = [ 'both' , 10 ] , rowSpacing = 0 , columnWidth = 170 , bgc = [ 0.27 , 0.27 , 0.27 ]  )
		mc.text( l = ' ' , h = 25 )		
		mc.button( l = '>>> MAKE CNS <<<' , bgc = [ 0.5 , 0.3 , 0.3 ] , c = makeCnsCmds , h = 35 )
		mc.text( l = ' ' , h = 20 )				
		
		mc.text( l = '' , h = 10 , p = mainColumName)
		mc.separator( height=20, style='in', p = mainColumName  )
		self.toolGrid(mainColumName)
		mc.separator( height=20, style='in', p = mainColumName  )
		
			

				
				
				
				
				
		mc.showWindow( self.win )
	
	
