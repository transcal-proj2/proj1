import numpy as np

class Solver():
  def __init__(self, ite, tol, k, f):
    self.ite = ite
    self.tol = tol
    self.k = k
    self.f = f    

  def jacobi(self):
    u = []
    height = np.shape(self.k)[0]
    for i in range(height):
      u.append([0])

    for j in range(self.ite):
            
      maior_erro = 0

      for l in range(height):
        temp = self.f[l] / self.k[l][l]
        
        for w in range(1,height):
          temp -= ((self.k[l][w-1] * u[w-1][0]) / (self.k[l][l]))

        if(temp == 0):
          erro = (temp - u[l][0])

        else:
          erro = (temp - u[l][0])/temp

        if(erro > maior_erro):
          maior_erro = erro

        u[l][0] = temp

        print(erro)
          
      if(maior_erro <= self.tol):
        return u, maior_erro
        ##u[l] = temp
    return u, maior_erro

        #u[k] = ( self.f[k[k][height] / k[height][0] ) * u[k+1]] / k[0][k] ) - ( k
        
      

    print(u)

k = np.array([[3, -1, 0, 0], [-1, 3, 0, -2], [0, 0, 3, 1], [0, -2, 1, 3]])
k = k * 5 * (10 ** 4)
f = [[0],[0],[0],[1000]]
print(k)
solver = Solver(100, 10**-3, k, f)
print(solver.jacobi())




