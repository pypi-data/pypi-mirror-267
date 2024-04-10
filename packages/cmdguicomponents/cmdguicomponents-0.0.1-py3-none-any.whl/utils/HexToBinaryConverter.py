class HexToBinaryConverter:
    def __init__(self, hexString):
        self.hexString = hexString

    def convertToBinary(self):
        try:
            decimalValue = int(self.hexString, 16)
            binaryString = bin(decimalValue)[2:]
            return binaryString
        except ValueError:
            print("Invalid hexadecimal string.")

    def __str__(self):
        return self.convertToBinary()
