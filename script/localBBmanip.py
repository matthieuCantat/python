import sys
import maya.cmds as mc
import maya.OpenMaya as om   
import maya.mel as mel
import time


#sys.path.append('/u/mcantat/Sandbox/script/localBBpy')
#import localBBoptim5
#reload( localBBoptim5 )

# localBB    ------->   localBBoptim

 
'''

------------------------ UTILS
getAllVertexCoords
getBarycentre
sortAndRemoveDupli
getConstraintSlaves
getSpecifieTypeChildrens
trueIfMsh
getAllChildrenMsh


------------------------ Get INFO FROM UI
getUIrotIndex
getUI_shapeName

------------------------ BUILD SHAPE 
offsetInitManipShape
rotateManipShape
convertToScaleHomothetique
resizeCtrlShape


--------------------- BUILD TRSF
buildCtrlShape
buildManipBase
setManipInHierarchie
addInAnimSet


translateManipTrsf


------------------------ VECTEUR >>>> ORIENTATION

convertTripleVecteurToEulerRot

------------------------ATTR BB COORDS
setBBreelCoordsAttr
getBBreelCoordsAttr

getPositionBBreel
getOrientationBBreel
getScaleBBreel

------------------------HELP Convert
convertBBpointsToString
convertStringToBBpoint

convertElemToVertex
replaceManipBylocTmp
convertLocatorToVertexCoords
contraintManipToSlave
convertVertexMshToMshIndex


------------------------Main proc COMPUTE
computeCreateManip
createManip
switchManipShape

'''
	
#------------------------------------------------------------	
# ------------------------   UTILS   ------------------------
#------------------------------------------------------------	



def getAllVertexCoords(_nameMesh):
 
	# get the active selection
	selection = om.MSelectionList()
	selection.add(_nameMesh)
	iterSel = om.MItSelectionList(selection, om.MFn.kMesh)
 
	# go througt selection
	while not iterSel.isDone():
 
		# get dagPath
		dagPath = om.MDagPath()
		iterSel.getDagPath( dagPath )
 
		# create empty point array
		inMeshMPointArray = om.MPointArray()
 
		# create function set and get points in world space
		currentInMeshMFnMesh = om.MFnMesh(dagPath)
		currentInMeshMFnMesh.getPoints(inMeshMPointArray, om.MSpace.kWorld)
 
		# put each point to a list
		pointList = []
 
		for i in range( inMeshMPointArray.length() ) :
			
			pointList.append( [inMeshMPointArray[i][0], inMeshMPointArray[i][1], inMeshMPointArray[i][2]] )
 
		return pointList



def getBarycentre( *points ):
    
    sizePoints = len( points )    
    bCoords = [ 0.0 , 0.0 , 0.0 ]
    
    for point in points:
        bCoords[0] += point[0]
        bCoords[1] += point[1]
        bCoords[2] += point[2]

    bCoords = [ bCoords[0] / sizePoints , bCoords[1] / sizePoints , bCoords[2] / sizePoints  ]

    return bCoords




	
def sortAndRemoveDupli(_input):
    
  output = []
  
  for x in _input:
    if x not in output:
      output.append(x)
      
  output.sort()
  
  return output

  


  
def getConstraintSlaves( _trsf , _constraintType , _deleteConstraint ):
	
	slaveTrsfs = []
	
	constraintes = mc.listConnections( _trsf + '.parentMatrix[0]' , s = False , d = True )
	matchTypeConstraintes = []
	
	
	if( constraintes == None ):
	    return slaveTrsfs

	
	for constrainte in constraintes:
	
		nType = mc.nodeType( constrainte)
		
		if nType == _constraintType :
			matchTypeConstraintes.append( constrainte )
				
	if( matchTypeConstraintes == None ):
	    return slaveTrsfs
							
	for matchTypeConstrainte in matchTypeConstraintes :
		slaveTrsf = mc.listConnections( matchTypeConstrainte + '.constraintParentInverseMatrix' , s = True , d = False ) 
		slaveTrsfs.append( slaveTrsf[0] )
		
	if( _deleteConstraint == 1 ):
		mc.delete(matchTypeConstraintes)
		
		slaveTrsfs = sortAndRemoveDupli( slaveTrsfs )	

	return slaveTrsfs
  

	
	

def getSpecifieTypeChildrens( _father , _exludedTypes ):

    childrensNoShape = []
        
    childrens = mc.listRelatives( _father , c = True )
    
    #wrongTypes = { 'nurbsCurve' , 'mesh' , 'nurbsSurface' } 
    
    for children in childrens:
        
        type = mc.nodeType( children )
        
        passChildren = 0
                
        for exludedType in _exludedTypes:            
            if( type == exludedType ): 
                passChildren = 1
    
        if( passChildren == 1 ):
            continue
            
        childrensNoShape.append( children )   
            
                       
    return childrensNoShape



    
    	
def trueIfMsh(_elem):
	result = 0
	
	if not( mc.objExists(_elem) ):
		return result
		
	children = mc.listRelatives(_elem, c = 1)
	if(children == None):
		return result
	ntype = mc.nodeType(children[0])	
	if(ntype == 'mesh'):
		result = 1
	return result


	
	
	
