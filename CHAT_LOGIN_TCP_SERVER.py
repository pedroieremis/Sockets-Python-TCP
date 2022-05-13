#ALUNOS:    PEDRO IÉREMIS BRITO DE MEDEIROS | MATRÍCULA: 20211014050019
#           RUTH CELESTE DO NASCIMENTO BORGES | MATRÍCULA: 20211014050007

import socket, threading#IMPORTAÇÃO DAS BIBLIOTECAS PARA USO
#ESTABELECIMENTO DE ENDEREÇO E PORTA PARA A CONEXÃO
HOST = '192.168.0.13'
PORT = 55555
#CRIAÇÃO DO SOCKET SERVIDOR, ATIVAÇÃO E ESCUTA DELE
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
#CRIAÇÃO DE LISTAS, LOGINS E PROTOCOLOS PADRÃO
clients = []
keys0 = ['F11123', 'F16456', 'F22789']
msg_reply_no = 'Login Não Reconhecido !'
msg_reply_yes = 'Login Bem-Sucedido !'
#DEFINIÇÃO DO MÉTODO PARA ENVIO GERAL DAS MENSAGENS DO SERVIDOR AO(S) CLIENTE(S)
def alls(data, msg):
    for all in clients:
        if all != data:
            all.send(msg.encode('utf-8'))
#CRIAÇÃO DA FUNÇÃO QUE AVERIGUA OS LOGINS E TRATA TODAS AS MENSAGENS
def tratamento(data):
    try:#VERIFICAÇÃO DO LOGIN
        user = data.recv(64).decode('utf-8')
        key = data.recv(64).decode('utf-8')
        login = user+key
        if login in keys0:#ADIÇÃO DO CLIENTE NA LISTA DE CLIENTES E ENVIO DE ENTRADA DO MESMO EM BROADCAST PARA OS DEMAIS CLIENTES SE HOUVER
            clients.append(data)
            msg_reply_all_01 = f'{user} Entrou no Chat !!'
            alls(data, msg_reply_all_01)
            data.send(msg_reply_yes.encode('utf-8'))#CASO CLIENTE TENHA ACESSO, SERÁ ENVIADO A MENSAGEM DO PROTOCOLO
            while True:#CRIAÇÃO DO LAÇO INFINITO PARA O USO DA THREAD QUE RECEBE AS MENSAGENS E FAZ TODOS OS TRATAMENTOS NECESSÁRIOS PARA ENVIO
                try:
                    msg_rev = data.recv(2048).decode('utf-8')
                    if msg_rev == '01&&':#SE CLIENTE OPTAR POR LOGOFF, CHAMARÁ O MÉTODO DE BROADCAST E O CLIENTE SERÁ REMOVIDO DAS CONEXÕES
                        print(f'Fechando conexão com {data}')
                        msg_reply_all_02 = f'{user} Está saindo do Chat !!'
                        alls(data, msg_reply_all_02)
                        clients.remove(data)
                        return print('Conexão Fechada !')#ENCERRANDO A FUNÇÃO COM O RETURN APÓS REMOÇÃO DO CLIENTE
                    else:
                        alls(data, msg_rev)#CASO SEJA QUALQUER OUTRA MENSAGEM, SIMPLESMENTE ENVIARÁ PARA OS DEMAIS CLIENTES
                except Exception as er:
                   return print(f'ERRO 002: {er}')#TRATAMENTO DE ERROS ENCERRANDO A FUNÇÃO COM O RETURN
        else:
            data.send(msg_reply_no.encode('utf-8'))#CASO O CLIENTE NÃO TENHA ACESSO (LOGIN ERRADO) SERÁ ENVIADO A MENSAGEM DO PROTOCOLO
    except Exception as e:
        return print(f'ERRO 003: {e}')#TRATAMENTO DE ERROS ENCERRANDO A FUNÇÃO COM O RETURN

def serv():#CRIAÇÃO DE FUNÇÃO/MÉTODO PARA O SERVIDOR ACEITAR E CHAMAR A THREAD QUE TRATARÁ AS MENSAGENS
    while True:
        try:
            print('\nAguardando nova conexão...')
            data, conn = server.accept()#SERVIDOR ACEITANDO CONEXÕES
            print(f'Nova conexão aceita !\nCliente: {conn}')
            th1 = threading.Thread(target=tratamento, args=(data,))#CRIAÇÃO E INICIALIZAÇÃO DA THREAD
            th1.start()
        except Exception as e:
            print(f'ERRO 001: {e}')#TRATAMENTO DE ERROS COM O CONTINUE PARA VOLTAR A ACEITAR CONEXÕES
            continue

serv()#CHAMADA DA  FUNÇÃO INICIAL