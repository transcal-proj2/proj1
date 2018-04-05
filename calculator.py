from reader import Reader
from pprint import pprint
import numpy as np
np.set_printoptions(threshold=np.nan,edgeitems=6,linewidth=200)


class Calculator():
  def __init__(self, result = {}):
    self.result = result
    self.sortAndReverseNodes()
    self.globalK = self.createGlobalK()

  def createGlobalK(self):
    l = len(self.result['coordinates']['nodes']) * 2
    zeroedGlobal = np.zeros((l, l))
    # print("global created: \n", zeroedGlobal)
    return zeroedGlobal
    
  def sortAndReverseNodes(self):
    self.result['coordinates']['nodes'] = sorted(self.result['coordinates']['nodes'], key=lambda node: node.n)
    # self.result['coordinates']['nodes'].reverse()

    # for node in self.result['coordinates']['nodes']:
    #   print(node.n)
    self.log("-> Nodes sorted and reversed \n")

  def log(self, input):
    print('[Calculator]', input)

  def calculate(self):
    # print(self.globalK)

    for bar in self.result['bars']:
      # print(bar.id)
      s = bar.startNode
      e = bar.endNode
      # a = np.array([[[s.dofx], [s.dofy], [e.dofx], [e.dofy]]])
      # b = a[np.newaxis, :].T
      m = np.array([
        [[s.dofx, s.dofx], [s.dofx, s.dofy], [s.dofx, e.dofx], [s.dofx, e.dofy]],
        [[s.dofy, s.dofx], [s.dofy, s.dofy], [s.dofy, e.dofx], [s.dofy, e.dofy]],
        [[e.dofx, s.dofx], [e.dofx, s.dofy], [e.dofx, e.dofx], [e.dofx, e.dofy]],
        [[e.dofy, s.dofx], [e.dofy, s.dofy], [e.dofy, e.dofx], [e.dofy, e.dofy]],
      ])
      
      for i in range(4):
        for j in range(4):
          self.globalK[m[i][j][0]][m[i][j][1]] += bar.local[i][j]
            
      # print(self.globalK)
    restrictedDofs = []
    restrictedX = list(filter(lambda n: n.xRestricted == True, self.result['coordinates']['nodes']))
    restrictedY = list(filter(lambda n: n.yRestricted == True, self.result['coordinates']['nodes']))
    
    for i in range(len(restrictedX)):
      restrictedDofs.append(restrictedX[i].dofx)
  
    for i in range(len(restrictedY)):
      restrictedDofs.append(restrictedY[i].dofy)

    restrictedDofs = np.flip(np.unique(restrictedDofs),0)
    # print(restrictedDofs)

    for rd in restrictedDofs:
      self.globalK = np.delete(self.globalK, rd, 0)
      self.globalK = np.delete(self.globalK, rd, 1)

    print(self.globalK)
    

reader = Reader()
result = reader.read('./input.txt')
calculator = Calculator(result)
calculator.calculate()




