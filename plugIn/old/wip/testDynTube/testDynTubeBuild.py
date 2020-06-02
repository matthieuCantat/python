
import maya.cmds as mc


nodeTypeName = 'dynTubeNode'
loadingPath = 'D:/mcantat_BDD/Travail/code/maya/node/python/MAYA NODES MATTHIEU/nodeMatTest/testDynTube/{0}.py'.format( 'dynTubeNode2' )


mc.loadPlugin( loadingPath , qt = True )	
nodeCreated = mc.createNode( nodeTypeName )

leadALocator = mc.spaceLocator( n = 'leadA_loc' )
leadBLocator = mc.spaceLocator( n = 'leadB_loc' )

baseALocator = mc.spaceLocator( n = 'baseA_loc' )
baseBLocator = mc.spaceLocator( n = 'baseB_loc' )
baseGLocator = mc.spaceLocator( n = 'baseG_loc' )


mc.setAttr( leadALocator[0] + '.translateX' , 5  )
mc.setAttr( leadBLocator[0] + '.translateX' , -5  )

mc.setAttr( baseALocator[0] + '.translateX' , 5  )
mc.setAttr( baseBLocator[0] + '.translateX' , -5  )



middleGrp = mc.createNode( 'transform' , n = 'middle_grp' )


mc.connectAttr( leadALocator[0] + '.worldMatrix[0]' , nodeCreated + '.inMatrixA' )
mc.connectAttr( leadBLocator[0] + '.worldMatrix[0]' , nodeCreated + '.inMatrixB' )

mc.connectAttr( baseALocator[0] + '.worldMatrix[0]' , nodeCreated + '.inMatrixBaseA' )
mc.connectAttr( baseBLocator[0] + '.worldMatrix[0]' , nodeCreated + '.inMatrixBaseB' )
mc.connectAttr( baseGLocator[0] + '.worldMatrix[0]' , nodeCreated + '.inMatrixBaseG' )

slaveCube = mc.polyCube( n = 'slave_msh' )

mc.connectAttr( nodeCreated + '.outTranslate' , slaveCube[0] + '.translate' )
mc.connectAttr( nodeCreated + '.outRotate'    , slaveCube[0] + '.rotate'    )
mc.connectAttr( nodeCreated + '.outScale'     , slaveCube[0] + '.scale'     )

mc.connectAttr( 'time1.outTime' , nodeCreated + '.time' )

mc.setAttr( nodeCreated + '.activate'   , 1 )
mc.setAttr( nodeCreated + '.masse'      , 1 )
mc.setAttr( nodeCreated + '.elasticity' , 1 )
mc.setAttr( nodeCreated + '.damping'    , 1 )
mc.setAttr( nodeCreated + '.gravity'    , 1 )
