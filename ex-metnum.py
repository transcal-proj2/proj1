import numpy as np
import math

l = 2 # params
a = 0.02 # Area da seção transversal
e = 200 * (10**9) # módulo de elasticidade
p = 50 * (10**3) # carga aplicada na ext da barra


forcas = np.array([
  [0],
  [p]
])

k = (e * a) / l

r = np.array([
  [ 1,-1],
  [-1, 1]
])

print('R:\n',r)

# r_inv = np.linalg.inv(k*r)
# print('R_inv',r_inv)

print('K:',k)
print('F:',forcas)
us = forcas * (1/k)
print('Result :\n',us)

d = us/l #deformacao

print('Deformação:\n',d)

t = forcas/a #tensao
print("Tensões: \n{} ".format(t))
