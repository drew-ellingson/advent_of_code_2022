with open("input.txt") as my_file:
    pairs = [
        [list(map(int, rooms.split("-"))) for rooms in line.strip().split(",")]
        for line in my_file.readlines()
    ]


def contained(pair, partial=False):
    p1, p2 = pair
    if partial:
        return (
            (p2[0] <= p1[0] <= p2[1])
            or (p2[0] <= p1[1] <= p2[1])
            or (p1[0] <= p2[0] <= p1[1])
            or (p1[0] <= p2[1] <= p1[1])
        )
    else:
        return (p1[0] <= p2[0] and p1[1] >= p2[1]) or (
            p1[0] >= p2[0] and p1[1] <= p2[1]
        )


eclipse_pairs = list(filter(contained, pairs))
partial_eclipse_pairs = list(filter(lambda x: contained(x, partial=True), pairs))

print(f"P1 Soln is: {len(eclipse_pairs)}")
print(f"P2 Soln is: {len(partial_eclipse_pairs)}")
