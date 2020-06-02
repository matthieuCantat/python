
############################################################################ UPDATE RIG BASE
import maya.cmds as mc
import python
#___________________________________________________________________________LOAD RIG BASE
from python.classe.readWriteInfo import *
reload( python.classe.readWriteInfo)
rwi = readWriteInfo()
rwi.mayaScene_load( 'D:/mcantat_BDD/projects/cute/assets/SkydomeParking/maya/scenes/SkydomeParking_rigBase.ma' , open = True )
#___________________________________________________________________________LOAD RIG BASE

import python.utils.utilsMaya as utilsMaya
utilsMaya.setSceneUnitToMeter()


#delete OLD
mc.delete(['render_CAM'])
#___________________________________________________________________________LOAD MODEL
rwi.mayaScene_load( 'D:/mcantat_BDD/projects/cute/assets/SkydomeParking/maya/scenes/SkydomeParking_model.ma' , clean = False )
#___________________________________________________________________________SAVE  RIG BASE
rwi.mayaScene_save( 'D:/mcantat_BDD/projects/cute/assets/SkydomeParking/maya/scenes/SkydomeParking_rigBase.ma' )
