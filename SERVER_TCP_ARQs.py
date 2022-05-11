#import da biblioteca
import socket, struct

#definição das variaveis
print('Iniciando...')
INTERFACE = '127.0.0.1'
PORT = 12345

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Definição do socket com o protocolo TCP
sock.bind((INTERFACE, PORT)) # Estabelecimento da INTERFACE local com o IP e PORTA
sock.listen(1)
print("Escutando em ...", (INTERFACE, PORT))

#criação da função "servidor" que vai esperar que o cliente se conecte
def server():
    print('Aguardando cliente...')
    data, con = sock.accept()
    print(f'Cliente {con} conectado!\n')
    sock.settimeout(None) #inicia a API de tempo da biblioteca

    try: #inicia a estação de tratamento
        while True:
                nameArq = data.recv(512) #recebe do cliente
                with open(nameArq, 'rb') as arq: #abre o arquivo que o cliente chama
                    read = arq.read() #lê o arq
                    print(f'Arquivo pedido: {nameArq.decode()}\n'
                          f'Pedido do Cliente: {con}\nTamanho do arquivo pedido: {len(read)} bytes')
                    s = struct.pack('I', len(read))
                    data.send(s) #envia o tamanho do arquivo para o cliente
                    pos = 0
                    while len(read) > pos:#loop para enviar de forma fragmentada
                        #print(end='.') # Se tirar do comentário e testar com arquivo grande, leva bastante tempo imprimindo os pontos, um vídeo por exemplo
                        env = data.send(read[pos:pos+4096])
                        pos += int(env)
                print('='*70)
    except Exception as e: #cria a exceção do tratamento
        print(f'Ocorreu algum problema na execução do programa com o cliente.'
                f'\nERROR: {e}')
        print('='*70,'\n\n')
        data.close()
        server()
server()
