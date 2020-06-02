

'''                                                           

________________________________________________ NAME
removeFullPathIfNoDupli
convertFullPathToDupliPath                
incrBaseNameIfExist
sortObjsByHierarchy
renameObjsByAddPrefixSuffix
getLongName
getShortName
________________________________________________ FIX
fixBugDupli_getShapeTransform
fixBug_convertShapeComponentToTransformComponent   
________________________________________________ TRS
setTRSValueToObj       # in trsClass
getWorldTrsValue       # in trsClass
________________________________________________ CURVE
getCurveLength
simlifyCurve
convertCurveToBezier
getCurveCoords
buildCurveShapeWithCoords
________________________________________________ UI
buildUi_makeNiceBox 
________________________________________________ SHADER
convertShaderEnginesToShaders
getShadersOfObj
getObjsOfShader
getSimilarShaders
setShaderToObj
cleanSceneDupliShader   
________________________________________________ CONSTRAINT	
getConstraintSlaves			 
getConstraintMasters		
buildConstraint		
resetConstraint
buildConstraintProximity
________________________________________________ BUILD BASE 
buildCurveShape
buildCurveShapeWithCoords
buildManipBase
buildOrig
createDagNodes 
createSets 
________________________________________________ BUILD RIG 
buildDistDimensionSys
createLocsOnCoords
buildSimpleLoc
createAllConstraintGrp  <<<<<<
________________________________________________ ATTR
getManipulableAttr
addSpecialAttr
addSpecialAttrs
writeStringAttr
writeStringArrayAttr
readStringArrayAttr
writeCustomDv
setToCustomDv
resetControlValue
________________________________________________ NODE CONNECTION
buildConnections
buildOffsetConnection
buildNodeNetWork
createSpecialNode
buildSimpleExpression
________________________________________________ AUTRE <<<<<
getSpecialType
getAllChildrenMsh                  
findManipMaster 
addInSet  
transfereAnim                        
deleteTypeChildren
deleteAllNamespace
convertFaceEdgeTovtx
sortObjWithHisClosestOne		
sortObjByProximity	
buildFollicle
getAllChildrens
filterType


'''

import maya.cmds as mc
import maya.OpenMaya as om
import string
import types
from . import utilsMath
from . import utilsMayaApi
from . import utilsBin
from . import utilsPython

from ..classe import trsBackUp as trsClass
from ..classe import coords as coordsClasse

print(' === import utilsMaya ===')

#================================================================================================================================================================================================================================
#======================================================     NAME     ============================================================================================================================================================
#================================================================================================================================================================================================================================

#_____________________________________________________________________________________________________________________________________________________________________ remove full path if no dupli 	

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

#_____________________________________________________________________________________________________________________________________________________________________ convert Full Path To Dupli Path 	

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
	
#================================================================================================================================================================================================================================
#======================================================      FIX     ============================================================================================================================================================
#================================================================================================================================================================================================================================ 

	
#_____________________________________________________________________________________________________________________________________________________________________ fixBugDupli_getShapeTransform

def fixBugDupli_getShapeTransform( shapeName ):
	
	
	'''
		===== bug find in MAYA 2016 ===== 
		
		If you duplicate a hierarchy. the objs name will be replace by a dupli path(     elemA|elemB    and    elemA1|elemB    ).
		It s working if there is shapes but it will raise an error if you selected them (     elemA|elemB|shapeB    and    elemA1|elemB|shapeB    ).
		
		the solution is to rename.
		
		In the case of (     elemA|elemB|shapeB    and    elemA1|elemB|shapeC    ) both shapes are renamed but there transform have the same name.
		This time you can selecte the shape.		
		BUT when you use    listRelatives( shapeC , p = True) ----->  elemB     instead of his dupliName    elemA1|elemB| 
						
		==========================

		this proc fix the probleme and return a duplipath if its a dupli		
	
	'''

	parents         = mc.listRelatives( shapeName , p = True , f = True )
	transformParent = convertFullPathToDupliPath( parents[0] )
	transformName   = removeFullPathIfNoDupli( transformParent )
			
	return transformName

	

 
#_____________________________________________________________________________________________________________________________________________________________________ fixBug_convertShapeComponentToTransformComponent 	

def fixBug_convertShapeComponentToTransformComponent( selection ):
	
	
	'''
		===== bug find in 2016 ===== 
		
		In Maya, for ALL geometry ( mesh , curve , nurbs ... ) , when you query component's name ( by selecting it for exemple ) , it give you either :
		
		'transformName'.vtx[0]      ----> if there is only the shape under the transform     
		
		or 
		
		'shapeName'.vtx[0]          ----> if there is more objs than the shape under the transform
		
		warning: when you select or use the component there is no bug, both name works
		
		==========================
		
		This proc convert only the  'shapeName'.vtx[0]   to   'transformName'.vtx[0] 
		
		return the input if nothing to convert
		
	
	'''

	newSelection = []
	
	for elem in selection:
		
		objName = elem 
		
		if( "." in elem ):
			
			objName =       elem.split(".")[0] 
		
			if( mc.objectType( objName , isa = 'transform' ) ):
				newSelection.append( elem )	
			else:				
				transformParent =  fixBugDupli_getShapeTransform( shapeName )			
				suffix          = '.' + elem.split(".")[1] 				
				newElem         =  transformParent + suffix				
				newSelection.append( newElem )					
		
		else:
			
			newSelection.append(elem)
				
				
	return newSelection

#================================================================================================================================================================================================================================
#======================================================     TRS      ============================================================================================================================================================
#================================================================================================================================================================================================================================
#_____________________________________________________________________________________________________________________________________________________________________ set TRS Value  # in trsClass

def setTRSValueToObj( obj  , TRSvalue ):  # in trsClass
	
	'''
		TRSValue = [ 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1 ]      TRS stand for Translate Rotate Scale	
	'''
		
	axes = [ 'X' , 'Y' , 'Z' ]
	
	for i in range( 0 , 3 ):
		 mc.setAttr( obj + ( '.translate' + axes[i] )    , TRSvalue[i    ]  )
		 mc.setAttr( obj + ( '.rotate'    + axes[i] )    , TRSvalue[i + 3]  )
		 mc.setAttr( obj + ( '.scale'     + axes[i] )    , TRSvalue[i + 6]  )	


#_____________________________________________________________________________________________________________________________________________________________________ getWorldTrsValue  # in trsClass
def getWorldTrsValue( obj ):  # in trsClass
	
	'''
		TRSValue = [ 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1 ]      TRS stand for Translate Rotate Scale	
	'''


	worldValues = mc.xform( obj , q = True , t   = True , ws = True )
	pivValues   = mc.xform( obj , q = True , piv = True )	
	tValues     = [ ( worldValues[0] + pivValues[0] ) , ( worldValues[1] + pivValues[1] ) , ( worldValues[2] + pivValues[2] )  ]
	
	
	rValues = mc.xform( obj , q = True , ro = True , ws = True )
	sValues = mc.xform( obj , q = True , s = True  , ws = True )	
	
	trsValues = tValues + rValues + sValues 
	
	return trsValues



#================================================================================================================================================================================================================================
#======================================================    CURVE     ============================================================================================================================================================
#================================================================================================================================================================================================================================

#_________________________________________________________________________________________________________________________________________________________________________  getCurveLength	

def getCurveLength( curveName ):
	
	curveInfoNode  = mc.arclen( curveName , ch = True )
	length         = mc.getAttr( curveInfoNode + '.arcLength' )
	mc.delete(curveInfoNode)
	
	return length


#_________________________________________________________________________________________________________________________________________________________________________  simlifyCurve	
	
def simlifyCurve( curveBaseName , tolerence ):
	
	'''
		will simpify the curve until the length of the simplify curve and the initial one are too diffenrent.
		the tolerence is for control this different
		
		tolerence:
		0 ---> 10
		1     : no   change of the length is tolerate
		1 < x : some change of the length is tolerate
		
		the curve is replaced by the simplified one
	
	'''
	
	tolerence /= 20.0  # tol 1 ---> 10

	lengthBase = getCurveLength( curveBaseName ) 
	
	nbrCvBase   = mc.getAttr( curveBaseName + '.spans')
	nbrCvMinMax = [ 0 , nbrCvBase ]	
	curveTest   = curveBaseName + '_test'

	i = 0
	while( ( nbrCvMinMax[1] - nbrCvMinMax[0] ) > 1 ):
		
		nbrCvTest = nbrCvMinMax[0] + ( nbrCvMinMax[1] - nbrCvMinMax[0] ) / 2	
				    
		mc.rebuildCurve( curveBaseName , n = curveTest , spans = nbrCvTest , ch = 1 , rpo = 0 , rebuildType = 0 , end = 1 , kr = 0 , kcp = 0 , kep = 1 , kt = 0 , d = 3 , tol = 0.01 )
		
		lengthTest = getCurveLength( curveTest )  
	
		if( lengthTest <  ( lengthBase - tolerence * lengthBase  ) ):
		    nbrCvMinMax[0] = nbrCvTest    
		else:
		    nbrCvMinMax[1] = nbrCvTest
      		
		i += 1
		mc.delete(curveTest)
		
		if( i > 200 ):
			mc.error('loop')

			
	mc.rebuildCurve( curveBaseName , n = curveTest , spans = nbrCvMinMax[1] , ch = 1 , rpo = 0 , rebuildType = 0 , end = 1 , kr = 0 , kcp = 0 , kep = 1 , kt = 0 , d = 3 , tol = 0.01 )	
	mc.delete( curveBaseName )
	mc.rename( curveTest , curveBaseName )	


#____________________________________________________________________________________ convertCurveToBezier	
		
def convertCurveToBezier( curveName ):
    mc.select( curveName )
    mc.nurbsCurveToBezier()
    

	
#____________________________________________________________________________________ getCurveCoords	


def getCurveCoords( curveName ):
	
	'''
		return an array of coords [ [0,0,0] , [0,0,0] ] corresponding to coords's CVs 
		
		CVs = spans + degree
		knot = CVs + degree - 1
		
	'''
	
	allCoords = []
	
	nbrSpans     = mc.getAttr( curveName + '.spans' ) 
	degree       = mc.getAttr( curveName + '.degree' )  	
	nbrCvs       = nbrSpans + degree  
	
	for i in range( 0 , nbrCvs ):
	    cvCoords  = mc.xform( '{0}.cv[{1}]'.format( curveName , i ), q = True , t = True , ws = True  )
	    allCoords.append(cvCoords)    

	
	return allCoords

'''
def getCurveCoords( curveName ):
	

		return an array of coords [ [0,0,0] , [0,0,0] ] corresponding to coords's CVs 

	
	allCoords = []
	
	nbrSpans     = mc.getAttr( curveName + '.spans' ) 
	nbrCvs       = nbrSpans + 2
	
	for i in range( 0 , nbrCvs + 1 ):
		cvCoords  = mc.xform( '{0}.cv[{1}]'.format( curveName , i ), q = True , t = True , ws = True  )
		allCoords.append(cvCoords)    
	
	
	# each time you create a curve it add degree + 1 coords 
	degree = mc.getAttr( curveName + '.degree' ) 	 
	nbrCoordToRemove = degree + 1	
	curveCoords = allCoords[ 0 : len(allCoords) - nbrCoordToRemove ] 
	    
	return curveCoords
'''


#____________________________________________________________________________________ simplifyCurveCoords	
		
def simplifyCurveCoords( curveCoordsBase ):
	
	curveTmpName = 'simplifyCurveCoordsTmp_crv'
	mc.createNode( 'transform' , n = curveTmpName )		
	buildCurveShapeWithCoords( curveTmpName , curveTmpName + 'Shape' , curveCoordsBase  , 3 , 'blue' )		
	simlifyCurve( curveTmpName , 2 ) # 0.3
	convertCurveToBezier( curveTmpName )

	curveCoordsSimplify = getCurveCoords( curveTmpName )		
	
	mc.delete( curveTmpName )

	return curveCoordsSimplify
		    
    
#================================================================================================================================================================================================================================
#======================================================      UI      ============================================================================================================================================================
#================================================================================================================================================================================================================================

#__________________________________________________________________________________________________________________________________________________________________________________________ buildUi_makeNiceBox


def buildUi_makeNiceBox( name , father , layoutWidth , casesHeight , caseCommands , caseWidthPercent ):
	
	'''		
		create a UI box in a raw with this shape:
		
		                        				    layoutWith		
		                        *________________________________________________*
		                        
		                        --------------------------------------------------
		                 *      | |----------------| |---------------| |-------| |
		                 |      | |                | |               | |       | |
		       caseHeight|      | |       40%      | |      35%      | |  15%  | |  ( 100% - ( 40% + 35% + 15% ) ---> 10% intervales )
		                 |      | |                | |               | |       | |
		                 *      | |----------------| |---------------| |-------| |
		                        --------------------------------------------------
		
		You define a layoutWith , a caseHeight  and  a  % for the width of case ( the % of intervales is compute by the proc )
		
		Give it a name , a father and some commands to fill the cases and thats all

		exemple:
		buildUi_makeNiceBox( layoutWidth =  90  , casesHeight = 10 , caseCommands = [ 'mc.textField('toto')' , mc.button( 'tata' , c = 'goHome' )     ] , caseWidthPercent = [ 10 , 80 ]  ):
		
	'''	
	# calcule some dimention    casesWidth casesHeight intevalSize
	
	
	nbrWCases      = len( caseCommands )
	nbrWIntervals  = nbrWCases + 1

	nbrHCases      = 1
	nbrHIntervals  = 2
		
	casesWidth     = []
	allCasesWidthPercent = 0
	
	
	for i in range( 0 , nbrWCases ):
		casesWidth.append( caseWidthPercent[i] * layoutWidth / 100 )
		allCasesWidthPercent += caseWidthPercent[i]
		
	intevalWPercent = ( 100 - allCasesWidthPercent   ) / nbrWIntervals 	
	intevalSize     =   layoutWidth * intevalWPercent  / 100

	# create layout
	
	nbrColumn        = ( nbrWCases + nbrWIntervals )
	arrayColumnWidth = []	
	columnWidth      = []	
	j                = 0

	for i in range( 0 , nbrColumn ):

		if( i % 2 ):		
			columnWidth.append( casesWidth[j] )
			j += 1						
		else:
			columnWidth.append( intevalSize )
		
	for i in range( 0 , nbrColumn ):
		arrayColumnWidth.append( ( ( i + 1 ) , columnWidth[i] ) )
		
	mc.rowColumnLayout( name , nc = nbrColumn , columnWidth = arrayColumnWidth  , p = father )
	j = 0
	
	for i in range( 0 , nbrColumn ):
		mc.text( l = ' ' , h = intevalSize )

	for i in range( 0 , nbrColumn ):
		
		if( i % 2):	
			exec( caseCommands[j] )
			j += 1				
		else:			
			mc.text( l = ' '  , h = casesHeight )	
		
	for i in range( 0 , nbrColumn ):
		mc.text( l = ' '  , h = intevalSize )

	return name	

#================================================================================================================================================================================================================================
#======================================================    SHADER    ============================================================================================================================================================
#================================================================================================================================================================================================================================



#_____________________________________________________________________________________________________________________________________________________________________ convertShaderEnginesToShaders  

def convertShaderEnginesToShaders( shaderEngines ):
	
	'''
		find the shader associated with the shaderEngine
		input and output are array	
	'''
	
	shaders = []
	    
	for sg in shaderEngines:
	    shadersSG = mc.listConnections( ( sg + '.surfaceShader' ) , s = True , d = False )
	    if not( shadersSG == None):
	        shaders.append(shadersSG[0]) 
	   	
	
	return shaders
	
#_____________________________________________________________________________________________________________________________________________________________________ getShadersOfObj 

