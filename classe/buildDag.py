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

Names.add( 'jointA'  , baseNameAppend = 'A'         , type = 'JNT' , ref = Names.base )
Names.add( 'jointB'  , baseNameAppend = 'B'         , type = 'JNT' , ref = Names.base )
Names.add( 'jointC'  , baseNameAppend = 'C'         , type = 'JNT' , ref = Names.base )

Names.add( 'ikHandle'     , baseNameAppend = ''           , type = 'handle'   , ref = Names.base )
Names.add( 'ikEffector'  , baseNameAppend = ''         , type = 'effector' , ref = Names.base )
# DAG
from python.classe.buildDag import *
reload(python.classe.buildDag)

Dag = buildDag()
Dag.add( 'buildA' , Name = Names.joint  , type = 'transform' , parent = Names.ctrlA   )
Dag.add( 'buildB' , Name = Names.ctrlA  , type = 'transform'  )

Dag.add( 'jointA' , Name = Names.jointA  , type = 'joint'  )
Dag.add( 'jointB' , Name = Names.jointB  , type = 'joint' , parent = Names.jointA )
Dag.add( 'jointC' , Name = Names.jointC  , type = 'joint' , parent = Names.jointB )

# MODIF NAMES
Names.add( 'base'   , replace = [ 'toto' , 'matthieu' ] ) # doesnt work ?

# BUILD
Dag.build()


from python.classe.buildLink import *
reload(python.classe.buildLink)

Link = buildLink()

ikSolvers = ['ikSCsolver','ikRPsolver']
Link.add( 'ik' , Sources = [ Names.ikHandle , Names.ikEffector ] , Destinations = [ Names.jointA,Names.jointC ] , type = ikSolvers[1] , parents = [Names.ctrlA , None ] )		
				
Link.build()



# DUPLI A
dupliValue = [0,0,0 , 0,1,0 , 0,0,1]
dupliMode  = 'mirror'

duplicatedDag   = Dag.duplicate( dupliValue , dupliMode , [0,0,0 , 0,0,0 , 1,1,1] , namePrefix = ['r','l'] , nameReplace = ['toto','tata'] , nameIncr = '' , orientLockAxe = 0 , orientInverseAxes = 0  )
duplicatedNames = Names.duplicate( dupliValue , dupliMode , [0,0,0 , 0,0,0 , 1,1,1] , namePrefix = ['r','l'] , nameReplace = ['toto','tata'] , nameIncr = '' , orientLockAxe = 0 , orientInverseAxes = 0  )
duplicateKey = str(dupliValue) + dupliMode

duplicatedDag[1].printInfo()

for i in range( 0 , len(duplicatedNames)):
    duplicatedDag[i].swapRefsToDuplicate(  duplicateKey , dupliIndex = i )


# DUPLI B
dupliValue = [10,0,0 , 0,15,0 , 0,0,1 , 5]
dupliMode  = 'transform'

duplicatedDag   = Dag.duplicate( dupliValue , dupliMode , [0,0,0 , 0,0,0 , 1,1,1] , namePrefix = ['',''] , nameReplace = ['',''] , nameIncr = 'A' , orientLockAxe = 0 , orientInverseAxes = 0  )
duplicatedNames = Names.duplicate( dupliValue , dupliMode , [0,0,0 , 0,0,0 , 1,1,1] , namePrefix = ['',''] , nameReplace = ['',''] , nameIncr = 'A' , orientLockAxe = 0 , orientInverseAxes = 0  )
duplicateKey    = str(dupliValue) + dupliMode

duplicatedNames[2].printInfo()
duplicatedDag[2].printInfo()


Names.keyToDuplicated

for i in range( 0 , len(duplicatedNames)):
    duplicatedDag[i].swapRefsToDuplicate(  duplicateKey , dupliIndex = i )

for i in range( 0 , len(duplicatedNames)):
    duplicatedDag[i].build()

