import re 
from copy import copy 

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

        # describes path through pipes. eg. ['AA', 'DD', 'valve', 'BB' , 'valve']
        self.curr_path = ['AA']
    
    def score(self, path):
        # every time a valve is turned on, multiply its flow by how many minutes it will be on.
        return sum(self.nodes[path[i - 1]].flow * (self.minutes - i) for i, v in enumerate(path) if v == 'valve')

    def get_len_n_paths(self, n):
        """
        return all viable paths which are n-steps forward from self.curr_path. 
        turning current valve is represented w/ string 'valve'
        
        paths that would turn on a valve w/ flow = 0 are omitted.
        no double-turning valves

        eg. get_len_n_paths(2) from 'AA' on the sample input would return:

        [['AA', 'DD', 'CC']
        ['AA', 'DD', 'AA']
        ['AA', 'DD', 'EE']
        ['AA', 'DD', 'valve']
        ['AA', 'II', 'AA']
        ['AA', 'II', 'JJ']
        ['AA', 'BB', 'CC']
        ['AA', 'BB', 'AA']
        ['AA', 'BB', 'valve']]
        """

        paths = [self.curr_path]
        curr_len = len(self.curr_path)
        while paths and len(paths[0]) < curr_len + n:
            next_paths = []
            for p in paths:
                opened_valves = [p[i] for i in range(len(p) - 1) if p[i + 1] == 'valve']
                curr_node = self.nodes[p[-1]] if p[-1] != 'valve' else self.nodes[p[-2]]
                
                # don't modify in place
                next_cand = copy(curr_node.children)
                
                # don't move to any valve you've visited since you last opened a valve
                
                try:
                    tail = p[len(p) - p[::-1].index('valve'):]
                    if len(tail) == 0:
                        tail = p
                except ValueError:
                    tail = p

                next_cand = [x for x in next_cand if x not in tail]

                # no double-opening valves
                if curr_node.label not in opened_valves and curr_node.flow > 0:
                    next_cand.append('valve')

                next_paths.extend(p + [n] for n in next_cand)

                if not next_paths:
                    return paths

            paths = next_paths 
        return paths 

    def make_best_move(self, n):
        """
        1. Find all paths forward of length n
        2. Pick the path that maximizes lifetime flux
        3. Take the first move of that path as next move
        """

        paths = self.get_len_n_paths(n)

        best = max(paths, key = lambda p: self.score(p))[len(self.curr_path)]

        self.curr_path.append(best)

    def find_max_flux(self, n):
        """Iterate make_best_move until you run out of time, and then score the path"""
        while self.minutes >= len(self.curr_path):
            self.make_best_move(n)
        return self.score(self.curr_path)

def parse(line):
    label = line[6:8]
    
    flow, children = line.split(';')
    flow = int(re.sub('[^0-9]', '', flow))
    
    children = re.sub(' tunnel[s]* lead[s]* to valve[s]*', '', children)
    children = children.strip().split(', ')
    
    return label, flow, children 

with open('input2.txt') as my_file: 
    nodes = [Node(*parse(line)) for line in my_file.readlines()]
    nodes = {node.label: node for node in nodes}

valves = Valves(nodes)

print(valves.find_max_flux(10))

# this is the path in the input, and it gets scored correctly.
# print(valves.score(['AA', 'DD', 'valve', 'CC', 'BB', 'valve', 'AA', 'II', 'JJ', 'valve', 'II', 'AA', 'DD', 'EE', 'FF', 'GG', 'HH', 'valve', 'GG', 'FF', 'EE', 'valve', 'DD', 'CC', 'valve']))