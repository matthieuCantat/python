
import maya.cmds as mc

nodeTypeNames = [ 'dynamicTrsNode_testEval' , 'dynamicRotationLimitesNode_testEval' ]
nodeTypeName = nodeTypeNames[0]


loadingPath = 'C:/Users/Matthieu/Desktop/Travail/code/maya/node/python/nodeMatTest/testEval/{0}.py'.format( nodeTypeName )
mc.loadPlugin( loadingPath , qt = True )	
nodeCreated = mc.createNode( nodeTypeName )



leadLocator = mc.spaceLocator( n = 'lead_loc')

mc.connectAttr( leadLocator[0] + '.translate' , nodeCreated + '.inTranslate' )
mc.connectAttr( leadLocator[0] + '.rotate'    , nodeCreated + '.inRotate'    )
mc.connectAttr( leadLocator[0] + '.scale'     , nodeCreated + '.inScale'     )

slaveCube = mc.polyCube( n = 'slave_msh' )

mc.connectAttr( nodeCreated + '.outTranslate' , slaveCube[0] + '.translate' )
mc.connectAttr( nodeCreated + '.outRotate'    , slaveCube[0] + '.rotate'    )
mc.connectAttr( nodeCreated + '.outScale'     , slaveCube[0] + '.scale'     )


