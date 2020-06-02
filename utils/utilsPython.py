

'''
________________________________________________ NAME       
getObjBaseName 
removeEndDigits
________________________________________________ ARRAY CONVERTION
convertFlatArrayTo3by3
convertArrayToFlatArray   
convertArrayToArrayString                
convertArrayStringToArray      
convertStringArrayPythonToMelStringCommand
________________________________________________ ARRAY SORTING
convertChildrensFathersToDictInfluences
sortIndexChildrensByHierarchy   
moveInArray
________________________________________________ INDEX
getObjNameAndIndexs		
getArrayIndexsOfObjs
getDictIndexsOfObjs
________________________________________________ XML
writeXmlDicoVar                      
readXmlDicoVar                       
createXmlDicoVar    
________________________________________________ OTHER
getActualDate      
getActualTimeArray
getActualPath
getfileListInPath
convertStringToNum
getActualPath
removeDuplicate
removeArray
isArray



'''

import maya.cmds as mc
import types

#================================================================================================================================================================================================================================
#======================================================     NAME     ============================================================================================================================================================
#================================================================================================================================================================================================================================


#__________________________________________________________________________________________________________________________________________________________________________________________ getObjBaseName


def getObjBaseName( obj , keepPrefix = 0  , keepSuffix = 0 ):
	
	'''
		get the base name of a object ( exemple:  r_toto_msh.vtx[0:1] --------> ( 0,0 ) toto , ( 1,0 ) l_toto , ( 0,1 ) toto_msh     )
	'''

	baseName = obj.split(".")[0]
	
	nbrChars = []
	nbr = 0
	
	for char in baseName :
		if( char == "_" ):
			nbrChars.append(nbr)	
			nbr = 0
		else:
			nbr += 1
			
	nbrChars.append(nbr)

	
	if ( len( nbrChars ) > 1 ) and not( nbrChars[0] == 0 ):
  
		if( nbrChars[0] == 1 ) and ( keepPrefix == 0 ):
				baseName = baseName[ 2 : len(baseName) ]
	
		if not( ( nbrChars[0] == 1 ) and ( len( nbrChars ) == 2 ) ):
			if( keepSuffix == 0 ):
				baseName = baseName[ 0 : - ( nbrChars[-1] + 1 )  ]			
	
	return baseName	
				
#__________________________________________________________________________________________________________________________________________________________________________________________ removeEndDigits

def removeEndDigits( name ):
	
	'''
		remove digits at the end of the name  exemple  toto75 ----> toto  A55B222 -------> A55B
	'''
	
	
	digits = [ '0' , '1' , '2' , '3' , '4' , '5' , '6' , '7' , '8' , '9' ]
	loop = 0
	while( name[len(name)-1] in digits ):
		name = name[0:len(name)-1]
		loop += 1
		if(loop>100):
			print('ERROR: loop on getObjBaseName()')
			break
				
				
	return name		


def getEndDigits( name ):
	
	
	digits = [ '0' , '1' , '2' , '3' , '4' , '5' , '6' , '7' , '8' , '9' ]
	loop = 0
	nameBase = name
	while( name[len(name)-1] in digits ):
		name = name[0:len(name)-1]
		loop += 1
		if(loop>100):
			print('ERROR: loop on getObjBaseName()')
			break
	
	if( len(nameBase) == len(name) ):
		return None

	return int(nameBase.split(name)[1])		



def incrName( name ):
	baseName = removeEndDigits( name )
	nbr      = getEndDigits( name )

	if( nbr == None ): 
		nbr = 0

	nbr += 1
	newName = baseName + str(nbr)

	return newName



def dictionnaryCreate( varNames , values ):
	return dict(zip(varNames, values))


def dictionnaryMerge( dictBase , dictOverride ):
	dictOverrideCopy = dictOverride.copy()
	dictBase.update(dictOverrideCopy)
	return dictBase

