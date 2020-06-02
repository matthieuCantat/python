

'''
#******************************************************** BUILD EXEMPLE RIG CTRL
import maya.cmds as mc
import python
from python.classe.rigModuleProjector import *
reload(python.classe.rigModuleProjector)

mc.file( f = True , new = True )
#=================================================



#_________________________________BUILD

projA = rigModuleProjector( n = 'projector' , pos = [ [1,0,1,0,0,0,1,1,1] , [1,0,1,0,0,0,1,1,1] , [1,2,1,0,0,0,1,1,1] , [9,2,1,0,0,0,1,1,1] ] , form = 'cube' , colors = [17]  )    
projA.printBuild = 1
toExec = projA.build()
exec(toExec)


#_________________________________MIRROR

args = {}
args['value']             = [0,0,0 , 0,1,0 , 0,0,1]
args['mode']              = 'mirror'
args['pivot']             = [0,0,0 , 0,0,0 , 1,1,1]
args['namePrefix']        = ['r','l']
args['nameReplace']       = ['toto','tata']
args['nameIncr']          = ''
args['nameAdd']           = []
args['noneMirrorAxe']     = 4

mirrored = projA.duplicate( **args )

for elem in mirrored:
    elem.build()

for elem in mirrored:
    elem.delete()
    

#_________________________________TRANSFORM
args = {}
args['value']             = [-2.36 , 2.876 , -2.247 , -23.629 , 18.578 , 33.015 , 1 , 1 , 1 , 5 ]
args['mode']              = 'transform'
args['pivot']             = [ 5 , 0 , -1 , 0 ,0,0 , 1 , 1 , 1 ]
args['namePrefix']        = ['','']
args['nameReplace']       = ['','']
args['nameIncr']          = 'A'
args['nameAdd']           = []
args['noneMirrorAxe']     = 4


duplicated = projA.duplicate( **args )

for elem in duplicated:
    elem.build()

for elem in duplicated:
    elem.delete()
    
'''

#ATTR
from .rigModule import *            
from .rigCtrl import *          
from .rigStretchyJoint import *         
from .rigLightCone import *  
from .rigModuleChain import *   

