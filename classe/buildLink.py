#SOMETHING TO DO WITH CONSTRAINT ?
'''
	add a fonction to link to link the result constraint to an other attr , of place a usefull node inbetween like a multiply divide
'''

'''
reload(python.classe.trsBackUp)

reload(python.utils.utilsMaya)
# NAMES
import python
from python.classe.buildName import *
reload(python.classe.buildName)


import maya.cmds as mc
mc.file( f = True , new = True )

Names = buildName( )
Names.add( 'base'   , baseNameAppend = 'toto'     , type = 'grp' )		
Names.add( 'rigA'   , baseNameAppend = 'Arm'      , type = 'grp' , ref = Names.base )
Names.add( 'ctrlA'  , baseNameAppend = 'OffsetA'  , type = 'CTRL', ref = Names.rigA )
Names.add( 'joint'  , baseNameAppend = ''         , type = 'JNT' , ref = Names.ctrlA )
Names.add( 'masterA'  , baseNameAppend = 'masterA'         , type = 'GRP' , ref = Names.base )
Names.add( 'masterB'  , baseNameAppend = 'masterB'         , type = 'GRP' , ref = Names.base )
Names.add( 'slaveAB'  , baseNameAppend = 'slaveAB'         , type = 'GRP' , ref = Names.base )

# ATTRIBUT
from python.classe.buildAttribute import *
reload(python.classe.buildAttribute)

Attrs = buildAttribute()
Attrs.add(  'ctrlA'  , Name = Names.ctrlA , attrName = ['activate' , 'addA' , 'addB' , 'addC' , 'posSpace'  ]     , attrType = ['float']*4 , attrValue = [0]*4 )
Attrs.add(  'jointA' , Name = Names.joint , attrName = [ 'choice' , 'addResult' , 'addPlusResult' ]  , attrType = ['float']*3 , attrValue = [1]*3 )
# LINKS
from python.classe.buildLink import *
reload(python.classe.buildLink)


Links = buildLink()
Links.add(  'choice'  , Sources = [ Attrs.ctrlA.activate ]                                         , Destinations = [ Attrs.jointA.choice        ]   )
Links.add(  'addPlus' , Sources = [ Attrs.ctrlA.addA , Attrs.ctrlA.addB , Attrs.ctrlA.addC ]       , Destinations = [ Attrs.jointA.addPlusResult ] , type = 'add+'  )
Links.add(  'addT'     , Sources = [ Attrs.ctrlA.addA , Attrs.ctrlA.addB , Attrs.ctrlA.addC , 10 ] , Destinations = [ Attrs.jointA.addResult     ] , type = 'add'  )
Links.add(  'parent'  , Sources = [ Names.ctrlA ]                       , Destinations = [ Names.joint    ] , type = 'parent'  )
Links.add(  'const'   , Sources = [ Names.masterA , Names.masterB ]     , Destinations = [ Names.slaveAB  ] , type = 'parent'  )
Links.add(  'multiPos'    , Sources = [ [1,2,3] , [4,5,6] ]             , Destinations = [ Names.masterB  ] , type = 'parentSpace'  , spaceDriver = Names.ctrlA  , spaceAttr = 'pivotSpace' ,  spaceNames = ['posA','posB'] )      
Links.add(  'multiParent' , Sources = [ Names.masterA , Names.masterB ] , Destinations = [ Names.ctrlA    ] , type = 'parentSpace'  , spaceDriver = Names.ctrlA , spaceAttr = 'parentSpace' , spaceNames = ['spaceA','spaceB'] )       


Links.printInfo()

mc.createNode('transform' , n = Names.ctrlA.str() )
mc.createNode('transform' , n = Names.joint.str() )
mc.createNode('transform' , n = Names.masterA.str() )
mc.createNode('transform' , n = Names.masterB.str() )
mc.createNode('transform' , n = Names.slaveAB.str() )
Attrs.build()
Links.build()





# DUPLI A
dupliValue = [0,0,0 , 0,1,0 , 0,0,1]
dupliMode  = 'mirror'

duplicatedLinks = Links.duplicate( dupliValue , dupliMode , [0,0,0 , 0,0,0 , 1,1,1] , namePrefix = ['r','l'] , nameReplace = ['toto','tata'] , nameIncr = '' , orientLockAxe = 0 , orientInverseAxes = 0  )
duplicatedAttrs = Attrs.duplicate( dupliValue , dupliMode , [0,0,0 , 0,0,0 , 1,1,1] , namePrefix = ['r','l'] , nameReplace = ['toto','tata'] , nameIncr = '' , orientLockAxe = 0 , orientInverseAxes = 0  )
duplicatedNames = Names.duplicate( dupliValue , dupliMode , [0,0,0 , 0,0,0 , 1,1,1] , namePrefix = ['r','l'] , nameReplace = ['toto','tata'] , nameIncr = '' , orientLockAxe = 0 , orientInverseAxes = 0  )
duplicateKey = str(dupliValue) + dupliMode

duplicatedLinks[1].printInfo()

for i in range( 0 , len(duplicatedNames)):
    duplicatedAttrs[i].swapRefsToDuplicate(  duplicateKey , dupliIndex = i )
    duplicatedLinks[i].swapRefsToDuplicate(  duplicateKey , dupliIndex = i )

# DUPLI B
dupliValue = [10,0,0 , 0,15,0 , 0,0,1 , 5]
dupliMode  = 'transform'

duplicatedLinks = Links.duplicate( dupliValue , dupliMode , [0,0,0 , 0,0,0 , 1,1,1] , namePrefix = ['',''] , nameReplace = ['',''] , nameIncr = 'A' , orientLockAxe = 0 , orientInverseAxes = 0  )
duplicatedAttrs = Attrs.duplicate( dupliValue , dupliMode , [0,0,0 , 0,0,0 , 1,1,1] , namePrefix = ['',''] , nameReplace = ['',''] , nameIncr = 'A' , orientLockAxe = 0 , orientInverseAxes = 0  )
duplicatedNames = Names.duplicate( dupliValue , dupliMode , [0,0,0 , 0,0,0 , 1,1,1] , namePrefix = ['',''] , nameReplace = ['',''] , nameIncr = 'A' , orientLockAxe = 0 , orientInverseAxes = 0  )
duplicateKey    = str(dupliValue) + dupliMode

duplicatedLinks[2].printInfo()

for i in range( 0 , len(duplicatedNames)):
    duplicatedAttrs[i].swapRefsToDuplicate(  duplicateKey , dupliIndex = i )
    duplicatedLinks[i].swapRefsToDuplicate(  duplicateKey , dupliIndex = i )



'''





