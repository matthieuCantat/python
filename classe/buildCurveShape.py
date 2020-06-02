# NOTE:
'''
	FOR the CURVE SHAPE
	-have an easy way to get the form
	-posibility to put string as color 'red' 'blue' 'rambow'
	-axe must have a reel meaning in world space like for each individual form
	-possibility to scale with one value
	-easy way to store
	-wasy way to display
'''


'''

#******************************************************** BUILD EXEMPLE

# NAMES
import python
from python.classe.buildName import *
reload(python.classe.buildName)
reload(python.classe.trsBackUp)

import maya.cmds as mc
mc.file( f = True , new = True )

Names = buildName( )

Names.add( 'base'   , baseNameAppend = 'toto'     , type = 'grp' )		
Names.add( 'rigA'   , baseNameAppend = 'Arm'      , type = 'grp'   , ref = Names.base  )
Names.add( 'ctrlA'  , baseNameAppend = 'OffsetA'  , type = 'CTRL'  , ref = Names.rigA  )
Names.add( 'jointA'  , baseNameAppend = ''        , type = 'JNT'   , ref = Names.ctrlA )
Names.add( 'ctrlB'  , baseNameAppend = 'OffsetB'  , type = 'CTRL'  , ref = Names.rigA  )
Names.add( 'jointB'  , baseNameAppend = ''        , type = 'JNT'   , ref = Names.ctrlB )



# SHAPE
from python.classe.buildCurveShape import *
reload(python.classe.buildCurveShape)


cShapeMaster = buildCurveShape()
cShapeMaster.add(  'ctrl'  , value = { 'form' : 'cube' , 'colors' : [13] , 'axe' : 'x' , 'offset' : [0,0,0,0,0,0,1,1,1] }  )

cShape = buildCurveShape()
cShape.add(  'ctrlA' , Name = Names.jointA  , value = cShapeMaster.ctrl  )
cShape.add(  'ctrlB' , Name = Names.jointB  , value = cShapeMaster.ctrl  )

cShape.printInfo()


# DUPLI A
dupliValue = [0,0,0 , 0,1,0 , 0,0,1]
dupliMode  = 'mirror'

duplicatedNames   = Names.duplicate( dupliValue , dupliMode , [0,0,0 , 0,0,0 , 1,1,1] , namePrefix = ['r','l'] , nameReplace = ['toto','tata'] , nameIncr = '' , orientLockAxe = 0 , orientInverseAxes = 0  )
duplicatedcShape   = cShape.duplicate( dupliValue , dupliMode , [0,0,0 , 0,0,0 , 1,1,1] , namePrefix = ['r','l'] , nameReplace = ['toto','tata'] , nameIncr = '' , orientLockAxe = 0 , orientInverseAxes = 0  )
duplicateKey      = str(dupliValue) + dupliMode

duplicatedcShape[1].printInfo()

for i in range( 0 , len(duplicatedNames)):
    duplicatedcShape[i].swapRefsToDuplicate(  duplicateKey , dupliIndex = i )


# DUPLI B
dupliValue = [10,0,0 , 0,15,0 , 0,0,1 , 5]
dupliMode  = 'transform'

duplicatedNames   = Names.duplicate( dupliValue , dupliMode , [0,0,0 , 0,0,0 , 1,1,1] , namePrefix = ['',''] , nameReplace = ['',''] , nameIncr = 'A' , orientLockAxe = 0 , orientInverseAxes = 0  )
duplicatedcShape  = cShape.duplicate( dupliValue , dupliMode , [0,0,0 , 0,0,0 , 1,1,1] , namePrefix = ['',''] , nameReplace = ['',''] , nameIncr = 'A' , orientLockAxe = 0 , orientInverseAxes = 0  )
duplicateKey      = str(dupliValue) + dupliMode

duplicatedcShape[2].printInfo()

for i in range( 0 , len(duplicatedNames)):
    duplicatedcShape[i].swapRefsToDuplicate(  duplicateKey , dupliIndex = i )


#test dupli

curveM = buildCurveShape()
curveM.add(  'master'     , value = { 'form' : 'cube' , 'colors' : [13] , 'axe' : 'x' , 'offset' : [0,0,0,0,0,0,1,1,1] } )


Curve = buildCurveShape()
Curve.add(  'ctrlA'      , value = { 'form' : 'sphere' , 'colors' : [13] , 'axe' : 'x' , 'offset' : [0,0,0,0,0,0,1,1,1] } )
Curve.add(  'ctrlB'      , value = Curve.ctrlA )
Curve.add(  'ctrlC'      , value = curveM.master )
Curve.printInfo()

CurveCopy = Curve.copy()

CurveCopy.add(  'ctrlA'    , value = { 'form' : 'loc' , 'colors' : [17] , 'axe' : 'x' , 'offset' : [0,0,0,0,0,0,1,1,1] }  )
Curve.printInfo()
CurveCopy.printInfo()


Curve.add(  'ctrlA'    , value = { 'form' : 'loc' , 'colors' : [17] , 'axe' : 'x' , 'offset' : [0,0,0,0,0,0,1,1,1] }  )
CurveCopy.printInfo()

Curve.add(  'ctrlA'    , baseNameReplace = 'bruno'  )


CurveCopy = PosM.copy()
CurveCopy.add(  'master'  ,  baseNameAppend = 'toto' )

CurveCopy.printInfo()


'''


import maya.cmds as mc

from ..utils import utilsMaya
from ..utils import utilsPython
from ..utils import utilsMath
from ..utils import utilsMayaApi
from ..utils import utilsRigPuppet
from .build import *