def getAllChildrenMsh( _elem ):
	
	msh = []	
	childrens = [_elem]
	
	
	i = 0

	while not(len(childrens) == 0):
		trsfs = childrens
		childrens = []
		i += 1
			
		for trsf in trsfs:
			
			if( trueIfMsh(trsf) ):			
				msh.append( trsf )
			else:
			    child = mc.listRelatives( trsf , c = 1)
			    if not(child == None):		    
				    for c in child:
					    childrens.append( c )
			    
		        

		if(10<i):
		    childrens = []
		
	return msh 	
	
	
	
	
	
	
    
#-----------------------------------------------------------------------	
# ------------------------   Get INFO FROM UI   ------------------------
#-----------------------------------------------------------------------	    
    


	
def getUI_shapeName():
	
	global AM_shapeChoice
	global AM_manipShapeNames
	
	index     = AM_shapeChoice.index( 1 )
	shapeName = AM_manipShapeNames[index] 

	return shapeName 
    
	
	
def getUI_positionManip():

	global  mc_pivotButtonValue
	
	return mc_pivotButtonValue	
	
	
	  
    
#-------------------------------------------------------------------	
# ------------------------   BUILD SHAPE    ------------------------
#-------------------------------------------------------------------	    
    


	
def offsetInitManipShape( _manipTrsf , _shape ):

	#shapeList = ['Cube', 'Sphere', 'Cylindre', 'Loc', 'ArrowA', 'ArrowB', 'ArrowC', 'ArrowD', 'ArrowE', 'Smiley', 'Oeil', 'Plane', 'Circle' ]	
	
	if( _shape == 'Cube' ):
		None				
	elif( _shape == 'Sphere' ):		
		None		
	elif( _shape == 'Cylindre' ):
		mc.setAttr(  ( _manipTrsf + '.rotateZ' ) , 90 )
		None		
	elif( _shape == 'Loc' ):
		None				
	elif( _shape == 'ArrowA' ):
		mc.setAttr(  ( _manipTrsf + '.scaleX' ) , 1.4 )	
		mc.setAttr(  ( _manipTrsf + '.scaleY' ) , 1.4 )	
		mc.setAttr(  ( _manipTrsf + '.scaleZ' ) , 1.4 )			
		mc.setAttr(  ( _manipTrsf + '.rotateZ' ) , 90 )		
		None				
	elif( _shape == 'ArrowB' ):
		mc.setAttr(  ( _manipTrsf + '.scaleX' ) , 1.4 )	
		mc.setAttr(  ( _manipTrsf + '.scaleY' ) , 1.4 )	
		mc.setAttr(  ( _manipTrsf + '.scaleZ' ) , 1.4 )			
		mc.setAttr(  ( _manipTrsf + '.rotateZ' ) , 90 )				
		None				
	elif( _shape == 'ArrowC' ):
		mc.setAttr(  ( _manipTrsf + '.scaleX' ) , 1.4 )	
		mc.setAttr(  ( _manipTrsf + '.scaleY' ) , 1.4 )	
		mc.setAttr(  ( _manipTrsf + '.scaleZ' ) , 1.4 )			
		mc.setAttr(  ( _manipTrsf + '.rotateZ' ) , 90 )				
		None				
	elif( _shape == 'ArrowD' ):
		mc.setAttr(  ( _manipTrsf + '.scaleX' ) , 1.4 )	
		mc.setAttr(  ( _manipTrsf + '.scaleY' ) , 1.4 )	
		mc.setAttr(  ( _manipTrsf + '.scaleZ' ) , 1.4 )				
		mc.setAttr(  ( _manipTrsf + '.rotateZ' ) , 90 )				
		None				
	elif( _shape == 'ArrowE' ):
		mc.setAttr(  ( _manipTrsf + '.scaleX' ) , 1.4 )	
		mc.setAttr(  ( _manipTrsf + '.scaleY' ) , 1.4 )	
		mc.setAttr(  ( _manipTrsf + '.scaleZ' ) , 1.4 )				
		mc.setAttr(  ( _manipTrsf + '.rotateZ' ) , 90 )				
		None				
	elif( _shape == 'Smiley' ):
		None				
	elif( _shape == 'Oeil' ):
		None				
	elif( _shape == 'Plane' ):
		mc.setAttr(  ( _manipTrsf + '.rotateZ' ) , 90 )			
		None				
	elif( _shape == 'Circle' ):
		mc.setAttr(  ( _manipTrsf + '.rotateZ' ) , 90 )			
		None		
		
	mc.makeIdentity( _manipTrsf , a = True , s = True , r = True  )	

	
	
