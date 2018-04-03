from reader import Reader
from pprint import pprint
import numpy as np

class Calculator():
  def __init__(self, result = {}):
    self.result = result
    self.sortAndReverseNodes()
    # self.local = nu

  def sortAndReverseNodes(self):
    self.result['coordinates']['nodes'] = sorted(self.result['coordinates']['nodes'], key=lambda node: node.n)
    self.result['coordinates']['nodes'].reverse()

    # for node in self.result['coordinates']['nodes']:
    #   print(node.n)
    self.log("-> Nodes sorted and reversed \n")

  # def 
  # def solve()

  def log(self, input):
    print('[Calculator]', input)

reader = Reader()
result = reader.read('./input.txt')
calculator = Calculator(result)