'''
def dictionnaryMerge( dicoA , dicoB  , keepDuplicates = 0 ):
	if( keepDuplicates == 1 ):
		return dictionnaryMergeKeepDupli( dicoA , dicoB ) 
	else:
		return dictionnaryMergeOverrideDupli( dicoA , dicoB )

def dictionnaryMergeKeepDupli( dicoA , dicoB ):
	stop = 0
	while( stop == 0 ):
		stop = 1
		for keyB in dicoB.keys():
			if( keyB in dicoA.keys() ):
				keyBIncr = utilsPython.incrName(keyB)
				dicoB[keyBIncr] = dicoB[keyB]
				del dicoB[keyB]
				stop = 0
				break
	dico = dicoA.copy()					
	dico.update(dicoB)
	return dico


def dictionnaryMergeOverrideDupli(  dicoA , dicoB ):
	stop = 0
	while( stop == 0 ):
		stop = 1
		for keyB in dicoB.keys():
			if( keyB in dicoA.keys() ):
				del dicoA[keyB]
				stop = 0
				break
	dico = dicoA.copy()					
	dico.update(dicoB)
	return dico
	
'''


#================================================================================================================================================================================================================================
#======================================================     ARRAY CONVERTION     ================================================================================================================================================
#================================================================================================================================================================================================================================

#__________________________________________________________________________________________________________________________________________________________________________________________ convertArrayToArrayString

def convertArrayToArrayString( array ):
	
	arrayStr = str(array)
	
	return arrayStr 

#__________________________________________________________________________________________________________________________________________________________________________________________ convertArrayStringToArray
	
def convertArrayStringToArray( arrayStr ):
	
	varArrayTmp = []
	
	stringToExec = 'varArrayTmp = ' + arrayStr
	exec(stringToExec)
	
	return varArrayTmp 

#__________________________________________________________________________________________________________________________________________________________________________________________ convertStringArrayPythonToMelStringCommand
	
def convertStringArrayPythonToMelStringCommand( objs ):
	
	'''
		in python can be remplace by str( toto ) if toto is a list
		
		but in mel it didnt accept the '', and the []  , so '' ----> ""   [] ----> {}
	
	'''
	
	
	stringC  = ( '{"'+ objs[0] )
	for i in range( 1 , len(objs) ):
		stringC += ( '","' + objs[i] )
	stringC += '"}'	
	
	return stringC
				  


#__________________________________________________________________________________________________________________________________________________________________________________________ convertFlatArrayTo3by3


def convertFlatArrayTo3by3( flatArray ):

	'''
		converte [ 0 , 1 , 2 , 3 , 4 , 5 ] --------> [ [ 0 , 1 , 2 ] , [ 3 , 4 , 5 ] ]
	'''	
	
	array3by3 = []
	tmp       = []	
	
	for e in flatArray:
		tmp.append( e )
		if( len( tmp ) == 3 ):
			array3by3.append( tmp )
			tmp = []

	return array3by3	

	

    	
	
#__________________________________________________________________________________________________________________________________________________________________________________________ convertArrayToFlatArray

def convertArrayToFlatArray( array , maxlevel = 999999 ):
	
	'''
		flatten array to the minimum possible ( = down to one index)
		keep entire world for string
	'''
	currentLevel = 1
	flattenArray = array

	while not( maxlevel == currentLevel ):
		
		
		flattenArray = []
		
		sizeArray = len(array)
		noChangeLap = 0
		
		for elem in array:
			
			if( list == type( elem ) ):
				for e in elem:			
					flattenArray.append( e )
			else:
					flattenArray.append( elem )	
					noChangeLap += 1
							
		
		if( noChangeLap == sizeArray ):
			return flattenArray
				
		array = flattenArray
		currentLevel += 1
			
			
	return flattenArray	
	

#================================================================================================================================================================================================================================
#======================================================     ARRAY SORTING     ===================================================================================================================================================
#================================================================================================================================================================================================================================


#__________________________________________________________________________________________________________________________________________________________________________________________ convertChildrensFathersToDict		


