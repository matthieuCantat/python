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


#__all__ = [ 'classe'  , 'plugIn'  , 'script'  , 'utils' , 'projects' ]


'''
for elem in __all__:
	print('import ' + elem)
	exec('import {0}'.format( elem ) )

'''
