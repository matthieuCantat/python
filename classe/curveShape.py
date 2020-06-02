'''
#******************************************************** BUILD EXEMPLE 
import maya.cmds as mc
import python
from python.classe.curveShape import *
reload( python.classe.curveShape)
curve = curveShape()	

forms = curve.getForms()
print(forms)
curve.createFromFile("cube")
curve.toCurve('locator1')


curve = curveShape()
curve.setColorSelection('red')
curve.setFormSelection('arrow2sideBend')
curve.setFormSelection('sphere')
curve.setFormSelection('cylinder')
curve.setFormSelection('circle')
curve.extractSelected()


curve.replaceSameNameFile('D:\mcantat_BDD\projects\cute\carrierShipD\maya\scenes\carrierShipD_saveCtrlShapes.ma')

curve.replace( 'nurbsCircle1' , 'propulsorRoot_CTRL')




'''


import maya.cmds as mc


from . import coords as coordsClasse
from . import readWriteInfo
from ..utils import utilsMaya
from ..utils import utilsPython
from ..utils import utilsMath
from ..utils import utilsMayaApi
from .mayaClasse import *
from .trsBackUp import *


'''
UNIFY CLASSES
totoProc( inValue = 'coords' )
#________________________________________________________________BUILDER FRIENDLY
#________________________________________________________________USER FRIENDLY (shortCut)
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
toCurve -----> toObj
toSelectedCurve	
toSaveFile
selectionToFile
printAttrs
#________________________________________________________________UTILS	
utils_rotateCoordsWithAxeOrient
utils_separateCoords
utils_mergeCoords
utils_buildCurveShape
utils_getCurveShapeCoords
'''
	





