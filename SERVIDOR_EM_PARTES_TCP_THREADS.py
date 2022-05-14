# Protocolo
#   Cliente -> Server 
#       4 bytes        - Tamanho do nome do arquivo
#       nome_arquivo   - Os bytes com o nome do arquivo
#
#   Server  -> Cliente
#       4 bytes        - Tamanho do arquivo
#       nome_arquivo   - Os bytes do arquivo

import socket, struct, threading, time

SERVER = '127.0.0.1'
PORT = 5555
protol_tam = 4096

def serveFile(conn):
    lenFileName = struct.unpack('I', conn.recv(4))[0]
    fileName = conn.recv(lenFileName).decode('utf-8')
    fd = open(fileName, "rb")
    lenFile = fd.read()
    st1 = struct.pack("I", len(lenFile))
    conn.send(st1)
    # Substituir comando abaixo por envio em blocos de 4096
    # separar cada envio com 0.1s (sleep)
    #conn.sendall(fd.read())
    #fd.close()
    pos = 0
    while len(lenFile) > pos:
        env = conn.send(lenFile[pos:pos+protol_tam])
        pos += int(env)
        time.sleep(0.1)
    conn.close()
    #sock.close()

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((SERVER, PORT))
    sock.listen(1)

    while True:
        print('Aguardando conexão e pedido de cliente...')
        conn, addr = sock.accept()
        print(f'Conexão e pedido de: {addr}')
        t = threading.Thread(target=serveFile, args=(conn,))
        t.start()

main()