def getShadersOfObj( elem ):
	
	'''
		find the shaders associated with on obj 
		obj must be one geometry but can containt an array of face
		if there is more than on shader, it sort the shaders by the most present to the less ( by the nbr of face )
	
	'''
	
	
	if( type(elem) == list ):
		obj , indexs = utilsPython.getObjNameAndIndexs( elem[0] )
		indexs = utilsPython.getArrayIndexsOfObjs( elem , obj )
		for e in elem:
			if not( obj in e ):
				mc.error(' input must be one elem or a list of component of ONE obj ')
	else:		
		obj , indexs = utilsPython.getObjNameAndIndexs( elem )
	
	if( mc.nodeType(obj) == 'mesh' ):	
		objShape = obj
	else:
		objShape = mc.listRelatives( obj , shapes = True , c = True )[0]	
	
	#get shaders of all the geometry
	
	objShadingEngines = mc.listConnections( objShape , s = False , d = True , type = 'shadingEngine' )
	
	objShadingEngines = list(set(objShadingEngines))
	
	objShaders = convertShaderEnginesToShaders( objShadingEngines )
	
	if( len( objShaders ) == 1 ):
		return objShaders 
	
	# filtre shaders with the indexs
	
	objShadingEnginesIFilter = []
	
	if( len( indexs ) == 0 ):
		objShadingEnginesIFilter = objShadingEngines		
	else:
		
		for sg in objShadingEngines:
	
			members = mc.sets( sg , q = True )
			sgIndexs = utilsPython.getArrayIndexsOfObjs(members , obj)
								
			for sgI in sgIndexs:
				if( sgI in indexs ):
					objShadingEnginesIFilter.append( sg )
					break
		
					
	# sort important shader	
	
	dicoSg      = {}
	nbrFaceList = []
	
	for sg in objShadingEnginesIFilter:			
		sgIndexs = []
		members = mc.sets( sg , q = True )
		sgIndexs = utilsPython.getArrayIndexsOfObjs(members , obj )
		
		if not( len( indexs ) == 0 ):
			sgIndexs = [ sgI for sgI in sgIndexs if sgI in indexs ]
	
		nbrFace = len(sgIndexs)
		nbrFaceList.append( nbrFace )		
		dicoSg[ sg ] = nbrFace
	
	nbrFaceList.sort()
	nbrFaceList.reverse()
	
	objShadingEnginesIFilterSort = []
	
	for nbr in nbrFaceList:
		for sg in objShadingEnginesIFilter:
			if( dicoSg[sg] == nbr ) and not( sg in objShadingEnginesIFilterSort):
				objShadingEnginesIFilterSort.append( sg )
	
	# convert to shader	
	
	shadersList = convertShaderEnginesToShaders( objShadingEnginesIFilterSort )	
	
	return shadersList
			
#_____________________________________________________________________________________________________________________________________________________________________ getObjsOfShader  

def getObjsOfShader( shader ):
	'''
		return all objs with the shader on it 
	'''
	
	shadingEngine = mc.listConnections( shader , s = False , d = True , type = 'shadingEngine' )	
	objs = mc.sets( shadingEngine[0] , q = True   )	
	
	return objs

#_____________________________________________________________________________________________________________________________________________________________________ getSimilarShaders  

def getSimilarShaders( shader , attrsToCheck = [ 'color' , 'transparency' , 'ambientColor' , 'incandescence' , 'diffuse' ]):
	
	'''
		get all the shaders of same type and same value on attibuts ( attrsToCheck ) than the given shader
		default attrsToCheck are the common material proprieties of many shaders
	'''	
	
	shadingEngines = mc.ls( type = 'shadingEngine')	
	sceneShaders = convertShaderEnginesToShaders( shadingEngines )
	
	shaderType = mc.nodeType(shader)
	
	sameShaders = []
	
	for sceneShader in sceneShaders:
		
		if not( mc.nodeType(sceneShader) == shaderType ) or( shader == sceneShader):
			continue
		
		same = 1
		for attr in attrsToCheck:
			refValue = mc.getAttr( shader      + '.' + attr ) 
			value    = mc.getAttr( sceneShader + '.' + attr )
			if not( refValue == value ):
				same = 0
				break
				
		if( same == 1 ):
			sameShaders.append(sceneShader)
	
	return sameShaders
	

#_____________________________________________________________________________________________________________________________________________________________________ setShaderToObj  

def setShaderToObj( shader , obj ):
	
	'''
		assigne given shader to obj, obj can be list 
	'''	
	saveSelection = mc.ls( sl = True )
		
	shadingEngine = mc.listConnections( shader , s = False , d = True , type = 'shadingEngine' )
	mc.select(obj)	
	mc.sets(  e = True , forceElement = shadingEngine[0]   )
	
	mc.select(saveSelection)
	
	return 1
		

#_____________________________________________________________________________________________________________________________________________________________________ cleanSceneDupliShader

def cleanSceneDupliShader():
	
	'''
		regroup the similar shader
	'''
	
	shadingEngines = mc.ls( type = 'shadingEngine')	
	sceneShaders = convertShaderEnginesToShaders( shadingEngines )
	
	
	remainShaders  = []
	deletedShaders = []	
	
	for shader in sceneShaders:
		
		if( shader in deletedShaders ):
			continue
			
		remainShaders.append(shader)
		
		similarShaders = getSimilarShaders( shader )
		
		for similarShader in similarShaders:
			objsToTransfere = getObjsOfShader( similarShader )
			setShaderToObj( shader , objsToTransfere )
			mc.delete( similarShader )
			deletedShaders.append(similarShader)
			
	
	print( 'cleanSceneDupliShade:  ===  {0} shader deleted ==='.format(len(deletedShaders)) )	
	
	return remainShaders 
			
			
#================================================================================================================================================================================================================================
#======================================================  CONSTRAINT  ============================================================================================================================================================
#================================================================================================================================================================================================================================


#_____________________________________________________________________________________________________________________________________________________________________ get Constraint Slaves	
	
def getConstraintSlaves( trsf , constraintTypesFilter = [ 'parentConstraint' , 'pointConstraint' ,'orientConstraint' ,'scaleConstraint' , 'aimConstraint' ] , deleteConstraint = 0 ):
	
	'''
		get the constraint slaves of an obj
		you can precise the constraint type wanted,  array needed
		you can ask to delete constraint on the fly 
	
	'''
	
	slaveTrsfs = []
		
	constraintes = mc.listConnections( trsf + '.parentMatrix[0]' , s = False , d = True )
		
	if( constraintes == None ):
	    return slaveTrsfs	
		    
	# type of constraint    	    
	matchTypeConstraintes = []
	
	for constrainte in constraintes:
	
		nType = mc.nodeType( constrainte )
		
		if nType in constraintTypesFilter :
			matchTypeConstraintes.append( constrainte )
							
	if( matchTypeConstraintes == None ):
	    return slaveTrsfs
		
	# name slave  		    
	    
	for matchTypeConstrainte in matchTypeConstraintes :
		slaveTrsf = mc.listConnections( matchTypeConstrainte + '.constraintParentInverseMatrix' , s = True , d = False ) 
		slaveTrsfs.append( slaveTrsf[0] )

	slaveTrsfs = list(set( slaveTrsfs ))	
		
	# delete constraint ?  		
	
	if( deleteConstraint == 1 ):
		mc.delete(matchTypeConstraintes)
                                                                                                                                

	return slaveTrsfs

	
#_____________________________________________________________________________________________________________________________________________________________________ getConstraintMasters


	
def getConstraintMasters( obj , constraintTypesFilter = [ 'parentConstraint' , 'pointConstraint' ,'orientConstraint' ,'scaleConstraint' , 'aimConstraint' ] , deleteConstraint = 0 ):
	
	'''
		get the constraint masters of an obj
		you can precise the constraint type wanted,  array needed
		you can ask to delete constraint on the fly 
	
	'''
	
	objMasters = []
		
	constraintes = mc.listConnections( ( obj + '.parentInverseMatrix[0]' ) , s = False , d = True )
		
	if( constraintes == None ):
	    return objMasters	
		    
	# type of constraint    	    
	matchTypeConstraintes = []
	
	for constrainte in constraintes:
	
		nType = mc.nodeType( constrainte )
		
		if nType in constraintTypesFilter :
			matchTypeConstraintes.append( constrainte )
							
	if( matchTypeConstraintes == None ):
	    return objMasters
		
	# name Masters  		    
	    
	for matchTypeConstrainte in matchTypeConstraintes :
		masters = mc.listConnections( ( matchTypeConstrainte + '.target[*].targetParentMatrix' ) , s = True , d = False )
		objMasters += masters

	objMasters = list(set( objMasters ))	
		
	# delete constraint ?  		
	
	if( deleteConstraint == 1 ):
		mc.delete(matchTypeConstraintes)
                                                                                                                                

	return objMasters	
	

#_____________________________________________________________________________________________________________________________________________________________________ buildConstraint	

def buildConstraint( objs , types , mode , maintainOffset , skipAttr = [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ] , clear = False ):

	'''
		build constraint between objs
		
		types    is an array of constraint type you want to build: 	constraintType = [ 'parent' , 'point' , 'orient' , 'scale' , 'aim' ]
		mode     is the way you want to constraint objs:  	modes = [ "normal" , "oneMaster" , "2by2" ];
		
				oneSlave   : the last obj of the list is constraint by all the other

				oneMaster: the first obj constraint all the other				

				2by2     : the first obj constraint the second , the third constraint the fourth , etc...						

		maintainOffset  0 or 1, if you want to activate maintaint offset of the constraint
		
		skipAttr = [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ] <<----- corresplond to tx ty tz rx ry rz sx sy sz
	'''
	#______ SKIP _______ DEBUT
	trsAttrs = ['.translateX','.translateY','.translateZ','.rotateX','.rotateY','.rotateZ','.scaleX','.scaleY','.scaleZ']
	dicoSkip = { 'parent' : '' , 'point' : '' , 'orient' : '' , 'scale' : ''  , 'aim' : '' }

	axesSkips = []
	for i in range( 0 , len(skipAttr) , 3 ):	
		axesSkip = []
		if( skipAttr[i]   ):axesSkip.append( 'x' )
		if( skipAttr[i+1] ):axesSkip.append( 'y' )		
		if( skipAttr[i+2] ):axesSkip.append( 'z' )				

		axesSkips.append(axesSkip)

	
	for cType in types:
		if( cType == 'point'      ): dicoSkip[cType] = ',sk=' + str( axesSkips[0] ) 
		if( cType == 'orient'     ): dicoSkip[cType] = ',sk=' + str( axesSkips[1] ) 
		if( cType == 'scale'      ): dicoSkip[cType] = ',sk=' + str( axesSkips[2] )		
		if( cType == 'aim'        ): dicoSkip[cType] = ',sk=' + str( axesSkips[1] ) 		
		if( cType == 'parent'     ): dicoSkip[cType] = ',st=' + str( axesSkips[0] ) + ',sr=' + str( axesSkips[1] ) 	
		if( cType == 'poleVector' ): dicoSkip[cType] = ''		

	#______ SKIP _______ FIN		
			
	modes = [ "oneSlave" , "oneMaster" , "2by2" ];

	maintainOffsetArg = ''
	if( maintainOffset == 1):
		maintainOffsetArg = ', mo = 1'
	
	if not( type( types ) == list ):
		types = [ types ]

	
	masters = []

	constraintsCreated = []
	
	for cType in types:

		if( mode == "oneSlave" ):
			masters = objs[0:-1]
			slave  = objs[-1]

			if(clear):
				if( skipAttr == [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ] ):
					sourcesConnections = mc.listConnections( slave , s = True , d = False , type = '{0}Constraint'.format(cType) )
					if not(sourcesConnections == None)and(0<len(sourcesConnections)):
						mc.delete(sourcesConnections)
				else:
					for j in range( 0 , len(trsAttrs) ):
						if( skipAttr[j] == 0 ):
							source = mc.listConnections( slave + trsAttrs[j] , s = True , p = True )
							if not( source == None ):
								mc.disconnectAttr( source[0] , slave + trsAttrs[j] )
			
			stringToEval = ( 'mc.{0}Constraint( ["{1}'.format( cType , masters[0] ) ) 		
			for i in range( 1 , len( masters) ):
				stringToEval += ( '","{0}'.format( masters[i]) )			
			stringToEval += ( '"] , "{0}" {1} {2})'.format( slave , maintainOffsetArg , dicoSkip[cType] )  )	 
			constraintsCreated += eval( stringToEval )
			
		elif( mode == "oneMaster" ):
   	
			master = objs[0] 
			slaves =  objs[1:len(objs)] 
			
			if(clear):
				if( skipAttr == [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ] ):
					for i in range( 0 , len(slaves)):
						sourcesConnections = mc.listConnections( slaves[i] , s = True , d = False , type = '{0}Constraint'.format(cType) )
						if not(sourcesConnections == None)and(0<len(sourcesConnections)):mc.delete(sourcesConnections)
				else:
					for i in range( 0 , len(slaves)):
						for j in range( 0 , len(trsAttrs) ):
							if( skipAttr[j] == 0 ):
								source = mc.listConnections( slaves[i] + trsAttrs[j] , s = True , p = True )
								if not( source == None ):
									mc.disconnectAttr( source[0] , slaves[i] + trsAttrs[j] )			

			for i in range( 0 , len(slaves)):
				print( 'mc.{0}Constraint( "{1}" , "{2}" {3} {4} )'.format( cType , master , slaves[i] , maintainOffsetArg , dicoSkip[cType] )  ) 
				constraintsCreated += eval( 'mc.{0}Constraint( "{1}" , "{2}" {3} {4} )'.format( cType , master , slaves[i] , maintainOffsetArg , dicoSkip[cType] )  )
				
			masters = [ master ]
			
			
		elif( mode == "2by2" ):
			
			if(clear):
				for i in range( 0 , len(objs) , 2 ):
					if not ( ( i + 1 ) == len(objs) ):
						sourcesConnections = mc.listConnections( objs[i+1] , s = True , d = False , type = '{0}Constraint'.format(cType) )
						if not(sourcesConnections == None)and(0<len(sourcesConnections)):mc.delete(sourcesConnections)


			for i in range( 0 , len(objs) , 2 ):
				if not ( ( i + 1 ) == len(objs) ):
					constraintsCreated += eval( 'mc.{0}Constraint( "{1}" , "{2}" {3} {4} )'.format( cType , objs[i] , objs[i+1] , maintainOffsetArg , dicoSkip[cType]  ))
					masters.append(objs[i])
						

	return constraintsCreated



def buildConstraintSpace( objs , types , skipAttr = [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ] ):

	'''
	 ======================================= OLD =======================================
	 ------------> buildSpacesSwitch
	'''

	constraintTypes = []
	for type in types:
		constraintTypes.append( type.split('Space')[0] )

	slave   = objs[-1] 
	#CHECK CONSTRAINT
	constraintBase = mc.listConnections( ( slave + '.parentInverseMatrix[0]' ) , s = False , d = True )
	
	maxWeight = 0
	weightAttrBase = []
	if not(constraintBase == None ):
		attrsTmp = mc.listAttr( constraintBase[0] , k = True )
		weightNbr = []
		for attr in attrsTmp:
			if( 'W' in attr ):
				try: 
				    weightNbr.append( int( attr.split('W')[1] ) )
				    weightAttrBase.append(attr)
				except: pass
		
		weightNbr.sort()
		maxWeight = weightNbr[-1] + 1	            
	            
	#BUILD CONSTRAINT
	masters = objs[0:-1]
	buildConstraint( objs , constraintTypes , 'oneSlave' , 1 , skipAttr )
	constraint = mc.listConnections( ( slave + '.parentInverseMatrix[0]' ) , s = False , d = True )[0]

	#GET NEXT CTRL
	children = slave
	i = 0
	iMax = 500
	while not( '_CTRL' in children ):
		print( '-----' + children )
		childrens = mc.listRelatives( children , c = True , type = 'transform' )
		if( childrens == None ):
			children = slave
			break
		children = childrens[0]
		i+=1

		if( iMax < i ):
			mc.error('mayaUtils.buildConstraintSpace LOOP error')

	ctrl = children

	#BUILD ATTR
	
	attrExists = mc.objExists(ctrl + '.parentSpace') 
	enumStrBase = 'None'
	if( attrExists ):
	    enumStrBase = mc.addAttr( ctrl + '.parentSpace' , q = True , en = True  )
	
	enumStr = '{}:{}:'.format( enumStrBase , ':'.join(masters) )
	
	if( attrExists ):
	     mc.addAttr( ctrl + '.parentSpace' , e = True , en = enumStr  )
	else:
	    mc.addAttr( ctrl   , ln = 'parentSpace' , at = "enum"  , en = enumStr , dv = 0 )
	    mc.setAttr( ( ctrl + '.parentSpace' ) , e = True , keyable = False , cb = True )

	#BUILD CONNECTIONS
	if not( attrExists ):
		for i in range( 0 , maxWeight ):
			condition = mc.createNode('condition')
			mc.connectAttr( ( ctrl + '.parentSpace' ) , ( condition + '.firstTerm') )
	
			mc.setAttr(( condition + '.secondTerm' ), 0 )
			mc.setAttr(( condition + '.operation' ), 0 ) #is equal
			mc.setAttr(( condition + '.colorIfTrueR' ), 1 )
			mc.setAttr(( condition + '.colorIfFalseR' ), 0 )
	
			mc.connectAttr( ( condition + ".outColorR") ,  '{}.{}'.format(constraint,weightAttrBase[i])  )
		
	
	valueOffset = len(enumStrBase.split(':'))
	
	for i in range( 0 , len(masters) ):
		condition = mc.createNode('condition')
		mc.connectAttr( ( ctrl + '.parentSpace' ) , ( condition + '.firstTerm') )

		mc.setAttr(( condition + '.secondTerm' ), i + valueOffset )
		mc.setAttr(( condition + '.operation' ), 0 ) #is equal
		mc.setAttr(( condition + '.colorIfTrueR' ), 1 )
		mc.setAttr(( condition + '.colorIfFalseR' ), 0 )

		mc.connectAttr( ( condition + ".outColorR") ,  '{}.{}W{}'.format(constraint,masters[i],i+maxWeight)  )
		

