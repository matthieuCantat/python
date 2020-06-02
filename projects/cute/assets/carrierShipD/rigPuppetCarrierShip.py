
'''





##########################################
############### RIG PUPPET ###############
##########################################



#INIT
import maya.cmds as mc
import python
import python.classe.readWriteInfo as readWriteInfo
import python.utils.utilsRigPuppet as utilsRigPuppet
import python.utils.utilsMaya      as utilsMaya
import python.utils.utilsPython    as utilsPython

from    python.projects.cute.assets.carrierShipD.rigPuppetCarrierShip import *
reload( python.projects.cute.assets.carrierShipD.rigPuppetCarrierShip          )
reload( python.projects.cute.assets.carrierShipD.rigPuppetCarrierShip_damp     )
reload( python.projects.cute.assets.carrierShipD.rigPuppetCarrierShip_reactor  )
reload( python.projects.cute.assets.carrierShipD.rigPuppetCarrierShip_propulsor)
reload( python.projects.cute.assets.carrierShipD.rigPuppetCarrierShip_hook     )

reload(python.classe.readWriteInfo)
reload(python.utils.utilsRigPuppet)
reload(python.utils.utilsMaya )
reload(python.utils.utilsPython )

rwi = readWriteInfo.readWriteInfo()

pathRigBoundB   = 'D:/mcantat_BDD/projects/cute/assets/carrierShipD/maya/scenes/carrierShipD_rigBoundB.ma'
pathCtrlShape   = 'D:/mcantat_BDD/projects/cute/assets/carrierShipD/maya/scenes/carrierShipD_utils_ctrlShape.ma'
pathRigPuppet   = 'D:/mcantat_BDD/projects/cute/assets/carrierShipD/maya/scenes/carrierShipD_rigPuppet.ma'


driver = 'traj_CTRL'

####################################################################
rwi.mayaScene_load( pathRigBoundB , open = True  )
####################################################################



#BUILD
puppet = rigPuppetCarrierShip()	
puppet.debug = 1
toExec = puppet.build()
exec(toExec)


utilsRigPuppet.rigPuppet_importAndReplaceCtrlShape( pathCtrlShape , adjustPosition = False )
#utilsRigPuppet.rigPuppet_saveCtrls( pathCtrlShape )


#PREPARE VISIBILITY GRP
dampGrp   = 'damp_GRP'
dampElems = mc.ls( "rigPuppet_GRP|*damp*" , type = "transform" )
mc.createNode('transform' , n = dampGrp , p = 'rigPuppet_GRP')
mc.parent( dampElems , dampGrp )

blockGrp = 'block_GRP'
mc.createNode('transform' , n = blockGrp , p = 'rigPuppet_GRP')

otherGrp = 'other_GRP'
mc.createNode('transform' , n = otherGrp , p = 'rigPuppet_GRP')

#ADD GEO TO VISIBILITY GRP
geos = mc.ls( "*_GEO",type = "transform" )
rigPuppetsGrps = mc.ls( "rigPuppet_GRP|*_GRP",type = "transform" )
grpsToSkip = ['all_GRP','tubes_GRP','tubesStraight_GRP']

for geo in geos:
	doParent = 0
	for grp in rigPuppetsGrps:
		if not( grp in grpsToSkip ):
			bodyName = grp.split('_GRP')[0]
			if( bodyName in geo ):
				mc.parent( geo , grp )
				doParent = 1
	if(doParent==0):
		mc.parent( geo , otherGrp )
        
#ADD RIG TO VISIBILITY GRP
ctrls = mc.ls('|rigPuppet_GRP|*_OFFSET')

driverBaseName = driver.split('_CTRL')[0]
for ctrl in ctrls:
    if not( driverBaseName in ctrl ):
        mc.parent( ctrl , otherGrp )


#SPLIT VISIBILITY GRP
grps = [ 'r_hook0_GRP' , 'r_hook1_GRP' , 'l_hook0_GRP' , 'l_hook1_GRP' ]

dictSplitTitleToMembers = {}
dictSplitTitleToMembers['in']  = []
dictSplitTitleToMembers['out']  = ['Cover','Piston','Holder','Middle','Offset','Support','Fix']
dictSplitTitleToMembers['tube'] = ['Tube']

utilsRigPuppet.splitGrpsMembers( grps , dictSplitTitleToMembers )


grps = [ 'r_reac_GRP' , 'l_reac_GRP']

dictSplitTitleToMembers = {}
dictSplitTitleToMembers['in']  = ['reactorArm','Core','Piston','Out','Air','Compressor','BurnPanel','Fire','ArmPropulsor']
dictSplitTitleToMembers['out']  = []
dictSplitTitleToMembers['tube'] = ['Tube']

utilsRigPuppet.splitGrpsMembers( grps , dictSplitTitleToMembers )




#COMBINE AND CONVERT TO SKIN
grps = mc.ls('rigPuppet_GRP|*_GRP' , type = "transform" )
geosToSkip = ['Tube','Ray' , 'Fire']
combinedMesh = ''
for grp in grps:
    meshes = utilsMaya.getMeshesFromGrps( [grp] )
    print(grp)
    meshesToCombine = []
    for mesh in meshes:
        doCombine = 1
        for geoToSkip in geosToSkip:
            if( geoToSkip in mesh ):
                doCombine = 0
                
        if( doCombine ):
            meshesToCombine.append(mesh)
       
    if( len(meshesToCombine) == 1  ):
    	combinedMesh = meshes[0]
    	utilsMaya.safeParent(combinedMesh,grp)
    elif( 1 < len(meshesToCombine) ):
    	combinedMesh = utilsRigPuppet.rigPuppet_combineMesh(  meshesToCombine , grp.split('_GRP')[0] + '_GEO' )
    	utilsMaya.safeParent(combinedMesh,grp)

		



    
def sortStringArrayWithRefs( array , listOrderRef ):
	arraySorted = []
	for orderRef in listOrderRef:
		for i in range(0,len(array)):
			if( orderRef in array[i] ) and not( array[i] in arraySorted ):
				arraySorted.append(array[i])

	for i in range(0,len(array)):
		if not( array[i] in arraySorted ):
			arraySorted.append(array[i])

	return arraySorted

#createSwitchVisibility
attr = utilsMaya.addSpecialAttr( driver , 'ctrlVis'  , 'int+' , 20 , attrKeyable = False , attrCb  = True , attrLock  =  False )
mc.connectAttr( attr ,'rigPuppet_GRP.ctrlVis')

grps = mc.ls('rigPuppet_GRP|*_GRP' , type = "transform" )
listOrderRef = ['r_reac','l_reac','r_hook','l_hook','r_propulsor','l_propulsor','damp']
grps = utilsPython.sortStringArrayWithRefs( grps , listOrderRef )

for grp in grps:
    meshes = utilsMaya.getMeshesFromGrps( [grp] )
    if( len(meshes) == 0 ):
        mc.setAttr( grp + '.visibility' , 0 )
        continue
    baseName = grp.split('_GRP')[0]
    attr = utilsMaya.addSpecialAttr( driver , baseName  , 'intOnOff' , 1 , attrKeyable = False , attrCb  = True , attrLock  =  False )
    mc.connectAttr( attr , grp + '.v')



#SET ATTR
mc.setAttr( driver + ".block" , 0 )
mc.setAttr( "pos0_JNT.v" , 0 )







#CONNECT STRAIGTHEN TUBE
ctrlDrivers = mc.ls( "*Hang*_CTRL" , type = "transform" )

for i in range(0,len(ctrlDrivers)):
    ctrlDriver = ctrlDrivers[i]
    jointDriver = ctrlDriver.split("_CTRL")[0] + "0_JNT"
    mc.connectAttr( ctrlDriver + '.straighten' , jointDriver + '.straighten'  )

	    
for tubeStraightGeo in mc.ls( "*TubeStraight*_GEO" , type = "transform" ):
	mc.setAttr( tubeStraightGeo + '.visibility' , 0 )	



#CONNECT LIGHT
attr = '.lightVisibility'
mc.connectAttr( 'dampGiro_CTRL'+attr , 'dampGiro0_JNT'+attr )
for side in ['r','l']:

	mc.connectAttr( '{}_propulsorFire_CTRL{}'.format(side,attr)   , '{}_propulsorFire0_JNT{}'.format(side,attr) )
	mc.connectAttr( '{}_reacFire_CTRL{}'.format(side,attr)        , '{}_reacFire0_JNT{}'.format(side,attr) )

	mc.connectAttr( '{}_reacGiro_CTRL{}'.format(side,attr)        , '{}_reacGiro0_JNT{}'.format(side,attr) )
	mc.connectAttr( '{}_propulsorGiro_CTRL{}'.format(side,attr)   , '{}_propulsorGiro0_JNT{}'.format(side,attr) )
	mc.connectAttr( '{}_hook0GiroCover_CTRL{}'.format(side,attr)  , '{}_hook0GiroCover0_JNT{}'.format(side,attr) )
	mc.connectAttr( '{}_hook1GiroCover_CTRL{}'.format(side,attr)  , '{}_hook1GiroCover0_JNT{}'.format(side,attr) )

	for letter in ['A','B','C','D','E','F']:
		mc.connectAttr( '{}_projector{}_CTRL{}'.format(side,letter,attr), '{}_projector{}0_JNT{}'.format(side,letter,attr) )
	
	for letter in ['A','B','C','D','E']:
		mc.connectAttr( '{}_giro{}_CTRL{}'.format(side,letter,attr), '{}_giro{}0_JNT{}'.format(side,letter,attr) )


#ADD PATH ATTR
pathSave = 'D:/mcantat_BDD/projects/cute/assets/carrierShipD/maya/scenes/carrierShipD_rigPuppet.ma'
utilsMaya.addSpecialAttr( driver , 'path'  , 'string' , pathSave , attrKeyable = False , attrCb  = True , attrLock  =  False )



#CLEAN ROOT 
toKeep = ['rigPuppet_GRP']
rootElem = mc.ls("|*" , type = "transform")

init   = ['front','persp','side','top']
for elem in rootElem:
	if not (elem in toKeep ) and not ( elem in init ):
		mc.delete(elem)




####################################################################
rwi.mayaScene_save( pathRigPuppet )
####################################################################








'''








