from camadaFisica import converterBinario
from camadaFisica import ErroMeioFisico
from convertions import *
#from notebook import ocorreuErro,erroEnquad,erroTransmit
#from configs import *
def calculate_parity(bits, positions):
    """
    Calcula o bit de paridade para os índices fornecidos.
    """
    parity = 0
    for pos in positions:
        if pos - 1 < len(bits):             #Em cada posiçao do encoded
            parity ^= bits[pos - 1]         # XOR nos bits especificados
    return parity


def encode_hamming_12_8(data_bits):
    """
    Codifica os dados usando o código de Hamming (12,8).
    """
    data_size = len(data_bits)

    # Calcula as posições dos bits de paridade (1, 2, 4, 8)
    encoded = [0] * data_size  # Total de 13 bits (dados + paridade)

    # Insere os bits de dados nas posições não-paridade
    j = 0
    for i in range(1, len(encoded) + 1):            #Pelos 12 bits de dados
        if i & (i - 1) != 0:  # Verifica se i não é potência de 2 = ! math.log2(i).is_integer()
            encoded[i - 1] = int(data_bits[j]) # Se não é, é por que é bit de dado e coloca no devido lugar
            j += 1                             #Vai pro proximo

    # Calcula os bits de paridade
    for i in range(len(encoded)):
        if (i + 1) & i == 0:  # É uma potência de 2
            positions = [] 
            for j in range(len(encoded)): 
                position = j + 1            
                if position & (i + 1) != 0:      #Verifica se esse bit faz parte da contagem de paridade
                    positions.append(position)   #Apenas as posiçoes que conta para esse bit 
            encoded[i] = calculate_parity(encoded, positions)   #coloca na posiçao original o bit de paridade
    return encoded

def decode_hamming_12_8(encoded):
    """
    Decodifica a mensagem e corrige um único erro, se houver.
    """
    print("this is a encoded:",encoded)
    encoded = [int(bit) for sublist in encoded for bit in sublist]

    n = len(encoded)
    print("Received encoded is: ",encoded)
    encoded = [int(bit) for bit in encoded]

    # Calcula a posição do erro (se houver)
    error_position = 0
    for i in range(n):
        if (i + 1) & i == 0:  # Potência de 2
            positions = [j + 1 for j in range(n) if (j + 1) & (i + 1) != 0]
            parity = calculate_parity(encoded, positions)
            if parity != 0:
                error_position += i + 1

    # Corrige o erro, se necessário
    if error_position > 0:
        encoded[error_position - 1] ^= 1  # Inverte o bit errado

    # Retorna os dados decodificados (sem os bits de paridade)
    data_bits = []
    for i in range(n):
        if (i + 1) & i != 0:  # Não é potência de 2
            data_bits.append(encoded[i])

    return data_bits, error_position

def hamming(data): #["01010101"] -> "000110100101"
    data = convertToByte(data)
    encoded = encode_hamming_12_8(data)
    return encoded

def dec_hamming_correct(data): #"000110100101" → "01010101"
    decoded, error_position = decode_hamming_12_8(data)
    return ''.join(map(str, decoded))

def dec_hamming_position(data): #"000110100101" se tiver erro retorna a posiçao senao 0
    decoded, error_position = decode_hamming_12_8(data)
    return error_position
def encode_hamming(data_bits_list):
    """
    Codifica uma lista de listas de inteiros no formato de um código de Hamming.

    :param data_bits_list: Lista de listas contendo bits de carga útil
    :return: Lista de listas codificadas com os bits de Hamming
    """
    hamming_encoded = []

    for data_bits in data_bits_list:
        n = len(data_bits)
        r = 0

        # Calcular o número de bits redundantes (r)
        while (2 ** r) < (n + r + 1):
            r += 1

        # Criar o array de Hamming com posições para os bits redundantes
        hamming_code = [-1] * (n + r)  # -1 indica posições a serem preenchidas

        # Colocar os bits de carga útil
        j = 0
        for i in range(1, len(hamming_code) + 1):
            # Verificar se a posição é uma potência de 2 (reservada para bits redundantes)
            if (i & (i - 1)) == 0:  # Posições de potência de 2
                continue
            hamming_code[i - 1] = data_bits[j]
            j += 1

        # Calcular os valores dos bits redundantes
        for i in range(r):
            parity_pos = 2 ** i
            parity_value = 0

            # Checar os bits que influenciam no bit de paridade atual
            for j in range(1, len(hamming_code) + 1):
                if j & parity_pos and hamming_code[j - 1] != -1:
                    parity_value ^= hamming_code[j - 1]

            # Atribuir o valor calculado ao bit redundante
            hamming_code[parity_pos - 1] = parity_value

        hamming_encoded.append(hamming_code)

    return hamming_encoded
