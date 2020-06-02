
#******************************************************** BUILD MODEL
import maya.cmds as mc
import python
from python.classe.model import *
reload( python.classe.model)
reload( python.classe.buildPosition)

#___________________________________________________________________________LOAD MODEL BASE
from python.classe.readWriteInfo import *
reload(python.classe.readWriteInfo)
rwi = readWriteInfo()
rwi.mayaScene_load( 'D:/mcantat_BDD/projects/cute/assets/camera/maya/scenes/camera_modelBase.ma'  , open = True )
#rwi.mayaScene_save( 'D:/mcantat_BDD/projects/cute/assets/camera/maya/scenes/camera_modelBase.ma' )
#___________________________________________________________________________LOAD MODEL BASE

import python.utils.utilsMaya as utilsMaya
utilsMaya.setSceneUnitToMeter()



#___________________________________________________________________________SAVE TO MODEL
rwi.mayaScene_save( 'D:/mcantat_BDD/projects/cute/assets/camera/maya/scenes/camera_model.ma' )
#___________________________________________________________________________SAVE TO MODEL
