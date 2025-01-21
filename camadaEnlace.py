from camadaFisica import converterBinario
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

def decode_hamming_12_8(encoded):
    """
    Decodifica a mensagem e corrige um único erro, se houver.
    """
    if len(encoded) != 12:
        raise ValueError("São necessários exatamente 12 bits codificados.")

    n = len(encoded)
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
    encoded = encode_hamming_12_8(data)
    return ''.join(map(str, encoded))

def dec_hamming_correct(data): #"000110100101" → "01010101"
    decoded, error_position = decode_hamming_12_8(data)
    return ''.join(map(str, decoded))

def dec_hamming_position(data): #"000110100101" se tiver erro retorna a posiçao senao 0
    decoded, error_position = decode_hamming_12_8(data)
    return error_position

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
                if i == "0":                # Se é 0 ou 1
                    self.aux += 0
                else:
                    self.aux += 1
            if (self.aux % 2) == 0:         # verifica se é par ou impar
                self.novo_item = item + "0" # se é par apenas 0
            else:
                self.novo_item = item + "1" # Se nao é 1 no final
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
            for j in range(len(item) - 1):               # Conta quantos bits
                bit = int(item[j])
                aux += bit
            bit_paridade = int(item[-1])                 # O último bit é o de paridade
            if (aux % 2) == bit_paridade:                # Verifica se o calculado é igual o esperado
                self.decoded_lista.append(item[:-1])
            else:
                print(f"\nAlgum bit está incorreto! no item : {item}\n")  # Paridade inválida encontrada
        return self.decoded_lista

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
    def inserir_bytes(self):
        tamanho = len(self.lista)
        self.lista.insert(0, format(self.comeco, '08b'))
        self.lista.append(format(self.fim, '08b')) 
        return self.lista

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
