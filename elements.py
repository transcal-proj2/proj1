from pprint import pprint
import math
import numpy as np

class Node():
  def __init__(self,n,x,y):
    self.n = int(n)
    self.x = float(x)
    self.y = float(y)
    self.xRestricted = False
    self.yRestricted = False
    self.loads = []
    # self.dof = 0 / -1 / 1

  def addLoad(self, load):
    self.loads.append(load)
  
  def setRestriction(self, axis):
    if axis == 1:
      self.xRestricted = True
    elif axis == 2:
      self.yRestricted = True

class Bar():
  def __init__(self, id, startNode, endNode, group = None):
    self.id = id
    self.startNode = startNode
    self.endNode = endNode
    self.group = group
    self.l = self.calculateLength()
    self.sin = None
    self.cos = None
    self.calculateDegree()
    self.local = None # np.array

  def calculateLength(self):
    dx = abs(self.startNode.x - self.endNode.x)
    dy = abs(self.startNode.y - self.endNode.y)
    return math.sqrt(dx**2 + dy**2)

  def calculateDegree(self):
    dx = abs(self.startNode.x - self.endNode.x)
    dy = abs(self.startNode.y - self.endNode.y)
    self.sin = dy/self.l
    self.cos = dx/self.l

  def createLocalArray(self):
    c2 = self.cos**2
    s2 = self.sin**2
    cs = self.cos * self.sin
    # print('mde:',type(self.group.material.mde), ' section area:',type(self.group.sectionArea), 'l:', type(self.l))
    eal = (self.group.material.mde * self.group.sectionArea) / self.l
    local = np.array([
      [c2, cs, -1*c2, -1*cs],
      [cs, s2, -1*cs, -1*s2],
      [-1*c2, -1*cs, c2, cs],
      [-1*cs, -1*s2, cs, s2],
    ])

    self.local = local * eal
    print(self.local)

  def show(self):
    pprint(vars(self))

class Load():
  def __init__(self, direction, value):
    self.direction = direction
    self.value = value

class Material():
  def __init__(self, mde, tta, tca):
    self.mde = float(mde)
    self.tta = float(tta)
    self.tca = float(tca)

  def show(self):
    pprint(vars(self))

class Group():
  def __init__(self, n, amount, elementType, material = None):
    self.n = int(n)
    self.amount = int(amount)
    self.elementType = elementType
    self.material = material
    self.sectionArea = None

  def setMaterial(self, material):
    self.material = material

  def setSectionArea(self, sectionArea):
    self.sectionArea = float(sectionArea)
