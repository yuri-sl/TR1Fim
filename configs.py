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
    "deteccao_erro": None,  # Tipo de detecção de erro (paridade, CRC, Hamming etc.)
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
        binWord = convertToString(binWord)

        crc_class = CRC_32(binWord)
        crc_class = crc_class.calcula_crc()
        crc_class = convertToByte(crc_class)
        print("crc_class em bytes ficou como: ",crc_class)
        return crc_class
    if config["deteccao_erro"] =='Hamming':
        binWord = encode_hamming(binWord)
        return binWord
    
def demod_detect(binword):
    if config["deteccao_erro"]=='paridade':
        binword = removeLSBit(binword)
        return binword
    if config["deteccao_erro"]=='CRC':
        print("This is CRC: ",binword)
        return binword
    if config["deteccao_erro"] == "Hamming":
        return demodularHamming(binword)

def demod_enq(binword):
    if config["enquadramento"]=='charCount':
        if not config["modulacao"]=="Manchester":
            binword = removeIntegersToChar(binword)
            print("Esta é a binword da demod. enq",binword)
            if not binword == None:
                return binword
            
    if config["enquadramento"]=='insByte':
        #binword =
        return binword