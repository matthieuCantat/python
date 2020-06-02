





import maya.cmds as mc
import types
import string
import math
import os
from ..classe.trsBackUp import *
from ..classe.coords import *
from ..classe.curveShape import *
from ..classe.buildName import *
from ..classe.animCurve import *
from ..classe.animAttribute import *
from . import utilsMaya
from . import utilsMayaApi
from ..classe import readWriteInfo
import time
import maya.api.OpenMaya as ompy
from ..classe import skinCluster
import maya.mel


#dico[ctrlName] = [ ['ctrlA', transformValue , transformType , transformPivot] , ['ctrlB', transformValue , transformType , transformPivot]  ]



'''
import python.utils.utilsRigPuppet as uPuppet
reload(python.utils.utilsRigPuppet)
pathCtrlShape   = 'D:/mcantat_BDD/projects/cute/assets/carrierShipD/maya/scenes/carrierShipD_utils_ctrlShape.ma'
utilsRigPuppet.rigPuppet_saveCtrls( pathCtrlShape )
'''

def rigPuppet_saveCtrls( pathCtrlShape ):

	result = mc.confirmDialog(
	                title='SAVE CTRLS',
	                message='You will lose you current scene, do you want to continue?',
	                button=['Yes', 'No'],
	                defaultButton='No',
	                cancelButton='No',
	                dismissString='No')
	
	if( result == 'No'):
		return 0    
	
	rwi = readWriteInfo.readWriteInfo()
	ctrls = mc.ls( "*_CTRL" , type = "transform" )
	
	#CLEAN ATTR
	baseAttrs = ['translateX','translateY','translateZ','rotateX','rotateY','rotateZ','scaleX','scaleY','scaleZ','visibility']
	for ctrl in ctrls:
	    for attr in baseAttrs:
	        soucres = mc.listConnections( ( ctrl + '.' + attr ) , s = True , d = False , p = True )
	        if not( soucres == None ):
	            mc.disconnectAttr( soucres[0] , ( ctrl + '.' + attr ) )
	        mc.setAttr( ( ctrl + '.' + attr ) , cb = True , l = False , k = True )

	#UNPARENT
	mc.parent( ctrls , w = True )   
	
	#DELETE CHILDREN
	for ctrl in ctrls:
	    childrens = mc.listRelatives( ctrl , c = True)    
	    for child in childrens:
	        if not( mc.nodeType(child) == "nurbsCurve" ):
	            mc.delete(child)
		            
	#CLEAN ROOT 
	toKeep = ctrls
	rootElem = mc.ls("|*" , type = "transform")
	
	init   = ['front','persp','side','top']
	for elem in rootElem:
		if not (elem in toKeep ) and not ( elem in init ):
			mc.delete(elem)
	                
	#SAVE FILE                
	rwi.mayaScene_save( pathCtrlShape )   
	
	return 1


'''
import python.utils.utilsRigPuppet as uPuppet
reload(python.utils.utilsRigPuppet)
grps = [ 'r_hook0_GRP' , 'r_hook1_GRP' , 'l_hook0_GRP' , 'l_hook1_GRP' ]

dictSplitTitleToMembers = {}
dictSplitTitleToMembers['in']  = []
dictSplitTitleToMembers['out'] = ['Cover','Piston','Holder','Middle','Offset']

utilsRigPuppet.splitGrpsMembers( grps , dictSplitTitleToMembers )
'''

def splitGrpsMembers( grps , dictSplitTitleToMembers ):

	titles     = dictSplitTitleToMembers.keys()
	allMembersCombined = [ member for title in titles for member in dictSplitTitleToMembers[title] ]

	for grp in grps:
	    for title in titles:
	    	members = dictSplitTitleToMembers[title]

	        visGrpsMembers = []        
	        if( 0 < len(members) ):
	            for member in members:
	                visGrpsMembers += mc.ls( '{}|*{}*'.format(grp,member) , type = "transform" )
	        else:
	            allChildrens = mc.listRelatives( grp , c = True , type = "transform" )
	            allVisGrpMembers = []
	            for member in allMembersCombined:
	                allVisGrpMembers += mc.ls( '{}|*{}*'.format(grp,member) , type = "transform" )
	            visGrpsMembers = [ child for child in allChildrens if not( child in allVisGrpMembers) ]
	                
	        
	        newGrp = grp.split('_GRP')[0] + title.capitalize() + '_GRP'
	        mc.createNode( 'transform' , n = newGrp , p = 'rigPuppet_GRP')
	        mc.parent( visGrpsMembers , newGrp )



'''
import python.utils.utilsRigPuppet as uPuppet
reload(python.utils.utilsRigPuppet)
uPuppet.render_combineRenderScene( ['carrierShipD_workoutDamp','carrierShipD_workoutReactor','carrierShipD_workoutPropulsor','carrierShipD_workoutHook','carrierShipD_turnDeployment'] )
'''

def render_combineRenderScene( shotList ):
	pathCombinedShots = 'D:/mcantat_BDD/projects/cute/shots/_combinedShots/maya/scenes/'
	pathCombinedShotsMayaScene    = pathCombinedShots + 'combinedShots_render.ma'
	pathCombinedShotsAnimSkeleton = pathCombinedShots + 'combinedShots_render.xml'

	pathAnimSkeletonFiles = render_shotsToRenderAnimSkeletonFiles(shotList)
	print('pathAnimSkeletonFiles',pathAnimSkeletonFiles)

	AnimCurves = render_combineAnimSkeletonFile( pathAnimSkeletonFiles )
	AnimCurves.toFile(pathCombinedShotsAnimSkeleton)

	render_animSkeletonFileToMayaScene(pathCombinedShotsAnimSkeleton)

	#MIN MAX RANGE SET
	shotRange = AnimCurves.getRange()
	mc.playbackOptions( min = shotRange[0] , max = shotRange[1] )

	minRangeAttr = "camera_001:pos0_JNT.shotRangeMin"
	maxRangeAttr = "camera_001:pos0_JNT.shotRangeMax"

	minRangeAttrSource = mc.listConnections( minRangeAttr , s = True , d = False , p = True )
	maxRangeAttrSource = mc.listConnections( maxRangeAttr , s = True , d = False , p = True )

	if not( minRangeAttrSource == None ): mc.disconnectAttr( minRangeAttrSource[0] , minRangeAttr )
	if not( maxRangeAttrSource == None ): mc.disconnectAttr( maxRangeAttrSource[0] , maxRangeAttr )

	mc.setAttr(minRangeAttr , shotRange[0])
	mc.setAttr(maxRangeAttr , shotRange[1])

	#SAVE
	rwi = readWriteInfo.readWriteInfo()
	rwi.mayaScene_save( pathCombinedShotsMayaScene )



def render_shotsToRenderAnimSkeletonFiles(shotList):
	paths = []
	for shot in shotList:
		paths.append( 'D:/mcantat_BDD/projects/cute/shots/{0}/maya/scenes/{0}_render.xml'.format(shot) )
	return paths

def render_combineAnimSkeletonFile( pathAnimSkeletonFiles ):

	AnimCurves = []
	for path in pathAnimSkeletonFiles:
		AnimCurveTmp = animCurve()
		AnimCurveTmp.createFromFile(path)
		AnimCurves.append(AnimCurveTmp)

	AnimCurveCombined = animCurve()
	tOffset = 0
	for i in range( 0 , len(AnimCurves) ):

		for j in range( 0 , len(AnimCurves[i].objsAttrs) ):
			
			timesOffseted = [ time + tOffset for time in AnimCurves[i].times[j] ]

			if( AnimCurves[i].objsAttrs[j] in AnimCurveCombined.objsAttrs ):

				objAttrIndex = AnimCurveCombined.objsAttrs.index( AnimCurves[i].objsAttrs[j] )
				AnimCurveCombined.times[objAttrIndex]          += timesOffseted
				AnimCurveCombined.values[objAttrIndex]         += AnimCurves[i].values[j]

			else:

				AnimCurveCombined.objsAttrs.append( AnimCurves[i].objsAttrs[j] )
				AnimCurveCombined.times.append(     timesOffseted              )
				AnimCurveCombined.values.append(    AnimCurves[i].values[j]    ) 

		nbrFrames = 0
		for times in AnimCurves[i].times:
			if( nbrFrames < len(times) ):
				nbrFrames = len(times)
		tOffset += nbrFrames


	return AnimCurveCombined

'''
import python.utils.utilsRigPuppet as uPuppet
reload(python.utils.utilsRigPuppet)
uPuppet.render_animSkeletonFileToMayaScene( "" )
'''

