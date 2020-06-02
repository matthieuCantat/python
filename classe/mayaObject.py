'''

#******************************************************** BUILD EXEMPLE MAYA OBJECT
import maya.cmds as mc
import python
from python.classe.mayaObject import *
reload(python.classe.mayaObject)
reload(python.classe.buildPosition)


import maya.cmds as mc
mc.file( f = True , new = True )


saveObj = 'saveObj'
tmpPath = 'C:\Users\mcantat\AppData\Local\Temp\mayaClasseSave'
#=================================================
base = mayaObject()
base.name    = 'matthieu'
base.surname = 'cantat'
base.birth   = [ 21 , 03 , 1990 ]
base.printAttrs()

saveObj = 'saveObj'
mc.createNode( 'transform' , n = saveObj )
base.toMayaObj(saveObj)
#=================================================
toto = mayaObject()
toto.createFromMayaObj(saveObj)
toto.printAttrs()
toto.toFile(tmpPath)
#=================================================
test = mayaObject()
test.createFromFile(tmpPath)
test.printAttrs()
#=================================================
print('ALL THE DIFFERENT CLASSES:')
for elem in test.utilsClasseNames:    
    print( elem )


#******************************************************** BUILD EXEMPLE MAYA OBJECT
print("__________________ SET NAME")
base.Name.add( 'topNode' , baseNameAppend = 'Top' , type = 'grp' , ref = base.Name.base )  
base.Name.add( 'ctrlA'   , baseNameAppend = 'CtrlA' , type = 'Ctrl' , ref = base.Name.base )  
base.Name.add( 'ctrlB'   , baseNameAppend = 'CtrlB' , type = 'Ctrl' , ref =  base.Name.base )  
print("__________________ SET DAG")
base.Dag.add( base.Name.topNode , 'transform' )
base.Dag.add( base.Name.ctrlA   , 'transform' , parent = base.Name.topNode )
base.Dag.add( base.Name.ctrlB   , 'transform' , parent = base.Name.topNode )
print("__________________ SET POSITION")
base.Pos.add( 'ctrlA' , [ 5 , 2 , 3  , 15 , 15 , 15 , 1 , 1 , 1 ] , Name = base.Name.ctrlA  )
base.Pos.add( 'ctrlB' , [ 3 , 3 , -3 , 0 , 45 , 45 , 1 , 1 , 1 ]  , Name = base.Name.ctrlB  )
print("__________________ SET CURVE SHAPE")
base.CurveShape.add( 'ctrlA' , { 'form' : 'cube'   , 'colors' : [13] , 'axe' : 'x' , 'offset' : [0,0,0,0,0,0,1,1,1] } , Name = base.Name.ctrlA  )
base.CurveShape.add( 'ctrlB' , { 'form' : 'cube'   , 'colors' : [17] , 'axe' : 'y' , 'offset' : [0,0,0,0,0,0,1,1,1] } , Name = base.Name.ctrlB  )
print("__________________ BUILD")
base.build()

print("__________________ MODIF NAME & REBUILD")
base.delete()
base.Name.add( 'base' , replace = [ 'base' , "toto" ])
base.build()
print("__________________  REBUILD")
#base.rebuild()
print("__________________  MIRROR")
base.delete()
mirrored = base.mirror( [ 0,0,0 , 0,1,0 ,0,0,1 ] , 0 , 0 , ['l' , 'r' ] , ['' , '' ]  )


mirrored[0].build()
mirrored[1].build()

#===================RELOAD===================================
import python
import python.classe
import python.classe.rigPuppet
import python.classe.rigPuppetCarrierShip
import python.classe.rigPuppetHowie
import python.classe.rigModuleProjector
import python.classe.rigModulePiston
import python.classe.rigModuleRotatingBeacon
import python.classe.rigModuleChain
import python.classe.rigModuleArm

reload(python.classe.build)
reload(python.classe.buildAttribute)
reload(python.classe.buildCurveShape)
reload(python.classe.buildDag)
reload(python.classe.buildLink)
reload(python.classe.buildName)
reload(python.classe.buildParent)
reload(python.classe.buildPosition)

reload(python.classe.mayaClasse)
reload(python.classe.mayaObject)

reload(python.classe.rig)
reload(python.classe.rigCtrl)
reload(python.classe.rigLightCone)
reload(python.classe.rigSkeletonChain)
reload(python.classe.rigStretchyJoint)

reload(python.classe.rigModule)
reload(python.classe.rigModuleArm)
reload(python.classe.rigModuleProjector)
reload(python.classe.rigModulePiston)
reload(python.classe.rigModuleRotatingBeacon)
reload(python.classe.rigModuleChain)

reload(python.classe.rigPuppet)
reload(python.classe.rigPuppetCarrierShip)
reload(python.classe.rigPuppetCarrierShip_damp)
reload(python.classe.rigPuppetCarrierShip_hook)
reload(python.classe.rigPuppetCarrierShip_propulsor)
reload(python.classe.rigPuppetCarrierShip_reactor)
reload(python.classe.rigPuppetHowie)



reload(python.utils.utilsMaya)


'''


