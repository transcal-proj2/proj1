from elements import Node, Bar, Material, Group
from pprint import pprint

class Reader():
  def read(self, filePath):
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
    }
    # print(result['coordinates']['nodes'])
    
    with open(filePath,'r') as f:
      lines = f.readlines()
      elementCounter = 0

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
          currentGroupAmount = groups[elementCounter].amount

          if elementCounter < result['element_groups']['number_of_elements']:
            if (currentGroupAmount > 0):
              bar = Bar(el[0], nodes[int(el[1])-1], nodes[int(el[2])-1], groups[elementCounter])
              result['bars'].append(bar)
              currentGroupAmount -= 1
            elementCounter += 1

         
          # if len(allAmounts) == 0:
          #   for i in range(result['element_groups']['count']):
          #     allAmounts.append(groups[i].amount)
          #   print(allAmounts)

          # for j in range(len(allAmounts)):



    pprint(result)
          
    
    
          



            # print(eg)
            
# line.find("E") != -1
          # else:
          #   line = line.lower()        
          #   num = float(line)
          #   print("found number",num)
        




reader = Reader()
reader.read("./input.txt")
