'''
#******************************************************** BUILD EXEMPLE RIG CTRL
import maya.cmds as mc
import python
from python.classe.rigCtrl import *
reload( python.classe.rigCtrl)


mc.file( f = True , new = True )

#_________________________________BUILD

manipA = rigCtrl( n = 'manipA' , pos = [[5,0,3,0,0,0,1,1,1]] , form = 'sphere' , colors = [17] )
	
toExec = manipA.build()
exec(toExec)


#_________________________________MIRROR
args = {}
args['value']             = [0,0,0 , 0,1,0 , 0,0,1]
args['mode']              = 'mirror'
args['pivot']             = [0,0,0 , 0,0,0 , 1,1,1]
args['namePrefix']        = ['r','l']
args['nameReplace']       = ['','']
args['nameIncr']          = ''
args['nameAdd']           = []
args['noneMirrorAxe']     = 4

duplicatedmanipA = manipA.duplicate( **args )

toExec = ''
for dupli in duplicatedmanipA:
    toExec += dupli.build()

exec(toExec)



#_________________________________DUPLI

args = {}
args['value']             = [-2.36 , 2.876 , -2.247 , -23.629 , 18.578 , 33.015 , 1 , 1 , 1 , 5 ]
args['mode']              = 'transform'
args['pivot']             = [ 5 , 0 , -1 , 0 ,0,0 , 1 , 1 , 1 ]
args['namePrefix']        = ['','']
args['nameReplace']       = ['','']
args['nameIncr']          = 'A'
args['nameAdd']           = []
args['noneMirrorAxe']     = 4


duplicatedmanipA  = manipA.duplicate( **args )

for i in range( 0 , len(duplicatedmanipA) ):
    duplicatedmanipA[i].build()


#_________________________________REF

from python.classe.buildName import *
from python.classe.buildCurveShape import *
from python.classe.buildPosition import *

Name = buildName()
Name.add( 'base'   , baseNameAppend = 'manip'  )
Name.add( 'manipB' , baseNameAppend = 'B'     , ref = Name.base   )

Pos = buildPosition()
Pos.add(  'manipB' , replace = [5,0,-3,0,0,0,1,1,1]  )

cShape = buildCurveShape()
cShape.add(  'manipB' , value = { 'form' : 'sphere'   , 'colors' : [13] , 'axe' : 'x' , 'offset' : [0,0,0,0,0,0,1,1,1] }  )

manipB = rigCtrl( n = Name.manipB , pos = [ Pos.manipB ] , shape = cShape.manipB )	

manipB.CurveShape.add(  'ctrl' , value = { 'form' : 'loc'   , 'colors' : [17] , 'axe' : 'x' , 'offset' : [0,0,0,0,0,0,1,1,1] }  )

manipB.build()

manipB.delete()


'''

'''
#******************************************************** BUILD EXEMPLE RIG CTRL
import maya.cmds as mc
import python
from python.classe.rigCtrl import *
reload( python.classe.rigCtrl)

mc.file( f = True , new = True )

manipA = rigCtrl( n = 'manipA' , pos = [[5,0,3,0,0,0,1,1,1]] , form = 'sphere' , colors = [17] , 
t = True , r = False , s = False , v = True , ro = True , pivot = True , gimbal = True,
pivotSpace     = [ [5,0,3,0,0,0,1,1,1] , [5,0,3,0,0,0,1,1,1] , [5,0,3,0,0,0,1,1,1] ] , #CAN BE A TRS A POS CLASS 
pivotSpaceName = [ 'high'              , 'mid'              , 'low'                  ] # current high mid low


what should be in the args or not:
everything that not involve external element or specificities like extra attribute



'''




import maya.cmds as mc
from .rig import *	
import types


