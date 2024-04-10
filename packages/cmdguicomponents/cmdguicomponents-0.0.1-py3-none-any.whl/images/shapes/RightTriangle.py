class CMDRightTriangle:
    def __init__(self, *, size: int, orientation: str, color: str='#ffffff', hollow: bool=False):
        self.size = size
        self.orientation = orientation
        self.color = color
        self.hollow = hollow
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

        asciiColor, asciiReset = hexToAsciiColor(self.color)
        print(asciiColor)

        if self.orientation == 'rightDown':
            if not self.hollow:
                clearLastLines(1)
                for i in range(self.size):
                    print(f"{((self.size-i)*'██')+(i*'  ')}\n", end='')
                print(asciiReset)
                clearLastLines(1)

            elif self.hollow:
                clearLastLines(1)
                self.index = 0
                for i in range(self.size):
                    if i == 0:
                        print(self.size*'██')
                    elif i == self.size - 1:
                        print(f"██")
                    else:        
                        print(f"{('██')+((self.size-self.index-3)*'  ')+('██')}")
                        self.index += 1
                print(asciiReset)
                clearLastLines(1)

        elif self.orientation == 'rightUp':
            if not self.hollow:
                clearLastLines(1)
                for i in range(self.size):
                    print(f"{((i+1)*'██')+(i*'  ')}\n", end='')
                print(self.asciiReset)
                clearLastLines(1)

            elif self.hollow:
                clearLastLines(1)
                self.index = self.size
                for i in range(size):
                    if i == 0:
                        print(f"██")
                    elif i == self.size - 1:
                        print(self.size*'██')
                    else:
                        print(f"{('██')+((self.size-self.index)*'  ')+('██')}")
                        self.index -= 1
                print(asciiReset)
                clearLastLines(1)

        elif self.orientation == 'leftDown':
            if not self.hollow:
                clearLastLines(1)
                self.index = 0
                for i in range(self.size):
                    if i == 0:
                        print(self.size*'██')
                    elif i == self.size - 1:
                        print(((self.size-1)*'  ')+('██'))
                    else:
                        print(((self.index+1)*'  ')+('██')+((self.size-i-2)*'██')+('██'))
                        self.index += 1
                print(asciiReset)
                clearLastLines(1)

            elif self.hollow:
                clearLastLines(1)
                self.index = 0
                for i in range(self.size):
                    if i == 0:
                        print(self.size*'██')
                    elif i == self.size - 1:
                        print(((self.size-1)*'  ')+('██'))
                    else:
                        print(((self.index+1)*'  ')+('██')+((self.size-i-2)*'  ')+('██'))
                        self.index += 1
                print(asciiReset)
                clearLastLines(1)

        elif self.orientation == 'leftUp':
            if not self.hollow:
                clearLastLines(1)
                self.index = self.size
                self.indexC = 0
                for i in range(self.size):
                    if i == 0:
                        print(((self.size-1)*'  ')+'██')
                    elif i == self.size - 1:
                        print(self.size*'██')
                    else:
                        print(((self.index-2)*'  ')+('██')+(self.indexC*'██')+('██'))
                        self.index -= 1
                        self.indexC += 1
                print(asciiReset)
                clearLastLines(1)

            elif self.hollow:
                clearLastLines(1)
                self.index = self.size
                self.indexC = 0
                for i in range(self.size):
                    if i == 0:
                        print(((self.size-1)*'  ')+'██')
                    elif i == self.size - 1:
                        print(self.size*'██', end='')
                    else:
                        print(((self.index-2)*'  ')+('██')+(self.indexC*'  ')+('██'))
                        self.index -= 1
                        self.indexC += 1
                print(asciiReset, end='')
                clearLastLines(0)
