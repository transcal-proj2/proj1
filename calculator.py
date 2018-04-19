# -*- coding: utf-8 -*-
from reader import Reader
from pprint import pprint
from solver import Solver
import numpy as np
import jsonpickle

# print(jsonpickle)
# np.set_printoptions(threshold=np.nan,edgeitems=6,linewidth=200)

class Calculator():
  def __init__(self, result = {}):
    self.result = result
    self.restrictedDofs = []

    self.sortAndReverseNodes()

    self.globalK = self.createGlobalK()
    self.forces = self.createForcesMatrix()
    self.us = self.createUs()
    self.deformacao, self.strains = self.calcDeformation()
    self.is_elastica(self.deformacao, self.strains, 900)
    
    for bar in self.result['bars']:
      print(bar.strain)


  def sortAndReverseNodes(self):
    #print("MATERIALS: ", self.result["element_groups"]["groups"][1].sectionArea)
    self.result['coordinates']['nodes'] = sorted(self.result['coordinates']['nodes'], key=lambda node: node.n)
    self.log("-> Nodes sorted and reversed \n")

  def log(self, input):
    print('[Calculator]', input)

  def createGlobalK(self):
    l = len(self.result['coordinates']['nodes']) * 2
    globalK = np.zeros((l, l))

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
          globalK[m[i][j][0]][m[i][j][1]] += bar.local[i][j]
            
    #print(self.globalK)
    restrictedX = list(filter(lambda n: n.xRestricted == True, self.result['coordinates']['nodes']))
    restrictedY = list(filter(lambda n: n.yRestricted == True, self.result['coordinates']['nodes']))
    
    for i in range(len(restrictedX)):
      self.restrictedDofs.append(restrictedX[i].dofx)
  
    for i in range(len(restrictedY)):
      self.restrictedDofs.append(restrictedY[i].dofy)

    self.restrictedDofs = np.flip(np.unique(self.restrictedDofs),0)
    # print(restrictedDofs)

    #self.globalK[5][5] = 40728.26
    print('GLOBAL K ANTES: \n', globalK, '\n')
    
    for rd in self.restrictedDofs:
      globalK = np.delete(globalK, rd, 0)
      globalK = np.delete(globalK, rd, 1)

    # print('GLOBAL K DEPOIS: \n', self.globalK, '\n')
    return globalK


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
    
    print("f: ", f)
    print(np.shape(f))

    print(self.restrictedDofs)

    for i in reversed(range(len(f))):
      # print(i)
      if i in self.restrictedDofs:
        f = np.delete(f, i, 0)

    # f = f[np.newaxis, :].T
    # print(np.shape(f))
    return f

  def createUs(self):
    print('getus \n')
    f = self.forces
    print('dofs presos:', self.restrictedDofs)
    # b = np.linalg.inv(self.globalK)
    # u = np.linalg.solve(self.globalK, f)  # Solution to the system a x = b
    solver = Solver(600, 10**-9, self.globalK, f)

    u = solver.gauss()[0]

    print("U sem corte: ", u)
    
    for i in np.flip(self.restrictedDofs, 0):
      #print(i)
      u = np.insert(u, i, 0)
    print('u = \n', u)


    print(self.result['coordinates']['nodes'])
    i = 0
    while i < len(u):
      self.result['coordinates']['nodes'][int(i/2)].deslocx = u[i]
      self.result['coordinates']['nodes'][int(i/2)].deslocy = u[i + 1]
      i += 2

    return u

  def calcDeformation(self):
    u = self.us
    deformacoes = []
    stresses = []
    for bar in self.result['bars']:
      currentU = []
      print("Barra: ", bar.id)
      print("Area: ", bar.group.sectionArea)
      print("GrupoID: ", bar.group.n)

      currentU.append(u[bar.startNode.dofx])
      currentU.append(u[bar.startNode.dofy])
      currentU.append(u[bar.endNode.dofx])
      currentU.append(u[bar.endNode.dofy])

      currentU = np.array(currentU)
      #print(np.shape(currentU))
      print("Current u: ", currentU)
      matrizCosSin = np.array([-1*bar.cos, -1*bar.sin, bar.cos, bar.sin])
      deformacao = np.dot(matrizCosSin, currentU)
      deformacao = deformacao * (1/bar.l)
      print("sin: {}, cos: {}".format(bar.sin, bar.cos))
      deformacoes.append(deformacao)
      print("N Bar: ", bar.id)
      print("Deformacao especifica: ", deformacao)
      bar.strain = deformacao

      #print("------------------")

      #f = (d[0]**2 + d[1]**2) ** 0.5
      #print(f)
      #df.append(f)

      stress = deformacao * bar.group.material.mde
      stresses.append(stress)
      bar.stress = stress
      
      print("Tensao: ", stress)
      print("------------------")

      if bar.startNode.xRestricted:
         reactionX = stress * bar.group.sectionArea * -bar.cos
         if(reactionX != 0):
           bar.startNode.rf[0] = reactionX
           print("no: {}, FX, valor: {}".format(bar.startNode.n, reactionX))
           print("------------------")
        
      if bar.startNode.yRestricted:
        reactionY = stress * bar.group.sectionArea * -bar.sin
        if(reactionY != 0):
          bar.startNode.rf[1] = reactionY
          print("no: {}, FY, valor: {}".format(bar.startNode.n, reactionY))
          print("------------------")

      if bar.endNode.xRestricted:
        reactionX = stress * bar.group.sectionArea * bar.cos
        if(reactionX != 0):
          bar.endNode.rf[0] = reactionX
          print("no: {}, FX, valor: {}".format(bar.endNode.n, reactionX))
          print("------------------")
      
      if bar.endNode.yRestricted:
        reactionY = stress * bar.group.sectionArea * bar.sin
        if(reactionY != 0):
          bar.endNode.rf[1] = reactionY
          print("no: {}, FY, valor: {}".format(bar.endNode.n, reactionY))
          print("------------------")

      # print("reactionY: ", reactionY)
      # print("current f: ", f)
      # print("current strain: ", strain)
    #print("df:\n {},\n strain:\n {}".format(df, strain))
    # print("df: ", df)
    # print("strains: ", strains)
    return deformacoes, stresses
      #print("dx: {}, dy: {}, f: {}".format(dx, dy, f))
      # print(bar.localSemEal)

  def is_elastica(self, deformacao, strains, admissivel):
    for i in range(len(self.result["bars"])) :
      aguenta = False
      #print("Tensao aplicada na barra {}: {}".format(self.result["bars"][i].id, strains[i]))
      if(strains[i] > admissivel):
        aguenta = True
        print("Barra {} nao permanece na fase elastica".format(self.result["bars"][i].id))

        newArea = (abs(strains[i]) * self.result["bars"][i].group.sectionArea)/admissivel
        print("Nova area da Barra {} deve ser de: {}".format(self.result["bars"][i].id, newArea))

      else:
        print("Barra {} permanece na fase elastica".format(self.result["bars"][i].id))

      #print

  def getResult(self):
    return self.result

  def getResultAsJSON(self):
    return jsonpickle.encode(self.result, unpicklable=False)

# reader = Reader()  
# result = reader.read('./input_p1.txt')
# # print(jr)
# calculator = Calculator(result)




