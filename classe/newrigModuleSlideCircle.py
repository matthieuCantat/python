
import maya.cmds as mc

from ..utils import utilsMaya
from ..utils import utilsMayaApi

from . import buildRigClass	
from . import buildRigClassManip
from . import buildRigClassPiston

class rigModuleSlideCircle( rigModule ):
	
	'''
	________________________ TO MODIF	
	__init__
	refreshNamesWithBaseName
	fillAttrFromUI
	fillAttrManualy
	createSubRig
	createRig
	fillAttrFromRig
	________________________ STRUCTURE	
	createFromSelection
	createManualy
	createSubRigMirror
	createMirror
	changeBaseName
	getMainGrp
	isElem
	saveWriteMainGrpAttr
	readMainGrpAttr
	writeBeaconsAttr
	readBeaconAttr
	'''
	
	
	def __init__( self ):
	
		'''
		# MAIN GRP ATTR
		self.insAttr          = 'ins'		
		self.ctrlsAttr        = 'ctrls'	
		self.outsAttr         = 'outs'
		self.beaconsAttr      = 'beacons'		
		self.allsAttr         = 'alls'
		self.subMainGrpsAttr  = 'subMainGrps'

		self.rigTypeAttr      = 'rigType'	
		self.buildTrsAttr     = 'buildTrs'

		# BEACONS GRP ATTR
		self.mainGrpAttr      = 'mainGrp'	
		
		# CLASSES INFO
		self.dico_rigType_classImport = { 'manip':'from . import manipClass' , 'pistonRig':'from . import pistonRigClass' , 'tubeRig':'from . import tubeRigClass' , 'armRig':'from . import armRigClass' , 'slideCircleRig':'from . import slideCircleRigClass'    }		
		self.dico_rigType_classBuild  = { 'manip':'manipClass.manip()'       , 'pistonRig':'pistonRigClass.pistonRig()'   , 'tubeRig':'tubeRigClass.tubeRig()'     , 'armRig':'armRigClass.armRig()'      , 'slideCircleRig':'slideCircleRigClass.slideCircleRig()' }		
		
		# EMPTY VAR			
		self.subRigObjs         = []
		'''
		
		#________________________________________TO MODIF <------------------------ START
		
		buildRigClass.buildRig.__init__(self)			
		'''		
		  ------>fill this attr and add others 		  		  
		'''				
		
		self.rigType            = 'slideCircle'
		self.baseName           = 'slideCircle'  	
		
		self.mainGrpSuffix      = 'CircleSlideRig_grp'          
		self.subRigSuffix       = [ 'Root' , 'Offset' , 'Piston'] 
		 		  
		self.buildTrs           = [ [  0 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1 ] , [  1 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1 ] , [ -1 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1 ] ]
		self.buildTrsDupli      = [ [0,1.5,0,0,0,0,1,1,1] , [0,0,0,0,0,0,1,1,1] , [0,0,0,0,0,0,0,0,0] , [0,0,0,0,0,0,0,0,0] ] 
	
		#______ attr name 		
		self.slideDirectionAttr = 'switchDirection' 
		self.rotationAttr       = 'holdOrient'
				
		#_______subRig		
		self.rootObj        = None
		self.manipOffsetObj = None
		self.pistonRigObj   = None
		
		#_______manip option
		
		self.root_animSet      = 0
		self.root_form         = 'sphere'
		self.root_shapeAxe     = 1
		self.root_color        = 'red'
		self.root_skn          = 0
		self.root_multiOrig    = 0
		self.root_customDv     = 0				

		self.offset_animSet    = 0
		self.offset_form       = 'plane'
		self.offset_shapeAxe   = 1
		self.offset_color      = 'red'
		self.offset_skn        = 1
		self.offset_multiOrig  = 0
		self.offset_customDv   = 0	

		
		#________________________________________TO MODIF <------------------------ END
 

	#___________________________________________________________________________________________________________________________________________________________________ refreshNamesWithBaseName
	
	def refreshNamesWithBaseName(self):	
		'''
		# main Hierarchy		
		self.mainGrp       = self.baseName + self.mainGrpSuffix
		self.manipGrp      = self.baseName + '_manips_grp' 
		self.rigGrp        = self.baseName + '_rig_grp' 
			
		#baseName subRig
		self.subRigBaseNames = []
		for suffix in self.subRigSuffix:
			self.subRigBaseNames.append( self.baseName + suffix )	
		'''
		
		#________________________________________TO MODIF <------------------------ START	
		
		buildRigClass.buildRig.refreshNamesWithBaseName(self)
		
		'''		
			------> add some attrs which depend on baseName 			
		'''	
		
		self.leadA     = self.baseName + 'LeadA_loc'
		self.leadB     = self.baseName + 'LeadB_loc'
		self.locSysGrp = self.baseName + 'LocSysGrp_loc'
		self.middle    = self.baseName + 'Middle_loc'
		self.center    = self.baseName + 'Center_loc'
		self.radius    = self.baseName + 'Radius_loc'
		
		self.expName   = self.baseName + 'CircleSlide_EXP' 
		
		#________________________________________TO MODIF <------------------------ END		
		


	#___________________________________________________________________________________________________________________________________________________________________ fillAttrFromUI	
	
	def fillAttrFromUI( self , uiClass ):
		#________________________________________TO MODIF <------------------------ START	
		
		buildRigClass.buildRig.fillAttrFromUI( self , uiClass )	
		
		'''		
			------> add some attrs if you using an UI 			
		'''	

		#________________________________________TO MODIF <------------------------ END	
		

	#___________________________________________________________________________________________________________________________________________________________________ fillAttrManualy	
	
	def fillAttrManualy( self , baseName , buildTrs , isSubRig = None , buildTrsDupli = None ):
		'''
		self.baseName  = baseName
		self.refreshNamesWithBaseName()
		self.buildTrs = buildTrs 
		'''
		#________________________________________TO MODIF <------------------------ START	
		
		buildRigClass.buildRig.fillAttrManualy( self , baseName , buildTrs , isSubRig , buildTrsDupli )	
		
		'''		
			make calcule for filling attribute 		
		'''	
		
		# DECLARATION	
		self.centerTrs  = self.buildTrs[0][0:6] + [1,1,1]
		self.borderATrs = self.buildTrs[1][0:6] + [1,1,1]
		self.borderBTrs = self.buildTrs[2][0:6] + [1,1,1]

		
		self.borderMidTrs  = [ 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1 ]			
		self.rootTrs       = [ 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1 ]		 		
		self.manipTrs      = [ 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1 ]			
		self.rootShapeTrs  = [ 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1 ]	
		
		# MIDDLE 		
		for i in range( 0 , 9 ): 		
			self.borderMidTrs[i] = ( self.borderATrs[i] + self.borderBTrs[i] ) / 2				

		# ROOT & MANIP
			
		vborderAB  = [ 0 , 0 , 0 ]
		vMidCenter = [ 0 , 0 , 0 ]
		vZ         = [ 0 , 0 , 1 ]
			
		for i in range( 0 , 3 ): 		
			vborderAB[i]  =  self.borderATrs[i]   - self.borderBTrs[i] 
			vMidCenter[i] =  self.borderMidTrs[i] - self.centerTrs[i] 			
						
		self.borderMidTrs[3:6] = utilsMayaApi.API_convertTripleVecteurToEulerRot( vborderAB , vMidCenter , vZ )	
		
		self.rootTrs   = self.borderMidTrs[0:3] + utilsMayaApi.API_convertTripleVecteurToEulerRot( vborderAB , vMidCenter , vZ ) + [ 1 , 1 , 1 ]	 		
		self.manipTrs  = self.centerTrs[0:3]    + utilsMayaApi.API_convertTripleVecteurToEulerRot( vborderAB , vMidCenter , vZ ) + [ 1 , 1 , 1 ]	 	

		
		# ROOT SHAPE
		
		centerUpT = [ 0 , 0 , 0 ]		
		for i in range( 0 , 3 ): 		
			centerUpT[i] = self.borderMidTrs[i] + vMidCenter[i]
			
		self.rootShapeTrs = centerUpT + utilsMayaApi.API_convertTripleVecteurToEulerRot( vborderAB , vMidCenter , vZ ) + [ 1 , 1 , 1 ]			

		#________________________________________TO MODIF <------------------------ END	
		
	
