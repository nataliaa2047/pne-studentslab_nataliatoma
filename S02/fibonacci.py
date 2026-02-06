sequence = [0,1]        #lista que representa los dos primeros números de Fibonacci
for i in range(2,11):     #se repite sólo 9 veces porque el 0 y el 1 y los tenemos incluidos de antes, así que ya tenemos 11 números
    fic = sequence[-1] + sequence[-2]  #suma del último más penúltimo número de la lista
    sequence.append(fic)    #se añade lo nuevo calculado al final de la lista
for item in sequence:    #recorre la lista uno por uno
    print(item, end=" ")   #imprime cada número en la misma línea

