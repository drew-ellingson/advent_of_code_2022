with open("input.txt") as my_file:
    signal = my_file.read()


def dist_char_check(signal, char_num):
    return min(
        i
        for i in range(char_num, len(signal))
        if len(set(signal[i - char_num : i])) == char_num
    )


print(f"P1 Soln is: {dist_char_check(signal, 4)}")
print(f"P2 Soln is: {dist_char_check(signal, 14)}")
