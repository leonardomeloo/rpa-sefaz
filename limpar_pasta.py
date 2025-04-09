import os

def limpar_pasta(nome_pasta):
    pasta_pai = os.path.dirname(os.getcwd())
    pasta = os.path.join(pasta_pai, nome_pasta)  # Substitua pelo caminho da pasta que deseja limpar

    # Percorra todos os arquivos da pasta
    for arquivo in os.listdir(pasta):
        caminho_arquivo = os.path.join(pasta, arquivo)  # Obtém o caminho completo do arquivo
        if os.path.isfile(caminho_arquivo):  # Verifica se é um arquivo
            os.remove(caminho_arquivo)  # Apaga o arquivo

    print('Todos os arquivos foram removidos da pasta.')