def rotateManipShape( _manipTrsf , rIndex ):


	rIndex = maya.eval()
	
	
	if( rIndex == 0 ):
		mc.setAttr( _manipTrsf + '.rotateX' , 0  )
		None				
	elif( rIndex == 1 ):
		mc.setAttr( _manipTrsf + '.rotateY' , 90  )		
		None		
	elif( rIndex == 2 ):
		mc.setAttr( _manipTrsf + '.rotateX' , 90  )
		mc.setAttr( _manipTrsf + '.rotateZ' , 90  )
		None		
	
		
	mc.makeIdentity( _manipTrsf , a = True , s = True , r = True  )	

	

	
def convertToScaleHomothetique( _scaleXYZ ):
	
	# pour certaine shape , meme valeur scale XYZ 
	#shapeList = ['Cube', 'Sphere', 'Cylindre', 'Loc', 'ArrowA', 'ArrowB', 'ArrowC', 'ArrowD', 'ArrowE', 'Smiley', 'Oeil', 'Plane', 'Circle' ]
	newScale = _scaleXYZ	
	
	shapeName = getUI_shapeName()

	if( ( shapeName == 'Cube' ) or ( shapeName == 'Loc' ) or ( shapeName == 'ArrowC' ) or ( shapeName == 'Plane' ) ): 
		return _scaleXYZ 
	
	newScale.sort()	
	newScale =[ newScale[1] , newScale[1] , newScale[1] ]

	return newScale 
	

	
	
	
def resizeCtrlShape( _ctrlShape , scaleXYZ ):	
	
	ctrlTrsf = mc.listRelatives( _ctrlShape , p = True )
	
	childrens = getSpecifieTypeChildrens( ctrlTrsf[0] , ['nurbsCurve' , 'mesh' , 'nurbsSurface' ]  )

	mc.parent( childrens , w = True)
	
	#axes = [ 'X' , 'Y' , 'Z' ]	( changement d axe car X up )

	axes = [ 'Z' , 'X' , 'Y' ]
	
	scaleXYZ = convertToScaleHomothetique( scaleXYZ )
	
	for i in range( 0 , 3 ):
		 mc.setAttr( ctrlTrsf[0] + ('.scale' + axes[i] ) , scaleXYZ[i] )	
		 
	mc.makeIdentity( ctrlTrsf[0] , a = True , s = True , r = True  )
		
	mc.parent( childrens , ctrlTrsf[0] )

	
	
	
	
#-------------------------------------------------------------------	
# ------------------------   BUILD TRSF    ------------------------
#-------------------------------------------------------------------	    
    	
	


	
def buildCtrlShape( _ctrlTrsf ):
	
	manipTrsfTmp  = 'manipNameTMP'
	mc.createNode( 'transform' , n = manipTrsfTmp )
	
	manipShapeTmp = manipTrsfTmp + 'Shape'
	manipShape = _ctrlTrsf + 'Shape'
	
	shapeName = getUI_shapeName()

	mel.eval( 'AM_med_manipShape( "%s" , "%s" , 0.55 ) ' %( shapeName , manipTrsfTmp) )	
	
	offsetInitManipShape( manipTrsfTmp , shapeName )
	rotateManipShape(manipTrsfTmp)

	
	mc.parent( manipShapeTmp , _ctrlTrsf , s = True , r = True )
	
	mc.select( _ctrlTrsf )	
	mel.eval(' AM_med_ChangeManipColorCB(); ')

	mc.delete( manipTrsfTmp )
	mc.rename( manipShapeTmp , manipShape )	
	
	return manipShape 
	


	
	
def buildManipBase( _trsf , _position , _rotation ):

	# creation du manip
		
	ntrsf = _trsf.replace( "RIG:BDD:" , "") 
	ntrsf = ntrsf.replace( "_msh" , "")
	ntrsf = ntrsf.replace( "_ctrl" , "")
	
	jointCtrl = mc.createNode( 'transform' , n = (ntrsf + "_ctrl") )
	
	# ajout d'attr par defaut

	mc.setAttr( (jointCtrl+'.rotateOrder') , k = 1);	
	mc.addAttr( jointCtrl , ln = 'object_display' , min = 0 , max = 1 , dv = 1, at = 'long' )
	mc.setAttr( (jointCtrl+'.object_display') , e=1 , keyable = True )

	jointSkn = mc.joint( n = (ntrsf + "_skn") )
	mc.setAttr( ( jointSkn +'.radius' ) , 0.01 )
	
	orig = mc.createNode("transform", n = (ntrsf + "_orig") ) 
	mc.parent( jointCtrl , orig , s = 1 , r = 1 , )


	origCtrlJoint = [ orig , jointCtrl , jointSkn ]

	
	#positionnement de l'orig
	
	axes = [ 'X' , 'Y' , 'Z' ]
	
	for i in range( 0 , 3 ):
		 mc.setAttr( origCtrlJoint[0] + ('.translate' + axes[i] ) , _position[i] )
		 mc.setAttr( origCtrlJoint[0] + ('.rotate' + axes[i] )    , _rotation[i] )

	return origCtrlJoint		

	

	




	
