import maya.cmds as mc

from ..utils import utilsMaya
from ..utils import utilsPython
from ..utils import utilsMath
from ..utils import utilsMayaApi


class transform( mayaObject ):
	
	'''
	getAttr( curves )
	save( form )
	saveSelected()
	build()
	buildOnSelection( form = '' , debug = 1 )
	modif( parent = None , form = None , coords = None  , nbrPoints = None , degrees = None , colors = None , axe = None , offset = None )
	delete()
	mirror( parent , mirrorPlaneCoords )
	copy( parent )
	load( form )
	printAttrs( title = '' )
	'''
	
	def __init__(self):

		self.debug = 0
	
		self.fileBaseName = 'curveShape' 		
		self.path         = 'D:/mcantat_BDD/projects/code/xml/'		
		utilsPython.createXmlDicoVar( self.fileBaseName , self.path )		

		self.formToCurveInfo = utilsPython.readXmlDicoVar( self.fileBaseName , self.path )		
		self.forms = self.formToCurveInfo.keys()
		self.forms.sort()
		self.names     = ['None']
		self.parent    = 'curveLibDefaultTransform_CTRL'
		self.form      = 'cube'		
		self.coords    = self.formToCurveInfo[self.form][0]
		self.nbrPoints = self.formToCurveInfo[self.form][1]
		self.degrees   = self.formToCurveInfo[self.form][2]
		self.colors    = self.formToCurveInfo[self.form][3]
		self.axeOrient = ''
		self.trsOffset = [ 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1 ]
		self.worldSpaceMode = False

		self.utils_centerWorldTrs = [ 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1 ]
		#self.colorNameToColorIndex = { 'red':13 , 'yellow' , 'green' , 'blue' , 'black' , 'white'}
		#self.ctrlFonctionToColorIndex = { 'principal':13 , 'principalLeft' , 'principalRight' , 'secondary' , 'secondaryLeft' , 'secondaryRight'}


	def getAttr( self , curves ):

		#GET PARENT
		if ( mc.nodeType(curves[0]) == 'transform' ):
			parent = curves[0]
		else:
			parent = mc.listRelatives( curves[0] , p = True , c = False )[0]

		self.parent = parent

		#CONVERT CURVE INTO SHAPES
		childrensTmp = utilsMaya.getAllChildrens( curves , includeParents = True );
		shapes       = utilsMaya.filterType( childrensTmp , [ 'nurbsCurve' ] )    

		#IF NO NURBS SHAPES STOP
		if ( len( shapes ) == 0 ):
			return 0

		#GET CURVES INFO	
		names , coords , coordsTmp , nbrPoints , degrees , colors = [] , [] , [] , [] , [] , []
		for shape in shapes :
			coordsTmp = self.utils_getCurveShapeCoords( shape , self.worldSpaceMode )
			coords   += coordsTmp
			names.append( shape )
			nbrPoints.append( len(coordsTmp) / 3 )
			degrees.append( mc.getAttr( shape +'.degree' ) )
			colors.append( mc.getAttr( shape +'.overrideColor' ) )

		self.names , self.coords , self.nbrPoints , self.degrees , self.colors  = names , coords , nbrPoints , degrees , colors 

		self.printAttrs( 'getAttr')
		return 1
		

	def getAttrSelected( self ):

		selection = mc.ls(sl=True)
		self.getAttr( selection )
		self.printAttrs( 'getAttrSelected' )
		return 1
		

	def save( self , form ):

		#INIT DICO
		self.formToCurveInfo = utilsPython.readXmlDicoVar( self.fileBaseName , self.path )

		#YELD MESSAGE IF THE NAME ALREADY EXIST
		if( form in self.formToCurveInfo.keys() ):
			respond = mc.confirmDialog( title='Confirm', message='Name already exist!\nDo you want to Overwrite it?', button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
			if( respond == 'No' ):
				print(' Operation canceled ')
				return 0

		#SAVE NEW CURVE IN DICO
		self.formToCurveInfo[ form ] = [ self.coords , self.nbrPoints , self.degrees , self.colors ]
		self.formList = self.formToCurveInfo.keys()	

		#SAVE DICO IN FILE			
		utilsPython.writeXmlDicoVar(  self.fileBaseName , self.path , self.formToCurveInfo )


		self.printAttrs( 'save' )		
		return 1

	def saveSelected( self ):	

		#GET SELECTION			
		selection = mc.ls(sl=True)

		#FILL CLASS ATTR
		self.getAttr( selection )
		
		#ASK THE NAME OF THE FORM
		result = mc.promptDialog( title= 'Save Curve Form ', message='Enter name of the form:', button=['OK', 'Cancel'], defaultButton='OK', cancelButton='Cancel', dismissString='Cancel' )	
	
		if( result == 'OK' ):
			form = mc.promptDialog(query=True, text=True)
		else:
			return 0

		#SAVE CURVE
		self.save( form )
	
		self.printAttrs( 'saveSelected' )		
		return 1
		
	def build( self ):

		#ROTATE COORDS WITH AXE ORIENT
		coordsRot   = self.utils_rotateCoordsWithAxeOrient( self.coords , self.axeOrient , self.utils_centerWorldTrs )	

		#ARRAY COORDS TO ONE ARRAY PER CURVE
		multiCoords = self.utils_separateCoords( coordsRot , self.nbrPoints )

		#BUILD EACH CURVE
		for i in range( 0 , len(multiCoords) ):
			self.names[i] = self.utils_buildCurveShape( self.parent , self.names[i] , multiCoords[i] , self.degrees[i] , self.colors[i] , self.trsOffset , self.worldSpaceMode )
		
		
		self.printAttrs( 'build' )	
		return 1    

	def buildOnSelection( self , form = '' , debug = 1 ):	

		selection = mc.ls(sl=True)
		self.getAttrSelected()

		if not( form == '' ):
			self.load( form )

		self.build()

		self.printAttrs( 'buildOnSelection' )		
		return 1


	def modif( self , parent = None , form = None , coords = None  , nbrPoints = None , degrees = None , colors = None , axe = None , offset = None ):


		#UPDATE LAST VALUES
		self.getAttr( self.names )
		
		#DELETE EXISTING CURVE
		self.delete()

		#GET ALL THE MODIFICATION
		if not ( form == None ):
			self.form = form
			self.load( self.form )				

		if not ( parent == None ):
			self.parent = parent
		if not ( coords == None ):
			self.coords = coords
		if not ( nbrPoints == None ):
			self.nbrPoints = nbrPoints
		if not ( degrees == None ):
			self.degrees = degrees
		if not ( colors == None ):
			self.colors = colors
		if not ( axe == None ):
			self.axeOrient = axe
		if not ( offset == None ):
			self.trsOffset = offset

		#REBUILD
		self.build()

		self.printAttrs( 'modif')		
		return 1

	def delete(self):
		mc.delete(self.names)

	def mirror( self , parent , mirrorPlaneCoords ):
		#UPDATE LAST VALUES
		self.getAttr( self.names )
		#SWITCH PARENT
		self.parent = parent
		#MIRROR COORDS	
		print( self.coords  )
		coordsTmp   = [ [ self.coords[i+0] , self.coords[i+1] , self.coords[i+2] ] for i in range( 0 , len(self.coords) , 3 ) ]
		print( coordsTmp )
		coordsTmp   = utilsMayaApi.mirrorCoords( coordsTmp , mirrorPlaneCoords )
		print( coordsTmp )
		self.coords = [ coordsTmp[i][j] for i in range( 0 , len(coordsTmp) ) for j in range(0,3) ]
		print( self.coords )
		#BUILD		
		self.build()
		#DEBUG
		self.printAttrs( 'mirror' )
		return 1
	
	def copy( self , parent ):
		#UPDATE LAST VALUES
		self.getAttr( self.names )
		#SWITCH PARENT
		self.parent = parent
		#BUILD
		self.build()
		#DEBUG
		self.printAttrs( 'copy' )
		return 1

	def load( self , form ):

		#INIT DICO
		self.formToCurveInfo = utilsPython.readXmlDicoVar( self.fileBaseName , self.path )

		#FILL CLASS ATTR
		self.form      = form
		self.coords    = self.formToCurveInfo[form][0] 
		self.nbrPoints = self.formToCurveInfo[form][1]
		self.degrees   = self.formToCurveInfo[form][2]
		self.colors	   = self.formToCurveInfo[form][3]

		self.printAttrs( 'load' )				
		return 1


	def printAttrs( self , title = '' ):

		if( self.debug == 0 ):
			return 0

		print('START_____________________________ ' + title)
		print('**********ATTRS***********')
		print( 'names     : ' , self.names )
		print( 'parent    : ' , self.parent )
		print( 'form      : ' , self.form )
		print( 'coords    : ' , self.coords )
		print( 'nbrPoints : ' , self.nbrPoints )
		print( 'degrees   : ' , self.degrees )
		print( 'colors    : ' , self.degrees )
		print( 'axeOrient : ' , self.axeOrient )
		print( 'trsOffset : ' , self.trsOffset )
		print('END________________________________ ' + title)

		return 1


	def utils_rotateCoordsWithAxeOrient( self , coords , axeOrient , trsPivot , oldAxeOrient = 'y' ):

		newCoords = coords
		if(   axeOrient == 'x' ):
			newCoords = utilsMath.transformCoords( self.coords , trsPivot[0:3]  , [ 0 , 0 , 0 , 0  , 0 , 90 , 1 , 1 , 1 ] , 'XYZ' )							
		elif( axeOrient == 'y' ):
			newCoords = utilsMath.transformCoords( self.coords , trsPivot[0:3]  , [ 0 , 0 , 0 , 90 , 0 , 0  , 1 , 1 , 1 ] , 'XYZ' )

		return newCoords
		


	def utils_separateCoords( self , coords , nbrPoints ):
		
		splitCoords = []
		lastSize = 0

		for size in nbrPoints:
			coordsTmp = []
			for i in range( 0 + lastSize * 3 , size * 3 + lastSize * 3 ):
				coordsTmp.append(coords[i])
			splitCoords.append(coordsTmp)
			lastSize = size

		return splitCoords



	def utils_mergeCoords( self , splitCoords ):

		coords = []
		nbrPoints = []

		for curveCoords in splitCoords:
			nbrPoints.append( len(curveCoords) / 3 )
			coords += curveCoords


		return [ coords , nbrPoints ]

	def utils_buildCurveShape( self , transformName , shapeName , coords , degree , colorIndex , trsOffset = None  , worldSpace = False  ):		
		'''
			CVs  = Spans + Degree
			Knot = CVs   + Degree -1		
		'''

		#OFFSET POSITION			
		if not( trsOffset == None ):
			coords = utilsMath.transformCoords( coords , [ 0 , 0 , 0 ]  , trsOffset , 'XYZ' )  	


		#CONVERT COORDS
		pos = []
		for i in range( 0 , len(coords) , 3 ):
			pos.append([ coords[i+0] , coords[i+1] , coords[i+2] ] )		

		#FILL ATTR
		knot = []
		nbrKnot = len(pos) + degree - 1  		#_knot	= spans + 2 degree - 1	degree first knot identical    and   degree las knot identical	
		
		for i in range( 0 , degree ):
			knot.append(0)
			
		for i in range( degree , nbrKnot - degree):
			knot.append(i)
				
		for i in range( 0 , degree ):
			knot.append(nbrKnot - degree)
				
		#BUILD 
		nameTmp   = 'curveManip_Tmp'	
		mc.curve( n = nameTmp , d = degree , p = pos , k = knot )
		curveShape = mc.listRelatives( nameTmp , c = 1 , s = 1 )

		if( mc.objExists( transformName ) == 0 ):
			mc.createNode( 'transform' , n = transformName )

		mc.parent( curveShape[0] , transformName , s = True , r = True ) 
		mc.delete( nameTmp )	

		if( worldSpace == True ):
			for i in range( 0 , len(pos) ):
				mc.xform( '{0}.cv[{1}]'.format( curveShape[0] , i ) , t = pos[i] , ws = True  )

		#COLOR
		mc.setAttr( ( curveShape[0] + ".overrideEnabled" ) , 1 )
		mc.setAttr( ( curveShape[0] + ".overrideColor" )   , colorIndex )

		#RENAME	
		reelshapeName = curveShape[0]
		if not( shapeName == 'None'):
			reelshapeName = mc.rename( curveShape[0] , shapeName )

		return reelshapeName         


	def utils_getCurveShapeCoords( self , curveShapeName , worldSpace = False ):
		'''		
			CVs = spans + degree
			knot = CVs + degree - 1			
		'''
		allCoords = []		
		nbrSpans  = mc.getAttr( curveShapeName + '.spans' ) 
		degree    = mc.getAttr( curveShapeName + '.degree' )  	
		nbrCvs    = nbrSpans + degree  
		
		for i in range( 0 , nbrCvs ):
		    cvCoords  = mc.xform( '{0}.cv[{1}]'.format( curveShapeName , i ), q = True , t = True , ws = worldSpace  )
		    allCoords += cvCoords    
		
		return allCoords	