#___________________________________________________________________________________________________________________________________________________________________ createManualy	
 	
 	def createSubRig( self ):
		#________________________________________TO MODIF <------------------------ START		
		
		buildRigClass.buildRig.createSubRig( self )
		
		'''	 
			 create all the subRig you want here , subRig is a classRig 
			
			you have:			 
				self.subRigBaseNames  -------> the base name of all subRig you want to create
				self.subRigObjs = []      <--- a remplir avec l'obj de chaque rigs !!
		
		'''

		self.subRigObjs = [] #<------ a remplir
 
		rootObj = buildRigClassManip.manip() 
		rootObj.fillAttrManualy( self.subRigBaseNames[0] , [ self.rootTrs ] , isSubRig = 1 , buildTrsDupli = [ self.buildTrsDupli[0] ] , shapeTrsValue = self.rootShapeTrs , animSet = self.root_animSet ,  shapeForm = self.root_form , shapeAxe = self.root_shapeAxe , indexColor = self.root_color , skn = self.root_skn , multiOrig = self.root_multiOrig , customDv = self.root_customDv )	
		rootObj.createManualy()
		self.subRigObjs.append( rootObj )		
				
		manipOffsetObj = buildRigClassManip.manip()
		manipOffsetObj.fillAttrManualy( self.subRigBaseNames[1] , [ self.manipTrs ] , isSubRig = 1 , buildTrsDupli = [ self.buildTrsDupli[1] ], animSet = self.offset_animSet ,  shapeForm = self.offset_form , shapeAxe = self.offset_shapeAxe , indexColor = self.offset_color , skn = self.offset_skn , multiOrig = self.offset_multiOrig , customDv = self.offset_customDv )
		manipOffsetObj.createManualy()			
		self.subRigObjs.append( manipOffsetObj )  	
		
		pistonRigObj = buildRigClassPiston.piston()
		pistonRigObj.fillAttrManualy( self.subRigBaseNames[2] , self.buildTrs[1:3] , isSubRig = 1 , buildTrsDupli = self.buildTrsDupli[2:4] )
		pistonRigObj.createManualy()			
		self.subRigObjs.append( pistonRigObj ) 
		
		#________________________________________TO MODIF <------------------------ END	
		
		
	#___________________________________________________________________________________________________________________________________________________________________ createRig	

	def createRig( self ):
		#________________________________________TO MODIF <------------------------ START	

		buildRigClass.buildRig.createRig( self )
		
		'''	 
			 build the rig  a partir des subRig deja cree 
			 
			you have:
				self.mainGrp   
				self.manipGrp  
				self.rigGrp    					
				self.subRigObjs  -------> the obj of all subRig  
			 	self.buildTrs -------> world trsValue of selection
		 
			 self.alls = []    # a remplir avec chaque element cree dans createRig!!!!! 
		 
		'''		
		self.alls = [] #<------ a remplir
		
		# DECLARATION
		
		root   = self.subRigObjs[0]
		manip  = self.subRigObjs[1]		
		piston = self.subRigObjs[2]			

		# BASE HIERARCHY	

		utilsMaya.createDagNodes( [ 'transform'  , 'transform'   , 'transform'  ]  , [ self.mainGrp , self.manipGrp , self.rigGrp  ] , [ ''  , self.mainGrp  , self.mainGrp ] )
		self.alls += [ self.mainGrp , self.manipGrp , self.rigGrp  ] 
		
		# MANIP ATTR			
		utilsMaya.addSpecialAttr( root.ctrl , 'EXTRA_ATTR' , 'separator' )	
		
		objAttrName = utilsMaya.addSpecialAttr( root.ctrl , self.slideDirectionAttr  , 'float1'    )
		mc.addAttr( objAttrName , e = True , min = -1 , max = 1 , dv = -1  )
		mc.setAttr( objAttrName , -1 )
		
		objAttrName = utilsMaya.addSpecialAttr( root.ctrl , self.rotationAttr        , 'float1'    )	
		mc.addAttr( objAttrName , e = True , min = 0  , max = 1  )	
		
		# LEAD LOC
		
		locNames   = [ self.leadA        , self.leadB        , self.locSysGrp    , self.middle        , self.center     , self.radius        ]
		locTrs     = [ self.borderATrs   , self.borderBTrs   , self.borderMidTrs , self.borderMidTrs  , self.centerTrs  , self.borderATrs    ]
		locfathers = [ root.ctrl         , root.ctrl         , self.rigGrp       , self.locSysGrp     , self.middle     , self.center        ]
		locTypes   = [ 'locator'         , 'locator'         , 'transform'       ,'locator'           , 'locator'       , 'locator'          ]	
		utilsMaya.createDagNodes( locTypes , locNames , locfathers , locTrs )	
		self.alls  += locNames		
	
		# PARENT & CONSTRAINT
		
		utilsMaya.buildConstraint( [ self.leadA      , piston.ins[0]  ,  self.leadB   , piston.ins[1]    ] , [ 'parent' , 'scale' ] , '2by2' , 1 )	
		
		mc.parent( root.mainGrp   , self.manipGrp )
		mc.parent( manip.mainGrp  , self.manipGrp )		
		mc.parent( piston.mainGrp  , self.rigGrp   )		
		
		utilsMaya.buildConstraint( [ root.ctrl       ,  self.locSysGrp    ] , [ 'parent' , 'scale' ] , 'oneMaster' , 1 )
		utilsMaya.buildConstraint( [ root.ctrl       ,  self.center       ] , [ 'orient'           ] , 'oneMaster' , 1 )		
		utilsMaya.buildConstraint( [ piston.ctrls[0] ,  self.middle       ] , [ 'parent'           ] , 'oneMaster' , 1 )		
		utilsMaya.buildConstraint( [ self.center     ,  manip.orig        ] , [ 'parent' , 'scale' ] , 'oneMaster' , 1 )

		orientConstraintRoot = mc.listRelatives( self.center , c = True , type = 'orientConstraint' )
		mc.connectAttr( root.ctrl + '.' + self.rotationAttr , orientConstraintRoot[0] + '.' + root.ctrl + 'W0' )
		
		# SLIDE EXPRESSION
		
		scaleConstraintRoot = mc.listRelatives( self.middle , c = True , type = 'scaleConstraint' )
		scaleConstraintRootWAttr =  piston.ctrls[0] + 'W0'
		
		expContent  = ''
		expContent += '\n'		
		expContent += '\n' + 'vector $vRayon        = << {0}.translateX , {0}.translateY , {0}.translateZ >>;'.format( self.radius )
		expContent += '\n' + 'float $distLeadMiddle = {0}.{1} / 2 ;'.format( piston.mainGrp , piston.distAttrNames[1] )
		expContent += '\n'
		expContent += '\n' + 'float $h = 0;'		
		expContent += '\n' + 'float $stretchMode = 1;'
		expContent += '\n'		
		expContent += '\n' + 'if( mag($vRayon) >  $distLeadMiddle )'		
		expContent += '\n' + '{'
		expContent += '\n' + '	$h = sqrt( pow( mag($vRayon) , 2 ) - pow( $distLeadMiddle , 2 ) );'		
		expContent += '\n' + '	$stretchMode = 0 ;'	
		expContent += '\n' + '}'	
		expContent += '\n'				
		expContent += '\n' + '{0}.translateY                           =  $h * {1}.{2};'.format( self.center , root.ctrl , self.slideDirectionAttr )
		
		utilsMaya.buildSimpleExpression( self.expName  , expContent )		
		
		self.alls.append(self.expName)	
		
		# DV VALUE
		
		mc.setAttr( self.rigGrp + '.visibility' , 0 ) 
	
		
		# WRITE BUILD INFO		
	
		#____WRITE BUILD INFO		                                    
		buildTrs    = self.buildTrs
		ins         = [ root.mainGrp , self.leadA , self.leadB  ]
		ctrls       = [ root.ctrl , manip.ctrl  ]
		outs        = manip.outs 
		subMainGrps = [ rigObj.mainGrp for rigObj in self.subRigObjs ]
		beacons     = subMainGrps 
		
		self.saveWriteMainGrpAttr(  self.mainGrp , self.rigType , buildTrs , ins , ctrls , outs , beacons , self.alls , subMainGrps )
		self.writeBeaconsAttr()							
	
		#________________________________________TO MODIF <------------------------ END	


		
	#___________________________________________________________________________________________________________________________________________________________________ fillAttrFromRig	
	
	def fillAttrFromRig( self , rigGrpName , masterRig = 1 ):

		'''
		# get the main Grp
		self.getMainGrp(rigGrpName , masterRig  )
		
		# get the other attr
		self.readMainGrpAttr( self.mainGrp )	
		
		# get the baseName
		self.baseName = self.mainGrp.split( self.mainGrpSuffix )[0]		
		
		self.fillAttrManualy( self.baseName , self.buildTrs )
		'''
		
		buildRigClass.buildRig.fillAttrFromRig( self , rigGrpName , masterRig )

	#___________________________________________________________________________________________________________________________________________________________________ createFromSelectionOptionBox	
	
	def createFromSelectionOptionBox( self ):
		'''
		self.optionBoxNames   = [ 'option1'      , 'option2'      , 'option3'      , 'optionToto'  ]
		self.optionBoxAttrs   = [ 'self.option1' , 'self.option1' , 'self.option1' , 'self.option1']		
		self.optionBoxTypes   = [ 'checkBox'     , 'textField'    , 'checkBox'     , 'textField'   ]			
		'''
		buildRigClass.buildRig.createFromSelectionOptionBox( self )							
	#___________________________________________________________________________________________________________________________________________________________________ createFromSelection	
	
	def createFromSelection( self ):
		
		'''
		selection = mc.ls( sl = True )	
	
		for i in range( 0 , len( selection ) , len( self.buildTrs ) ):
			
			
			#____on verifie si on a suffisement d'element pour cree le rig
			try:
				for j in range( 0 , len(self.buildTrs) ):
					toto = selection[i+j]
			except:
				break
			
				
			#____on rassemble les infos
			baseName = selection[i]
			buildTrs = []
			for j in range( 0 , len( self.buildTrs ) ):				
				buildTrs.append( utilsMaya.getWorldTrsValue( selection[i+j] ) )		
			
			#____build
			self.fillAttrManualy(  baseName , buildTrs  )
			self.createManualy()
		'''
		
		buildRigClass.buildRig.createFromSelection( self )			
			
	#___________________________________________________________________________________________________________________________________________________________________ createManualy	
	
	def createManualy( self ):
		'''
		self.createSubRig()
		self.createRig()		
 		'''			
		buildRigClass.buildRig.createManualy( self )


	#___________________________________________________________________________________________________________________________________________________________________ createSubRigMirror			

 	def createSubRigMirror( self , planSymCoords , lockAxe , inverseAxes ,  prefix , replace  ):
 		'''
		self.subRigObjs = []  			
		rigObj          = None		
		subMainGrps     = self.subMainGrps
		
		for rigGrp in self.subMainGrps:
			
			rigType = mc.getAttr( rigGrp + '.' + self.rigTypeAttr )

			exec( '{0}'.format(          self.dico_rigType_classImport[ rigType ]  ) )			
			exec( 'rigObj = {0}'.format( self.dico_rigType_classBuild[  rigType ]  ) )
			
			rigObj.fillAttrFromRig( rigGrp , masterRig = 0  )
			rigObj.createMirror( planSymCoords , inverseAxes ,  prefix , replace )
			self.subRigObjs.append( rigObj )
		'''
		buildRigClass.buildRig.createSubRigMirror( self , planSymCoords , lockAxe , inverseAxes ,  prefix , replace  )
		
	#___________________________________________________________________________________________________________________________________________________________________ createMirror	
	
	def createMirror( self , planSymCoords , lockAxe , inverseAxes ,  prefix , replace  ):	
		'''
		self.createSubRigMirror( planSymCoords , inverseAxes ,  prefix , replace )	
				
		oldBaseName = self.baseName		
		
		# OLD NAME
		self.changeBaseName( prefix[0] + self.baseName , incr = 0	, renameSubRig = 0)
		
		# NEW NAME
		self.baseName = oldBaseName 
		if( replace[0] in self.baseName ) and not( replace[0] == '' ):		
			splitTmp      = self.baseName.split( replace[0] )
			self.baseName = splitTmp[0] + replace[1] + splitTmp[1]	
			
		self.baseName = prefix[1] + self.baseName		

		# MIRROR

		newBuildTrs = []
		for trsValue in self.buildTrs:
			trsValueTmp = utilsMayaApi.mirrorTrsValue( trsValue , planSymCoords ) 
	

			if( inverseAxes == [ 0 , 0 , 0 ] ):
				pass
			elif( inverseAxes == [ 1 , 1 , 0 ]  ):
				trsValueTmp[3:6] = utilsMayaApi.API_rotOffsetInsideEulerRot( trsValueTmp[3:6] , [ 0 , 0 , 180 ] )
			elif( inverseAxes == [ 1 , 0 , 1 ]  ):
				trsValueTmp[3:6] = utilsMayaApi.API_rotOffsetInsideEulerRot( trsValueTmp[3:6] , [ 0 , 180 , 0 ] )
			elif( inverseAxes == [ 0 , 1 , 1 ]  ):
				trsValueTmp[3:6] = utilsMayaApi.API_rotOffsetInsideEulerRot( trsValueTmp[3:6] , [ 180 , 0 , 0 ] )
					
			newBuildTrs.append( trsValueTmp )	
			
		self.fillAttrManualy( self.baseName , newBuildTrs ) 	
		self.createRig()	
		'''
 		buildRigClass.buildRig.createMirror( self , planSymCoords , lockAxe , inverseAxes ,  prefix , replace  )
 		
	#___________________________________________________________________________________________________________________________________________________________________ changeBaseName
	
	def changeBaseName( self , newBaseName , incr = 0 , renameSubRig = 1 ):
		
		'''
		
		# CHECK BASENAME		
		oldBaseName   = self.baseName
		if( incr == 1):
			self.baseName = utilsMaya.incrBaseNameIfExist( newBaseName  ,  [ '' , 'r_' , 'l_']  ,  [ '_ctrl' , '_skn' , self.mainGrpSuffix] )
		else:
			self.baseName = newBaseName		
			
		self.refreshNamesWithBaseName()	
			
		# RENAME SUBRIG
		
		if( renameSubRig == 1 ):
			
			for i in range( 0 ,  len( self.subMainGrps ) ):				
				rigType = mc.getAttr( self.subMainGrps[i] + '.' + self.rigTypeAttr )
				exec( '{0}'.format(          self.dico_rigType_classImport[ rigType ]  ) )				
				exec( 'rigObj = {0}'.format( self.dico_rigType_classBuild[  rigType ]  ) )
				
				rigObj.fillAttrFromRig( self.subMainGrps[i] , masterRig = 0 )
				rigObj.changeBaseName( newBaseName + self.subRigSuffix[i]  , incr , renameSubRig )
			
		# RENAME ALL
		
		newAlls = []
		for elem in self.alls:
			newElem = elem.replace( oldBaseName , self.baseName )
			mc.rename( elem , newElem )
			newAlls.append( newElem )
				
		# ACTUALISE NAME IN MAIN GRP ATTRS
		
		newIns = []
		for elem in self.ins:
			newIn = elem.replace( oldBaseName , self.baseName )
			newIns.append( newIn )		
				
		newCtrls = []
		for elem in self.ctrls:
			newCtrl = elem.replace( oldBaseName , self.baseName )
			newCtrls.append( newCtrl )	
			
		newOuts = []
		for elem in self.outs:
			newOut = elem.replace( oldBaseName , self.baseName )
			newOuts.append( newOut )				

		newBeacons = []
		for elem in self.beacons:
			newBeacon = elem.replace( oldBaseName , self.baseName )
			newBeacons.append( newBeacon )				
	
		newSubMainGrps = []
		for elem in self.subMainGrps:			
			newSubMainGrp = elem.replace( oldBaseName , self.baseName )
			newSubMainGrps.append( newSubMainGrp )					

		
		self.saveWriteMainGrpAttr(  self.mainGrp , self.rigType , self.buildTrs , newIns , newCtrls , newOuts , newBeacons , newAlls , newSubMainGrps )
		self.writeBeaconsAttr()			
		'''
 		buildRigClass.buildRig.changeBaseName( self , newBaseName , incr  , renameSubRig  )		

	#___________________________________________________________________________________________________________________________________________________________________ getMainGrp	

	def getMainGrp( self , elem  , masterRig = 0 ):
		
		'''
			if masterRig == 0 prend le premier rig grp qui arrive
			if masterRig == 1 prend le dernier rig grp qui arrive		
		'''
		'''
		self.mainGrp = elem
		loop = 0
		
		if( masterRig == 1 ): 
			while( mc.objExists( self.mainGrp + '.' + self.mainGrpAttr )  ):
				self.mainGrp = mc.getAttr( self.mainGrp + '.' + self.mainGrpAttr )
				loop +=1
				if( loop > 400 ):
					mc.error('loop')
		else:
			if not( mc.objExists( self.mainGrp + '.' + self.rigTypeAttr ) ) and ( mc.objExists( self.mainGrp + '.' + self.mainGrpAttr ) ):
				self.mainGrp = mc.getAttr( self.mainGrp + '.' + self.mainGrpAttr )			
				
		return self.mainGrp 
		'''
		
 		return buildRigClass.buildRig.getMainGrp( self , elem  , masterRig  )		
		
	#___________________________________________________________________________________________________________________________________________________________________ isElem	
	
	def isElem( self , elemToAnalyse  , masterRig = 1 ):
		'''
		
		if not( mc.objExists( elemToAnalyse + '.' + self.mainGrpAttr ) ):
			return False
			
		self.getMainGrp(elemToAnalyse , masterRig )	
			
		rigType = mc.getAttr( self.mainGrp  + '.' + self.rigTypeAttr )
		
		if( rigType ==  self.rigType ):
			return True
		else:
			return False
		'''
 		return buildRigClass.buildRig.isElem( self , elemToAnalyse  , masterRig  )			
			
	#___________________________________________________________________________________________________________________________________________________________________ saveWriteMainGrpAttr	
	
	def saveWriteMainGrpAttr( self ,  mainGrp = '' , rigType = '' , buildTrs = [] , ins = [] , ctrls = [] , outs = [] , beacons = [] ,  alls = [] , subMainGrps = [] ):
		'''
		#save
	
		self.ins          = ins		
		self.ctrls        = ctrls		
		self.outs         = outs
		self.beacons      = beacons
		self.alls         = alls
		self.subMainGrps  = subMainGrps
		
		self.rigType      = rigType
		self.buildTrs     = buildTrs		
				
		#write			
		if not ( mc.objExists( mainGrp ) ):
			return 0
			
		self.mainGrp = mainGrp
		
		utilsMaya.writeStringAttr(        self.mainGrp   ,   self.rigTypeAttr       ,     self.rigType      )				
		utilsMaya.writeStringArrayAttr(   self.mainGrp   ,   self.insAttr           ,     self.ins          )			
		utilsMaya.writeStringArrayAttr(   self.mainGrp   ,   self.ctrlsAttr         ,     self.ctrls        )		
		utilsMaya.writeStringArrayAttr(   self.mainGrp   ,   self.outsAttr          ,     self.outs         )
		utilsMaya.writeStringArrayAttr(   self.mainGrp   ,   self.beaconsAttr       ,     self.beacons      )		
		utilsMaya.writeStringArrayAttr(   self.mainGrp   ,   self.allsAttr          ,     self.alls         )		
		utilsMaya.writeStringArrayAttr(   self.mainGrp   ,   self.subMainGrpsAttr   ,     self.subMainGrps  )
		
		for i in range( 0 , len( self.buildTrs ) ):
			utilsMaya.writeStringArrayAttr(   self.mainGrp   ,   self.buildTrsAttr + str(i)   ,     self.buildTrs[i]  )	
			
		return 1
		'''		
 		return buildRigClass.buildRig.saveWriteMainGrpAttr( self ,  mainGrp , rigType , buildTrs , ins , ctrls , outs  , beacons  ,  alls  , subMainGrps )
 		
	#___________________________________________________________________________________________________________________________________________________________________ readMainGrpAttr
	
	def readMainGrpAttr( self , mainGrp ):
		
		'''
		
		if not( mc.objExists( mainGrp) ) or not(  mc.objExists( mainGrp + '.' + self.rigTypeAttr ) ):		
			return 0			
		
		self.rigType          = mc.getAttr( self.mainGrp + '.' + self.rigTypeAttr )
		self.ins              = utilsMaya.readStringArrayAttr(   self.mainGrp   ,   self.insAttr          )
		self.ctrls            = utilsMaya.readStringArrayAttr(   self.mainGrp   ,   self.ctrlsAttr        )
		self.outs             = utilsMaya.readStringArrayAttr(   self.mainGrp   ,   self.outsAttr         )
		self.beacons          = utilsMaya.readStringArrayAttr(   self.mainGrp   ,   self.beaconsAttr      )		
		self.alls             = utilsMaya.readStringArrayAttr(   self.mainGrp   ,   self.allsAttr         )
		self.subMainGrps      = utilsMaya.readStringArrayAttr(   self.mainGrp   ,   self.subMainGrpsAttr  )

		
		self.buildTrs = [] 		
		for i in range( 0 , 100 ):
			if not(  mc.objExists( self.mainGrp + '.' + self.buildTrsAttr + str(i) )  ):
				break
			self.buildTrs.append( utilsMaya.readStringArrayAttr(   self.mainGrp   ,   self.buildTrsAttr + str(i) ) )		
					
		return 1
		'''

 		return buildRigClass.buildRig.readMainGrpAttr( self , mainGrp )
 		
	#___________________________________________________________________________________________________________________________________________________________________ writeBeaconsAttr	
	
	def writeBeaconsAttr( self ):
		'''
		for beacon in self.beacons:
			utilsMaya.writeStringAttr( beacon , self.mainGrpAttr , self.mainGrp )			
			
		return 1
		'''
 		return buildRigClass.buildRig.writeBeaconsAttr( self )	
		
	#___________________________________________________________________________________________________________________________________________________________________ readBeaconAttr
	
	def readBeaconAttr( self , beacon ):

		'''
		if not( mc.objExists( beacon ) ) or not(  mc.objExists( beacon + '.' + self.mainGrpAttr  )  ):		
			return 0	
			
		self.mainGrp = utilsMaya.readStringAttr( beacon , self.mainGrpAttr)				
			
		return 1
		'''
 		return buildRigClass.buildRig.readBeaconAttr( self , beacon )			





		