def render_animSkeletonFileToMayaScene( pathAnimSkeletonFile ):

	#PROJECT INFO
	nsToPath = {}
	nsToPath["carrierShipD"] = 'D:/mcantat_BDD/projects/cute/shots/ASSET_LIBRARY/carrierShipD_rigBoundA.ma'
	nsToPath["quadriPod"]    = 'D:/mcantat_BDD/projects/cute/shots/ASSET_LIBRARY/quadriPod_rigBoundA.ma'
	nsToPath["camera"]       = 'D:/mcantat_BDD/projects/cute/shots/ASSET_LIBRARY/camera_rigBoundA.ma'
	nsToPath["skydome"]      = 'D:/mcantat_BDD/projects/cute/shots/ASSET_LIBRARY/skydomeParking_rigBoundA.ma'
	
	#READ AnimSkeletonFile
	AnimCurve = animCurve()
	AnimCurve.createFromFile(pathAnimSkeletonFile)

	#GET SCENE INFORMATION
	namespaces = []
	for objAttr in AnimCurve.objsAttrs:
		nsSplit = objAttr.split(':')
		namespaces.append(nsSplit[0])
	
	namespaces = list(set(namespaces))

	assetsNbr = {key: 0 for key in nsToPath.keys()} 

	for ns in namespaces:
		for key in nsToPath.keys():
			if( key in ns ):
				assetsNbr[key] +=1
				break
	
	#BUILD SCENE
	
	mc.file( new = True , f = True )
	utilsMaya.setSceneUnitToMeter()
	
	rwi = readWriteInfo.readWriteInfo()

	for key in assetsNbr.keys():
		for i in range(0,assetsNbr[key]):
			rwi.mayaScene_load( nsToPath[key] , ref = key + "_???" , incr = False )
	

	AnimCurve.toObjs()



'''
import python.utils.utilsRigPuppet as uPuppet
reload(python.utils.utilsRigPuppet)
uPuppet.render_save( rangeOverride = [1001,1178] )
'''

def render_save( rangeOverride = None , launchBatch = True ):
	#set the correct workspace
	path = mc.file( q = True , location = True )
	projectPath = path.split("maya")[0] + 'maya'

	existingWorkspaces = mc.workspace( listWorkspaces = True )
	if not( projectPath in existingWorkspaces ):
		mc.workspace( projectPath , newWorkspace = True )
	mc.workspace( projectPath , openWorkspace = True )

	#setScene
	attrs  = ["skydome_001:pos0_JNT.vp2","skydome_001:pos0_JNT.arnold","camera_001:pos0_JNT.rimLight"]
	values = [ 0                        , 1                           , 0                   ]
	for i in range( 0 , len(attrs) ):
	    upstream = mc.listConnections( attrs[i] , s = True , d = False , p = True )
	    if not( upstream == None ):mc.disconnectAttr( upstream[0] , attrs[i]  )
	    mc.setAttr( attrs[i] , values[i] )
	#setScene INFO
	cam = "camera_001:render_CAM"
	camShape = mc.listRelatives( cam , s = True , c = True , type = "camera" )[0]
	shotRangeMin = mc.getAttr( "camera_001:pos0_JNT.shotRangeMin")
	shotRangeMax = mc.getAttr( "camera_001:pos0_JNT.shotRangeMax")
	if not( rangeOverride == None ):
		shotRangeMin = rangeOverride[0]
		shotRangeMax = rangeOverride[1]
	
	#setScene RENDER
	mc.setAttr( 'defaultArnoldDriver.ai_translator', 'jpeg', type='string' )
	mc.setAttr( 'defaultArnoldDriver.colorManagement', 1 )
	camNamespace = cam.split(":")[0]
	mc.setAttr( "defaultRenderGlobals.imageFilePrefix" , camNamespace , type = "string" )
	mc.setAttr( "defaultRenderGlobals.imfPluginKey" , "jpeg" , type = "string" )
	mc.setAttr( "defaultRenderGlobals.animationRange" , 0 )
	mc.setAttr( "defaultRenderGlobals.startFrame" , shotRangeMin )
	mc.setAttr( "defaultRenderGlobals.endFrame" , shotRangeMax )
	for cam in mc.ls(type = "camera"):mc.setAttr( "{}.renderable".format(cam) , 0 )
	mc.setAttr( camShape + ".renderable" , 1 )
	mc.setAttr( "defaultRenderGlobals.imageFormat" , 8 )
	mc.setAttr( "defaultRenderGlobals.animation" , 1 )
	mc.setAttr( "defaultRenderGlobals.outFormatControl" , 0 )
	mc.setAttr( "defaultRenderGlobals.extensionPadding" , 4 )
	maya.mel.eval('setMayaSoftwareFrameExt("7", 0)')
	maya.mel.eval('multiframeFormat("jpeg");')
	
	mc.setAttr( "defaultResolution.width" , 1920 )
	mc.setAttr( "defaultResolution.height" , 1080 )
	mc.setAttr( "defaultResolution.deviceAspectRatio" , 1.778 )
	
	mc.setAttr( "defaultArnoldDriver.quality" , 100 )#100


	#setScene
	mc.setAttr(  "defaultArnoldRenderOptions.AASamples"             , 2 )#3
	mc.setAttr(  "defaultArnoldRenderOptions.GIDiffuseSamples"      , 2 )#2
	mc.setAttr(  "defaultArnoldRenderOptions.GISpecularSamples"     , 2 )#2
	mc.setAttr(  "defaultArnoldRenderOptions.GITransmissionSamples" , 1 )#2
	mc.setAttr(  "defaultArnoldRenderOptions.GISssSamples"          , 0 )#2
	mc.setAttr(  "defaultArnoldRenderOptions.GIVolumeSamples"       , 0 )#2

	if( launchBatch == True ):
		maya.mel.eval('mayaBatchRender();')
	

	


'''
import maya.cmds as mc
import os
import python
import python.utils.utilsRigPuppet as uPuppet
reload(python.utils.utilsRigPuppet)
reload(python.classe.readWriteInfo)
uPuppet.playblast_save()
'''

def playblast_save():
	rwi = readWriteInfo.readWriteInfo()

	filePath     = mc.file( q = True , location = True )
	fileName     = filePath.split('/')[-1]
	fileNameBase = fileName.split('.')[0]

	moviesPath   = '/'.join(filePath.split('/')[0:-2]) + '/movies'

	path = '{}/{}_v.avi'.format(moviesPath , fileNameBase)
	path = rwi.utils_pathIncrAndArchiveOld( path )

	mc.playblast( format = "avi" , filename = path , sequenceTime = 0 , clearCache = 1 , viewer = 0 , showOrnaments = 0 , fp = 4 , percent = 100 , compression = "none" , quality = 100 )


'''

import maya.cmds as mc
import os
import python
import python.utils.utilsRigPuppet as uPuppet
reload(python.utils.utilsRigPuppet)

uPuppet.pipe_setProjectWorkSpace('cute')
'''


def pipe_setProjectWorkSpace( projectName ):
	
	projectPath = 'D:/mcantat_BDD/projects/' + projectName
	shotPath    = projectPath + '/shots'
	assetPath   = projectPath + '/assets'

	shots  = os.listdir(shotPath)
	assets = os.listdir(assetPath)

	wsNameShots = []
	wsPathShots = []
	for shot in shots:
		pathTmp = shotPath + '/' + shot + '/maya/scenes'
		if( os.path.exists(pathTmp) ):
			wsNameShots.append(shot  )
			wsPathShots.append(pathTmp)
	
	wsNameAssets = []
	wsPathAssets = []
	for asset in assets:
		pathTmp = assetPath + '/' + asset + '/maya/scenes'
		if( os.path.exists(pathTmp) ):
			wsNameAssets.append(asset  )
			wsPathAssets.append(pathTmp)

	wsNames = wsNameAssets + wsNameShots
	wsPaths = wsPathAssets + wsPathShots

	existingWorkspaces = mc.workspace( listWorkspaces = True )
	print(existingWorkspaces)
	for i in range(0,len(wsPaths)):
		if not( wsPaths[i] in existingWorkspaces ):
			print('path: {}'.format(wsPaths[i]) )
			mc.workspace( wsPaths[i] , newWorkspace = True )



'''
#_________ SAVE
import python.utils.utilsRigPuppet as utilsRigPuppet
reload(python.utils.utilsRigPuppet)

path = 'D:/mcantat_BDD/projects/cute/shots/carrierShipD_lookDev/maya/scenes/carrierShipD_lookDev_modelValue.xml'
utilsRigPuppet.model_bakeAndSaveValues( path , ["carrierShipD_001:all_GRP"] )


#_________ LOAD
import python.classe.animCurve as ac
reload(python.classe.animCurve)
path = 'D:/mcantat_BDD/projects/cute/shots/carrierShipD_lookDev/maya/scenes/carrierShipD_lookDev_modelValue.xml'
AnimCurve = ac.animCurve()
AnimCurve.createFromFile(path)
AnimCurve.toObjs( overrideNamespace = "" )

'''

