compactado = open("arquivo2.zipadissimo","w+")

with open("arquivo2.txt", "r") as arquivo_original:
    conteudo = arquivo_original.read()

alfabeto = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
frequencias = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "G": 0, "H": 0, "I": 0, "J": 0, "K": 0, "L": 0, "M": 0, "N": 0, "O": 0, "P": 0, "Q": 0, "R": 0, "S": 0, "T": 0, "U": 0, "V": 0, "W": 0, "X": 0, "Y": 0, "Z": 0}

def definir_freq(texto):
    for letra in alfabeto:
        frequencias[letra] = texto.count(letra)

fila = []

class No:
    def __init__(self, char, freq, noEsq, noDir):
        self.char = char
        self.freq = freq
        self.noEsq = noEsq
        self.noDir = noDir
    
def ordenar_freq(fila):
    for letra in frequencias:
        if frequencias[letra] > 0:
            fila.append(No(letra, frequencias[letra], None, None))
    fila.sort(key=lambda no: no.freq)
            
def arvore_huff(fila):
    while len(fila) > 1:
        no1 = fila.pop(0)
        no2 = fila.pop(0)
        novoNo = No(None, no1.freq + no2.freq, no1, no2)
        fila.append(novoNo)
        fila.sort(key=lambda no: no.freq)
        
codigos = {}

def gerarCod(no, caminho):
    if no.char is not None:
        codigos[no.char] = caminho
    else:
        gerarCod(no.noEsq, caminho + "0")
        gerarCod(no.noDir, caminho + "1")

definir_freq(conteudo)
ordenar_freq(fila)
arvore_huff(fila)
gerarCod(fila[0], "")

bits = ""
for letra in conteudo:
    bits += codigos[letra]
    


bytezar = (8 - len(bits) % 8) % 8
bits_bytezados = bits + "0" * bytezar
dados = bytearray()
for i in range(0, len(bits_bytezados), 8):
    byte_str = bits_bytezados[i:i+8]
    dados.append(int(byte_str, 2))
    
with open("arquivo2.zipadissimo", "wb") as f:
    f.write(bytes([bytezar]))
    f.write(bytes([len(codigos)]))  
    for letra, código in codigos.items():
        f.write(letra.encode())
        f.write(bytes([len(código)]))
        f.write(código.encode())
    f.write(dados)



def descompacta_arquivo2():
    with open("arquivo2.zipadissimo", "rb") as f:
        padding = f.read(1)[0]
        ncodigos = f.read(1)[0]
        codigos = {}
        for codigo in range(ncodigos):
            letra = f.read(1).decode()
            tam = f.read(1)[0]
            codigo = f.read(tam).decode()
            codigos[letra] = codigo
        dados = f.read()
    bits = "".join(format(b, '08b') for b in dados)
    bits = bits[:-padding]
    inv = {v: k for k, v in codigos.items()}
    prefixo = ""
    resultado = []
    for bit in bits:
        prefixo += bit
        if prefixo in inv:
            resultado.append(inv[prefixo])
            prefixo = ""
    with open("arquivo2.restaurado", "w") as out:
        out.write("".join(resultado))

descompacta_arquivo2()
compactado.close()