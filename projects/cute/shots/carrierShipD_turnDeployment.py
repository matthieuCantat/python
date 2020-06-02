'''
#ANIM____________________________________________________FIRST BUILD
import maya.cmds as mc
import python.utils.utilsMaya as utilsMaya
from python.classe.readWriteInfo import *
rwi = readWriteInfo()

mc.file( new = True , f = True )
utilsMaya.setSceneUnitToMeter()


path =  'D:/mcantat_BDD/projects/cute/shots/ASSET_LIBRARY/carrierShipD_rigPuppet.ma'
nbr  = 1
ns   = 'carrierShipD_???'
for i in range(0,nbr):rwi.mayaScene_load( path , ref = ns , incr = False )


path =  'D:/mcantat_BDD/projects/cute/shots/ASSET_LIBRARY/quadriPod_rigPuppet.ma'
nbr  = 0
ns   = 'quadriPod_???'
for i in range(0,nbr):rwi.mayaScene_load( path , ref = ns , incr = False )


path =  'D:/mcantat_BDD/projects/cute/shots/ASSET_LIBRARY/camera_rigPuppet.ma'
nbr  = 1
ns   = 'camera_???'
for i in range(0,nbr):rwi.mayaScene_load( path , ref = ns , incr = False )


path =  'D:/mcantat_BDD/projects/cute/shots/ASSET_LIBRARY/skydomeParking_rigPuppet.ma'
nbr  = 1
ns   = 'skydome_???'
for i in range(0,nbr):rwi.mayaScene_load( path , ref = ns , incr = False )


rwi.mayaScene_save( 'D:/mcantat_BDD/projects/cute/shots/carrierShipD_turnDeployment/maya/scenes/carrierShipD_turnDeployment_anim.ma' )


#RENDER____________________________________________________FIRST BUILD
import maya.cmds as mc
import python.utils.utilsMaya as utilsMaya
from python.classe.readWriteInfo import *
rwi = readWriteInfo()

mc.file( new = True , f = True )
utilsMaya.setSceneUnitToMeter()


path =  'D:/mcantat_BDD/projects/cute/shots/ASSET_LIBRARY/carrierShipD_rigBoundA.ma'
nbr  = 1
ns   = 'carrierShipD_???'
for i in range(0,nbr):rwi.mayaScene_load( path , ref = ns , incr = False )


path =  'D:/mcantat_BDD/projects/cute/shots/ASSET_LIBRARY/quadriPod_rigBoundA.ma'
nbr  = 0
ns   = 'quadriPod_???'
for i in range(0,nbr):rwi.mayaScene_load( path , ref = ns , incr = False )


path =  'D:/mcantat_BDD/projects/cute/shots/ASSET_LIBRARY/camera_rigBoundA.ma'
nbr  = 1
ns   = 'camera_???'
for i in range(0,nbr):rwi.mayaScene_load( path , ref = ns , incr = False )


path =  'D:/mcantat_BDD/projects/cute/shots/ASSET_LIBRARY/skydomeParking_rigBoundA.ma'
nbr  = 1
ns   = 'skydome_???'
for i in range(0,nbr):rwi.mayaScene_load( path , ref = ns , incr = False )



#RENDER_________ LOAD SKELETON ANIM
import python.classe.animCurve as ac
reload(python.classe.animCurve)
path = 'D:/mcantat_BDD/projects/cute/shots/carrierShipD_turnDeployment/maya/scenes/carrierShipD_turnDeployment_render.xml'
AnimCurve = ac.animCurve()
AnimCurve.createFromFile(path)
AnimCurve.toObjs()


#RENDER_________ SAVE
import maya.cmds as mc
import python
from python.classe.readWriteInfo import *
reload(python.classe.readWriteInfo)
rwi = readWriteInfo()

#rwi.mayaScene_load( 'D:/mcantat_BDD/projects/cute/shots/carrierShipD_turnDeployment/maya/scenes/carrierShipD_turnDeployment_render.ma' , open = True )
rwi.mayaScene_save( 'D:/mcantat_BDD/projects/cute/shots/carrierShipD_turnDeployment/maya/scenes/carrierShipD_turnDeployment_render.ma' )


'''


#ANIM_________ SAVE
import maya.cmds as mc
import python
from python.classe.readWriteInfo import *
reload(python.classe.readWriteInfo)
rwi = readWriteInfo()

#rwi.mayaScene_load( 'D:/mcantat_BDD/projects/cute/shots/carrierShipD_turnDeployment/maya/scenes/carrierShipD_turnDeployment_anim.ma' , open = True )
rwi.mayaScene_save( 'D:/mcantat_BDD/projects/cute/shots/carrierShipD_turnDeployment/maya/scenes/carrierShipD_turnDeployment_anim.ma' )



#ANIM_________ SAVE SKELETON ANIM
import python.utils.utilsRigPuppet as utilsRigPuppet
reload(python.utils.utilsRigPuppet)

path = 'D:/mcantat_BDD/projects/cute/shots/carrierShipD_turnDeployment/maya/scenes/carrierShipD_turnDeployment_render.xml'
rigs = ['carrierShipD_001:rigPuppet_GRP']
utilsRigPuppet.rigSkeleton_bakeAndSaveValues( path , mc.ls( "*rigPuppet_GRP" , type = "transform" , r = True ) )




#RENDER_________ SAVE
import maya.cmds as mc
import python
from python.classe.readWriteInfo import *
reload(python.classe.readWriteInfo)
rwi = readWriteInfo()

#rwi.mayaScene_load( 'D:/mcantat_BDD/projects/cute/shots/carrierShipD_turnDeployment/maya/scenes/carrierShipD_turnDeployment_render.ma' , open = True )
rwi.mayaScene_save( 'D:/mcantat_BDD/projects/cute/shots/carrierShipD_turnDeployment/maya/scenes/carrierShipD_turnDeployment_render.ma' )



#RENDER_________ LOAD SKELETON ANIM
import python.classe.animCurve as ac
reload(python.classe.animCurve)
path = 'D:/mcantat_BDD/projects/cute/shots/carrierShipD_turnDeployment/maya/scenes/carrierShipD_turnDeployment_render.xml'
AnimCurve = ac.animCurve()
AnimCurve.createFromFile(path)
AnimCurve.toObjs(replace = True)


