'''

import python
from python.classe.buildName import *
reload(python.classe.buildName)


Names = buildName( )
Names.add( 'base'   , baseNameAppend = 'toto'     , type = 'grp' )		
Names.add( 'rigA'   , baseNameAppend = 'Arm'     , type = 'grp' , ref = Names.base )
Names.add( 'ctrlA'  , baseNameAppend = 'OffsetA' , type = 'CTRL', ref = Names.rigA )
Names.add( 'jointA' , baseNameAppend = '1'       , type = 'JNT' , ref = Names.ctrlA )

Names.add( 'rigB'   , baseNameAppend = 'Leg'     , type = 'grp'   , ref = Names.base  )
Names.add( 'ctrlB'  , baseNameAppend = 'OffsetA' , type = 'CTRL'  , ref = Names.rigB  )
Names.add( 'jointB'  , baseNameAppend = ''        , type = 'joint' , ref = Names.rigB )	


NamesB = buildName()
NamesB.add( 'ctrlA'     , baseName = 'ctrl'       , type = 'grp' , parent = Names.rigA )	
NamesB.add( 'skeletonA' , baseName = 'skeleton'   , type = 'grp' , parent = Names.rigA)
NamesB.add( 'rigA'      , baseName = 'rig'        , type = 'grp' , parent = Names.rigA)	

NamesB.add( 'ctrlB'     , baseName = 'ctrl'       , type = 'grp' , parent = Names.rigB)
NamesB.add( 'skeletonB' , baseName = 'skeleton'   , type = 'grp' , parent = Names.rigB)
NamesB.add( 'rigB'      , baseName = 'rig'        , type = 'grp' , parent = Names.rigB)	


NamesC = buildName()
NamesC.add( 'rigC'     , baseNameAppend = 'Swap' , type = 'grp' , ref = Names.rigA       )
NamesC.add( 'swap1'    , copy = Names.rigA      , parent = NamesC.rigC , parentChildrenAndDeleteName = True  )	


#BUILD
Names += NamesB
Names += NamesC
toExec = Names.build()
exec(toExec)


#MIRROR
args = {}
args['value']             = [0,0,0 , 0,1,0 , 0,0,1]
args['mode']              = 'mirror'
args['pivot']             = [0,0,0 , 0,0,0 , 1,1,1]
args['namePrefix']        = ['r','l']
args['nameReplace']       = ['toto','tata']
args['nameIncr']          = ''
args['orientLockAxe']     = 0
args['orientInverseAxes'] = 0


duplicatedNames  = Names.duplicate(  **args )
duplicatedNamesB = NamesB.duplicate( **args )
duplicatedNamesC = NamesC.duplicate( **args )

duplicateKey = str( args['value'] ) + args['mode']

for i in range(0,len(duplicatedNames)):
    duplicatedNames[i].swapRefsToDuplicate(  duplicateKey , i )
    duplicatedNamesB[i].swapRefsToDuplicate( duplicateKey , i )
    duplicatedNamesC[i].swapRefsToDuplicate( duplicateKey , i )
    
toExec = ''
for i in range(0,len(duplicatedNames)):
    duplicatedNames[i] += duplicatedNamesB[i]
    duplicatedNames[i] += duplicatedNamesC[i]
    toExec += duplicatedNames[i].build()

print(toExec)



args = {}
args['value']             = [10,0,0 , 0,15,0 , 0,0,1 , 5]
args['mode']              = 'transform'
args['pivot']             = [0,0,0 , 0,0,0 , 1,1,1]
args['namePrefix']        = ['','']
args['nameReplace']       = ['','']
args['nameIncr']          = 'toto0'
args['orientLockAxe']     = 0
args['orientInverseAxes'] = 0


duplicatedNames = Names.duplicate( **args )

for i in range(0,len(duplicatedNames)):
    print('================================= {}'.format(i) )
    print( duplicatedNames[i].base.str() )
    print( duplicatedNames[i].rigA.str() )
    print( duplicatedNames[i].ctrlA.str() )
    print( duplicatedNames[i].jointA.str() )
    


from python.classe.buildName import *
reload(python.classe.buildName)

Names = buildName()
dictA = Names.decomposeName('l_pCubeA1_CTRL')
dictB = Names.decomposeName('pCubeA_CTRL')
dictC = Names.decomposeName('r_pCubeA4_CTRL')


Names.convertNamesToMatchExemple( ['pCubeA_CTRL' , 'pSphereAToto2_CTRL']  , 'l_pCubeA1_CTRL' )




'''




