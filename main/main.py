import os
import pandas as pd
from datetime import date, timedelta
import sys
from config import *

sys.path.append(os.path.dirname(os.getcwd()))
from main_root import main


data_atual = date.today()
data_mes_anterior = data_atual - timedelta(days=30)

mes_atual = data_atual.strftime('%m')
ano_atual = data_atual.strftime('%Y')

# Formatar as datas no formato desejado
mes_anterior = data_mes_anterior.strftime('%m')
ano_anterior = data_mes_anterior.strftime('%Y')
data_atual_tratada = data_atual.strftime('%d/%m/%Y')

#Configurações e-mail
title_mes_anterior = f'Emissão Extrato nota fiscal {data_atual_tratada} Mês {mes_anterior}'
title_mes_atual = f'Emissão Extrato nota fiscal {data_atual_tratada} Mês {mes_atual}'
body = 'Emissao Extrato Nota Fiscal - Automático'#Texto do e-mail
sender_email = "rpa@gmail.com" #e-mail de envio
receiver_email = 'email@gmail.com', 'planoacont.atendimento@gmail.com'
password = 'password' #Senha de e-mail de envio
# file_paths = #lista dos caminhos dos arquivos


main(mes_anterior,ano_anterior,sender_email, password, receiver_email, title_mes_anterior, body, file_paths=None)
print('Fazendo mes atual')
main(mes_atual,ano_atual,sender_email, password, receiver_email, title_mes_atual, body, file_paths=None)
