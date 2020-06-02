'''



import maya.cmds as mc
import math



pA = [0,0]
pB = [0,0]

pA[0] = mc.getAttr( 'pCube1.tx' )
pA[1] = mc.getAttr( 'pCube1.ty' )
pB[0] = mc.getAttr( 'pCube2.tx' )
pB[1] = mc.getAttr( 'pCube2.ty' )

r_length = 5
N        = 60
sag  = 1

outX , outY = catenary(pA,pB,r_length,N,sag)

for i in range(1,len(outX) ):
    mc.setAttr( 'locator{}.tx'.format(i) , outX[i] )
    mc.setAttr( 'locator{}.ty'.format(i) , outY[i] )



'''


def catenary(pA,pB,r_length,N,sag=1):
	# given two points a=[ax ay] and b=[bx by] in the vertical plane,
	# rope length r_length, and the number of intermediate points N,
	# outputs the coordinates outX and outY of the hanging rope from a to b
	# the optional input sagInit initializes the sag parameter for the
	# root-finding procedure.
	maxIter	 = 100       # maximum number of iterations
	minGrad	 = 1e-10     # minimum norm of gradient
	minVal	 = 1e-8      # minimum norm of sag function
	stepDec	 = 0.5       # factor for decreasing stepsize
	minStep	 = 1e-9		 # minimum step size
	minHoriz = 1e-3      # minumum horizontal distance
	

	if( pA[0] > pB[0] ): 
		pATmp = pA[:]
		pA    = pB
		pB    = pATmp

	d = pB[0]-pA[0]
	h = pB[1]-pA[1]

	# almost perfectly vertical
	if( abs(d) < minHoriz ): 
		print('almost perfectly vertical')
		outX = [ (pA[0]+pB[0])/2 ]*N

		if( r_length < abs(h) ):
			# rope is stretched
			outY  = getLinearArray( pA[1] , pB[1] , N )
		else:
			sag	  = ( r_length - abs(h) )/2
			n_sag = ceil( N * sag/r_length )
			y_max = max( pA[1] , pB[1] )
			y_min = min( pA[1] , pB[1] )
			outY  = getLinearArray( y_max     , y_min-sag , N-n_sag )
			outY += getLinearArray( y_min-sag , y_min     , n_sag   )


	outX = getLinearArray(pA[0],pB[0],N)

	r_length = 120
	h = 20
	d = 80
	sag = 25.13

	if( r_length <= math.sqrt( pow(d,2) + pow(h,2) ) ):
		print("rope is stretched: straight line")
		outY = getLinearArray(pA[1],pB[1],N)
	else:
		print("rope is loose")
		'''
		for i in range( 1 , maxIter ):
			print( i , "sag" , sag )
			val		= g( sag ,d,h,r_length)
			grad    = dg(sag ,d)

			if( ( abs(val) < minVal )or( abs(grad) < minGrad ) ):
				break

			search	= -g(sag ,d,h,r_length)/dg(sag ,d)
			
			alpha	= 1
			sag_new = sag + alpha*search
			
			while( ( sag_new < 0 )or( abs(g(sag_new ,d,h,r_length)) > abs(val) ) ):
				alpha = stepDec*alpha
				if( alpha < minStep ): break
				sag_new	= sag + alpha*search
			
			sag = sag_new
		'''
		# get location of rope minimum and vertical bias
		x_left	= 1/2*(math.log((r_length+h)/(r_length-h))/sag-d)
		print('x_left',x_left)
		x_min   = pA[0] - x_left
		bias    = pA[1] - math.cosh(x_left*sag)/sag
		
		outY    = [ math.cosh((x-x_min)*sag)/sag + bias for x in outX ]
	
	return [outX,outY]


def g( s , d , h , r_length ):
	return 2*math.sinh(s*d/2)/s - math.sqrt( pow(r_length,2)-pow(h,2))


def dg( s , d ):
	return 2*math.cosh(s*d/2)*d/(2*s) - 2*math.sinh(s*d/2)/pow(s,2);


def getLinearArray(vA,vB,nbrElements):

	delta     = vB-vA
	deltaStep = delta/(nbrElements-1)

	outArray = []
	vTmp = vA
	for i in range(0,nbrElements):
		outArray.append(vTmp)
		vTmp += deltaStep

	return outArray




##########################################################################################################################################
##########################################################################################################################################
##########################################################################################################################################
##########################################################################################################################################
##########################################################################################################################################



