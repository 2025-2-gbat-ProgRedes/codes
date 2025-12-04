import socket, time, os

SERVIDOR = ''
PORTA = 60000

MEU_ENDERECO = (SERVIDOR, PORTA)
CODIFICACAO = 'utf-8'
ENDIANESS = 'big'
TAM_BUFFER = 1460

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(MEU_ENDERECO)
sock.listen(5)

print (f"Esperando pedidos de arquivos em {MEU_ENDERECO}.... ")
while True:
    sock_con, origem = sock.accept()    
    tam_nome = sock_con.recv(1)
    tam_nome = int.from_bytes(tam_nome, ENDIANESS)
    nome_arquivo = sock_con.recv(tam_nome)
    print (f"Recebido pedido para {nome_arquivo} de {origem}.")
    
    if os.path.exists(nome_arquivo):
        sock_con.send(b'\x01')
        tam_arquivo = os.path.getsize(nome_arquivo)
        sock_con.send(tam_arquivo.to_bytes(4, ENDIANESS))
        
        fd = open (nome_arquivo, 'rb')
        while tam_arquivo > 0:
            dados = fd.read(TAM_BUFFER)
            sock_con.send(dados)
            tam_arquivo -= len(dados)
        fd.close()
    else:
        sock_con.send(b'\x00')
    sock_con.close()


sock.close()