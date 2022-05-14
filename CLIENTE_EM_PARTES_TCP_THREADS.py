# Protocolo
#   Cliente -> Server 
#       4 bytes        - Tamanho do nome do arquivo
#       nome_arquivo   - Os bytes com o nome do arquivo
#
#   Server  -> Cliente
#       4 bytes        - Tamanho do arquivo
#       nome_arquivo   - Os bytes do arquivo

import socket, struct, threading

SERVER = '127.0.0.1'
PORT = 5555

baixados = []
baixando = []

def getFile(fileName):
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER, PORT))
    fileNameB = fileName.encode('utf-8')
    st1 = struct.pack('I', len(fileNameB))
    sock.send(st1)
    sock.send(fileNameB)
    toRead = struct.unpack('I', sock.recv(4))[0]
    if toRead > 0:
        fd = open(fileNameB, 'wb')
        baixando.append(fileNameB.decode('utf-8'))
        while toRead > 0:
            buf = sock.recv(4096)
            toRead -= len(buf)
            fd.write(buf)
        baixados.append(fileNameB.decode('utf-8'))
        fd.close()
    else:
        return print('Tamanho do arquivo é de 0 bytes, portanto não será recebido !')

def main():
    while True:
        print('-'*70)
        fileName = input('Digite:\n? - Para arquivos baixando/baixados\n?? - Para arquivos totalmente baixados\n'
                         '! - Para encerrar\n"Nome de arquivo" - Para baixar:\n')
        if fileName == '?':
            print(baixando)
        elif fileName == '??':
            print(baixados)
        elif fileName == '!':
            sock.close()
            return print('\nEncerrado !')
        else:
            t = threading.Thread(target=getFile, args=(fileName,))
            t.start()
main()
