import msvcrt

class CMDCheckbox:
	def __init__(self, *, value: str, continueBind: str, color: str='#ffffff'):
		self.selected = False
		self.value = value
		self.continueBind = continueBind
		def clearLastLines():
			for _ in range(1):
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
		print(f"☐ {self.value}")
		while True:
			self.key = msvcrt.getch()
			if self.key == b'\xe0':
				self.key = msvcrt.getch()
				if self.key == b'M' or self.key == b'K':
					if self.selected == False:
						self.selected = True
						clearLastLines()
						print(f"☒ {self.value}")

					elif self.selected == True:
						self.selected = False
						clearLastLines()
						print(f"☐ {self.value}")

			elif self.continueBind == self.key.decode():
				break

	def get(self):
		return self.selected
