import socket  # Importa o módulo de sockets para comunicação de rede

def sendMessage(message):
    try:
        print("Entrou em SendMessage")  # Informa que entrou na função sendMessage

        target_host = 'localhost'  # Define o alvo como 'localhost' (máquina local)
        target_port = 8030         # Define a porta de conexão como 8030
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria um socket TCP/IP
        client.connect((target_host, target_port))  # Conecta ao servidor no host e porta definidos

        # Se a mensagem for um bytearray, converte para bytes
        if isinstance(message, bytearray):
            message = bytes(message)

        print(message)  # Exibe a mensagem que será enviada
        print(f"Mensagem enviada: {message}")  # Informa qual mensagem está sendo enviada
        client.send(message)  # Envia a mensagem para o servidor

        response = client.recv(4096)  # Recebe a resposta do servidor (tamanho máximo de 4096 bytes)
        print(f"Resposta do servidor: {response.decode('utf-8')}")  # Exibe a resposta decodificada

        client.close()  # Fecha a conexão com o servidor
    except Exception as e:
        print(f"Erro ao enviar para o servidor: {e}")  # Exibe erro caso ocorra uma exceção