def convertChildrensFathersToDictInfluences( childrens , fathers ):
	
	
	'''
		return a dictionary of the influance of the father: dico[father] = [ childrenA , chidrenB , childrenC]
		
		the two array must have the same size.
		one father   can have many childrens
		one children can have many fathers
	
	'''
	
	if not( len(childrens) == len(fathers) ):
		mc.error(' convertChildrensFathersToDict -----> both arrays must have the same size')

	influenceDict = {}
	
	size = len( childrens )
	
	#_1 get the influanced fathers and childrens
	
	for i in range( 0 , size ):
		if( fathers[i] in influenceDict.keys() ):
			influenceDict[ fathers[i] ] += [ childrens[i] ]			
		else:
			influenceDict[ fathers[i] ] = [ childrens[i] ]

	#_2 get the rest
	
	for i in range( 0 , size ):
		if not( childrens[i] in influenceDict.keys() ):
			influenceDict[ childrens[i] ] = ''
	
		if not( fathers[i] in influenceDict.keys() ):
			influenceDict[ fathers[i] ] = ''			
			
	return influenceDict

#__________________________________________________________________________________________________________________________________________________________________________________________ sortIndexChildrensByHierarchy		







def sortIndexChildrensByHierarchy( childrens , fathers ):

	'''
		
		the two array must have the same size.
		one father   can have many childrens
		---> one children can't have many fathers <--- because its a hierarchy
		
		return a list of index , the first is at the root of the hierarchy.
		
	
	'''
	#FILTER NONE
	childrensTmp = []
	fathersTmp   = []
	for i in range(0,len(childrens) ):
		if( type(childrens[i]) == types.StringType ):
			childrensTmp.append(childrens[i])
			fathersTmp.append(  fathers[i]  )

	childrens = childrensTmp
	fathers   = fathersTmp

	childrensDico = convertChildrensFathersToDictInfluences( childrens , fathers )
	#_____________________________________________find top fathers

	fatherTop = fathers
	lap = 0
	
	nbrEnd , nbrStart = 0 , 1 
	
	while( nbrEnd < nbrStart ):
		
		nbrStart = len(fatherTop)
		fathersTest = []

		for father in fatherTop:
			fatherFound = 0
			for i in range( 0 , len(childrens) ):
				if( father == childrens[i] ):
					fathersTest.append( fathers[i] )
					fatherFound = 1
					break
					
			if ( fatherFound == 0 ):
				fathersTest.append(	father)	
			
		fatherTop = list(set(fathersTest))
		nbrEnd    = len(fatherTop)	
	
		lap += 1
		if( lap > 500 ):
			mc.error('loop!')	

	#_____________________________________________find hierarchy	
	childrensTest  = []	
	indexSorted    = []
	
	lap = 0

	while not ( len(indexSorted) == len(childrens) ):
		
		childrensFound = []		
		for i in range( 0 , len(childrens) ):
			for father in fatherTop:	
				if( childrens[i] in childrensDico[father] ) and not( i in indexSorted ):
					indexSorted.append(i)
					childrensFound.append(childrens[i])
					
		fatherTop = childrensFound					
				
		lap += 1
		if( lap > 500 ):
			mc.error('loop!')
			
	return indexSorted	
	
	
	
	
	
	
#__________________________________________________________________________________________________________________________________________________________________________________________ moveInArray			
	
def moveInArray( array , elem , iToMove ):
	
	'''
		move an elem inside an array of iToMove index
		
		moveInArray( [ 'a' , 'b' , 'c' , 'D' , 'e' ] , 'D' , -2  )	   -----------> ['a', 'D', 'b', 'c', 'e']
	
	'''
	
	index =  array.index(elem)
	array.pop( index )
	newI = index + iToMove
	
	array.insert( newI , elem)
	
	return array
		
	
	
	
	
#================================================================================================================================================================================================================================
#======================================================     INDEX     ===========================================================================================================================================================
#================================================================================================================================================================================================================================

		

#__________________________________________________________________________________________________________________________________________________________________________________________ getObjNameAndIndexs

def getObjNameAndIndexs( componentName ):
	
	'''
		toto ----> [ toto , [] ]
		toto.f[10] ----> [ toto , [10] ]
		toto.vtx[0:3] ----> [ toto , [ 0 , 1 , 2 , 3 ] ]		
	'''
	
	
	splitName = componentName.split('.')
	
	if( len( splitName ) == 1 ):
	    return [ componentName , [] ]
	
	obj = splitName[0]
	indexRaw = splitName[1]
	
	indexsMinMax = indexRaw.split('[')[1].split(']')[0].split(':')
	
	if( len(indexsMinMax) == 1 ):
	    return [ obj , [int(indexsMinMax[0])] ]  
	
	indexsList = [ i for i in range( int(indexsMinMax[0]) , int(indexsMinMax[1]) + 1 )]
	
	return [ obj , indexsList ]
	
