


'''
________________________________________________ COORDS INFO	
getBarycentre                  
getBoundingBox                 
getBBbarycentre                
getBBscale  
________________________________________________ COORDS TRANSFORM	              
rotateCoords                   
transformCoords 
________________________________________________ COORDS OTHER  
getCubeCoords  
________________________________________________ OTHER  
specialClamp
sortDates
 
'''

import math
import maya.OpenMaya as om


print(' === import utilsMath ===')

#================================================================================================================================================================================================================================
#======================================================     COORDS INFO     =====================================================================================================================================================
#================================================================================================================================================================================================================================

#_____________________________________________________________________________________________________________________________________________________________________ getBarycentre

def getBarycentre( coords ):
	
	i = 0
	
	barycentre = [ 0 , 0 , 0 ]
	
	for c in coords:
		barycentre[0] += c[0] 
		barycentre[1] += c[1]
		barycentre[2] += c[2]
		i += 1
		
	barycentre[0] /= i
	barycentre[1] /= i
	barycentre[2] /= i					
	
		
	return barycentre

	
#_____________________________________________________________________________________________________________________________________________________________________ getBoundingBox

def getBoundingBox( coords ):
	
	x , y , z = [] , [] , []
	
	for i in range( 0 , len( coords ) , 3 ):
		x.append( coords[ i + 0 ] )
		y.append( coords[ i + 1 ] )		
		z.append( coords[ i + 2 ] )
		
	x.sort()		
	y.sort()		
	z.sort()	

	minMaxCoords = [ x[0] , y[0] , z[0] , x[-1] , y[-1] , z[-1] ]

	return minMaxCoords
	      
#_____________________________________________________________________________________________________________________________________________________________________ getBoundingBox

def getBoundingBox3( coords ):
	
	x , y , z = [] , [] , []
	
	for i in range( 0 , len( coords ) ):
		x.append( coords[ i ][ 0 ] )
		y.append( coords[ i ][ 1 ] )		
		z.append( coords[ i ][ 2 ] )
		
	x.sort()		
	y.sort()		
	z.sort()	

	minMaxCoords = [ [x[0] , y[0] , z[0]] , [x[-1] , y[-1] , z[-1]] ]

	return minMaxCoords
	      	
#_____________________________________________________________________________________________________________________________________________________________________ getBBbarycentre	

def getBBbarycentre( coords ):
	
	bbCoords = getBoundingBox( coords )		
	
	barycentre = [  ( ( bbCoords[3] + bbCoords[0] ) / 2 ) , ( ( bbCoords[4] + bbCoords[1] ) / 2 ) , ( ( bbCoords[5] + bbCoords[2] ) / 2 )  ]	
		
	return barycentre


#_____________________________________________________________________________________________________________________________________________________________________ getBBscale
	
	
def getBBscale( coords ):
	
	bbCoords = getBoundingBox( coords )		
	
	barycentre = [   ( bbCoords[3] - bbCoords[0] )  , ( bbCoords[4] - bbCoords[1] )  , (  bbCoords[5] - bbCoords[2] )  ]	
		
	return barycentre


def getBBscaleLength( coords ):
	barycentre = getBBscale( coords )
	return om.MVector(barycentre[0],barycentre[1],barycentre[2]).length()


	
	
	
#================================================================================================================================================================================================================================
#======================================================     COORDS TRANSFORM     ================================================================================================================================================
#================================================================================================================================================================================================================================	
	
	
#_____________________________________________________________________________________________________________________________________________________________________ rotateCoords		


def rotateCoords( coords , piv , axe , value ):
 
	
	dicoAxe  = { 'X' : [ 1 , 2 , 0 ]  ,  'Y' : [ 0 , 2 , 1 ]   ,  'Z' : [ 0 , 1 , 2 ] }	
	j = dicoAxe[ axe ]	
	
	if( axe == 'Y' ):
		value *= -1    
		
	#COMPUTE ROTATION			
	rotRad = math.radians(value)	
	newVertexCoords = []
	
	for i in range( 0 , len(coords) , 3 ):	
		newCoord = [ 0 , 0 , 0 ]	
		newCoord[ j[0] ] = math.cos( rotRad ) * ( coords[ i+j[0] ] - piv[ j[0] ] )  -  math.sin( rotRad ) * ( coords[ i+j[1] ] - piv[ j[1] ] )  +  piv[ j[0] ]        
		newCoord[ j[1] ] = math.sin( rotRad ) * ( coords[ i+j[0] ] - piv[ j[0] ] )  +  math.cos( rotRad ) * ( coords[ i+j[1] ] - piv[ j[1] ] )  +  piv[ j[1] ]              
		newCoord[ j[2] ] = coords[ i+j[2] ] 
		
		newVertexCoords += newCoord
		
		    
	return newVertexCoords

		                                                                                                                                                                                              
