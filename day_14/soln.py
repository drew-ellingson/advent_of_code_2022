import math 

def _add(tup1, tup2):
    return list(map(sum, zip(tup1, tup2)))

def _mult(tup1, scal):
    return tuple(scal * a for a in tup1)

def _diff(tup1, tup2):
    return _add(tup1, _mult(tup2, -1))

def _mag(tup1):
    return math.sqrt(tup1[0] ** 2 + tup1[1] ** 2)

class Grid():
    def __init__(self, rock_corners):
        # adding some padding - shouldn't matter
        self.min_x = min(a[0] for a in rock_corners) - 5
        self.max_x = max(a[0] for a in rock_corners) + 5 
        self.min_y = 0
        self.max_y = max(a[1] for a in rock_corners) + 5

        self.rocks = self.get_all_rocks_coords(rock_corners)

        # tuple-indexed grid. might be slow as hell
        self.grid = ['#' if (i,j) in self.rocks else '.' for i in range(self.min_x, self.max_x) for j in range(self.min_y, self.max_y)]
    
    def __repr__(self):
        msg = ''
        for j in range(self.min_y, self.max_y):
            msg = f"{msg}\n{''.join(self.grid[(i, j)] for i in range(self.min_x, self.max_x))}")
        return msg

    def add_one_sand(self):
        pass 

    def get_capacity(self):
        pass
    
    def get_all_rock_coords(self, rock_corners):
        rocks = []
        for i in range(len(rock_corners) - 1):
            diff = _diff(rock_corners[i], rock_corners[i + 1])
            
            #unit
            u_diff = _mult(diff, _mag(diff))

            rocks.extend([_add(rock_corners[i]) + _mult(u_diff, j) for j in range(_mag(diff) + 1)])
        
        return rocks

def parse(rock_line):
    return [tuple(int(x) for x in coord.split(',')) for coord in rock_line.split(' -> ')]

with open('input2.txt') as my_file:
    rocks = [parse(line) for line in my_file.readlines()]

