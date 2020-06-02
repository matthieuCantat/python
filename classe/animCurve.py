'''
#******************************************************** BUILD EXEMPLE 
import maya.cmds as mc
import python
from python.classe.animCurve import *
reload( python.classe.animCurve)


reload( python.classe.readWriteInfo)

#CREATE
anim = animCurve()	
anim.createFromSelection()
anim.delete()
anim.toObjs() 

anim.toObjs( inverse = True , startFrame = 1080 ) 

anim.getInfo() 
anim.getObjs() 
anim.getMatchObjs('l_reactorArmPropulsorHandle_CTRL') 

anim.toMatchSelection( mirror = 'X' , replace = True )

mc.select(anim.goMatchObjs('l_reactorArmPropulsorHandle_CTRL'))



#CREATE FROM FILE
anim.delete()
path = 'D:/mcantat_BDD/projects/cute/carrierShipD/maya/scenes/animCurves/test.xml'
anim.toFile( path , info = 'test test test 123 ultime' )

newAnim = animCurve()	
newAnim.createFromFile(path)
newAnim.toObjs()
newAnim.getInfo() 
newAnim.getObjs() 
newAnim.objsAttrs




'''


import maya.cmds as mc
import math


from . import coords as coordsClasse
from . import readWriteInfo
from ..utils import utilsMaya
from ..utils import utilsPython
from ..utils import utilsMath
from ..utils import utilsMayaApi
from .mayaClasse import *
from .trsBackUp import *
from .buildName import *