import maya.cmds as mc
from .mayaClasse import *
import copy
import types
from .trsBackUp import *
from .coords import *
import time

from .buildAttribute   import *	
from .buildDag         import *
from .buildLink        import *
from .buildName        import *
from .buildParent      import *	
from .buildPosition    import *	
from .buildCurveShape  import *	


class mayaObject( mayaClasse ):

	'''
		instance with a representation physique in maya    instance <-------> maya elem
		autoFill self.alls in self.build()
		autoMirror with self.utilsAttrToMirror	

		FONCTION:
			-build  
			-rebuild
			-delete
			-mirror 	
			-modifBaseName
			-mirrorBuild			
			-modifBaseNameBuild			
	'''
	def __init__(self , **args ):
		mayaClasse.__init__( self , **args )
		self.debug        = args.get( 'debug'   , 0 )
		self.TimeBuild    = args.get( 'TimeBuild'   , {} )
		self.fillAllVar = 0
		#UTILS
		self.utilsAttrToMirror = []	
		#CLASSE
		self.classeType = 'mayaObject'
		self.depthLevel = 0	
		#InstanceType
		self.utilsAttrToMirror  = [ 'Name' , 'Position' , 'CurveShape' ]
		self.Attr        = buildAttribute()	
		self.Dag         = buildDag()      
		self.Link        = buildLink()   
		self.Name        = buildName() 
		self.Parent      = buildParent()   	
		self.Pos         = buildPosition()
		self.CurveShape  = buildCurveShape()
		self.SubRigs     = []
		self.SubRigsName = []
		self.alls        = []
		self.Name.add( 'base' , baseName = 'base' )
		self.keyToDuplicated = {}	
		#INSTANCE_______________________________INFO
		self.ins         = []
		self.outs        = []
		self.outsToCtrls = []	


	def build( self ):
		buildCmds = ''
		buildCmds = ''
		buildCmds += '\n\n'
		buildCmds += '########################################################\n'
		buildCmds += '##################### START BUILD ######################\n'
		buildCmds += '########################################################\n'
		buildCmds += '\n\n'
		buildCmds += 'import python.utils.utilsMaya as utilsMaya\n\n'

		self.TimeBuild['Start'] = time.clock()
		TimeTmp = time.clock()
		#BUILD
		if(self.debug ):
			print('\n\n==== START BUILD ==== {} - {}'.format(  self.classeType , self.Name.base.value() ) )

		self.postInit()

		if( self.fillAllVar == 1 ):
			listMayaNodesBefore = mc.ls()

		if(self.debug ):
			self.TimeBuild['PostInit'] = time.clock() - TimeTmp
			TimeTmp = time.clock()
			print('PreBuild')			

		self.preBuild()

		if(self.debug ):
			self.TimeBuild['PreBuild'] = time.clock() - TimeTmp 
			TimeTmp = time.clock()
			print('subRigs')


		if(self.debug ):
			TimeTmp = time.clock()
			print('Dag')

		buildCmds += self.buildSubRigsBuilds('Name')

		if(self.debug ):
			self.TimeBuild['Dag'] = time.clock() - TimeTmp
			TimeTmp = time.clock()
			print('Attr')	

		buildCmds += self.buildSubRigsBuilds('Attr')

		if(self.debug ):		
			self.TimeBuild['Attr'] = time.clock() - TimeTmp
			TimeTmp = time.clock()
			print('Pos')

		buildCmds += self.buildSubRigsBuilds('Pos')

		if(self.debug ):
			self.TimeBuild['Pos'] = time.clock() - TimeTmp
			TimeTmp = time.clock()
			print('Parent')

		buildCmds += self.buildSubRigsBuilds('Parent')

		if(self.debug ):
			self.TimeBuild['Parent'] = time.clock() - TimeTmp
			TimeTmp = time.clock()
			print('Link')

		buildCmds += self.buildSubRigsBuilds('Link')

		if(self.debug ):	
			self.TimeBuild['Link'] = time.clock() - TimeTmp
			TimeTmp = time.clock()
			print('CurveShape')

		buildCmds += self.buildSubRigsBuilds('CurveShape')

		if(self.debug ):
			self.TimeBuild['CurveShape'] = time.clock() - TimeTmp
			TimeTmp = time.clock()
			print('postBuild')

		buildCmds += self.postBuild()

		if(self.debug ):
			self.TimeBuild['PostBuild'] = time.clock() - TimeTmp
			TimeTmp = time.clock()
			print('buildMayaObject')

		self.buildMayaObject()
		self.customFinalize()
		
		if( self.fillAllVar == 1 ):
			listMayaNodesAfter = mc.ls()
			self.alls = [obj for obj in listMayaNodesAfter if obj not in listMayaNodesBefore]	

		if(self.debug ):
			print('==== END BUILD ==== {} - {}'.format(  self.classeType , self.Name.base.value() ) )
			totalTime = time.clock() - self.TimeBuild['Start']
			print('\n==== TIME ==== {} min {} sec '.format( int(totalTime/60) , totalTime%60 ) )
			print('PostInit        - {} %'.format(self.TimeBuild['PostInit']        / totalTime) )
			print('PreBuild        - {} %'.format(self.TimeBuild['PreBuild']        / totalTime) )
			print('Dag             - {} %'.format(self.TimeBuild['Dag']             / totalTime) )
			print('Attr            - {} %'.format(self.TimeBuild['Attr']            / totalTime) )
			print('Pos             - {} %'.format(self.TimeBuild['Pos']             / totalTime) )
			print('Parent          - {} %'.format(self.TimeBuild['Parent']          / totalTime) )
			print('Link            - {} %'.format(self.TimeBuild['Link']            / totalTime) )
			print('CurveShape      - {} %'.format(self.TimeBuild['CurveShape']      / totalTime) )
			print('PostBuild       - {} %'.format(self.TimeBuild['PostBuild']       / totalTime) )
			print('==========================\n\n')
	
		return buildCmds

	

	def buildSubRigsBuilds( self , BuildType ):
		Builds          = self.Builds_getFromSubRigs(BuildType)	
		priorityIndexes = self.Builds_getPriorityIndexes(Builds)
		self.Builds_importAndFlattenData( Builds , importOrder = priorityIndexes )
		Builds[0].dataFlatReorderCustom() 
		cmds = Builds[0].build()	
		return cmds

	def Builds_getFromSubRigs( self , BuildType ):
		Builds = []
		#FIRST GET WHAT'S INSIDE SUBRIGs
		for Rig in self.SubRigs:

			if( BuildType == 'Name' ):
				if( 'rigModule' in self.classeType ) or ( 'rigPuppet' in self.classeType ): 
					if( 'rigModule' in Rig.classeType ) or ( 'rigPuppet' in Rig.classeType ):
						Rig.Name.add( 'topNode'     , parent  = self.Name.topNode       )

			if( BuildType == 'Link' ):
				if( 'rigModule' in self.classeType ) or ( 'rigPuppet' in self.classeType ): 
					if( 'rigModule' in Rig.classeType ) or ( 'rigPuppet' in Rig.classeType ):
						Rig.Link.add(   'skeletonVis'  , Sources = [self.Attr.topNode.skeletonVis ] , Destinations = [ Rig.Attr.topNode.skeletonVis ] )
						Rig.Link.add(   'skeletonRef'  , Sources = [self.Attr.topNode.skeletonRef ] , Destinations = [ Rig.Attr.topNode.skeletonRef ] )		
						Rig.Link.add(    'ctrlVis'     , Sources = [ self.Attr.topNode.ctrlVis , Rig.ctrlVisPriority*-1 ] , Destinations = [ Rig.Attr.topNode.ctrlVis    ]   , type = 'add'  )
					#CTRL VISIBILITY SETUP	
					elif(   'rigCtrl'   in Rig.classeType ):
						Rig.Link.add( 'ctrlVis' , Sources = [ self.Attr.topNode.ctrlVis , Rig.ctrlVisPriority*-1 ] , Destinations = [ Rig.Attr.topNode.visibility ]   , type = 'add+' )		

			Builds += Rig.Builds_getFromSubRigs( BuildType )

		#THEN INSIDE THE CURRENT
		exec( 'Builds.append( self.{} )'.format(BuildType) )

		return Builds
	
	def Builds_getPriorityIndexes( self , Builds ):
		PriorityIndexes = []

		#FLATTEN Data
		BuildRefsSlaves  = []
		BuildRefsMasters = []
		for i in range( 0 , len(Builds) ):
			instanceSlaves  = []
			instanceMasters = []
			for j in range( 0 , len(Builds[i].data)):

				if( Builds[i].utils_dataIsBuildable( j ) ):

					key = Builds[i].data[j]['key']
					exec( 'instanceSlaves.append( [ Builds[i].{} ] )'.format(key) )
					
					valueHistory = Builds[i].data[j]['value']
					InstanceMasters = []
					for v in valueHistory:
						vKey = v.keys()[0]
						
						if(   type(v[vKey]) == types.ListType ):
							for elem in v[vKey]:
								if( type(elem) == types.InstanceType ) and ( elem.classeType == self.classeType ):
									InstanceMasters.append(elem)
	
						elif( type(v[vKey]) == types.InstanceType ) and ( v[vKey].classeType == self.classeType ):
							InstanceMasters.append(v[vKey])
	
					instanceMasters.append(  InstanceMasters )

				else:
					instanceSlaves.append([None])
					instanceMasters.append([None])

			BuildRefsSlaves.append(  instanceSlaves  )
			BuildRefsMasters.append( instanceMasters )
		

		#FLATTEN Data
		infOrder = self.sortIndexChildrensByReference( BuildRefsMasters , BuildRefsSlaves )
		
		return infOrder

	def sortIndexChildrensByReference( self , Masters , Slaves ):
		infOrder = []

		links = [ [ [-1,-1] for mj in range( len(Masters[mi]) ) ] for mi in range( len(Masters)) ]
		#GET LINKS
		for mi in range( len(Masters)):
			for mj in range( len(Masters[mi])):
				for m in Masters[mi][mj]:

					if( m == None ): 
						links[mi][mj] = [None,None]
						break

					for si in range( len(Slaves)):
						for sj in range( len(Slaves[si])):
							for s in Slaves[si][sj]:
					
								if( m == s ): links[mi][mj] = [si,sj]


		#ADD INDEPENDANT LINKS
		for mi in range( len(Masters)):
			for mj in range( len(Masters[mi])):
				if( links[mi][mj] == [-1,-1] ):
					infOrder.append( [mi,mj] )

		#ADD SORTED DEPENDANT LINKS
		stop = False
		loop = 0
		infOrderNext = infOrder
		while( stop == False ):

			infOrderStart = infOrderNext[:]

			infOrderNext = []
			for i in range( len(infOrderStart) ):
				for mi in range( len(Masters)):
					for mj in range( len(Masters[mi])):				
						if( infOrderStart[i] == links[mi][mj] ):
							infOrderNext.append( [ mi , mj ] )

			if( len(infOrderNext) == 0 ):
				stop = True

			infOrder += infOrderNext

			loop+=1
			if( 500 < loop ):
				mc.error('sortIndexChildrensByReference LOOP 500')


		return infOrder

	def Builds_importAndFlattenData( self , Builds , importOrder = None ):

		if not( importOrder == None ):
			for order in importOrder:
				i , j = order[0] , order[1]		
				flattenDataDict          = Builds[i].refs(  j , updateData = True )
				flattenDataDict['value'] = Builds[i].value( j , updateData = True )
				Builds[0].dataFlat.append(flattenDataDict)
		else:
			for i in range( 0 , len(Builds) ):
				for j in range(0,len(Builds[i].data) ):
					flattenDataDict          = Builds[i].refs(  j , updateData = True )
					flattenDataDict['value'] = Builds[i].value( j , updateData = True )
					Builds[0].dataFlat.append(flattenDataDict)

		return Builds[0]



	def Builds_mergeFlattenData( self , BuildType , Builds ):
		for i in range( 1 , len(Builds) ):
			Builds[0] += Builds[i]
		return Builds[0]


	def postInit(self):
		'''
		#ADD ATTRS CTRL INF
		if( 'rigModule' in self.classeType ) or ( self.classeType == 'rigCtrl'):
			for j in range( 0 , len(self.outs) ):

				outsToCtrls = []
				if( j < len(self.outsToCtrls) ):
					for i in range( 0 , len(self.outsToCtrls[j]) ):
						if not( self.outs[j].value() == self.outsToCtrls[j][i].value() ):
							outsToCtrls.append( self.outsToCtrls[j][i] )
				
				if not( len(outsToCtrls) == 0 ):
					self.Attr.add( 'out{}'.format(j) , Name = self.outs[j] , attrName = ['ctrlInf'] , attrType = ['string'] , attrValue = [ outsToCtrls ] )
		'''			

	def preBuild(self):
		pass


	def postBuild(self):
		return ''

	def buildMayaObject( self ):         
		return ''

	def customFinalize( self ):
		return ''

	def rebuild( self ):
		self.delete()
		self.build()


	def delete( self ):
		elemNotFound = []
		for elem in self.alls:
			try:
				mc.delete( elem )
			except:
				elemNotFound.append( elem )

		if( 0 < len(elemNotFound) ):
			print( 'elemNotFound' , elemNotFound )


	def utils_printHistory( self , data , shift = '' ):
		d = data
		history = d['trs']
		operation = d['operation'] 
		shift = '\t' + shift

		for i in range( 0 , len(history) ):
			if( type(history[i]) == types.InstanceType ):
				print( '{}--->REF ({})'.format( shift , operation[i] ) )
				history[i].utils_printHistory( history[i].data[history[i].index] , shift = shift )
				print( '{}***{}***'.format( shift , history[i].value() ) )
			else:
				print( '{}{} ({})'.format( shift , history[i] , operation[i] ) )



	def duplicateRigs( self , dupliInfo , rigs ):
		'''
		there is some probleme with the normal duplication and the ref inside the classe

		the result depend of the order of duplication

		if you make a swap ref to a rig that point to an other rig not yet processed, the swap will not work
		After when that pointed rig is processed the other rig is not swap anymore

		that proc will make a big swap for everyone at the end of the transformation
		'''
		value             = dupliInfo.get( 'value'             , [0,0,0 , 0,1,0 , 0,0,1] )		
		mode              = dupliInfo.get( 'mode'              , 'mirror'                )	
		pivot             = dupliInfo.get( 'pivot'             , [0,0,0 , 0,0,0 , 1,1,1] )
		namePrefix        = dupliInfo.get( 'namePrefix'        , ['r','l']               )		
		nameReplace       = dupliInfo.get( 'nameReplace'       , ['','']                 )	
		nameIncr          = dupliInfo.get( 'nameIncr'          , ''                      )
		nameAdd           = dupliInfo.get( 'nameAdd'           , []                      )
		noneMirrorAxe     = dupliInfo.get( 'noneMirrorAxe'     , 4                       )
		duplicateKey      = str(value) + mode

		duplicateds    = []
		duplicatedsNbr = []

		for rig in rigs:
			duplicateds.append( rig.duplicate( **dupliInfo ) )

		for i in range( len(duplicateds) ):
			for j in range( len(duplicateds[i]) ):
				duplicateds[i][j].swapRefsToDuplicate( duplicateKey , j , self.debug )

		return duplicateds



	def duplicate( self , **args ):
		self.debug = args.get( 'debug', 0 )

		value             = args.get( 'value'             , [0,0,0 , 0,1,0 , 0,0,1] )		
		mode              = args.get( 'mode'              , 'mirror'                )	
		pivot             = args.get( 'pivot'             , [0,0,0 , 0,0,0 , 1,1,1] )
		namePrefix        = args.get( 'namePrefix'        , ['r','l']               )		
		nameReplace       = args.get( 'nameReplace'       , ['','']                 )	
		nameIncr          = args.get( 'nameIncr'          , ''                      )
		nameAdd           = args.get( 'nameAdd'           , []                      )
		noneMirrorAxe     = args.get( 'noneMirrorAxe'     , 4                       )

		if(self.debug ):
			self.TimeBuild['Name'] = 0
			self.TimeBuild['Attr'] = 0
			self.TimeBuild['Pos'] = 0
			self.TimeBuild['Parent'] = 0
			self.TimeBuild['Link'] = 0
			self.TimeBuild['CurveShape'] = 0
			self.TimeBuild['otherAttr'] = 0
			self.TimeBuild['createInstance'] = 0
			#PRE BUILD
			print('\n\n==== START DUPLICATE ==== {} - {}'.format(  self.classeType , self.Name.base.value() ) )
			TimeTmp = time.clock()
			self.TimeBuild['Start'] = TimeTmp
			print('duplicateBasic')
		

		self.depthLevel = 0


		duplicateKey = str(value) + mode
		duplicateds  = self.duplicateBasic( **args )


		if(self.debug ):		
			self.TimeBuild['duplicateBasic'] = time.clock() - TimeTmp
			TimeTmp = time.clock()
			print('swapRefsToDuplicate')


		for i in range(0,len(duplicateds)):
			duplicateds[i].swapRefsToDuplicate( duplicateKey , i )


		if(self.debug ):		
			self.TimeBuild['swapRefsToDuplicate'] = time.clock() - TimeTmp
			TimeTmp = time.clock()
			print('addDupliAttrs')


		for i in range(1,len(duplicateds)):
			duplicateds[i].addDupliAttrs( duplicateds[0] , i , **args )


		if(self.debug ):		
			self.TimeBuild['addDupliAttrs'] = time.clock() - TimeTmp
			TimeTmp = time.clock()
			print('updateSubRigAttr')


		for i in range(0,len(duplicateds)):
			duplicateds[i].updateSubRigAttr()		


		if(self.debug ):		
			self.TimeBuild['updateSubRigAttr'] = time.clock() - TimeTmp
			TimeTmp = time.clock()


		if( self.debug ):
			print('==== END DUPLICATE ==== {} - {}'.format(  self.classeType , self.Name.base.value() ) )
			totalTime = time.clock() - self.TimeBuild['Start']
			print('\n==== TIME ==== {} min {} sec '.format( int(totalTime/60) , totalTime%60 ) )			
			print('duplicateBasic      - {} %'.format(self.TimeBuild['duplicateBasic']      / totalTime) )
			print('\tName              - {} %'.format(self.TimeBuild['Name']                / totalTime) )
			print('\tAttr              - {} %'.format(self.TimeBuild['Attr']                / totalTime) )
			print('\tPos               - {} %'.format(self.TimeBuild['Pos']                 / totalTime) )
			print('\tParent            - {} %'.format(self.TimeBuild['Parent']              / totalTime) )
			print('\tLink              - {} %'.format(self.TimeBuild['Link']                / totalTime) )
			print('\tCurveShape        - {} %'.format(self.TimeBuild['CurveShape']          / totalTime) )
			print('\totherAttr         - {} %'.format(self.TimeBuild['otherAttr']           / totalTime) )
			print('\tcreateInstance    - {} %'.format(self.TimeBuild['createInstance']      / totalTime) )
			print('swapRefsToDuplicate - {} %'.format(self.TimeBuild['swapRefsToDuplicate'] / totalTime) )
			print('addDupliAttrs       - {} %'.format(self.TimeBuild['addDupliAttrs']       / totalTime) )
			print('updateSubRigAttr    - {} %'.format(self.TimeBuild['updateSubRigAttr']    / totalTime) )
			print('==========================\n\n')
	

		return duplicateds


	def duplicateBasic( self , **args  ):
		value             = args.get( 'value'             , [0,0,0 , 0,1,0 , 0,0,1] )		
		mode              = args.get( 'mode'              , 'mirror'                )	
		pivot             = args.get( 'pivot'             , [0,0,0 , 0,0,0 , 1,1,1] )
		namePrefix        = args.get( 'namePrefix'        , ['r','l']               )		
		nameReplace       = args.get( 'nameReplace'       , ['','']                 )	
		nameIncr          = args.get( 'nameIncr'          , ''                      )
		nameAdd           = args.get( 'nameAdd'           , []                      )
		noneMirrorAxe     = args.get( 'noneMirrorAxe'     , 4                       )	
			
		duplicateKey = str(value) + mode

		if( self.debug ):
			self.depthLevel += 1
			pTab   = '\t' * self.depthLevel
			print( '{}{} - {}'.format( pTab , self.classeType , self.Name.base.str() ) )

		#DUPLICATE - SUBRIG
		duplicatedSubRigs = []
		for SubRig in self.SubRigs:
			SubRig.TimeBuild = self.TimeBuild
			SubRig.depthLevel = self.depthLevel + 1
			duplicatedSubRigs.append( SubRig.duplicateBasic(**args ) )

		if( self.debug ): TimeTmp = time.clock()	
		#DUPLICATE - BUILD CLASS
		duplicatedNames   = self.Name.duplicate(       **args )

		if( self.debug ):
			self.TimeBuild['Name'] += time.clock() - TimeTmp
			TimeTmp = time.clock()	

		duplicatedAttrs   = self.Attr.duplicate(       **args )

		if( self.debug ):
			self.TimeBuild['Attr'] += time.clock() - TimeTmp
			TimeTmp = time.clock()

		duplicatedPoses   = self.Pos.duplicate(        **args )

		if( self.debug ):
			self.TimeBuild['Pos'] += time.clock() - TimeTmp
			TimeTmp = time.clock()

		duplicatedParents = self.Parent.duplicate(     **args )

		if( self.debug ):
			self.TimeBuild['Parent'] += time.clock() - TimeTmp
			TimeTmp = time.clock()

		duplicatedLinks   = self.Link.duplicate(       **args )

		if( self.debug ):
			self.TimeBuild['Link'] += time.clock() - TimeTmp
			TimeTmp = time.clock()

		duplicatedCurves  = self.CurveShape.duplicate( **args )

		if( self.debug ):
			self.TimeBuild['CurveShape'] += time.clock() - TimeTmp
			TimeTmp = time.clock()

		#DUPLICATE - OTHER ATTR
		duplicatedIns     = [ copy.copy(self.ins ) for i in range( 0 , len(duplicatedNames) ) ]
		duplicatedOuts    = [ copy.copy(self.outs) for i in range( 0 , len(duplicatedNames) ) ]
		#duplicatedOutsToCtrls = [[copy.copy(self.outsToCtrls[j]) for j in range( 0 , len(self.outsToCtrls) )] for i in range( 0 , len(duplicatedNames) ) ]

		if( self.debug ):	
			self.TimeBuild['otherAttr'] += time.clock() - TimeTmp
			TimeTmp = time.clock()

		#CREATE ALL THE INSTANCE
		duplicatedInstances = []
		for i in range( 0 , len(duplicatedNames) ):
			instanceTmp = copy.copy(self)

			instanceTmp.SubRigs = [ duplicatedSubRigs[j][i] for j in range( len(self.SubRigs) ) ]

			instanceTmp.Name       = duplicatedNames[i]
			instanceTmp.Attr       = duplicatedAttrs[i]
			instanceTmp.Pos        = duplicatedPoses[i]
			instanceTmp.Parent     = duplicatedParents[i]
			instanceTmp.Link       = duplicatedLinks[i]			
			instanceTmp.CurveShape = duplicatedCurves[i]

			if( 0 < len(self.ins)         ): instanceTmp.ins         = duplicatedIns[i]
			if( 0 < len(self.outs)        ): instanceTmp.outs        = duplicatedOuts[i]
			#if( 0 < len(self.outsToCtrls) ): instanceTmp.outsToCtrls = duplicatedOutsToCtrls[i]

			duplicatedInstances.append(instanceTmp)


		self.keyToDuplicated[duplicateKey] = duplicatedInstances

		if( self.debug ):	
			self.TimeBuild['createInstance'] += time.clock() - TimeTmp
			TimeTmp = time.clock()	


		return duplicatedInstances


	def swapRefsToDuplicate( self , duplicateKey , dupliIndex , debug = 0 ):

		#SWAP REF - SUBRIG
		for i in range( len(self.SubRigs) ):
			self.SubRigs[i].swapRefsToDuplicate( duplicateKey , dupliIndex , debug )

		#SWAP REF - BUILD CLASS	
		self.Name.swapRefsToDuplicate(       duplicateKey , dupliIndex , debug )
		self.Attr.swapRefsToDuplicate(       duplicateKey , dupliIndex , debug )
		self.Pos.swapRefsToDuplicate(        duplicateKey , dupliIndex , debug )
		self.Parent.swapRefsToDuplicate(     duplicateKey , dupliIndex , debug )
		self.Link.swapRefsToDuplicate(       duplicateKey , dupliIndex , debug )
		self.CurveShape.swapRefsToDuplicate( duplicateKey , dupliIndex , debug )

		#SWAP REF - OTHER ATTR
		#print(self.classeType , self.Name.base.value() ,self.ins)
		for i in range(len(self.ins )):self.ins[i]  = self.ins[i].getDuplicatedInstance(  duplicateKey , dupliIndex )
		for i in range(len(self.outs)):self.outs[i] = self.outs[i].getDuplicatedInstance( duplicateKey , dupliIndex )
        '''
		for i in range( 0 , len(self.outsToCtrls)):
			for j in range( 0 , len(self.outsToCtrls[i]) ):
				self.outsToCtrls[i][j] = self.outsToCtrls[i][j].getDuplicatedInstance(  duplicateKey , dupliIndex )
        '''

	def addDupliAttrs( self , selfOrig , dupliIndex , **args  ):
		value             = args.get( 'value'             , [0,0,0 , 0,1,0 , 0,0,1] )		
		mode              = args.get( 'mode'              , 'mirror'                )	
		pivot             = args.get( 'pivot'             , [0,0,0 , 0,0,0 , 1,1,1] )
		namePrefix        = args.get( 'namePrefix'        , ['r','l']               )		
		nameReplace       = args.get( 'nameReplace'       , ['','']                 )	
		nameIncr          = args.get( 'nameIncr'          , ''                      )
		nameAdd           = args.get( 'nameAdd'           , []                      )
		noneMirrorAxe     = args.get( 'noneMirrorAxe'     , 4                       )		

		#UPDATE FOR TRANSFORM
		if( mode == 'transform' ) and (len(value)==10):
			value = value[0:9] + [ dupliIndex + 1 ]


		#SWAP REF - SUBRIG
		for i in range( 0 , len(self.SubRigs)):
			self.SubRigs[i].addDupliAttrs( selfOrig.SubRigs[i] , dupliIndex , **args  )


		#SPECIAL DUPLI ATTR
		if( self.classeType =='rigCtrl' ):
			self.Attr.add(     'dupliOrig' , Name = self.Name.ctrl     , empty = True , attrName = ['dupliOrig'  ] , attrType = ['string'] , attrValue = [ [ selfOrig.Name.ctrl, value , mode , pivot ] ] )
			self.Attr.remove(  'dupli' , attrName = ['dupli'      ] )
			selfOrig.Attr.add( 'dupli'     , Name = selfOrig.Name.ctrl , empty = True , attrName = ['dupli'      ] , attrType = ['string'] , attrValue = [ [ self.Name.ctrl    , value , mode , pivot ] ]  , incrKeyIfExist = True )		
		
		elif( self.classeType =='model' ):
			for j in range( 0 , len(self.objs) ):
				exec( 'NameTmp = self.Name.model{}'.format(j) )
				exec( 'NameTmpOrig = selfOrig.Name.model{}'.format(j) )
				self.Attr.add(     'dupliOrig{}'.format(j) , Name = NameTmp      , empty = True , attrName = ['dupliOrig'] , attrType = ['string'] , attrValue = [ [NameTmpOrig, value , mode , pivot ] ] )
				self.Attr.remove(  'dupli{}'.format(j) , attrName = ['dupli'] )
				selfOrig.Attr.add( 'dupli{}'.format(j)     , Name = NameTmpOrig  , empty = True , attrName = ['dupli']     , attrType = ['string'] , attrValue = [ [NameTmp    , value , mode , pivot ] ] , incrKeyIfExist = True )

		elif( self.classeType =='rigSkeletonChain' ):

			for i in range( 0 , len(self.outs) ):
				self.Attr.add( 'dupliOrig{}'.format(i) , Name = self.outs[i]     , empty = True , attrName = ['dupliOrig'] , attrType = ['string'] , attrValue = [ [ selfOrig.outs[i], value , mode , pivot ] ] )
				self.Attr.remove(  'dupli{}'.format(i) , attrName = ['dupli'] )
				selfOrig.Attr.add( 'dupli{}'.format(i) , Name = selfOrig.outs[i] , empty = True , attrName = ['dupli']     , attrType = ['string'] , attrValue = [ [ self.outs[i]    , value , mode , pivot ] ] , incrKeyIfExist = True )

		'''
		for j in range( 0 , len(self.outs) ):
			self.Attr.add( 'out{0}'.format(j) , Name = self.outs[j]  , empty = True , attrName = ['dupliOrig'] , attrType = ['string'] , attrValue = [ [ selfOrig.outs[j] , value , mode , pivot ] ] )
		'''


	def updateSubRigAttr( self ):

		for i in range( 0 , len(self.SubRigs)):
			self.SubRigs[i].updateSubRigAttr()
			
		for i in range( 0 , len(self.SubRigsName)):
			exec('self.{} = self.SubRigs[i]'.format(self.SubRigsName[i]) )



