def convertToString(byteList):
    ans = ''
    for byte in byteList:
        #print('The byte is',byte)
        for bit in byte:
            ans += str(bit)
            #rint('the bit is',bit)
    print(ans)
    return ans

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