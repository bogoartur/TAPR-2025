compactado = open("arquivo2.zipadissimo","w+")

with open("arquivo2.txt", "r") as arquivo_original:
    conteudo = arquivo_original.read()

alfabeto = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
frequencias = {}
for letra in alfabeto:
    frequencias.append(conteudo.count(letra))

print(frequencias)