import socket
import threading
import time

server_running = True  # Controle global de iniciar/fechar o servidor

def start_server():
    global server_running

    bind_ip = 'localhost'  # IP que o servidor está escutando
    bind_port = 8030       # Porta do servidor

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((bind_ip, bind_port))
    server.listen(5)  # Escutando até 5 conexões simultâneas
    server.settimeout(1.0)  # Timeout para evitar bloqueios ao encerrar

    print(f'[*] Servidor escutando em {bind_ip}:{bind_port}')

    def handle_client(client_socket, addr):
        print("Entrou em handle client")
        try:
            request = client_socket.recv(1024)
            print(f'[*] Mensagem recebida de {addr[0]}: {request.decode("utf-8")}')
            response = f'\nMensagem destinada ao cliente: {addr[0]}\n'
            client_socket.send(response.encode('utf-8'))
            ack_message = '\nACK!\nRecebido pelo servidor!\n'
            client_socket.send(ack_message.encode('utf-8'))
            return request
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

    server.close()
    print('[*] Servidor encerrado.')

def stop_server():
    global server_running
    server_running = False
    print('[*] Encerrando o servidor...')
