'''

#******************************************************** BUILD EXEMPLE RIG CTRL
import maya.cmds as mc
import python
from python.classe.rigCtrl import *
from python.classe.mayaRig import *
reload(python.classe.mayaClasse)
reload(python.classe.mayaObject)
reload(python.classe.mayaRig)
reload(python.classe.rigCtrl)
#=================================================


manipA = mayaObject()

manipA = mayaRig()


manipA = rigCtrl( )	

manipA = rigCtrl( n = 'manipA' , pos = [5,0,3,0,0,0,1,1,1] , form = 'cube' , colors = [13] )	

# REF

from python.classe.buildName import *
reload(python.classe.buildName)
from python.classe.buildCurveShape import *
reload(python.classe.buildCurveShape)
from python.classe.buildPosition import *
reload(python.classe.buildPosition)

Name = buildName( )
Name.setBaseName('manip')
Name.add( 'manipB'        , appendBaseName = 'B'    )

Pos = buildPosition()
Pos.add(  'manipB'      , [5,0,-3,0,0,0,1,1,1]  )

cShape = buildCurveShape()
cShape.add(  'manipB' , form = 'sphere'   , colors = [13] , axe = 'x' , offset = [0,0,0,0,0,0,1,1,1]   )

manipB = rigCtrl( n = Name.manipB , pos = [ Pos.manipB ] , shape = CurveShape.manipB )	


print('____________________MODIF')
print('____________________BUILD')
manipA.build()
manipB.build()


'''

from .mayaObject import *

class mayaRig(mayaObject):

	'''
		Basic rigs
			no ctrl

		FONCTION:		
			-modif
			-buildCustom
			-buildRig

		IN MAYA:			
			top node
				+ ATTR scale
				+ ATTR classeInfoAttr
	'''	

	def __init__( self , **args ):
		mayaObject.__init__( self , **args )
		#mayaObject.__init__(self)
		#print("init mayaRig")
		#UTILS			
		#CLASSE
		self.classeType = 'mayaRig'
		self.depthLevel = 0															
		#INSTANCE_______________________________BLUEPRINT
		self.Name.add( 'base'    , baseName = self.classeType )			
		self.Name.add( 'topNode' , ref = self.Name.base , baseNameAppend = 'Top' , type = 'GRP'  )
		self.Dag.add(  'topNode' , Name = self.Name.topNode   , type = 'transform' )
		self.Attr.add( 'topNode' , Name = self.Name.topNode  )

		#INSTANCE_______________________________INFO
		self.ins        = []
		self.insAnim    = []
		self.outs       = []
		self.ctrls      = []
		self.ctrlsDupli = []

	def buildMayaObject( self ):
		#self.toMayaObj( self.Name.topNode.str() )
		self.buildMayaRig()

	def buildMayaRig( self ):
		pass



