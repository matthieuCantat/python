
#___________________________________________________________ EXEC EVAL & INSTANCE STRING FORMAT

'''
exec execute itself inside the encapsulation and not outside. 
so we can use the variabe inside the encapsulation
no need to transform them into string
wich is handy for the instance
'''

class A():
    def __init__(self):
        self.value = "classA"

class B():
    def __init__(self):
        self.value = "classB"

class useExec():
    def __init__( self ):    
        self.instanceA = A()
        self.instanceB = B()
        
    def printValueError(self):
        letters = [ 'A' , 'B' ]
        for letter in letters:
            exec( 'print( "print using exec", {}.instance{}.value)'.format( self , letter) )
            value = eval( '{}.instance{}.value'.format( self , letter) )      
            print('print using eval' , value )
            
    def printValueFixed(self):
        letters = [ 'A' , 'B' ]
        for letter in letters:
            exec( 'print( "print using exec", self.instance{}.value)'.format(  letter) )
            value = eval( 'self.instance{}.value'.format( letter) )      
            print('print using eval' , value )
      
      
test = useExec()
try:    
    test.printValueError()
except:
    print('error in test.printValueError() ')
else:
    print('test.printValueError() is good')
    
try:    
    test.printValueFixed()
except:
    print('error in test.printValueFixed() ')
else:
    print('test.printValueFixed() is good')



#___________________________________________________________ INHERITANCE AND PYTHON 2.7
'''
THE FOLLOW LINES GAVE ME AN ERROR
'''

#========================= OLD CLASSE INERITANCE
class A(): 
    def __init__( self ):
        print('init A')

class B(A):
    def __init__( self ):
        A.__init__()         # ERROR!!! MUST ADD Self
        print('init B')


test = B()
test = A()

#========================= OLD CLASSE INERITANCE
'''
I THOUGHT IT WAS A PROBLEM OF OLD CLASS AND MULTI INERITANCE BUT IN FACT I FORGOT A SELF
IN THE AGRUMENT OF INIT OF THE SUPER CLASSE
'''

class A(): 
    def __init__( self ):
        print('init A')

class B(A):
    def __init__( self ):
        A.__init__(self)          # DONE !
        print('init B')


test = B()
test = A()

#========================= OLD CLASSE INERITANCE -SOLUTION-
'''
THAT'S HOW IT WORKS WITH SOME ARGS 
'''

class A(): 
    def __init__( self, **args  ):
        name  = args.get( 'n'     , None ) 
        print('init A === args: ' , name )

class B(A):
    def __init__( self, **args  ):
        A.__init__( self , **args )
        shape  = args.get( 'shape'     , None )
        print('init B === args: ' , shape )


test = B( n = 'toto' , shape = 'sisi' )
test = A()


#========================= SUPER INERITANCE

'''
SO I TRIED SUPER FOR HERITANCE BUT IT DIDNT WORK ( TYPE ERROR )
BECAUSE MY CLASS IS AN OLD PYTHON CLASS, IT MUST BE UPGRADE WITH THE CLASS "object"
'''


class A():                  # PUT AN OBJECT
    def __init__( self ):
        print('init A')

class B(A):
    def __init__( self ):
        super( B , self ).__init__()
        print('init B')

test = B()
test = A()



#========================= SUPER INERITANCE NEW CLASS
'''
HERE THAT'S WORKING FINE, EXEPT IF THIS EXEMPLE IS IN A FILE AND YOU IMPORT IT, TRY IT
AND RELOAD IT. IT THROW A TYPE ERROR!
THE RELOADING DOESNT WORK WITH SUPER... I NEED TO TEST MY CODE AND RELOAD IT A LOT
THE IS A SOLUTION ON THE NET BUT SOUNDS COMPLICATED...
SO I THINK I WILL AVOID SUPER
'''
class A(object):             #DONE
    def __init__( self ):
        print('init A')

class B(A):
    def __init__( self ):
        super( B , self ).__init__()
        print('init B')

test = B()
test = A()


#========================= SUPER INERITANCE NEW CLASS ARGS
'''
THAT'S HOW IT WORKS WITH SOME ARGS 
'''
class A(object): 
    def __init__( self, **args  ):
        name       = args.get( 'n'     , None ) 
        print('init A')
        print(name)

class B(A):
    def __init__( self, **args  ):
        super( B , self ).__init__( **args )
        print('init B')


test = B( n = 'toto' , shape = 'sisi' )
test = A()



#___________________________________________________________ COPY / DEEF COPY with attr array... ref or no ref?



#_________________________________REF IN VARIABLE
#REF IN STRING
a = 'matthieu'
b = a
print( 'a' , a)
print('b',b)

a = 'bruno'
print( 'a' , a)
print( 'b' , b )

print('b contain a string - no ref')

#REF IN ARRAY
a = ['matthieu']
b = a
print( 'a' , a)
print('b',b)

a = ['bruno' ]
print( 'a' , a)
print( 'b' , b )

print('b contain an array - no ref')

#REF IN ARRAY2
a = ['matthieu']
b = a
print( 'a' , a)
print('b',b)

a[0] = 'bruno'
print( 'a' , a)
print( 'b' , b )

print('b contain an array - REF')


#REF IN ARRAY3
a = ['matthieu']
b = a
print( 'a' , a)
print('b',b)

a.append( 'bruno' )
print( 'a' , a)
print( 'b' , b )

print('b contain an array -  REF')


#REF IN DICTINARY
a = { 'name' : 'matthieu'}
b = a
print( 'a' , a)
print('b',b)

a = { 'name' : 'bruno'}
print( 'a' , a)
print( 'b' , b )

