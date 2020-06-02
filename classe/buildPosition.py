'''

#******************************************************** BUILD EXEMPLE

# NAMES
import python
from python.classe.buildName import *
reload(python.classe.buildName)
reload(python.classe.trsBackUp)
reload(python.classe.trsBackUp)


import maya.cmds as mc
mc.file( f = True , new = True )


Names = buildName( )

Names.add( 'base'   , baseNameAppend = 'toto'     , type = 'grp' )
Names.add( 'rigA'   , baseNameAppend = 'Arm'        , type = 'grp'   , ref = Names.base  )
Names.add( 'ctrlA'  , baseNameAppend = 'OffsetA'    , type = 'CTRL'  , ref = Names.rigA  )
Names.add( 'jointA'  , baseNameAppend = ''           , type = 'JNT'   , ref = Names.ctrlA )
Names.add( 'ctrlB'  , baseNameAppend = 'OffsetB'    , type = 'CTRL'  , ref = Names.rigA  )
Names.add( 'jointB'  , baseNameAppend = ''           , type = 'JNT'   , ref = Names.ctrlB )

# POS
from python.classe.buildPosition import *
reload(python.classe.buildPosition)

PosMaster = buildPosition()
PosMaster.add( 'A' , replace = [2,5,6,0,0,0,1,1,1]  )

Pos = buildPosition()
Pos.add(  'ctrlA'      , replace = PosMaster.A                                  , Name = Names.ctrlA  )
Pos.add(  'ctrlB'      , replace = Pos.ctrlA                                    , Name = Names.ctrlB  )
Pos.add(  'ctrlB'      , addLocal = [0,3,3,0,0,0,1,1,1]                                               )
Pos.add(  'ctrlAjoint' , replace = Pos.ctrlA                                    , Name = Names.jointA )
Pos.add(  'ctrlBjoint' , append = [{'replace': Pos.ctrlB} , {'aim': Pos.ctrlA}] , Name = Names.jointB )
Pos.add(  'toto'       , append = [{'replace': Pos.ctrlB} , {'aim': Pos.ctrlA}]                       )
Pos.add(  'tata'       , append = [{'replace': Pos.ctrlA} , {'aim': Pos.toto }]                       )


PosMaster.printInfo()
Pos.printInfo()

# DUPLI A
dupliValue = [0,0,0 , 0,1,0 , 0,0,1]
dupliMode  = 'mirror'

duplicatedPos   = Pos.duplicate(   dupliValue , dupliMode , [0,0,0 , 0,0,0 , 1,1,1] , namePrefix = ['r','l'] , nameReplace = ['toto','tata'] , nameIncr = '' , orientLockAxe = 0 , orientInverseAxes = 0  )
duplicatedNames = Names.duplicate( dupliValue , dupliMode , [0,0,0 , 0,0,0 , 1,1,1] , namePrefix = ['r','l'] , nameReplace = ['toto','tata'] , nameIncr = '' , orientLockAxe = 0 , orientInverseAxes = 0  )
duplicateKey = str(dupliValue) + dupliMode

duplicatedPos[1].printInfo()

for i in range( 0 , len(duplicatedNames)):
	duplicatedPos[i].swapRefsToDuplicate(  duplicateKey , dupliIndex = i )

# DUPLI B
dupliValue = [10,0,0 , 0,15,0 , 0,0,1 , 5]
dupliMode  = 'transform'

duplicatedPos   = Pos.duplicate(  dupliValue , dupliMode , [0,0,0 , 0,0,0 , 1,1,1] , namePrefix = ['',''] , nameReplace = ['',''] , nameIncr = 'A' , orientLockAxe = 0 , orientInverseAxes = 0  )
duplicatedNames = Names.duplicate( dupliValue , dupliMode , [0,0,0 , 0,0,0 , 1,1,1] , namePrefix = ['',''] , nameReplace = ['',''] , nameIncr = 'A' , orientLockAxe = 0 , orientInverseAxes = 0  )
duplicateKey    = str(dupliValue) + dupliMode

duplicatedPos[2].printInfo()

for i in range( 0 , len(duplicatedNames)):
	duplicatedPos[i].swapRefsToDuplicate(  duplicateKey , dupliIndex = i )


'''




import maya.cmds as mc

from ..utils import utilsMaya
from ..utils import utilsPython
from ..utils import utilsMath
from ..utils import utilsMayaApi
from ..utils import utilsRigPuppet 
from .build import *

import types
import copy

from .trsBackUp import *
from .coords import *


