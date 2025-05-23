import time
import os
import bz2
import gzip
import lzma
import shutil
import subprocess
import sys
import brotli
import lz4.frame
import snappy
import zstandard
import py7zr


seven_zip_exe = shutil.which('7z.exe')

def criar_arquivo_exemplo(nome_arq, tamanho=1):
    if not os.path.exists(nome_arq): #só cria o arquivo se não tiver um na pasta
        repeticao_final = "Este é um exemplo de texto para compressão. Repetição é a chave para boa compressão. " * 200
        repeticao = "Linha de teste para algoritmos de compactacao ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz 0123456789 !@#$%^&*()_+[];',./{}|:<>?\n"
        qtd_linhas = (tamanho * 1024 * 1024) // len(repeticao.encode('utf-8'))
        if qtd_linhas == 0:
            qtd_linhas = 100 
        with open(nome_arq, "w", encoding="utf-8") as f:
            for i in range(qtd_linhas):
                f.write(f"{i}: {repeticao}")
            f.write(repeticao_final * (tamanho * 2)) 

def tamanho_arq(caminho):
    if os.path.exists(caminho):
        return os.path.getsize(caminho)
    return 0

def calcular_taxa_compactacao(tamanho_inicial, tamanho_comprimido):
    if tamanho_inicial == 0:
        return 0
    return ((tamanho_inicial - tamanho_comprimido) / tamanho_inicial) * 100 #porcentagem

def teste_gzip(arquivo_input):
    algoritmo = "GZip (DEFLATE)"
    nome_comprimido = arquivo_input + ".comprimido" + ".gz"
    nome_descomprimido = arquivo_input + ".descomprimido" + ".gz.txt"
    tamanho_inicial = tamanho_arq(arquivo_input)
    
    tempo_ini = time.perf_counter()
    with open(arquivo_input, "rb") as f_in, gzip.open(nome_comprimido, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)
    tempo_comprimir = time.perf_counter() - tempo_ini
    tamanho_comprimido = tamanho_arq(nome_comprimido)

    tempo_ini = time.perf_counter()
    with gzip.open(nome_comprimido, "rb") as f_in, open(nome_descomprimido, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)
    tempo_descomprimir = time.perf_counter() - tempo_ini
    
    return algoritmo, tempo_comprimir, tempo_descomprimir, tamanho_inicial, tamanho_comprimido

def teste_bzip2(arquivo_input):
    algoritmo = "BZip2 (Burrows-Wheeler)"
    nome_comprimido = arquivo_input + ".comprimido" + ".bz2"
    nome_descomprimido = arquivo_input + ".descomprimido" + ".bz2.txt"
    tamanho_inicial = tamanho_arq(arquivo_input)

    tempo_ini = time.perf_counter()
    with open(arquivo_input, "rb") as f_in, bz2.open(nome_comprimido, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)
    tempo_comprimir = time.perf_counter() - tempo_ini
    tamanho_comprimido = tamanho_arq(nome_comprimido)

    tempo_ini = time.perf_counter()
    with bz2.open(nome_comprimido, "rb") as f_in, open(nome_descomprimido, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)
    tempo_descomprimir = time.perf_counter() - tempo_ini

    return algoritmo, tempo_comprimir, tempo_descomprimir, tamanho_inicial, tamanho_comprimido

def teste_xz_lzma2(arquivo_input):
    algoritmo = "Xz (LZMA2)"
    nome_comprimido = arquivo_input + ".comprimido" + ".xz"
    nome_descomprimido = arquivo_input + ".descomprimido" + ".xz.txt"
    tamanho_inicial = tamanho_arq(arquivo_input)

    tempo_ini = time.perf_counter()
    with open(arquivo_input, "rb") as f_in, lzma.open(nome_comprimido, "wb", format=lzma.FORMAT_XZ, preset=6) as f_out:
        shutil.copyfileobj(f_in, f_out)
    tempo_comprimir = time.perf_counter() - tempo_ini
    tamanho_comprimido = tamanho_arq(nome_comprimido)

    tempo_ini = time.perf_counter()
    with lzma.open(nome_comprimido, "rb", format=lzma.FORMAT_XZ) as f_in, open(nome_descomprimido, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)
    tempo_descomprimir = time.perf_counter() - tempo_ini
        
    return algoritmo, tempo_comprimir, tempo_descomprimir, tamanho_inicial, tamanho_comprimido

