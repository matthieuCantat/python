


'''

pythonFilePath = 'D:/mcantat_BDD/projects/code/maya/' 

import sys
sys.path.append( pythonFilePath )

import python
from python.classe.uiPuppetCtrlCurve import *
reload(python.classe.uiPuppetCtrlCurve)

reload(python.classe.uiPuppetCtrlCurve)
reload(python.utils.utilsRigPuppet)
reload(python.classe.curveShape)
reload(python.classe.coords)
reload(python.classe.trsBackUp)


uiPuppetCtrlCurveVar = uiPuppetCtrlCurve()
uiPuppetCtrlCurveVar.build()






'''

import sys	
import maya.cmds as mc	
import maya.mel as mel

from ..utils import utilsBin
from ..utils import utilsPython

from ..utils.utilsRigPuppet import *
from .curveShape import *
from .animCurve import *
import python.classe.readWriteInfo as rwi
import python.classe.skinCluster as sCluster
import python.script.alignBetween2Vertices as alignBetween2Vertices
import python.script.setCustomAxisOrientation as setCustomAxisOrientation




global uiPuppetCtrlCurveVar

def uiPuppetCtrlCurve_launch(): 
	print('LAUNCHING UI...')
	print('global uiPuppetCtrlCurveVar')
	print('uiPuppetCtrlCurveVar = uiPuppetCtrlCurve()')
	print('uiPuppetCtrlCurveVar.build()')
	print(' ')
	exec('global uiPuppetCtrlCurveVar')	
	exec('uiPuppetCtrlCurveVar = uiPuppetCtrlCurve()') in globals()
	exec('uiPuppetCtrlCurveVar.build()'              ) in globals() 


