#SYMBOLS USED FOR ASCII ART (BIGGER TEXT SYMBOLS): ╱╲│‾╵─╷_
class CMDGiantText:
	def __init__(self, *, text: str, size: int):
		self.text = text
		self.size = size
		self.giantChars = {
			"sizeTwo": {
				"upperCase": {
					"A": {
						"1": " ╱╲  ",
						"2": "╱‾‾╲ ",
						"3": "     "
					},
					"B": {
						"1": "│‾) ",
						"2": "│_) ",
						"3": "    "
					},
					"C": {
						"1": "╱‾‾ ",
						"2": "╲__ ",
						"3": "    "
					},
					"D": {
						"1": "│‾‾╲ ",
						"2": "│__╱ ",
						"3": "     "
					},
					"E": {
						"1": "│‾‾ ",
						"2": "│‾  ",
						"3": " ‾‾ "
					},
					"F": {
						"1": "│‾‾ ",
						"2": "│‾  ",
						"3": "    "
					},
					"G": {
						"1": "╱‾‾_ ",
						"2": "╲__╱ ",
						"3": "     "
					},
					"H": {
						"1": "│__│ ",
						"2": "│  │ ",
						"3": "     "
					},
					"I": {
						"1": "‾│‾ ",
						"2": "_│_ ",
						"3": "    "
					},
					"J": {
						"1": "‾‾│‾‾ ",
						"2": "╷ │   ",
						"3": "╰─╯   "
					},
					"K": {
						"1": "│╱ ",
						"2": "│╲ ",
						"3": "   "
					},
					"L": {
						"1": "│   ",
						"2": "│__ ",
						"3": "    "
					},
					"M": {
						"1": "│╲╱│",
						"2": "│  │",
						"3": "    "
					},
					"N": {
						"1": "│╲ │ ",
						"2": "│ ╲│ ",
						"3": "     "
					},
					"O": {
						"1": "╱‾‾╲ ",
						"2": "╲__╱ ",
						"3": "     "
					},
					"P": {
						"1": "│‾) ",
						"2": "│‾  ",
						"3": "    "
					},
					"Q": {
						"1": "╱‾‾╲ ",
						"2": "╲__╳ ",
						"3": "     "
					},
					"R": {
						"1": "│‾) ",
						"2": "│‾╲ ",
						"3": "    "
					},
					"S": {
						"1": "(‾‾ ",
						"2": " ‾) ",
						"3": "‾‾  "
					},
					"T": {
						"1": "‾│‾ ",
						"2": " │  ",
						"3": "    "
					},
					"U": {
						"1": "│  │ ",
						"2": "│__│ ",
						"3": "     "
					},
					"V": {
						"1": "╲  ╱ ",
						"2": " ╲╱  ",
						"3": "     "
					},
					"W": {
						"1": "╲    ╱ ",
						"2": " ╲╱╲╱  ",
						"3": "       "
					},
					"X": {
						"1": "╲╱ ",
						"2": "╱╲ ",
						"3": "   "
					},
					"Y": {
						"1": "╲_╱ ",
						"2": " │  ",
						"3": "    "
					},
					"Z": {
						"1": "‾╱ ",
						"2": "╱_ ",
						"3": "    "
					}
				},
				"lowerCase": {
					"a": {
						"1": " _  ",
						"2": "(_╲ ",
						"3": "    "
					},
					"b": {
						"1": "│   ",
						"2": "│‾) ",
						"3": " ‾  "
					},
					"c": {
						"1": "   ",
						"2": "(‾ ",
						"3": " ‾ "
					},
					"d": {
						"1": "  │ ",
						"2": "(‾│ ",
						"3": " ‾  "
					},
					"e": {
						"1": " _  ",
						"2": "(─⁾ ",
						"3": " ‾  "
					},
					"f": {
						"1": " ╱‾ ",
						"2": "‾│‾ ",
						"3": "    "
					},
					"g": {
						"1": " _  ",
						"2": "(_│ ",
						"3": "╲_│ "
					},
					"h": {
						"1": "│   ",
						"2": "│‾| ",
						"3": "    "
					},
					"i": {
						"1": ". ",
						"2": "│ ",
						"3": "  "
					},
					"j": {
						"1": " . ",
						"2": " │ ",
						"3": "╰╯ "
					},
					"k": {
						"1": "│/ ",
						"2": "│╲ ",
						"3": "   "
					},
					"l": {
						"1": "│ ",
						"2": "│ ",
						"3": "  "
					},
					"m": {
						"1": "      ",
						"2": "│‾|‾| ",
						"3": "      "
					},
					"n": {
						"1": "    ",
						"2": "│‾| ",
						"3": "    "
					},
					"o": {
						"1": "   ",
						"2": "() ",
						"3": "   "
					},
					"p": {
						"1": " _  ",
						"2": "│_) ",
						"3": "│   "
					},
					"q": {
						"1": " _  ",
						"2": "(_│ ",
						"3": "  │ "
					},
					"r": {
						"1": "   ",
						"2": "│‾ ",
						"3": "   "
					},
					"s": {
						"1": " __ ",
						"2": "╵─╷ ",
						"3": "‾‾  "
					},
					"t": {
						"1": "─│─ ",
						"2": " │  ",
						"3": "    "
					},
					"u": {
						"1": "    ",
						"2": "│_│ ",
						"3": "    "
					},
					"v": {
						"1": "   ",
						"2": "╲╱ ",
						"3": "   "
					},
					"w": {
						"1": "     ",
						"2": "╲╱╲╱ ",
						"3": "     "
					},
					"x": {
						"1": "  ",
						"2": "╳ ",
						"3": "  "
					},
					"y": {
						"1": "   ",
						"2": "╲╱ ",
						"3": "╱  "
					},
					"z": {
						"1": "_ ",
						"2": "╱ ",
						"3": "‾ "
					}
				},
				"numbers": {
					"1": {
						"1": "╱│  ",
						"2": "_│_ ",
						"3": "    "
					},
					"2": {
						"1": "/‾) ",
						"2": "_╱_ ",
						"3": "    "
					},
					"3": {
						"1": "‾) ",
						"2": "_) ",
						"3": "   "
					},
					"4": {
						"1": "╱│  ",
						"2": "‾│‾ ",
						"3": "    "
					},
					"5": {
						"1": "│̲ ‾‾ ",
						"2": "__│ ",
						"3": "    "
					},
					"6": {
						"1": "╱̲ ‾‾ ",
						"2": "│_│ ",
						"3": "    "
					},
					"7": {
						"1": "‾‾╱ ",
						"2": " ╱  ",
						"3": "    "
					},
					"8": {
						"1": "(‾) ",
						"2": "(_) ",
						"3": "    "
					},
					"9": {
						"1": "(̲ ‾) ",
						"2": "__╱ ",
						"3": "    "
					},
					"0": {
						"1": "╱‾╲ ",
						"2": "╲_╱ ",
						"3": "    "
					}
				},
				"symbols": {
					"`": {
						"1": "╵ ",
						"2": "  ",
						"3": "  "
					},
					"~": {
						"1": "/\\/ ",
						"2": "     ",
						"3": "     "
					},
					"!": {
						"1": "│ ",
						"2": ". ",
						"3": "  "
					},
					"@": {
						"1": "╱‾╲ ",
						"2": "╲a╱ ",
						"3": "    "
					},
					"#": {
						"1": "─││─ ",
						"2": "─││─ ",
						"3": "     "
					},
					"$": {
						"1": "(│‾ ",
						"2": "_│) ",
						"3": " ╵  "
					},
					"%": {
						"1": "O╱ ",
						"2": "╱O ",
						"3": "   "
					},
					"^": {
						"1": "^ ",
						"2": "  ",
						"3": "  "
					},
					"&": {
						"1": "(‾) ",
						"2": "(_╲ ",
						"3": "    "
					},
					"*": {
						"1": "✶ ",
						"2": "  ",
						"3": "  "
					},
					"(": {
						"1": "╱ ",
						"2": "╲ ",
						"3": "  "
					},
					")": {
						"1": "╲ ",
						"2": "╱ ",
						"3": "   "
					},
					"-": {
						"1": "__ ",
						"2": "   ",
						"3": "   "
					},
					"_": {
						"1": "   ",
						"2": "___",
						"3": "   "
					},
					"=": {
						"1": "__ ",
						"2": "── ",
						"3": "   "
					},
					"+": {
						"1": "_╷_ ",
						"2": " ╵  ",
						"3": "    "
					},
					"[": {
						"1": "│‾ ",
						"2": "│_ ",
						"3": "   "
					},
					"{": {
						"1": "╱‾ ",
						"2": "╲_ ",
						"3": "   "
					},
					"]": {
						"1": "‾│ ",
						"2": "_│ ",
						"3": "   "
					},
					"}": {
						"1": "‾╲ ",
						"2": "_╱ ",
						"3": "   "
					},
					"\\": {
						"1": "╲  ",
						"2": " ╲ ",
						"3": "   "
					},
					"|": {
						"1": "│ ",
						"2": "│ ",
						"3": "  "
					},
					";": {
						"1": ". ",
						"2": ", ",
						"3": "  "
					},
					":": {
						"1": ". ",
						"2": ". ",
						"3": "  "
					},
					"'": {
						"1": "' ",
						"2": "  ",
						"3": "  "
					},
					'"': {
						"1": '" ',
						"2": '  ',
						"3": '  '
					},
					",": {
						"1": "  ",
						"2": ", ",
						"3": "  "
					},
					"<": {
						"1": "  ",
						"2": "< ",
						"3": "  "
					},
					".": {
						"1": "  ",
						"2": ". ",
						"3": "  "
					},
					">": {
						"1": "  ",
						"2": "> ",
						"3": "  "
					},
					"/": {
						"1": " ╱ ",
						"2": "╱  ",
						"3": "   "
					},
					"?": {
						"1": "‾) ",
						"2": "|  ",
						"3": ".  "
					}
				},
				"space": {
					"1": "   ",
					"2": "   ",
					"3": "   "
				}
			},
			"sizeThree": {
				"upperCase": {
					"A": {
						"1": "  ╱╲   ",
						"2": " ╱──╲  ",
						"3": "╱    ╲ ",
						"4": "       "
					},
					"B": {
						"1": "│‾‾) ",
						"2": "│─<  ",
						"3": "│__) ",
						"4": "     "
					},
					"C": {
						"1": "╱‾‾‾ ",
						"2": "│    ",
						"3": "╲___ ",
						"4": "     "
					},
					"D": {
						"1": "│‾‾‾╲ ",
						"2": "│   │ ",
						"3": "│___╱ ",
						"4": "      "
					},
					"E": {
						"1": "│‾‾‾ ",
						"2": "│─   ",
						"3": "│___ ",
						"4": "     "
					},
					"F": {
						"1": "│‾‾‾ ",
						"2": "│─   ",
						"3": "│    ",
						"4": "     "
					},
					"G": {
						"1": "╱‾‾‾  ",
						"2": "│ ──╷ ",
						"3": "╲___│ ",
						"4": "      "
					},
					"H": {
						"1": "│   │ ",
						"2": "│───│ ",
						"3": "│   │ ",
						"4": "      "
					},
					"I": {
						"1": "‾‾│‾‾ ",
						"2": "  │   ",
						"3": "__│__ ",
						"4": "      "
					},
					"J": {
						"1": "‾‾│‾‾ ",
						"2": "  │   ",
						"3": "╲_│   ",
						"4": "      "
					},
					"K": {
						"1": "│  ╱ ",
						"2": "│─<  ",
						"2": "│  ╲ ",
						"3": "    ",
						"4": "    "
					},
					"L": {
						"1": "│    ",
						"2": "│    ",
						"3": "│___ ",
						"4": "     "
					},
					"M": {
						"1": "│╲  ╱│ ",
						"2": "│ ╲╱ │ ",
						"3": "│    │ ",
						"4": "       "
					},
					"N": {
						"1": "│╲  │ ",
						"2": "│ ╲ │ ",
						"3": "│  ╲│ ",
						"4": "      "
					},
					"O": {
						"1": "╱‾‾‾‾╲ ",
						"2": "│    │ ",
						"3": "╲____╱ ",
						"4": "       "
					},
					"P": {
						"1": "│‾‾) ",
						"2": "│‾‾  ",
						"3": "│    ",
						"4": "     "
					},
					"Q": {
						"1": "╱‾‾‾‾╲ ",
						"2": "│    │ ",
						"3": "╲____╳ ",
						"4": "       "
					},
					"R": {
						"1": "│‾‾) ",
						"2": "│‾╲  ",
						"3": "│  ╲ ",
						"4": "     "
					},
					"S": {
						"1": "╱‾‾‾ ",
						"2": "\\──\\ ",
						"3": "___╱ ",
						"4": "     "
					},
					"T": {
						"1": "‾‾│‾‾ ",
						"2": "  │   ",
						"3": "  │   ",
						"4": "      "
					},
					"U": {
						"1": "│   │ ",
						"2": "│   │ ",
						"3": "╲___╱ ",
						"4": "      "
					},
					"V": {
						"1": "╲    ╱ ",
						"2": " ╲  ╱  ",
						"3": "  ╲╱   ",
						"4": "       "
					},
					"W": {
						"1": "╲        ╱ ",
						"2": " ╲  ╱╲  ╱  ",
						"3": "  ╲╱  ╲╱   ",
						"4": "           "
					},
					"X": {
						"1": "╲ ╱ ",
						"2": " ╳  ",
						"3": "╱ ╲ ",
						"4": "    "
					},
					"Y": {
						"1": "╲_╱ ",
						"2": " │  ",
						"3": " │  ",
						"4": "    "
					},
					"Z": {
						"1": "‾‾╱ ",
						"2": " ╱  ",
						"3": "╱__ ",
						"4": "    "
					} 
				},
				"lowerCase": {
					"a": {
						"1": "    ",
						"2": " ‾╲ ",
						"3": "(‾│ ",
						"4": " ‾  "
					},
					"b": {
						"1": "│    ",
						"2": "│‾‾╲ ",
						"3": "│__╱ ",
						"4": "     "
					},
					"c": {
						"1": "    ",
						"2": "╱‾‾ ",
						"3": "╲__ ",
						"4": "    "
					},
					"d": {
						"1": "   │ ",
						"2": "╱‾‾│ ",
						"3": "╲__│ ",
						"4": "     "
					},
					"e": {
						"1": "    ",
						"2": "╱̲‾| ",
						"3": "╲_  ",
						"4": "    "
					},
					"f": {
						"1": " ╱‾ ",
						"2": "─┼─ ",
						"3": " │  ",
						"4": "    "
					},
					"g": {
						"1": " ___ ",
						"2": "│__│ ",
						"3": "│──╷ ",
						"4": "│__│ "
					},
					"h": {
						"1": "│    ",
						"2": "│──╷ ",
						"3": "│  │ ",
						"4": "     "
					},
					"i": {
						"1": ". ",
						"2": "╷ ",
						"3": "│ ",
						"4": "  "
					},
					"j": {
						"1": "  . ",
						"2": "  ╷ ",
						"3": "╷ │ ",
						"4": "╰─╯ "
					},
					"k": {
						"1": "│  ",
						"2": "│╱ ",
						"3": "│╲ ",
						"4": "   "
					},
					"l": {
						"1": "│ ",
						"2": "│ ",
						"3": "│ ",
						"4": "  "
					},
					"m": {
						"1": "      ",
						"2": "╷─╷─╷ ",
						"3": "│ │ │ ",
						"4": "      "
					},
					"n": {
						"1": "    ",
						"2": "╷─╷ ",
						"3": "│ │ ",
						"4": "    "
					},
					"o": {
						"1": "     ",
						"2": "╱‾‾╲ ",
						"3": "╲__╱ ",
						"4": "     "
					},
					"p": {
						"1": "     ",
						"2": "│‾‾╲ ",
						"3": "│__╱ ",
						"4": "│    "
					},
					"q": {
						"1": "     ",
						"2": "╱‾‾│ ",
						"3": "╲__│ ",
						"4": "   │ "
					},
					"r": {
						"1": "   ",
						"2": "│‾ ",
						"3": "│  ",
						"4": "   "
					},
					"s": {
						"1": " __ ",
						"2": "│_  ",
						"3": "__│ ",
						"4": "    "
					},
					"t": {
						"1": " ╷  ",
						"2": "─┼─ ",
						"3": " │  ",
						"4": "    "
					},
					"u": {
						"1": "    ",
						"2": "│ │ ",
						"3": "│_│ ",
						"4": "    "
					},
					"v": {
						"1": "     ",
						"2": "╲  ╱ ",
						"3": " ╲╱  ",
						"4": "     "
					},
					"w": {
						"1": "       ",
						"2": "╲    ╱ ",
						"3": " ╲╱╲╱  ",
						"4": "       "
					},
					"x": {
						"1": "   ",
						"2": "╲╱ ",
						"3": "╱╲ ",
						"4": "   "
					},
					"y": {
						"1": "     ",
						"2": "╲  ╱ ",
						"3": " ╲╱  ",
						"4": " ╱   "
					},
					"z": {
						"1": "   ",
						"2": "‾╱ ",
						"3": "╱_ ",
						"4": "   "
					}
				},
				"numbers": {
					"1": {
						"1": "╱│  ",
						"2": " │  ",
						"3": "_│_ ",
						"4": "    "
					},
					"2": {
						"1": "╱‾‾╲  ",
						"2": "   ╱  ",
						"3": "__╱__ ",
						"4": "      "
					},
					"3": {
						"1": "╱‾‾╲ ",
						"2": " ──< ",
						"3": "╲__╱ ",
						"4": "     "
					},
					"4": {
						"1": " ╱│  ",
						"2": "╱_│_ ",
						"3": "  │  ",
						"4": "     "
					},
					"5": {
						"1": "│‾‾‾ ",
						"2": "╵──╷ ",
						"3": "___│ ",
						"4": "     "
					},
					"6": {
						"1": "│‾‾‾ ",
						"2": "│──╷ ",
						"3": "│__│ ",
						"4": "     "
					},
					"7": {
						"1": "‾‾‾╱ ",
						"2": "  ╱  ",
						"3": " ╱   ",
						"4": "     "
					},
					"8": {
						"1": "│‾‾│ ",
						"2": " ><  ",
						"3": "│__│ ",
						"4": "     "
					},
					"9": {
						"1": "│‾‾│ ",
						"2": "╵──│ ",
						"3": "___│ ",
						"4": "     "
					},
					"0": {
						"1": "│‾‾│ ",
						"2": "│  │ ",
						"3": "│__│ ",
						"4": "     "
					}
				},
				"symbols": {
					"`": {
						"1": "\\ ",
						"2": "  ",
						"3": "  ",
						"4": "  "
					},
					"~": {
						"1": "/\\/ ",
						"2": "    ",
						"3": "    ",
						"4": "    "
					},
					"!": {
						"1": "│ ",
						"2": "│ ",
						"3": ". ",
						"4": "  "
					},
					"@": {
						"1": "╱‾‾╲ ",
						"2": "│  │ ",
						"3": "╲_α╱ ",
						"4": "     "
					},
					"#": {
						"1": "_│_│_ ",
						"2": " │ │  ",
						"3": "‾│‾│‾ ",
						"4": "      "
					},
					"$": {
						"1": "│‾‾╱ ",
						"2": "╵─╱╷ ",
						"3": "_╱_│ ",
						"4": "╱    "
					},
					"%": {
						"1": "◯╱ ",
						"2": " ╱  ",
						"3": "╱◯ ",
						"4": "    "
					},
					"^": {
						"1": "╱╲ ",
						"2": "   ",
						"3": "   ",
						"4": "   "
					},
					"&": {
						"1": "│‾‾│ ",
						"2": " ><  ",
						"3": "│_╱╲ ",
						"4": "     "
					},
					"*": {
						"1": "✶ ",
						"2": "  ",
						"3": "  ",
						"4": "  "
					},
					"(": {
						"1": "╱ ",
						"2": "│ ",
						"3": "╲ ",
						"4": "  "
					},
					")": {
						"1": "╲ ",
						"2": "│ ",
						"3": "╱ ",
						"4": "  "
					},
					"-": {
						"1": "    ",
						"2": "─── ",
						"3": "    ",
						"4": "    "
					},
					"_": {
						"1": "     ",
						"2": "     ",
						"3": "____ ",
						"4": "     "
					},
					"=": {
						"1": "___ ",
						"2": "___ ",
						"3": "    ",
						"4": "    "
					},
					"+": {
						"1": " ╷  ",
						"2": "─┼─ ",
						"3": " ╵  ",
						"4": "    "
					},
					"[": {
						"1": "│‾‾ ",
						"2": "│   ",
						"3": "│__ ",
						"4": "    "
					},
					"{": {
						"1": " ╱‾ ",
						"2": "<   ",
						"3": " ╲_ ",
						"4": "    "
					},
					"]": {
						"1": "‾‾│ ",
						"2": "  │ ",
						"3": "__│ ",
						"4": "    "
					},
					"}": {
						"1": "‾╲  ",
						"2": "  > ",
						"3": "_╱  ",
						"4": "    "
					},
					"\\": {
						"1": "╲   ",
						"2": " ╲  ",
						"3": "  ╲ ",
						"4": "    "
					},
					"|": {
						"1": "│ ",
						"2": "│ ",
						"3": "│ ",
						"4": "  "
					},
					";": {
						"1": "  ",
						"2": ". ",
						"3": ", ",
						"4": "  "
					},
					":": {
						"1": "  ",
						"2": ". ",
						"3": ". ",
						"4": "  "
					},
					"'": {
						"1": "╵ ",
						"2": "  ",
						"3": "  ",
						"4": "  "
					},
					'"': {
						"1": "╵╵ ",
						"2": "   ",
						"3": "   ",
						"4": "   "
					},
					",": {
						"1": "  ",
						"2": "  ",
						"3": ", ",
						"4": "  "
					},
					"<": {
						"1": "  ",
						"2": "╱ ",
						"3": "╲ ",
						"4": "  "
					},
					".": {
						"1": "  ",
						"2": "  ",
						"3": "• ",
						"4": "  "
					},
					">": {
						"1": "  ",
						"2": "╲ ",
						"3": "╱ ",
						"4": "  "
					},
					"/": {
						"1": "  ╱ ",
						"2": " ╱  ",
						"3": "╱   ",
						"4": "    "
					},
					"?": {
						"1": "‾) ",
						"2": "│  ",
						"3": "•  ",
						"4": "    "
					}
				},
				"space": {
					"1": "    ",
					"2": "    ",
					"3": "    ",
					"4": "    "
				}
			},
			"sizeFour": {
				"upperCase": {
					"A": {
						"1": "   ╱╲    ",
						"2": "  ╱──╲   ",
						"3": " ╱    ╲  ",
						"4": "╱      ╲ ",
						"5": "         "
					},
					"B": {
						"1": "│‾‾‾╲ ",
						"2": "│___╱ ",
						"3": "│   ╲ ",
						"4": "│___╱ ",
						"5": "      "
					},
					"C": {
						"1": "╱‾‾‾‾ ",
						"2": "│     ",
						"3": "│     ",
						"4": "╲____ ",
						"5": "      "
					},
					"D": {
						"1": "│‾‾‾‾╲ ",
						"2": "│    │ ",
						"3": "│    │ ",
						"4": "│____╱ ",
						"5": "       "
					},
					"E": {
						"1": "│‾‾‾‾ ",
						"2": "│__   ",
						"3": "│     ",
						"4": "│____ ",
						"5": "      "
					},
					"F": {
						"1": "│‾‾‾‾ ",
						"2": "│__   ",
						"3": "│     ",
						"4": "│     ",
						"5": "      "
					},
					"G": {
						"1": "╱‾‾‾‾‾ ",
						"2": "│      ",
						"3": "│ ‾‾‾│ ",
						"4": "╲____│ ",
						"5": "       "
					},
					"H": {
						"1": "│    │ ",
						"2": "│____│ ",
						"3": "│    │ ",
						"4": "│    │ ",
						"5": "       "
					},
					"I": {
						"1": "‾‾‾│‾‾‾ ",
						"2": "   │    ",
						"3": "   │    ",
						"4": "___│___ ",
						"5": "        "
					},
					"J": {
						"1": "‾‾‾│‾‾‾ ",
						"2": "   │    ",
						"3": "   │    ",
						"4": "╲__│    ",
						"5": "        "
					},
					"K": {
						"1": "│   ╱ ",
						"2": "│__╱  ",
						"3": "│  ╲  ",
						"4": "│   ╲ ",
						"5": "      ",
					},
					"L": {
						"1": "│     ",
						"2": "│     ",
						"3": "│     ",
						"4": "│____ ",
						"5": "      "
					},
					"M": {
						"1": "│╲    ╱│ ",
						"2": "│ ╲  ╱ │ ",
						"3": "│  ╲╱  │ ",
						"4": "│      │ ",
						"5": "         "
					},
					"N": {
						"1": "│╲   │ ",
						"2": "│ ╲  │ ",
						"3": "│  ╲ │ ",
						"4": "│   ╲│ ",
						"5": "       "
					},
					"O": {
						"1": "╱‾‾‾‾‾╲ ",
						"2": "│     │ ",
						"3": "│     │ ",
						"4": "╲_____╱ ",
						"5": "       "
					},
					"P": {
						"1": "│‾‾‾╲ ",
						"2": "│___╱ ",
						"3": "│     ",
						"4": "│     ",
						"5": "      "
					},
					"Q": {
						"1": "╱‾‾‾‾‾╲  ",
						"2": "│     │  ",
						"3": "│    ╲│  ",
						"4": "╲_____╳  ",
						"5": "       ╲ "
					},
					"R": {
						"1": "│‾‾‾╲ ",
						"2": "│___╱ ",
						"3": "│  ╲  ",
						"4": "│   ╲ ",
						"5": "      "
					},
					"S": {
						"1": "╱‾‾‾‾ ",
						"2": "╲___  ",
						"3": "    ╲ ",
						"4": "____╱ ",
						"5": "      "
					},
					"T": {
						"1": "‾‾‾│‾‾‾ ",
						"2": "   │    ",
						"3": "   │    ",
						"4": "   │    ",
						"5": "        "
					},
					"U": {
						"1": "│     │ ",
						"2": "│     │ ",
						"3": "│     │ ",
						"4": "╲_____╱ ",
						"5": "        "
					},
					"V": {
						"1": "╲      ╱ ",
						"2": " ╲    ╱  ",
						"3": "  ╲  ╱   ",
						"4": "   ╲╱    ",
						"5": "         "
					},
					"W": {
						"1": "╲            ╱ ",
						"2": " ╲    ╱╲    ╱  ",
						"3": "  ╲  ╱  ╲  ╱   ",
						"4": "   ╲╱    ╲╱    ",
						"5": "               "
					},
					"X": {
						"1": "╲  ╱ ",
						"2": " ╲╱  ",
						"3": " ╱╲  ",
						"4": "╱  ╲ ",
						"5": "     "
					},
					"Y": {
						"1": "╲   ╱ ",
						"2": " ╲_╱  ",
						"3": "  │   ",
						"4": "  │   ",
						"5": "      "
					},
					"Z": {
						"1": "‾‾‾╱ ",
						"2": "  ╱  ",
						"3": " ╱   ",
						"4": "╱___ ",
						"5": "     "
					} 
				},
				"lowerCase": {
					"a": {
						"1": "     ",
						"2": " __  ",
						"3": " __│ ",
						"4": "│__│ ",
						"5": "     "
					},
					"b": {
						"1": "│    ",
						"2": "│    ",
						"3": "│‾‾╲ ",
						"4": "│__╱ ",
						"5": "     "
					},
					"c": {
						"1": "    ",
						"2": "    ",
						"3": "╱‾‾ ",
						"4": "╲__ ",
						"5": "    "
					},
					"d": {
						"1": "   │ ",
						"2": "   │ ",
						"3": "╱‾‾│ ",
						"4": "╲__│ ",
						"5": "     "
					},
					"e": {
						"1": "     ",
						"2": "     ",
						"3": "╱‾‾| ",
						"4": "╲‾‾  ",
						"5": " ‾‾  "
					},
					"f": {
						"1": " ╱‾‾ ",
						"2": "─┼── ",
						"3": " │   ",
						"4": " │   ",
						"5": "     "
					},
					"g": {
						"1": " ___ ",
						"2": "│__│ ",
						"3": "│──╷ ",
						"4": "│__│ ",
						"5": "     "
					},
					"h": {
						"1": "│     ",
						"2": "│___  ",
						"3": "│   │ ",
						"4": "│   │ ",
						"5": "      "
					},
					"i": {
						"1": "  ",
						"2": "  ",
						"3": "│ ",
						"4": "│ ",
						"5": "  "
					},
					"j": {
						"1": "  . ",
						"2": "  ╷ ",
						"3": "  │ ",
						"4": "│ │ ",
						"5": "╰─╯ "
					},
					"k": {
						"1": "│   ",
						"2": "│ ╱ ",
						"3": "│<  ",
						"4": "│ ╲ ",
						"5": "    "
					},
					"l": {
						"1": "│ ",
						"2": "│ ",
						"3": "│ ",
						"4": "│ ",
						"5": "  "
					},
					"m": {
						"1": "        ",
						"2": "╷__ __  ",
						"3": "│  │  │ ",
						"4": "│  │  │ ",
						"5": "        "
					},
					"n": {
						"1": "     ",
						"2": "╷__  ",
						"3": "│  │ ",
						"4": "│  │ ",
						"5": "     "
					},
					"o": {
						"1": "     ",
						"2": "     ",
						"3": "╱‾‾╲ ",
						"4": "╲__╱ ",
						"5": "     "
					},
					"p": {
						"1": "     ",
						"2": "│‾‾╲ ",
						"3": "│__╱ ",
						"4": "│    ",
						"5": "│    "
					},
					"q": {
						"1": "     ",
						"2": "╱‾‾│ ",
						"3": "╲__│ ",
						"4": "   │ ",
						"5": "   │ "
					},
					"r": {
						"1": "    ",
						"2": "╷__ ",
						"3": "│   ",
						"4": "│   ",
						"5": "    "
					},
					"s": {
						"1": "    ",
						"2": "╷── ",
						"3": "╵─╷ ",
						"4": "__│ ",
						"5": "    "
					},
					"t": {
						"1": " ╷  ",
						"2": "_│_ ",
						"3": " │  ",
						"4": " │  ",
						"5": "     "
					},
					"u": {
						"1": "     ",
						"2": "     ",
						"3": "│  │ ",
						"4": "│__│ ",
						"5": "     "
					},
					"v": {
						"1": "      ",
						"2": "      ",
						"3": "╲  ╱  ",
						"4": " ╲╱   ",
						"5": "      "
					},
					"w": {
						"1": "       ",
						"2": "       ",
						"3": "╲    ╱ ",
						"4": " ╲╱╲╱  ",
						"5": "       "
					},
					"x": {
						"1": "   ",
						"2": "   ",
						"3": "╲╱ ",
						"4": "╱╲ ",
						"5": "   "
					},
					"y": {
						"1": "     ",
						"2": "     ",
						"3": "╲  ╱ ",
						"4": " ╲╱  ",
						"5": " ╱   "
					},
					"z": {
						"1": "   ",
						"2": "__ ",
						"3": " ╱ ",
						"4": "╱  ",
						"5": "‾‾ "
					}
				},
				"numbers": {
					"1": {
						"1": " ╱│   ",
						"2": "╱ │   ",
						"3": "  │   ",
						"4": "  │   ",
						"5": "‾‾‾‾‾ "
					},
					"2": {
						"1": "╱‾‾‾╲ ",
						"2": "    ╱ ",
						"3": "   ╱  ",
						"4": "__╱__ ",
						"5": "       "
					},
					"3": {
						"1": "╱‾‾‾╲ ",
						"2": " ___╱ ",
						"3": "    ╲ ",
						"4": "╲___╱ ",
						"5": "      "
					},
					"4": {
						"1": " ╱│   ",
						"2": "╱ │   ",
						"3": "‾‾│‾‾ ",
						"4": "  │   ",
						"5": "      "
					},
					"5": {
						"1": "│‾‾‾‾ ",
						"2": "│___  ",
						"3": "    │ ",
						"4": "____│ ",
						"5": "      "
					},
					"6": {
						"1": "│‾‾‾‾‾ ",
						"2": "│      ",
						"3": "│‾‾‾‾│ ",
						"4": "│____│ ",
						"5": "       "
					},
					"7": {
						"1": "‾‾‾‾╱ ",
						"2": "   ╱  ",
						"3": "  ╱   ",
						"4": " ╱    ",
						"5": "      "
					},
					"8": {
						"1": "╱‾‾‾╲ ",
						"2": "╲___╱ ",
						"3": "╱   ╲ ",
						"4": "╲___╱ ",
						"5": "      "
					},
					"9": {
						"1": "╱‾‾‾╲ ",
						"2": "╲___╱ ",
						"3": "   ╱  ",
						"4": "  ╱   ",
						"5": "      "
					},
					"0": {
						"1": "│‾‾‾‾│ ",
						"2": "│    │ ",
						"3": "│    │ ",
						"4": "│____│ ",
						"5": "       "
					}
				},
				"symbols": {
					"`": {
						"1": "╲ ",
						"2": "  ",
						"3": "  ",
						"4": "  ",
						"5": "  "
					},
					"~": {
						"1": "╱╲╱ ",
						"2": "    ",
						"3": "    ",
						"4": "    ",
						"5": "    "
					},
					"!": {
						"1": "│ ",
						"2": "│ ",
						"3": "╵ ",
						"4": "• ",
						"5": "  "
					},
					"@": {
						"1": "╱‾‾‾‾‾╲ ",
						"2": "││‾‾╲ │ ",
						"3": "││__│╲│ ",
						"4": "╲_____╱ ",
						"5": "        "
					},
					"#": {
						"1": "  │  │   ",
						"2": "──│──│── ",
						"3": "──│──│── ",
						"4": "  │  │   ",
						"5": "         "
					},
					"$": {
						"1": "│‾‾‾╱ ",
						"2": "│__╱  ",
						"3": "  ╱ │ ",
						"4": "_╱__│ ",
						"5": "╱     "
					},
					"%": {
						"1": "╱‾╲ ╱  ",
						"2": "╲_╱╱   ",
						"3": "  ╱╱‾╲ ",
						"4": " ╱ ╲_╱ ",
						"5": "       "
					},
					"^": {
						"1": "╱╲ ",
						"2": "   ",
						"3": "   ",
						"4": "   ",
						"5": "   "
					},
					"&": {
						"1": "╱‾‾╲ ",
						"2": "╲__╱ ",
						"3": "╱ ╲╲ ",
						"4": "╲__╳ ",
						"5": "     "
					},
					"*": {
						"1": "_\\/_ ",
						"2": " /\\  ",
						"3": "     ",
						"4": "     ",
						"5": "     "
					},
					"(": {
						"1": "╱ ",
						"2": "│ ",
						"3": "│ ",
						"4": "╲  ",
						"5": "  "
					},
					")": {
						"1": "╲ ",
						"2": "│ ",
						"3": "│ ",
						"4": "╱ ",
						"5": "  "
					},
					"-": {
						"1": "     ",
						"2": "____ ",
						"3": "     ",
						"4": "     ",
						"5": "     "
					},
					"_": {
						"1": "      ",
						"2": "      ",
						"3": "      ",
						"4": "_____ ",
						"5": "      "
					},
					"=": {
						"1": "    ",
						"2": "___ ",
						"3": "___ ",
						"4": "    ",
						"5": "    "
					},
					"+": {
						"1": "  │   ",
						"2": "──│── ",
						"3": "  │   ",
						"4": "      "
					},
					"[": {
						"1": "│‾‾‾ ",
						"2": "│    ",
						"3": "│    ",
						"4": "│___ ",
						"5": "     " 
					},
					"{": {
						"1": " ╱‾‾ ",
						"2": "/│   ",
						"3": "\\│   ",
						"4": " ╲__ ",
						"5": "     "
					},
					"]": {
						"1": "‾‾‾│ ",
						"2": "   │ ",
						"3": "   │ ",
						"4": "___│  ",
						"5": "    "
					},
					"}": {
						"1": "‾‾╲  ",
						"2": "  │\\ ",
						"3": "  │/ ",
						"4": "__╱  ",
						"5": "     "
					},
					"\\": {
						"1": "╲    ",
						"2": " ╲   ",
						"3": "  ╲  ",
						"4": "   ╲ ",
						"5": "     "
					},
					"|": {
						"1": "│ ",
						"2": "│ ",
						"3": "│ ",
						"4": "│ ",
						"5": "  "
					},
					";": {
						"1": "  ",
						"2": "• ",
						"3": "  ",
						"4": ", ",
						"5": "  "
					},
					":": {
						"1": "  ",
						"2": "• ",
						"3": "  ",
						"4": "• ",
						"5": "  "
					},
					"'": {
						"1": "| ",
						"2": "  ",
						"3": "  ",
						"4": "  ",
						"5": "  "
					},
					'"': {
						"1": "|| ",
						"2": "   ",
						"3": "   ",
						"4": "   ",
						"5": "   "
					},
					",": {
						"1": "  ",
						"2": "  ",
						"3": "  ",
						"4": ", ",
						"5": "  "
					},
					"<": {
						"1": "",
						"2": "",
						"3": "╱",
						"4": "╲",
						"5": ""
					},
					".": {
						"1": "  ",
						"2": "  ",
						"3": "  ",
						"4": "• ",
						"5": "  "
					},
					">": {
						"1": "  ",
						"2": "  ",
						"3": "╲ ",
						"4": "╱ ",
						"5": "  "
					},
					"/": {
						"1": "   ╱ ",
						"2": "  ╱  ",
						"3": " ╱   ",
						"4": "╱    ",
						"5": "     "
					},
					"?": {
						"1": "‾)     ",
						"2": "T      ",
						"3": "│      ",
						"4": "•      ",
						"5": "       "
					}
				},
				"space": {
					"1": "      ",
					"2": "      ",
					"3": "      ",
					"4": "      ",
					"5": "      "
				}
			}
		}
	def sizeTwoText(self):
		global returnText
		self.outputTextRowOneList = []
		self.outputTextRowTwoList = []
		self.outputTextRowThreeList = []
		for char in self.text:
			if char in 'abcdefghijklmnopqrstuvwxyz':
				self.outputTextRowOneList.append(self.giantChars["sizeTwo"]["lowerCase"][char]["1"])
				self.outputTextRowTwoList.append(self.giantChars["sizeTwo"]["lowerCase"][char]["2"])
				self.outputTextRowThreeList.append(self.giantChars["sizeTwo"]["lowerCase"][char]["3"])
			elif char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
				self.outputTextRowOneList.append(self.giantChars["sizeTwo"]["upperCase"][char]["1"])
				self.outputTextRowTwoList.append(self.giantChars["sizeTwo"]["upperCase"][char]["2"])
				self.outputTextRowThreeList.append(self.giantChars["sizeTwo"]["upperCase"][char]["3"])
			elif char in '1234567890':
				self.outputTextRowOneList.append(self.giantChars["sizeTwo"]["numbers"][char]["1"])
				self.outputTextRowTwoList.append(self.giantChars["sizeTwo"]["numbers"][char]["2"])
				self.outputTextRowThreeList.append(self.giantChars["sizeTwo"]["numbers"][char]["3"])
			elif char in '`~!@#$%^&*()-_=+[{]}\\|;:",<.>/?' or char in "'":
				self.outputTextRowOneList.append(self.giantChars["sizeTwo"]["symbols"][char]["1"])
				self.outputTextRowTwoList.append(self.giantChars["sizeTwo"]["symbols"][char]["2"])
				self.outputTextRowThreeList.append(self.giantChars["sizeTwo"]["symbols"][char]["3"])
			elif char in ' ':
				self.outputTextRowOneList.append(self.giantChars["sizeTwo"]["space"]["1"])
				self.outputTextRowTwoList.append(self.giantChars["sizeTwo"]["space"]["2"])
				self.outputTextRowThreeList.append(self.giantChars["sizeTwo"]["space"]["3"])

		self.outputTextRowOne = ''.join(self.outputTextRowOneList)
		self.outputTextRowTwo = ''.join(self.outputTextRowTwoList)
		self.outputTextRowThree = ''.join(self.outputTextRowThreeList)

		self.returnText = f"{self.outputTextRowOne}\n{self.outputTextRowTwo}\n{self.outputTextRowThree}\n"

	def sizeThreeText(self):
		global returnText
		self.outputTextList = []
		self.outputTextRowOneList = []
		self.outputTextRowTwoList = []
		self.outputTextRowThreeList = []
		self.outputTextRowFourList = []
		for char in self.text:
			if char in 'abcdefghijklmnopqrstuvwxyz':
				self.outputTextRowOneList.append(self.giantChars["sizeThree"]["lowerCase"][char]["1"])
				self.outputTextRowTwoList.append(self.giantChars["sizeThree"]["lowerCase"][char]["2"])
				self.outputTextRowThreeList.append(self.giantChars["sizeThree"]["lowerCase"][char]["3"])
				self.outputTextRowFourList.append(self.giantChars["sizeThree"]["lowerCase"][char]["4"])
			elif char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
				self.outputTextRowOneList.append(self.giantChars["sizeThree"]["upperCase"][char]["1"])
				self.outputTextRowTwoList.append(self.giantChars["sizeThree"]["upperCase"][char]["2"])
				self.outputTextRowThreeList.append(self.giantChars["sizeThree"]["upperCase"][char]["3"])
				self.outputTextRowFourList.append(self.giantChars["sizeThree"]["upperCase"][char]["4"])
			elif char in '1234567890':
				self.outputTextRowOneList.append(self.giantChars["sizeThree"]["numbers"][char]["1"])
				self.outputTextRowTwoList.append(self.giantChars["sizeThree"]["numbers"][char]["2"])
				self.outputTextRowThreeList.append(self.giantChars["sizeThree"]["numbers"][char]["3"])
				self.outputTextRowFourList.append(self.giantChars["sizeThree"]["numbers"][char]["4"])
			elif char in '`~!@#$%^&*()-_=+[{]}\\|;:",<.>/?' or char in "'":
				self.outputTextRowOneList.append(self.giantChars["sizeThree"]["symbols"][char]["1"])
				self.outputTextRowTwoList.append(self.giantChars["sizeThree"]["symbols"][char]["2"])
				self.outputTextRowThreeList.append(self.giantChars["sizeThree"]["symbols"][char]["3"])
				self.outputTextRowFourList.append(self.giantChars["sizeThree"]["symbols"][char]["4"])
			elif char in ' ':
				self.outputTextRowOneList.append(self.giantChars["sizeThree"]["space"]["1"])
				self.outputTextRowTwoList.append(self.giantChars["sizeThree"]["space"]["2"])
				self.outputTextRowThreeList.append(self.giantChars["sizeThree"]["space"]["3"])
				self.outputTextRowFourList.append(self.giantChars["sizeThree"]["space"]["4"])
			elif char == '\n':
				self.index = self.outputTextRowOneList.index(char)
				self.outputTextRowOneList[self.index:]

		self.outputTextRowOne = ''.join(self.outputTextRowOneList)
		self.outputTextRowTwo = ''.join(self.outputTextRowTwoList)
		self.outputTextRowThree = ''.join(self.outputTextRowThreeList)
		self.outputTextRowFour = ''.join(self.outputTextRowFourList)

		self.returnText = f"{self.outputTextRowOne}\n{self.outputTextRowTwo}\n{self.outputTextRowThree}\n{self.outputTextRowFour}"

	def sizeFourText(self):
		global returnText
		self.outputTextList = []
		self.outputTextRowOneList = []
		self.outputTextRowTwoList = []
		self.outputTextRowThreeList = []
		self.outputTextRowFourList = []
		self.outputTextRowFiveList = []
		for char in self.text:
			if char in 'abcdefghijklmnopqrstuvwxyz':
				self.outputTextRowOneList.append(self.giantChars["sizeFour"]["lowerCase"][char]["1"])
				self.outputTextRowTwoList.append(self.giantChars["sizeFour"]["lowerCase"][char]["2"])
				self.outputTextRowThreeList.append(self.giantChars["sizeFour"]["lowerCase"][char]["3"])
				self.outputTextRowFourList.append(self.giantChars["sizeFour"]["lowerCase"][char]["4"])
				self.outputTextRowFiveList.append(self.giantChars["sizeFour"]["lowerCase"][char]["5"])
			elif char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
				self.outputTextRowOneList.append(self.giantChars["sizeFour"]["upperCase"][char]["1"])
				self.outputTextRowTwoList.append(self.giantChars["sizeFour"]["upperCase"][char]["2"])
				self.outputTextRowThreeList.append(self.giantChars["sizeFour"]["upperCase"][char]["3"])
				self.outputTextRowFourList.append(self.giantChars["sizeFour"]["upperCase"][char]["4"])
				self.outputTextRowFiveList.append(self.giantChars["sizeFour"]["upperCase"][char]["5"])
			elif char in '1234567890':
				self.outputTextRowOneList.append(self.giantChars["sizeFour"]["numbers"][char]["1"])
				self.outputTextRowTwoList.append(self.giantChars["sizeFour"]["numbers"][char]["2"])
				self.outputTextRowThreeList.append(self.giantChars["sizeFour"]["numbers"][char]["3"])
				self.outputTextRowFourList.append(self.giantChars["sizeFour"]["numbers"][char]["4"])
				self.outputTextRowFiveList.append(self.giantChars["sizeFour"]["numbers"][char]["5"])
			elif char in '`~!@#$%^&*()-_=+[{]}\\|;:",<.>/?' or char in "'":
				self.outputTextRowOneList.append(self.giantChars["sizeFour"]["symbols"][char]["1"])
				self.outputTextRowTwoList.append(self.giantChars["sizeFour"]["symbols"][char]["2"])
				self.outputTextRowThreeList.append(self.giantChars["sizeFour"]["symbols"][char]["3"])
				self.outputTextRowFourList.append(self.giantChars["sizeFour"]["symbols"][char]["4"])
				self.outputTextRowFiveList.append(self.giantChars["sizeFour"]["symbols"][char]["5"])
			elif char in ' ':
				self.outputTextRowOneList.append(self.giantChars["sizeFour"]["space"]["1"])
				self.outputTextRowTwoList.append(self.giantChars["sizeFour"]["space"]["2"])
				self.outputTextRowThreeList.append(self.giantChars["sizeFour"]["space"]["3"])
				self.outputTextRowFourList.append(self.giantChars["sizeFour"]["space"]["4"])
				self.outputTextRowFiveList.append(self.giantChars["sizeFour"]["space"]["5"])
			elif char == '\n':
				self.index = self.outputTextRowOneList.index(char)
				self.outputTextRowOneList[self.self.index:]

		self.outputTextRowOne = ''.join(self.outputTextRowOneList)
		self.outputTextRowTwo = ''.join(self.outputTextRowTwoList)
		self.outputTextRowThree = ''.join(self.outputTextRowThreeList)
		self.outputTextRowFour = ''.join(self.outputTextRowFourList)
		self.outputTextRowFive = ''.join(self.outputTextRowFiveList)

		self.returnText = f"{self.outputTextRowOne}\n{self.outputTextRowTwo}\n{self.outputTextRowThree}\n{self.outputTextRowFour}\n{self.outputTextRowFive}"

	def __str__(self):
		if self.size == 2:
		    self.sizeTwoText()
		elif self.size == 3:
		    self.sizeThreeText()
		elif self.size == 4:
		    self.sizeFourText()

		return self.returnText
