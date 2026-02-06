sequence = [0,1]
for i in range(2,11):
    fic = sequence[-1] + sequence[-2]
    sequence.append(fic)
for item in sequence:
    print(item, end=" ")