def model_bakeAndSaveValues( path , rigs , timeRange = None ):

	#GET NAMESPACE FROM RIGS
	namespaces = []
	for rig in rigs:
		if( ":" in rig ): namespaces.append(rig.split(":")[0])
		else:			  namespaces.append('')

	namespaces = list(set(namespaces))

	#GET RIGS INFO
	mainGrp = "all_GRP"
	objs = []
	for namespace in namespaces:
		transforms = mc.listRelatives( "{}:{}".format(namespace,mainGrp) , ad = True , type = "transform" )
		for trsf in transforms:
			shapeTmp = mc.listRelatives( trsf , c = True , s = True  )

			if not( shapeTmp == None ) and ( mc.nodeType(shapeTmp[0]) == "mesh" ):
				inMeshConnections = mc.listConnections( shapeTmp[0] + '.inMesh' , s = True , d = True )
				if( inMeshConnections == None ):
					objs.append( trsf )
		

	#GET OBJ ATTRS
	attrsToSkip = ['radius','visibility']
	objAttrs = []
	for obj in objs:
		attrs = utilsMaya.getManipulableAttr( obj ,  skipConnected = False  ) # radius visibility
		for attr in attrs:
			if not( attr in attrsToSkip ):
				objAttr = '{}.{}'.format(obj,attr) 
				objAttrs.append( objAttr )


	AnimCurve = animCurve()
	#GET TIME RANGE
	if( timeRange == None ):
		timeRange = [ mc.playbackOptions( q = True , min = True ) , mc.playbackOptions( q = True , max = True )]
		timeRange[0] = int(timeRange[0])
		timeRange[1] = int(timeRange[1]+1) 



	#GET NBR OF FRAME
	frameNbr = timeRange[1] - timeRange[0]

	#INIT AnimCurve
	for i in range(0,len(objAttrs)):
		AnimCurve.objsAttrs.append(  objAttrs[i]                        )
		AnimCurve.values.append(     [0    ]*frameNbr                   )
		AnimCurve.times.append(      range(timeRange[0],timeRange[1])   )

	#FILL AnimCurve with values
	for t in range(0,frameNbr):
		mc.currentTime( timeRange[0] + t )
		for i in range(0,len(objAttrs)):
			AnimCurve.values[i][t] = mc.getAttr(objAttrs[i])

	mc.currentTime( timeRange[0] )

	AnimCurve.removeUnchangedKeys()
	AnimCurve.toFile( path , clearOldVar = 1 , incr = 1 )






def rigSkeleton_bakeAndSaveValues( path , rigs , timeRange = None ):

	#GET NAMESPACE FROM RIGS
	namespaces = []
	for rig in rigs:
		if( ":" in rig ): namespaces.append(rig.split(":")[0])
		else:			  namespaces.append('')

	namespaces = list(set(namespaces))

	#GET RIGS INFO
	posJoint = "pos0_JNT"
	objs = []
	for namespace in namespaces:
		objs.append("{}:{}".format(namespace,posJoint))
		skeletonJoints = mc.listRelatives( "{}:{}".format(namespace,posJoint) , ad = True , type = "joint" )
		for jnt in skeletonJoints:
			if not( "End_JNT" in jnt):
				objs.append( jnt )
		

	#GET OBJ ATTRS
	attrsToSkip = ['radius','visibility']
	objAttrs = []
	for obj in objs:
		attrs = utilsMaya.getManipulableAttr( obj ,  skipConnected = False  ) # radius visibility
		for attr in attrs:
			if not( attr in attrsToSkip ):
				objAttr = '{}.{}'.format(obj,attr) 
				sources = mc.listConnections( objAttr , s = True , d = False )
				if not( sources == None ) and( 0 < len(sources) ):
					objAttrs.append( objAttr )


	AnimCurve = animCurve()
	#GET TIME RANGE
	if( timeRange == None ):
		timeRange = [ mc.playbackOptions( q = True , min = True ) , mc.playbackOptions( q = True , max = True )]
		timeRange[0] = int(timeRange[0])
		timeRange[1] = int(timeRange[1]+1) 



	#GET NBR OF FRAME
	frameNbr = timeRange[1] - timeRange[0]

	#INIT AnimCurve
	for i in range(0,len(objAttrs)):
		AnimCurve.objsAttrs.append(  objAttrs[i]                        )
		AnimCurve.values.append(     [0    ]*frameNbr                   )
		AnimCurve.times.append(      range(timeRange[0],timeRange[1])   )

	#FILL AnimCurve with values
	for t in range(0,frameNbr):
		mc.currentTime( timeRange[0] + t )
		for i in range(0,len(objAttrs)):
			AnimCurve.values[i][t] = mc.getAttr(objAttrs[i])

	mc.currentTime( timeRange[0] )

	AnimCurve.removeUnchangedKeys()
	AnimCurve.toFile( path , clearOldVar = 1 , incr = 1 )



def rigPuppet_combineMesh( objs , newMesh ):
	Skin = skinCluster.skinCluster()
	Skin.createFromObjs(objs , convertConstraint = True )
	Skin.toCombinedObj(newMesh)
	return newMesh
	


def spaceSwitch_getDictInfo( objAttrSwitch ):
	dictInfo = {}
	dictInfo['attr']           = objAttrSwitch       
	dictInfo['slave']          = spaceSwitch_getSlave(       dictInfo['attr'] )       
	dictInfo['slaveParent']    = spaceSwitch_getSlaveParent( dictInfo['attr'] )
	dictInfo['masters']        = spaceSwitch_getMasters(     dictInfo['attr'] )  
	dictInfo['value'] 		   = mc.getAttr(                 dictInfo['attr'] )
	dictInfo['offsetAttr']     = spaceSwitch_getOffsetAttrs( dictInfo['attr'] )
	dictInfo['offsetAttrBase'] = spaceSwitch_getOffsetAttrs( dictInfo['attr'] , suffix = 'Base' )
	enumValue                  = mc.addAttr(                 dictInfo['attr'] , q = True , enumName = True)		
	dictInfo['choices']        = enumValue.split(':')

	return dictInfo


def spaceSwitch_doSwitch( dictInfo  , value ,  transitionFrames = 0 ):
	print('rigPuppet_switchSpace')	
	baseAttrs = ['.translateX','.translateY','.translateZ','.rotateX','.rotateY','.rotateZ' ]	
	currentFrame =  mc.currentTime( q = True )
	valueOld = dictInfo['value']

	#KEY SWITCH
	mc.setKeyframe( dictInfo['attr'] , t=currentFrame-1 , v = dictInfo['value'] )
	mc.setKeyframe( dictInfo['attr'] , t=currentFrame   , v = value )
	
	#BUILD SNAP
	snapTmpBaseName    = "switchSpaceTMP_{}".format( dictInfo['attr'].split('.')[0] ) 
	snapGrp              = mc.createNode( 'transform' , n = snapTmpBaseName + '_GRP'  )
	snapSlaveParentGrp   = mc.createNode( 'transform' , n = snapTmpBaseName + '_slaveParent_GRP'   , p = snapGrp  )
	snapNextMasterGrp    = mc.createNode( 'transform' , n = snapTmpBaseName + '_nextMaster_GRP'    , p = snapGrp  )
	snapNextMasterOffset = mc.createNode( 'transform' , n = snapTmpBaseName + '_nextMaster_OFFSET' , p = snapNextMasterGrp )
	snapSlaveTarget      = mc.spaceLocator(             n = snapTmpBaseName + '_target_CTRL'  )[0]
	snapSlaveCurrent     = mc.spaceLocator(             n = snapTmpBaseName + '_current_CTRL' )[0]
	mc.parent( snapSlaveTarget  , snapSlaveParentGrp )
	mc.parent( snapSlaveCurrent , snapSlaveParentGrp )

	#KEY -1
	mc.currentTime(currentFrame-1) #========================================

	for attr in dictInfo['offsetAttr'][value]: 
		mc.setKeyframe( attr , t=currentFrame-1 )

	#SET SNAP VALUES  -1
	'''
	mc.delete(mc.parentConstraint( dictInfo['slaveParent'] , snapGrp ))

	for i in range( 0 , len( dictInfo['offsetAttrBase'][value] ) ): 
		mc.setAttr( snapOffset + baseAttrs[i] , mc.getAttr( dictInfo['offsetAttrBase'][value][i] ) )
	'''

	#KEY FK ++
	for t in range(0,transitionFrames+1):
		mc.currentTime(currentFrame+t) #========================================

		mc.delete(mc.parentConstraint( dictInfo['masters'][value] , snapSlaveParentGrp ))
	
		mc.delete(mc.parentConstraint( dictInfo['masters'][value] , snapNextMasterGrp ))
		for i in range( 0 , len( dictInfo['offsetAttrBase'][value] ) ): 
			mc.setAttr( snapNextMasterOffset + baseAttrs[i] , mc.getAttr( dictInfo['offsetAttrBase'][value][i] ) )
	
		mc.delete(mc.parentConstraint( snapNextMasterOffset    , snapSlaveCurrent ))

		#SET SNAP VALUES
		mc.setAttr( dictInfo['attr'] , dictInfo['value'] )	

		mc.delete(mc.parentConstraint( dictInfo['slave'] , snapSlaveTarget  ))

		mc.setAttr( dictInfo['attr'] , value )

		for i in range( 0 , len( dictInfo['offsetAttr'][value] ) ):
			newValueOffset = mc.getAttr( snapSlaveTarget + baseAttrs[i] ) - mc.getAttr( snapSlaveCurrent + baseAttrs[i] )
			mc.setAttr( dictInfo['offsetAttr'][value][i] , newValueOffset )
			mc.setKeyframe( dictInfo['offsetAttr'][value][i] , v = newValueOffset ) 
		
	#5CLEAN
	mc.delete(snapGrp)	