import math
import numpy as np 
import matplotlib.pyplot as plt
from scipy.optimize import fsolve  
from inout import write_file


def cat(a):
	# defining catenary function
	#catenary eq (math): a*sinh(L/(2*a)+atanh(d/S))+a*sinh(L/(2*a)-atanh(d/S))-S=0
	return a*math.sinh(L/(2*a))+math.atanh(d/S)+a*math.sinh(L/(2*a))-math.atanh(d/S)-S

L=float(input("Horizontal Distance between supports [m]: "))
d=float(input ("Vertical Distance between supports [m]: "))
S=float(input("Length of cable [m] - must be greater than distance between supports:  "))
w=float(input("Unit weight of cable [kg/m]: "))
za=float(input("Elevation of higher support from reference plane [m]: "))

#checking if cable length is bigger than total distance between supports
distance=(L**2+d**2)**0.5
if S <= distance:
	print ("Length of cable must be greater than TOTAL distance between supports!")
	S=float(input("Length of cable [m]: "))
else:
	pass 

# solving catenary function for 'a'

a=fsolve(cat, 1)

# hor. distance between lowest catenary point (P) to higher support point (La)
La=a*(L/(2*a)+math.atanh(d/S))
# hor. distance between lowest catenary point (P) to lower support point (Lb)
Lb=L-La
# vert. distance from higher support point to lowest point (P) in catenary (ha)
ha=a*math.cosh(La/a)-a
## calculating reaction forces and angles
# catenary lenght between support "A" (higher) and "P" - Sa
Sa=a*math.sinh(La/a)
# catenary lenght between support "B" )lower) and "P" - Sb
Sb=a*math.sinh(Lb/a)
# horizontal tension - constant through catenary: H
H=w*a
# vertical tension at "A"  (Va) and "B" (Vb)
Va=Sa*w
Vb=Sb*w
# tension at "A" (TA) and B (TB)
TA=(H**2+Va**2)**0.5
TB=(H**2+Vb**2)**0.5
# inclination angles from vertical at "A" (ThetA) and B (ThetB)
ThetA=math.atan(H/Va)
ThetB=math.atan(H/Vb)
ThetAd=ThetA*180/math.pi;
ThetBd=ThetB*180/math.pi;
# establishing A, B and P in coordinate system
# index "a" corresponding to point "A", "b" to "B"-point and "P" to lowest caten. point
zb=za-d
zp=za-ha
xa=La
xp=0
xb=-Lb

# writting results to file
fname='catenary_res.txt'
fn=open(fname, 'a')
write_file(fn, "Horizontal Distance between supports in meters: ", round(L,3))
write_file(fn, "Catenary length in meters: ", round(S,3))
write_file(fn, "Vertical Distance Between supports in meters: ", round(d,3))
write_file(fn, "Unit Weight of Catenary line in kg/m: ", round(w,3))
write_file(fn, "Elevation of higher support (A) from reference plane in meters: ", round(za,3))
write_file(fn, "\Catenary coef.: ", round(a,5))
write_file(fn, "Horizontal tension in kg (constant along line: ", round(H,3))
write_file(fn, "Vertical tension in A in kg: ", round(Va,3))
write_file(fn, "Total tension in A in kg: ", round(TA,3))
write_file(fn, "Total tension in B in kg: ", round(TB,3))
write_file(fn, "Inclination angle from vertical at A in radians: ", round(ThetA,3))
write_file(fn, "Inclination angle from vertical at B in radians: ", round(ThetB,3))
write_file(fn, "Inclination angle from vertical at A in degrees: ", round(ThetAd,3))
write_file(fn, "Inclination angle from vertical at B in degrees: ", round(ThetBd,3))
fn.close()


# graphing catenary curve - matplotlib & writting coordinates in file 
xinc=L/100
y=[]
xc=[]
fncoords="catenary_coords.txt"
fn=open(fncoords, "a")

for x in np.arange (xb, xa+xinc, xinc):
	ycal=a*math.cosh(x/a)
	fn.write("\n")
	fn.write(str(round(x,3)))
	fn.write("\t")
	fn.write(str(round(ycal[0],3)))
	y.append(ycal)
	xc.append(x)
fn.close()

# plotting, finally 
plt.plot(xc,y)
plt.xlabel("X-distance [m]")
plt.ylabel("Y-distance [m]")
plt.grid()
plt.show()	