def buildSdkPositionSwitch( trsArray , slave , driverAttr , offsetValueDriver = 0 ):
	trsAttrs = ['tx','ty','tz','rx','ry','rz','sx','sy','sz']
	for i in range( 0 , len(trsArray) ):
		for j in range( 0 , len(trsArray[i]) ):
			sdk = mc.listConnections( '{}.{}'.format(slave,trsAttrs[j]) , s = True , d = False )
			print( '{}.{}'.format(slave,trsAttrs[j]) , sdk , driverAttr )
			if( sdk == None ):
				mc.setDrivenKeyframe( '{}.{}'.format(slave,trsAttrs[j]) , cd = driverAttr , v = trsArray[i][j] , dv = i + offsetValueDriver ) 
			else:
				mc.setDrivenKeyframe( '{}.{}'.format(slave,trsAttrs[j]) , v = trsArray[i][j] , dv = i + offsetValueDriver ) 



def constraintGetMasters( parentConstraint ):
	
	masters = []
	for i in range(0,99):
	 	attr = '{}.target[{}].targetParentMatrix'.format(parentConstraint,i)
	 	inConnections = mc.listConnections(  attr , s = True , d = False, type = 'transform'  )
	 	if(inConnections==None):break
	 	else:                   masters += inConnections

	return masters



def buildSpacesSwitch( AttrSource , AttrDestination , connectionType , spaceDriver , spaceAttr , spaceNames , spaceValue , skipAxes , maintainOffset ):
	baseAttrs = ['.translateX','.translateY','.translateZ','.rotateX','.rotateY','.rotateZ']

	#GET VALUE
	masters           = AttrSource
	slave             = AttrDestination[0]
	slaveParent       = mc.listRelatives( slave , p = True , fullPath = True )
	attrDriver        = spaceDriver + '.' + spaceAttr
	constraintType    = connectionType[0].split('Space')[0]
	skipAxes          = [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ]

	
	#OVERRIDE IF CONSTRAINT == ORIENT
	saveValues = []
	if( constraintType == 'orient' ): 
		constraintType = 'parent'
		skipAxes = [ 1 , 1 , 1 , 0 , 0 , 0 , 0 , 0 , 0 ]
		for i in range( 0 , len(baseAttrs) ):
			saveValues.append( mc.getAttr( slave + baseAttrs[i] ) )		

	#IF CONSTRAINT ALREADY EXISTS - GET WEIGHT
	oldConstraintWeights = []

	oldConstraints = mc.listConnections( ( slave + '.parentInverseMatrix[0]' ) , s = False , d = True , type = ( constraintType + "Constraint" )  )
	if not(oldConstraints == None ): 
		oldConstraintWeights = constraintExtractWeightAttrs(oldConstraints[0])
		oldConstraintMasters = constraintGetMasters(oldConstraints[0])


	noneOffset = 0
	if( len(oldConstraintWeights) == 0): noneOffset = 1
	

	#BUILD ATTR
	if not( mc.objExists(attrDriver) ):
		#CREATE ATTR
		if( spaceNames == None ): mc.addAttr( spaceDriver , ln = spaceAttr , at = "long" , dv = 0 )
		else:                     mc.addAttr( spaceDriver , ln = spaceAttr , at = "enum" , dv = 0  , en = '{}:{}:'.format('None',':'.join(spaceNames))    )
		mc.setAttr( attrDriver  , e = True , keyable = False , cb = True )
		#SET ATTR
		if not( spaceValue == None ):
			mc.setAttr( attrDriver , spaceValue+1 )
	else:
		#EDIT ATTR
		if( spaceNames == None ):
			pass
		else:
			oldAttrEnumValue = mc.addAttr( attrDriver , q = True , en = True  )
			mc.addAttr( attrDriver , e = True , en = '{}:{}:'.format( oldAttrEnumValue , ':'.join(spaceNames) )  )		

	attrRangeLength = getAttrRangeLength(attrDriver)

	#BUILD CONSTRAINT OR SDK SWITCH
	if( type(masters[0]) == types.StringType ):

		#BUILD CONSTRAINT
		if not( slaveParent == None ):
			if( len(oldConstraintWeights) == 0 ): # if its a new attr
				if not( attrRangeLength == len(masters) ):
					masters = slaveParent + masters


		constraint = buildConstraint( masters + [ slave ] , [constraintType] , 'oneSlave' , 1 , skipAxes )[0]

		### SAVE VALUE ###
		if not( len(oldConstraintWeights) == 0 ): # if its an update
			if not( saveValues == [] ):# if its an orient cns
				#PUT saved value
				for i in range( 0 , len(baseAttrs) ):
					mc.setAttr( slave + baseAttrs[i] , saveValues[i] )
				#REBUILD OLD CNS WITHOUT ROTATE
				buildConstraint( oldConstraintMasters + [ slave ] , ['parent'] , 'oneSlave' , 1 , [0,0,0,1,1,1,0,0,0] )


		#BUILD CONNECTIONS
		constraintWeights = constraintExtractWeightAttrs(constraint)
		for i in range( 0 , len(constraintWeights) ):
			conditionOnOffEqual( attrDriver , i , '{}.{}'.format(constraint,constraintWeights[i]) )

		
		# allow multiple parentspace on the same ctrl
		attrs = ['TranslateX','TranslateY','TranslateZ','RotateX','RotateY','RotateZ']

		attrTmp = '{}.{}{}{}'.format( spaceDriver , spaceAttr , 0 , attrs[0] ) 
		if( mc.objExists( attrTmp ) ):
			for char in string.ascii_uppercase: 
				attrTmp = '{}.{}{}{}{}'.format( spaceDriver , spaceAttr , char , 0 , attrs[0] ) 
				if not( mc.objExists(attrTmp) ):
					spaceAttr += char
					break

		#BUILD ATTR OFFSET
		for i in range( 0 , len(constraintWeights) ):
			for j in range( 0 , len(attrs) ):

				#NAMES
				ctrlAttr      = '{}{}{}'.format( spaceAttr , i , attrs[j] )
				ctrlAttrBase  = ctrlAttr + 'Base'
				#GET VALUE
				cnsAttr       = '{}.target[{}].targetOffset{}'.format( constraint , i , attrs[j] )
				#BUILD ATTR BASE
				obj         = spaceDriver
				attr        = ctrlAttrBase
				objAttrBase = '{}.{}'.format(obj,attr)
				mc.addAttr(  obj         , ln = attr , at = "double" , dv = mc.getAttr(cnsAttr) )
				mc.setAttr(  objAttrBase , e = True , keyable = False , cb = False , lock = True )
				#BUILD ATTR
				obj     = spaceDriver
				attr    = ctrlAttr
				objAttr = '{}.{}'.format(obj,attr)
				mc.addAttr(  obj     , ln = attr , at = "double" , dv = 0 )
				mc.setAttr(  objAttr , e = True , keyable = True , cb = True , lock = False )
				#BUILD CONNECTIONS
				addNode = mc.createNode('addDoubleLinear')
				mc.connectAttr(objAttrBase                 , '{}.input1'.format(addNode) )
				mc.connectAttr(objAttr                     , '{}.input2'.format(addNode) )	
				mc.connectAttr('{}.output'.format(addNode) , cnsAttr                     )			
				



	else:
		ValueTrs = trs()
		ValueTrs.createFromObj(slave, worldSpace = False)
		positions = [ ValueTrs.value ] + maters 
		buildSdkPositionSwitch( positions , slave , attrDriver , len(oldConstraintWeights) )
			



def constraintExtractWeightAttrs( constraint ):
    weightAttrs = []
    attrs = mc.listAttr( constraint , k = True )
    for attr in attrs:
        if( 'W' in attr ):
            try:
                num = int(attr.split('W')[1])
                weightAttrs.append(attr)
            except:
            	pass

    return weightAttrs


def conditionOnOffEqual( inA  , inB , out ):
	condition = mc.createNode('condition')
	mc.setAttr(( condition + '.operation' ), 0 ) #is equal
	mc.setAttr(( condition + '.colorIfTrueR' ), 1 )
	mc.setAttr(( condition + '.colorIfFalseR' ), 0 )

	if( type(inA) == types.StringType ): mc.connectAttr(        inA               , (condition+'.firstTerm') )
	else:                                mc.setAttr(     (condition+'.firstTerm') , inA                      )

	if( type(inB) == types.StringType ): mc.connectAttr(        inB               , (condition+'.secondTerm') )
	else:                                mc.setAttr(     (condition+'.secondTerm') , inB                      )

	mc.connectAttr( ( condition + ".outColorR") ,  out )

	return condition
			



#__________________________________________________________________________________________________________________________________________________________________________________________ resetConstraints						

def resetConstraint( obj ):
	
	'''
		set to 0 the value ( translate , rotate ) under constraint. ( 1 for scale )

	'''

	
	attrs =  [ 'translate' , 'rotate' ] 
	axes  =  [ 'X','Y','Z' ]
	
	constraintTypes = [ 'parent' , 'point' , 'orient' , 'scale' , 'aim' ]
	dicoAttrName    = { 'parent' : [ 'translate' , 'rotate' ] , 'point' : ['translate'] , 'orient' : ['rotate'] , 'scale' : ['scale'] , 'aim' : ['rotate'] } 
	dicoAttrValue   = { 'parent' : 0                          , 'point' : 0             , 'orient' : 0          , 'scale' : 1         , 'aim' : 1          }
	
	objConstraints = []
	
	for cType in constraintTypes:
		masters = getConstraintMasters( obj , [ cType + 'Constraint' ] , 1 )
		
		if( masters == [] ):
			continue

	   	for axe in axes :
	   	    for attr in dicoAttrName[cType] :
	   	    	mc.setAttr( ( obj + '.' + attr + axe ) , dicoAttrValue[cType] )  		

	   	if( len(masters) > 1 ):
			buildConstraint( ( masters + [ obj ] ) , [ cType ] , 'normal'    , 1 )
		else:
			buildConstraint( ( masters + [ obj ] ) , [ cType ] , 'oneMaster' , 1 )			
		
		
	    
	return 1
	
#__________________________________________________________________________________________________________________________________________________________________________________________ buildConstraintProximity			
def buildConstraintProximity( masters , slaves , types = [ 'parent' , 'scale' ] , maintainOffset = 1 , skipAttr = [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ] ):
		
	objs = sortObjWithHisClosestOne( masters , slaves )
	buildConstraint( objs , types , '2by2' , maintainOffset , skipAttr )


	
	
	
#================================================================================================================================================================================================================================
#======================================================  BUILD BASE  ============================================================================================================================================================
#================================================================================================================================================================================================================================

#__________________________________________________________________________________________________________________________________________________________________________________________ buildCurveShape		



def buildCurveShape( transformName , shapeName , coords , degree , colorIndex , position = None , trsOffset = None  , worldSpace = True ):		
	'''
		CVs  = Spans + Degree
		Knot = CVs   + Degree -1
	'''
	Coords = coordsClasse.coords()		
	Coords.createFromCoords( coords )

	#OFFSET POSITION			
	if not( position == None ):
		Coords.offset( position , [ 0 , 0 , 0 ] , 'XYZ')

	if not( trsOffset == None ):
		Coords.offset( trsOffset , [ 0 , 0 , 0 ] , 'XYZ')

	#GET KNOT INDEXES
	knot = getKnotIndexes( Coords.coords , degree )
			
	#BUILD 
	nameTmp   = 'curveManip_Tmp'	
	mc.curve( n = nameTmp , d = degree , p = Coords.points , k = knot )
	curveShape = mc.listRelatives( nameTmp , c = 1 , s = 1 )

	if( mc.objExists( transformName ) == 0 ):
		mc.createNode( 'transform' , n = transformName )

	mc.parent( curveShape[0] , transformName , s = True , r = True ) 
	mc.delete( nameTmp )

	#SET COORDS SPACE
	Coords.toObj( curveShape[0], worldSpace )

	#COLOR
	mc.setAttr( ( curveShape[0] + ".overrideEnabled" ) , 1 )
	mc.setAttr( ( curveShape[0] + ".overrideColor" )   , colorIndex )

	#RENAME	
	reelshapeName = curveShape[0]
	if not( shapeName == 'None'):
		if('|' in shapeName ): shapeName = shapeName.split('|')[-1]
		reelshapeName = mc.rename( reelshapeName , shapeName )

	return reelshapeName         


def getKnotIndexes( coords , degree ):

	nbrKnot = len(coords)/3 + degree - 1  		#_knot	= spans + 2 degree - 1	degree first knot identical    and   degree las knot identical	
	
	knot = []
	for i in range( 0 , degree ):
		knot.append(0)
		
	for i in range( degree , nbrKnot - degree):
		knot.append(i)
			
	for i in range( 0 , degree ):
		knot.append(nbrKnot - degree)

	return knot




	

def buildCurveShapeOld( transformName , shapeName , formCurve , colorName , shapeAxe = 'X' , trsPosition = None ):
	
	'''
	
		build a curve shape under transform node,
		formCurve   -  you can choose the form of the curve, here is some exemple: ['arrow' , 'arrow2Sides' , 'arrow2SidesBend' , 'cross' , 'crossArrow' , 'crossArrowBend' , 'circle' , 'cube' , 'cylinder' , 'loc' , 'oeil' , 'plane' , 'smiley' , 'sphere' ]
		colorName   -  choose the color :     blue    red   yellow    or you can give an index
		shapeAxe    -  the orientation plane of the curve,   here is the perpendicular plane to X
		trsPosition -  Position in space of the curve. by default is snap to the tansform. but at [ 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1 ] it's at the center of the world
	
		it return the name of the shape
	'''
	#_1 get form info	

		
	formBank = utilsBin.curveFormBank()	
	pos    = formBank.getFormCoords(formCurve)
	degree = formBank.getFormDegree(formCurve)
					                                               
	#_2 modif axe plane	
	
	if(   shapeAxe == 'X' ):
		pos = utilsMath.transformCoords( pos , [ 0 , 0 , 0 ]  , [ 0 , 0 , 0 , 0  , 0 , 90 , 1 , 1 , 1 ] , 'XYZ' )							
	elif( shapeAxe == 'Z' ):
		pos = utilsMath.transformCoords( pos , [ 0 , 0 , 0 ]  , [ 0 , 0 , 0 , 90 , 0 , 0  , 1 , 1 , 1 ] , 'XYZ' )			


	reelshapeName = buildCurveShapeWithCoords( transformName , shapeName , pos , degree , colorName , trsPosition )
	
	return reelshapeName         

	
	
	
	
#__________________________________________________________________________________________________________________________________________________________________________________________ buildCurveShapeWithCoords	
	
def buildCurveShapeWithCoords( transformName , shapeName , coords , degree , colorName , trsPosition = None  ):
	
	'''
		CVs  = Spans + Degree
		Knot = CVs   + Degree -1
	
	'''
	pos = coords	
							

	#_knot	= spans + 2 degree - 1	 // degree first knot identical    and   degree las knot identical
	
	knot = []
	nbrKnot = len(pos) + degree - 1 	
	
	for i in range( 0 , degree ):
		knot.append(0)
		
	for i in range( degree , nbrKnot - degree):
		knot.append(i)
			
	for i in range( 0 , degree ):
		knot.append(nbrKnot - degree)
	
		
	#_4 build shape 
	
	nameTmp   = 'curveManip_Tmp'	
	mc.curve( n = nameTmp , d = degree , p = pos , k = knot )

	curveShape = mc.listRelatives( nameTmp , c = 1 , s = 1 )
	mc.parent( curveShape[0] , transformName , s = True , r = True ) 
	mc.delete( nameTmp )	

	#_3 modif position

	newCurveShape = mc.listRelatives( transformName , c = 1 , s = 1 )		
	
	if not( trsPosition == None ):
		pos  = utilsMath.transformCoords( pos , [ 0 , 0 , 0 ]  , trsPosition , 'XYZ' )  				
		for i in range(0 , len(pos) ):
			mc.xform( newCurveShape[0] + '.cv[{0}]'.format(i) , t = pos[i] , ws = True  )
	

	
	#_5 change color
	
	dicoColorIndex = { 'red' : 13 , 'green' : 14 , 'blue' : 6 , 'yellow' : 17 , 'cyan' : 19 , 'violet' : 9 , 'black' : 1  }	
	
	mc.setAttr( ( curveShape[0] + ".overrideEnabled" ) , 1      )

	if( type( colorName ) == int ):	
		mc.setAttr( ( curveShape[0] + ".overrideColor" )   , colorName)
	else:
		mc.setAttr( ( curveShape[0] + ".overrideColor" )   , dicoColorIndex[ colorName ] )
		
	#_6 rename
	
	reelshapeName = mc.rename( curveShape[0] , shapeName )

	return reelshapeName         
		

