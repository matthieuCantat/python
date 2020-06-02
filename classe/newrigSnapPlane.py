
import maya.cmds as mc
import maya.api.OpenMaya as ompy

from ..utils import utilsMath
from ..utils import utilsPython
from ..utils import utilsMaya
from ..utils import utilsMayaApi
from ..utils import utilsBin

from . import buildRigClass
from . import buildRigClassChainDyn

from . import trsClass


class rigSnapPlane( rigModule ):
    
    '''
    ________________________ TO MODIF   
    __init__
    refreshNamesWithBaseName
    fillAttrFromUI
    fillAttrManualy
    createSubRig
    createRig
    fillAttrFromRig
    ________________________ STRUCTURE  
    createFromSelection
    createManualy
    createSubRigMirror
    createMirror
    changeBaseName
    getMainGrp
    isElem
    saveWriteMainGrpAttr
    readMainGrpAttr
    writeBeaconsAttr
    readBeaconAttr
    '''
    
    
    def __init__( self ):
    
        '''
        # MAIN GRP ATTR
        self.insAttr          = 'ins'       
        self.ctrlsAttr        = 'ctrls' 
        self.outsAttr         = 'outs'
        self.beaconsAttr      = 'beacons'       
        self.allsAttr         = 'alls'
        self.subMainGrpsAttr  = 'subMainGrps'

        self.rigTypeAttr      = 'rigType'   
        self.buildTrsAttr     = 'buildTrs'

        # BEACONS GRP ATTR
        self.mainGrpAttr      = 'mainGrp'   
        
        # CLASSES INFO
        self.dico_rigType_classImport = { 'manip':'from . import manipClass' , 'pistonRig':'from . import pistonRigClass' , 'tubeRig':'from . import tubeRigClass' , 'armRig':'from . import armRigClass' , 'slideCircleRig':'from . import slideCircleRigClass'    }       
        self.dico_rigType_classBuild  = { 'manip':'manipClass.manip()'       , 'pistonRig':'pistonRigClass.pistonRig()'   , 'tubeRig':'tubeRigClass.tubeRig()'     , 'armRig':'armRigClass.armRig()'      , 'slideCircleRig':'slideCircleRigClass.slideCircleRig()' }       
        
        # EMPTY VAR         
        self.subRigObjs         = []
        '''
        
        #________________________________________TO MODIF <------------------------ START
        
        buildRigClass.buildRig.__init__(self)           
        '''     
          ------>fill this attr and add others                
        '''             
        
        self.rigType            = 'snapPlane'
        self.baseName           = 'snapPlaneRig'    
        
        self.mainGrpSuffix      = '_snapPlaneRig_grp'          
        self.subRigSuffix       = [ 'LeadA' , 'LeadB' , 'LeadC' , 'LeadD' , 'Slave' ] 
  
        self.buildTrs           = [ [0,0,0,0,0,0,1,1,1] , [0,0,0,0,0,0,1,1,1] , [0,0,0,0,0,0,1,1,1] , [0,0,0,0,0,0,1,1,1]  , [0,0,0,0,0,0,1,1,1]  ]
        self.buildTrsDupli      = [ [-1,1,0,0,0,0,0.5,0.5,0.5] , [1,1,0,0,0,0,0.5,0.5,0.5] , [1,-1,0,0,0,0,0.5,0.5,0.5] , [-1,-1,0,0,0,0,0.5,0.5,0.5]  , [0,0,0,0,0,0,1,1,1]  ]
        
        
        self.nodeType = 'snapPlaneNode'             
        #mc.loadPlugin( 'C:/Users/Matthieu/Desktop/Travail/code/maya/node/python/{0}.py'.format(self.nodeType) , qt = True )
        self.nodeName =  self.baseName + '_' + self.nodeType 
    
        self.outLoc = ''
        # ATTR
        
        self.dynIn  = 0
        self.dynOut = 0     
        
        self.trsCollisionPlane = [0,5,0,0,0,-90,5,5,5]    
                
        #________________________________________TO MODIF <------------------------ END
 

    #___________________________________________________________________________________________________________________________________________________________________ refreshNamesWithBaseName
    
    def refreshNamesWithBaseName(self): 
        '''
        # main Hierarchy        
        self.mainGrp       = self.baseName + self.mainGrpSuffix
        self.manipGrp      = self.baseName + '_manips_grp' 
        self.rigGrp        = self.baseName + '_rig_grp' 
            
        #baseName subRig
        self.subRigBaseNames = []
        for suffix in self.subRigSuffix:
            self.subRigBaseNames.append( self.baseName + suffix )   
        '''
        
        #________________________________________TO MODIF <------------------------ START   
        
        buildRigClass.buildRig.refreshNamesWithBaseName(self)
        
        '''     
            ------> add some attrs which depend on baseName             
        ''' 
        self.nodeName        = self.baseName + '_' + self.nodeType
        self.outLoc          = self.baseName + 'Slave_loc'
        self.collisionPlane  =   self.baseName + 'CollisionPlane_nbrs'        
        
        #________________________________________TO MODIF <------------------------ END     
        


    #___________________________________________________________________________________________________________________________________________________________________ fillAttrFromUI 
    
    def fillAttrFromUI( self , uiClass ):
        #________________________________________TO MODIF <------------------------ START   
        
        buildRigClass.buildRig.fillAttrFromUI( self , uiClass ) 
        
        '''     
            ------> add some attrs if you using an UI           
        ''' 
        
        # ...................................
        # ...................................               
        # ...................................
        
        #________________________________________TO MODIF <------------------------ END 
        

    #___________________________________________________________________________________________________________________________________________________________________ fillAttrManualy    
    
    def fillAttrManualy( self , baseName , buildTrs , isSubRig = None , buildTrsDupli = None ):
        '''
        self.baseName  = baseName
        self.refreshNamesWithBaseName()
        self.buildTrs = buildTrs 
        '''
        #________________________________________TO MODIF <------------------------ START   
        
        buildRigClass.buildRig.fillAttrManualy( self , baseName , buildTrs , isSubRig , buildTrsDupli ) 
        
        '''     
            make calcule for filling attribute      
        ''' 



        
        #________________________________________TO MODIF <------------------------ END 
        
    
