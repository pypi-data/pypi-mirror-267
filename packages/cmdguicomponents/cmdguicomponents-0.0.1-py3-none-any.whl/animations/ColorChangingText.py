import time
import sys

class CMDColorChangingText:
    def __init__(self, *, text: str, colors: list, transitionDelay: float, loop: bool, mode: str):
        def rgbToANSI(rgbColor):
            if rgbColor.startswith('#') and len(rgbColor) == 7:
                try:
                    r = int(rgbColor[1:3], 16)
                    g = int(rgbColor[3:5], 16)
                    b = int(rgbColor[5:], 16)
                    return f'\033[38;2;{r};{g};{b}m'
                except ValueError:
                    pass
            return ''

        def fadeColors(startColor, endColor, steps):
            startRGB = [int(startColor[i:i+2], 16) for i in range(1, 7, 2)]
            endRGB = [int(endColor[i:i+2], 16) for i in range(1, 7, 2)]
            stepSize = [(endRGB[i] - startRGB[i]) / steps for i in range(3)]
            currentRGB = startRGB.copy()
            for _ in range(steps):
                currentRGB = [int(currentRGB[i] + stepSize[i]) for i in range(3)]
                yield f'#{currentRGB[0]:02x}{currentRGB[1]:02x}{currentRGB[2]:02x}'

        def colorChangingTextAnimation(text: str, colors: list, transitionDelay: float, loop: bool, mode: str):
            colorAmount = len(colors)
            index = 0
            mode = mode.lower()
            if mode == 'solid':
                while loop:
                    currentColorRGB = colors[index % colorAmount]
                    currentColorANSI = rgbToANSI(currentColorRGB)
                    sys.stdout.write(f"\r{currentColorANSI}{text}\033[m")
                    sys.stdout.flush()
                    time.sleep(transitionDelay)
                    index += 1
            elif mode == 'fade':
                while loop:
                    startColor = colors[index % colorAmount]
                    endColor = colors[(index + 1) % colorAmount]
                    for color in fadeColors(startColor, endColor, int(transitionDelay * 10)):
                        currentColorANSI = rgbToANSI(color)
                        sys.stdout.write(f"\r{currentColorANSI}{text}\033[m")
                        sys.stdout.flush()
                        time.sleep(transitionDelay)
                    index += 1
            else:
                print("Unknown mode. Please choose 'solid' or 'fade'.")

        colorChangingTextAnimation(text, colors, transitionDelay, loop, mode)
