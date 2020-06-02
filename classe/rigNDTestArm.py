'''

#******************************************************** BUILD EXEMPLE RIG CTRL
import maya.cmds as mc
import python
from python.classe.rigModuleArm import *
reload(python.classe.rigModuleArm)

#_________________________________BUILD

position = ['l_shoulder_bind','l_elbow_bind','l_wrist_bind']

armA = rigModuleArm( n = 'arm' , pos = position , fk = True , ik = True , pv = True ,offset = True  )    
toExec = armA.build()
exec(toExec)


#_________________________________BUILD

manipA = rigCtrl( n = 'clavile' , pos = ['locator1'] , form = 'circle' , colors = [17] )
	
toExec = manipA.build()
exec(toExec)


manipA = rigCtrl( n = 'root' , pos = ['spinea_bind'] , form = 'crossArrow' , colors = [17] )
	
toExec = manipA.build()
exec(toExec)



#******************************************************** BUILD EXEMPLE RIG CTRL
import maya.cmds as mc
import python
from python.classe.rigStretchyJoint import *
reload( python.classe.rigStretchyJoint)


#_________________________________BUILD
sjA = rigStretchyJoint( n = 'scapula' , pos = [ 'scapulaStretchy1','scapulaStretchy2' ]  , aim = True  )
exec(sjA.build())


#_________________________________BUILD
sjA = rigStretchyJoint( n = 'pecA' , pos = [ 'pectoralStretchy1','pectoralStretchy2' ]  , aim = True  )
exec(sjA.build())


#_________________________________BUILD
sjA = rigStretchyJoint( n = 'pecB' , pos = [ 'pectoralStretchy3','pectoralStretchy4' ]  , aim = True  )
exec(sjA.build())


#_________________________________BUILD
sjA = rigStretchyJoint( n = 'pecC' , pos = [ 'pectoralStretchy5','pectoralStretchy6' ]  , aim = True  )
exec(sjA.build())


#_________________________________BUILD
sjA = rigStretchyJoint( n = 'trap' , pos = [ 'trapStretchy1','trapStretchy2' ]  , aim = True  )
exec(sjA.build())


#_________________________________BUILD
sjA = rigStretchyJoint( n = 'trapBack' , pos = [ 'trapStretchy3','trapStretchy4' ]  , aim = True  )
exec(sjA.build())




#_________________________________BUILD
sjA = rigStretchyJoint( n = 'dorsal' , pos = [ 'dorsalStretchy1','dorsalStretchy2' ]  , aim = True  )
exec(sjA.build())


#_________________________________BUILD
sjA = rigStretchyJoint( n = 'deltoid' , pos = [ 'deltoidStretchy1','deltoidStretchy2' ]  , aim = True  )
exec(sjA.build())


#_________________________________BUILD
sjA = rigStretchyJoint( n = 'deltoidFront' , pos = [ 'deltoidStretchy3','deltoidStretchy4' ]  , aim = True  )
exec(sjA.build())


#_________________________________BUILD
sjA = rigStretchyJoint( n = 'deltoidBack' , pos = [ 'deltoidStretchy5','deltoidStretchy6' ]  , aim = True  )
exec(sjA.build())


#_________________________________BUILD
sjA = rigStretchyJoint( n = 'triceps' , pos = [ 'triceps1','triceps2' ]  , aim = True  )
exec(sjA.build())


#_________________________________BUILD
sjA = rigStretchyJoint( n = 'biceps' , pos = [ 'biceps1','biceps2' ]  , aim = True  )
exec(sjA.build())



#_________________________________BUILD
sjA = rigStretchyJoint( n = 'fingerExtend' , pos = [ 'fingerExtend1','fingerExtend2' ]  , aim = True  )
exec(sjA.build())


#_________________________________BUILD
sjA = rigStretchyJoint( n = 'fingerCompr' , pos = [ 'fingerCompr1','fingerCompr2' ]  , aim = True  )
exec(sjA.build())


#_________________________________BUILD
sjA = rigStretchyJoint( n = 'dorsalB' , pos = [ 'dorsalStretchy5','dorsalStretchy6' ]  , aim = True  )
exec(sjA.build())



#_________________________________BUILD
sjA = rigStretchyJoint( n = 'tricepsInv' , pos = [ 'triceps2','triceps1' ]  , aim = True  )
exec(sjA.build())


#_________________________________BUILD
sjA = rigStretchyJoint( n = 'bicepsInv' , pos = [ 'biceps2','biceps1' ]  , aim = True  )
exec(sjA.build())


#_________________________________BUILD
sjA = rigStretchyJoint( n = 'fingerExtendInv' , pos = [ 'fingerExtend2','fingerExtend1' ]  , aim = True  )
exec(sjA.build())


#_________________________________BUILD
sjA = rigStretchyJoint( n = 'fingerComprInv' , pos = [ 'fingerCompr2','fingerCompr1' ]  , aim = True  )
exec(sjA.build())



#_________________________________BUILD
sjA = rigStretchyJoint( n = 'backA' , pos = [ 'backStretchy1','backStretchy2' ]  , aim = True  )
exec(sjA.build())


#_________________________________BUILD
sjA = rigStretchyJoint( n = 'backB' , pos = [ 'backStretchy3','backStretchy4' ]  , aim = True  )
exec(sjA.build())


#_________________________________BUILD
sjA = rigStretchyJoint( n = 'backC' , pos = [ 'backStretchy5','backStretchy6' ]  , aim = True  )
exec(sjA.build())



#### CLEAN TRANSPHERE CNS TO PARENT
import maya.cmds as mc
import python.utils.utilsMaya as utilsMaya

obj = mc.ls(sl=True)[0]
master = utilsMaya.getConstraintMasters( obj , constraintTypesFilter = [ 'parentConstraint' ] , deleteConstraint = 1 )
father = mc.listRelatives( obj , p = True )[0]

mc.parent( obj , w = True )
mc.delete( mc.parentConstraint( obj , father  ) )
mc.parent( obj ,father )
mc.parentConstraint( master , father , mo = True  )
#### CLEAN TRANSPHERE CNS TO PARENT



#rebindWithIncrMesh( 'base_male_body' )

def rebindWithIncrMesh( skinnedMeshBaseName ):
	skinnedMesh = mc.ls( skinnedMeshBaseName + "*" , type = "transform" )[-1]
	shape = mc.listRelatives( skinnedMesh , c = True , s = True )[0]
	skinClusterNode = mc.listConnections( shape + '.inMesh' , s = True , d = False )[0]
	joints = mc.listConnections( skinClusterNode + '.matrix' , s = True , d = False , type = 'joint' )
	
	mc.setAttr( skinClusterNode + '.envelope' , 0 )
	newMesh = mc.duplicate( skinnedMesh )[0]
	mc.select( joints )
	mc.skinCluster( joints,  newMesh , toSelectedBones = True )
	mc.copySkinWeights( skinnedMesh , newMesh , noMirror = True , surfaceAssociation = 'closestPoint' , influenceAssociation  = 'closestJoint' )   
	mc.setAttr( skinnedMesh + '.visibility' , 0 )



import maya.cmds as mc
from python.utils.utilsMaya import *

name = 'toto'
jointToCompare = 'joint2'
axeToMeasure = 0 
createPoseDeformer( name , jointToCompare , axeToMeasure )



'''