
'''
	name:  buildMoveOnAxeCamRig
	type:  RIGGING
	tag:   build
	date:  15/07/2016	
	input: none

	lauch a UI.
	then select a camera and some geometry. It create a rig witch can move the geometry in space without changing the image on the camera.
'''


import maya.cmds as mc		
from ..utilsMaya import utilsMaya             



# moacInstance

def buildMoveOnAxeCamRig():
	exec('moacInstance = moveOnAxeCam()') in globals()
	
	
class moveOnAxeCam():
	
	
	def __init__(self):
		self.importPath = 'toolBox.tools.buildMoveOnAxeCamRig.buildMoveOnAxeCamRig'
		self.varName    = 'moacInstance'
		self.importCmds    = 'import maya.cmds as mc ;'		
		self.buildUi()

	#______________________________________________________________________________________________________________________________________________ refreshUI
	
	def refreshUI( self ):
		
		# DELETE
	
		try:
			mc.deleteUI( 'emptyText' )
		except:
			pass
		
			
		for i in range( 1 , 100):
			try:
				mc.deleteUI( 'commandBox%r' %i )
			except:
				break
	
	
		# CREATE
	
		if not( mc.objExists( 'moveOnAxeCamRig_grp' ) ):
			mc.text( 'emptyText' , l = "---- empty ----" , p = 'commandColumn' , w = 300 , h = 20  )
			return 0					
		
		childrens = mc.listRelatives( 'moveOnAxeCamRig_grp' , c = True )
		
		if( childrens == None ):
			mc.text( 'emptyText' , l = "---- empty ----" , p = 'commandColumn' , w = 300 , h = 20  )
			return 0			
				
	
		cSize = 17
		i = 1
	
		for children in childrens:
			
			baseName = utilsMaya.getObjBaseName( children , 0 , 0 )
			
			
			manip = baseName +'_ctrl'		
			objs = utilsMaya.readStringArrayAttr( children, 'objsSlave' )	
			cam  = utilsMaya.readStringArrayAttr( children, 'camera'    )
	
			objBases = []
			for obj in objs:
				objBase = utilsMaya.getObjBaseName( obj , 0 , 0 ) 
				if not( objBase in objBases ):
					objBases.append( objBase )
				
					
			selectObjsC  = ( self.importCmds + 'mc.select(' + utilsMaya.convertStringArraytoStringCommand( objs ) + ')' )
			selectManipC = ( self.importCmds + 'mc.select( \"'+ manip    +'\" )'                )		
			selectCamC   = ( self.importCmds + 'mc.select( \"'+ cam[0]   +'\" )'                )		
			applyC       = ( self.importCmds + 'mc.delete( ' + utilsMaya.convertStringArraytoStringCommand( objBases ) + ' , ch = True )  ;mc.delete( \"'+ children +'\" );  ' + self.importPath +'.'+ self.varName + '.refreshUI();'  )
			deleteC      = ( self.importCmds + 'mc.delete( \"'+ children +'\" );  ' + self.importPath +'.'+ self.varName + '.refreshUI();'  )
	
			selectManipBuild = ( 'mc.button( l = \''+ manip    +'\'  , bgc = [ 0.3 , 0.4 , 0.5 ]  , c = \''+ selectManipC +'\' )' ) 		
			selectObjsBuild  = ( 'mc.button( l = \''+ objs[0]  +'\'  , bgc = [ 0.3 , 0.4 , 0.5 ]  , c = \''+ selectObjsC  +'\' )' ) 		
			selectCamBuild   = ( 'mc.button( l = \''+ cam[0]   +'\'  , bgc = [ 0.3 , 0.4 , 0.5 ]  , c = \''+ selectCamC   +'\' )' )		
			applyBuild       = ( 'mc.button( l = "V"                 , bgc = [ 0.3 , 0.5 , 0.3 ]  , c = \''+ applyC       +'\' )' ) 		
			deleteBuild      = ( 'mc.button( l = "X"                 , bgc = [ 0.5 , 0.3 , 0.3 ]  , c = \''+ deleteC      +'\' )' ) 	
	
			utilsMaya.buildUi_makeNiceBox( 'commandBox%r' %i   , 'commandColumn' ,  300 , 20  , [ selectManipBuild , selectObjsBuild , selectCamBuild , applyBuild , deleteBuild ] , [ cSize, cSize , cSize , cSize , cSize ]  )		
			i += 1
	
			
		moveOneAxeWin = 'moveOneAxeWin'
		
		if( mc.windowPref( moveOneAxeWin , ex = True ) ):
			mc.windowPref( moveOneAxeWin , e = True , w = 295 , h = 50 )		
			
		mc.window( moveOneAxeWin , e = True , w = 295 , h = 50 ) 	
		
		return 1	
	
	
	#_________________________________________________________________________________________________________________________________________________ buildUI
	
	
	def buildUi( self ):
	
		moveOneAxeWin = 'moveOneAxeWin' 
		
		if( mc.windowPref( moveOneAxeWin , ex = True ) ):
			mc.windowPref( moveOneAxeWin , e = True , w = 295 , h = 50 )
		
		if( mc.window( moveOneAxeWin , ex = True ) ):
			mc.deleteUI( moveOneAxeWin , wnd = True )
				
		
		
		mc.window( moveOneAxeWin , w = 295 , h = 50 , rtf = True , s = True ) 	
				
				
				
		mc.columnLayout( 'mainColumn' )
		
		cSize = 18
		
		utilsMaya.buildUi_makeNiceBox( 'titleWinBox'     , 'mainColumn' ,  300 , 30  , [ 'mc.text( l= "BUILD MOVE ON AXE CAM RIG" , bgc = [ 0.3 , 0.4 , 0.5 ] )' ] , [ 95 ]  )
		utilsMaya.buildUi_makeNiceBox( 'titleCommandBox' , 'mainColumn' ,  300 , 20  , [ 'mc.text( l = "MANIP"  )' , 'mc.text( l = "OBJS"  )' , 'mc.text( l = "CAM"  )' , 'mc.text( l = "APPLY"  )' , 'mc.text( l = "DELETE"  )' ] , [ cSize, cSize , cSize , cSize , cSize ]  )
		mc.columnLayout( 'commandColumn' , p = 'mainColumn' , bgc = [ 0.2 , 0.2 , 0.2 ]   )
		utilsMaya.buildUi_makeNiceBox( 'ExecBox' , 'mainColumn' ,  300 , 40  , [ 'mc.button( l = "CREATE" , c = "{0}.{1}.buildRigButton();{0}.{1}.refreshUI();" )'.format( self.importPath , self.varName ) , 'mc.button( l = "REFRESH" , c = "{0}.{1}.refreshUI()" )'.format( self.importPath , self.varName ) ] , [ 65 , 25 ]  )
		
		mc.showWindow( 'moveOneAxeWin' )
				
		self.refreshUI()
	
			
			
			
	#_________________________________________________________________________________________________________________________________________________ buildRig		
		
	
		
	def buildRig( self ,objs , cam ):
	
	
		#builds allgrp
		
		allGrp = 'moveOnAxeCamRig_grp'
		
		if not( mc.objExists( allGrp ) ):
			mc.createNode( 'transform' , n = allGrp )
		
		#builds sysGrp	
			
		for i in range( 0 , 100 ):
			
			baseName =  'moac%r' %( i )
			grpName  =  baseName + '_grp' 
			
			if( mc.objExists( grpName ) ):
				continue
				
			mc.createNode( 'transform' , n = grpName , p = allGrp )
			break
			
		utilsMaya.writeStringArrayAttr( grpName, 'objsSlave' ,  objs )	
		utilsMaya.writeStringArrayAttr( grpName, 'camera' ,  [ cam ] )	
			
		#builds DAG elem
		
		moacSysNames   = [ baseName + '_orig' , baseName + '_ctrl' , baseName + '_scale' ]
		moacSysTypes   = [ 'transform'        , 'locator'          , 'transform'         ]
		moacSysParents = [ grpName            , baseName + '_orig' , baseName + '_ctrl'  ]
			 
		newNodes = utilsMaya.createDagNodes( moacSysNames , moacSysTypes , moacSysParents )
		mc.setAttr( ( moacSysNames[2] + '.visibility' ) , 0 )	
		#create cluster
	
		clusterNames = mc.cluster( objs , n = ( baseName + '_cluster' )  )
		
		# orienter manip
		
		mc.delete( mc.pointConstraint( clusterNames[1] , moacSysNames[0] )  )	
		mc.delete( mc.aimConstraint(   cam             , moacSysNames[0] )  )	
		
		#  create attr on loc manip
		
		attrNames = [ 'EXTRA_ATTR' , 'modifScale' , 'modifProfondeur' , 'INFO_ATTR' , 'distance'   , 'distanceBase'  ]
		attrTypes  = [ 'separator' , 'enumOnOff'  , 'float1'         , 'separator' , 'floatInput' , 'floatInput'    ]
		
		objAttrNames = utilsMaya.addSpecialAttrs(  moacSysNames[1] , attrNames , attrTypes )
		
		
		
		# builds ditance dimension
		
		baseNameDistDim = baseName + '_DistDim' 
		
		dimGrp = utilsMaya.buildDistDimensionSys( baseNameDistDim , moacSysNames[1] , cam , objAttrNames[4] )
		
		mc.setAttr( ( dimGrp + '.visibility' ) , 0 )
		mc.parent( dimGrp , grpName )
		
		mc.setAttr( objAttrNames[5] , mc.getAttr( objAttrNames[4] ) , lock = True  )
		 
		# builds all node sys
		
		moacNodes = [ ( baseName + '_scale_muliDiv' ) , ( baseName + '_scale_blendColor' ) , ( baseName + '_scaleX_blendColor' ) ]
		
		mc.createNode( 'multiplyDivide' , n = moacNodes[0]  )	
		mc.setAttr( (  moacNodes[0] + '.operation' )  , 2 )
		mc.connectAttr( objAttrNames[4] , ( moacNodes[0] + '.input1X' ) )
		mc.connectAttr( objAttrNames[4] , ( moacNodes[0] + '.input1Y' ) )
		mc.connectAttr( objAttrNames[4] , ( moacNodes[0] + '.input1Z' ) )	
		mc.connectAttr( objAttrNames[5] , ( moacNodes[0] + '.input2X' ) )
		mc.connectAttr( objAttrNames[5] , ( moacNodes[0] + '.input2Y' ) )
		mc.connectAttr( objAttrNames[5] , ( moacNodes[0] + '.input2Z' ) )
	
		
		mc.createNode( 'blendColors'     , n = moacNodes[1]  )
		mc.connectAttr( objAttrNames[1]              , (  moacNodes[1] + '.blender' ) )		
		mc.connectAttr( ( moacNodes[0] + '.output' ) , (  moacNodes[1] + '.color1'  ) )		
		mc.setAttr( (  moacNodes[1] + '.color2R' )  , 1 )	
		mc.setAttr( (  moacNodes[1] + '.color2G' )  , 1 )	
		mc.setAttr( (  moacNodes[1] + '.color2B' )  , 1 )		
		
		mc.createNode( 'blendColors'     , n = moacNodes[2]  )		
		mc.connectAttr( objAttrNames[2]              , (  moacNodes[2] + '.blender' ) )		
		mc.connectAttr( ( moacNodes[1] + '.output' ) , (  moacNodes[2] + '.color1'  ) )	
		mc.setAttr( (  moacNodes[2] + '.color2R' )  , 1 )	
		mc.setAttr( (  moacNodes[2] + '.color2G' )  , 1 )	
		mc.setAttr( (  moacNodes[2] + '.color2B' )  , 1 )		
				 
		mc.connectAttr( ( moacNodes[2] + '.outputR' ) , (  moacSysNames[2] + '.scaleX'  ) )		
		mc.connectAttr( ( moacNodes[1] + '.outputG' ) , (  moacSysNames[2] + '.scaleY'  ) )
		mc.connectAttr( ( moacNodes[1] + '.outputB' ) , (  moacSysNames[2] + '.scaleZ'  ) )	
		
		# parentCluster
		
	
		mc.parent( clusterNames[1] , moacSysNames[2] )	
		
		
		# select
		
		mc.select( moacSysNames[1])
	
		
		
		return 1
		
	
		
		
	#_________________________________________________________________________________________________________________________________________________ buildRig		
		
	
		
	def buildRigButton( self ):
	
		selection = mc.ls( sl=True )
		
		nbrCam = 0
		
		for elem in selection :
			childrens = mc.listRelatives( elem , s = True )
			
			if( childrens == None ):
				continue
			
			if( mc.objectType( childrens[0] , isa = 'camera')  ):
				cam = elem
				nbrCam += 1
		
		if not( nbrCam == 1 ):
			mc.error( 'you must select one camera' )
			
		selection.remove( cam )
		
		
		self.buildRig( selection , cam )
	


