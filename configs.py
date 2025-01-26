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
    "deteccao_erro": None,  # Tipo de detecção de erro (paridade, CRC, Hamming etc.)
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
        insByte = InsercaoDeBytes(binWord)
        insByte = insByte.inserir_bytes()
        return insByte
def config_deteccao(binWord):
    if config["deteccao_erro"] =='paridade':
        parity = BitDeParidade(binWord)  # Cria instância de verificação de paridade
        parity = parity.bit_de_paridade()  # Calcula o bit de paridade
        return parity  # Retorna a palavra binária com bit de paridade
    if config["deteccao_erro"] =='CRC':
        print("A binword está como: ",binWord)
        crc_bit = []
        for bit in binWord:    
            print("O bit que vai sofrer o CRC é: ",bit)
            bit = convertToString(bit)
            crc_class = CRC_32(bit)
            a = crc_class.data_crc()
            b = CRC_32(a)
            resultado = b.remove_crc()
            print("O CRC INSERIDO NA STRING FICOU: ",a)
            a = convertToByteCRCAdapt(a)
            print("crc_class em bytes ficou como: ",a)
            crc_bit.append(a)
        print("No fim, o crc ficou: ",crc_bit)
        return crc_bit

    if config["deteccao_erro"] =='Hamming':
        binWord = encode_hamming(binWord)
        return binWord
def demod_detect(binword):
    if config["deteccao_erro"]=='paridade':
        # binWord = removeLSBit(binWord)
        binWord,erro = BitDeParidade().decode_bit_de_paridade([binWord])
        return binWord[0],erro

    if config["deteccao_erro"]=='CRC':
        # print("This is CRC: ",binWord)
        # crc = CRC_32(binWord)
        # error_ocurred = crc.verifica_crc()
        # return crc.remove_crc(), error_ocurred
        print("This is CRC: ",binword)
        binword = binword[:-3]
        return binword
    if config["deteccao_erro"] == "Hamming":
        error_ocurred = verify_hamming([binWord])
        return demodularHamming(binWord),error_ocurred

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
        else:
            return binword
            
    if config["enquadramento"]=='insByte':
        print("Em desenquadramento, a BinWord está como: ",binword)
        if (binword == [0,0,0,0,0,1,0,0]) or (binword==[0,0,0,0,0,0,0,1]) or (binword==[1,0,0,0,0,0,0,1]):
            return None
        else:
            return binword
def demod_mod(binword):
    if config["modulacao"]=="Manchester":
        print("Você está demodulando um sinal Manchester")
        print("Esta é a sua binword",binword)