class rigModuleProjector( rigModule ):

	def __init__( self , **args ):
		rigModule.__init__( self , **args )
		#CLASSE TYPE
		self.classeType = 'rigModuleProjector'
		#CLASSE BLUE PRINT
		self.Name.add( 'base'   , baseName = self.classeType )
		self.Pos.add( 'masterA' , replace = [0,0,0,0,0,0,1,1,1]  )
		self.Pos.add( 'masterB' , replace = [0,0,0,0,0,0,1,1,1]  )
		self.Pos.add( 'masterC' , replace = [0,2,0,0,0,0,1,1,1]  )
		self.Pos.add( 'masterD' , replace = [8,2,0,0,0,0,1,1,1]  )				
		self.Pos.add( 'masterE' , replace = [8,0,0,0,0,0,1,1,1]  )	

		self.Name.add( 'ctrlRoot'     , ref = self.Name.base , baseNameAppend = 'root'      )
		self.Name.add( 'chain'        , ref = self.Name.base , baseNameAppend = 'rot'       )	
		self.Name.add( 'ctrlTarget'   , ref = self.Name.base , baseNameAppend = 'target'    )
		self.Name.add( 'stretchyRotA' , ref = self.Name.base , baseNameAppend = 'stretchyA' )		
		self.Name.add( 'stretchyRotB' , ref = self.Name.base , baseNameAppend = 'stretchyB' )
		self.Name.add( 'lightCone'    , ref = self.Name.base , baseNameAppend = 'lightCone' )		

		self.CurveShape.add(  'root'      , value = { 'form' : 'crossArrow' , 'colors' : ['green']  , 'axe' : 'y' , 'offset' : [0,0,0,0,0,0,1,1,1] }  )
		self.CurveShape.add(  'rotation'  , value = { 'form' : 'cylinder'   , 'colors' : ['red']    , 'axe' : 'x' , 'offset' : [0,0,0,0,0,0,1,1,1] }  )
		self.CurveShape.add(  'target'    , value = { 'form' : 'cube'       , 'colors' : ['yellow'] , 'axe' : 'x' , 'offset' : [0,0,0,0,0,0,1,1,1] }  )

		self.CtrlRoot     = rigCtrl(           n = self.Name.ctrlRoot      , pos = [ self.Pos.masterA ]                     , ctrlScale = self.ctrlScale     , shape = self.CurveShape.root     , parent = self.Name.ctrlGrp  )	
		self.Chain        = rigModuleChain(    n = self.Name.chain         , pos = [ self.Pos.masterB  , self.Pos.masterC ] , ctrlScale = self.ctrlScale*0.2 , shape = self.CurveShape.rotation  )	
		self.CtrlTarget   = rigCtrl(           n = self.Name.ctrlTarget    , pos = [ self.Pos.masterD ]                     , ctrlScale = self.ctrlScale*0.5 , shape = self.CurveShape.target   , modif = True , parent = self.Name.ctrlGrp  )
		self.StretchyRotA = rigStretchyJoint(  n = self.Name.stretchyRotA  , pos = [ self.Pos.masterB , self.Pos.masterE ]  , parent = self.Name.rigGrp       )			
		self.StretchyRotB = rigStretchyJoint(  n = self.Name.stretchyRotB  , pos = [ self.Pos.masterC , self.Pos.masterD ]  , parent = self.Name.rigGrp       )			
		self.LightCone    = rigLightCone(      n = self.Name.lightCone     , pos = [ self.Pos.masterC , self.Pos.masterD ]  , parent = self.Name.skeletonGrp  )


		self.Link.add( 'paRootTarget'       , Sources = [ self.CtrlRoot.outs[0]     ] , Destinations = [ self.CtrlTarget.ins[0]   ] , type = 'parent' , operation = 'oneMaster' ,  maintainOffset = 1 )		
		self.Link.add( 'paRootChain0'       , Sources = [ self.CtrlRoot.outs[0]     ] , Destinations = [ self.Chain.ins[0]        ] , type = 'parent' , operation = 'oneMaster' ,  maintainOffset = 1 )		

		self.Link.add( 'paRootStretchyA0'   , Sources = [ self.CtrlRoot.outs[0]     ] , Destinations = [ self.StretchyRotA.ins[0] ] , type = 'parent' , operation = 'oneMaster' ,  maintainOffset = 1 )
		self.Link.add( 'poTargetStretchyA1' , Sources = [ self.CtrlTarget.outs[0]   ] , Destinations = [ self.StretchyRotA.ins[1] ] , type = 'point'  , operation = 'oneMaster' ,  maintainOffset = 0  , skipAxes = [0,1,0 ,1,1,1 , 1,1,1]  )		

		self.Link.add( 'oStretchyAChain1'   , Sources = [ self.StretchyRotA.outs[0] ] , Destinations = [ self.Chain.ins[1]        ] , type = 'orient' , operation = 'oneMaster' ,  maintainOffset = 1 )

		self.Link.add( 'paChain0StretchyB0' , Sources = [ self.Chain.outs[0]        ] , Destinations = [ self.StretchyRotB.ins[0] ] , type = 'parent' , operation = 'oneMaster' ,  maintainOffset = 1 )
		self.Link.add( 'poTargetStretchyB1' , Sources = [ self.CtrlTarget.outs[0]   ] , Destinations = [ self.StretchyRotB.ins[1] ] , type = 'point'  , operation = 'oneMaster' ,  maintainOffset = 1  , skipAxes = [0,0,1 ,1,1,1 , 1,1,1]  )		

		self.Link.add( 'oStretchyBChain1'   , Sources = [ self.StretchyRotB.outs[0] ] , Destinations = [ self.Chain.ins[1]        ] , type = 'orient' , operation = 'oneMaster' ,  maintainOffset = 1 )

		self.Link.add( 'paChain1Cone0'      , Sources = [ self.Chain.outs[1]        ] , Destinations = [ self.LightCone.ins[0]    ] , type = 'parent' , operation = 'oneMaster' ,  maintainOffset = 1 )
		self.Link.add( 'paTargetCone1'      , Sources = [ self.CtrlTarget.Name.ctrl ] , Destinations = [ self.LightCone.ins[1]    ] , type = 'parent' , operation = 'oneMaster' ,  maintainOffset = 1 )		

		attrsName  = [ 'lightConeShape'  , 'intensity' , 'colorR'  , 'colorG'  , 'colorB'  , 'sizeStart' , 'sizeEnd' , 'keepProportion' , 'offset' ]
		attrsType  = [ 'separator'       , 'float'     , 'float'   , 'float'   , 'float'   , 'float'     , 'float'   , 'floatOnOff'     , 'float' ]		
		attrsValue = [  None             ,  1          ,    1      , 0.821     ,  0.39     ,   0.05      ,     1      ,     1            ,   2      ]
		self.Attr.add(  'ctrlTarget'  , Name = self.CtrlTarget.Name.ctrl , attrName = attrsName , attrType = attrsType , attrValue = attrsValue )

		attrsName  = [ 'intensity' , 'colorR' , 'colorG' , 'colorB' , 'sizeStart' , 'sizeEnd' , 'keepProportion' , 'offset' ]
		for attr in attrsName:
			exec( "self.Link.add( '{0}' , Sources = [ self.Attr.ctrlTarget.{0} ]  , Destinations = [ self.LightCone.Attr.topNode.{0} ] , type = 'simple' , operation = 'oneMaster' )".format( attr )	)

		#CLASSE UTILS
		self.SubRigs     = [ self.CtrlRoot , self.Chain , self.CtrlTarget , self.StretchyRotA , self.StretchyRotB , self.LightCone ]
		self.SubRigsName = [ 'CtrlRoot'    , 'Chain'    , 'CtrlTarget'    , 'StretchyRotA'    , 'StretchyRotB'    , 'LightCone'    ]
		self.ins         = [ self.CtrlRoot.ins[0]     , self.CtrlTarget.ins[1] ]
		self.outs        = [ self.CtrlRoot.outs[0]    , self.Chain.outs[0]     , self.Chain.outs[1]     , self.CtrlTarget.outs[0]    ]
		#self.outsToCtrls = [[self.CtrlRoot.Name.ctrl] ,[self.Chain.Name.ctrl0] ,[self.Chain.Name.ctrl1] ,[self.CtrlTarget.Name.ctrl] ]		
		#CLASSE MODIF
		#INSTANCE MODIF
		name       = args.get( 'n'     , None )	
		pos        = args.get( 'pos'   , None )
		shape      = args.get( 'shape' , None )
		form       = args.get( 'form'  , None )	
		colors     = args.get( 'colors'  , None )	
		aim        = args.get( 'aim'  , None )						
		#UPDATE
		if not( name == None ): self.Name.add( 'base', copy = name ) 
		if not( pos  == None ): 
			self.Pos.add( 'masterA' , replace = pos[0] )
			self.Pos.add( 'masterB' , replace = pos[1] )
			self.Pos.add( 'masterC' , replace = pos[2] )	
			self.Pos.add( 'masterD' , replace = pos[3] )	

		constraintOuts = args.get( 'constraintOuts' , True )	
		if not( pos == None ) and( type(pos[0]) == types.StringType ):
			if( mc.objExists(pos[0]) == True ):

				if( constraintOuts ):
					for i in range( 0 , len(pos) ):
						self.Name.add(  'out{}'.format(i) , copy = pos[i] , objExists = True )
						self.Link.add(  'out{}'.format(i)      , Sources = [ self.outs[i] ] , Destinations = [ eval('self.Name.out{}'.format(i) )  ] , type = 'parent' , operation = 'oneMaster'  )					
						self.Link.add(  'outScale{}'.format(i) , Sources = [ self.outs[i] ] , Destinations = [ eval('self.Name.out{}'.format(i) )  ] , type = 'scale'  , operation = 'oneMaster'  )

				fathers = mc.listRelatives( pos[0] , p = True )
				if not( fathers == None ):		
					self.Name.add(  'in0' , copy = fathers[0] , objExists = True )		
					self.Link.add(  'in0' , Sources = [eval('self.Name.in0' )] , Destinations = [ self.ins[0] ] , type = 'parent' , operation = 'oneMaster'  )					


		'''											
		if not( shape  == None ): self.CurveShape.add(  'ctrl'    , shape                 )
		if not( form   == None ): self.CurveShape.add(  'ctrl'    , { 'form'   : form   } )
		if not( colors == None ): self.CurveShape.add(  'ctrl'    , { 'colors' : colors } )	
		'''


	def postBuild( self ):
		#BUILD
		'''
		print( self.Attr.ctrlTarget.offset.str() )
		pA = self.Pos.masterC.value()
		pB = self.Pos.masterD.value()
		vector = om.MVector( pA[0] - pB[0] , pA[1] - pB[1] , pA[2] - pB[2] )
		dist   = vector.length()
		mc.setAttr( self.Attr.ctrlTarget.offset.str()  , dist )		
		# SET ATTR
		mc.setAttr( self.StretchyRotB.Name.topNode.str() + '.visibility' , 0)	
		mc.setAttr( self.StretchyRotA.Name.topNode.str() + '.visibility' , 0)					
		mc.setAttr( self.Attr.topNode.skeletonRef.str() , 2)		
		'''
		return ''



