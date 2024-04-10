class CMDEquilateralTriangle:
    def __init__(self, *, size: int, orientation: str, color: str='#ffffff', hollow: bool):
        self.orientation = orientation
        self.hollow = hollow
        self.size = size
        def clearLastLines(number):
            for _ in range(number):
                print("\033[F\033[K", end="")

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
        print(asciiColor)

        if self.orientation == 'up':
            if not self.hollow:
                if self.size == 1:
                    print('▲')
                else:
                    clearLastLines(1)
                    self.index = self.size
                    self.indexC = 1
                    for i in range(self.size):
                        print(((self.index-1)*' ')+((self.indexC)*'██')+((self.index-1)*''))
                        self.indexC += 1
                        self.index -= 1
                    print(asciiReset)
                    clearLastLines(1)

            elif self.hollow:
                if self.size == 1:
                    print('△')
                else:
                    clearLastLines(1)
                    self.index = 0
                    self.indexC = (self.size)-1
                    for i in range(self.size):
                        if i == size-1:
                            print(('█')+((size-1)*'▄▄')+('█'))
                        else:
                            print(((self.indexC)*' ')+('█')+(self.index*'  ')+('█')+((self.indexC)*' '))
                        self.index += 1
                        self.indexC -= 1
                    print(asciiReset)
                    clearLastLines(1)

        elif self.orientation == 'down':
            if not self.hollow:
                if self.size == 1:
                    print('▼')
                else:
                    clearLastLines(1)
                    self.index = 1
                    self.indexC = self.size
                    for i in range(self.size):
                        print(((self.index-1)*' ')+((self.indexC)*'██')+((self.index-1)*''))
                        self.indexC -= 1
                        self.index += 1
                    print(asciiReset)
                    clearLastLines(1)

            elif self.hollow:
                if self.size == 1:
                    print('▽')
                else:
                    clearLastLines(1)
                    self.index = (self.size)-1
                    self.indexC = 0
                    for i in range(self.size):
                        if i == 0:
                            print(('█')+((size-1)*'▀▀')+('█'))
                        else:
                            print(((self.indexC)*' ')+('█')+(self.index*'  ')+('█')+((self.indexC)*' '))
                        self.index -= 1
                        self.indexC += 1
                    print(asciiReset)
                    clearLastLines(1)

        elif self.orientation == 'right':
            if not self.hollow:
                if self.size == 1:
                    print('▶')

                elif (self.size % 2) == 0:
                    clearLastLines(1)
                    index = 1
                    print('██▄▄')
                    for i in range((self.size//2)-1):
                        print(('██')+(index*'██')+('██▄▄'))
                        index += 2

                    for i in reversed(range(int(self.size//2)-1)):
                        print(('██')+((index-2)*'██')+('██▀▀'))
                        index -= 2
                    print('██▀▀')
                    print(asciiReset)
                    clearLastLines(1)

                elif (self.size % 2) == 1:
                    clearLastLines(1)
                    index = 1
                    middleIndex = int((self.size//2)+1.5)
                    print('██▄▄')
                    for i in range(int((self.size//2)+0.5)-1):
                        print(('█ ')+(index*'██')+('██▄▄'))
                        index += 2

                    print(('██')+((index)*'██')+('██'))

                    for i in reversed(range(int((self.size//2)+0.5)-1)):
                        print(('██')+((index-2)*'██')+('██▀▀'))
                        index -= 2
                    print('██▀▀')
                    print(asciiReset)
                    clearLastLines(1)

            elif self.hollow:
                if self.size == 1:
                    print('▷')

                elif (self.size % 2) == 0:
                    clearLastLines(1)
                    index = 1
                    print('█▀▄▄')
                    for i in range((self.size//2)-1):
                        print(('█ ')+(index*'  ')+('▀▀▄▄'))
                        index += 2

                    for i in reversed(range(int(self.size//2)-1)):
                        print(('█ ')+((index-2)*'  ')+('▄▄▀▀'))
                        index -= 2
                    print('█▄▀▀')
                    print(asciiReset)
                    clearLastLines(1)

                elif (self.size % 2) == 1:
                    clearLastLines(1)
                    index = 1
                    middleIndex = int((self.size//2)+1.5)
                    print('█▀▄▄')
                    for i in range(int((self.size//2)+0.5)-1):
                        print(('█ ')+(index*'  ')+('▀▀▄▄'))
                        index += 2

                    print(('█ ')+((index)*'  ')+('██'))

                    for i in reversed(range(int((self.size//2)+0.5)-1)):
                        print(('█ ')+((index-2)*'  ')+('▄▄▀▀'))
                        index -= 2
                    print('█▄▀▀')
                    print(asciiReset)
                    clearLastLines(1)

        elif self.orientation == 'left':
            if not self.hollow:
                if self.size == 1:
                    print('◀')

                elif (self.size % 2) == 0:
                    clearLastLines(1)
                    a = self.size-4
                    b = 0
                    print(((self.size-2)*'  ')+('▄▄██'))
                    for i in range((self.size//2)-1):
                        print((a*'  ')+('▄▄██')+((self.size-(a+3))*'██')+('██'))
                        a -= 2

                    for i in range((self.size//2)-1):
                        print((b*'  ')+('▀▀██')+((self.size-(b+3))*'██')+('██'))
                        b += 2
                    print(((self.size-2)*'  ')+('▀▀██'))
                    print(asciiReset)
                    clearLastLines(1)

                elif (self.size % 2) == 1:
                    clearLastLines(1)
                    index = self.size-4
                    a = 1
                    middleIndex = int((self.size//2)+1.5)
                    print(((self.size-2)*'  ')+('▄▄██'))

                    for i in range(int(self.size//2-1)):
                        print((index*'  ')+('▄▄██')+(a*'██')+('██'))
                        index -= 2
                        a += 2

                    print(('██')+((self.size-2)*'██')+('██'))

                    for i in range(self.size//2-1):
                        if i == 0:
                            print(('  ')+((index//2)*'    ')+('▀▀██')+((a-2)*'██')+('██'))
                        else:
                            print(('      ')+((index//2)*'    ')+('▀▀██')+((a-2)*'██')+('██'))
                        index += 2
                        a -= 2

                    print(((self.size-2)*'  ')+('▀▀██'))
                    print(asciiReset)
                    clearLastLines(1)


            elif self.hollow:
                if self.size == 1:
                    print('◁')

                elif (self.size % 2) == 0:
                    clearLastLines(1)
                    a = self.size-4
                    b = 0
                    print(((self.size-2)*'  ')+('▄▄▀█'))
                    for i in range((self.size//2)-1):
                        print((a*'  ')+('▄▄▀▀')+((self.size-(a+3))*'  ')+(' █'))
                        a -= 2

                    for i in range((self.size//2)-1):
                        print((b*'  ')+('▀▀▄▄')+((self.size-(b+3))*'  ')+(' █'))
                        b += 2
                    print(((self.size-2)*'  ')+('▀▀▄█'))
                    print(asciiReset)
                    clearLastLines(1)

                elif (self.size % 2) == 1:
                    clearLastLines(1)
                    index = self.size-4
                    a = 1
                    middleIndex = int((self.size//2)+1.5)
                    print(((self.size-2)*'  ')+('▄▄▀█'))

                    for i in range(int(self.size//2-1)):
                        print((index*'  ')+('▄▄▀▀')+(a*'  ')+(' █'))
                        index -= 2
                        a += 2

                    print(('██')+((self.size-2)*'  ')+(' █'))

                    for i in range(self.size//2-1):
                        if i == 0:
                            print(('  ')+((index//2)*'    ')+('▀▀▄▄')+((a-2)*'  ')+(' █'))
                        else:
                            print(('      ')+((index//2)*'    ')+('▀▀▄▄')+((a-2)*'  ')+(' █'))
                        index += 2
                        a -= 2

                    print(((self.size-2)*'  ')+('▀▀▄█'))
                    print(asciiReset)
                    clearLastLines(1)
