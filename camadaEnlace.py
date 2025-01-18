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
    if len(data_bits) != 8:
        raise ValueError("São necessários exatamente 8 bits de dados.")

    # Calcula as posições dos bits de paridade (1, 2, 4, 8)
    encoded = [0] * 12  # Total de 12 bits (dados + paridade)

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

class CRC_32:
    def __init__(self, data):
        self.aux = ""
        for i in data:
            self.aux += i
        self.data = self.aux
        self.crc = None
        self.generator = "100000100110000010001110110110111"
        self.calcula_crc()
    def data_crc(self):                 #Os bits de dados + o CRC
        self.crc = self.calcula_crc()
        self.aux = self.data + self.crc
        return self.aux
    def get_crc_lib(self):              #CRC de uma lib. é diferente!
        import zlib
        crc32_valor = zlib.crc32(self.data)
        return f"crc32_valor:#010x"

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


class BitDeParidade:
    def __init__(self,lista = None):
        self.aux = 0
        if lista is None:
            self.lista = []
        else:
            self.lista = lista
            self.nova_lista = []
            self.novo_item = None

    def bit_de_paridade(self):              # Par ["01010101"] ->["010101010"]
        for item in self.lista:             # Por cada caractere
            self.aux = 0                    # Sempre reinicia o contador
            for i in item:                  # Em cada bit do caractera
                i = int(i)
                if i == 0:
                    self.aux += 0
                else:
                    self.aux += 1
            if (self.aux % 2) == 0:              # verifica se é par ou impar
                self.novo_item = item + "0"                  # se é par apenas 0
            else:
                self.novo_item = item + "1"                  # Se nao é 1 no final
            self.nova_lista.append(self.novo_item)
        return self.nova_lista

def criar_quadro_binario(dados_binarios):
    """
    Cria um quadro com contagem de caracteres para dados binários.
    Prefixa os dados com o tamanho em 2 bytes (unsigned short, 16 bits).
    """
    tamanho = len(dados_binarios)
    tamanho_binario = tamanho.to_bytes(2, byteorder='big')  # 2 bytes para o tamanho
    return tamanho_binario + dados_binarios


def extrair_quadro_binario(quadro_binario):
    """
    Extrai o dado do quadro binário utilizando a contagem de caracteres.
    """
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
