import maya.cmds as mc


from . import coords as coordsClasse
from . import readWriteInfo
from ..utils import utilsMaya
from ..utils import utilsPython
from ..utils import utilsMath
from ..utils import utilsMayaApi
from .mayaClasse import *





class name( mayaClasse ):
	
	def __init__(self):
		mayaClasse.__init__(self )	
		#UTILS	
		self.utilsSuffixGrp       = '_GRP'          
		self.utilsSuffixOffset    = '_OFFSET'   
		self.utilsSuffixCtrl      = '_CTRL'
		self.utilsSuffixJnt       = '_JNT'
		self.utilsSuffixLoc       = '_LOC'
		self.utilsSuffixIkHandle  = '_IKH'				
		self.utilsSuffixCtrlShape = 'Shape'	
	
		self.utilsManipDupliGrp        = 'manipDupli_grp'
		self.utilsManipDupliCAM        = 'manipDupliCamera1' 
		self.utilsManipDupliSuffix     = '_dupli'			
		# MAIN GRP ATTR NAME
		'''
		self.mainGrpAttrNameIns        = 'ins'				
		self.mainGrpAttrNameOuts       = 'outs'
		self.mainGrpAttrNameCtrls      = 'ctrls'
		self.mainGrpAttrNameBeacons    = 'beacons'		
		self.mainGrpAttrNameAlls       = 'alls'
		self.mainGrpAttrNameSubRigs    = 'subRigsMainGrp'
		self.mainGrpAttrNameRigType    = 'rigType'	
		self.mainGrpAttrNameBuildTrs   = 'buildTrs'
		self.beaconAttrNameMainGrp     = 'mainGrp'	
		self.mainGrpAttrNameInsPrefix  = '_in_'		
		self.mainGrpAttrNameOutsPrefix = '_out_'		
		'''
		self.utilsDefaut = 'default' 		
		#____________________________________________________________________RIG INFO				
		#CLASSE
		self.classeType = 'name'
		#INSTANCE
		self.prefix    = '';
		self.baseName  = ''
		self.baseNames = []
		self.suffix    = []	
		self.value     = None			


	getMayaObjSuffix()
	mirror()
	getLogicalSide()
	getLogicalSuffix()
	getLogicalBaseName()


	.baseName ===> return only base name of the name 


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

def removeFullPathIfNoDupli( oldName ):

	'''
		remove full path if no duplicate   else   keep it
		if oldName is not a full path do nothing
	'''
	
	if not ( '|' in oldName ):
		return oldName
					
	shortName  = oldName.split('|')[-1]
	nameDuplis = mc.ls(shotName)
	
	if( len(nameDuplis) > 1 ):
		return oldName

	return shortName





def convertFullPathToDupliPath( path ):

	'''
	in maya this is a full path :    |toto|tata|tataShape          and this is a dupli path :    toto|tata|tataShape
	the goal is to remove the first |     , it easier to compare name after that
	'''
	
	if( '|' == path[0] ):
		path = path[1:len(path)]
			
	return path

	
#_______________________________________________________________________________________________________________________________________________________________________ incrBaseNameIfExist


def incrBaseNameIfExist( baseName , prefixsToCheck = [] , suffixsToCheck  = []  ):
	
	'''
		increment if the baseName is already use with the specified suffix and specified prefix:
		exemple:   incrBaseNameIfExist(  'toto'  ,  ['' , 'l_']  ,  ['' , '_ctrl' , '_msh']   )


		nothing           exist    toto -------> toto		
		toto1-toto2-toto3 exist    toto -------> toto4
		toto4             exist    toto -------> toto1
		toto1-toto2-toto4 exist    toto -------> toto3		

		nothing           exist    toto5 -------> toto1		
		toto1-toto2-toto3 exist    toto5 -------> toto4
		toto4             exist    toto5 -------> toto1
		toto1-toto2-toto4 exist    toto5 -------> toto3		
		
	'''
	
	
	# BASENAME WITHOUT END DIGITS
	baseNameNoEndDigits = utilsPython.removeEndDigits(baseName)
	
	# FILTERED OBJ IN THE SCENE
	objs = mc.ls( '*{0}*'.format(baseNameNoEndDigits)  )
	
	if( len(objs) == 0 ):
		if(  baseNameNoEndDigits == baseName ):
			return baseName
		else:
			return baseNameNoEndDigits + '1'	

	# OBJ WITHOUT SUFFIX OR PREFIX
	objsBaseName = []
	for elem in objs:
				
		matching = 0
		curentElem = elem
		
		curPrefix = '' 

		matching = []
		for prefix in prefixsToCheck:

			if( curentElem[0:len(prefix)] == prefix ) and not ( prefix == '' ):
				curentElem = curentElem[len(prefix):len(curentElem)]
				matching.append( 1 )
				curPrefix  = prefix 			
				
			elif( prefix == '' ) and ( curentElem[0:len(baseNameNoEndDigits)] == baseNameNoEndDigits  ):				
				matching.append( 1 )
				
			else:
				matching.append( 0 )

		if not ( 1 in matching ):
			continue
			
		matching = []				
		for suffix in suffixsToCheck:		
		
			if( curentElem[len(curentElem)-len(suffix):len(curentElem)] == suffix )  and not ( suffix == '' ):
				curentElem = curentElem[0:len(curentElem)-len(suffix)]
				matching.append( 1 )					
				
			elif( suffix == '' ) and ( curentElem[len(curPrefix):len(curPrefix)+len(baseNameNoEndDigits)] == baseNameNoEndDigits  ):
				matching.append( 1 )							
				
			else:
				matching.append( 0 )					

				
		if ( 1 in matching ):
			objsBaseName.append( curentElem )	
	
	
	if( objsBaseName == [] ):
		if(  baseNameNoEndDigits == baseName ):
			return baseName
		else:
			return baseNameNoEndDigits + '1'		
			

	# END DIGITS OF OBJ	
	baseNameNbr = []
	for obj in objsBaseName:
		
		if( obj[0:len(baseNameNoEndDigits)] == baseNameNoEndDigits  ):
			try:
				baseNameNbr.append( int( obj[len(baseNameNoEndDigits):len(obj)] ) )
			except:
				pass
		
	baseNameNbr.sort()
			
	# RIGHT DIGIT FOR THE BASE NAME		
				
	i = 1			
	rightDigit = 0
	while( rightDigit == 0):
		
		if not( i in baseNameNbr ):
			rightDigit = i
	
		i += 1		
		if( i > 700 ):
			mc.error('loop')
	
	newBaseName = baseNameNoEndDigits + str(rightDigit) 		
	
	return newBaseName


