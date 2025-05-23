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

def サンプル_を_作成する(ファイル名, サイズ=1):
    if not os.path.exists(ファイル名): #フォルダに存在しない場合のみファイルを作成します
        最終_繰り返し = "これは圧縮用のサンプルテキストです。繰り返しは良い圧縮の鍵です。 " * 200
        繰り返し_テキスト = "圧縮アルゴリズム用のテスト文字列 ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz 0123456789 !@#$%^&*()_+[];',./{}|:<>?\n"
        行数 = (サイズ * 1024 * 1024) // len(繰り返し_テキスト.encode('utf-8'))
        if 行数 == 0:
            行数 = 100 
        with open(ファイル名, "w", encoding="utf-8") as f:
            for i in range(行数):
                f.write(f"{i}: {繰り返し_テキスト}")
            f.write(最終_繰り返し * (サイズ * 2)) 

def ファイルサイズ_を_取得する(パス):
    if os.path.exists(パス):
        return os.path.getsize(パス)
    return 0

def 圧縮率_を_計算する(初期_サイズ, 圧縮_サイズ):
    if 初期_サイズ == 0:
        return 0
    return ((初期_サイズ - 圧縮_サイズ) / 初期_サイズ) * 100 #パーセント

def gzip_を_テストする(入力ファイル):
    アルゴリズム = "GZip (DEFLATE)"
    圧縮ファイル名 = 入力ファイル + ".圧縮済み" + ".gz"
    解凍ファイル名 = 入力ファイル + ".解凍済み" + ".gz.txt"
    初期_サイズ = ファイルサイズ_を_取得する(入力ファイル)
    
    開始時間 = time.perf_counter()
    with open(入力ファイル, "rb") as f_in, gzip.open(圧縮ファイル名, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)
    圧縮時間 = time.perf_counter() - 開始時間
    圧縮_サイズ = ファイルサイズ_を_取得する(圧縮ファイル名)

    開始時間 = time.perf_counter()
    with gzip.open(圧縮ファイル名, "rb") as f_in, open(解凍ファイル名, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)
    解凍時間 = time.perf_counter() - 開始時間
    
    return アルゴリズム, 圧縮時間, 解凍時間, 初期_サイズ, 圧縮_サイズ

def bzip2_を_テストする(入力ファイル):
    アルゴリズム = "BZip2 (Burrows-Wheeler)"
    圧縮ファイル名 = 入力ファイル + ".圧縮済み" + ".bz2"
    解凍ファイル名 = 入力ファイル + ".解凍済み" + ".bz2.txt"
    初期_サイズ = ファイルサイズ_を_取得する(入力ファイル)

    開始時間 = time.perf_counter()
    with open(入力ファイル, "rb") as f_in, bz2.open(圧縮ファイル名, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)
    圧縮時間 = time.perf_counter() - 開始時間
    圧縮_サイズ = ファイルサイズ_を_取得する(圧縮ファイル名)

    開始時間 = time.perf_counter()
    with bz2.open(圧縮ファイル名, "rb") as f_in, open(解凍ファイル名, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)
    解凍時間 = time.perf_counter() - 開始時間

    return アルゴリズム, 圧縮時間, 解凍時間, 初期_サイズ, 圧縮_サイズ

def xz_lzma2_を_テストする(入力ファイル):
    アルゴリズム = "Xz (LZMA2)"
    圧縮ファイル名 = 入力ファイル + ".圧縮済み" + ".xz"
    解凍ファイル名 = 入力ファイル + ".解凍済み" + ".xz.txt"
    初期_サイズ = ファイルサイズ_を_取得する(入力ファイル)

    開始時間 = time.perf_counter()
    with open(入力ファイル, "rb") as f_in, lzma.open(圧縮ファイル名, "wb", format=lzma.FORMAT_XZ, preset=6) as f_out:
        shutil.copyfileobj(f_in, f_out)
    圧縮時間 = time.perf_counter() - 開始時間
    圧縮_サイズ = ファイルサイズ_を_取得する(圧縮ファイル名)

    開始時間 = time.perf_counter()
    with lzma.open(圧縮ファイル名, "rb", format=lzma.FORMAT_XZ) as f_in, open(解凍ファイル名, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)
    解凍時間 = time.perf_counter() - 開始時間
        
    return アルゴリズム, 圧縮時間, 解凍時間, 初期_サイズ, 圧縮_サイズ

