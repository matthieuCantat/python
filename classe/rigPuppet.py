'''
#******************************************************** BUILD EXEMPLE 
import maya.cmds as mc
import python
from python.classe.rigPuppet import *

reload( python.classe.rigPuppet)

mc.file( f = True , new = True )
#=================================================
puppet = rigPuppet( n = 'arm' , pos = [ [5,0,3,0,0,0,1,1,1] , [0,0,0,0,0,0,1,1,1] ] )	
puppet.build()

setupSwitchVisibilityModel( modelTopGrp , driver , lods = ['low' , 'block' ] )
'''


from .rigModule import *
from .rigCtrl import *	
       
class rigPuppet(rig):

	def __init__( self , **args ):
		rig.__init__( self , **args )

		#CLASSE TYPE
		self.classeType = 'rigPuppet'
		#CLASSE BLUE PRINT
		self.Name.add( 'base'     , baseName = self.classeType )		
		self.Name.add( 'topNode' , ref = self.Name.base , type = 'GRP'  )	

		self.Attr.add( 'topNode'     , Name = self.Name.topNode     , attrName = ['ctrlVis' , 'skeletonVis' , 'skeletonRef' ] , attrType = [ 'int+'  , 'intOnOff'  , 'normal:template:reference' ]  , attrValue = [ 1 , 0 , 1 ] )
		#CLASSE UTILS
		self.SubRigs     += []
		self.SubRigsName += []
		self.ins        = []
		self.insAnim    = []
		self.outs       = []
		self.outsToCtrls= []
		self.ctrls      = []
		self.ctrlsDupli = []		
		#CLASSE MODIF
		self.ctrlVisPriority = args.get( 'ctrlVisPriority', 0 )
		self.ctrlScale       = args.get( 'ctrlScale' , 1 )	
		#INSTANCE MODIF
		name       = args.get( 'n'   , None )	
		pos        = args.get( 'pos' , None )

		if not( name == None ): self.Name.add( 'base' , copy = name ) 





import maya.cmds as mc
from ..utils import utilsMaya
from .buildAttribute import *

def setupSwitchVisibilityModel( modelTopGrp , driver , lods = ['low' , 'block' ] ):
	
	#INIT   
	Attr = buildAttribute()
	lodsDefault = ['default','none','all']
	lodsAll = [ lodsDefault[0] ] + lods + lodsDefault[1:]
	enumValues = ':'.join(lodsAll) + ':' 
	#GET MODEL GRPS
	modelGrps = mc.listRelatives( modelTopGrp , c = True , type = 'transform' )
	
	#GET ATTR INFO
	attrGrpLod = []

	for grp in modelGrps:
		#BUILD ATTR
		suffix = '_GRP'
		currentLod = ''
		for lod in lodsAll:
			tmp = lod.capitalize() + '_GRP'
			if( tmp in grp ):
				suffix = tmp 
				currentLod = lod
				break

		attrGrpLod.append( ( grp.split(suffix)[0] , currentLod , grp ) )

	#BUILD ATTR
	for i in range( 0 , len(modelGrps) ):

		attrName = attrGrpLod[i][0]
		driverAttr = driver + '.' + attrName
		if not( mc.objExists( driverAttr ) ):
			driverAttr = Attr.utils_mayaAddSpecialAttr( driver , attrName , enumValues , 0 )

		#BUILD CONDITIONS NODE
		currentLod = attrGrpLod[i][1]
		if( currentLod == '' ):
			currentLod = 'default'

		attrValue = lodsAll.index(currentLod)
		##########################################################
		condition = mc.createNode('condition')
		mc.connectAttr( driverAttr , ( condition + '.firstTerm') )

		mc.setAttr(( condition + '.secondTerm' ), attrValue )
		mc.setAttr(( condition + '.operation' ), 0 ) #is equal
		mc.setAttr(( condition + '.colorIfTrueR' ), 1 )
		mc.setAttr(( condition + '.colorIfFalseR' ), 0 )

		##########################################################
		conditionNone = mc.createNode('condition')
		mc.connectAttr( driverAttr , ( conditionNone + '.firstTerm') )

		mc.setAttr(( conditionNone + '.secondTerm' ), len(lodsAll) - 2 )
		mc.setAttr(( conditionNone + '.operation' ), 0 ) #is equal
		mc.setAttr(( conditionNone + '.colorIfTrueR' ), 0 )
		mc.setAttr(( conditionNone + '.colorIfFalseR' ), 1 )
		
		##########################################################
		conditionAll = mc.createNode('condition')
		mc.connectAttr( driverAttr , ( conditionAll + '.firstTerm') )

		mc.setAttr(( conditionAll + '.secondTerm' ), len(lodsAll) - 1 )
		mc.setAttr(( conditionAll + '.operation' ), 0 ) #is equal
		mc.setAttr(( conditionAll + '.colorIfTrueR' ), 1 )
		mc.setAttr(( conditionAll + '.colorIfFalseR' ), 0 )

		utilsMaya.buildOffsetConnection( (condition + ".outColorR") , (modelGrps[i] + '.visibility') , offsetAttrs = [[ '*' , (conditionNone + ".outColorR")] , [ '+' ,  (conditionAll + ".outColorR")]] ) 