def switchIKFK_IKtoFKmatchSetup( objBase , objTarget , lengthA , rotAValue , rotBValue ,  objUp = None   ):
    root = mc.createNode( "transform" , n = objTarget+"_root_GRP_IKmatchTmp" )
    rotAOffset = mc.createNode( "transform" , n = objTarget+"rotA_OFFSET_IKmatchTmp" , p = root )
    rotA       = mc.spaceLocator(  n = objTarget+"rotA_CTRL_IKmatchTmp"  )[0]
    mc.parent(rotA,rotAOffset)
    rotBOffset = mc.createNode( "transform" , n = objTarget+"rotB_OFFSET_IKmatchTmp" , p = rotA )
    rotB       = mc.spaceLocator(  n = objTarget+"rotB_CTRL_IKmatchTmp" )[0]
    mc.parent(rotB,rotBOffset)
    mc.setAttr( rotBOffset + '.tx' , lengthA )
    mc.setAttr( rotBOffset + '.rz' , -180 )
    
    mc.pointConstraint(objBase,root)
    
    if( objUp == None ):
        mc.aimConstraint( objTarget , root , aimVector=[1,0,0] , upVector=[0,1,0] , worldUpType = "objectrotation" , worldUpVector = [0,1,0] , worldUpObject = objBase )
    else:
        mc.aimConstraint( objTarget , root , aimVector=[1,0,0] , upVector=[0,1,0] , worldUpType = "object" , worldUpObject = objUp )
    
    mc.setAttr( rotA + '.rz' , rotAValue )
    mc.setAttr( rotB + '.rz' , rotBValue )
    
    return [ root , rotA , rotB ]

#switchIKFK_IKtoFKmatchSetup('armHandleBase_CTRL' , 'armHandle_CTRL' , 4 , 20 , 25 , 'armPv_CTRL' )





def rigModuleArm_switchToFK( dictInfo  , transitionFrames = 0 ):
	root       = dictInfo['root']
	fk         = dictInfo['fk']
	handle     = dictInfo['handle']
	handleBase = dictInfo['handleBase']
	pv         = dictInfo.get( 'pv' , None )

	currentFrame =  mc.currentTime( q = True )

	#KEY SWITCH
	objAttrIK = root + '.IK'
	oldValue = 1.1
	newValue = 0

	mc.setKeyframe( objAttrIK , t=currentFrame-1 , v = oldValue)
	mc.setKeyframe( objAttrIK , t=currentFrame   , v = newValue)
	#KEY SWITCH - MODIF KEYS AFTER
	keyTimes  = mc.keyframe( objAttrIK , time=(currentFrame+1,currentFrame+10000), query=True,  timeChange=True)
	keyValues = mc.keyframe( objAttrIK , time=(currentFrame+1,currentFrame+10000), query=True, valueChange=True)

	if not ( keyTimes == None ):
		for i in range(0,len(keyTimes)):
			if( keyValues[i] == oldValue ): mc.setKeyframe( objAttrIK , t = keyTimes[i] , v = newValue )
			else: break
	

	#KEY FK - 1
	for i in range(0,len(fk)):
		attrsTmp = utilsMaya.getManipulableAttr( fk[i] )
		for j in range(0,len(attrsTmp)):
			objAttr = fk[i] + '.' + attrsTmp[j]
			mc.setKeyframe( objAttr , t=currentFrame-1 )

	#KEY FK ++
	for t in range(0,transitionFrames+1):

		if(0<t):mc.currentTime(currentFrame+t)

		dA = utilsMayaApi.getDistanceBetweenObjs( fk[0] , fk[1] )
		dB = utilsMayaApi.getDistanceBetweenObjs( fk[1] , fk[2] )
		dC = utilsMayaApi.getDistanceBetweenObjs( handleBase , handle )

		dA2 = pow(dA,2)
		dB2 = pow(dB,2)
		dC2 = pow(dC,2)

		if not( dA + dB < dC ):
			angleRootRad  = math.acos( (dA2 + dC2 - dB2)/(2*dA*dC) )
			angleElbowRad = math.acos( (dB2 + dA2 - dC2)/(2*dB*dA) )

			angleRoot  = math.degrees(angleRootRad)
			angleElbow = math.degrees(angleElbowRad)
		else:
			angleRoot  = 0
			angleElbow = 180


		setupTmp = switchIKFK_IKtoFKmatchSetup( handleBase , handle , dA , angleRoot , angleElbow , objUp = pv )
		
		try:    mc.orientConstraint( setupTmp[1] , fk[0] ) 
		except: mc.setKeyframe( fk[0] + '.rotateZ', angleRoot )

		try:    mc.orientConstraint( setupTmp[2] , fk[1] ) 
		except: mc.setKeyframe( fk[1] + '.rotateZ', angleElbow )

		for i in range(0,2):
			for axe in ['X','Y','Z']:
				try: mc.setKeyframe( fk[i] + '.rotate' + axe , t=currentFrame+t )
				except:pass	

		#mc.delete(setupTmp)

	if not(transitionFrames == 0):mc.currentTime(currentFrame)

	return 1	

def rigModuleArm_switchToIK( dictInfo , transitionFrames = 0 ):
	root       = dictInfo['root']
	fk         = dictInfo['fk']
	handle     = dictInfo['handle']
	handleBase = dictInfo['handleBase']
	pv         = dictInfo.get( 'pv' , None )

	currentFrame =  mc.currentTime( q = True )

	#KEY SWTITCH
	objAttrIK = root + '.IK'
	oldValue = 0
	newValue = 1.1

	mc.setKeyframe( objAttrIK , t=currentFrame-1 , v = oldValue)
	mc.setKeyframe( objAttrIK , t=currentFrame   , v = newValue)
	#KEY SWITCH - MODIF KEYS AFTER
	keyTimes  = mc.keyframe( objAttrIK, time=(currentFrame+1,currentFrame+10000), query=True,  timeChange=True)
	keyValues = mc.keyframe( objAttrIK, time=(currentFrame+1,currentFrame+10000), query=True, valueChange=True)

	if not ( keyTimes == None ):
		for i in range(0,len(keyTimes)):
			if( keyValues[i] == oldValue ): mc.setKeyframe( root + '.IK', t = keyTimes[i] , v = newValue )
			else: break
	
	#KEY IK -1
	masters   = [ fk[0]      , fk[2]  , fk[1] ]
	ctrls     = [ handleBase , handle , pv    ]
	for i in range(0,len(ctrls)):

		if(ctrls[i] == None ):continue
		objAttrs = [ '{}.{}'.format( ctrls[i] , attr ) for attr in utilsMaya.getManipulableAttr( ctrls[i] ) ]
	
		for objAttr in objAttrs: mc.setKeyframe( objAttr , t=currentFrame-1 )



	#KEY IK ++
	for t in range(0,transitionFrames+1):
		for i in range(0,len(ctrls)):
	
			if(ctrls[i] == None ):continue	
			objAttrs = [ '{}.{}'.format( ctrls[i] , attr ) for attr in utilsMaya.getManipulableAttr( ctrls[i] ) ]
		
			if(0<t):mc.currentTime(currentFrame+t)

			cnsTmp = mc.parentConstraint(masters[i],ctrls[i])
			for objAttr in objAttrs: mc.setKeyframe( objAttr )
			mc.delete(cnsTmp)

	if not(transitionFrames == 0):mc.currentTime(currentFrame)

	return 1


def rigModuleArm_getCtrlsFromSelection():
	selection = mc.ls(sl=True)
	topNode   = rigModuleArm_getTopNodeFromRigElem(selection[0])
	dictCtrls = rigModuleArm_getCtrlsFromTopNode( topNode )
	return dictCtrls

def rigModuleArm_getTopNodeFromRigElem( elem ):
    nbrElemUnderTopNode = 4  
    elemLong = mc.ls( elem , l = True )[0]
    hrcElems = elemLong.split('|')
    for i in range( len(hrcElems)-1 , -1 , -1 ):
        if( 'Top_GRP' in hrcElems[i] ):
            topNode = hrcElems[i]
            topNodeChildrens = mc.listRelatives( topNode , c = True )
            if( len(topNodeChildrens) == nbrElemUnderTopNode ):
                return hrcElems[i]
    
def rigModuleArm_getCtrlsFromTopNode( topNode ):
    dictOut = {}
    topNodeSuffix = 'Top_GRP'
    baseName = topNode[0:len(topNode)-len(topNodeSuffix)]

    #GET CTRLS
    root       = baseName + 'Root_CTRL'
    offset     = baseName + 'Offset_CTRL'
    handle     = baseName + 'Handle_CTRL'
    handleBase = baseName + 'HandleBase_CTRL'
    pv         = baseName + 'Pv_CTRL'

    if(mc.objExists(root      )): dictOut['root'      ] = root
    if(mc.objExists(offset    )): dictOut['offset'    ] = offset
    if(mc.objExists(handle    )): dictOut['handle'    ] = handle
    if(mc.objExists(handleBase)): dictOut['handleBase'] = handleBase
    if(mc.objExists(pv        )): dictOut['pv'        ] = pv

    #GET FK
    topNodeChildrens = mc.listRelatives( topNode , c = True )
    fkChainTopNode = ''
    for child in topNodeChildrens:
    	if( topNodeSuffix in child ):
    		fkChainTopNode = child
    		fkChainBaseName = fkChainTopNode[0:len(fkChainTopNode)-len(topNodeSuffix)]
    		dictOut['fk'] = [ '{}{}{}'.format(fkChainBaseName,i,'_CTRL') for i in range(0,3) ]
    		break

    return dictOut
            
def spaceSwitch_getOffsetAttrs( spaceSwitchObjAttr , suffix = '' ):

	attrs = ['TranslateX','TranslateY','TranslateZ','RotateX','RotateY','RotateZ']
	outAttrs = []
	for i in range(0,99):
		attrTmp = '{}{}{}'.format( spaceSwitchObjAttr , i , attrs[0] ) 
		if( mc.objExists( attrTmp ) ):
			oneMasterAttrs = []
			for attr in attrs:
				attrTmp = '{}{}{}{}'.format( spaceSwitchObjAttr , i , attr , suffix )
				oneMasterAttrs.append(attrTmp)
			outAttrs.append(oneMasterAttrs)
		else:
			break

	return outAttrs

