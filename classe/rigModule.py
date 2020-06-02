'''
#******************************************************** BUILD EXEMPLE RIG CTRL
import maya.cmds as mc
import python
from python.classe.rigModule import *
reload(python.classe.rigModule)
reload(python.classe.buildAttribute)
#=================================================
module = rigModule()
print('____________________MODIF')
module.Name.setBaseName('panelA')

print('____________________BUILD')
module.build()

'''


from .rig import *
	
      
class rigModule(rig):	

	def __init__( self , **args ):
		rig.__init__(self , **args )
		#CLASSE TYPE
		self.classeType = 'rigModule'
		#CLASSE BLUE PRINT
		self.Name.add( 'base'    , baseName = self.classeType  )	
		self.Name.add( 'topNode' , ref = self.Name.base , baseNameAppend = 'Top' , type = 'GRP'  )
						
		self.Name.add( 'ctrlGrp'     , baseName = 'ctrl'     , type = 'hrc' , parent = self.Name.topNode)
		self.Name.add( 'skeletonGrp' , baseName = 'skeleton' , type = 'hrc' , parent = self.Name.topNode)							
		self.Name.add( 'rigGrp'      , baseName = 'rig'      , type = 'hrc' , parent = self.Name.topNode)

		self.Attr.add( 'topNode'     , Name = self.Name.topNode     , attrName = ['ctrlVis' , 'skeletonVis' , 'skeletonRef' ] , attrType = [ 'int+'  , 'intOnOff'  , 'normal:template:reference' ]  , attrValue = [ 1 , 0 , 1 ] )
		self.Attr.add( 'ctrlGrp'     , Name = self.Name.ctrlGrp     , attrName = ['visibility'] , attrType = ['float']  , attrValue = [1] )
		self.Attr.add( 'skeletonGrp' , Name = self.Name.skeletonGrp , attrName = [ 'overrideEnabled' , 'visibility' ] , attrType = ['set' , 'float']  , attrValue = [ 1 , 0 ] )#!!!!!!!!!!!!!!
		self.Attr.add( 'rigGrp'      , Name = self.Name.rigGrp      , attrName = ['visibility'] , attrType = ['float']  , attrValue = [0] )

		self.Link.add( 'skeletonVis' , Sources = [self.Attr.topNode.skeletonVis] , Destinations = [self.Attr.skeletonGrp.visibility]           )
		self.Link.add( 'skeletonRef' , Sources = [self.Attr.topNode.skeletonRef] , Destinations = [self.Attr.skeletonGrp.overrideDisplayType]  )		
		self.Link.add( 'rigGrp'      , Sources = [self.Attr.rigGrp.visibility]   , Destinations = [0]                                          )				
		#CLASSE UTILS
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
		name = args.get( 'n', None )
		if not( name == None ): self.Name.add( 'base' , copy = name ) 

										


	def buildMayaRig( self ):
		pass

