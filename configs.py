servidorAtivo = False
entryBoxPreenchida = False
errorOcurred = False

ocorreuErro = False
erroEnquad = False
erroTransmit = False

config = {
    "texto": None,          # Texto que o usuário quer transmitir
    "modulacao": None,      # Tipo de modulação (NRZ, Manchester, Bipolar, etc.)
    "deteccao_erro": None,  # Tipo de detecção de erro (paridade, CRC, etc.)
    "enquadramento": None   # Tipo de enquadramento (se aplicável)
}