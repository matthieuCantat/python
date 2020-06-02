
import math
import maya.cmds as mc
import maya.OpenMaya as om
import maya.api.OpenMaya as ompy




'''

getBarycentre                  ______UTILS_coords  
getBoundingBox                 ______UTILS_coords  
getBBbarycentre                ______UTILS_coords  
getBBscale                     ______UTILS_coords
getCubeCoords                  ______UTILS_coords
rotateCoords                   ______UTILS_coords
transformCoords                ______UTILS_coords

convertTripleVecteurToEulerRot ______UTILS_API
offsetEulerRot                 ______UTILS_API
convertTRSValueToMMatrix       ______UTILS_API
convertTRSvalueUnderParent     ______UTILS_API
setUpAxis                      ______UTILS_API


addInSet                       ______UTILS_Maya
getConstraintSlaves            ______UTILS_Maya
findPivot                      ______UTILS_maya
findMasterConstraint           ______UTILS_maya
findManipMaster                ______UTILS_maya
isManip                        ______UTILS_maya
isMesh                         ______UTILS_maya
isManipSlave                   ______UTILS_maya
isGroupMesh                    ______UTILS_maya
getAllChildrenMsh              ______UTILS_maya
incrIfExist                    ______UTILS_maya

setTRSValueToObj               ______UTILS_MayaAttr
writeStringAttr                ______UTILS_MayaAttr

removeComponentSuffix          ______UTILS_string
getBaseName                    ______UTILS_string
sortAndRemoveDupli             ______UTILS_string
convertToString                ______UTILS_string
convertStringToArrayValue      ______UTILS_string
array_flatTo3by3               ______UTILS_string
getComponentIndex              ______UTILS_string
extractIndex                   ______UTILS_string

TRSValue_resetScaleTo1         ______UTILS_TRS
TRSValue_extractRotate         ______UTILS_TRS
TRSValue_ModifRotate           ______UTILS_TRS
TRSValue_setUpAxis             ______UTILS_TRS_API


createManipShape               ______UTILS_mayaManip
buildManipBase                 ______UTILS_mayaManip
contraintManipToSlaves         ______UTILS_mayaManip
connectVisManipToSlaves        ______UTILS_mayaManip
createAllConstraintGrp         ______UTILS_mayaManip



'''





#=========================================================================================================================================================================================
#======================================================================================================================================================================      MATH    =====
#=========================================================================================================================================================================================
	

	
#_______________________________________________________________________________________________________________________________________________________________________  get barycentre	

def getBarycentre( coords ):
	
	i = 0
	
	barycentre = [ 0 , 0 , 0 ]
	
	for c in coords:
		barycentre[0] += c[0] 
		barycentre[1] += c[1]
		barycentre[2] += c[2]
		i += 1
		
	barycentre[0] /= i
	barycentre[1] /= i
	barycentre[2] /= i					
	
		
	return barycentre

	
#_______________________________________________________________________________________________________________________________________________________________________  get Bounding Box	

def getBoundingBox( coords ):
	
	x , y , z = [] , [] , []
	
	for i in range( 0 , len( coords ) , 3 ):
		x.append( coords[ i + 0 ] )
		y.append( coords[ i + 1 ] )		
		z.append( coords[ i + 2 ] )
		
	x.sort()		
	y.sort()		
	z.sort()	

	minMaxCoords = [ x[0] , y[0] , z[0] , x[-1] , y[-1] , z[-1] ]

	return minMaxCoords
	      
	
#_______________________________________________________________________________________________________________________________________________________________________  get BB barycentre	

def getBBbarycentre( coords ):
	
	bbCoords = getBoundingBox( coords )		
	
	barycentre = [  ( ( bbCoords[3] + bbCoords[0] ) / 2 ) , ( ( bbCoords[4] + bbCoords[1] ) / 2 ) , ( ( bbCoords[5] + bbCoords[2] ) / 2 )  ]	
		
	return barycentre


#_______________________________________________________________________________________________________________________________________________________________________  get BB scale	
	
	
def getBBscale( coords ):
	
	bbCoords = getBoundingBox( coords )		
	
	barycentre = [   ( bbCoords[3] - bbCoords[0] )  , ( bbCoords[4] - bbCoords[1] )  , (  bbCoords[5] - bbCoords[2] )  ]	
		
	return barycentre



	
#_______________________________________________________________________________________________________________________________________________________________________  get Cube Coords	

def getCubeCoords( offset ):
	
	cubeCoords = [ [-0.5,-0.5,-0.5] , [0.5,-0.5,-0.5] , [0.5,-0.5,0.5] , [-0.5,-0.5,0.5] , [-0.5,0.5,-0.5] , [0.5,0.5,-0.5] , [0.5,0.5,0.5] , [-0.5,0.5,0.5]  ]  # <---- ordre a revoir
	
	cubeCoords = transformCoords( cubeCoords , [ 0 , 0 , 0 ]  , offset , 'XYZ'  )
	
	return cubeCoords
		

#_______________________________________________________________________________________________________________________________________________________________________  rotate Coords		


def rotateCoords( coords , piv , axe , value ):
 
	
	dicoAxe  = { 'X' : [ 1 , 2 , 0 ]  ,  'Y' : [ 0 , 2 , 1 ]   ,  'Z' : [ 0 , 1 , 2 ] }	
	i = dicoAxe[ axe ]	
	
	if( axe == 'Y' ):
		value *= -1    
		
	# calcule Rot		
		
	rotRad = math.radians(value)
	
	newVertexCoords = []
	
	for coord in coords:
		
		newCoord = [ 0 , 0 , 0 ]
		
		newCoord[ i[0] ] = math.cos( rotRad ) * ( coord[i[0]] - piv[i[0]] )     -     math.sin( rotRad ) * ( coord[i[1]] - piv[i[1]] )     +     piv[i[0]]        
		newCoord[ i[1] ] = math.sin( rotRad ) * ( coord[i[0]] - piv[i[0]] )     +     math.cos( rotRad ) * ( coord[i[1]] - piv[i[1]] )     +     piv[i[1]]              
		newCoord[ i[2] ] = coord[i[2]] 
		
		newVertexCoords.append( newCoord )
		
		    
	return newVertexCoords

		                                                                                                                                                                                              
#_______________________________________________________________________________________________________________________________________________________________________  transform Coords			
	

	

def transformCoords( coords , center , offsets , rotateOrder ):


	# scale
	
	for i in range( 0 , len( coords ) ):
		coords[i][0] =   coords[i][0] * offsets[6]
		coords[i][1] =   coords[i][1] * offsets[7]
		coords[i][2] =   coords[i][2] * offsets[8]


	# rotate 
	
	for i in range( 0 , 3 ):
		coords = rotateCoords( coords , center , rotateOrder[i] , offsets[ 3 + i ]  )			
		
	# translate	
		
	for i in range( 0 , len( coords ) ):
		coords[i][0] =   coords[i][0] + offsets[0]
		coords[i][1] =   coords[i][1] + offsets[1]
		coords[i][2] =   coords[i][2] + offsets[2]	
		
	
	return coords                                                                                                                                                                                  
	
	
	
#=========================================================================================================================================================================================
#======================================================================================================================================================================   MATH MAYA  =====
#=========================================================================================================================================================================================

#_______________________________________________________________________________________________________________________________________________________________________  convert Triple Vecteur To Euler Rot	


