class CMDEllipse:
    def __init__(self, *, width: int, height: int, color: str='#ffffff', hollow: bool):
        self.width = width
        self.height = height
        self.hollow = hollow
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

        if not self.hollow:
            for y in range(-self.height, self.height + 1):
                for x in range(-self.width, self.width + 1):
                    if (x / self.width) ** 2 + (y / self.height) ** 2 <= 1:
                        print("██", end="")
                    else:
                        print("  ", end="")
                print()

        elif self.hollow:
            for y in range(-self.height, self.height + 1):
                for x in range(-self.width, self.width + 1):
                    self.distance = ((x / self.width) ** 2 + (y / self.height) ** 2) ** 0.5
                    if abs(self.distance - 1) < 0.05:
                        print("██", end="")
                    else:
                        print("  ", end="")
                print()
        print(asciiReset)