def spaceSwitch_getSlave( spaceSwitchObjAttr ):
	conditionNode    = mc.listConnections( spaceSwitchObjAttr , s = False , d = True , skipConversionNodes = True , type = 'condition' )[0]
	parentConstraint = mc.listConnections( conditionNode + '.outColorR' , s = False , d = True )[0]

	slaveTranslate   = mc.listConnections( parentConstraint + '.constraintTranslateX' , s = False , d = True )
	slaveRotate      = mc.listConnections( parentConstraint + '.constraintRotateX' , s = False , d = True )

	if not(   slaveTranslate == None ) and ( 0 < len(slaveTranslate) ):
		return slaveTranslate[0]
	elif not( slaveRotate    == None ) and ( 0 < len(slaveRotate   ) ):
		return slaveRotate[0]
	else:
		return ''

def spaceSwitch_getSlaveParent( spaceSwitchObjAttr ):	
	slave = spaceSwitch_getSlave( spaceSwitchObjAttr )	
	parents = mc.listRelatives( slave , p = True , f = True )
	if not(   parents == None ) and ( 0 < len(parents) ):
		return parents[0]
	else:
		return ''

def spaceSwitch_getMasters( spaceSwitchObjAttr ):
	conditionNode    = mc.listConnections( spaceSwitchObjAttr , s = False , d = True , skipConversionNodes = True , type = 'condition' )[0]
	parentConstraint = mc.listConnections( conditionNode + '.outColorR' , s = False , d = True )[0]

	masters = []
	for i in range(0,99):
	 	attr = '{}.target[{}].targetParentMatrix'.format(parentConstraint,i)
	 	inConnections = mc.listConnections(  attr , s = True , d = False, type = 'transform'  )
	 	if(inConnections==None):break
	 	else:                   masters += inConnections

	return masters

def rigPuppet_reloadRigSelected( optimize = False ):
	ctrlDriver = 'traj_CTRL'

	#GET CTRL FROM SELECTION	
	selection = mc.ls(sl=True)
	if(len(selection) == 0 ):
		print("rigPuppet_reloadRigSelected: YOU MUST SELECT AN ELEMENT OF A RIG")
		return 0

	ctrl = selection[0]

	#GET NAMESPACE
	if not( ":" in ctrl ):
		print("rigPuppet_reloadRigSelected: THE RIG ELEMENT MUST HAVE A NAMESPACE")
		return 0
	rigNameSpace = ctrl.split(":")[0]

	#GET PATH SCENE	
	pathFile = mc.file( q = True , loc = True )
	if( ( pathFile == 'unknown' ) or (pathFile == None) ):
		print("rigPuppet_reloadRigSelected: CURRENT FILE PATH UNKNOWN --> YOU MUST BE IN A SCENE")
		return 0
	pathFileSplit = pathFile.split('/')
	pathScene     = '/'.join( pathFileSplit[0:len(pathFileSplit)-1] ) + '/'
	pathAnimAttr  = pathScene + rigNameSpace + '_AttrValuesBuffer.xml'
	pathAnimCurve = pathScene + rigNameSpace + '_AnimCurvesBuffer.xml'	

	#GET PATH RIG
	objAttrRigPath = "{}:{}.path".format(rigNameSpace,ctrlDriver)
	if not( mc.objExists(objAttrRigPath) ):
		print("rigPuppet_reloadRigSelected: CANT FIND THE ATTR THAT HOLD THE RIG PATH")
		return 0	
	pathRig = mc.getAttr( objAttrRigPath)

	#RELOAD
	rigPuppet_reloadImportedRig( rigNameSpace , pathRig , pathAnimCurve , pathAnimAttr , optimize = optimize )
	#OPTIMIZE
	rigVisibilityDriver = "{}:{}".format(rigNameSpace,ctrlDriver)
	if(optimize):
		rigPuppet_deleteInvisibleRigAndModel(rigVisibilityDriver, attrsToSkip = ['ctrlVis'])


def rigPuppet_reloadImportedRig( rigNameSpace ,  pathRig , pathAnimCurveFile , pathAnimAttrFile , optimize = False ):

	#SAVE CTRLS INPUT
	ctrls = mc.ls( '{}:*_CTRL'.format(rigNameSpace) , r = True)
	AnimAttribute = animAttribute()
	AnimAttribute.createFromObjs( ctrls )
	AnimAttribute.toFile( pathAnimAttrFile  , clearOldVar = 0 , incr = 0 )

	AnimCurve     = animCurve()
	AnimCurve.createFromObjs( ctrls )
	AnimCurve.toFile( pathAnimCurveFile , clearOldVar = 0 , incr = 0 )
	
	#DELETE RIG
	mc.delete( mc.ls( '{}:*'.format(rigNameSpace) , r = True) )
	mc.namespace( rm = rigNameSpace  )

	#LOAD RIG
	rwi = readWriteInfo.readWriteInfo()
	rwi.mayaScene_load( pathRig , nameSpace = rigNameSpace )

	#LOAD CTRLS INPUT
	AnimAttribute.createFromFile( pathAnimAttrFile , latest = 0 )
	AnimCurve.createFromFile(     pathAnimCurveFile , latest = 0 )
	AnimAttribute.toObjs()
	AnimCurve.toObjs()

def rigPuppet_deleteInvisibleRigAndModel( visibilityDriver , attrsToSkip = ['ctrlVis'] ):
	#DELETE UNWANTED PART OF THE RIG
	attrs = utilsMaya.getManipulableAttr( visibilityDriver , allowTypes = [ 'long' ] )
	for attr in attrs:
		if not( attr in attrsToSkip ):
			objAttr = visibilityDriver + '.' + attr
			if( mc.getAttr(objAttr) == 0 ):
				slaves = mc.listConnections( objAttr  , s = False , d = True )
				mc.delete(slaves)





def rigModuleArm_swithIKFK( rootCtrl ):
	ikAttrName = 'IK'
	objAttr = rootCtrl + '.' + ikAttrName
	value = mc.getAttr(objAttr)
	
	if( value == 0 ):
	    mc.setAttr( objAttr , 1 )
	else:
	    mc.setAttr( objAttr , 0 )

'''
mc.select(rigModuleArm_getRootFromCtrl( mc.ls(sl=True)[0] ))
'''
def rigModuleArm_getRootFromCtrl( ctrlName ):
    ctrlGrp = 'ctrl_hrc'
    topNodeSuffix = 'Top_GRP'
    rootOffsetSuffix = 'Root_OFFSET' 
    
    ctrlNameLong = mc.ls( "*{}".format(ctrlName) , l = True )[0]

    rootCtrl = ''
    dagPath = ''
    for split in ctrlNameLong.split(topNodeSuffix):
    	dagPath += split + topNodeSuffix
    	print(dagPath)
    	if( mc.objExists(dagPath)==0 ):continue
    	ctrlGrpLong = dagPath + '|' + ctrlGrp
    	if( mc.objExists(ctrlGrpLong)==0 ):continue
    	childrens = mc.listRelatives( ctrlGrpLong  , c = True , type = 'transform' )
    	
    	for child in childrens:
    	    #print( rootOffsetSuffix , child[ len(rootOffsetSuffix)*-1 : -1 ] )
    	    if( rootOffsetSuffix == child[ len(rootOffsetSuffix)*-1 :] ):
    	        rootCtrl = mc.listRelatives( child , c = True , type = 'transform' )[0]   
    	

    return rootCtrl





import maya.cmds as mc


def setFrozenInvisible( rigTopNodes = [] ):

	#GET TOP NODES
	if( len(rigTopNodes) == 0 ):
		topNodes = mc.ls( '*Top_GRP' , type = "transform" )
		for top in topNodes:
			parents = mc.listRelatives( top , p = True , f = True)
			if( parents == None ) or ( len(parents) == 0 ):
				rigTopNodes.append( top )

	for top in rigTopNodes:
		grps = mc.listRelatives( top , c = True , f = True )
		for grp in grps:
			if( mc.getAttr( grp + '.v') == 0 ):
				allChildrens = mc.listRelatives( grp , ad = True, f = True )
				for child in allChildrens:
					mc.setAttr( ( child + '.frozen') , 1 ) 
			else:
				allChildrens = mc.listRelatives( grp , ad = True , f = True)
				for child in allChildrens:
					mc.setAttr( ( child + '.frozen') , 1 ) 



def setCurveLineWidth( objs , value = -1 ):
    for elem in objs:
        shapes = mc.listRelatives( elem , s = True , c = True ) 
        for shape in shapes:
            mc.setAttr( shape + '.lineWidth' , value )

'''
import python
from python.utils.utilsRigPuppet import *
reload( python.utils.utilsRigPuppet )
path = 'D:/mcantat_BDD/projects/cute/carrierShipD/maya/scenes/carrierShipD_rig_modelConstraints.xml'

#SAVE
rigPuppet_saveConstraints( path , mc.ls( '*_GEO' , type = 'transform' ) )

#LOAD
rigPuppet_loadConstraints( path )

import maya.cmds as mc
mc.select( mc.ls('*_GEO'))
'''