from . import curveShape
from .coords import *
from .trsBackUp import *

import time
import copy

class buildCurveShape( build ):

	def __init__(self , **args):
		build.__init__(self , **args )
		#____________________________________________________________________RIG INFO

		#UTILS
		self.valueInit =  { 'form' : '' , 'colors' : [13] , 'axe' : 'x' , 'offset' : [0,0,0,0,0,0,1,1,1] , 'position' : None , 'coords' : [[]] , 'nbrPoints' : [0] , 'degrees' : [1] , 'scale' : 1 } 			
		self.CurveShapeTmp = curveShape.curveShape()	
		self.CurveShapeTmp.modify( **self.valueInit )															
		#CLASSE
		self.classeType   = 'buildCurveShape'	
		self.argsValue    = [ 'value' , 'operation' ]
		self.argsRef      = [ 'Name' ]


	def processValue( self , value , valueToAdd , operation , index = None , updateData = False ):
		
		#INIT VALUE--------------------------------------------------------
		inValue = copy.deepcopy(self.CurveShapeTmp)
		#EXTRACT ARGS
		if not( value == None ):
			args = {}					
			for key in self.valueInit.keys():
				exec('args["{0}"] = copy.copy(value.{0})'.format(key) )
			#ADD TO VALUE
			inValue.modify( **args )

		value = inValue

		#INIT VALUE TO ADD------------------------------------------------------
		if( type(valueToAdd) == types.InstanceType ):
			#INIT VALUE TO ADD
			if(   valueToAdd.classeType == 'buildCurveShape' ): CurveToAdd = valueToAdd.value()
			elif( valueToAdd.classeType == 'curveShape'      ): CurveToAdd = valueToAdd
			#EXTRACT ARGS
			args = {}					
			for key in self.valueInit.keys():
				if not( key == 'position' ):
					exec('args["{0}"] = copy.copy(CurveToAdd.{0})'.format(key) )
			#ADD TO VALUE
			value.modify( **args )

		elif( type(valueToAdd) == types.DictType ):

			if( valueToAdd.keys()[0] == 'mirror' ): 
				#CONVERT PLAN COORDS
				planSymCoords = utilsRigPuppet.convertMirrorInfoToCoords(valueToAdd['mirror'])
				value.mirror( planSymCoords )
	
			elif( valueToAdd.keys()[0] == 'transform' ): 

				pivot         = valueToAdd['transform']['pivot']
				valueTrs      = valueToAdd['transform']['value']
				dupliPosOrder = valueToAdd['transform']['dupliPosOrder']
	
				value.transform( valueTrs , pivot , dupliPosOrder )


			else:
				args = {}
				for key in valueToAdd.keys():
					args[key] = valueToAdd[key]

				#POSITION
				if( 'position' in args.keys() ) and ( type(args['position']) == types.InstanceType ):
					args['position'] = args['position'].value()
				#MODIFY CURVE SHAPE						
				value.modify( **args )
				


		return value

	def utils_dataIsBuildable(self , index ):

		for value in self.data[index]['value']:
			if( 'Name' in value.keys() ) and not( value['Name'] in [None,'None']  ):
				return True

		return False



	def valuePrint( self , index = None ):
		curveShape = self.value(index)
		stringToPrint = 'names: {} , form: {} , colors: {} , degrees: {} , nbrPoints: {} , axeOrient: {} , trsOffset: {} , scale: {} , coords: {} '.format(curveShape.names , curveShape.form , curveShape.colors , curveShape.degrees , curveShape.nbrPoints , curveShape.axe , curveShape.offset , curveShape.scale , curveShape.coords )
		return stringToPrint


	def processBuild( self , refs , value ):
		Name = refs.get( 'Name' , None )

		if( Name == None ):
			return ''

		buildCmds = value.toObjCmds( Name , worldSpace = True )
		return buildCmds

					
	def processDuplicate( self , duplicateds , **args  ):

		value             = args.get( 'value'             , [0,0,0 , 0,1,0 , 0,0,1] )		
		mode              = args.get( 'mode'              , 'mirror'                )	
		pivot             = args.get( 'pivot'             , [0,0,0 , 0,0,0 , 1,1,1] )
		namePrefix        = args.get( 'namePrefix'        , ['r','l']               )		
		nameReplace       = args.get( 'nameReplace'       , ['','']                 )	
		nameIncr          = args.get( 'nameIncr'          , ''                      )
		nameAdd           = args.get( 'nameAdd'           , []                      )
		noneMirrorAxe     = args.get( 'noneMirrorAxe'     , 2                       )
		
		#PROCESS VALUE
		duplicatedsProcessed = []
		for i in range( 0 , len(duplicateds) ):
			instanceTmp = duplicateds[i] 

			for j in range( 0 , len(self.data) ):
				key = self.data[j]["key"]

				if(   mode == 'mirror'    ) and ( i == 1 ): instanceTmp.add( key , value = { 'mirror':value } )
				elif( mode == 'transform' ) and ( 0 < i  ): instanceTmp.add( key , value = { 'transform': { 'value':value , 'pivot':pivot , 'dupliPosOrder':i } } )
		
			duplicatedsProcessed.append(instanceTmp) 		

		return duplicatedsProcessed



	def processCopy( self , newInstance ):

		for j in range( 0 , len(self.data) ):
			key          = self.data[j]["key"]
			newInstance.add( key , value = eval('self.{}'.format(key) ) )

		return newInstance		