def 7zip_lzma2_py7zr_を_テストする(入力ファイル):
    アルゴリズム = "7-zip (LZMA2 via py7zr)"
    圧縮ファイル名 = 入力ファイル + ".圧縮済み" + ".7z"
    解凍フォルダ = 入力ファイル + ".解凍済み" + "_7z"
    初期_サイズ = ファイルサイズ_を_取得する(入力ファイル)
    
    lzma_フィルター = [{'id': py7zr.FILTER_LZMA2, 'preset': 5}] 

    開始時間 = time.perf_counter()
    with py7zr.SevenZipFile(圧縮ファイル名, 'w', filters=lzma_フィルター) as ファイル:
        ファイル.write(入力ファイル, arcname=os.path.basename(入力ファイル))
    圧縮時間 = time.perf_counter() - 開始時間
    圧縮_サイズ = ファイルサイズ_を_取得する(圧縮ファイル名)

    開始時間 = time.perf_counter()
    os.makedirs(解凍フォルダ, exist_ok=True)
    with py7zr.SevenZipFile(圧縮ファイル名, 'r') as ファイル:
        ファイル.extractall(path=解凍フォルダ)
    解凍時間 = time.perf_counter() - 開始時間

    if os.path.exists(解凍フォルダ):
        shutil.rmtree(解凍フォルダ)
        
    return アルゴリズム, 圧縮時間, 解凍時間, 初期_サイズ, 圧縮_サイズ


def brotli_を_テストする(入力ファイル):
    アルゴリズム = "Brotli (BROTLI)"
    圧縮ファイル名 = 入力ファイル + ".圧縮済み" + ".br"
    解凍ファイル名 = 入力ファイル + ".解凍済み" + ".br.txt"
    初期_サイズ = ファイルサイズ_を_取得する(入力ファイル)

    開始時間 = time.perf_counter()
    with open(入力ファイル, "rb") as f_in:
        データ = f_in.read()
    データ_圧縮 = brotli.compress(データ, quality=6)
    with open(圧縮ファイル名, "wb") as f_out:
        f_out.write(データ_圧縮)
    圧縮時間 = time.perf_counter() - 開始時間
    圧縮_サイズ = ファイルサイズ_を_取得する(圧縮ファイル名)

    開始時間 = time.perf_counter()
    with open(圧縮ファイル名, "rb") as f_in:
        データ_圧縮 = f_in.read()
    データ_解凍 = brotli.decompress(データ_圧縮)
    with open(解凍ファイル名, "wb") as f_out:
        f_out.write(データ_解凍)
    解凍時間 = time.perf_counter() - 開始時間

    return アルゴリズム, 圧縮時間, 解凍時間, 初期_サイズ, 圧縮_サイズ

def lz4_を_テストする(入力ファイル):
    アルゴリズム = "LZ4 (LZ4)"
    圧縮ファイル名 = 入力ファイル + ".圧縮済み" + ".lz4"
    解凍ファイル名 = 入力ファイル + ".解凍済み" + ".lz4.txt"
    初期_サイズ = ファイルサイズ_を_取得する(入力ファイル)

    開始時間 = time.perf_counter()
    with open(入力ファイル, "rb") as f_in, lz4.frame.open(圧縮ファイル名, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)
    圧縮時間 = time.perf_counter() - 開始時間
    圧縮_サイズ = ファイルサイズ_を_取得する(圧縮ファイル名)

    開始時間 = time.perf_counter()
    with lz4.frame.open(圧縮ファイル名, "rb") as f_in, open(解凍ファイル名, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)
    解凍時間 = time.perf_counter() - 開始時間

    return アルゴリズム, 圧縮時間, 解凍時間, 初期_サイズ, 圧縮_サイズ

def snappy_を_テストする(入力ファイル):
    アルゴリズム = "Snappy (LZ77)"
    圧縮ファイル名 = 入力ファイル + ".圧縮済み" + ".snappy"
    解凍ファイル名 = 入力ファイル + ".解凍済み" + ".snappy.txt"
    初期_サイズ = ファイルサイズ_を_取得する(入力ファイル)

    開始時間 = time.perf_counter()
    with open(入力ファイル, "rb") as f_in:
        データ = f_in.read()
    データ_圧縮 = snappy.compress(データ)
    with open(圧縮ファイル名, "wb") as f_out:
        f_out.write(データ_圧縮)
    圧縮時間 = time.perf_counter() - 開始時間
    圧縮_サイズ = ファイルサイズ_を_取得する(圧縮ファイル名)

    開始時間 = time.perf_counter()
    with open(圧縮ファイル名, "rb") as f_in:
        データ_圧縮 = f_in.read()
    データ_解凍 = snappy.decompress(データ_圧縮)
    with open(解凍ファイル名, "wb") as f_out:
        f_out.write(データ_解凍)
    解凍時間 = time.perf_counter() - 開始時間

    return アルゴリズム, 圧縮時間, 解凍時間, 初期_サイズ, 圧縮_サイズ

