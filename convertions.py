#from configs import *

#Entrada: [[0,0,1,1,1,1]] Saída: '001111'
def convertToString(byteList):
    ans = ''
    for bit in byteList:
        ans += str(bit)
    print(ans)
    return ans

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

def demodularHamming(word:list[int]) -> list[int]:
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

def removeIntegersToChar(data:list[int]):
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