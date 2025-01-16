
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
