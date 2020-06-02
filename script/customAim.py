
import maya.cmds as mc
import maya.mel

'''
path   = 'D:\mcantat_BDD\projects\code\maya\c++\mayaNode\\aim\Build\Debug\\aim.mll'
pathGL = 'D:\mcantat_BDD\projects\code\maya\c++\mayaNode\\aimGL\Build\Debug\\aimGL.mll'
buildCustomAim( path , pathGL , 'joint2' , 'locator2' , 'locator3' )
'''
def buildCustomAim( path , pathGL , slave , target , up ):
	
	nodeType  = 'aim'  
	try: mc.loadPlugin( path  )
	except:pass
	newNode = mc.createNode( nodeType ) 
	
	#IN
	mc.connectAttr( slave + '.parentMatrix[0]'      , newNode+'.origParent'               , f = True )
	mc.connectAttr( slave + '.translate'            , newNode+'.origTranslate'            , f = True )
	mc.connectAttr( slave + '.rotatePivotTranslate' , newNode+'.origRotatePivotTranslate' , f = True )
	mc.connectAttr( slave + '.rotatePivot'          , newNode+'.origRotatePivot'          , f = True )
	mc.connectAttr( slave + '.rotateAxis'           , newNode+'.origRotateAxis'           , f = True )
	mc.connectAttr( slave + '.rotateOrder'          , newNode+'.origRotateOrder'          , f = True )
	if( mc.objExists(slave + '.jointOrient') ):
		mc.connectAttr( slave + '.jointOrient'          , newNode+'.origJointOrient'          , f = True )		


	mc.connectAttr( target+'.worldMatrix[0]' , newNode+'.target' , f = True )
	mc.connectAttr( up    +'.worldMatrix[0]' , newNode+'.up'     , f = True )
	
	mc.setAttr( newNode+'.origRotate'          , mc.getAttr(slave + '.rotate' )[0][0], mc.getAttr(slave + '.rotate' )[0][1], mc.getAttr(slave + '.rotate' )[0][2] , type = "double3"   )
	
	#OUT
	mc.connectAttr( newNode+'.outRotation' , slave + '.rotate'  , f = True )
	
	print('===DONE AIM===')

	nodeType  = 'aimGL'  
	try: mc.loadPlugin( pathGL  )
	except:pass
	newNodeGL = mc.createNode( nodeType ) 	

	visTrigGeo = mc.polyCube( n = 'drawTrigger' )[0]

	mc.connectAttr( slave  + '.worldMatrix[0]'  , '{}.orig'.format( newNodeGL )  )
	mc.connectAttr( target + '.worldMatrix[0]'  , '{}.target'.format( newNodeGL )  )
	mc.connectAttr( up     + '.worldMatrix[0]'  , '{}.up'.format( newNodeGL )  )
	

	mc.connectAttr( '{}.aimAxe'.format( newNode )       , '{}.aimAxe'.format( newNodeGL )        )
	mc.connectAttr( '{}.upAxe'.format( newNode )        , '{}.upAxe'.format( newNodeGL )        )
	mc.connectAttr( '{}.upAxeTarget'.format( newNode )  , '{}.upAxeTarget'.format( newNodeGL )  )
	mc.connectAttr( '{}.offset'.format( newNode )       , '{}.offset'.format( newNodeGL )       )	

	mc.connectAttr( ( newNodeGL + '.outTrig' ) , ( visTrigGeo + '.visibility' ) )
	
	maya.mel.eval("setRendererInModelPanel base_OpenGL_Renderer modelPanel4");

	print('===DONE GL===')

	return 1


