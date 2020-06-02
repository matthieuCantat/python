import maya.cmds as mc
import copy
import inspect
import types
from xml.dom.minidom import Document
from xml.dom.minidom import parse

from ..utils import utilsMaya
from ..utils import utilsPython
from ..utils import utilsMath
from ..utils import utilsMayaApi


class mayaClasse():

	'''
		baseClasse of manipulation in maya

		CANVAS:
		init( value )
		createFrom( elem , updateValue = 1  , **args )
			createFromMayaSelection
			createFromMayaObjs
			createFromValues
			createFromMayaObjAttr
			createFromMayaObj
			createFromFile
			createFromValue		
		to( elem , overrideValue = None  , **args )
			toMayaSelection
			buildMayaObjs
			toMayaObjs
			toValues
			toValue
			toMayaObjAttr
			toMayaObj
			toFile
			toInstance

		FONCTION:
		saveInFile
		saveInMayaAttr

		createFromFile
		createFromMayaAttr


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
		self.utilsClasseInfoAttr               = 'mayaClasseInfoAttrs'	
		self.utilsClasseNames                  = []
		self.utilsClasseNameToFileName         = {}
		self.utilsClasseNameToExecutableImport = {}			
		self.utilsClasseNameToExecutableBuild  = {}
		self.refreshClassesInfo()		
		#CLASSE
		self.classeType = 'mayaClasse'
		#INSTANCE	
		self.value      = None	
		

	#USER FRIENDLY ( simplify )
	def createFrom( self , value = None , updateValue = 1 , **args ):
		print('mayaClasse.createFrom')
		if( value == None ): 
			return self.createFromMayaSelection( updateValue , **args )
		elif( type(value) == types.ListType ):
			if( mc.objExists(value[0]) ): 
				return self.createFromMayaObjs( value , updateValue , **args )
			else:                         
				return self.createFromValues(   value , updateValue , **args )
		else:
			if( mc.objExists(value) ): 
				if(mc.objExists(value + '.' + self.utilsClasseInfoAttr ) ):
					return self.createFromMayaObjAttr( value , updateValue )
				else:
					return self.createFromMayaObj( value , updateValue , **args ) 
			else:                      
				if( '/' in value ): 
					return self.createFromFile( value , updateValue )
				else:
					return self.createFromValue(   value , updateValue , **args )
		
	def copy( self , inValue = None , updateValue = 1 , **args):
		return self.copyInstance( inValue , updateValue , **args )

	def to( self , obj = None , inValue = None , **args):
		if( obj == None ):
			selection = mc.ls(sl=True) 
			if( 0 < len(selection) ):
				return self.toMayaSelection( inValue , **args )
			else:
				return self.buildMayaObjs( inValue , **args )
		elif( type(obj) == types.ListType ):
			if( mc.objExists(obj[0]) ): 
				return self.toMayaObjs( obj , inValue , **args )
			else:                         
				return 0 #self.toValues(  obj , inValue , **args  )
		else:
			if( mc.objExists(obj) ): 
				if(mc.objExists(obj + '.' + self.utilsClasseInfoAttr ) ):
					return self.toMayaObjAttr( obj , inValue )	
				else:
					return self.toMayaObj( obj , inValue , **args )
			else:                      
				if( '/' in obj ): 
					return self.toFile( file , inValue )
				else:
					return 0 #self.toValue(  obj , inValue , **args  )


	#__________________________________________________________________

	def printInfo( self , title = '' , doPrint = 1 , match = '' , **args ):
		self.printAttrs(  title , doPrint , match , **args )


	#DEV FRIENLY ( NAME ACCURACY )
	def createFromValue( self , customValue , updateValue = 1 , **args):
		print('\tmayaClasse.createFromValue')
		customValue = self.createFromValueCustom( customValue , **args )
		if( updateValue == 1 ): self.value = customValue
		return customValue

	def createFromValues( self , customValues , updateValue = 1 , **args):
		print('\tmayaClasse.createFromValues')		
		customValue = self.createFromValuesCustom( customValues , **args )
		if( updateValue == 1 ): self.value = customValue
		return customValue

	def createFromMayaObj( self , obj , updateValue = 1 , **args ):
		print('\tmayaClasse.createFromMayaObj')		
		customValue = self.createFromMayaObjCustom( obj , **args )
		if( updateValue == 1 ): self.value = customValue
		return customValue

	def createFromMayaObjs( self , objs , updateValue = 1 , **args ):
		print('\tmayaClasse.createFromMayaObjs')				
		customValue = self.createFromMayaObjsCustom( objs , **args )
		if( updateValue == 1 ): self.value = customValue
		return customValue
		

	def createFromMayaSelection( self , updateValue = 1 , **args ):
		print('\tmayaClasse.createFromMayaSelection')				
		selection = mc.ls(sl = True )
		customValue = self.createFromMayaObjs( selection , updateValue , **args )
		if( customValue == 0 ) and ( len(selection) == 1 ):
			customValue = self.createFromMayaObj( selection[0] , updateValue , **args )	
		return customValue


	def createFromFile( self , file , updateValue = 1 ):
		dictionary = self.utils_xmlFileToDictionary( file )
		classeInstance = self.utils_dictToMayaClasse( dictionary )
		if( updateValue == 1 ):
			self.__class__ = classeInstance.__class__
			self.__dict__  = classeInstance.__dict__
		return classeInstance			

	def createFromMayaObjAttr( self , objAttr , updateValue = 1  ):
		dictionary = self.utils_mayaObjInfoToDictionary( objAttr )
		print( 'utils_mayaObjInfoToDictionary' , dictionary )
		classeInstance = self.utils_dictToMayaClasse( dictionary )
		print( 'utils_dictToMayaClasse' , classeInstance )	
		if( updateValue == 1 ): 
			self.__class__ = classeInstance.__class__
			self.__dict__  = classeInstance.__dict__
		return classeInstance	


	#__________________________________________________________________
	def copyInstance( self , inValue = None , updateValue = 1  , **args):
		return self.copyInstanceCustom( **args)

	def mirrorInstance( self , mirrorPlaneCoords , parent = None , **args ):
		return self.mirrorInstanceCustom( mirrorPlaneCoords , parent , **args )

	def deleteMayaObjs(self , **args):
		return self.deleteMayaObjsCustom( **args )

	#__________________________________________________________________
	def toMayaObj( self , obj  , inValue = None , **args ):
		print('\ttoMayaObj')
		value = self.utils_overrideValue( inValue )
		return self.toMayaObjCustom( obj , value , **args )    

	def toMayaObjs( self , objs , inValue = None , **args ):
		print('\ttoMayaObjs')
		value = self.utils_overrideValue( inValue )		
		return self.toMayaObjsCustom( objs , value , **args )    


	def toMayaSelection( self , inValue = None , **args ):
		print('\ttoMayaSelection')
		selection = mc.ls(sl = True )
		value     = self.utils_overrideValue( inValue )
		return self.toMayaObjsCustom( selection , value , **args )

	def buildMayaObj(self , inValue = None , **args ):
		print('\tbuildMayaObj')
		value  = self.utils_overrideValue( inValue )
		return self.buildMayaObjCustom( value , **args )

	def toFile( self , file , inValue = None ):
		dictionary = self.utils_mayaClasseToDict( self )
		if( inValue != None ): dictionary = self.utils_mayaClasseToDict( inValue )						
		self.utils_dictionaryToXmlFile( file , dictionary )		
		return 1
	
	def toMayaObjAttr( self , obj , inValue = None ):				
		dictionary = self.utils_mayaClasseToDict( self )
		if( inValue != None ): dictionary = self.utils_mayaClasseToDict( inValue )		
		self.utils_dictionaryToMayaObjInfo( obj , dictionary )		
		return 1		

	def printAttrs( self , title = '' , doPrint = 0 , match = '' , all = 0 ):
		if( doPrint == 1 ) or( self.debug == 1):
			attrNames = self.utils_getClasseAttributeNames( self )

			if( all == 1 ):
				print('#________UTILS')
				prefix = 'utils' 
				for attr in attrNames:
					if( len(prefix) <= len(attr) ) and ( attr[:len(prefix)] == prefix ):
						exec( 'self.utilsPrint = self.{1}'.format( self , attr ) )
						print( '{}.{}'.format(self.classeType , attr) , self.utilsPrint )	
	
				print('#________CLASSE')
				prefix = 'classe' 
				for attr in attrNames:
					if( len(prefix) <= len(attr) ) and ( attr[:len(prefix)] == prefix ):
						exec( 'self.utilsTmpPrint = self.{1}'.format( self , attr ) )
						print( '{}.{}'.format(self.classeType , attr) , self.utilsTmpPrint )	
	
			print('#________INSTANCE')
			prefix = 'instance' 				
			for attr in attrNames:
				if not( 'utils' in attr) and not( 'classe' in attr ):
					exec( 'self.utilsTmpPrint = self.{1}'.format( self , attr ) )
					print( '{}.{}'.format(self.classeType , attr) , self.utilsTmpPrint )

	

	#CLASSES FRIENLY ( HERITAGE )
	def createFromValueCustom(    self , obj , **args ):
		print('\t\tmayaClasse.createFromValueCustom') 
		return obj
	def createFromValuesCustom(    self , objs , **args ): 
		print('\t\tmayaClasse.createFromValuesCustom') 
		return objs	
	def createFromMayaObjCustom(  self , obj , **args ):
		print('\t\tmayaClasse.createFromMayaObjCustom')
		return obj
	def createFromMayaObjsCustom( self , objs , **args ):
		print('\t\tmayaClasse.createFromMayaObjsCustom') 
		return objs
	#__________________________________________________________________
	def copyInstanceCustom( self , **args ): 
		return copy.copy(self)
	def mirrorInstanceCustom( self , mirrorPlaneCoords , parent = None , **args ):
		return 0
	def deleteMayaObjsCustom( self , **args ):
		return 0
	#________________________________________________________________
	def toMayaObjCustom( self , obj , inValue , **args ):
		print( "\t\ttoMayaObjCustom") 
		return 0     
	def toMayaObjsCustom( self , objs , inValue = None , **args ):
		print( "\t\ttoMayaObjsCustom" ) 
		return 0    
	def buildMayaObjCustom(self , inValue = None , **args ):
		print( "\t\tbuildMayaObjCustom" ) 
		return 0
	

	#UTILS

	def utils_overrideValue( self , inValue ):
		if( inValue == None):
			outValue = self.value
		else:
			outValue = inValue	

		return outValue		

	
	
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
	

