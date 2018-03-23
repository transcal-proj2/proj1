from elements import Node, Bar, Material

class Reader():
  def read(self, filePath):
    result = {}

    with open(filePath,'r') as f:
      lines = f.readlines()
      # while (line):
      for line in lines:
        line = line.strip()
        print(line)

        if len(line) != 0 and line[0] == "*":
          section = line[1:].lower()
          result[section] = {}
          continue
        
        if section == 'coordinates':
          coord = line.split(' ')
          if len(coord) == 1:
            result[section]['count'] = coord[0]
            result[section]['nodes'] = []
          else:
            print("appending node")
            result[section]['nodes'].append(Node(coord[0],coord[1],coord[2]))
            

        elif section == 'element_groups':
            eg = line.split(' ')
            print(eg)
            
# line.find("E") != -1
          # else:
          #   line = line.lower()        
          #   num = float(line)
          #   print("found number",num)
        

        print(result)



reader = Reader()
reader.read("./input.txt")