class rigCtrl( rig ):

	def __init__( self , **args):
		rig.__init__( self , **args )
		#CLASSE TYPE
		self.classeType = 'rigCtrl'		

		#CLASSE BLUE PRINT
		self.Name.add( 'base'    , baseName = self.classeType )	
		self.Name.add( 'topNode' , ref = self.Name.base , type = 'OFFSET'  )	
		self.Attr.add( 'topNode' , Name = self.Name.topNode  )
	
		self.Pos.add(     'topNode' , Name = self.Name.topNode , replace = [0,0,0,0,0,0,1,1,1] )

		self.Name.add(       'ctrl' , ref  = self.Name.base    , type    = 'CTRL'  , parent  = self.Name.topNode     )
		self.Pos.add(        'ctrl' , Name = self.Name.ctrl    , replace = self.Pos.topNode    )	
		self.Attr.add(       'ctrl' , Name = self.Name.ctrl    , attrName= ['defaultTrs'] , attrType = ['string']  , attrValue = [ [0,0,0,0,0,0,1,1,1]] )
		self.CurveShape.add( 'ctrl' , Name = self.Name.ctrl    , value   = { 'form' : 'cube' , 'colors' : [13] , 'axe' : 'x' , 'offset' : [0,0,0,0,0,0,1,1,1]  , 'position' : self.Pos.ctrl }   )		
		
		#CLASSE UTILS
		self.SubRigs     = []
		self.SubRigsName = []
		self.ins         = [ self.Name.topNode ]
		self.outs        = [ self.Name.ctrl    ]
		self.outsToCtrls = [[self.Name.ctrl]   ]	
		
		#CLASSE MODIF 
		self.ctrlVisPriority = args.get( 'ctrlVisPriority' , 0    )
		self.modif           = args.get( 'modif'           , None )	
		self.pivot           = args.get( 'pivot'           , None )
		self.pivotSpace      = args.get( 'pivotSpace'      , None )  
		self.pivotSpaceName  = args.get( 'pivotSpaceName'  , None ) 
		self.gimbal          = args.get( 'gimbal'          , None )
		self.joint           = args.get( 'joint'           , None )
		self.attrStates      = args.get( 'attrStates'      , None )

		

		'''
		t  = args.get( 't'  , None )
		tx = args.get( 'tx' , None )
		ty = args.get( 'ty' , None )
		tz = args.get( 'tz' , None )

		r  = args.get( 'r'  , None )
		rx = args.get( 'rx' , None )
		ry = args.get( 'ry' , None )
		rz = args.get( 'rz' , None )

		s  = args.get( 's'  , None )
		sx = args.get( 'sx' , None )
		sy = args.get( 'sy' , None )
		sz = args.get( 'sz' , None )

		v   = args.get( 'v'  , False )
		ro  = args.get( 'ro' , True )


		t , tx , ty , tz = None , None , None , None
		r , rx , ry , rz = None , None , None , None
		s , sx , sy , sz = None , None , None , None
		v  = False
		ro = True

		attrNames  = ['t','r','s','v','ro','tx','ty','tz','rx','ry','rz','sx','sy','sz']
		attrState  = [ t , r , s , v , ro , tx , ty , tz , rx , ry , rz , sx , sy , sz ]
		'''

		#ATTR STATE - GET ATTRSTATE
		attrNames  = [] 
		attrNames += [ 't' , 'r' , 's' , 'v' , 'ro'] 
		attrNames += [ 'tx' , 'ty' , 'tz' ] 
		attrNames += [ 'rx' , 'ry' , 'rz' ] 
		attrNames += [ 'sx' , 'sy' , 'sz' ] 

		attrState  = [] 
		attrState += [ None , None , None , False , True ] 
		attrState += [ None , None , None ] 
		attrState += [ None , None , None ] 
		attrState += [ None , None , None ] 

		if not( self.attrStates == None ):
			attrState[0:4] = [ False , False , False , False ]

			currentStates = self.attrStates[0]
			for j in range(0,len(currentStates)):
				for i in range(0,len(attrNames)):
					if( attrNames[i] == currentStates[j] ):
						attrState[i] = True

		#ATTR STATE - ATTRSTATE ---> ATTRSTATE LOCK & KEYEABLE

		attrStateLock    = []
		attrStateKeyable = []
		for i in range( 0 , len(attrNames) ):

			if(   attrNames[i] == 'v'  ):attrStateLock.append( False )
			elif( attrState[i] == None ):attrStateLock.append( None  )
			else:                        attrStateLock.append( not attrState[i] )

			if(   attrNames[i] == 'ro'  ):attrStateKeyable.append( False )
			else:                         attrStateKeyable.append( attrState[i] )

		#ATTR STATE - ADD INFO IN BUILDATTR
		self.Attr.add(  'ctrl'  , Name = self.Name.ctrl  , attrName = attrNames , attrCb = attrState , attrLock = attrStateLock , attrKeyable = attrStateKeyable  )
	



		if ( self.modif ):
			self.Name.add(   'modif'  , ref  = self.Name.base  , type = 'MODIF' , parent  = self.Name.topNode )
			self.Pos.add(    'modif'  , Name = self.Name.modif , replace = self.Pos.topNode  )
			self.Name.add(   'ctrl'   , parent  = self.Name.modif )			
			self.ins += [ self.Name.modif ]				



		if( self.pivot )or not( self.pivotSpace == None ):
			self.Name.add(   'pivotOffset' , ref  = self.Name.base         , baseNameAppend = 'Pivot' , type = 'GRP' , parent  = self.outs[0] )
			self.Pos.add(    'pivotOffset' , Name = self.Name.pivotOffset  , replace = self.Pos.topNode  )	

			self.Name.add(       'pivot' , ref  = self.Name.base  , baseNameAppend = 'Pivot' , type    = 'CTRL'  , parent  = self.Name.pivotOffset  )
			self.Pos.add(        'pivot' , Name = self.Name.pivot , replace = self.Pos.topNode  )
			self.CurveShape.add( 'pivot' , Name = self.Name.pivot , value   = { 'form' : 'sphere' , 'colors' : [13] , 'axe' : 'x' , 'offset' : [0,0,0,0,0,0,1,1,1] , 'position' : self.Pos.ctrl }   )		
			
			self.Attr.add(  'ctrl'        , Name = self.Name.ctrl  , attrName = ['pivot'] , attrType = ['intOnOff']  , attrkeyable = [0]   , attrValue = [0]  )
			self.Attr.add(  'pivotOffset' , Name = self.Name.pivotOffset )
			self.Attr.add(  'pivot'       , Name = self.Name.pivot       )
						
			self.Link.add(  'pivot' , Sources = [ self.Attr.ctrl.pivot      ] , Destinations = [ self.Attr.pivotOffset.visibility  ] , type = 'normal' , operation = 'oneMaster'  )					
			self.Link.add(  'ctrl'  , Sources = [ self.Attr.pivot.translate ] , Destinations = [ self.Attr.ctrl.rotatePivot  ] , type = 'normal' , operation = 'oneMaster'  )					
			
			if not( self.pivotSpace == None ):
				for i in range( 0 , len(self.pivotSpace) ):
					if( len(self.pivotSpaceName) <= i ):
						self.pivotSpaceName.append( 'space{}'.format(i) )
				#self.Link.add( 'pivotSpace' , Sources = [ [0,0,0,1,1,1,2,2,2] , self.Name.ctrl , self.Pos.topNode ] , Destinations = [ self.Name.pivotOffset ] , spaceDriver = [ self.Name.ctrl ] , spaceNames = [ "toto" , "toto" , "toto" ] , type = 'parentSpace' )		
				self.Link.add( 'pivotSpace' , Sources = self.pivotSpace , Destinations = [ self.Name.pivotOffset ] , spaceDriver = [ self.Name.ctrl ] , spaceNames = self.pivotSpaceName , type = 'parentSpace' )										


		if( self.gimbal ):
			self.Name.add(   'gimbalOffset' , ref  = self.Name.base          , baseNameAppend = 'Gimbal' , type = 'GRP' , parent  = self.outs[0]   )
			self.Pos.add(    'gimbalOffset' , Name = self.Name.gimbalOffset  , replace = self.Pos.topNode  )
			#self.Dag.add(    'gimbalOffset' , Name = self.Name.gimbalOffset  , type    ='transform'        )
			#self.Parent.add( 'gimbalOffset' , Name = self.Name.gimbalOffset  , parent  = self.outs[0]      )			

			self.Name.add(       'gimbal' , ref  = self.Name.base   , baseNameAppend = 'Gimbal' , type = 'CTRL' , parent  = self.Name.gimbalOffset )
			self.Pos.add(        'gimbal' , Name = self.Name.gimbal , replace = self.Pos.topNode  )
			#self.Dag.add(        'gimbal' , Name = self.Name.gimbal , type    ='transform'        )
			#self.Parent.add(     'gimbal' , Name = self.Name.gimbal , parent  = self.Name.gimbalOffset   )
			self.CurveShape.add( 'gimbal' , Name = self.Name.gimbal , value   = { 'form' : 'sphere' , 'colors' : [13] , 'axe' : 'x' , 'offset' : [0,0,0,0,0,0,1,1,1] , 'position' : self.Pos.ctrl }   )		
			
			self.Attr.add(  'ctrl'         , Name = self.Name.ctrl  , attrName = ['gimbal'] , attrType = ['intOnOff']  , attrkeyable = [0]   , attrValue = [0]  )
			self.Attr.add(  'gimbalOffset' , Name = self.Name.gimbalOffset )
			self.Attr.add(  'gimbal'       , Name = self.Name.gimbal  , attrName = attrNames , attrCb = attrState  )			
			self.Attr.add(  'gimbal'       , Name = self.Name.gimbal       )

			self.Link.add(  'gimbal' , Sources = [ self.Attr.ctrl.gimbal     ] , Destinations = [ self.Attr.gimbalOffset.visibility  ] , type = 'normal' , operation = 'oneMaster'  )					
			self.outs = [ self.Name.gimbal ]

		if ( self.joint ):
			self.Name.add(   'joint' , ref  = self.Name.base  , type    = 'JNT'  , parent  = self.outs[0]            )
			self.Pos.add(    'joint' , Name = self.Name.joint , replace = self.Pos.topNode  )
			#self.Dag.add(    'joint' , Name = self.Name.joint , type    ='joint'            )
			#self.Parent.add( 'joint' , Name = self.Name.joint , parent  = self.outs[0]      )
			self.outs = [ self.Name.joint ]


		#INSTANCE MODIF
		name                 = args.get( 'n'               , None )	
		pos                  = args.get( 'pos'             , None )
		shape                = args.get( 'shape'           , None )
		form                 = args.get( 'form'            , None )
		colors               = args.get( 'colors'          , None )	
		ctrlScale            = args.get( 'ctrlScale'       , 1 )	
		parent               = args.get( 'parent'          , None )	

		if not( name      == None ): self.Name.add(        'base'    , copy    = name                     ) 
		if not( pos       == None ): self.Pos.add(         'topNode' , replace = pos[0]                   )
		if not( shape     == None ): self.CurveShape.add(  'ctrl'    , value   = shape                    )
		if not( form      == None ): self.CurveShape.add(  'ctrl'    , value   = { 'form'   : form   }    )
		if not( colors    == None ): self.CurveShape.add(  'ctrl'    , value   = { 'colors' : colors }    )		
		if not( ctrlScale == 1    ): self.CurveShape.add(  'ctrl'    , value   = { 'scale' : ctrlScale }  )	
		if not( parent    == None ): self.Name.add(       'topNode'  , parent = parent                    )


		constraintOuts = args.get( 'constraintOuts' , True )	
		if not( pos == None ) and( type(pos[0]) == types.StringType ):
			if( mc.objExists(pos[0]) == True ):

				if( constraintOuts ):
					for i in range( 0 , len(pos) ):
						self.Name.add(  'out{}'.format(i)      , copy = pos[i] , objExists = True )
						self.Link.add(  'out{}'.format(i)      , Sources = [ self.outs[i] ] , Destinations = [ eval('self.Name.out{}'.format(i) )  ] , type = 'parent' , operation = 'oneMaster'  )					
						self.Link.add(  'outScale{}'.format(i) , Sources = [ self.outs[i] ] , Destinations = [ eval('self.Name.out{}'.format(i) )  ] , type = 'scale'  , operation = 'oneMaster'  )

				fathers = mc.listRelatives( pos[0] , p = True )
				if not( fathers == None ):		
					self.Name.add(  'in0' , copy = fathers[0] , objExists = True )		
					self.Link.add(  'in0' , Sources = [eval('self.Name.in0' )] , Destinations = [ self.ins[0] ] , type = 'parent' , operation = 'oneMaster'  )					


	def buildMayaRig( self ):
		pass
