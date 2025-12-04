# To run: python udp-file-client.py 10.25.2.154 50000

import socket, time, sys

SERVIDOR = 'localhost'
PORTA = 60000

CODIFICACAO = 'utf-8'
ENDIANESS = 'big'
TAM_BUFFER = 1460

def main():
    DESTINO = (SERVIDOR, PORTA)

    while True:
        nome_arq = input('Nome do arquivo a fazer download: ')
        if nome_arq:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(DESTINO)
            # Envia solicitacao do arquivo
            nome_arq = nome_arq.encode(CODIFICACAO)
            tam_nome = len(nome_arq)
            tam_nome = tam_nome.to_bytes(1, ENDIANESS)
            print (f"Enviando {tam_nome} para {DESTINO}")
            sock.send(tam_nome)
            print (f"Enviando {nome_arq} para {DESTINO}")
            sock.send(nome_arq)
            
            # Recebe informação sobre existência
            existe = sock.recv(1)
            print (f"Recebi {existe} como resposta.")
            if existe == b'\x01':
                # Recebe o tamanho do arquivo
                tamanho = sock.recv(4)
                tamanho = int.from_bytes(tamanho, ENDIANESS)

                print (f"Recebi {tamanho} como tamanho do arquivo.")
                   
                fd = open (nome_arq, 'wb')
                while tamanho > 0:
                    dado = sock.recv(TAM_BUFFER)
                    fd.write(dado)
                    tamanho -= len(dado)
                    print (f"Lidos {len(dado)} bytes. "+ 
                           f"Faltam {tamanho} bytes.")
                fd.close()
                
                print ("Arquivo recebido com sucesso!")
            else:
                print ("Arquivo não existe no servidor!")
            sock.close()

if len(sys.argv) >= 3:
    SERVIDOR = sys.argv[1]
    PORTA = int(sys.argv[2])
elif len(sys.argv) >= 2:
    SERVIDOR = sys.argv[1]
else:
    print (f"uso: python {sys.argv[0]} servidor porta")

print (f"Usando {SERVIDOR}:{PORTA}")
main()