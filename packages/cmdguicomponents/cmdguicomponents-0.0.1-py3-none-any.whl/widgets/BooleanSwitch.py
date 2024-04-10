import msvcrt

class CMDBooleanSwitch:
    def __init__(self, *, style: str, continueBind: str, color: str='#ffffff'):
        self.value = False
        self.style = style
        self.continueBind = continueBind
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

        def clearLastLines():
            for _ in range(3):
                print("\033[F\033[K", end="")

        self.frames = {
            "tf": {
                "0": {
                    "1": "╷───────╷______ ",
                    "2": "│ False │ True │",
                    "3": "╵───────╵‾‾‾‾‾‾ "
                },
                "1": {
                    "1": " _______╷──────╷",
                    "2": "│ False │ True │",
                    "3": " ‾‾‾‾‾‾‾╵──────╵"
                }
            },
            "yn": {
                "0": {
                    "1": "╷────╷_____ ",
                    "2": "│ No │ Yes │",
                    "3": "╵────╵‾‾‾‾‾ "
                },
                "1": {
                    "1": " ____╷─────╷",
                    "2": "│ No │ Yes │",
                    "3": " ‾‾‾‾╵─────╵"
                }
            },
            "pn": {
                "0": {
                    "1": "╷──────────╷__________ ",
                    "2": "│ Negative │ Positive │",
                    "3": "╵──────────╵‾‾‾‾‾‾‾‾‾‾ "
                },
                "1": {
                    "1": " __________╷──────────╷",
                    "2": "│ Negative │ Positive │",
                    "3": " ‾‾‾‾‾‾‾‾‾‾╵──────────╵"
                }
            },
            "ad": {
                "0": {
                    "1": "╷─────────╷________ ",
                    "2": "│ Decline │ Accept │",
                    "3": "╵─────────╵‾‾‾‾‾‾‾‾ "
                },
                "1": {
                    "1": " ________╷─────────╷",
                    "2": "│ Accept │ Decline │",
                    "3": " ‾‾‾‾‾‾‾‾╵─────────╵"
                }
            },
            "ar": {
                "0": {
                    "1": "╷────────╷_______ ",
                    "2": "│ Reject │ Allow │",
                    "3": "╵────────╵‾‾‾‾‾‾‾ "
                },
                "1": {
                    "1": " ________╷───────╷",
                    "2": "│ Reject │ Allow │",
                    "3": " ‾‾‾‾‾‾‾‾╵───────╵"
                }
            }
        }

        if self.style == 'trueFalse':
            print(f"\r{self.frames['tf']['0']['1']}")
            print(f"\r{self.frames['tf']['0']['2']}")
            print(f"\r{self.frames['tf']['0']['3']}")
            while True:
                self.key = msvcrt.getch()
                if self.key == b'\xe0':
                    self.key = msvcrt.getch()
                    if self.key == b'M':  # right
                        self.value = True
                        clearLastLines()
                        print(f"\r{self.frames['tf']['1']['1']}")
                        print(f"\r{self.frames['tf']['1']['2']}")
                        print(f"\r{self.frames['tf']['1']['3']}")

                    elif self.key == b'K':  # left
                        self.value = False
                        clearLastLines()
                        print(f"\r{self.frames['tf']['0']['1']}")
                        print(f"\r{self.frames['tf']['0']['2']}")
                        print(f"\r{self.frames['tf']['0']['3']}")

                elif self.continueBind == self.key.decode():
                    break

        elif self.style == 'yesNo':
            print(f"\r{self.frames['yn']['0']['1']}")
            print(f"\r{self.frames['yn']['0']['2']}")
            print(f"\r{self.frames['yn']['0']['3']}")
            while True:
                self.key = msvcrt.getch()
                if self.key == b'\xe0':
                    self.key = msvcrt.getch()
                    if self.key == b'M':  # right
                        self.value = True
                        clearLastLines()
                        print(f"\r{self.frames['yn']['1']['1']}")
                        print(f"\r{self.frames['yn']['1']['2']}")
                        print(f"\r{self.frames['yn']['1']['3']}")

                    elif self.key == b'K':  # left
                        self.value = False
                        clearLastLines()
                        print(f"\r{self.frames['yn']['0']['1']}")
                        print(f"\r{self.frames['yn']['0']['2']}")
                        print(f"\r{self.frames['yn']['0']['3']}")

                elif self.continueBind == self.key.decode():
                    break

        elif self.style == 'positiveNegative':
            print(f"\r{self.frames['pn']['0']['1']}")
            print(f"\r{self.frames['pn']['0']['2']}")
            print(f"\r{self.frames['pn']['0']['3']}")
            while True:
                self.key = msvcrt.getch()
                if self.key == b'\xe0':
                    self.key = msvcrt.getch()
                    if self.key == b'M':  # right
                        self.value = True
                        clearLastLines()
                        print(f"\r{self.frames['pn']['1']['1']}")
                        print(f"\r{self.frames['pn']['1']['2']}")
                        print(f"\r{self.frames['pn']['1']['3']}")

                    elif self.key == b'K':  # left
                        self.value = False
                        clearLastLines()
                        print(f"\r{self.frames['pn']['0']['1']}")
                        print(f"\r{self.frames['pn']['0']['2']}")
                        print(f"\r{self.frames['pn']['0']['3']}")

                elif self.continueBind == self.key.decode():
                    break

        elif self.style == 'acceptDecline':
            print(f"\r{self.frames['ad']['0']['1']}")
            print(f"\r{self.frames['ad']['0']['2']}")
            print(f"\r{self.frames['ad']['0']['3']}")
            while True:
                self.key = msvcrt.getch()
                if self.key == b'\xe0':
                    self.key = msvcrt.getch()
                    if self.key == b'M':  # right
                        self.value = True
                        clearLastLines()
                        print(f"\r{self.frames['ad']['1']['1']}")
                        print(f"\r{self.frames['ad']['1']['2']}")
                        print(f"\r{self.frames['ad']['1']['3']}")

                    elif self.key == b'K':  # left
                        self.value = False
                        clearLastLines()
                        print(f"\r{self.frames['ad']['0']['1']}")
                        print(f"\r{self.frames['ad']['0']['2']}")
                        print(f"\r{self.frames['ad']['0']['3']}")

                elif self.continueBind == self.key.decode():
                    break

        elif self.style == 'allowReject':
            print(f"\r{self.frames['ar']['0']['1']}")
            print(f"\r{self.frames['ar']['0']['2']}")
            print(f"\r{self.frames['ar']['0']['3']}")
            while True:
                self.key = msvcrt.getch()
                if self.key == b'\xe0':
                    self.key = msvcrt.getch()
                    if self.key == b'M':  # right
                        self.value = True
                        clearLastLines()
                        print(f"\r{self.frames['ar']['1']['1']}")
                        print(f"\r{self.frames['ar']['1']['2']}")
                        print(f"\r{self.frames['ar']['1']['3']}")

                    elif self.key == b'K':  # left
                        self.value = False
                        clearLastLines()
                        print(f"\r{self.frames['ar']['0']['1']}")
                        print(f"\r{self.frames['ar']['0']['2']}")
                        print(f"\r{self.frames['ar']['0']['3']}")

                elif self.continueBind == self.key.decode():
                    break

    def get(self):
        return self.value
