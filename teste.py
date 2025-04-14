tabuleiro = [["X", "X", "X", "X", "X", "X", "X", "X"], ["X", "X", "X", "X", "X", "X", "X", "X"], ["X", "X", "X", "X", "X", "X", "X", "X"], ["X", "X", "X", "X", "X", "X", "X", "X"], ["X", "X", "X", "X", "X", "X", "X", "X"], ["X", "X", "X", "X", "X", "X", "X", "X"], ["X", "X", "X", "X", "X", "X", "X", "X"], ["X", "X", "X", "X", "X", "X", "X", "X"]]

posAtual = [0, 0]

posicoesRainhas = []


def podeAqui(coord):
    cont = 0
    validos = 0
    if "R" in tabuleiro[coord[0]]:
        return False
    while cont < 8:
        if tabuleiro[cont][coord[1]] == "R":
            return False
        cont += 1
    if posicoesRainhas != []:
        for rainha in posicoesRainhas:
            if (abs((rainha[0]) - coord[0])) == (abs((rainha[1]) - coord[1])):
                return False

    return True



def colocaRainhas():

    while posAtual[0] < 8:
        linha_valida = False
        if podeAqui(posAtual):
            tabuleiro[posAtual[0]][posAtual[1]] = "R"
            posicoesRainhas.append(list(posAtual))
            posAtual[1] = 0
            posAtual[0] += 1
            linha_valida = True

        else:
            if posAtual[1] < 8:
                posAtual[1] += 1
    if not linha_valida:
        if not posicoesRainhas:
            print("Buguei")
            return

        ultima = posicoesRainhas.pop()
        tabuleiro[ultima[0]][ultima[1]] = "X"

        posAtual[0] = ultima[0]
        posAtual[1] = ultima[1] + 1


colocaRainhas()
for linha in tabuleiro:
    print(linha)
            






