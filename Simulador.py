import math
import socket
import threading
import time
from camadaFisica import buildNRZ
from camadaEnlace import *
from convertions import *
from processSignal import length

server_running = True  # Controle global de iniciar/fechar o servidor
received = 'ola'
lock = threading.Lock()

#Variavel global em lista que reserva as mensagens enviadas
saved_message = []

def config_u_dectError(word):
    global config
    if config["deteccao_erro"] == 'paridade':
        word = removeLSBit(word)
        return word
    if config["deteccao_erro"] == 'CRC':
        crc_class = CRC_32(word)
        crc_class = crc_class.verifica_crc()
        return crc_class




def receberSinal():
    #Acessar a variavel global saved_message
    global saved_message
    print("A saved message é: ",saved_message)
    print("Atual o tamanho de mensage é: ",len(saved_message))
    #Pegar a primeira mensagem enviada
    word = saved_message[0]
    print(word)
    word,x_axis = buildNRZ(word)
    return word,x_axis

def demodularSinal(size):
    global saved_message
    print("DEMODULANDO O SINAL!!!!!!")
    word = saved_message[0]
    print("THIS IS THE WORD WE ARE DEMODULATING!!",word)
    word = convertToString(word)
    print("THIS IS THE SIZE: ",size)
    word = convertToByteDetect(word,size)
    added = math.log2(size)
    size - size - added
    word = dec_hamming_correct(word)
    print("A Hamming demodulada fica: ",word)
    word = convertToByteDetect(word,size)
    #word = removeLSBit(word)
    print("Tornando em int list: ",word)
    word = config_u_dectError(word)
    print("A word sem detect erro ficou como: ",word)




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
        global length
        print("Entrou em handle client")
        print("O global length é: ",length)
        try:
            request = client_socket.recv(1024)
            print("request recebido (em bytes): ",request)
            #print(f'[*] Mensagem recebida de {addr[0]}: {request.decode("utf-8")}')
            #response = f'\nMensagem destinada ao cliente: {addr[0]}\n'
            #client_socket.send(response.encode('utf-8'))
            #binary_list = [bin(byte)[2:].zfill(8)for byte in request]
            #print("A lista binária recebida é:",binary_list)
            #length = size[0]

            bit_list = bytes_to_bits(request,13)
            print("A bit_list ficou: ",bit_list)

            #bit_list = [list(map(int,bin(byte)[2:].zfill(8)))for byte in request]
            #print("A lista de inteiros binários é:",bit_list)

            #ack_message = '\nACK!\nRecebido pelo servidor!\n'
            #client_socket.send(ack_message.encode('utf-8'))
            with lock:
                received = bit_list
            print("O received original é: ",received)
            print("A mensagem received é: ",received)
            saved_message.clear()
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
