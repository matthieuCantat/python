
'''
#******************************************************** BUILD EXEMPLE RIG CTRL
import maya.cmds as mc
import python
from python.classe.rigModuleChain import *
reload(python.classe.rigModuleChain)



mc.file( f = True , new = True )
#=================================================


#_________________________________BUILD

chainA = rigModuleChain( n = 'chain' , pos = [ [1,0,5,0,0,0,1,1,1] , [3,0,5,0,0,0,1,1,1] , [5,0,5,0,0,0,1,1,1] , [7,0,5,0,0,0,1,1,1] ] , form = 'cube' , colors = ['red'] , skeleton = 1  )    
chainA.printBuild = 1
toExec = chainA.build()
print(toExec)

#_________________________________MIRROR
args = {}
args['value']             = [0,0,0 , 0,1,0 , 0,0,1]
args['mode']              = 'mirror'
args['pivot']             = [0,0,0 , 0,0,0 , 1,1,1]
args['namePrefix']        = ['r','l']
args['nameReplace']       = ['toto','tata']
args['nameIncr']          = ''
args['nameAdd']           = []
args['noneMirrorAxe']     = 4

mirrored = chainA.duplicate( **args )

for elem in mirrored:
    elem.build()

#_________________________________TRANSFORM
args = {}
args['value']             = [-2.36 , 2.876 , -2.247 , -23.629 , 18.578 , 33.015 , 1 , 1 , 1 , 5 ]
args['mode']              = 'transform'
args['pivot']             = [ 5 , 0 , -1 , 0 ,0,0 , 1 , 1 , 1 ]
args['namePrefix']        = ['','']
args['nameReplace']       = ['','']
args['nameIncr']          = 'A'
args['nameAdd']           = []
args['noneMirrorAxe']     = 4


duplicated = chainA.duplicate( **args )
for elem in duplicated:
    elem.build()

    
'''

from .rigModule import *            
from .rigCtrl import *          
from .rigStretchyJoint import *   
from .rigSkeletonChain import *      
from .trsBackUp import *
import maya.api.OpenMaya as ompy