def rigPuppet_saveConstraints( path , meshes , updateFile = False , debug = False ):

	dictConstraints = {}
	for i in range( 0 , len(meshes)):
		masters = utilsMaya.getConstraintMasters( meshes[i] )
		
		if( debug == True ):print( '{}/{} {} ---> {}'.format( i , len(meshes) , masters , meshes[i] ) )
		
		if( 0 < len(masters) ):
			dictConstraints[meshes[i]] = masters[0]

	ReadWriteInfo = readWriteInfo.readWriteInfo()
	if(updateFile):ReadWriteInfo.createFromFile( path , latest = 1)	
	ReadWriteInfo.dict = dictConstraints			
	ReadWriteInfo.toFile( path , clearOldVar = 1 , incr = 1 )
	if( debug == True ): print('===== Save ===== path: {}'.format(path) )


def rigPuppet_loadConstraints( path , suffix = None , searchReplace = None , debug = False ):
	Names = buildName()

	ReadWriteInfo = readWriteInfo.readWriteInfo()
	ReadWriteInfo.createFromFile( path , latest = 1)				
	dictCns = ReadWriteInfo.dict	

	meshes = dictCns.keys()
	for i in range(len(meshes)):
		master = dictCns[meshes[i]]		
		slave  = meshes[i]

		if not( searchReplace == None ):
			nameDict = Names.decomposeName( slave )
			for j in range(0,len(nameDict['baseSplit'])):
				if( searchReplace[0] == nameDict['baseSplit'][j] ):
					nameDict['baseSplit'][j] = searchReplace[1]
			slave = Names.composeName( nameDict )

		if not( suffix == None ):
			nameDict = Names.decomposeName( slave )
			nameDict['baseSplit'].append(suffix)
			slave = Names.composeName( nameDict )

		#CONSTRAINT
		if( mc.objExists( slave ) )and(mc.objExists(master)):
			utilsMaya.buildConstraint( [ master , slave ] , ['parent','scale'] , 'oneMaster' , 1)

		if( debug == True ):print( '{}/{} {} ---> {}'.format( i , len(meshes) , master , slave ) )

	if( debug == True ): print('===== LOAD ===== path Base: {}'.format(path) )


def rigPuppet_saveSkinning( path , meshes , updateFile = False , debug = False ):
	Skin = skinCluster.skinCluster()
	Skin.createFromObjs(meshes)
	Skin.toFile(path)

	if( debug == True ): print('===== Save ===== path: {}'.format(path) )


def rigPuppet_loadSkinning( path , suffix = None , searchReplace = None , debug = False ):
	Skin = skinCluster.skinCluster()
	Skin.createFromFile(path)

	Names = buildName()

	for i in range( len(Skin.meshs) ):

		mesh = Skin.meshs[i]

		if not( searchReplace == None ):
			nameDict = Names.decomposeName( mesh )
			for j in range(0,len(nameDict['baseSplit'])):
				if( searchReplace[0] == nameDict['baseSplit'][j] ):
					nameDict['baseSplit'][j] = searchReplace[1]
			mesh = Names.composeName( nameDict )

		if not( suffix == None ):
			nameDict = Names.decomposeName( mesh )
			nameDict['baseSplit'].append(suffix)
			mesh = Names.composeName( nameDict )

		#REPLACE
		if( mc.objExists( mesh ) ):
			vtxNbr = mc.polyEvaluate( mesh , v = True )
			if( vtxNbr == Skin.vtxNbr[i] ):
				Skin.meshs[i] = mesh
			

	Skin.toObjs()

	if( debug == True ): print('===== LOAD ===== path Base: {}'.format(path) )



'''

from python.utils.utilsRigPuppet import *
path = 'D:/mcantat_BDD/projects/cute/carrierShipD/maya/scenes/carrierShipD_rig_ctrlShape.ma'
rigPuppet_importAndReplaceCtrlShape( path , adjustPosition = False )
'''

def rigPuppet_importAndReplaceCtrlShape( path , adjustPosition = True , debug = False ):

	nameSpace = 'ctrlShapes'

	if( debug ):
		print('rigPuppet_importAndReplaceCtrlShape___________________________________ START')
		print('IMPORT       : {}'.format( path ))
		print('add namespace: {}'.format( nameSpace ))

	
	rwi = readWriteInfo.readWriteInfo()
	rwi.mayaScene_load( path , nameSpace = nameSpace )

	importCTRLs = mc.ls( (nameSpace + ':*_CTRL') , type = 'transform' )

	if( debug ):
		print('{} CTRLs imported'.format( len(importCTRLs) ))

	for iCtrl in importCTRLs:

		ctrl = iCtrl.split(nameSpace + ':')[1]
		if( mc.objExists(ctrl) ):

			iCtrlShapes = mc.listRelatives( iCtrl , c = True ,  s = True )
			ctrlShapes  = mc.listRelatives( ctrl , c = True , s = True )
			
			if not( ctrlShapes == None ):
				mc.delete(ctrlShapes)

			if not( iCtrlShapes == None ):

				#REPLACE SHAPE
				if( adjustPosition ):
					mc.parent( iCtrlShapes , ctrl , s = True , r = True )
				else:
					mc.parent( iCtrl , ctrl )
					mc.makeIdentity( iCtrl , a = True ,  t = True , r = True , s = True )
					mc.parent( iCtrlShapes , ctrl , s = True , r = True )

				#DELETE	IMPORTED CTRL				
				mc.delete(iCtrl)

				#RENAME SHAPE	
				for iCtrlShape in iCtrlShapes:
					mc.rename( iCtrlShape , iCtrlShape.split(nameSpace + ':')[1] )

				if( debug ):
					print("\t{} REPLACE BY {}".format( ctrl , iCtrl ) )
			else:
				if( debug ):
					print("\t{} existe but no shape on {}".format( ctrl , iCtrl ) )				
		else:
			if( debug ):
				print("\t{} not found".format( ctrl ) )


	importObjsLefted  = mc.ls( (nameSpace + ':*') )
	if( debug ):
		print('{} imported to clean'.format( len(importObjsLefted) ))

	for elem in importObjsLefted:
		if( debug ):
			print("\t{} to delete".format( elem ) )
		try:    mc.delete(elem)
		except: print('cannot delete: {}'.format(elem) )
	
	if( debug ):print('delete namespace: {}'.format( nameSpace ))
	mc.namespace( rm = nameSpace )

	if( debug ):
		print('rigPuppet_importAndReplaceCtrlShape___________________________________ END')




def ctrlRelationShip_convertCoords( dict , source , dest , coordsSource ):
	print('convertCoords: {} -> {}'.format( source , dest ) )
	Coords = coords()
	Coords.createFromCoords(coordsSource)

	values = dict[source]
	print('values' , values )
	for i in range( 0 , len(values) ):

		if not( values[i][0] == dest ) or ( len(values[i]) < 4 ):
			continue

		for j in range( 1,len(values[i]),3):
			dValue = values[i][j+0]
			dType  = values[i][j+1]
			dPivot = values[i][j+2]
			dIter  = 1 
			if( 9 < len(dValue) ):dIter = dValue[9]

			if(   dType == 'mirror'    ):Coords.mirror( convertMirrorInfoToCoords(dValue) )
			elif( dType == 'transform' ):Coords.transform( dValue[0:9] , dPivot , dIter )


	return Coords.coords 

def ctrlRelationShip_copyCtrlCoords( dict , ctrl , ctrlTarget ):
	CurveT = curveShape()
	CurveT.createFromCurve( ctrlTarget , worldSpace = True )

	Curve = curveShape()
	Curve.createFromCurve( ctrl , worldSpace = True )
	Curve.coords = ctrlRelationShip_convertCoords( dict , ctrlTarget , ctrl , CurveT.coords )
	Curve.delete()
	Curve.toObj(ctrl , worldSpace = True)



'''
dictCtrlRelationship = ctrlRelationShip_getDict()
print(dictCtrlRelationship)
objsRelationShip_selectOthers(dictCtrlRelationship)
'''

def getDupliDictModels( debug = False , namespace = None ):
	print('\n\ngetDupliDict______________________________________________________________Models')
	return objsRelationShip_getDict( ["*_GEO","*_LIGHT"] , "transform" ,  "dupliOrig" , 4 , debug = debug , namespace = namespace )

def getDupliDictCtrls( debug = False , namespace = None ):
	print('\n\ngetDupliDict______________________________________________________________Ctrls')
	return objsRelationShip_getDict( ["*_CTRL"] , "transform" ,  "dupliOrig" , 4 , debug = debug , namespace = namespace )

def getDupliDictJoints( debug = False , namespace = None ):
	print('\n\ngetDupliDict______________________________________________________________Joints')
	return objsRelationShip_getDict( ["*_JNT"] , "joint" ,  "dupliOrig" , 4 , debug = debug , namespace = namespace  )

def getDupliDictCtrlJoints( debug = False , namespace = None ):
	print('\n\ngetDupliDict______________________________________________________________CtrlJoints')
	return objsRelationShip_getDict( ["*_JNT"] , "joint" ,  "ctrlInf" , 1 , debug = debug , namespace = namespace )



def objsRelationShip_selectOthers( dict , addSource = False ):
	selection = mc.ls(sl=True)

	newSelection = objsRelationShip_getOthers( dict , selection , addSource )

	mc.select( cl = True)
	for elem in newSelection:
		mc.select(elem , add = True )

