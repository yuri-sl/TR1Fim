import socket
import threading

def start_server():
    bind_ip = 'localhost' #IP q o servidor tá rodando
    bind_port = 8030        #Conexao está sendo estabelecida pela porta 80. 
    # se o apache server estiver rodanddo é só trocar a porta que está configurada aqui

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #socket.AF_INET -> Estamos trabalhando com o IPV6
    #SOCK_STREAM -> Trabalhando com protocolo ICP, rodar com o SOCK_DEGRAM caso queira rodar com outro protocolo

    server.bind((bind_ip,bind_port))
    server.listen(5) #Escutar 5 conexões simultaneas

    print('[*] Escutando %s:%d' %(bind_ip,bind_port))

    def handle_client(client_socket):
        request = client_socket.recv(1024)
        print('[*] Recebido: %s' %request)
        print('\n-----------\n')
        message_to_client = '\nMensagem destinada ao cliente: %s\n' %addr[0]
        client_socket.send(message_to_client.encode('utf-8'))
        ACKMessage = '\n ACK! \nRecebido pelo servidor!\n'
        client_socket.send(ACKMessage.encode('utf-8'))
        client_socket.close()

    while(True):
        (client,addr) = server.accept() #Quando a conexão for aceita, ele vai passar essa tupla
        print ('[*] conexão aceita de: %s%d' %(addr[0],addr[1]))
        client_handler = threading.Thread(target=handle_client,args=(client,))
        client_handler.start()
start_server()

