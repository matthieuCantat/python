'''
#******************************************************** BUILD EXEMPLE
import maya.cmds as mc

import python
from python.classe.buildName import *
from python.classe.buildAttribute import *

reload(python.classe.buildName)
reload(python.classe.buildAttribute)

mc.file( f = True , new = True )

# BUILD INIT
Names = buildName( )
Names.add( 'base' , baseNameAppend = 'attrTest'  )	
Names.add( 'A'    , baseNameAppend = 'A'   , type = 'grp' , ref = Names.base )
Names.add( 'B'    , baseNameAppend = 'B'   , type = 'grp', ref = Names.base )
Names.add( 'C'    , baseNameAppend = 'C'   , type = 'grp' , ref = Names.base )

mc.createNode('transform' , n = Names.A.str() )
mc.createNode('transform' , n = Names.B.str() )
mc.createNode('transform' , n = Names.C.str() )

#_________________________________________________________ATTRIBUT BUILD

Attrs = buildAttribute()

#_________________________________________________________ATTRIBUT BUILD - add attrs
attrNames = [ 'none' ]
attrTypes = [ None ]
attrNames += ['float' , 'double' , 'int' , 'enum'              , 'string' ]
attrTypes += ['float' , 'double' , 'int' , 'enumA:enumB:enumC' , 'string' ]
attrNames += ['intPos' , 'intNeg' , 'intOnOff'   ]
attrTypes += ['int+'   , 'int-'   , 'intOnOff'   ]
attrNames += ['floatPos' , 'floatNeg' , 'floatOnOff' ]
attrTypes += ['float+'   , 'float-'   , 'floatOnOff' ]
attrNames += ['enumOnOff' ]
attrTypes += ['enumOnOff' ]
attrNames += ['separator' , 'title' ]
attrTypes += ['separator' , 'title' ]

Attrs.add(  'A' , Name = Names.A , attrName = attrNames , attrType = attrTypes )


#_________________________________________________________ATTRIBUT BUILD - modif attrs
Attrs.add(  'A' , Name = Names.A , attrName = ['t', 'r' ,'s','v' , 'ro' , 'ry' ] , attrKeyable = [0,1,0,0,1,1] , attrCb = [0,1,1,1,1,1] , attrLock = [1,0,0,1,0,1] )



Attrs.build()

'''


import maya.cmds as mc

from ..utils import utilsMaya
from ..utils import utilsPython
from ..utils import utilsMath
from ..utils import utilsMayaApi
from .build import *

