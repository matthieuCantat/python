

import maya.cmds as mc


def createRopeDynamicsExp( slaves , attrDriver , attractObjs , cSpheres , store ):
	
	#DRIVER ATTR
	attrs   = [ 'mass' , 'friction' , 'collision' , 'nbrAttractEval' ]
	values  = [ 0.1 , 0.1 , 1 , 1 ]

	for i in range( 0 , len(attractObjs[0]) ):
		attrs.append( 'elasticity{}'.format(i) )
		values.append( 1 )
	
	for i in range( 0 , len(attractObjs[0]) ):
		attrs.append( 'lengthRope{}'.format(i) )
		values.append( 4 )

	for i in range( 0 , len(attrs) ):
		mc.addAttr( attrDriver , ln = attrs[i], at = "double" , dv = values[i] )
		mc.setAttr( ( attrDriver + '.' + attrs[i] ) , e = True , keyable = True )


	#STORE ATTR
	attr    = 'slave'
	letters = [ 'A' , 'B' , 'C' ]
	axes    = [ 'X' , 'Y' , 'Z' ]
	
	for slave in slaves:
		for letter in letters:
			for axe in axes:
				attrToWrite = slave + letter + axe
				mc.addAttr( store , ln = attrToWrite, at = "double" , dv = 0 )
				mc.setAttr( ( store + '.' + attrToWrite ) , e = True , keyable = True )

	#GET SLAVE POSITION
	slavesPos = []
	for i in range( 0 , len(slaves) ):
		pos = [0,0,0]
		pos[0] = mc.getAttr( slaves[i] + '.tx')
		pos[1] = mc.getAttr( slaves[i] + '.ty')
		pos[2] = mc.getAttr( slaves[i] + '.tz')
		slavesPos.append(pos)


	#EXPRESSSION
	exp = ''
	exp += ('\n//INIT_______________________________________________________ {}'.format( attrDriver ) )                                                                                                                                  
	exp += ('\n')
	exp += ('\nvector $vGravity = << 0 , -9.8 , 0 >>;')
	exp += ('\nfloat $raySlave = 1;')
	exp += ('\nfloat $startFrame = `playbackOptions -q -min`;')
	exp += ('\n')		
	exp += ('\n//GATHER VALUES')
	exp += ('\nfloat $mass           = {}.mass;      '.format( attrDriver  )  )
	exp += ('\nfloat $friction       = {}.friction;  '.format( attrDriver  )  )
	exp += ('\nint $nbrAttractEval   = {}.nbrAttractEval;  '.format( attrDriver  )  )

	for i in range( 0 , len(cSpheres)):	
		exp += ('\nfloat $collision{1}     = {0}.collision;'.format( attrDriver   , i )  )
		exp += ('\nfloat $collisionRay{1}  = {0}.scaleX;    '.format( cSpheres[i]  , i )  )	
	for i in range( 0 , len(attractObjs[0])):	
		exp += ('\nfloat $elasticity{1}   = {0}.elasticity{1};'.format( attrDriver , i ) )
		exp += ('\nfloat $lengthRope{1}   = {0}.lengthRope{1};'.format( attrDriver , i ) )
	exp += ('\n')
	exp += ('\n')

	for i in range( 0 , len(slaves)):		
		exp += ('\n//_______________________________________________________ ' + slaves[i] )
		exp += ('\n//GATHER COORDS')	
		exp += ('\nvector $pSlaveA = << {0}.{1}AX , {0}.{1}AY , {0}.{1}AZ >>;'.format( store ,slaves[i] ) )
		exp += ('\nvector $pSlaveB = << {0}.{1}BX , {0}.{1}BY , {0}.{1}BZ >>;'.format( store ,slaves[i] ) )
		exp += ('\nvector $pSlaveC = << {0}.{1}CX , {0}.{1}CY , {0}.{1}CZ >>;'.format( store ,slaves[i] ) )	     		
		exp += ('\n')
		exp += ('\nvector $pSlave = $pSlaveA;')
		exp += ('\n')			
		exp += ('\n//COMPUTE DYN')
		exp += ('\n')
		exp += ('\nvector $vWeight   = $vGravity * $mass;')
		exp += ('\nvector $vMomentum = $pSlaveB - $pSlaveC;')
		exp += ('\nvector $vFriction = $vMomentum * -1 * $friction;')
		exp += ('\n')
		exp += ('\n$pSlave += $vMomentum + $vFriction + $vWeight;')
		exp += ('\n')

		exp += ('\nfor( $e = 0 ; $e < $nbrAttractEval ; $e++)')
		exp += ('\n{')
		
		for j in range( 0 , len(attractObjs[i])):
			exp += ('\n//ATTRACT {0}'.format( attractObjs[i][j] ) )
			exp += ('\nvector $pAttract = << {0}.tx , {0}.ty , {0}.tz >>;'.format( attractObjs[i][j] ) )
			exp += ('\nvector $vAttractSlave = $pAttract - $pSlave;')
			exp += ('\nvector $vAttractA = unit( $vAttractSlave )* clamp( 0 , 999999 ,  mag( $vAttractSlave ) - $lengthRope{0} ) * $elasticity{0} / $nbrAttractEval;'.format(j))
			exp += ('\n$pSlave += $vAttractA;')
			exp += ('\n')	
			exp += ('\n')

		exp += ('\n}')

		for j in range( 0 , len(cSpheres)):	
			exp += ('\n//COLLISION {}'.format( cSpheres[j] ) )
			exp += ('\nvector $pCSphere = << {0}.tx , {0}.ty , {0}.tz >>;'.format( cSpheres[j] ) )			
			exp += ('\nvector $vSlaveCSphere = $pSlave - $pCSphere;')
			exp += ('\nvector $vCollisionA = unit( $vSlaveCSphere ) * clamp( 0 , 999999 , $collisionRay{0} - mag( $vSlaveCSphere ) ) * $collision{0} ;'.format( j ) )
			exp += ('\n$pSlave += $vCollisionA;')
			exp += ('\n')
			exp += ('\n')			

		exp += ('\n')
		exp += ('\n')	
		exp += ('\nif( frame == $startFrame )')
		exp += ('\n{')
		exp += ('\n//OUT')
		exp += ('\n{}.translateX = {};'.format( slaves[i] , slavesPos[i][0] ) )
		exp += ('\n{}.translateY = {};'.format( slaves[i] , slavesPos[i][1] ) )
		exp += ('\n{}.translateZ = {};'.format( slaves[i] , slavesPos[i][2] ) )
		exp += ('\n')
		exp += ('\n//STORE')
		exp += ('\n{}.{}CX = {};'.format( store , slaves[i] , slavesPos[i][0] ) )
		exp += ('\n{}.{}CY = {};'.format( store , slaves[i] , slavesPos[i][1] ) )
		exp += ('\n{}.{}CZ = {};'.format( store , slaves[i] , slavesPos[i][2] ) )
		exp += ('\n')
		exp += ('\n{}.{}BX = {};'.format( store , slaves[i] , slavesPos[i][0] ) )
		exp += ('\n{}.{}BY = {};'.format( store , slaves[i] , slavesPos[i][1] ) )
		exp += ('\n{}.{}BZ = {};'.format( store , slaves[i] , slavesPos[i][2] ) )
		exp += ('\n')
		exp += ('\n{}.{}AX = {};'.format( store , slaves[i] , slavesPos[i][0] ) )
		exp += ('\n{}.{}AY = {};'.format( store , slaves[i] , slavesPos[i][1] ) )
		exp += ('\n{}.{}AZ = {};'.format( store , slaves[i] , slavesPos[i][2] ) )
		exp += ('\n')
		exp += ('\n}')
		exp += ('\nelse')
		exp += ('\n{')
		exp += ('\n')
		exp += ('\n//OUT')
		exp += ('\n{}.translateX = $pSlave.x;'.format(slaves[i]) )
		exp += ('\n{}.translateY = $pSlave.y;'.format(slaves[i]) )
		exp += ('\n{}.translateZ = $pSlave.z;'.format(slaves[i]) )
		exp += ('\n')
		exp += ('\n//STORE')
		exp += ('\n{0}.{1}CX = {0}.{1}BX;'.format( store , slaves[i] ) )
		exp += ('\n{0}.{1}CY = {0}.{1}BY;'.format( store , slaves[i] ) )
		exp += ('\n{0}.{1}CZ = {0}.{1}BZ;'.format( store , slaves[i] ) )
		exp += ('\n')
		exp += ('\n{0}.{1}BX = {0}.{1}AX;'.format( store , slaves[i] ) )
		exp += ('\n{0}.{1}BY = {0}.{1}AY;'.format( store , slaves[i] ) )
		exp += ('\n{0}.{1}BZ = {0}.{1}AZ;'.format( store , slaves[i] ) )
		exp += ('\n')
		exp += ('\n{0}.{1}AX = $pSlave.x;'.format( store , slaves[i] ) )
		exp += ('\n{0}.{1}AY = $pSlave.y;'.format( store , slaves[i] ) )
		exp += ('\n{0}.{1}AZ = $pSlave.z;'.format( store , slaves[i] ) )
		exp += ('\n}')
		exp += ('\n')

	mc.expression( n = 'ropeDyn_EXP'  , s = exp  , o = '' , ae=  1 , uc = 'all'  )
	



