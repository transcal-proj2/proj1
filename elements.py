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
    self.dofx = (self.n * 2) - 2
    self.dofy = (self.n * 2) - 1
    self.deslocx = 0
    self.deslocy = 0
    self.rf = [0, 0, 0] # reaction forces

  def show(self):
    pprint(vars(self))

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
    self.localSemEal = None # np.array
    self.strain = None # deformacao
    self.stress = None # tensao

  def setGroup(self,group):
    self.group = group
  def calculateLength(self):
    dx = self.startNode.x - self.endNode.x
    dy = self.startNode.y - self.endNode.y
    return math.sqrt(dx**2 + dy**2)

  def calculateDegree(self):
    dx = self.endNode.x - self.startNode.x
    
    dy = self.endNode.y - self.startNode.y
    self.sin = dy/self.l
    #print("SInnnnn: ", self.sin)
    self.cos = dx/self.l
    #print("COSSSS: ", self.cos)

  def createLocalArray(self):
    c2 = self.cos**2
    s2 = self.sin**2
    cs = self.cos * self.sin
    print('mde:',type(self.group.material.mde), ' section area:',self.group.sectionArea, 'l:', type(self.l))
    eal = (self.group.material.mde * self.group.sectionArea) / self.l
    local = np.array([
      [c2, cs, -1*c2, -1*cs],
      [cs, s2, -1*cs, -1*s2],
      [-1*c2, -1*cs, c2, cs],
      [-1*cs, -1*s2, cs, s2],
    ])
    self.localSemEal = local
    # print("LOCAL \n",local)
    self.local = local * eal

    print('\n bar',self.id,'\n',self.local)
    print(
    """Start node: {} End Node: {}
    sin: {} cos: {}
    """
    .format(self.startNode.n,self.endNode.n, self.sin, self.cos))

  def show(self):
    pprint(vars(self))

class Load():
  def __init__(self, direction, value):
    self.direction = int(direction)
    self.value = float(value)

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