def setManipInHierarchie(_trsf , _manip):
	
	AD = 'RIG:ADDITIVE_RIG'	
	root = 'RIG:root' 
	grpRoot = 'all_rootConstrain_grp'; 
	
		
	# creation all_rootConstrain_grp	
	
	if not mc.objExists( grpRoot ):
		mc.createNode('transform' , n = grpRoot)
		if mc.objExists( AD ):		
			mc.parent(grpRoot , AD )	
		if mc.objExists( root ):		
			mc.parentConstraint( root , grpRoot , mo = True )
			mc.scaleConstraint( root , grpRoot , mo = True )	
	
	mc.parent(_manip[0] , grpRoot)
	
	
	#si c'est un remplacement de manip
	locReplaceManip = ( _trsf + '_TMPreplaceLoc' )
	
	if( mc.objExists( locReplaceManip )  ):
		father = mc.listRelatives( locReplaceManip , p = True  )
		childrens = mc.listRelatives( locReplaceManip , c = True  )
		mc.parent( _manip[0] , father )
		mc.parent( childrens , _manip[2] )
		mc.delete( locReplaceManip )
		
	
	# hierarchie dans AD ---->
	'''
	# on recupere tout les ctrlorig enfant
	
	cOrigs = []
	
	trsfChildrens = mc.listRelatives( _trsf , ad = True , typ = 'transform' )
	
	if not( trsfChildrens == None ):
		for t in trsfChildrens:
	
			tChildrens = mc.listRelatives( t , c = True , typ = 'parentConstraint')	
			
			if( tChildrens == None ):
				continue
			cManip = mc.listConnections( '%s.target[0].targetTranslate' %( tChildrens[0] ) , s = True, d = False ) 
			
			if( (cManip[0] == root) or ( len(cManip) == 0) ):
				continue
			else:
				cOrig = mc.listRelatives( cManip[0] , p = True )
				cOrigs.append(cOrig[0])				
		
		for o in cOrigs:  				
			mc.delete( o , cn = True )
			mc.parent( o , _manip[2] )
	
		
	# on recupere tout le ctrl parent
	pElem =['']
	pElem[0] = _trsf		
	cManip = []	
	i = 0
	
	while not ( (pElem[0] == 'RIG:BDD:MODEL_HI_GRP') or (pElem[0] == 'RIG:BDD:MODEL_RLO_GRP') or (pElem[0] == 'RIG:BDD:MODEL_OPT_GRP') ):
		pElem = mc.listRelatives( pElem[0] , p = True )
		pChildren = mc.listRelatives( pElem[0] , c = True , typ = 'parentConstraint')
		if not( pChildren == None ):
			cManip = mc.listConnections( '%s.target[0].targetTranslate' %(pChildren[0]) , s = True, d = False )
			break
			
		i += 1 	
		if( i == 20 ):
			pElem[0] ='RIG:BDD:MODEL_HI_GRP'
	
	
	if(( len(cManip) == 1 ) and not ( cManip[0][0:4] == 'RIG:' )):	
		cJoint = mc.listRelatives( cManip[0] , c = True , typ = 'joint')
	
		if( cJoint[0] == None ):
			mc.parent( _manip[0], cManip[0])
		else:
			mc.parent( _manip[0], cJoint[0])
	'''

	

def addInAnimSet(manip):

	selection = mc.ls( sl = True )
	
	animSet = 'RIG:ANIM_accessories_set' 
			
	if mc.objExists( animSet ):		
		mc.select( manip)
		mc.select( animSet , add = True , ne = True) 
		mel.eval(" mgUtils_addRemoveSelectionToSet(\"add\" , \"outlinerPanel1\")")
		
	mc.select( selection )
	
	
	
	

	
def translateManipTrsf( selection ):
	
	
	if( selection == '' ):
		selection = mc.ls( sl = True )
	
	axes = [ 'X' , 'Y' , 'Z' ]
	oGrp = mc.createNode( 'transform' , n = 'trashO_grp' )	
	
	for elem in selection :
		
		reelBBCoords = getBBreelCoordsAttr( elem )
		
		if( len( reelBBCoords ) ):
			position = getPositionBBreel(reelBBCoords)

			# --------> enlever les contraintes
			
			parentConstraintChildrens = getConstraintSlaves( elem , 'parentConstraint' , 1 )
			scaleConstraintChildrens = getConstraintSlaves( elem , 'scaleConstraint' , 1  )
			
			# --------> sortir les enfants
			childrens = getSpecifieTypeChildrens( elem , ['nurbsCurve' , 'mesh' , 'nurbsSurface' , 'joint' ] )
			if( len( childrens ) ): 
				mc.parent( childrens , w = True )
			
			
			# --------> sortir la shape
			ctrlshape = mc.listRelatives( elem , c = True , s = True )
			
			mc.parent( ctrlshape[0] , oGrp , s = True )
			
			
			pIndex = getUI_positionManip()
			
			# mettre nouvelle position sur orig
			orig = mc.listRelatives( elem , p = True )
			for i in range( 0 , 3 ):
				 mc.setAttr( orig[0] + ('.translate' + axes[i] ) , position[ pIndex ][i] )	
						
			# <----- remettre la shape
			
			mc.parent(  ctrlshape[0]  , elem  , s = True )
			fatherTrashGrp = mc.listRelatives( ctrlshape[0]  , p = True )
			mc.makeIdentity( fatherTrashGrp[0] , a = True , t = True , r = True , s = True )
			mc.parent(  ctrlshape[0]  , elem  , s = True  , r = True ) 
			mc.delete(fatherTrashGrp[0])
			
			# <----- remettre les enfants
			
			if( len( childrens ) ): 			
				mc.parent( childrens , elem )
				
			# <----- remettre les constrainte
			for parentConstraintChildren in parentConstraintChildrens:
				mc.parentConstraint( elem , parentConstraintChildren , mo = True  )
				
			for scaleConstraintChildren in scaleConstraintChildrens:				
				mc.scaleConstraint( elem , scaleConstraintChildren , mo = True  )
				

	mc.delete(oGrp)	
	mc.select(selection)


	
	


