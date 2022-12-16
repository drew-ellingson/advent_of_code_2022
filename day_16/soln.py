import re 

class Node:
    def __init__(self, label, flow, children):
        self.label = label
        self.flow = flow 
        self.children = children 

    def __repr__(self):
        return f'valve: {self.label}\nflow rate: {self.flow}\nchildren: {self.children}\n'

class Valves:
    def __init__(self, nodes):
        self.nodes = nodes 
        self.minutes = 30
        self.curr_path = ['AA']
    
    def score(path):
        pass 

    def get_len_n_paths(self, n):
        pass 

    def make_best_move(self, n):
        paths = self.get_len_n_paths(n)
        best = max(paths, key = lambda p: self.score(p))[0]
        
        self.curr_path.append(best)
        self.minutes -= 1

    def find_max_flux(self, n):
        while self.minutes > 0:
            self.make_best_move(n)
        return self.score(self.curr_path)

def parse(line):
    label = line[6:8]
    flow, children = line.split(';')
    flow = int(re.sub('[^0-9]', '', flow))
    children = re.sub(' tunnel[s]* lead[s]* to valve[s]*', '', children)
    children = children.strip().split(',')
    return label, flow, children 

with open('input2.txt') as my_file: 
    nodes = [Node(*parse(line)) for line in my_file.readlines()]

for n in nodes:
    print(n)