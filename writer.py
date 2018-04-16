from elements import Node, Bar, Material, Group, Load
from pprint import pprint

# query
#  next((e for e in result['coordinates']['nodes'] if e.n == int(el[0])), None)

class Writer():
  def __init__(self, result):
    self.result = result
    self.file = open('arquivoSaida.out', 'w')
    pprint(result)
    self.writeDisplacements()
    self.writeReactionForces()
    self.writeElementStrains()
    self.writeElementStresses()
  
  def write(self, string):
    self.file.write(string + '\n')

  def writeDisplacements(self):
    self.write('*DISPLACEMENTS')
    for node in self.result['coordinates']['nodes']:
      self.write("{} {} {}".format(node.n, node.deslocx, node.deslocy))
    self.write('')

  def writeReactionForces(self):
    self.write('*REACTION_FORCES')
    for node in self.result['coordinates']['nodes']:
      if node.rf[0] != 0:
        self.write("{} FX = {}".format(node.n, node.rf[0]))
      if node.rf[1] != 0:
        self.write("{} FY = {}".format(node.n, node.rf[1]))
    self.write('')

  def writeElementStrains(self):
    self.write('*ELEMENT_STRAINS')
    for bar in self.result['bars']:
      self.write("{} {}".format(bar.id, bar.strain))
    self.write('')

  def writeElementStresses(self):
    self.write('*ELEMENT_STRESSES')
    for bar in self.result['bars']:
      self.write("{} {}".format(bar.id, bar.stress))
