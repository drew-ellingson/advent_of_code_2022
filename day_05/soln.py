import re
from copy import copy

# ---------------- parse helpers ------------------------


def parse_boxes(boxes):
    """assumes constant 4 char width per stack in input"""
    levels = boxes.split("\n")
    labels = [int(i) for i in levels[-1].split()]
    stacks = [[] for i in range(max(labels))]  # initialize empty stacks

    levels = list(reversed(levels[:-1]))  # remove label and start from bottom
    width = max(len(l) for l in levels)

    for i in range(int(width / 4) + 1):
        for l in levels:
            if l[4 * i + 1] != " ":
                stacks[i].append(l[4 * i + 1])  # index of letter
    return stacks


def parse_instr(instr):
    instr = re.sub("[^0-9 ]", "", instr)
    instr = re.sub("[\s]{2,}", " ", instr)  # remove excess whitespace
    return list(map(int, instr[1:].split(" ")))  # skip first space


# ---------------- box moving functions -------------------------


def apply(instr, boxes, p2=False):
    from_idx, to_idx = instr[1] - 1, instr[2] - 1  # 1-indexed
    move_num = instr[0]

    move = boxes[from_idx][-move_num:]
    boxes[from_idx] = boxes[from_idx][:-move_num]
    if p2:
        boxes[to_idx] = boxes[to_idx] + move
    else:
        boxes[to_idx] = boxes[to_idx] + list(reversed(move))


def apply_all(instrs, boxes, p2=False):
    for instr in instrs:
        apply(instr, boxes, p2=p2)


# ----------------- actually do the thing --------------

with open("input.txt") as my_file:
    boxes, instrs = my_file.read().split("\n\n")
    boxes = parse_boxes(boxes)
    instrs = [parse_instr(instr) for instr in instrs.split("\n")]

cm_9000_boxes, cm_9001_boxes = boxes, copy(boxes)

apply_all(instrs, cm_9000_boxes)
apply_all(instrs, cm_9001_boxes, p2=True)

print(f'P1 Soln is: {"".join(s[-1] for s in cm_9000_boxes)}')
print(f'P2 Soln is: {"".join(s[-1] for s in cm_9001_boxes)}')
