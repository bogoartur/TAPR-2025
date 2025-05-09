


def compacta_arquivo1():
    compactado = open("arquivo1.zipadissimo","w+")

    with open("arquivo1.txt", "r") as arquivo_original:
        conteudo = arquivo_original.read()
        
    posicao = 0
    while posicao < len(conteudo):
        char_atual = conteudo[posicao]
        cont = 1
        while posicao + 1 < len(conteudo) and char_atual == conteudo[posicao + 1]:
            cont += 1
            posicao += 1
        compactado.write(str(char_atual) + str(cont))
        posicao += 1
    compactado.close()
    

def descompacta_arquivo1():
    descompactado = open("arquivo1.restaurado","w+")

    with open("arquivo1.zipadissimo", "r") as zipadissimo:
        conteudo = zipadissimo.read()
        
    posicao = 0
    
    while posicao < len(conteudo):
        char_atual = conteudo[posicao]
        numero = ""
        while posicao + 1 < len(conteudo) and conteudo[posicao + 1].isdigit():
            numero += conteudo[posicao + 1]
            posicao += 1
        sequencia = char_atual * int(numero)
        descompactado.write(sequencia)
        posicao += 1

    descompactado.close()
    
compacta_arquivo1()
descompacta_arquivo1()