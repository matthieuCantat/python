

###########################################
############### RIG BOUND B ###############
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
pathConstraints = 'D:/mcantat_BDD/projects/cute/assets/carrierShipD/maya/scenes/carrierShipD_utils_rigBoundBConstraints.xml'
pathSkinning    = 'D:/mcantat_BDD/projects/cute/assets/carrierShipD/maya/scenes/carrierShipD_utils_rigBoundBSkinning.xml'
pathRigBoundB   = 'D:/mcantat_BDD/projects/cute/assets/carrierShipD/maya/scenes/carrierShipD_rigBoundB.ma'




####################################################################
rwi.mayaScene_load( pathRigSkeleton , open = True  )
####################################################################



#BUILD
mc.delete('hi_GRP')
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


#REORDER HIERARCHY TUBE
tubeGrp         = 'tubes_GRP'
tubeStraightGrp = 'tubesStraight_GRP'
mc.createNode( 'transform' , n = tubeGrp         , p = 'rigPuppet_GRP' )
mc.createNode( 'transform' , n = tubeStraightGrp , p = 'rigPuppet_GRP' )
mc.parent( mc.ls( "*Tube*_GEO"         , type = 'transform' ) , tubeGrp         )
mc.parent( mc.ls( "*TubeStraight*_GEO" , type = 'transform' ) , tubeStraightGrp )



#CONNECT LIGHT
attr = '.lightVisibility'
attrVis = '.visibility'
mc.connectAttr( 'dampGiro0_JNT'+attr , 'dampGiroRayLow_GEO'+attrVis )
for side in ['r','l']:

	mc.connectAttr( '{}_propulsorFire0_JNT{}'.format(side,attr)   , '{}_propulsorFireLow_GEO{}'.format(side,attrVis) )
	mc.connectAttr( '{}_reacFire0_JNT{}'.format(side,attr)        , '{}_reacFireLow_GEO{}'.format(side,attrVis) )

	mc.connectAttr( '{}_reacGiro0_JNT{}'.format(side,attr)        , '{}_reactorGiroRayLow_GEO{}'.format(side,attrVis) )
	mc.connectAttr( '{}_propulsorGiro0_JNT{}'.format(side,attr)   , '{}_propulsorGiroRayLow_GEO{}'.format(side,attrVis) )
	mc.connectAttr( '{}_hook0GiroCover0_JNT{}'.format(side,attr) , '{}_hook0GiroHolderRayLow_GEO{}'.format(side,attrVis) )
	mc.connectAttr( '{}_hook1GiroCover0_JNT{}'.format(side,attr) , '{}_hook1GiroHolderRayLow_GEO{}'.format(side,attrVis) )
	mc.connectAttr( '{}_hook0GiroArm0_JNT{}'.format(side,attr)    , '{}_hook0GiroArmRayLow_GEO{}'.format(side,attrVis) )
	mc.connectAttr( '{}_hook1GiroArm0_JNT{}'.format(side,attr)    , '{}_hook1GiroArmRayLow_GEO{}'.format(side,attrVis) )
	
	for letter in ['A','B','C','D','E','F']:
		mc.connectAttr( '{}_projector{}0_JNT{}'.format(side,letter,attr), '{}_sideProjector{}RayLow_GEO{}'.format(side,letter,attrVis) )
	
	for letter in ['A','B','C','D','E']:
		mc.connectAttr( '{}_giro{}0_JNT{}'.format(side,letter,attr), '{}_giro{}RayLow_GEO{}'.format(side,letter,attrVis) )




#CONNECT STRAIGTHEN TUBE
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




#CLEAN VISIBILITY
grps = mc.listRelatives("low_GRP", ad = True , type = "transform")
for grp in grps:
	soucres = mc.listConnections( grp + '.visibility' , s = True , d = False )
	if(soucres==None):mc.setAttr( grp + '.visibility' , 1 )


#CLEAN ROOT 
toKeep = ['rigPuppet_GRP','symPlane_reactor1','symPlane_hook1','symPlane_damp1']
rootElem = mc.ls("|*" , type = "transform")

init   = ['front','persp','side','top']
for elem in rootElem:
	if not (elem in toKeep ) and not ( elem in init ):
		mc.delete(elem)




####################################################################
rwi.mayaScene_save( pathRigBoundB )
####################################################################

