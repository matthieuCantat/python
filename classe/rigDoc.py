'''


AUTO-RIG with procedural & heritance structure


GOAL:
Create an set of script to help build some rig.
It must be:
- Easy to read and understand:
	-short as possible( avoid Repetition)
	-with intuitive name for element ( class,methode,attribute,definition,variable)
	-intuitive behavior (bluePrint)
	-good documentation (here)
	-easy way to debug (printInfo) 
-Easy to use for a rigger
	-intuitive behavior (init/build/duplicate)
	-common and logical behavior (add/build/every ctrl Class is use on every rig with ctrl)
	-with intuitive name for element ( printInfo , build )
	- avoid repeatition with a duplicate fonction
	-possibility to modif the rig with one argument
	-easy to install, one path to define and he will find every other module
-Easy to use for a developper:
	- avoid repeatition with a rig use into rig ( ctrl in arm )
	-avoid multiple argument update with argument handle with dictionnary
	-allow customisation for the main script  with little proc ( process )



RIGGER BUILD SIDE (rig placement).

 Every rig is represented by a class:
 rigStretchyJoint
 rigModuleArm
 rigPuppetHuman

There is 3 level of rig here: rig / rig module / rigPuppet

rig: The simplest rig, there is no ctrl for the animator, there are mainly use for the skinning of part of a higher7 rig  ( stretchy joint / twist joint / interpolation joint )
rigModule: rig with ctrl for the animator is no ctrl for the animator ( arm , tail , chain )
rigPuppet: rig with ctrl and modeling. rigPuppetHuman

All those inherite from each other
mayaClasse -> mayaObject -> rig ->  rigModule -> rigPuppet

And each heritance bring some specificities:
mayaClasse:
	createFromFile( file )
	toFile( file )
	createFromMayaObj( obj )		
	toMayaObj( obj )							
mayaObject:
	build()
	rebuild()
	delete()
	duplicate( value = [0,0,0 , 0,1,0 , 0,0,1] , mode = 'mirror' , pivot = [0,0,0 , 0,0,0 , 1,1,1] , namePrefix = ['r','l'] , nameReplace = ['',''] , nameIncr = '' , nameAdd = [] , orientLockAxe = 0 , orientInverseAxes = 0  )	
	Attr / Dag / Link / Name / Parent / Pos / CurveShape (buildAttr)
rig:
	self.depthLevel = 0	
		self.ins        = []
		self.insAnim    = []
		self.outs       = []
		self.ctrls      = []
		self.ctrlsDupli = []	
	autoCreate a top node 
	everything created will be store in it
rigModule:
	autoCreate a group control skeleton and rig store under the top node with some switch state and visibility
	everything created will automaticely be sorted and place in those
rigPuppet:
	autoCreate a control called root that will be store under the group control
	autoCreate a groupe Model with a switch state and visibility on it, the model must be store in it


All the rig data is handle by those attributes:
Attr / Dag / Link / Name / Parent / Pos / CurveShape (buildAttr)

each attribute is a child of the build attribute. They got every information for building the rig.
the build script will call the build methode of each one of those class in that order
preBuild()
buildSubRigs()
Dag
Attr
Pos
Parent
Link
CurveShape
postBuild()
buildMayaObject()

if some of the build doesnt correspond to those Attribute, you can always ude the preBuild() or the postBuild()
Everything excepte those two last proc take the information define in the init of the rig

SubRigs correspond to the rig build under the rig. Every thing is handle by the autorig, you declare it in the init and put the 
return class in the array subRigs and subRigsName and the classe take care of everything

its build first in the build sequence with buildSubRig()



#RIGGER USE
#DEVELOPPER USE
#INTERNAL WORK





PRESENTION:

HOWIE

focus on arm:
- manual test to build on module on locators / skeleton arleady skin / 
SHOW-----> args name/pos/features like stretch or dyn 
SHOW-----> duplicate / 
SHOW-----> outs joints for the bind
SHOW-----> duplicate workflow ->model/rig/skin/anim*


focus on body:
SHOW-----> Same but for an entire rig

SPACE SHIP
SHOW-----> duplicate workflow ->model/rig/skin/anim*


'''