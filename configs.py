from camadaEnlace import *
from camadaFisica import convert_Manchester


servidorAtivo = False
entryBoxPreenchida = False
errorOcurred = False

ocorreuErro = False
erroEnquad = False
erroTransmit = False
size = []

config = {
    "texto": None,          # Texto que o usuário quer transmitir
    "modulacao": None,      # Tipo de modulação (NRZ, Manchester, Bipolar, etc.)
    "deteccao_erro": None,  # Tipo de detecção de erro (paridade, CRC, etc.)
    "enquadramento": None   # Tipo de enquadramento (se aplicável)
}
def config_modulacao(binWord):
    if config["modulacao"] == "Manchester":
        return convert_Manchester(binWord)
    else:
        return binWord

def config_enquadramento(binWord):
    if config["enquadramento"] == 'charCount':
        charCount = ContagemDeCaracteres(binWord)
        charCount =  charCount.contar_caracteres()
        return charCount
    if config["enquadramento"] == 'insByte':
        insByte = InsercaoDeBytes(binWord)
        insByte = insByte.inserir_bytes()
        return insByte
def config_deteccao(binWord):
    if config["deteccao_erro"] =='paridade':
        parity = BitDeParidade(binWord)
        parity = parity.bit_de_paridade()
        return parity
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
def demod_detect(binword):
    if config["deteccao_erro"]=='paridade':
        binword = removeLSBit(binword)
        return binword
    if config["deteccao_erro"]=='CRC':
        print("This is CRC: ",binword)
        binword = binword[:-3]

        return binword
def demod_enq(binword):
    if config["enquadramento"]=='charCount':
        if not config["modulacao"]=="Manchester":
            binword = removeIntegersToChar(binword)
            print("Esta é a binword da demod. enq",binword)
            if not binword == None:
                return binword
        else:
            binword = removeIntegersToChar(binword)
            print("Esta é a sua binword em manchester após demodular o enquadramento:",binword)
            if not binword == None:
                print("Você entrou no if que é para não adicionar o None")
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