def teste_7zip_lzma2_py7zr(arquivo_input):
    algoritmo = "7-zip (LZMA2 via py7zr)"
    nome_comprimido = arquivo_input + ".comprimido" + ".7z"
    pasta_descomp = arquivo_input + ".descomprimido" + "_7z"
    tamanho_inicial = tamanho_arq(arquivo_input)
    
    filtros_lzma = [{'id': py7zr.FILTER_LZMA2, 'preset': 5}] 

    tempo_ini = time.perf_counter()
    with py7zr.SevenZipFile(nome_comprimido, 'w', filters=filtros_lzma) as arquivo:
        arquivo.write(arquivo_input, arcname=os.path.basename(arquivo_input))
    tempo_comprimir = time.perf_counter() - tempo_ini
    tamanho_comprimido = tamanho_arq(nome_comprimido)

    tempo_ini = time.perf_counter()
    os.makedirs(pasta_descomp, exist_ok=True)
    with py7zr.SevenZipFile(nome_comprimido, 'r') as arquivo:
        arquivo.extractall(path=pasta_descomp)
    tempo_descomprimir = time.perf_counter() - tempo_ini

    if os.path.exists(pasta_descomp):
        shutil.rmtree(pasta_descomp)
        
    return algoritmo, tempo_comprimir, tempo_descomprimir, tamanho_inicial, tamanho_comprimido


def teste_brotli(arquivo_input):
    algoritmo = "Brotli (BROTLI)"
    nome_comprimido = arquivo_input + ".comprimido" + ".br"
    nome_descomprimido = arquivo_input + ".descomprimido" + ".br.txt"
    tamanho_inicial = tamanho_arq(arquivo_input)

    tempo_ini = time.perf_counter()
    with open(arquivo_input, "rb") as f_in:
        dados = f_in.read()
    dados_comp = brotli.compress(dados, quality=6)
    with open(nome_comprimido, "wb") as f_out:
        f_out.write(dados_comp)
    tempo_comprimir = time.perf_counter() - tempo_ini
    tamanho_comprimido = tamanho_arq(nome_comprimido)

    tempo_ini = time.perf_counter()
    with open(nome_comprimido, "rb") as f_in:
        dados_comp = f_in.read()
    dados_descomp = brotli.decompress(dados_comp)
    with open(nome_descomprimido, "wb") as f_out:
        f_out.write(dados_descomp)
    tempo_descomprimir = time.perf_counter() - tempo_ini

    return algoritmo, tempo_comprimir, tempo_descomprimir, tamanho_inicial, tamanho_comprimido

def teste_lz4(arquivo_input):
    algoritmo = "LZ4 (LZ4)"
    nome_comprimido = arquivo_input + ".comprimido" + ".lz4"
    nome_descomprimido = arquivo_input + ".descomprimido" + ".lz4.txt"
    tamanho_inicial = tamanho_arq(arquivo_input)

    tempo_ini = time.perf_counter()
    with open(arquivo_input, "rb") as f_in, lz4.frame.open(nome_comprimido, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)
    tempo_comprimir = time.perf_counter() - tempo_ini
    tamanho_comprimido = tamanho_arq(nome_comprimido)

    tempo_ini = time.perf_counter()
    with lz4.frame.open(nome_comprimido, "rb") as f_in, open(nome_descomprimido, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)
    tempo_descomprimir = time.perf_counter() - tempo_ini

    return algoritmo, tempo_comprimir, tempo_descomprimir, tamanho_inicial, tamanho_comprimido

def teste_snappy(arquivo_input):
    algoritmo = "Snappy (LZ77)"
    nome_comprimido = arquivo_input + ".comprimido" + ".snappy"
    nome_descomprimido = arquivo_input + ".descomprimido" + ".snappy.txt"
    tamanho_inicial = tamanho_arq(arquivo_input)

    tempo_ini = time.perf_counter()
    with open(arquivo_input, "rb") as f_in:
        dados = f_in.read()
    dados_comp = snappy.compress(dados)
    with open(nome_comprimido, "wb") as f_out:
        f_out.write(dados_comp)
    tempo_comprimir = time.perf_counter() - tempo_ini
    tamanho_comprimido = tamanho_arq(nome_comprimido)

    tempo_ini = time.perf_counter()
    with open(nome_comprimido, "rb") as f_in:
        dados_comp = f_in.read()
    dados_descomp = snappy.decompress(dados_comp)
    with open(nome_descomprimido, "wb") as f_out:
        f_out.write(dados_descomp)
    tempo_descomprimir = time.perf_counter() - tempo_ini

    return algoritmo, tempo_comprimir, tempo_descomprimir, tamanho_inicial, tamanho_comprimido

