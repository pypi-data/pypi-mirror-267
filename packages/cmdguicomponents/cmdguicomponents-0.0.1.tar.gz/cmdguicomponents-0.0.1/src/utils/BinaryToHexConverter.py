class BinaryToHexConverter:
    def __init__(self, binaryString):
        self.binaryString = binaryString

    def convertToHex(self):
        try:
            decimalValue = int(self.binaryString, 2)
            hexString = hex(decimalValue)[2:].upper()
            return hexString
        except ValueError:
            print("Invalid binary string.")

    def __str__(self):
        return self.convertToHex()
