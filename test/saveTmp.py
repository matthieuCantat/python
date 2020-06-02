import maya.cmds as mc

selection = mc.ls( sl = True )

baseName = ''
father = ''
for elem in selection:
    if( elem[-4:] == '_GEO' ):
        baseName = elem
        father = mc.listRelatives( elem , p = True )[0]
        
for elem in selection:
    mc.setAttr( elem + '.v' , 0 )
    if not( elem == baseName ):
        mc.parent( elem ,  father )
        mc.rename( elem , baseName + 'low' )
        
        