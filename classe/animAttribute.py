'''
#******************************************************** BUILD EXEMPLE 
import maya.cmds as mc
import python
from python.classe.animCurve import *
reload( python.classe.animCurve)


reload( python.classe.readWriteInfo)

#CREATE
anim = animCurve()	
anim.createFromSelection()
anim.delete()
anim.toObjs() 

anim.toObjs( inverse = True , startFrame = 1080 ) 

anim.getInfo() 
anim.getObjs() 
anim.getMatchObjs('l_reactorArmPropulsorHandle_CTRL') 

anim.toMatchSelection( mirror = 'X' , replace = True )

mc.select(anim.goMatchObjs('l_reactorArmPropulsorHandle_CTRL'))



#CREATE FROM FILE
anim.delete()
path = 'D:/mcantat_BDD/projects/cute/carrierShipD/maya/scenes/animCurves/test.xml'
anim.toFile( path , info = 'test test test 123 ultime' )

newAnim = animCurve()	
newAnim.createFromFile(path)
newAnim.toObjs()
newAnim.getInfo() 
newAnim.getObjs() 
newAnim.objsAttrs




'''


import maya.cmds as mc
import math


from . import coords as coordsClasse
from . import readWriteInfo
from ..utils import utilsMaya
from ..utils import utilsPython
from ..utils import utilsMath
from ..utils import utilsMayaApi
from .mayaClasse import *
from .trsBackUp import *
from .buildName import *
import time


class animAttribute(mayaClasse):
	
	'''
	#________________________________________________________________CREATE
	createFromCurve
	createFromCurves
	createFromSelection
	createFromFile
	#________________________________________________________________MODIF
	modify
	copy
	mirror
	delete
	#________________________________________________________________OUT
	toCurve
	toSelectedCurve	
	toSaveFile
	selectionToFile
	printAttrs
	#________________________________________________________________UTILS	
	'''
	
	def __init__(self):

		self.type      = 'animCurve'
		self.debug     = 0		
		#CURVE INFO	
		self.filePath  = ''	
		self.info      = ''
		self.nodes       = []
		self.objsAttrs   = []
		self.times       = []
		self.values      = []
		self.tLock       = []
		self.tWeightLock = []
		self.tInType     = []
		self.tInX        = []
		self.tInY        = []
		self.tOutType    = []
		self.tOutX       = []
		self.tOutY       = []
		self.breakdown   = []
		self.others      = []


	def printAttrs( self , title = '' , printInfo = 1 ):
		if( printInfo == 1 ):
			print('START_____________________________ ' + title)
			print('**********ATTRS***********')
			for i in range(0,len(self.objsAttrs )):
				print( '{} {}'.format( self.objsAttrs[i] , self.values[i] ) )
			print('END________________________________ ' + title)

	#________________________________________________________________CREATE

	def createFromObjs( self , objs , worldSpace = False ):
		print('animAttribute createFromObjs')
		self.objsAttrs   = []
		self.values      = []

		for obj in objs:

			attrs = utilsMaya.getManipulableAttr( obj )
			
			for attr in attrs:
				objAttr = obj + '.' + attr
				value   = mc.getAttr(objAttr)
				self.objsAttrs.append( objAttr ) 
				self.values.append(    value   ) 

		return 1
		
	def createFromSelection( self ):
		selection = mc.ls(sl=True)
		self.createFromObjs( selection )
		return 1

	def createFromFile( self , filePath , latest = 1 ):
		print('animAttribute createFromFile')
		self.filePath = filePath
		#GET INFO FROM FILE				
		ReadWriteInfo = readWriteInfo.readWriteInfo()
		ReadWriteInfo.createFromFile( self.filePath , latest = latest )				
		dictAnim = ReadWriteInfo.dict	
		#FILL CLASS ATTR
		self.objsAttrs   = [ key for key in dictAnim.keys() if not( key == 'info' ) ]
		self.values      = [ dictAnim[objAttr] for objAttr in self.objsAttrs ]

		self.printAttrs( 'createFromFile' , self.debug )				
		return 1		


	#________________________________________________________________OUT
	def toFile( self , filePath , clearOldVar = 1 , incr = 1 ):
		print('animAttribute toFile')
		self.filePath = filePath
		#GET INFO FROM FILE	
		ReadWriteInfo = readWriteInfo.readWriteInfo()
		'''
		ReadWriteInfo.createFromFile( self.filePath , latest = incr )			
		dictAnim = ReadWriteInfo.dict	
		'''
		dictAnim = {}
		for i in range(0,len(self.objsAttrs)):
			dictAnim[self.objsAttrs[i]] = self.values[i]

		#SAVE DICO IN FILE
		ReadWriteInfo.dict = dictAnim			
		ReadWriteInfo.toFile( self.filePath , incr = incr , clearOldVar = clearOldVar )

		self.printAttrs( 'toFile' , self.debug )
		return 1

	def getObjs( self ):
		objs = []
		for i in range(0,len(self.objsAttrs)):
			objs.append( self.objsAttrs[i].split('.')[0] )

		objs = list(set(objs))
		return objs

	def selectObjs( self ):
		mc.select(self.getObjs())

	def getMatchObjs( self , objToMatch ):
		objs = self.getObjs()

		Names = buildName()
		convertedObjs = Names.convertNamesToMatchExemple( objs , objToMatch )

		return convertedObjs


	def toObjs( self , **args ):
		print('animAttribute toObjs')
		objsToFilter  = args.get( 'objsToFilter' , None )
		matchObjName  = args.get( 'matchObjName' , None ) 
		mirror        = args.get( 'mirror' , None ) 

		#MATCH OBJ
		objs = self.getObjs()
		matchObjs = objs
		if not( matchObjName == None):
			matchObjs = self.getMatchObjs( matchObjName )


		for i in range(len(self.objsAttrs)):

			outObj , outAttr = self.objsAttrs[i].split('.')

			objsAttr = outObj +'.'+ outAttr

			if( matchObjName ):
				iTmp = objs.index(outObj)
				outObj = matchObjs[iTmp]
				objsAttr = outObj +'.'+ outAttr

			if( objsToFilter ) and not( outObj in objsToFilter ): continue

			mc.setAttr( objsAttr , self.values[i] )


	def toMatchObjs( self , objToMatch , **args ):
		args['matchObjName'] = objToMatch	
		self.toObjs( **args )
		return 1    

	def toMatchSelection( self , **args ):
		args['matchObjName'] = mc.ls(sl=True)[0]	
		self.toObjs( **args )
		return 1    

	def toSelection( self  , **args ):	
		args['objsToFilter'] = mc.ls( sl = True )	
		self.toObjs( **args )	
		return 1




	#________________________________________________________________UTILS



#test for git



