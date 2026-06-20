def fibon(n):
    sequence = [0,1]
    for i in range(2,1+n):
        fic = sequence[-1] + sequence[-2]
        sequence.append(fic)
    return sequence

print(f"5th Fibonacci term: {fibon(5)[-1]}")
print(f"10th Fibonacci term: {fibon(10)[-1]}")
print(f"15th Fibonacci term: {fibon(15)[-1]}")

