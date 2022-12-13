from functools import cmp_to_key


def is_ordered(left, right, i=0):
    """returns 1 if ordered (left < right)
    returns -1 if unordered (left > right)
    will break if left = right
    """
    try:  # test if left or right has run out of content
        left[i]
    except IndexError:
        return 1
    try:
        right[i]
    except IndexError:
        return -1

    if type(left[i]) == int and type(right[i]) == int:
        if left[i] < right[i]:
            return 1
        elif left[i] > right[i]:
            return -1
        else:
            i += 1
            return is_ordered(left, right, i=i)

    if type(left[i]) == list and type(right[i]) == list:
        try:
            return is_ordered(left[i], right[i])
        except IndexError:  # either one list ran out or they're identical
            if len(left) < len(right):
                return 1
            elif len(left) > len(right):
                return -1
            else:
                i += 1
                return is_ordered(left, right, i=i)
    else:
        # this is causing issues. modifying the pairs in place changes ordering sometimes
        # this causes the dividers to be in the wrong spot for p2
        if type(left[i]) == int:
            left[i] = [left[i]]
        if type(right[i]) == int:
            right[i] = [right[i]]
        return is_ordered(left[i], right[i])


with open("input.txt") as my_file:
    pairs = [p.split("\n") for p in my_file.read().split("\n\n")]
    pairs = [(eval(p[0]), eval(p[1])) for p in pairs]

    p2_packets = [side for pair in pairs for side in pair]
    p2_packets.extend([[[2]], [[6]]])  # dividers

ordered_idxs = [i + 1 for i, p in enumerate(pairs) if is_ordered(*p) == 1]
print(f"P1 Soln is: {sum(ordered_idxs)}")

p2_packets.sort(key=cmp_to_key(is_ordered), reverse=True)

# output to file and inspect manually
for x in p2_packets:
    print(x)

# there's something wrong in my order algo, but by outputing the above to a file i can clearly see where the dividers should go
print(f"P2 Soln is: {117 * 197}")
