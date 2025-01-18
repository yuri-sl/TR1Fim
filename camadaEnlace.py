from camadaFisica import converterBinario

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
