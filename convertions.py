
#Entrada: [[0,0,1,1,1,1]] Saída: '001111'
def convertToString(byteList):
    ans = ''
    for byte in byteList:
        #print('The byte is',byte)
        for bit in byte:
            ans += str(bit)
            #rint('the bit is',bit)
    print(ans)
    return ans

#Entrada: '001111' Saída: [[0,0,1,1,1,1]] 
def convertToByte(stringList):
    byteWord = []
    byte = []
    for bit in stringList:
        if len(byte) < 8:
            bit = int(bit)
            byte.append(bit)
        else:
            print(byte)
            byteWord.append(byte.copy())
            byte.clear()
    print(byteWord)
    return byteWord

def convertToByteDetect(stringList,desiredSize):
    byteWord = []
    byte = []
    for bit in stringList:
        if len(byte) < desiredSize:  # 8 bits per byte
            byte.append(int(bit))
        else:
            byteWord.append(byte.copy())  # Add completed byte to the list
            byte.clear()  # Clear byte for the next one
            byte.append(int(bit))  # Start a new byte with the current bit
    
    if byte:  # Check if there are any leftover bits and add them
        byteWord.append(byte.copy())

    print(byteWord)  # Debug print to check the result
    return byteWord

def removeLSBit(byteWord):
    for i in range(len(byteWord)):
        byteWord[i] = byteWord[i][:-1]  # Remove the last bit from each byte
    return byteWord

def bits_to_bytes(wordBit):
    byte_array = bytearray()
    lengths = []

    for bit_list in wordBit:
        # Calculate how many zeros to pad (nearest multiple of 8)
        padding = (8 - (len(bit_list) % 8)) % 8
        padded_bits = bit_list + [0] * padding  # Add the necessary padding

        # Store the original length for recovery
        lengths.append(len(bit_list))

        # Group bits into chunks of 8 and convert each chunk to a byte
        byte_array.extend(
            int("".join(map(str, padded_bits[i:i + 8])), 2)
            for i in range(0, len(padded_bits), 8)
        )

    return byte_array, lengths


def bytes_to_bits(byte_array, length):
    bit_list = []
    all_recovered_bits = []

    # Converter cada byte do byte_array para representação binária de 8 bits
    for byte in byte_array:
        bit_list.extend(int(bit) for bit in format(byte, "08b"))

    # Extrair a lista original de bits do comprimento especificado
    start = 0
    while start < len(bit_list):
        # Extrair o bloco ajustado ao comprimento especificado
        all_recovered_bits.append(bit_list[start:start + length])
        start += length  # Pular exatamente o comprimento necessário

    return all_recovered_bits