import msvcrt

class CMDSlider:
	def __init__(self, *, length: int, continueBind: str, color: str='#ffffff'):
		self.value = 1
		self.length = length
		self.continueBind = continueBind
		def clearLastLines():
			for _ in range(2):
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

		self.frames = {
			"2": {
				"1": {
					"1": "╷╭╮_╷",
					"2": "╵╰╯‾╵"
				},
				"2": {
					"1": "╷_╭╮╷",
					"2": "╵‾╰╯╵"
				}
			},
			"3": {
				"1": {
					"1": "╷╭╮__╷",
					"2": "╵╰╯‾‾╵"
				},
				"2": {
					"1": "╷_╭╮_╷",
					"2": "╵‾╰╯‾╵"
				},
				"3": {
					"1": "╷__╭╮╷",
					"2": "╵‾‾╰╯╵"
				}
			},
			"4": {
				"1": {
					"1": "╷╭╮___╷",
					"2": "╵╰╯‾‾‾╵"
				},
				"2": {
					"1": "╷_╭╮__╷",
					"2": "╵‾╰╯‾‾╵"
				},
				"3": {
					"1": "╷__╭╮_╷",
					"2": "╵‾‾╰╯‾╵"
				},
				"4": {
					"1": "╷___╭╮╷",
					"2": "╵‾‾‾╰╯╵"
				}
			},
			"5": {
				"1": {
					"1": "╷╭╮____╷",
					"2": "╵╰╯‾‾‾‾╵"
				},
				"2": {
					"1": "╷_╭╮___╷",
					"2": "╵‾╰╯‾‾‾╵"
				},
				"3": {
					"1": "╷__╭╮__╷",
					"2": "╵‾‾╰╯‾‾╵"
				},
				"4": {
					"1": "╷___╭╮_╷",
					"2": "╵‾‾‾╰╯‾╵"
				},
				"5": {
					"1": "╷____╭╮╷",
					"2": "╵‾‾‾‾╰╯╵"
				}
			},
			"6": {
				"1": {
					"1": "╷╭╮_____╷",
					"2": "╵╰╯‾‾‾‾‾╵"
				},
				"2": {
					"1": "╷_╭╮____╷",
					"2": "╵‾╰╯‾‾‾‾╵"
				},
				"3": {
					"1": "╷__╭╮___╷",
					"2": "╵‾‾╰╯‾‾‾╵"
				},
				"4": {
					"1": "╷___╭╮__╷",
					"2": "╵‾‾‾╰╯‾‾╵"
				},
				"5": {
					"1": "╷____╭╮_╷",
					"2": "╵‾‾‾‾╰╯‾╵"
				},
				"6": {
					"1": "╷_____╭╮╷",
					"2": "╵‾‾‾‾‾╰╯╵"
				}
			},
			"7": {
				"1": {
					"1": "╷╭╮______╷",
					"2": "╵╰╯‾‾‾‾‾‾╵"
				},
				"2": {
					"1": "╷_╭╮_____╷",
					"2": "╵‾╰╯‾‾‾‾‾╵"
				},
				"3": {
					"1": "╷__╭╮____╷",
					"2": "╵‾‾╰╯‾‾‾‾╵"
				},
				"4": {
					"1": "╷___╭╮___╷",
					"2": "╵‾‾‾╰╯‾‾‾╵"
				},
				"5": {
					"1": "╷____╭╮__╷",
					"2": "╵‾‾‾‾╰╯‾‾╵"
				},
				"6": {
					"1": "╷_____╭╮_╷",
					"2": "╵‾‾‾‾‾╰╯‾╵"
				},
				"7": {
					"1": "╷______╭╮╷",
					"2": "╵‾‾‾‾‾‾╰╯╵"
				}
			},
			"8": {
				"1": {
					"1": "╷╭╮_______╷",
					"2": "╵╰╯‾‾‾‾‾‾‾╵"
				},
				"2": {
					"1": "╷_╭╮______╷",
					"2": "╵‾╰╯‾‾‾‾‾‾╵"
				},
				"3": {
					"1": "╷__╭╮_____╷",
					"2": "╵‾‾╰╯‾‾‾‾‾╵"
				},
				"4": {
					"1": "╷___╭╮____╷",
					"2": "╵‾‾‾╰╯‾‾‾‾╵"
				},
				"5": {
					"1": "╷____╭╮___╷",
					"2": "╵‾‾‾‾╰╯‾‾‾╵"
				},
				"6": {
					"1": "╷_____╭╮__╷",
					"2": "╵‾‾‾‾‾╰╯‾‾╵"
				},
				"7": {
					"1": "╷______╭╮_╷",
					"2": "╵‾‾‾‾‾‾╰╯‾╵"
				},
				"8": {
					"1": "╷_______╭╮╷",
					"2": "╵‾‾‾‾‾‾‾╰╯╵"
				}
			},
			"9": {
				"1": {
					"1": "╷╭╮________╷",
					"2": "╵╰╯‾‾‾‾‾‾‾‾╵"
				},
				"2": {
					"1": "╷_╭╮_______╷",
					"2": "╵‾╰╯‾‾‾‾‾‾‾╵"
				},
				"3": {
					"1": "╷__╭╮______╷",
					"2": "╵‾‾╰╯‾‾‾‾‾‾╵"
				},
				"4": {
					"1": "╷___╭╮_____╷",
					"2": "╵‾‾‾╰╯‾‾‾‾‾╵"
				},
				"5": {
					"1": "╷____╭╮____╷",
					"2": "╵‾‾‾‾╰╯‾‾‾‾╵"
				},
				"6": {
					"1": "╷_____╭╮___╷",
					"2": "╵‾‾‾‾‾╰╯‾‾‾╵"
				},
				"7": {
					"1": "╷______╭╮__╷",
					"2": "╵‾‾‾‾‾‾╰╯‾‾╵"
				},
				"8": {
					"1": "╷_______╭╮_╷",
					"2": "╵‾‾‾‾‾‾‾╰╯‾╵"
				},
				"9": {
					"1": "╷________╭╮╷",
					"2": "╵‾‾‾‾‾‾‾‾╰╯╵"
				}
			},
			"10": {
				"1": {
					"1": "╷╭╮_________╷",
					"2": "╵╰╯‾‾‾‾‾‾‾‾‾╵"
				},
				"2": {
					"1": "╷_╭╮________╷",
					"2": "╵‾╰╯‾‾‾‾‾‾‾‾╵"
				},
				"3": {
					"1": "╷__╭╮_______╷",
					"2": "╵‾‾╰╯‾‾‾‾‾‾‾╵"
				},
				"4": {
					"1": "╷___╭╮______╷",
					"2": "╵‾‾‾╰╯‾‾‾‾‾‾╵"
				},
				"5": {
					"1": "╷____╭╮_____╷",
					"2": "╵‾‾‾‾╰╯‾‾‾‾‾╵"
				},
				"6": {
					"1": "╷_____╭╮____╷",
					"2": "╵‾‾‾‾‾╰╯‾‾‾‾╵"
				},
				"7": {
					"1": "╷______╭╮___╷",
					"2": "╵‾‾‾‾‾‾╰╯‾‾‾╵"
				},
				"8": {
					"1": "╷_______╭╮__╷",
					"2": "╵‾‾‾‾‾‾‾╰╯‾‾╵"
				},
				"9": {
					"1": "╷________╭╮_╷",
					"2": "╵‾‾‾‾‾‾‾‾╰╯‾╵"
				},
				"10": {
					"1": "╷_________╭╮╷",
					"2": "╵‾‾‾‾‾‾‾‾‾╰╯╵"
				}
			}
		}

		if self.length == 0 or self.length == 1 or self.length > 10:
			print("Length cannot be lower than 2 or higher than 10!")
			exit()

		elif self.length == 2:
		    self.frame = 1
		    clearLastLines()
		    print(f"\r{self.frames['2']['1']['1']}")
		    print(f"\r{self.frames['2']['1']['2']}")

		    while True:
		        self.key = msvcrt.getch()
		        if self.key == b'\xe0':
		            self.key = msvcrt.getch()
		            if self.key == b'M':  # right
		                if self.frame == 1:
		                    self.frame = 2
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['2']['2']['1']}")
		                    print(f"\r{self.frames['2']['2']['2']}")
		                elif self.frame == 2:
		                    self.frame = 2
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['2']['2']['1']}")
		                    print(f"\r{self.frames['2']['2']['2']}")
		            elif self.key == b'K':  # left
		                if self.frame == 1:
		                    self.frame = 1
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['2']['1']['1']}")
		                    print(f"\r{self.frames['2']['1']['2']}")
		                elif self.frame == 2:
		                    self.frame = 1
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['2']['1']['1']}")
		                    print(f"\r{self.frames['2']['1']['2']}")
		        elif self.continueBind == self.key.decode():
		            break

		elif self.length == 3:
		    self.frame = 1
		    clearLastLines()
		    print(f"\r{self.frames['3']['1']['1']}")
		    print(f"\r{self.frames['3']['1']['2']}")

		    while True:
		        self.key = msvcrt.getch()
		        if self.key == b'\xe0':
		            self.key = msvcrt.getch()
		            if self.key == b'M':  # right
		                if self.frame == 1:
		                    self.frame = 2
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['3']['2']['1']}")
		                    print(f"\r{self.frames['3']['2']['2']}")
		                elif self.frame == 2:
		                    self.frame = 3
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['3']['3']['1']}")
		                    print(f"\r{self.frames['3']['3']['2']}")
		                elif self.frame == 3:
		                    self.frame = 3
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['3']['3']['1']}")
		                    print(f"\r{self.frames['3']['3']['2']}")
		            elif self.key == b'K':  # left
		                if self.frame == 1:
		                    self.frame = 1
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['3']['1']['1']}")
		                    print(f"\r{self.frames['3']['1']['2']}")
		                elif self.frame == 2:
		                    self.frame = 1
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['3']['1']['1']}")
		                    print(f"\r{self.frames['3']['1']['2']}")
		                elif self.frame == 3:
		                    self.frame = 2
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['3']['2']['1']}")
		                    print(f"\r{self.frames['3']['2']['2']}")
		        elif self.continueBind == self.key.decode():
		            break

		elif self.length == 4:
		    self.frame = 1
		    clearLastLines()
		    print(f"\r{self.frames['4']['1']['1']}")
		    print(f"\r{self.frames['4']['1']['2']}")

		    while True:
		        self.key = msvcrt.getch()
		        if self.key == b'\xe0':
		            self.key = msvcrt.getch()
		            if self.key == b'M':  # right
		                if self.frame == 1:
		                    self.frame = 2
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['4']['2']['1']}")
		                    print(f"\r{self.frames['4']['2']['2']}")
		                elif self.frame == 2:
		                    self.frame = 3
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['4']['3']['1']}")
		                    print(f"\r{self.frames['4']['3']['2']}")
		                elif self.frame == 3:
		                    self.frame = 4
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['4']['4']['1']}")
		                    print(f"\r{self.frames['4']['4']['2']}")
		                elif self.frame == 4:
		                    self.frame = 4
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['4']['4']['1']}")
		                    print(f"\r{self.frames['4']['4']['2']}")
		            elif self.key == b'K':  # left
		                if self.frame == 1:
		                    self.frame = 1
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['4']['1']['1']}")
		                    print(f"\r{self.frames['4']['1']['2']}")
		                elif self.frame == 2:
		                    self.frame = 1
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['4']['1']['1']}")
		                    print(f"\r{self.frames['4']['1']['2']}")
		                elif self.frame == 3:
		                    self.frame = 2
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['4']['2']['1']}")
		                    print(f"\r{self.frames['4']['2']['2']}")
		                elif self.frame == 4:
		                    self.frame = 3
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['4']['3']['1']}")
		                    print(f"\r{self.frames['4']['3']['2']}")
		        elif self.continueBind == self.key.decode():
		            break


		elif self.length == 5:
		    self.frame = 1
		    clearLastLines()
		    print(f"\r{self.frames['5']['1']['1']}")
		    print(f"\r{self.frames['5']['1']['2']}")

		    while True:
		        self.key = msvcrt.getch()
		        if self.key == b'\xe0':
		            self.key = msvcrt.getch()
		            if self.key == b'M':  # right
		                if self.frame == 1:
		                    self.frame = 2
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['5']['2']['1']}")
		                    print(f"\r{self.frames['5']['2']['2']}")
		                elif self.frame == 2:
		                    self.frame = 3
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['5']['3']['1']}")
		                    print(f"\r{self.frames['5']['3']['2']}")
		                elif self.frame == 3:
		                    self.frame = 4
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['5']['4']['1']}")
		                    print(f"\r{self.frames['5']['4']['2']}")
		                elif self.frame == 4:
		                    self.frame = 5
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['5']['5']['1']}")
		                    print(f"\r{self.frames['5']['5']['2']}")
		                elif self.frame == 5:
		                    self.frame = 5
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['5']['5']['1']}")
		                    print(f"\r{self.frames['5']['5']['2']}")
		            elif self.key == b'K':  # left
		                if self.frame == 1:
		                    self.frame = 1
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['5']['1']['1']}")
		                    print(f"\r{self.frames['5']['1']['2']}")
		                elif self.frame == 2:
		                    self.frame = 1
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['5']['1']['1']}")
		                    print(f"\r{self.frames['5']['1']['2']}")
		                elif self.frame == 3:
		                    self.frame = 2
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['5']['2']['1']}")
		                    print(f"\r{self.frames['5']['2']['2']}")
		                elif self.frame == 4:
		                    self.frame = 3
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['5']['3']['1']}")
		                    print(f"\r{self.frames['5']['3']['2']}")
		                elif self.frame == 5:
		                    self.frame = 4
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['5']['4']['1']}")
		                    print(f"\r{self.frames['5']['4']['2']}")
		        elif self.continueBind == self.key.decode():
		            break

		elif self.length == 6:
		    self.frame = 1
		    clearLastLines()
		    print(f"\r{self.frames['6']['1']['1']}")
		    print(f"\r{self.frames['6']['1']['2']}")

		    while True:
		        self.key = msvcrt.getch()
		        if self.key == b'\xe0':
		            self.key = msvcrt.getch()
		            if self.key == b'M':  # right
		                if self.frame == 1:
		                    self.frame = 2
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['6']['2']['1']}")
		                    print(f"\r{self.frames['6']['2']['2']}")
		                elif self.frame == 2:
		                    self.frame = 3
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['6']['3']['1']}")
		                    print(f"\r{self.frames['6']['3']['2']}")
		                elif self.frame == 3:
		                    self.frame = 4
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['6']['4']['1']}")
		                    print(f"\r{self.frames['6']['4']['2']}")
		                elif self.frame == 4:
		                    self.frame = 5
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['6']['5']['1']}")
		                    print(f"\r{self.frames['6']['5']['2']}")
		                elif self.frame == 5:
		                    self.frame = 6
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['6']['6']['1']}")
		                    print(f"\r{self.frames['6']['6']['2']}")
		                elif self.frame == 6:
		                    self.frame = 6
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['6']['6']['1']}")
		                    print(f"\r{self.frames['6']['6']['2']}")
		            elif self.key == b'K':  # left
		                if self.frame == 1:
		                    self.frame = 1
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['6']['1']['1']}")
		                    print(f"\r{self.frames['6']['1']['2']}")
		                elif self.frame == 2:
		                    self.frame = 1
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['6']['1']['1']}")
		                    print(f"\r{self.frames['6']['1']['2']}")
		                elif self.frame == 3:
		                    self.frame = 2
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['6']['2']['1']}")
		                    print(f"\r{self.frames['6']['2']['2']}")
		                elif self.frame == 4:
		                    self.frame = 3
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['6']['3']['1']}")
		                    print(f"\r{self.frames['6']['3']['2']}")
		                elif self.frame == 5:
		                    self.frame = 4
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['6']['4']['1']}")
		                    print(f"\r{self.frames['6']['4']['2']}")
		                elif self.frame == 6:
		                    self.frame = 5
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['6']['5']['1']}")
		                    print(f"\r{self.frames['6']['5']['2']}")
		        elif self.continueBind == self.key.decode():
		            break

		elif self.length == 7:
		    self.frame = 1
		    clearLastLines()
		    print(f"\r{self.frames['7']['1']['1']}")
		    print(f"\r{self.frames['7']['1']['2']}")

		    while True:
		        self.key = msvcrt.getch()
		        if self.key == b'\xe0':
		            self.key = msvcrt.getch()
		            if self.key == b'M':  # right
		                if self.frame == 1:
		                    self.frame = 2
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['7']['2']['1']}")
		                    print(f"\r{self.frames['7']['2']['2']}")
		                elif self.frame == 2:
		                    self.frame = 3
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['7']['3']['1']}")
		                    print(f"\r{self.frames['7']['3']['2']}")
		                elif self.frame == 3:
		                    self.frame = 4
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['7']['4']['1']}")
		                    print(f"\r{self.frames['7']['4']['2']}")
		                elif self.frame == 4:
		                    self.frame = 5
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['7']['5']['1']}")
		                    print(f"\r{self.frames['7']['5']['2']}")
		                elif self.frame == 5:
		                    self.frame = 6
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['7']['6']['1']}")
		                    print(f"\r{self.frames['7']['6']['2']}")
		                elif self.frame == 6:
		                    self.frame = 7
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['7']['7']['1']}")
		                    print(f"\r{self.frames['7']['7']['2']}")
		                elif self.frame == 7:
		                    self.frame = 7
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['7']['7']['1']}")
		                    print(f"\r{self.frames['7']['7']['2']}")
		            elif self.key == b'K':  # left
		                if self.frame == 1:
		                    self.frame = 1
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['7']['1']['1']}")
		                    print(f"\r{self.frames['7']['1']['2']}")
		                elif self.frame == 2:
		                    self.frame = 1
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['7']['1']['1']}")
		                    print(f"\r{self.frames['7']['1']['2']}")
		                elif self.frame == 3:
		                    self.frame = 2
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['7']['2']['1']}")
		                    print(f"\r{self.frames['7']['2']['2']}")
		                elif self.frame == 4:
		                    self.frame = 3
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['7']['3']['1']}")
		                    print(f"\r{self.frames['7']['3']['2']}")
		                elif self.frame == 5:
		                    self.frame = 4
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['7']['4']['1']}")
		                    print(f"\r{self.frames['7']['4']['2']}")
		                elif self.frame == 6:
		                    self.frame = 5
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['7']['5']['1']}")
		                    print(f"\r{self.frames['7']['5']['2']}")
		                elif self.frame == 7:
		                    self.frame = 6
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['7']['6']['1']}")
		                    print(f"\r{self.frames['7']['6']['2']}")
		                elif self.frame == 7:
		                    self.frame = 7
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['7']['7']['1']}")
		                    print(f"\r{self.frames['7']['7']['2']}")
		        elif self.continueBind == self.key.decode():
		            break

		elif self.length == 8:
		    self.frame = 1
		    clearLastLines()
		    print(f"\r{self.frames['8']['1']['1']}")
		    print(f"\r{self.frames['8']['1']['2']}")

		    while True:
		        self.key = msvcrt.getch()
		        if self.key == b'\xe0':
		            self.key = msvcrt.getch()
		            if self.key == b'M':  # right
		                if self.frame == 1:
		                    self.frame = 2
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['8']['2']['1']}")
		                    print(f"\r{self.frames['8']['2']['2']}")
		                elif self.frame == 2:
		                    self.frame = 3
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['8']['3']['1']}")
		                    print(f"\r{self.frames['8']['3']['2']}")
		                elif self.frame == 3:
		                    self.frame = 4
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['8']['4']['1']}")
		                    print(f"\r{self.frames['8']['4']['2']}")
		                elif self.frame == 4:
		                    self.frame = 5
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['8']['5']['1']}")
		                    print(f"\r{self.frames['8']['5']['2']}")
		                elif self.frame == 5:
		                    self.frame = 6
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['8']['6']['1']}")
		                    print(f"\r{self.frames['8']['6']['2']}")
		                elif self.frame == 6:
		                    self.frame = 7
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['8']['7']['1']}")
		                    print(f"\r{self.frames['8']['7']['2']}")
		                elif self.frame == 7:
		                    self.frame = 8
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['8']['8']['1']}")
		                    print(f"\r{self.frames['8']['8']['2']}")
		                elif self.frame == 8:
		                    self.frame = 8
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['8']['8']['1']}")
		                    print(f"\r{self.frames['8']['8']['2']}")
		            elif self.key == b'K':  # left
		                if self.frame == 1:
		                    self.frame = 1
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['8']['1']['1']}")
		                    print(f"\r{self.frames['8']['1']['2']}")
		                elif self.frame == 2:
		                    self.frame = 1
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['8']['1']['1']}")
		                    print(f"\r{self.frames['8']['1']['2']}")
		                elif self.frame == 3:
		                    self.frame = 2
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['8']['2']['1']}")
		                    print(f"\r{self.frames['8']['2']['2']}")
		                elif self.frame == 4:
		                    self.frame = 3
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['8']['3']['1']}")
		                    print(f"\r{self.frames['8']['3']['2']}")
		                elif self.frame == 5:
		                    self.frame = 4
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['8']['4']['1']}")
		                    print(f"\r{self.frames['8']['4']['2']}")
		                elif self.frame == 6:
		                    self.frame = 5
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['8']['5']['1']}")
		                    print(f"\r{self.frames['8']['5']['2']}")
		                elif self.frame == 7:
		                    self.frame = 6
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['8']['6']['1']}")
		                    print(f"\r{self.frames['8']['6']['2']}")
		                elif self.frame == 8:
		                    self.frame = 7
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['8']['7']['1']}")
		                    print(f"\r{self.frames['8']['7']['2']}")
		                elif self.frame == 8:
		                    self.frame = 8
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['8']['8']['1']}")
		                    print(f"\r{self.frames['8']['8']['2']}")
		        elif self.continueBind == self.key.decode():
		            break

		elif self.length == 9:
		    self.frame = 1
		    clearLastLines()
		    print(f"\r{self.frames['9']['1']['1']}")
		    print(f"\r{self.frames['9']['1']['2']}")

		    while True:
		        self.key = msvcrt.getch()
		        if self.key == b'\xe0':
		            self.key = msvcrt.getch()
		            if self.key == b'M':  # right
		                if self.frame == 1:
		                    self.frame = 2
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['9']['2']['1']}")
		                    print(f"\r{self.frames['9']['2']['2']}")
		                elif self.frame == 2:
		                    self.frame = 3
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['9']['3']['1']}")
		                    print(f"\r{self.frames['9']['3']['2']}")
		                elif self.frame == 3:
		                    self.frame = 4
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['9']['4']['1']}")
		                    print(f"\r{self.frames['9']['4']['2']}")
		                elif self.frame == 4:
		                    self.frame = 5
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['9']['5']['1']}")
		                    print(f"\r{self.frames['9']['5']['2']}")
		                elif self.frame == 5:
		                    self.frame = 6
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['9']['6']['1']}")
		                    print(f"\r{self.frames['9']['6']['2']}")
		                elif self.frame == 6:
		                    self.frame = 7
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['9']['7']['1']}")
		                    print(f"\r{self.frames['9']['7']['2']}")
		                elif self.frame == 7:
		                    self.frame = 8
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['9']['8']['1']}")
		                    print(f"\r{self.frames['9']['8']['2']}")
		                elif self.frame == 8:
		                    self.frame = 9
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['9']['9']['1']}")
		                    print(f"\r{self.frames['9']['9']['2']}")
		                elif self.frame == 9:
		                    self.frame = 9
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['9']['9']['1']}")
		                    print(f"\r{self.frames['9']['9']['2']}")
		            elif self.key == b'K':  # left
		                if self.frame == 1:
		                    self.frame = 1
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['9']['1']['1']}")
		                    print(f"\r{self.frames['9']['1']['2']}")
		                elif self.frame == 2:
		                    self.frame = 1
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['9']['1']['1']}")
		                    print(f"\r{self.frames['9']['1']['2']}")
		                elif self.frame == 3:
		                    self.frame = 2
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['9']['2']['1']}")
		                    print(f"\r{self.frames['9']['2']['2']}")
		                elif self.frame == 4:
		                    self.frame = 3
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['9']['3']['1']}")
		                    print(f"\r{self.frames['9']['3']['2']}")
		                elif self.frame == 5:
		                    self.frame = 4
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['9']['4']['1']}")
		                    print(f"\r{self.frames['9']['4']['2']}")
		                elif self.frame == 6:
		                    self.frame = 5
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['9']['5']['1']}")
		                    print(f"\r{self.frames['9']['5']['2']}")
		                elif self.frame == 7:
		                    self.frame = 6
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['9']['6']['1']}")
		                    print(f"\r{self.frames['9']['6']['2']}")
		                elif self.frame == 8:
		                    self.frame = 7
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['9']['7']['1']}")
		                    print(f"\r{self.frames['9']['7']['2']}")
		                elif self.frame == 9:
		                    self.frame = 8
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['9']['8']['1']}")
		                    print(f"\r{self.frames['9']['8']['2']}")
		                elif self.frame == 9:
		                    self.frame = 9
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['9']['9']['1']}")
		                    print(f"\r{self.frames['9']['9']['2']}")
		        elif self.continueBind == self.key.decode():
		            break

		elif self.length == 10:
		    self.frame = 1
		    clearLastLines()
		    print(f"\r{self.frames['10']['1']['1']}")
		    print(f"\r{self.frames['10']['1']['2']}")

		    while True:
		        self.key = msvcrt.getch()
		        if self.key == b'\xe0':
		            self.key = msvcrt.getch()
		            if self.key == b'M':  # right
		                if self.frame == 1:
		                    self.frame = 2
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['10']['2']['1']}")
		                    print(f"\r{self.frames['10']['2']['2']}")
		                elif self.frame == 2:
		                    self.frame = 3
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['10']['3']['1']}")
		                    print(f"\r{self.frames['10']['3']['2']}")
		                elif self.frame == 3:
		                    self.frame = 4
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['10']['4']['1']}")
		                    print(f"\r{self.frames['10']['4']['2']}")
		                elif self.frame == 4:
		                    self.frame = 5
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['10']['5']['1']}")
		                    print(f"\r{self.frames['10']['5']['2']}")
		                elif self.frame == 5:
		                    self.frame = 6
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['10']['6']['1']}")
		                    print(f"\r{self.frames['10']['6']['2']}")
		                elif self.frame == 6:
		                    self.frame = 7
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['10']['7']['1']}")
		                    print(f"\r{self.frames['10']['7']['2']}")
		                elif self.frame == 7:
		                    self.frame = 8
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['10']['8']['1']}")
		                    print(f"\r{self.frames['10']['8']['2']}")
		                elif self.frame == 8:
		                    self.frame = 9
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['10']['9']['1']}")
		                    print(f"\r{self.frames['10']['9']['2']}")
		                elif self.frame == 9:
		                    self.frame = 10
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['10']['10']['1']}")
		                    print(f"\r{self.frames['10']['10']['2']}")
		                elif self.frame == 10:
		                    self.frame = 10
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['10']['10']['1']}")
		                    print(f"\r{self.frames['10']['10']['2']}")
		            elif self.key == b'K':  # left
		                if self.frame == 1:
		                    self.frame = 1
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['10']['1']['1']}")
		                    print(f"\r{self.frames['10']['1']['2']}")
		                elif self.frame == 2:
		                    self.frame = 1
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['10']['1']['1']}")
		                    print(f"\r{self.frames['10']['1']['2']}")
		                elif self.frame == 3:
		                    self.frame = 2
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['10']['2']['1']}")
		                    print(f"\r{self.frames['10']['2']['2']}")
		                elif self.frame == 4:
		                    self.frame = 3
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['10']['3']['1']}")
		                    print(f"\r{self.frames['10']['3']['2']}")
		                elif self.frame == 5:
		                    self.frame = 4
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['10']['4']['1']}")
		                    print(f"\r{self.frames['10']['4']['2']}")
		                elif self.frame == 6:
		                    self.frame = 5
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['10']['5']['1']}")
		                    print(f"\r{self.frames['10']['5']['2']}")
		                elif self.frame == 7:
		                    self.frame = 6
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['10']['6']['1']}")
		                    print(f"\r{self.frames['10']['6']['2']}")
		                elif self.frame == 8:
		                    self.frame = 7
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['10']['7']['1']}")
		                    print(f"\r{self.frames['10']['7']['2']}")
		                elif self.frame == 9:
		                    self.frame = 8
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['10']['8']['1']}")
		                    print(f"\r{self.frames['10']['8']['2']}")
		                elif self.frame == 10:
		                    self.frame = 9
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['10']['9']['1']}")
		                    print(f"\r{self.frames['10']['9']['2']}")
		                elif self.frame == 10:
		                    self.frame = 10
		                    self.value = str(self.frame)
		                    clearLastLines()
		                    print(f"\r{self.frames['10']['10']['1']}")
		                    print(f"\r{self.frames['10']['10']['2']}")
		        elif self.continueBind == self.key.decode():
		            break

	def get(self):
		return int(self.value - 1)
