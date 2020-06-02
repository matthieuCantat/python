


'''
________________________________________________ CLASS	
alignTool                           
customTmpHotkeyManager              
curveFormBank

'''
import os
import math
import maya.mel as mel
import maya.cmds as mc
import maya.OpenMaya as om
import maya.api.OpenMaya as ompy

from . import utilsPython



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

#================================================================================================================================================================================================================================
#======================================================     CLASS     ===========================================================================================================================================================
#================================================================================================================================================================================================================================


#_____________________________________________________________________________________________________________________________________________________________________ alignTool


class alignTool():

	def __init__(self):		
		self.refCoords     = [ [0,0,0] , [0,0,0] ]
		self.refCoordsBase = [ [0,0,0] , [0,0,0] ]	


	def getAlignCoords( self , lineCoords , oldCoords ):
	
		vectorRef              = om.MVector( ( lineCoords[1][0] - lineCoords[0][0] ) , ( lineCoords[1][1] - lineCoords[0][1] ) , ( lineCoords[1][2] - lineCoords[0][2] ) )
		vectorOldCoords = om.MVector( ( oldCoords[0]      - lineCoords[0][0] ) , ( oldCoords[1]       - lineCoords[0][1] ) , ( oldCoords[2]      - lineCoords[0][2] ) )
		angleA                  = vectorRef.angle( vectorOldCoords )
			
		dist = math.cos( angleA ) * vectorOldCoords.length()
		
		vectorRef.normalize()
			
		newCoords = [  vectorRef.x * dist + lineCoords[0][0] , vectorRef.y * dist + lineCoords[0][1] , vectorRef.z * dist + lineCoords[0][2] ] 
		
		return newCoords
				
				
	def getPlaneLineIntersectionCoords( self , planeCoords , lineCoords , vDirection ):
		
		vDirection.normalize()
		
		# on determine d de la formule du plan  2x + 3y + 7z +d = 0
		
		d = ( ( vDirection.x *  planeCoords[0][0] ) + ( vDirection.y *  planeCoords[0][1] ) + ( vDirection.z *  planeCoords[0][2] ) ) * -1 
		
		# on determine la distance entre le point de la ligne et le point de l'intersection
	
		dist = (   - ( vDirection.x * lineCoords[0] ) - ( vDirection.y * lineCoords[1] ) - ( vDirection.z * lineCoords[2] ) - d  ) / ( ( vDirection.x * vDirection.x ) + ( vDirection.y * vDirection.y ) + ( vDirection.z * vDirection.z )   ) 	
		
		# on determine les coordoonee de l'intersection
		
		iCoords = [  vDirection.x * dist + lineCoords[0] , vDirection.y * dist + lineCoords[1] , vDirection.z * dist + lineCoords[2] ] 
		
		return iCoords
	    
	    
	    
	def get2VectorsNormal( self , vectorA , vectorB , vectorMoyen ):
	    
	    normalx = ((vectorA.y)*(vectorB.z)-(vectorA.z)*(vectorB.y))
	    normaly = ((vectorA.z)*(vectorB.x)-(vectorA.x)*(vectorB.z))
	    normalz = ((vectorA.x)*(vectorB.y)-(vectorA.y)*(vectorB.x))
	    
	    vecteurNormal = om.MVector( normalx , normaly , normalz )
	    
	    coef = self.getSignScalaireProduct(vecteurNormal , vectorMoyen )
	    
	    vecteurNormal = om.MVector( normalx * coef , normaly * coef  , normalz * coef  )
	        
	         
	    return vecteurNormal 

	    
	def getSignScalaireProduct( self , vectorA , vectorRef ):
	    
	    sign = 1
	    
	    dotPoductVector = vectorA * vectorRef 
	    
	    if(dotPoductVector < 0):
	        sign = -1
	        
	    if(dotPoductVector == 0):
	        sign = 1         
	                
	    return sign  

	    
    	
	def doIt( self ):
		
		selection = mc.filterExpand( sm = 31 )
		
		if( selection == None ) or ( len(selection) == 0 ):
			self.refCoords = self.refCoordsBase
			print( 'clear of ref coords' )			
			
		elif( self.refCoords == self.refCoordsBase ) and (  len(selection) == 2 ):
			coordsA = mc.xform( selection[0] , q = True , t = True , ws = True )
			coordsB = mc.xform( selection[1] , q = True , t = True , ws = True )			
			self.refCoords = [ coordsA , coordsB ]
			print( 'save 2 ref coords : line mode' )

		elif( self.refCoords == self.refCoordsBase ) and (  len(selection) == 3 ):
			coordsA = mc.xform( selection[0] , q = True , t = True , ws = True )
			coordsB = mc.xform( selection[1] , q = True , t = True , ws = True )
			coordsC = mc.xform( selection[2] , q = True , t = True , ws = True )			
			self.refCoords = [ coordsA , coordsB , coordsC ]
			print( 'save 3 ref coords : plane mode' )
			
		elif( self.refCoords == self.refCoordsBase ) and not (  len(selection) == 2 ) and not (  len(selection) == 3 ):
			mc.error( 'you must select 2 or 3 objs' )

		else:
			
			for elem in selection:
				oldCoords = mc.xform( elem , q = True , t = True , ws = True )
				
				if( len( self.refCoords ) == 2 ):
					newCoords = self.getAlignCoords( self.refCoords , oldCoords )
				else:
					
					vPlaneA = om.MVector( ( self.refCoords[1][0] - self.refCoords[0][0] ) , ( self.refCoords[1][1] - self.refCoords[0][1] ) , ( self.refCoords[1][2] - self.refCoords[0][2] ) ) 
					vPlaneB = om.MVector( ( self.refCoords[2][0] - self.refCoords[0][0] ) , ( self.refCoords[2][1] - self.refCoords[0][1] ) , ( self.refCoords[2][2] - self.refCoords[0][2] ) ) 	
	
					rawDir   = om.MVector( ( self.refCoords[0][0] - oldCoords[0] ) , ( self.refCoords[0][1] - oldCoords[1] ) , ( self.refCoords[0][2] - oldCoords[2] ) )
	
					vPlaneNormal = self.get2VectorsNormal( vPlaneA , vPlaneB , rawDir )
					
					newCoords = self.getPlaneLineIntersectionCoords( self.refCoords , oldCoords , vPlaneNormal ) 
					
				
				mc.xform( elem , t = newCoords , ws = True )
			


	

