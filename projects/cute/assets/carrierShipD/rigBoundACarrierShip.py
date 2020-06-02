

###########################################
############### RIG BOUND A ###############
###########################################



#INIT
import maya.cmds as mc
import python
import python.classe.readWriteInfo as readWriteInfo
import python.utils.utilsRigPuppet as utilsRigPuppet
import python.utils.utilsMaya      as utilsMaya

reload(python.classe.readWriteInfo)
reload(python.utils.utilsRigPuppet)
reload(python.utils.utilsMaya )

rwi = readWriteInfo.readWriteInfo()

pathRigSkeleton = 'D:/mcantat_BDD/projects/cute/assets/carrierShipD/maya/scenes/carrierShipD_rigSkeleton.ma'
pathConstraints = 'D:/mcantat_BDD/projects/cute/assets/carrierShipD/maya/scenes/carrierShipD_utils_rigBoundAConstraints.xml'
pathSkinning    = 'D:/mcantat_BDD/projects/cute/assets/carrierShipD/maya/scenes/carrierShipD_utils_rigBoundASkinning.xml'
pathRigBoundA   = 'D:/mcantat_BDD/projects/cute/assets/carrierShipD/maya/scenes/carrierShipD_rigBoundA.ma'




####################################################################
rwi.mayaScene_load( pathRigSkeleton , open = True  )
####################################################################




#BUILD
mc.delete('low_GRP')
mc.delete('block_GEO')
mc.parent("all_GRP","rigPuppet_GRP")


utilsRigPuppet.rigPuppet_loadConstraints( pathConstraints  , debug = True )
'''
objConstraints = mc.ls( '*_GEO' , type = 'transform' ) + mc.ls( '*_LIGHT' , type = 'transform' )
utilsRigPuppet.rigPuppet_saveConstraints( pathConstraints ,  objConstraints )
'''

utilsRigPuppet.rigPuppet_loadSkinning( pathSkinning  , debug = True )
'''
objSkinning = mc.ls( '*_GEO' , type = 'transform' )
utilsRigPuppet.rigPuppet_saveSkinning( pathSkinning ,  objSkinning )
'''


#CUSTOM TUBE SETUP
tubeGrp         = 'tubes_GRP'
tubeStraightGrp = 'tubesStraight_GRP'
mc.createNode( 'transform' , n = tubeGrp         , p = 'rigPuppet_GRP' )
mc.createNode( 'transform' , n = tubeStraightGrp , p = 'rigPuppet_GRP' )
mc.parent( mc.ls( "*Tube*_GEO"         , type = 'transform' ) , tubeGrp         )
mc.parent( mc.ls( "*TubeStraight*_GEO" , type = 'transform' ) , tubeStraightGrp )

meshes = mc.listRelatives( "tubes_GRP" , c = True , type = "transform" )
for i in range( 0 , len(meshes) ):
	splitTmp = meshes[i].split("Tube")
	tubeStraight = splitTmp[0] + "TubeStraight" + splitTmp[1]
	if(mc.objExists(tubeStraight)):
		ctrlDriver = None
		shape     = mc.listRelatives( meshes[i] , c = True , s =  True , f = True)[0]
		skinInput  = mc.listConnections( shape , s = True , d = False , t = "skinCluster" )[0]
		sJoints = mc.listConnections( skinInput , s = True , d = True , type = "joint" )
		for joint in sJoints:
			if( "Hang" in joint ):
				jointDriver = joint
		
		outAttr = utilsMaya.addSpecialAttr( jointDriver , 'straighten' , 'floatOnOff' , 0  )
		node = mc.blendShape(tubeStraight,meshes[i], foc = False)[0]
		mc.connectAttr( outAttr , node + '.' + tubeStraight )
		

for tubeStraightGeo in mc.ls( "*TubeStraight*_GEO" , type = "transform" ):
	mc.setAttr( tubeStraightGeo + '.visibility' , 0 )	


#CUSTOM LIGHT SETUP
for light in mc.ls( "*_LIGHT" , type = "transform" ):
    masters = utilsMaya.getConstraintMasters(light)
    mc.connectAttr(  masters[0] + '.lightVisibility'  , light + '.visibility'  )



#CLEAN VISIBILITY
grps = mc.listRelatives("hi_GRP", ad = True , type = "transform")
for grp in grps:
	soucres = mc.listConnections( grp + '.visibility' , s = True , d = False )
	if(soucres==None):mc.setAttr( grp + '.visibility' , 1 )


#CLEAN ROOT 
toKeep = ['rigPuppet_GRP']
rootElem = mc.ls("|*" , type = "transform")

init   = ['front','persp','side','top']
for elem in rootElem:
	if not (elem in toKeep ) and not ( elem in init ):
		mc.delete(elem)



for side in ['l','r']:
    mc.connectAttr( side + "_propulsorFire0_JNT.lightVisibility" , side + "_propulsorFireHi_GEO.visibility" )
    mc.connectAttr( side + "_reacFire0_JNT.lightVisibility"      , side + "_reacFireHi_GEO.visibility" )


####################################################################
rwi.mayaScene_save( pathRigBoundA )
####################################################################