def convertTripleVecteurToEulerRot( vX , vY , vZ):

	vecteurX = om.MVector( vX[0] , vX[1] , vX[2]  )
	vecteurY = om.MVector( vY[0] , vY[1] , vY[2]  )
	vecteurZ = om.MVector( vZ[0] , vZ[1] , vZ[2]  )	
	
	vecteurX.normalize()	
	vecteurY.normalize()
	vecteurZ.normalize()	
		
	matrixValues = ( vecteurX.x , vecteurX.y , vecteurX.z , 0 , vecteurY.x , vecteurY.y , vecteurY.z , 0 , vecteurZ.x , vecteurZ.y , vecteurZ.z , 0 , 0 , 0 , 0 , 0 )
	matrix = om.MMatrix()
	
	matrix_util = om.MScriptUtil()
	matrix_util.createMatrixFromList( matrixValues , matrix ) 	
	
	matrixTrsf = om.MTransformationMatrix(matrix)

	rotEuler = matrixTrsf.eulerRotation( )	

	rotXYZ = [ rotEuler.x , rotEuler.y , rotEuler.z ]
	
	#conversion en degres
	
	for i in range( 0 , 3):
		rotXYZ[i] = ( rotXYZ[i] / ( 2 * 3.14 ) ) * 360

	                                                                                                                                                                                                                                                                                                                                                   
	return rotXYZ	
	


	
#_______________________________________________________________________________________________________________________________________________________________________  offset Euler Rot	
		
		
def offsetEulerRot( oldRot , rotOrder , offset ):
        
	
	radOldRot    =  [  math.radians( oldRot[0]  ) , math.radians( oldRot[1]  )  , math.radians( oldRot[2]  )   ]			
	radOffset    =  [  math.radians( offset[0]  ) , math.radians( offset[1]  )  , math.radians( offset[2]  )   ]				
	
	axis         =  [   om.MVector( 1 , 0 , 0 )   ,   om.MVector( 0 , 1 , 0 )   ,   om.MVector( 0 , 0 , 1 )    ]

	# rotate Wold Axis whith oldRot
		
	eulerRotInit =  om.MEulerRotation(   radOldRot[0]  ,  radOldRot[1]  ,  radOldRot[2]  ,  om.MEulerRotation.kXYZ   )
	
	rotatedAxisRef  =  [   axis[0].rotateBy( eulerRotInit )  ,   axis[1].rotateBy( eulerRotInit )  ,   axis[2].rotateBy( eulerRotInit )   ]
	
	vAxis = rotatedAxisRef                                                                                
	
	# apply Offset
	
	quatOffset  = [  om.MQuaternion( radOffset[0] , rotatedAxisRef[0]  )  ,  om.MQuaternion( radOffset[1] , rotatedAxisRef[1] )  ,  om.MQuaternion( radOffset[2] , rotatedAxisRef[2]  )  ]		
	
	for quat in quatOffset:
		vAxis[0] = vAxis[0].rotateBy( quat ) 
		vAxis[1] = vAxis[1].rotateBy( quat ) 
		vAxis[2] = vAxis[2].rotateBy( quat )
		
	
	vX = [ vAxis[0].x , vAxis[0].y  , vAxis[0].z ]
	vY = [ vAxis[1].x , vAxis[1].y  , vAxis[1].z ]
	vZ = [ vAxis[2].x , vAxis[2].y  , vAxis[2].z ]
	
	eulerRotOffset = convertTripleVecteurToEulerRot( vX  , vY , vZ )
	
	
	return eulerRotOffset


	
#=========================================================================================================================================================================================
#======================================================================================================================================================================      MAYA    =====
#=========================================================================================================================================================================================	
	

#_______________________________________________________________________________________________________________________________________________________________________  add In Set	


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


	
#______________________________________________________________________________________________________________________________________________________________________ get Constraint Slaves	
	
def getConstraintSlaves( trsf , constraintType , deleteConstraint ):
	
	slaveTrsfs = []
	
	
	# constraint
	constraintes = mc.listConnections( trsf + '.parentMatrix[0]' , s = False , d = True )
		
	if( constraintes == None ):
	    return slaveTrsfs	
	
	    
	# type of constraint    
	    
	matchTypeConstraintes = []
	
	for constrainte in constraintes:
	
		nType = mc.nodeType( constrainte )
		
		if nType == constraintType :
			matchTypeConstraintes.append( constrainte )
							
	if( matchTypeConstraintes == None ):
	    return slaveTrsfs
		
	# name slave  		    
	    
	for matchTypeConstrainte in matchTypeConstraintes :
		slaveTrsf = mc.listConnections( matchTypeConstrainte + '.constraintParentInverseMatrix' , s = True , d = False ) 
		slaveTrsfs.append( slaveTrsf[0] )

	slaveTrsfs = sortAndRemoveDupli( slaveTrsfs )	
		
	# delete constraint ?  		
	
	if( deleteConstraint == 1 ):
		mc.delete(matchTypeConstraintes)
                                                                                                                                

	return slaveTrsfs

			 
	
#______________________________________________________________________________________________________________________________________________________________________ set TRS Value

def setTRSValueToObj( obj  , TRSvalue ):
		
	axes = [ 'X' , 'Y' , 'Z' ]
	
	
	for i in range( 0 , 3 ):
		 mc.setAttr( obj + ( '.translate' + axes[i] )    , TRSvalue[i    ] )
		 mc.setAttr( obj + ( '.rotate'    + axes[i] )    , TRSvalue[i + 3]    )
		 mc.setAttr( obj + ( '.scale'     + axes[i] )    , TRSvalue[i + 6]     )	

 
    	
		        		
	
#_______________________________________________________________________________________________________________________________________________________________________  write String Attr			


def writeStringAttr( master, attrName ,  value ):
				
	mAttr = master +'.'+ attrName 
	
	if not( mc.objExists( mAttr ) ):
		mc.addAttr(  master     ,  ln = attrName , dt = "string"  )		
		mc.setAttr(  mAttr  ,  value   , type = "string" , l = True ) 
		return 1
		
	mc.setAttr(  mAttr  ,  l = False ) 
	mc.setAttr(  mAttr  ,  value   , type = "string" , l = True ) 
					
	return 1			
	

	
#=========================================================================================================================================================================================
#========================================================================================================================================================================    STRING    ===
#=========================================================================================================================================================================================	
		
#_______________________________________________________________________________________________________________________________________________________________________  get Base Name	

def removeComponentSuffix( obj ):

	if( "." in obj ):
		obj = obj.split(".")[0]   	
		

	return obj
		
#_______________________________________________________________________________________________________________________________________________________________________  clean Base Name	

def getBaseName( obj ):

	# prefix
	baseName =      obj.replace( "RIG:BDD:" , "")
	# suffix	
	baseName = baseName.replace( "_loc" , "")		
	baseName = baseName.replace( "_msh" , "")
	baseName = baseName.replace( "_ctrl" , "")			
	baseName = baseName.replace( "_grp" , "")
	baseName = baseName.replace( "_hi" , "")
	baseName = baseName.replace( "_rlo" , "")		
	return baseName		
	
	
#_______________________________________________________________________________________________________________________________________________________________________  sortAndRemoveDupli 	
	                                                                                                                            

def sortAndRemoveDupli( input):
    
  output = []
  
  for x in input:
    if x not in output:
      output.append(x)
      
  output.sort()
  
  return output	


#_______________________________________________________________________________________________________________________________________________________________________  convert To String 

def convertToString( variable ):
	
		
	if not( type(variable) == list ):
		return str(variable)
		
	stringArray = []		
		
	for elem in variable :
		if( type( elem ) == list ):
			for e in elem :
				stringArray.append( str(e) )	
		else:
			stringArray.append( str(elem) )			
	

	catenateVar = " ".join( stringArray ) 		
	
	
	return catenateVar	
	
#_______________________________________________________________________________________________________________________________________________________________________  convert String To Value

