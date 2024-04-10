from HexDataType import hex

class HexToASCIIColor:
    def __init__(self, hexColor: hex):
        if hexColor.startswith('#'):
            hexColor = hexColor[1:]

        try:
            r = int(hexColor[0:2], 16)
            g = int(hexColor[2:4], 16)
            b = int(hexColor[4:6], 16)

            self.asciiColor = f"\033[38;2;{r};{g};{b}m"
            self.asciiReset = "\033[0m"
        except ValueError:
            print("Invalid color code!")
            exit()
