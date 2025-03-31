

def fibonacci(pos):
    if pos <= 1:
        return pos
    else:
        for n in range(pos):
            return fibonacci(pos-2) + fibonacci(pos-1)

pos = int(input("Digite a posicao que quer saber o fibonacci: "))
resultado = fibonacci(pos   )
print ("O elemento de fibonacci na posicao ", pos, " é ", fibonacci(pos))