def convertStringToArrayValue( string ):

	array = string.split( ' ' )	
	numElem = [ '0' , '1' , '2' , '3' , '4' , '5' , '6' , '7' , '8' , '9' , '.' , '-' , 'e' ]
	
	
	numArray = []

	if( array[0] == '' ):
		return [''] 	
		
	if( len(array) == 1 ):
		elem = array[0]
		
		for e in elem:
			if not( e in numElem ):
				return [elem]
				
		return [float( elem )]
		
	else:
		
		for elem in array:
			for e in elem:
				if not( e in numElem ):
					return array
		
		
		for elem in array:
			numArray.append( float( elem ) )		
					
	return numArray
	
#__________________________________________________________________________________________________________________________________          array Flat To 3by3 


def array_flatTo3by3( flatArray ):	
	
	array3by3 = []
	tmp       = []	
	
	for e in flatArray:
		tmp.append( e )
		if( len( tmp ) == 3 ):
			array3by3.append( tmp )
			tmp = []

	return array3by3	

	
	
	
#__________________________________________________________________________________________________________________________________          set Up Axis	
	

def setUpAxis( rotValue , axis ):
	
 		
	if( axis == 'X' ):
		rotValue = offsetEulerRot( rotValue , 'XYZ' , [ 0 , 0 , 90 ] )
	
	elif( axis == 'Z' ):
		rotValue = offsetEulerRot( rotValue , 'XYZ' , [ -90 , 0 , 0 ] )		

		
	return rotValue 	


#__________________________________________________________________________________________________________________________________          TRSValue_resetScaleTo1

def TRSValue_resetScaleTo1( TRSValueTrsf ):

	TRSValueTrsf[6:9]  =  [ 1 , 1 , 1 ]
	
	return TRSValueTrsf 	
	
	

def TRSValue_extractRotate( TRSValueTrsf ):

	rotateValue = [ TRSValueTrsf[3] , TRSValueTrsf[4] , TRSValueTrsf[5] ]
	
	return rotateValue	


def TRSValue_ModifRotate( TRSValueTrsf , rotateValue ):

	TRSValueTrsf[3:6] = [ rotateValue[0] , rotateValue[1] , rotateValue[2] ] 	
	
	return TRSValueTrsf	

	
def TRSValue_setUpAxis( TRSValueTrsf , axis ):

	rotateValue  = TRSValue_extractRotate( TRSValueTrsf )
	rotateValue  = setUpAxis( rotateValue , axis )
	TRSValueTrsf = TRSValue_ModifRotate( TRSValueTrsf , rotateValue )
		
	return TRSValueTrsf	
	
		
#__________________________________________________________________________________________________________________________________          find Pivot

def findPivot( obj ):
	
	pivObj     = mc.xform( obj , q = True , piv = True , ws =  True )
	
	return pivObj  
		  
	
	
#__________________________________________________________________________________________________________________________________         getComponentIndex

def getComponentIndex( selectionVtx ):
	
	vIndex = []
	vIndexExpend = []
	
	for elem in selectionVtx:
		if( '[' in elem  ) and ( ']' in elem  ) and ( ':' in elem  ):
			
			vIndexExpend = mc.filterExpand( elem , ex = True , sm = 31 )
			for v in vIndexExpend:
				vIndex.append( extractIndex(v) )	
				
		elif( '.vtx' in elem  ):
			vIndex.append( extractIndex(elem) )		

						
			
	return vIndex
	
    
#__________________________________________________________________________________________________________________________________          extract Index

	
def extractIndex( name ):

	iA = name.find('[') + 1
	iB = name.find(']') 
	
	index = name[ iA : iB ]
	
	return int(index)
	
		
#__________________________________________________________________________________________________________________________________          findMaster Constraint

def findMasterConstraint( obj ):
	
	constraintParentNode = mc.listConnections( ( obj + '.parentInverseMatrix[0]' ) , s = False , d = True )
	
	if( constraintParentNode  == None ):
		return ''
		
	
	masters = mc.listConnections( ( constraintParentNode[0] + '.target[0].targetParentMatrix' ) , s = True , d = False )
	
	return masters[0]
	
	
	
	
#__________________________________________________________________________________________________________________________________          createManipShape	