#__________________________________________________________________________________________________________________________________________________________________________________________ createDagNodes		
	
def createDagNodes( types , names , fathers , trs = None ):
	
	'''
		create dag node and take care of shape. mean that if a shape is created, the transform node above is automaticaly rename with the right name.
	'''

	indexSorted = utilsPython.sortIndexChildrensByHierarchy( names , fathers )
	
	nodes = []
	
	selection = mc.ls(sl=True)
	trsObj = trsClass.trs()
	
	for i in indexSorted:
		mc.select( cl = True )
		rawName = mc.createNode( types[i] )				
		transformNode = mc.listRelatives( rawName , p = True  )
		
		if( transformNode == None):
		    mc.rename( rawName , names[i] )
		    		    
		    if(  types[i] == 'joint'  ) and not ( fathers[i] == ''  ) and not ( trs == None ) :
		    			    	
		    	trsFather = trsObj.createFromObj( fathers[i] )
		    	trsObj.value = trs[i]
		    	trsObj.parent( trsFather )
		    	
		    	mc.parent( names[i] , fathers[i] )
		    	trsObj.toObj(names[i])
		    	mc.joint( names[i] , e = True , o = [ 0 , 0 , 0 ] )
		    
		    else:	
	    			    		
		    	if not( fathers[i] == '' ):
		    		mc.parent( names[i] , fathers[i] )	

		    	if not( trs == None ):
		    		trsObj.toObj( names[i] , worldSpace = 0 , inValue = trs[i] )

		    		    			    			    	
		    	
		else:
			
		    mc.rename( transformNode , names[i] )
   
		    if not( fathers[i] == '' ):
		    	mc.parent( names[i] , fathers[i] )

		    if not( trs == None ):
		    	trsObj.toObj( names[i] , worldSpace = 0 , inValue = trs[i] )
	
	mc.select(selection)
	return names
	                                                        
#__________________________________________________________________________________________________________________________________________________________________________________________ createSets	



'''
names    = [ 'A' , 'B' , 'C'  ]
parents  = [ ''  , 'A' , 'A'  ] 
contents = [ ['pCube1' , 'pCube2']  ,[] , ['pCube3']  ] 
createSets( names , parents , contents )
'''

def createSets( names , parents , contents ):

	indexSorted = utilsPython.sortIndexChildrensByHierarchy( names , parents )
	selection = mc.ls(sl=True)

	#BUILD
	mc.select( cl = True );
	for i in indexSorted:
		mc.sets( n = names[i] )
		mc.select( cl = True );

	#PARENT SETS
	for i in indexSorted:
		if not( parents[i] == '' ):
			mc.sets(names[i] , add = parents[i] )
			mc.select( cl = True );

	#ADD CONTENT
	for i in indexSorted:
		if( 0 < len(contents[i]) ):
			for content in contents[i]:
				mc.sets(content, add = names[i] )
				mc.select( cl = True );

	mc.select( selection );
	return names
		                                                                                                                                                                                                                                               
#__________________________________________________________________________________________________________________________________________________________________________________________ buildManipBase		
	
def buildManipBase( baseName , jointExist = 1 , mutliOrigExist = 0 ):
	'''
		create the base of a manip ( without the shape ) orig ---> ( multiOrig ?) --> ctrl ---> ( joint ?)
		
		if the baseName already exist, it automatiquely increment
		return the created objs

	'''	
	
	
	types   = [ 'transform'        , 'transform'         ]
	names   = [ baseName + '_orig' , baseName + '_ctrl'  ]
	parents = [ ''                 , names[0]            ]
	
	if( jointExist == 1 ):
		types      += [ 'joint' ]
		names      += [ baseName + '_skn' ]
		parents    += [ names[1] ]

	if( mutliOrigExist == 1 ):
		types      += [ 'transform' ]
		names      += [ baseName + '_multiOrig' ]
		parents    += [ names[0] ]		
		parents[1]  =  names[len(names)-1]  		
		
	names = createDagNodes( types , names , parents )
	
	
	if( jointExist == 1 ):		
		mc.setAttr( ( names[2]      +'.radius' ),  0.01   )
	
	addSpecialAttrExtend( names[1] , 'object_display' , 'intOnOff' )				

	return names 

	
#__________________________________________________________________________________________________________________________________________________________________________________________ buildOrig	
	
	
def buildOrig( obj ):
	
	'''
		create an orig father of obj
		it takes all obj's values, so obj became clean
		if obj is already a child, orig is place between him and his father
		if orig already exist it replace by orig1 then orig2 orig3....
	
	'''
		
	baseName = utilsPython.getObjBaseName( obj , 1 , 0 )
	
	orig = baseName + '_orig'
	
	i = 1
	while( mc.objExists( orig ) ):
		orig = baseName + '_orig' + str(i)
		i += 1
		if( i == 3000 ):
			mc.error('loop')
				
	mc.createNode( 'transform' , n = orig )
	mc.delete( mc.parentConstraint( obj , orig ) )	
	
	objParent = mc.listRelatives( obj , p = True )
	
	if not( objParent == None ):
		mc.parent( orig , objParent )
		
	mc.parent( obj , orig )

	# sometimes obj have value on translate and in local rotate pivot
	# in that case we must freeze transform the translate
	
	localRotatePivot = mc.getAttr( obj + '.rotatePivot' )
	if not( localRotatePivot == [0,0,0] ):
		mc.makeIdentity( obj , a = True , t = True )

	
	return orig	
	

	

		
	
#================================================================================================================================================================================================================================
#======================================================  BUILD RIG   ============================================================================================================================================================
#================================================================================================================================================================================================================================

#__________________________________________________________________________________________________________________________________________________________________________________________ buildDistDimensionSys		
'''	
def buildDistDimensionSys( baseName , inputA , inputB , attrOut  ):
	
	
		#create distance dimention in his own group baseName_grp ( this name is return )
		#a simple parent constraint is create to link inputA/B to the loc of the distance dimention created
		
	
	allGrp = baseName + '_grp'
	
	if( mc.objExists( allGrp ) ):
		mc.error( 'systeme already exist !' )
		
	ddSysNames   = [ allGrp      , baseName + '_distanceDimension' , baseName + 'A_loc' , baseName + 'B_loc' ]
	ddSysTypes   = [ 'transform' , "distanceDimShape"              , 'locator'          , 'locator'          ]
	ddSysParents = [ ''          , allGrp                          , allGrp             , allGrp             ]
	
	
	newNodes = createDagNodes( ddSysTypes , ddSysNames , ddSysParents )
	
	ddShape   = mc.listRelatives( ddSysNames[1] , s = True )
	locAShape = mc.listRelatives( ddSysNames[2] , s = True )
	locBShape = mc.listRelatives( ddSysNames[3] , s = True )
	
	mc.connectAttr( ( locAShape[0] + '.worldPosition' ) , ( ddShape[0] + '.startPoint' ) )
	mc.connectAttr( ( locBShape[0] + '.worldPosition' ) , ( ddShape[0] + '.endPoint' )   )
		
	mc.parentConstraint( inputA , ddSysNames[2] ) 
	mc.parentConstraint( inputB , ddSysNames[3] )
	
	mc.connectAttr( ( ddSysNames[1] + '.distance' ) , attrOut )
	
	return allGrp 
'''


def buildDistDimensionSys( baseName , inputA , inputB , attrOut  ):
	
	'''
		create distance dimention in his own group baseName_grp ( this name is return )
		a simple parent constraint is create to link inputA/B to the loc of the distance dimention created
	'''	

	allGrp = baseName + '_grp'
	
	if( mc.objExists( allGrp ) ):
		mc.error( 'systeme already exist !' )
		
	ddSysNames   = [ allGrp      , baseName + '_distanceDimension' , baseName + 'A_loc' , baseName + 'B_loc' ]
	ddSysTypes   = [ 'transform' , "distanceDimShape"              , 'locator'          , 'locator'          ]
	ddSysParents = [ ''          , allGrp                          , allGrp             , allGrp             ]
	
	
	newNodes = createDagNodes( ddSysTypes , ddSysNames , ddSysParents )

	
	ddShape   = mc.listRelatives( ddSysNames[1] , s = True )
	locAShape = mc.listRelatives( ddSysNames[2] , s = True )
	locBShape = mc.listRelatives( ddSysNames[3] , s = True )
	
	mc.connectAttr( ( locAShape[0] + '.worldPosition' ) , ( ddShape[0] + '.startPoint' ) )
	mc.connectAttr( ( locBShape[0] + '.worldPosition' ) , ( ddShape[0] + '.endPoint' )   )
		
	mc.parentConstraint( inputA , ddSysNames[2] ) 
	mc.parentConstraint( inputB , ddSysNames[3] )
	
	mc.connectAttr( ( ddSysNames[1] + '.distance' ) , attrOut )
	
	return ddSysNames 

	


def buildDistanceNode( distanceNode , inObjA , inObjB , parent = None , outAttrDistance = None , inOutAttrsStretch = []  ):
	
	#CREATE
	distanceShape = mc.createNode( "distanceDimShape" )
	distanceTrsf  = mc.listRelatives( distanceShape , p = True )[0]

	#RENAME
	if not( distanceNode in [ None , '' ] ):
		mc.rename( distanceTrsf , distanceNode )
		distanceTrsf   = distanceNode
		distanceShape  = mc.listRelatives( distanceNode , s = True )[0]

	#SET IN
	safeParent( distanceTrsf , parent )
	decompMatrixNodeA = mc.createNode("decomposeMatrix")
	decompMatrixNodeB = mc.createNode("decomposeMatrix")

	mc.connectAttr( inObjA + '.worldMatrix[0]' , decompMatrixNodeA + '.inputMatrix' )
	mc.connectAttr( inObjB + '.worldMatrix[0]' , decompMatrixNodeB + '.inputMatrix' )

	mc.connectAttr( decompMatrixNodeA + '.outputTranslate' , distanceShape + '.startPoint' )
	mc.connectAttr( decompMatrixNodeB + '.outputTranslate' , distanceShape + '.endPoint' )
	
	#SET PROCESS
	objAttrOut        = addSpecialAttr( distanceTrsf , 'out'        , 'float' , 1 , attrKeyable = True , attrCb  = True , attrLock  =  False )
	objAttrInTarget   = addSpecialAttr( distanceTrsf , 'inTarget'   , 'float' , 0 , attrKeyable = True , attrCb  = True , attrLock  =  False )
	objAttrOutDelta   = addSpecialAttr( distanceTrsf , 'outDelta'   , 'float' , 1 , attrKeyable = True , attrCb  = True , attrLock  =  False )	
	objAttrInBase     = addSpecialAttr( distanceTrsf , 'inBase'     , 'float' , 1 , attrKeyable = True , attrCb  = True , attrLock  =  False )
	objAttrOutStretch = addSpecialAttr( distanceTrsf , 'outStretch' , 'float' , 1 , attrKeyable = True , attrCb  = True , attrLock  =  False )

	mc.connectAttr( distanceShape + '.distance' , objAttrOut )
	buildNodeOperations( [ objAttrOut , "-" , objAttrInTarget , "=" , objAttrOutDelta , "/" , objAttrInBase , "=" , objAttrOutStretch ] )
	
	#SET OUT
	if not( outAttrDistance == None ):
		mc.connectAttr( objAttrOut , outAttrDistance )
	
	if not( inOutAttrsStretch == [] ):
		mc.connectAttr( inOutAttrsStretch[0] , objAttrInBase        )
		mc.connectAttr( objAttrOutStretch    , inOutAttrsStretch[1] )

	#SET DISTANCE BASE
	posA = mc.xform( inObjA , q = True , t = True , ws = True )
	posB = mc.xform( inObjB , q = True , t = True , ws = True )
	dist = om.MVector( posB[0] - posA[0] , posB[1] - posA[1] , posB[2] - posA[2] ).length()
	mc.setAttr( inOutAttrsStretch[0] , dist )


	return distanceNode



#__________________________________________________________________________________________________________________________________________________________________________________________ createLocsOnCoords	



def createLocsOnCoords( baseName , coords ):
	
	'''
		simply create locators on Coords of type [ [ 0 , 0 , 0 ] , [ 1 , 1 , 1 ]  ]
		Place them into a group
		
		with a systeme of incremetation
	
	'''
	
	#coords[x][3]

	axes       = [ 'X' , 'Y' , 'Z' ]
	baseName = incrBaseNameIfExist( baseName , [''] , ['_grp'])	

	locGrpName = ( baseName + '_grp')
	locGrp     = mc.createNode( 'transform' , n = locGrpName )

	locs       = []
	
	for coord in coords:
		baseNameModif = incrBaseNameIfExist( baseName , [''] , ['_loc'])		
		loc = mc.spaceLocator( n = ( baseNameModif + '_loc') )
		locs.append( loc[0] )
		for i in range( 0 , 3 ):
			mc.setAttr( ( loc[0] + '.translate' + axes[i] ) , coord[i] )
		
	mc.parent( locs , locGrp )
	
	return locs
		

#__________________________________________________________________________________________________________________________________________________________________________________________ createLocsOnCoords	

def buildLocators( coords ):
	axis = ['X','Y','Z']
	grp = mc.createNode("transform" , n = "locs_GRP")
	for i in range(0,len(coords),3):
		loc = mc.spaceLocator()
		for j in range(0,len(axis)):
			mc.setAttr( ( loc[0] + '.translate' + axis[j] ) , coords[i+j] )
		mc.parent( loc , grp )




def buildSimpleLoc( baseName , trsValue ):
	
	baseName = incrBaseNameIfExist( baseName , [''] ,['_loc'] )
	locName = baseName + '_loc'
	loc = mc.spaceLocator( n = locName )
	setTRSValueToObj( loc[0] , trsValue )

	return locName	



def snapLocatorSelection():
	
	selection = mc.ls(sl = True)

	locs = []
	for elem in selection:
		#CREATE
		loc = mc.spaceLocator( n = 'pos_' + elem )[0]
		#SNAP
		mc.delete( mc.parentConstraint(elem,loc) )
		#SCALE
		bbCoords = mc.xform( elem, q = True , bb = True )
		bbDists = [ bbCoords[3] - bbCoords[0] , bbCoords[4] - bbCoords[1]  , bbCoords[5] - bbCoords[2]  ]
		bbDists.sort()
		mc.setAttr( loc + '.scaleX' , bbDists[-1] )
		mc.setAttr( loc + '.scaleY' , bbDists[-1] )
		mc.setAttr( loc + '.scaleZ' , bbDists[-1] )
		#COLOR
		mc.setAttr( loc + '.overrideEnabled' , 1 )
		color = mc.getAttr( elem + '.overrideColor')
		if( color == 0 ):
		    shape = mc.listRelatives(elem , s = True , c = True )
		    if( 0 < len(shape) ):
		        color = mc.getAttr( shape[0] + '.overrideColor')
		mc.setAttr( loc + '.overrideColor' , color )
		#STORE
		locs.append(loc)

	return locs

	
#__________________________________________________________________________________________________________________________________________________________________________________________ createAllConstraintGrp

def createAllConstraintGrp():
	
	rootCtrl  = 'RIG:root'
	grpParent = 'RIG:ADDITIVE_RIG'
	grpName   = 'all_rootConstrain_grp'
	
	
	if( mc.objExists( grpName ) ):
		return grpName	
	
	mc.createNode( 'transform' , n = grpName )
	
	if( mc.objExists( grpParent ) ):
		mc.parent( grpName , grpParent )
			
	if( mc.objExists( rootCtrl ) ):
		contraintManipToSlaves( rootCtrl , [ grpName ] )	

	return grpName		
	
