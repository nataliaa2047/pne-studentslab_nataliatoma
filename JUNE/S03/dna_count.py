def bases_counter(seq):
    count_a = 0
    count_c = 0
    count_g = 0
    count_t = 0
    for i in seq:
        if i == "A":
            count_a += 1
        if i == "C":
            count_c += 1
        if i == "G":
            count_g += 1
        if i == "T":
            count_t += 1
    return count_a, count_c, count_g, count_t

sequence = input("Introduce the sequence: ")
print(f"Total length: {len(sequence)}")
print(f"A: {bases_counter(sequence)[0]}")
print(f"C: {bases_counter(sequence)[1]}")
print(f"G: {bases_counter(sequence)[2]}")
print(f"T: {bases_counter(sequence)[3]}")