def createManipShape( parentName , shapeName , type , iColor , offsets , shapeAxe ):
	    
	pos = []
	degree = 1
					                                               
	if( type ==                                          'ArrowA'):   
		                                       
		pos.append( [  0       ,   0       ,   1       ] )
		pos.append( [  0.334   ,   0       ,   0.668   ] )
		pos.append( [  0.167   ,   0       ,   0.668   ] )
		pos.append( [  0.167   ,   0       ,  -1       ] )
		pos.append( [ -0.167   ,   0       ,  -1       ] )
		pos.append( [ -0.167   ,   0       ,   0.668   ] )
		pos.append( [ -0.334   ,   0       ,   0.668   ] )
		pos.append( [  0       ,   0       ,   1       ] )
		
		pos = transformCoords( pos , [ 0 , 0 , 0 ]  , [ 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1 ] , 'XYZ' )		    	
		                                               
	elif( type ==                                         'ArrowB'):  
		                                               
		pos.append( [ -0.334   ,   0       ,   0.668   ] )
		pos.append( [  0       ,   0       ,   1       ] )
		pos.append( [  0.334   ,   0       ,   0.668   ] )
		pos.append( [  0.167   ,   0       ,   0.668   ] )
		pos.append( [  0.167   ,   0       ,  -0.668   ] )
		pos.append( [  0.334   ,   0       ,  -0.668   ] )
		pos.append( [  0       ,   0       ,  -1       ] )
		pos.append( [ -0.334   ,   0       ,  -0.668   ] )
		pos.append( [ -0.167   ,   0       ,  -0.668   ] )
		pos.append( [ -0.167   ,   0       ,   0.668   ] )
		pos.append( [ -0.334   ,   0       ,   0.668   ] )
		
		pos = transformCoords( pos , [ 0 , 0 , 0 ]  , [ 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1 ] , 'XYZ' )		    	
		                                               
	elif( type ==                                          'ArrowC'):   
		                                               
		pos.append( [ -0.6666  ,   0       ,  -0.334   ] )
		pos.append( [ -1.0000  ,   0       ,   0       ] )
		pos.append( [ -0.6666  ,   0       ,   0.334   ] )
		pos.append( [ -0.6666  ,   0       ,   0.167   ] )
		pos.append( [ -0.1666  ,   0       ,   0.167   ] )
		pos.append( [ -0.1666  ,   0       ,   0.668   ] )
		pos.append( [ -0.3333  ,   0       ,   0.668   ] )
		pos.append( [  0       ,   0       ,   1       ] )
		pos.append( [  0.3333  ,   0       ,   0.668   ] )
		pos.append( [  0.1666  ,   0       ,   0.668   ] )
		pos.append( [  0.1666  ,   0       ,   0.167   ] )
		pos.append( [  0.6666  ,   0       ,   0.167   ] )
		pos.append( [  0.6666  ,   0       ,   0.334   ] )
		pos.append( [  1.0000  ,   0       ,   0       ] )
		pos.append( [  0.6666  ,   0       ,  -0.334   ] )
		pos.append( [  0.6666  ,   0       ,  -0.167   ] )
		pos.append( [  0.1666  ,   0       ,  -0.167   ] )
		pos.append( [  0.1666  ,   0       ,  -0.668   ] )
		pos.append( [  0.3333  ,   0       ,  -0.668   ] )
		pos.append( [  0       ,   0       ,  -1       ] )
		pos.append( [ -0.3333  ,   0       ,  -0.668   ] )
		pos.append( [ -0.1666  ,   0       ,  -0.668   ] )
		pos.append( [ -0.1666  ,   0       ,  -0.167   ] )
		pos.append( [ -0.6666  ,   0       ,  -0.167   ] )
		pos.append( [ -0.6666  ,   0       ,  -0.334   ] )
		
		pos = transformCoords( pos , [ 0 , 0 , 0 ]  , [ 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1 ] , 'XYZ' )		    	
		                                               
	elif( type ==                                          'ArrowD'):  
		                                               
		pos.append( [  0.1662  ,   0.2211  ,   0.1670  ] )
		pos.append( [  0.3278  ,   0.1798  ,   0.1670  ] )
		pos.append( [  0.4803  ,   0.1123  ,   0.1670  ] )
		pos.append( [  0.6196  ,   0.0204  ,   0.1670  ] )
		pos.append( [  0.6196  ,   0.0204  ,   0.3340  ] )
		pos.append( [  0.6826  ,  -0.0335  ,   0.2515  ] )
		pos.append( [  0.7414  ,  -0.0929  ,   0.1677  ] )
		pos.append( [  0.7950  ,  -0.1571  ,   0.0838  ] )
		pos.append( [  0.8431  ,  -0.2255  ,   0       ] )
		pos.append( [  0.7950  ,  -0.1571  ,  -0.0838  ] )
		pos.append( [  0.7414  ,  -0.0929  ,  -0.1677  ] )
		pos.append( [  0.6826  ,  -0.0335  ,  -0.2515  ] )
		pos.append( [  0.6196  ,   0.0204  ,  -0.3339  ] )
		pos.append( [  0.6196  ,   0.0204  ,  -0.1669  ] )
		pos.append( [  0.4803  ,   0.1123  ,  -0.1669  ] )
		pos.append( [  0.3278  ,   0.1798  ,  -0.1670  ] )
		pos.append( [  0.1662  ,   0.2211  ,  -0.1669  ] )
		pos.append( [  0.1670  ,   0.1798  ,  -0.3278  ] )
		pos.append( [  0.1670  ,   0.1123  ,  -0.4803  ] )
		pos.append( [  0.1670  ,   0.0204  ,  -0.6196  ] )
		pos.append( [  0.3340  ,   0.0204  ,  -0.6196  ] )
		pos.append( [  0.2515  ,  -0.0335  ,  -0.6826  ] )
		pos.append( [  0.1677  ,  -0.0929  ,  -0.7414  ] )
		pos.append( [  0.0838  ,  -0.1571  ,  -0.7950  ] )
		pos.append( [  0       ,  -0.2255  ,  -0.8431  ] )
		pos.append( [ -0.0838  ,  -0.1571  ,  -0.7950  ] )
		pos.append( [ -0.1677  ,  -0.0929  ,  -0.7414  ] )
		pos.append( [ -0.2515  ,  -0.0335  ,  -0.6826  ] )
		pos.append( [ -0.3339  ,   0.0204  ,  -0.6196  ] )
		pos.append( [ -0.1669  ,   0.0204  ,  -0.6196  ] )
		pos.append( [ -0.1669  ,   0.1123  ,  -0.4803  ] )
		pos.append( [ -0.1669  ,   0.1798  ,  -0.3278  ] )
		pos.append( [ -0.1669  ,   0.2211  ,  -0.1662  ] )
		pos.append( [ -0.3278  ,   0.1798  ,  -0.1669  ] )
		pos.append( [ -0.4803  ,   0.1123  ,  -0.1669  ] )
		pos.append( [ -0.6196  ,   0.0204  ,  -0.1669  ] )
		pos.append( [ -0.6196  ,   0.0204  ,  -0.3339  ] )
		pos.append( [ -0.6826  ,  -0.0335  ,  -0.2515  ] )
		pos.append( [ -0.7414  ,  -0.0929  ,  -0.1677  ] )
		pos.append( [ -0.7950  ,  -0.1571  ,  -0.0838  ] )
		pos.append( [ -0.8431  ,  -0.2255  ,   0       ] )
		pos.append( [ -0.7950  ,  -0.1571  ,   0.0838  ] )
		pos.append( [ -0.7414  ,  -0.0929  ,   0.1677  ] )
		pos.append( [ -0.6826  ,  -0.0335  ,   0.2515  ] )
		pos.append( [ -0.6196  ,   0.0204  ,   0.3340  ] )
		pos.append( [ -0.6196  ,   0.0204  ,   0.1670  ] )
		pos.append( [ -0.4803  ,   0.1123  ,   0.1670  ] )
		pos.append( [ -0.3278  ,   0.1798  ,   0.1670  ] )
		pos.append( [ -0.1662  ,   0.2211  ,   0.1670  ] )
		pos.append( [ -0.1669  ,   0.1798  ,   0.3278  ] )
		pos.append( [ -0.1669  ,   0.1123  ,   0.4803  ] )
		pos.append( [ -0.1669  ,   0.0204  ,   0.6196  ] )
		pos.append( [ -0.3339  ,   0.0204  ,   0.6196  ] )
		pos.append( [ -0.2515  ,  -0.0335  ,   0.6826  ] )
		pos.append( [ -0.1677  ,  -0.0929  ,   0.7414  ] )
		pos.append( [ -0.0838  ,  -0.1571  ,   0.7950  ] )
		pos.append( [  0       ,  -0.2255  ,   0.8431  ] )
		pos.append( [  0.0838  ,  -0.1571  ,   0.7950  ] )
		pos.append( [  0.1677  ,  -0.0929  ,   0.7414  ] )
		pos.append( [  0.2515  ,  -0.0335  ,   0.6826  ] )
		pos.append( [  0.3340  ,   0.0204  ,   0.6196  ] )
		pos.append( [  0.1670  ,   0.0204  ,   0.6196  ] )
		pos.append( [  0.1670  ,   0.1123  ,   0.4803  ] )
		pos.append( [  0.1670  ,   0.1798  ,   0.3278  ] )
		pos.append( [  0.1670  ,   0.2211  ,   0.1662  ] )
		
		pos = transformCoords( pos , [ 0 , 0 , 0 ]  , [ 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1 ] , 'XYZ' )		     	
		                                               
	elif( type ==                                            'ArrowE'):      
		                                               
		pos.append( [  0.167   ,   0.2349  ,   0       ] )
		pos.append( [  0.167   ,   0.2211  ,  -0.1662  ] )
		pos.append( [  0.167   ,   0.1798  ,  -0.3278  ] )
		pos.append( [  0.167   ,   0.1123  ,  -0.4803  ] )
		pos.append( [  0.167   ,   0.0204  ,  -0.6196  ] )
		pos.append( [  0.334   ,   0.0204  ,  -0.6196  ] )
		pos.append( [  0.2515  ,  -0.0335  ,  -0.6826  ] )
		pos.append( [  0.1677  ,  -0.0930  ,  -0.7414  ] )
		pos.append( [  0.0838  ,  -0.1571  ,  -0.7950  ] )
		pos.append( [  0       ,  -0.2256  ,  -0.8431  ] )
		pos.append( [ -0.0838  ,  -0.1571  ,  -0.7950  ] )
		pos.append( [ -0.1677  ,  -0.0930  ,  -0.7414  ] )
		pos.append( [ -0.2515  ,  -0.0335  ,  -0.6826  ] )
		pos.append( [ -0.334   ,   0.0204  ,  -0.6196  ] )
		pos.append( [ -0.167   ,   0.0204  ,  -0.6196  ] )
		pos.append( [ -0.167   ,   0.1123  ,  -0.4803  ] )
		pos.append( [ -0.167   ,   0.1798  ,  -0.3278  ] )
		pos.append( [ -0.167   ,   0.2211  ,  -0.1662  ] )
		pos.append( [ -0.167   ,   0.2349  ,   0       ] )
		pos.append( [ -0.167   ,   0.2211  ,   0.1662  ] )
		pos.append( [ -0.167   ,   0.1798  ,   0.3278  ] )
		pos.append( [ -0.167   ,   0.1123  ,   0.4803  ] )
		pos.append( [ -0.167   ,   0.0204  ,   0.6196  ] )
		pos.append( [ -0.334   ,   0.0204  ,   0.6196  ] )
		pos.append( [ -0.2515  ,  -0.0335  ,   0.6826  ] )
		pos.append( [ -0.1677  ,  -0.0930  ,   0.7414  ] )
		pos.append( [ -0.0838  ,  -0.1571  ,   0.7950  ] )
		pos.append( [  0       ,  -0.2256  ,   0.8431  ] )
		pos.append( [  0.0838  ,  -0.1571  ,   0.7950  ] )
		pos.append( [  0.1677  ,  -0.0930  ,   0.7414  ] )
		pos.append( [  0.2515  ,  -0.0335  ,   0.6826  ] )
		pos.append( [  0.334   ,   0.0204  ,   0.6196  ] )
		pos.append( [  0.167   ,   0.0204  ,   0.6196  ] )
		pos.append( [  0.167   ,   0.1123  ,   0.4803  ] )
		pos.append( [  0.167   ,   0.1798  ,   0.3278  ] )
		pos.append( [  0.167   ,   0.2211  ,   0.1662  ] )
		pos.append( [  0.167   ,   0.2349  ,   0       ] )
		
		pos = transformCoords( pos , [ 0 , 0 , 0 ]  , [ 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1 ] , 'XYZ' )		     	
		                                               
	elif( type ==                                             'Circle'):      
		                                               
		pos.append( [  0.7836  ,   0       ,  -0.7836  ] )
		pos.append( [  0       ,   0       ,  -1.1081  ] )
		pos.append( [ -0.7836  ,   0       ,  -0.7836  ] )
		pos.append( [ -1.1081  ,   0       ,   0       ] )
		pos.append( [ -0.7836  ,   0       ,   0.7836  ] )
		pos.append( [  0       ,   0       ,   1.1081  ] )
		pos.append( [  0.7836  ,   0       ,   0.7836  ] )
		pos.append( [  1.1081  ,   0       ,   0       ] )
		pos.append( [  0.7836  ,   0       ,  -0.7836  ] )
		pos.append( [  0       ,   0       ,  -1.1081  ] )
		pos.append( [ -0.7836  ,   0       ,  -0.7836  ] )
		
		pos = transformCoords( pos , [ 0 , 0 , 0 ]  , [ 0 , 0 , 0 , 0 , 0 , 0 , 0.7 , 0.7 , 0.7 ] , 'XYZ' )
		degree = 3
		                                               
	elif( type ==                                             'Cross'):      
		                                               
		pos.append( [  0       ,   0       ,   1       ] )
		pos.append( [  2       ,   0       ,   3       ] ) 
		pos.append( [  3       ,   0       ,   2       ] )
		pos.append( [  1       ,   0       ,   0       ] )
		pos.append( [  3       ,   0       ,  -2       ] ) 
		pos.append( [  2       ,   0       ,  -3       ] ) 
		pos.append( [  0       ,   0       ,  -1       ] ) 
		pos.append( [ -2       ,   0       ,  -3       ] ) 
		pos.append( [ -3       ,   0       ,  -2       ] ) 
		pos.append( [ -1       ,   0       ,   0       ] ) 
		pos.append( [ -3       ,   0       ,   2       ] ) 
		pos.append( [ -2       ,   0       ,   3       ] ) 
		pos.append( [  0       ,   0       ,   1       ] )
		
		pos = transformCoords( pos , [ 0 , 0 , 0 ]  , [ 0 , 0 , 0 , 0 , 0 , 0 , 0.25 , 0.25 , 0.25 ] , 'XYZ' )		     	
		                                               
	elif( type ==                                            'Cube'):
		                                               
		pos.append( [ -1       ,   1       ,  -1       ] )
		pos.append( [ -1       ,   1       ,   1       ] )
		pos.append( [ -1       ,  -1       ,   1       ] )
		pos.append( [ -1       ,  -1       ,  -1       ] )
		pos.append( [  1       ,  -1       ,  -1       ] )
		pos.append( [  1       ,  -1       ,   1       ] )
		pos.append( [ -1       ,  -1       ,   1       ] )
		pos.append( [ -1       ,  -1       ,  -1       ] )
		pos.append( [ -1       ,   1       ,  -1       ] )
		pos.append( [  1       ,   1       ,  -1       ] )
		pos.append( [  1       ,  -1       ,  -1       ] )
		pos.append( [  1       ,  -1       ,   1       ] )
		pos.append( [  1       ,   1       ,   1       ] )
		pos.append( [ -1       ,   1       ,   1       ] )
		pos.append( [  1       ,   1       ,   1       ] )
		pos.append( [  1       ,   1       ,  -1       ] )
		
		pos = transformCoords( pos , [ 0 , 0 , 0 ]  , [ 0 , 0 , 0 , 0 , 0 , 0 , 0.55 , 0.55 , 0.55 ] , 'XYZ' )		     	
		                                               
	elif( type ==                                           'Cylindre'):         
		                                               
		pos.append( [ -1       ,  -1       ,   0       ] )
		pos.append( [ -1       ,  -0.3333  ,   0       ] )
		pos.append( [ -1       ,   0.3333  ,   0       ] )
		pos.append( [ -1       ,   1       ,   0       ] )
		pos.append( [ -1       ,   1       ,   0       ] )
		pos.append( [ -1       ,   1       ,   0.2612  ] )
		pos.append( [ -0.7836  ,   1       ,   0.7834  ] )
		pos.append( [ -0.2615  ,   1       ,   1       ] )
		pos.append( [  0       ,   1       ,   1       ] )
		pos.append( [  0       ,   1       ,   1       ] )
		pos.append( [  0.2610  ,   1       ,   1       ] )
		pos.append( [  0.7835  ,   1       ,   0.7836  ] )
		pos.append( [  0.9999  ,   1       ,   0.2613  ] )
		pos.append( [  0.9999  ,   1       ,   0       ] )
		pos.append( [  0.9999  ,   0.3333  ,   0       ] )
		pos.append( [  0.9999  ,  -0.3333  ,   0       ] )
		pos.append( [  0.9999  ,  -1       ,   0       ] )
		pos.append( [  0.9999  ,  -1       ,   0       ] )
		pos.append( [  1.0000  ,  -1       ,  -0.2611  ] )
		pos.append( [  0.7835  ,  -1       ,  -0.7835  ] )
		pos.append( [  0.2610  ,  -1       ,  -0.9999  ] )
		pos.append( [ -0.0003  ,  -1       ,  -0.9999  ] )
		pos.append( [  0       ,  -1       ,  -0.9999  ] )
		pos.append( [  0       ,  -0.3333  ,  -0.9999  ] )
		pos.append( [  0       ,   0.3333  ,  -0.9999  ] )
		pos.append( [ -0.0004  ,   1       ,  -0.9999  ] )
		pos.append( [ -0.2615  ,   1       ,  -0.9999  ] )
		pos.append( [ -0.7836  ,   1       ,  -0.7834  ] )
		pos.append( [ -1       ,   1       ,  -0.2611  ] )
		pos.append( [ -1       ,   1       ,   0       ] )
		pos.append( [ -1       ,   0.3333  ,   0       ] )
		pos.append( [ -1       ,  -0.3333  ,   0       ] )
		pos.append( [ -1       ,  -1       ,   0       ] )
		pos.append( [ -1       ,  -1       ,  -0.2611  ] )
		pos.append( [ -0.7836  ,  -1       ,  -0.7834  ] )
		pos.append( [ -0.2615  ,  -1       ,  -0.9999  ] )
		pos.append( [  0       ,  -1       ,  -0.9999  ] )
		pos.append( [  0       ,  -0.3333  ,  -0.9999  ] )
		pos.append( [  0       ,   0.3333  ,  -0.9999  ] )
		pos.append( [ -0.0004  ,   1       ,  -0.9999  ] )
		pos.append( [ -0.0003  ,   1       ,  -0.9999  ] )
		pos.append( [  0.2610  ,   1       ,  -1.0000  ] )
		pos.append( [  0.7835  ,   1       ,  -0.7835  ] )
		pos.append( [  1       ,   1       ,  -0.2611  ] )
		pos.append( [  0.9999  ,   1       ,   0.0001  ] )
		pos.append( [  0.9999  ,   1       ,   0       ] )
		pos.append( [  0.9999  ,   0.3333  ,   0       ] )
		pos.append( [  0.9999  ,  -0.3333  ,   0       ] )
		pos.append( [  0.9999  ,  -1       ,   0       ] )
		pos.append( [  0.9999  ,  -1       ,   0.2613  ] )
		pos.append( [  0.7835  ,  -1       ,   0.7836  ] )
		pos.append( [  0.2610  ,  -1       ,   1       ] )
		pos.append( [ -0.0003  ,  -1       ,   1       ] )
		pos.append( [ -0.0005  ,  -1       ,   1       ] )
		pos.append( [ -0.2615  ,  -1       ,   0.9998  ] )
		pos.append( [ -0.7836  ,  -1       ,   0.7834  ] )
		pos.append( [ -1       ,  -1       ,   0.2612  ] )
		pos.append( [ -1       ,  -1       ,   0       ] )
		pos.append( [ -1       ,  -1       ,   0       ] )
		pos.append( [ -1       ,  -1       ,   0       ] )
		pos.append( [ -1       ,  -1       ,   0.2612  ] )
		pos.append( [ -0.7836  ,  -1       ,   0.7834  ] )
		pos.append( [ -0.2615  ,  -1       ,   1       ] )
		pos.append( [ -0.0005  ,  -1       ,   1       ] )
		pos.append( [  0       ,  -0.3333  ,   1       ] )
		pos.append( [  0       ,   0.3333  ,   1       ] )
		pos.append( [  0       ,   1       ,   1       ] )
		
		pos = transformCoords( pos , [ 0 , 0 , 0 ]  , [ 0 , 0 , 0 , 0 , 0 , 0 , 0.65 , 0.6 , 0.65 ] , 'XYZ' )

		             	                               
	elif( type ==                                              'Loc' ):      
		                                               
		pos.append( [  1       ,   0       ,   0       ] )
		pos.append( [  0       ,   0       ,   0       ] )
		pos.append( [ -1       ,   0       ,   0       ] )
		pos.append( [  0       ,   0       ,   0       ] )
		pos.append( [  0       ,   1       ,   0       ] )
		pos.append( [  0       ,  -1       ,   0       ] )
		pos.append( [  0       ,   0       ,   0       ] )
		pos.append( [  0       ,   0       ,  -1       ] )
		pos.append( [  0       ,   0       ,   1       ] )
		
		pos = transformCoords( pos , [ 0 , 0 , 0 ]  , [ 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1 ] , 'XYZ' )		     	
		                                               
	elif( type ==                                              'Oeil'): 
		       	                                       
		pos.append( [  0       ,   0       ,   4.2535  ] )
		pos.append( [ -0.1541  ,   0       ,   0       ] )
		pos.append( [  0.1541  ,   0       ,   0       ] )
		pos.append( [  0       ,   0       ,   4.2535  ] )
		pos.append( [  0.2907  ,  -0.0875  ,   4.2535  ] )
		pos.append( [  0.2907  ,   0.0875  ,   4.2535  ] )
		pos.append( [  0       ,   0       ,   4.2535  ] )
		pos.append( [  0.0962  ,   0.2907  ,   4.2535  ] )
		pos.append( [ -0.0962  ,   0.2907  ,   4.2535  ] )
		pos.append( [  0       ,   0       ,   4.2535  ] )
		pos.append( [ -0.0962  ,  -0.2907  ,   4.2535  ] )
		pos.append( [  0.0962  ,  -0.2907  ,   4.2535  ] )
		pos.append( [  0       ,   0       ,   4.2535  ] )
		pos.append( [ -0.2907  ,   0.0875  ,   4.2535  ] )
		pos.append( [ -0.2907  ,  -0.0875  ,   4.2535  ] )
		pos.append( [  0       ,   0       ,   4.2535  ] )
		pos.append( [  0.1541  ,   0       ,   0       ] )
		pos.append( [ -0.1541  ,   0       ,   0       ] )
		pos.append( [  0       ,   0       ,   4.2535  ] )
		
		pos = transformCoords( pos , [ 0 , 0 , 0 ]  , [ 0 , 0 , 0 , 0 , 0 , 0 , 0.55 , 0.55 , 0.55 ] , 'XYZ' )		     	
		             	                               
	elif( type ==                                           'Plane' ):   
		                                               
		pos.append( [ -1       ,   0       ,   1       ] )
		pos.append( [ -1       ,   0       ,  -1       ] )
		pos.append( [  1       ,   0       ,  -1       ] )
		pos.append( [  1       ,   0       ,   1       ] )
		pos.append( [ -1       ,   0       ,   1       ] )
		
		pos = transformCoords( pos , [ 0 , 0 , 0 ]  , [ 0 , 0 , 0 , 0 , 0 , 0 , 0.55 , 0.55 , 0.55 ] , 'XYZ' )		     	
		                                               
	elif( type ==                                            'Smiley' ):   
		                                               
		pos.append( [  0.7836  ,   0.7836  ,   0       ] )
		pos.append( [  0       ,   1.1081  ,   0       ] )
		pos.append( [ -0.7836  ,   0.7836  ,   0       ] )
		pos.append( [ -1.1081  ,   0       ,   0       ] )
		pos.append( [ -0.7836  ,  -0.7836  ,   0       ] )
		pos.append( [  0       ,  -1.1081  ,   0       ] )
		pos.append( [  0.7836  ,  -0.7836  ,   0       ] )
		pos.append( [  1.1081  ,   0       ,   0       ] )
		pos.append( [  0.7836  ,   0.7836  ,   0       ] )
		pos.append( [  0       ,   1.1081  ,   0       ] )
		pos.append( [ -0.7836  ,   0.7836  ,   0       ] )
		                                               
		pos.append( [  0.4806  ,  -0.5274  ,   0       ] )
		pos.append( [  0       ,  -0.6160  ,   0       ] )
		pos.append( [ -0.4806  ,  -0.5274  ,   0       ] )
		pos.append( [ -0.7513  ,  -0.1900  ,   0       ] )
		pos.append( [ -0.4806  ,  -0.6337  ,   0       ] )
		pos.append( [  0       ,  -0.8173  ,   0       ] )
		pos.append( [  0.4806  ,  -0.6337  ,   0       ] )
		pos.append( [  0.7513  ,  -0.1900  ,   0       ] )
		pos.append( [  0.4806  ,  -0.5274  ,   0       ] )
		pos.append( [  0       ,  -0.6160  ,   0       ] )
		pos.append( [ -0.4806  ,  -0.5274  ,   0       ] )
		                                                    	                                                                                  
		pos.append( [  0.5261  ,   0.4956  ,   0       ] )
		pos.append( [  0.4132  ,   0.5498  ,   0       ] )
		pos.append( [  0.2278  ,   0.2408  ,   0       ] )
		pos.append( [ -0.0093  ,   0.1827  ,   0       ] )
		pos.append( [  0.0981  ,  -0.0768  ,   0       ] )
		pos.append( [  0.3577  ,  -0.1843  ,   0       ] )
		pos.append( [  0.6303  ,  -0.0132  ,   0       ] )
		pos.append( [  0.6795  ,   0.2772  ,   0       ] )
		pos.append( [  0.5261  ,   0.4956  ,   0       ] )
		pos.append( [  0.4132  ,   0.5498  ,   0       ] )
		pos.append( [  0.2278  ,   0.2408  ,   0       ] )
		                                                    	                                                                                  
		pos.append( [ -0.5261  ,   0.4956  ,   0       ] )
		pos.append( [ -0.4132  ,   0.5498  ,   0       ] )
		pos.append( [ -0.2278  ,   0.2408  ,   0       ] )
		pos.append( [  0.0093  ,   0.1827  ,   0       ] )
		pos.append( [ -0.0981  ,  -0.0768  ,   0       ] )
		pos.append( [ -0.3577  ,  -0.1843  ,   0       ] )
		pos.append( [ -0.6303  ,  -0.0132  ,   0       ] )
		pos.append( [ -0.6795  ,   0.2772  ,   0       ] )
		pos.append( [ -0.5261  ,   0.4956  ,   0       ] )
		pos.append( [ -0.4132  ,   0.5498  ,   0       ] )
		pos.append( [ -0.2278  ,   0.2408  ,   0       ] )
		
		pos = transformCoords( pos , [ 0 , 0 , 0 ]  , [ 0 , 0 , 0 , 0 , 0 , 0 , 0.7 , 0.7 , 0.7 ] , 'XYZ' )
		degree = 3		
		                                               
	elif( type ==                                           'Sphere'):     
		                                               
		pos.append( [  0       ,  -1       ,   0       ] )
		pos.append( [  0       ,  -1       ,  -0.1300  ] )
		pos.append( [  0       ,  -0.9479  ,  -0.3930  ] )
		pos.append( [  0       ,  -0.7254  ,  -0.7254  ] )
		pos.append( [  0       ,  -0.3930  ,  -0.9479  ] )
		pos.append( [  0       ,  -0.1300  ,  -1       ] )
		pos.append( [  0       ,   0       ,  -1       ] )
		pos.append( [ -0.1300  ,   0       ,  -1       ] )
		pos.append( [ -0.3930  ,   0       ,  -0.9479  ] )
		pos.append( [ -0.7254  ,   0       ,  -0.7254  ] )
		pos.append( [ -0.9479  ,   0       ,  -0.3930  ] )
		pos.append( [ -1       ,   0       ,  -0.1300  ] )
		pos.append( [ -1       ,   0       ,   0       ] )
		pos.append( [ -1       ,  -0.1300  ,   0       ] )
		pos.append( [ -0.9479  ,  -0.3930  ,   0       ] )
		pos.append( [ -0.7254  ,  -0.7254  ,   0       ] )
		pos.append( [ -0.3930  ,  -0.9479  ,   0       ] )
		pos.append( [ -0.1300  ,  -1       ,   0       ] )
		pos.append( [  0       ,  -1       ,   0       ] )
		pos.append( [  0.1300  ,  -1       ,   0       ] )
		pos.append( [  0.3930  ,  -0.9479  ,   0       ] )
		pos.append( [  0.7254  ,  -0.7254  ,   0       ] )
		pos.append( [  0.9479  ,  -0.3930  ,   0       ] )
		pos.append( [  1       ,  -0.1300  ,   0       ] )
		pos.append( [  1       ,   0       ,   0       ] )
		pos.append( [  1       ,   0       ,  -0.1300  ] )
		pos.append( [  0.9479  ,   0       ,  -0.3930  ] )
		pos.append( [  0.7254  ,   0       ,  -0.7254  ] )
		pos.append( [  0.3930  ,   0       ,  -0.9479  ] )
		pos.append( [  0.1300  ,   0       ,  -1       ] )
		pos.append( [  0       ,   0       ,  -1       ] )
		pos.append( [  0       ,   0.1300  ,  -1       ] )
		pos.append( [  0       ,   0.3930  ,  -0.9479  ] )
		pos.append( [  0       ,   0.7254  ,  -0.7254  ] )
		pos.append( [  0       ,   0.9479  ,  -0.3930  ] )
		pos.append( [  0       ,   1       ,  -0.1300  ] )
		pos.append( [  0       ,   1       ,   0       ] )
		pos.append( [ -0.1300  ,   1       ,   0       ] )
		pos.append( [ -0.3930  ,   0.9479  ,   0       ] )
		pos.append( [ -0.7254  ,   0.7254  ,   0       ] )
		pos.append( [ -0.9479  ,   0.3930  ,   0       ] )
		pos.append( [ -1.0000  ,   0.1300  ,   0       ] )
		pos.append( [ -1.0000  ,   0       ,   0       ] )
		pos.append( [ -1.0000  ,   0       ,   0.1300  ] )
		pos.append( [ -0.9479  ,   0       ,   0.3930  ] )
		pos.append( [ -0.7254  ,   0       ,   0.7254  ] )
		pos.append( [ -0.3930  ,   0       ,   0.9479  ] )
		pos.append( [ -0.1300  ,   0       ,   1       ] )
		pos.append( [  0       ,   0       ,   1       ] )
		pos.append( [  0.1300  ,   0       ,   1       ] )
		pos.append( [  0.3930  ,   0       ,   0.9479  ] )
		pos.append( [  0.7254  ,   0       ,   0.7254  ] )
		pos.append( [  0.9479  ,   0       ,   0.3930  ] )
		pos.append( [  1       ,   0       ,   0.1300  ] )
		pos.append( [  1       ,   0       ,   0       ] )
		pos.append( [  1       ,   0.1300  ,   0       ] )
		pos.append( [  0.9479  ,   0.3930  ,   0       ] )
		pos.append( [  0.7254  ,   0.7254  ,   0       ] )
		pos.append( [  0.3930  ,   0.9479  ,   0       ] )
		pos.append( [  0.1300  ,   1       ,   0       ] )
		pos.append( [  0       ,   1       ,   0       ] )
		pos.append( [  0       ,   1       ,   0.1300  ] )
		pos.append( [  0       ,   0.9479  ,   0.3930  ] )
		pos.append( [  0       ,   0.7254  ,   0.7254  ] )
		pos.append( [  0       ,   0.3930  ,   0.9479  ] )
		pos.append( [  0       ,   0.1300  ,   1       ] )
		pos.append( [  0       ,   0       ,   1       ] )
		pos.append( [  0       ,  -0.1300  ,   1       ] )
		pos.append( [  0       ,  -0.3930  ,   0.9479  ] )
		pos.append( [  0       ,  -0.7254  ,   0.7254  ] )
		pos.append( [  0       ,  -0.9479  ,   0.3930  ] )
		pos.append( [  0       ,  -1       ,   0.1300  ] )
		pos.append( [  0       ,  -1       ,   0       ] )
		
		pos = transformCoords( pos , [ 0 , 0 , 0 ]  , [ 0 , 0 , 0 , 0 , 0 , 0 , 0.71 , 0.71 , 0.71 ] , 'XYZ' )
		degree = 3		
		
			
	if(   shapeAxe == 2 ):
		pos = transformCoords( pos , [ 0 , 0 , 0 ]  , [ 0 , 0 , 0 , 0  , 0 , 90 , 1 , 1 , 1 ] , 'XYZ' )							
	elif( shapeAxe == 3 ):
		pos = transformCoords( pos , [ 0 , 0 , 0 ]  , [ 0 , 0 , 0 , 90 , 0 , 0  , 1 , 1 , 1 ] , 'XYZ' )			
		
		
	# debut ------------------------get World TRS of parent
	
	locTmp = 'parentTRStmp_loc'
	mc.spaceLocator( n = locTmp )
	attrs = [ 'translateX' , 'translateY' , 'translateZ' , 'rotateX' , 'rotateY' , 'rotateZ' , 'scaleX' , 'scaleY' , 'scaleZ' ]
	
	for i in range( 0 , 9 ):
		mc.setAttr(  ( locTmp + '.' + attrs[i] ) , offsets[i] )
			
	mc.parent( locTmp , parentName )

	invOffsets = []
	for i in range( 0 , 9 ):
		invOffsets.append(    mc.getAttr(  ( locTmp + '.' + attrs[i] )    )      )
	
		
	mc.delete( locTmp )			

	# fin ------------------------get World TRS of parent
	




	pos = transformCoords( pos , [ 0 , 0 , 0 ]  , invOffsets , 'XYZ' )  					
	knot = range( 0 , len( pos ) + ( degree - 1 ) )
	
	
	
	# creation de la shape
			

	nameTmp   = 'curveManip_Tmp' 	
	
	mc.curve( n = nameTmp , d = degree , p = pos , k = knot ) 	
	curveShape = mc.listRelatives( nameTmp , c = 1 , s = 1 )
	mc.rename( curveShape , shapeName )
	
	
	mc.parent( shapeName , parentName , s = True , r = True ) 
	mc.delete( nameTmp )


	# color
	mc.setAttr( ( shapeName + ".overrideEnabled" ) , 1      )
	mc.setAttr( ( shapeName + ".overrideColor" )   , iColor )
	

	
	return shapeName                                                                                     
	                                                                                                                                                                                                  
		
		                                                                                                                                                                                                                                               
