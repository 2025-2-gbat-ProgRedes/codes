import socket, time, os

SERVIDOR = ''
PORTA = 60000

MEU_ENDERECO = (SERVIDOR, PORTA)
CODIFICACAO = 'utf-8'
ENDIANESS = 'big'

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(MEU_ENDERECO)

print ("Esperando pedidos de arquivos .... ")
while True:
    tam_nome, origem = sock.recvfrom(1)
    tam_nome = int.from_bytes(tam_nome, ENDIANESS)
    nome_arquivo, origem = sock.recvfrom(tam_nome)
    print (f"Recebido pedido para {nome_arquivo} de {origem}")
    
    if os.path.exists(nome_arquivo):
        sock.sendto(b'\x01', origem)
        tam_arquivo = os.path.getsize(nome_arquivo)
        sock.sendto(tam_arquivo.to_bytes(4, ENDIANESS), origem)
        
        fd = open (nome_arquivo, 'rb')
        while tam_arquivo > 0:
            dados = fd.read(4096)
            sock.sendto(dados, origem)
            tam_arquivo -= len(dados)
        fd.close()
    else:
        sock.sendto(b'\x00', origem)


sock.close()