'''


import maya.cmds as mc

from ..utils import utilsMaya
from ..utils import utilsPython
from ..utils import utilsMath
from ..utils import utilsMayaApi
from .build import *

import types


class buildDag( build ):

	def __init__(self , **args):
		build.__init__(self , **args )
		#____________________________________________________________________RIG INFO
		#UTILS																			
		#CLASSE
		self.classeType   = 'buildDag'	
		self.argsValue    = [ ]
		#self.argsRef      = [ 'Name' , 'type' , 'parent'  ]


	def build( self ):
		'''
		names   = []
		types   = [] 
		parents = []		
		for i in range( 0 , len( self.data ) ):
			refs = self.refs(i)
			names.append(   refs['Name']          )
			types.append(   refs['type']          )
			parents.append( refs.get('parent','') )

		utilsMaya.createDagNodes( types , names , parents )
		'''
		buildCmds = ''

		#CREATE NODE
		outNames = []
		types    = []
		parents  = []
		for i in range( 0 , len( self.data ) ):
			refs    = self.refs(i)
			name    = refs['Name'] 

			buildCmds += self.utils_createNode(**refs)

			outNames.append( name )
			types.append(  refs.get('type',None)  )
			parents.append(refs.get('parent',None))

		#PARENT
		for i in range( 0 , len( parents ) ):
			if not( parents[i] == None ):
				buildCmds += self.utils_parentNode( name = outNames[i] , type = types[i] , parent = parents[i] )

		return buildCmds
		
	def utils_createNode( self , **args ):
		buildCmds = ''

		nodeType = args['type'] 
		name     = args['Name'] 

		nameOut = None
		if( nodeType == None ): pass
		else:
			buildCmds += 'rawName = mc.createNode( "{}" , n = "{}" )\n'.format(nodeType,name)
			buildCmds += 'transformNode = mc.listRelatives( rawName , p = True  )\n'
			buildCmds += 'if not( transformNode == None):mc.rename( transformNode , "{}" )\n'.format(name)
 			    			    	
		return buildCmds			

	def utils_parentNode( self , **args ):
		buildCmds = ''

		nodeType = args['type'] 
		name     = args['name'] 
		father   = args['parent'] 

		if( nodeType == None ): pass
		else:
			if( type(name) == types.ListType ):
				for j in range( 0 , len(name) ):
					buildCmds += 'utilsMaya.safeParent( "{}" , "{}" )\n'.format(name[j] , father[j])
			else:
				buildCmds += 'utilsMaya.safeParent( "{}" , "{}" )\n'.format(name , father)
	
		return buildCmds
	'''
	#def utils_createDagNodes( self , types , names , fathers , trs = None ):

		types   = args['types']
		names   = args['names']
		fathers = args['fathers']

		indexSorted = utilsPython.sortIndexChildrensByHierarchy( names , fathers )
		
		trsObj = trsClass.trs()
		
		for i in indexSorted:
			#SORT ARGS
			argsPerObj = {}
			for key in args.keys():
				if not( args[key][i] == None ):
					argsPerObj[key] = args[key][i]

			self.utils_createDagNode( argsPerObj ):

			rawName = mc.createNode( types[i] )				
			transformNode = mc.listRelatives( rawName , p = True  )
			
			if( transformNode == None):
			    mc.rename( rawName , names[i] )
			    		    
			    if(  types[i] == 'joint'  ) and not ( fathers[i] == ''  ) and not ( trs == None ) :
			    			    	
			    	trsFather = trsObj.createFromObj( fathers[i] )
			    	trsObj.value = trs[i]
			    	trsObj.parent( trsFather )
			    	
			    	mc.parent( names[i] , fathers[i] )
			    	trsObj.toObj(names[i])
			    	mc.joint( names[i] , e = True , o = [ 0 , 0 , 0 ] )
			    
			    else:	
		    			    		
			    	if not( fathers[i] == '' ):
			    		mc.parent( names[i] , fathers[i] )	
	
			    	if not( trs == None ):
			    		trsObj.toObj( names[i] , worldSpace = 0 , inValue = trs[i] )
	
			    		    			    			    	
			    	
			else:
				
			    mc.rename( transformNode , names[i] )
	   
			    if not( fathers[i] == '' ):
			    	mc.parent( names[i] , fathers[i] )
	
			    if not( trs == None ):
			    	trsObj.toObj( names[i] , worldSpace = 0 , inValue = trs[i] )
		
		return names	
	'''