#__________________________________________________________________________________________________________________________________          buildManipBase		
	
def buildManipBase(  orig , ctrl , jnt ):
		
	mc.createNode( 'transform' , n = orig ) 
	mc.createNode( 'transform' , n = ctrl )
	
	if not( jnt == '' ):
		jnt  = mc.joint( n = jnt                     )		
		mc.setAttr( ( jnt      +'.radius' ),  0.01   )
	
	mc.addAttr(   ctrl , ln = 'object_display' , min = 0 , max = 1 , dv = 1 , at = 'long' , k = True )			
	mc.setAttr( ( ctrl + '.rotateOrder' ) ,  k = 1  )	
	mc.parent(    ctrl , orig , s = 1 , r = 1  )			                                                                                                                                                                                  
		
	
    
	
#_________________________________________________________________________________________________________________________________________________________________________  contraint Manip To Slave
	


def contraintManipToSlaves(  manip , trsfs ):
	
	for trsf in trsfs:
		mc.parentConstraint( manip , trsf , mo = True  )
		mc.scaleConstraint(  manip , trsf , mo = True  )
		
#_________________________________________________________________________________________________________________________________________________________________________  connectVis Manip To Slaves
		
def connectVisManipToSlaves(  manip , trsfs ):	
	for trsf in trsfs:
		mc.connectAttr(  ( manip + '.object_display' ) , ( trsf + '.visibility') )		
	
		
	
	
	
	
