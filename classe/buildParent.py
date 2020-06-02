'''

#******************************************************** BUILD EXEMPLE

# NAMES
import python
from python.classe.buildName import *
reload(python.classe.buildName)


import maya.cmds as mc
mc.file( f = True , new = True )

Names = buildName( )
Names.add( 'base'   , baseNameAppend = 'toto'     , type = 'grp' )		
Names.add( 'rigA'   , baseNameAppend = 'Arm'      , type = 'grp' , ref = Names.base )
Names.add( 'ctrlA'  , baseNameAppend = 'OffsetA'  , type = 'CTRL', ref = Names.rigA )
Names.add( 'joint'  , baseNameAppend = ''         , type = 'JNT' , ref = Names.ctrlA )


# PARENT
from python.classe.buildParent import *
reload(python.classe.buildParent)


Parents = buildParent()
Parents.add(  'test' , Name = Names.joint   ,  parent = Names.ctrlA   )

# MODIF NAMES
Names.add( 'base'   , replace = [ 'toto' , 'matthieu' ] )

# BUILD
import maya.cmds as mc
mc.createNode( 'transform' , n = Names.ctrlA.str()  )
mc.createNode( 'transform' , n = Names.joint.str()  )


Parents.build()

ParentsMirror = Parents.mirror( [ 0,0,0 , 0,1,0 ,0,0,1 ] , 0 , 0 , ['l' , 'r' ] , ['' , '' ]  )
mc.file( f = True , new = True )


for elem in ParentsMirror.data[0]['Name']:
    print( elem.str() , ParentsMirror.data[0]['parent'].str() )




# DUPLI A
dupliValue = [0,0,0 , 0,1,0 , 0,0,1]
dupliMode  = 'mirror'

duplicatedParents = Parents.duplicate( dupliValue , dupliMode , [0,0,0 , 0,0,0 , 1,1,1] , namePrefix = ['r','l'] , nameReplace = ['toto','tata'] , nameIncr = '' , orientLockAxe = 0 , orientInverseAxes = 0  )
duplicatedNames   = Names.duplicate( dupliValue , dupliMode , [0,0,0 , 0,0,0 , 1,1,1] , namePrefix = ['r','l'] , nameReplace = ['toto','tata'] , nameIncr = '' , orientLockAxe = 0 , orientInverseAxes = 0  )
duplicateKey      = str(dupliValue) + dupliMode

duplicatedParents[1].printInfo()

for i in range( 0 , len(duplicatedParents)):
    duplicatedParents[i].swapRefsToDuplicate(  duplicateKey , dupliIndex = i )


# DUPLI B
dupliValue = [10,0,0 , 0,15,0 , 0,0,1 , 5]
dupliMode  = 'transform'

duplicatedParents = Parents.duplicate( dupliValue , dupliMode , [0,0,0 , 0,0,0 , 1,1,1] , namePrefix = ['',''] , nameReplace = ['',''] , nameIncr = 'A' , orientLockAxe = 0 , orientInverseAxes = 0  )
duplicatedNames   = Names.duplicate( dupliValue , dupliMode , [0,0,0 , 0,0,0 , 1,1,1] , namePrefix = ['',''] , nameReplace = ['',''] , nameIncr = 'A' , orientLockAxe = 0 , orientInverseAxes = 0  )
duplicateKey      = str(dupliValue) + dupliMode

duplicatedParents[2].printInfo()

for i in range( 0 , len(duplicatedNames)):
    duplicatedParents[i].swapRefsToDuplicate(  duplicateKey , dupliIndex = i )



'''


import maya.cmds as mc

from ..utils import utilsMaya
from ..utils import utilsPython
from ..utils import utilsMath
from ..utils import utilsMayaApi
from .build import *


class buildParent( build ):

	def __init__(self , **args):
		build.__init__(self , **args )
		#____________________________________________________________________RIG INFO
		#UTILS																			
		#CLASSE
		self.classeType   = 'buildParent'	
		self.argsValue    = []




	def processBuild( self , refs , value ):
		childrens = refs.get('Name'  , None )
		parent    = refs.get('parent', None )

		buildCmds = ''
		if( type(childrens) == types.ListType ):
			for child in childrens:

				if( type(child) == types.InstanceType ) and ( child.classeType == "buildName"     ): 
					child = child.value()

				buildCmds += 'utilsMaya.safeParent("{}","{}")\n'.format( child , parent )
		else:
			buildCmds += 'utilsMaya.safeParent("{}","{}")\n'.format( childrens , parent )
			

		return buildCmds


