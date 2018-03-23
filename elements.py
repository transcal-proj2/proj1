class Node():
  def __init__(self,n,x,y):
    self.n = n
    self.x = x
    self.y = y

class Bar():
  def __init__(self, startNode, endNode, group = None, material = None):
    self.startNode = startNode
    self.endNode = endNode
    self.group = group
    self.material = material

class Material():
  def __init__(self, mde, tta, tca):
    self.mde = mde
    self.tta = tta
    self.tca = tca