'''
# ONE SLAVE

slaves = ['slave']
attractObjs = [[ 'masterA' , 'masterB' , 'masterC' , 'masterD' ]]
cSpheres = [ 'collisionA' , 'collisionB' ]
attrDriver = 'driver'
store = 'store'
createRopeDynamicsExp( slaves , attrDriver , attractObjs , cSpheres , store )

'''



'''
#ROPE
slaves = [ 'slave{}'.format(i) for i in range( 1 , 30 ) ]

attractObjs = [[ 'masterA' , slaves[1] ]]
for i in range( 1 , len( slaves ) - 1 ):
    attractObjs.append( [ slaves[i-1] , slaves[i+1] ] )
attractObjs.append( [ slaves[-2] , 'masterB' ] )    

cSpheres = [ 'collisionA' , 'collisionB' ]
attrDriver = 'driver'
store = 'store'
createRopeDynamicsExp( slaves , attrDriver , attractObjs , cSpheres , store )

'''


'''
#ROPE
slaves = [ 'slave{}'.format(i) for i in range( 1 , 30 ) ]

attractObjs = [[ 'masterA' , slaves[1] ]]
for i in range( 1 , len( slaves ) - 1 ):
    attractObjs.append( [ slaves[i-1] , slaves[i+1] ] )
attractObjs.append( [ slaves[-2] , 'masterB' ] )    

cSpheres = [ 'collisionA' , 'collisionB' ]
attrDriver = 'driver'
store = 'store'
createRopeDynamicsExp( slaves , attrDriver , attractObjs , cSpheres , store )

'''

