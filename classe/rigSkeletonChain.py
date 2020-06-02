
'''
#******************************************************** BUILD EXEMPLE RIG CTRL
import maya.cmds as mc
import python
from python.classe.rigSkeletonChain import *
reload( python.classe.rigSkeletonChain)

mc.file( f = True , new = True )
#=================================================


#_________________________________BUILD
SkeletonChain = rigSkeletonChain( n = 'arm' , pos =  [ [2,0,3,0,0,0,1,1,1] , [4,0,3,0,0,0,1,1,1] , [6,0,3,0,0,0,1,1,1] , [8,0,3,0,0,0,1,1,1] ]  )	


toExec = SkeletonChain.build()
exec(toExec)

#_________________________________TRANSFORM
args = {}
args['value']             = [-2.36 , 2.876 , -2.247 , -23.629 , 18.578 , 33.015 , 1 , 1 , 1 , 2 ]
args['mode']              = 'transform'
args['pivot']             = [ 5 , 0 , -1 , 0 ,0,0 , 1 , 1 , 1 ]
args['namePrefix']        = ['','']
args['nameReplace']       = ['','']
args['nameIncr']          = 'A'
args['nameAdd']           = []
args['noneMirrorAxe']     = 4


duplicated = SkeletonChain.duplicate( **args )


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
args['debug']     = 1


rigOut = SkeletonChain.duplicateRigs( args , duplicated )

toExec = ''
for rig in rigOut:
    for r in rig:
        toExec += r.build()

exec(toExec)





'''


import maya.cmds as mc
from ..utils import utilsMaya
from ..utils import utilsMath

from .rig import *
import maya.OpenMaya as om
	

class rigSkeletonChain(rig):

	def __init__( self , **args ):
		rig.__init__( self , **args )

		self.doEndJoint    = args.get( 'endJoint' , True )   

		#CLASSE TYPE
		self.classeType = 'rigSkeletonChain' 

		#CLASSE BLUE PRINT
		self.Name.add( 'base'  , baseName = self.classeType , type = 'GRP' )

		#CLASSE UTILS
		self.SubRigs = []
		self.ins     = []
		self.outs    = []
		self.jointsPositionBase = [ [0,0,0,0,0,0,1,1,1] , [2,0,0,0,0,0,1,1,1] , [4,0,0,0,0,0,1,1,1] ] 

		#CLASSE MODIF
		self.doAim    = args.get( 'aim' , None )

		#INSTANCE MODIF
		name   = args.get( 'n'   , None ) 
		pos    = args.get( 'pos' , self.jointsPositionBase )
		parent = args.get( 'parent'   , None ) 

		if not( name == None ): self.Name.add( 'base' , copy = name )                                
		if not( pos  == None ): jointsPosition = pos                        
		
		#CLASSE BLUE PRINT
		for i in range( len(pos) ):
			#NAME
			if( i == 0 ): exec( 'self.Name.add( "joint{0}" , ref = self.Name.base , baseNameAppend = "{0}" , type = "JNT"                               )'.format(i)      )
			else:         exec( 'self.Name.add( "joint{0}" , ref = self.Name.base , baseNameAppend = "{0}" , type = "JNT" , parent = self.Name.joint{1} )'.format(i,i-1 ) )

			exec('self.Pos.add(  "joint{0}" , Name = self.Name.joint{0} , replace = pos[{0}]  )'.format(i) )
			exec('self.Attr.add( "joint{0}" , Name = self.Name.joint{0}                       )'.format(i) )
			#ARRAY
			exec( 'self.ins.append(  self.Name.joint{} )'.format(i) )
			exec( 'self.outs.append( self.Name.joint{} )'.format(i) )
		
		if( self.doEndJoint ) and ( 1 < len(pos) ):
			#COMPUTE SMALLEST DIST
			smallestDist = 0
			if( 1 < len(pos) ):
				distList     = []
				for i in range(0,len(pos)-1):
					if( type(pos[i]) == types.InstanceType): 
						distList.append(om.MVector( pos[i].value()[0] - pos[i+1].value()[0] , pos[i].value()[1] - pos[i+1].value()[1] , pos[i].value()[2] - pos[i+1].value()[2]).length() )
					elif( type(pos[i]) == types.StringType ):
						pA = mc.xform( pos[i]   , q = True , t = True , ws = True )
						pB = mc.xform( pos[i+1] , q = True , t = True , ws = True )
						distList.append(om.MVector( pA[0] - pB[0] , pA[1] - pB[1] , pA[2] - pB[2]).length() )
					else:
						distList.append(om.MVector( pos[i][0] - pos[i+1][0] , pos[i][1] - pos[i+1][1] , pos[i][2] - pos[i+1][2]).length() )
				
				distList.sort()
				smallestDist = distList[0] * 0.3
		
			#ADD LAST JOINT
			exec( 'self.Name.add( "jointEnd"  , ref = self.Name.base      , baseNameAppend = "End"         , type = "JNT" , parent = self.Name.joint{} )         '.format( len(pos)-1 ) ) 	
			exec( 'self.Pos.add(  "jointEnd"  , Name = self.Name.jointEnd , append = [ {"replace":pos[%d]} , {"addLocal":[ smallestDist,0,0 ,0,0,0,1,1,1]} ] )'%( len(pos)-1 ) )       

		#CLASSE MODIF			
		if( self.doAim ):
			for i in range( len(pos) - 1 ):
				exec( 'self.Pos.add( "joint{0}" , aim = self.Pos.joint{1} )'.format( i , i+1 ) )


		if not( parent == None ): self.Name.add( 'joint0' , parent = parent )