#================================================================================================================================================================================================================================
#======================================================     ATTR     ============================================================================================================================================================
#================================================================================================================================================================================================================================

  
#__________________________________________________________________________________________________________________________________________________________________________________________ getManipulableAttr  

def getManipulableAttr( obj , allowTypes = [ 'double' , 'bool' , 'enum' , 'long' , 'doubleLinear' , 'doubleAngle'] , skipConnected = True ):
	
	'''
		return the attrs manipulable by the user ( in channel box , without input connection , unlocked )
		you can also filter the type, the default is [ 'double' , 'bool' , 'enum' , 'long' ]		
	'''

	cbKeyableAttr    = mc.listAttr( obj  , k = True ,  u = True )
	cbNonkeyableAttr = mc.listAttr( obj  , k = False , v = True , cb = True , u = True  )
	
	if( cbKeyableAttr    == None ): cbKeyableAttr = []
	if( cbNonkeyableAttr == None ): cbNonkeyableAttr = []

	cbAttrs = cbKeyableAttr + cbNonkeyableAttr 
	cbAttrs = list(set(cbAttrs))    
	
	cbAttrsClean = []
	for attr in cbAttrs:

		if(skipConnected == True ):
			sourceConnections = mc.listConnections( ( obj + '.' + attr ) , d = False , s = True )
			if( sourceConnections == None )or( 'animCurve' in mc.nodeType(sourceConnections[0]) ):
				cbAttrsClean.append(attr)
		else:
			cbAttrsClean.append(attr)
	
	cbAttrsTypeFiltered = []        
	for attr in cbAttrsClean:
		attrType = mc.getAttr( ( obj + '.' + attr ) ,  typ = True )
		if( attrType in allowTypes ):
			cbAttrsTypeFiltered.append(attr)           
		
	return cbAttrsTypeFiltered


#__________________________________________________________________________________________________________________________________________________________________________________________ addSpecialAttr	

def addSpecialAttrExtend( obj , attrName , attrType ):
	


	objAttrName = ( obj + '.' + attrName )

			
	if( attrType == 'separator' ):
		
		mc.addAttr( obj         , ln = attrName , at = "enum"  , en = "#####:#####:" )
		mc.setAttr( objAttrName , e  = True         , channelBox = True    , lock = True         )	
		
	elif( attrType == 'enumOnOff' ):
	
		mc.addAttr( obj         , ln = attrName , at = "enum"        , en = "off:on:" , dv = 1 )
		mc.setAttr( objAttrName , e = True      , keyable = True          )		
		
	elif( attrType == 'intOnOff' ):

		mc.addAttr( obj         , ln = attrName , at = "long"        , dv = 1   ,  min = 0 , max = 1        )
		mc.setAttr( objAttrName , e = True      , keyable = True    )		

	elif( attrType == 'int+' ):

		mc.addAttr( obj         , ln = attrName , at = "long"        , dv = 0   ,  min = 0  )
		mc.setAttr( objAttrName , e = True      , keyable = True    )	

	elif( attrType == 'floatOnOff' ):
	
		mc.addAttr( obj         , ln = attrName , at = "double"     , dv = 1   ,  min = 0 , max = 1        )
		mc.setAttr( objAttrName , e = True      , keyable = True     )		
		
	elif( attrType == 'floatInput' ):
	
		mc.addAttr( obj         , ln = attrName , at = "double"      , dv = 0           )
		mc.setAttr( objAttrName , e = True      , keyable = False , channelBox = True           )			
	
	elif( attrType == 'float1' ):
	
		mc.addAttr( obj         , ln = attrName , at = "double"      , dv = 1           )
		mc.setAttr( objAttrName , e = True      , keyable = True        )	

	elif( attrType == 'float1Pos' ):
	
		mc.addAttr( obj         , ln = attrName , at = "double"      , dv = 1, min = 0  )
		mc.setAttr( objAttrName , e = True      , keyable = True        )					
	
	elif( attrType == 'floatHide' ):
	
		mc.addAttr( obj         , ln = attrName , at = "double"      , dv = 0           )
		mc.setAttr( objAttrName , e = True          , channelBox = False   )

	elif( attrType == 'floatRead' ):
	
		mc.addAttr( obj         , ln = attrName , at = "double"      , dv = 0           )
		mc.setAttr( objAttrName , e = True          , channelBox = True , keyable = False )				
		
	else:
		
		mc.addAttr( obj         , ln = attrName , at = attrType   )
		mc.setAttr( objAttrName , e = True      , keyable = True        )						
	

	return objAttrName
    
	

#__________________________________________________________________________________________________________________________________________________________________________________________ addSpecialAttr	

def addSpecialAttrsExtend( objs , attrNames , attrTypes , attrValues = None  ):
	
	'''
		automate some attrBuiding : separator , enumOnOff , intOnOff, floatOnOff , floatInput , floatHide , float1 on obj
	'''	
	
	objAttrNames = []
	
	if( len(objs) == 0 ):
		mc.error('addSpecialAttrs: No OBJ')
		
	elif( len(objs) == 1 ):		
		for i in range( 0 , len(attrNames) ):
			objAttrName = addSpecialAttrExtend( objs[0] , attrNames[i] , attrTypes[i] )
			if not( attrValues == None ) and not ( attrValues[i] == None ):
				mc.setAttr( objAttrName , attrValues[i] )
				
			objAttrNames.append(objAttrName)
				
	elif( len(objs) == len(attrNames) ):				
		for i in range( 0 , len(attrNames) ):
			objAttrName = addSpecialAttrExtend( objs[i] , attrNames[i] , attrTypes[i] )
			if not( attrValues == None ) and not ( attrValues[i] == None ):
				mc.setAttr( objAttrName , attrValues[i] )
			objAttrNames.append(objAttrName)
				
	else:
		mc.error('addSpecialAttrs: difference between obj & attrNames')
		
	return objAttrNames
    
#__________________________________________________________________________________________________________________________________________________________________________________________ writeStringAttr		


def writeStringAttr( master, attrName ,  value ):
				
	mAttr = master +'.'+ attrName 
	
	if not( mc.objExists( mAttr ) ):
		mc.addAttr(  master     ,  ln = attrName , dt = "string"  )		
		mc.setAttr(  mAttr  ,  value   , type = "string" , l = True ) 
		return 1
		
	mc.setAttr(  mAttr  ,  l = False ) 
	mc.setAttr(  mAttr  ,  value   , type = "string" , l = True ) 
					
	return 1			


#__________________________________________________________________________________________________________________________________________________________________________________________ writeStringArrayAttr	

def writeStringArrayAttr( master, attrName ,  values ):
				
	mAttr = master +'.'+ attrName
	
	strValues = [ str(v) for v in values ]
	
	
	stringValue = ' '.join(strValues)
	
	if not( mc.objExists( mAttr ) ):
		mc.addAttr(  master     ,  ln = attrName , dt = "string"  )		
		mc.setAttr(  mAttr  ,  stringValue   , type = "string" , l = True ) 
		return 1
		
	mc.setAttr(  mAttr  ,  l = False ) 
	mc.setAttr(  mAttr  ,  stringValue   , type = "string" , l = True ) 
					
	return 1			
	
#__________________________________________________________________________________________________________________________________________________________________________________________ readStringArrayAttr


def readStringArrayAttr( master, attrName ):
				
	mAttr = master +'.'+ attrName 

	stringValue = mc.getAttr(  mAttr )
	
	if( stringValue == '' ):
		return []
	
	
	values = stringValue.split(' ')
	
	floatValues = []

	for v in values:
		try:
			floatValues.append(float(v))
		except:
			floatValues.append(v)
			
	return floatValues		


#__________________________________________________________________________________________________________________________________________________________________________________________ writeCustomDv


def writeCustomDv( obj , attrs ):
	
	'''
		create new attrs on the obj , non visible on the chanel box , named dv_attrName. with the value of attrName.
		if its already exist it's only whrite the new value on it
		return all the dv attr name
		
		attrs = [ 'translateX' , 'translateY' , 'translateZ' , 'rotateX' , 'rotateY' , 'rotateZ' , 'scaleX' , 'scaleY' , 'scaleZ' ]
	
	'''

	
	dvSuffix = 'dv_'
	
	newAttr = []
	
	for attr in attrs:
	    
	    dvAttrName = dvSuffix + attr
	    
	    dvObjAttr = obj + '.' + dvAttrName
	    objAttr   = obj + '.' + attr
	
	    if not( mc.objExists( dvObjAttr ) ):          
	        addSpecialAttrExtend( obj , dvAttrName , 'floatHide' )
	
	    mc.setAttr( dvObjAttr , mc.getAttr( objAttr ) )
	    newAttr.append(dvObjAttr)

	
	return newAttr

def writeCustomDvTrs( obj , trsValue ):
	attrs = [ 'tx' , 'ty' , 'tz' , 'rx' , 'ry' , 'rz' , 'sx' , 'sy' , 'sz' ]
	dvSuffix = 'dv_'
	newAttr = []

	for i in range( 0 , len(attrs) ):
	    
	    dvAttrName = dvSuffix + attrs[i]
	    
	    dvObjAttr = obj + '.' + dvAttrName
	    objAttr   = obj + '.' + attrs[i]
	
	    if not( mc.objExists( dvObjAttr ) ):          
	        addSpecialAttrExtend( obj , dvAttrName , 'floatHide' )
	
	    mc.setAttr( dvObjAttr , trsValue[i] )
	    newAttr.append(dvObjAttr)


def addSpecialAttr( obj , attrName , attrType , attrValue , attrKeyable = True , attrCb  = True , attrLock  = False , updateString = 1 ):
	
	if not( mc.objExists(obj) ):
		#print('buildAttribut.utils_mayaAddSpecialAttr() ---->    {}    doesnt exist (yet?), cannot add attr   {}   '.format(obj, attrName) );
		return None

	objAttrName = ( obj + '.' + attrName )

	if not( mc.objExists( objAttrName ) ):
		if(   attrType == None                  ): pass
		elif( attrType == 'int'                 ): mc.addAttr( obj , ln = attrName , at = 'long'    , k = 1                           )
		elif( attrType == 'float'               ): mc.addAttr( obj , ln = attrName , at = "double"  , k = 1                           )
		elif( attrType in [ 'long' , 'double' ] ): mc.addAttr( obj , ln = attrName , at = attrType  , k = 1                           )
		elif( ':'      in attrType              ): mc.addAttr( obj , ln = attrName , at = "enum"    , k = 1 , en = attrType           )                         
		elif( attrType == 'int+'                ): mc.addAttr( obj , ln = attrName , at = "long"    , k = 1 , min = 0                 )
		elif( attrType == 'int-'                ): mc.addAttr( obj , ln = attrName , at = "long"    , k = 1           , max = 0       )
		elif( attrType == 'intOnOff'            ): mc.addAttr( obj , ln = attrName , at = "long"    , k = 1 , min = 0 , max = 1       )
		elif( attrType == 'float+'              ): mc.addAttr( obj , ln = attrName , at = "double"    , k = 1 , min = 0                 )
		elif( attrType == 'float-'              ): mc.addAttr( obj , ln = attrName , at = "double"    , k = 1           , max = 0       )
		elif( attrType == 'floatOnOff'          ): mc.addAttr( obj , ln = attrName , at = "double"    , k = 1 , min = 0 , max = 1       )
		elif( attrType == 'enumOnOff'           ): mc.addAttr( obj , ln = attrName , at = "enum"    , k = 1 , en = "off:on:" , dv = 1 )
		elif( attrType == 'separator'           ):
			mc.addAttr( obj , ln = attrName , at = "enum"    , k = 1 , en = "#####:" )
			mc.setAttr( objAttrName , e = True , lock = 1 )
		elif( attrType == 'title'               ):
			mc.addAttr( obj , ln = attrName , at = "enum"    , k = 1 , en = "{}:".format(attrValue) )
			mc.setAttr( objAttrName , e = True , lock = 1 )
		elif( attrType == 'string'              ): 
			mc.addAttr( obj , ln = attrName , dt = "string"  , k = 1    )			
		else: 
			try: mc.addAttr( obj , ln = attrName , at = attrType , k = 1   )
			except: mc.error('buildAttribute.utils_mayaAddSpecialAttr - {} is not part of the list'.format(attrType) )

		attrCb = True

	#SET VALUE	
	if not( attrValue  == None ):
		isLock = mc.getAttr( objAttrName , l = True )
		mc.setAttr( objAttrName , e = True , lock = 0 )				
		
		if( attrType == 'string' ):
			if( updateString ):
				oldValue = mc.getAttr( objAttrName )
				if( oldValue == None ):oldValue = ''
				
				if( oldValue == '' ):mc.setAttr( objAttrName , attrValue , typ = 'string' )
				else:                mc.setAttr( objAttrName , '{} {}'.format( oldValue , attrValue ) , typ = 'string' )
				
			else:
				mc.setAttr( objAttrName , attrValue , typ = 'string' )
		else:
			mc.setAttr( objAttrName , attrValue  )
		
		if(isLock): mc.setAttr( objAttrName , e = True , lock = 1 )	

	#SET STATE
	if ( attrKeyable == None ): attrKeyable = mc.getAttr( objAttrName , k = True  )
	if ( attrCb      == None ): attrCb      = mc.getAttr( objAttrName , k = True ) # k because cb doesnt work...
	if ( attrLock    == None ): attrLock    = mc.getAttr( objAttrName , l = True  )
	
	if(   attrCb ) and    ( attrKeyable ): mc.setAttr( objAttrName , e = True , k = attrKeyable )
	elif( attrCb ) and not( attrKeyable ): mc.setAttr( objAttrName , e = True , channelBox = attrCb , k = attrKeyable )
	else:                                  mc.setAttr( objAttrName , e = True ,  k = attrCb , channelBox = attrCb )
	
	mc.setAttr( objAttrName , e = True , lock = attrLock ) 

	return objAttrName


#__________________________________________________________________________________________________________________________________________________________________________________________ setToCustomDv


def setToCustomDv( obj ):
	
	'''
	list the attrs of an obj , see the dv on. and apply the value of the dv attr to the attr corresponding.
	return the dv attribut found
		
	'''	
	
	dvSuffix = 'dv_'  
	
	attrs    = mc.listAttr(obj)
	dvAttrs  = []
	
	for attr in attrs:
	    if( attr[0:3] == dvSuffix ):
	        objDvAttr = ( obj + '.' + attr )
	        objAttr = ( obj + '.' + attr[3:len(attr)] )
	        mc.setAttr( objAttr , mc.getAttr( objDvAttr ) )
	        dvAttrs.append(attr)
	
	return dvAttrs 

		
	
#__________________________________________________________________________________________________________________________________________________________________________________________ resetControlValue		

def resetControlValue( obj ):


	father  = mc.listRelatives( obj , p = True );
	
	if( father == None ):
		mc.error( 'cant do this : this object doesnt have a father' )
		return 0
	
	mc.parent( obj , w = True )

	mc.delete( mc.parentConstraint( obj , father[0] ) )
	
	mc.parent( obj , father[0] )
	
	
	return 1




def getAttrRangeLength(attrDriver):
	rLength = 99999999999999999999999
	min = mc.addAttr( attrDriver , q = True , min = True )
	max = mc.addAttr( attrDriver , q = True , max = True )
	if not( min == None ) and not( max == None ):
		rLength = max-min+1

	return rLength

	
#================================================================================================================================================================================================================================
#======================================================     NODE CONNECTION     ============================================================================================================================================================
#================================================================================================================================================================================================================================


#__________________________________________________________________________________________________________________________________________________________________________________________ buildConnections

