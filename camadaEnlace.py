# Importa a função converterBinario da camadaFisica
from camadaFisica import converterBinario

# Importa a classe ErroMeioFisico da camadaFisica
from camadaFisica import ErroMeioFisico

# Importa todas as funções ou variáveis de convertions (aqui está o * porque não é especificado o que é importado)
from convertions import *

# Importa funções ou variáveis da camada notebook (comentadas)
#from notebook import ocorreuErro, erroEnquad, erroTransmit

# Importa configurações de configs (comentado)
#from configs import *


# Função que codifica uma lista de listas de inteiros no formato de um código de Hamming
def encode_hamming(data_bits_list):
    """
    Codifica uma lista de listas de inteiros no formato de um código de Hamming.

    :param data_bits_list: Lista de listas contendo bits de carga útil
    :return: Lista de listas codificadas com os bits de Hamming
    """
    # Lista que irá armazenar os códigos Hamming codificados
    hamming_encoded = []

    # Itera sobre cada lista de bits de dados
    for data_bits in data_bits_list:
        # Obtém o tamanho da lista de dados
        n = len(data_bits)
        # Inicializa o contador de bits redundantes (r)
        r = 0

        # Calcula o número de bits redundantes (r) necessários para o código de Hamming
        while (2 ** r) < (n + r + 1):
            r += 1

        # Cria um array para armazenar o código Hamming com espaço para os bits redundantes
        # O valor -1 indica que a posição ainda não foi preenchida
        hamming_code = [-1] * (n + r)

        # Preenche as posições não redundantes com os bits de dados
        j = 0
        for i in range(1, len(hamming_code) + 1):
            # Verifica se a posição é uma potência de 2 (reservada para bits de paridade)
            if (i & (i - 1)) == 0:  # Posições de potência de 2
                continue
            # Coloca o bit de dado na posição apropriada
            hamming_code[i - 1] = data_bits[j]
            j += 1

        # Calcula os bits de paridade (redundantes) e os coloca nas posições corretas
        for i in range(r):
            # Calcula a posição do bit de paridade (potência de 2)
            parity_pos = 2 ** i
            # Inicializa o valor do bit de paridade
            parity_value = 0

            # Checa quais bits influenciam no cálculo do bit de paridade
            for j in range(1, len(hamming_code) + 1):
                # Se a posição do bit atual influencia no cálculo do bit de paridade
                if j & parity_pos and hamming_code[j - 1] != -1:
                    # Aplica a operação XOR nos bits que afetam a paridade
                    parity_value ^= hamming_code[j - 1]

            # Atribui o valor calculado ao bit de paridade na posição correta
            hamming_code[parity_pos - 1] = parity_value

        # Adiciona o código Hamming codificado à lista final
        hamming_encoded.append(hamming_code)

    # Retorna a lista com todos os códigos Hamming codificados
    return hamming_encoded
# Função que verifica a correção de uma lista de códigos de Hamming.
# Retorna o status de cada código de Hamming ("OK" se correto, ou a posição do erro).
def verify_hamming(hamming_codes):
    """
    Verifica a correção de uma lista de códigos de Hamming.
    
    :param hamming_codes: Lista de listas representando os códigos de Hamming
    :return: Lista com o status de cada código de Hamming:
             - "OK" se o código estiver correto
             - Posição do bit incorreto caso haja erro
    """
    # Lista para armazenar os resultados da verificação
    verification_results = []
    erro = False

    # Itera sobre cada código de Hamming na lista
    for hamming_code in hamming_codes:
        # Obtém o tamanho do código
        n = len(hamming_code)
        # Inicializa a variável para armazenar a posição do erro
        error_position = 0

        # Verifica cada bit de paridade no código de Hamming
        r = 0
        while (2 ** r) <= n:
            # Posição do bit de paridade (potência de 2)
            parity_pos = 2 ** r
            # Inicializa o valor do bit de paridade
            parity_value = 0

            # Calcula o valor do bit de paridade atual
            for i in range(1, n + 1):
                # Verifica se a posição atual influencia no cálculo do bit de paridade
                if i & parity_pos:
                    # Aplica a operação XOR nos bits relevantes para este bit de paridade
                    parity_value ^= hamming_code[i - 1]

            # Se houver discrepância, marca a posição do erro
            if parity_value != 0:
                error_position += parity_pos

            r += 1

        # Exibe a posição do erro (se houver)
        print(error_position)

        # Verifica se houve erro
        if error_position == 0:
            # Se não houver erro, marca como "OK"
            verification_results.append("OK")
        else:
            # Caso contrário, adiciona a posição do erro
            erro = True
            verification_results.append(f"Erro no bit {error_position}")

    # Retorna a lista de resultados de verificação
    return erro #verification_results