'''



	#################################################################################################################################################################################		
	# IN ################################################################################################################################################################################# CREATE 
	################################################################################################################################################################################# 
	def createFromMayaObjCustom( self , value , **args ):
		self.mainGrp = self.getMainGrp( value )
		self.createFromMayaObjAttr( value )
		self.readClassAttrOnUserModifyRig()

	def createFromMayaObjsCustom( self , value , **args ): 
		Trs = trs.trs()
		#ARGS
		worldSpace    = args.get( 'updateBaseName' , 1 )
		#MODIF 
		self.buildTrs = [ Trs.createFrom(obj) for obj in value ]
		if( updateBaseName == 1 ): self.baseName = value[0]


	#################################################################################################################################################################################		
	# OUT ################################################################################################################################################################################# CREATE 
	################################################################################################################################################################################# 
	def buildMayaObjs( self , inValue ): return self.buildRig()

	def buildCustom( self ):
		return self.buildRig()

	def buildRig( self ):
		#BUILD MAIN GRP
		self.mainGrp = self.side + self.baseName + self.utilsNameBaseRig + self.utilsNameSuffixGrp
		self.utils_buildMainGrp( self.mainGrp ) 

		#BUILD RIG CUSTOM_______________________________________( TO MODIF IN CHILDREN)
		self.buildRigCustom()

		#WRITE AND CONNECT MAIN GRP ATTR
		self.utils_buildAttrInsOuts( self.mainGrp , self.ins , self.outs , self.insConnections , self.outsConnections , self.mainGrpAttrNameInsPrefix , self.mainGrpAttrNameOutsPrefix)		
		#BUILD SETS
		self.mainSet = self.side + self.baseName + self.utilsNameBaseRig +'_set'
		self.animSet = self.side + self.baseName + self.utilsNameBaseRig +'_animSet'	
		self.outSet  = self.side + self.baseName + self.utilsNameBaseRig +'_outSet'		
		names    = [ self.mainSet   , self.animSet , self.outSet  ]
		parents  = [ ''             , self.mainSet , self.mainSet ]
		contents = [ [self.mainGrp] , self.ctrls   , self.outs    ]		
		self.alls += utilsMaya.createSets( names , parents , contents )	
		#SAVE CLASS ATTR
		self.toMayaObjAttr( self.mainGrp )	

	def buildRigCustom( self ):return None


	def buildTemplate( self ): return None
	#################################################################################################################################################################################		
	# MODIF ################################################################################################################################################################################# CREATE 
	################################################################################################################################################################################# 			



	#################################################################################################################################################################################		
	# UTILS ################################################################################################################################################################################# CREATE 
	################################################################################################################################################################################# 

	def getMainGrp( self , elem  , masterRig = 0 ):		
		#masterRig == 0 prend le premier rig grp qui arrive       masterRig == 1 prend le dernier rig grp qui arrive		

		self.mainGrp = elem
		loop = 0	
		if( masterRig == 1 ): 
			while( mc.objExists( self.mainGrp + '.' + self.beaconAttrNameMainGrp )  ):
				self.mainGrp = mc.getAttr( self.mainGrp + '.' + self.beaconAttrNameMainGrp )
				loop +=1
				if( loop > 400 ):
					mc.error('loop')
		else:
			if not( mc.objExists( self.mainGrp + '.' + self.mainGrpAttrNameRigType ) ) and ( mc.objExists( self.mainGrp + '.' + self.beaconAttrNameMainGrp ) ):
				self.mainGrp = mc.getAttr( self.mainGrp + '.' + self.beaconAttrNameMainGrp )			
				
		return self.mainGrp 
    
	def isRigElem( self , elemToAnalyse  , getMasterRig = 1 ):
		if( mc.objExists( elemToAnalyse + '.' + self.beaconAttrNameMainGrp ) ):		
			self.getMainGrp( elemToAnalyse , getMasterRig )	
			rwi     = readWriteInfo.readWriteInfo()
			rigType = rwi.read( self.beaconAttrNameMainGrp , overrideObj = self.mainGrp ) 	
			if( rigType ==  self.type ):
				return True
		
		return False


	def readClassAttrOnUserModifyRig( self ):
		#GET THE NEW CONNECTION
		self.insConnections   = []
		for inObj in self.ins :
			attrName = self.mainGrp + '.' + self.mainGrpAttrNameInsPrefix + inObj 
			self.insConnections = mc.listConnections( attrName , s = True , d = False )[0]

		self.outsConnections   = []
		for outObj in self.outs :
			attrName = self.mainGrp + '.' + self.mainGrpAttrNameOutsPrefix + outObj 
			self.outsConnections = mc.listConnections( attrName , s = False , d = True  )[0]

		#GET THE NEW CTRL VALUE
		#for 
		#GET THE NEW CTRL SHAPEs
		#self.ctrls            = [] 
		#shapeInfo
		#values

	#________________________________________________________________________________________PRIVATE		
	def buildRigFromSel( self ):
		selection = mc.ls( sl = True )
		nbrElem        = len( selection )
		nbrElemPerRig  = len( self.buildTrs )	
	
		for i in range( 0 , nbrElem , nbrElemPerRig ):
			#CHECK SIZE						
			try:
				for j in range( 0 , nbrElemPerRig ): error = selection[i+j]
			except:
				break
			#GATHER INFO
			buildTrs = []
			for j in range( 0 , nbrElemPerRig ):				
				buildTrs.append( utilsMaya.getWorldTrsValue( selection[i+j] ) )					
			baseName = selection[i]
			#BUILD
			self.baseName = baseName
			self.buildTrs = buildTrs
			self.buildRig()

	def buildAttrMainGrpConnections( self ):		

		if( self.isSubRig == 1 ):
			return None
						
		for inElem in self.ins:
			attrName = self.mainGrpAttrNameInsPrefix + inElem			
			mc.addAttr( self.mainGrp , ln = attrName , dt = 'string' )
		
		for outElem in self.outs:
			attrName = self.mainGrpAttrNameOutsPrefix + outElem			
			mc.addAttr( self.mainGrp , ln = attrName , dt = 'string' )
			
		return 1

	def mirrorMainGrpConnections( self , prefix , replace ):
			
		if( self.isSubRig == 1 ):
			return None
			
		#NEW CONNECTION NAME
		newInConnections = []
		for connection in self.mainGrpAttrIns:
			newInConnections.append(  self.getMirrorMainGrpConnection( connection , self.mainGrpAttrNameOutsPrefix , prefix , replace )     )
				
		newOutConnections = []
		for connection in self.mainGrpAttrOuts:		
			newOutConnections.append(  self.getMirrorMainGrpConnection( connection , self.mainGrpAttrNameInsPrefix , prefix , replace )	     )	

		#RECONNECT INS		
		for i in range( 0 , len(self.ins) ):
			
			if( len(newInConnections) == 0 ) or ( len(self.mainGrpAttrIns) == 0 ):
				continue
			
			if( newInConnections[i] == None ) or ( self.mainGrpAttrIns[i] == None ):
				continue
			
			attrName = self.mainGrp + '.' + self.mainGrpAttrNameInsPrefix + self.ins[i]

			if( mc.objExists( newInConnections[i] ) ):
				mc.connectAttr( newInConnections[i] , attrName , f = True )
			else:
				mc.connectAttr( self.mainGrpAttrIns[i] , attrName , f = True )

		#RECONNECT OUTS								
		for i in range( 0 , len(self.outs) ):
			attrName = self.mainGrp + '.' + self.mainGrpAttrNameOutsPrefix + self.outs[i]
			
			try:			
				mc.connectAttr( attrName , newOutConnections[i] , f = True )
			except:
				pass		
				
		return 1
	
	def getMirrorBothSidesBaseNames( self, baseName , prefix , replace ):

		oldBaseName = self.baseName

		#OLD SIDE BASE NAME
		oldSideBaseName =  oldBaseName
		if( replace[0] in oldSideBaseName ) and not( replace[0] == '' ):		
			splitTmp      = oldSideBaseName.split( replace[0] )
			oldSideBaseName = splitTmp[0] + replace[1] + splitTmp[1]	

		if not( oldSideBaseName[0:len( prefix[0] )] == prefix[0] ):			
			oldSideBaseName = prefix[0] + oldSideBaseName

		#NEW SIDE BASE NAME
		newSideBaseName =  oldBaseName
		if( replace[0] in newSideBaseName ) and not( replace[0] == '' ):		
			splitTmp      = newSideBaseName.split( replace[0] )
			newSideBaseName = splitTmp[0] + replace[1] + splitTmp[1]	
			
		if not( newSideBaseName[0:len( prefix[1] )] == prefix[1] ):			
			newSideBaseName = prefix[1] + newSideBaseName

		return [ oldSideBaseName , newSideBaseName ]		

	def getMirrorBuildTrs( self , planSymCoords , lockAxe , inverseAxes ):
		trsObj = trsClass.trsClass()	

		mirrorBuildTrs = []
		for trsValue in self.buildTrs:
			trsObj.value = trsValue 
			trsObj.mirror( planSymCoords , lockAxe )
			trsObj.inverseAxes( inverseAxes )			
			newBuildTrs.append( trsObj.value )	

		return mirrorBuildTrs	

	def getMirrorMainGrpConnection( self , objAttr , inOutPrefix , prefix , replace ):

		if( objAttr == None ):
			return None
		
		splitTmp = objAttr.split('.')

		objName        = splitTmp[0]
		bothSidesNames = self.getMirrorBothSidesBaseNames( objName , prefix , replace )
		newObjName     = bothSidesNames[1]
						
		attrNameTmp    = splitTmp[1]
		attrName       = attrNameTmp[len(inOutPrefix):len(attrNameRaw)]			
		bothSidesNames = self.getMirrorBothSidesBaseNames( attrName , prefix , replace )
		newAttrNameTmp = bothSidesNames[1]
		newAttrName    = inOutPrefix + newAttrNameTmp
					
		newConnection  = newObjName + '.' + newAttrName			

		return newConnection
		
	
	@staticmethod
	def utils_buildMainGrp( name ):
		mc.createNode( "transform" , n = name )  

	@staticmethod
	def utils_buildAttrInsOuts( name , ins , outs , insConnections , outsConnections , insPrefix = '' , outsPrefix = ''  ):	
		for inElem in ins:
			attrName = insPrefix + inElem			
			mc.addAttr( name , ln = attrName , dt = 'string' )
			for inConnection in insConnections:
				mc.connectAttr( inConnection , ( name + '.' + attrName ) )
		
		for outElem in outs:
			attrName = outsPrefix + outElem			
			mc.addAttr( name , ln = attrName , dt = 'string' )
			for outConnection in outsConnections:
				mc.connectAttr( outConnection , ( name + '.' + attrName ) )		

		return 1



	def writeAttrBeacon( self  , mainGrp ):
		rwi = readWriteInfo.readWriteInfo()		
		rwi.write( self.beacons , self.beaconAttrNameMainGrp  , mainGrp )	
		return 1
				
	def readAttrBeacon( self , beacon ):
		rwi = readWriteInfo.readWriteInfo()				
		mainGrp = rwi.read( beacon , self.beaconAttrNameMainGrp )	
		if( mainGrp == None ):
			return 0
		else:
			self.mainGrp = mainGrp		
		return 1

	
	def modifTopRigNames( self , newBaseName  , doIncr = 0 , renameSubRig = 1 ):		
		newAlls = []
		for elem in self.alls:				
			newElem = elem.replace( self.baseName , newBaseName )
			mc.rename( elem , newElem )
			newAlls.append( newElem )
			
	
	def modifSubRigsNames( self , newBaseName  , doIncr = 0 , renameSubRig = 1 ):

		for i in range( 0 ,  len( self.subMainGrps ) ):				
			rigObj = self.getRigClassInstanceFilledFromMainGrp( self.subMainGrps[i] )
			subSuffix = rigObj.baseName.split( self.baseName )[1]
			rigObj.modifRigNames( newBaseName + subSuffix  , doIncr , renameSubRig )

							
	def modifAttrsNames( self , newBaseName  , doIncr = 0 , renameSubRig = 1 ):	

		# ATTR CONTENANT
		newMainGrp = newBaseName +  self.mainGrpSuffix

		newIns = []
		for elem in self.ins:
			newIn = elem.replace( self.baseName , newBaseName )
			newIns.append( newIn )		
				
		newCtrls = []
		for elem in self.ctrls:
			newCtrl = elem.replace( self.baseName , newBaseName )
			newCtrls.append( newCtrl )	
			
		newOuts = []
		for elem in self.outs:
			newOut = elem.replace( self.baseName , newBaseName )
			newOuts.append( newOut )				

		newBeacons = []
		for elem in self.beacons:
			newBeacon = elem.replace( self.baseName , newBaseName )
			newBeacons.append( newBeacon )				
	
		newSubMainGrps = []
		for elem in self.subMainGrps:			
			newSubMainGrp = elem.replace( self.baseName , newBaseName )
			newSubMainGrps.append( newSubMainGrp )					

		self.setWriteAttrMainGrp(  self.mainGrp , self.type , self.buildTrs , newIns , newCtrls , newOuts , newBeacons , newAlls , newSubMainGrps , setAttr = 0)
		self.writeAttrBeacon( newMainGrp )	

		# ATTR NAME
		if( self.isSubRig == 0 ) and not ( 'Dupli_' in self.mainGrp ):

			for i in range( 0 , len( self.ins ) ):
				oldAttr =  self.mainGrpAttrNameInsPrefix + self.ins[i]
				newAttr =  self.mainGrpAttrNameInsPrefix + newIns[i]
				if not ( oldAttr == newAttr ):
					mc.renameAttr( self.mainGrp + '.' + oldAttr , newAttr )
				
			for i in range( 0 , len( self.outs ) ):
				oldAttr =  self.mainGrpAttrNameOutsPrefix + self.outs[i]
				newAttr =  self.mainGrpAttrNameOutsPrefix + newOuts[i]
				if not ( oldAttr == newAttr ):				
					mc.renameAttr( self.mainGrp + '.' + oldAttr , newAttr )
			

	def buildSets( self ):
		if( self.isSubRig == 1 ):
			return None
		
		self.createFromMainGrp( self.mainGrp )
		selection = mc.ls(sl=True)
		mc.select( cl = True )	
		# animSet
		if not ( mc.objExists(self.mainAnimSet) ):
			mc.sets( n = self.mainAnimSet )
			
		mc.sets( n = self.animSet )
		mc.sets( self.animSet , e = True , add = self.mainAnimSet )	
		mc.sets( self.ctrls , e = True , add = self.animSet )
		mc.select( selection )
		
		return self.animSet


 	def mirrorSubRigs( self , planSymCoords , lockAxe , inverseAxes ,  prefix , replace  ):
 
		self.subRigObjs = []  			
		rigObj          = None		
		subMainGrps     = self.subMainGrps
	
		for rigGrp in self.subMainGrps:			
			rigObj = self.getRigClassInstanceFilledFromMainGrp( rigGrp )		
			rigObj.isSubRig = 1		
			rigObj.buildRigMirror( planSymCoords , lockAxe , inverseAxes ,  prefix , replace )	
			self.subRigObjs.append( rigObj )



	#++++TO MODIFY IN CHILDREN CLASS 
	def setAttrsBase( self , baseName , buildTrs , isSubRig = None , buildTrsDupli = None ):
	
		self.setAttrsNameFromBaseName( baseName )
		self.buildTrs      = buildTrs		
		self.isSubRig      = isSubRig      if not( isSubRig      == None ) else self.isSubRig			
		self.buildTrsDupli = buildTrsDupli if not( buildTrsDupli == None ) else self.buildTrsDupli
		
	#++++TO MODIFY IN CHILDREN CLASS 
	def setAttrsNameFromBaseName( self , baseName ):
	
		
		# main Hierarchy
		self.baseName      = baseName		
		self.mainGrp       = self.baseName + self.mainGrpSuffix
		self.manipGrp      = self.baseName + '_manips_grp' 
		self.rigGrp        = self.baseName + '_rig_grp' 
			
		#baseName subRig
		self.subRigBaseNames = []
		for suffix in self.subRigSuffix:
			self.subRigBaseNames.append( self.baseName + suffix )	
		
		self.animSet     =  self.baseName + 'AnimSet'		

	
	def setWriteAttrMainGrp( self ,  mainGrp = '' , rigType = '' , buildTrs = [] , ins = [] , ctrls = [] , outs = [] , beacons = [] ,  alls = [] , subMainGrps = [] , setAttr = 1 , writeAttr = 1 ):

		#SAVE
		if( setAttr == 1 ):	
			self.ins         = ins		
			self.ctrls       = ctrls		
			self.outs        = outs
			self.beacons     = beacons
			self.alls        = alls
			self.subMainGrps = subMainGrps		
			self.type     = rigType
			self.buildTrs    = buildTrs
			self.mainGrp     = mainGrp				
				
		#WRITE	
		if( writeAttr == 1 ):
			rwi = readWriteInfo.readWriteInfo()
			rwi.obj = mainGrp
			rwi.write( self.mainGrpAttrNameRigType  , rigType      )			
			rwi.write( self.mainGrpAttrNameIns      , ins          )			
			rwi.write( self.mainGrpAttrNameCtrls    , ctrls        )		
			rwi.write( self.mainGrpAttrNameOuts     , outs         )
			rwi.write( self.mainGrpAttrNameBeacons  , beacons      )		
			rwi.write( self.mainGrpAttrNameAlls     , alls         )		
			rwi.write( self.subMainGrpsAttr         , subMainGrps  )
			rwi.write( self.mainGrpAttrNameBuildTrs , buildTrs     )
			
		return 1
	





	def setAttrMainGrpConnections( self ):
		
		attrTest = self.mainGrp + '.' + self.mainGrpAttrNameInsPrefix + self.ins[0]	
		if not(  mc.objExists(attrTest) ):
			return None
					
		self.mainGrpAttrIns = []	
		for inElem in self.ins:
			attrName = self.mainGrp + '.' + self.mainGrpAttrNameInsPrefix + inElem		
			elem = mc.listConnections( attrName , s = True , plugs = True )
			if not( elem == None ):
				self.mainGrpAttrIns.append( elem[0] )
			else:
				self.mainGrpAttrIns.append( None )
				
		self.mainGrpAttrOuts = []	
		for outElem in self.outs:
			attrName = self.mainGrp + '.' + self.mainGrpAttrNameOutsPrefix + outElem		
			elem = mc.listConnections( attrName , d = True , plugs = True )
			if not( elem == None ):
				self.mainGrpAttrOuts.append( elem[0] )
			else:
				self.mainGrpAttrOuts.append( None )				
			
		return 1		

	def deleteRig( self ):
		# deleteRig DUPLI MANIP
		for elem in self.alls:
			if( '_orig' in elem ):
				dupliMainGrp = elem.split('_orig')[0] + 'Dupli_orig'

				if( mc.objExists( dupliMainGrp ) ):						
					mc.deleteRig( dupliMainGrp )
			
		# deleteRig SUB RIG
		self.subMainGrps.reverse() # for deleteRig the child rig first

		for i in range( 0 ,  len( self.subMainGrps ) ):
			if( mc.objExists(self.subMainGrps[i]) ):
				rigObj = getRigClassInstanceFilledFromMainGrp(self.subMainGrps[i]);
				rigObj.deleteRig()		
							
		# deleteRig ALL		
		for elem in self.alls:
			try:
				mc.deleteRig(elem)
			except:
				pass

		return 1	


	def modifRigNames( self , newBaseName ):
		#INCREMENTATION
		if( doIncr == 1):
			newBaseName = utilsMaya.incrBaseNameIfExist( newBaseName  ,  [ '' , 'r_' , 'l_']  ,  [ '_ctrl' , '_skn' , self.mainGrpSuffix] )

		self.modifSubRigsNames( newBaseName )
		self.modifAttrsNames( newBaseName )
		self.modifTopRigNames( newBaseName )				
		
		self.mainGrp = self.mainGrp.replace( self.baseName , newBaseName ) 
		self.readClasseAttrOnMainGrp()			



	def mirrorRig( self , planSymCoords , lockAxe , inverseAxes ,  prefix , replace ):

		#MIRROR BASE ATTR
		baseNames = self.getMirrorBothSidesBaseNames( self.baseName , prefix , replace )
		mirrorBuildTrs = self.getMirrorBuildTrs( planSymCoords , lockAxe , inverseAxes )
		#BUILD MIRROR
		mirrorInstance = copy.copy(self)
		mirrorInstance.mirrorSubRigs( planSymCoords ,lockAxe , inverseAxes ,  prefix , replace )			
		mirrorInstance.setAttrsBase( baseNames[1] , mirrorBuildTrs )	 		
		mirrorInstance.buildTopRig()
		mirrorInstance.buildAttrMainGrpConnections()
		mirrorInstance.buildSets()
		#CONNECTION ON MAIN		
		mirrorInstance.mirrorMainGrpConnections( prefix , replace )
		#MODIF CURRENT
		self.modifRigNames( baseNames[0] , doIncr = 0	, renameSubRig = 0)

		return mirrorInstance			
'''		