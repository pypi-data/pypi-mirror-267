import msvcrt

class CMDRadioButton:
    def __init__(self, *, amount: int, values: list, continueBind: str, color: str='#ffffff'):
        self.selectedRadioButton = '⦿\n\n'
        self.unselectedRadioButton = '⭕\n\n'
        self.continueBind = continueBind
        self.amount = amount
        self.values = values
        self.amountOfValues = len(self.values)

        if self.amountOfValues != self.amount:
            print("Amount and values must match!")
            exit()

        def clearLastLines():
            for _ in range(self.number):
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
        print(f"{asciiColor}")

        if self.amount == 0 or self.amount == 1 or self.amount > 10:
            print("Amount must be higher than 1 and less than 11.")
            exit()

        elif self.amount == 2:
            self.number = 3
            self.frame = 1
            self.amountTwoFrameOne = f"⦿  {self.values[0]}\n\n⭕  {self.values[1]}"
            self.amountTwoFrameTwo = f"⭕  {self.values[0]}\n\n⦿  {self.values[1]}"

            print(f"\r{self.amountTwoFrameOne}")

            while True:
                self.key = msvcrt.getch()
                if self.key == b'\xe0':
                    self.key = msvcrt.getch()
                    if self.key == b'H' or self.key == b'P':
                        if self.frame == 1:
                            self.frame = 2
                            clearLastLines()
                            print(f"\r{self.amountTwoFrameTwo}")
                        elif self.frame == 2:
                            self.frame = 1
                            clearLastLines()
                            print(f"\r{self.amountTwoFrameOne}")
                elif self.continueBind == self.key.decode():
                    break

        elif self.amount == 3:
            self.number = 5
            self.frame = 1
            self.amountThreeFrameOne = f"⦿  {self.values[0]}\n\n⭕  {self.values[1]}\n\n⭕  {self.values[2]}"
            self.amountThreeFrameTwo = f"⭕  {self.values[0]}\n\n⦿  {self.values[1]}\n\n⭕  {self.values[2]}"
            self.amountThreeFrameThree = f"⭕  {self.values[0]}\n\n⭕  {self.values[1]}\n\n⦿  {self.values[2]}"

            print(f"\r{self.amountThreeFrameOne}")

            while True:
                self.key = msvcrt.getch()
                if self.key == b'\xe0':
                    self.key = msvcrt.getch()
                    if self.key == b'H':
                        if self.frame == 1:
                            self.frame = 3
                            clearLastLines()
                            print(f"\r{self.amountThreeFrameThree}")
                        elif self.frame == 2:
                            self.frame = 1
                            clearLastLines()
                            print(f"\r{self.amountThreeFrameOne}")
                        elif self.frame == 3:
                            self.frame = 2
                            clearLastLines()
                            print(f"\r{self.amountThreeFrameTwo}")
                    elif self.key == b'P':
                        if self.frame == 1:
                            self.frame = 2
                            clearLastLines()
                            print(f"\r{self.amountThreeFrameTwo}")
                        elif self.frame == 2:
                            self.frame = 3
                            clearLastLines()
                            print(f"\r{self.amountThreeFrameThree}")
                        elif self.frame == 3:
                            self.frame = 1
                            clearLastLines()
                            print(f"\r{self.amountThreeFrameOne}")
                elif self.continueBind == self.key.decode():
                    break

        elif self.amount == 4:
            self.number = 7
            self.frame = 1
            self.amountFourFrameOne = f"⦿  {self.values[0]}\n\n⭕  {self.values[1]}\n\n⭕  {self.values[2]}\n\n⭕  {self.values[3]}"
            self.amountFourFrameTwo = f"⭕  {self.values[0]}\n\n⦿  {self.values[1]}\n\n⭕  {self.values[2]}\n\n⭕  {self.values[3]}"
            self.amountFourFrameThree = f"⭕  {self.values[0]}\n\n⭕  {self.values[1]}\n\n⦿  {self.values[2]}\n\n⭕  {self.values[3]}"
            self.amountFourFrameFour = f"⭕  {self.values[0]}\n\n⭕  {self.values[1]}\n\n⭕  {self.values[2]}\n\n⦿  {self.values[3]}"

            print(f"\r{self.amountFourFrameOne}")

            while True:
                self.key = msvcrt.getch()
                if self.key == b'\xe0':
                    self.key = msvcrt.getch()
                    if self.key == b'H':
                        if self.frame == 1:
                            self.frame = 4
                            clearLastLines()
                            print(f"\r{self.amountFourFrameFour}")
                        elif self.frame == 2:
                            self.frame = 1
                            clearLastLines()
                            print(f"\r{self.amountFourFrameOne}")
                        elif self.frame == 3:
                            self.frame = 2
                            clearLastLines()
                            print(f"\r{self.amountFourFrameTwo}")
                        elif self.frame == 4:
                            self.frame = 3
                            clearLastLines()
                            print(f"\r{self.amountFourFrameThree}")
                    elif self.key == b'P':
                        if self.frame == 1:
                            self.frame = 2
                            clearLastLines()
                            print(f"\r{self.amountFourFrameTwo}")
                        elif self.frame == 2:
                            self.frame = 3
                            clearLastLines()
                            print(f"\r{self.amountFourFrameThree}")
                        elif self.frame == 3:
                            self.frame = 4
                            clearLastLines()
                            print(f"\r{self.amountFourFrameFour}")
                        elif self.frame == 4:
                            self.frame = 1
                            clearLastLines()
                            print(f"\r{self.amountFourFrameOne}")
                elif self.continueBind == self.key.decode():
                    break

        elif self.amount == 5:
            self.number = 9
            self.frame = 1
            self.amountFiveFrameOne = f"⦿  {self.values[0]}\n\n⭕  {self.values[1]}\n\n⭕  {self.values[2]}\n\n⭕  {self.values[3]}\n\n⭕  {self.values[4]}"
            self.amountFiveFrameTwo = f"⭕  {self.values[0]}\n\n⦿  {self.values[1]}\n\n⭕  {self.values[2]}\n\n⭕  {self.values[3]}\n\n⭕  {self.values[4]}"
            self.amountFiveFrameThree = f"⭕  {self.values[0]}\n\n⭕  {self.values[1]}\n\n⦿  {self.values[2]}\n\n⭕  {self.values[3]}\n\n⭕  {self.values[4]}"
            self.amountFiveFrameFour = f"⭕  {self.values[0]}\n\n⭕  {self.values[1]}\n\n⭕  {self.values[2]}\n\n⦿  {self.values[3]}\n\n⭕  {self.values[4]}"
            self.amountFiveFrameFive = f"⭕  {self.values[0]}\n\n⭕  {self.values[1]}\n\n⭕  {self.values[2]}\n\n⭕  {self.values[3]}\n\n⦿  {self.values[4]}"

            print(f"\r{self.amountFiveFrameOne}")

            while True:
                self.key = msvcrt.getch()
                if self.key == b'\xe0':
                    self.key = msvcrt.getch()
                    if self.key == b'H':
                        if self.frame == 1:
                            self.frame = 5
                            clearLastLines()
                            print(f"\r{self.amountFiveFrameFive}")
                        elif self.frame == 2:
                            self.frame = 1
                            clearLastLines()
                            print(f"\r{self.amountFiveFrameOne}")
                        elif self.frame == 3:
                            self.frame = 2
                            clearLastLines()
                            print(f"\r{self.amountFiveFrameTwo}")
                        elif self.frame == 4:
                            self.frame = 3
                            clearLastLines()
                            print(f"\r{self.amountFiveFrameThree}")
                        elif self.frame == 5:
                            self.frame = 4
                            clearLastLines()
                            print(f"\r{self.amountFiveFrameFour}")
                    elif self.key == b'P':
                        if self.frame == 1:
                            self.frame = 2
                            clearLastLines()
                            print(f"\r{self.amountFiveFrameTwo}")
                        elif self.frame == 2:
                            self.frame = 3
                            clearLastLines()
                            print(f"\r{self.amountFiveFrameThree}")
                        elif self.frame == 3:
                            self.frame = 4
                            clearLastLines()
                            print(f"\r{self.amountFiveFrameFour}")
                        elif self.frame == 4:
                            self.frame = 5
                            clearLastLines()
                            print(f"\r{self.amountFiveFrameFive}")
                        elif self.frame == 5:
                            self.frame = 1
                            clearLastLines()
                            print(f"\r{self.amountFiveFrameOne}")
                elif self.continueBind == self.key.decode():
                    break

        elif self.amount == 6:
            self.number = 11
            self.frame = 1
            self.amountSixFrameOne = f"⦿  {self.values[0]}\n\n⭕  {self.values[1]}\n\n⭕  {self.values[2]}\n\n⭕  {self.values[3]}\n\n⭕  {self.values[4]}\n\n⭕  {self.values[5]}"
            self.amountSixFrameTwo = f"⭕  {self.values[0]}\n\n⦿  {self.values[1]}\n\n⭕  {self.values[2]}\n\n⭕  {self.values[3]}\n\n⭕  {self.values[4]}\n\n⭕  {self.values[5]}"
            self.amountSixFrameThree = f"⭕  {self.values[0]}\n\n⭕  {self.values[1]}\n\n⦿  {self.values[2]}\n\n⭕  {self.values[3]}\n\n⭕  {self.values[4]}\n\n⭕  {self.values[5]}"
            self.amountSixFrameFour = f"⭕  {self.values[0]}\n\n⭕  {self.values[1]}\n\n⭕  {self.values[2]}\n\n⦿  {self.values[3]}\n\n⭕  {self.values[4]}\n\n⭕  {self.values[5]}"
            self.amountSixFrameFive = f"⭕  {self.values[0]}\n\n⭕  {self.values[1]}\n\n⭕  {self.values[2]}\n\n⭕  {self.values[3]}\n\n⦿  {self.values[4]}\n\n⭕  {self.values[5]}"
            self.amountSixFrameSix = f"⭕  {self.values[0]}\n\n⭕  {self.values[1]}\n\n⭕  {self.values[2]}\n\n⭕  {self.values[3]}\n\n⭕  {self.values[4]}\n\n⦿  {self.values[5]}"

            print(f"\r{self.amountSixFrameOne}")

            while True:
                self.key = msvcrt.getch()
                if self.key == b'\xe0':
                    self.key = msvcrt.getch()
                    if self.key == b'H':
                        if self.frame == 1:
                            self.frame = 6
                            clearLastLines()
                            print(f"\r{self.amountSixFrameSix}")
                        elif self.frame == 2:
                            self.frame = 1
                            clearLastLines()
                            print(f"\r{self.amountSixFrameOne}")
                        elif self.frame == 3:
                            self.frame = 2
                            clearLastLines()
                            print(f"\r{self.amountSixFrameTwo}")
                        elif self.frame == 4:
                            self.frame = 3
                            clearLastLines()
                            print(f"\r{self.amountSixFrameThree}")
                        elif self.frame == 5:
                            self.frame = 4
                            clearLastLines()
                            print(f"\r{self.amountSixFrameFour}")
                        elif self.frame == 6:
                            self.frame = 5
                            clearLastLines()
                            print(f"\r{self.amountSixFrameFive}")
                    elif self.key == b'P':
                        if self.frame == 1:
                            self.frame = 2
                            clearLastLines()
                            print(f"\r{self.amountSixFrameTwo}")
                        elif self.frame == 2:
                            self.frame = 3
                            clearLastLines()
                            print(f"\r{self.amountSixFrameThree}")
                        elif self.frame == 3:
                            self.frame = 4
                            clearLastLines()
                            print(f"\r{self.amountSixFrameFour}")
                        elif self.frame == 4:
                            self.frame = 5
                            clearLastLines()
                            print(f"\r{self.amountSixFrameFive}")
                        elif self.frame == 5:
                            self.frame = 6
                            clearLastLines()
                            print(f"\r{self.amountSixFrameSix}")
                        elif self.frame == 6:
                            self.frame = 1
                            clearLastLines()
                            print(f"\r{self.amountSixFrameOne}")
                elif self.continueBind == self.key.decode():
                    break

        elif self.amount == 7:
            self.number = 11
            self.frame = 1
            self.amountSevenFrameOne = f"⦿  {self.values[0]}\n\n⭕  {self.values[1]}\n\n⭕  {self.values[2]}\n\n⭕  {self.values[3]}\n\n⭕  {self.values[4]}\n\n⭕  {self.values[5]}\n\n⭕  {self.values[6]}"
            self.amountSevenFrameTwo = f"⭕  {self.values[0]}\n\n⦿  {self.values[1]}\n\n⭕  {self.values[2]}\n\n⭕  {self.values[3]}\n\n⭕  {self.values[4]}\n\n⭕  {self.values[5]}\n\n⭕  {self.values[6]}"
            self.amountSevenFrameThree = f"⭕  {self.values[0]}\n\n⭕  {self.values[1]}\n\n⦿  {self.values[2]}\n\n⭕  {self.values[3]}\n\n⭕  {self.values[4]}\n\n⭕  {self.values[5]}\n\n⭕  {self.values[6]}"
            self.amountSevenFrameFour = f"⭕  {self.values[0]}\n\n⭕  {self.values[1]}\n\n⭕  {self.values[2]}\n\n⦿  {self.values[3]}\n\n⭕  {self.values[4]}\n\n⭕  {self.values[5]}\n\n⭕  {self.values[6]}"
            self.amountSevenFrameFive = f"⭕  {self.values[0]}\n\n⭕  {self.values[1]}\n\n⭕  {self.values[2]}\n\n⭕  {self.values[3]}\n\n⦿  {self.values[4]}\n\n⭕  {self.values[5]}\n\n⭕  {self.values[6]}"
            self.amountSevenFrameSix = f"⭕  {self.values[0]}\n\n⭕  {self.values[1]}\n\n⭕  {self.values[2]}\n\n⭕  {self.values[3]}\n\n⭕  {self.values[4]}\n\n⦿  {self.values[5]}\n\n⭕  {self.values[6]}"
            self.amountSevenFrameSeven = f"⭕  {self.values[0]}\n\n⭕  {self.values[1]}\n\n⭕  {self.values[2]}\n\n⭕  {self.values[3]}\n\n⭕  {self.values[4]}\n\n⭕  {self.values[5]}\n\n⦿  {self.values[6]}"

            print(f"\r{self.amountSevenFrameOne}")

            while True:
                self.key = msvcrt.getch()
                if self.key == b'\xe0':
                    self.key = msvcrt.getch()
                    if self.key == b'H':
                        if self.frame == 1:
                            self.frame = 7
                            clearLastLines()
                            print(f"\r{self.amountSevenFrameSeven}")
                        elif self.frame == 2:
                            self.frame = 1
                            clearLastLines()
                            print(f"\r{self.amountSevenFrameOne}")
                        elif self.frame == 3:
                            self.frame = 2
                            clearLastLines()
                            print(f"\r{self.amountSevenFrameTwo}")
                        elif self.frame == 4:
                            self.frame = 3
                            clearLastLines()
                            print(f"\r{self.amountSevenFrameThree}")
                        elif self.frame == 5:
                            self.frame = 4
                            clearLastLines()
                            print(f"\r{self.amountSevenFrameFour}")
                        elif self.frame == 6:
                            self.frame = 5
                            clearLastLines()
                            print(f"\r{self.amountSevenFrameFive}")
                        elif self.frame == 7:
                            self.frame = 6
                            clearLastLines()
                            print(f"\r{self.amountSevenFrameSix}")
                    elif self.key == b'P':
                        if self.frame == 1:
                            self.frame = 2
                            clearLastLines()
                            print(f"\r{self.amountSevenFrameTwo}")
                        elif self.frame == 2:
                            self.frame = 3
                            clearLastLines()
                            print(f"\r{self.amountSevenFrameThree}")
                        elif self.frame == 3:
                            self.frame = 4
                            clearLastLines()
                            print(f"\r{self.amountSevenFrameFour}")
                        elif self.frame == 4:
                            self.frame = 5
                            clearLastLines()
                            print(f"\r{self.amountSevenFrameFive}")
                        elif self.frame == 5:
                            self.frame = 6
                            clearLastLines()
                            print(f"\r{self.amountSevenFrameSix}")
                        elif self.frame == 6:
                            self.frame = 7
                            clearLastLines()
                            print(f"\r{self.amountSevenFrameSeven}")
                        elif self.frame == 7:
                            self.frame = 1
                            clearLastLines()
                            print(f"\r{self.amountSevenFrameOne}")
                elif self.continueBind == self.key.decode():
                    break

        elif self.amount == 8:
            self.number = 13
            self.frame = 1
            self.amountEightFrameOne = f"⦿  {self.values[0]}\n\n⭕  {self.values[1]}\n\n⭕  {self.values[2]}\n\n⭕  {self.values[3]}\n\n⭕  {self.values[4]}\n\n⭕  {self.values[5]}\n\n⭕  {self.values[6]}\n\n⭕  {self.values[7]}"
            self.amountEightFrameTwo = f"⭕  {self.values[0]}\n\n⦿  {self.values[1]}\n\n⭕  {self.values[2]}\n\n⭕  {self.values[3]}\n\n⭕  {self.values[4]}\n\n⭕  {self.values[5]}\n\n⭕  {self.values[6]}\n\n⭕  {self.values[7]}"
            self.amountEightFrameThree = f"⭕  {self.values[0]}\n\n⭕  {self.values[1]}\n\n⦿  {self.values[2]}\n\n⭕  {self.values[3]}\n\n⭕  {self.values[4]}\n\n⭕  {self.values[5]}\n\n⭕  {self.values[6]}\n\n⭕  {self.values[7]}"
            self.amountEightFrameFour = f"⭕  {self.values[0]}\n\n⭕  {self.values[1]}\n\n⭕  {self.values[2]}\n\n⦿  {self.values[3]}\n\n⭕  {self.values[4]}\n\n⭕  {self.values[5]}\n\n⭕  {self.values[6]}\n\n⭕  {self.values[7]}"
            self.amountEightFrameFive = f"⭕  {self.values[0]}\n\n⭕  {self.values[1]}\n\n⭕  {self.values[2]}\n\n⭕  {self.values[3]}\n\n⦿  {self.values[4]}\n\n⭕  {self.values[5]}\n\n⭕  {self.values[6]}\n\n⭕  {self.values[7]}"
            self.amountEightFrameSix = f"⭕  {self.values[0]}\n\n⭕  {self.values[1]}\n\n⭕  {self.values[2]}\n\n⭕  {self.values[3]}\n\n⭕  {self.values[4]}\n\n⦿  {self.values[5]}\n\n⭕  {self.values[6]}\n\n⭕  {self.values[7]}"
            self.amountEightFrameSeven = f"⭕  {self.values[0]}\n\n⭕  {self.values[1]}\n\n⭕  {self.values[2]}\n\n⭕  {self.values[3]}\n\n⭕  {self.values[4]}\n\n⭕  {self.values[5]}\n\n⦿  {self.values[6]}\n\n⭕  {self.values[7]}"
            self.amountEightFrameEight = f"⭕  {self.values[0]}\n\n⭕  {self.values[1]}\n\n⭕  {self.values[2]}\n\n⭕  {self.values[3]}\n\n⭕  {self.values[4]}\n\n⭕  {self.values[5]}\n\n⭕  {self.values[6]}\n\n⦿  {self.values[7]}"

            print(f"\r{self.amountEightFrameOne}")

            while True:
                self.key = msvcrt.getch()
                if self.key == b'\xe0':
                    self.key = msvcrt.getch()
                    if self.key == b'H':
                        if self.frame == 1:
                            self.frame = 8
                            clearLastLines()
                            print(f"\r{self.amountEightFrameEight}")
                        elif self.frame == 2:
                            self.frame = 1
                            clearLastLines()
                            print(f"\r{self.amountEightFrameOne}")
                        elif self.frame == 3:
                            self.frame = 2
                            clearLastLines()
                            print(f"\r{self.amountEightFrameTwo}")
                        elif self.frame == 4:
                            self.frame = 3
                            clearLastLines()
                            print(f"\r{self.amountEightFrameThree}")
                        elif self.frame == 5:
                            self.frame = 4
                            clearLastLines()
                            print(f"\r{self.amountEightFrameFour}")
                        elif self.frame == 6:
                            self.frame = 5
                            clearLastLines()
                            print(f"\r{self.amountEightFrameFive}")
                        elif self.frame == 7:
                            self.frame = 6
                            clearLastLines()
                            print(f"\r{self.amountEightFrameSix}")
                        elif self.frame == 8:
                            self.frame = 7
                            clearLastLines()
                            print(f"\r{self.amountEightFrameSeven}")
                    elif self.key == b'P':
                        if self.frame == 1:
                            self.frame = 2
                            clearLastLines()
                            print(f"\r{self.amountEightFrameTwo}")
                        elif self.frame == 2:
                            self.frame = 3
                            clearLastLines()
                            print(f"\r{self.amountEightFrameThree}")
                        elif self.frame == 3:
                            self.frame = 4
                            clearLastLines()
                            print(f"\r{self.amountEightFrameFour}")
                        elif self.frame == 4:
                            self.frame = 5
                            clearLastLines()
                            print(f"\r{self.amountEightFrameFive}")
                        elif self.frame == 5:
                            self.frame = 6
                            clearLastLines()
                            print(f"\r{self.amountEightFrameSix}")
                        elif self.frame == 6:
                            self.frame = 7
                            clearLastLines()
                            print(f"\r{self.amountEightFrameSeven}")
                        elif self.frame == 7:
                            self.frame = 8
                            clearLastLines()
                            print(f"\r{self.amountEightFrameEight}")
                        elif self.frame == 8:
                            self.frame = 1
                            clearLastLines()
                            print(f"\r{self.amountEightFrameOne}")
                elif self.continueBind == self.key.decode():
                    break

        elif self.amount == 9:
            self.number = 15
            self.frame = 1
            self.amountNineFrameOne = f"⦿  {self.values[0]}\n\n⭕  {self.values[1]}\n\n⭕  {self.values[2]}\n\n⭕  {self.values[3]}\n\n⭕  {self.values[4]}\n\n⭕  {self.values[5]}\n\n⭕  {self.values[6]}\n\n⭕  {self.values[7]}\n\n⭕  {self.values[8]}"
            self.amountNineFrameTwo = f"⭕  {self.values[0]}\n\n⦿  {self.values[1]}\n\n⭕  {self.values[2]}\n\n⭕  {self.values[3]}\n\n⭕  {self.values[4]}\n\n⭕  {self.values[5]}\n\n⭕  {self.values[6]}\n\n⭕  {self.values[7]}\n\n⭕  {self.values[8]}"
            self.amountNineFrameThree = f"⭕  {self.values[0]}\n\n⭕  {self.values[1]}\n\n⦿  {self.values[2]}\n\n⭕  {self.values[3]}\n\n⭕  {self.values[4]}\n\n⭕  {self.values[5]}\n\n⭕  {self.values[6]}\n\n⭕  {self.values[7]}\n\n⭕  {self.values[8]}"
            self.amountNineFrameFour = f"⭕  {self.values[0]}\n\n⭕  {self.values[1]}\n\n⭕  {self.values[2]}\n\n⦿  {self.values[3]}\n\n⭕  {self.values[4]}\n\n⭕  {self.values[5]}\n\n⭕  {self.values[6]}\n\n⭕  {self.values[7]}\n\n⭕  {self.values[8]}"
            self.amountNineFrameFive = f"⭕  {self.values[0]}\n\n⭕  {self.values[1]}\n\n⭕  {self.values[2]}\n\n⭕  {self.values[3]}\n\n⦿  {self.values[4]}\n\n⭕  {self.values[5]}\n\n⭕  {self.values[6]}\n\n⭕  {self.values[7]}\n\n⭕  {self.values[8]}"
            self.amountNineFrameSix = f"⭕  {self.values[0]}\n\n⭕  {self.values[1]}\n\n⭕  {self.values[2]}\n\n⭕  {self.values[3]}\n\n⭕  {self.values[4]}\n\n⦿  {self.values[5]}\n\n⭕  {self.values[6]}\n\n⭕  {self.values[7]}\n\n⭕  {self.values[8]}"
            self.amountNineFrameSeven = f"⭕  {self.values[0]}\n\n⭕  {self.values[1]}\n\n⭕  {self.values[2]}\n\n⭕  {self.values[3]}\n\n⭕  {self.values[4]}\n\n⭕  {self.values[5]}\n\n⦿  {self.values[6]}\n\n⭕  {self.values[7]}\n\n⭕  {self.values[8]}"
            self.amountNineFrameEight = f"⭕  {self.values[0]}\n\n⭕  {self.values[1]}\n\n⭕  {self.values[2]}\n\n⭕  {self.values[3]}\n\n⭕  {self.values[4]}\n\n⭕  {self.values[5]}\n\n⭕  {self.values[6]}\n\n⦿  {self.values[7]}\n\n⭕  {self.values[8]}"
            self.amountNineFrameNine = f"⭕  {self.values[0]}\n\n⭕  {self.values[1]}\n\n⭕  {self.values[2]}\n\n⭕  {self.values[3]}\n\n⭕  {self.values[4]}\n\n⭕  {self.values[5]}\n\n⭕  {self.values[6]}\n\n⭕  {self.values[7]}\n\n⦿  {self.values[8]}"

            print(f"\r{self.amountNineFrameOne}")

            while True:
                self.key = msvcrt.getch()
                if self.key == b'\xe0':
                    self.key = msvcrt.getch()
                    if self.key == b'H':
                        if self.frame == 1:
                            self.frame = 9
                            clearLastLines()
                            print(f"\r{self.amountNineFrameNine}")
                        elif self.frame == 2:
                            self.frame = 1
                            clearLastLines()
                            print(f"\r{self.amountNineFrameOne}")
                        elif self.frame == 3:
                            self.frame = 2
                            clearLastLines()
                            print(f"\r{self.amountNineFrameTwo}")
                        elif self.frame == 4:
                            self.frame = 3
                            clearLastLines()
                            print(f"\r{self.amountNineFrameThree}")
                        elif self.frame == 5:
                            self.frame = 4
                            clearLastLines()
                            print(f"\r{self.amountNineFrameFour}")
                        elif self.frame == 6:
                            self.frame = 5
                            clearLastLines()
                            print(f"\r{self.amountNineFrameFive}")
                        elif self.frame == 7:
                            self.frame = 6
                            clearLastLines()
                            print(f"\r{self.amountNineFrameSix}")
                        elif self.frame == 8:
                            self.frame = 7
                            clearLastLines()
                            print(f"\r{self.amountNineFrameSeven}")
                        elif self.frame == 9:
                            self.frame = 8
                            clearLastLines()
                            print(f"\r{self.amountNineFrameEight}")
                    elif self.key == b'P':
                        if self.frame == 1:
                            self.frame = 2
                            clearLastLines()
                            print(f"\r{self.amountNineFrameTwo}")
                        elif self.frame == 2:
                            self.frame = 3
                            clearLastLines()
                            print(f"\r{self.amountNineFrameThree}")
                        elif self.frame == 3:
                            self.frame = 4
                            clearLastLines()
                            print(f"\r{self.amountNineFrameFour}")
                        elif self.frame == 4:
                            self.frame = 5
                            clearLastLines()
                            print(f"\r{self.amountNineFrameFive}")
                        elif self.frame == 5:
                            self.frame = 6
                            clearLastLines()
                            print(f"\r{self.amountNineFrameSix}")
                        elif self.frame == 6:
                            self.frame = 7
                            clearLastLines()
                            print(f"\r{self.amountNineFrameSeven}")
                        elif self.frame == 7:
                            self.frame = 8
                            clearLastLines()
                            print(f"\r{self.amountNineFrameEight}")
                        elif self.frame == 8:
                            self.frame = 9
                            clearLastLines()
                            print(f"\r{self.amountNineFrameNine}")
                        elif self.frame == 9:
                            self.frame = 1
                            clearLastLines()
                            print(f"\r{self.amountNineFrameOne}")
                elif self.continueBind == self.key.decode():
                    break

        elif self.amount == 10:
            self.number = 17
            self.frame = 1
            self.amountTenFrameOne = f"⦿  {self.values[0]}\n\n⭕  {self.values[1]}\n\n⭕  {self.values[2]}\n\n⭕  {self.values[3]}\n\n⭕  {self.values[4]}\n\n⭕  {self.values[5]}\n\n⭕  {self.values[6]}\n\n⭕  {self.values[7]}\n\n⭕  {self.values[8]}\n\n⭕  {self.values[9]}"
            self.amountTenFrameTwo = f"⭕  {self.values[0]}\n\n⦿  {self.values[1]}\n\n⭕  {self.values[2]}\n\n⭕  {self.values[3]}\n\n⭕  {self.values[4]}\n\n⭕  {self.values[5]}\n\n⭕  {self.values[6]}\n\n⭕  {self.values[7]}\n\n⭕  {self.values[8]}\n\n⭕  {self.values[9]}"
            self.amountTenFrameThree = f"⭕  {self.values[0]}\n\n⭕  {self.values[1]}\n\n⦿  {self.values[2]}\n\n⭕  {self.values[3]}\n\n⭕  {self.values[4]}\n\n⭕  {self.values[5]}\n\n⭕  {self.values[6]}\n\n⭕  {self.values[7]}\n\n⭕  {self.values[8]}\n\n⭕  {self.values[9]}"
            self.amountTenFrameFour = f"⭕  {self.values[0]}\n\n⭕  {self.values[1]}\n\n⭕  {self.values[2]}\n\n⦿  {self.values[3]}\n\n⭕  {self.values[4]}\n\n⭕  {self.values[5]}\n\n⭕  {self.values[6]}\n\n⭕  {self.values[7]}\n\n⭕  {self.values[8]}\n\n⭕  {self.values[9]}"
            self.amountTenFrameFive = f"⭕  {self.values[0]}\n\n⭕  {self.values[1]}\n\n⭕  {self.values[2]}\n\n⭕  {self.values[3]}\n\n⦿  {self.values[4]}\n\n⭕  {self.values[5]}\n\n⭕  {self.values[6]}\n\n⭕  {self.values[7]}\n\n⭕  {self.values[8]}\n\n⭕  {self.values[9]}"
            self.amountTenFrameSix = f"⭕  {self.values[0]}\n\n⭕  {self.values[1]}\n\n⭕  {self.values[2]}\n\n⭕  {self.values[3]}\n\n⭕  {self.values[4]}\n\n⦿  {self.values[5]}\n\n⭕  {self.values[6]}\n\n⭕  {self.values[7]}\n\n⭕  {self.values[8]}\n\n⭕  {self.values[9]}"
            self.amountTenFrameSeven = f"⭕  {self.values[0]}\n\n⭕  {self.values[1]}\n\n⭕  {self.values[2]}\n\n⭕  {self.values[3]}\n\n⭕  {self.values[4]}\n\n⭕  {self.values[5]}\n\n⦿  {self.values[6]}\n\n⭕  {self.values[7]}\n\n⭕  {self.values[8]}\n\n⭕  {self.values[9]}"
            self.amountTenFrameEight = f"⭕  {self.values[0]}\n\n⭕  {self.values[1]}\n\n⭕  {self.values[2]}\n\n⭕  {self.values[3]}\n\n⭕  {self.values[4]}\n\n⭕  {self.values[5]}\n\n⭕  {self.values[6]}\n\n⦿  {self.values[7]}\n\n⭕  {self.values[8]}\n\n⭕  {self.values[9]}"
            self.amountTenFrameNine = f"⭕  {self.values[0]}\n\n⭕  {self.values[1]}\n\n⭕  {self.values[2]}\n\n⭕  {self.values[3]}\n\n⭕  {self.values[4]}\n\n⭕  {self.values[5]}\n\n⭕  {self.values[6]}\n\n⭕  {self.values[7]}\n\n⦿  {self.values[8]}\n\n⭕  {self.values[9]}"
            self.amountTenFrameTen = f"⭕  {self.values[0]}\n\n⭕  {self.values[1]}\n\n⭕  {self.values[2]}\n\n⭕  {self.values[3]}\n\n⭕  {self.values[4]}\n\n⭕  {self.values[5]}\n\n⭕  {self.values[6]}\n\n⭕  {self.values[7]}\n\n⭕  {self.values[8]}\n\n⦿  {self.values[9]}"

            print(f"\r{self.amountTenFrameOne}")

            while True:
                self.key = msvcrt.getch()
                if self.key == b'\xe0':
                    self.key = msvcrt.getch()
                    if self.key == b'H':
                        if self.frame == 1:
                            self.frame = 10
                            clearLastLines()
                            print(f"\r{self.amountTenFrameTen}")
                        elif self.frame == 2:
                            self.frame = 1
                            clearLastLines()
                            print(f"\r{self.amountTenFrameOne}")
                        elif self.frame == 3:
                            self.frame = 2
                            clearLastLines()
                            print(f"\r{self.amountTenFrameTwo}")
                        elif self.frame == 4:
                            self.frame = 3
                            clearLastLines()
                            print(f"\r{self.amountTenFrameThree}")
                        elif self.frame == 5:
                            self.frame = 4
                            clearLastLines()
                            print(f"\r{self.amountTenFrameFour}")
                        elif self.frame == 6:
                            self.frame = 5
                            clearLastLines()
                            print(f"\r{self.amountTenFrameFive}")
                        elif self.frame == 7:
                            self.frame = 6
                            clearLastLines()
                            print(f"\r{self.amountTenFrameSix}")
                        elif self.frame == 8:
                            self.frame = 7
                            clearLastLines()
                            print(f"\r{self.amountTenFrameSeven}")
                        elif self.frame == 9:
                            self.frame = 8
                            clearLastLines()
                            print(f"\r{self.amountTenFrameEight}")
                        elif self.frame == 10:
                            self.frame = 9
                            clearLastLines()
                            print(f"\r{self.amountTenFrameNine}")
                    elif self.key == b'P':
                        if self.frame == 1:
                            self.frame = 2
                            clearLastLines()
                            print(f"\r{self.amountTenFrameTwo}")
                        elif self.frame == 2:
                            self.frame = 3
                            clearLastLines()
                            print(f"\r{self.amountTenFrameThree}")
                        elif self.frame == 3:
                            self.frame = 4
                            clearLastLines()
                            print(f"\r{self.amountTenFrameFour}")
                        elif self.frame == 4:
                            self.frame = 5
                            clearLastLines()
                            print(f"\r{self.amountTenFrameFive}")
                        elif self.frame == 5:
                            self.frame = 6
                            clearLastLines()
                            print(f"\r{self.amountTenFrameSix}")
                        elif self.frame == 6:
                            self.frame = 7
                            clearLastLines()
                            print(f"\r{self.amountTenFrameSeven}")
                        elif self.frame == 7:
                            self.frame = 8
                            clearLastLines()
                            print(f"\r{self.amountTenFrameEight}")
                        elif self.frame == 8:
                            self.frame = 9
                            clearLastLines()
                            print(f"\r{self.amountTenFrameNine}")
                        elif self.frame == 9:
                            self.frame = 10
                            clearLastLines()
                            print(f"\r{self.amountTenFrameTen}")
                        elif self.frame == 10:
                            self.frame = 1
                            clearLastLines()
                            print(f"\r{self.amountTenFrameOne}")
                elif self.continueBind == self.key.decode():
                    break

    def get(self):
        return (self.frame - 1)