import maya.cmds as mc

from ..utils import utilsMaya
from ..utils import utilsPython
from ..utils import utilsMath
from ..utils import utilsMayaApi
from .build import *
import string

import types
import re


class buildName( build ):

	def __init__(self , **args):
		build.__init__(self , **args )
		#____________________________________________________________________RIG INFO
		#UTILS	
		self.suffixTypeDict = {}	
		self.suffixTypeDict['GRP']    = [ 'groupe' , 'grp' ] 
		self.suffixTypeDict['OFFSET'] = [ 'offset' ] 
		self.suffixTypeDict['CTRL']   = [ 'ctrl' , 'manip' , 'control' ] 	
		self.suffixTypeDict['JNT']    = [ 'jnt' , 'joint' , 'skin' ] 	
		self.suffixTypeDict['LOC']    = [ 'loc' , 'locator' ] 	
		self.suffixTypeDict['IKH']    = [ 'ik' , 'ikHandle' ] 	
		self.suffixTypeDict['Shape']  = [ 'shape' ] 	
		self.suffixTypeDict['MODIF']  = [ 'modif' ] 		
		self.sides    = ['l' , 'r']	
		self.types    = ['GRP' , 'OFFSET' , 'CTRL' , 'JNT' , 'LOC' , 'IKH' , 'Shape' , 'MODIF' ]	
		self.typeDict = { 'GRP' : 'transform' , 'OFFSET' : 'transform' , 'CTRL' : 'transform' , 'JNT' : 'joint' , 'LOC' : 'locator' , 'hrc' : 'transform' , 'MODIF' : 'transform' }																			
		self.lods     = ['hi','low']
		#CLASSE
		self.classeType   = 'buildName'		
		self.argsValue    = ['ref' , 'side' , 'type' , 'baseName' , 'baseNameAppend' , 'baseNameReplace' , 'copy' , 'prefixUnique' , 'suffixUnique' , 'suffixBeforeLod' ]


	def processValue( self , value , valueToAdd , operation , index = None , updateData = False  ):
		#VALUE______GET STR VERSION
		valueStr = ''
		if(   value == None                     ): valueStr = ''
		elif( type(value) == types.InstanceType ): valueStr = value.value( updateData = updateData )
		else:                                      valueStr = value

		valueDict = self.decomposeName( valueStr )
		#VALUE TO ADD______GET STR VERSION
		valueToAddDict = {}
		if(   type(valueToAdd) == types.InstanceType ): valueToAddStr = valueToAdd.value( updateData = updateData )
		elif( type(valueToAdd) == types.ListType     ): valueToAddStr = ''
		else:                                           valueToAddStr = valueToAdd
		#VALUE TO ADD______SPLIT
		valueToAddDict = self.decomposeName( valueToAddStr , operation )
		#OPERATION
		if(   operation == 'ref'      ):        valueDict['baseSplit'].insert( 0 , valueToAddDict['base'] )		
		elif( operation == 'side'     ):        valueDict['side']      = valueToAddDict['side']
		elif( operation == 'baseName' ):        valueDict['baseSplit'] = [ valueToAddDict['base'] ]
		elif( operation == 'baseNameAppend' ):  valueDict['baseSplit'].append( valueToAddDict['base'] )
		elif( operation == 'type'     ):        valueDict['type'] = valueToAddDict['type']
		elif( operation == 'copy'     ):  
			for key in valueToAddDict.keys():
				valueDict[key] = valueToAddDict[key]      
			#valueDict['baseSplit'] = [ valueToAddDict['base'] ]		
			#valueDict['side']      = valueToAddDict['side']
			#valueDict['type']      = valueToAddDict['type']


		elif( operation == 'baseNameReplace' ) and not( valueToAdd[0] == '' ):

			for i in range( 0 , len( valueDict['baseSplit'] ) ):
				if( valueDict['baseSplit'][i] == valueToAdd[0] ): 
					valueDict['baseSplit'][i]  = valueToAdd[1]

		elif( operation == 'prefixUnique' ):

			#MAKE IT UNIQUE IN THE BASE NAME			
			for i in range( 1 , len( valueDict['baseSplit'] ) ):
				if( valueDict['baseSplit'][i] == valueToAddDict['base'] ):
					valueDict['baseSplit'].pop(i)

			valueDict['baseSplit'].insert( 0 , valueToAddDict['base'] )

		elif( operation == 'suffixUnique' ):
			#????	
			valueDict['base'] = valueDict['baseSplit'][0]		
			
			#MAKE IT UNIQUE IN THE BASE NAME
			for i in range( 1 , len( valueDict['baseSplit'] ) ):
				if( valueDict['baseSplit'][i] == valueToAddDict['base'] ):
					valueDict['baseSplit'].pop(i)

			valueDict['baseSplit'].append( valueToAddDict['base'] )

		elif( operation == 'suffixBeforeLod' ):	
			#????	
			valueDict['base'] = valueDict['baseSplit'][0]	

			#MAKE IT UNIQUE IN THE BASE NAME
			for i in range( 1 , len( valueDict['baseSplit'] ) ):
				if( valueDict['baseSplit'][i] == valueToAddDict['base'] ):
					valueDict['baseSplit'].pop(i)

			insertIndex = None
			for i in range( len(valueDict['baseSplit'])-1 , -1 , -1 ):
				if( valueDict['baseSplit'][i] in self.lods ):
					insertIndex = i 
					break
					
			if not( insertIndex == None ): valueDict['baseSplit'].insert( insertIndex , valueToAddDict['base'] )
			else:                          valueDict['baseSplit'].append( valueToAddDict['base'] )

		#GET PARENT
		if not( index == None ):
			parent                      = self.ref( index = index , key = 'parent'                      , updateData = updateData )
			parentChildrenAndDeleteName = self.ref( index = index , key = 'parentChildrenAndDeleteName' , updateData = updateData )

			if not( parent == None ) and not( parentChildrenAndDeleteName == True ) and not ( operation == "copy" ):
				valueDict['parent'] = parent
		
		#EXTRA
		if( valueDict['type'] == 'hrc' ): valueDict['side'] = ''
		#BUILD STR
		return self.composeName(valueDict)


	def processBuild( self , refs , value ):
		parent     = refs.get('parent'   ,None )
		swap       = refs.get('swap'     ,False)	
		objExists  = refs.get('objExists',False)	


		if not( swap      == False ): return ''
		if not( objExists == False ): return ''

		valueDict  = self.decomposeName( value )

		nodeName   = valueDict['name']		

		suffixType = valueDict.get('type', None)
		if( suffixType in [ None, '' ] ) or not ( suffixType in self.typeDict.keys() ): return ''
		nodeType = self.typeDict[suffixType]

		buildCmds = 'utilsMaya.dagSafeBuild( "{}" , "{}" , "{}" )\n'.format( nodeType , nodeName , parent )

		#buildCmds += 'rawName = mc.createNode( "{}" , n = "{}" )\n'.format(nodeType,nodeName)
		#buildCmds += 'transformNode = mc.listRelatives( rawName , p = True  )\n'
		#buildCmds += 'if not( transformNode == None):rawName = mc.rename( transformNode , "{}" )\n'.format(nodeName)
		#buildCmds += 'utilsMaya.safeParent(rawName,"{}")\n'.format( parent )
		
		return buildCmds


	def utils_dataIsBuildable( self , index ):

		for value in self.data[index]['value']:
			if( 'type' in value.keys() ) and not( value['type'] in [None,'None']  ):
				return True

		return False


	def processDataFlat( self , dataFlat ):

		#SORT IN BUILD ORDER
		names   = [ data.get('value' ,'') for data in dataFlat ]
		fathers = [ data.get('parent','') for data in dataFlat ]

		rootIndexes = utilsPython.sortIndexChildrensByHierarchy( names , fathers )

		dataFlat   = [ dataFlat[i] for i in rootIndexes ]

		#SWAP AND DELETE VALUES
		namesToSwap = [ data['value']  for data in dataFlat if data.get('parentChildrenAndDeleteName',None) ]
		fathers     = [ data['parent'] for data in dataFlat if data.get('parentChildrenAndDeleteName',None) ]

		for i in range( 0 , len(dataFlat) ):
			if( dataFlat[i].get('parent','') in namesToSwap ):
				index = namesToSwap.index(dataFlat[i]['parent'])
				dataFlat[i]['parent'] = fathers[index]

		dataFlat = [ data for data in dataFlat if not( data['value'] in namesToSwap ) ]

		return dataFlat 




	def processDuplicate( self , duplicateds , **args ):
		value             = args.get( 'value'             , [0,0,0 , 0,1,0 , 0,0,1] )		
		mode              = args.get( 'mode'              , 'mirror'                )	
		pivot             = args.get( 'pivot'             , [0,0,0 , 0,0,0 , 1,1,1] )
		namePrefix        = args.get( 'namePrefix'        , []                      )		
		nameReplace       = args.get( 'nameReplace'       , []                      )	
		nameIncr          = args.get( 'nameIncr'          , ''                      )
		nameAdd           = args.get( 'nameAdd'           , []                      )
		orientLockAxe     = args.get( 'orientLockAxe'     , 2                       )
		orientInverseAxes = args.get( 'orientInverseAxes' , 0                       )


		letters = string.ascii_uppercase

		duplicatedsProcessed = []
		for i in range( 0 , len(duplicateds) ):
			instanceTmp = duplicateds[i] 

			baseNameSuffix = None
			prefix         = None
			replace        = None
			add            = None
	
			if(   nameIncr == 'A'    ): baseNameSuffix = letters[i]
			elif( nameIncr == '0'    ): baseNameSuffix = '{}'.format(i)
			elif( 0 < len(nameIncr) ) and ( nameIncr[-1] == '0' ): replace = [ nameIncr[0:len(nameIncr)-1] , '{}{}'.format(nameIncr[0:len(nameIncr)-1] , i         ) ]
			elif( 0 < len(nameIncr) ) and ( nameIncr[-1] == 'A' ): replace = [ nameIncr[0:len(nameIncr)-1] , '{}{}'.format(nameIncr[0:len(nameIncr)-1] , letters[i]) ]
	
			if( i < len(namePrefix )     ):prefix  = namePrefix[i]
			if( i < len(nameReplace)     ):replace = [ nameReplace[0] , nameReplace[i] ]
			if( i < len(nameAdd    )     ):add     = nameAdd[i]
	
			for j in range( 0 , len(self.data) ):
				key       = self.data[j]["key"]
				objExists = instanceTmp.ref( index = j , key = 'objExists' , convertInstance = False )

				if( objExists ):

					if( i == 0 ):continue
					#print('OBJ EXISTS----------------------------------------- {}'.format(instanceTmp.value(j)) )
					dupliAttr = instanceTmp.value(j) + '.dupli'

					if( mc.objExists(dupliAttr) ):
						#print('\tATTR EXISTS----------------------------------------- {}'.format(dupliAttr) )
						dupliInfo = dupliAttr_extractInfoArray( dupliAttr)


						for j in range( 0 , len(dupliInfo) , 4 ):
							#print('\t\tdupliKey     {} {} {}'.format( value , mode , pivot) )
							#print('\t\tdupliKeyTest {} {} {}'.format( dupliInfo[j+1] , dupliInfo[j+2] , dupliInfo[j+3]) )							
							dupliKey     = [ value          , mode           , pivot          ]
							dupliKeyTest = [ dupliInfo[j+1] , dupliInfo[j+2] , dupliInfo[j+3] ]

							if( dupliKey == dupliKeyTest ):
								instanceTmp.add( key , copy = dupliInfo[j+0] )
								#print('\t\t\tREPLACE <----- {}'.format( dupliInfo[j+0]) )
													
				else:

					if( prefix         ):instanceTmp.add( key , side    = prefix )
					if( replace        ):instanceTmp.add( key , baseNameReplace = replace )
					if( baseNameSuffix ):instanceTmp.add( key , baseNameAppend = baseNameSuffix )
					if( add            ):instanceTmp.add( key , suffixBeforeLod = add )
			
			duplicatedsProcessed.append(instanceTmp) 		

		return duplicatedsProcessed

	def str( self ):
		return self.value()

	'''
	def processCopy( self , newInstance ):

		for j in range( 0 , len(self.data) ):
			key          = self.data[j]["key"]
			newInstance.add( key , copy = eval('self.{}'.format(key) ) )

		return newInstance
	'''

	def decomposeName( self , name , operation = None ):

		parent = ''
		if( '|' in name ):
			splitTmp = name.split('|')
			parent = '|'.join(splitTmp[ 0:len(splitTmp)-1] )
			name = splitTmp[-1]

		namespace = ''
		if( ':' in name ):
			namespace = name.split(':')[0]
			name = name.split(':')[1]

		splitTmp  = name.split('_')
		valueDict = {}

		if(   len(splitTmp) == 3 ):                                      valueDict = { 'side' : splitTmp[0] , 'base' : splitTmp[1] , 'type' : splitTmp[2] }						
		elif( len(splitTmp) == 2 ) and    ( splitTmp[0] in self.sides ): valueDict = { 'side' : splitTmp[0] , 'base' : splitTmp[1] , 'type' : ''          }				
		elif( len(splitTmp) == 2 ) and not( splitTmp[0] in self.sides ): valueDict = { 'side' : ''          , 'base' : splitTmp[0] , 'type' : splitTmp[1] }										
		elif( len(splitTmp) == 1 ) and    ( splitTmp[0] in self.sides ): valueDict = { 'side' : splitTmp[0] , 'base' : ''          , 'type' : ''          }	
		elif( len(splitTmp) == 1 ) and    ( splitTmp[0] in self.types ): valueDict = { 'side' : ''          , 'base' : ''          , 'type' : splitTmp[0] }	
		elif( len(splitTmp) == 1 ) and    ( operation == "side"       ): valueDict = { 'side' : splitTmp[0] , 'base' : ''          , 'type' : ''          }	
		elif( len(splitTmp) == 1 ) and    ( operation == "type"       ): valueDict = { 'side' : ''          , 'base' : ''          , 'type' : splitTmp[0] }					
		else: 														     valueDict = { 'side' : ''          , 'base' : splitTmp[0] , 'type' : ''          }	

		baseSplitTmp = [ elem.lower() for elem in re.findall( '[A-Z][^A-Z]*', capitalizeFirst( valueDict['base'] ) ) ]
		if( len(baseSplitTmp) == 0 ): baseSplitTmp = [ valueDict['base'] ] 	

		baseSplit = []
		for i in range( len(baseSplitTmp) ):
			num = ''
			for char in baseSplitTmp[i]:
				if( char in string.digits ): num += char

			if( len( num ) ):
				numSplit = baseSplitTmp[i].split( num )
				baseSplit += [ numSplit[0] , num , numSplit[1] ]
			else:
				baseSplit.append( baseSplitTmp[i] )

		valueDict['baseSplit'] = [ elem for elem in baseSplit if not( elem == '' ) ]

		valueDict['name']   = name
		valueDict['parent'] = parent
		valueDict['split']  = splitTmp
		valueDict['namespace']  = namespace

		return valueDict

	def composeName( self , valueDict ):

		#BUILD BASE
		bSplit   =  valueDict['baseSplit']
		baseName = valueDict['base']
		if( 0 < len(bSplit) ):
			baseName = bSplit[0]
			for i in range( 1 , len(bSplit) ):
				baseName += capitalizeFirst(bSplit[i])

		valueDict['base'] = baseName
		#OVERRIDE TYPE
		for suffix in self.suffixTypeDict.keys():
			if( valueDict['type'] in self.suffixTypeDict[suffix] ):
				valueDict['type'] = suffix
		#BUILD ALL
		name = '{}_{}_{}'.format( valueDict['side'] , valueDict['base'] , valueDict['type'] )
		if( name[0]  == '_' ): name = name[1:]
		if( name[-1] == '_' ): name = name[:-1]


		if not( valueDict['namespace'] == '' ):
			name = valueDict['namespace'] + ':' + name

		if not( valueDict['parent'] == '' ):
			name = valueDict['parent'] + '|' + name

		return name

	def convertNamesToMatchExemple( self , objs , objToMatch ):
		Names = buildName()
		dictNameRef = Names.decomposeName(objToMatch)

		convertedObjs = []
		#GET CONVERTED OBJS
		for obj in objs:
			dictName = Names.decomposeName(obj)
			#SIDE
			dictName['side'] = dictNameRef['side']
			#BASENAME
			for i in range( len(dictNameRef['baseSplit'])-1 ):
				if( len(dictNameRef['baseSplit'][i+1]) == 1 ):
					if( dictName['baseSplit'][i] == dictNameRef['baseSplit'][i]   ):
						if(  len( dictName['baseSplit'] ) <= i+1 ):
							dictName['baseSplit'].append(dictNameRef['baseSplit'][i+1])
						else:
							if not( dictName['baseSplit'][i+1] == dictNameRef['baseSplit'][i+1] ):
								if(( len(dictName['baseSplit'][i+1]) == 1 )):
									dictName['baseSplit'][i+1] =  dictNameRef['baseSplit'][i+1]
								else:
									dictName['baseSplit'].insert( i+1  , dictNameRef['baseSplit'][i+1] )
								break

			convertedObjs.append( Names.composeName(dictName) )

		return convertedObjs


def capitalizeFirst( name ):

	if not( name == None ) and not( name == '' ):

		if( 1 < len(name) ):
			return name[0].capitalize() + name[1:]
		else:
			return name[0].capitalize()
	else:
		return ''
	
def dupliAttr_extractInfoArray( objAttr ):
	infoArray = []

	valueTmp = mc.getAttr( objAttr )
	valueTmpSplit = valueTmp.split(" ")

	bufferTmp = ''
	isArray = 0
	for v in valueTmpSplit:

		if( '[' in v ): isArray = 1
		if( ']' in v ): isArray = 0

		bufferTmp += v

		if( isArray == 0 ):
			if not( bufferTmp in [''] ):infoArray.append(bufferTmp)
			bufferTmp = ''

	#CONVERT ARRAY STR TO ARRAY
	for i in range(0,len(infoArray)):
		if( infoArray[i][0] == '[' ) and ( infoArray[i][-1] == ']' ):
			infoArray[i] = eval( infoArray[i] )

	return infoArray