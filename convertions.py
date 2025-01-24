
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