class curveShape(mayaClasse):
	
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
	utils_rotateCoordsWithAxeOrient
	utils_separateCoords
	utils_mergeCoords
	utils_buildCurveShape
	utils_getCurveShapeCoords
	'''
	
	def __init__(self):

		self.type      = 'curveShape'
		self.classeType = 'curveShape'
		self.debug     = 0
		#GET INFO FROM FILE				
		self.filePath = 'D:/mcantat_BDD/projects/code/xml/curveShape.xml'
		#ReadWriteInfo = readWriteInfo.readWriteInfo()
		#ReadWriteInfo.createFromFile( self.filePath , latest = 1)				
		#formToCurveInfo = ReadWriteInfo.dict
		self.formToCurveInfo = None			
		#CURVE INFO		
		self.names     = ['None']
		self.parent    = 'curveLibDefaultTransform_CTRL'
		self.form      = ''#'cube'
		self.coords    = []#formToCurveInfo[self.form][0]
		self.nbrPoints = []#formToCurveInfo[self.form][1]
		self.degrees   = []#formToCurveInfo[self.form][2]
		self.colors    = []#formToCurveInfo[self.form][3]		
		self.axe       = ''#'x'
		self.offset    = [ 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1 ]
		self.position  = None
		self.scale     = 1
		#self.forms = formToCurveInfo.keys() 
		self.Coords = coordsClasse.coords()
		self.Trs = trs()

		#UTILS
		self.formLast     = self.form     
		self.axeLast      = self.axe      
		self.positionLast = self.position
		self.offsetLast   = self.offset[:]

		self.colorNameToIndex  = { 
		'red' :13 , 'purple' :9  , 'yellow' :17 , 'green' :14 , 'blue' :6  , 'white' :16 , 'cyan':19 , 'black':1 , 'grey':2 , 'brown':10 , 'affect':9  , 'selection':19, 
		'red2':4  , 'purple2':30 , 'yellow2':22 , 'green2':23 , 'blue2':15 , 'white2':20,
		'red3':12 , 'purple3':8  , 'yellow3':25 , 'green3':7  , 'blue3':5  , 'white3':21,
		'red4':24 , 'purple4':8  , 'yellow4':26 , 'green4':27 , 'blue4':29 , 'white4':13,
		'red5':10 , 'purple5':8  , 'yellow4':26 , 'green4':19 , 'blue4':28 , 'white4':3  }

		self.fonctionToColorName  = {
		'left1':'red'  , 'center1':'yellow'  , 'right1':'blue'  , 'root1':'green'  , 'special1':'purple'  , 'neutral1':'white' ,
		'left2':'red2' , 'center2':'yellow2' , 'right2':'blue2' , 'root2':'green2' , 'special2':'purple2' , 'neutral2':'white2',
		'left3':'red3' , 'center3':'yellow3' , 'right3':'blue3' , 'root3':'green3' , 'special3':'purple3' , 'neutral3':'white3',
		'left4':'red4' , 'center4':'yellow4' , 'right4':'blue4' , 'root4':'green4' , 'special4':'purple4' , 'neutral4':'white4',
		'left5':'red5' , 'center5':'yellow4' , 'right5':'blue4' , 'root5':'green4' , 'special5':'purple5' , 'neutral5':'white4'}



	def printAttrs( self , title = '' , printInfo = 1 ):
		if( printInfo == 1 ):
			print('START_____________________________ ' + title)
			print('**********ATTRS***********')
			print( 'names     : ' , self.names )
			print( 'parent    : ' , self.parent )
			print( 'position  : ' , self.position )
			print( 'form      : ' , self.form )
			print( 'coords    : ' , self.coords )
			print( 'nbrPoints : ' , self.nbrPoints )
			print( 'degrees   : ' , self.degrees )
			print( 'colors    : ' , self.colors )
			print( 'axeOrient : ' , self.axe )
			print( 'trsOffset : ' , self.offset )
			print('END________________________________ ' + title)

	#________________________________________________________________CREATE
	def createFromCurve( self , curve , worldSpace = False  ):
		#GET PARENT
		if ( mc.nodeType(curve) == 'transform' ):
			self.parent = curve
		else:
			self.parent = mc.listRelatives( curve , p = True , c = False )[0]
		#CONVERT CURVE INTO SHAPES
		childrensTmp = mc.listRelatives( curve , s = True , c = True , f = True  ) 
		shapes       = childrensTmp
		#IF NO NURBS SHAPES STOP
		if(shapes==None) or( len( shapes ) == 0 ): 
			return 0
		#GET CURVES INFO	
		names , coords , coordsTmp , nbrPoints , degrees , colors = [] , [] , [] , [] , [] , []
		Coords = coordsClasse.coords()		
		for shape in shapes :	
			coords += Coords.createFromObj( shape  , worldSpace = worldSpace )
			names.append( shape )
			nbrPoints.append( len(Coords.coords) )
			degrees.append( mc.getAttr( shape +'.degree' ) )
			colors.append( mc.getAttr( shape +'.overrideColor' ) )

		self.names , self.coords , self.nbrPoints , self.degrees , self.colors  = names , coords , nbrPoints , degrees , colors 
		#GET POSITIION
		Trs = trs()
		Trs.createFromObj(curve)
		self.position = Trs.value

		self.printAttrs( 'createFromCurve' , self.debug )
		return 1

	def createFromCurves( self , curves , worldSpace = False ):
		#GET PARENT
		if ( mc.nodeType(curves[0]) == 'transform' ):
			self.parent = curves[0]
		else:
			self.parent = mc.listRelatives( curves[0] , p = True , c = False )[0]
		#CONVERT CURVE INTO SHAPES
		childrensTmp = mc.listRelatives( curves[0] , s = True , f = True )
		shapes       = childrensTmp
		#IF NO NURBS SHAPES STOP
		if ( len( shapes ) == 0 ):
			return 0
		#GET CURVES INFO	
		names , coords , coordsTmp , nbrPoints , degrees , colors = [] , [] , [] , [] , [] , []
		Coords = coordsClasse.coords()		
		for shape in shapes :			
			coords += Coords.createFromObjs( [shape]  , worldSpace = worldSpace )
			names.append( shape )
			nbrPoints.append( len(Coords.coords) )
			degrees.append( mc.getAttr( shape +'.degree' ) )
			colors.append( mc.getAttr( shape +'.overrideColor' ) )

		self.names , self.coords , self.nbrPoints , self.degrees , self.colors  = names , coords , nbrPoints , degrees , colors 
		self.printAttrs( 'createFromCurves' , self.debug )
		return 1
		
	def createFromSelection( self ):
		selection = mc.ls(sl=True)
		self.createFromCurves( selection )
		self.printAttrs( 'getAttrSelected' , self.debug )
		return 1

	def createFromFile( self ):
		#GET INFO FROM FILE				
		ReadWriteInfo = readWriteInfo.readWriteInfo()
		ReadWriteInfo.createFromFile( self.filePath , latest = 1 )				
		self.formToCurveInfo = ReadWriteInfo.dict	
		#FILL CLASS ATTR

	def updateForm( self  , form ):
		if( self.formToCurveInfo == None ): self.createFromFile()
		self.form      = form
		self.coords    = self.formToCurveInfo[form][0] 
		self.nbrPoints = self.formToCurveInfo[form][1]
		self.degrees   = self.formToCurveInfo[form][2]
		
		colors = self.formToCurveInfo[form][3]
		if( 1 < len(colors) ) and not ( colors[0] == colors[1] ):
			self.colors = colors
			
		return 1		


	#________________________________________________________________MODIF

	def setColorSelection( self , color ):
		selection = mc.ls(sl = True)
		for elem in selection:
			self.setColor( elem , color )

	def setColor( self , curve , color ):
		#self.createFromCurve( curve , worldSpace = False  )
		#self.colors = [color]
		#self.delete()
		#self.toObj(curve , worldSpace = False )
		shapes = mc.listRelatives( curve ,  s = True , c = True  )
		if( type(color) == types.StringType ):
			color = self.colorNameToIndex[color] 

		for shape in shapes:
			mc.setAttr( shape + '.overrideEnabled' , 1 )
			mc.setAttr( shape + '.overrideColor' ,  color )


	def setFormSelection( self , form ):
		selection = mc.ls(sl = True)
		for elem in selection:
			self.setForm( elem , form )

	def setForm( self , curve , form ):
		self.__init__()
		self.createFromCurve( curve , worldSpace = True )
		self.modify( form = form )
		self.delete()
		self.toObj(curve , worldSpace = True  )

	def transferCoords( self , curve , curveTarget , worldSpace = True ):
		
		curveShapes       = mc.listRelatives( curve       , s = True )
		curveTargetShapes = mc.listRelatives( curveTarget , s = True )

		Coords = coordsClasse.coords()	
		for i in range( 0 , len(curveShapes ) ):			
			Coords.createFromObj( curveTargetShapes[i]  , worldSpace )
			Coords.toObj( curveShapes[i] , worldSpace )


	def extractSelected( self ):
		selection = mc.ls(sl = True)
		for elem in selection:
			nameTmp = mc.duplicate( elem )[0]
			childrensTmp = mc.listRelatives( nameTmp , c = True , f =True )
			for children in childrensTmp:
				if not( mc.nodeType(children) == 'nurbsCurve' ):
					mc.delete(children)

			mc.setAttr( nameTmp + '.tx' , l = False )
			mc.setAttr( nameTmp + '.ty' , l = False )
			mc.setAttr( nameTmp + '.tz' , l = False )
			mc.setAttr( nameTmp + '.rx' , l = False )
			mc.setAttr( nameTmp + '.ry' , l = False )
			mc.setAttr( nameTmp + '.rz' , l = False )
			mc.setAttr( nameTmp + '.sx' , l = False )
			mc.setAttr( nameTmp + '.sy' , l = False )
			mc.setAttr( nameTmp + '.sz' , l = False )
			mc.parent(  nameTmp , w = True )
			mc.rename( nameTmp , elem )

	def replace( self , curveA , curveB , worldSpace = 1 ):
		self.createFromCurve( curveB )
		self.delete()

		if(worldSpace):
			curveA = mc.parent( curveA , curveB )
			mc.makeIdentity( curveA , apply = True , t = 1 , r = 1 , s = 1 , n = 0 , pn = 1 )
			curveA = mc.parent( curveA , w = True )
		
		self.createFromCurve( curveA )
		mc.parent( self.names , curveB , s = True , r = True )
		mc.delete(curveA)

	def replaceSameNameFile( self ,  path ):
		listMayaNodesBefore = mc.ls( l = True )	
		mc.file( path , i = True , f = True )
		listMayaNodesAfter = mc.ls( l = True )
		objImported = [obj for obj in listMayaNodesAfter if obj not in listMayaNodesBefore]	


		for obj in objImported:
			baseName = obj.split('|')[-1]
			dupli = mc.ls( ("*"+baseName) , type = 'transform' , l = True )
			if( 1 < len(dupli) ):
				if( obj == dupli[0] ):
					self.replace( obj , dupli[1] )
				elif( obj == dupli[1] ):
					self.replace( obj , dupli[0] )



	def modify( self , **args ):			

		parent         = args.get( 'parent'    , None )	
		colors         = args.get( 'colors'    , None )
		nbrPoints      = args.get( 'nbrPoints' , None )
		degrees        = args.get( 'degrees'   , None )
		coords         = args.get( 'coords'    , None )	
		axe            = args.get( 'axe'       , None )	
		offset         = args.get( 'offset'    , None )	
		position       = args.get( 'position'  , None )	
		form           = args.get( 'form'      , None )	
		scale          = args.get( 'scale'      , 1 )	
			

		if not ( parent    == None ):self.parent    = parent
		if not ( colors    == None ):self.colors    = colors
		if not ( nbrPoints == None ):self.nbrPoints = nbrPoints
		if not ( degrees   == None ):self.degrees   = degrees
		if not ( coords    == None ):self.coords    = coords
		if not ( axe       == None ):self.axe       = axe
		if not ( offset    == None ):self.offset    = offset
		if not ( position  == None ):self.position  = position	
		if not ( form      == None ):self.form      = form
		if not ( scale     == 1    ):self.scale     = scale

		#REBUILD
		#self.printAttrs( 'modif' , self.debug )		
		return 1

	def copy( self , parent ):
		#UPDATE LAST VALUES
		self.createFromCurve( self.names )
		#SWITCH PARENT
		self.parent = parent
		#BUILD
		#self.toObj()
		#DEBUG
		self.printAttrs( 'copy' , self.debug )
		return 1




	def mirror( self , mirrorPlaneCoords , parent = None ):
		self.updateCoords()
		#MIRROR COORDS
		if not( self.coords == [[]] ):
			self.coords   = self.Coords.mirror( mirrorPlaneCoords , overrideCoords = self.coords   )

		return self.coords
	
	def transform( self , value , pivot , iter ):
		self.updateCoords()
		self.Coords.coords = self.coords
		if not( self.coords == [[]] ):
			TrsPivot = trs( pivot )			
			for i in range(0,iter):
				self.Coords.offset( value , pivot[0:3] , 'XYZ')
				TrsPivot.offsetItself( pivot , value )
				pivot = TrsPivot.value
	
			self.coords = self.Coords.coords



	def delete(self):
		mc.delete(self.names)

	def offsetWithMayaObj( self , obj ):
		objTrs = trs()
		objTrs.createFromObj( obj , worldSpace = True )
		#ROTATE COORDS WITH AXE ORIENT
		self.Coords.coords = self.coords 
		self.Coords.offset( objTrs.value , [0,0,0] , ['X','Y','Z'] )
		self.coords = self.Coords.coords		
		return self.coords    



	def updateCoords( self ):
		#CONVERT COORDS
		if not( self.position == None ):
			if( type(self.position) == types.StringType ):
				self.Trs.createFromObj(position)
				self.position = Trs.value

		#RECOMPUTE COORDS
		recomputeCoords = False
		if not( self.form     == None ) and not( self.form     == self.formLast     ): recomputeCoords = True
		if not( self.axe      == None ) and not( self.axe      == self.axeLast      ): recomputeCoords = True
		if not( self.position == None ) and not( self.position == self.positionLast ): recomputeCoords = True
		if not( self.offset   == None ) and not( self.offset   == self.offsetLast   ): recomputeCoords = True	

		if( recomputeCoords )and not( self.form == '' ):
			self.coords = self.getCoords()

			self.formLast     = self.form    
			self.axeLast      = self.axe
			self.positionLast = self.position 
			self.offsetLast   = self.offset[:]



	#________________________________________________________________OUT
	def toFile( self , form ):

		#GET INFO FROM FILE				
		ReadWriteInfo = readWriteInfo.readWriteInfo()
		ReadWriteInfo.createFromFile( self.filePath , latest = 1 )				
		formToCurveInfo = ReadWriteInfo.dict	
		#YELD MESSAGE IF THE NAME ALREADY EXIST
		if( form in formToCurveInfo.keys() ):
			respond = mc.confirmDialog( title='Confirm', message='Name already exist!\nDo you want to Overwrite it?', button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
			if( respond == 'No' ):
				print(' Operation canceled ')
				return 0

		#SAVE NEW CURVE IN DICO
		formToCurveInfo[ form ] = [ self.coords , self.nbrPoints , self.degrees , self.colors ]
		self.formList = formToCurveInfo.keys()

		#SAVE DICO IN FILE
		ReadWriteInfo.dict = formToCurveInfo			
		ReadWriteInfo.toFile( self.filePath , incr = 1 )

		self.printAttrs( 'toFile' , self.debug )		
		return 1

	def selectionToFile( self ):	

		#GET SELECTION			
		selection = mc.ls(sl=True)

		#FILL CLASS ATTR
		self.createFromCurve( selection )
		
		#ASK THE NAME OF THE FORM
		result = mc.promptDialog( title= 'Save Curve Form ', message='Enter name of the form:', button=['OK', 'Cancel'], defaultButton='OK', cancelButton='Cancel', dismissString='Cancel' )	
	
		if( result == 'OK' ):
			form = mc.promptDialog(query=True, text=True)
		else:
			return 0

		#SAVE CURVE
		self.toFile( form )	
		self.printAttrs( 'toFileSelected' , self.debug )		
		return 1
		

	def getCoords( self ):
		self.updateForm( self.form )
		utils_centerWorldTrs = [0,0,0,0,0,0,1,1,1]
		coords = self.utils_rotateCoordsWithAxeOrient( self.coords , self.axe , utils_centerWorldTrs )		
		self.Coords.createFromCoords( coords )
		#OFFSET POSITION
		self.Coords.offset( [0,0,0,0,0,0,self.scale,self.scale,self.scale] , [ 0 , 0 , 0 ] , 'XYZ')		
		if not( self.position == None ):
			self.Coords.offset( self.position , [ 0 , 0 , 0 ] , 'XYZ' )

		if not( self.offset == None ):
			self.Coords.offset( self.offset , [ 0 , 0 , 0 ] , 'XYZ')

		return self.Coords.coords



	def toObj( self , obj , **args ):
		self.updateCoords()
		self.parent = obj

		colors     = args.get( 'colors' , None )	
		names      = args.get( 'names' , None )	
		worldSpace = args.get( 'worldSpace' , True )	

		if not( colors == None ): self.colors = colors

		nbr = len( self.nbrPoints )

		if( names == None ):
			names = []
			for i in range( 0 , nbr ):
				names.append(utilsMaya.incrBaseNameIfExist(  self.parent + 'Shape'  ,  ['']  ,  ['']   ) )

		if( self.colors == [] ): self.colors = [ 'red' ]*nbr
			
		multiCoords = self.utils_separateCoords( self.coords , self.nbrPoints )

		#BUILD EACH CURVE
		self.names = []
		for i in range( 0 , nbr ):
			self.names.append( utilsMaya.buildCurveShape( self.parent , names[i] , multiCoords[i] , self.degrees[i] , self.utils_convertToColorIndex(self.colors[i]) , worldSpace = worldSpace ) )
		
		return 1    



	def toObjCmds( self , obj , **args ):
		self.updateCoords()
		buildCmds = ''
		self.parent = obj

		colors     = args.get( 'colors' , None )	
		names      = args.get( 'names' , None )	
		worldSpace = args.get( 'worldSpace' , True )

		if not( colors == None ): self.colors = colors

		nbr = len( self.nbrPoints )

		if( names == None ):
			names = []
			for i in range( 0 , nbr ):
				names.append( '{}Shape{}'.format(self.parent,i) )

		if( self.colors == [] ): self.colors = [ 'red' ]*nbr
			
		multiCoords = self.utils_separateCoords( self.coords , self.nbrPoints )

		if( self.coords == [[]] ):
			for i in range( 0 , nbr ):
				print( 'SKIP: utilsMaya.buildCurveShape( "{}" , "{}" , {} , {} , {} , worldSpace = {} )\n'.format( self.parent , names[i] , multiCoords[i] , self.degrees[i] , self.utils_convertToColorIndex(self.colors[i]) ,  worldSpace) )
			return ''

		#BUILD EACH CURVE
		for i in range( 0 , nbr ):
			buildCmds += 'utilsMaya.buildCurveShape( "{}" , "{}" , {} , {} , {} , worldSpace = {} )\n'.format( self.parent , names[i] , multiCoords[i] , self.degrees[i] , self.utils_convertToColorIndex(self.colors[i]) ,  worldSpace)
		
		return buildCmds    



	def toSelection( self , axe = None , colors = None , debug = 1 ):	

		selection = mc.ls(sl=True)
		for elem in selection:
			self.toObj( elem , axe , colors )
		self.printAttrs( 'toSelectedObj' , self.debug )		
		return 1



	#________________________________________________________________UTILS

	def utils_rotateCoordsWithAxeOrient( self , coords , axeOrient , trsPivot , oldAxeOrient = 'y' ):
		axeOrientExemple = [ 'x' , 'y' , 'z' , '-x' , '-y' , '-z' , '-x90' , '-y180' , '-z270'     ]

		axe    = 'x'
		sign   = ''
		rotate = ''
		#GET AXE
		if( 'y' in axeOrient ): axe = 'y'
		if( 'z' in axeOrient ): axe = 'z'
		#GET sign and rotate
		axeOrientSplit = axeOrient.split(axe)
		if(len(axeOrient) == 1 ):
			pass
		elif( len(axeOrientSplit) == 2 ):
			sign   = axeOrientSplit[0]+axe
			rotate = axeOrientSplit[1]
		elif( len(axeOrientSplit) == 1 ):
			if( axeOrientSplit[0] == '-' ):
				sign = axeOrientSplit[0]+axe
			else:
				rotate = axeOrientSplit[0]

		
		Coords = coordsClasse.coords()

		rotateToTrs = { '' : [0,0,0, 0,0,0, 1,1,1]  , '90' : [0,0,0, 90,0,0, 1,1,1] , '180' : [0,0,0, 180,0,0, 1,1,1] , '270' : [0,0,0, 270,0,0, 1,1,1] }
		Coords.offset( rotateToTrs[rotate] , [0,0,0] , 'XYZ' , overrideCoords = coords )

		axeToTrs = { 'x' : [0,0,0, 0,0,0, 1,1,1]  , 'y' : [0,0,0, 0,0,90, 1,1,1] , 'z' : [0,0,0, 0,-90,0, 1,1,1] }
		Coords.offset( axeToTrs[axe] , [0,0,0] , 'XYZ' )

		signToTrs = { '' : [0,0,0, 0,0,0, 1,1,1]  , '-x' : [0,0,0, 0,0,0, -1,1,1] , '-y' : [0,0,0, 0,0,0, 1,-1,1] , '-z' : [0,0,0, 0,0,0, 1,1,-1]}
		return Coords.offset( signToTrs[sign] , [0,0,0] , 'XYZ' )

	def utils_separateCoords( self , coords , nbrPoints ):
		
		splitCoords = []
		last = 0

		for size in nbrPoints:
			coordsTmp = []
			begin = last
			end   = begin+size
			for i in range( begin , end ):
				coordsTmp.append(coords[i])
			splitCoords.append(coordsTmp)
			last = end

		return splitCoords



	def utils_mergeCoords( self , splitCoords ):

		coords = []
		nbrPoints = []

		for curveCoords in splitCoords:
			nbrPoints.append( len(curveCoords) / 3 )
			coords += curveCoords


		return [ coords , nbrPoints ]

	



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





	def utils_convertToColorIndex( self , color ):

		if( color in self.fonctionToColorName.keys() ):
			color = self.fonctionToColorName[color]

		if( color in self.colorNameToIndex.keys() ):
			color = self.colorNameToIndex[color]	

		return color

	def getForms( self ):
		ReadWriteInfo = readWriteInfo.readWriteInfo()
		ReadWriteInfo.createFromFile( self.filePath , latest = 1)				
		formToCurveInfo = ReadWriteInfo.dict			
		return formToCurveInfo.keys() 

	def getColors( self ):
		return self.fonctionToColorName.keys() + self.colorNameToIndex.keys()  


	def utils_connectTransformsToCurve( self , transforms , curve ):
		curveShape = mc.listRelatives( curve , s = True , c = True )[0]

		for i in range( len(transforms) ):
			decomposeMatrix = mc.createNode("decomposeMatrix")
			mc.connectAttr( transforms[i] + '.worldMatrix[0]' , decomposeMatrix + '.inputMatrix' )
			mc.connectAttr( decomposeMatrix + '.outputTranslate' , curveShape + '.controlPoints[{}]'.format(i) )


	def utils_getCurveLength( self, curve ):
	    curveShape = mc.listRelatives( curve , c = True , s = True )
	    curveInfoNode = mc.createNode("curveInfo")
	    mc.connectAttr( curveShape[0] + '.local' , curveInfoNode + '.inputCurve' )
	    length = mc.getAttr( curveInfoNode + '.arcLength' )
	    mc.delete( curveInfoNode )
	    return length
	    
	def value(self, **args ):
		return self