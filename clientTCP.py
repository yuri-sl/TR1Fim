import socket
target_host = 'localhost' #Alvo é localHost pois queremos enviar o localHost
target_port = 80	  #Porta que vamos passar

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((target_host,target_port))
message = 'Eu sou o cliente, estou me conectando ao servidor!'
client.send(message.encode('utf-8'))
#Enviando essa mensagem para o servidor

response = client.recv(4096)
#Resposta do servidor
print(response)