class uiPuppetCtrlCurve():

	
	#______________________________________________________________________________________________________________________________________________________________________   INIT
	
	def __init__(self):	
		
		self.globalPath   =  utilsPython.getActualPath()	
		pathSplitTmp      = self.globalPath.split('/' )
		self.toolBoxPath  = '/'.join( pathSplitTmp[0: len(pathSplitTmp) - 2 ] ) + '/'		
		
		self.variableNameInGlobal = 'uiPuppetCtrlCurveVar'
		self.cbModifDupli = 'checkBoxModifyDuplicate'	
		self.cbUpdateInWS = 'checkBoxWSupdate'

		self.btnDupliInfo  = 'btnDupliInfo'

		self.cbConstraintDuplicates = 'cbConstraintDuplicates'
		self.cbConstraintConvert = 'cbConstraintConvert'
		self.cbConstraint2by2 = 'cbConstraint2by2'
		self.cbConstraintPoint = 'cbConstraintPoint'
		self.cbConstraintRotate = 'cbConstraintRotate'
		self.cbConstraintScale = 'cbConstraintScale'

		self.cbAnimLoadMatchSelection = 'cbAnimLoadMatchSelection'
		self.cbAnimLoadOnSelection    = 'cbAnimLoadOnSelection'
		self.cbAnimOffsetCurrentFrame = 'cbAnimOffsetCurrentFrame'
		self.cbAnimOffsetEndFrame     = 'cbAnimOffsetEndFrame'
		self.cbAnimReplaceCurrent     = 'cbAnimReplaceCurrent'
		self.cbAnimInverse            = 'cbAnimInverse'
		self.cbAnimMirror             = 'cbAnimMirror'
		self.cbAnimLoadMatchSelection = 'cbAnimLoadMatchSelection'       	
		self.cbAnimLoadMatchNamespace = 'cbAnimLoadMatchNamespace' 
		self.rcAnimCurveReleaseOption = 'rcAnimCurveReleaseOption' 

		self.cbFileShowLatest         = 'cbShowLatest'
		self.omFileNames              = 'omFileNames'
		self.ftAnimPath               = 'ftAnimPath'
		self.ftAnimInfo               = 'ftAnimInfo'

		self.cbRigPuppetsOptimize = 'cbRigPuppetsOptimize'

		self.omSpaceSwitch            = 'omSpaceSwitch'
		self.btnSpaceSwitch			  = 'btnSpaceSwitch'
		self.isgSpacetransFrame	      = 'isgSpacetransFrame'
		self.spaceSwitchDictInfo      = {}

		self.btnIKFKSwitch     = 'omIKFKSwitch'
		self.isgIKFKtransFrame = 'isgIKFKtransFrame'
		self.IKFKdictArmInfo = {}
		self.IKFKvalue       = 0


		self.baseName           = None
		self.orient             = None
		self.pivotButtonValue   = 0  		
		self.shapeForm          = 'loc'
		self.shapeAxe           = 1 
		self.indexColor         = 13
		self.manipOptions       = [ 'position' , 'orient' , 'scale' , 'joint' , 'visibility' , 'constraint' , 'root' , 'animSet' ]		
		self.optionChoice       = [ 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1  ]  

		self.animCurvefiles = [ 'toto' ]
		self.animCurvePath = 'D:/mcantat_BDD/projects/cute/carrierShipD/maya/scenes/animCurves/'

		self.CurveShape = curveShape()	
		self.AnimCurve = animCurve()
		self.rwi = rwi.readWriteInfo()	

		self.dupliDictCtrls      = {} 
		self.dupliDictModels     = {}
		self.dupliDictJoints     = {}
		self.dupliDictCtrlJoints = {}


	
	def build(self):
	
		win  = 'uiPuppetCtrlCurveWindow'
		mCol = 'mainColumn'

		if( mc.windowPref( win , ex = True ) ):
			mc.windowPref( win , e = True , w = 280 , h = 200 )
		
		if( mc.window( win , ex = True ) ):
			mc.deleteUI( win , wnd = True )
		
		mc.window( win , w = 280 , h = 200 , s = True ) 
	
		mc.columnLayout(    mCol , bgc = [ 0.27 , 0.27 , 0.27 ] , columnAttach = [ 'both' , 10 ] , rowSpacing = 0 , columnWidth = 280  )
		mc.text(        p = mCol , l = '' , h = 1  )
		mc.button(      p = mCol , l = 'SET PROJECT WORKSPACE' , bgc = [ 0.5 , 0.3 , 0.3 ] , c = '{}.cmds_setProjectWorkSpace()'.format(self.variableNameInGlobal) )			
		mc.text(        p = mCol , l = '' , h = 5  )
		mc.button(self.btnDupliInfo ,  p = mCol , l = 'GET SELECTED RIG DUPLI INFO' , bgc = [ 0.3 , 0.3 , 0.3 ] , c = '{}.cmds_getSelectedRigDupliInfo()'.format(self.variableNameInGlobal) )		
		self.UI_manipShape( mCol )
		self.UI_model(      mCol )
		self.UI_puppetOuts( mCol )
		self.UI_constraint( mCol )
		self.UI_skin(       mCol )
		self.UI_animCurve(  mCol )
		self.UI_rigPuppets( mCol )
		self.UI_switch(     mCol )
		self.UI_IKFK(       mCol )
		mc.text(        p = mCol , l = '' , h = 30  )
		mc.button(      p = mCol , l = 'DO PLAYBLAST' , bgc = [ 0.5 , 0.3 , 0.3 ] , c = '{}.cmds_doPlayblast()'.format(self.variableNameInGlobal) )		
		mc.text(        p = mCol , l = '' , h = 1  )
		mc.showWindow( win )

		self.cmds_animCurvePathUpdateWithCurrent()
	




	def cmds_getSelectedRigDupliInfo(self):
		selection    = mc.ls(sl = True)[0]
		if( len(selection) == 0 ): print('getSelectedRigDupliInfo WORK ONLY WITH SELECTION')
		namespace    = None
		namespaceStr = ''
		if( ':' in selection ):
			namespace    = selection.split(':')[0]
			namespaceStr = namespace + ':'

		ctrls = mc.ls( "{}*_CTRL".format(namespaceStr) )
		geos  = mc.ls( "{}*_GEO".format( namespaceStr) )
		jnts  = mc.ls( "{}*_JNT".format( namespaceStr) )

		self.dupliDictCtrls      = {} 
		self.dupliDictModels     = {}
		self.dupliDictJoints     = {}
		self.dupliDictCtrlJoints = {}
		if( 0 < len(ctrls) ): self.dupliDictCtrls      = getDupliDictCtrls(      namespace = namespace )             
		if( 0 < len(geos)  ): self.dupliDictModels     = getDupliDictModels(     namespace = namespace )
		if( 0 < len(jnts)  ): self.dupliDictJoints     = getDupliDictJoints(     namespace = namespace )
		if( 0 < len(ctrls) ): self.dupliDictCtrlJoints = getDupliDictCtrlJoints( namespace = namespace )

		#UPDATE UI
		mc.button( self.btnDupliInfo , e = True , l = '{} DUPLI INFO STORED'.format(namespaceStr) , bgc = [ 0.3 , 0.5 , 0.3 ] )    



	def cmds_setProjectWorkSpace(self):
		pipe_setProjectWorkSpace('cute')


	def cmds_doPlayblast(self):
		playblast_save()


	def cmds_constraint(self):
		selection              = mc.ls(sl = True )
		doConstraintDuplicates = mc.checkBox( self.cbConstraintDuplicates , q = True , v = True )
		doConvertToOutJoints   = mc.checkBox( self.cbConstraintConvert , q = True , v = True )
		constaint2by2          = mc.checkBox( self.cbConstraint2by2 , q = True , v = True )
		doTranslate            = mc.checkBox( self.cbConstraintPoint , q = True , v = True )
		doRotation             = mc.checkBox( self.cbConstraintRotate , q = True , v = True )
		doScale                = mc.checkBox( self.cbConstraintScale , q = True , v = True )
				
		#CONVERT TO 2by2						
		masters = []
		slaves  = []
		if(constaint2by2):
			for i in range(0,len(selection),2):
				masters.append(selection[i])
				slaves.append(selection[i+1])
		else:
			for i in range(1,len(selection)):
				masters.append(selection[0])
				slaves.append(selection[i])

		#CONVERT
		mastersConverted = masters
		if( doConvertToOutJoints ):
			for i in range(0,len(masters)):
				mastersConverted[i] = objsRelationShip_getOthers( self.dupliDictCtrlJoints , [masters[i]] , 0 )[0]

		#CONSTRAINT
		print('CONTRAINT')
		for i in range(0,len(masters)):
			mc.parentConstraint( mastersConverted[i] , slaves[i] , mo = True )
			mc.scaleConstraint(  mastersConverted[i] , slaves[i] , mo = True )

		#CONTRAINT DUPLICATE
		print('CONTRAINT DUPLICATE')
		if( doConstraintDuplicates ):
			for i in range( 0 , len(masters) ):

				dictSimilar     = objsRelationShip_getSimilar( [self.dupliDictJoints , self.dupliDictCtrls , self.dupliDictModels] , [mastersConverted[i] , slaves[i] ] , 0 )
				dictDupliSlaves = objsRelationShip_getSimilar( [self.dupliDictModels] , [ slaves[i] ] , 0 )

				if not( dictSimilar == dictDupliSlaves ):
					# master dupli ---> slave dupli

					for key in dictSimilar.keys():
						if( len(dictSimilar[key]) < 2 ): continue
						mastersDupli = dictSimilar[key][0]
						slavesDupli  = dictSimilar[key][1]
	
						mc.parentConstraint( mastersDupli , slavesDupli , mo = True )
						mc.scaleConstraint(  mastersDupli , slavesDupli , mo = True )

				else:
					# master ---> slaves dupli 
					for key in dictDupliSlaves.keys():
						for slave in dictDupliSlaves[key]:

							mc.parentConstraint( mastersConverted[i] , slave , mo = True )
							mc.scaleConstraint(  mastersConverted[i] , slave , mo = True )
		print('DONE')

	def cmds_updateDuplicateCtrls(self):
		selection    = mc.ls(sl = True )
		localSpace = mc.checkBox( self.cbUpdateInWS , q = True , v = True )

		if( localSpace ):
			for elem in selection:
				objs = objsRelationShip_getOthers( self.dupliDictCtrls , [elem] , addSource = False  )
				for obj in objs:
					self.CurveShape.transferCoords( obj , elem , worldSpace = 0 )
		else:
			for elem in selection:
				objs = objsRelationShip_getOthers( self.dupliDictCtrls , [elem] , addSource = False  )
				for obj in objs:
					ctrlRelationShip_copyCtrlCoords( self.dupliDictCtrls  , obj , elem )	

		mc.select( selection )


	def cmds_updateLineWidthDuplicateCtrls(self , curveWidth = 3):
		selection    = mc.ls(sl = True )
		localSpace = mc.checkBox( self.cbUpdateInWS , q = True , v = True )

		for elem in selection:
			objs = objsRelationShip_getOthers( self.dupliDictCtrls , [elem] , addSource = True  )
			setCurveLineWidth( objs , value = curveWidth )


	def cmds_selectDuplicateCtrls(self):
		print(' ---- select dupli ctrls ----')
		objsRelationShip_selectOthers(self.dupliDictCtrls)

	def cmds_selectDuplicateModels(self):
		print(' ---- select dupli models ----')
		objsRelationShip_selectOthers(self.dupliDictModels)

	def cmds_selectDuplicateJoints(self):
		print(' ---- select dupli joints ----')
		objsRelationShip_selectOthers(self.dupliDictJoints)

	def cmds_selectDuplicateCtrlsJoints(self):
		print(' ---- select bind element ----')
		objsRelationShip_selectOthers(self.dupliDictCtrlJoints)




	#=========================================================================================================================================================================================		   		                  
	#======================================================================================================================================================================  UI manip Shape
	#=========================================================================================================================================================================================	

	def UI_constraint( self, UIparent ):
		
		panels =  [ 'constraintUI_manipShape' , 'constraintUI_colomn' ]	
		
		mc.frameLayout( panels[0]  , li = 80 ,  cl = 1 , cll = 1 ,  w = 262 ,  bgc = [ 0.23 , 0.23 , 0.24 ]  ,   label = 'CONSTRAINTS' , p = UIparent )
		
		mc.columnLayout( panels[1] , p = panels[0] , bgc = [ 0.27 , 0.27 , 0.27 ]  , columnAttach = [ 'both' , 10 ] , rowSpacing = 0 , columnWidth = 280  )

		mc.text(        p = panels[1] , l = '' , h = 5  )		
		mc.button(      p = panels[1] , l = 'CONSTRAINT' , bgc = [ 0.5 , 0.3 , 0.3 ] , c = '{}.cmds_constraint()'.format(self.variableNameInGlobal) )		
		mc.text(        p = panels[1] , l = '' , h = 5  )		
		mc.checkBox( self.cbConstraintDuplicates , p = panels[1] , l = 'MODIFY DUPLICATES' , v = 1  )
		mc.text(        p = panels[1] , l = '' , h = 5  )
		mc.checkBox( self.cbConstraintConvert , p = panels[1] , l = 'CONVERT CTRL TO OUT' , v = 1  )	
		mc.text(        p = panels[1] , l = '' , h = 5  )
		mc.checkBox( self.cbConstraint2by2 , p = panels[1] , l = '2BY2' , v = 1  )	
		mc.text(        p = panels[1] , l = '' , h = 5  )
		mc.checkBox( self.cbConstraintPoint , p = panels[1] , l = 'POINT' , v = 1  )	
		mc.text(        p = panels[1] , l = '' , h = 5  )
		mc.checkBox( self.cbConstraintRotate , p = panels[1] , l = 'ROTATE' , v = 1  )	
		mc.text(        p = panels[1] , l = '' , h = 5  )
		mc.checkBox( self.cbConstraintScale , p = panels[1] , l = 'SCALE' , v = 1  )								
		mc.text(        p = panels[1] , l = '' , h = 10 )
		

	def UI_skin( self, UIparent ):
		
		panels =  [ 'skinUI_manipShape' , 'skinUI_colomn' ]	
		
		mc.frameLayout( panels[0]  , li = 80 ,  cl = 1 , cll = 1 ,  w = 262 ,  bgc = [ 0.23 , 0.23 , 0.24 ]  ,   label = 'SKIN' , p = UIparent )
		
		mc.columnLayout( panels[1] , p = panels[0] , bgc = [ 0.27 , 0.27 , 0.27 ]  , columnAttach = [ 'both' , 10 ] , rowSpacing = 0 , columnWidth = 280  )

		mc.text(        p = panels[1] , l = '' , h = 5  )		
		mc.button(      p = panels[1] , l = 'copy to duplicate' , bgc = [ 0.5 , 0.3 , 0.3 ] , c = '{}.cmds_skinCopyToDuplicate()'.format(self.variableNameInGlobal) )		
		mc.text(        p = panels[1] , l = '' , h = 5  )	
		mc.button( l = 'REPEAT FLOOD 500'  ,  bgc = [ 0.35 , 0.35 , 0.35 ] , c = '{}.cmds_repeatFlood500()'.format(self.variableNameInGlobal) )	
		mc.text(        p = panels[1] , l = '' , h = 5  )	
		


	def UI_puppetOuts( self, UIparent ):
		
		panels =  [ 'rigPuppetOutsUI_manipShape' , 'rigPuppetOutsUI_colomn' ]	
		
		mc.frameLayout( panels[0]  , li = 80 ,  cl = 1 , cll = 1 ,  w = 262 ,  bgc = [ 0.23 , 0.23 , 0.24 ]  ,   label = 'OUTS' , p = UIparent )
		
		mc.columnLayout( panels[1] , p = panels[0] , bgc = [ 0.27 , 0.27 , 0.27 ]  , columnAttach = [ 'both' , 10 ] , rowSpacing = 0 , columnWidth = 280  )

		mc.text(        p = panels[1] , l = '' , h = 5  )		
		mc.button(      p = panels[1] , l = 'CTRL TO OUTS' , bgc = [ 0.5 , 0.3 , 0.3 ] , c = '{}.cmds_selectDuplicateCtrlsJoints()'.format(self.variableNameInGlobal) )		
		mc.text(        p = panels[1] , l = '' , h = 5  )		
		mc.button(      p = panels[1] , l = 'SELECT DUPLICATES OUTS' , bgc = [ 0.5 , 0.3 , 0.3 ] , c = '{}.cmds_selectDuplicateJoints()'.format(self.variableNameInGlobal) )
		mc.text(        p = panels[1] , l = '' , h = 5  )
		

	def UI_model( self, UIparent ):
		
		panels =  [ 'modeUI_manipShape' , 'modeUI_colomn' ]	
		
		mc.frameLayout( panels[0]  , li = 80 ,  cl = 1 , cll = 1 ,  w = 262 ,  bgc = [ 0.23 , 0.23 , 0.24 ]  ,   label = 'MODEL' , p = UIparent )
		
		mc.columnLayout( panels[1] , p = panels[0] , bgc = [ 0.27 , 0.27 , 0.27 ]  , columnAttach = [ 'both' , 10 ] , rowSpacing = 0 , columnWidth = 280  )

		mc.text(        p = panels[1] , l = '' , h = 5  )		
		mc.button(      p = panels[1] , l = 'SELECT DUPLICATES MODEL' , bgc = [ 0.5 , 0.3 , 0.3 ] , c = '{}.cmds_selectDuplicateModels()'.format(self.variableNameInGlobal) )		
		mc.text(        p = panels[1] , l = '' , h = 5  )		
		mc.button(      p = panels[1] , l = 'UPDATE DUPLICATES MODEL' , bgc = [ 0.5 , 0.3 , 0.3 ] , c = '{}.cmds_selectDuplicateModels()'.format(self.variableNameInGlobal) )
		mc.text(        p = panels[1] , l = '' , h = 20  )
		mc.button(      p = panels[1] , l = 'ALIGN BETWEEN 2 VERTICES' , bgc = [ 0.5 , 0.3 , 0.3 ] , c = 'alignBetween2Vertices.alignBetween2Vertices()'.format(self.variableNameInGlobal) )
		mc.text(        p = panels[1] , l = '' , h = 5  )		
		mc.button(      p = panels[1] , l = 'ORIENT MANIPUlATOR PIVOT' , bgc = [ 0.5 , 0.3 , 0.3 ] , c = 'setCustomAxisOrientation.setCustomAxisOrientation()'.format(self.variableNameInGlobal) )
		mc.text(        p = panels[1] , l = '' , h = 5  )	

	def UI_manipShape( self, UIparent ):
		
		panels =  [ 'bmUI_manipShape' , 'bmUI_manipShapeForm' , 'bmUI_manipShapeAxe' ,  'bmUI_manipShapeColor' ,  'bmUI_colomn' ]	
		
		mc.frameLayout( panels[0]  , li = 80 , cl = 1 ,  cll = 1 ,  w = 262 ,  bgc = [ 0.23 , 0.23 , 0.24 ]  ,   label = 'CTRL SHAPE' , p = UIparent )
		
		mc.columnLayout( panels[4] , p = panels[0] , bgc = [ 0.27 , 0.27 , 0.27 ]  , columnAttach = [ 'both' , 10 ] , rowSpacing = 0 , columnWidth = 280  )
		mc.text(  p = panels[4] , l = '' , h = 1  )

		form = mc.formLayout( p = panels[4] , numberOfDivisions = 100 ,  bgc = [ 0.27 , 0.27 , 0.27 ]  ) 
		self.UI_manipShape_form(  panels[1]  , form )
		self.UI_manipShape_colorSorted(  panels[2] , form )			
		self.UI_manipShape_color( panels[3]  , form )  	
		mc.formLayout( form , e = True ,  af =[  ( panels[1] , 'top'    , 5  ) , ( panels[1] , 'left'   , 0   )   ]   , ac = [ ]                                                )  # manipShapeForm                   			                          
		mc.formLayout( form , e = True ,  af =[  ( panels[2] , 'left'   , 0   )   ]                                   , ac = [  ( panels[2] , 'top'   ,  5   ,  panels[1] )   ]                                               )  # manipShapeForm  
		mc.formLayout( form , e = True ,  af =[  ( panels[3] , 'left'   , 0  ) ,( panels[3] , 'bottom'   , 10 )    ]   , ac = [  ( panels[3] , 'top'   ,  5   ,  panels[2] )   ] )  # manipShapeColor 	                                          

		mc.text(        p = panels[4] , l = '' , h = 5  )
		mc.checkBox( self.cbModifDupli , p = panels[4] , l = 'MODIFY DUPLICATES' , v = 1  )
		mc.text(        p = panels[4] , l = '' , h = 5  )		
		mc.button(      p = panels[4] , l = 'SELECT DUPLICATES SHAPE' , bgc = [ 0.5 , 0.3 , 0.3 ] , c = '{}.cmds_selectDuplicateCtrls()'.format(self.variableNameInGlobal) )		
		mc.text(        p = panels[4] , l = '' , h = 5  )		
		mc.button(      p = panels[4] , l = 'UPDATE DUPLICATES SHAPE' , bgc = [ 0.5 , 0.3 , 0.3 ] , c = '{}.cmds_updateDuplicateCtrls()'.format(self.variableNameInGlobal) )
		mc.text(        p = panels[4] , l = '' , h = 5  )
		mc.checkBox( self.cbUpdateInWS , p = panels[4] , l = 'in local Space' , v = 0  )	
		mc.text(        p = panels[4] , l = '' , h = 5 )
		mc.button(      p = panels[4] , l = 'CURVE LINE 3' , bgc = [ 0.5 , 0.3 , 0.3 ] , c = '{}.cmds_updateLineWidthDuplicateCtrls( 3 )'.format(self.variableNameInGlobal) )
		mc.text(        p = panels[4] , l = '' , h = 10  )



	def cmds_animCurveRelease(self):
		print('cmds_animCurveRelease')
		#GET RELEASE OPTION 
		rcSelected = mc.radioCollection( self.rcAnimCurveReleaseOption , q = True , select = True )
		rcChoices  = mc.radioCollection( self.rcAnimCurveReleaseOption , q = True , collectionItemArray = True )
		rcChoice = 0 
		for i in range(0,len(rcChoices)):
		    if( rcSelected in rcChoices[i] ):
		        rcChoice = i 
		        break      

		path = mc.textField(  self.ftAnimPath  , q = True , tx = True )   
		file = mc.optionMenu( self.omFileNames , q = True , v = True )  
		namespace = None		
		#CREATE
		if(   rcChoice == 0 ):
			#ALL
			self.AnimCurve.createFromObjs( mc.ls( '*_CTRL' , r = True , type = 'transform' ) )
		elif( rcChoice == 1 ):
			#RIG
			selection = mc.ls(sl = True)[0]
			namespace = selection.split(':')[0]
			self.AnimCurve.createFromObjs( mc.ls( '{}:*_CTRL'.format(namespace) , r = True , type = 'transform' ) )	
		else:
			#SELECTION
			self.AnimCurve.createFromObjs( mc.ls( '*_CTRL' , sl = True , r = True , type = 'transform' ) )


		outFile = file

		#PROMPT SET FILE NAME
		result = mc.promptDialog(
		                title='SAVE ANIM',
		                message='Enter File Name:',
		                text = file,
		                button=['OK', 'Cancel'],
		                defaultButton='OK',
		                cancelButton='Cancel',
		                dismissString='Cancel')
		
		if( result == 'OK'):
			outFile = mc.promptDialog(query=True, text=True)

		#PROMPT SET RIG NAMESPACE
		namesSpacePrefix = None
		if not( file == outFile) and not( namespace == None ):
			result = mc.promptDialog(
			                title='SAVE ANIM',
			                message='add the rig namespace as prefix:',
			                text = namespace,
			                button=['OK', 'Cancel'],
			                defaultButton='OK',
			                cancelButton='Cancel',
			                dismissString='Cancel')
			
			if( result == 'OK'):
				namesSpacePrefix = mc.promptDialog(query=True, text=True)

		if not( namesSpacePrefix == None ):
			outFile = '{}_{}'.format(namesSpacePrefix,outFile)

		#PROMPT ADD INFO
		minRange = int(mc.playbackOptions( q = True , min = True ))
		maxRange = int(mc.playbackOptions( q = True , max = True ))
		desciption = '{} - {} : None'.format(minRange,maxRange)

		result = mc.promptDialog(
		                title='RELEASE INFO',
		                message='Comment:',
		                text = desciption,
		                button=['OK', 'Cancel'],
		                defaultButton='OK',
		                cancelButton='Cancel',
		                dismissString='Cancel')
		
		if result == 'OK':
		    animInfo = mc.promptDialog(query=True, text=True)

		#REMOVE SUFFIX 
		suffix = '_v'
		if( suffix in outFile ): outFile = outFile.split(suffix)[0]
		#ADD .XML
		if not( '.' in outFile ): outFile = outFile + '.xml'

		path = self.animCurvePath +'/'+ outFile
		self.AnimCurve.toFile( path , info = animInfo )
		return 1


	def cmds_animCurveGather(self):
		print('cmds_animCurveGather')

		print('GET UI INFO')
		loadOnSelection     = mc.checkBox( self.cbAnimLoadOnSelection    , q = True , v = True )
		loadMatchSelection  = mc.checkBox( self.cbAnimLoadMatchSelection , q = True , v = True )
		loadMatchNamespace  = mc.checkBox( self.cbAnimLoadMatchNamespace , q = True , v = True )
		replaceCurrent      = mc.checkBox( self.cbAnimReplaceCurrent     , q = True , v = True )
		offsetCurrentFrame  = mc.checkBox( self.cbAnimOffsetCurrentFrame , q = True , v = True )
		offsetEndFrame      = mc.checkBox( self.cbAnimOffsetEndFrame     , q = True , v = True )
		inverseAnimation    = mc.checkBox( self.cbAnimInverse            , q = True , v = True )
		mirrorAnimation     = mc.checkBox( self.cbAnimMirror             , q = True , v = True )

		print('GET SCENE INFO')
		frameEnd     = mc.playbackOptions( q = True , max = True )
		frameCurrent = mc.currentTime( q=True )
		selection    = mc.ls(sl=True)

		namespace = None
		if(loadMatchNamespace):
			namespace = ''
			if( ':' in selection[0] ):
				namespace = selection[0].split(':')[0]

		args = {}
		if( replaceCurrent     ):args['replace'      ] = True 
		if( offsetCurrentFrame ):args['startFrame'   ] = frameCurrent
		if( offsetEndFrame     ):args['startFrame'   ] = frameEnd	
		if( loadOnSelection    ):args['objsToFilter' ] = selection 
		if( loadMatchSelection ):args['matchObjName' ] = selection[0] 
		if( inverseAnimation   ):args['inverse'      ] = True 
		if( mirrorAnimation    ):args['mirror'       ] = 'X' 

		if not( namespace == None ):args['overrideNamespace'] = namespace 

		self.AnimCurve.toObjs( **args ) 


	def cmds_animCurveRefreshFile(self):
		print('cmds_animCurveRefreshFile')   
		file = mc.optionMenu( self.omFileNames , q = True , v = True )  
		pathFile = '{}/{}'.format(self.animCurvePath,file)	
		print('pathFile',pathFile)
		self.AnimCurve.createFromFile(pathFile)
		info = self.AnimCurve.getInfo()
		mc.optionMenu( self.omFileNames , e = True , ann = info )

	def cmds_animCurveObjSelect(self):
		self.AnimCurve.selectObjs()

	def cmds_animCurveRefreshPath(self):

		#GET INFO
		print('cmds_animCurveRefreshPath')
		self.animCurvePath  = self.rwi.utilsPath_RemoveFile( mc.textField( self.ftAnimPath , q = True , tx = True ) )
		showLatest          = mc.checkBox( self.cbFileShowLatest , q = True , v = True )
		self.animCurvefiles = self.rwi.utilsPath_getFiles( self.animCurvePath , extention = 'xml' , latest = showLatest )

		#REFRESH UI LIST
		menuItems = mc.optionMenu(self.omFileNames, q=True, itemListLong=True)
		if menuItems: mc.deleteUI(menuItems)
		for animCurvefile in self.animCurvefiles: mc.menuItem( p = self.omFileNames , l = animCurvefile )

		#REFRESH UI TEXT FIELD
		mc.textField( self.ftAnimPath , e = True , ann = self.animCurvePath )
		


	def UI_animCurve( self, UIparent ):
		
		panels =  [ 'flAnimCurve',  'colAnimCurve' ,  'flAnimGather' ,  'colAnimGather' , 'flAnimRelease' ,  'colAnimRelease' ]	
		
		mc.frameLayout( panels[0]  , li = 80 , cl = 1 , cll = 1 ,  w = 262 ,  bgc = [ 0.23 , 0.23 , 0.24 ]  ,   label = 'ANIM CURVE' , p = UIparent )
		
		mc.columnLayout( panels[1] , p = panels[0] , bgc = [ 0.27 , 0.27 , 0.27 ]  , columnAttach = [ 'both' , 10 ] , rowSpacing = 0 , columnWidth = 280  )
		
		mc.text(                             p = panels[1] , l = ''                         , h = 1  )
		mc.textField(self.ftAnimPath       , p = panels[1] , tx = self.animCurvePath        , ann = self.animCurvePath , ec = '{}.cmds_animCurveRefreshPath()'.format(self.variableNameInGlobal) , cc = '{}.cmds_animCurveRefreshPath()'.format(self.variableNameInGlobal) )
		mc.text(                             p = panels[1] , l = ''                         , h = 5  )	
		mc.button(                           p = panels[1] , l = 'PATH - GET CURRENT SCENE' , bgc = [ 0.5 , 0.3 , 0.3 ]    , c = '{}.cmds_animCurvePathUpdateWithCurrent()'.format(self.variableNameInGlobal) )					
		mc.text(                             p = panels[1] , l = ''                         , h = 5  )		
		mc.button(                           p = panels[1] , l = 'PATH - OPEN IN EXPLORER'  , bgc = [ 0.3 , 0.3 , 0.3 ]    , c = '{}.cmds_animCurvePathOpen()'.format(self.variableNameInGlobal) )				
		mc.text(                             p = panels[1] , l = ''                         , h = 5  )
		mc.text(                             p = panels[1] , l = '' , h = 5  )	
		mc.checkBox( self.cbFileShowLatest , p = panels[1] , l = 'show only latest' , v = 1 , cc = '{}.cmds_animCurveRefreshPath()'.format(self.variableNameInGlobal) )
		mc.text(                             p = panels[1] , l = '' , h = 5  )		
		mc.optionMenu(self.omFileNames     , p = panels[1] , w = 120 ,  bgc = [ 0.35 , 0.35 , 0.35 ] , cc = '{}.cmds_animCurveRefreshFile()'.format(self.variableNameInGlobal) )				
		mc.text(                             p = panels[1] , l = '' , h = 1  )
		mc.frameLayout( panels[2]    , p = panels[1] , l = 'GATHER'                   , bgc = [ 0.23 , 0.23 , 0.24 ] , li = 80 , cl = 1 , cll = 1 ,  w = 262 )
		mc.text(                       p = panels[1] , l = ''                         , h = 1  )
		mc.frameLayout( panels[4]    , p = panels[1] , l = 'RELEASE'                  , bgc = [ 0.23 , 0.23 , 0.24 ] , li = 80 , cl = 1 , cll = 1 ,  w = 262  )		

		mc.columnLayout( panels[3]                 , p = panels[2] , bgc = [ 0.27 , 0.27 , 0.27 ]  , columnAttach = [ 'both' , 10 ] , rowSpacing = 0 , columnWidth = 280  )

		mc.text(                                     p = panels[3] , l = '' , h = 1  )	
		mc.button(                                   p = panels[3] , l = 'GATHER' , bgc = [ 0.5 , 0.3 , 0.3 ] , c = '{}.cmds_animCurveGather()'.format(self.variableNameInGlobal) )		
		mc.text(                                     p = panels[3] , l = '' , h = 5  )
		mc.button(                                   p = panels[3] , l = 'SELECT CTRLS' , bgc = [ 0.5 , 0.3 , 0.3 ] , c = '{}.cmds_animCurveObjSelect()'.format(self.variableNameInGlobal) )		
		mc.text(                                     p = panels[3] , l = '' , h = 5  )		
		mc.checkBox( self.cbAnimLoadOnSelection    , p = panels[3] , l = 'CTRLS - load on selection' , v = 0  )
		mc.text(                                     p = panels[3] , l = '' , h = 5  )		
		mc.checkBox( self.cbAnimLoadMatchSelection , p = panels[3] , l = 'CTRLS - match selection' , v = 0  )		
		mc.text(                                     p = panels[3] , l = '' , h = 5  )		
		mc.checkBox( self.cbAnimLoadMatchNamespace , p = panels[3] , l = 'CTRLS - match selected namespace' , v = 0  )			
		mc.text(                                     p = panels[3] , l = '' , h = 5  )		
		mc.checkBox( self.cbAnimReplaceCurrent     , p = panels[3] , l = 'CURVES - replace' , v = 0  )	
		mc.text(                                     p = panels[3] , l = '' , h = 5  )		
		mc.checkBox( self.cbAnimOffsetCurrentFrame , p = panels[3] , l = 'TIME - load at current frame' , v = 0  )
		mc.text(                                     p = panels[3] , l = '' , h = 5  )
		mc.checkBox( self.cbAnimOffsetEndFrame     , p = panels[3] , l = 'TIME - load at end frame' , v = 0  )	
		mc.text(                                     p = panels[3] , l = '' , h = 5  )
		mc.checkBox( self.cbAnimInverse            , p = panels[3] , l = 'TIME - inverse' , v = 0  )
		mc.text(                                     p = panels[3] , l = '' , h = 5  )
		mc.checkBox( self.cbAnimMirror             , p = panels[3] , l = 'VALUE - mirror' , v = 0  )				
		mc.text(                                     p = panels[3] , l = '' , h = 10 )

		for animCurvefile in self.animCurvefiles:
			mc.menuItem( p = self.omFileNames , l = animCurvefile )	

		mc.columnLayout( panels[5]                         , p = panels[4] , bgc = [ 0.27 , 0.27 , 0.27 ]  , columnAttach = [ 'both' , 10 ] , rowSpacing = 0 , columnWidth = 280  )

		mc.button(                                           p = panels[5] , l = 'RELEASE' , bgc = [ 0.5 , 0.3 , 0.3 ] , c = '{}.cmds_animCurveRelease()'.format(self.variableNameInGlobal) )		
		mc.text(                                             p = panels[5] , l = '' , h = 5  )

		mc.radioCollection( self.rcAnimCurveReleaseOption , p = panels[5] )
		mc.radioButton(  l = 'from All' )
		mc.radioButton(  l = 'from selected RIG'  )
		mc.radioButton(  l = 'from selected CTRLS' , select = True  )
		mc.text(                                             p = panels[5] , l = '' , h = 10 )

	def UI_rigPuppets( self, UIparent ):
		
		panels =  [ 'bmUI_rigPuppets' , 'bmUI_rigPuppetsCol' ]	
		
		mc.frameLayout( panels[0]  , li = 80 , cl = 1 , cll = 1 ,  w = 262 ,  bgc = [ 0.23 , 0.23 , 0.24 ]  ,   label = 'RIG PUPPETS' , p = UIparent )
		
		mc.columnLayout( panels[1] , p = panels[0] , bgc = [ 0.27 , 0.27 , 0.27 ]  , columnAttach = [ 'both' , 10 ] , rowSpacing = 0 , columnWidth = 280  )
		mc.text(        p = panels[1] , l = '' , h = 1  )
		mc.button(      p = panels[1] , l = 'RELOAD SELECTED RIG' , bgc = [ 0.5 , 0.3 , 0.3 ] , c = '{}.cmds_reloadSelectedRig()'.format(self.variableNameInGlobal) )		
		mc.text(        p = panels[1] , l = '' , h = 5  )		
		mc.checkBox( self.cbRigPuppetsOptimize , p = panels[1] , l = 'optimize perfomance' , v = 0  )
		mc.text(        p = panels[1] , l = '' , h = 10  )		
		
		
	def cmds_reloadSelectedRig(self):
		doOptimize = mc.checkBox( self.cbRigPuppetsOptimize , q = True , v = True )
		rigPuppet_reloadRigSelected(optimize = doOptimize )



	def UI_switch( self, UIparent ):
		
		panels =  [ 'bmUI_switch' , 'bmUI_switchCol' ]	
		
		mc.frameLayout( panels[0]  , li = 80 , cl = 1 , cll = 1 ,  w = 262 ,  bgc = [ 0.23 , 0.23 , 0.24 ]  ,   label = 'SWITCH' , p = UIparent )
		
		mc.columnLayout( panels[1] ,               p = panels[0] , bgc = [ 0.27 , 0.27 , 0.27 ]  , columnAttach = [ 'both' , 10 ] , rowSpacing = 0 , columnWidth = 280  )
		mc.text(                                   p = panels[1] , l = '' , h = 1  )
		mc.button(                                 p = panels[1] , l = 'LOAD SELECTED SPACE SWITCH' , bgc = [ 0.5 , 0.3 , 0.3 ] , c = '{}.cmds_loadSelectedSpaceSwitch()'.format(self.variableNameInGlobal) )		
		mc.text(                                   p = panels[1] , l = '' , h = 5  )	
		mc.button(      self.btnSpaceSwitch      , p = panels[1] , l = '' , bgc = [ 0.35 , 0.35 , 0.35  ] , c = '{}.cmds_selectCurrentSwitchAttr()'.format(self.variableNameInGlobal) )			
		mc.text(                                   p = panels[1] , l = '' , h = 5  )	
		mc.optionMenu( self.omSpaceSwitch        , p = panels[1] , w = 120 ,  bgc = [ 0.35 , 0.35 , 0.35 ] , cc = '{}.cmds_doSwitchSpace()'.format(self.variableNameInGlobal)  )
		mc.text(                                   p = panels[1] , l = '' , h = 5  )		
		mc.intSliderGrp( self.isgSpacetransFrame , p = panels[1] , l ='transitionFrame', field=True, minValue=0, maxValue=50, fieldMinValue=0, fieldMaxValue=50, value=0 )
		mc.text(                                   p = panels[1] , l = '' , h = 10  )		

	def cmds_animCurvePathOpen(self):
		print('cmds_animCurvePathOpen')
		path = mc.textField(  self.ftAnimPath  , q = True , tx = True )
		print( self.rwi.utilsPath_toPythonSyntax(path) )
		self.rwi.utilsPath_openInExplorer(path)
		self.cmds_animCurveRefreshPath()

	def cmds_animCurvePathUpdateWithCurrent(self):
		print('cmds_animCurvePathUpdateWithCurrent')
		path = self.rwi.utilsPath_getCurrentSceneFolderPath()
		mc.textField(  self.ftAnimPath  , e = True , tx = path )
		self.cmds_animCurveRefreshPath()



	def cmds_loadSelectedSpaceSwitch(self):
		print('cmds_loadSelectedSpaceSwitch')	
		selectedAttrs = utilsMaya.getSelectedAttrs()

		if( len( selectedAttrs ) == 0 ):
			print('cmds_loadSelectedSpaceSwitch: SELECT ONE ATTR IN THE CHANNEL BOX')
			return 0

		self.spaceSwitchDictInfo = spaceSwitch_getDictInfo(selectedAttrs[0])

		#DELETE OLD
		menuItems = mc.optionMenu(self.omSpaceSwitch, q=True, itemListLong=True)
		if menuItems:
			mc.deleteUI(menuItems)

		#CREATE NEW
		for i in range(0,len(self.spaceSwitchDictInfo['choices'])):
			if( i == self.spaceSwitchDictInfo['value'] ):
				mc.menuItem( 'miSpaceSwitch{}'.format(i) , p = self.omSpaceSwitch , l = self.spaceSwitchDictInfo['choices'][i] , boldFont = True )
			else:                             
				mc.menuItem( 'miSpaceSwitch{}'.format(i) , p = self.omSpaceSwitch , l = self.spaceSwitchDictInfo['choices'][i] )

		#UPDATE UI WITH NEW VALUES
		mc.optionMenu(self.omSpaceSwitch , e = True , v = self.spaceSwitchDictInfo['choices'][self.spaceSwitchDictInfo['value']] )
		mc.button(   self.btnSpaceSwitch , e = True , l = self.spaceSwitchDictInfo['attr'] )

		return 1



	def cmds_doSwitchSpace(self):
		print('cmds_doSwitchSpace')
		#GET NEW VALUE
		userSpaceChoice    = mc.optionMenu(self.omSpaceSwitch, q = True , v = True )
		value              = self.spaceSwitchDictInfo['choices'].index(userSpaceChoice)
		transitionFrames   = mc.intSliderGrp( self.isgSpacetransFrame , q = True , v = True )
		#DO
		print('--------> {}'.format(value))
		spaceSwitch_doSwitch( self.spaceSwitchDictInfo , value , transitionFrames = transitionFrames )
		#STORE NEW VALUE
		self.spaceSwitchDictInfo['value'] = value

		return 1


		
	def cmds_selectCurrentSwitchAttr( self ):
		print('cmds_doSwitchSpace')
		objAttr = mc.button(self.btnSpaceSwitch , q = True , l = True )
		obj  = objAttr.split('.')[0]
		attr = objAttr.split('.')[1]
		mc.select( obj )






	def UI_IKFK( self, UIparent ):
		
		panels =  [ 'bmUI_IKFK' , 'bmUI_IKFKCol' ]	
		
		mc.frameLayout( panels[0]  , li = 80 , cl = 1 , cll = 1 ,  w = 262 ,  bgc = [ 0.23 , 0.23 , 0.24 ]  ,   label = 'IK/FK' , p = UIparent )
		
		mc.columnLayout( panels[1] , p = panels[0] , bgc = [ 0.27 , 0.27 , 0.27 ]  , columnAttach = [ 'both' , 10 ] , rowSpacing = 0 , columnWidth = 280  )
		mc.text(                                  p = panels[1] , l = '' , h = 1  )
		mc.button(                                p = panels[1] , l = 'LOAD SELECTED IK/FK SWITCH' , bgc = [ 0.5 , 0.3 , 0.3 ] , c = '{}.cmds_loadSelectedIKFKSwitch()'.format(self.variableNameInGlobal) )		
		mc.text(                                  p = panels[1] , l = '' , h = 5  )	
		mc.button(      self.btnIKFKSwitch      , p = panels[1] , l = '' , bgc = [ 0.35 , 0.35 , 0.35  ] , c = '{}.cmds_doIKFKSwitch()'.format(self.variableNameInGlobal) )			
		mc.text(                                  p = panels[1] , l = '' , h = 5  )	
		mc.intSliderGrp( self.isgIKFKtransFrame , p = panels[1] , l ='transitionFrame', field=True, minValue=0, maxValue=50, fieldMinValue=0, fieldMaxValue=50, value=0 )
		mc.text(                                  p = panels[1] , l = '' , h = 10  )	

		
	def cmds_loadSelectedIKFKSwitch( self ):
		print('cmds_loadSelectedIKFKSwitch')
		self.IKFKdictArmInfo = rigModuleArm_getCtrlsFromSelection()
		rootCtrl             = self.IKFKdictArmInfo['root']
		self.IKFKvalue       = mc.getAttr( rootCtrl + '.IK' )
		self.cmds_IKFKUpdateButtonLook( self.IKFKvalue , rootCtrl )	

	def cmds_doIKFKSwitch( self ):
		print('cmds_doIKFKSwitch')
		rootCtrl             = self.IKFKdictArmInfo['root']
		transitionFrames     = mc.intSliderGrp( self.isgIKFKtransFrame , q = True , v = True )

		if( self.IKFKvalue == 1 ):
			print('\tdo IK---->FK')
			rigModuleArm_switchToFK(self.IKFKdictArmInfo , transitionFrames = transitionFrames )
		else:
			print('\tdo FK---->IK')
			rigModuleArm_switchToIK(self.IKFKdictArmInfo , transitionFrames = transitionFrames )

		#UPDATE UI
		self.IKFKvalue       = 1 - self.IKFKvalue
		mc.setAttr( rootCtrl + '.IK' , self.IKFKvalue )
		self.cmds_IKFKUpdateButtonLook( self.IKFKvalue , rootCtrl )


	def cmds_IKFKUpdateButtonLook( self , IKFKvalue , rootCtrlName ):
		rootBaseName = rootCtrlName.split('_CTRL')[0]
		btnLabel = rootBaseName + ' toIK'
		btnColor = [ 0.5 , 0.35 , 0.35  ]
		if(IKFKvalue==1):
			btnLabel = rootBaseName + ' toFK'
			btnColor = [ 0.35 , 0.5 , 0.35 ]

		mc.button(      self.btnIKFKSwitch , e = True, l = btnLabel , ann = btnLabel , bgc = btnColor  )	
	#_______________________________________________________________________________________________________________________________________________________________________ UI_manipShape_form		
	def UI_manipShape_form( self , name , parent ):
			
		mc.rowColumnLayout( name , nc = 3 , columnWidth = [ ( 1 , 120 ) , ( 2 , 10 ) , ( 3 , 140 ) ]  , p = parent )

		#---------------------------------------		
		mc.rowColumnLayout(  nc = 1 , w = 120)
		mc.text( l = ' ' , h = 15 )
		
		mc.optionMenu( 'formList' , w = 120 ,  bgc = [ 0.35 , 0.35 , 0.35 ] )
		
		for form in self.CurveShape.getForms():
			mc.menuItem( l = form )
			
		mc.menuItem( l = '>> ADD <<' )

		mc.text( l = ' ' , h = 15 )
		mc.setParent(name)	

		mc.text( l = ' ' , h = 15 )

		mc.rowColumnLayout(  nc = 1 , w = 140)
		mc.text( l = ' ' , h = 15 )
		mc.button( l = 'CHANGE SHAPE'  ,  bgc = [ 0.35 , 0.35 , 0.35 ] , c = '{}.cmds_changeShape()'.format(self.variableNameInGlobal) )
		mc.text( l = ' ' , h = 15 )

	def cmds_changeShape(self):
		selection    = mc.ls(sl = True )
		form         = mc.optionMenu( 'formList' , q = True , v = True )
		updateOthers = mc.checkBox( self.cbModifDupli , q = True , v = True )

		objs = selection
		if( updateOthers == 1 ):
			objs = objsRelationShip_getOthers( self.dupliDictCtrls , selection , addSource = True )


		print( '--- form {} apply to {} ---'.format( form , objs ) )

		for obj in objs:
			self.CurveShape.setForm( obj , form )

		mc.select( selection )


	def cmds_skinCopyToDuplicate(self):
		selection    = mc.ls(sl = True )

		Skin = sCluster.skinCluster()
		for elem in selection:
			Skin.createFromObjs([elem])
			
			meshSource   = Skin.meshs[0]
			jointsSource = Skin.joints[0][:]

			isShape = 0
			if( mc.nodeType(meshSource) == 'mesh' ):
				isShape = 1 
				meshSource = mc.listRelatives( meshSource , p = True )[0]

			meshsDictSimilar  = objsRelationShip_getSimilar( [ self.dupliDictModels ] , [meshSource] , 0 )

			jointsDictSimilars = []
			for i in range( 0 , len(jointsSource) ):
				jointsDictSimilars.append( objsRelationShip_getSimilar( [ self.dupliDictJoints ] , [ jointsSource[i] ] , 0 ) )


			for mKey in meshsDictSimilar.keys():
				meshes = meshsDictSimilar[mKey]
				print( 'mKey: {}  ArrayToCheck: {}'.format( mKey , meshes ) )

				for mI in range(0,len(meshes) ):
					print( '\t{}/{} MIRROR MESH {} ---> \'{}\''.format( mI , len(meshes) , elem , meshes[mI] ) )
					Skin.meshs[0]  = meshes[mI]
	
					for i in range( 0 , len(jointsSource) ):
						jointsDictSimilar = jointsDictSimilars[i]
	
						mirrorJoint      = None
						keyDifferenceNbr = 999999999999999

						for jKey in jointsDictSimilar.keys():
							joints = jointsDictSimilar[jKey]
							print( '\t\tjKey: {}  ArrayToCheck: {}'.format( jKey , joints) )

							if( jKey == mKey ): 
								mirrorJoint = joints[mI]
								keyDifferenceNbr = 0
								print( '\t\tjKey == mKey - {} ---> \'{}\''.format(jointsSource[i] , joints[mI]) )

							elif( jKey in mKey ):
								keyDifferenceNbrCurrent = len(mKey) - len(jKey)

								if( keyDifferenceNbrCurrent < keyDifferenceNbr ):
									for jI in range(0,len(joints) ):
										print( '\t\tjKey in mKey - {} ---> \'{}\''.format(jointsSource[i] , joints[jI]) )
										mirrorJoint = joints[jI]

									keyDifferenceNbr = keyDifferenceNbrCurrent


						if not( mirrorJoint == None):
							Skin.joints[0][i] = mirrorJoint
						else:
							Skin.joints[0][i] = jointsSource[i]
	
					if( isShape ):
						Skin.meshs[0] = mc.listRelatives( Skin.meshs[0] , c = True , s = True , type = 'mesh' )[0]
	
					Skin.toObjs()

			return 0


	def cmds_repeatFlood500(self):
		utilsMaya.skin_repeatFlood( iter = 500 )

	#_______________________________________________________________________________________________________________________________________________________________________ UI_manipShape_color				
	def UI_manipShape_color( self , name , parent ):
	
	
		# w = 240	
		rows      = 2
		columns   = 16 
		cellHeigh = 19 
		cellWidth = 15
		
		mc.palettePort( name ,      dim = [ columns , rows  ]   ,    width = (columns * cellWidth)    ,    height = (rows * cellHeigh)    , transparent = 0 , topDown = True , colorEditable = False , setCurCell = 0  , p = parent  )	
		mc.palettePort( name , e = True , cc = ( '{}.cmds_changeShapeColorButton("{}")'.format( self.variableNameInGlobal , name ) ) )	
		
		for i  in range( 1 , 32 ):	
			componentColors = mc.colorIndex( i , q = True )	
			mc.palettePort(   name ,  e = True ,  rgbValue = [ i , componentColors[0] , componentColors[1] , componentColors[2] ]   )
			
		mc.palettePort(       name ,  e = True ,  rgbValue = [ 0 , 0.6 , 0.6 , 0.6 ]   )

	#_______________________________________________________________________________________________________________________________________________________________________ changeShapeColorButton				
	def cmds_changeShapeColorButton( self , palettePortName ):		
		#_UI			
		selection    = mc.ls(sl = True )
		index   = mc.palettePort( palettePortName , query=True , scc = True ) 
		colorIndex  = self.CurveShape.colorNameToIndex[ self.colorkeys[index] ]	
		updateOthers = mc.checkBox( self.cbModifDupli , q = True , v = True )

		objs = selection
		if( updateOthers == 1 ):
			objs = objsRelationShip_getOthers( self.dupliDictCtrls , selection , addSource = True )

		for elem in objs:
			self.CurveShape.setColor( elem , colorIndex )
			print('cmds - CHANGE COLOR FOR {} to the color {}'.format(elem , colorIndex ) )

		mc.select( selection )

	#_______________________________________________________________________________________________________________________________________________________________________ UI_manipShape_color				
	def UI_manipShape_colorSorted( self , name , parent ):

		keys = self.CurveShape.fonctionToColorName.keys()
		keys.sort()

		colorSection = ['neutral' , 'left' , 'center'  , 'right' , 'root'   , 'spectial']
		self.colorkeys         = []
		self.colorkeys        += [ 'None'   , 'red'  , 'yellow'  , 'blue'  , 'green'  , 'purple'  ]
		self.colorkeys        += [ 'white'  , 'red2' , 'yellow2' , 'blue2' , 'green2' , 'purple2' ]
		self.colorkeys        += [ 'white2' , 'red3' , 'yellow3' , 'blue3' , 'green3' , 'purple3' ]
		self.colorkeys        += [ 'white3' , 'red4' , 'yellow4' , 'blue4' , 'green4' , 'purple4' ]
		self.colorkeys        += [ 'white4' , 'red5' , 'yellow4' , 'blue4' , 'green4' , 'purple5' ]

		# w = 240	
		rows      = 5
		columns   = 6
		cellHeigh = 19 
		cellWidth = 40

		
		mc.columnLayout(    name , bgc = [ 0.27 , 0.27 , 0.27 ] , columnAttach = [ 'both' , 0 ] , rowSpacing = 0 , columnWidth = (columns * cellWidth)  , parent = parent )

		rowColumnLayoutName = name + 'text'
		mc.rowColumnLayout( rowColumnLayoutName , nc = columns , columnWidth = [ ( i , cellWidth ) for i in range(1,columns) ]  , p = name )
		for elem in colorSection: mc.text( l = elem , h = 15 , p = rowColumnLayoutName );

		paletteName = name + 'Palette'
		mc.palettePort( paletteName , dim = [ columns , rows  ] , width = (columns * cellWidth)  , height = (rows * cellHeigh) , transparent = 0 , topDown = True , colorEditable = False , setCurCell = 0  , p = name  )	
		mc.palettePort( paletteName , e = True , cc = ( '{}.cmds_changeShapeColorButton("{}")'.format(self.variableNameInGlobal,paletteName) ) )	
		
		for i  in range( 1 , rows*columns ):	
			colorIndex  = self.CurveShape.colorNameToIndex[ self.colorkeys[i] ]
			componentColors = mc.colorIndex( colorIndex , q = True )		
			mc.palettePort(   paletteName ,  e = True ,  rgbValue = [ i , componentColors[0] , componentColors[1] , componentColors[2] ]  )
			