#_____________________________________________________________________________________________________________________________________________________________________ transformCoords		
	

	

def transformCoords( coords , center , offsets , rotateOrder ):
	#SCALE	
	for i in range( 0 , len( coords ) , 3 ):
		coords[i+0] = ( coords[i+0] - center[0] ) * offsets[6] + center[0]
		coords[i+1] = ( coords[i+1] - center[1] ) * offsets[7] + center[1]
		coords[i+2] = ( coords[i+2] - center[2] ) * offsets[8] + center[2]

	#ROTATE
	for i in range( 0 , 3 ):
		coords = rotateCoords( coords , center , rotateOrder[i] , offsets[ 3 + i ]  )			
		
	#TRANSLATE		
	for i in range( 0 , len( coords ) , 3 ):	
		coords[i+0] = coords[i+0] + offsets[0]
		coords[i+1] = coords[i+1] + offsets[1]
		coords[i+2] = coords[i+2] + offsets[2]		
		
	
	return coords                                                                                                                                                                                  


#================================================================================================================================================================================================================================
#======================================================     COORDS OTHER     ================================================================================================================================================
#================================================================================================================================================================================================================================	

#_____________________________________________________________________________________________________________________________________________________________________ getCubeCoords

def getCubeCoords( offset ):
	
	cubeCoords = [ [-0.5,-0.5,-0.5] , [0.5,-0.5,-0.5] , [0.5,-0.5,0.5] , [-0.5,-0.5,0.5] , [-0.5,0.5,-0.5] , [0.5,0.5,-0.5] , [0.5,0.5,0.5] , [-0.5,0.5,0.5]  ]  # <---- ordre a revoir
	
	cubeCoords = transformCoords( cubeCoords , [ 0 , 0 , 0 ]  , offset , 'XYZ'  )
	
	return cubeCoords
	
	
#================================================================================================================================================================================================================================
#======================================================     OTHER     ===========================================================================================================================================================
#================================================================================================================================================================================================================================

	
#_____________________________________________________________________________________________________________________________________________________________________ specialClamp		


def specialClamp( nbr , min , max ):
	
	'''
		clamp mais ajoute la difference dans l echelle entre min et max
		ex:    specialClamp( 10 , 0 , 3 ) ----> 1      (3 3 3 1)
		le max n'est pas inclu
	'''
	
	
	size = ( max - min )
	
	if( nbr < min ):
		difference = min - nbr
		reste = difference % size
		newNbr = max - reste
	elif( nbr >= max ):
		difference = nbr - max
		reste = difference % size
		newNbr = min + reste
		
	else:
		newNbr = nbr
		
	return newNbr  
	
	

#_____________________________________________________________________________________________________________________________________________________________________ sortDates	

def sortDates( rawDates ):
	
	'''
	sort date of type xx/xx/xxxx
	'''

	sortedDates = [] 
	days   = []
	months = []
	years  = []
	
	for date in rawDates:
		stringdates = date.split('/')
		days.append(   int(stringdates[0]) )
		months.append( int(stringdates[1]) )
		years.append(  int(stringdates[2]) )
	
	days   = list(set(days))	
	months = list(set(months))	
	years  = list(set(years))	
	
	days.sort()
	months.sort()
	years.sort()
	
	sameYearDates = []
	sameMonthDates = []
	
	for year in years:
		sameYearDates = []
		for date in rawDates:
			if( int( date.split('/')[2] ) == year ):
				sameYearDates.append(date)
				
		
		for month in months:
			sameMonthDates = []
			for sameYearDate in sameYearDates:				
				if( int( sameYearDate.split('/')[1] ) == month ):
					sameMonthDates.append(sameYearDate)
		
			for day in days:
				for sameMonthDate in sameMonthDates:				
					if( int( sameMonthDate.split('/')[0] ) == day ):
						sortedDates.append(sameMonthDate)			
		
	return sortedDates                                                           
                            


#_____________________________________________________________________________________________________________________________________________________________________ makePointGrid	

def makePointGrid( nbrElem , nbrByLine , distIntervalL , distIntervalH , lAxe , hAxe ):
	
	
	nbr  = 0
	
	posL = 0
	posH = 0
	
	gridCoords = []
	
	for i in range( 0 , nbrElem ):
	
		
	    coords = [ 0 , 0 , 0 ]
	    coords[lAxe] = posL 
	    coords[hAxe] = posH 
	    
	    gridCoords.append( coords )
	
	    
	    posL += distIntervalL ;
	    nbr += 1
	    
	    if( nbr == nbrByLine ):
	    
	        posL = 0
	        nbr  = 0
	        posH += distIntervalH
	        
	return gridCoords












	