def resetSelectedManipToWorldOrient( _axe ):

	selection = mc.ls( sl = True )

	for elem in selection :
	
		#on verifie que c'est bien un manip
		shapes = mc.listRelatives( elem , c = True , s = True )
		
		if not( len( shapes ) ):
			continue
		if not( mc.nodeType( shapes[0] ) == 'nurbsCurve'  ):
			continue
		
		# on get les contraint slaves( + suppr )
		
		parentConstraintSlaves = getConstraintSlaves( elem , 'parentConstraint', 1 )
		scaleConstraintSlaves  = getConstraintSlaves( elem , 'scaleConstraint' , 1 )
		
		# on get les enfant du manip

		childrens = getSpecifieTypeChildrens( elem , ['nurbsCurve' , 'mesh' , 'nurbsSurface' , 'joint' ] )
		if( len( childrens ) ): 
			mc.parent( childrens , w = True )				
		
		# on set a 0 le orig      <------------

		orig = mc.listRelatives( elem , p = True )

		if( _axe == 'X' ):
			
			rotValue = mc.getAttr( ( orig[0] + '.rotateX' ) )
			rotValue = snapOrientValue( rotValue , [-180 , -90 , 0 , 90 , 180 ] )
			mc.setAttr( ( orig[0] + '.rotateX' ) , rotValue )
		
		if( _axe == 'Y' ):
			rotValue = mc.getAttr( ( orig[0] + '.rotateY' ) )			
			rotValue = snapOrientValue( rotValue , [-180 , -90 , 0 , 90 , 180 ] )
			mc.setAttr( ( orig[0] + '.rotateY' ) , rotValue )		
	
		if( _axe == 'Z' ):
			rotValue = mc.getAttr( ( orig[0] + '.rotateZ' ) )			
			rotValue = snapOrientValue( rotValue , [-180 , -90 , 0 , 90 , 180 ] )
			mc.setAttr( ( orig[0] + '.rotateZ' ) , rotValue )	
			
			
		# <----- remettre les enfants
		
		if( len( childrens ) ): 			
			mc.parent( childrens , elem )
			
		# <----- remettre les constrainte
		for parentConstraintSlave in parentConstraintSlaves:
			mc.parentConstraint( elem , parentConstraintSlave , mo = True  )
			
		for scaleConstraintSlave in scaleConstraintSlaves:				
			mc.scaleConstraint( elem , scaleConstraintSlave , mo = True  )			
			


			
			


def snapOrientValue( value , toSnapValues ):
	
	diff = []
	
	
	for toSnapValue in toSnapValues:
		diff.append( abs( value - toSnapValue ) )
		
	diff.sort()
	
	snapValue = value + diff[0]
	if( snapValue in toSnapValues ): 	
		return snapValue
	
	snapValue = value - diff[0]
	if( snapValue in toSnapValues ): 	
		return snapValue			
	
#-------------------------------------------------------------------	
# ------------------------   VECTEUR TO ORIENTATION    -------------
#-------------------------------------------------------------------	    
	

	
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
	    
    
	
	
#-------------------------------------------------------------------	
# ------------------------   ATTR BB COORDS    ---------------------
#-------------------------------------------------------------------	    



def setBBreelCoordsAttr( _trsf , _reelBBPoints ):
	
	reelBBcoordsStr = convertBBpointsToString( _reelBBPoints )
	
	i = 1
	loop = 1		
	attr = "BBreelCoords_" 
	
	if not( mc.objExists( _trsf +'.'+ attr + str(i) ) ):
		mc.addAttr( _trsf , ln = ( attr + str(i) ) , dt = "string" )		
		mc.setAttr( ( _trsf + '.' + attr + str(i) ) , reelBBcoordsStr , type = "string" , l = True ) 
		return 1
		

	
	i = 0		
	while( loop == 1 ):
		i += 1		
		if not( mc.objExists( _trsf +'.'+ attr + str( i + 1 ) )  ):
			lastAttr = attr + str(i)
			loop = 0


		
	oldReelBBcoordsStr = mc.getAttr( _trsf +'.'+ lastAttr )	
	

	
	if( reelBBcoordsStr != oldReelBBcoordsStr ):
		i += 1
		mc.addAttr( _trsf , ln = ( attr + str(i) ) , dt = "string" )		
		mc.setAttr( ( _trsf + '.' + attr + str(i) ) , reelBBcoordsStr , type = "string" , l = True ) 		

	return 1		
	
			