def buildConnections( objs , inAttrs , outAttrs , mode , mo = False ):

	'''
		build connections between objs

		mode     is the way you want to constraint objs:  	modes = [  "oneMaster" , "2by2" ];
		
				oneMaster: the first obj constraint all the other				

				2by2     : the first obj constraint the second , the third constraint the fourth , etc...	
				
				mo : if mo 'maintient offset' is True , the destination keep its value 
	'''
	
	modes = [ "normal" , "oneMaster" , "2by2" ];

	
	masters = []
	

	if( mode == "oneMaster" ):
	
		master = objs[0] 
		slaves =  objs[1:len(objs)] 
	
		for i in range( 0 , len(slaves) ):
			for j in range( 0 , len(inAttrs) ):
				
				sourceAttr = master    + '.' + inAttrs[j]
				destAttr   = slaves[i] + '.' + outAttrs[j]			
				
				if( mc.objExists( sourceAttr ) ) and ( mc.objExists( destAttr ) ):
					
					if( mo == True ):
						valueSource = mc.getAttr( sourceAttr )[0]
						valueDest   = mc.getAttr( destAttr )[0]						
						
						isMultiAttr = 1
						if( sourceAttr[-1] in ['X','Y','Z'] ):
							isMultiAttr = 0
						
						buildOffsetConnection( sourceAttr , destAttr , offsetAttrs = [  [ '-' , valueSource ] , [ '+' , valueDest ] ] , multiAttr = isMultiAttr )						
					else:
						mc.connectAttr( sourceAttr , destAttr )
				
		masters = [ master ]

	elif( mode == "2by2" ):
		
		for i in range( 0 , len(objs) , 2 ):
			if not ( ( i + 1 ) == len(objs) ):
				for j in range( 0 , len( inAttrs) ):
					
					sourceAttr = objs[i]   + '.' + inAttrs[j]
					destAttr   = objs[i+1] + '.' + outAttrs[j]
					
					if( mc.objExists( sourceAttr ) ) and ( mc.objExists( destAttr ) ):
						
						if( mo == True ):
							valueSource = mc.getAttr( sourceAttr )[0]
							valueDest   = mc.getAttr( destAttr   )[0]	
							
							isMultiAttr = 1
							if( sourceAttr[-1] in ['X','Y','Z'] ):
								isMultiAttr = 0			
								
							buildOffsetConnection( sourceAttr , destAttr , offsetAttrs = [  [ '-' , valueSource ] , [ '+' , valueDest ] ] , multiAttr = isMultiAttr )						
						else:
							mc.connectAttr( sourceAttr , destAttr )					

				masters.append(objs[i])
					

	return masters	
	

#__________________________________________________________________________________________________________________________________________________________________________________________ buildOffsetConnection



def buildOffsetConnection( inAttr , outAttr , offsetAttrs = [] , multiAttr = 0 ):

	'''
		between two attrs, build series of node ( multiplyDivide or plusMinusAverage ) that modify the output
		inAttr , outAttr =  'toto.translateX'
		
		offsetAttrs = [  [ '*' , 'toto.translateY'] , [ '-' , 'toto.translateZ'] ,  [ '-' , 10 ] ]   <--- if its a name it connect , he just put a number
		
		* / + -     are valids characters
			
	'''
	
	nodesCreated = []
	outObjName , outAttrName = outAttr.split('.')
	
	multiplyDivName   = outObjName + '_' + outAttrName + '_multiplyDivide'
	addMinAverageName = outObjName + '_' + outAttrName + '_plusMinusAverage'

	curentInAttr = inAttr	
	
	
	dicoOperation = { '*' :  1 , '/' : 2 , '+' : 1  , '-' : 2  }
	
	endAttrAxe = 'X'
	endAttrNbr = '1' 
	if( multiAttr == 1 ):
		endAttrAxe = ''
		endAttrNbr = '3'
		
	
	
	for i in range( 0 , len( offsetAttrs ) ):
		
		
		if( offsetAttrs[i][0] == '*' ) or ( offsetAttrs[i][0] == '/' ):
			
			multiplyDivNode = mc.createNode( 'multiplyDivide' , n = multiplyDivName )
			mc.setAttr( multiplyDivNode + '.operation' , dicoOperation[offsetAttrs[i][0]] )
 			
			mc.connectAttr( curentInAttr      , multiplyDivNode + '.input1' + endAttrAxe )
			
			newNumValue = utilsPython.convertStringToNum( offsetAttrs[i][1] )
			
			isString = 0
			if( newNumValue == False ):
				isString = 1				
			else:
				offsetAttrs[i][1] = newNumValue
				
			
			if( isString == 1 ):
				mc.connectAttr( offsetAttrs[i][1] , multiplyDivNode + '.input2' + endAttrAxe )
			else:
				try:
					mc.setAttr( multiplyDivNode + '.input2' + endAttrAxe , offsetAttrs[i][1] )
				except:
					mc.setAttr( multiplyDivNode + '.input2' + endAttrAxe , offsetAttrs[i][1][0] , offsetAttrs[i][1][1] , offsetAttrs[i][1][2] , type = 'double3' )					
					
			curentInAttr = multiplyDivNode  + '.output' + endAttrAxe 			
			nodesCreated.append( multiplyDivNode )
			
		elif( offsetAttrs[i][0] == '+' ) or ( offsetAttrs[i][0] == '-' ):

			addMinAverageNode = mc.createNode( 'plusMinusAverage' , n = addMinAverageName )		
			mc.setAttr( addMinAverageNode + '.operation' , dicoOperation[offsetAttrs[i][0]] )		

			mc.connectAttr( curentInAttr      , addMinAverageNode + '.input'+endAttrNbr+'D[0]' )
	
			newNumValue = utilsPython.convertStringToNum( offsetAttrs[i][1] )
			
			isString = 0
			if( newNumValue == False ):
				isString = 1				
			else:
				offsetAttrs[i][1] = newNumValue
				
			
			if( isString == 1 ):			
				mc.connectAttr( offsetAttrs[i][1] , addMinAverageNode + '.input'+endAttrNbr+'D[1]'  )
			else:
				try:
					mc.setAttr( addMinAverageNode + '.input'+endAttrNbr+'D[1]' , offsetAttrs[i][1] )
				except:
					mc.setAttr( addMinAverageNode + '.input'+endAttrNbr+'D[1]' , offsetAttrs[i][1][0] , offsetAttrs[i][1][1] , offsetAttrs[i][1][2] , type = 'double3' )						
				
			curentInAttr = addMinAverageNode + '.output'+endAttrNbr+'D'	
			nodesCreated.append( addMinAverageNode )					
		
		
		if( i == len(offsetAttrs) - 1 ):
			mc.connectAttr( curentInAttr, outAttr  )
		

		
	return nodesCreated	



#__________________________________________________________________________________________________________________________________________________________________________________________ buildNodeNetWork


def buildNodeNetWork( baseName , inAttrs = [] , nodesType = [] ):

	'''
		between list of attr, build series of node ( multiplyDivide or plusMinusAverage ) that modify the outputs
		inAttr , outAttr =  'toto.translateX'
		
		offsetAttrs = [ [  'input.translateY' , [ '*' , 'toto.translateY'] , [ '-' , 'toto.translateZ'] ,  [ '-' , 10 ] , 'output.translateY' ]  , ...  ]   <--- if its a name it connect , he just put a number
		
		* / + - blend rev     are valids characters
		
		
		exemple:
		
		inAttrs = []
		nodesType = []
		
		inAttrs.append(    [  'A.ty'         , 'B.ty'          , 10             , [ 1   , 'D.ry'  ] , 'D.ty'  ]	)
		nodesType.append(  [  'in'           ,     '*'         , '/'            , 'blend'           , 'out'   ]	)
		inAttrs.append(    [  ''             , ''              , ''             , [ 1   , 'E.ry'  ] , 'E.ty'  ]	)
		nodesType.append(  [  ''             , ''              , ''             , 'blend'           , 'out'   ]	)
		inAttrs.append(    [  ''             , ''              , ''             , [ 1   , 'F.ry'  ] , 'F.ty'  ]	)
		nodesType.append(  [  ''             , ''              , ''             , 'blend'           , 'out'   ]	)
		inAttrs.append(    [  ''             , ''              , 'C.scaleX'     , [ 1   , 'G.ry'  ] , 'G.ty'  ]	)
		nodesType.append(  [  ''             , ''              , '/'            , 'blend'           , 'out'   ]	)
		inAttrs.append(    [  ''             , ''              , ''             , [ 1   , 'H.ry'  ] , 'H.ty'  ]	)
		nodesType.append(  [  ''             , ''              , ''             ,  'blend'          , 'out'   ]	)
		inAttrs.append(    [  ''             , ''              , ''             , [ 1   , 'I.ry'  ] , 'I.ty'  ]	)
		nodesType.append(  [  ''             , ''              , ''             ,  'blend'          , 'out'   ]	)		
			
	'''
	
	nbrLists   = len( inAttrs    )
	listLength = len( inAttrs[0] )
	
	nodesCreated     = []
	fathers          = []
	nodesfathers     = []
	nodesfathersNext = []
	
	for iLength in range( 1 , listLength ):
		
		newNodes         = []
		nodesfathersNext = nodesfathers
		nodesfathers     = []	
		

		for i in range( 0 , nbrLists ):		
			
			
			if not( ( inAttrs[i][iLength] == '' ) or ( inAttrs[i][iLength] == None ) ):
				
				if( iLength == 1 ):		
					newNode = createSpecialNode( baseName , nodesType[i][ iLength ]  ,  utilsPython.convertArrayToFlatArray( [ inAttrs[i][ iLength - 1 ] , inAttrs[i][ iLength ] ] )    )	
				elif( iLength == listLength - 1 ):									
					mc.connectAttr( nodesfathersNext[i] , inAttrs[i][ iLength ] )   						
				else:						
					newNode = createSpecialNode( baseName , nodesType[i][ iLength ]  , utilsPython.convertArrayToFlatArray( [ nodesfathersNext[i]  ,  inAttrs[i][ iLength ] ] )  )					

			nodesfathers.append( newNode )					
		nodesCreated += nodesfathers
	
		
	
	# clean nodeCreated array
	nodesCreated = list(set(nodesCreated))
	
	for i in range( 0 , len(nodesCreated) ):
		nodesCreated[i] = nodesCreated[i].split('.')[0]	
	
	return nodesCreated	
	


def buildNodeOperations( operations ):

	dicoTypeSuffix = { '*' :  'MULT' , '/' : 'DIV' , '+' : 'ADD'  , '-' : 'SUB' , 'blend' : 'BLEND'  , 'reverse' : 'REV', 
	'mult' :  'MULT' , 'div' : 'DIV' , 'add' : 'ADD'  , 'sub' : 'SUB'  , 'inverse01' : 'INV' }

	opType = ''
	buildConnection = False
	attrList = []

	for i in range( 0 , len(operations) ):
		
		if( operations[i] in dicoTypeSuffix.keys() ):
			opType = operations[i]
		elif( operations[i] == '=' ):
			buildConnection = True
		else:
			attrList.append( operations[i] )
			
			if( buildConnection == True ):
				buildSpecialConnection( attrList , opType )
				opType = ''
				buildConnection = False
				attrList = [ operations[i] ]




#__________________________________________________________________________________________________________________________________________________________________________________________ createSpecialNode




def insertClamp( attr , input = 0 , min = 0 , max = 999999999  ):

	'''
		insertClamp( "transform3.tx" , input = 1  )
	'''


	clampNode = mc.createNode("clamp")
	mc.setAttr( clampNode + '.minR' , min )
	mc.setAttr( clampNode + '.maxR' , max )

	if( input ):
		inputAttr  = mc.listConnections( attr , s = True , d = False , p = True  )[0]
		outputAttr = attr

		mc.connectAttr( inputAttr              , clampNode + '.inputR'  )
		mc.connectAttr( clampNode + '.outputR' , outputAttr            , f = True )
	else:
		inputAttr  = attr
		outputAttr = mc.listConnections( attr , s = False , d = True , p = True  )[0]

		mc.connectAttr( inputAttr              , clampNode + '.inputR'  )
		mc.connectAttr( clampNode + '.outputR' , outputAttr            , f = True  )


	return clampNode




def buildSpecialConnection( attrs , nodeType ):
	'''

		testA = mc.createNode("transform")
		test = mc.createNode("transform")
		
		buildSpecialConnection( [ testA + '.translateX' , 10 , test + '.translateY' , test + '.translateX'] , 'mult' , '' )
	
		TO DO:
		-improving for vector type of attribute
		-add bend and reverse
	'''
	#CONVERT STRING TO FLOAT IF POSSIBLE
	for i in range( 0 , len(attrs) ):
		attrs[i] = utilsPython.convertStringToNum( attrs[i] )

	dicoTypeSuffix = { '*' :  'MULT' , '/' : 'DIV' , '+' : 'ADD'  , '-' : 'SUB' , 'blend' : 'BLEND' , 'reverse' : 'REV', 
	'mult' :  'MULT' , 'div' : 'DIV' , 'add' : 'ADD'  , 'sub' : 'SUB'  , 'inverse01' : 'INV' }
	stringTypes = [ types.StringType , types.UnicodeType ] 

	lastIndex = len(attrs)-1

	splitTmp = attrs[lastIndex].split('.')
	baseName = splitTmp[0] + '_' + splitTmp[1]
	#nodeName = '{0}_{1}'.format( baseName , dicoTypeSuffix[nodeType] )	

	lastIndex = len(attrs)-1
	nodedCreated = []
	if( nodeType in ['*','mult'] ):
		
		lastNode = ''
		for i in range( 1 , lastIndex ):
			#BUILD NODE
			nodeName = mc.createNode( 'multiplyDivide'  )
			mc.setAttr( nodeName + '.operation' , 1 )
			#CONNECT IN	A
			nodeAttrInA = '{0}.input1X'.format( nodeName )
			if( i == 1 ):		
				if( type(attrs[i-1]) in stringTypes ): mc.connectAttr( attrs[i-1] , nodeAttrInA , f = True )
				else:                                   mc.setAttr( nodeAttrInA , float(attrs[i-1]) )
			else:
				nodeAttrOut = lastNode + '.outputX'
				mc.connectAttr( nodeAttrOut , nodeAttrInA )
			#CONNECT IN	B
			nodeAttrInB = '{0}.input2X'.format( nodeName )
			if( type(attrs[i]) in stringTypes ): mc.connectAttr( attrs[i] , nodeAttrInB , f = True )
			else:                                 mc.setAttr( nodeAttrInB , float(attrs[i]) )

			lastNode = nodeName
			nodedCreated.append(nodeName)

		#CONNECT OUT
		if( type(attrs[lastIndex]) in stringTypes  ):
				mc.connectAttr( lastNode + '.outputX' , attrs[lastIndex] , f = True )


	elif( nodeType in ['/','div'] ):

		lastNode = ''
		for i in range( 1 , lastIndex ):
			#BUILD NODE
			nodeName = mc.createNode( 'multiplyDivide' )
			mc.setAttr( nodeName + '.operation' , 2 )
			#CONNECT IN	A
			nodeAttrInA = '{0}.input1X'.format( nodeName )
			if( i == 1 ):		
				if( type(attrs[i-1]) in stringTypes ): mc.connectAttr( attrs[i-1] , nodeAttrInA , f = True )
				else:                                   mc.setAttr( nodeAttrInA , float(attrs[i-1]) )
			else:
				nodeAttrOut = lastNode + '.outputX'
				mc.connectAttr( nodeAttrOut , nodeAttrInA , f = True )
			#CONNECT IN	B
			nodeAttrInB = '{0}.input2X'.format( nodeName )
			if( type(attrs[i]) in stringTypes ): mc.connectAttr( attrs[i] , nodeAttrInB , f = True )
			else:                                 mc.setAttr( nodeAttrInB , float(attrs[i]) )

			lastNode = nodeName
			nodedCreated.append(nodeName)

		#CONNECT OUT
		if( type(attrs[lastIndex]) in stringTypes  ):
				mc.connectAttr( lastNode + '.outputX' , attrs[lastIndex]  , f = True )


	elif( nodeType in ['+','add'] ):
		#BUILD NODE			
		nodeName = mc.createNode( 'plusMinusAverage' )		
		mc.setAttr( nodeName + '.operation' , 1 )	
 	
 		#CONNECT IN
		for i in range( 0 , lastIndex ):	
			nodeAttrIn = '{0}.input1D[{1}]'.format( nodeName , i )

			if( type(attrs[i]) in stringTypes ): mc.connectAttr( attrs[i] , nodeAttrIn , f = True )
			else:                                      mc.setAttr( nodeAttrIn , float(attrs[i]) )

		#CONNECT OUT
		if( type(attrs[lastIndex]) in stringTypes  ):
				mc.connectAttr( nodeName + '.output1D' , attrs[lastIndex] , f = True )

		nodedCreated.append(nodeName)


	elif( nodeType in ['-','sub'] ):
		#BUILD NODE			
		nodeName = mc.createNode( 'plusMinusAverage'  )		
		mc.setAttr( nodeName + '.operation' , 2 )	

		#CONNECT IN	
		for i in range( 0 , lastIndex ):	
			nodeAttrIn = '{0}.input1D[{1}]'.format( nodeName , i )

			if( type(attrs[i]) in stringTypes ): mc.connectAttr( attrs[i] , nodeAttrIn , f = True )
			else:                                      mc.setAttr( nodeAttrIn , float(attrs[i]) )

		#CONNECT OUT
		if( type(attrs[lastIndex]) in stringTypes  ):
				mc.connectAttr( nodeName + '.output1D' , attrs[lastIndex] , f = True )

		nodedCreated.append(nodeName)
				
	elif( nodeType == 'blend' ):
		nodeName = mc.createNode( 'blendColors'  )		
		blendColorsAttrs = [ '.color2R' , '.color1R' , '.blender' ]	

		#CONNECT IN	
		for i in range( 0 , lastIndex ):	
			nodeAttrIn = nodeName + blendColorsAttrs[i]

			if( type(attrs[i]) in stringTypes ): mc.connectAttr( attrs[i] , nodeAttrIn )
			else:                                mc.setAttr( nodeAttrIn , float(attrs[i]) )
		#CONNECT OUT
		if( type(attrs[lastIndex]) in stringTypes  ):
				mc.connectAttr( nodeName + '.outputR' , attrs[lastIndex] , f = True )

		nodedCreated.append(nodeName)

	elif( nodeType == 'inverse01' ):
		nodeName = mc.createNode( 'plusMinusAverage' )		
		mc.setAttr( nodeName + '.operation' , 2 )	

		mc.setAttr( '{0}.input1D[0]'.format(nodeName) , 1 )
		mc.connectAttr( attrs[0] , '{0}.input1D[1]'.format(nodeName) , f = True )

		mc.connectAttr( nodeName + '.output1D' , attrs[lastIndex] , f = True )