def objsRelationShip_getOthers( dict , elements , addSource = False ):

	duplicates = []
	for elem in elements:

		if( addSource ): duplicates.append(elem)
		values = dict.get( elem , [[elem]] )

		for v in values:
			duplicates.append( v[0] )

	return duplicates


'''
def objsRelationShip_getDictDuplicateKeys( dict ):
    
    duplicateKeys = []
    
    for key in dict.keys():
        for values in dict[key]:
            if( 1 < len(values) ):
                strTmp = ''
                for i in range( 2 , len(values) , 3 ):
                    strTmp += '{}'.format(values[i])
                duplicateKeys.append( strTmp )
    
    duplicateKeys = list(set(duplicateKeys))
    return duplicateKeys    


def objsRelationShip_getOthersSameValue( dict , elements , valuesMatch , addSource = False ):

	duplicates = []
	for elem in elements:

		if( addSource ): duplicates.append(elem)
		values = dict.get( elem , [[elem]] )

		for v in values:
			if( 1 < len(v) ):
				valueKey = v[1:]
				if( valueKey in valuesMatch )
					duplicates.append( v[0] )

	return duplicates

'''


def objsRelationShip_getSimilar( dicts , elements , addSource = False ):
	print('_______________objsRelationShip_getSimilar')
	dictSimilar = {}
	for i in range(0,len(dicts)):
		print('+++++ dict num : {}'.format(i))

		for j in range(0,len(elements)):

			values = dicts[i].get( elements[j] , [] )
			print('{} --->[{}]    =   {}'.format(j , elements[j] , values))
	
			for value in values:
				name = value[0]

				transformInfo = ''
				for iv in range( 1 , len(value)):
					transformInfo += '{}'.format(value[iv])
				
				print( '\t create {} --> ++ {}'.format( transformInfo , name ) )
				dictSimilar.setdefault( transformInfo , [] )
				dictSimilar[transformInfo].append(name)
	
	print('_______________objsRelationShip_getSimilar')
	return dictSimilar


def dupliAttr_extractInfoArray( objAttr ):
	infoArray = []

	valueTmp = mc.getAttr( objAttr )
	valueTmpSplit = valueTmp.split(" ")

	bufferTmp = ''
	isArray = 0
	for v in valueTmpSplit:

		if( '[' in v ): isArray = 1
		if( ']' in v ): isArray = 0

		bufferTmp += v

		if( isArray == 0 ):
			if not( bufferTmp in [''] ):infoArray.append(bufferTmp)
			bufferTmp = ''

	#CONVERT ARRAY STR TO ARRAY
	for i in range(0,len(infoArray)):
		if( infoArray[i][0] == '[' ) and ( infoArray[i][-1] == ']' ):
			infoArray[i] = eval( infoArray[i] )

	return infoArray



def objsRelationShip_getDict( objNameSearchs , objType ,  attrInfoName , attrInfoNbrElement , longName = False , debug = False , namespace = None ):
	
	attr = attrInfoName
	infoElemNbr = attrInfoNbrElement
	namespaceStr = ''
	if not( namespace == None ): namespaceStr = namespace + ':' 

	ctrls = []
	for objNameSearch in objNameSearchs:
		ctrls += mc.ls(  namespaceStr + objNameSearch , type = objType , l = longName , r = True)

	if(debug):print( 'objsRelationShip_getDict ================ START objNameSearch: {} objType: {} attrInfoName: {} lenSearch: {}'.format( objNameSearch , objType ,  attrInfoName , len(ctrls)) )

	#SIMPLE FILL
	out = {}
	for ctrl in ctrls:
		if(debug):print( '\t{}'.format(ctrl) )

		if( mc.objExists( ctrl + '.' + attr ) ):

			rawInfo = dupliAttr_extractInfoArray( ctrl + '.' + attr )			

			for i in range( 0 , len(rawInfo) , infoElemNbr ):

				if( infoElemNbr == 1 ):
					ctrlB        = namespaceStr + rawInfo[i+0]
					ctrlA        = ctrl
					if not( ctrlA in out.keys() ): out[ctrlA] = []
					if not( ctrlB in out.keys() ): out[ctrlB] = []
					out[ctrlB].append( [ ctrlA ] ) 
					out[ctrlA].append( [ ctrlB ] )
					continue

				ctrlB        = namespaceStr + rawInfo[i+0]
				dupliBAValue = rawInfo[i+1]
				dupliBAType  = rawInfo[i+2]
				dupliBAPivot = rawInfo[i+3]

				if not(longName) and( '|' in ctrlB ): ctrlB = namespaceStr + ctrlB.split('|')[-1]

				if(type(dupliBAValue[0]) == types.StringType ): 
					Coords = coords()
					Coords.createFromObj(dupliBAValue)
					dupliBAValue = Coords.coords[0:9]
						   		
				if(debug): 
					print( '\t\t------>{}'.format(i) )
					print( '\t\tctrlB        {}'.format(ctrlB       ) )
					print( '\t\tdupliBAValue {}'.format(dupliBAValue) )
					print( '\t\tdupliBAType  {}'.format(dupliBAType ) )
					print( '\t\tdupliBAPivot {}'.format(dupliBAPivot) )
					
				ctrlA        = ctrl

				'''				
				#MAKE THE INVERSE
				

				dupliABValue = rawInfo[i+1]
				dupliABType  = rawInfo[i+2]
				dupliABPivot = rawInfo[i+3]

				if(type(dupliABValue[0]) == types.StringType ): 
					Coords = coords()
					Coords.createFromObj(dupliABValue)
					dupliABValue = Coords.coords[0:9]

				if(debug): 
					print( '\t\tINV------>{}'.format(i) )
					print( '\t\tctrlA        {}'.format(ctrlA       ) )
					print( '\t\tdupliABValue {}'.format(dupliABValue) )
					print( '\t\tdupliABType  {}'.format(dupliABType ) )
					print( '\t\tdupliABPivot {}'.format(dupliABPivot) )

				if not( ctrlA in out.keys() ): out[ctrlA] = []
				if not( ctrlB in out.keys() ): out[ctrlB] = []
				'''		
				if not( ctrlB in out.keys() ): out[ctrlB] = []
				out[ctrlB].append( [ ctrlA , dupliBAValue , dupliBAType  , dupliBAPivot ] )  #<<<<<<<<<<<<<<<< split problem			
				#out[ctrlA].append( [ ctrlB , dupliABValue , dupliABType  , dupliABPivot ] )  #<<<<<<<<<<<<<<<< split problem
	

	out = dictArraySortBySimilarity( out , bothWay = True , addValueAsKey = True , debug = 0 )

	if(debug): print( 'objsRelationShip_getDict ================ END' )

	return out


'''
out = { 'A' : [['B','B']] , 'B' : [['C','C']] , 'C' : [['Z','Z']] , 'D' : [['Y','Y'],['X','X']] , 'E' : [['X','X']] , 'F' : [['B','B']] }    

#dictSorted = dictArraySortBySimilarity( out , bothWay = True , addValueAsKey = True ) 
#RESULT oneWay SAME INPUT ( default )
'A' : [['B'],['C'],['Z']]    
'B' : [['C'],['Z']]  
'C' : [['Z']] 
'D' : [['Y'],['X']]  
'E' : [['X']]
'F' : [['B'],['C'],['Z']]   
#RESULT BOTH WAY SAME INPUT    
'A' : [['B'],['C'],['Z'],['F']]    
'B' : [['C'],['A'],['Z'],['F']]  
'C' : [['Z'],['A'],['B'],['F']] 
'D' : [['Y'],['X'],['E']]  
'E' : [['X'],['Y'],['D']]
'F' : [['B'],['C'],['Z'],['A']]   
#RESULT BOTH WAY ADD INPUT 
'A' : [['B'],['C'],['Z'],['F']]    
'B' : [['C'],['A'],['Z'],['F']]  
'C' : [['Z'],['A'],['B'],['F']] 
'D' : [['Y'],['X'],['E']]  
'E' : [['X'],['Y'],['D']]
'F' : [['B'],['C'],['Z'],['A']]   
'X' : [['Y'],['D'],['E']]    
'Y' : [['D'],['X'],['E']]   
'Z' : [['C'],['A'],['B'],['F']]    
'''






def dictArraySortBySimilarity( dictIn , bothWay = True , addValueAsKey = True , debug = False ):

	dictOut = dictIn

	'''
	MERGE OF KEYS:
	'A' : [['B']]
	'B' : [['C']]
	-------> 'A' : [['B'],['C']]
	'''
	loop = 0
	stop = 0
	while( stop == 0 ):
		stop = 1 

		objs = dictOut.keys()

		for obj in objs:
			targets = [ dictOut[obj][i][0] for i in range(0,len(dictOut[obj])) ]

			for i in range(0,len(dictOut[obj]) ):
				target     = dictOut[obj][i][0]
				targetInfo = dictOut[obj][i][1:]

				if( target in objs ):
					for j in range(0,len(dictOut[target]) ):
						target2     = dictOut[target][j][0]
						target2Info = dictOut[target][j][1:]

						if not( target2 in targets ) and not ( target2 == obj):
							dictOut[obj].append( [target2] +targetInfo + target2Info  )
							targets.append(target2)
							stop = 0

		loop += 1
		if( 700<loop ):mc.error("utilsRigPuppet.dictArraySortBySimilarity - LOOP")
	

	'''
	MERGE OF KEYS INV:
	'A' : [['B']]
	'C' : [['B']]
	-------> 'A' : [['B'],['C']]
	'''


	dictOutInv = {}

	objs = dictOut.keys()

	for obj in objs:

		for i in range(0,len(dictOut[obj]) ):
			target     = dictOut[obj][i][0]
			targetInfo = dictOut[obj][i][1:]
			targetInfoInv = utils_dictArraySortBySimilarity_inverseTransform( dictOut[obj][i] )[1:]


			dictOutInv.setdefault(target,[])
			dictOutInv[target].append( [obj] + targetInfoInv )


	#MERGE DICT
	objs = dictOutInv.keys()

	for obj in objs:
		dictOut.setdefault(obj,[])
		dictOut[obj] += dictOutInv[obj]


	return dictOut	