class CRC_32:
    def __init__(self, data):
        """
        Inicializa a classe com dados para calcular o CRC.

        :param data: A string de dados (bits) para aplicar o CRC
        """
        self.aux = ""
        for i in data:
            self.aux += str(i)
        self.data = self.aux # Armazena os dados em formato string
        self.crc = None # Inicializa o valor do CRC como None
        self.generator = "1011" # exemplo "1011"    
    def data_crc(self):    # Obter os bits de dados + o CRC
        self.crc = self.calcula_crc()
        return self.data + self.crc
    
    def data_crc(self):
        """
        Obtém os dados com o CRC anexado.

        :return: A string de dados concatenada com o CRC calculado
        """
        self.crc = self.calcula_crc()  # Calcula o CRC
        return self.data + self.crc  # Retorna os dados concatenados com o CRC
    
    def calcula_crc(self):
        """
        Calcula o CRC utilizando divisão binária com XOR.

        :return: O resto da divisão binária, ou seja, o CRC como uma string de bits
        """
        grau = len(self.generator) - 1  # Calcula o grau do polinômio gerador
        data_padded = self.data + '0' * grau  # Adiciona zeros à mensagem original

        # Converte os dados e o gerador para listas de bits
        data_bits = list(data_padded)
        generator_bits = list(self.generator)

        # Realiza a divisão binária
        for i in range(len(self.data)):
            if data_bits[i] == '1':  # Se o bit atual for 1, aplica o XOR com o gerador
                for j in range(len(generator_bits)):
                    data_bits[i + j] = str(int(data_bits[i + j]) ^ int(generator_bits[j]))

        # O resto da divisão é o CRC
        crc = ''.join(data_bits[-grau:])  # Extrai os últimos bits como o CRC
        return crc

    def verifica_crc(self):
        """
        Verifica se o CRC é válido.

        :return: True se o CRC for válido, False caso contrário
        """
        data_crc_bits = list(self.data)  # Converte os dados com CRC para lista de bits
        generator_bits = list(self.generator)  # Polinômio gerador como lista de bits

        # Realiza a divisão binária para verificar o CRC
        for i in range(len(data_crc_bits)-len(generator_bits)+1):
            if data_crc_bits[i] == '1':  # Se o bit atual for 1, aplica o XOR com o gerador
                for j in range(len(generator_bits)):
                    try:
                        data_crc_bits[i + j] = str(int(data_crc_bits[i + j]) ^ int(generator_bits[j]))
                    except:
                        return False  # Se houver erro, o CRC não é válido
        # O que sobra nos últimos bits é o CRC
        for i in range(len(data_crc_bits)):
            data_crc_bits[i] = int(data_crc_bits[i])

        crc = any(data_crc_bits)
        return crc  # Verifica se o CRC é 0 (sem erro)
    
    def remove_crc(self):
        """
        Remove os últimos 32 bits de CRC dos dados.

        :return: A string de dados sem o CRC
        """
        return [int(i) for i in self.data[:-(len(self.generator)-1)]] # Retorna os dados sem os últimos 32 bits (CRC)
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