def getBBreelCoordsAttr( _trsf ):
	
	loop = 1	
	attr = "BBreelCoords_" 
	
	i = 0		
	while( loop == 1 ):
		i += 1		
		if not( mc.objExists( _trsf +'.'+ attr + str( i + 1 ) )  ):
			lastAttr = attr + str(i)
			loop = 0
	
	if not( mc.objExists( _trsf +'.'+ lastAttr ) ):
		reelBBcoords = []
		return reelBBcoords 		
			
			
	reelBBcoordsStr = mc.getAttr ( _trsf +'.'+ lastAttr )	
	reelBBcoords = convertStringToBBpoint( reelBBcoordsStr )
	
	return reelBBcoords
	



def getPositionBBreel( _reelBBPoint ):


	baseA = _reelBBPoint[0] 	
	baseB = _reelBBPoint[1] 
	baseC = _reelBBPoint[2]
	baseD = _reelBBPoint[3]
	topA  = _reelBBPoint[4]
	topB  = _reelBBPoint[5]
	topC  = _reelBBPoint[6]
	topD  = _reelBBPoint[7]

	centreBBreel   = getBarycentre( baseA , baseB , baseC , baseD , topA , topB , topC , topD )	
	
	centreBaseABCD = getBarycentre( baseA , baseB , baseC , baseD )
	centreTopABCD  = getBarycentre(  topA , topB  , topC  , topD  )
	
	centreCoteA  = getBarycentre(  baseA , baseB  , topA  , topB  )
	centreCoteB  = getBarycentre(  baseB , baseC  , topB  , topC  )
	centreCoteC  = getBarycentre(  baseC , baseD  , topC  , topD  )
	centreCoteD  = getBarycentre(  baseD , baseA  , topD  , topA  )
	
	positions = [ centreBBreel , centreBaseABCD , centreTopABCD , centreCoteA , centreCoteB , centreCoteC , centreCoteD ]

	return positions     
            
	
def getOrientationBBreel( _reelBBPoint ):
	
	baseB = _reelBBPoint[1]
	baseD = _reelBBPoint[3] 	
	baseC = _reelBBPoint[2]
	topC  = _reelBBPoint[6]

	vX = [  baseB[0] - baseC[0]  ,  baseB[1] - baseC[1]  ,  baseB[2] - baseC[2]  ]	
	vY = [   topC[0] - baseC[0]  ,   topC[1] - baseC[1]  ,   topC[2] - baseC[2]  ]
	vZ = [  baseD[0] - baseC[0]  ,  baseD[1] - baseC[1]  ,  baseD[2] - baseC[2]  ]

    
	rotXYZ = convertTripleVecteurToEulerRot( vY , vX , vZ )    
    
	return rotXYZ    
    	
	


def getScaleBBreel( _reelBBPoint ):
	
	baseB = _reelBBPoint[1] 
	baseC = _reelBBPoint[2]
	baseD = _reelBBPoint[3]
	topC  = _reelBBPoint[6]


	scaleX  = om.MVector(  baseD[0] - baseC[0] ,  baseD[1] - baseC[1] ,  baseD[2] - baseC[2]  ).length()	
	scaleY  = om.MVector(  topC[0] - baseC[0]  ,  topC[1] - baseC[1]  ,  topC[2] - baseC[2]  ).length()
	scaleZ  = om.MVector(  baseB[0] - baseC[0] ,  baseB[1] - baseC[1] ,  baseB[2] - baseC[2]  ).length()

	
	scaleXYZ = [ scaleX , scaleY , scaleZ ]

	return scaleXYZ     
    	
	
	
	
	
#-------------------------------------------------------------------	
# ------------------------   HELP Convert	    ---------------------
#-------------------------------------------------------------------		
	

	
	

def convertBBpointsToString( _reelBBcoords ):
	
	reelBBcoordsSTR = ''
	
	for coords in _reelBBcoords:
		reelBBcoordsSTR += '%f %f %f '%( coords[0] , coords[1] , coords[2] )
		
	return reelBBcoordsSTR	
	
	
    
    
def convertStringToBBpoint( _reelBBcoordsStr ):
	
	e = _reelBBcoordsStr.split(" ")	
	reelBBcoords = []

	for i in range( 0 , 22 , 3) : 
		reelBBcoords.append( [ float( e[i] ) , float( e[1 + i] ) , float( e[2 + i] ) ] )


	return reelBBcoords 
	


