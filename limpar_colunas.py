import pandas as pd

def limpar_colunas(file_name,lista_colunas):
    tabela = pd.read_excel(file_name)

    for nome_coluna in lista_colunas:
        tabela[nome_coluna] = ''
        tabela.to_excel(file_name,index=False)


