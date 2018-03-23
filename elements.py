from pprint import pprint

class Node():
  def __init__(self,n,x,y):
    self.n = n
    self.x = x
    self.y = y

class Bar():
  def __init__(self, id, startNode, endNode, group = None, material = None):
    self.id = id
    self.startNode = startNode
    self.endNode = endNode
    self.group = group
    self.material = material

  def show(self):
    pprint(vars(self))

class Material():
  def __init__(self, mde, tta, tca):
    self.mde = mde
    self.tta = tta
    self.tca = tca

class Group():
  def __init__(self, n, amount, elementType):
    self.n = int(n)
    self.amount = int(amount)
    self.elementType = elementType
