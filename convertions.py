
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

def convertToByteDetect(stringList):
    byteWord = []
    byte = []
    for bit in stringList:
        if len(byte) < 9:  # 8 bits per byte
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