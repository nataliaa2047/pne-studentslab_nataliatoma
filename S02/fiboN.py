def fibon(n):
    sequence = [0,1]
    for i in range(2, n+1):    #in this case we can't put range(2,15), because it varies depending on the case, it depends on the n. And knowing that the range always takes the last value minus 1, that's why we have to put a +1.
        fic = sequence[-1] + sequence[-2]
        sequence.append(fic)
    return sequence

seq_5 = fibon(5)
print("5th Fibonacci term:", seq_5[-1])

seq_10 = fibon(10)
print("10th Fibonacci term:", seq_10[-1])

seq_15 = fibon(15)
print("15th Fibonacci term:", seq_15[-1])