def createSpecialNode( baseName , nodeType , inputs  ):
	
	'''

	build nodes 		* / + - blend rev     are valids characters for nodeType
	
	connect automaticaly the input
	inputs = [ toto.scaleX , 1 ]
	inputs = [ toto.scaleX , yolo.scaleY ]	
	inputs = [ toto.scaleX , yolo.scaleY , yolo.scaleZ ]
	...
	
	'''

	dicoOperation = { '*' :  1 , '/' : 2 , '+' : 1  , '-' : 2  }
	dicoTypeSuffix = { '*' :  'mult' , '/' : 'div' , '+' : 'plus'  , '-' : 'minus' , 'blend' : 'blend'  , 'reverse' : 'rev'  }
	
	baseName = incrBaseNameIfExist( baseName , ['']  , [ '' , ('_'+dicoTypeSuffix[nodeType]) ] )
	nodeName = '{0}_{1}'.format( baseName , dicoTypeSuffix[nodeType] )	

	if( nodeType == '*' ) or ( nodeType == '/' ):
						
		mc.createNode( 'multiplyDivide' , n = nodeName )
		mc.setAttr( nodeName + '.operation' , dicoOperation[nodeType] )
 	
		for i in range( 0 , len(inputs) ):

			isString = 0	
			try:
				toto = float( inputs[i] )
			except:	
				isString = 1		
		
				
			if( isString == 1 ):
				mc.connectAttr( inputs[i] , '{0}.input{1}X'.format( nodeName , i + 1 ) )
			else:
				mc.setAttr( '{0}.input{1}X'.format( nodeName , i + 1 ) , float(inputs[i]) )


		return nodeName  + '.outputX' 					
				
				
	elif( nodeType == '+' ) or ( nodeType== '-' ):
		
		mc.createNode( 'plusMinusAverage' , n = nodeName )		
		mc.setAttr( nodeName + '.operation' , dicoOperation[nodeType] )		
		
		 	
		for i in range( 0 , len(inputs) ):
			
			isString = 0	
			try:
				toto = float( inputs[i] )
			except:	
				isString = 1		
		
			if( isString == 1 ):
				mc.connectAttr( inputs[i] , '{0}.input1D[{1}]'.format( nodeName , i )  )
			else:
				mc.setAttr( '{0}.input1D[{1}]'.format( nodeName , i )  , float(inputs[i]) )			
						

		return nodeName + '.output1D'
	
	elif( nodeType == 'blend' ):
		
		mc.createNode( 'blendColors' , n = nodeName )		
		blendColorsAttrs = [ '.color1.color1R' , '.color2.color2R' , '.blender' ]	
		 	
		for i in range( 0 , len(inputs) ):
			
			isString = 0	
			try:
				toto = float( inputs[i] )
			except:	
				isString = 1		
		
			if( isString == 1 ):
				mc.connectAttr( inputs[i] , blendColorsAttrs[i]  )
			else:
				mc.setAttr( nodeName + blendColorsAttrs[i]  , float(inputs[i]) )			

		return nodeName + '.output.outputR'
		
	elif( nodeType == 'reverse' ):
		
		mc.createNode( 'reverse' , n = nodeName )		
		mc.connectAttr( inputs[0] , nodeName + '.input.inputX'  )

								
		return nodeName + '.output.outputX'
		
		
		
#__________________________________________________________________________________________________________________________________________________________________________________________ buildSimpleExpression
def buildSimpleExpression( name , content ):
	
	return mc.expression( n = name  , s = content  , o = '' , ae=  1 , uc = 'all'  )


def buildTimeSinExp( inSpeed , inAmplitude , inOffset , out ):	
	expContent = '\n' + '{} = sin( {} * time + {} ) * {} ;'.format( out  , inSpeed , inOffset , inAmplitude )		
	return buildSimpleExpression( out + '_SinEXP' , expContent )
	
def buildTimeLinear( inSpeed , inOffset , out , multOffset = 1 ):	
	buildNodeOperations( [ "time1.outTime" , "*" , inSpeed , "+" , inOffset , "*" , multOffset , "=" , out ] )
	
def buildTimeRotationSetup( inSpeedSin , inAmplitudeSin , inOffsetSin , inSpeedLinear , inOffsetLinear , out , multOffsetLinear = 1 ):
	nodeName = mc.createNode( 'plusMinusAverage' )		
	mc.setAttr( nodeName + '.operation' , 1 )	
	mc.connectAttr( nodeName + '.output1D' , out , f = True )

	buildTimeSinExp( inSpeedSin , inAmplitudeSin , inOffsetSin , '{}.input1D[0]'.format( nodeName) )
	buildTimeLinear( inSpeedLinear , inOffsetLinear            , '{}.input1D[1]'.format( nodeName) , multOffsetLinear )	
	
#================================================================================================================================================================================================================================
#======================================================    AUTRE     ============================================================================================================================================================
#================================================================================================================================================================================================================================

def isMesh(obj):

	shape = mc.listRelatives( obj , c = True , s = True , pa = True )
	
	if not ( shape == None) and ( 0<len( shape ) ):
		shapeType = mc.nodeType( shape[0] )
		if( shapeType == 'mesh' ):
			return 1
	return 0	




#_____________________________________________________________________________________________________________________________________________________________________ getSpecialType 
'''
def getSpecialType(obj):


	# manip
	if( mc.objExists( obj + '.baseName' ) ):
		return 'manip'		

	# mesh		
	baseNameShape = mc.listRelatives( obj , c = True , s = True )
	
	if not ( baseNameShape == None) and ( len( baseNameShape ) > 0 ):
		baseNameShapeType = mc.nodeType( baseNameShape[0] )
		if( baseNameShapeType == 'mesh' ):
			return 'mesh'

	# manipSlave
	master = findManipMaster(obj)	
	if not ( master == '' ):
		if( isManip( master ) ):			
			return 'manipSlave'			
			
	# GroupMesh		
	allMesh = getAllChildrenMsh( obj )
	if( obj in allMesh ):
		allMesh.remove( obj )
	
	if not ( 0 == len( allMesh ) ):
		return 'groupMesh'	

	# autre	
	typeObj = mc.nodeType(obj)
		
	return typeObj

'''
	
#_________________________________________________________________________________________________________________________________________________________________________  findManipMaster

def findManipMaster( obj ):	
	obj    = removeComponentSuffix( obj )	
	
	#fix bug maya
	
	if( 'Shape' in obj ):
		obj = mc.listRelatives( obj , p = True )[0]
	
	master = findMasterConstraint( obj )
	
	return master	
		


#_________________________________________________________________________________________________________________________________________________________________________  get All Children Msh	
	
	
def getAllChildrenMsh( elem ):
	
	msh = []	
	childrens = [elem]
	
	
	i = 0

	while not(len(childrens) == 0):
		trsfs = childrens
		childrens = []
		i += 1
			
		for trsf in trsfs:
			
			if( isMesh(trsf) ):			
				msh.append( trsf )
			else:
			    child = mc.listRelatives( trsf , c = 1 , pa = True )
			    if not(child == None):		    
				    for c in child:
					    childrens.append( c )
			    
		        

		if(10<i):
		    childrens = []
		
	return msh 	

#__________________________________________________________________________________________________________________________________________________________________________________________ add In Set	


def addInSet( elem , sets ):
	
	if( sets == ['']):
		return 0
	
	selection = mc.ls( sl = True )
	
	for set in sets:	
		mc.select( cl = True )
		
		mc.sets( elem , add = set )
		
		mc.select( cl = True )	
		
	mc.select( selection )		
		
	return 1	


#__________________________________________________________________________________________________________________________________________________________________________________________ transfereAnim

def transfereAnim( objSource , destination ):
	
	'''
	this proc connect the anim node of the source to the destination. This is not a copy of node!
	'''
	# get information 
	
	upStreamNodes = mc.listRelatives( objSource , s = True , d = False )

	animCurveNodes = []
	attrToConnect  = []
	
	for node in upStreamNodes:
		if( 'animCurve' in mc.nodeType(node) ):
			animCurveNodes.append(node)
			
			plugDest = mc.listConnections( node , d = True , s= False , p = True )
			attrDest = plugDest[0].split('.')[1]
			attrToConnect.append(attrDest)
		
	
	# connect to dest
	
	for i in range( 0 , len(animCurveNodes) ):
		mc.connectAttr( (animCurveNodes[i] + '.output') , (destination + '.' + attrToConnect[i])  )

		
#__________________________________________________________________________________________________________________________________________________________________________________________ deleteTypeChildren		
		


def deleteTypeChildren( selection , typeToKeep ):
	
	'''
		deleteTypeChildren( mc.ls(sl=True) , [ 'mesh' , 'nurbsSurface' , 'nurbsCurve' ] )
	'''
	
	for elem in selection:
		childrens = mc.listRelatives( elem , f = True , p = False ,  c = True )
		if not( len( childrens ) == 0 ):
			for children in childrens:
				type = mc.nodeType( children )
				if not( type in typeToKeep ):
					mc.delete(children)
	
	return 1

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
	


#_____________________________________________________________________________________________________________________________________________________________________ convertFaceEdgeTovtx

def convertFaceEdgeTovtx( selection ):
	
	selectionVtx = []	
	
	componentToConvert = [  '.f['  , '.e['   ]	
	vertexTmp = []
	
	
	for elem in selection:
		
		if ( componentToConvert[0]  in elem ):
			
			vertexTmp = mc.polyListComponentConversion( elem ,  ff = True ,  tv = True )
			for v in vertexTmp:
				selectionVtx.append(v)
				
		elif ( componentToConvert[1]  in elem ):
			
			vertexTmp = mc.polyListComponentConversion( elem ,  fe = True ,  tv = True )
			for v in vertexTmp: 
				selectionVtx.append(v)
		else:
			selectionVtx.append(elem)
	
	
	return selectionVtx	


		
#__________________________________________________________________________________________________________________________________________________________________________________________ sortObjWithHisClosestOne	
def sortObjWithHisClosestOne( masters , slaves ):
	
	'''
		pas exactement un resultat coherent , mais marche dans la plupart des cas
	'''
	
	couplesProxy = []
	
	for i in range( 0 , len(masters) ):
		slavesSorted = sortObjByProximity( masters[i] , slaves )
		slaveClosest = slavesSorted[0]
		couplesProxy += [ masters[i] , slaveClosest ]				
		slaves.remove( slaveClosest )
		
	return couplesProxy	
	

#__________________________________________________________________________________________________________________________________________________________________________________________ sortObjByProximity		


def sortObjByProximity( master , slaves ):
		
	trsObj    = trsClass.trsClass()
	trsMaster = trsObj.createFromObj( master )
	
	distances = []
	dico = {}
	for slave in slaves:
		
		trsObj.createFromObj( slave )
		distance = trsObj.toDistance( trsMaster[0:3] )
		distances.append( distance )
		dico[ str(distance) ] = slave
			
	distances.sort()
	
	slavesSorted = []
	for d in distances:
		slavesSorted.append( dico[ str( d ) ] ) 	
	
	return slavesSorted


#__________________________________________________________________________________________________________________________________________________________________________________________ buildFollicle		
def buildFollicle( surfaceTrs , baseName = None , n = None , u = 0 , v = 0 ):

	selection = mc.ls( sl = True )

	#_______________________________________ NAME

	if( baseName == None ): 
		baseName = surfaceTrs + 'Fol1' 
	baseName = incrBaseNameIfExist(  baseName  ,  ['' , 'l_', 'r_' ]  ,  ['' , '_FOL']   )

	follicle      = baseName + '_FOL'
	follicleShape = baseName + '_FOLShape'

	if not( n == None ):
		follicle = n
		follicleShape = n + 'Shape' 



	#_______________________________________ BUILD

	mc.createNode( 'follicle' , n = follicleShape )

	follicleShapeParents = mc.listRelatives( follicleShape , p = True )
	mc.rename( follicleShapeParents[0] , follicle )

	#_______________________________________ ATTR

	attrNames  = [ 'EXTRA_ATTR', 'uValue'     , 'vValue'     ]
	attrTypes  = [ 'separator' , 'floatOnOff' , 'floatOnOff' ]
	attrValues = [  None       ,  u           ,  v           ]	 
	objs       = [ follicle for i in range( 0 , len(attrNames) ) ]

	addSpecialAttrsExtend( objs , attrNames , attrTypes , attrValues )

	#_______________________________________ CONNECTIONS

	mc.connectAttr( follicleShape + '.outTranslate' , follicle      + '.translate'  )
	mc.connectAttr( follicleShape + '.outRotate'    , follicle      + '.rotate'     )
	mc.connectAttr( follicle      + '.uValue'       , follicleShape + '.parameterU' )	
	mc.connectAttr( follicle      + '.vValue'       , follicleShape + '.parameterV' )	

	#_______________________________________ CONNECTIONS SURFACE

	surfaceShape = 	mc.listRelatives( surfaceTrs , c = True , s = True )

	inputAttr    = 'local'
	outputAttr   = 'inputSurface'	
	if( mc.nodeType( surfaceShape[0] ) == 'mesh' ):
		inputAttr  = 'outMesh'
		outputAttr = 'inputMesh'	

	mc.connectAttr( surfaceShape[0] + '.' +  inputAttr        , follicleShape + '.' +  outputAttr        )		
	mc.connectAttr( surfaceTrs      + '.' + 'worldMatrix[0]'  , follicleShape + '.' + 'inputWorldMatrix' )



	mc.select( selection )

	return follicle 	


def parentToChildrens( parent , includeParent = True , returnLongName = False ):
	allSceneObj = mc.ls( l = True , r = True );	
	#GET LONG NAME OF PARENT
	parentLongName = getLongName( parent )     
	#GET CHILDRENS
	childrensLongName = []
	for obj in allSceneObj:    
		if(  len(parentLongName) <= len(obj)  ) and ( obj[0:(len(parentLongName)+1)] == (parentLongName+'|') ):
			childrensLongName.append(obj)    
	#REMOVE DUPLICATE
	childrensLongName = utilsPython.removeDuplicate(childrensLongName)   
	#REMOVE PARENTS
	if( includeParent == True ):
		childrensLongName.append(parentLongName)
	#REMOVE PARENTS
	childrens = childrensLongName
	if( returnLongName == False ):
		childrens = []
		for children in childrensLongName:
			childrens.append( getShortName( children ) )	
	return childrens
	


def parentsToChildrens( parents , includeParents = False , returnLongName = False ):
	allSceneObj = mc.ls( l = True , r = True );	
	#GET LONG NAME OF PARENT
	parentsLongName = []
	for parent in parents:
		parentsLongName.append( getLongName( parent ) );	    
	#GET CHILDRENS
   	childrensLongName = []
	for obj in allSceneObj:
		for parent in parentsLongName:	    
			if(  len(parent) <= len(obj)  ) and ( obj[0:(len(parent)+1)] == (parent+'|') ):
				childrensLongName.append(obj)    
   	#REMOVE DUPLICATE
   	childrensLongName = utilsPython.removeDuplicate(childrensLongName)   
   	#REMOVE PARENTS
   	if( includeParents == True ):
   		childrensLongName += parentsLongName 
   	#REMOVE PARENTS
   	childrens = childrensLongName
   	if( returnLongName == False ):
		childrens = []
		for children in childrensLongName:
			childrens.append( getShortName( children ) )	
	return childrens
	
	
