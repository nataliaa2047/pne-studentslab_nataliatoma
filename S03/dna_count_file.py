count_a = 0
count_c = 0
count_t = 0
count_g = 0

with open("dna.txt", "r") as f:
    for l in f:
        l = l.strip()
        count_a += l.count("A")
        count_c += l.count("C")
        count_t += l.count("T")
        count_g += l.count("G")

total_length = count_a + count_c + count_t + count_g

print("Total length:", total_length)
print("A:", count_a)
print("C:", count_c)
print("T:", count_t)
print("G:", count_g)

count_a = count_c = count_t = count_g = 0

with open("dna.txt", "r") as f:
    for line in f:
        line = line.strip().upper()
        count_a += line.count("A")
        count_c += line.count("C")
        count_t += line.count("T")
        count_g += line.count("G")

total_length = count_a + count_c + count_t + count_g

print("Total length:", total_length)
print("A:", count_a)
print("C:", count_c)
print("T:", count_t)
print("G:", count_g)
