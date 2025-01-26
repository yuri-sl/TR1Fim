from camadaEnlace import *
from camadaFisica import *
from configs import *
from tuple import tuple
length = []

def processSignal(sentText):
    ##Rodar algoritmos de configuracao
    binWord = converterBinario(sentText)
    binWord = config_modulacao(binWord)
    print("A binword digital é",binWord)
    if config["modulacao"] == "Manchester":
        flattened = [bit for pair in binWord for bit in pair]

        # Group bits into bytes (blocks of 8 bits)
        binWord = [flattened[i:i + 8] for i in range(0, len(flattened), 8)]

        print("A manchester reajustada ficou: ",binWord)
    binWord = config_enquadramento(binWord)
    print("A binword enquadrada é:",binWord)
    ##Falta aplicarmos a Detecção de erros!!
    # Adiciona a detecção ou correção de erros Paridade, CRC ou Hamming
    binWord = config_deteccao(binWord)
    print("A binword com a detecção ficou: ",binWord)

    print("A binword antes do erro é: ",binWord)
    #Aplica a % do Erro no enquadramento
    print("Erro no enquadramento---")
    erro = ErroMeioFisico(binWord)
    binWord = erro.erro()
    print("Binword após erro em enq: ",binWord)
    #Hamming para corrigir o erro
    verify_hamming(binWord)
    if errorOcurred == True:
        erroEnquad = True
    
    #Erro na propagação
    print("Erro na propagação---")
    erro = ErroMeioFisico(binWord)
    binWord = erro.erro()
    print("Binword com erro na propagação: ",binWord)        
    #utfWord = convertUTF(binWord)
    output_bytearray,original_lengths = convert_to_bytearray(binWord)
    print(output_bytearray)
    return output_bytearray,original_lengths
    #ans = executeSecondHalf(blist,tamanho)
    #print("THE EXECUTION WAS A SUCCEEEEEEEEEEEEEEEEEEEESSSSSSSSSSSS")
    #print(ans)
    #return utfWord

def copy_length(alist):
    global length
    print("O length é: ",length)
    length = alist.copy()
    print("O length atualizado é: ",length)
    return length