#_________________________________________________________________________________________________________________________________________________________________________  findManipMaster

def findManipMaster( obj ):	
	obj    = removeComponentSuffix( obj )	
	
	#fix bug maya
	
	if( 'Shape' in obj ):
		obj = mc.listRelatives( obj , p = True )[0]
	
	master = findMasterConstraint( obj )
	
	return master	
		
	
#_________________________________________________________________________________________________________________________________________________________________________  is manip		
	
def isManip(  manipName ):
	if( mc.objExists( manipName + '.baseName' ) ):
		return 1
		
	return 0		

	
#______________________________________________________________________________________________________________________________________________________________________ is Mesh

def isMesh( baseName ):
	
	isMesh = 0
	
	baseNameShape = mc.listRelatives( baseName , c = True , s = True )
	
	if not ( baseNameShape == None) and ( len( baseNameShape ) > 0 ):
		baseNameShapeType = mc.nodeType( baseNameShape[0] )
		if( baseNameShapeType == 'mesh' ):
			isMesh = 1

	return isMesh				
	
	
#_________________________________________________________________________________________________________________________________________________________________________  isManipSlave

def isManipSlave( obj ):
	
	master = findManipMaster(obj)	
	if not ( master == '' ):
		if( isManip( master ) ):			
			return 1	

	return 0		

