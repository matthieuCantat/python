

'''

import python
from python.classe.readWriteInfo import *
reload(python.classe.readWriteInfo)

rwi = readWriteInfo()
rwi.mayaScene_load( 'D:/mcantat_BDD/projects/cute/carrierShipD/maya/scenes/carrierShipD_rigSkeleton.ma' )
rwi.mayaScene_save( 'D:/mcantat_BDD/projects/cute/carrierShipD/maya/scenes/carrierShipD_rigSkeleton_v1.ma' )

'''





from xml.dom.minidom import Document
from xml.dom.minidom import parse
import types
import inspect
import string
import os
import time
import subprocess

import maya.cmds as mc
import maya.OpenMaya as om
import maya.api.OpenMaya as ompy

from ..utils import utilsMaya
from ..utils import utilsPython
from ..utils import utilsMath
from ..utils import utilsMayaApi
from .mayaClasse import *
from . import trs


class readWriteInfo(mayaClasse):
	
	'''
	#_________________________________________________________________CREATE
	createFromFile
	createFromFiles
	createFromMayaObj
	createFromMayaObjs
	updateClasseAttrWithDictionary
	#_________________________________________________________________OUT
	update
	toFile
	toFiles
	toObj
	toObjs
	toValueDefaut
	#_________________________________________________________________UTILS
	utils_xmlFileToDictionary
	utils_dictionaryToXmlFile
	utils_mayaObjInfoToDictionary
	utils_dictionaryToMayaObjInfo

	'''

	def __init__(self):
		self.type      = 'readWriteInfo'
		self.objs      = None
		self.varNames  = []
		self.dict      = {}
		self.values    = []
		self.suffixIncr = '_v'

		self.classeNames                  = []
		self.classeNameToFileName         = {}
		self.classeNameToExecutableImport = {}			
		self.classeNameToExecutableBuild  = {}
		self.refreshClassesInfo()		

	#_________________________________________________________________CREATE
	def createFromFile( self , file , latest = 1 ):
		print('readWriteInfo createFromFile')
		self.dict = self.utils_xmlFileToDictionary( file , latest , self.suffixIncr )
		self.objs = [file]		
		self.updateClasseAttrWithDictionary()
		return self.dict	

	def createFromFiles( self , files , latest = 0 ):
		dictOutObjs = {}
		for file in files:
			dictOutObj  = self.createFromFile( file , latest )
			dictOutObjs = utilsPython.dictionnaryMerge( dictOutObjs , dictOutObj )
		self.objs = files			
		self.dict = dictOutObjs
		self.updateClasseAttrWithDictionary()		

	def createFromMayaObj( self , obj ):
		self.dict = self.utils_mayaObjInfoToDictionary( obj )
		self.objs = [obj]		
		self.updateClasseAttrWithDictionary()	
		return self.dict	

	def createFromMayaObjs( self , objs ):
		dictOutObjs = {}
		for obj in objs:
			dictOutObj  = self.createFromMayaObj( obj )
			dictOutObjs = utilsPython.dictionnaryMerge( dictOutObjs , dictOutObj  )
		self.objs = objs			
		self.dict = dictOutObjs
		self.updateClasseAttrWithDictionary()	

	def createFromClasse( self , instance ):
		self.dict = self.utils_classeToDictAttrValue( instance )
		self.objs = [instance]		
		self.updateClasseAttrWithDictionary()	
		return self.dict	

	def updateClasseAttrWithDictionary( self , inValue = None ):
		if not( inValue == None ):
			self.dict = inValue
		if not( self.dict == {} ):
			self.values = [ self.dict[key] for key in self.dict.keys() ]



	def mayaScene_load( self , path , historyFolder = None , incr = True , clean = False , nameSpace = None , ref = None , open = None ):

		if( incr ):
			fileIndex = self.utils_findLatestPathIndex( path      , suffix = "_v" )
			path = self.utils_insertIndexToPath( path , fileIndex , suffix = "_v" )	


		if( clean ):mc.file( new = True , f = True )

		if(            open == True ):mc.file( path , o = True , f = True  )
		elif not( nameSpace == None ):mc.file( path , i         = True , ns = self.utils_incrNameSpace(nameSpace) , f = True  ) 
		elif not( ref       == None ):mc.file( path , reference = True , ns = self.utils_incrNameSpace(ref)       , f = True  ) 	
		else:                         mc.file( path , i         = True , f = True )


	def mayaScene_save( self , path , historyFolder = None , incr = True ):

		latestPath = self.utils_findLatestPath( path          , suffix = "_v" )
		if( incr ):
			fileIndex = self.utils_findLatestPathIndex( path          , suffix = "_v" )
			path = self.utils_insertIndexToPath( path , fileIndex + 1 , suffix = "_v" )

		mc.file( rename = path)
		mc.file( save=True, type='mayaAscii' )

		fileName = latestPath.split('/')[-1]
		if( historyFolder ):
			os.rename(latestPath, historyFolder + '/' + fileName)		
		else:			
			latestPathSplit =  latestPath.split('/')[0:len(latestPath)-2]
			parentFolder = '/'.join( latestPathSplit[0:len(latestPathSplit)-1] )
			historyFolder = parentFolder + '/history'
			if not( os.path.exists(historyFolder) ):
				os.mkdir(historyFolder)
			os.rename(latestPath, historyFolder + '/' + fileName)



	#_________________________________________________________________OUT

	def update( self ):
		if( self.objs == [] ):
			return 0
		for obj in self.objs:
			if( utilsPython.isPath(obj) ):
				self.utils_xmlFileWriteDictionary( obj , self.dict )
			elif( mc.objExists(obj) ):
				self.utils_writeInfoFromMayaObj( obj , self.dict )	
		return 1

	def toFile( self , file , clearOldVar = 1 , incr = 0 ):
		print('readWriteInfo toFile')

		#UPDATE WITH DICT
		self.updateClasseAttrWithDictionary()

		#READ INFO
		dictClass = self.dict
		dictOutObj = self.utils_xmlFileToDictionary( file , latest = incr )

		if( clearOldVar ): dictInObj = dictClass
		else:              dictInObj = utilsPython.dictionnaryMerge( dictOutObj , dictClass )

		#WRITE INFO		
		self.utils_dictionaryToXmlFile( file , dictInObj , incr , self.suffixIncr )		

		return 1
	

	def toFiles( self , files , clearOldVar = 0 , incr = 0 ):
		for file in files:
			self.toFile( files , clearOldVar , incr )
		return 1

	def toObj( self , obj , clearOldVar = 0 ):
		#UPDATE WITH DICO
		self.updateClasseAttrWithDictionary()					
		#READ INFO
		dictClass = self.dict
		dictOutObj = self.utils_mayaObjInfoToDictionary( obj )
		if( clearOldVar ): 
			dictOutObj = []
		#MERGE INFO		
		dictInObj  = utilsPython.dictionnaryMerge( dictOutObj , dictClass  )
		#WRITE INFO		
		self.utils_dictionaryToMayaObjInfo( obj , dictInObj )		
		return 1		

	def toClasse( self , classeInstance , clearOldVar = 0 ):
		#UPDATE WITH DICO
		self.updateClasseAttrWithDictionary()					
		#WRITE INFO		
		self.utils_dictToClasseAttr( classeInstance , self.dict )		
		return 1		



	def toObjs( self , objs = None , clearOldVar = 0 ):
		for obj in objs:
			self.toObj( obj , clearOldVar )
		return 1

	def toValueDefaut( self , varName , defautValue = None ):
		if not( varName in self.dict.keys() ):
			return defautValue 
		return self.dict[varName]

	#_________________________________________________________________UTILS

	def utils_xmlFileToDictionary( self , path , latest = 0 , suffix = ''):
		path = self.utilsPath_toPythonSyntax(path)
		#ADD XML AT THE END
		if not( path[-4:len(path)] == '.xml' ): path += '.xml'

		#FIND LATEST FILE
		if( latest ):
			fileIndex = self.utils_findLatestPathIndex( path , suffix )
			incrPath = self.utils_insertIndexToPath( path , fileIndex , suffix )
			if( self.utilsPath_exists(incrPath) ): path = incrPath 		

		#INIT
		dictValues = {}	
		if( os.path.exists(path) ):
			dom = parse(path)
			for node in dom.getElementsByTagName('object'):
				varName  = str( node.getAttribute("__name__") )
				valueStr = str( node.getAttribute("value") )
				exec( 'value = ' + valueStr )
				dictValues[varName] = value	
	
		return dictValues  


	def utils_dictionaryToXmlFile( self , path , dictionary , incr = 0 , suffix = '' , historyFolder = None ):
		
		if( incr ):
			latestPath = self.utils_findLatestPath( path  , suffix = suffix )
			fileIndex = self.utils_findLatestPathIndex( path , suffix )
			path = self.utils_insertIndexToPath( path , fileIndex + 1 , suffix )

		#INIT
		doc = Document()		
		root_node = doc.createElement("scene")
		doc.appendChild(root_node)
		#FILL WITH DICT
		for key in dictionary.keys():		    
			#CREATE ATTR
			object_node = doc.createElement("object")
			root_node.appendChild(object_node)	
			object_node.setAttribute("__name__", key )
			#FILL ATTR	    
			value = dictionary[key]
			if( utilsPython.isString(value) ): value = ( '\'' + value + '\'' )  
			valueStr = str(value)
			object_node.setAttribute( "value" , valueStr )		
		#WRITE
		xml_file = open( path , "w")
		xml_file.write(doc.toprettyxml())
		xml_file.close()


		
		#CREATE HISTORY FOLDER AND FILL IT
		if( incr ):
			if not(latestPath == '' ):

				fileName = latestPath.split('/')[-1]
				if( historyFolder ):
					os.rename(latestPath, historyFolder + '/' + fileName)		
				else:			
					latestPathSplit =  latestPath.split('/')[0:len(latestPath)-2]
					parentFolder = '/'.join( latestPathSplit[0:len(latestPathSplit)-1] )
					historyFolder = parentFolder + '/history'
	
					if not( os.path.exists(historyFolder) ):
						os.mkdir(historyFolder)
					os.rename(latestPath, historyFolder + '/' + fileName)


		return 1



	def utils_pathIncrAndArchiveOld( self , path , incr = 1 , suffix = '' , historyFolder = None ):
		
		if( incr ):
			latestPath = self.utils_findLatestPath( path  , suffix = suffix )
			fileIndex = self.utils_findLatestPathIndex( path , suffix )
			path = self.utils_insertIndexToPath( path , fileIndex + 1 , suffix )


		#CREATE HISTORY FOLDER AND FILL IT
		if( incr ):
			if not(latestPath == '' ):

				fileName = latestPath.split('/')[-1]
				if( historyFolder ):
					os.rename(latestPath, historyFolder + '/' + fileName)		
				else:			
					latestPathSplit =  latestPath.split('/')[0:len(latestPath)-2]
					parentFolder = '/'.join( latestPathSplit[0:len(latestPathSplit)-1] )
					historyFolder = parentFolder + '/history'
	
					if not( os.path.exists(historyFolder) ):
						os.mkdir(historyFolder)
					os.rename(latestPath, historyFolder + '/' + fileName)


		return path



	def utils_getPathToIncr( self, path , suffix = ''):
		pathBody   =        path.split('.')[0]

		pathBodyNbr = ''
		for i in range( len(pathBody)-1 , 0 , -1 ):
			if( pathBody[i] in string.digits ): pathBodyNbr += pathBody[i]
			else: break

		pathBodyStr = pathBody[0:len(pathBody)-len(pathBodyNbr)]

		pathToIncr = ''
		if( pathBodyStr[-len(pathBodyStr):-1] == suffix ):pathToIncr = pathBodyStr
		else:                                             pathToIncr = pathBody + suffix

		return pathToIncr


	def utils_findLatestPath( self , path , suffix = ''):
		incrMax    = 999
		extention  =  '.' + path.split('.')[1]
		pathToIncr = self.utils_getPathToIncr(path,suffix)

		latestPath = ''
		for i in range( incrMax , -1 , -1 ):
			pathTmp = pathToIncr + str(i) + extention
			if( os.path.exists(pathTmp) ):
				latestPath = pathTmp
				break

		return latestPath


	def utils_findLatestPathIndex( self , path , suffix = ''):
		incrMax    = 999
		extention  =  '.' + path.split('.')[1]
		pathToIncr = self.utils_getPathToIncr(path,suffix)

		index = 0
		for i in range( incrMax , -1 , -1 ):
			if( os.path.exists(pathToIncr + str(i) + extention) ):
				index = i
				break

		return index

	def utils_insertIndexToPath( self , path , index , suffix = ''):
		extention  =  '.' + path.split('.')[1]
		pathToIncr = self.utils_getPathToIncr(path,suffix)

		if( index == -1 ): path = '{}{}{}'.format( pathToIncr , extention)
		else:              path = '{}{}{}'.format( pathToIncr , index , extention)
		return path


	def utils_mayaObjInfoToDictionary( self ,  obj ):
		#INIT		
		attributInfo = 'rwi_store'
		if not( mc.objExists(obj + '.' + attributInfo) ):
			return {}
		#READ
		dictStr = mc.setAttr( obj + '.' + attributInfo , type = 'string' )
		return eval(dictStr)  

	def utils_dictionaryToMayaObjInfo( self ,  obj  , dictionary ):
		#INIT		
		attributInfo = 'rwi_store'
		dictValues = {}		
		if not( mc.objExists(obj) )and not( mc.nodeType(obj) == 'transform' ):
			return 0
		#DELETE
		objAttrs = mc.listAttr(obj)

		if( mc.objExists(obj+'.'+attributInfo) ):
			mc.deleteAttr(obj+'.'+attributInfo)			

		#WRITE
		dictKeys = dictionary.keys()
		dictStr  = '{'
		for i in range( 0 , len(dictKeys) ):

			value = dictionary[dictKeys[i]]

			if( type(value) == types.InstanceType):
				value = str(value)
			if( type(value) == types.StringType ) or ( type(value) == types.UnicodeType):
				value = ( '\'' + value + '\'' ) 

			dictStr += '\'' +dictKeys[i] + '\':' + str(value)
			if not( len(dictKeys) - 1 <= i ):
				dictStr += ','

		dictStr += '}'

		mc.addAttr( obj , longName=attributInfo, dataType='string' )
		mc.setAttr( obj + '.' + attributInfo , dictStr , type = 'string' )

		return 1  		



	@staticmethod	
	def utils_getClasseAttributeNames( classeInstance ):
		attributes = inspect.getmembers( classeInstance , lambda a:not( inspect.isroutine(a) ) )
		attributes = [a[0] for a in attributes if not(a[0].startswith('__') and a[0].endswith('__'))]
		return attributes			
	
		
	def utils_classeToDictAttrValue( self , classeInstance ):
		attributes = self.utils_getClasseAttributeNames(classeInstance)
	
		dictAttrToValue = {}
		lap = 0
	
		while not( len(attributes) == 0 ):
			lap += 1
			if( 500 < lap ):
				mc.error()
			
			attributesToRemove = []    
			for i in range( 0 , len(attributes) ):
				attrValue = eval( '{}.{}'.format( 'classeInstance' , attributes[i] ) )
				attrType = type( attrValue )
				
				if( attrType == types.InstanceType ):	
								    
					subAttributes = self.utils_getClasseAttributeNames( attrValue )
	
					subAttributes = [ '{}.{}'.format( attributes[i] , sub ) for sub in subAttributes ]
					attributes += subAttributes
					
					dictAttrToValue[ attributes[i] ] = attrValue				
					attributesToRemove.append(attributes[i])					
							
				else:
					dictAttrToValue[ attributes[i] ] = attrValue
					attributesToRemove.append(attributes[i])
	
			for a in attributesToRemove:
			    attributes.remove(a)

		return dictAttrToValue
	



	def utils_dictToClasseAttr( self , instance , dict ):
		for key in dict.keys():
			value = dict[key]

			if( type(value) == types.InstanceType ):
				keyClasseType = key + '.type'
				classeType = dict[keyClasseType]
				exec( self.classeNameToExecutableImport[classeType])
				exec( 'instance.{} = {}'.format( key, self.classeNameToExecutableBuild[classeType] ) )				

			elif( type(value) == types.StringType ) or ( type(value) == types.UnicodeType ):
				exec( 'instance.{} = \'{}\''.format( key , value ) )
			else:
				exec( 'instance.{} = {}'.format( key , value ) )


	
	@staticmethod
	def utils_getSelfPath():
		arrayPath  = __file__.split('\\')
		selfPath   = '/'.join(arrayPath[0:-1]) + '/'
		return selfPath 
			
	
	def refreshClassesInfo(self):
		allFiles = utilsPython.getFilesInPath( self.utils_getSelfPath() , extention = '.py' ) 
		func = lambda s: s[:1].lower() + s[1:] if s else ''
	
		for elem in allFiles:
			if not( '_' in elem ):
	
				moduleName   = elem.split('.py')[0]
				classeName = moduleName
				if( 'rig' in  moduleName ):
					classeName = func( moduleName[3:] )
	
				self.classeNames.append(classeName)
				self.classeNameToFileName[classeName]        =  moduleName
				self.classeNameToExecutableImport[classeName] = 'import python.classe.{0}'.format(moduleName)			
				self.classeNameToExecutableBuild[classeName]  = 'python.classe.{0}.{1}()'.format(moduleName,classeName)
	


	def utils_incrNameSpace( self , ref ):
		refNameSpace = ref
		if('?' in ref ):
			nbrIncr = 0
			for i in range( len(ref)-1, 0 , -1 ):
				if( '?' == ref[i] ):nbrIncr += 1
			
			refNameSpaceBody = ref[0:nbrIncr * -1]

			for i in range(1,999):
				nbrPrefix = '{}'.format(i)
				nbrO = nbrIncr - len(nbrPrefix)
				nbrPrefix = '{}{}'.format('0'*nbrO , nbrPrefix )

				refNameSpace = refNameSpaceBody + nbrPrefix

				if not( mc.namespace( exists=refNameSpace ) ):
					break

		return refNameSpace

	def utilsPath_exists( self , path ):
		return os.path.exists(path)

	def utilsPath_toWindowsSyntax( self , path ):
		newPath = path

		if( '/' in path ):
			newPath = '\\'.join( path.split('/') )
			if( '/' == path[-1] ):
				newPath += '\\'

		return newPath
	
	def utilsPath_toPythonSyntax( self , path ):
		newPath = path

		if( '\\' in path ):
			newPath = '/'.join( path.split('\\') )
			if( '\\' == path[-1] ):
				newPath += '/'

		return path

	def utilsPath_RemoveFile( self , path ):

		if(  '\\' == path[-1] ) or ( '/' == path[-1] ): path = path[0:-1]


		lastElem = None
		if(  '\\' in path ): lastElem = path.split('\\')[-1]
		elif( '/' in path ): lastElem = path.split('/')[-1]

		newPath = path
		if not( lastElem == None ):
			if( '.' in lastElem ):
				if(  '\\' in path ): newPath = '\\'.join( path.split('\\')[0:-1] )
				elif( '/' in path ): newPath = '/'.join( path.split('/')[0:-1] )
		
		return newPath

	def utilsPath_extractFile( self , path ):

		lastElem = ''
		if(  '\\' in path ): lastElem = path.split('\\')[-1]
		elif( '/' in path ): lastElem = path.split('/')[-1]

		if not( '.' in lastElem ):
			lastElem = ''
		return lastElem

	def utilsPath_openInExplorer( self , path):
		if( self.utilsPath_exists(path) ):
			path = self.utilsPath_toWindowsSyntax( path )
			path = self.utilsPath_RemoveFile( path )
			subprocess.Popen(r'explorer /select,"{}"'.format(path) ) 
			return 1
		else:
			print( 'utilsPath_openInExplorer - path doesnt exists')
			return 0

	def utilsPath_getCurrentScenePath(self):

		pathFile = mc.file( q = True , loc = True )
		if( ( pathFile == 'unknown' ) or (pathFile == None) ):
			print("rigPuppet_reloadRigSelected: CURRENT FILE PATH UNKNOWN --> YOU MUST BE IN A SCENE")
			return ''
		else:
			return pathFile

	def utilsPath_getCurrentSceneFolderPath(self):
		pathFile = self.utilsPath_getCurrentScenePath()
		pathFileSplit = pathFile.split('/')
		pathScene     = '/'.join( pathFileSplit[0:len(pathFileSplit)-1] ) + '/'
		return pathScene
	
	def utilsPath_getFiles(self , path , extention = None , latest = False , incrSuffix = "_v"):
		path = self.utilsPath_RemoveFile(path)
		files  = []
		for child in os.listdir( path ):
			if not( '.' in child         ): pass
			elif( extention == child[-len(extention):]    ): files.append( child)

		if( latest ):
			latestFiles = []

			for f in files:
				filePath       = '{}/{}'.format( path , f )
				fileIndex      = self.utils_findLatestPathIndex( filePath  , suffix = incrSuffix )
				latestFilePath = self.utils_insertIndexToPath( filePath , fileIndex , suffix = incrSuffix )	
				latestFile     = self.utilsPath_extractFile(latestFilePath)

				if( self.utilsPath_exists(latestFile) ): latestFiles.append( latestFile )
				else:                               latestFiles.append( f )

			files = latestFiles


		return files
