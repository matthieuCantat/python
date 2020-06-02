import os

# GET CURRENT PATH
arrayPath = __file__.split('\\')
selfPath  = '/'.join(arrayPath[0:-1]) + '/'

# LIST ALL FOLDER CHILD
folders  = []
pyFiles  = []
for child in os.listdir( selfPath ):
	if not( '.' in child         ): folders.append( child )
	elif( child == '__init__.py' ): pass
	elif( '.py' == child[-3:]    ): pyFiles.append( child.split('.')[0] )

__all__ = folders + pyFiles

'''

import os

# get the path
arrayPath = __file__.split('\\')
selfPath  = '/'.join(arrayPath[0:-1]) + '/'

# list tous les fichier .py 
__all__ = []
for elem in os.listdir( selfPath ):
	if( '.py' == elem[ -3 : len(elem) ] ) and not( elem == '__init__.py' ) and not( elem == '_buildRigClassTPL.py' ):
		__all__.append( elem.split('.')[0] )
'''

'''
# import tous les fichier .py
for elem in __all__:
	print( 'import ' + elem )
	exec('import {0}'.format( elem ) )
'''