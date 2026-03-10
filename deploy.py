#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path

def git_tracked_files():
    # Lista arquivos rastreados (respeita .gitignore)
    out = subprocess.check_output(["git", "ls-files", "-z"])
    files = [p for p in out.decode("utf-8").split("\x00") if p]
    return files

def ensure_dirs_on_board(paths):
    # Cria as pastas necessárias na placa, em ordem de profundidade
    dirs = sorted({os.path.dirname(p) for p in paths if "/" in p}, key=lambda d: d.count("/"))
    for d in dirs:
        if not d or d == ".":
            continue
        # Ignora erro se já existir
        subprocess.run(["mpremote", "mkdir", f":{d}"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def copy_files(paths):
    for p in paths:
        if not Path(p).is_file():
            continue
        # Garante separador POSIX no destino
        dest = p.replace(os.sep, "/")
        print(f"📤 {p} -> :{dest}")
        # Falha interrompe para você ver qual arquivo deu erro
        subprocess.run(["mpremote", "cp", p, f":{dest}"], check=True)

if __name__ == "__main__":
    files = git_tracked_files()          # respeita .gitignore
    ensure_dirs_on_board(files)          # cria pastas na placa
    copy_files(files)                    # envia arquivos
    print("✅ Deploy concluído.")