class rigModuleChain( rigModule ):

    def __init__( self , **args ):
        rigModule.__init__( self , **args )
    
        #CLASSE TYPE
        self.classeType = 'rigModuleChain'
        #CLASSE BLUE PRINT
        self.Name.add( 'base' , baseName = self.classeType )    

        self.CurveShape.add( 'ctrl' , value = { 'form' : 'circle' , 'colors' : [13] , 'axe' : 'x' , 'offset' : [0,0,0,0,0,0,1,1,1] }  )        
        
        self.doJoint    = args.get( 'joint'      , None )   
        self.doOffset   = args.get( 'offset'     , None )
        pos             = args.get( 'pos'        , None )
        manipsPosition  = [ [0,0,0,0,0,0,1,1,1] , [2,0,0,0,0,0,1,1,1] , [4,0,0,0,0,0,1,1,1] ]                                
        if not( pos == None ): manipsPosition = pos 

        #ATTR STATE
        self.attrStates = args.get( 'attrStates' , None )
        argsCtrls = [ {'attrStates':None} ]*len(manipsPosition)
        if not( self.attrStates == None ):
            argsCtrls = []
            lastValueTmp = None
            for i in range( len(manipsPosition) ):
                if( i < len(self.attrStates) ):
                    argsCtrls.append( {'attrStates':[self.attrStates[i]]} )
                    lastValueTmp                  = [self.attrStates[i]]
                else:
                    argsCtrls.append( {'attrStates':lastValueTmp} )


        self.SubRigs     = []
        self.SubRigsName = []
        self.ins         = []
        self.outs        = []
        self.outsToCtrls = []
        for i in range( len(manipsPosition) ):
            self.Name.add( 'ctrl{}'.format(i) , ref = self.Name.base , baseNameAppend = '{}'.format(i) )
            self.Pos.add(  'ctrl{}'.format(i) , replace = manipsPosition[i]  )
            #SUBRIG
            if( i == 0 ): exec( 'self.Ctrl{0} = rigCtrl( n = self.Name.ctrl{0} , pos = [ self.Pos.ctrl{0} ] , shape = self.CurveShape.ctrl , joint = {1} , offset = {2} , ctrlScale = {3}*1 , parent = self.Name.ctrlGrp    , **argsCtrls[{0}] )'.format(i , self.doJoint , self.doOffset , self.ctrlScale        ) )
            else:         exec( 'self.Ctrl{0} = rigCtrl( n = self.Name.ctrl{0} , pos = [ self.Pos.ctrl{0} ] , shape = self.CurveShape.ctrl , joint = {1} , offset = {2} , ctrlScale = {3}*1 , parent = self.Ctrl{4}.outs[0] , **argsCtrls[{0}] )'.format(i , self.doJoint , self.doOffset , self.ctrlScale , i -1 ) )
            exec( 'self.SubRigs.append(self.Ctrl{0})'.format(i) )
            exec( 'self.SubRigsName.append("Ctrl{0}")'.format(i) )
           
            exec( 'self.ins.append(self.Ctrl{0}.ins[0])'.format(i) )
            exec( 'self.outs.append(         self.Ctrl{0}.outs[0]     )'.format(i) )
            exec( 'self.outsToCtrls.append( [self.Ctrl{0}.Name.ctrl ] )'.format(i) )

        #CLASSE UTILS
        #CLASSE MODIF
        self.doSkeleton = args.get( 'skeleton'   , None )
        self.doAim      = args.get( 'aim'        , None )
        self.doDynamic  = args.get( 'dynamic'    , None )

        if( self.doSkeleton ):
            #POSITION
            PositionTmp = []
            for i in range( len(manipsPosition) ):
                exec('PositionTmp.append( self.Pos.ctrl{0} )'.format(i))
            #SUBRIG
            self.Name.add( 'skeleton' , ref = self.Name.base , baseNameAppend = 'skeleton' )    
            self.Joints = rigSkeletonChain( n = self.Name.skeleton , pos = PositionTmp , parent = self.Name.skeletonGrp ) 
            #LINK
            for i in range( len(manipsPosition) ):
                exec( 'self.Link.add( "skeleton{0}" , Sources = [ self.SubRigs[{0}].outs[0] ] , Destinations = [ self.Joints.ins[{0}] ] , type = "parent" , operation = "oneMaster" , maintainOffset = 0 )'.format(i) )   
            #STORE
            self.SubRigs     += [ self.Joints ]
            self.SubRigsName += [ 'Joints' ]
            self.outs = self.Joints.outs    
     
        if( self.doAim ):
            for i in range( len(manipsPosition) - 1 ):
                exec( 'self.Pos.add( "ctrl{0}" , aim = self.Pos.ctrl{1} )'.format( i , i+1 ) )

        if( self.doDynamic ):
            pass
            

        #INSTANCE MODIF 
        name          = args.get( 'n'          , None ) 
        shape         = args.get( 'shape'      , None )
        form          = args.get( 'form'       , None ) 
        colors        = args.get( 'colors'     , None )
        aimNextPos    = args.get( 'aimNextPos' , None )

        if not( name   == None ): self.Name.add(       'base' , copy  = name                  )   
        if not( shape  == None ): self.CurveShape.add( 'ctrl' , value = shape                 )
        if not( form   == None ): self.CurveShape.add( 'ctrl' , value = { 'form'   : form   } )
        if not( colors == None ): self.CurveShape.add( 'ctrl' , value = { 'colors' : colors } )  

        constraintOuts = args.get( 'constraintOuts' , True )    
        if not( pos == None ) and( type(pos[0]) == types.StringType ):
            if( mc.objExists(pos[0]) == True ):

                if( constraintOuts ):
                    for i in range( 0 , len(pos) ):
                        self.Name.add(  'out{}'.format(i) , copy = pos[i] , objExists = True )
                        self.Link.add(  'out{}'.format(i)      , Sources = [ self.outs[i] ] , Destinations = [ eval('self.Name.out{}'.format(i) )  ] , type = 'parent' , operation = 'oneMaster'  )                  
                        self.Link.add(  'outScale{}'.format(i) , Sources = [ self.outs[i] ] , Destinations = [ eval('self.Name.out{}'.format(i) )  ] , type = 'scale'  , operation = 'oneMaster'  )

                fathers = mc.listRelatives( pos[0] , p = True )
                if not( fathers == None ):      
                    self.Name.add(  'in0' , copy = fathers[0] , objExists = True )      
                    self.Link.add(  'in0' , Sources = [eval('self.Name.in0' )] , Destinations = [ self.ins[0] ] , type = 'parent' , operation = 'oneMaster'  )                  


        '''     
        #INSTANCE_______________________________INFO
        self.ins        = self.CtrlA.ins         + self.CtrlB.ins
        self.insAnim    = self.CtrlA.insAnim     + self.CtrlA.insAnim
        self.outs       = self.StretchyA.outs    + self.StretchyB.outs
        self.ctrls      = self.CtrlA.ctrls       + self.CtrlB.ctrls
        self.ctrlsDupli = self.CtrlA..ctrlsDupli + self.CtrlA..ctrlsDupli
        #INSTANCE_______________________________CUSTOM
        ''' 

    def postBuild( self ):
        
        return ''



