import os
from datetime import date

data = date.today()
mes_atual = data.strftime('%m')
mes_anterior = int(mes_atual) - 1
mes_anterior = '0' + str(mes_anterior)
ano = data.strftime('%Y')

# Inicializar o Selenium
diretorio_atual = os.getcwd()
diretorio_pai = os.path.dirname(diretorio_atual)
diretorio_destino_pdf = os.path.join(diretorio_pai,'Notas_PDF')
diretorio_destino_xls = os.path.join(diretorio_pai,'Notas_XLS')
