


import maya.cmds as mc	
import maya.api.OpenMaya as ompy

from ..utils import utilsMath
from ..utils import utilsMaya
from ..utils import utilsPython
from ..utils import utilsMayaApi

from . import buildRigClass
from . import buildRigClassManip


class mirrorRig():

	#______________________________________________________________________________________________________________________________________________________________________   INIT
	
	def __init__(self):	

		buildRigObj = buildRigClass.buildRig()
		self.dico_rigType_classBuild  = buildRigObj.dico_rigType_classBuild
		self.dico_rigType_classImport = buildRigObj.dico_rigType_classImport 
		
		self.variableNameInGlobal = 'toolBox.tools.rigManager.rigManager.rigManagerVar.mirrorRigVar'
		#self.variableNameInGlobal = 'toolBox.utils.mirrorRigClass.mirrorRigVar'

		self.radioButtonsName = [ 'ui_planeX' , 'ui_planeY' , 'ui_planeZ' , 'ui_planeCustom' ]
		self.uiCoords  = [ 'ui_coordsAX' , 'ui_coordsAY' , 'ui_coordsAZ' , 'ui_coordsBX' , 'ui_coordsBY' , 'ui_coordsBZ' , 'ui_coordsCX' , 'ui_coordsCY' , 'ui_coordsCZ' ] 		
		self.planeCoordsChoice  = [[ 0.0 , 0.0 , 0.0 , 0.0 , 1.0 , 0.0 , 0.0 , 0.0 , 1.0 ] , [ 0.0 , 0.0 , 0.0 , 1.0 , 0.0 , 0.0 , 0.0 , 0.0 , 1.0 ] , [ 0.0 , 0.0 , 0.0 , 0.0 , 1.0 , 0.0 , 1.0 , 0.0 , 0.0 ] , [ 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 ]] 		
		self.curPlanCoords	= [ 0.0 , 0.0 , 0.0 , 0.0 , 1.0 , 0.0 , 1.0 , 0.0 , 0.0 ]
		
		self.lockAxe = 2
		self.uiLockAxeButtonNames  = [ 'ui_lockX' , 'ui_lockY' , 'ui_lockZ' ]

		self.uiInvertButtonNames = [ 'ui_invX' , 'ui_invY' , 'ui_invZ' ]
		self.invertAxes = [ 0 , 0 , 0 ]

		self.bgcOn = 'bgc = [ 0.4 , 0.5 , 0.4 ]'
		self.bgcOff = 'bgc = [0.4,0.4,0.4] '

		self.prefixName  = [ 'ui_prefixA'  , 'ui_prefixB'  ]
		self.prefix      = [ 'l_'  , 'r_'  ]
		self.replaceName = [ 'ui_replaceA' , 'ui_replaceB' ]
		self.replace     = [ '' , '' ]
		
		
		self.mainHeight = [ 177 , 266 ]
		self.mainHeightIndex = 0
		
		self.nameFrame = 'planCoords'
		self.win = 'mirrorRigWindow'		


	#=========================================================================================================================================================================================		   		                  
	#======================================================================================================================================================================  
	#=========================================================================================================================================================================================	
	
	
	def UI_plan( self, UIparent ):
		
		
		planNameColumn = 'planColumn'
		nameChoice = 'planChoice'
		nameFrameColumn = 'planCoords2'
		
		mc.columnLayout( planNameColumn , p = UIparent , w = 280 )
		
		planeChoiceCmds = self.variableNameInGlobal + '.setCoordsBoard()'  
		
		cmdsStringD  = [ 'mc.text( l = "PLAN: " );mc.radioCollection()' ]
		cmdsStringD += [ 'mc.radioButton( "{0}" , label="X"      , onc = "{1}"                 )'.format( self.radioButtonsName[0] , planeChoiceCmds ) ]
		cmdsStringD += [ 'mc.radioButton( "{0}" , label="Y"      , onc = "{1}"                 )'.format( self.radioButtonsName[1] , planeChoiceCmds ) ]
		cmdsStringD += [ 'mc.radioButton( "{0}" , label="Z"      , onc = "{1}"     , sl = True )'.format( self.radioButtonsName[2] , planeChoiceCmds ) ]
		cmdsStringD += [ 'mc.radioButton( "{0}" , label="CUSTOM" , onc = "{1}"                 )'.format( self.radioButtonsName[3] , planeChoiceCmds ) ] 		
		
		
		utilsMaya.buildUi_makeNiceBox( nameChoice , planNameColumn , layoutWidth =  280  , casesHeight = 10 , caseCommands = cmdsStringD  , caseWidthPercent = [ 16 , 16 , 16 , 16 , 30 ]  )		
		
		
		
		mc.frameLayout( self.nameFrame  , li = 60 ,  cll = 1 , cl = True ,  bgc = [ 0.23 , 0.23 , 0.23 ]  , w = 260 ,   label = 'plan Coords' , p = planNameColumn , cc = (self.variableNameInGlobal + '.resize()') , ec = (self.variableNameInGlobal + '.resize()')  )			
		mc.columnLayout( nameFrameColumn , p = self.nameFrame , w = 260 , bgc = [ 0.3 , 0.3 , 0.4 ])
		
		bgc = 'bgc = [ 0.18 , 0.18 , 0.18 ]'

		getSymPlanCmds      = self.variableNameInGlobal + '.getSymPlanCoords()' 		
		getSelectedPlanCmds = self.variableNameInGlobal + '.getSelectedPlanCoords()' 		
		showPlanCmds        = self.variableNameInGlobal + '.showPlan()' 		
		
		
		cmdsStringA = [ 'mc.text( l = "A" )' , 'mc.textField( "{0}" ,{1} , tx = "0.0" )'.format( self.uiCoords[0] , bgc ) , 'mc.textField( "{0}" ,{1}, tx = "0.0"  )'.format( self.uiCoords[1] , bgc ) , 'mc.textField( "{0}" ,{1} , tx = "0.0"  )'.format( self.uiCoords[2] , bgc ) , 'mc.button( w = 50 , l = "create symPlan"   , bgc = [0.4,0.4,0.4]  , c = "{0}") '.format(getSymPlanCmds     ) ] 
		cmdsStringB = [ 'mc.text( l = "B" )' , 'mc.textField( "{0}" ,{1} , tx = "1.0" )'.format( self.uiCoords[3] , bgc ) , 'mc.textField( "{0}" ,{1}, tx = "0.0"  )'.format( self.uiCoords[4] , bgc ) , 'mc.textField( "{0}" ,{1} , tx = "0.0"  )'.format( self.uiCoords[5] , bgc ) , 'mc.button( w = 50 , l = "get plan coords"  , bgc = [0.4,0.4,0.4]  , c = "{0}") '.format(getSelectedPlanCmds) ] 	
		cmdsStringC = [ 'mc.text( l = "C" )' , 'mc.textField( "{0}" ,{1} , tx = "0.0" )'.format( self.uiCoords[6] , bgc ) , 'mc.textField( "{0}" ,{1}, tx = "1.0"  )'.format( self.uiCoords[7] , bgc ) , 'mc.textField( "{0}" ,{1} , tx = "0.0"  )'.format( self.uiCoords[8] , bgc ) , 'mc.button( w = 50 , l = "show plan"        , bgc = [0.4,0.4,0.4]  , c = "{0}") '.format(showPlanCmds       ) ] 			
		utilsMaya.buildUi_makeNiceBox( 'toto0' , nameFrameColumn , layoutWidth =  260  , casesHeight = 10 , caseCommands = cmdsStringA  , caseWidthPercent = [ 3 , 16 , 16 , 16 , 42 ]  )
		utilsMaya.buildUi_makeNiceBox( 'toto1' , nameFrameColumn , layoutWidth =  260  , casesHeight = 10 , caseCommands = cmdsStringB  , caseWidthPercent = [ 3 , 16 , 16 , 16 , 42 ]  )
		utilsMaya.buildUi_makeNiceBox( 'toto2' , nameFrameColumn , layoutWidth =  260  , casesHeight = 10 , caseCommands = cmdsStringC  , caseWidthPercent = [ 3 , 16 , 16 , 16 , 42 ]  )

		
	def setCoordsBoard( self ):
		

		for i in range( 0 , len( self.radioButtonsName) ):
			value = mc.radioButton( self.radioButtonsName[i] , q = True , sl = True )
			if( value == True ):
				self.curPlanCoords = self.planeCoordsChoice[i]
				break

		for i in range(  0 , len( self.uiCoords ) ): 
			mc.textField( self.uiCoords[i] , e = True , tx = self.curPlanCoords[i] )
		
		
	def getCoordsBoard( self ):
		
		self.curPlanCoords = []		
		for i in range(  0 , len( self.uiCoords ) ): 
			stringBValue = mc.textField( self.uiCoords[i] , q = True , tx = True )
			self.curPlanCoords.append( float( stringBValue ) )
			

	def resize(self):

		self.mainHeight = [ 177 , 266 ]
		
		colapse = mc.frameLayout( self.nameFrame , q = True , cl=True )
		
		
		if( colapse == 1 ):
			self.mainHeightIndex = 0
		else:
			self.mainHeightIndex = 1
			
		sizeH = self.mainHeight[self.mainHeightIndex]
		
		mc.window( self.win , e = True , h = sizeH )
		


	
	def UI_lockAxe( self , UIparent ):			

		
		label     = 'l = "Free"'
		
		lockXCmds  = self.variableNameInGlobal + '.lockButtonCmds(0)' 	
		lockYCmds  = self.variableNameInGlobal + '.lockButtonCmds(1)' 	
		lockZCmds  = self.variableNameInGlobal + '.lockButtonCmds(2)' 	
		
		cmdsStringC  = [ 'mc.text( l = "Axe:  " )' , 'mc.text( l = "X:" )' , 'mc.button( "{0}" , {1} , {2} , c = "{3}" )'.format( self.uiLockAxeButtonNames[0] , label , self.bgcOff , lockXCmds ) , 'mc.text( l = "Y:" )' , 'mc.button( "{0}" , {1} , {2}, c = "{3}" )'.format( self.uiLockAxeButtonNames[1] , label , self.bgcOff , lockYCmds ) , 'mc.text( l = "Z:" )' , 'mc.button( "{0}" , {1} , {2}, c = "{3}" )'.format( self.uiLockAxeButtonNames[2] , label , self.bgcOn , lockZCmds ) ]
		caseWide     = [ 17 ,  6 , 17 ,  6 , 17  ,  6 , 17  ]		
				
		utilsMaya.buildUi_makeNiceBox( 'toto111' , UIparent , layoutWidth =  280  , casesHeight = 10 , caseCommands = cmdsStringC  , caseWidthPercent = caseWide )		

	
	def lockButtonCmds( self , index ):
		
		self.lockAxe = index
		
		for i in range( 0 , 3 ):
			exec( 'mc.button( "{0}" , e = True , {1} )'.format( self.uiLockAxeButtonNames[i] , self.bgcOff ) )				
		exec( 'mc.button( "{0}" , e = True , {1} )'.format( self.uiLockAxeButtonNames[index] , self.bgcOn ) )	
		
		
	def UI_orient( self , UIparent ):			

		
		label     = 'l = "Inv"'
		
		invXCmds  = self.variableNameInGlobal + '.invButtonCmds(0)' 	
		invYCmds  = self.variableNameInGlobal + '.invButtonCmds(1)' 	
		invZCmds  = self.variableNameInGlobal + '.invButtonCmds(2)' 	
		
		cmdsStringC  = [ 'mc.text( l = "ORIENT:  " )' , 'mc.text( l = "X:" )' , 'mc.button( "{0}" , {1} , {2} , c = "{3}" )'.format( self.uiInvertButtonNames[0] , label , self.bgcOff , invXCmds ) , 'mc.text( l = "Y:" )' , 'mc.button( "{0}" , {1} , {2}, c = "{3}" )'.format( self.uiInvertButtonNames[1] , label , self.bgcOff , invYCmds ) , 'mc.text( l = "Z:" )' , 'mc.button( "{0}" , {1} , {2}, c = "{3}" )'.format( self.uiInvertButtonNames[2] , label , self.bgcOff , invZCmds ) ]
		caseWide     = [ 17 ,  6 , 17 ,  6 , 17  ,  6 , 17  ]		
				
		utilsMaya.buildUi_makeNiceBox( 'toto10' , UIparent , layoutWidth =  280  , casesHeight = 10 , caseCommands = cmdsStringC  , caseWidthPercent = caseWide )		

	
		
	def invButtonCmds( self , index ):
		
		self.invertAxes[index] = abs( self.invertAxes[index] - 1 )
		
		for i in range( 0 , len(self.invertAxes) ):

			if( self.invertAxes[i] == 1 ):
				exec( 'mc.button( "{0}" , e = True , {1} )'.format( self.uiInvertButtonNames[i] , self.bgcOn ) )
			else:
				exec( 'mc.button( "{0}" , e = True , {1} )'.format( self.uiInvertButtonNames[i] , self.bgcOff ) )				
		


				
				
				
				
	def UI_name( self , UIparent ):	
		
		bgc = 'bgc = [ 0.2 , 0.2 , 0.2 ]'		
		
		cmdsStringA  = [ 'mc.text( l = "PREFIX:  " )' , 'mc.textField("{0}" , tx = "{1}" , {2} )'.format( self.prefixName[0]  , self.prefix[0]  , bgc ) ,  'mc.text( l = " -------> " )' , 'mc.textField( "{0}" , tx = "{1}" , {2} )'.format( self.prefixName[1]  , self.prefix[1]  , bgc ) ]
		cmdsStringB  = [ 'mc.text( l = "REPLACE: " )' , 'mc.textField("{0}" , tx = "{1}" , {2} )'.format( self.replaceName[0] , self.replace[0] , bgc ) ,  'mc.text( l = " -------> " )' , 'mc.textField( "{0}" , tx = "{1}" , {2} )'.format( self.replaceName[1] , self.replace[1] , bgc ) ]	
				
		utilsMaya.buildUi_makeNiceBox( 'toto11' , UIparent , layoutWidth =  280  , casesHeight = 10 , caseCommands = cmdsStringA  , caseWidthPercent = [19,25,20,25] )		
		utilsMaya.buildUi_makeNiceBox( 'toto12' , UIparent , layoutWidth =  280  , casesHeight = 10 , caseCommands = cmdsStringB  , caseWidthPercent = [19,25,20,25] )	

	def getNameAddReplace(self):

		
		for i in range( 0 , 2 ):
			self.prefix[i] = mc.textField( self.prefixName[i] , q = True , tx = True ) 
			self.replace[i] = mc.textField( self.replaceName[i] , q = True , tx = True ) 			

			
			
			
			
			
			
			
			
			
	#_____________________________________________________________________________________________________________________________________________ showPlan				
	def showPlan( self ):
		
		self.getCoordsBoard()
		
		coords = [ self.curPlanCoords[0:3] , self.curPlanCoords[3:6] , self.curPlanCoords[6:9] ] 
		
		# get trs
		position = utilsMath.getBBbarycentre( self.curPlanCoords )
		vUp      = [  coords[2][0] - coords[1][0] , coords[2][1] - coords[1][1] , coords[2][2] - coords[1][2]  ]
		rotation = utilsMayaApi.API_convert2CoordsToEulerOrient( coords[0] , coords[1] , vUp )
		scale        = [ 100 , 100 , 100 ]			

		trs =  position + rotation + scale 
		
		
		# build plane
		symPlaneName = 'mirrorManip_symPlane_msh'
		
		if( mc.objExists( symPlaneName ) ):
			mc.delete( symPlaneName )
			
		mc.polyPlane( n = symPlaneName )
		mc.setAttr( symPlaneName + '.rx' , 90 )
		mc.makeIdentity( symPlaneName , r = True , a = True)		
		utilsMaya.setTRSValueToObj( symPlaneName , trs )

		print(  'create mesh representing plan of coords :' , self.curPlanCoords)		
		return 1
			


	
	#_____________________________________________________________________________________________________________________________________________ getSelectedPlanCoords	
	def getSelectedPlanCoords( self ):
		mc.radioButton( self.radioButtonsName[3] , e = True , sl = True )
		
		selection = mc.ls(sl = True )
		
		# from selection get 3 coords plan
		
		selectionComponent = []
		
		
		# if poly get all coord, else append component
		for elem in selection:
			if not( '.' in elem ):
				coords = utilsMayaApi.API_getAllVertexCoords( elem )
				planCoords = coords[0] + coords[1] + coords[2]  
			else:
				selectionComponent.append(elem)
				
		# if componnent get coords	
		if( len( selectionComponent ) > 0  ):		
			selectionVtx = utilsMaya.convertFaceEdgeTovtx( selectionComponent )
			dicoVtx      = utilsPython.getDictIndexsOfObjs( selectionVtx )	
					
			poly    =  dicoVtx.keys()[0]
			        
			indexA  = dicoVtx[ poly ][0]
			indexB  = dicoVtx[ poly ][1]
			indexC  = dicoVtx[ poly ][2]
			        
			coordsA = mc.xform(  '{0}.vtx[{1}]'.format( poly , indexA ) , q = True , t = True , ws = True )
			coordsB = mc.xform(  '{0}.vtx[{1}]'.format( poly , indexB ) , q = True , t = True , ws = True )
			coordsC = mc.xform(  '{0}.vtx[{1}]'.format( poly , indexC ) , q = True , t = True , ws = True )
			
			planCoords = coordsA + coordsB + coordsC  
		
			
		# set 3 coords plan / update ui				
		self.planeCoordsChoice[3] = planCoords 		
		self.setCoordsBoard()		
		print('get plane coords ')
		
		
	#_____________________________________________________________________________________________________________________________________________ getSymPlanCoords				
	def getSymPlanCoords(self):
		
		
		selection = mc.ls(sl=True)
		
		# selection must be 2 faces
		
		if( len(selection) == 2 ) and ( '.f[' in selection[0] ) and ( '.f[' in selection[1] ):
			
			obj    = selection[0].split('.')[0]
			indexs = [ selection[0].split('[')[1].split(']')[0] , selection[1].split('[')[1].split(']')[0] ]
			
		elif( len(selection) == 1 ) and ( '.f[' in selection[0] ) and ( ':' in selection[0] ):
			
			obj          = selection[0].split('.')[0]
			indexsString = selection[0].split('[')[1].split(']')[0].split(':')			
			indexs       = [ int(indexsString[0]) , int(indexsString[1])  ]
			
			if not( indexs[0] + 1 == indexs[1]):
				mc.error( ' you must select only 2 faces ')						
		else:
			mc.error( ' you must select only 2 faces ')
			
		
		
		# sort face vtx in 3 paire of vtx
		
		vtxARaw    = utilsMaya.convertFaceEdgeTovtx(   [ '{0}.f[{1}]'.format( obj , indexs[0] ) ]   )		
		vtxAindexs = utilsPython.getArrayIndexsOfObjs( vtxARaw  )
		
		vtxA = []
		for i in vtxAindexs:
			vtxA.append( '{0}.vtx[{1}]'.format( obj , i )  )
		
		vtxBRaw    = utilsMaya.convertFaceEdgeTovtx(   [ '{0}.f[{1}]'.format( obj , indexs[1] ) ]   )
		vtxBindexs = utilsPython.getArrayIndexsOfObjs( vtxBRaw  )
		
		vtxB = []
		for i in vtxBindexs:
			vtxB.append( '{0}.vtx[{1}]'.format( obj , i )  )
			
			
			
		vtxCouples = []
		
		loop = 0
		
		while( len(vtxCouples) < 3 ):
			
			distances = []
			dico = {}

			
			for vA in vtxA:
				for vB in vtxB:
					coordsA  = mc.xform( vA , q = True , t = True , ws = True )
					coordsB  = mc.xform( vB , q = True , t = True , ws = True )
					distance = ompy.MVector( ( coordsA[0] - coordsB[0] ) , ( coordsA[1] - coordsB[1] ) , ( coordsA[2] - coordsB[2] ) ).length()
					distances.append(distance)
					
					dico[str(distance)] = vA + '/' + vB
					
			distances.sort()
			
			vtxCoupleCurent = dico[ str(distances[0] ) ].split('/')
			vtxA.remove(vtxCoupleCurent[0])
			vtxB.remove(vtxCoupleCurent[1])					
						
			vtxCouples.append(vtxCoupleCurent)
			
			loop += 1
			
			if( 400 < loop ):
				mc.error('loop')

		
		#find the middle of this pair
		
		middleCoords = []
		
		for couple in vtxCouples:
			coordsA  = mc.xform( couple[0] , q = True , t = True , ws = True )
			coordsB  = mc.xform( couple[1] , q = True , t = True , ws = True )

			middleCoords += [ ( coordsA[0] + coordsB[0] )/2 , ( coordsA[1] + coordsB[1] )/2 , ( coordsA[2] + coordsB[2] )/2 ]  		
			
			
			
		# ui 
		mc.radioButton( self.radioButtonsName[3] , e = True , sl = True )	
		print( ' get sym  plan coords  ' )
		self.planeCoordsChoice[3] = middleCoords 		
		self.setCoordsBoard()

		return middleCoords		
		

	#_____________________________________________________________________________________________________________________________________________ duplicateRig	
	def duplicateRig( self ):
		
		selection = mc.ls(sl=True)
		
		# PREPARATION
		count = 0
		for elem in self.invertAxes:
			if( elem == 1 ):
				count += 1

		if( count == 1 ) or ( count == 3 ):
			mc.error( " you can have only two axe INV " )
			
			
		self.getNameAddReplace()
		self.getCoordsBoard()
		
		planeCoords = [ self.curPlanCoords[0:3] , self.curPlanCoords[3:6] , self.curPlanCoords[6:9] ] 

		
		
		# DUPLICATE RIG
					
		rigObj      = None				

		fathers = []
		manips  = []
		
		for elem in selection:

			for rigType in self.dico_rigType_classBuild.keys():	
				
				exec( '{0}'.format(          self.dico_rigType_classImport[ rigType ]  ) )			
				exec( 'rigObj = {0}'.format( self.dico_rigType_classBuild[  rigType ]  ) )
				
				if( rigObj.isElem( elem ) ):		
				
					if(  rigType == 'manip' ):
						rigObj.fillAttrFromRig( elem )						
						manips.append(elem) 
						fathers.append( rigObj.father ) 						
					else:						
						rigObj.fillAttrFromRig( elem )
						rigObj.createMirror( planeCoords , self.lockAxe , self.invertAxes ,  self.prefix , self.replace  )	
		
						
						
		# MANIP HIERARCHY EXCEPTTION

		indexList = utilsPython.sortIndexChildrensByHierarchy( manips , fathers )
		indexList.reverse()

		for i in indexList:
			manipObj = buildRigClassManip.manip()
			manipObj.fillAttrFromRig(manips[i])
			manipObj.createMirror( planeCoords , self.lockAxe , self.invertAxes , self.prefix , self.replace , replaceInHierarchy = 1 )					
					
	
	

		
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
		
		mc.text( l = '' , h = 1  , p = mainColumName)
		
		self.UI_plan(mainColumName)	
		self.UI_lockAxe( mainColumName)
		self.UI_orient(mainColumName)	
		self.UI_name(mainColumName)	
		
		
		dupliManipCmds  = self.variableNameInGlobal + '.duplicateRig()' 
		
		mc.button( l = 'DUPLICATE MANIP' , bgc = [ 0.5 , 0.3 , 0.3 ] , p = mainColumName , c = dupliManipCmds )
		mc.text( l = '' , h = 10 , p = mainColumName)
		
			
		
				
		mc.showWindow( self.win )
	
	