print('b contain a dict - no ref')


'''
     list and dict
'''

tata = [ 1 , 2 , 3 , 4 ]
toto = {'test':tata}
tata = [ 0 ]
print( toto)
print('b contain a dict - no ref')

tata = [ 1 , 2 , 3 , 4 ]
toto = {'test':copy.copy(tata)}
tata = [ 0 ]
print( toto)
print('b contain a dict - no ref')

tata = [ 1 , 2 , 3 , 4 ]
toto = {'test':tata}
tata.append(5)
print( toto)
print('b contain a dict - REF')

tata = [ 1 , 2 , 3 , 4 ]
toto = {'test':tata}
tata[1] = 99999
print( toto)
print('b contain a dict - REF')

#_________________________________REF IN ARRAY
a = ['matthieu']

for elem in a:
    elem = 'bruno'

print(a)

print('b contain an array -  REF')


a = ['matthieu']

for i in range( 0 , len(a) ):
    a[i] = 'bruno'

print(a)

print('b contain an array -  REF')

#_________________________________REF IN ARGS DEF
def modify( b , value ):
    b = value

#REF IN BOOL
a = False
modify(a , True )
print(a)

#_________________________________REF IN ClASSES
class variableHolder():
    
    def __init__( self ):
        self.a = True
        self.b = self.a
        self.array = [ 0 , 1 , 2 , 3 , 4 ]

Vh = variableHolder()
print( Vh.a  , Vh.b )
Vh.a = False
print( Vh.a  , Vh.b )


Vh = variableHolder()
Vh.b = Vh.a
print( Vh.a  , Vh.b )
Vh.a = False
print( Vh.a  , Vh.b )

print( Vh.b  )
modify( Vh.b , False )  
print( Vh.b  )  



#_________________________________copy IN ClASSES
import copy 

'''
     bool in class'attr
'''
Vh = variableHolder()
Vhcopy     = copy.copy(Vh)
VhDeepcopy = copy.deepcopy(Vh)


print( 'origin' , 'copy' , 'deepcopy'  )
print( Vh.a , Vhcopy.a , VhDeepcopy.a  )
Vh.a = False
print( Vh.a , Vhcopy.a , VhDeepcopy.a  )
print('no ref for bool')


'''
     float in class'attr
'''
Vh = variableHolder()
Vh.a = 0.1
Vhcopy     = copy.copy(Vh)
VhDeepcopy = copy.deepcopy(Vh)


print( 'origin' , 'copy' , 'deepcopy'  )
print( Vh.a , Vhcopy.a , VhDeepcopy.a  )
Vh.a = 0.999999
print( Vh.a , Vhcopy.a , VhDeepcopy.a  )
print('no ref for float')



'''
    class instance in in class'attr
'''
Vh = variableHolder()
Vh.a = variableHolder()
Vhcopy     = copy.copy(Vh)
VhDeepcopy = copy.deepcopy(Vh)

print( 'origin' , 'copy' , 'deepcopy'  )
print( Vh.a.a , Vhcopy.a.a , VhDeepcopy.a.a  )
Vh.a.a = False
print( Vh.a.a , Vhcopy.a.a , VhDeepcopy.a.a  )
print('ref in copy , no ref in deepcopy ')

'''
    list in in class'attr
'''

Vh = variableHolder()
Vh.a = [ 5 , 9 , 1 ]
Vhcopy     = copy.copy(Vh)
VhDeepcopy = copy.deepcopy(Vh)

print( 'origin' , 'copy' , 'deepcopy'  )
print( Vh.a , Vhcopy.a , VhDeepcopy.a  )
Vh.a[0] = 'toto'
print( Vh.a , Vhcopy.a , VhDeepcopy.a  )
print('ref in copy , no ref in deepcopy ')


'''
    dict in in class'attr
'''

Vh = variableHolder()
Vh.a = {'A' : 1 , 'B' : 2 }
Vhcopy     = copy.copy(Vh)
VhDeepcopy = copy.deepcopy(Vh)

print( 'origin' , 'copy' , 'deepcopy'  )
print( Vh.a , Vhcopy.a , VhDeepcopy.a  )
Vh.a['ZZZ'] = 999
print( Vh.a , Vhcopy.a , VhDeepcopy.a  )
print('ref in copy , no ref in deepcopy ')




'''
    list that contain a class instance in in class'attr
'''

Vh = variableHolder()
Vh.a = [ 5 , 9 , variableHolder() ]
Vhcopy     = copy.copy(Vh)
VhDeepcopy = copy.deepcopy(Vh)

print( 'origin' , 'copy' , 'deepcopy'  )
print( Vh.a , Vhcopy.a , VhDeepcopy.a  )
print( Vh.a[2].a , Vhcopy.a[2].a , VhDeepcopy.a[2].a  )
Vh.a[0] = 'toto'
Vh.a[2].a = False
print( Vh.a , Vhcopy.a , VhDeepcopy.a  )
print( Vh.a[2].a , Vhcopy.a[2].a , VhDeepcopy.a[2].a  )
print('ref in copy , no ref in deepcopy ')




#___________________________________________UPPER CASE
toto = 'AHAHA'
toto.isUpper()


#___________________________________________DICO FORMAT ERROR
print("dico = {'toto':333}".format('toto') ) # error
print("dico = {'toto':333}" )# no error
print("dico = \{'toto':333\}".format('toto') ) # error



#_________________________________________ ref in proc args


def incrVarA( var ):
    var += 1

varTest = 0
incrVarA(varTest)
print(varTest)


def incrVarB( var ):
    var[0] += 1

varTest = [0]
incrVarB(varTest)
print(varTest)
