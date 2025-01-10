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
