from camadaEnlace import *  # Importa funções ou classes da camada de enlace
from camadaFisica import convert_Manchester  # Importa a função de conversão Manchester da camada física

# Variáveis de controle de estado
servidorAtivo = False  # Define se o servidor está ativo ou não
entryBoxPreenchida = False  # Define se a caixa de entrada foi preenchida
errorOcurred = False  # Define se ocorreu um erro
ocorreuErro = False  # Define se um erro ocorreu (dupla definição com errorOcurred)
erroEnquad = False  # Define se há erro de enquadramento
erroTransmit = False  # Define se há erro de transmissão
size = []  # Lista para armazenar o tamanho de dados ou informações

# Configurações do sistema
config = {
    "texto": None,          # Texto que o usuário quer transmitir
    "modulacao": None,      # Tipo de modulação (NRZ, Manchester, Bipolar, etc.)
    "deteccao_erro": None,  # Tipo de detecção de erro (paridade, CRC, etc.)
    "enquadramento": None   # Tipo de enquadramento (se aplicável)
}

def config_modulacao(binWord):
    if config["modulacao"] == "Manchester":
        return convert_Manchester(binWord)  # Converte para modulação Manchester
    else:
        return binWord  # Retorna a palavra binária sem modulação

def config_enquadramento(binWord):
    if config["enquadramento"] == 'charCount':
        charCount = ContagemDeCaracteres(binWord)  # Cria instância de contagem de caracteres
        charCount = charCount.contar_caracteres()  # Conta os caracteres da palavra binária
        return charCount  # Retorna a palavra binária com contagem de caracteres
    if config["enquadramento"] == 'insByte':
        insByte = InsercaoDeBytes(binWord)  # Cria instância de inserção de bytes
        insByte = insByte.inserir_bytes()  # Insere bytes na palavra binária
        return insByte  # Retorna a palavra binária com inserção de bytes

def config_deteccao(binWord):
    if config["deteccao_erro"] == 'paridade':
        parity = BitDeParidade(binWord)  # Cria instância de verificação de paridade
        parity = parity.bit_de_paridade()  # Calcula o bit de paridade
        return parity  # Retorna a palavra binária com bit de paridade
    if config["deteccao_erro"] == 'CRC':
        print("A binword está como: ", binWord)  # Exibe a palavra binária antes da conversão
        binWord = convertToString(binWord)  # Converte a palavra binária para string

        crc_class = CRC_32(binWord)  # Cria instância de cálculo de CRC-32
        crc_class = crc_class.calcula_crc()  # Calcula o CRC da palavra
        crc_class = convertToByte(crc_class)  # Converte o CRC calculado para bytes
        print("crc_class em bytes ficou como: ", crc_class)  # Exibe o CRC em bytes
        return crc_class  # Retorna a palavra binária com CRC

def demod_detect(binword):
    """
    Aplica a demodulação e verificação de erro configurada na palavra binária.

    :param binword: Palavra binária a ser demodulada e verificada
    :return: Palavra binária após a demodulação e remoção de erro
    """
    if config["deteccao_erro"] == 'paridade':
        binword = removeLSBit(binword)  # Remove o bit menos significativo se for paridade
        return binword  # Retorna a palavra binária após remoção do bit de paridade
    if config["deteccao_erro"] == 'CRC':
        print("This is CRC: ", binword)  # Exibe a palavra binária com CRC
        return binword  # Retorna a palavra binária com CRC (sem alteração)

def demod_enq(binword):
    """
    Aplica a demodulação de enquadramento configurada na palavra binária.

    :param binword: Palavra binária a ser desencaixada
    :return: Palavra binária após o enquadramento ser removido
    """
    if config["enquadramento"] == 'charCount':
        if not config["modulacao"] == "Manchester":  # Verifica se a modulação não é Manchester
            binword = removeIntegersToChar(binword)  # Remove inteiros de caracteres, se necessário
            print("Esta é a binword da demod. enq", binword)  # Exibe a palavra binária após a remoção
            if not binword == None:  # Verifica se a palavra não está vazia
                return binword  # Retorna a palavra binária desencaixada

    if config["enquadramento"] == 'insByte':
        # A lógica para desencaixar bytes ainda não está implementada
        return binword  # Retorna a palavra binária sem alteração