class buildAttribute( build ):

	def __init__(self , **args):
		build.__init__(self , **args )
		#____________________________________________________________________RIG INFO
		#UTILS	
		self.defaultAttrNames    = []
		self.defaultAttrNames    += [ 'translate' , 'rotate' , 'scale' , 'rotatePivot' ]
		self.defaultAttrNames    += [ 'translateX' , 'translateY' , 'translateZ' ]
		self.defaultAttrNames    += [ 'rotateX'    , 'rotateY'    , 'rotateZ' ]
		self.defaultAttrNames    += [ 'scaleX'     , 'scaleY'     , 'scaleZ' ]
		self.defaultAttrNames    += [ 'visibility' , 'overrideDisplayType' , 'overrideEnabled' ]	
		self.defaultAttrNames    += [ 'rotatePivotX' , 'rotatePivotY' , 'rotatePivotZ' ]

		self.defaultAttrFlags       = { 't' : 'translate'  , 'tx' : 'translateX' , 'ty' : 'translateY' , 'tz' : 'translateZ'  }
		self.defaultAttrFlags.update( { 'r' : 'rotate'     , 'rx' : 'rotateX'    , 'ry' : 'rotateY'    , 'rz' : 'rotateZ'     } )
		self.defaultAttrFlags.update( { 's' : 'scale'      , 'sx' : 'scaleX'     , 'sy' : 'scaleY'     , 'sz' : 'scaleZ'      } )
		self.defaultAttrFlags.update( { 'v' : 'visibility' , 'ro' : 'rotateOrder'                                             } )

		#CLASSE
		self.classeType    = 'buildAttribute'	
		self.argsValue     = []
		self.argsRef       = [ 'Name' , 'attrName' , 'attrType' , 'attrValue' , 'attrKeyable' , 'attrCb' , 'attrLock' ]
		self.skipRefValues = [ None ]

	def add( self , key , **args ):
		Name           = args.pop('Name'        ,None)
		attrNames      = args.pop('attrName'    ,[] )
		attrTypes      = args.pop('attrType'    ,[] )
		attrValues     = args.pop('attrValue'   ,[] )
		attrKeyables   = args.pop('attrKeyable' ,[] )
		attrCbs        = args.pop('attrCb'      ,[] )	
		attrLocks      = args.pop('attrLock'    ,[] )				
		empty          = args.pop('empty'       , False )
		
		#FILL EMPTY ARRAY WITH NONE
		for i in range( 0,len(attrNames) ):
			if( len(attrTypes)    <= i): attrTypes.append(   None)
			if( len(attrValues)   <= i): attrValues.append(  None)
			if( len(attrKeyables) <= i): attrKeyables.append(None)
			if( len(attrCbs)      <= i): attrCbs.append(     None)
			if( len(attrLocks)    <= i): attrLocks.append(   None)

		#CONVECT ATTR FLAG DATA
		for i in range( 0,len(attrNames) ):	
			if( attrNames[i] in self.defaultAttrFlags.keys() ): attrNames[i] = self.defaultAttrFlags[attrNames[i]]

		#GET KEYS FROM DATA
		keyList = self.utilsData_getKeyList()

		# IF FIRST TIME ADD
		if not( key in keyList ): 
			self.dataAdd( key )	
			if not(empty):
				attrNames    = self.defaultAttrNames    + attrNames
				attrTypes    = [None]*len(self.defaultAttrNames) + attrTypes
				attrValues   = [None]*len(self.defaultAttrNames) + attrValues
				attrKeyables = [None]*len(self.defaultAttrNames) + attrKeyables
				attrCbs      = [None]*len(self.defaultAttrNames) + attrCbs
				attrLocks    = [None]*len(self.defaultAttrNames) + attrLocks

		# ADD
		newArgs = args
		newArgs['Name'] = Name 
		for i in range( 0,len(attrNames) ):

			newArgs['attrName']    = attrNames[i]
			newArgs['attrType']    = attrTypes[i]
			newArgs['attrValue']   = attrValues[i]
			newArgs['attrKeyable'] = attrKeyables[i]
			newArgs['attrCb']      = attrCbs[i]
			newArgs['attrLock']    = attrLocks[i]
	
			if('.' in key)or( attrNames[i] == None ):continue
			newKey = key + '.' + attrNames[i]
	
			self.dataAdd( newKey , **newArgs )


	def remove( self , key , **args ):
		Name           = args.pop('Name'        ,None)
		attrNames      = args.pop('attrName'    ,[] )
		
		#CONVECT ATTR FLAG DATA
		for i in range( 0,len(attrNames) ):	
			if( attrNames[i] in self.defaultAttrFlags.keys() ): attrNames[i] = self.defaultAttrFlags[attrNames[i]]

		#GET KEYS FROM DATA
		#keyList = self.utilsData_getKeyList()

		# REMOVE
		for i in range( 0,len(attrNames) ):

			if('.' in key)or( attrNames[i] == None ):continue
			newKey = key + '.' + attrNames[i]
	
			self.dataRemove( newKey )




	def processBuild( self , refs , value ):
		buildCmds = ''

		nameRef     = refs.get('Name'       , None )
		attrName    = refs.get('attrName'   , None )
		attrType    = refs.get('attrType'   , None )
		attrValue   = refs.get('attrValue'  , None )
		attrKeyable = refs.get('attrKeyable', None )	
		attrCb      = refs.get('attrCb'     , None )
		attrLock    = refs.get('attrLock'   , None )			
		#if not( attrName in self.defaultAttrNames ) or ( attrType == 'set' ):
		
		if not( nameRef == None ) and not( attrName == None ):

			if( attrType in [None , "None"] ) and ( [ attrValue , attrKeyable , attrCb , attrLock ] == [ None , None , None , None ] ):
				return ''
		
			if( attrType == 'string') and ( type(attrValue) == types.ListType ):
				attrValue = self.utils_mayaConvertToEnumValue(attrValue)

			if( attrName in ['translate' , 'rotate' , 'scale' , 'rotatePivot' ] ):
				for axe in ['X','Y','Z']:
					if(attrType == "string" ): buildCmds += 'utilsMaya.addSpecialAttr( "{}" , "{}" , "{}" , "{}" , {} , {} , {} )\n'.format(nameRef , attrName+axe , attrType , attrValue , attrKeyable , attrCb , attrLock)	
					else:                      buildCmds += 'utilsMaya.addSpecialAttr( "{}" , "{}" , "{}" ,  {}  , {} , {} , {} )\n'.format(nameRef , attrName+axe , attrType , attrValue , attrKeyable , attrCb , attrLock)	
			else:
				if(attrType == "string" ): buildCmds += 'utilsMaya.addSpecialAttr( "{}" , "{}" , "{}" , "{}" , {} , {} , {} )\n'.format(nameRef , attrName , attrType , attrValue , attrKeyable , attrCb , attrLock)	
				else:                      buildCmds += 'utilsMaya.addSpecialAttr( "{}" , "{}" , "{}" ,  {}  , {} , {} , {} )\n'.format(nameRef , attrName , attrType , attrValue , attrKeyable , attrCb , attrLock)	 


		return buildCmds

	def utils_dataIsBuildable( self , index ):
		refs = self.refs( index , convertInstance = False )

		nameRef     = refs.get('Name'       , None )
		attrName    = refs.get('attrName'   , None )
		attrType    = refs.get('attrType'   , None )
		attrValue   = refs.get('attrValue'  , None )
		attrKeyable = refs.get('attrKeyable', None )	
		attrCb      = refs.get('attrCb'     , None )
		attrLock    = refs.get('attrLock'   , None )

		if ( nameRef == None ) or ( attrName == None ):
			return False

		if( attrType in [None , "None"] ) and ( [ attrValue , attrKeyable , attrCb , attrLock ] == [ None , None , None , None ] ):
			return False


		return True

	def value( self , index = None , updateData = False ):
		dictTmp = self.refs( index  )
		return '{}.{}'.format( dictTmp.get('Name','') , dictTmp.get('attrName','') )

	def valuePrint(self , index = None ):
		dictTmp = self.refs(index)

		attrValue = dictTmp.get('attrValue','') 
		attrValueStr = ''
		if( type(attrValue) == types.InstanceType ):attrValueStr += '{} '.format( attrValue.str() )
		elif( type(attrValue) == types.ListType     ):
			for elem in attrValue:
				if( type(elem) == types.InstanceType ): attrValueStr += '{} '.format( elem.str() )
				else:                                   attrValueStr += '{} '.format( elem       )
		else: attrValueStr += '{} '.format( attrValue )

		return '{}.{} {} {}'.format( dictTmp.get('Name','') , dictTmp.get('attrName','') , dictTmp.get('attrType','') , attrValueStr )



	def str( self ):
		dictTmp = self.refs()
		return '{}.{}'.format( dictTmp.get('Name','') , dictTmp.get('attrName','') )




	def utils_mayaConvertToEnumValue( self , attrValue ):

		attrValueStr = ''
		for value in attrValue:
			if( type(value) == types.InstanceType ): attrValueStr += '{} '.format( value.str() )
			else:                                    attrValueStr += '{} '.format( value       )
		return attrValueStr
