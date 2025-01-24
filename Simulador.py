import socket
import threading
import time

server_running = True  # Controle global de iniciar/fechar o servidor
received = 'ola'
lock = threading.Lock()
saved_message = []

def start_server():
    global server_running 
    server_running = True

    bind_ip = 'localhost'  # IP que o servidor está escutando
    bind_port = 8030       # Porta do servidor

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((bind_ip, bind_port))
    server.listen(5)  # Escutando até 5 conexões simultâneas
    server.settimeout(1.0)  # Timeout para evitar bloqueios ao encerrar

    print(f'[*] Servidor escutando em {bind_ip}:{bind_port}')

    def handle_client(client_socket, addr):
        global received
        print("Entrou em handle client")
        try:
            request = client_socket.recv(1024)
            print("request recebido (em bytes): ",request)
            #print(f'[*] Mensagem recebida de {addr[0]}: {request.decode("utf-8")}')
            #response = f'\nMensagem destinada ao cliente: {addr[0]}\n'
            #client_socket.send(response.encode('utf-8'))
            binary_list = [bin(byte)[2:].zfill(8)for byte in request]
            print("A lista binária recebida é:",binary_list)

            bit_list = [list(map(int,bin(byte)[2:].zfill(8)))for byte in request]
            print("A lista de inteiros binários é:",bit_list)

            #ack_message = '\nACK!\nRecebido pelo servidor!\n'
            #client_socket.send(ack_message.encode('utf-8'))
            with lock:
                received = bit_list
            print("O received original é: ",received)
            print("A mensagem received é: ",received)
            saved_message.append(received)
            print("Mensagem salva em variável fica como: ",saved_message)
        except Exception as e:
            print(f"Erro ao processar cliente {addr}: {e}")
        finally:
            client_socket.close()

    while server_running:
        try:
            client, addr = server.accept()  # Aceitar conexão
            print(f'[*] Conexão aceita de: {addr[0]}:{addr[1]}')
            client_handler = threading.Thread(target=handle_client, args=(client, addr))
            client_handler.start()
        except socket.timeout:
            continue  # Timeout permite verificar o estado do servidor e continuar

    #server.close()
    #print('[*] Servidor encerrado.')

def stop_server():
    global server_running
    server_running = False
    print('[*] Encerrando o servidor...')
