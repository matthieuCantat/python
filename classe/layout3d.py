
import math
import copy

import maya.cmds as mc
import maya.OpenMaya as om
import maya.api.OpenMaya as ompy

from ..utils import utilsMaya
from ..utils import utilsPython
from ..utils import utilsMath
from ..utils import utilsMayaApi

from . import trs
from . import coords
from . import boundingBox2d

class layout3d(mayaClasse):
	
	'''
	#_________________________________________________________________ATTRS

	#_________________________________________________________________UTILS
	'''

	def __init__(self):



	def createCanvasFromObjs( self , objs ):
		bb2d  = boundingBox2d.boundingBox2d()
		self.canvas = []
		for obj in objs:
			bb2d.createFromObj( obj )
			self.canvas.append( copy.copy(bb2d) )


	def createBlockFromObjs( self , objs ):
		bb2d  = boundingBox2d.boundingBox2d()
		self.blocks = []
		for obj in objs:
			bb2d.createFromObj( obj )
			self.blocks.append( copy.copy(bb2d) )

	def createPicturesFromObjs( self , objs ):
		bb2d  = boundingBox2d.boundingBox2d()
		self.pictures = []
		for obj in objs:
			bb2d.createFromObj( obj )
			self.pictures.append( copy.copy(bb2d) )

	def getAllLayoutPoints( self ):
		points = []
		for block in self.blocks:
			points += block.squareCoords
		for canva in self.canvas:
			points += canva.squareCoords

		return points



	#_________________________________________________________________MODIF

	self.objToPresent = []
	self.camera       = []
	self.pictures     = []
	self.layoutType   = ''


	def initLayout( self , persp ):
		pass

	def initMayaObj( mayaObj ):
		pass

	def modifMayaObjsLayout( self , layoutType ):
		pass


	def setPictures( self , pictures , accuracy , foreGround = 0 ):
		pass