'''

def incrBaseNameIfExist( baseName , prefixsToCheck = [''] , suffixsToCheck  = ['']  ):
	
	
		increment if the baseName is already use with the specified suffix and specified prefix:
		exemple:   incrBaseNameIfExist(  'toto'  ,  ['' , 'l_']  ,  ['' , '_ctl' , '_msh']   )


		nothing           exist    toto -------> toto		
		toto1-toto2-toto3 exist    toto -------> toto4
		toto4             exist    toto -------> toto1
		toto1-toto2-toto4 exist    toto -------> toto3		
		
	
	
	
	baseNameNoEndDigits = utilsPython.removeEndDigits(baseName)

	i = 1	
	if not( baseNameNoEndDigits == baseName ):
		i = 1			

	loop = 1
	baseNameToCheck = baseNameNoEndDigits
	
	while( loop == 1 ):
		
		loop = 0	
		
		if not( i == 0 ):			
			baseNameToCheck = baseNameNoEndDigits + str(i)
			
		for prefix in prefixsToCheck:			
			for suffix in suffixsToCheck:				
				if( mc.objExists( prefix + baseNameToCheck + suffix ) ):
					loop = 1
					i   += 1
					break
					
			if(loop == 1):
				break
	
		if( i > 700 ):
			mc.error('loop')
	
			
	return baseNameToCheck

'''

#_____________________________________________________________________________________________________________________________________________________________________ sortObjsByHierarchy

def sortObjsByHierarchy( objs ):
	
	fathers = []
		    
	for elem in objs:
		father = mc.listRelatives( elem , p = True )
		if( father == None ) or not( father in objs ):
		    fathers.append('')
		else:
		    fathers.append(father[0])	
	
	indexs = utilsPython.sortIndexChildrensByHierarchy( objs ,  fathers )
	
	sortedObjs = []
	
	for i in indexs:
		sortedObjs.append(objs[i])
	
	return sortedObjs



#_____________________________________________________________________________________________________________________________________________________________________ renameObjsByAddPrefixSuffix

def renameObjsByAddPrefixSuffix( objs , prefix = '' , suffix = '' ):
		
	sortedObjs = sortObjsByHierarchy( objs )
	sortedObjs.reverse()

	newNames = []
	
	for elem in sortedObjs:
		
		if( '|' in elem ):
			splitName = elem.split('|')
			newName   = prefix + splitName[-1] + suffix
		else:
			newName = prefix + elem  + suffix
			
		mc.rename( elem , newName )
		newNames.append(newName)
	    	
	return newNames
	



def getLongName( shortName ):
    return mc.ls( shortName , l = True , r = True)[0];
    
def getShortName( longName ):
    return mc.ls( longName , l = False , r = True)[0];



#_____________________________________________________________________________________________________________________________________________________________________ deleteAllNamespace

def deleteAllNamespace():
	
	nsToKeep = [ 'UI' , 'shared' ]
	
	nsAll = mc.namespaceInfo( lon = True )
	i = 0
	
	while not ( len(nsAll) == len(nsToKeep) ):
	    
	    nsAll = mc.namespaceInfo( lon = True )
	
	    for ns in nsAll:
	        if( ns in nsToKeep ):
	            continue
	        mc.namespace( rm = ns , mnr = True )
	
	    i+=1
	    
	    if( i > 100 ):
	        mc.error('loop')
	
   	