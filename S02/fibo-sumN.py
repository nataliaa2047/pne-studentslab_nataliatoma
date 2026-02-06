def fibosum(n):
    sequence = [0, 1]
    sum = 1  #es igual a 1 y no a 0 porque la lista contiene [0,1], por lo que 0+1=1, de modo que tiene que iniciar en 1
    for i in range(2,n+1):
        fic = sequence[-1] + sequence[-2]
        sum += int(fic)  #esto suma todos los 10 primeros términos de Fibonacci, y a partir de aquí nosotros ya seleccionamos la parte que queramos
        sequence.append(fic)
    return sum

print("Sum of the First 5 terms of the Fibonacci series:", fibosum(5))
print("Sum of the First 10 terms of the Fibonacci series:", fibosum(10))



