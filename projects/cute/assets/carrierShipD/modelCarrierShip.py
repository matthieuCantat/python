
############################################################################ BUILD MODEL
import maya.cmds as mc
import python
from python.classe.model import *
reload( python.classe.model)
reload( python.classe.buildPosition)
reload( python.utils.utilsRigPuppet)
#___________________________________________________________________________LOAD MODEL BASE
from python.classe.readWriteInfo import *
reload(python.classe.readWriteInfo)
rwi = readWriteInfo()
rwi.mayaScene_load( 'D:/mcantat_BDD/projects/cute/assets/carrierShipD/maya/scenes/carrierShipD_modelBase.ma' , open = True )
#___________________________________________________________________________LOAD MODEL BASE
#rwi.mayaScene_save( 'D:/mcantat_BDD/projects/cute/assets/carrierShipD/maya/scenes/carrierShipD_modelBase.ma'  )


import python.utils.utilsMaya as utilsMaya
utilsMaya.setSceneUnitToMeter()


mirrorReactor = {}
mirrorReactor['value']             = 'symPlane_reactor1'
mirrorReactor['mode']              = 'mirror'
mirrorReactor['pivot']             = [0,0,0 , 0,0,0 , 1,1,1]
mirrorReactor['namePrefix']        = []
mirrorReactor['nameReplace']       = []
mirrorReactor['nameIncr']          = ''
mirrorReactor['nameAdd']           = [ 'Left' , 'Right' ]
mirrorReactor['noneMirrorAxe']     = -1

mirrorHook = {}
mirrorHook['value']             = 'symPlane_hook1'
mirrorHook['mode']              = 'mirror'
mirrorHook['pivot']             = [0,0,0 , 0,0,0 , 1,1,1]
mirrorHook['namePrefix']        = []
mirrorHook['nameReplace']       = []
mirrorHook['nameIncr']          = ''
mirrorHook['nameAdd']           = [ 'Left' , 'Right' ]
mirrorHook['noneMirrorAxe']     = -1

mirrorDamp = {}
mirrorDamp['value']             = 'symPlane_damp1'
mirrorDamp['mode']              = 'mirror'
mirrorDamp['pivot']             = [0,0,0 , 0,0,0 , 1,1,1]
mirrorDamp['namePrefix']        = []
mirrorDamp['nameReplace']       = []
mirrorDamp['nameIncr']          = ''
mirrorDamp['nameAdd']           = [ 'Left' , 'Right' ]
mirrorDamp['noneMirrorAxe']     = -1

mirrorX = {}
mirrorX['value']             = [0,0,0 , 0,1,0 , 0,0,1]
mirrorX['mode']              = 'mirror'
mirrorX['pivot']             = [0,0,0 , 0,0,0 , 1,1,1]
mirrorX['namePrefix']        = ['r','l']
mirrorX['nameReplace']       = ['','']
mirrorX['nameIncr']          = ''
mirrorX['nameAdd']           = []
mirrorX['noneMirrorAxe']     = -1

transformHook = {}
transformHook['value']             = [0,0, -0.823 , 0, -28.847,0 , 1,1,1 ]
transformHook['mode']              = 'transform'
transformHook['pivot']             = [0,0,0 , 0,0,0 , 1,1,1]
transformHook['namePrefix']        = []
transformHook['nameReplace']       = []
transformHook['nameIncr']          = 'hook0'
transformHook['nameAdd']           = []
transformHook['noneMirrorAxe']     = 4


#BUILD
for lod in [ 'Hi' , 'Low' ]:
    modelClass_duplicateAndBuild( 'reactorCenter'+lod+'_GRP' , [ mirrorX ] )
    modelClass_duplicateAndBuild( 'reactorSym'+lod+'_GRP'    , [ mirrorReactor , mirrorX ] )    

    modelClass_duplicateAndBuild( 'hookCenter'+lod+'_GRP'    , [ transformHook , mirrorX] )
    modelClass_duplicateAndBuild( 'hookSym'+lod+'_GRP'       , [ mirrorHook , transformHook , mirrorX ] )   

    modelClass_duplicateAndBuild( 'dampSym'+lod+'_GRP'       , [ mirrorDamp , mirrorX ] )   
    
    modelClass_duplicateAndBuild( 'propulsor'+lod+'_GRP'     , [ mirrorX ] )    

    modelClass_duplicateAndBuild( 'side'+lod+'_GRP'          , [ mirrorX ] )    
    


#REORDER HIERARCHY          
for side in ['l','r']:
    for lod in [ 'Hi' , 'Low' ]:
        for name in ['hook0','hook1','reactor']:
            nameGrp = side + '_' + name + lod + '_GRP'
            matchObjs = mc.ls( side + '_' + name + '*' + lod + '*_GRP' , type = 'transform'  )
            mc.createNode( 'transform' , n = nameGrp , p = "ALL_grp" )
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
mc.parent(mc.ls("ALL_grp|*Hi_GRP"),"hi_GRP")
mc.parent("block_GEO","all_GRP")
mc.delete("ALL_grp")



#TMP FIX LIGHT MIRROR - REMOVING - IN SCALE
leftLights = mc.ls("l_*_LIGHT",type = "transform")
for light in leftLights:
    mc.setAttr( light + '.sz' , mc.getAttr(light + '.sz') * -1 )
    mc.setAttr( light + '.rx' , mc.getAttr(light + '.rx') + 180 )
    
#Freeze Transform tubes 
tubes = mc.ls("*Tube*_GEO",type = "transform")
for tube in tubes:
    mc.makeIdentity( tube , a = True , t = True , r = True , s = True)



mc.delete("tubeBuild_GRP")

#___________________________________________________________________________SAVE TO MODEL
rwi.mayaScene_save( 'D:/mcantat_BDD/projects/cute/assets/carrierShipD/maya/scenes/carrierShipD_model.ma' )
#___________________________________________________________________________SAVE TO MODEL


