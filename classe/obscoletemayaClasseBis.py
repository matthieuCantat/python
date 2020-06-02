import maya.cmds as mc
import inspect
import types
from xml.dom.minidom import Document
from xml.dom.minidom import parse

from ..utils import utilsMaya
from ..utils import utilsPython


class mayaClasse():

	'''
		baseClasse of manipulation in maya

		FONCTION:
			createFromFile
			toFile
			createFromMayaObj
			toMayaObj
			printAttrs

		RULES:
			-all proc with maya cmds must be called mayaSomething
			-all proc without a reel use of self.attr define in init must be call utils

	'''
	
	def __init__(self , **args ):	
		#UTILS	
		self.utilsAxes                         = [ 'X' , 'Y' , 'Z' ]
		self.utilsTrsAttrs                     = [ 'translateX' , 'translateY' , 'translateZ' , 'rotateX' , 'rotateY' , 'rotateZ' , 'scaleX' , 'scaleY' , 'scaleZ' ]
		self.utilsDebug                        = 0
		self.utilsAttrPrefixToNotSave          = [ 'utils' , 'classe' ]
		self.utilsClasseInfoAttr               = 'classeInfoAttrs'	
		self.utilsClasseNames                  = []
		self.utilsClasseNameToFileName         = {}
		self.utilsClasseNameToExecutableImport = {}			
		self.utilsClasseNameToExecutableBuild  = {}
		self.refreshClassesInfo()		
		#CLASSE
		self.classeType = 'mayaClasse'
		#INSTANCE	
		self.value      = None	
		

	def createFromFile( self , file ):
		dictionary     = self.utils_xmlFileToDictionary( file )
		classeInstance = self.utils_dictToMayaClasse( dictionary )
		self.__class__ = classeInstance.__class__
		self.__dict__  = classeInstance.__dict__
		return classeInstance			

	def toFile( self , file ):
		dictionary = self.utils_mayaClasseToDict( self )						
		self.utils_dictionaryToXmlFile( file , dictionary )		
		return 1

	def createFromMayaObj( self , obj ):
		if not( '.' in obj ): obj += '.' + self.utilsClasseInfoAttr			
		dictionary     = self.utils_mayaObjInfoToDictionary( obj )
		classeInstance = self.utils_dictToMayaClasse( dictionary )	
		self.__class__ = classeInstance.__class__
		self.__dict__  = classeInstance.__dict__
		return classeInstance	

	def toMayaObj( self , obj ):
		if not( '.' in obj ): obj += '.' + self.utilsClasseInfoAttr							
		dictionary = self.utils_mayaClasseToDict( self )
		self.utils_dictionaryToMayaObjInfo( obj , dictionary )		
		return 1		

	def printAttrs( self , match = '' , instanceAttrsOnly = 0 ):
		attrNames = self.utils_getClasseAttributeNames( self )

		if( instanceAttrsOnly == 0 ):
			print('#________UTILS ATTRS')
			prefix = 'utils' 
			for attr in attrNames:
				if( len(prefix) <= len(attr) ) and ( attr[:len(prefix)] == prefix ) and ( match in attr ):
					exec( 'self.utilsPrint = self.{1}'.format( self , attr ) )
					print( '{}.{}'.format(self.classeType , attr) , self.utilsPrint )	
	
			print('#________CLASSE ATTRS')
			prefix = 'classe' 
			for attr in attrNames:
				if( len(prefix) <= len(attr) ) and ( attr[:len(prefix)] == prefix ) and ( match in attr ):
					exec( 'self.utilsTmpPrint = self.{1}'.format( self , attr ) )
					print( '{}.{}'.format(self.classeType , attr) , self.utilsTmpPrint )	
	
		print('#________INSTANCE ATTRS')
		prefix = 'instance' 				
		for attr in attrNames:
			if not( 'utils' in attr) and not( 'classe' in attr ) and ( match in attr ):
				exec( 'self.utilsTmpPrint = self.{1}'.format( self , attr ) )
				print( '{}.{}'.format(self.classeType , attr) , self.utilsTmpPrint )


	#____________________________________________________________________________UTILS	
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
	
				self.utilsClasseNames  .append(classeName)
				self.utilsClasseNameToFileName[classeName]        =  moduleName
				self.utilsClasseNameToExecutableImport[classeName] = 'import python.classe.{0}'.format(moduleName)			
				self.utilsClasseNameToExecutableBuild[classeName]  = 'python.classe.{0}.{1}()'.format(moduleName,classeName)
	
	def utils_xmlFileToDictionary( self , path ):
		#ADD XML AT THE END
		if not( path[-4:len(path)] == '.xml' ): path += '.xml'
		#INIT
		try:
			dom = parse(path)
		except:
			return {}
		dictValues = {}	
		#BROWSE THE FILE 
		for node in dom.getElementsByTagName('object'):
			varName = str( node.getAttribute("__name__") )
			valueStr = str( node.getAttribute("value") )
			exec( 'value = ' + valueStr )
			dictValues[varName] = value	

		return dictValues  

	def utils_dictionaryToXmlFile( self , path , dictionary ):
		#ADD XML AT THE END
		if not( path[-4:len(path)] == '.xml' ): path += '.xml'	
		#INIT
		doc = Document()		
		root_node = doc.createElement("scene")
		doc.appendChild(root_node)
		#FILL WITH DICO
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
		
		return 1
	
	def utils_mayaObjInfoToDictionary( self ,  obj ):
		#INIT		
		if not( mc.objExists(obj + '.' + self.utilsClasseInfoAttr) ):
			return {}
		#READ
		dictStr = mc.getAttr( obj + '.' + self.utilsClasseInfoAttr )
		return eval(dictStr)  

	def utils_dictionaryToMayaObjInfo( self ,  obj  , dictionary ):
		#INIT		
		dictValues = {}		
		if not( mc.objExists(obj) )and not( mc.nodeType(obj) == 'transform' ):
			return 0
		#DELETE
		objAttrs = mc.listAttr(obj)

		if( mc.objExists(obj+'.'+self.utilsClasseInfoAttr) ):
			mc.deleteAttr(obj+'.'+self.utilsClasseInfoAttr)			

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

		mc.addAttr( obj , longName=self.utilsClasseInfoAttr, dataType='string' )
		mc.setAttr( obj + '.' + self.utilsClasseInfoAttr , dictStr , type = 'string' )

		return 1  		


	@staticmethod	
	def utils_getClasseAttributeNames( classeInstance ):
		attributes = inspect.getmembers( classeInstance , lambda a:not( inspect.isroutine(a) ) )
		attributes = [a[0] for a in attributes if not(a[0].startswith('__') and a[0].endswith('__'))]
		return attributes			

	def utils_dictToMayaClasse( self , dict ):
		#INIT INSTANCE
		classeType = dict['classeType']
		exec( self.utilsClasseNameToExecutableImport[classeType] )
		exec( 'instance = {}'.format( self.utilsClasseNameToExecutableBuild[classeType] ) )	

		for key in dict.keys():
			value = dict[key]
			print( key , value , type(value))

			if( type(value) == types.InstanceType ):
				keyClasseType = key + '.classeType'
				classeType = dict[keyClasseType]
				print('======================================')
				print(self.utilsClasseNameToExecutableImport[classeType])
				exec( self.utilsClasseNameToExecutableImport[classeType])
				print(self.utilsClasseNameToExecutableBuild[classeType])
				exec( 'instance.{} = {}'.format( key, self.utilsClasseNameToExecutableBuild[classeType] ) )				

			elif( type(value) == types.StringType ) or ( type(value) == types.UnicodeType ):
				print('instance.{} = \'{}\''.format( key , value ))
				exec( 'instance.{} = \'{}\''.format( key , value ) )
			else:
				print('instance.{} = {}'.format( key , value ))
				exec( 'instance.{} = {}'.format( key , value ) )

		return instance

	def utils_mayaClasseToDict( self , classeInstance ):
		attributes = self.utils_getClasseAttributeNames(classeInstance)

		#FILTER ATTRS
		attributesFiltered = [ 'classeType' ]	
		for attr in attributes:
			exclude = 0
			for prefix in self.utilsAttrPrefixToNotSave:
				if ( len(prefix) <= len(attr) ) and ( attr[:len(prefix)] == prefix ):
					exclude = 1

			if( exclude == 0 ): 
				attributesFiltered.append( attr )

		attributes = attributesFiltered
		#FILTER ATTRS

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




	
	