def filterType( dagObjs , types ):

	filteredObjs = []
	
	for elem in dagObjs:
		for type in types:
			if( mc.nodeType(elem) == type ): 	
				filteredObjs.append(elem)	

	return utilsPython.removeDuplicate(filteredObjs)


def safeParent( child , father ):
	if not( child == None ) and not( father == None ):
		if( mc.objExists(child) ) and ( mc.objExists(father) ):
			if not ( child == father ):
				curentParent = mc.listRelatives( child , p = True )
				
				if( curentParent == None ):mc.parent(child , father )
				else:
					if not( curentParent[0] == father ):
						mc.parent( child , father )

def dagSafeBuild( type , name , father ):
	rawName = mc.createNode( type , n = name )
	transformNode = mc.listRelatives( rawName , p = True  )
	if not( transformNode == None):
		mc.rename( rawName , name + 'Shape' )
		rawName = mc.rename( transformNode , name )
	safeParent(rawName,father)
	return rawName
	

def safeConnectAttr( attrSource , attrDest ):
	attrSourcesCurrent = mc.listConnections( attrDest , s = True , d = False , p = True)
	attrLock = mc.getAttr( attrDest , l = True )

	if(attrLock):mc.setAttr( attrDest , l = False )
	
	if( attrSourcesCurrent == None )or(len(attrSourcesCurrent)==0):
		mc.connectAttr( attrSource , attrDest , f = True )
	elif( attrSourcesCurrent[0] == attrSource ):
		print('safeConnectAttr: ALREADY EXIST , SKIP: {} -----> {}'.format(attrSource,attrDest) )
	else:
		print('safeConnectAttr: SWAP {} --x--> {} TO {} -----> {}'.format(attrSourcesCurrent[0],attrDest,attrSource,attrDest) )
		mc.disconnectAttr( attrSourcesCurrent[0] , attrDest )
		mc.connectAttr(    attrSource            , attrDest , f = True )



def prepareJointForIk( ikJoints ):

	for joint in ikJoints:
		jointOrientToRotation( joint )
		rotationToPrefAngle( joint )



def jointOrientToRotation( joint ):
	#CREATE AND PLACE TRSF
	trsfTmp = mc.createNode( 'transform' , n = 'utils_jointOrientToRotation_' + joint )
	father  = mc.listRelatives( joint , p = True , f = True)
	mc.parent( trsfTmp , father )
	mc.delete( mc.parentConstraint( joint , trsfTmp) )
	#CLEAN JOINT
	for axe in ['X','Y','Z']:
		mc.setAttr( '{}.jointOrient{}'.format( joint , axe) , 0 )
		mc.setAttr( '{}.rotate{}'.format( joint , axe) , mc.getAttr( '{}.rotate{}'.format( trsfTmp , axe) ) )
	mc.delete( trsfTmp )


def rotationToJointOrient( joint ):
	pass

def rotationToPrefAngle( joint ):
	for axe in ['X','Y','Z']:
		mc.setAttr( '{}.preferredAngle{}'.format( joint , axe) , mc.getAttr( '{}.rotate{}'.format( joint , axe) ) )


def buildConeGeometry( masters , coneGeometryName = "cone_GEO" , attrsShape = [] , attrsColor = [] ):

	# BUILD CONE
	circleStart = coneGeometryName + "ConeCrvSTART"
	circleEnd   = coneGeometryName + "ConeCrvEnd"
	circleStartOut = mc.circle( n = circleStart , nr = ( 1 , 0 , 0 ) , c = (0, 0, 0) )				
	circleEndOut   = mc.circle( n = circleEnd   , nr = ( 1 , 0 , 0 ) , c = (0, 0, 0) )

	mc.delete(mc.parentConstraint( masters[0] , circleStart ))
	mc.delete(mc.parentConstraint( masters[1] , circleEnd   ))

	mc.parent( circleStart , masters[0] )
	mc.parent( circleEnd   , masters[0] )

	mc.loft( circleStart , circleEnd , n = coneGeometryName ,  constructionHistory =  1 , uniform =  1 , close = 0 , autoReverse = 1 , degree = 3 , sectionSpans = 1 , range = 0 , polygon = 0 , reverseSurfaceNormals = True )

	mc.connectAttr(  attrsShape[0] , circleStartOut[1] + '.radius' )
	mc.connectAttr(  attrsShape[1] , circleEndOut[1]   + '.radius' )

	#CREATE LAMBERT
	lambertName     = coneGeometryName + '_lambert'		
	mc.shadingNode( 'lambert' , n = lambertName , asShader=True )
	shadingGrp = mc.sets( renderable=True , noSurfaceShader=True , empty=True )
	mc.connectAttr( lambertName + '.outColor'   , shadingGrp + '.surfaceShader' )
	setShaderToObj( lambertName , coneGeometryName )

	#CREATE LAMBERT NODE NETWORK
	reverseName     = coneGeometryName + '_reverse'
	layerShaderName = coneGeometryName + '_layerShader'		
	rampShaderName  = coneGeometryName + '_rampShader'	
	rampName        = coneGeometryName + '_ramp'	

	reverseName     = mc.createNode( 'reverse'        , n = reverseName     )
	layerShaderName = mc.createNode( 'layeredTexture' , n = layerShaderName )
	rampShaderName  = mc.createNode( 'rampShader'     , n = rampShaderName  )
	rampName        = mc.createNode( 'ramp'           , n = rampName        )
	
	mc.connectAttr( reverseName     + '.output'   , lambertName + '.transparency',  force = True ) 
	mc.connectAttr( layerShaderName + '.outColor' , reverseName + '.input'       ,  force = True )		

	mc.connectAttr( attrsColor[1] , lambertName + '.colorR',  force = True )	
	mc.connectAttr( attrsColor[2] , lambertName + '.colorG',  force = True )	
	mc.connectAttr( attrsColor[3] , lambertName + '.colorB',  force = True )	

	mc.connectAttr(  rampName       + '.outColor'  , layerShaderName + '.inputs[0].color' ,  force = True )
	mc.connectAttr(  rampShaderName + '.outColor'  , layerShaderName + '.inputs[1].color' ,  force = True )

	mc.connectAttr(  attrsColor[0] ,( rampName + ".colorEntryList[0].colorR" ) , force = True )
	mc.connectAttr(  attrsColor[0] ,( rampName + ".colorEntryList[0].colorG" ) , force = True )
	mc.connectAttr(  attrsColor[0] ,( rampName + ".colorEntryList[0].colorB" ) , force = True )


	# SET SHADER
	mc.setAttr( layerShaderName + '.inputs[0].blendMode' , 6 )		
	
	mc.setAttr( rampName + '.type'                       , 0          )
	
	mc.setAttr( rampName + '.colorEntryList[0].position' , 0.0557276  )
	
	
	mc.setAttr( rampName + '.colorEntryList[1].position' , 1  )
	mc.setAttr( rampName + '.colorEntryList[1].colorR'   , 0  )
	mc.setAttr( rampName + '.colorEntryList[1].colorG'   , 0  )
	mc.setAttr( rampName + '.colorEntryList[1].colorB'   , 0  )
	
	mc.setAttr( rampShaderName + '.color[0].color_Position' , 1 )
	mc.setAttr( rampShaderName + '.color[1].color_Interp'   , 1 )
	mc.setAttr( rampShaderName + '.color[0].color_ColorR'   , 1 )
	mc.setAttr( rampShaderName + '.color[0].color_ColorG'   , 1 )
	mc.setAttr( rampShaderName + '.color[0].color_ColorB'   , 1 )
	
	mc.setAttr( rampShaderName + '.color[1].color_Position' , 0.530435 )
	mc.setAttr( rampShaderName + '.color[1].color_Interp'   , 1        )		
	mc.setAttr( rampShaderName + '.color[1].color_ColorR'   , 0        )		
	mc.setAttr( rampShaderName + '.color[1].color_ColorG'   , 0        )
	mc.setAttr( rampShaderName + '.color[1].color_ColorB'   , 0        )

	mc.setAttr( ( lambertName + ".ambientColorR" ) , 1 )
	mc.setAttr( ( lambertName + ".ambientColorG" ) , 1 ) 
	mc.setAttr( ( lambertName + ".ambientColorB" ) , 1 )

	mc.setAttr( circleStart + ".visibility" , 0 )
	mc.setAttr( circleEnd  + ".visibility"  , 0 )



	return coneGeometryName



def convertConstraintToParent( objs ):

	for obj in objs: 
		masters = getConstraintMasters( obj , constraintTypesFilter = [ 'parentConstraint' , 'scaleConstraint'  ] , deleteConstraint = 1 )
		safeParent( obj , masters[0] )


def convertConstraintToSkin( objs ):
	
	vectexCount = []
	joints      = []
	for i in range( len(objs) ):
		contraints = getConstraintMasters( objs[i] , constraintTypesFilter = [ 'parentConstraint' , 'scaleConstraint'  ] , deleteConstraint = 1 )
		if( len(contraints) == 0 ):mc.error( 'convertConstraintToSkin: no constraint on --> {} '.format(objs[i]) )
		joints.append( contraints[0] )
		vectexCount.append( mc.polyEvaluate(  objs[i] , v = True ) )		

	if( len(objs) == 1 ): newMesh = objs[0]
	else:                 newMesh = mc.polyUnite( objs )[0]
	mc.DeleteHistory(newMesh)	

	mc.select( joints )
	skinClusterNode = mc.skinCluster( joints,  newMesh , normalizeWeights = 1 , ignoreHierarchy = True , includeHiddenSelections = True , maximumInfluences = 4 , toSelectedBones = True )[0]

	currentVtx = 0
	vertJointWeightData = []
	for i in range( len(objs)):
		for j in range( currentVtx , currentVtx + vectexCount[i] ):
			vertJointWeightData.append(    ( '{}.vtx[{}]'.format(newMesh,j) , [(joints[i], 1.0)] )    )
		currentVtx += vectexCount[i]

	utilsMayaApi.setSkinWeights( skinClusterNode, vertJointWeightData )	

	return newMesh




#rebindWithIncrMesh( 'base_male_body' )

def rebindWithIncrMesh( skinnedMeshBaseName ):
	skinnedMesh = mc.ls( skinnedMeshBaseName + "*" , type = "transform" )[-1]
	shape = mc.listRelatives( skinnedMesh , c = True , s = True )[0]
	skinClusterNode = mc.listConnections( shape + '.inMesh' , s = True , d = False )[0]
	joints = mc.listConnections( skinClusterNode + '.matrix' , s = True , d = False , type = 'joint' )
	
	mc.setAttr( skinClusterNode + '.envelope' , 0 )
	newMesh = mc.duplicate( skinnedMesh )[0]
	mc.select( joints )
	mc.skinCluster( joints,  newMesh , toSelectedBones = True )
	mc.copySkinWeights( skinnedMesh , newMesh , noMirror = True , surfaceAssociation = 'closestPoint' , influenceAssociation  = 'closestJoint' )   
	mc.setAttr( skinnedMesh + '.visibility' , 0 )


'''
import maya.cmds as mc
from python.utils.utilsMaya import *

name = 'toto'
jointToCompare = 'joint2'
axeToMeasure = 0 
createPoseDeformer( name , jointToCompare , axeToMeasure )
'''

def createPoseDeformer( name , jointToCompare , axeToMeasure ):
		
	#BUILD DAG
	grp = dagSafeBuild(       'transform' , name + '_GRP'           , '' )
	ref = dagSafeBuild(       'transform' , name + 'JointRef'       , grp )
	loc = dagSafeBuild(       'locator'   , name                    , grp )
	refMesure = dagSafeBuild( 'transform' , name + 'JointRefMesure' , grp )
	locMesure = dagSafeBuild( 'transform' , name + 'Mesure'         , grp )
	
	#BUILD POS    
	axis = ['X','Y','Z']
	axe = 'X'
	value = 1
	if( 2 < axeToMeasure ):
	    axeToMeasure -= 3
	    value *= -1
	
	mc.setAttr( '{}.translate{}'.format(refMesure,axis[axeToMeasure]) , value )
	mc.setAttr( '{}.translate{}'.format(locMesure,axis[axeToMeasure]) , value )
	 
	#BUILD ATTR
	deltaAttr = addSpecialAttr( loc , 'delta' , 'float' , 0 , attrKeyable = True , attrCb  = True)
	outAttr   = addSpecialAttr( loc , 'out'   , 'float' , 0 , attrKeyable = True , attrCb  = True)
	
	#BUILD LINK
	mc.parentConstraint( ref , refMesure , mo = True )
	mc.parentConstraint( loc , locMesure , mo = True )
	
	angleBetweenNode = mc.createNode("angleBetween")
	mc.connectAttr( refMesure + '.translate' , angleBetweenNode + ".vector1")
	mc.connectAttr( locMesure + '.translate' , angleBetweenNode + ".vector2")
	
	mc.connectAttr( angleBetweenNode + '.angle' , deltaAttr)
	
	angle = 20
	mc.setDrivenKeyframe( outAttr , cd = deltaAttr , v = 0 , dv = angle ) 
	mc.setDrivenKeyframe( outAttr , cd = deltaAttr , v = 1 , dv = 0 ) 
	
	#SETUP
	mc.delete(mc.parentConstraint( jointToCompare , grp))
	father = mc.listRelatives( jointToCompare , p = True )
	if not( father == None ): safeParent( grp , father[0] )
	
	mc.orientConstraint( jointToCompare , ref)
	    


#safeDuplicateMesh('hookPlug_GEO')

def safeDuplicateMesh( name , n = None):
	newObj = mc.duplicate(name)[0]
	#FIX OBJ SHADER ASSIGNEMENT
	shapes = mc.listRelatives( name , c = True , s = True )
	newShapes = mc.listRelatives( newObj , c = True , s = True )


	shadingEngines = mc.ls( type = 'shadingEngine')
	for inShaderSet in shadingEngines:
		setElements = mc.sets( inShaderSet, q=True )
		if( setElements == None ):continue
		setShapes        = []
		setShapesIndexes = []
		for elem in setElements:
			if( '.' in elem ): 
				setShapes.append( elem.split('.')[0] )
				setShapesIndexes.append( '.' + elem.split('.')[1] )
			else:
				setShapes.append( elem )
				setShapesIndexes.append('')         
		#FIX SETS
		for i in range(0,len(setShapes)):
			if( setShapes[i] == name  ):
				if not( mc.sets( newObj + setShapesIndexes[i] , im = inShaderSet ) ): 
					mc.sets(  newObj + setShapesIndexes[i] , e = True , forceElement = inShaderSet )

	if not(n==None): newObj = mc.rename(newObj, n)
	return [newObj]	



def safeDuplicate( name , n = None):
	if( isMesh(name) ):
		return safeDuplicateMesh(name, n = n )
	else:
		return mc.duplicate(name, n = n )



def getMeshesFromGrps( inList ):

	outMeshes = []
	for elem in inList:
		if( isMesh(elem) ):
			outMeshes.append(elem)
		else:
			outMeshes += getAllChildrenMsh(elem)


	return outMeshes	


def getSelectedAttrs():
	selection    = mc.ls(sl=True)
	selectedAttr = mc.channelBox( 'mainChannelBox' , q= True , selectedMainAttributes = True )

	if( selectedAttr == None )or( selection == None ):
		return []

	objAttrs = []
	for obj in selection:
		for attr in selectedAttr:
			objAttrs.append( obj + '.' + attr )


	return objAttrs
	

def setSceneUnitToMeter():
	mc.currentUnit( linear = 'm' )
	cams = mc.ls(type = 'camera')
	for cam in cams:
		mc.setAttr( cam + '.nearClipPlane' , 0.1 )
		mc.setAttr( cam + '.farClipPlane' , 100 )



def skin_repeatFlood( iter = 300 ):
    for i in range(0,iter):
        mc.artAttrSkinPaintCtx( mc.currentCtx() , e = True , clear = True )



'''
import python.utils.utilsMaya as utilsMaya
utilsMaya.selectUnusualScaleTrsf( "pos_*" , "transform" )
'''


def selectUnusualScaleTrsf( search , type ):
	
	posLoc = mc.ls( search , type = type )
	
	wrongLocs = []
	for loc in posLoc:
		value = 0
		value += mc.getAttr( loc + '.scaleX')
		value += mc.getAttr( loc + '.scaleY')
		value += mc.getAttr( loc + '.scaleZ')
		
		if not( round(value, 1) == 3.0 ):
			wrongLocs.append(loc)
 
	mc.select(wrongLocs)     