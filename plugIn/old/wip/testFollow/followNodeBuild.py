
import maya.cmds as mc


nodeTypeName = 'followNode'
loadingPath = 'C:/Users/Matthieu/Desktop/Travail/code/maya/node/python/MAYA NODES MATTHIEU/nodeMatTest/testFollow/{0}.py'.format( nodeTypeName )
mc.loadPlugin( loadingPath , qt = True )	
nodeCreated = mc.createNode( nodeTypeName )

'''

leadALocator = mc.spaceLocator( n = 'leadA_loc' )
leadBLocator = mc.spaceLocator( n = 'leadB_loc' )
leadGLocator = mc.spaceLocator( n = 'leadG_loc' )


mc.setAttr( leadALocator[0] + '.translateX' , 5  )
mc.setAttr( leadBLocator[0] + '.translateX' , -5  )

middleGrp = mc.createNode( 'transform' , n = 'middle_grp' )
mc.parent( leadGLocator[0] , middleGrp )
mc.parentConstraint( leadALocator[0] , leadBLocator[0] ,  middleGrp )
mc.setAttr( leadGLocator[0] + '.translateY' , 3)


mc.connectAttr( leadALocator[0] + '.worldMatrix[0]' , nodeCreated + '.inMatrixA' )
mc.connectAttr( leadBLocator[0] + '.worldMatrix[0]' , nodeCreated + '.inMatrixB' )
mc.connectAttr( leadGLocator[0] + '.matrix' , nodeCreated + '.inMatrixG' )

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

'''