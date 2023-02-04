import socket, struct
#Definição das variáveis
print('Iniciando...')
SERVER = '127.0.0.1'
PORT = 12345

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #criação do socket TCP
sock.connect((SERVER, PORT)) #Fazendo conexão com o servidor
print('Conectado ao servidor.\n')

sock.settimeout(None)
op = 'sim'
while op.lower() == 'sim':
    try: #inicio da estação do tratamento de erro
        nameArq = input('Digite o nome do arquivo desejado: ').encode()
        sock.send(nameArq)#envio do pedido
        tam = sock.recv(512) #recebimento do tamanho do pedido
        s = struct.unpack('I', tam)[0]
        print(f'Arquivo pedido: {nameArq.decode()}\nTamanho do arquivo: {s} bytes.')

        cont_arq = b''
        pos = 0
        while s > pos: #loop para armazenamento do arquivo, de forma fracionada até que se complete
            #print(end='.') # Se tirar do comentário e testar com arquivo grande, leva bastante tempo imprimindo os pontos, um vídeo por exemplo
            data = sock.recv(4096)
            cont_arq += data
            pos += len(data)
        with open(nameArq, 'wb') as arq: #criação e escrita do arquivo
            w = arq.write(cont_arq)

        op = input('Deseja continuar conectado? (sim ou não) ')
        print('='*70)
    except Exception as e:
        print(f'Ocorreu algum erro na aplicação cliente !\n\nERROR: {e}')
        break

sock.close()