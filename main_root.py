from verificacao_download import verificacao_celula_vazia
from extrato_nota_fiscal import extrato_nota_fiscal
from zipar_arquivo import zipar_pasta
from limpar_colunas import limpar_colunas
from email_gmail import enviar
from limpar_pasta import limpar_pasta
import os
import pandas as pd

def main(mes,ano,sender_email, password, receiver_email, title, body, file_paths=None):
    file_name = 'TABELA DAS EMPRESAS.XML'
    if verificacao_celula_vazia(file_name) == True:
       
        print('EXTRATO NOTA FISCAL INICIADO')
        extrato_nota_fiscal(mes,ano)

    #Verificação para iniciar o RPA:           #false
    if verificacao_celula_vazia(file_name) == False:
        
        print("Zipando pastas PDF e XLS")
        zipar_pasta(os.path.join(os.path.dirname(os.getcwd()),f'Notas_PDF'),    f'Notas_PDF_mes_{mes}.zip')
        zipar_pasta(os.path.join(os.path.dirname(os.getcwd()),'Notas_XLS'),     f'Notas_XLS_mes_{mes}.zip')
        file_paths = [os.path.join(os.getcwd(),f'Notas_PDF_mes_{mes}.zip') , os.path.join(os.getcwd(),f'Notas_XLS_mes_{mes}.zip'), os.path.join(os.getcwd(),file_name)]
        enviar(sender_email, password, receiver_email, title, body, file_paths)
        print('Limpando colunas')
        limpar_colunas(file_name,['Status_não_calculado', 'Status_PDF', 'Status_XLS'])
        print('Limpando pastas PDF e XLS')
        limpar_pasta('Notas_PDF')
        limpar_pasta('Notas_XLS')

    
        