def parse_inst(inst_line):
    direc, mag = inst_line.strip().split()
    mag = int(mag)
    return (direc, mag)

def _mult(tup, scal):
    return tuple(scal * x for x in tup)

def _add(tup1, tup2):
    return tuple(map(sum, zip(tup1, tup2)))

def _diff(tup1, tup2):
    return _add(tup1, _mult(tup2, -1))

def get_new_tail_pos(head_pos, tail_pos):
    diff = _diff(head_pos[-1], tail_pos[-1])
    move = (int((a > 0) - (a < 0)) for a in diff) if any(abs(a) >= 2 for a in diff) else (0,0)
    return _add(tail_pos[-1], move)

def do_instr(instr, head_pos, tail_pos):
    for i in range(instr[1]):
        # print(f'instr: {instr}')
        # print(f'head: {head_pos}')
        # print(f'tail: {tail_pos}')
        # input()
        head_pos.append(_add(head_pos[-1], dirs[instr[0]]))
        tail_pos.append(get_new_tail_pos(head_pos, tail_pos))

def all_instr(instrs, head_pos, tail_pos):
    for i in instrs:
        do_instr(i, head_pos, tail_pos)


with open('input.txt') as my_file: 
    instrs = [parse_inst(line) for line in my_file.readlines()]

dirs = {'U': (0,1), 'R': (1,0), 'D': (0,-1), 'L': (-1,0)}

head_pos = [(0,0)]
tail_pos = [(0,0)]

all_instr(instrs, head_pos, tail_pos)

print(f'P1 Answer is: {len(set(tail_pos))}')
