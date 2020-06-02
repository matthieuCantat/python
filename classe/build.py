'''    
import python
from python.classe.build import *
reload(python.classe.build)

Names = build( )


import python
from python.classe.build import *
from python.classe.buildAttribute import *
from python.classe.buildCurveShape import *
from python.classe.buildDag import *
from python.classe.buildLink import *
from python.classe.buildName import *
from python.classe.buildParent import *
from python.classe.buildPosition import *

reload( python.classe.build)
reload( python.classe.buildAttribute)
reload( python.classe.buildCurveShape)
reload( python.classe.buildDag)
reload( python.classe.buildLink)
reload( python.classe.buildName)
reload( python.classe.buildParent)
reload( python.classe.buildPosition)


'''

import maya.cmds as mc
import types
import copy


from ..utils import utilsMaya
from ..utils import utilsPython
from ..utils import utilsMath
from ..utils import utilsMayaApi




class build():
	
	def __init__(self , **args):
		#buildClasse.__init__(self , **args )
		#CHILDREN
		self.classeType    = 'build'	
		self.argsValue     = []
		#self.skipRefValues = []
		#UTILS
		self.data            = args.get( 'data'            , []   )		
		self.dataFlat        = []
		self.index           = args.get( 'index'           , None )	
		self.keyToDuplicated = args.get( 'keyToDuplicated' , {}   )
		self.argsRef         = args.get( 'argsRef'         , []   )	


	#_______________________________________________ ADD
	def add( self , key , **args ):
		self.updateAddArgsInfo(**args)
		self.dataAdd( key , **args )
		

	def updateAddArgsInfo(self,**args):
		for arg in args.keys():
			if not( arg in self.argsValue ) and not( arg in self.argsRef ):
				self.argsRef.append(arg)

	def utils_dataGetKeyIndex( self , key ):
		keyIndex = None
		for i in range( 0 , len(self.data) ):
			if( key == self.data[i]['key'] ):
				keyIndex = i
				break
		return keyIndex

	def dataAdd( self , key , **args ):
		#CONVERT ARGS TO VALUE
		value    = []
		addFirst        = args.pop( 'addFirst'       , None )	
		append          = args.pop( 'append'         , None )
		clear           = args.pop( 'clear'          , None )
		incrKeyIfExist  = args.pop( 'incrKeyIfExist' , None )

		for argsKey in args.keys():
			value.append( { argsKey : args[argsKey] } )

		if not( append == None ):
			value += append

		#ADD VALUE IN DATA
		if(self.index == None): keyIndex = self.utils_dataGetKeyIndex(key)
		else:                   keyIndex = self.index 

		#INCR KEY
		if not( incrKeyIfExist == None ):
			lap , stop = 0 , 0
			while not( keyIndex == None ):
				key = '{}{}'.format(key,lap)
				keyIndex = self.utils_dataGetKeyIndex(key)
				lap += 1
				if(500<lap):
					mc.error('build.dataAdd - incr key - Loop')


		#ADD VALUE IN DATA
		if( keyIndex == None ):

			newData = { 'key' : key  , 'value' : value }

			if( addFirst == None):self.data.append( newData )
			else:         		  self.data.insert( 0 , newData )

			#CREATE NEW CLASSE IN ATTRIBUT
			toExec  = 'from .{} import *;'.format(self.classeType)
			toExec += 'self.{} = {}( data = self.data , index = {} , keyToDuplicated = self.keyToDuplicated , argsRef = self.argsRef  )'.format( key , self.classeType , len( self.data )-1  )
			exec( toExec )
		else:
			if( clear == None ): self.data[keyIndex]['value'] += value
			else:                self.data[keyIndex]['value']  = value

	#_______________________________________________ REMOVE
	def remove( self , key ):
		self.dataRemove( key)
		
	def dataRemove( self , key ):
		#CONVERT ARGS TO VALUE
		value    = []
		#REMOVE VALUE IN DATA
		if(self.index == None): keyIndex = self.utils_dataGetKeyIndex(key)
		else:                   keyIndex = self.index 

		#REMOVE VALUE IN DATA
		if( keyIndex == None ):
			return 0
		else:
			#self.data[keyIndex]['key']   = None
			self.data[keyIndex]['value'] = []

			#toExec = 'del(self.{})'.format( key )
			#exec( toExec )
			
			return 1

	#_______________________________________________ BUILD
	def value(self , index = None , updateData = False ):
		
		#CHECK IF THERE IS AN index OR argsValue
		if( index == None ): index = self.index
		if( index == None ) or ( self.argsValue == [] ): return None

		#IF valueResult EXIST RETURN valueResult
		valueHistory = self.data[index]['value']
		for v in valueHistory:
			if( 'valueResult' in v.keys() ):
				return v['valueResult']

		#COMPUTE VALUE
		values = self.data_getValue( index , keepKeys = self.argsValue , skipValues = [ None ] , keepLastDuplicateKey = None  )
		values = self.preProcessValues( values )

		newValue = None 
		for i in range( 0 , len(values) ):
			key      = values[i].keys()[0]
			value    = values[i][key]
			newValue = self.processValue( newValue , value , key , index = index , updateData = updateData )

		# ADD valueResult TO DATA
		if(updateData):
			self.data[index]['value'].append( { 'valueResult' : newValue } )

		return newValue

	def preProcessValues( self , values ):
		return values

	def processValue( self , value , valueToAdd , operation , index = None , updateData = False):
		return None


	def refs(self , index = None , convertInstance = True , updateData = False ):

		#CHECK IF THERE IS AN index OR argsValue
		if( index == None ): index = self.index
		if( index == None ): return {} #if( index == None ) or ( self.argsRef == [] ): return {}

		#GET REFS
		values = self.data_getValue( index , skipKeys = self.argsValue , skipValues = [ None ] , keepLastDuplicateKey = True  )

		#CONVERT VALUE TO DICT
		refs = {}
		for i in range( 0 , len(values)):
			key   = values[i].keys()[0]
			value = values[i][key]
			refs[key] = value

		#CONVERT REF INSTANCE TO VALUE
		if( convertInstance == True ):
			for key in refs.keys():

				if( type( refs[key] ) == types.ListType ):
					for i in range( 0 , len(refs[key]) ):
						if( type( refs[key][i] ) == types.InstanceType ):

							refs[key][i] = refs[key][i].value( updateData = updateData )

							if( updateData ):
								valueHistoryIndexes = self.utilsData_getValueHistoryIndexesFromKey( index , key )
								valueHistoryIndex   = valueHistoryIndexes[-1]
								self.data[index]['value'][valueHistoryIndex][key][i] = refs[key][i]

				elif( type( refs[key] ) == types.InstanceType ): 

					refs[key] = refs[key].value( updateData = updateData )

					if( updateData ):
						valueHistoryIndexes = self.utilsData_getValueHistoryIndexesFromKey( index , key )
						valueHistoryIndex   = valueHistoryIndexes[-1]						
						self.data[index]['value'][valueHistoryIndex][key] = refs[key]
	

		return refs


	def ref(self , index = None , key = None , convertInstance = True , updateData = False ):

		#CHECK IF THERE IS AN index OR argsValue
		if( index == None ): index = self.index
		if( index == None ): return [] #if( index == None ) or ( self.argsRef == [] ): return []

		#GET REFS
		values = self.data_getValue( index , skipKeys = self.argsValue , skipValues = [ None ] , keepLastDuplicateKey = True  )
		#CONVERT VALUE TO DICT
		valueOut = None
		for i in range( 0 , len(values)):
			if( key == values[i].keys()[0] ):
				valueOut = values[i][key]
		#CONVERT REF INSTANCE TO VALUE
		if( convertInstance == True ):
			if( valueOut == types.ListType ):
				for i in range( 0 , len(valueOut) ):
					if( type( valueOut[i] ) == types.InstanceType ):

						valueOut[i] = valueOut[i].value( updateData = updateData )

						if( updateData ):
							valueHistoryIndexes = self.utilsData_getValueHistoryIndexesFromKey( index , key )
							valueHistoryIndex   = valueHistoryIndexes[-1]
							self.data[index]['value'][valueHistoryIndex][key][i] = valueOut[i]

			elif( type( valueOut ) == types.InstanceType ): 

				valueOut = valueOut.value( updateData = updateData )

				if( updateData ):
					valueHistoryIndexes = self.utilsData_getValueHistoryIndexesFromKey( index , key )
					valueHistoryIndex   = valueHistoryIndexes[-1]						
					self.data[index]['value'][valueHistoryIndex][key] = valueOut

		return valueOut

	def processDataFlatForBuild(self):
		pass

	def utils_dataIsBuildable(self , index ):
		return True



	def build( self ):
		buildCmds = ''
		self.dataFlat = self.processDataFlat(self.dataFlat)

		for i in range(0,len(self.dataFlat) ):
			value = self.dataFlat[i].get( 'value' , None )
			
			refs = {}
			for key in self.dataFlat[i].keys():
				if not( key == 'value' ):
					refs[key] = self.dataFlat[i][key]
			
			buildCmds += self.processBuild( refs , value )

		return buildCmds

	def processDataFlat( self , dataFlat ):
		return dataFlat

	def dataFlatReorderCustom(self):
		'''
			last reorder possible before build (see buildLink)
		'''
		pass

	def processBuild( self , refs , value ):
		return ''

	def data_getValue( self , index , skipKeys = [] , skipValues = [] , keepLastDuplicateKey = None , keepKeys = None ):

		values = self.data[index]['value']

		keyLastIndex = {}
		for i in range( 0 , len(values) ):
			key   = values[i].keys()[0]
			keyLastIndex[key] = i
			
		valueOut = []
		for i in range( 0 , len(values) ):
			key   = values[i].keys()[0]
			value = values[i][key]

			if not( key in skipKeys ) and not( value in skipValues ):

				if( keepKeys == None ):

					if(keepLastDuplicateKey):
						if( keyLastIndex[key] == i ):
							valueOut.append( values[i] )
					else:
						valueOut.append( values[i] )

				elif( key in keepKeys ):

					if(keepLastDuplicateKey):
						if( keyLastIndex[key] == i ):
							valueOut.append( values[i] )
					else:
						valueOut.append( values[i] )

				else:
					pass

		return valueOut

	'''
	def utils_dataValueExtract( self , index , keysToExtract = [] ):
		values = self.data[index]['value']

		valuesExtracted = []
		for i in range( 0 , len(values) ):
			key = values[i].keys()[0]

			if( key in keysToExtract):
				valuesExtracted.append( values[i] )

		return valuesExtracted

	def utils_dataValueExtractLasts( self , index  , keysToExtract = [] , skipValues = [] ):
		values    = self.data[index]['value']

		dictLasts = {}
		for i in range( 0 , len(values) ):
			key   = values[i].keys()[0]
			value = values[i][key]
			if( key in keysToExtract )and not( value in skipValues ):
				dictLasts[key] = value

		return dictLasts
	'''

	#_______________________________________________ DEBUG
	def valuePrint(self , index = None ):
		return self.value(index)

	def printInfo( self , key = None ):

		if( key == None ):
			print(' ')
			print(' ')
			print(' ')
			print(' ')
			print('###########################################################################################')
			print('START ########################################################################## PRINT INFO {}'.format(self.classeType) )
			print('###########################################################################################')
			print(' ')
			print(' ')
			for i in range(0,len(self.data) ):
				key      = self.data[i]['key']
				rawValue = self.data[i]['value']
				refs     = self.refs(i)
				value    = self.valuePrint(i)
				print('============================================================== {}     {}/{}'.format( key , i+1 , len(self.data) ) )
				print('________________________________________________RAW DATA')
				print(rawValue)
				print('________________________________________________OUTS')
				print( '***key***** ----->'  ,  key  )
				print( '***refs**** ----->' ,  refs  )
				print( '***value*** ----->' ,  value )
				print('________________________________________________VALUE HISTORY')
				print('START')
				self.utils_printValueHistory( i )
				print( '***{}***'.format( value ) )	
				print('END')
				print(' ')
				print(' ')
	
	
			print('###########################################################################################')
			print('END ############################################################################ PRINT INFO {}'.format(self.classeType) )
			print('###########################################################################################')
			print(' ')
			print(' ')
		else:
			index = None
			for i in range(0,len(self.data) ):
				if( key == self.data[i]['key'] ):
					index = i
					break
			
			if not( index == None ):
				rawValue = self.data[index]['value']
				nameStr = ''
				for elem in rawValue:
					Name = elem.get( 'Name' , None )
					if not( Name == None ):
						nameStr = Name.str()




				print( nameStr , rawValue )
			else:
				print(' no key: {}'.format(key))

				

	def printData( self ):
		
		for i in range( 0 , len( self.data) ):
			elem = self.data[i]
			print( '{}/{} {}'.format( i , len( self.data ) , elem['key'] ) )
			
			#PUT SAME VALUE TYPE IN A LIST
			dictArray = {}
			for value in elem['value']:
				key = value.keys()[0]
				dictArray.setdefault( key , [] )
				dictArray[key].append( value[key] )
			
			#GET VALUE TYPE NAME LENGTH MAX    
			keyValueLengths = [ len(key) for key in dictArray.keys() ]
			keyValueLengthMax = 0
			for l in keyValueLengths:
				if( keyValueLengthMax < l ):
					keyValueLengthMax = l
			    
			for key in dictArray.keys():
				lenDelta = keyValueLengthMax - len(key)
				#CONVERT NAME
				for j in range( 0 , len(dictArray[key]) ):
					if( type(dictArray[key][j]) == types.InstanceType ):
						dictArray[key][j] = dictArray[key][j].value()

				#PRINT
				print('\t{}{} : {} {}'.format( key , ' '*lenDelta , len(dictArray[key]) , dictArray[key] ) )
				
		

	def utils_printValueHistory( self , index , shift = ''):
		shift  += '\t'

		for values in self.data[index]['value']:
			key   = values.keys()[0]
			if not( key in self.argsValue ):
				continue
			value = values[key]
			if( type(value) == types.InstanceType ):
				print( '{}--->REF'.format( shift ) )
				value.utils_printValueHistory( value.index , shift = shift )
				print( '{}***{}***'.format( shift , value.value() ) )
			else:
				print( '{}{} ({})'.format( shift , value , key ) )



	#_______________________________________________ DUPLICATE
	# modes   = [ 'mirror' , 'tranform , 'axe' ]
	# nameIncrs = [ 'A' , '0' , 'B' , '1' ]
	def duplicate( self , **args ):
		value             = args.get( 'value'             , [0,0,0 , 0,1,0 , 0,0,1] )		
		mode              = args.get( 'mode'              , 'mirror'                )	
		pivot             = args.get( 'pivot'             , [0,0,0 , 0,0,0 , 1,1,1] )
		namePrefix        = args.get( 'namePrefix'        , []               )		
		nameReplace       = args.get( 'nameReplace'       , []                 )	
		nameIncr          = args.get( 'nameIncr'          , ''                      )
		nameAdd           = args.get( 'nameAdd'           , []                      )
		noneMirrorAxe     = args.get( 'noneMirrorAxe'     , 2                       )


		duplicateKey = str(value) + mode

		nbrInstance = 2
		if( type(value) == types.ListType ) and ( 9 < len(value) ): 
			nbrInstance = value[9]

		duplicateds = [ self.copy() for i in range( 0 , nbrInstance ) ]
		duplicateds = self.processDuplicate( duplicateds , **args )
		#dupli KEY	
		self.keyToDuplicated[duplicateKey] = duplicateds

		return duplicateds

	def processDuplicate( self , duplicateds , **args ):
		value             = args.get( 'value'             , [0,0,0 , 0,1,0 , 0,0,1] )		
		mode              = args.get( 'mode'              , 'mirror'                )	
		pivot             = args.get( 'pivot'             , [0,0,0 , 0,0,0 , 1,1,1] )
		namePrefix        = args.get( 'namePrefix'        , []                      )		
		nameReplace       = args.get( 'nameReplace'       , []                      )	
		nameIncr          = args.get( 'nameIncr'          , ''                      )
		nameAdd           = args.get( 'nameAdd'           , []                      )
		noneMirrorAxe     = args.get( 'noneMirrorAxe'     , 2                       )	
		return duplicateds


	def copy(self):
		instanceTmp = None
		exec('if not( "{0}" in dir() ): from .{0} import *;'.format(self.classeType) ) 
		exec('instanceTmp = {}()'.format(self.classeType) ) 
		#FILL DATA
		for j in range( 0 , len(self.data) ):

			key          = self.data[j]["key"]
			valueHistory = self.data[j]["value"]

			instanceTmp.add( key , empty = True ) # change that ! ( modif build attribute)
			for k in range( 0 , len(valueHistory) ):
				keyB   = self.data[j]["value"][k].keys()[0]
				instanceTmp.data[j]["value"].append( { keyB : self.data[j]["value"][k][keyB] } )

		return self.processCopy( instanceTmp )


	def processCopy( self , newInstance ):
		return newInstance


	def swapRefsToDuplicate( self , duplicateKey , dupliIndex = 0 , debug = 0 ):
		if( self.index == None ):
			for j in range( len(self.data) ): self.dataValue_swapRefsToDuplicate( j          , duplicateKey , dupliIndex , debug )		
		else:                                 self.dataValue_swapRefsToDuplicate( self.index , duplicateKey , dupliIndex , debug )


	def dataValue_swapRefsToDuplicate( self , index , duplicateKey , dupliIndex , debug = 0 ):
		
		if(debug):print('swapRefsToDuplicate: {} - {} - duplicateKey: {} - dupliIndex: {}'.format( self.classeType , self.data[index]["key"] , duplicateKey , dupliIndex ) )
		
		valueHistory = self.data[index]["value"]

		for i in range( 0 , len(valueHistory) ):
			key   = valueHistory[i].keys()[0]
			value = valueHistory[i][key]
			if( key in self.argsValue ):continue

			if( type(value) == types.InstanceType ):

				if(debug):print('\t{}: {} {}'.format( key , value.value() , value ) )

				duplicated = self.utils_getDuplicated( value , duplicateKey , dupliIndex )
				if not( duplicated == None ):  
					self.data[index]["value"][i][key] = eval( 'duplicated.{}'.format( value.utils_getCurrentKey() ) )
					
					if(debug):print('\t\tSWAP!: {} {}'.format( self.data[index]["value"][i][key].value() , self.data[index]["value"][i][key] ) )

			elif( type(value) == types.ListType ):
				valueSwaped = value[:]

				for j in range( 0 , len(value) ):

					if( type(value[j]) == types.InstanceType ):

						if(debug):print('\t{} {}/{}: {} {}'.format( key , j , len(value) , value[j].value() , value[j] ) )

						duplicated = self.utils_getDuplicated( value[j] , duplicateKey , dupliIndex )
						if not( duplicated == None ):
							valueSwaped[j] = eval( 'duplicated.{}'.format(value[j].utils_getCurrentKey()) ) 
							swapAction = True
							if(debug):print('\t\tSWAP!: {} {}'.format( self.data[index]["value"][i][key][j].value() , self.data[index]["value"][i][key][j] ) )


				if not(value == valueSwaped):
					self.data[index]["value"][i][key] = valueSwaped #have to do that trick for avoiding unwanted reference with list


	def getDuplicatedInstance( self , duplicateKey , dupliIndex ):

		duplicateds = self.keyToDuplicated.get( duplicateKey , None )
		
		if not( duplicateds == None ):
			duplicated = duplicateds[dupliIndex]

			if( self.index == None ): return duplicated
			else:                     return eval('duplicated.{}'.format(self.data[self.index]["key"]) )

		return self	



	def utils_getDuplicated( self , instance , duplicateKey , dupliIndex ):
		duplicated  = None

		duplicateds = instance.keyToDuplicated.get( duplicateKey , None )
		if not( duplicateds == None ): duplicated = duplicateds[dupliIndex]

		return duplicated

	def utils_getCurrentKey(self):
		if not( self.index == None ):
			return self.data[self.index]['key']
		return None





	def utilsData_getKeyList(self):
		return [ valueH['key'] for valueH in self.data ]

	def utilsData_getValueHistoryIndexesFromKey( self , index , key ):
		valueHistoryIndexes = []

		valueHistory = self.data[index]['value']
		for i in range( 0 , len(valueHistory) ):
			if( key in valueHistory[i].keys() ):
				valueHistoryIndexes.append(i)
		
		return valueHistoryIndexes