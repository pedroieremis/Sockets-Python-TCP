#ALUNOS:    PEDRO IÉREMIS BRITO DE MEDEIROS | MATRÍCULA: 20211014050019
#           RUTH CELESTE DO NASCIMENTO BORGES | MATRÍCULA: 20211014050007

import socket, threading, time#IMPORTAÇÃO DAS BIBLIOTECAS PARA USO
#ESTABELECIMENTO DE ENDEREÇO E PORTA PARA A CONEXÃO
ServerIP = '177.193.108.13'
PORT = 55555
#CRIAÇÃO DO SOCKET CLIENTE E PEDIDO DE CONEXÃO NO ENDEREÇO E PORTA INDICADO
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((ServerIP, PORT))
padrao_msg = ' >> '#CRIAÇÃO DE PROTOCOLO PADRÃO DE MENSAGEM

def msg_env(user):#CRIAÇÃO DE FUNÇÃO PARA O ENVIO DAS MENSAGENS
    #print('-'*70,'\nDigite: 01&& para logoff\n ')
    while True:#LAÇO PARA A THREAD FUNCIONAR CONSTANTEMENTE
        try:
            print('-'*70,'\nDigite: 01&& para logoff\n ')
            txt = input('> ')
            if txt == '01&&':#SE A MENSAGEM FOR A DO COMANDO DE LOGOFF, ENTRARÁ NO IF, ENVIADO A MENSAGEM DE LOGOFF AO SERVIDOR
                client.send(txt.encode('utf-8')) # FECHARÁ A CONEXÃO DO SOCKET E UM RETURN CONFIRMANDO ESTAR DESCONECTADO
                print('Desconectando...')
                client.close()
                time.sleep(0.5)
                return print('Desconectado !')
            else:#CASO CONTRÁRIO ELE ENVIARÁ TODAS AS DEMAIS MENSAGENS PARA PASSAR PELO SERVIDOR E CHEGAR AOS DEMAIS CLIENTES
                msg = f'{user}{padrao_msg}{txt}'
                client.send(msg.encode('utf-8'))
        except Exception as e:
             return print(f'Ocorreu algum erro ! 002\nERROR: {e}')#TRATAMENTO DE ERROS ENCERRANDO A FUNÇÃO COM O RETURN

def msg_rec():#CRIAÇÃO DA FUNÇÃO PARA RECEBER AS MENSAGENS DOS DEMAIS CLIENTES ENVIADAS PELO SERVIDOR
    while True:#LAÇO PARA A THREAD FUNCIONAR CONSTANTEMENTE
        try:
            msg = client.recv(2048).decode('utf-8')#RECEBENDO AS MENSAGENS E EXIBINDO
            print(msg)
        except:
            return print(f'Será Desconectado a Seguir.')#TRATAMENTO DE ERROS ENCERRANDO A FUNÇÃO COM O RETURN

def cliente():#CRIAÇÃO DE FUNÇÃO/MÉTODO PARA O CLIENTE
    try:#INSERÇÃO DE USUÁRIO E SENHA PARA EFETUAR LOGIN NO SERVIDOR E DEFINIR QUEM VOCÊ É NO CHAT
        print('Faça login no Chat;\n')
        user = input('Informe seu usuário: ')
        senha = input('Informe sua senha: ')
        #ENVIOS DE USUÁRIO E SENHA E RECEBIMENTO DA MENSAGEM DE LOGIN BEM OU MAL SUCEDIDO
        client.send(user.encode('utf-8'))
        client.send(senha.encode('utf-8'))
        msg_login = client.recv(64).decode('utf-8')
        if msg_login == 'Login Bem-Sucedido !':#SE LOGIN FOR BEM SUCEDIDO, CHAMARÁ AS THREADS QUE IRÃO ENVIAR E RECEBER MENSAGENS DO SERVIDOR
            print(msg_login+'\n')
            th1 = threading.Thread(target=msg_env, args=(user,))#CRIAÇÃO E INICIALIZAÇÃO DAS THREADS
            th1.start()
            th2 = threading.Thread(target=msg_rec)
            th2.start()
        else:
            return print(msg_login)#CASO O LOGIN NÃO SEJA BEM SUCEDIDO, MOSTRARÁ A MENSAGEM ENVIADA DO SERVIDOR ENCERRANDO COM O RETURN
    except Exception as e:
        return print(f'Ocoreu algum erro 001:\nERROR {e}')#TRATAMENTO DE ERROS ENCERRANDO O PROGRAMA POR NÃO TER EXISTIDO CONEXÃO

cliente()#CHAMANDO A FUNÇÃO PARA INICIAR AS FUNCIONALIDADES DO CLIENTE



