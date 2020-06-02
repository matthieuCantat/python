import maya.cmds as mc
import maya.api.OpenMaya as ompy



#GET POSITION INTO MPOINTARRAY
selection = mc.ls(sl=True)
mPosition = ompy.MPointArray()
for elem in selection:
    positionTmp = mc.xform( elem , q = True , t = True , ws = True )
    mPoint = ompy.MPoint( positionTmp[0] , positionTmp[1] , positionTmp[2] )
    mPosition.append( 	mPoint	) 	
    


curve = ompy.MFnNurbsCurve()
curve.create()



#=============================================================

#=============================================================
import maya.cmds as mc
import maya.api.OpenMaya as ompy
#IN
degree = 3
build    = 'open' # 'close'
mode     = 'CV' # 'EP' 'BEZIER'
matrices = []
offset   = [ 0 , 0 , 0 ]
#GET MATRIX 
selection = mc.ls(sl=True)
mMatrixArray = ompy.MMatrixArray()
for elem in selection:
    matrixNumTmp = mc.xform( elem , q = True , matrix = True , ws = True )
    mMatrix = ompy.MMatrix( matrixNumTmp )
    mMatrixArray.append( mMatrix ) 	
#GET POINT FROM MATRIX
positions = ompy.MPointArray()
for i in range( 0 , len(mMatrixArray) ):
	mTrs = ompy.MTransformationMatrix(mMatrixArray[i]) 
	mVector = mTrs.translation(ompy.MSpace.kWorld)
	mPoint = ompy.MPoint( mVector.x , mVector.y , mVector.z ) 
	positions.append( mPoint )
#GET Knot
nbrKnot = len(positions) + degree - 1
knotsValues = ompy.MDoubleArray()
for i in range(0,3): knotsValues.append(0.0)
for i in range(1,nbrKnot-5): knotsValues.append(i/(nbrKnot-5.0))
for i in range(nbrKnot-3,nbrKnot): knotsValues.append(1.0)

for i in range( 0 , len(knotsValues) ):
    print(knotsValues[i])
    
#FILL ATTR
curve = ompy.MFnNurbsCurve()
cvs = positions
knots = knotsValues
form = curve.kOpen
is2D = False
rational = True
parent = ompy.MObject()
#CREATE CURVE
curve.create(cvs, knots, degree, form, is2D, rational , parent )
curve.updateCurve()