class buildPosition( build ):

	def __init__(self , **args):
		build.__init__(self , **args )
		#____________________________________________________________________RIG INFO
		#UTILS	
		self.ValueTrs       = trs()
		self.ValuesToAddTrs = trs()																				
		#CLASSE
		self.classeType   = 'buildPosition'	
		self.argsValue    = [ 'replace' , 'transform' , 'addLocal' , 'orient' , 'aim' , 'mirror' , 'blend' , 'overshoot' ] #DO SOMETHING LIKE REF?


	def processValue( self , value , valueToAdd , operation , index = None , updateData = False ):
		
		#VALUE______GET TRS VERSION
		self.ValueTrs.value = [0,0,0,0,0,0,1,1,1]
		if( value == None ):                                                                   pass
		elif( type(value) == types.InstanceType ) and ( value.classeType == "buildPosition" ): self.ValueTrs.value = value.value( updateData = updateData ) 
		elif( type(value) == types.InstanceType ) and ( value.classeType == "buildName"     ): pass
		elif( type(value) == types.StringType   ):                                             self.ValueTrs.createFromObj( value          , worldSpace = 1 )			
		elif( type(value) == types.ListType     ) and ( len(value) == 9 ):                     self.ValueTrs.value = value
		else:                                                                                  pass

		#VALUE TO ADD______GET TRS VERSION
		self.ValuesToAddTrs.value = [0,0,0,0,0,0,1,1,1]
		ValuesToAddTrs = [self.ValuesToAddTrs] 
		if( valueToAdd == None ):                                                                        pass	
		elif( type(valueToAdd) == types.InstanceType ) and ( valueToAdd.classeType == "buildPosition" ): ValuesToAddTrs[0].value = valueToAdd.value( updateData = updateData ) 
		elif( type(valueToAdd) == types.InstanceType ) and ( valueToAdd.classeType == "buildName"     ): pass
		elif( type(valueToAdd) == types.StringType   ):                                                  ValuesToAddTrs[0].createFromObj( valueToAdd          , worldSpace = 1 )
		elif( type(valueToAdd) == types.ListType     ):

			isTrsNum = True
			for v in valueToAdd:
				if not( type(v) in [ types.IntType , types.FloatType ] ):
					isTrsNum = False
					break

			if(isTrsNum): 
				for i in range(0,len(valueToAdd)):
					ValuesToAddTrs[0].value[i] = valueToAdd[i]
			else:
				ValuesToAddTrs = []
				for v in valueToAdd:
					if(   type(v) == types.InstanceType ) and ( v.classeType == "buildPosition" ): ValuesToAddTrs.append( trs( inValue = v.value( updateData = updateData ) ) ) 
					elif( type(v) == types.InstanceType ) and ( v.classeType == "buildName"     ): ValuesToAddTrs.append( trs( inValue = v.value( updateData = updateData ) ) ) 
					elif( type(v) == types.StringType   ):                                         ValuesToAddTrs.append( trs( inValue = v         ) )
					else:
						ValuesToAddTrs.append(v)

		#OPERATION
		if(   operation in ['replace','pos'] ): self.ValueTrs.value[0:9]  = ValuesToAddTrs[0].value[0:9] 					
		elif( operation == 'addLocal'        ): self.ValueTrs.offsetItself( ValuesToAddTrs[0].value[0:9] )
		elif( operation == 'orient'          ): self.ValueTrs.value[3:6]  = ValuesToAddTrs[0].value[3:6]	
		elif( operation == 'aim'             ): self.ValueTrs.aim(          ValuesToAddTrs[0].value[0:9] )	
		elif( operation == 'blend'           ): self.ValueTrs.blendArray(   ValuesToAddTrs , includeCurrent = 1 )
		elif( operation == 'overshoot'       ): self.ValueTrs.overshoot(    ValuesToAddTrs[0] , mult = ValuesToAddTrs[1] )			
		elif( operation == 'mirror'          ):

			mirror         = valueToAdd['value']
			noneMirrorAxe  = valueToAdd['noneMirrorAxe']

			#CONVERT PLAN COORDS
			planSymCoordsNew = utilsRigPuppet.convertMirrorInfoToCoords(mirror)
			self.ValueTrs.mirror( planSymCoordsNew , noneMirrorAxe = noneMirrorAxe )
			

		elif( operation == 'transform' ): 

			toMove        = self.ValueTrs.value
			pivot         = valueToAdd['pivot']
			transform     = valueToAdd['value']
			dupliPosOrder = valueToAdd['dupliPosOrder']

			Trs      = trs( toMove )
			TrsPivot = trs( pivot )			

			for i in range(0,dupliPosOrder):
			    Trs.offsetTrs( pivot , transform )
			    TrsPivot.offsetItself( pivot , transform )
			    pivot = TrsPivot.value

			self.ValueTrs.value = Trs.value

		else:
			ValueTrs.value[0:9] = ValuesToAddTrs[0].value[0:9] 		


		#clean self.ValuesToAddTrs
		ValuesToAddTrs = [ self.ValuesToAddTrs ]

		return self.ValueTrs.value	




	def processBuild( self , refs , value ):

		if( refs.get('Name' , None ) == None ):
			return ''
			
		Trs = trs( value )			
		buildCmds = Trs.toObjCmds( refs['Name'] , worldSpace = 1 )
		return buildCmds




		'''
		value = [0,0,0 , 0,1,0 , 0,0,1]    , mode = 'mirror'    -> 2 instance
		value = ['locA' , 'locB' , 'locC'] , mode = 'mirror'    -> 2 instance
		value = ['planeA']                 , mode = 'mirror'    -> 2 instance

		value = [10,0,0 , 0,0,0 , 1,1,1]        , mode = 'transform'   -> 2 instance
		value = [10,0,0 , 0,0,0 , 1,1,1 , 4]    , mode = 'transform'   -> 4 instance

		value = [10,0,0 , 0,0,0 , 7]    , mode = 'axe'              -> 7 instance
		value = [10,0,0 , 0,0,0 , 7 , 20]    , mode = 'axe'              -> 7 instance
		'''


	def utils_dataIsBuildable( self , index ):

		valueHistory       = self.data[index]['value']
		valueHistoryKeys   = [ value.keys()[0]        for value in valueHistory  if value.keys()[0] in self.argsValue ]
		valueHistoryValues = [ value[value.keys()[0]] for value in valueHistory  if value.keys()[0] in self.argsValue ]

		if( 0 < len(valueHistoryKeys) ) and ( valueHistoryKeys[-1] == 'replace' ):
			valueReplace = valueHistoryValues[-1]
			if( type(valueReplace) == types.InstanceType ):
				name        = self.ref( index = index , key = 'Name' , convertInstance = False )
				nameReplace = valueReplace.ref(         key = 'Name' , convertInstance = False )
				
				if not( nameReplace == None ) and not ( name == None ):

					parent = name.ref( key = 'parent' , updateData = 1 )
					if( type(nameReplace) == types.InstanceType ): nameReplace = nameReplace.value(updateData = 1)
									
					if( nameReplace == parent ):
						pos        = self.value(index , updateData = 1)
						posReplace = valueReplace.value(updateData = 1)
						if( pos == posReplace ):
							return False

		return True



	def processDuplicate( self , duplicateds , **args  ):
		
		value             = args.get( 'value'             , [0,0,0 , 0,1,0 , 0,0,1] )		
		mode              = args.get( 'mode'              , 'mirror'                )	
		pivot             = args.get( 'pivot'             , [0,0,0 , 0,0,0 , 1,1,1] )
		namePrefix        = args.get( 'namePrefix'        , ['r','l']               )		
		nameReplace       = args.get( 'nameReplace'       , ['','']                 )	
		nameIncr          = args.get( 'nameIncr'          , ''                      )
		nameAdd           = args.get( 'nameAdd'           , []                      )
		noneMirrorAxe     = args.get( 'noneMirrorAxe'     , 4                       )	

		#PROCESS VALUE
		duplicatedsProcessed = []
		for i in range( 0 , len(duplicateds) ):
			instanceTmp = duplicateds[i] 

			for j in range( 0 , len(self.data) ):
				key = self.data[j]["key"]

				if(   mode == 'mirror'    ) and ( i == 1 ): instanceTmp.add( key , mirror    = { 'value':value , 'noneMirrorAxe': noneMirrorAxe  } )
				elif( mode == 'transform' ) and ( 0 < i  ): instanceTmp.add( key , transform = { 'value':value , 'pivot'  :pivot   , 'dupliPosOrder':i           } )
		
			duplicatedsProcessed.append(instanceTmp) 		

		return duplicatedsProcessed

	def processCopy( self , newInstance ):

		for j in range( 0 , len(self.data) ):
			key          = self.data[j]["key"]
			newInstance.add( key , replace = eval('self.{}'.format(key) ) )

		return newInstance



	def processDataFlat( self , dataFlat ):

		#SORT IN BUILD ORDER
		names   = [ data.get('Name' ,'') for data in dataFlat ]

		fathers = []
		for name in names:
			if( '|' in name ): fathers.append( '|'.join( name.split('|')[0:-1] ) )
			else:              fathers.append('')

		rootIndexes = utilsPython.sortIndexChildrensByHierarchy( names , fathers )

		dataFlat   = [ dataFlat[i] for i in rootIndexes ]

		return dataFlat 



	'''


	# modes   = [ 'mirror' , 'tranform , 'axe' ]
	# nameIncrs = [ 'A' , '0' , 'B' , '1' ]
	def duplicate( self , value = [0,0,0 , 0,1,0 , 0,0,1] , mode = 'mirror' , pivot = [0,0,0 , 0,0,0 , 1,1,1] , namePrefix = ['r','l'] , nameReplace = ['',''] , nameIncr = '' , orientLockAxe = 0 , orientInverseAxes = 0  ):

		duplicateKey = str(value) + mode

		nbrInstance = 2
		if( 9 < len(value) ): 
			nbrInstance = value[9]


		duplicatedPoses = []
		for i in range( 0 , nbrInstance ):

			Pos = buildPosition()

			for j in range( 0 , len(self.data) ):
				key        = self.data[j]["key"]
				Name       = self.data[j]["Name"]
				PosCurrent = exec('self.{}'.format( key ) )
				#FILL POSITION DUPLICATE
				Pos.add( key , [ PosCurrent ] , Name = Name )		
				Pos.add( key , [[value , namePrefix , nameReplace , nameIncr , orientLockAxe , orientInverseAxes]] , operations = [mode] )

			duplicatedPoses.append(Pos)

		#dupli KEY
		self.keyToDuplicated[duplicateKey] = duplicatedPoses

		return duplicatedPoses

	'''