class animCurve(mayaClasse):
	
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
	utils_getKnotIndexes
	'''
	
	def __init__(self):

		self.type      = 'animCurve'
		self.debug     = 0		
		#CURVE INFO	
		self.filePath  = ''	
		self.info      = ''
		self.nodes       = []
		self.objsAttrs   = []
		self.times       = []
		self.values      = []
		self.tLock       = []
		self.tWeightLock = []
		self.tInType     = []
		self.tInX        = []
		self.tInY        = []
		self.tOutType    = []
		self.tOutX       = []
		self.tOutY       = []
		self.breakdown   = []
		self.others      = []


	def printAttrs( self , title = '' , printInfo = 1 ):
		if( printInfo == 1 ):
			print('START_____________________________ ' + title)
			print('**********ATTRS***********')
			for i in range(0,len(self.objsAttrs )):
				print( '{} {}'.format( self.objsAttrs[i] , self.values[i] ) )
			print('END________________________________ ' + title)

	#________________________________________________________________CREATE

	def createFromObjs( self , objs , bakedValue = False , worldSpace = False ):
		print('animCurve createFromObjs')
		self.nodes       = []
		self.objsAttrs   = []
		self.times       = []
		self.values      = []
		self.tLock       = []
		self.tWeightLock = []
		self.tInType     = []
		self.tInX        = []
		self.tInY        = []
		self.tOutType    = []
		self.tOutX       = []
		self.tOutY       = []
		self.breakdown   = []
		self.others      = []

		for obj in objs:

			inConnections = mc.listConnections( obj , s = True , d = False , p = True , c = True )

			if( inConnections == None ): continue

			for j in range(0,len(inConnections) , 2):
				outObjAttr , inObjAttr = inConnections[j+0] , inConnections[j+1]
				outObj     , outAttr   = outObjAttr.split('.')
				inObj      , inAttr    = inObjAttr.split('.')

				if( 'animCurve' in mc.nodeType(inObj) ):

					times       = []
					values      = []
					tLock       = []
					tWeightLock = []
					tInType     = []
					tInX        = []
					tInY        = []
					tOutType    = []
					tOutX       = []
					tOutY       = []
					breakdown   = []

					animKeysNbr = mc.getAttr( inObj + '.keyTimeValue' , size = True )

					for i in range( animKeysNbr ):
						times.append(       mc.getAttr( '{}.keyTimeValue[{}]'.format(    inObj,i) )[0][0] )
						values.append(      mc.getAttr( '{}.keyTimeValue[{}]'.format(    inObj,i) )[0][1] )
						if(bakedValue == False):
							tLock.append(       mc.getAttr( '{}.keyTanLocked[{}]'.format(    inObj,i) )    )
							tWeightLock.append( mc.getAttr( '{}.keyWeightLocked[{}]'.format( inObj,i) )    )
							tInType.append(     mc.getAttr( '{}.keyTanInType[{}]'.format(    inObj,i) )    )
							tInX.append(        mc.getAttr( '{}.keyTanInX[{}]'.format(       inObj,i) )    )
							tInY.append(        mc.getAttr( '{}.keyTanInY[{}]'.format(       inObj,i) )    )
							tOutType.append(    mc.getAttr( '{}.keyTanOutType[{}]'.format(   inObj,i) )    )
							tOutX.append(       mc.getAttr( '{}.keyTanOutX[{}]'.format(      inObj,i) )    )
							tOutY.append(       mc.getAttr( '{}.keyTanOutY[{}]'.format(      inObj,i) )    )
							breakdown.append(   mc.getAttr( '{}.keyBreakdown[{}]'.format(    inObj,i) )    )

					if(bakedValue == False):
						tType        = mc.getAttr( '{}.tangentType'.format(      inObj ) )
						tWeighted    = mc.getAttr( '{}.weightedTangents'.format( inObj ) )
						preInfinity  = mc.getAttr( '{}.preInfinity'.format(      inObj ) )
						postInfinity = mc.getAttr( '{}.postInfinity'.format(     inObj ) )

					print( inObj , values )

					self.nodes.append(       inObj       )
					self.objsAttrs.append(   outObjAttr  )
					self.times.append(       times       )
					self.values.append(      values      )
					if(bakedValue == False):
						self.tLock.append(       tLock       )
						self.tWeightLock.append( tWeightLock )
						self.tInType.append(     tInType     )
						self.tInX.append(        tInX        )
						self.tInY.append(        tInY        )
						self.tOutType.append(    tOutType    )
						self.tOutX.append(       tOutX       )
						self.tOutY.append(       tOutY       )
						self.breakdown.append(   breakdown   )
						self.others.append( [ tType , tWeighted , preInfinity , postInfinity ] )




		return 1
		
	def createFromSelection( self ):
		selection = mc.ls(sl=True)
		self.createFromObjs( selection )
		return 1

	def createFromFile( self , filePath , latest = 1 ):
		print('animCurve createFromFile')
		self.filePath = filePath
		#GET INFO FROM FILE				
		ReadWriteInfo = readWriteInfo.readWriteInfo()
		ReadWriteInfo.createFromFile( self.filePath , latest = latest)				
		dictAnim = ReadWriteInfo.dict	
		#FILL CLASS ATTR
		self.objsAttrs   = [ key for key in dictAnim.keys() if not( key == 'info' ) ]
		self.times       = []
		self.values      = []
		self.tLock       = []
		self.tWeightLock = []
		self.tInType     = []
		self.tInX        = []
		self.tInY        = []
		self.tOutType    = []
		self.tOutX       = []
		self.tOutY       = []
		self.breakdown   = []
		self.others      = [] # preInfinity , postInfinity , weightTan

		for objAttr in self.objsAttrs:
			self.times.append(       dictAnim[objAttr][0] )       
			self.values.append(      dictAnim[objAttr][1] )
			if( 2 < len(dictAnim[objAttr]) ):      
				self.tLock.append(       dictAnim[objAttr][2] )       
				self.tWeightLock.append( dictAnim[objAttr][3] ) 
				self.tInType.append(     dictAnim[objAttr][4] )     
				self.tInX.append(        dictAnim[objAttr][5] )        
				self.tInY.append(        dictAnim[objAttr][6] )        
				self.tOutType.append(    dictAnim[objAttr][7] )    
				self.tOutX.append(       dictAnim[objAttr][8] )       
				self.tOutY.append(       dictAnim[objAttr][9] )       
				self.breakdown.append(   dictAnim[objAttr][10] )   
				self.others.append(      dictAnim[objAttr][11] )

		self.info = dictAnim['info']       

		self.printAttrs( 'createFromFile' , self.debug )				
		return 1		


	#________________________________________________________________MODIF

	def delete(self):
		mc.delete(self.nodes)


	#________________________________________________________________OUT
	def toFile( self , filePath , info = None , incr = 1 , clearOldVar = 1):
		print('animCurve toFile')
		self.filePath = filePath
		#GET INFO FROM FILE				
		ReadWriteInfo = readWriteInfo.readWriteInfo()
		'''
		ReadWriteInfo.createFromFile( self.filePath , latest = 1 )				
		dictAnim = ReadWriteInfo.dict	
		'''

		dictAnim = {}
		for i in range(0,len(self.objsAttrs)):
			key = self.objsAttrs[i]
			dictAnim[key] = []
			dictAnim[key].append( self.times      [i] )
			dictAnim[key].append( self.values     [i] )
			if( 0 < len( self.tLock)       ):dictAnim[key].append( self.tLock      [i] )
			if( 0 < len( self.tWeightLock) ):dictAnim[key].append( self.tWeightLock[i] )
			if( 0 < len( self.tInType)     ):dictAnim[key].append( self.tInType    [i] )
			if( 0 < len( self.tInX)        ):dictAnim[key].append( self.tInX       [i] )
			if( 0 < len( self.tInY)        ):dictAnim[key].append( self.tInY       [i] )
			if( 0 < len( self.tOutType)    ):dictAnim[key].append( self.tOutType   [i] )
			if( 0 < len( self.tOutX)       ):dictAnim[key].append( self.tOutX      [i] )
			if( 0 < len( self.tOutY)       ):dictAnim[key].append( self.tOutY      [i] )
			if( 0 < len( self.breakdown)   ):dictAnim[key].append( self.breakdown  [i] )
			if( 0 < len( self.others)      ):dictAnim[key].append( self.others     [i] )

		if( info == None ):dictAnim['info'] = self.info
		else:              dictAnim['info'] = info

		#SAVE DICO IN FILE
		ReadWriteInfo.dict = dictAnim			
		ReadWriteInfo.toFile( self.filePath , incr = incr , clearOldVar = clearOldVar )

		self.printAttrs( 'toFile' , self.debug )		
		return 1

	def getInfo( self ):
		return self.info

	def getRange( self ):

		min = 999999999999999999999999.0
		max = -99999999999999999999999.0

		for i in range(len(self.times)):
			for j in range(len(self.times[i])):
				if(       self.times[i][j] < min ): min = self.times[i][j]
				if( max < self.times[i][j]       ): max = self.times[i][j]

		return [ min , max ]

	def getObjs( self ):
		objs = []
		for i in range(0,len(self.objsAttrs)):
			objs.append( self.objsAttrs[i].split('.')[0] )

		objs = list(set(objs))
		return objs

	def selectObjs( self ):
		mc.select(self.getObjs())

	def getNodes( self ):
		return self.nodes

	def getMatchObjs( self , objToMatch ):
		objs = self.getObjs()

		Names = buildName()
		convertedObjs = Names.convertNamesToMatchExemple( objs , objToMatch )

		return convertedObjs


	def toObjs( self , **args ):

		replace       = args.get( 'replace' , False )	
		inverse       = args.get( 'inverse' , False ) 
		startFrame    = args.get( 'startFrame' , self.getRange()[0] )
		objsToFilter  = args.get( 'objsToFilter' , None )
		matchObjName  = args.get( 'matchObjName' , None ) 
		mirror        = args.get( 'mirror' , None ) 
		overrideNamespace = args.get( 'overrideNamespace' , None )  

		tanType = ['clamped', 'fast', 'flat', 'linear', 'plateau', 'slow', 'spline', 'step next' , 'fixed' , 'stepped' ]
		# default: keyTangent 
		listCmdsTanType = []
		listCmdsTanType.append('fixed' )
		listCmdsTanType.append('linear')
		listCmdsTanType.append('flat')
		listCmdsTanType.append('step')
		listCmdsTanType.append('slow')
		listCmdsTanType.append('fast')
		listCmdsTanType.append('spline')
		listCmdsTanType.append('clamped')
		listCmdsTanType.append('plateau')
		listCmdsTanType.append('stepnext')
		listCmdsTanType.append('auto')

		dictNodeTanType = {}
		dictNodeTanType['1']  = listCmdsTanType[0]#'Fixed'
		dictNodeTanType['2']  = listCmdsTanType[1]#'Linear'
		dictNodeTanType['3']  = listCmdsTanType[2]#'Flat'
		dictNodeTanType['5']  = listCmdsTanType[3]#'Step'
		dictNodeTanType['6']  = listCmdsTanType[4]#'Slow'
		dictNodeTanType['7']  = listCmdsTanType[5]#'Fast'
		dictNodeTanType['9']  = listCmdsTanType[6]#'Spline'
		dictNodeTanType['10'] = listCmdsTanType[7]#'Clamped'
		dictNodeTanType['16'] = listCmdsTanType[8]#'Plateau'
		dictNodeTanType['17'] = listCmdsTanType[9]#'StepNext'
		dictNodeTanType['18'] = listCmdsTanType[10]#'Auto'







		#RANGE
		curentRange = self.getRange()
		middleRange = ( curentRange[0] + curentRange[1] ) / 2
		offsetFrame = startFrame - curentRange[0]

		#MATCH OBJ
		objs = self.getObjs()
		matchObjs = objs
		if not( matchObjName == None):
			matchObjs = self.getMatchObjs( matchObjName )


		for i in range(len(self.objsAttrs)):

			outObj , outAttr = self.objsAttrs[i].split('.')

			objsAttr = outObj +'.'+ outAttr

			if( matchObjName ):
				iTmp = objs.index(outObj)
				outObj = matchObjs[iTmp]
				objsAttr = outObj +'.'+ outAttr

			if not( overrideNamespace == None):
				if( ':' in objsAttr ):
					if( overrideNamespace == ''):
						objsAttr = objsAttr.split(':')[1]
					else:
						objsAttr =  overrideNamespace + ':' + objsAttr.split(':')[1]
				else:
					if not( overrideNamespace == ''):
						objsAttr =  overrideNamespace + ':' + objsAttr


			if not( mc.objExists(objsAttr) ):
				print('animCurve - toObjs - ATTR DOESNT EXISTS - {}'.format(objsAttr))
				continue


			if( objsToFilter ) and not( outObj in objsToFilter ): continue

			if( replace ):
				inConnections = mc.listConnections( objsAttr , s = True , d = False  )
				if( 'animCurve' in mc.nodeType( inConnections[0] ) ):
					mc.delete( inConnections[0] )

			inverseMult = 1
			if( inverse ):
				inverseMult = -1


			for j in range( len(self.values[i]) ):

				time = ( self.times[i][j] - middleRange ) * inverseMult + middleRange + offsetFrame
				
				value = self.values[i][j]
				#if( '.rotate' in objsAttr ):value = math.degrees(self.values[i][j])
				if(mirror)and( '.translateX' in objsAttr ): value = self.values[i][j] * -1
				if(mirror)and( '.translateY' in objsAttr ): value = self.values[i][j] * -1
				if(mirror)and( '.translateZ' in objsAttr ): value = self.values[i][j] * -1
				if(mirror)and( 'TranslateX' in objsAttr ): value = self.values[i][j] * -1
				if(mirror)and( 'TranslateY' in objsAttr ): value = self.values[i][j] * -1
				if(mirror)and( 'TranslateZ' in objsAttr ): value = self.values[i][j] * -1

				mc.setKeyframe( objsAttr , t=time        , v = value  )

				if not(self.breakdown == []):
					mc.setKeyframe( objsAttr , e = True , t=time , v = value , bd = self.breakdown[i][j] )
				
				if not(self.tInType == []):
					mc.keyTangent(  objsAttr , t=(time,time) , itt = dictNodeTanType['{}'.format(self.tInType[i][j])] , ott = dictNodeTanType['{}'.format(self.tOutType[i][j])] , ix = self.tInX[i][j] , iy = self.tInY[i][j] , ox = self.tOutX[i][j] , oy = self.tOutY[i][j] , l = self.tLock[i][j] ) #, wl = self.tWeightLock[i][j] )

			if not(self.others == []):
				try:   mc.setInfinity( objsAttr , pri = self.others[i][2] , poi = self.others[i][3] )
				except:print('animCurve - toObjs - setInfinity issue - {}'.format(objsAttr))
			#mc.getAttr( '{}.tangentType'.format(      inObj ) , self.others[i][0] )
			#mc.getAttr( '{}.weightedTangents'.format( inObj ) , self.others[i][1] )




	def toMatchObjs( self , objToMatch , **args ):
		args['matchObjName'] = objToMatch	
		self.toObjs( **args )
		return 1    

	def toMatchSelection( self , **args ):
		args['matchObjName'] = mc.ls(sl=True)[0]	
		self.toObjs( **args )
		return 1    

	def toSelection( self  , **args ):	
		args['objsToFilter'] = mc.ls( sl = True )	
		self.toObjs( **args )	
		return 1


	def removeUnchangedKeys( self , **args ):

		for i in range(0,len(self.objsAttrs)):

			currentValues   = [ round(value,3) for value in self.values[i] ]
			unchangedValues = [ round(self.values[i][0],3) ]* len(self.times[i])
			if( currentValues == unchangedValues ):
				self.times[i]  = [ self.times[i][0] ,self.times[i][-1]  ]
				self.values[i] = [ self.values[i][0],self.values[i][-1] ]

				if( 0 < len(self.tLock)       ): self.tLock[i]       = self.tLock[i][0]
				if( 0 < len(self.tWeightLock) ): self.tWeightLock[i] = self.tWeightLock[i][0]
				if( 0 < len(self.tInType)     ): self.tInType[i]     = self.tInType[i][0]
				if( 0 < len(self.tInX)        ): self.tInX[i]        = self.tInX[i][0]
				if( 0 < len(self.tInY)        ): self.tInY[i]        = self.tInY[i][0]
				if( 0 < len(self.tOutType)    ): self.tOutType[i]    = self.tOutType[i][0]
				if( 0 < len(self.tOutX)       ): self.tOutX[i]       = self.tOutX[i][0]
				if( 0 < len(self.tOutY)       ): self.tOutY[i]       = self.tOutY[i][0]
				if( 0 < len(self.breakdown)   ): self.breakdown[i]   = self.breakdown[i][0]



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

	def utils_buildCurveShape( self , transformName , shapeName , coords , degree , colorIndex , position = None , trsOffset = None  , worldSpace = True ):		
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
		knot = self.utils_getKnotIndexes( Coords.coords , degree )
				
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



	def utils_getKnotIndexes( self , coords , degree ):

		nbrKnot = len(coords)/3 + degree - 1  		#_knot	= spans + 2 degree - 1	degree first knot identical    and   degree las knot identical	
		
		knot = []
		for i in range( 0 , degree ):
			knot.append(0)
			
		for i in range( degree , nbrKnot - degree):
			knot.append(i)
				
		for i in range( 0 , degree ):
			knot.append(nbrKnot - degree)

		return knot


	def utils_convertToColorIndex( self , color ):

		if( color in self.fonctionToColorName.keys() ):
			color = self.fonctionToColorName[color]

		if( color in self.colorNameToIndex.keys() ):
			color = self.colorNameToIndex[color]	

		return color

	def getForms( self ):
		return self.forms

	def getColors( self ):
		return self.fonctionToColorName.keys() + self.colorNameToIndex.keys()  






