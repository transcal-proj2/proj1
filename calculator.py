from reader import Reader
from pprint import pprint
import numpy as np
import jsonpickle

print(jsonpickle)
np.set_printoptions(threshold=np.nan,edgeitems=6,linewidth=200)


class Calculator():
  def __init__(self, result = {}):
    self.result = result
    self.sortAndReverseNodes()
    self.globalK = self.createGlobalK()
    self.restrictedDofs = []

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
            
    #print(self.globalK)
    restrictedX = list(filter(lambda n: n.xRestricted == True, self.result['coordinates']['nodes']))
    restrictedY = list(filter(lambda n: n.yRestricted == True, self.result['coordinates']['nodes']))
    
    for i in range(len(restrictedX)):
      self.restrictedDofs.append(restrictedX[i].dofx)
  
    for i in range(len(restrictedY)):
      self.restrictedDofs.append(restrictedY[i].dofy)

    self.restrictedDofs = np.flip(np.unique(self.restrictedDofs),0)
    # print(restrictedDofs)

    print('GLOBAL K ANTES: \n', self.globalK, '\n')

    for rd in self.restrictedDofs:
      self.globalK = np.delete(self.globalK, rd, 0)
      self.globalK = np.delete(self.globalK, rd, 1)

    # print('GLOBAL K DEPOIS: \n', self.globalK, '\n')


  def createForcesMatrix(self):
    fShape = np.shape(self.result['coordinates']['nodes'])[0] * 2
    f = np.zeros(fShape)
    for node in self.result['coordinates']['nodes']:
      fx = 0
      fy = 0
      for load in node.loads:
        if load.direction == 1:
          fx += load.value 
        if load.direction == 2:
          fy += load.value
      f[node.dofx] = fx
      f[node.dofy] = fy
    
    print(f)
    print(np.shape(f))

    print(self.restrictedDofs)

    for i in reversed(range(len(f))):
      # print(i)
      if i in self.restrictedDofs:
        f = np.delete(f, i, 0)

    # f = f[np.newaxis, :].T
    # print(np.shape(f))
    return f

  def getUs(self):
    print('getus \n')
    f = self.createForcesMatrix()
    print('dofs presos:', self.restrictedDofs)
    # b = np.linalg.inv(self.globalK)
    u = np.linalg.solve(self.globalK, f)  # Solution to the system a x = b
    print(u)
    
    for i in np.flip(self.restrictedDofs, 0):
      print(i)
      u = np.insert(u, i, 0)
    print('u = \n', u)
    return u

  def calcDeformation(self):
    u = self.getUs()
    df = []
    strains = []
    for bar in self.result['bars']:
      currentU = []
    
      currentU.append(u[bar.startNode.dofx])
      #print(bar.startNode.dofx)
      currentU.append(u[bar.startNode.dofy])
      #print(bar.startNode.dofy)
      currentU.append(u[bar.endNode.dofx])
      #print(bar.endNode.dofx)
      currentU.append(u[bar.endNode.dofy])
      #print(bar.endNode.dofy)
      #print("alo")
      currentU = np.array(currentU)
      #print(np.shape(currentU))
      #print("Current u: ", currentU)

      d = np.dot(currentU, bar.localSemEal)
      d = d * (1/bar.l)
      #print("current d: ", d)
      #dx = d[0] + d[2]
      #dy = d[1] + d[3]
      
      f = (d[0]**2 + d[1]**2) ** 0.5
      #print(f)
      df.append(f)

      strain = f * bar.group.material.mde
      strains.append(strain)

      if bar.startNode.xRestricted:
        reactionX = strain * bar.group.sectionArea * bar.cos
        if(reactionX != 0):
          print("n: {}, FX, valor: {}".format(bar.startNode.n, reactionX))
        
      if bar.startNode.yRestricted:
        reactionY = strain * bar.group.sectionArea * bar.sin
        if(reactionY != 0):
          print("n: {}, FY, valor: {}".format(bar.startNode.n, reactionY))

      if bar.endNode.xRestricted:
        reactionX = strain * bar.group.sectionArea * bar.cos
        if(reactionX != 0):
          print("n: {}, FX, valor: {}".format(bar.endNode.n, reactionX))
      
      if bar.endNode.yRestricted:
        reactionY = strain * bar.group.sectionArea * bar.sin
        if(reactionY != 0):
          print("n: {}, FY, valor: {}".format(bar.endNode.n, reactionY))

      # print("reactionY: ", reactionY)
      # print("current f: ", f)
      # print("current strain: ", strain)
    #print("df:\n {},\n strain:\n {}".format(df, strain))
    # print("df: ", df)
    # print("strains: ", strains)
    return df, strains
      #print("dx: {}, dy: {}, f: {}".format(dx, dy, f))
      # print(bar.localSemEal)
  
reader = Reader()  
result = reader.read('./input.txt')
# jr = jsonpickle.encode(result,unpicklable=False)
# print(jr)
calculator = Calculator(result)
calculator.calculate()
# calculator.createForcesMatrix()
# calculator.getUs()
calculator.calcDeformation()



