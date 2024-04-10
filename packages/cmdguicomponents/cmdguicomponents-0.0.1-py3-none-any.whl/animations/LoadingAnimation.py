import time
import threading

class CMDLoadingAnimation:
    def __init__(self, *, animationType: str, direction: str, delay: float, color: str='#ffffff', duration: float, beforeMessage: str='', afterMessage: str=''):
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

        self.animations = {
            "rotatingLine": {
                "right": {
                    "0": "|",
                    "1": "/",
                    "2": "—",
                    "3": "\\"
                },
                "left": {
                    "0": "|",
                    "1": "\\",
                    "2": "—",
                    "3": "/"
                }
            },
            "growingDot": {
                "n/a": {
                    "0": ".",
                    "1": "o",
                    "2": "O",
                    "3": "o"
                }
            },
            "jumpingDots": {
                "right": {
                    "0": "∙..",
                    "1": ".∙.",
                    "2": "..∙"
                },
                "left": {
                    "0": "..∙",
                    "1": ".∙.",
                    "2": "∙.."
                }
            },
            "spinningCircle": {
                "right": {
                    "0": "◜",
                    "1": "◝",
                    "2": "◞",
                    "3": "◟"
                },
                "left": {
                    "0": "◝",
                    "1": "◜",
                    "2": "◟",
                    "3": "◞"
                }
            }
        }
        self.animationType = animationType
        self.direction = direction
        self.delay = delay
        self.duration = duration
        self.beforeMessage = beforeMessage
        self.afterMessage = afterMessage
        def clearLastLines():
            for _ in range(1):
                print("\033[F\033[K", end="")

        self.duration = self.duration - 0.35
        startTime = time.time()

        if self.animationType == 'rotatingLine':
            if self.direction == 'right' or self.direction == 'left':
                self.currentFrameIndex = 0
                while time.time() - startTime <= self.duration:
                    self.currentFrameIndex %= 4
                    self.currentFrame = self.animations["rotatingLine"][self.direction][str(self.currentFrameIndex)]
                    clearLastLines()
                    print(f"{self.beforeMessage}{self.currentFrame}{self.afterMessage}")
                    time.sleep(self.delay)
                    self.currentFrameIndex += 1
            else:
                print("Invalid direction! Valid directions are 'right', and 'left'.")
                exit()

        elif self.animationType == 'growingDot':
            if self.direction == 'n/a':
                self.currentFrameIndex = 0
                while time.time() - startTime <= self.duration:
                    self.currentFrameIndex %= 4
                    self.currentFrame = self.animations["growingDot"][self.direction][str(self.currentFrameIndex)]
                    clearLastLines()
                    print(f"{self.beforeMessage}{self.currentFrame}{self.afterMessage}")
                    time.sleep(self.delay)
                    self.currentFrameIndex += 1
            else:
                print("Invalid direction! Valid direction is 'n/a'.")
                exit()

        elif self.animationType == 'jumpingDots':
            if self.direction == 'right' or self.direction == 'left':
                self.currentFrameIndex = 0
                while time.time() - startTime <= self.duration:
                    self.currentFrameIndex %= 3
                    self.currentFrame = self.animations["jumpingDots"][self.direction][str(self.currentFrameIndex)]
                    clearLastLines()
                    print(f"{self.beforeMessage}{self.currentFrame}{self.afterMessage}")
                    time.sleep(self.delay)
                    self.currentFrameIndex += 1
            else:
                print("Invalid direction! Valid direction is 'right', and 'left'.")
                exit()

        elif self.animationType == 'spinningCircle':
            if self.direction == 'right' or self.direction == 'left':
                self.currentFrameIndex = 0
                while time.time() - startTime <= self.duration:
                    self.currentFrameIndex %= 4
                    self.currentFrame = self.animations["spinningCircle"][self.direction][str(self.currentFrameIndex)]
                    clearLastLines()
                    print(f"{self.beforeMessage}{self.currentFrame}{self.afterMessage}")
                    time.sleep(self.delay)
                    self.currentFrameIndex += 1
            else:
                print("Invalid direction! Valid direction is 'right', and 'left'.")
                exit()