import maya.cmds as mc

from .....classe.rigPuppet import *  
from .....classe.rigCtrl import *  
from .....classe.rigModuleChain import *     
from .....classe.rigModuleArm import *    
from .....classe.rigModulePiston import *  
from .....classe.rigModuleProjector import *
from .....classe.rigModuleRotatingBeacon import *

from .rigPuppetCarrierShip_reactor import *  
from .rigPuppetCarrierShip_hook import *   
from .rigPuppetCarrierShip_propulsor import *  
from .rigPuppetCarrierShip_damp import * 




class rigPuppetCarrierShip(rigPuppet):

	def __init__( self , **args ):
		rigPuppet.__init__( self , **args )
		#UTILS	
		#CLASSE
		self.classeType   = 'rigPuppetCarrierShip'
		self.doTubes      = args.get( 'tubes'      , True )
		self.doProjectors = args.get( 'projectors' , True )
		self.doGiros      = args.get( 'giros'      , True )
		#NAME
		self.Name.add( 'carrier' , baseName = self.classeType    , type = 'GRP' )			
		#INSTANCE_______________________________BLUEPRINT
		posLocs         = ['pos0_JNT' ]
		trajLocs        = ['traj0_JNT']
		bodyLocs        = ['body0_JNT']
		reactorsLocs    = ['reactors0_JNT']
		hooksPlugsLocs  = ['hooksPlugs0_JNT']
		projsFrontLocs  = ['projsFront0_JNT']
		projsCenterLocs  = ['projsCenter0_JNT']
		
		dampBaseLocs          = [x.encode('UTF8') for x in mc.ls('dampBase??_JNT'       , type = 'joint' )]
		dampContactLocs       = ['dampContact0_JNT']
		dampLocs              = ['damp0_JNT']
		dampClosePanelALocs   = ['dampClosePanelA0_JNT']
		dampClosePanelBLocs   = ['dampClosePanelB0_JNT']

		dampGiroLocs          = ['dampGiro0_JNT']
		giroLocs              = [x.encode('UTF8') for x in mc.ls('r_giro?0_JNT'       , type = 'transform' )]		
		projLocs              = [x.encode('UTF8') for x in mc.ls('r_projector?0_JNT'    , type = 'transform' )]


		mirrorPlane            = [0,0,0 , 0,1,0 , 0,0,1 ]
		translateInfo          = [0,0, -0.823 , 0, -28.847,0 , 1,1,1 ]
		sideHookDuplicateTrs   = []

		#CLASSE BLUE PRINT
		self.Name.add( 'pos'               , baseName = 'pos'           )
		self.Name.add( 'traj'              , baseName = 'traj'          )	
		self.Name.add( 'body'              , baseName = 'body'          )
		self.Name.add( 'reactors'          , baseName = 'reactors'      )
		self.Name.add( 'hooksPlugs'        , baseName = 'hooksPlugs'    )
		self.Name.add( 'projsCenter'       , baseName = 'projsCenter'   )
		self.Name.add( 'projsFront'        , baseName = 'projsFront'    )
		self.Name.add( 'reactor'           , baseName = 'reactor'       )
		self.Name.add( 'hook'              , baseName = 'hook'          )
		self.Name.add( 'propulsor'         , baseName = 'propulsor'     )
		self.Name.add( 'damp'              , baseName = 'damp'          )
		self.Name.add( 'rootB'             , baseName = 'damp'          )
		self.Name.add( 'coverSlide'        , baseName = 'damp'          )	
		self.Name.add( 'projector'         , baseName = 'projector'     )	
		self.Name.add( 'giro'              , baseName = 'giro'          )		
		self.Name.add( 'dampContact'       , ref = self.Name.damp , baseNameAppend = 'Contact'   )
		self.Name.add( 'dampBaseA'         , ref = self.Name.damp , baseNameAppend = 'BaseA'     )
		self.Name.add( 'dampBaseB'         , ref = self.Name.damp , baseNameAppend = 'BaseB'     )
		self.Name.add( 'dampBaseC'         , ref = self.Name.damp , baseNameAppend = 'BaseC'     )
		self.Name.add( 'dampGiro'          , ref = self.Name.damp , baseNameAppend = 'giro'      )
		self.Name.add( 'dampClosePanelA'   , ref = self.Name.damp , baseNameAppend = 'closePanelA' )
		self.Name.add( 'dampClosePanelB'   , ref = self.Name.damp , baseNameAppend = 'closePanelB' )

		self.Name.add( 'projector'  , baseName = 'projector' )
		self.Name.add( 'projectorA' , ref = self.Name.projector , baseNameAppend = 'A' )
		self.Name.add( 'projectorB' , ref = self.Name.projector , baseNameAppend = 'B' )
		self.Name.add( 'projectorC' , ref = self.Name.projector , baseNameAppend = 'C' )
		self.Name.add( 'projectorD' , ref = self.Name.projector , baseNameAppend = 'D' )
		self.Name.add( 'projectorE' , ref = self.Name.projector , baseNameAppend = 'E' )
		self.Name.add( 'projectorF' , ref = self.Name.projector , baseNameAppend = 'F' )

		self.Name.add( 'giro'       , baseName = 'giro' )	
		self.Name.add( 'giroA' , ref = self.Name.giro , baseNameAppend = 'A' )	
		self.Name.add( 'giroB' , ref = self.Name.giro , baseNameAppend = 'B' )	
		self.Name.add( 'giroC' , ref = self.Name.giro , baseNameAppend = 'C' )	
		self.Name.add( 'giroD' , ref = self.Name.giro , baseNameAppend = 'D' )	
		self.Name.add( 'giroE' , ref = self.Name.giro , baseNameAppend = 'E' )		


		#MAIN CTRLS
		print('MAIN CTRLS')
		self.Position    = rigCtrl(  n = self.Name.pos         , pos = posLocs                     , form = 'plane'       , colors = ['green']  , ctrlVisPriority = 0 , parent = self.Name.topNode ) 			
		self.Traj        = rigCtrl(  n = self.Name.traj        , pos = trajLocs                    , form = 'crossArrow'  , colors = ['yellow'] , ctrlVisPriority = 1 , parent = self.Name.topNode , attrStates = [['t','r']] )
		self.Body        = rigCtrl(  n = self.Name.body        , pos = bodyLocs                    , form = 'crossArrow'  , colors = ['green']  , ctrlVisPriority = 1 , parent = self.Name.topNode , attrStates = [['t','r']] )
		self.Reactors    = rigCtrl(  n = self.Name.reactors    , pos = reactorsLocs                , form = 'crossArrow'  , colors = ['green']  , ctrlVisPriority = 2 , parent = self.Name.topNode , attrStates = [['t','r']] )
		self.HooksPlugs  = rigCtrl(  n = self.Name.hooksPlugs  , pos = hooksPlugsLocs              , form = 'crossArrow'  , colors = ['green']  , ctrlVisPriority = 2 , parent = self.Name.topNode , attrStates = [['t','r']] )
		self.ProjsCenter = rigCtrl(  n = self.Name.projsCenter , pos = projsCenterLocs             , form = 'crossArrow'  , colors = ['yellow'] , ctrlVisPriority = 3 , parent = self.Name.topNode , attrStates = [['t','r']] )
		self.ProjsFront  = rigCtrl(  n = self.Name.projsFront  , pos = projsFrontLocs              , form = 'crossArrow'  , colors = ['yellow'] , ctrlVisPriority = 3 , parent = self.Name.topNode , attrStates = [['t','r']] )
		self.SubRigs     += [ self.Position , self.Traj , self.Body , self.Reactors , self.HooksPlugs , self.ProjsCenter , self.ProjsFront  ]		
		self.SubRigsName += [    'Posistion'    , 'Traj'    , 'Body'    , 'Reactors'    , 'HooksPlugs'    , 'ProjsCenter'    , 'ProjsFront'  ]	

		#DAMP CTRLS
		print('DAMP CTRLS')
		self.DampRoot    = rigCtrl(  n = self.Name.damp        , pos = dampLocs          , form = 'crossArrow'      , colors = ['green'] , ctrlVisPriority = 4 , parent = self.Name.topNode , attrStates = [['t','r']] )
		self.DampContact = rigCtrl(  n = self.Name.dampContact , pos = dampContactLocs   , form = 'crossArrow'      , colors = ['green'] , ctrlVisPriority = 4 , parent = self.Name.topNode , attrStates = [['t','r']] )
		self.DampBaseA   = rigCtrl(  n = self.Name.dampBaseA   , pos = [dampBaseLocs[0]] , form = 'crossArrow'      , colors = ['green'] , ctrlVisPriority = 4 , parent = self.Name.topNode )
		self.DampBaseB   = rigCtrl(  n = self.Name.dampBaseB   , pos = [dampBaseLocs[1]] , form = 'crossArrow'      , colors = ['green'] , ctrlVisPriority = 4 , parent = self.Name.topNode )
		self.DampBaseC   = rigCtrl(  n = self.Name.dampBaseC   , pos = [dampBaseLocs[2]] , form = 'crossArrow'      , colors = ['green'] , ctrlVisPriority = 4 , parent = self.Name.topNode , attrStates = [['t','r']] )
		self.DampGiro    = rigCtrl(  n = self.Name.dampGiro    , pos = dampGiroLocs      , form = 'arrow2SidesBend' , colors = ['red']   , ctrlVisPriority = 6 , parent = self.Name.topNode , attrStates = [['rz']] )
		self.DampClosePanelA = rigCtrl(  n = self.Name.dampClosePanelA , pos = dampClosePanelALocs  , form = 'arrow2Sides' , colors = ['red'] , ctrlVisPriority = 4 , parent = self.Name.topNode , attrStates = [['t','r']] )
		self.DampClosePanelB = rigCtrl(  n = self.Name.dampClosePanelB , pos = dampClosePanelBLocs  , form = 'arrow2Sides'  , colors = ['red'] , ctrlVisPriority = 4 , parent = self.Name.topNode , attrStates = [['t','r']] )
		self.SubRigs     += [ self.DampRoot , self.DampContact , self.DampBaseA , self.DampBaseB , self.DampBaseC , self.DampGiro  , self.DampClosePanelA , self.DampClosePanelB ]		
		self.SubRigsName += [ 'DampRoot'    , 'DampContact'    , 'DampBaseA'    , 'DampBaseB'    , 'DampBaseC'    ,     'DampGiro' ,     'DampClosePanelA',     'DampClosePanelB']	

		#PROJECTOR CTRLS
		self.ProjectorA = rigCtrl( n = self.Name.projectorA , pos = [projLocs[0]]  , form = 'arrow2SidesBend' , colors = ['red']   , ctrlVisPriority = 6 , parent = self.Name.topNode , attrStates = [['rz']] )
		self.ProjectorB = rigCtrl( n = self.Name.projectorB , pos = [projLocs[1]]  , form = 'arrow2SidesBend' , colors = ['red']   , ctrlVisPriority = 6 , parent = self.Name.topNode , attrStates = [['rz']] )
		self.ProjectorC = rigCtrl( n = self.Name.projectorC , pos = [projLocs[2]]  , form = 'arrow2SidesBend' , colors = ['red']   , ctrlVisPriority = 6 , parent = self.Name.topNode , attrStates = [['rz']] )	
		self.ProjectorD = rigCtrl( n = self.Name.projectorD , pos = [projLocs[3]]  , form = 'arrow2SidesBend' , colors = ['red']   , ctrlVisPriority = 6 , parent = self.Name.topNode , attrStates = [['rz']] )	
		self.ProjectorE = rigCtrl( n = self.Name.projectorE , pos = [projLocs[4]]  , form = 'arrow2SidesBend' , colors = ['red']   , ctrlVisPriority = 6 , parent = self.Name.topNode , attrStates = [['rz']] )
		self.ProjectorF = rigCtrl( n = self.Name.projectorF , pos = [projLocs[5]]  , form = 'arrow2SidesBend' , colors = ['red']   , ctrlVisPriority = 6 , parent = self.Name.topNode , attrStates = [['rz']] )
		
		#GIRO CTRLS
		self.GiroA = rigCtrl( n = self.Name.giroA , pos = [giroLocs[0]]  , form = 'arrow2SidesBend' , colors = ['red']   , ctrlVisPriority = 6 , parent = self.Name.topNode , attrStates = [['rz']] )
		self.GiroB = rigCtrl( n = self.Name.giroB , pos = [giroLocs[1]]  , form = 'arrow2SidesBend' , colors = ['red']   , ctrlVisPriority = 6 , parent = self.Name.topNode , attrStates = [['rz']] )
		self.GiroC = rigCtrl( n = self.Name.giroC , pos = [giroLocs[2]]  , form = 'arrow2SidesBend' , colors = ['red']   , ctrlVisPriority = 6 , parent = self.Name.topNode , attrStates = [['rz']] )	
		self.GiroD = rigCtrl( n = self.Name.giroD , pos = [giroLocs[3]]  , form = 'arrow2SidesBend' , colors = ['red']   , ctrlVisPriority = 6 , parent = self.Name.topNode , attrStates = [['rz']] )	
		self.GiroE = rigCtrl( n = self.Name.giroE , pos = [giroLocs[4]]  , form = 'arrow2SidesBend' , colors = ['red']   , ctrlVisPriority = 6 , parent = self.Name.topNode , attrStates = [['rz']] )


		#SUBRIG
		self.Reactor   = rigPuppetCarrierShip_reactor(   n = self.Name.reactor   , ctrlVisPriority = 1 , tubes = self.doTubes )
		self.Hook      = rigPuppetCarrierShip_hook(      n = self.Name.hook      , ctrlVisPriority = 1 , tubes = self.doTubes )
		self.Propulsor = rigPuppetCarrierShip_propulsor( n = self.Name.propulsor , ctrlVisPriority = 1 , tubes = self.doTubes )
		self.Damp      = rigPuppetCarrierShip_damp(      n = self.Name.damp      , ctrlVisPriority = 1 , tubes = self.doTubes )

		argsTransformHook = {}
		argsTransformHook['value']             = translateInfo
		argsTransformHook['mode']              = 'transform'
		argsTransformHook['pivot']             = [0,0,0 , 0,0,0 , 1,1,1]
		argsTransformHook['namePrefix']        = []
		argsTransformHook['nameReplace']       = []
		argsTransformHook['nameIncr']          = 'hook0'
		argsTransformHook['nameAdd']           = []
		argsTransformHook['noneMirrorAxe']     = 4
		argsTransformHook['debug']             = self.debug

		self.HookFront , self.HookBack    = self.Hook.duplicate( **argsTransformHook )


		argsMirrorZ = {}
		argsMirrorZ['value']             = 'symPlane_damp1'
		argsMirrorZ['mode']              = 'mirror'
		argsMirrorZ['pivot']             = [0,0,0 , 0,0,0 , 1,1,1]
		argsMirrorZ['namePrefix']        = []
		argsMirrorZ['nameReplace']       = []
		argsMirrorZ['nameIncr']          = 'damp0'
		argsMirrorZ['nameAdd']           = []
		argsMirrorZ['noneMirrorAxe']     = 4
		argsMirrorZ['debug']             = self.debug

		self.DampFront , self.DampBack  = self.Damp.duplicate( **argsMirrorZ )

		argsMirrorX = {}
		argsMirrorX['value']             = [0,0,0 , 0,1,0 , 0,0,1]
		argsMirrorX['mode']              = 'mirror'
		argsMirrorX['pivot']             = [0,0,0 , 0,0,0 , 1,1,1]
		argsMirrorX['namePrefix']        = ['r','l']
		argsMirrorX['nameReplace']       = []
		argsMirrorX['nameIncr']          = ''
		argsMirrorX['nameAdd']           = []
		argsMirrorX['noneMirrorAxe']     = 4
		argsMirrorX['debug'] = self.debug
		
		rigsToDuplicate = []
		rigsToDuplicate.append( self.Reactor    )
		rigsToDuplicate.append( self.HookFront  )
		rigsToDuplicate.append( self.HookBack   )
		rigsToDuplicate.append( self.Propulsor  )
		rigsToDuplicate.append( self.DampFront  )
		rigsToDuplicate.append( self.DampBack   )

		rigsToDuplicate.append( self.ProjectorA   )
		rigsToDuplicate.append( self.ProjectorB   )
		rigsToDuplicate.append( self.ProjectorC   )
		rigsToDuplicate.append( self.ProjectorD   )
		rigsToDuplicate.append( self.ProjectorE   )
		rigsToDuplicate.append( self.ProjectorF   )

		rigsToDuplicate.append( self.GiroA   )
		rigsToDuplicate.append( self.GiroB   )
		rigsToDuplicate.append( self.GiroC   )
		rigsToDuplicate.append( self.GiroD   )
		rigsToDuplicate.append( self.GiroE   )

		print('duplicateRigs IN')
		duplicated = self.duplicateRigs( argsMirrorX , rigsToDuplicate )
		print('duplicateRigs OUT')

		self.ReactorR   , self.ReactorL   = duplicated[0][0] , duplicated[0][1]
		self.HookFrontR , self.HookFrontL = duplicated[1][0] , duplicated[1][1]
		self.HookBackR  , self.HookBackL  = duplicated[2][0] , duplicated[2][1]
		self.PropulsorR , self.PropulsorL = duplicated[3][0] , duplicated[3][1]
		self.DampFrontR , self.DampFrontL = duplicated[4][0] , duplicated[4][1]
		self.DampBackR  , self.DampBackL  = duplicated[5][0] , duplicated[5][1]

		self.ProjectorAR  , self.ProjectorAL  = duplicated[6][0]  , duplicated[6][1] 
		self.ProjectorBR  , self.ProjectorBL  = duplicated[7][0]  , duplicated[7][1] 		
		self.ProjectorCR  , self.ProjectorCL  = duplicated[8][0]  , duplicated[8][1] 
		self.ProjectorDR  , self.ProjectorDL  = duplicated[9][0]  , duplicated[9][1] 
		self.ProjectorER  , self.ProjectorEL  = duplicated[10][0] , duplicated[10][1]
		self.ProjectorFR  , self.ProjectorFL  = duplicated[11][0] , duplicated[11][1]

		self.GiroAR  , self.GiroAL = duplicated[12][0]  , duplicated[12][1]
		self.GiroBR  , self.GiroBL = duplicated[13][0]  , duplicated[13][1]
		self.GiroCR  , self.GiroCL = duplicated[14][0]  , duplicated[14][1]
		self.GiroDR  , self.GiroDL = duplicated[15][0]  , duplicated[15][1]
		self.GiroER  , self.GiroEL = duplicated[16][0]  , duplicated[16][1]

		self.SubRigs += [ self.ReactorL   , self.ReactorR   ]
		self.SubRigs += [ self.HookFrontL , self.HookFrontR ]
		self.SubRigs += [ self.HookBackL  , self.HookBackR  ]
		self.SubRigs += [ self.PropulsorL , self.PropulsorR ]
		self.SubRigs += [ self.DampFrontR , self.DampFrontL ]
		self.SubRigs += [ self.DampBackR  , self.DampBackL  ]		

		self.SubRigs += [ self.ProjectorAR  , self.ProjectorAL  ]	
		self.SubRigs += [ self.ProjectorBR  , self.ProjectorBL  ]			
		self.SubRigs += [ self.ProjectorCR  , self.ProjectorCL  ]	
		self.SubRigs += [ self.ProjectorDR  , self.ProjectorDL  ]
		self.SubRigs += [ self.ProjectorER  , self.ProjectorEL  ]				
		self.SubRigs += [ self.ProjectorFR  , self.ProjectorFL  ]

		self.SubRigs += [ self.GiroAR  , self.GiroAL ]
		self.SubRigs += [ self.GiroBR  , self.GiroBL ]
		self.SubRigs += [ self.GiroCR  , self.GiroCL ]
		self.SubRigs += [ self.GiroDR  , self.GiroDL ]
		self.SubRigs += [ self.GiroER  , self.GiroEL ]		

		self.SubRigsName += [ 'ReactorL'    , 'ReactorR'   ]
		self.SubRigsName += [ 'HookFrontL'  , 'HookFrontR' ]
		self.SubRigsName += [ 'HookBackL'   , 'HookBackR'  ]
		self.SubRigsName += [ 'PropulsorL'  , 'PropulsorR' ]
		self.SubRigsName += [ 'DampFrontR'  , 'DampFrontL' ]
		self.SubRigsName += [ 'DampBackR'   , 'DampBackL'  ]

		self.SubRigsName += [ 'ProjectorAR'  , 'ProjectorAL'  ]	
		self.SubRigsName += [ 'ProjectorBR'  , 'ProjectorBL'  ]			
		self.SubRigsName += [ 'ProjectorCR'  , 'ProjectorCL'  ]	
		self.SubRigsName += [ 'ProjectorDR'  , 'ProjectorDL'  ]
		self.SubRigsName += [ 'ProjectorER'  , 'ProjectorEL'  ]				
		self.SubRigsName += [ 'ProjectorFR'  , 'ProjectorFL'  ]

		self.SubRigsName += [ 'GiroAR'  , 'GiroAL' ]
		self.SubRigsName += [ 'GiroBR'  , 'GiroBL' ]
		self.SubRigsName += [ 'GiroCR'  , 'GiroCL' ]
		self.SubRigsName += [ 'GiroDR'  , 'GiroDL' ]
		self.SubRigsName += [ 'GiroER'  , 'GiroEL' ]	


		self.Attr.add( "DampGiro" , Name = self.DampGiro.Name.ctrl , attrName = ["lightVisibility"] , attrType = ["intOnOff"] , attrValue = [1] )
		for side in ['R','L']:
			for letter in ['A','B','C','D','E','F']:
				exec( 'self.Attr.add( "Projector{0}{1}" , Name = self.Projector{0}{1}.Name.ctrl , attrName = ["lightVisibility"] , attrType = ["intOnOff"] , attrValue = [1] )'.format(letter,side) )	
			
			for letter in ['A','B','C','D','E']:
				exec( 'self.Attr.add( "Giro{0}{1}" , Name = self.Giro{0}{1}.Name.ctrl , attrName = ["lightVisibility"] , attrType = ["intOnOff"] , attrValue = [1] )'.format(letter,side) )	



		self.Link.add( 'paHooksPlugs' , Sources = [ self.HooksPlugs.outs[0] ]  , Destinations = [ self.HookFrontL.ins[1] , self.HookFrontR.ins[1] , self.HookBackL.ins[1]  , self.HookBackR.ins[1]  ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )
		self.Link.add( 'paReactors'   , Sources = [ self.Reactors.outs[0]   ]  , Destinations = [ self.ReactorL.ins[1]   , self.ReactorR.ins[1]   , self.PropulsorL.ins[0] , self.PropulsorR.ins[0] ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )				

		self.Link.add( 'dampA'        , Sources = [ self.DampBaseA.outs[0]   ] , Destinations = [ self.DampFrontL.CtrlPiston.ins[0] , self.DampFrontR.CtrlPiston.ins[0] , self.DampBackL.CtrlPiston.ins[0] , self.DampBackR.CtrlPiston.ins[0] ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )
		self.Link.add( 'dampB'        , Sources = [ self.DampBaseB.outs[0]   ] , Destinations = [ self.DampFrontL.Arm.ins[0]       , self.DampFrontR.Arm.ins[0]       , self.DampBackL.Arm.ins[0]       , self.DampBackR.Arm.ins[0]       ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )
		self.Link.add( 'dampContact'  , Sources = [ self.DampContact.outs[0] ] , Destinations = [ self.DampFrontL.Arm.ins[1]       , self.DampFrontR.Arm.ins[1]       , self.DampBackL.Arm.ins[1]       , self.DampBackR.Arm.ins[1]       ] , type = 'parent' , operation = 'oneMaster' , maintainOffset = 1 )
		self.Link.add( 'dampC'        , Sources = [ self.DampContact.outs[0] ] , Destinations = [ self.DampBaseC.ins[0]   ] , type = 'parentSpace'  , spaceDriver = self.DampBaseC.Name.ctrl , spaceAttr = 'parentSpace' , spaceNames = ['followContact'] , spaceValue = 0 )
		

		#CLASSE UTILS

		#UPDATE
		name = args.get( 'n'   , None )	
		pos  = args.get( 'pos' , None )
		if not( name == None ): self.Name.add( 'base' , copy = name ) 
		if not( pos  == None ): pass


	def postBuild( self ):
		'''
		setupSwitchVisibilityModel( 'ALL_grp' , 'rigPuppetRoot_CTRL' , lods = ['low' , 'block' ] )

		attrNames = ['bodyCtrl'           , 'r_reactorCtrl'      ,'l_reactorCtrl'      ,  'r_hook0Ctrl'      , 'r_hook1Ctrl'      , 'l_hook0Ctrl'      , 'l_hook1Ctrl'    ]
		topNodes  = [['rigPuppetTop_GRP'] , ['r_reactorTop_GRP'] ,['l_reactorTop_GRP'] ,  ['r_hook0Top_GRP'] , ['r_hook1Top_GRP'] , ['l_hook0Top_GRP'] , ['l_hook1Top_GRP'] ]
		
		attrNames += [ 'l_propulsorCtrl'      , 'r_propulsorCtrl'      , 'dampCtrl']
		topNodes  += [ ['l_propulsorTop_GRP'] , ['r_propulsorTop_GRP'] , ['r_damp0Top_GRP' , 'r_damp1Top_GRP' , 'l_damp0Top_GRP' , 'l_damp1Top_GRP'] ]
		
		for i in range( 0 , len(attrNames) ):
			attr = self.Attr.utils_mayaAddSpecialAttr( 'rigPuppetRoot_CTRL' , attrNames[i] , 'int+' , 10 )
			for topNode in topNodes[i]:
				mc.connectAttr( attr , topNode + '.ctrlVis' )

		'''
		return ""