#_____________________________________________________________________________________________________________________________________________________________________ customTmpHotkeyManager



class customTmpHotkeyManager():
	
	'''
		create hotkey linked to custom script. When it is active a window open. when the window is closed, all hotkeys are delete.
		
		
		Here is the tricky thing for saving a python script as script lauch when hotkey is pressed:
		pythonScript ---in---> runTimeCommand ---in---> nameCommand ---in----> hotkey
		You must to pass throught all these steps.
		
		warning if you dont want the hotkey in the defaultHotkeySet , you must precise at each step default = False
		
	
	'''

	
	def __init__(self):
		self.var = 'customTmpHotkeyVar'
		self.nameSpace = ''		
		#====== tool
		self.hotkeysInfo = []
		self.lastKeySet    = ''
		self.newKeySet     = 'customTmpHotkeyManagerSet'
		self.customCmdBaseName = 'TmpHotkeyCmd'
		self.runTimeCmdNames = []		
		#====== UI
		self.win = 'customTmpHotkeyManagerWin'
		self.winTitle = 'Hotkey Manager'
		self.firstColumn = 'firstColumn'
		self.secondColumn = 'secondColumn'
		self.whMainWin = [ 300 , 200 ]
		self.wInterSpace = 5
		self.wMiddleColumn = 190



	def doIt(self):
		self.createHotkeySet()
		self.launchHotkeys()	
		self.buildUI()				
		
		
		
	def addHotkey( self , name , letter , specialButton , cmd ):		
		self.hotkeysInfo.append( [ name , letter , specialButton , cmd ]  )

		
	def createHotkeySet(self):

		hotkeySetArray =  mc.hotkeySet( q = True, hotkeySetArray = True )	
		if( self.newKeySet in hotkeySetArray ):
			mc.hotkeySet( self.newKeySet , e = True , delete = True  )
		
		self.lastKeySet = mc.hotkeySet( q = True, current = True ) 
		mc.hotkeySet( self.newKeySet , current = True , source = self.lastKeySet )		
	
	def deleteHotkeySet(self):	
		mc.hotkeySet( self.newKeySet  , e = True , delete = True )			
		for runTimeCmdName in self.runTimeCmdNames:
			melToEval = 'runTimeCommand -e -delete {0}; '.format( runTimeCmdName )
			mel.eval(melToEval)
		mc.hotkeySet( self.lastKeySet ,e = True , current = True )
				
	def launchHotkeys(self):
		

		if( len(self.hotkeysInfo) == 0 ):
			mc.error( 'first add some hotkeys with:  addHotkey( letter , specialButton , cmd )' )
			

		for keyInfo in self.hotkeysInfo:
			runTimeCmdName = keyInfo[0] + '_' + self.customCmdBaseName
			self.runTimeCmdNames.append(runTimeCmdName)				
			nameCmdName    = runTimeCmdName  + 'NameCommand'

			specialKeys = [0,0,0]
			
			if( keyInfo[2] == 'ctrl' ):
				specialKeys = [1,0,0]
			elif( keyInfo[2] == 'alt' ):
				specialKeys = [0,1,0]			
			elif( keyInfo[2] == 'shift' ):
				specialKeys = [0,0,1]		

			melToEval = 'runTimeCommand -annotation "" -category "Custom Scripts" -hotkeyCtx "" -default false -commandLanguage "python" -command ( "{0}" ) {1} ; '.format( keyInfo[3] , runTimeCmdName )
		
			mel.eval(melToEval)					
			mc.nameCommand( nameCmdName , sourceType = 'mel' , annotation = nameCmdName , command = runTimeCmdName , default = False )					
			mc.hotkey( k= keyInfo[1] , ctl= specialKeys[0] , alt = specialKeys[1] , sht = specialKeys[2] ,  ctxClient = '' , name = nameCmdName  )
			


		
	def buildUI(self):
		
		if( mc.window( self.win  , ex = True ) ):
			mc.deleteUI(self.win)
		
		mc.window( self.win  , wh = self.whMainWin , s = True , t = self.winTitle )  

		mc.rowColumnLayout( self.firstColumn , nc = 3 , p = self.win )

		mc.text( l = '' , w = self.wInterSpace , p = self.firstColumn )
		
		mc.columnLayout( self.secondColumn , w = self.wMiddleColumn ,  p = self.firstColumn   )
			
		for keyInfo in self.hotkeysInfo:
			mc.text( l = ( keyInfo[1] + ' + ' + keyInfo[2] + '     ---->     ' + keyInfo[0] ) , h = 20 , w = self.wMiddleColumn  , p = self.secondColumn )
		mc.text( l = '' , h = 5 )
		
		mc.button( l = 'CLOSE' , c = ( '{0}.{1}.deleteHotkeySet();{0}.{1}.closeUI()'.format(self.nameSpace , self.var) )  , h = 20 , w = self.wMiddleColumn , bgc = [ 0.4 , 0.7 , 0.4 ] , p = self.secondColumn )
		
		mc.text( l = ''  , h = 5 , w = self.wMiddleColumn , p = self.secondColumn )		
		mc.text( l = '       WARNING       ' , bgc = [ 0.8 , 0.4 , 0.4 ] , w = self.wMiddleColumn , p = self.secondColumn )
		mc.text( l = 'DONT ENTER NEW HOTKEY' , bgc = [ 0.8 , 0.4 , 0.4 ] , w = self.wMiddleColumn , p = self.secondColumn )
		
			
		mc.text( l = '' , w = 10 , p = self.firstColumn)
		
		mc.showWindow(self.win)	

	def closeUI(self):
		mc.deleteUI(self.win)
		
	def launchScriptJob(self):
		pass


		
		
		
