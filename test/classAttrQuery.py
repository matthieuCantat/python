
import inspect
import types 


#DEF

def utils_getClasseAttributeNames( classeInstance ):
	attributes = inspect.getmembers( classeInstance , lambda a:not( inspect.isroutine(a) ) )
	attributes = [a[0] for a in attributes if not(a[0].startswith('__') and a[0].endswith('__'))]
	return attributes			


def utils_classeToDictAttrValue( classeInstance ):
	attributes = utils_getClasseAttributeNames(classeInstance)

	dictAttrToValue = {}
	lap = 0

	while not( len(attributes) == 0 ):
		lap += 1
		if( 500 < lap ):
			mc.error()
		
		attributesToRemove = []    
		for i in range( 0 , len(attributes) ):
			print('================ {}'.format(i))
			print(attributes[i])
			print('{}.{}'.format( 'classeInstance' , attributes[i] ))
			attrValue = eval( '{}.{}'.format( 'classeInstance' , attributes[i] ) )
			attrType = type( attrValue )
			print(attrType)			
			if( attrType == types.InstanceType ):	
							    
				subAttributes = utils_getClasseAttributeNames( attrValue )

				subAttributes = [ '{}.{}'.format( attributes[i] , sub ) for sub in subAttributes ]
				print(subAttributes)
				attributes += subAttributes
				
				dictAttrToValue[ attributes[i] ] = attrValue				
				attributesToRemove.append(attributes[i])					
						
			else:
				dictAttrToValue[ attributes[i] ] = attrValue
				attributesToRemove.append(attributes[i])

		for a in attributesToRemove:
		    attributes.remove(a)
	
	return dictAttrToValue

	
#TEST


class parents(object):  
    def __init__(self):
        self.attrA = 'toto'
        self.attrB = ['a' , 'b' , 'c' ]    
        
class child(parents):  
	def __init__(self):
		parents.__init__(self)
		#super(parent, self).__init__()
		self.attrC = [ 1 , 2 , 3 , 4 ]
		self.Class = classAttrA()

class classAttrA():
    def __init__(self):
        self.toto = [ 3 , 4 , 5 ]
        self.tata = 'tata'

instanceA = child()
utils_classeToDictAttrValue(instanceA)
	
	