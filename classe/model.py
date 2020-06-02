'''

#******************************************************** BUILD EXEMPLE RIG CTRL
import maya.cmds as mc
import python
from python.classe.model import *
reload( python.classe.model)

mc.file( 'D:/mcantat_BDD/projects/cute/quadripod/maya/scenes/quadriPod_modelBase.ma' , o = True , f = True  )
#_________________________________BUILD


toeRotation = {}
toeRotation['value']             = [0,0,0 , 0,90,0 , 1,1,1 , 4]
toeRotation['mode']              = 'transform'
toeRotation['pivot']             = [4.685,0,4.443 , 0,0,0 , 1,1,1]
toeRotation['namePrefix']        = []
toeRotation['nameReplace']       = []
toeRotation['nameIncr']          = 'toe0'
toeRotation['nameAdd']           = []
toeRotation['noneMirrorAxe']     = 4



mirrorZ = {}
mirrorZ['value']             = [0,0,0 , 0,1,0 , 1,0,0]
mirrorZ['mode']              = 'mirror'
mirrorZ['pivot']             = [0,0,0 , 0,0,0 , 1,1,1]
mirrorZ['namePrefix']        = ['r','l']
mirrorZ['nameReplace']       = ['','']
mirrorZ['nameIncr']          = ''
mirrorZ['nameAdd']           = []
mirrorZ['noneMirrorAxe']     = -1



mirrorX = {}
mirrorX['value']             = [0,0,0 , 0,1,0 , 0,0,1]
mirrorX['mode']              = 'mirror'
mirrorX['pivot']             = [0,0,0 , 0,0,0 , 1,1,1]
mirrorX['namePrefix']        = []
mirrorX['nameReplace']       = []
mirrorX['nameIncr']          = 'leg0'
mirrorX['nameAdd']           = []
mirrorX['noneMirrorAxe']     = -1


#_________________________________DUPLI TOE

toe   = model( names = ['legToe_GRP'] )

toeDuplicates = [toe]
dupliDicts = [ toeRotation , mirrorZ , mirrorX ]

for dict in dupliDicts:
	toeDuplicatesNext = []
	for dupli in toeDuplicates:
		toeDuplicatesNext += dupli.duplicate( **dict )
	toeDuplicates = toeDuplicatesNext[:]

for elem in toeDuplicates:
	elem.Pos.mirrorScale = 1
	elem.build()

#_________________________________DUPLI LEG
leg   = model( names = ['leg_GRP'] )

legDupli = leg.duplicate( **mirrorX )
#
legDupliFront  = legDupli[0].duplicate( **mirrorZ )
legDupliBack   = legDupli[1].duplicate( **mirrorZ )
#
legDupliFront[0].Pos.mirrorScale = 1	
legDupliFront[1].Pos.mirrorScale = 1	

legDupliBack[0].Pos.mirrorScale = 1
legDupliBack[1].Pos.mirrorScale = 1


legDupliFront[0].build()	
legDupliFront[1].build()	

legDupliBack[0].build()	
legDupliBack[1].build()	

#_________________________________BODY SIDE
bodySide   = model( names = ['bodySide_GRP'] )

bodySide.Pos.mirrorScale

bodySideDupliMirror = bodySide.duplicate( **mirrorZ )	


bodySideDupliMirror[0].Pos.mirrorScale = 1
bodySideDupliMirror[1].Pos.mirrorScale = 1	


bodySideDupliMirror[0].build()	
bodySideDupliMirror[1].build()	



pathSave = 'D:/mcantat_BDD/projects/cute/quadriPod/maya/scenes/quadriPod_modelOk.ma'


'''

from .mayaObject import *

class model(mayaObject):

	def __init__( self , **args ):
		mayaObject.__init__( self , **args )
		names  = args.get( 'names' , [] )	
		
		#GET ALL OBJS
		self.objs = []
		while( 0 < len(names) ):
	
			namesNext = []
			for name in names:
				shapes = mc.listRelatives( name , s = True , c = True )
				if( shapes == None ):
					childrens = mc.listRelatives( name , c = True )
					if not( childrens == None ):
						namesNext += childrens

				self.objs.append(name)
	
			names = namesNext


		self.objs = [x.encode('UTF8') for x in self.objs ]
		#CLASSE
		self.classeType = 'model'													
		#INSTANCE_______________________________BLUEPRINT
		for i in range( 0 , len(self.objs) ):		
			self.Name.add( 'model{}'.format(i) , copy = self.objs[i]  )

			shapes = mc.listRelatives( self.objs[i] , s = True , c = True )
			if( shapes == None ): continue			
			exec( 'self.Pos.add(  "model{0}" , Name = self.Name.model{0} , replace = self.objs[i] )'.format(i) )	

	def preBuild( self ):
		
		#CHECK PARENT
		objsParent = []
		for i in range( 0 , len(self.objs) ):
			parents = mc.listRelatives( self.objs[i] , p = True )
			if not( parents == None ):
				if( parents[0] in self.objs ): objsParent.append( self.objs.index(parents[0]) )
				else:                          objsParent.append( parents[0] )
			else:                              objsParent.append( '' )

		#GET NEW NAMES
		objsNew = []
		for i in range( 0 , len(self.objs) ):
			exec( 'dupli = self.Name.model{}.str()'.format(i) )
			objsNew.append(dupli)

		#BUILD
		for i in range( 0 , len(self.objs) ):
			utilsMaya.safeDuplicate( self.objs[i] , n = objsNew[i] )
			mc.delete( mc.listRelatives( objsNew[i] , c = True , type = 'transform' , f = True ) )

		#PARENT
		for i in range( 0 , len(self.objs) ):
			if( objsParent[i] == '' ):
				pass
			elif( type(objsParent[i]) == types.IntType ): 
				mc.parent( objsNew[i] , objsNew[objsParent[i]] )
			else:
				try:    mc.parent( objsNew[i] , objsParent[i] )
				except: pass

def modelClass_duplicateAndBuild( modelName , duplicateInfos ):
	Model         = model( names = [modelName] )
	ModelDupli = [Model]
	for dInfo in duplicateInfos:
		ModelDupliTmp = []
		for dupli in ModelDupli:
			ModelDupliTmp += dupli.duplicate( **dInfo )
		ModelDupli = ModelDupliTmp	       
	
	toExec = ''
	for Dupli in ModelDupli: 
		toExec += Dupli.build()
	exec(toExec)
	mc.delete( modelName )

	return toExec