#__________________________________________________________________________________________________________________________________________________________________________________________ getObjNameAndIndexs

def getArrayIndexsOfObjs( componentNames , filtre = '' ):
	
	'''
		return all indexs of the objs in filtre in a simple array 
		
		[ toto.vtx[0:3] , baba.vtx[10:15]  ] , filtre = ['toto'] ----> [ 0 , 1 , 2 , 3 ]
		
	
	'''
				
	indexs = []
	for elem in componentNames:
		obj , objIndexs = getObjNameAndIndexs( elem )
		if( filtre in obj ):
			indexs += objIndexs
	  
	return indexs

	
#__________________________________________________________________________________________________________________________________________________________________________________________ getDictIndexsOfObjs	
def getDictIndexsOfObjs( componentNames ):
	
	'''
		return all indexs and obj in dictionnary 
		
		[ toto.vtx[0:3] , baba.vtx[10:15]  ] , dict['toto'] = [ 0 , 1 , 2 , 3 ]
		
	
	'''
				
	dico = {}
	for elem in componentNames:
		obj , objIndexs = getObjNameAndIndexs( elem )
		
		try:
			dico[obj] = list(set(objIndexs + dico[obj] )) 
		except:
			dico[obj] = objIndexs
    	        	  
	return dico


#================================================================================================================================================================================================================================
#======================================================      XML      ===========================================================================================================================================================
#================================================================================================================================================================================================================================




#__________________________________________________________________________________________________________________________________________________________________________________________ writeXmlDicoVar


	
from xml.dom.minidom import Document
from xml.dom.minidom import parse

def writeXmlDicoVar( fileBaseName , path , dictToWrite ):

	
	doc = Document()
	
	root_node = doc.createElement("scene")
	doc.appendChild(root_node)
	
	for key in dictToWrite.keys():
	    
	    # create object element
	    object_node = doc.createElement("object")
	    root_node.appendChild(object_node)
	
	    # set attributes
	    object_node.setAttribute("__name__", key )
	    
	    for i in range( 0 , len(dictToWrite[key]) ):
	        object_node.setAttribute( ("attr" + str(i) ), str( dictToWrite[key][i] )  )

	xml_file = open( ( path + fileBaseName + '.xml'), "w")
	xml_file.write(doc.toprettyxml())
	xml_file.close()
	
	return 1

#__________________________________________________________________________________________________________________________________________________________________________________________ readXmlDicoVar	
	
def readXmlDicoVar( fileBaseName , path ):
	
	dom = parse(( path + fileBaseName + '.xml'))
	
	dictValues = {}
	
	 # visit every object node 
	for node in dom.getElementsByTagName('object'):
		toolName = str(node.getAttribute("__name__"))
		attrNames  = node.attributes.keys()
		attrNames.sort()
		attrsValueStr = []
		for attr in attrNames:
			if not( attr == "__name__" ):
				attrsValueStr.append( str( node.getAttribute(attr) ) )
		
		#COORDS
		attrsValue = []	
		toEval = ''
		for i in range( 0 , len(attrsValueStr) ):
			toEval =  ( 'attrsValue.append( ' + attrsValueStr[i] + ')' )
			exec(toEval)
		
		dictValues[toolName] = attrsValue	            
	        
	return dictValues  

#__________________________________________________________________________________________________________________________________________________________________________________________ createXmlDicoVar	


def createXmlDicoVar( fileBaseName , path ):
	'''
	seulement si il n existe pas
	'''
	try:
		dom = parse(( path + fileBaseName + '.xml'))
	except:
		doc = Document()
		root_node = doc.createElement("scene")
		doc.appendChild(root_node)
		object_node = doc.createElement("object")
		root_node.appendChild(object_node)	
		
		xml_file = open( ( path + fileBaseName + '.xml'), "w")
		xml_file.write(doc.toprettyxml())		
		xml_file.close()

	


