def is_ordered(left, right, i=0):
    try:     # test if left or right has run out of content
        left[i]
    except IndexError:
        return 
    try:
        right[i]
    except IndexError:
        return False

    if type(left[i]) == int and type(right[i]) == int:
        if left[i] < right[i]:
            return True 
        elif left[i] > right[i]:
            return False 
        else:
            i += 1
            return is_ordered(left, right, i=i)
    
    if type(left[i]) == list and type(right[i]) == list:
        try:
            return is_ordered(left[i], right[i])
        except IndexError: # either one list ran out or they're identical
            if len(left) < len(right):
                return True
            elif len(left) > len(right):
                return False
            else:
                i += 1
                return is_ordered(left, right, i=i)
    else:
        if type(left[i]) == int:
            left[i] = [left[i]]
        if type(right[i]) == int:
            right[i] = [right[i]]
        return is_ordered(left[i], right[i])

with open('input.txt') as my_file: 
    pairs = [p.split('\n') for p in my_file.read().split('\n\n')]
    pairs = [(eval(p[0]), eval(p[1])) for p in pairs]

    dividers = [[[2]], [[6]]]
    p2_packets = [side for pair in pairs for side in pairs] + dividers # flatten

ordered_idxs = [i + 1 for i, p in enumerate(pairs) if is_ordered(*p)]

print(f'P1 Soln is: {sum(ordered_idxs)}')

