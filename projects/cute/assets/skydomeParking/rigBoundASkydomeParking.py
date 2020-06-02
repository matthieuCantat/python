
############################################################################ BUILD SKELETON
import maya.cmds as mc
import python
#___________________________________________________________________________LOAD RIG BASE
from python.classe.readWriteInfo import *
reload(python.classe.readWriteInfo)
rwi = readWriteInfo()
rwi.mayaScene_load( 'D:/mcantat_BDD/projects/cute/assets/skydomeParking/maya/scenes/skydomeParking_rigSkeleton.ma' , open = True )
#___________________________________________________________________________LOAD RIG BASE

import python.utils.utilsMaya as utilsMaya
utilsMaya.setSceneUnitToMeter()


#CONVERT CONSTRAINT TO SKIN
posJnt   = "pos0_JNT"

mc.parent("all_GRP","rigPuppet_GRP")
mc.parentConstraint( "body0_JNT" , "aiSkyDomeLight1" , mo = True )
mc.parentConstraint( "body0_JNT" , "sky" , mo = True )
mc.parentConstraint( "body0_JNT" , "groundBounce" , mo = True )
mc.parentConstraint( "body0_JNT" , "ambientLight1" , mo = True )
mc.parentConstraint( "sun0_JNT" , "directionalLight1" , mo = True )


mc.connectAttr( posJnt + ".vp2"  , "vp2_GRP.visibility"  )
mc.connectAttr( posJnt + ".arnold" , "arnold_GRP.visibility"  )


#CLEAN ROOT 
toKeep = ['rigPuppet_GRP']
rootElem = mc.ls("|*" , type = "transform")
rootElem = [ elem for elem in rootElem if not (elem in toKeep ) ]
mc.delete(rootElem)


#___________________________________________________________________________SAVE TO SKELETON
rwi.mayaScene_save( 'D:/mcantat_BDD/projects/cute/assets/skydomeParking/maya/scenes/skydomeParking_rigBoundA.ma' )
#___________________________________________________________________________SAVE TO SKELETON