def _add(tup1, tup2):
    return tuple(map(sum, zip(tup1, tup2)))

pieces = {
    '-': [(0,0), (1,0), (2,0), (3,0)],
    '+': [(0,1), (1,0), (1,1), (1,2), (2,1)],
    'J': [(0,0), (1,0), (2,0), (2,1), (2,2)],
    '|': [(0,0), (0,1), (0,2), (0,3)],
    'o': [(0,0), (0,1), (1,0), (1,1)]
}

piece_order = ['-' ,'+', 'J', '|', 'o']

class Tower:
    def __init__(self, wind):
        self.wind = wind # list of vector tuples
        self.wind_idx = 0

        self.width = 7 # static
        self.height = 0 # grows as you add pieces
        
        self.curr_tower = [] # list of 'full' coordinate tuples
        self.curr_piece = [] # list of coordinate tuples
        
        self.pieces_added = 0

    def __repr__(self):
        msg = ''
        for j in range(self.height + 7,-1, -1):
            msg = msg + ''.join('#' if (i,j) in self.curr_tower else '@' if (i,j) in self.curr_piece else '.' for i in range(self.width)) + '\n'
        return msg

    def is_stable(self):
        return any( (i, j-1) in self.curr_tower or j == 0 for (i,j) in self.curr_piece )
    
    def move(self, vec):
        moved = list(_add(x, vec) for x in self.curr_piece)
        if vec == (0,-1) and self.is_stable():
            pass
        elif any(p[0] < 0 or p[0] >= self.width or p in self.curr_tower for p in moved):
            pass
        else:
            self.curr_piece = moved

    def add_piece(self):
        self.curr_piece = pieces[piece_order[self.pieces_added % len(pieces)]]
        self.move((2, self.height + 3))

        while True:
            self.move(self.wind[self.wind_idx])
            self.wind_idx = (self.wind_idx + 1) % len(self.wind)
            
            if self.is_stable(): # feelsbadman
                break 
            
            self.move((0,-1))

        self.curr_tower.extend([x for x in self.curr_piece])
        self.pieces_added += 1 
        self.curr_piece = []
        
        self.height = max(p[1] for p in self.curr_tower) + 1

    def add_n_pieces(self, n):
        for i in range(n):
            self.add_piece()
            if not i % 100:
                print(f'i: {i}, height: {self.height}')

    def add_many_pieces(self, n):
        pass 

with open('input.txt') as my_file:
    wind = [(-1, 0) if x == '<' else (1,0) for x in my_file.read().strip()]


tower = Tower(wind)
tower.add_n_pieces(2022)

print(f'P1 Soln is: {tower.height}')