#___________________________________________________________________________________________________________________________________________________________________ createManualy  
    
    def createSubRig( self ):
        #________________________________________TO MODIF <------------------------ START       
        
        buildRigClass.buildRig.createSubRig( self )
        
        '''  
             create all the subRig you want here , subRig is a classRig 
            
            you have:            
                self.subRigBaseNames  -------> the base name of all subRig you want to create
                self.subRigObjs = []      <--- a remplir avec l'obj de chaque rigs !!
        
        '''
        self.subRigObjs = []
        
        trsObj = trsClass.trsClass()
        
        for i in range( 0 , len( self.buildTrs ) ):
            
            buildTrsOffset = trsObj.offsetItself( [1,0,0,0,0,0,0,0,0] , inTrsValue = self.buildTrs[i]  )
                        
            chainDynObj = buildRigClassChainDyn.chainDyn()
            chainDynObj.fillAttrManualy( self.subRigBaseNames[i] , [ self.buildTrs[i] , buildTrsOffset  ] , isSubRig = 1 , buildTrsDupli = [ self.buildTrsDupli[i] ] , dynMode = 'values' )     
            chainDynObj.createManualy()
            self.subRigObjs.append( chainDynObj )           
            
        

        
        #________________________________________TO MODIF <------------------------ END 
        
        
    #___________________________________________________________________________________________________________________________________________________________________ createRig  

    def createRig( self ):
        #________________________________________TO MODIF <------------------------ START   

        buildRigClass.buildRig.createRig( self )
        
        '''  
             build the rig  a partir des subRig deja cree 
             
            you have:
                self.mainGrp   
                self.manipGrp  
                self.rigGrp                     
                self.subRigObjs  -------> the obj of all subRig  
                self.buildTrs -------> world trsValue of selection
         
             self.alls = []    # a remplir avec chaque element cree dans createRig!!!!! 
         
        ''' 
        self.alls = [] #<------ a remplir
        trsObj = trsClass.trsClass()        
        
        chainDynObjs = self.subRigObjs

        # BASE HIERARCHY    
        hierarchyNames   = [ self.mainGrp , self.manipGrp , self.rigGrp  ]  
        hierarchyTypes   = [ 'transform'  , 'transform'   , 'transform'  ]
        hierarchyFathers = [ ''           , self.mainGrp  , self.mainGrp ]
        utilsMaya.createDagNodes( hierarchyTypes  , hierarchyNames , hierarchyFathers )
        self.alls += hierarchyNames         
    
        # PARENT SUBRIG
        for i in range( 0 , len( chainDynObjs ) ):      
            mc.parent( chainDynObjs[i].mainGrp   , self.manipGrp )         
        
        # SLAVE LOC
        mc.spaceLocator(  n = self.outLoc )
        mc.parent( self.outLoc , self.rigGrp )
        mc.setAttr( self.outLoc + '.visibility' , 0 )
        
        self.alls += [self.outLoc]
        
        # COLLISION PLANE
        
        mc.nurbsPlane( n = self.collisionPlane , p = [0,0,0] , ax = [1,0,0] , w = 1 , lr = 1 , d = 1 , u = 1 , v = 1 , ch = 1  )
        trsObj.toObj( self.collisionPlane , inTrsValue = self.trsCollisionPlane )
        mc.parent( self.collisionPlane , self.rigGrp )
        utilsMaya.buildConstraint( [ self.collisionPlane , chainDynObjs[0].collisionPlane , chainDynObjs[1].collisionPlane , chainDynObjs[2].collisionPlane  , chainDynObjs[3].collisionPlane , chainDynObjs[4].collisionPlane  ] , [ 'parent' ] , 'oneMaster' , 0 )        
        self.alls += [self.collisionPlane]            
        # NODE CONNECTION
        
        mc.createNode( self.nodeType , n = self.nodeName )

        mc.connectAttr( self.nodeName + '.outTranslate' , self.outLoc + '.translate' )
        mc.connectAttr( self.nodeName + '.outRotate'    , self.outLoc + '.rotate'    )
        
        mc.connectAttr(  chainDynObjs[0].outs[0] + '.worldMatrix[0]' , self.nodeName + '.worldMatrixA' )
        mc.connectAttr(  chainDynObjs[1].outs[0] + '.worldMatrix[0]' , self.nodeName + '.worldMatrixB' )
        mc.connectAttr(  chainDynObjs[2].outs[0] + '.worldMatrix[0]' , self.nodeName + '.worldMatrixC' )
        mc.connectAttr(  chainDynObjs[3].outs[0] + '.worldMatrix[0]' , self.nodeName + '.worldMatrixD' )
        
        
        self.alls += [self.nodeName]                                               
        # OTHER
        mc.refresh()
        mc.dgdirty(self.nodeName)
        
        utilsMaya.buildConstraint( [ self.outLoc , chainDynObjs[4].ins[0] ] , [ 'parent' ] , 'oneMaster' , 1 )
        
        


        #____WRITE BUILD INFO                                           
        buildTrs    = self.buildTrs
        ins         = [ chainDynObjs[0].ins[0] , chainDynObjs[1].ins[0] , chainDynObjs[2].ins[0]  , chainDynObjs[3].ins[0] ]
        ctrls       = [ obj.ctrls[0] for obj in chainDynObjs ]
        outs        = [ chainDynObjs[4].outs[0] ]
        subMainGrps = [ rigObj.mainGrp for rigObj in self.subRigObjs ]
        beacons     = subMainGrps 
        
        self.saveWriteMainGrpAttr(  self.mainGrp , self.rigType , buildTrs , ins , ctrls , outs , beacons , self.alls , subMainGrps )
        self.writeBeaconsAttr()                 



        #________________________________________TO MODIF <------------------------ END 


        
    #___________________________________________________________________________________________________________________________________________________________________ fillAttrFromRig    
    
    def fillAttrFromRig( self , rigGrpName , masterRig = 1 ):

        '''
        # get the main Grp
        self.getMainGrp(rigGrpName , masterRig  )
        
        # get the other attr
        self.readMainGrpAttr( self.mainGrp )    
        
        # get the baseName
        self.baseName = self.mainGrp.split( self.mainGrpSuffix )[0]     
        
        self.fillAttrManualy( self.baseName , self.buildTrs )
        '''
        
        buildRigClass.buildRig.fillAttrFromRig( self , rigGrpName , masterRig )

    #___________________________________________________________________________________________________________________________________________________________________ createFromSelectionOptionBox   
    
    def createFromSelectionOptionBox( self ):


        #self.optionBoxNames   = [ 'dynIn'        , 'dynOut'      ]
        #self.optionBoxAttrs   = [ 'self.dynIn'   , 'self.dynOut' ]      
        #self.optionBoxTypes   = [ 'checkBox'     , 'checkBox'    ]          

        buildRigClass.buildRig.createFromSelectionOptionBox( self )                         
    #___________________________________________________________________________________________________________________________________________________________________ createFromSelection    
    
    def createFromSelection( self ):
        
        '''
        selection = mc.ls( sl = True )  
    
        for i in range( 0 , len( selection ) , len( self.buildTrs ) ):
            
            
            #____on verifie si on a suffisement d'element pour cree le rig
            try:
                for j in range( 0 , len(self.buildTrs) ):
                    toto = selection[i+j]
            except:
                break
            
                
            #____on rassemble les infos
            baseName = selection[i]
            buildTrs = []
            for j in range( 0 , len( self.buildTrs ) ):             
                buildTrs.append( utilsMaya.getWorldTrsValue( selection[i+j] ) )     
            
            #____build
            self.fillAttrManualy(  baseName , buildTrs  )
            self.createManualy()
        '''
        
        buildRigClass.buildRig.createFromSelection( self )          
            
    #___________________________________________________________________________________________________________________________________________________________________ createManualy  
    
    def createManualy( self ):
        '''
        self.createSubRig()
        self.createRig()        
        '''         
        buildRigClass.buildRig.createManualy( self )


    #___________________________________________________________________________________________________________________________________________________________________ createSubRigMirror         

    def createSubRigMirror( self , planSymCoords , lockAxe , inverseAxes ,  prefix , replace  ):
        '''
        self.subRigObjs = []            
        rigObj          = None      
        subMainGrps     = self.subMainGrps
        
        for rigGrp in self.subMainGrps:
            
            rigType = mc.getAttr( rigGrp + '.' + self.rigTypeAttr )

            exec( '{0}'.format(          self.dico_rigType_classImport[ rigType ]  ) )          
            exec( 'rigObj = {0}'.format( self.dico_rigType_classBuild[  rigType ]  ) )
            
            rigObj.fillAttrFromRig( rigGrp , masterRig = 0  )
            rigObj.createMirror( planSymCoords , inverseAxes ,  prefix , replace )
            self.subRigObjs.append( rigObj )
        '''
        buildRigClass.buildRig.createSubRigMirror( self , planSymCoords , lockAxe , inverseAxes ,  prefix , replace  )
        
    #___________________________________________________________________________________________________________________________________________________________________ createMirror   
    
    def createMirror( self , planSymCoords , lockAxe , inverseAxes ,  prefix , replace  ):    
        '''
        self.createSubRigMirror( planSymCoords , inverseAxes ,  prefix , replace )  
                
        oldBaseName = self.baseName     
        
        # OLD NAME
        self.changeBaseName( prefix[0] + self.baseName , incr = 0   , renameSubRig = 0)
        
        # NEW NAME
        self.baseName = oldBaseName 
        if( replace[0] in self.baseName ) and not( replace[0] == '' ):      
            splitTmp      = self.baseName.split( replace[0] )
            self.baseName = splitTmp[0] + replace[1] + splitTmp[1]  
            
        self.baseName = prefix[1] + self.baseName       

        # MIRROR

        newBuildTrs = []
        for trsValue in self.buildTrs:
            trsValueTmp = utilsMayaApi.mirrorTrsValue( trsValue , planSymCoords ) 
    

            if( inverseAxes == [ 0 , 0 , 0 ] ):
                pass
            elif( inverseAxes == [ 1 , 1 , 0 ]  ):
                trsValueTmp[3:6] = utilsMayaApi.API_rotOffsetInsideEulerRot( trsValueTmp[3:6] , [ 0 , 0 , 180 ] )
            elif( inverseAxes == [ 1 , 0 , 1 ]  ):
                trsValueTmp[3:6] = utilsMayaApi.API_rotOffsetInsideEulerRot( trsValueTmp[3:6] , [ 0 , 180 , 0 ] )
            elif( inverseAxes == [ 0 , 1 , 1 ]  ):
                trsValueTmp[3:6] = utilsMayaApi.API_rotOffsetInsideEulerRot( trsValueTmp[3:6] , [ 180 , 0 , 0 ] )
                    
            newBuildTrs.append( trsValueTmp )   
            
        self.fillAttrManualy( self.baseName , newBuildTrs )     
        self.createRig()    
        '''
        buildRigClass.buildRig.createMirror( self , planSymCoords , lockAxe , inverseAxes ,  prefix , replace  )
        
    #___________________________________________________________________________________________________________________________________________________________________ changeBaseName
    
    def changeBaseName( self , newBaseName , incr = 0 , renameSubRig = 1 ):
        
        '''
        
        # CHECK BASENAME        
        oldBaseName   = self.baseName
        if( incr == 1):
            self.baseName = utilsMaya.incrBaseNameIfExist( newBaseName  ,  [ '' , 'r_' , 'l_']  ,  [ '_ctrl' , '_skn' , self.mainGrpSuffix] )
        else:
            self.baseName = newBaseName     
            
        self.refreshNamesWithBaseName() 
            
        # RENAME SUBRIG
        
        if( renameSubRig == 1 ):
            
            for i in range( 0 ,  len( self.subMainGrps ) ):             
                rigType = mc.getAttr( self.subMainGrps[i] + '.' + self.rigTypeAttr )
                exec( '{0}'.format(          self.dico_rigType_classImport[ rigType ]  ) )              
                exec( 'rigObj = {0}'.format( self.dico_rigType_classBuild[  rigType ]  ) )
                
                rigObj.fillAttrFromRig( self.subMainGrps[i] , masterRig = 0 )
                rigObj.changeBaseName( newBaseName + self.subRigSuffix[i]  , incr , renameSubRig )
            
        # RENAME ALL
        
        newAlls = []
        for elem in self.alls:
            newElem = elem.replace( oldBaseName , self.baseName )
            mc.rename( elem , newElem )
            newAlls.append( newElem )
                
        # ACTUALISE NAME IN MAIN GRP ATTRS
        
        newIns = []
        for elem in self.ins:
            newIn = elem.replace( oldBaseName , self.baseName )
            newIns.append( newIn )      
                
        newCtrls = []
        for elem in self.ctrls:
            newCtrl = elem.replace( oldBaseName , self.baseName )
            newCtrls.append( newCtrl )  
            
        newOuts = []
        for elem in self.outs:
            newOut = elem.replace( oldBaseName , self.baseName )
            newOuts.append( newOut )                

        newBeacons = []
        for elem in self.beacons:
            newBeacon = elem.replace( oldBaseName , self.baseName )
            newBeacons.append( newBeacon )              
    
        newSubMainGrps = []
        for elem in self.subMainGrps:           
            newSubMainGrp = elem.replace( oldBaseName , self.baseName )
            newSubMainGrps.append( newSubMainGrp )                  

        
        self.saveWriteMainGrpAttr(  self.mainGrp , self.rigType , self.buildTrs , newIns , newCtrls , newOuts , newBeacons , newAlls , newSubMainGrps )
        self.writeBeaconsAttr()         
        '''
        buildRigClass.buildRig.changeBaseName( self , newBaseName , incr  , renameSubRig  )     

    #___________________________________________________________________________________________________________________________________________________________________ getMainGrp 

    def getMainGrp( self , elem  , masterRig = 0 ):
        
        '''
            if masterRig == 0 prend le premier rig grp qui arrive
            if masterRig == 1 prend le dernier rig grp qui arrive       
        '''
        '''
        self.mainGrp = elem
        loop = 0
        
        if( masterRig == 1 ): 
            while( mc.objExists( self.mainGrp + '.' + self.mainGrpAttr )  ):
                self.mainGrp = mc.getAttr( self.mainGrp + '.' + self.mainGrpAttr )
                loop +=1
                if( loop > 400 ):
                    mc.error('loop')
        else:
            if not( mc.objExists( self.mainGrp + '.' + self.rigTypeAttr ) ) and ( mc.objExists( self.mainGrp + '.' + self.mainGrpAttr ) ):
                self.mainGrp = mc.getAttr( self.mainGrp + '.' + self.mainGrpAttr )          
                
        return self.mainGrp 
        '''
        
        return buildRigClass.buildRig.getMainGrp( self , elem  , masterRig  )       
        
    #___________________________________________________________________________________________________________________________________________________________________ isElem 
    
    def isElem( self , elemToAnalyse  , masterRig = 1 ):
        '''
        
        if not( mc.objExists( elemToAnalyse + '.' + self.mainGrpAttr ) ):
            return False
            
        self.getMainGrp(elemToAnalyse , masterRig ) 
            
        rigType = mc.getAttr( self.mainGrp  + '.' + self.rigTypeAttr )
        
        if( rigType ==  self.rigType ):
            return True
        else:
            return False
        '''
        return buildRigClass.buildRig.isElem( self , elemToAnalyse  , masterRig  )          
            
    #___________________________________________________________________________________________________________________________________________________________________ saveWriteMainGrpAttr   
    
    def saveWriteMainGrpAttr( self ,  mainGrp = '' , rigType = '' , buildTrs = [] , ins = [] , ctrls = [] , outs = [] , beacons = [] ,  alls = [] , subMainGrps = [] ):
        '''
        #save
    
        self.ins          = ins     
        self.ctrls        = ctrls       
        self.outs         = outs
        self.beacons      = beacons
        self.alls         = alls
        self.subMainGrps  = subMainGrps
        
        self.rigType      = rigType
        self.buildTrs     = buildTrs        
                
        #write          
        if not ( mc.objExists( mainGrp ) ):
            return 0
            
        self.mainGrp = mainGrp
        
        utilsMaya.writeStringAttr(        self.mainGrp   ,   self.rigTypeAttr       ,     self.rigType      )               
        utilsMaya.writeStringArrayAttr(   self.mainGrp   ,   self.insAttr           ,     self.ins          )           
        utilsMaya.writeStringArrayAttr(   self.mainGrp   ,   self.ctrlsAttr         ,     self.ctrls        )       
        utilsMaya.writeStringArrayAttr(   self.mainGrp   ,   self.outsAttr          ,     self.outs         )
        utilsMaya.writeStringArrayAttr(   self.mainGrp   ,   self.beaconsAttr       ,     self.beacons      )       
        utilsMaya.writeStringArrayAttr(   self.mainGrp   ,   self.allsAttr          ,     self.alls         )       
        utilsMaya.writeStringArrayAttr(   self.mainGrp   ,   self.subMainGrpsAttr   ,     self.subMainGrps  )
        
        for i in range( 0 , len( self.buildTrs ) ):
            utilsMaya.writeStringArrayAttr(   self.mainGrp   ,   self.buildTrsAttr + str(i)   ,     self.buildTrs[i]  ) 
            
        return 1
        '''     
        return buildRigClass.buildRig.saveWriteMainGrpAttr( self ,  mainGrp , rigType , buildTrs , ins , ctrls , outs  , beacons  ,  alls  , subMainGrps )
        
    #___________________________________________________________________________________________________________________________________________________________________ readMainGrpAttr
    
    def readMainGrpAttr( self , mainGrp ):
        
        '''
        
        if not( mc.objExists( mainGrp) ) or not(  mc.objExists( mainGrp + '.' + self.rigTypeAttr ) ):       
            return 0            
        
        self.rigType          = mc.getAttr( self.mainGrp + '.' + self.rigTypeAttr )
        self.ins              = utilsMaya.readStringArrayAttr(   self.mainGrp   ,   self.insAttr          )
        self.ctrls            = utilsMaya.readStringArrayAttr(   self.mainGrp   ,   self.ctrlsAttr        )
        self.outs             = utilsMaya.readStringArrayAttr(   self.mainGrp   ,   self.outsAttr         )
        self.beacons          = utilsMaya.readStringArrayAttr(   self.mainGrp   ,   self.beaconsAttr      )     
        self.alls             = utilsMaya.readStringArrayAttr(   self.mainGrp   ,   self.allsAttr         )
        self.subMainGrps      = utilsMaya.readStringArrayAttr(   self.mainGrp   ,   self.subMainGrpsAttr  )

        
        self.buildTrs = []      
        for i in range( 0 , 100 ):
            if not(  mc.objExists( self.mainGrp + '.' + self.buildTrsAttr + str(i) )  ):
                break
            self.buildTrs.append( utilsMaya.readStringArrayAttr(   self.mainGrp   ,   self.buildTrsAttr + str(i) ) )        
                    
        return 1
        '''

        return buildRigClass.buildRig.readMainGrpAttr( self , mainGrp )
        
    #___________________________________________________________________________________________________________________________________________________________________ writeBeaconsAttr   
    
    def writeBeaconsAttr( self ):
        '''
        for beacon in self.beacons:
            utilsMaya.writeStringAttr( beacon , self.mainGrpAttr , self.mainGrp )           
            
        return 1
        '''
        return buildRigClass.buildRig.writeBeaconsAttr( self )  
        
    #___________________________________________________________________________________________________________________________________________________________________ readBeaconAttr
    
    def readBeaconAttr( self , beacon ):

        '''
        if not( mc.objExists( beacon ) ) or not(  mc.objExists( beacon + '.' + self.mainGrpAttr  )  ):      
            return 0    
            
        self.mainGrp = utilsMaya.readStringAttr( beacon , self.mainGrpAttr)             
            
        return 1
        '''
        return buildRigClass.buildRig.readBeaconAttr( self , beacon )           


    

        
    def getChainDistance( self ):
        
        lastTrs = []
        distance = 0
        for i in range( 0 , len(self.buildTrs) - 1 ):
            
            if not ( lastTrs == [] ):
                distance += ompy.MVector( self.buildTrs[i][0] - lastTrs[0] , self.buildTrs[i][1] - lastTrs[1]  , self.buildTrs[i][2] - lastTrs[2] ).length()
                            
            lastTrs = self.buildTrs[i]  

        return distance
            
        
        
        
        
















        