import maya.cmds as mc

from ..utils import utilsMaya
from ..utils import utilsPython
from ..utils import utilsMath
from ..utils import utilsMayaApi
from .build import *

import types
from .trsBackUp import *

class buildLink( build ):

	def __init__(self , **args):
		build.__init__(self , **args )
		#____________________________________________________________________RIG INFO
		#UTILS																
		#CLASSE
		self.classeType   = 'buildLink'	
		self.argsValue    = []
		#self.argsRef      = [ 'Sources' , 'Destinations' , 'type' , 'operation' , 'maintainOffset' , 'skipAxes' , 'spaceDriver', 'spaceAttr' , 'spaceNames' ]
	'''
	def add( self , key , **args ):
		Sources        = args.get( 'Sources'        , None                    )	
		Destinations   = args.get( 'Destinations'   , None                    )
		type           = args.get( 'type'           , 'normal'                )	
		operation      = args.get( 'operation'      , 'oneSlave'              )
		maintainOffset = args.get( 'maintainOffset' , 0                       )	
		skipAxes       = args.get( 'skipAxes'       , [0,0,0 , 0,0,0 , 0,0,0] )	
		spaceDriver    = args.get( 'spaceDriver'    , None                    )	
		spaceAttr      = args.get( 'spaceAttr'      , None                    )	
		spaceNames     = args.get( 'spaceNames'     , None                    )	

		args['Sources']        = Sources
		args['Destinations']   = Destinations
		args['type']           = type
		args['operation']      = operation
		args['maintainOffset'] = maintainOffset
		args['skipAxes']       = skipAxes		
		args['spaceDriver']    = spaceDriver
		args['spaceAttr']      = spaceAttr
		args['spaceNames']     = spaceNames		


		keyList = [ valueH['key'] for valueH in self.data ]
		if not( key in keyList ):
			self.dataAdd( key , **args )
		

		#if( type in ['add' , 'add+' , 'sub' , 'mult' , 'div' ] ) or ( operation in ['oneSlave'] ) or ( 1):
		#	return 1
	'''
	'''
		Names = []
		if( Sources == None ) or ( Destinations == None ): 
			pass
		elif( operation == '2by2' ):
			for i in range( 0 , len( Destinations ) ):
				if( i<len(Sources)      ): Names.append( Sources[i] )
				if( i<len(Destinations) ): Names.append( Destinations[i] )
	
		elif( operation == 'oneMaster' ):
			for i in range( 0 , len(Destinations) ):
				Names.append(Sources[0])
				Names.append( Destinations[i] )
		
		elif( operation == 'oneSlave' ):
			for i in range( 0 , len(Sources) ):
				Names.append(Sources[i])
				Names.append( Destinations[0] )
	
	
		for i in range( 0, len(Names) , 2 ):
			if( len(Names) <= i+1 ): break
			j = i/2
			newKey  = '{}.{}{}'.format( key , 'link' , j )
			newArgs = { 'Sources' : Names[i] , 'Destinations' : Names[i+1] , 'type' : type , 'operation' : operation , 'maintainOffset' : maintainOffset , 'skipAxes' : skipAxes }
			self.dataAdd( newKey , **newArgs )

	'''
	'''

	def processBuild( self , refs , value ):
		AttrSource       = refs['Sources']
		AttrDestination  = refs['Destinations'] 
		connectionType   = refs['type']
		operation        = refs['operation'] 
		maintainOffset   = refs['maintainOffset'] 
		skipAxes         = refs['skipAxes'] 
		spaceDriver      = refs['spaceDriver']
		spaceAttr        = refs['spaceAttr']
		spaceNames       = refs['spaceNames']

		if( type( AttrSource ) == types.ListType ):


			Names = []
			if( operation == '2by2' ):
				for i in range( 0 , len( AttrDestination ) ):
					if( i<len(AttrSource)      ): Names.append( AttrSource[i] )
					if( i<len(AttrDestination) ): Names.append( AttrDestination[i] )
			
			elif( operation in ['oneMaster','oneSlave'] ): Names = AttrSource + AttrDestination



			if( connectionType in [ 'add' , 'sub' , 'mult' , 'div' ] ):
				utilsMaya.buildSpecialConnection(  AttrSourceStr + AttrDestinationStr  , connectionType )
	
			elif( connectionType == 'add+' ):
				utilsMaya.buildSpecialConnection(  AttrSourceStr + AttrDestinationStr  , 'add' )
				utilsMaya.insertClamp( AttrDestinationStr[-1] , input = 1 , min = 0 , max = 999999999  )

			elif( connectionType in [ 'parent' , 'point' , 'orient' , 'aim' , 'scale' , 'poleVector' ] ):			
				utilsMaya.buildConstraint(  Names , [connectionType] , operation , maintainOffset , skipAxes )
			
			elif( connectionType in [ 'parentSpace' , 'pointSpace' , 'orientSpace' , 'aimSpace' , 'scaleSpace' , 'poleVectorSpace' ] ):				
				self.utils_buildSpacesSwitch( AttrSource , AttrDestination , [connectionType] , spaceDriver , spaceAttr , spaceNames , skipAxes )															
			else:
				intFloatType = [ types.IntType , types.FloatType ]

				if( operation == "2by2" ):
					for i in range( 0, len(Names) , 2 ):
						if(   type(Names[i+1]) in intFloatType ): mc.setAttr(     Names[i]   , Names[i+1] )
						elif( type(Names[i]  ) in intFloatType ): mc.setAttr(     Names[i+1] , Names[i]   )
						else:                                     mc.connectAttr( Names[i]   , Names[i+1] , f = True  )		
				elif( operation == "oneMaster" ):
					for i in range( 1, len(Names) ):
						if(   type(Names[i]) in intFloatType ): mc.setAttr(     Names[0] , Names[i] )
						elif( type(Names[0]) in intFloatType ): mc.setAttr(     Names[i] , Names[0] )
						else:                                   mc.connectAttr( Names[0] , Names[i] , f = True  )						

		else:

			if( connectionType in [ 'parent' , 'point' , 'orient' , 'aim' , 'scale' , 'poleVector' ] ):			
				utilsMaya.buildConstraint( [ AttrSource , AttrDestination ] , [connectionType] , operation , maintainOffset , skipAxes )
			else:
				if( type(AttrDestination) in [ types.IntType , types.FloatType ] ):
					mc.setAttr( AttrSource , AttrDestination )
				elif( type(AttrSource) in [ types.IntType , types.FloatType ] ):
					mc.setAttr( AttrDestination , AttrSource )
				else:
					mc.connectAttr( AttrSource , AttrDestination , f = True  )		


	'''

	def processBuild( self , refs , value ):
		buildCmds = ''

		connectionType   = refs.get('type' , 'simple' )

		if( connectionType in [ 'add' , 'sub' , 'mult' , 'div' , 'inverse01' ] ):
			#args 
			src   = refs['Sources']
			dest  = refs['Destinations']
			#BUILD 			
			src  = self.utils_addVisibilityIfNoAttr(src )
			dest = self.utils_addVisibilityIfNoAttr(dest)		
			buildCmds += 'utilsMaya.buildSpecialConnection( {} , "{}" )\n'.format( src + dest , connectionType)
		
		elif( connectionType == 'add+' ):
			#args 
			src   = refs['Sources']
			dest  = refs['Destinations']
			#BUILD  	
			src  = self.utils_addVisibilityIfNoAttr(src )
			dest = self.utils_addVisibilityIfNoAttr(dest)
			buildCmds += 'utilsMaya.buildSpecialConnection( {} , "add" )\n'.format( src + dest )						
			buildCmds += 'utilsMaya.insertClamp( "{}" , input = 1 , min = 0 , max = 999999999  )\n'.format( dest[-1] )

		elif( connectionType in [ 'parent' , 'point' , 'orient' , 'aim' , 'scale' , 'poleVector' ] ):
			#args 
			src            = refs['Sources']
			dest           = refs['Destinations']
			operation      = refs.get('operation'     , 'oneMaster' )
			maintainOffset = refs.get('maintainOffset', 1           )
			skipAxes       = refs.get('skipAxes'      , [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ]          ) 
			clear          = refs.get('clear'      , True )   
			#BUILD 				
			Names = src + dest
			if( operation == '2by2' ):
				Names = []
				for i in range( 0 , len( dest ) ):
					if( i<len(src)  ): Names.append( src[i]  )
					if( i<len(dest) ): Names.append( dest[i] )

			buildCmds += 'utilsMaya.buildConstraint( {} , ["{}"] , "{}" , {} , {} , clear = {} )\n'.format( Names , connectionType , operation , maintainOffset , skipAxes , clear )		
		
		elif( connectionType in [ 'parentSpace' , 'pointSpace' , 'orientSpace' , 'aimSpace' , 'scaleSpace' , 'poleVectorSpace' ] ):				
			#args 
			src            = refs['Sources']
			dest           = refs['Destinations']
			skipAxes       = refs.get('skipAxes', [0,0,0 , 0,0,0 , 0,0,0] )    
			spaceDriver    = refs['spaceDriver']
			spaceAttr      = refs['spaceAttr']
			spaceNames     = refs.get('spaceNames' , None ) 
			spaceValue     = refs.get('spaceValue' , None ) 
			maintainOffset = refs.get('maintainOffset' , 1 )      
			#BUILD 	
			buildCmds += 'utilsMaya.buildSpacesSwitch( {} , {} , ["{}"] , "{}" , "{}" , {} , {} , {} , {} )\n'.format( src , dest , connectionType , spaceDriver , spaceAttr , spaceNames , spaceValue , skipAxes , maintainOffset )															
		
		elif( connectionType in ['ikSCsolver','ikRPsolver'] ):
			#args 
			src            = refs['Sources']
			dest           = refs['Destinations']
			parents        = refs['parents']     
			#BUILD 
			buildCmds += 'utilsMaya.prepareJointForIk({})\n'.format(dest)	
			buildCmds += 'nameOut = mc.ikHandle( sol = "{}" ,  sj = "{}" , ee = "{}" )\n'.format( connectionType , dest[0] , dest[-1] )	
			buildCmds += 'mc.rename( nameOut[0] , "{}" )\n'.format(src[0])
			buildCmds += 'mc.rename( nameOut[1] , "{}" )\n'.format(src[1])
			for i in range(0,len(parents)):
				buildCmds += 'utilsMaya.safeParent( "{}" , "{}" )\n'.format(src[i],parents[i])	
		
		elif( connectionType == 'stretch' ):
			#args 
			src            = refs['Sources']
			dest           = refs['Destinations']
			parents        = refs['parents']  
			#BUILD 
			buildCmds += 'utilsMaya.buildDistanceNode( "" , "{}" , "{}" , parent = "{}" , outAttrDistance = "{}" , inOutAttrsStretch = [ "{}" , "{}" ]  )\n'.format(src[0] , src[1] , parents[0] , dest[0] , dest[1] , dest[2] )	
		elif( connectionType == 'blend' ):
			#args 
			src            = refs['Sources']
			dest           = refs['Destinations']
			#BUILD
			buildCmds += 'utilsMaya.buildNodeOperations( [ "{}" , "{}" , "blend" , "{}" , "=" , "{}"] )\n'.format(src[0],src[1],src[2],dest[0])
		elif( connectionType == 'coneGeometry' ):
			#args 
			src            = refs['Sources']
			dest           = refs['Destinations']
			parents        = refs['parents']     
			#BUILD 
			buildCmds += 'nameOut = utilsMaya.buildConeGeometry( {} , coneGeometryName = "{}" , attrsShape = {} , attrsColor = {} )\n'.format( src[0:2] , dest[0] , src[2:6] , src[6:] )	
			buildCmds += 'utilsMaya.safeParent( nameOut , "{}" )\n'.format(parents[0])	
		
		elif( connectionType == 'timeRotation' ):
			#args 
			src            = refs['Sources']
			dest           = refs['Destinations']  
			#BUILD 
			buildCmds += 'utilsMaya.buildTimeRotationSetup( inSpeedSin = "{}" , inAmplitudeSin = "{}" , inOffsetSin = "{}" , inSpeedLinear = "{}" , inOffsetLinear = "{}" , out = "{}" , multOffsetLinear = {} )\n'.format( src[0] , src[1] , src[2] , src[3] , src[4] , dest[0] , src[5] )
		else:
			intFloatType = [ types.IntType , types.FloatType ]
			#args
			src            = refs['Sources']
			dest           = refs['Destinations']			
			operation      = refs.get('operation', 'oneMaster' )
			#BUILD 
			src  = self.utils_addVisibilityIfNoAttr(src )
			dest = self.utils_addVisibilityIfNoAttr(dest)
			if( operation == "2by2" ):
				for i in range( 0, len(dest)  ):
					if(   type(dest[i]) in intFloatType ): buildCmds += 'mc.setAttr(     "{}" , {}              )\n'.format(src[i] ,dest[i])	
					elif( type(src[i] ) in intFloatType ): buildCmds += 'mc.setAttr(     "{}" , {}              )\n'.format(dest[i],src[i] )	
					else:                                  buildCmds += 'utilsMaya.safeConnectAttr( "{}" , "{}" )\n'.format(src[i] ,dest[i])			
			elif( operation == "oneMaster" ):
				for i in range( 0 , len(dest) ):
					if(   type(dest[i]) in intFloatType ): buildCmds += 'mc.setAttr(     "{}" ,  {}             )\n'.format(src[0] ,dest[i])	
					elif( type(src[0])  in intFloatType ): buildCmds += 'mc.setAttr(     "{}" ,  {}             )\n'.format(dest[i],src[0] )	
					else:                                  buildCmds += 'utilsMaya.safeConnectAttr( "{}" , "{}" )\n'.format(src[0] ,dest[i])							

		return buildCmds

	def value( self , index = None , updateData = False ):
		dictTmp = self.refs(index)
		#args
		src   = dictTmp['Sources']
		dst   = dictTmp['Destinations']
		cType = dictTmp.get('type', 'simple')

		#build
		if( type( src ) == types.ListType ):			
			toPrint = ''
			for Attr in src:
				if( type(Attr) == types.InstanceType ): toPrint += Attr.str()
				else:                                   toPrint += '{}'.format(Attr)
				toPrint += ' '
			
			toPrint += ' --- {} ---> '.format( cType )

			for Attr in dst:
				if( type(Attr) == types.InstanceType ): toPrint += Attr.str()
				else:                                   toPrint += '{}'.format(Attr)
				toPrint += ' '

			return toPrint
		else:
			return '{} --- {} ---> {}'.format( src , cType , dst )


	def str( self ):
		return self.value()

	def dataFlatReorderCustom(self):
		'''
			put parentSpace at the end because it override the existing constraint
		'''
		newDataFlat     = []
		dataParentSpace = []
		for i in range( 0 , len(self.dataFlat)):

			if( 'spaceDriver' in self.dataFlat[i].keys() ):
				dataParentSpace.append( self.dataFlat[i] )
			else:
				newDataFlat.append(self.dataFlat[i])


		self.dataFlat = newDataFlat + dataParentSpace

	'''
	def utils_buildSpacesSwitch( self , AttrSource , AttrDestination , connectionType , spaceDriver , spaceAttr , spaceNames , skipAxes ):

		AttrSourceStr = []
		for Attr in AttrSource:
			if(   type(Attr) == types.InstanceType ): AttrSourceStr.append( Attr.value() )
			else:                                     AttrSourceStr.append( Attr         )

		AttrDestinationStr = []
		for Attr in AttrDestination:
			if( type(Attr) == types.InstanceType ): AttrDestinationStr.append( Attr.value() )
			else:                                   AttrDestinationStr.append( Attr       )

		if( type(spaceDriver) == types.InstanceType ): spaceDriver = spaceDriver.str()
		if( type(spaceAttr  ) == types.InstanceType ): spaceAttr   = spaceAttr.str()
		

		#GET VALUE
		attrDriver        = spaceDriver + '.' + spaceAttr
		attrDriverExists  = mc.objExists(attrDriver)
		masters           = AttrSourceStr
		slave             = AttrDestinationStr[0]

		#CHECK CONSTRAINT
		weightAttrs = []
		constraintBase = mc.listConnections( ( slave + '.parentInverseMatrix[0]' ) , s = False , d = True )
		if not(constraintBase == None ):
			weightAttrs = self.utils_constraintExtractWeightAttrs(constraintBase[0])
 		
		valueOffset = len(weightAttrs)

		#BUILD ATTR
		if( spaceNames == None ):
			if not( attrDriverExists ):
				mc.addAttr( spaceDriver , ln = spaceAttr , at = "long" , dv = 0 )
				mc.setAttr( attrDriver  , e = True , keyable = True )
		else:
			if not( attrDriverExists ):
				enumStr = '{}:{}:'.format( 'None' , ':'.join(spaceNames) )
				mc.addAttr( spaceDriver , ln = spaceAttr , at = "enum"  , en = enumStr , dv = 0 )
				mc.setAttr( attrDriver  , e = True , keyable = True )
			else:
				enumStrBase = mc.addAttr( attrDriver , q = True , en = True  )
				enumStr = '{}:{}:'.format( enumStrBase , ':'.join(spaceNames) )
				mc.addAttr( attrDriver , e = True , en = enumStr  )

		#BUILD CONSTRAINT OR SDK SWITCH
		if( type(masters[0]) == types.StringType ):

			#GET CONTRAINT TYPE
			constraintTypes = []
			for cType in connectionType:
				constraintTypes.append( cType.split('Space')[0] )

			#BUILD CONSTRAINT
			utilsMaya.buildConstraint( masters + [ slave ] , constraintTypes , 'oneSlave' , 1 , skipAxes )
			constraint = mc.listConnections( ( slave + '.parentInverseMatrix[0]' ) , s = False , d = True )[0]

			#BUILD CONNECTIONS
			for i in range( 0 , valueOffset ):
				self.utils_conditionOnOffEqual( attrDriver , i             , constraint + '.' + weightAttrs[i] )
					
			for i in range( 0 , len(masters) ):
				self.utils_conditionOnOffEqual( attrDriver , i+valueOffset , constraint + '.' + masters[i] + 'W{}'.format(i+valueOffset)  )
		
		else:
			ValueTrs = trs()
			ValueTrs.createFromObj(slave, worldSpace = False)
			positions = [ ValueTrs.value ] + maters 
			utilsMaya.buildSdkPositionSwitch( positions , slave , attrDriver , valueOffset )
	'''				

	def utils_addVisibilityIfNoAttr( self , attrs ):
		for i in range(0,len(attrs)):
			if( type(attrs[i]) == types.StringType ):
				if not( '.' in attrs[i] ):
					attrs[i] += '.visibility'

		return attrs




	def utils_constraintExtractWeightAttrs( self , constraint ):
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


	def utils_conditionOnOffEqual( self , inA  , inB , out ):
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
				