def verify_hamming(hamming_codes):
    """
    Verifica a correção de uma lista de códigos de Hamming.
    
    :param hamming_codes: Lista de listas representando os códigos de Hamming
    :return: Lista com o status de cada código de Hamming:
             - "OK" se o código estiver correto
             - Posição do bit incorreto caso haja erro
    """
    verification_results = []

    for hamming_code in hamming_codes:
        n = len(hamming_code)
        error_position = 0

        # Verificar cada bit de paridade
        r = 0
        while (2 ** r) <= n:
            parity_pos = 2 ** r
            parity_value = 0

            # Calcular o valor do bit de paridade atual
            for i in range(1, n + 1):
                if i & parity_pos:  # Verifica se a posição influencia este bit de paridade
                    parity_value ^= hamming_code[i - 1]

            # Se houver discrepância, marcar a posição do erro
            if parity_value != 0:
                error_position += parity_pos

            r += 1
        print(error_position)
        if error_position == 0:
            verification_results.append("OK")  # Sem erro
        else:
            verification_results.append(f"Erro no bit {error_position}")  # Indicar posição do erro

    return verification_results
class CRC_32:
    def __init__(self, data):
        self.aux = ""
        for i in data:
            self.aux += i
        self.data = self.aux
        self.crc = None
        self.generator = "100110000010001110110110111" # exemplo "1011"    
    def data_crc(self):    # Obter os bits de dados + o CRC
        self.crc = self.calcula_crc()
        return self.data + self.crc
    
    def calcula_crc(self):              #Apenas o CRC
        """
        Calcula o CRC usando divisão binária baseada em XOR.

        Args:
            data (str): String de bits representando a mensagem original.
            generator (str): String de bits representando o polinômio gerador.

        Returns:
            str: O resto (CRC) como uma string de bits.
        """
        # Adicionar zeros (padding) ao final da mensagem
        grau = len(self.generator) - 1  # Grau do polinômio gerador
        data_padded = self.data + '0' * grau

        # Converter os dados e o gerador em listas de bits para manipulação
        data_bits = list(data_padded)
        generator_bits = list(self.generator)

        # Realizar a divisão binária
        for i in range(len(self.data)):
            # Se o bit atual for 1, faça XOR com o gerador
            if data_bits[i] == '1':
                for j in range(len(generator_bits)):
                    data_bits[i + j] = str(int(data_bits[i + j]) ^ int(generator_bits[j]))

        # O que sobra nos últimos bits é o CRC
        crc = ''.join(data_bits[-grau:])
        return crc

    def verifica_crc(self):
        """Verifica o CRC, retornando True se for válido."""
        data_crc_bits = list(self.data)  # Converte os dados com CRC para lista de bits
        generator_bits = list(self.generator)  # Polinômio gerador como lista de bits

        # Realiza a divisão binária para verificar o CRC
        for i in range(len(data_crc_bits)):
            # Se o bit atual for 1, faça XOR com o gerador
            if data_crc_bits[i] == '1':
                for j in range(len(generator_bits)):
                    try:
                        data_crc_bits[i + j] = str(int(data_crc_bits[i + j]) ^ int(generator_bits[j]))
                    except:
                        return False
        # O que sobra nos últimos bits é o CRC
        crc = ''.join(data_crc_bits[-1:])
        if ( crc == "0" ):
            return True
        else:
            return False
    def remove_crc(self):
        return self.data[:-32]
"""
Como usar crc32
junte todas as strings e retorne uma str só e passe dessa maneira ↓

if __name__ == "__main__":
    data = "110110111"
    crc32 = CRC_32(data)
    data = crc32.data_crc()
    print(data)

    data = "11011011100010011110011000100100011"
    crc32 = CRC_32(data)
    resultado = crc32.verifica_crc()
    if resultado:
        print("ta certo") #Se rodar esse teste vai dar certo
    else:
        print ( "Ta errado" ) # se colocar qq outro numero vai dar errado
"""