# Classe que implementa a codificação e decodificação de bits com paridade
class BitDeParidade:
    def __init__(self, lista=None):
        """
        Inicializa a classe, verificando se os itens na lista têm 8 bits.

        :param lista: Lista de listas de bits (por padrão, None, para inicializar uma lista vazia)
        """
        self.aux = 0
        if lista is None:
            self.lista = []
        else:
            for item in lista:
                if len(item) == 8:
                    continue
                else:
                    print("Existe algum caractere que não é de 8 bits")  # Verifica se cada item tem 8 bits
            self.lista = lista  # Atribui a lista de bits fornecida
            self.encoded_lista = []  # Lista para armazenar os dados codificados

    def bit_de_paridade(self):
        """
        Adiciona um bit de paridade a cada caractere na lista de bits.

        Para cada item de 8 bits, calcula a paridade (par ou ímpar) e adiciona um bit de paridade:
        - Paridade par: 0
        - Paridade ímpar: 1

        :return: Lista de bits codificados com bit de paridade
        """
        self.encoded_lista = []  # Limpa a lista de codificação
        for item in self.lista:  # Para cada item na lista de bits
            self.aux = 0  # Reseta o contador de bits '1'
            for i in item:  # Para cada bit do item
                if i == 0:  # Se o bit for 0
                    self.aux += 0
                else:  # Se o bit for 1
                    self.aux += 1
            if (self.aux % 2) == 0:  # Se a quantidade de bits '1' for par
                self.novo_item = item + [0]  # Adiciona 0 como bit de paridade
            else:
                self.novo_item = item + [1]  # Adiciona 1 como bit de paridade
            self.encoded_lista.append(self.novo_item)  # Adiciona o item codificado na lista
        return self.encoded_lista  # Retorna a lista de bits com paridade

    def decode_bit_de_paridade(self, lista=None):
        """
        Decodifica uma lista de bits com paridade, removendo o bit de paridade se ele for válido.
        
        :param lista: Lista de bits a ser decodificada. Se não for fornecida, utiliza a lista codificada atual.
        :return: Lista de bits decodificados ou uma mensagem de erro se a paridade for inválida
        """
        erro = False
        if lista is not None:  # Se a lista for fornecida, usa a lista fornecida
            self.encoded_lista = lista
        elif not self.encoded_lista:  # Se a lista codificada não existir, retorna erro
            print("Não há nenhuma informação prévia!")
            return []  # Retorna uma lista vazia
        self.decoded_lista = []  # Lista para armazenar os dados decodificados
        for item in self.encoded_lista:  # Para cada item na lista codificada
            aux = 0  # Contador de bits '1'
            for j in range(len(item)-1):  # Conta os bits '1'
                bit = int(item[j])
                aux += bit
            bit_paridade = int(item[-1])  # O último bit é o bit de paridade
            self.decoded_lista.append(item[:-1])  # Adiciona o item sem o bit de paridade
            if (aux % 2) != bit_paridade:  # Verifica se a paridade calculada é válida
                print(f"\nAlgum bit está incorreto! no item: {item}\n")  # Informa se a paridade estiver incorreta
                erro = True
        return self.decoded_lista,erro  # Retorna a lista de bits decodificados

# Classe para contar e manipular caracteres em uma lista de strings binárias
class ContagemDeCaracteres:
    def __init__(self, lista=None):
        """
        Inicializa a classe com uma lista de caracteres binários.

        :param lista: Lista de strings binárias (por padrão, None, para inicializar uma lista vazia)
        """
        if lista is None:
            self.lista = []  # Se não for fornecida, inicializa uma lista vazia
        else:
            self.lista = lista  # Atribui a lista fornecida (ex: ["01011010", "01011010", "01011010"])

    def contar_caracteres(self):
        """
        Conta o número de elementos na lista e adiciona o tamanho como o primeiro item da lista.

        O tamanho da lista é convertido para binário e inserido no início da lista.

        :return: Lista de caracteres com o tamanho da lista (em binário) inserido no início.
        """
        tamanho = len(self.lista)  # Obtém o tamanho da lista
        bin_tamanho = converterBinario(str(tamanho))  # Converte o tamanho da lista para binário
        self.lista.insert(0, bin_tamanho[0])  # Insere o tamanho binário como o primeiro item da lista
        return self.lista  # Retorna a lista com o tamanho binário adicionado

# Classe para inserir e remover bytes de controle em uma lista de dados binários
class InsercaoDeBytes:
    def __init__(self, lista=None):
        """
        Inicializa a classe com uma lista de dados binários e define os bytes de controle.

        :param lista: Lista de strings binárias (por padrão, None, para inicializar uma lista vazia)
        """
        # Definindo os bytes de controle para sinalizar diferentes estágios da transmissão
        self.comeco = 0x01   # Byte 01: Iniciar a transmissão
        self.fim = 0x04       # Byte 04: Terminar a transmissão

        # Se não for fornecida uma lista, inicializa uma lista vazia
        if lista is None:
            self.lista = []
        else:
            self.lista = lista  # Atribui a lista fornecida

    def byte_to_bits(self, byte):
        """
        Converte um byte em uma lista de bits.

        :param byte: Um valor numérico (byte) para ser convertido em bits
        :return: Uma lista de 8 bits representando o byte (ex: 0x01 -> [0, 0, 0, 0, 0, 0, 0, 1])
        """
        # Converte o byte para binário e mapeia para uma lista de bits (8 bits)
        return list(map(int, bin(byte)[2:].zfill(8)))

    def inserir_bytes(self):
        """
        Insere bytes de controle no início e no final da lista de dados.

        - Adiciona o byte de início de transmissão (0x01) no início da lista.
        - Adiciona o byte de fim de transmissão (0x04) no final da lista.

        :return: A lista de dados binários com os bytes de controle inseridos.
        """
        # Insere o byte de início no começo e o byte de fim no final
        self.lista.insert(0, self.byte_to_bits(self.comeco))  # Inserir byte de início
        self.lista.append(self.byte_to_bits(self.fim))        # Inserir byte de fim
        return self.lista  # Retorna a lista com os bytes de controle