def teste_zstd(arquivo_input):
    algoritmo = "Zstd (ZSTD)"
    nome_comprimido = arquivo_input + ".comprimido" + ".zst"
    nome_descomprimido = arquivo_input + ".descomprimido" + ".zst.txt"
    tamanho_inicial = tamanho_arq(arquivo_input)
    
    cctx = zstandard.ZstdCompressor(level=3) 
    dctx = zstandard.ZstdDecompressor()

    tempo_ini = time.perf_counter()
    with open(arquivo_input, "rb") as f_in, open(nome_comprimido, "wb") as f_out:
        dados = f_in.read()
        dados_comp = cctx.compress(dados)
        f_out.write(dados_comp)
    tempo_comprimir = time.perf_counter() - tempo_ini
    tamanho_comprimido = tamanho_arq(nome_comprimido)

    tempo_ini = time.perf_counter()
    with open(nome_comprimido, "rb") as f_in, open(nome_descomprimido, "wb") as f_out:
        dados_comp = f_in.read()
        dados_descomp = dctx.decompress(dados_comp)
        f_out.write(dados_descomp)
    tempo_descomprimir = time.perf_counter() - tempo_ini

    return algoritmo, tempo_comprimir, tempo_descomprimir, tamanho_inicial, tamanho_comprimido

if __name__ == "__main__":
    criar_arquivo_exemplo("arquivo_teste.txt", tamanho=int(input("Digite um número para o tamanho do arquivo teste em MB"))) #em megabytes

    lista_algoritmos = [
        teste_gzip,
        teste_bzip2,
        teste_xz_lzma2,
        teste_7zip_lzma2_py7zr,
        teste_brotli,
        teste_lz4,
        teste_snappy,
        teste_zstd,
    ]

    resultados = []

    print("\nIniciando testes de compactação...\n")
    for teste_func in lista_algoritmos:
        base_comp = "arquivo_teste.txt" + ".comprimido" 
        base_descomp = "arquivo_teste.txt" + ".descomprimido"
        
        for item in os.listdir('.'):
            if item.startswith(base_comp.split('/')[-1]) or item.startswith(base_descomp.split('/')[-1]):
                if os.path.isdir(item): 
                    shutil.rmtree(item)

        print(f"Testando {teste_func.__name__.replace('teste_', '').upper()}...")
        nome, comp_t, decomp_t, orig_s, comp_s = teste_func("arquivo_teste.txt")
        resultados.append((nome, comp_t, decomp_t, orig_s, comp_s))
        
        ratio = calcular_taxa_compactacao(orig_s, comp_s)
        print(f"  Tempo de Compactação: {comp_t:.4f}s")
        print(f"  Tempo de Descompactação: {decomp_t:.4f}s")
        print(f"  Tamanho Original: {orig_s / (1024*1024):.2f} MB")
        print(f"  Tamanho Compactado: {comp_s / (1024*1024):.2f} MB")
        print(f"  Taxa de Compactação: {ratio:.2f}%")
        print("-" * 30)

    print("\n--- Resultados Finais ---")
    print(f"{'Algoritmo':<30} | {'Tempo compr (s)':<15} | {'Tempo descomp (s)':<18} | {'Tamanho original (MB)':<19} | {'Tamanho compr (MB)':<15} | {'Taxa (%)':<10}")
    print("-" * 120)

    def ordenador(res):
        nome, comp_t, decomp_t, orig_s, comp_s = res
        ratio = calcular_taxa_compactacao(orig_s, comp_s)
        return (-ratio, comp_t) 

    resultados.sort(key=ordenador)

    for nome, tempo_comprimir, tempo_descomprimir, tamanho_inicial, tamanho_comprimido in resultados:
        mb_original = f"{tamanho_inicial / (1024*1024):.2f}"
        tempo_compr = f"{tempo_comprimir:.4f}"
        tempo_descompr = f"{tempo_descomprimir:.4f}"
        mb_compr = f"{tamanho_comprimido / (1024*1024):.2f}"
        taxa_comp = f"{calcular_taxa_compactacao(tamanho_inicial, tamanho_comprimido):.2f}"

        print(f"{nome:<30} | {tempo_compr:<15} | {tempo_descompr:<18} | {mb_original:<19} | {mb_compr:<15} | {taxa_comp:<10}")
