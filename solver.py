import numpy as np
from decimal import Decimal

class Solver():
  def __init__(self, ite, tol, k, f):
    self.ite = ite
    self.tol = tol
    self.k = k
    self.f = f    

  def gauss(self):
    u = []
    height = np.shape(self.k)[0]

    for i in range(height):
      u.append(0)


    for j in range(self.ite):
      print('----- Iteração {} -----'.format(j))
      maior_erro = 0
      

      for l in range(height):
        temp = self.f[l] / self.k[l][l]
        #print(self.k[l][l])

        for w in range(height):
          if (w != l):
            temp -= ((self.k[l][w] * u[w]) / (self.k[l][l]))
          
        if (temp == 0):
          erro = abs(temp - u[l])
        else:
          erro = abs((temp - u[l])/temp) 

        if (erro > maior_erro):
          maior_erro = erro

        u[l] = temp
        # print('e:',erro)

      print(u)
      if (maior_erro <= self.tol):
        return u, maior_erro
        ##u[l] = temp
    return u, maior_erro

        #u[k] = ( self.f[k[k][height] / k[height][0] ) * u[k+1]] / k[0][k] ) - ( k

  def jacobi(self):
    u = []
    height = np.shape(self.k)[0]

    for i in range(height):
      u.append(0)


    for j in range(self.ite):
      print('----- Iteração {} -----'.format(j))
      maior_erro = 0
      uite = u

      for l in range(height):
        temp = self.f[l] / self.k[l][l]

        for w in range(height):
          if (w != l):
            temp -= ((self.k[l][w] * uite[w]) / (self.k[l][l]))

        u[l] = temp
 
        if(j > 0):
          if (temp == 0):
            print("alo")
            print(uite[l])
            erro = abs((temp - uite[l]))
          else:
            erro = abs((temp - uite[l])/temp)

          print("erro: ",erro)

          if (erro > maior_erro):
            maior_erro = erro


      print('maior erro: ',maior_erro)

      if (maior_erro <= self.tol):
        return u, maior_erro
        ##u[l] = temp
    return u, maior_erro


k = np.array([[3, -1, 0, 0], [-1, 3, 0, -2], [0, 0, 3, 1], [0, -2, 1, 3]])
k = k * 5 * (10 ** 4)
f = [0,0,0,-100]
# print(k)
solver = Solver(600, 10**-9, k, f)
print(k)
teste = solver.jacobi()
print("Matriz de Us: ", teste[0])
print("Erro: ", teste[1])
# teste = [x for el in teste]




