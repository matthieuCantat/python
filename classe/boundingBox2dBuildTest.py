#IMPORT
import python.classe.boundingBox2d
reload( python.classe.boundingBox2d )
#CLASS DECLARATION
bb = python.classe.boundingBox2d.boundingBox2d()
bbCanvas = python.classe.boundingBox2d.boundingBox2d()
bbBlock = python.classe.boundingBox2d.boundingBox2d()
bbCanvas.createFromObj('canvas')
bbBlock.createFromObj('block')
bb.createFromObj('bb', bbOrigineIndex = 2 )
#GROW
bb.grow( 0.5 , [bbBlock] , [bbCanvas] )
#INFO
bb.visualize('toto')


bbBlock.visualize('toto')

bbCanvas.printAttrs('canvas')
bbBlock.printAttrs('block')
bb.printAttrs('bb')




import maya.cmds as mc
#IMPORT
import python.classe.boundingBox2d
import python.classe.layout2dGenerator
reload( python.classe.boundingBox2d )
reload( python.classe.layout2dGenerator )
#CLASS DECLARATION
layout = python.classe.layout2dGenerator.layout2dGenerator()
layout.createCanvasFromObjs(['canvas'])
layout.createBlockFromObjs(['block' , 'bb'])
#GROW
createdBBs = layout.fillFreeSpaceWithBB()









import maya.cmds as mc
#IMPORT
import python.classe.boundingBox2d
import python.classe.layout2dGenerator
reload( python.classe.boundingBox2d )
reload( python.classe.layout2dGenerator )
#CLASS DECLARATION
layout = python.classe.layout2dGenerator.layout2dGenerator()
layout.createCanvasFromObjs(['canvas'])
layout.createBlockFromObjs(['block' , 'block1' ])
layout.createPicturesFromObjs(['picture' , 'picture1' , 'picture2' , 'picture3' , 'picture4' ])
#GROW
createdBBs = layout.setBbsOnFreeSpace( layout.pictures )

    
for bb in createdBBs:
    bb.visualize('toto')



