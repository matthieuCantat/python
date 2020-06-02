
import maya.cmds as mc
import python
import python.classe
reload( python.classe)
############################################################### MAYA CLASSE
#______________________________ IMPORT

import python.classe.mayaClasse as mClasse
reload( python.classe.mayaClasse )
mClasse = python.classe.mayaClasse.mayaClasse()

#______________________________ CREATE
mClasse.createFrom( updateValue =  0 )
mClasse.createFrom(1)
mClasse.createFrom('locator1')
mc.spaceLocator()
mClasse.createFrom(['locator1'])
mClasse.createFrom(['toto','tata'])
mClasse.printInfo()
#______________________________ save
pathTest = 'C:/Users/mcantat/Desktop/saveFileTest/toto.xml'
mClasse.toFile( pathTest )
mClasse.toMayaObjAttr( 'locator1' )
#______________________________ load
mClasse.createFromFile( pathTest )
mClasse.createFromMayaObjAttr( 'locator1' )

############################################################### TRS

import python.classe.trs 
reload( python.classe.trs )
trsClasse = python.classe.trs.mayaClasse()






