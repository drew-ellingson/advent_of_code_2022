def _add(tup1, tup2):
    return tuple(map(sum, zip(tup1, tup2)))

dirs = [(0,0,1), (0,0,-1), (0,1,0), (0,-1,0), (1,0,0), (-1,0,0)]

with open('input2.txt') as my_file:
    cubes = [tuple(int(y) for y in x.strip().split(',')) for x in my_file.readlines()]

open_dirs = [_add(c,d) for c in cubes for d in dirs if _add(c,d) not in cubes]

print(f'P1 Soln is: {len(open_dirs)}')