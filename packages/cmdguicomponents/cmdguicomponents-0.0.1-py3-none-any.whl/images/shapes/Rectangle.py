class CMDRectangle:
    def __init__(self, *, length: int, height: int, color: str='#ffffff', hollow: bool=False):
        def hexToAsciiColor(hexColor):
            if hexColor.startswith('#'):
                hexColor = hexColor[1:]

            try:
                r = int(hexColor[0:2], 16)
                g = int(hexColor[2:4], 16)
                b = int(hexColor[4:6], 16)
                asciiColor = f"\033[38;2;{r};{g};{b}m"
                asciiReset = "\033[0m"
                return asciiColor, asciiReset
            except ValueError:
                print("Invalid color code!")
                exit()

        asciiColor, asciiReset = hexToAsciiColor(color)
        print(f"{asciiColor}")

        self.length = length
        self.height = height
        self.hollow = hollow

        if self.height == 0 or self.length == 0:
            print("Both height and length cannot be zero!")
            exit()

        if not self.hollow:
            self.xList = ['██'] * self.length
            self.xText = ''.join(self.xList)

            self.yList = []
            for i in range(self.height):
                if i == self.height - 1:
                    self.yList.append(self.xText)
                else:
                    self.yList.append(self.xText + '\n')

            self.yText = ''.join(self.yList)

            print(self.yText)

        elif self.hollow:
            self.firstXList = []
            self.middleXList = []
            self.middleList = []
            self.middleXListSide = '██'
            self.middleXListMiddle = '  '

            self.middleXList.append(self.middleXListSide)
            self.middleXList.append(self.middleXListSide)

            for i in range(self.length):
                self.firstXList.append('██')

            self.firstXText = ''.join(self.firstXList)

            for i in range(self.length - 2):
                self.middleXList.insert(1, self.middleXListMiddle)

            self.middleRow = ''.join(self.middleXList)

            for i in range(self.height - 2):
                self.middleList.append(f"{self.middleRow}\n")

            self.middleText = ''.join(self.middleList)

            self.firstXTextB = self.firstXText

            if self.length == 1:
                if self.height == 1:
                    print('██')
                else:
                    self.oneMiddleXList = []
                    self.middleText = '██\n'
                    for i in range(self.height - 2):
                        self.oneMiddleXList.append(self.middleText)

                    self.oneMiddleXText = ''.join(self.oneMiddleXList)
                    print(f"{self.firstXText}\n{self.oneMiddleXText}{self.firstXTextB}")
            elif self.height == 1:
                print(f"{self.firstXText}")
            else:
                print(f"{self.firstXText}\n{self.middleText}{self.firstXTextB}")
        print(asciiReset)
