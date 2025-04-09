from selenium import webdriver
import pandas as pd
import shutil
from verificacao_download import verificacao_download_pdf, verificacao_download_xls
from tratamento_inscricao_estadual import inscricao_estadual_zero_inicio
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import os
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import subprocess

def extrato_nota_fiscal(mes,ano):
    
    while 1:
        try:
            # Inicializar o Selenium
            diretorio_atual = os.getcwd()
            diretorio_pai = os.path.dirname(diretorio_atual)
            diretorio_destino_pdf = os.path.join(diretorio_pai,'Notas_PDF')
            diretorio_destino_xls = os.path.join(diretorio_pai,'Notas_XLS')
            tabela = pd.read_excel('TABELA DAS EMPRESAS.XML')
            
            #Entrando no site
            options = Options()

            options.add_argument("--disable-popup-blocking")  # Desativar o bloqueio de pop-ups

            prefs = {
                        
                        "download.default_directory": diretorio_atual, 
                        "savefile.default_directory": diretorio_atual,
                        "download.prompt_for_download": False,
                        "download.directory_upgrade": True,
                        "plugins.always_open_pdf_externally": True,
                        "ignore-certificate-errors": True,
                        "ignore-ssl-errors=yes": True,
                        "allow-running-insecure-content": True,
                        "disable-web-security": True,
                        "profile.accept_untrusted_certs": True,
                        "safebrowsing.enabled": True,
                        "plugins.plugins_disabled": ["Chrome PDF Viewer"],
                        "safebrowsing.disable_download_protection": True,
                        "profile.default_content_settings.popups": 0,        
                }


            options.add_experimental_option("prefs", prefs)
            #------------------------

            browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


            browser.maximize_window()

            # Navegar até o site
            browser.get('https://efisco.sefaz.pe.gov.br/sfi_com_sca/PRMontarMenuAcesso')
            sleep(2)
            browser.find_element(By.XPATH, '//*[@id="botao_gov_br"]').click()
            sleep(1)

            ################## usando SUBPROCESS###########################
                #colocar na pasta do projeto para setar o caminho com 'OS'
            caminho_python = fr'C:\Users\leona\AppData\Local\Programs\Python\Python310\python.exe'
            caminho_codigo = fr'C:\Projetos Python\sub_programa\click_ok.py'

            # Iniciar o processo para executar o segundo código
            subprocess.Popen([caminho_python, caminho_codigo])

            ################## usando SUBPROCESS###########################
            WebDriverWait(browser,13).until(EC.presence_of_element_located((By.XPATH, '//*[@id="cert-digital"]/button'))).click()

            browser.find_element(By.LINK_TEXT, 'Extrato Contribuinte - CONTESTAÇÃO').click()

            


            for index, row in tabela.iterrows():
                
                if pd.isnull(row['Status_não_calculado']) or pd.isnull(row['Status_PDF']) or pd.isnull(row['Status_XLS']) :
                    if pd.isnull(tabela.loc[index, 'Status_não_calculado']):
                        print('VERIFICANDO NÃO CALCULADO')
                        if browser.find_element(By.XPATH, '//*[@id="primeiro_campo"]').text == '':
                        
                            browser.find_element(By.NAME, 'DtPeriodoFiscal').send_keys(mes)
                            sleep(0.8)
                            browser.find_element(By.NAME, 'DtPeriodoFiscal').send_keys(ano)
                            
                        sleep(1.2)
                        browser.find_element(By.ID, 'nuDocumentoIdentificacao').clear()
                        sleep(0.8)
                        browser.find_element(By.ID, 'nuDocumentoIdentificacao').send_keys(inscricao_estadual_zero_inicio(str(row['inscricao_estadual'])))
                        sleep(1)
                        browser.find_element(By.XPATH, '//*[@id="bttemitirRelatorioNaoCalculadas"]').click()
                        sleep(1)
                        if WebDriverWait(browser,10).until(EC.presence_of_element_located((By.ID, 'btt_prosseguir'))):
                            print('Entrou no prosseguir')
                            try:
                                WebDriverWait(browser, 3).until(EC.text_to_be_present_in_element_value((By.XPATH, '//*[@id="corpo"]/form/div[2]/div/div/div/div[2]/p[2]/input'), 'Salvar documento (s)'))
                                if browser.find_element(By.XPATH, '//*[@id="corpo"]/form/div[2]/div/div/div/div[2]/p[2]/input').get_attribute('value') == 'Salvar documento (s)':
                                    print('Entrou no botão salvar')
                                    browser.find_element(By.XPATH, '//*[@id="corpo"]/form/div[2]/div/div/div/div[2]/p[2]/input').click()
                                    print('Clicou')
                                    verificacao_download_pdf()
                                    
                                    caminho_origem = os.path.join(diretorio_atual,'RelatorioExtratoNaoCalculadas.pdf')
                                    print(caminho_origem)
                                    nome_arquivo = row['apelido'] + '_NÃO_CALCULADO' +'.pdf'
                                    caminho_destino = os.path.join(diretorio_destino_pdf,nome_arquivo)
                                    shutil.move(caminho_origem, caminho_destino)
                                    print('Arquivo PDF, movido com sucesso.')
                                    tabela.at[index, 'Status_não_calculado'] = 'OK'
                                    tabela.to_excel('TABELA DAS EMPRESAS.XML',index=False)
                                    print(f"Inscrição  NÃO CALCULADO {row['inscricao_estadual']}, OK salvo Status_PDF")
                                    sleep(1)
                                    browser.find_element(By.ID, 'btt_prosseguir').click()
                        
                    
                            except:
                                browser.find_element(By.ID, 'btt_prosseguir').click()
                                tabela.at[index, 'Status_não_calculado'] = 'Sem movimento'
                                tabela.to_excel('TABELA DAS EMPRESAS.XML',index=False)


                # arquivo de saida para PDF não precisa ser clicado

                
                if pd.isnull(tabela.loc[index, 'Status_PDF']):
                    print('VERIFICANDO PDF')
                    if browser.find_element(By.ID, 'primeiro_campo').text == '':
                        browser.find_element(By.NAME, 'DtPeriodoFiscal').send_keys(mes)
                        sleep(0.8)
                        browser.find_element(By.NAME, 'DtPeriodoFiscal').send_keys(ano)

                    # sleep(1.2)
                    # browser.find_element(By.ID, 'nuDocumentoIdentificacao').clear()
                    # sleep(1)
                    # browser.find_element(By.ID, 'nuDocumentoIdentificacao').send_keys(inscricao_estadual_zero_inicio(str(row['inscricao_estadual'])))

                    #Pegando o arquivo no formato PDF
                    #verificação do download, mudança de nome para o da apelido e mover para a pasta de pdf
                    browser.find_element(By.ID, 'bttemitirRelatorioCalculadas').click()

                    try:
                        WebDriverWait(browser, 3).until( EC.presence_of_element_located((By.XPATH, '//*[@id="corpo"]/form/div[2]/div/div/div/div[2]/p[2]/input'))).click()

                        verificacao_download_pdf()
                        sleep(2)
                        caminho_origem = os.path.join(diretorio_atual,'RelatorioExtratoCalculadas.pdf')
                        nome_arquivo = row['apelido'] + '.pdf'
                        caminho_destino = os.path.join(diretorio_destino_pdf,nome_arquivo)
                        shutil.move(caminho_origem, caminho_destino)
                        print('Arquivo PDF, movido com sucesso.')
                        tabela.loc[index, 'Status_PDF'] = 'OK'
                        tabela.to_excel('TABELA DAS EMPRESAS.XML',index=False)
                        print(f"Inscrição {row['inscricao_estadual']}, OK salvo Status_PDF")
                        sleep(1)
                        browser.find_element(By.ID, 'btt_prosseguir').click()
                    except:

                        tabela.loc[index, 'Status_PDF'] = 'Sem movimento'
                        tabela.to_excel('TABELA DAS EMPRESAS.XML',index=False)
                        print(f"Inscrição {row['inscricao_estadual']}, Não encontrada informação, salvo Status_PDF")
                        browser.find_element(By.ID, 'btt_prosseguir').click()

                #Pegando arquivo no formato XLS
                #verificação download xls mudança de nome e mover para a pasta de xls
                if pd.isnull(tabela.loc[index, 'Status_XLS']):
                        print('VERIFICANDO XLS')
                        if browser.find_element(By.ID, 'primeiro_campo').text == '':
                            browser.find_element(By.NAME, 'DtPeriodoFiscal').send_keys(mes)
                            sleep(0.8)
                            browser.find_element(By.NAME, 'DtPeriodoFiscal').send_keys(ano)

                        # sleep(1.2)
                        # browser.find_element(By.ID, 'nuDocumentoIdentificacao').clear()
                        # sleep(1)
                        # browser.find_element(By.ID, 'nuDocumentoIdentificacao').send_keys(inscricao_estadual_zero_inicio(str(row['inscricao_estadual'])))
                        #Clicando o arquivo no formato XLS
                        browser.find_element(By.XPATH, '//*[@id="table_filtro"]/tbody/tr[4]/td/input[2]').click()
                        sleep(0.5)
                        browser.find_element(By.ID, 'bttemitirRelatorioCalculadas').click()
                        
                        try:
                            WebDriverWait(browser, 3).until( EC.presence_of_element_located((By.XPATH, '//*[@id="corpo"]/form/div[2]/div/div/div/div[2]/p[2]/input'))).click()

                            verificacao_download_xls()
                            sleep(2)
                            caminho_origem = os.path.join(diretorio_atual,'RelatorioExtratoCalculadas.xls')
                            nome_arquivo = row['apelido'] + '.xls'
                            caminho_destino = os.path.join(diretorio_destino_xls,nome_arquivo)
                            shutil.move(caminho_origem, caminho_destino)
                            print('Arquivo XLS, movido com sucesso.')
                            tabela.loc[index, 'Status_XLS'] = 'OK'
                            tabela.to_excel('TABELA DAS EMPRESAS.XML',index=False)
                            print(f"Inscrição {row['inscricao_estadual']}, OK salvo Status_XLS")
                            browser.find_element(By.ID, 'btt_prosseguir').click()
                        except:
                            
                            tabela.loc[index, 'Status_XLS'] = 'Sem movimento'
                            tabela.to_excel('TABELA DAS EMPRESAS.XML',index=False)
                            print(f"Inscrição {row['inscricao_estadual']}, Não encontrada informação, salvo Status_XLS")
                            browser.find_element(By.ID, 'btt_prosseguir').click()
                
            print('Terminou')
            browser.close()
            break
        except Exception as error:
            print(error)
            browser.close()
            continue



