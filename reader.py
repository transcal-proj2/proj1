from elements import Node, Bar, Material, Group, Load
from pprint import pprint

# query
#  next((e for e in result['coordinates']['nodes'] if e.n == int(el[0])), None)

class Reader():
  def read(self, filePath):
    """
    Reads text file with nodes and returns the result dict with all objects
    and their nested properties
    """
  
    result = {
      'coordinates': {
        'count': 0,
        'nodes': []
      },
      'element_groups': { 
        'number_of_elements': 0,
        'count': 0,
        'groups': []
      },
      'bars': [],
      'materials': {
        'count': 0,
        'materials': []
      },
      'geometric_properties': {
        'count': 0
      },
      'bcnodes': {
        'count': 0
      },
      'loads': {
        'count': 0
      }
    }
    # print(result['coordinates']['nodes'])
    
    with open(filePath,'r') as f:
      lines = f.readlines()
      elementCounter = 0
      groupCounter = 0
      geometricCounter = 0

      for line in lines:
        line = line.strip()
        el = line.split(' ')
        
        if len(line) == 0:
          continue

        if len(line) != 0 and line[0] == "*":
          section = line[1:].lower()
          continue
        
        if section == 'coordinates':
          if len(el) == 1 :
            result[section]['count'] = el[0]
          else:
            result[section]['nodes'].append(Node(int(el[0]), float(el[1]), float(el[2])))
            
        elif section == 'element_groups':
          if len(line) == 1:
            result[section]['count'] = int(el[0])
          else: 
            result[section]['groups'].append(Group(el[0], el[1], el[2]))
            result[section]['number_of_elements'] += int(el[1])

        elif section == 'incidences':
          groups = result['element_groups']['groups']
          nodes = result['coordinates']['nodes']
          print(elementCounter)
          print(el)
          currentGroupAmount = groups[elementCounter].amount
          print("the current group has", currentGroupAmount, 'elements')
          if elementCounter < result['element_groups']['number_of_elements']:
            if (currentGroupAmount > 0):
              bar = Bar(el[0], nodes[int(el[1])-1], nodes[int(el[2])-1], groups[elementCounter])
              print(
              """
              Bar {} created 
              Start node: {} End Node: {}
              """.format(bar.id, bar.startNode.n, bar.endNode.n))
              result['bars'].append(bar)
              currentGroupAmount -= 1
            if(currentGroupAmount == 0):
              elementCounter += 1
    
        elif section == 'materials':
          if len(el) == 1:
            result[section]['count'] = el[0]
          else:
            material = Material(el[0], el[1], el[2])
            result[section]['materials'].append(material)
            result['element_groups']['groups'][groupCounter].setMaterial(material)
            groupCounter += 1

        elif section == 'geometric_properties':
          if geometricCounter == 0:
            result[section]['count'] = el[0]
          else:
            result['element_groups']['groups'][geometricCounter - 1].setSectionArea(
              el[0]
            )
          geometricCounter += 1

        elif section == 'bcnodes':
          if len(el) == 1:
            result[section]['count'] = el[0]
          else:
            nodeIndex = next((e for e, item in enumerate(
                result['coordinates']['nodes']) if item.n == int(el[0])), None
              )
            result['coordinates']['nodes'][nodeIndex].setRestriction(int(el[1]))

        elif section == 'loads':
          if len(el) == 1:
            result[section]['count'] = el[0]
          else:
            load = Load(el[1], el[2])
            nodeIndex = next((e for e, item in enumerate(
                result['coordinates']['nodes']) if item.n == int(el[0])), None
              )
            result['coordinates']['nodes'][nodeIndex].addLoad(load)

    for bar in result['bars']:
      bar.createLocalArray()
      
    print('---------- Parsing complete! ----------')
    pprint(result)
    print('---------------------------------------')

    return result
  

# reader = Reader()
# reader.read("./arquivoentrada.fem")