#_________________________________________________________________________________________________________________________________________________________________________  is Group Mesh

def isGroupMesh( obj ):
	

	allMesh = getAllChildrenMsh( obj )
	if( obj in allMesh ):
		allMesh.remove( obj )
	
	if( 0 == len( allMesh ) ):
		return 0	
	else:
		return 1
	

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
			    child = mc.listRelatives( trsf , c = 1)
			    if not(child == None):		    
				    for c in child:
					    childrens.append( c )
			    
		        

		if(10<i):
		    childrens = []
		
	return msh 	
	
	
		
	
	
	
	
#_________________________________________________________________________________________________________________________________________________________________________  createAllConstraintGrp

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
	
	
	
#_______________________________________________________________________________________________________________________________________________________________________ convertTRSValueToMMatrix



	


	
def convertTRSValueToMMatrix( TRSValue ):


	tMatrix = ompy.MTransformationMatrix()
	tMatrix.setTranslation( ompy.MVector( TRSValue[0]  , TRSValue[1] , TRSValue[2] ) , ompy.MSpace.kWorld )
	tMatrix.setRotation( ompy.MEulerRotation( math.radians(TRSValue[3]) , math.radians(TRSValue[4]) , math.radians(TRSValue[5]) )     )
	tMatrix.setScale( [ TRSValue[6] ,TRSValue[7] ,   TRSValue[8]  ]   , ompy.MSpace.kWorld  )
	tMatrix.setShear(   [ 0     ,   0     ,   0  ]   , ompy.MSpace.kWorld   )
	
	
	matrix = tMatrix.asMatrix()

	return matrix 	