def zstd_を_テストする(入力ファイル):
    アルゴリズム = "Zstd (ZSTD)"
    圧縮ファイル名 = 入力ファイル + ".圧縮済み" + ".zst"
    解凍ファイル名 = 入力ファイル + ".解凍済み" + ".zst.txt"
    初期_サイズ = ファイルサイズ_を_取得する(入力ファイル)
    
    cctx = zstandard.ZstdCompressor(level=3) 
    dctx = zstandard.ZstdDecompressor()

    開始時間 = time.perf_counter()
    with open(入力ファイル, "rb") as f_in, open(圧縮ファイル名, "wb") as f_out:
        データ = f_in.read()
        データ_圧縮 = cctx.compress(データ)
        f_out.write(データ_圧縮)
    圧縮時間 = time.perf_counter() - 開始時間
    圧縮_サイズ = ファイルサイズ_を_取得する(圧縮ファイル名)

    開始時間 = time.perf_counter()
    with open(圧縮ファイル名, "rb") as f_in, open(解凍ファイル名, "wb") as f_out:
        データ_圧縮 = f_in.read()
        データ_解凍 = dctx.decompress(データ_圧縮)
        f_out.write(データ_解凍)
    解凍時間 = time.perf_counter() - 開始時間

    return アルゴリズム, 圧縮時間, 解凍時間, 初期_サイズ, 圧縮_サイズ

if __name__ == "__main__":
    サンプル_を_作成する("arquivo_teste.txt", サイズ=int(input("MBでテストファイルのサイズの数字を入力してください"))) #メガバイトで

    アルゴリズム_リスト = [
        gzip_を_テストする,
        bzip2_を_テストする,
        xz_lzma2_を_テストする,
        7zip_lzma2_py7zr_を_テストする,
        brotli_を_テストする,
        lz4_を_テストする,
        snappy_を_テストする,
        zstd_を_テストする,
    ]

    結果 = []

    print("\n圧縮テストの開始...\n")
    for テスト関数 in アルゴリズム_リスト:
        ベース_圧縮 = "arquivo_teste.txt" + ".圧縮済み" 
        ベース_解凍 = "arquivo_teste.txt" + ".解凍済み"
        
        for 項目 in os.listdir('.'):
            if 項目.startswith(ベース_圧縮.split('/')[-1]) or 項目.startswith(ベース_解凍.split('/')[-1]):
                if os.path.isdir(項目): 
                    shutil.rmtree(項目)

        print(f"{テスト関数.__name__.replace('_を_テストする', '').upper()}のテスト...")
        名前, 圧縮_t, 解凍_t, 初期_s, 圧縮_s = テスト関数("arquivo_teste.txt")
        結果.append((名前, 圧縮_t, 解凍_t, 初期_s, 圧縮_s))
        
        比率 = 圧縮率_を_計算する(初期_s, 圧縮_s)
        print(f"  圧縮時間: {圧縮_t:.4f}秒")
        print(f"  解凍時間: {解凍_t:.4f}秒")
        print(f"  オリジナルサイズ: {初期_s / (1024*1024):.2f} MB")
        print(f"  圧縮サイズ: {圧縮_s / (1024*1024):.2f} MB")
        print(f"  圧縮率: {比率:.2f}%")
        print("-" * 30)

    print("\n--- 最終結果 ---")
    print(f"{'アルゴリズム':<30} | {'圧縮時間 (秒)':<15} | {'解凍時間 (秒)':<18} | {'オリジナルサイズ (MB)':<19} | {'圧縮サイズ (MB)':<15} | {'圧縮率 (%)':<10}")
    print("-" * 120)

    def ソートキー(結果):
        名前, 圧縮_t, 解凍_t, 初期_s, 圧縮_s = 結果
        比率 = 圧縮率_を_計算する(初期_s, 圧縮_s)
        return (-比率, 圧縮_t) 

    結果.sort(key=ソートキー)

    for 名前, 圧縮_時間, 解凍_時間, 初期_サイズ, 圧縮_サイズ in 結果:
        mb_オリジナル = f"{初期_サイズ / (1024*1024):.2f}"
        時間_圧縮 = f"{圧縮_時間:.4f}"
        時間_解凍 = f"{解凍_時間:.4f}"
        mb_圧縮 = f"{圧縮_サイズ / (1024*1024):.2f}"
        比率_圧縮 = f"{圧縮率_を_計算する(初期_サイズ, 圧縮_サイズ):.2f}"

        print(f"{名前:<30} | {時間_圧縮:<15} | {時間_解凍:<18} | {mb_オリジナル:<19} | {mb_圧縮:<15} | {比率_圧縮:<10}")