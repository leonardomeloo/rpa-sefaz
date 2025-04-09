import os
import zipfile

def zipar_pasta(destino, nome_zip):
    with zipfile.ZipFile(nome_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(destino):
            for file in files:
                arquivo = os.path.join(root, file)
                zipf.write(arquivo, os.path.relpath(arquivo, destino))


