import re 

class Node:
    def __init__(self, label, flow, children):
        self.label = label
        self.flow = flow 
        self.children = children 

    def __repr__(self):
        return f'valve: {self.label}\nflow rate: {self.flow}\nchildren: {self.children}\n'

def parse(line):
    flow, children = line.split(';')
    label = flow[6:8]
    flow = re.sub('[^0-9]', '', flow)
    children = re.sub(' tunnel[s]* lead[s]* to valve[s]*', '', children)
    children = children.strip().split(',')
    return label, flow, children 

with open('input2.txt') as my_file: 
    nodes = [Node(*parse(line)) for line in my_file.readlines()]

for n in nodes:
    print(n)