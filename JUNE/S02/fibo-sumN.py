def fibosumn(n):
    sequence = [0,1]
    for i in range(2,1+n):
        fic = sequence[-1] + sequence[-2]
        sequence.append(fic)
        count = 0
        for j in sequence:
            count += j
    return count

print(f"Sum of the first 5 terms of the Fibonacci series: {fibosumn(5)}")
print(f"Sum of the first 10 terms of the Fibonacci series: {fibosumn(10)}")