'''

class rigModuleProjector( rigModule ):
	

	
	def __init__( self ):

		#________________________________________TO MODIF <------------------------ START
		
		buildRigClass.buildRig.__init__(self)			

		self.rigType            = 'projector'
		self.baseName           = 'projectorRig'  	
		
		self.mainGrpSuffix      = '_projectorRig_grp'          
		self.subRigSuffix       = [ 'Root' , 'RotA' , 'RotB' , 'Target' , 'RotAOrient' , 'RotBOrient' , 'LightCone' ]	
		 		  
		self.buildTrs           = [ [0,0,0,0,0,0,1,1,1] , [0,0,0,0,0,0,1,1,1] , [0,0,0,0,0,0,1,1,1] , [0,0,0,0,0,0,1,1,1] ]
		self.buildTrsDupli      = [ [0,0,0,0,0,0,1,1,1] , [0,1.3,0,0,0,-90,0.8,0.8,0.8] , [0,2,0,0,0,-90,0.8,0.8,0.8] , [1.7,1.7,0,0,0,0,1,1,1] ]
		self.buildTrsDupli     += [ [0,0,0,0,0,0,0,0,0] , [0,0,0,0,0,0,0,0,0] , [0,0,0,0,0,0,0,0,0] , [0,0,0,0,0,0,0,0,0] ]
		self.buildTrsDupli     += [ [0,0,0,0,0,0,0,0,0] , [0,0,0,0,0,0,0,0,0] , [0,0,0,0,0,0,0,0,0] , [0,0,0,0,0,0,0,0,0] ]	
		
		# ATTR
		self.targetRotAttr = 'targetRot'
		
		# MANIPS OPTION
		
		self.root_animSet    = 1
		self.root_form       = 'crossArrow'
		self.root_shapeAxe   = 1
		self.root_color      = 'green'
		self.root_skn        = 1
		self.root_multiOrig  = 0
		self.root_customDv   = 0		

		self.rotA_animSet    = 1
		self.rotA_form       = 'arrow2SidesBend'
		self.rotA_shapeAxe   = 1
		self.rotA_color      = 'yellow'
		self.rotA_skn        = 1
		self.rotA_multiOrig  = 1
		self.rotA_customDv   = 0		

		self.rotB_animSet    = 1
		self.rotB_form       = 'arrow2SidesBend'
		self.rotB_shapeAxe   = 1
		self.rotB_color      = 'yellow'
		self.rotB_skn        = 1
		self.rotB_multiOrig  = 1
		self.rotB_customDv   = 0		

		self.target_animSet    = 0
		self.target_form       = 'cube'
		self.target_shapeAxe   = 1
		self.target_color      = 'red'
		self.target_skn        = 1
		self.target_multiOrig  = 0
		self.target_customDv   = 0		


		# PISTON OPTION
		
		self.rotAPiston_flipDirA = None
		self.rotBPiston_flipDirA = None	
		
		#________________________________________TO MODIF <------------------------ END
 

	#___________________________________________________________________________________________________________________________________________________________________ refreshNamesWithBaseName
	
	def refreshNamesWithBaseName(self):	

		buildRigClass.buildRig.refreshNamesWithBaseName(self)

		self.transLocA = self.baseName + 'rotATrans_loc' 		
		self.transLocB = self.baseName + 'rotBTrans_loc'  


	#___________________________________________________________________________________________________________________________________________________________________ fillAttrFromUI	
	
	def fillAttrFromUI( self , uiClass ):

		buildRigClass.buildRig.fillAttrFromUI( self , uiClass )	

	def fillAttrManualy( self , baseName , buildTrs , isSubRig = None , buildTrsDupli = None ):
		buildRigClass.buildRig.fillAttrManualy( self , baseName , buildTrs , isSubRig , buildTrsDupli )	

		self.stretchyRotATrs    = self.buildTrs[3][:]
		self.stretchyRotATrs[1] = self.buildTrs[1][1]
		
		
		vRotBRotA = [ self.buildTrs[1][0] - self.buildTrs[2][0] , self.buildTrs[1][1] - self.buildTrs[2][1] , self.buildTrs[1][2] - self.buildTrs[2][2]    ]
		
		self.rotAPiston_flipDirA = None
		self.rotBPiston_flipDirA = vRotBRotA	


#___________________________________________________________________________________________________________________________________________________________________ createManualy	
 	
 	def createSubRig( self ):

		buildRigClass.buildRig.createSubRig( self )
		
		self.subRigObjs = [] #<------ a remplir
	
		
		root_manipObj = buildRigClassManip.manip() 
		root_manipObj.fillAttrManualy(    self.subRigBaseNames[0] , [ self.buildTrs[0] ] , isSubRig = 1 , buildTrsDupli = [ self.buildTrsDupli[0] ] , animSet = self.root_animSet ,  shapeForm = self.root_form , shapeAxe = self.root_shapeAxe , indexColor = self.root_color , skn = self.root_skn , multiOrig = self.root_multiOrig , customDv = self.root_customDv ) 	
		root_manipObj.createManualy()	
		self.subRigObjs.append( root_manipObj )		
		
		rotA_manipObj = buildRigClassManip.manip() 
		rotA_manipObj.fillAttrManualy(    self.subRigBaseNames[1] , [ self.buildTrs[1] ] , isSubRig = 1 , buildTrsDupli = [ self.buildTrsDupli[1] ] , animSet = self.rotA_animSet ,  shapeForm = self.rotA_form , shapeAxe = self.rotA_shapeAxe , indexColor = self.rotA_color , skn = self.rotA_skn , multiOrig = self.rotA_multiOrig , customDv = self.rotA_customDv ) 	
		rotA_manipObj.createManualy()	
		self.subRigObjs.append( rotA_manipObj )	

		rotB_manipObj = buildRigClassManip.manip() 
		rotB_manipObj.fillAttrManualy(    self.subRigBaseNames[2] , [ self.buildTrs[2] ] , isSubRig = 1 , buildTrsDupli = [ self.buildTrsDupli[2] ] , animSet = self.rotB_animSet ,  shapeForm = self.rotB_form , shapeAxe = self.rotB_shapeAxe , indexColor = self.rotB_color , skn = self.rotB_skn , multiOrig = self.rotB_multiOrig , customDv = self.rotB_customDv ) 	
		rotB_manipObj.createManualy()	
		self.subRigObjs.append( rotB_manipObj )	

		target_manipObj = buildRigClassManip.manip() 
		target_manipObj.fillAttrManualy(  self.subRigBaseNames[3] , [ self.buildTrs[3] ] , isSubRig = 1 , buildTrsDupli = [ self.buildTrsDupli[3] ] , animSet = self.target_animSet ,  shapeForm = self.target_form , shapeAxe = self.target_shapeAxe , indexColor = self.target_color , skn = self.target_skn , multiOrig = self.target_multiOrig , customDv = self.target_customDv ) 	
		target_manipObj.createManualy()	
		self.subRigObjs.append( target_manipObj )	
		
		
		rotA_PistonObj = buildRigClassPiston.piston()
		rotA_PistonObj.fillAttrManualy(  self.subRigBaseNames[4]  , [ self.buildTrs[1]  , self.stretchyRotATrs ] , isSubRig = 1 , buildTrsDupli = self.buildTrsDupli[4:6]  , flipDirA = self.rotAPiston_flipDirA  ) 
		rotA_PistonObj.createManualy()			
		self.subRigObjs.append( rotA_PistonObj )

		rotB_PistonObj = buildRigClassPiston.piston()
		rotB_PistonObj.fillAttrManualy(  self.subRigBaseNames[5]  , [ self.buildTrs[2]  , self.buildTrs[3] ] , isSubRig = 1 , buildTrsDupli = self.buildTrsDupli[6:8]  , flipDirA = self.rotBPiston_flipDirA  ) 
		rotB_PistonObj.createManualy()			
		self.subRigObjs.append( rotB_PistonObj )
		

		lightConeObj = buildRigClassLightCone.lightCone()		
		lightConeObj.fillAttrManualy(  self.subRigBaseNames[6]  , [ self.buildTrs[2]  , self.buildTrs[3] ] , isSubRig = 1 , buildTrsDupli = self.buildTrsDupli[8:12]  ) 
		lightConeObj.createManualy()			
		self.subRigObjs.append( lightConeObj )
	

	def createRig( self ):
		#________________________________________TO MODIF <------------------------ START	

		buildRigClass.buildRig.createRig( self )
	
		self.alls = [] #<------ a remplir
		
		# DECLARATION
		
		root       = self.subRigObjs[0]
		rotA       = self.subRigObjs[1]		
		rotB       = self.subRigObjs[2]			
		target     = self.subRigObjs[3]	
		
		rotAPiston = self.subRigObjs[4]	
		rotBPiston = self.subRigObjs[5]	
		
		lightCone  = self.subRigObjs[6]			
		
		# BASE HIERARCHY	
		utilsMaya.createDagNodes( [ 'transform'  , 'transform'   , 'transform'  ]  , [ self.mainGrp , self.manipGrp , self.rigGrp  ] ,  [ ''   , self.mainGrp  , self.mainGrp ] )
		self.alls += [ self.mainGrp , self.manipGrp , self.rigGrp  ] 		
	
		# PARENT SUBRIG
		
		mc.parent( root.mainGrp   , self.manipGrp )
		mc.parent( rotA.mainGrp   , root.outs[0] )
		mc.parent( rotB.mainGrp   , rotA.outs[0] )
		mc.parent( target.mainGrp , root.outs[0])

		mc.parent( rotAPiston.mainGrp   , self.rigGrp )
		mc.parent( rotBPiston.mainGrp   , self.rigGrp )

		mc.parent( lightCone.mainGrp    , self.manipGrp )
		
		# ATTR
		for manip in [ rotA.ctrl , rotB.ctrl ]:
			utilsMaya.addSpecialAttr( manip , 'EXTRA_ATTR'      , 'separator' )		
			utilsMaya.addSpecialAttr( manip , self.targetRotAttr, 'floatOnOff' )

		
		# CONSTRAINT SUBRIG
		
		utilsMaya.buildConstraint( [ root.outs[0]   , rotAPiston.mainGrp ] , [ 'parent' ] , 'oneMaster' , 1 )		
		utilsMaya.buildConstraint( [ root.outs[0]   , rotAPiston.ins[0] ] , [ 'parent' ]  , 'oneMaster' , 1 )
		utilsMaya.buildConstraint( [ target.outs[0] , rotAPiston.ins[1] ] , [ 'point' ]   , 'oneMaster' , 1 , [ 0 , 1 , 0 , 1,1,1,1,1,1 ] )

		utilsMaya.buildConstraint( [ rotA.outs[0]   , rotBPiston.mainGrp ] , [ 'parent' ] , 'oneMaster' , 1 )			
		utilsMaya.buildConstraint( [ rotA.outs[0]   , rotBPiston.ins[0] ] , [ 'parent' ]  , 'oneMaster' , 1 )
		utilsMaya.buildConstraint( [ target.outs[0] , rotBPiston.ins[1] ] , [ 'point' ]   , 'oneMaster' , 1 , [ 0 , 0 , 1 , 1,1,1,1,1,1 ] )	
		
		# TRANS LOC		
	
		locNames   = [ self.transLocA        , self.transLocB    ]
		locTrs     = [ self.buildTrs[1]      , self.buildTrs[2]  ]
		locfathers = [ rotA.orig             , rotB.orig         ]
		locTypes   = [ 'locator'             , 'locator'         ]	
		utilsMaya.createDagNodes( locTypes , locNames , locfathers , locTrs )	
		self.alls  += locNames			

		# CONSTRAINT
		utilsMaya.buildConstraint( [ rotAPiston.outs[0]    , self.transLocA  ] , [ 'parent' ] , 'oneMaster' , 1 , [ 1 , 1 , 1 , 0,0,0,0,0,0 ] )		
		utilsMaya.buildConstraint( [ rotBPiston.outs[0]    , self.transLocB  ] , [ 'parent' ] , 'oneMaster' , 1 , [ 1 , 1 , 1 , 0,0,0,0,0,0 ]  )		

		# CONNECTION
		for axe in [ 'X' , 'Y' , 'Z' ]:
			utilsMaya.buildOffsetConnection( self.transLocA + '.rotate' + axe  , rotA.multiOrig + '.rotate' + axe , offsetAttrs = [ ['*' , rotA.ctrl +'.'+ self.targetRotAttr ] ] )
			utilsMaya.buildOffsetConnection( self.transLocB + '.rotate' + axe  , rotB.multiOrig + '.rotate' + axe , offsetAttrs = [ ['*' , rotB.ctrl +'.'+ self.targetRotAttr ] ] )		


		# LIGHT CONE SETUP
		utilsMaya.buildConstraint( [ rotB.outs[0]   , lightCone.ins[0] , lightCone.ins[1]  ] , [ 'parent' , 'scale' ] , 'oneMaster' , 1  )	

		# LIGHT CONE ATTR
		
		for i in range( 0 , len( lightCone.attrNames ) ):
			utilsMaya.addSpecialAttr( target.ctrl , lightCone.attrNames[i] , lightCone.attrType[i] )
			if not ( lightCone.attrType[i] == 'separator' ) and not ( lightCone.attrNames[i] == 'offsetDistance' ):
				mc.setAttr( target.ctrl +'.'+ lightCone.attrNames[i] , mc.getAttr( lightCone.ctrls[1] +'.'+ lightCone.attrNames[i] ) )
				mc.connectAttr( target.ctrl +'.'+ lightCone.attrNames[i] , lightCone.ctrls[1] +'.'+ lightCone.attrNames[i] )		
				
		utilsMaya.buildOffsetConnection( rotBPiston.mainGrp + '.distance' , lightCone.ctrls[1] + '.offsetDistance' , offsetAttrs = [ ['-' , rotBPiston.mainGrp +'.distanceBase' ] , ['+', target.ctrls[0] + '.offsetDistance' ] ] )
		
		
		# DV ATTR
		mc.setAttr( target.ctrl + '.sizeOrig' , -0.01 ) 		
		mc.setAttr( lightCone.manipGrp + '.visibility' , 0 ) 	
		
		mc.setAttr( self.transLocA + '.visibility' , 0 ) 
		mc.setAttr( self.transLocB + '.visibility' , 0 ) 		

		mc.setAttr( self.rigGrp + '.visibility' , 0 ) 			
		
		#to add at the end:		
	
		#____WRITE BUILD INFO

		buildTrs    = self.buildTrs
		ins         = [ root.mainGrp  ]
		ctrls       = [ root.ctrl , rotA.ctrl , rotB.ctrl , target.ctrl  ]	
		outs        = [ root.outs[0] , rotA.outs[0] , rotB.outs[0] ]
		subMainGrps = [ rigObj.mainGrp for rigObj in self.subRigObjs ]
		beacons     = subMainGrps 
		
		self.saveWriteMainGrpAttr(  self.mainGrp , self.rigType , buildTrs , ins , ctrls , outs , beacons , self.alls , subMainGrps )
		self.writeBeaconsAttr()							


		#________________________________________TO MODIF <------------------------ END	


		
	#___________________________________________________________________________________________________________________________________________________________________ fillAttrFromRig	
	
	def fillAttrFromRig( self , rigGrpName , masterRig = 1 ):

		
		buildRigClass.buildRig.fillAttrFromRig( self , rigGrpName , masterRig )

	#___________________________________________________________________________________________________________________________________________________________________ createFromSelectionOptionBox	
	
	def createFromSelectionOptionBox( self ):

		buildRigClass.buildRig.createFromSelectionOptionBox( self )							
	#___________________________________________________________________________________________________________________________________________________________________ createFromSelection	
	
	def createFromSelection( self ):
		
		buildRigClass.buildRig.createFromSelection( self )			
			
	#___________________________________________________________________________________________________________________________________________________________________ createManualy	
	
	def createManualy( self ):
	
		buildRigClass.buildRig.createManualy( self )


	#___________________________________________________________________________________________________________________________________________________________________ createSubRigMirror			

 	def createSubRigMirror( self , planSymCoords , lockAxe , inverseAxes ,  prefix , replace  ):

		buildRigClass.buildRig.createSubRigMirror( self , planSymCoords , lockAxe , inverseAxes ,  prefix , replace  )
		
	#___________________________________________________________________________________________________________________________________________________________________ createMirror	
	
	def createMirror( self , planSymCoords , lockAxe , inverseAxes ,  prefix , replace  ):	

 		buildRigClass.buildRig.createMirror( self , planSymCoords , lockAxe , inverseAxes ,  prefix , replace  )
 		
	#___________________________________________________________________________________________________________________________________________________________________ changeBaseName
	
	def changeBaseName( self , newBaseName , incr = 0 , renameSubRig = 1 ):

 		buildRigClass.buildRig.changeBaseName( self , newBaseName , incr  , renameSubRig  )		

	#___________________________________________________________________________________________________________________________________________________________________ getMainGrp	

	def getMainGrp( self , elem  , masterRig = 0 ):
		

		
 		return buildRigClass.buildRig.getMainGrp( self , elem  , masterRig  )		
		
	#___________________________________________________________________________________________________________________________________________________________________ isElem	
	
	def isElem( self , elemToAnalyse  , masterRig = 1 ):

 		return buildRigClass.buildRig.isElem( self , elemToAnalyse  , masterRig  )			
			
	#___________________________________________________________________________________________________________________________________________________________________ saveWriteMainGrpAttr	
	
	def saveWriteMainGrpAttr( self ,  mainGrp = '' , rigType = '' , buildTrs = [] , ins = [] , ctrls = [] , outs = [] , beacons = [] ,  alls = [] , subMainGrps = [] ):
	
 		return buildRigClass.buildRig.saveWriteMainGrpAttr( self ,  mainGrp , rigType , buildTrs , ins , ctrls , outs  , beacons  ,  alls  , subMainGrps )
 		
	#___________________________________________________________________________________________________________________________________________________________________ readMainGrpAttr
	
	def readMainGrpAttr( self , mainGrp ):


 		return buildRigClass.buildRig.readMainGrpAttr( self , mainGrp )
 		
	#___________________________________________________________________________________________________________________________________________________________________ writeBeaconsAttr	
	
	def writeBeaconsAttr( self ):

 		return buildRigClass.buildRig.writeBeaconsAttr( self )	
		
	#___________________________________________________________________________________________________________________________________________________________________ readBeaconAttr
	
	def readBeaconAttr( self , beacon ):

 		return buildRigClass.buildRig.readBeaconAttr( self , beacon )			
		




'''		