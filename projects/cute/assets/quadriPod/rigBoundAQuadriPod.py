
############################################################################ BUILD SKELETON
import maya.cmds as mc
import python
#___________________________________________________________________________LOAD RIG BASE
from python.classe.readWriteInfo import *
reload(python.classe.readWriteInfo)
rwi = readWriteInfo()
rwi.mayaScene_load( 'D:/mcantat_BDD/projects/cute/assets/quadriPod/maya/scenes/quadriPod_rigSkeleton.ma' , open = True )
#___________________________________________________________________________LOAD RIG BASE

import python.utils.utilsMaya as utilsMaya
utilsMaya.setSceneUnitToMeter()


#DELETE HI
mc.delete('low_GRP')

#___________________________________________________________________________LOAD CONSTRAINT
from python.utils.utilsRigPuppet import *
reload( python.utils.utilsRigPuppet )
path = 'D:/mcantat_BDD/projects/cute/assets/quadriPod/maya/scenes/quadriPod_utils_rigBoundAConstraints.xml'
rigPuppet_loadConstraints( path  , debug = True )
#rigPuppet_saveConstraints( path , mc.ls( '*_GEO' , type = 'transform' ) )
#___________________________________________________________________________LOAD CONSTRAINT

#___________________________________________________________________________LOAD SKINNING
from python.utils.utilsRigPuppet import *
reload( python.utils.utilsRigPuppet )
path = 'D:/mcantat_BDD/projects/cute/assets/quadriPod/maya/scenes/quadriPod_utils_rigBoundASkinning.xml'
rigPuppet_loadSkinning( path  , debug = True  )
#rigPuppet_saveSkinning( path ,  mc.ls( '*_GEO' , type = 'transform' )  )
#___________________________________________________________________________LOAD SKINNING



mc.parent("all_GRP","rigPuppet_GRP")

#CLEAN ROOT 
toKeep = ['rigPuppet_GRP']
rootElem = mc.ls("|*" , type = "transform")
rootElem = [ elem for elem in rootElem if not (elem in toKeep ) ]
mc.delete(rootElem)

#___________________________________________________________________________SAVE TO SKELETON
rwi.mayaScene_save( 'D:/mcantat_BDD/projects/cute/assets/quadriPod/maya/scenes/quadriPod_rigBoundA.ma' )
#___________________________________________________________________________SAVE TO SKELETON
