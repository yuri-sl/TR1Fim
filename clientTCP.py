import socket

def sendMessage(message):
    print("Entrou em SendMessage")
    try:
        target_host = 'localhost'  # Alvo
        target_port = 8030         # Porta
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((target_host, target_port))
        client.send(message.encode('utf-8'))  # Enviar mensagem
        response = client.recv(4096)         # Receber resposta
        print(f"Resposta do servidor: {response.decode('utf-8')}")
        client.close()
    except Exception as e:
        print(f"Erro ao enviar para o servidor: {e}")
