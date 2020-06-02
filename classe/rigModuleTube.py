


'''
#******************************************************** BUILD EXEMPLE RIG CTRL
import maya.cmds as mc
import python
from python.classe.rigModuleTube import *
reload(python.classe.rigModuleTube)

mc.file( f = True , new = True )
#=================================================


#_________________________________BUILD

armA = rigModuleTube( n = 'tube' , curve = 'curve1' )    
armA.build()

mc.setAttr( "tubeTop_GRP.skeletonVis" ,1)
mc.setAttr( "tubeTop_GRP.skeletonRef" ,2)

armA.delete()

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

mirrored = armA.duplicate( **args )

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


duplicated = armA.duplicate( **args )

for elem in duplicated:
    elem.build()

for elem in duplicated:
    elem.delete()


'''


import maya.cmds as mc
import maya.api.OpenMaya as ompy

from ..utils import utilsMath
from ..utils import utilsPython
from ..utils import utilsMaya
from ..utils import utilsMayaApi
from ..utils import utilsBin

#ATTR
from . import curveShape
from .coords import *
from .rigModule import *            
from .rigCtrl import *          
from .rigStretchyJoint import *         
from .rigModuleChain import *
from .rigStretchyJoint import *   

class rigModuleTube( rigModule ):

	def __init__( self , **args ):
		rigModule.__init__( self , **args )

		self.doFkDynamic    = args.get( 'fkDyn'        , None )	
		name                = args.get( 'n'            , None )	
		curve               = args.get( 'curve'        , None )	
		pos                 = args.get( 'pos'          , None )
		
		#CLASSE TYPE
		self.classeType = 'rigModuleTube'

		#CLASSE BLUE PRINT
		self.Name.add( 'base'   , baseName = self.classeType )
						
		#UPDATE
		self.pos = pos
		if not( curve == None ):
			CoordsCurve = coords() 
			coordsTmp = CoordsCurve.createFromObj(curve)
			pos = []
			self.pos = []
			for i in range(0,len(coordsTmp),3):
				trsTmp = [coordsTmp[i+0],coordsTmp[i+1],coordsTmp[i+2],0,0,0,1,1,1]
				pos.append( trsTmp )
				self.pos += [coordsTmp[i+0],coordsTmp[i+1],coordsTmp[i+2]] 

			#COMPUTE POS PV
			iMiddle = int(len(pos)/2)
			posCvMiddle = pos[iMiddle][0:3]
			posAverage = [ (pos[0][0] + pos[-1][0])/2 , (pos[0][1] + pos[-1][1])/2 , (pos[0][2] + pos[-1][2])/2 ]
			vMiddle = ompy.MVector( posCvMiddle[0] - posAverage[0] , posCvMiddle[1] - posAverage[1] , posCvMiddle[2] - posAverage[2] )
			vMiddle *= 1.2
			posPv = [ vMiddle[0] + posAverage[0] , vMiddle[1] + posAverage[1] , vMiddle[2] + posAverage[2] ] + [0,0,0,1,1,1] 

		if( pos == None ): pos = []


		self.CurveShape.add( 'ctrlMaster' , value = { 'form' : 'cylinder' , 'colors' : ['yellow'] , 'axe' : 'x' , 'offset' : [0,0,0,0,0,0,1,1,1] }  )        
		self.CurveShape.add( 'ctrl'       , value = { 'form' : 'sphere' , 'colors' : [13] , 'axe' : 'x' , 'offset' : [0,0,0,0,0,0,1,1,1] }  )     
		self.CurveShape.add( 'pv'        , value = { 'form' : 'sphere' , 'colors' : ['yellow'] , 'axe' : 'x' , 'offset' : [0,0,0,0,0,0,1,1,1] }  )           
		
		self.doJoint    = args.get( 'joint'      , None )   
		self.doOffset   = args.get( 'offset'     , None )

		self.SubRigs     = []
		self.SubRigsName = []
		self.ins         = []
		self.outs        = []
		self.outsToCtrls = []

		#MATER CTRLS
		self.Name.add( 'ctrlA' , ref = self.Name.base , type = 'CTRL' , baseNameAppend = 'A'  )
		self.Name.add( 'ctrlB' , ref = self.Name.base , type = 'CTRL' , baseNameAppend = 'B'  )
		self.Name.add( 'pv'    , ref = self.Name.base , type = 'CTRL' , baseNameAppend = 'Pv' )

		self.Pos.add(  'ctrlA' , replace = pos[0]  )        
		self.Pos.add(  'ctrlB' , replace = pos[-1] )  
		self.Pos.add(  'ctrlA' , aim     = pos[-1] )        
		self.Pos.add(  'ctrlB' , orient  = self.Pos.ctrlA   ) 
		self.Pos.add(  'pv'    , replace  = posPv  ) 
		self.Pos.add(  'pv'    , orient  = self.Pos.ctrlA  )

		self.CtrlA = rigCtrl( n = self.Name.ctrlA , pos = [ self.Pos.ctrlA ] , shape = self.CurveShape.ctrlMaster , joint = self.doJoint , offset = self.doOffset , ctrlScale = self.ctrlScale , ctrlVisPriority = 0 )
		self.CtrlB = rigCtrl( n = self.Name.ctrlB , pos = [ self.Pos.ctrlB ] , shape = self.CurveShape.ctrlMaster , joint = self.doJoint , offset = self.doOffset , ctrlScale = self.ctrlScale , ctrlVisPriority = 1 )
		self.Pv    = rigCtrl( n = self.Name.pv    , pos = [ self.Pos.pv    ] , shape = self.CurveShape.pv         , joint = None         , offset = None          , ctrlScale = self.ctrlScale , ctrlVisPriority = 2 )

		if not( curve == None  ): self.curveRef = curve

		# COMPUTE TUBE THICKNESS
		self.thickness = 1

		bbCoords = mc.xform( self.curveRef  , q = True , bb = True )
		vector   = ompy.MVector( bbCoords[3] - bbCoords[0] , bbCoords[4] - bbCoords[1] , bbCoords[5] - bbCoords[2] )
		length   = vector.length()

		bbThicknessRatio = 0.016
		self.thickness = 1
		self.outThickness = length * bbThicknessRatio * self.thickness

		# COMPUTE OUT MESH POLYCOUNT 
		Curve = curveShape.curveShape()
		curveLength = Curve.utils_getCurveLength( curve )
		lengthPolyCountRatio = 40.0
		self.polycount = int(curveLength*lengthPolyCountRatio)

		ctrlAttrs      = [ 'lengthScale' , 'thickness'       , 'polyCount'    ]
		ctrlAttrsType  = [ 'float'       , 'float'           , 'int'          ]
		ctrlAttrsValue = [ 1             , self.outThickness , self.polycount ]
		self.Attr.add( 'ctrl' , Name = self.CtrlB.Name.ctrl , attrName = ctrlAttrs , attrType = ctrlAttrsType , attrValue = ctrlAttrsValue )

		self.SubRigs     = [ self.CtrlA , self.CtrlB , self.Pv ]
		self.SubRigsName = [ 'CtrlA'    , 'CtrlB'    , 'Pv'    ]
		self.Parent.add(  "CtrlA" , Name = self.CtrlA.Name.topNode , parent = self.Name.ctrlGrp    )
		self.Parent.add(  "CtrlB" , Name = self.CtrlB.Name.topNode , parent = self.Name.ctrlGrp    )
		self.Parent.add(  "pv"    , Name = self.Pv.Name.topNode    , parent = self.Name.ctrlGrp    )
		self.Link.add(    "pv"    , Sources = [ self.CtrlA.outs[0] ] , Destinations = [ self.Pv.ins[0] ] , type = "parent" , operation = "oneMaster" , maintainOffset = 1 )
		self.ins         = [ self.CtrlA.ins[0]      ,  self.CtrlB.ins[0]     ,  self.Pv.ins[0]         ]
		self.outs        = [ self.CtrlA.outs[0]     ,  self.CtrlB.outs[0]    ,  self.Pv.outs[0]        ]
		self.outsToCtrls = [ [self.CtrlA.Name.ctrl] , [self.CtrlB.Name.ctrl] , [self.CtrlA.Name.ctrl]  ]

		# CTRLS
		for i in range( len(pos) ):
			self.Name.add( 'ctrl{}'.format(i) , ref = self.Name.base , type = 'CTRL' , baseNameAppend = '{}'.format(i) )
			self.Pos.add(  'ctrl{}'.format(i) , replace = pos[i]  )
			if( i < len(pos)-1 ):self.Pos.add(  'ctrl{}'.format(i) , aim    = pos[i+1]  )
			else                :self.Pos.add(  'ctrl{}'.format(i) , aim    = pos[i-1]  )
			#SUBRIG
			exec( 'self.Ctrl{0} = rigCtrl( n = self.Name.ctrl{0} , pos = [ self.Pos.ctrl{0} ] , shape = self.CurveShape.ctrl , joint = {1} , offset = {2} ,  ctrlVisPriority = 3 , ctrlScale = {3}*1 )'.format(i , self.doJoint , self.doOffset , self.ctrlScale * 0.5 ) )
			exec( 'self.SubRigs.append(self.Ctrl{0})'.format(i) )
			exec( 'self.SubRigsName.append("Ctrl{0}")'.format(i) )
			#PARENT
			exec( 'self.Parent.add(  "Ctrl{0}" , Name = self.Ctrl{0}.Name.topNode , parent = self.Name.ctrlGrp    )'.format(i)      )
			exec( 'self.ins.append(self.Ctrl{0}.ins[0])'.format(i) )
			exec( 'self.outs.append(         self.Ctrl{0}.outs[0]     )'.format(i) )
			exec( 'self.outsToCtrls.append( [self.Ctrl{0}.Name.ctrl ] )'.format(i) )

		#SKELETON
		PositionTmp = []
		for i in range( len(pos) ):
		    exec('PositionTmp.append( self.Pos.ctrl{0} )'.format(i))
		#SUBRIG
		self.Name.add( 'skeleton' , ref = self.Name.base , baseNameAppend = 'skeleton' )    
		self.Joints = rigSkeletonChain( n = self.Name.skeleton , pos = PositionTmp , endJoint = False ) 
		#LINK
		for i in range( len(pos) ):
		    exec( 'self.Link.add( "skeleton{0}"      , Sources = [ self.Joints.outs[{0}] ] , Destinations = [ self.Ctrl{0}.ins[0] ] , type = "parent" , operation = "oneMaster" , maintainOffset = 0 )'.format(i) )  
		    exec( 'self.Link.add( "skeletonScale{0}" , Sources = [ self.Attr.ctrl.lengthScale ] , Destinations = [ self.Joints.Attr.joint{0}.scaleX ] , type = "simple" , operation = "oneMaster"  )'.format(i) )    
		#PARENT
		self.Parent.add( 'skeleton' , Name = self.Joints.Name.topNode , parent = self.Name.skeletonGrp )  
		#STORE
		self.SubRigs     += [ self.Joints ]
		self.SubRigsName += [ 'Joints' ]    

		#ik
		self.Name.add( 'handleIkSolver' , ref = self.Name.base , baseNameAppend = 'IkHandle' )
		self.Name.add( 'curve'          , ref = self.Name.base , baseNameAppend = 'curve' )
		self.Name.add( 'circle'         , ref = self.Name.base , baseNameAppend = 'circle' )

		#outGEO
		self.Name.add( 'outGeometry' , ref = self.Name.base , type = 'GEO' , baseNameAppend = 'out'  )


		if not( name  == None  ): self.Name.add( 'base' , copy = name ) 
		if not( pos   == None  ): pass
		


	def postBuild( self ):
		jointsNames = []
		for i in range( len(self.Joints.outs) ):
			exec('jointsNames.append( self.Joints.outs[{0}].str() )'.format(i))

		self.utils_prepareJointForIk( jointsNames )

		# IK___________CREATE SOLVER				
		mc.ikHandle( sj = self.Joints.outs[0].str() , ee = self.Joints.outs[-1].str() , sol = 'ikRPsolver' , n = self.Name.handleIkSolver.str() )
		mc.parent( self.Name.handleIkSolver.str() , self.Name.rigGrp.str()  )
		#mc.poleVectorConstraint( self.Pv.Name.ctrl.str() , self.Name.handleIkSolver.str() )	
		utilsMaya.buildConstraint( [ self.CtrlB.outs[0].str()  , self.Name.handleIkSolver.str()  ] , [ 'parent' , 'scale' ] , 'oneMaster' , 1 )			   
		utilsMaya.buildConstraint( [ self.CtrlA.outs[0].str()  , self.Joints.ins[0].str()        ] , [ 'parent'  ] , 'oneMaster' , 1 )		 	
		utilsMaya.buildConstraint( [ self.Pv.outs[0].str()     , self.Name.handleIkSolver.str()  ] , [ 'poleVector'  ] , 'oneMaster' , 0 )		 	
			
		# CREATE CURVE
		Curve = curveShape.curveShape()
		curveShapeName = Curve.utils_buildCurveShape( self.Name.curve.str() , 'None' , self.pos , 3 , 5  )
		
		ctrlsName = []
		for i in range( 3 , len(self.outs) ):
			ctrlsName.append(self.outs[i].str())
				
		Curve.utils_connectTransformsToCurve( ctrlsName , self.Name.curve.str() )
		mc.parent( self.Name.curve.str(), self.Name.rigGrp.str() )	

		# CREATE thicknessCuve
		circleShape = mc.circle( nr = [1,0,0] , n = self.Name.circle.str() )[0]
		utilsMaya.buildConstraint( [ self.Ctrl0.outs[0].str()  , self.Name.circle.str()  ] , [ 'parent'  ] , 'oneMaster' , 0 )		
		mc.connectAttr( self.Attr.ctrl.thickness.str() , self.Name.circle.str() + '.scaleX' ) 	
		mc.connectAttr( self.Attr.ctrl.thickness.str() , self.Name.circle.str() + '.scaleY' ) 			
		mc.connectAttr( self.Attr.ctrl.thickness.str() , self.Name.circle.str() + '.scaleZ' ) 
		mc.parent( self.Name.circle.str(), self.Name.rigGrp.str() )	

		#CREATE POLY TUBE
		extrudeOut  = mc.extrude( circleShape , self.Name.curve.str() , ch = True , rn = True , po = 1 , et = 2 , ucp = 1 , fpt = 0 , upn = 0 , rotation = 0 , scale = 1 , rsp = 1 ) ;
		extrudeMesh = extrudeOut[0]
		extrudeNode = extrudeOut[1]
		mc.rename( extrudeMesh , self.Name.outGeometry.str() )
		extrudeMesh = self.Name.outGeometry.str()
		#mc.parent( extrudeMesh , w = True )
		mc.setAttr( (extrudeNode + ".fixedPath") , 0)
		mc.setAttr( (extrudeNode + ".useComponentPivot") , 0)
		mc.setAttr( (extrudeNode + ".useProfileNormal" )  , 0)

		nurbsTessellateNode = mc.listConnections( extrudeNode + '.outputSurface', s = False, d = True )[0]
		mc.setAttr( (nurbsTessellateNode + ".format") , 0)
		mc.setAttr( (nurbsTessellateNode + ".polygonType") , 1)		
		mc.connectAttr( self.Attr.ctrl.polyCount.str() , (nurbsTessellateNode + ".polygonCount") )


		#VISIBILITY
		mc.setAttr( self.Name.topNode.str() + ".skeletonVis" ,1)
		mc.setAttr( self.Name.topNode.str() + ".skeletonRef" ,2)
		mc.setAttr( self.Joints.Name.topNode.str() + ".v" ,0)
		'''
		if ( self.doIk ):
			#BUILD				
			ikJointsGrp = mc.createNode( 'transform' , n = self.Name.ikJoint.str() + '_GRP' )
			mc.parent( ikJointsGrp , self.Name.rigGrp.str() )
			utilsMaya.buildConstraint( [ self.Root.outs[0].str()  , ikJointsGrp  ] , [ 'parent' , 'scale' ] , 'oneMaster' , 1 )			    	
			# IK___________CREATE JOINT
			ikJoints = [ self.Name.ikJoint.str() + 'A' , self.Name.ikJoint.str() + 'B' , self.Name.ikJoint.str() + 'C' ]
			ikJointsPos = [ self.Pos.aimAB.value() , self.Pos.aimBC.value() , self.Pos.C.value() ]
			mc.select( cl = True )
			mc.joint( n = ikJoints[0] , p = ikJointsPos[0][0:3] , o = ikJointsPos[0][3:6]  )
			mc.select( cl = True )
			mc.joint( n = ikJoints[1] , p = ikJointsPos[1][0:3] , o = ikJointsPos[1][3:6]  )
			mc.select( cl = True )
			mc.joint( n = ikJoints[2] , p = ikJointsPos[2][0:3] , o = ikJointsPos[2][3:6]  )
			mc.parent( ikJoints[0] , ikJointsGrp )
			mc.parent( ikJoints[1] , ikJoints[0] )
			mc.parent( ikJoints[2] , ikJoints[1] )
	
			self.utils_prepareJointForIk( ikJoints )
			# IK___________CREATE JOINT TRANSFER
			ikJointsTransfer = [ self.Name.ikJoint.str() + 'TransferA' , self.Name.ikJoint.str() + 'TransferB' , self.Name.ikJoint.str() + 'TransferC' ]
			mc.select( cl = True )
			mc.joint( n = ikJointsTransfer[0] , p = ikJointsPos[0][0:3] , o = ikJointsPos[0][3:6]  )
			mc.select( cl = True )
			mc.joint( n = ikJointsTransfer[1] , p = ikJointsPos[1][0:3] , o = ikJointsPos[1][3:6]  )
			mc.select( cl = True )
			mc.joint( n = ikJointsTransfer[2] , p = ikJointsPos[2][0:3] , o = ikJointsPos[2][3:6]  )
			mc.parent( ikJointsTransfer[0] , ikJointsGrp )
			mc.parent( ikJointsTransfer[1] , ikJointsTransfer[0] )
			mc.parent( ikJointsTransfer[2] , ikJointsTransfer[1] )
	
			self.utils_prepareJointForIk( ikJointsTransfer )
			utilsMaya.buildConstraint( [ ikJoints[0]  , ikJointsTransfer[0] ] , [ 'parent' ] , 'oneMaster' , 1 )	
			utilsMaya.buildConstraint( [ ikJoints[1]  , ikJointsTransfer[1] ] , [ 'parent' ] , 'oneMaster' , 1 )		
			utilsMaya.buildConstraint( [ ikJoints[2]  , ikJointsTransfer[2] ] , [ 'parent' ] , 'oneMaster' , 1 )				    	

			# IK___________CREATE SOLVER				
			mc.ikHandle( sj = ikJoints[0] , ee = ikJoints[2] , sol = 'ikRPsolver' , n = self.Name.handleIkSolver.str() )
			mc.parent( self.Name.handleIkSolver.str() , self.Name.rigGrp.str()  )
			mc.poleVectorConstraint( self.Pv.Name.ctrl.str() , self.Name.handleIkSolver.str() )	
			utilsMaya.buildConstraint( [ self.Handle.outs[0].str()      , self.Name.handleIkSolver.str()  ] , [ 'parent' , 'scale' ] , 'oneMaster' , 1 )			   
			utilsMaya.buildConstraint( [ self.HandleBase.outs[0].str()  , ikJoints[0]                     ] , [ 'parent'  ] , 'oneMaster' , 1 )		 	
			# IK___________PV ORIENT SYSTEME			
			constraintCreated = mc.listRelatives( self.Pv.Name.topNode.str() , c = True , type = 'parentConstraint' )	
			
			mc.createNode( 'reverse' , n = self.Name.followWrist_reverse.str()  )
			mc.connectAttr(  self.Attr.pv.followHandle.str() , self.Name.followWrist_reverse.str() + '.inputX' )	
			
			mc.connectAttr(   self.Name.followWrist_reverse.str() + '.outputX' ,  constraintCreated[0] + '.' + self.HandleBase.Name.ctrl.str()  + 'W0' )			
			mc.connectAttr(   self.Attr.pv.followHandle.str()                  ,  constraintCreated[0] + '.' + self.StretchyPv.Name.jointA.str() + 'W1' )			
			# IK___________FK LINK	
			utilsMaya.buildConnections(  [ ikJointsTransfer[0]  , self.Fk.Ctrl0.Name.topNode.str()  ] , [ 'translate','rotate' ] , [ 'translate','rotate' ] , 'oneMaster'  )		
			utilsMaya.buildConnections(  [ ikJointsTransfer[1]  , self.Fk.Ctrl1.Name.topNode.str()  ] , [ 'translate','rotate' ] , [ 'translate','rotate' ] , 'oneMaster'  )		
			utilsMaya.buildConnections(  [ ikJointsTransfer[2]  , self.Fk.Ctrl2.Name.topNode.str()  ] , [ 'translate','rotate' ] , [ 'translate','rotate' ] , 'oneMaster'  )		
			#STRETCHY CONNECTION		
			#utilsMaya.buildConnections(  [ ikJoints[0]  , self.Fk.Ctrl0.outs[0].str()  ] , [ 'scaleX'] , [ 'scaleX'] , 'oneMaster' )
			#utilsMaya.buildConnections(  [ ikJoints[1]  , self.Fk.Ctrl1.outs[0].str()  ] , [ 'scaleX'] , [ 'scaleX'] , 'oneMaster' )
			#FK HOLD ROTATIONS
			utilsMaya.buildConstraint( [ self.Handle.Name.ctrl.str()  , ikJoints[2]  ] , [  'orient'  ] , 'oneMaster' , 1 )
			constraintCreated = mc.listRelatives( ikJoints[2] , c = True , type = 'orientConstraint' )	
			mc.connectAttr( self.Attr.Ctrl2.holdRot.str() , constraintCreated[0] + '.' + self.Handle.Name.ctrl.str() + 'W0' )
	
			# IK___________STRETCH EXPRESSION	
			stretchAxes = [0,0,0] #only work with x axis
	
			pA = self.Pos.A.value()
			pB = self.Pos.B.value()
			pC = self.Pos.C.value()				
			distanceMax = 0
			distanceMax += ompy.MVector( pB[0] - pA[0] , pB[1] - pA[1]  , pB[2] - pA[2] ).length()
			distanceMax += ompy.MVector( pC[0] - pB[0] , pC[1] - pB[1]  , pC[2] - pB[2] ).length()
											
			stretchExp = '\n\n'		
			stretchExp += '\n' +   '\n'
			stretchExp += '\n' +   'float $rapport = {0}/{1} / {2}.scaleX;'.format( self.StretchyPv.Attr.topNode.distance.str() , distanceMax , self.Fk.Name.topNode.str() ) 
			stretchExp += '\n' +   'float $scaleValue = 1;'
			stretchExp += '\n' +   '\n'
			stretchExp += '\n' +   'if( $rapport > 1 )'
			stretchExp += '\n' +   '{'
			stretchExp += '\n' +   '	$scaleValue = $rapport * {0} + ( 1 - {0} );'.format( self.Attr.handle.stretchUP.str()  )
			stretchExp += '\n' +   '}else{'
			stretchExp += '\n' +   '	$scaleValue = $rapport * {0} + ( 1 - {0} );'.format( self.Attr.handle.stretchDwn.str() )
			stretchExp += '\n' +   '}'
			stretchExp += '\n' +   '\n'
			stretchExp += '\n' +   '//_______________________________________________________________________________reduce claping____START'
			stretchExp += '\n' +   '\n'
			stretchExp += '\n' +   'float $scaleReduceClapping = 0.1 ;'
			stretchExp += '\n' +   'float $distanceReduceClapping[] = { 0.75 , 0.85 , 1.0 };'
			stretchExp += '\n' +   'float $mult =  0;'		
			stretchExp += '\n' +   '\n'		
			stretchExp += '\n' +   'if( $rapport <  $distanceReduceClapping[1] )'
			stretchExp += '\n' +   '{'				
			stretchExp += '\n' +   '	$mult = ( clamp( $distanceReduceClapping[0] , $distanceReduceClapping[1] , $rapport ) - $distanceReduceClapping[0] ) / ( $distanceReduceClapping[1] - $distanceReduceClapping[0] );'		
			stretchExp += '\n' +   '}else{'		
			stretchExp += '\n' +   '	$mult = 1 - ( clamp( $distanceReduceClapping[1] , $distanceReduceClapping[2] , $rapport ) - $distanceReduceClapping[1] ) / ( $distanceReduceClapping[2] - $distanceReduceClapping[1] );'				
			stretchExp += '\n' +   '}'		
			stretchExp += '\n' +   '\n'		
			stretchExp += '\n' +   'if( ( $rapport <  $distanceReduceClapping[0] )||( $rapport >  $distanceReduceClapping[2] ) )'				
			stretchExp += '\n' +   '{'				
			stretchExp += '\n' +   '	$mult = 0;'
			stretchExp += '\n' +   '}'		
			stretchExp += '\n' +   '\n'		
			stretchExp += '\n' +   'float $reduceClappingValue = $scaleValue - {0} * $scaleReduceClapping * $mult;'.format( self.Attr.handle.reduceClapping.str() )		
			stretchExp += '\n' +   '\n'				
			stretchExp += '\n' +   '//_______________________________________________________________________________reduce claping____END'		
			stretchExp += '\n' +   '\n'	
			stretchExp += '\n' +   '{0}.scaleX = $reduceClappingValue;'.format( ikJoints[0] )	
			stretchExp += '\n' +   '{0}.scaleX = $reduceClappingValue;'.format( ikJoints[1] )	
					     
			utilsMaya.buildSimpleExpression( self.Name.stretchExp.str() , stretchExp )
        


			'''


	def utils_prepareJointForIk( self , ikJoints ):

		for joint in ikJoints :
			utils_jointOrientToRotation( joint )
			utils_rotationToPrefAngle( joint )



def utils_jointOrientToRotation( joint ):
	#CREATE AND PLACE TRSF
	trsfTmp = mc.createNode( 'transform' , n = 'utils_jointOrientToRotation_' + joint )
	father  = mc.listRelatives( joint , p = True )
	mc.parent( trsfTmp , father )
	mc.delete( mc.parentConstraint( joint , trsfTmp) )
	#CLEAN JOINT
	for axe in ['X','Y','Z']:
		mc.setAttr( '{}.jointOrient{}'.format( joint , axe) , 0 )
		mc.setAttr( '{}.rotate{}'.format( joint , axe) , mc.getAttr( '{}.rotate{}'.format( trsfTmp , axe) ) )
	mc.delete( trsfTmp )


def utils_rotationToJointOrient( joint ):
	pass

def utils_rotationToPrefAngle( joint ):
	for axe in ['X','Y','Z']:
		mc.setAttr( '{}.preferredAngle{}'.format( joint , axe) , mc.getAttr( '{}.rotate{}'.format( joint , axe) ) )
