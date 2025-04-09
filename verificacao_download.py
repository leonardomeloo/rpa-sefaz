import os
import pandas as pd

def verificacao_download_pdf():
    diretorio_atual = os.getcwd()
    print('Verificando download do arquivo PDF')

    while True:
        for arquivo in os.listdir(diretorio_atual):
            if arquivo.endswith('.pdf'):
                print('Download concluído com sucesso.')
                break
        else:
            continue  
        break  

def verificacao_download_xls():
    diretorio_atual = os.getcwd()
    print('Verificando download do arquivo XLS')

    while True:
        for arquivo in os.listdir(diretorio_atual):
            if arquivo.endswith('.xls'):
                print('Download concluído com sucesso.')
                break
        else:
            continue  
        break 

def verificacao_celula_vazia(tabela):
    
    # Carregar o arquivo XLS
    df = pd.read_excel(tabela)

    # Verificar se alguma célula não foi preenchida
    celula_vazia = False
    for coluna in ['Status_não_calculado', 'Status_PDF', 'Status_XLS']:
        if df[coluna].isnull().any():
            celula_vazia = True
            break

    # Verificar se alguma célula não foi preenchida
    if celula_vazia:
        print("Pelo menos uma célula não foi preenchida nas três colunas.")
        return True
    else:
        print("Todas as células estão preenchidas nas três colunas.\nPassando para o proximo passo...")
        return False
