def sumn(n):
    result = 0
    for i in range(1, n+1):
        result += i
    return result

print("Sum of the 20 first integers:", sumn(20))
print("Sum of the 100 first integers:", sumn(100))