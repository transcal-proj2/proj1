from pprint import pprint

class Node():
  def __init__(self,n,x,y):
    self.n = int(n)
    self.x = x
    self.y = y
    self.xRestricted = False
    self.yRestricted = False
    self.loads = []

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


class Group():
  def __init__(self, n, amount, elementType, material = None):
    self.n = int(n)
    self.amount = int(amount)
    self.elementType = elementType
    self.material = material
    self.sectionArea = None;

  def setMaterial(self, material):
    self.material = material

  def setSectionArea(self, sectionArea):
    self.sectionArea = sectionArea