arquivo = open("passados.txt", "r")

sequencia = []

for line in arquivo:
    sequencia.append(int(line))
arquivo.close()

arquivo = open("passados.txt", "a")


def fibonacci(pos):
    if pos <= len(sequencia):
        return sequencia[pos - 1]
    else:
        if pos <= 1:
            return pos
        else:
            for n in range(pos - len(sequencia)):
                valor = fibonacci(pos - 1) + fibonacci(pos - 2)
                sequencia.append(valor)
                arquivo.write(str(sequencia[-1]) + "\n")
                return valor

pos = int(input("Digite a posicao que quer saber o fibonacci: "))
print ("O elemento de fibonacci na posicao ", pos, " é ", fibonacci(pos))