class BitDeParidade:
    def __init__(self,lista = None):
        self.aux = 0
        if lista is None:
            self.lista = []
        else:
            for item in lista:
                if len(item) == 8:
                    continue
                else:
                    print("Existe algum caractere que não é de 8 bits")
            self.lista = lista
            self.encoded_lista = []
    
    def bit_de_paridade(self):              # Par ["01010101"] ->["010101010"]
        self.encoded_lista= []
        for item in self.lista:             # Por cada caractere
            self.aux = 0                    # Sempre reinicia o contador
            for i in item:                  # Em cada bit do caractere
                if i == 0:                # Se é 0 ou 1
                    self.aux += 0
                else:
                    self.aux += 1
            if (self.aux % 2) == 0:         # verifica se é par ou impar
                self.novo_item = item + [0] # se é par apenas 0
            else:
                self.novo_item = item + [1] # Se nao é 1 no final
            self.encoded_lista.append(self.novo_item)
        return self.encoded_lista           # Retorna a lista toda codificada

    def decode_bit_de_paridade(self, lista = None):
        """
        Decodifica uma lista de bits com paridade, removendo o bit de paridade se for válido.
        """
        if lista != None:                               # Se não passar argumento vai considerar a lista ja existente
            self.encoded_lista = lista
        elif not self.encoded_lista:
            print("Não há nenhuma informaçao previa!")  #Não é pra cair aqui, se caiu é pq tem coisa errada
            return []                                   # Retorna nada
        self.decoded_lista = []
        for item in self.encoded_lista:
            aux = 0                                      # Contador de bits '1'
            for j in range(len(item)):                   # Conta quantos bits
                bit = int(item[j])
                aux += bit
            bit_paridade = int(item[-1])                 # O último bit é o de paridade
            if (aux % 2) == bit_paridade:                # Verifica se o calculado é igual o esperado
                self.decoded_lista.append(item[:-1])
            else:
                print(f"\nAlgum bit está incorreto! no item : {item}\n")  # Paridade inválida encontrada
        return self.decoded_lista
    def remover_bit_de_paridade(self, lista):
        lista = convertToByteDetect(lista)
        lista = removeLSBit(lista)
        return lista
        


class ContagemDeCaracteres:
    def __init__(self, lista = None):
        if lista is None:
            self.lista = []
        else:
            self.lista = lista #["01011010","01011010","01011010"] -> (3 em ascii é decw51 ou 0x33) ->["00110011","01011010","01011010","01011010"]

    def contar_caracteres(self):
        tamanho = len(self.lista)
        bin_tamanho = converterBinario(str(tamanho))
        self.lista.insert(0,bin_tamanho[0])
        return self.lista

    def desenquadrar_caracteres(self,data): #["00110011","01011010","01011010","01011010"] -> ["01011010","01011010","01011010"]
        return data[1:]

class InsercaoDeBytes:
    def __init__(self, lista = None):
        self.comeco = 0x01                  #byte 01 para iniciar a transmissao
        self.inicioTx = 0x02                #byte 02 para iniciar o texto
        self.fimTX = 0x03                   #byte 03 para terminar o texto
        self.fim = 0x04                     #byte 04 para terminar a transmissao
        if lista is None:
            self.lista = []
        else:
            self.lista = lista
#["01011010","01011010","01011010"] ->["00000001","01011010","01011010","01011010","00000100"]
    def byte_to_bits(self, byte):
        # Converte o byte para uma lista de bits
        return list(map(int,bin(byte)[2:].zfill(8)))
    def inserir_bytes(self):
        self.lista.insert(0, self.byte_to_bits(self.comeco))
        self.lista.append(self.byte_to_bits(self.fim)) 
        return self.lista
    def tirar_bytes_flags(self,data):
        return data[1:len(data)-1]

"""
def criar_quadro_binario(dados_binarios):

    Cria um quadro com contagem de caracteres para dados binários.
    
    Prefixa os dados com o tamanho em 2 bytes (unsigned short, 16 bits).
    tamanho = len(dados_binarios)
    tamanho_binario = tamanho.to_bytes(2, byteorder='big')  # 2 bytes para o tamanho
    return tamanho_binario + dados_binarios


def extrair_quadro_binario(quadro_binario):

    Extrai o dado do quadro binário utilizando a contagem de caracteres.

    tamanho = int.from_bytes(quadro_binario[:2], byteorder='big')  # Lê os 2 primeiros bytes
    dados_binarios = quadro_binario[2:2 + tamanho]  # Extrai os dados com base no tamanho
    return dados_binarios


# Teste
mensagem = b"Hello, Layer 2 in binary!"  # Dados em binário
quadro = criar_quadro_binario(mensagem)
print(f"Quadro criado (hex): {quadro.hex()}")

dados_recebidos = extrair_quadro_binario(quadro)
print(f"Dados recebidos (binário): {dados_recebidos}")
print(f"Dados recebidos (texto): {dados_recebidos.decode('utf-8')}")
"""