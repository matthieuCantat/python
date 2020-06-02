
############################################################################ BUILD SKELETON
import maya.cmds as mc
import python
#___________________________________________________________________________LOAD RIG BASE
from python.classe.readWriteInfo import *
reload(python.classe.readWriteInfo)
rwi = readWriteInfo()
rwi.mayaScene_load( 'D:/mcantat_BDD/projects/cute/assets/camera/maya/scenes/camera_rigSkeleton.ma' , open = True )
#___________________________________________________________________________LOAD RIG BASE

import python.utils.utilsMaya as utilsMaya
utilsMaya.setSceneUnitToMeter()


#CONVERT CONSTRAINT TO SKIN
posJnt   = "pos0_JNT"
camTrsf  = "render_CAM"
camShape = mc.listRelatives( camTrsf , s = True , c = True )[0]

mc.parent("all_GRP","rigPuppet_GRP")
mc.parentConstraint( "body0_JNT" , "all_GRP" , mo = True )


mc.connectAttr( "nearClipPlane0_JNT.translateX" , camShape + ".nearClipPlane" )
mc.connectAttr( "farClipPlane0_JNT.translateX"   , camShape + ".farClipPlane"  )
mc.connectAttr( posJnt + ".clipPlaneVis"  , camShape + ".displayCameraNearClip"  )
mc.connectAttr( posJnt + ".clipPlaneVis"  , camShape + ".displayCameraFarClip"  )
mc.connectAttr( posJnt + ".clipPlaneVis"  , camShape + ".displayCameraFrustum"  )
mc.connectAttr( posJnt + ".rimLight"  , "rim_LIGHT.visibility" )

#CLEAN ROOT 
toKeep = ['rigPuppet_GRP']
rootElem = mc.ls("|*" , type = "transform")
rootElem = [ elem for elem in rootElem if not (elem in toKeep ) ]
mc.delete(rootElem)


#___________________________________________________________________________SAVE TO SKELETON
rwi.mayaScene_save( 'D:/mcantat_BDD/projects/cute/assets/camera/maya/scenes/camera_rigBoundA.ma' )
#___________________________________________________________________________SAVE TO SKELETON