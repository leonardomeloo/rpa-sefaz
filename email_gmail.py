import yagmail

def enviar(sender_email, password, receiver_email, title, body, file_paths):
    # Credenciais de login
    email = sender_email
    senha = password

    # Detalhes do e-mail
    para = receiver_email
    assunto = title
    mensagem = body

    # Cria uma conexão com o servidor SMTP do Gmail
    yag = yagmail.SMTP(email, senha)

    # Cria uma lista para armazenar os conteúdos (mensagens e arquivos) a serem enviados
    contents = [mensagem]

    # Adiciona os arquivos da lista ao conteúdo a ser enviado
    for file_path in file_paths:
        contents.append(file_path)

    # Envia o e-mail com os arquivos anexados
    yag.send(
        to=para,
        subject=assunto,
        contents=contents
    )

    print('E-MAIL ENVIADO COM SUCESSO!')
