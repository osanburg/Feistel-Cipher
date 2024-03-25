import random
import binascii

# convert plain text to 8-bit binary
def TextToBinary(txt):
    return ''.join(bin(ord(chr)) for chr in txt).replace('b','')

# convert 8-bit binary to ASCII characters
def BinaryToASCII(bin):
    asc = ""
    for i in range(0, len(bin), 7):
        asc += chr(int(bin[i:i+7], 2))
    return asc

# convert 8-bit binary to plain text
def BinaryToPlainText(bin):
    return (binascii.unhexlify( '%x'% int(bin, 2))).decode()
  
# generate a random binary key with a length equal to num
def GenKey(num):
    newKey = ""
    for i in range(num):
        newKey += str(random.randint(0,1))
    return newKey

# return result of bitwise XOR operation on two binary strings
def XorBit(bin1, bin2):
    result = ""
    for i in range(len(bin1)):
        if bin1[i] == bin2[i]:
            result += "0"
        else:
            result += "1"
    return result

# encrypt and decrypt plain text string with feistel cipher
def FeistelEncryptDecrypt(message):

    print("Plain text message:", message)

    BinMessage = TextToBinary(message)

    # split message in two
    l =  len(BinMessage)//2
    L1 = BinMessage[:l]
    R1 = BinMessage[l:]

    # generate keys for each round
    key1 = GenKey(l)
    key2 = GenKey(l)

    # feistel encryption round 1: xor the right part with key1, then xor the result with the left part to get the new right part.
    #   The left part then becomes the previous right part 
    F1 = XorBit(R1, key1)
    R2 = XorBit(L1, F1)
    L2 = R1

    # feistel encryption round 2: perform the same steps as the first round with key2 and the new left and right parts
    F2 = XorBit(R2, key2)
    R3 = XorBit(L2, F2)
    L3 = R2

    # Combining the left and right part gives the binary cipher
    BinCipher = L3 + R3
    
    # convert the binary cipher to ASCII characters and print to show encryption
    CipherText = BinaryToASCII(BinCipher)
    print("Cipher text:", CipherText)

    # The process to decrypt a feistel cipher is very similar to the process to create it, need to work backwords to get back to the original
    L4 = R3
    R4 = L3

    # feistel decryption round 1: xor the left part with key2, then xor the result with the right part
    F3 = XorBit(R4, key2)
    R5 = XorBit(L4, F3)
    L5 = R4

    # feistel decryption round 2: perform the same steps as round 1 but with key1 and the new left and right parts
    F4 = XorBit(R5, key1)
    R6 = XorBit(L5, F4)
    L6 = R5

    # swap halves and combine to get decrypted binary string
    L7 = R6
    R7 = L6
    BinDecrypt = L7 + R7

    # convert the decrypted binary back to plain text and print to show decryption 
    DecryptedMessage = BinaryToPlainText(BinDecrypt)
    print("Decrypted message:", DecryptedMessage)
    print("")



message1 = "HelloWorld"
message2 = "Password"
message3 = "It_Is_Raining"

FeistelEncryptDecrypt(message1)
FeistelEncryptDecrypt(message2)
FeistelEncryptDecrypt(message3)
