
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
rwi.mayaScene_load( 'D:/mcantat_BDD/projects/cute/assets/quadriPod/maya/scenes/quadriPod_modelBase.ma'  , open = True )
#rwi.mayaScene_save( 'D:/mcantat_BDD/projects/cute/assets/quadriPod/maya/scenes/quadriPod_modelBase.ma' )
#___________________________________________________________________________LOAD MODEL BASE

import python.utils.utilsMaya as utilsMaya
utilsMaya.setSceneUnitToMeter()


toeRotation = {}
toeRotation['value']             = [0,0,0 , 0,90,0 , 1,1,1 , 4]
toeRotation['mode']              = 'transform'
toeRotation['pivot']             = [ -1.506 , -0.019 , 1.588 , 0,0,0 , 1,1,1]
toeRotation['namePrefix']        = []
toeRotation['nameReplace']       = []
toeRotation['nameIncr']          = 'toe0'
toeRotation['nameAdd']           = []
toeRotation['noneMirrorAxe']     = 4


mirrorZ = {}
mirrorZ['value']             = [0,0,0 , 0,1,0 , 1,0,0]
mirrorZ['mode']              = 'mirror'
mirrorZ['pivot']             = [0,0,0 , 0,0,0 , 1,1,1]
mirrorZ['namePrefix']        = []
mirrorZ['nameReplace']       = []
mirrorZ['nameIncr']          = 'leg0'
mirrorZ['nameAdd']           = []
mirrorZ['noneMirrorAxe']     = -1


mirrorX = {}
mirrorX['value']             = [0,0,0 , 0,1,0 , 0,0,1]
mirrorX['mode']              = 'mirror'
mirrorX['pivot']             = [0,0,0 , 0,0,0 , 1,1,1]
mirrorX['namePrefix']        = ['r','l']
mirrorX['nameReplace']       = ['','']
mirrorX['nameIncr']          = ''
mirrorX['nameAdd']           = []
mirrorX['noneMirrorAxe']     = -1


#BUILD
for lod in [ 'Hi' , 'Low' ]:  
    modelClass_duplicateAndBuild( ('legToe'  +lod+'_GRP') , [ toeRotation , mirrorZ , mirrorX ] )
    modelClass_duplicateAndBuild( ('leg'     +lod+'_GRP') , [               mirrorZ , mirrorX ] )
    modelClass_duplicateAndBuild( ('bodySide'+lod+'_GRP') , [                         mirrorX ] )


#REORDER HIERARCHY      
for side in ['l','r']:
    for lod in [ 'Hi' , 'Low' ]:
        for name in ['leg0','leg1']:
            nameMatch = side + '_' + name +'Toe' 
            nameGrp  =  side + '_' + name + lod +'_GRP'
            matchObjs = mc.ls( nameMatch + '?' + lod + '_GRP' , type = 'transform'  )
            mc.parent( matchObjs , nameGrp )



#CLEAN HIERARCHY
grps = mc.listRelatives("ALL_grp", c = True )
for i in range(0,len(grps) ):
    childrens = mc.listRelatives( grps[i] , c = True )
    if( childrens == None )or( len(childrens) == 0 ): mc.delete(grps[i])


#REORDER HIERARCHY
mc.createNode( "transform" , n = "all_GRP" )
mc.createNode( "transform" , n = "hi_GRP"  , p = "all_GRP" )
mc.createNode( "transform" , n = "low_GRP" , p = "all_GRP" )
mc.parent(mc.ls("ALL_grp|*Low_GRP"),"low_GRP")
mc.parent(mc.ls("ALL_grp|*_GRP"),"hi_GRP")
mc.delete("ALL_grp")




#___________________________________________________________________________SAVE TO MODEL
rwi.mayaScene_save( 'D:/mcantat_BDD/projects/cute/assets/quadriPod/maya/scenes/quadriPod_model.ma' )
#___________________________________________________________________________SAVE TO MODEL