'''


def dictArraySortBySimilarity( dictIn , bothWay = True , addValueAsKey = True , debug = False ):
	debugKey = 'l_hook0Plug_GEO'
	dictOut = dictIn

	#LIST ALL VALUES IN DICT
	if( addValueAsKey == True ):
		for key in dictOut.keys():
			for value in dictOut[key]:
				name = value[0]
				info = value[1:]
				if not( name in dictOut.keys() ): 
					infoInv = utils_dictArraySortBySimilarity_inverseTransform( [name] + info)
					dictOut[name] = [ [ key ] + infoInv[1:] ]

	print('\n\n')
	print( 'start dict' , dictOut )
	#SORTED
	stop = 0
	nbrElementsLast = 0
	lap    = 0
	lapMax = 1000

	print( '== while start ==' )
	if(debug)and(debugKey in key):print('\n\t==ONE WAY== {}'.format(dictOut[key]) )

	while( stop == 0 ): 
		print( '______________________while lap : ' , lap )

		for key in dictOut.keys():

			if(debug)and(debugKey in key):print('KEY : {}'.format(key) )
			
			values = dictOut[key][:]

			dNames  = [ elem[0]  for elem in dictOut.get( key , [] ) ]
			dInfos  = [ elem[1:] for elem in dictOut.get( key , [] ) ]
			for i in range(0,len(dNames)):
				dNamesB  = [ elem[0]  for elem in dictOut.get( dNames[i] , [] ) ]
				dInfosB  = [ elem[1:] for elem in dictOut.get( dNames[i] , [] ) ]

				for j in range(0,len(dNamesB)):
					if not( key == dNamesB[j] ) and not( dNamesB[j] in dNames ):
						values.append( [ dNamesB[j] ] + dInfos[i] + dInfosB[j] )

			dictOut[key] = utils_dictArraySortBySimilarity_arrayRemoveDuplicate( values )


		if(debug)and(debugKey in dictOut.keys()):print('\n\t==ONE WAY== {}'.format(dictOut[debugKey]) )		

		if( bothWay == True ):
			for key in dictOut.keys():
				if(debug)and(debugKey in key):print('KEY : {}'.format(key) )


				values = dictOut[key][:]

				dNames  = [ elem[0]  for elem in dictOut.get( key , [] ) ]
				dInfos  = [ elem[1:] for elem in dictOut.get( key , [] ) ]

				for i in range(0,len(dNames)):

					for keyB in dictOut.keys():
						if( keyB == key ): continue
						dNamesB  = [ elem[0]  for elem in dictOut.get( keyB , [] ) ]
						dInfosB  = [ elem[1:] for elem in dictOut.get( keyB , [] ) ]
			
						for j in range(0,len(dNamesB)):
							if( dNamesB[j] == dNames[i] ) and not ( keyB in dNames ):
								if(debug)and(debugKey in key):print('KEY to add: {} base on the info of {}  {}'.format( keyB , dNamesB[j] , dInfosB[j] ) )
								#infoInv = utils_dictArraySortBySimilarity_inverseTransform( [dNamesB[j]] + dInfosB[j] )
								values.append( [keyB] + dInfos[i] + dInfosB[j] )



				dictOut[key] = utils_dictArraySortBySimilarity_arrayRemoveDuplicate( values )
			
		if(debug)and(debugKey in dictOut.keys()):print('\n\t==BOTH WAY== {}'.format(dictOut[debugKey]) )	

		nbrElements = 0
		for key in dictOut.keys():
			nbrElements += len( dictOut[key] ) 


		if( nbrElementsLast == nbrElements ) or ( lapMax < lap ):
			stop = 1
		nbrElementsLast = nbrElements
		lap += 1

	print( '== while end ==' )

	return dictOut		
'''

def utils_dictArraySortBySimilarity_inverseTransform( trsfArray ):
	'''
	trsfArray = ['name' , value,'type',pivot , value,'type',pivot , value,'type',pivot ]

	'''

	trsfArrayInv = [trsfArray[0]]
	rangeInv = range( 1 , len(trsfArray) , 3 )
	rangeInv.reverse()

	for i in rangeInv:
		value = trsfArray[i+0][:]
		type  = trsfArray[i+1]
		pivot = trsfArray[i+2][:]

		if( type == 'transform' ):
			# INVERSE VALUE
			valueInv = value[:]

			for j in range( 0 , 6 ):valueInv[j] *= -1
			valueInv[6] = 1 / valueInv[6] 
			valueInv[7] = 1 / valueInv[7] 
			valueInv[8] = 1 / valueInv[8] 


			nbrCopy = 1
			if( 9 < len(valueInv) ):
				nbrCopy = valueInv[9]
			
			if(nbrCopy == 0):
				nbrCopy = 1

			# DECOMPOSE TRS & INVERSE ORDER 
			valueTranslate = [value[0],value[1],value[2],0,0,0,1,1,1]
			valueRotate    = [0,0,0,value[3],value[4],value[5],1,1,1] 
			valueScale     = [0,0,0,0,0,0,value[6],value[7],value[8]]
	
			valueTranslateInv = [valueInv[0],valueInv[1],valueInv[2],0,0,0,1,1,1]
			valueRotateInv    = [0,0,0,valueInv[3],valueInv[4],valueInv[5],1,1,1] 
			valueScaleInv     = [0,0,0,0,0,0,valueInv[6],valueInv[7],valueInv[8]]
	
			
			
			pivotTranslateInvStart = pivot[:]
			pivotRotateInvStart    = pivot[:]
			pivotScaleInvStart     = pivot[:]			
			for k in range(0,3):
				pivotTranslateInvStart[k] += valueTranslate[k]*nbrCopy
				pivotRotateInvStart[k]    += valueTranslate[k]*(nbrCopy-1)


			pivotTranslateInv = pivotTranslateInvStart
			pivotRotateInv    = pivotRotateInvStart   
			pivotScaleInv     = pivotScaleInvStart  

			for j in range(0,nbrCopy):
				trsfArrayInv += [ valueTranslateInv , type , pivotTranslateInv[:] ]
				trsfArrayInv += [ valueRotateInv    , type , pivotRotateInv[:]    ]
				trsfArrayInv += [ valueScaleInv     , type , pivotScaleInv[:]     ]

				for k in range(0,3):
					pivotTranslateInv[k] += valueTranslateInv[k]
					pivotRotateInv[k]    += valueTranslateInv[k]
					pivotScaleInv[k]     += valueTranslateInv[k]



		elif( type == 'mirror' ):
			trsfArrayInv += [ value , type , pivot ]

	return trsfArrayInv



def utils_dictArraySortBySimilarity_arrayRemoveDuplicate( array ):
	'''
	arrayShape = [ ['nameA' , 1 , 2 ] , [ 'nameB' , 1 ] , [ 'nameA' , 999 ] , [ 'nameB' , 00000 ] , ['nameC' , 12345 ] ] 
	utils_dictArraySortBySimilarity_arrayRemoveDuplicate( arrayShape )
	'''

	keys = [ elem[0] for elem in array ]
	keys = list(set(keys))

	newArray = []

	for key in keys:
		for elem in array:
			if( elem[0] == key ):
				newArray.append( elem )
				break

	return newArray
	

'''


for i in uiPuppetCtrlCurveVar.dictCtrlRelationship['r_hookPlugHook1RightB_CTRL'] :
    print('========================================================================')
    print(i[0])
    for j in range(1,len(i),3):
        print('{} {}'.format( i[j+1] , i[j+0] ))
'''


def convertMirrorInfoToCoords(mirror):
	
	planSymCoordsNew = []
	if( type( mirror ) == types.ListType ):
	
		for i in range( 0 , len(mirror) ):
			if( type( mirror[i] ) in [ types.StringType , types.UnicodeType ] )and( mc.objExists(mirror[i]) ):
				Trs = trs()
				Trs.createFromObj(mirror[i])
				planSymCoordsNew += Trs.value[0:3]
			else:
				planSymCoordsNew.append( mirror[i] )
	else:
	
		if( type( mirror )  in [ types.StringType , types.UnicodeType ] )and( mc.objExists(mirror) ):
			#COORDS USE MAYA API Mfn mesh that return the coords in centimeters... use xForm instead
			#Coords = coords()
			#Coords.createFromObj(mirror)
			#planSymCoordsNew = Coords.coords[0:9]
			planSymCoordsNew += mc.xform(mirror + '.vtx[0]', q = True , t = True , ws = True )
			planSymCoordsNew += mc.xform(mirror + '.vtx[1]', q = True , t = True , ws = True )
			planSymCoordsNew += mc.xform(mirror + '.vtx[2]', q = True , t = True , ws = True )
	
	return planSymCoordsNew