'''
#PLANE

slaves = [ 'slave{}'.format(i) for i in range( 1 , 50 ) ]

attractObjs = []
nbrRow = 7
for i in range( 0 , len( slaves ) ):
    attractTmp = []
    if( 0 <= i - nbrRow ):
        attractTmp.append( slaves[i - nbrRow] )
    if not( i+1 in [1,8,15,22,29,36,43] ):
        attractTmp.append( slaves[i - 1] )  
    if not( i+1 in [7,14,21,28,35,42,49] ):
        attractTmp.append( slaves[i + 1] )         
    if( i + nbrRow < len(slaves) ):
        attractTmp.append( slaves[i + nbrRow] ) 
                      
    attractObjs.append( attractTmp )
      
cSpheres = [ 'collisionA' , 'collisionB' ]
attrDriver = 'driver'
store = 'store'
createRopeDynamicsExp( slaves , attrDriver , attractObjs , cSpheres , store )
'''



import maya.cmds as mc


def addAttrFloat( master , attrs ,values ):
	for i in range( 0 , len(attrs) ):
		mc.addAttr( master , ln = attrs[i], at = "double" , dv = values[i] )
		mc.setAttr( ( master + '.' + attrs[i] ) , e = True , keyable = True )


def addAttrStore( master , slaves , nbrMemorySlot ):
	attr    = 'slave'
	letters = ['A' , 'B' , 'C' , 'D' ]
	axes    = [ 'X' , 'Y' , 'Z' ]
	for slave in slaves:
		for i in range( 0 , nbrMemorySlot ):
			for axe in axes:
				attrToWrite = slave + letters[i] + axe
				mc.addAttr( master , ln = attrToWrite, at = "double" , dv = 0 )
				mc.setAttr( ( master + '.' + attrToWrite ) , e = True , keyable = True )
				


def addAttrPoint( master , attrs ):
	axis = [ 'X' , 'Y' , 'Z' ]
	for attr in attrs:
		mc.addAttr( master , ln = attr, at = "double3" )
		for axe in axis:
			mc.addAttr( master , ln = (attr+axe) , at = "double" , p = attr )
		mc.setAttr( ( master + '.' + attr ) , e = True , keyable = True )
		for axe in axis:
			mc.setAttr( ( master + '.' + (attr+axe) ) , e = True , keyable = True )



'''				
addAttrFloat( 'driver_GEO' , [ 'activate' , 'mass' , 'gravity' , 'friction' , 'attract' ] , [ 1 , 9.8 , 0.1 , 0.2 ] )				
addAttrStore( 'store' , ['slave'] , 2 )
addAttrPoint( 'visuStopEval' , ['pSim' , 'pSimStoreA' , 'pDriver' , 'vWeight' , 'vMomentum' , 'vFriction' , 'vAttractA' ] )
'''	