def convertElemToVertex( _trsf ):

	coords =[] 
	
	splitVtxs = _trsf.split(" ")
	vtxCoords = []	
	
	
	if( trueIfMsh(_trsf) ):   # si c'est un mesh
		
		coords = getAllVertexCoords( _trsf )
		return coords	
		
		
	
	if( 1 < len(splitVtxs) ):   # si c'est plusieurs vertex
		_trsf = splitVtxs[0]
		
		coords = convertElemToVertex(_trsf)
		
		for i in range( 1 , len(splitVtxs) ):			
			vtxCoords.append( coords[ int( splitVtxs[i] ) ] )					

		coords = vtxCoords

		#pour sel Vertex avec manip


		constraintNode = mc.listConnections( ( _trsf + '.rotatePivotTranslate' ) , s = False , d = True )		
	
		if( constraintNode  == None ):		
			return coords	
	
		manip = mc.listConnections( ( constraintNode[0] + '.target[0].targetTranslate' ) , s = True , d = False )
		_trsf = manip[0]
				
		
		
		
	shapeElem = mc.listRelatives( _trsf , c = True , s = True )
	
			
		
	if( shapeElem == None ):   # si c'est un grp

		msh = getAllChildrenMsh( _trsf )
		for m in msh: 
			coords += getAllVertexCoords( m )	
			
		return coords			
		
	
		
		
	if( mc.nodeType(shapeElem[0]) == "locator" ): # si c'est un locator	
		
		coords = convertLocatorToVertexCoords( _trsf )	
		return coords
	

		
		
		
	if( mc.nodeType(shapeElem[0]) == "nurbsCurve" ): # si c'est un manip 

		msh = getConstraintSlaves( _trsf , 'parentConstraint' , 0 )		
		locTmp = replaceManipBylocTmp( _trsf )
		
		
		
		if( len(msh) == 0 ):
			mc.error( 'no Msh constraint to this manip' )
		
		if( len(msh) > 1 ):
			coords = getAllVertexCoords( msh[0][0] )
		else:
			coords = getAllVertexCoords( msh[0] )
			
		#pour sel Vertex avec manip
		if( 0 < len(vtxCoords) ):
			coords = vtxCoords
			
			
		return coords
		
		
	return coords



	
	
	
	
	
	
	

	
	
def replaceManipBylocTmp( _ctrl ): 
	
	locTmp = (  _ctrl + '_TMPreplaceLoc' )
	
	mc.spaceLocator( n = locTmp )
	
	orig = mc.listRelatives( _ctrl , p = 1 )
	skn = mc.listRelatives( _ctrl , c = 1 , type = "joint" )
	
	
	# place in outliner
	
	if( skn == None ):
		allChildrens = mc.listRelatives( _ctrl , c = 1 )
	else:
		allChildrens = mc.listRelatives( skn[0] , c = 1 )
		
	
	father = mc.listRelatives( orig , p = True)

	mc.parent( locTmp , father )	

	if not( allChildrens == None):	
		mc.parent( allChildrens , locTmp )	
		
	# constrainte

	slaves = getConstraintSlaves( _ctrl , 'parentConstraint' , 1 )
	
	
	for slave in slaves :
		mc.parentConstraint( locTmp , slave , mo = True)

	mc.delete( orig[0]) 		
		
	return locTmp				


	
	

def convertLocatorToVertexCoords( _loc ):

	sizeManip = 5
	
	incrLetters = [ 'A' , 'B' , 'C' , 'D' , 'E' , 'F' , 'G' , 'H' ]
	axes = [ 'X' , 'Y' , 'Z' ]
	suffix = '_TMP_'
	cubeCoords = [ [ 1 , 1 , 1 ] , [ -1 , 1 , 1 ] , [ 1 , -1 , 1 ] , [ -1 , -1 , 1 ]    ,    [ 1 , 1 , -1 ] , [ -1 , 1 , -1 ] , [ 1 , -1 , -1 ] , [ -1 , -1 , -1 ]  ]
	coords = []
	
	for i in range( 0 , 8 ) :
		newLoc = ( _loc + suffix + incrLetters[ i ] ) 
		mc.spaceLocator( n = newLoc )
		mc.parent( newLoc , _loc )
		
		for j in range( 0 , 3 ):
			mc.setAttr( ( newLoc + '.translate' + axes[j] ) ,  ( cubeCoords[i][j] * sizeManip ) ) 

		mc.parent( newLoc , w = True )
		
		for j in range( 0 , 3 ):
			cubeCoords[i][j] = mc.getAttr( ( newLoc + '.translate' + axes[j] ) )
			
		mc.delete( newLoc )
		
		coords = cubeCoords

	return coords 
		
		
	
	




def contraintManipToSlave( _origCtrlJoint , _trsf):

	
	#si c'est un remplacement de manip
	locReplaceManip = ( _trsf + '_TMPreplaceLoc' )
	
	if( mc.objExists( locReplaceManip )  ):		
		msh = getConstraintSlaves( locReplaceManip , 'parentConstraint' , 1 )
		mc.delete(locReplaceManip)		
		

		for m in msh :
		
			mc.parentConstraint( _origCtrlJoint[1] , m , mo = True  )
			mc.scaleConstraint( _origCtrlJoint[1] , m , mo = True  )	
	else:	
		mc.parentConstraint( _origCtrlJoint[1] , _trsf , mo = True  )
		mc.scaleConstraint( _origCtrlJoint[1] , _trsf , mo = True  )

	
		


		
		
		
		
		