#_____________________________________________________________________________________________________________________________________________________________________ curveFormBank		
			


class curveFormBank():
	
	'''
		store the differents shape coords and degree in a XML file
	'''
	
	def __init__(self):
	
		self.fileBaseName = 'curveFormBank' 		
		self.path = utilsPython.getActualPath()
		self.pathPictures = self.path + 'cruveFormBankPictures/'
		self.formPictures = os.listdir(self.pathPictures)
		
		
		
		utilsPython.createXmlDicoVar( self.fileBaseName , self.path )		
		dicoFormName  = utilsPython.readXmlDicoVar( self.fileBaseName , self.path )	
		
		self.formNames = dicoFormName.keys()
		self.formNames.sort()

	
	def saveSelectedForm( self ):				
		selection = mc.ls(sl=True)
		
		if ( len(selection) == 1 ) and ( mc.nodeType( selection[0] ) == 'nurbsCurve' ):
			pass
		else:
			mc.error('You must select one curveShape')
			
		result = mc.promptDialog( title= 'Save Curve Form ', message='Enter name of the form:', button=['OK', 'Cancel'], defaultButton='OK', cancelButton='Cancel', dismissString='Cancel' )	
	
		if( result == 'OK' ):
			formName = mc.promptDialog(query=True, text=True)
		else:
			return 0
	
		curveShapeName = selection[0]				
		curveCoords    = getCurveCoords( curveShapeName )
		curveDegree    = mc.getAttr( curveShapeName +'.degree' )	
		
		self.saveForm( formName , curveCoords , curveDegree )
		
		print('=== Curve Form Saved ===')
	
		return 1

		
		
	def saveForm( self, formName , curveCoords , degree ):
		dicoFormName = utilsPython.readXmlDicoVar( self.fileBaseName , self.path )
		
		if( formName in dicoFormName.keys() ):
			respond = mc.confirmDialog( title='Confirm', message='Name already exist!\nDo you want to Overwrite it?', button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
			if( respond == 'No' ):
				print(' Operation canceled ')
				return 0
				
		dicoFormName[ formName ] = [ curveCoords , degree ]
		self.formList = dicoFormName.keys()		
		utilsPython.writeXmlDicoVar(  self.fileBaseName , self.path , dicoFormName )
		
		return 1

	
		
	def getForm( self , formName ):	
		dicoFormName = utilsPython.readXmlDicoVar( self.fileBaseName , self.path )
		
		toEval = 'coordsFloatList = ' + dicoFormName[formName][0]
		exec(toEval)
		
		degree = int( dicoFormName[formName][1] )
		
		return [ coordsFloatList , degree ] 			
		
		
	def getFormCoords( self , formName ):	
		return self.getForm( formName )[0]
		
	def getFormDegree( self , formName ):
		return self.getForm( formName )[1]	
				
		
				
		
	def getFormNameFromCurve( self , curveName ):	

		curveCoords   = getCurveCoords( curveName )
		formSameIndex = []		
		fromName      = ''
	
		#____________________________________________________________________
		for form in self.formNames:
			coords = self.getFormCoords(form)

			if( len(curveCoords) == len(coords) ):
				formSameIndex.append(form)

		#____________________________________________________________________				
		distA       = ompy.MVector( curveCoords[1][0] - curveCoords[0][0] , curveCoords[1][1] - curveCoords[0][1] , curveCoords[1][2] - curveCoords[0][2] ).length()
		distB       = ompy.MVector( curveCoords[2][0] - curveCoords[0][0] , curveCoords[2][1] - curveCoords[0][1] , curveCoords[2][2] - curveCoords[0][2] ).length()
		rapportRef  = distA / distB	
		#____________________________________________________________________			
		lastDiff = 999999999999999999999999999999
		

		
		for form in formSameIndex:
			
			coords  = self.getFormCoords(form)		
			distA   = ompy.MVector( coords[1][0] - coords[0][0] , coords[1][1] - coords[0][1] , coords[1][2] - coords[0][2] ).length()
			distB   = ompy.MVector( coords[2][0] - coords[0][0] , coords[2][1] - coords[0][1] , coords[2][2] - coords[0][2] ).length()
			rapport = distA / distB
			diff    = abs(rapportRef - rapport)
			
			
			
			if( diff < lastDiff ):
				formName = form				
				lastDiff = diff
	
		return formName

		
		


