#_______________________________________________________________________________________________________________________________________________________________________ convertTRSvalueUnderParent




	
def convertTRSvalueUnderParent( TRSValue , parentTRSValue  ):

	matrixP = convertTRSValueToMMatrix( parentTRSValue )
	matrixP = matrixP.inverse()
	
	matrixG = convertTRSValueToMMatrix( TRSValue )
	
	mChildren = matrixG * matrixP
	
	mtransChildren = ompy.MTransformationMatrix( mChildren )

	translate = mtransChildren.translation( ompy.MSpace.kWorld) 
	rotate    = mtransChildren.rotationComponents()
	scale     = mtransChildren.scale( ompy.MSpace.kWorld)
 	
	childrenTRSValue = [ translate[0] , translate[1] , translate[2] , math.degrees(rotate[0]) , math.degrees(rotate[1]) , math.degrees(rotate[2]) , scale[0] , scale[1] , scale[2] ]	

	return childrenTRSValue


#_______________________________________________________________________________________________________________________________________________________________________ incrIfExist

def incrIfExist( baseName ):
	
	loop = 1
	i = 0
	baseNameModif = baseName	
	while( loop == 1 ):
		
		i+=1
		if( mc.objExists( baseNameModif + '_ctrl' ) ) or ( mc.objExists( baseNameModif + '_ctrl' ) ):
			baseNameModif = baseName + str(i)
		else:
			loop = 0
			newName = baseNameModif 

	return newName
	
	
	
	
	
	