#from configs import *

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
def convertToByteCRCAdapt(stringList):
    byteWord = []
    byte = []
    for bit in stringList:
        if len(byte) < 11:
            bit = int(bit)
            byte.append(bit)
        else:
            print(byte)
            byteWord.append(byte.copy())
            byte.clear()
    print(byte)
    return byte

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
    print('This is your byteWord: ',byteWord)
    return byteWord[:-1]

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

    # Convert each byte in the bytearray to its 8-bit binary representation
    for byte in byte_array:
        bit_list.extend(int(bit) for bit in format(byte, "08b"))

    # Extrair os blocos corretamente com base no comprimento desejado
    total_bits = len(bit_list)
    for i in range(0, total_bits, length):
        # Certifique-se de que o último bloco não ultrapasse o comprimento 'length'
        all_recovered_bits.append(bit_list[i:i + length])

    return all_recovered_bits
def executeEverything(int_list):
    """
    Processes a list of nested bit lists into a single bytearray and collects padding info.
    """
    print("LET'S EXECUTE THIS BULLSHIT", int_list)
    combined_bytearray = bytearray()
    padding_info = []
    lengths = []  # Store lengths of original sublists (before padding)

    for i, sublist in enumerate(int_list):
        if not sublist:  # Skip empty sublists
            padding_info.append([])
            lengths.append(0)
            continue

        bit_list, sub_padding_info = fitSize(sublist)
        byte_array = toByteArray(bit_list)
        combined_bytearray.extend(byte_array)
        lengths.append(len(byte_array))  # Store the length of the current sublist's bytearray
        padding_info.append(sub_padding_info)
    
    return combined_bytearray, padding_info, lengths


def executeSecondHalf(combined_bytearray, padding_info, lengths):
    """
    Reverses the process: reconstructs the original bit list from the combined bytearray.
    """
    restored_bit_list = []
    start = 0

    for i, sub_padding_info in enumerate(padding_info):
        if lengths[i] == 0:  # Handle empty sublist
            restored_bit_list.append([])
            continue

        # Extract the relevant section of the bytearray for this sublist
        sub_bytearray = combined_bytearray[start:start + lengths[i]]
        start += lengths[i]
        
        # Convert byte array back to bit list
        restored_bits = toBitList(sub_bytearray)
        # Remove the padding for this sublist
        restored_bits = removePadding(restored_bits, sub_padding_info)
        restored_bit_list.append(restored_bits)

    return restored_bit_list


def fitSize(alist):
    """
    Converts a flat list of bits into 8-bit chunks and tracks padding information.
    """
    byte_list = []  # List to store 8-bit chunks
    padding_info = []  # Info about how much padding was added
    
    for i in range(0, len(alist), 8):
        byte = alist[i:i + 8]
        if len(byte) < 8:
            padding = 8 - len(byte)
            byte = byte + [0] * padding  # Pad with zeros at the end
            padding_info.append((len(byte_list), padding))
        byte_list.append(byte)
        
    return byte_list, padding_info


def toByteArray(bit_list):
    """
    Converts a list of 8-bit lists into a bytearray.
    """
    byte_array = bytearray()
    for byte in bit_list:
        byte_value = int("".join(map(str, byte)), 2)
        byte_array.append(byte_value)
    return byte_array


def toBitList(byte_array):
    """
    Converts a bytearray back into a flat list of bits.
    """
    bit_list = []
    for byte in byte_array:
        bits = list(map(int, format(byte, "08b")))
        bit_list.extend(bits)
    return bit_list


def removePadding(bit_list, padding_info):
    """
    Removes padding bits based on padding information.
    """
    for index, padding in reversed(padding_info):
        if padding > 0:
            bit_list = bit_list[:-(padding)]
    return bit_list

def demodularHamming(word):
    n = len(word)
    two_data = []
    i = 0
    value = 2**i
    
    while value <= n:
        two_data.append(value - 1)
        i += 1
        value = 2**i
    
    removed_word = [bit for idx, bit in enumerate(word) if idx not in two_data]
    return removed_word

def removeIntegersToChar(data):
    result = []
    # Convert the 8-bit list to a string (representing binary)
    binary_string = ''.join(map(str, data))
    
    # Convert the binary string to a character
    char = chr(int(binary_string, 2))
    
    # Check if the character is a digit
    if not char.isdigit():
        return data
    else:
        print('Its a number',char)

def convert_to_bytearray(list_of_lists):
    """
    Converts a list of lists of integers into a bytearray.
    Pads bits to ensure proper byte alignment.

    Args:
        list_of_lists (list of lists of int): Input list of binary lists.

    Returns:
        bytearray: A bytearray containing the corresponding byte values.
        list: Original bit lengths of each list before padding.
    """
    def binary_to_integer(binary_list):
        # Converts a binary list into an integer.
        return int("".join(map(str, binary_list)), 2)

    bytearray_result = bytearray()
    padded_lengths = []  # Store the original lengths before padding
    bit_buffer = []  # Buffer to accumulate bits

    for binary_list in list_of_lists:
        original_length = len(binary_list)  # Store the original length of the list
        padded_lengths.append(original_length)

        # Add the bits to the buffer
        bit_buffer.extend(binary_list)

        # When buffer reaches or exceeds 8 bits, convert to byte (8 bits)
        while len(bit_buffer) >= 8:
            byte_chunk = bit_buffer[:8]
            bytearray_result.append(binary_to_integer(byte_chunk))
            bit_buffer = bit_buffer[8:]  # Remove the first 8 bits

    # If there are leftover bits, pad with zeros and add to bytearray
    if len(bit_buffer) > 0:
        byte_chunk = bit_buffer + [0] * (8 - len(bit_buffer))  # Pad with zeros
        bytearray_result.append(binary_to_integer(byte_chunk))

    return bytearray_result, padded_lengths


def bytearray_to_binary_integer_lists(byte_array, original_lengths):
    """
    Converts a bytearray back into a list of binary integer lists, 
    restoring the original bit lengths.

    Args:
        byte_array (bytearray): The bytearray to convert back.
        original_lengths (list of int): Original lengths of the binary lists before padding.

    Returns:
        list of lists of int: Binary lists with original bit lengths.
    """
    # Convert bytearray to binary format (8 bits per byte)
    binary_lists = [[int(bit) for bit in f"{byte:08b}"] for byte in byte_array]

    # Accumulate bits into a buffer to match the original lengths
    all_bits = []
    for binary_list in binary_lists:
        all_bits.extend(binary_list)

    # Now split back into the original lengths
    result = []
    bit_index = 0
    for length in original_lengths:
        # Get the next chunk of bits with the original length
        result.append(all_bits[bit_index:bit_index + length])
        bit_index += length

    return result
def bin_to_string(binary_lists):
    result = ""
    for binary_list in binary_lists:
        # Converte a lista de bits em uma string binária
        binary_string = ''.join(map(str, binary_list))
        # Converte a string binária em um número decimal
        decimal_value = int(binary_string, 2)
        # Converte o número decimal em um caractere ASCII
        result += chr(decimal_value)
    return result