#================================================================================================================================================================================================================================
#======================================================     OTHER     ===========================================================================================================================================================
#================================================================================================================================================================================================================================
	
	
#__________________________________________________________________________________________________________________________________________________________________________________________ getActualDate			
			
import datetime 

def getActualDate():
	dateClass = datetime.date.today()	
		
	return '{0}/{1}/{2}'.format( dateClass.day , dateClass.month , dateClass.year )		
	
	
#__________________________________________________________________________________________________________________________________________________________________________________________ getActualTimeArray		
def getActualTimeArray():
	dateClass = datetime.datetime.today()

	
	timeArray = [ dateClass.year , dateClass.month , dateClass.day , dateClass.hour , dateClass.minute , dateClass.second ]
		
	return timeArray		


 		
#__________________________________________________________________________________________________________________________________________________________________________________________ getActualTimeArray	
		
import os

def getFilesInPath( path , extention = None ):	
	
	if( extention == None ):
		files = [ elem    for elem in os.listdir( path ) ]	
	elif( extention == '' ):
		files = [ elem    for elem in os.listdir( path )    if not( '.' in elem ) ]
	else:
		files = [ elem    for elem in os.listdir( path )    if ( extention == elem[ -len(extention) : len(elem) ] ) ]
		
	return files	
	


#__________________________________________________________________________________________________________________________________________________________________________________________ convertStringToNum	
import string 


def convertStringToNum( rawString ):

	if not ( type(rawString) is str ) and not( type(rawString) is unicode ):
		return rawString

	for elem in rawString:	
		if( elem in string.ascii_lowercase ) or ( elem in string.ascii_uppercase ) :
			return rawString

	if( '[' in rawString ) or ( '(' in rawString ):
		
		cleanStringTmp = rawString[1:-1]
		cleanStringTmpArray = cleanStringTmp.split(',')
		
		arrayBuild = [ float(elem) for elem in cleanStringTmpArray ]
		newNum = arrayBuild
	
	else:
		newNum = float(rawString)
	
	return newNum
	
	
#__________________________________________________________________________________________________________________________________________________________________________________________ getActualPath		

def getActualPath():
	arrayPath = __file__.split('\\')
	selfPath  = '/'.join(arrayPath[0:-1]) + '/'
	return selfPath

	
#__________________________________________________________________________________________________________________________________________________________________________________________ getActualPath		
def removeDuplicate( rawArray ):
    
    seen = set()
    result = []
    for item in rawArray:
        if item not in seen:
            seen.add(item)
            result.append(item)

    return result
#__________________________________________________________________________________________________________________________________________________________________________________________ getActualPath		
def removeArray( array , toRemove ):
    
    for elem in toRemove:
        array.remove(elem)
    
    return array



def isArray( variable ):
	if( type(variable) == types.StringType ) or ( type(variable) == types.UnicodeType ): 
		return 0
	else:
		try:
			toto = variable[0]
		except:
			return 0
		return 1

def isString( variable ):
	if( type(variable) == types.StringType ) or ( type(variable) == types.UnicodeType): return 1
	else:                                     return 0

def isPath( variable ):
	if('/' in variable ):
		return 1
	else:
		return 0



def isMultiArray( variable ):

	for i in range( 0 , len( variable ) ):

		if( type(variable[i]) == types.StringType ) or ( type(variable[i]) == types.UnicodeType ): 
			continue

		try:
			toto = variable[i][0]
			return 1
		except:
			pass

	return 0


'''
grps = mc.ls('rigPuppet_GRP|*_GRP' , type = "transform" )
listOrderRef = ['r_reac','l_reac','r_hook','l_hook','r_propulsor','l_propulsor','damp']
grps = utilsPython.sortStringArrayWithRefs( grps , listOrderRef )
'''

def sortStringArrayWithRefs( array , listOrderRef ):
	arraySorted = []
	for orderRef in listOrderRef:
		for i in range(0,len(array)):
			if( orderRef in array[i] ) and not( array[i] in arraySorted ):
				arraySorted.append(array[i])

	for i in range(0,len(array)):
		if not( array[i] in arraySorted ):
			arraySorted.append(array[i])

	return arraySorted