def convertVertexMshToMshIndex( _selection ):

	mshIndex = []
	
	vtxs = mc.filterExpand( _selection , sm = 31 )
	
	oldTrsf = ''
	
	i = -1
	
	for vtx in vtxs :
		
		baseName = vtx.split('.')[0]	
		
		# add
		if( mc.nodeType(baseName) == 'mesh' ):
			baseNameTmp = mc.listRelatives( baseName , p = True ) 
			baseName = baseNameTmp[0]					
		# fin
		
		
		indexVtx = vtx.split('[')[1].split(']')[0]
			
		if not( baseName == oldTrsf ):
			mshIndex.append(baseName + ' ' + indexVtx )
			i += 1			
		else:
			mshIndex[i] += ( ' ' + indexVtx )
			
		oldTrsf = baseName
		
	return mshIndex	

			
	
	
################################################ UI



def progressWindowUI( curenteState , initState , finalState , message ):


	adaptProgress =  ( curenteState / finalState) * 100

	if( curenteState == initState ): 
		mc.progressWindow( title = "BUILD MANIP VIS" , progress = adaptProgress , status = message ) 
	else:	
		mc.progressWindow( e = True ,  progress = adaptProgress , status = message  )	
	
	if( curenteState == finalState ):
		mc.progressWindow( endProgress = True )

	

################################# COMPUTE #################################################################



def switchManipShape():
	
	selection = mc.ls( sl = True )
	
	for elem in selection :
		
		manipShape = mc.listRelatives( elem , c = True , s = True  )
		
		if(  manipShape  == None ) or ( mc.nodeType( manipShape[0] ) != 'nurbsCurve' ):
			continue

		mc.delete( manipShape[0] )
		
		ctrlShape    = buildCtrlShape( elem )	
		reelBBCoords = getBBreelCoordsAttr( elem )			
		scaleXYZ     = getScaleBBreel(reelBBCoords)	
		
		resizeCtrlShape( ctrlShape , scaleXYZ )	
		
	mc.select( selection )
		


	
	
def computeCreateManip( ):
	
	selection  = mc.ls( sl = True )
	size       = len(selection) 
	vtxPattern = '.vtx['	
	manips     = []	

	if( vtxPattern in selection[0] ):		
		selection = convertVertexMshToMshIndex( selection )
	
	for i in range( 0 , size ):		
		progressWindowUI( i , 0 , size,  elem  )		
		origCtrlJoint = createManip( selection[i] )		
		manips.append( origCtrlJoint[1] )
		
	mc.select( manips )	
	print(' ====================== SET MANIPS DONE      ====================== ')

	
	

def createManip( _trsf ):


	option = [ 'position' , 'orient' , 'scale' , 'joint' , 'visibility' , 'constraint' , 'root' , 'animSet' ]	



	
	rawCoords = convertElemToVertex(_trsf)

	# pour vertex	
	splitVtxs = _trsf.split(" ")	
	if( 1 < len(splitVtxs) ):
		_trsf = splitVtxs[0]	
	# fin pour vertex
	
	print(' ')
	print(' %r vertex to compute ' %( len(rawCoords) ) )
	print( ' find Local BoundingBox...' )

	
	#reelBBCoords = localBBoptim5.getLocalBB( rawCoords )

	coords = []
	
	for rawCoord in rawCoords:
	    for elem in rawCoord:
	        coords.append(elem)	
	
	timeA = time.clock()
	
	reelBBCoords = mc.MC_getRotatedBBCoordsCmd_referenceModif( coords )
	
	timeB = time.clock()
	
	print( timeB - timeA )
	
	
	#on reorganise array
	
	newpCoord = []
	newAllCoords = []	
	
	
	
	for c in reelBBCoords:
		newpCoord.append( c )
		if( len( newpCoord ) == 3 ):
			newAllCoords.append( newpCoord )
			newpCoord = []
		
	        	

	reelBBCoords = newAllCoords
	
	
	
	#on reorganise array <----	
	        	
	print( ' Build Manip...' )
	print(' ')
	
	
	position = getPositionBBreel(reelBBCoords) 	
	rotation = getOrientationBBreel(reelBBCoords)
	scale = getScaleBBreel(reelBBCoords)
	

	
	
	# trsf--------------
	
	origCtrlJoint = buildManipBase( _trsf , position[0] , rotation )	
	setBBreelCoordsAttr( origCtrlJoint[1] , reelBBCoords )
	
	# shape--------------
	
	ctrlShape = buildCtrlShape( origCtrlJoint[1] )
	resizeCtrlShape( ctrlShape , scale )

	# connect manip mesh --------------
	
	contraintManipToSlave( origCtrlJoint , _trsf )
	mc.connectAttr(  ( origCtrlJoint[1] + '.object_display' ) , (_trsf + '.visibility') )

	
	# change position Manip

	translateManipTrsf( [ origCtrlJoint[1] ]  )
	
	
	setManipInHierarchie( _trsf , origCtrlJoint )
	addInAnimSet( origCtrlJoint[1] )

	
	return origCtrlJoint
	
    