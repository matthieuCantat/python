

'''
	name:  transferAnim
	type:  RIGGING
	tag:   anim
	date:  27/09/2016	
	input: selected objs

	transfere 2 by 2 anim
	connect the anim nodes of the obj source to the dest obj attrs
		
'''



import maya.cmds as mc



def transferAnim():
		
	selection = mc.ls( sl = True )
	
	lastValue = ''
	
	for i in range( 0 , len( selection ) , 2 ):
		try:
			lastValue =  selection[i+1]
		except:
			break
			
		transfereAnim( selection[i] , selection[i+1] )




def transfereAnim( objSource , destination ):
	
	'''
	this proc connect the anim node of the source to the destination. This is not a copy of none!
	'''
	# get information 
	
	upStreamNodes = mc.listConnections( objSource , s = True , d = False )

	animCurveNodes = []
	attrToConnect  = []
	
	for node in upStreamNodes:
		if( 'animCurve' in mc.nodeType(node) ):
			animCurveNodes.append(node)
			
			plugDest = mc.listConnections( node , d = True , s = False , p = True )
			attrDest = plugDest[0].split('.')[1]
			attrToConnect.append(attrDest)
		
	
	# connect to dest
	
	for i in range( 0 , len(animCurveNodes) ):
		mc.connectAttr( (animCurveNodes[i] + '.output') , (destination + '.' + attrToConnect[i])  )
	

		
