import os
import shutil
from PIL import Image

class CMDImage:
    def __init__(self, *, imagePath):
        self.imagePath = imagePath
        self.convertImageToAscii()

    def getTerminalSize(self):
        columns, rows = shutil.get_terminal_size()
        return columns, rows

    def getHexColor(self, pixel):
        hexColor = '#{0:02x}{1:02x}{2:02x}'.format(*pixel)
        return hexColor

    def convertToAsciiColorCode(self, hexColor):
        r, g, b = tuple(int(hexColor[i:i+2], 16) for i in (1, 3, 5))
        return f'\033[38;2;{r};{g};{b}m'

    def convertImageToAscii(self):
        terminalWidth, terminalHeight = self.getTerminalSize()

        image = Image.open(self.imagePath)
        originalWidth, originalHeight = image.size

        scaleFactorWidth = terminalWidth / (originalWidth * 2)
        scaleFactorHeight = terminalHeight / originalHeight
        scaleFactor = min(scaleFactorWidth, scaleFactorHeight)
        newWidth = int(originalWidth * scaleFactor)
        newHeight = int(originalHeight * scaleFactor)

        image = image.resize((newWidth, newHeight))

        for y in range(newHeight):
            for x in range(newWidth):
                pixelColor = image.getpixel((x, y))
                hexColor = self.getHexColor(pixelColor)
                asciiColorCode = self.convertToAsciiColorCode(hexColor)
                print(f'{asciiColorCode}██', end='')
            print('\033[0m')
