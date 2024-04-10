import math

class CMDNonogon:
    def __init__(self, *, radius: int, color: str='#ffffff', hollow: bool, orientation: str):
        self.radius = radius
        self.hollow = hollow
        self.orientation = orientation.lower()

        if self.orientation not in ['up', 'down', 'left', 'right']:
            raise ValueError("Orientation must be one of: 'up', 'down', 'left', 'right'.")

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

        if self.orientation == 'down':
            for y in range(self.radius, -self.radius - 1, -1):
                for x in range(-self.radius, self.radius + 1):
                    if self.hollow and self.pointOnEdge(x, y):
                        print("██", end="")
                    elif not self.hollow and self.pointInNonogon(x, y):
                        print("██", end="")
                    else:
                        print("  ", end="")
                print()

        elif self.orientation == 'up':
            for y in range(-self.radius, self.radius + 1):
                for x in range(-self.radius, self.radius + 1):
                    if self.hollow and self.pointOnEdge(x, y):
                        print("██", end="")
                    elif not self.hollow and self.pointInNonogon(x, y):
                        print("██", end="")
                    else:
                        print("  ", end="")
                print()

        elif self.orientation == 'left':
            for x in range(self.radius, -self.radius - 1, -1):
                for y in range(-self.radius, self.radius + 1):
                    if self.hollow and self.pointOnEdge(x, y):
                        print("██", end="")
                    elif not self.hollow and self.pointInNonogon(x, y):
                        print("██", end="")
                    else:
                        print("  ", end="")
                print()
        elif self.orientation == 'right':
            for x in range(-self.radius, self.radius + 1):
                for y in range(self.radius, -self.radius - 1, -1):
                    if self.hollow and self.pointOnEdge(x, y):
                        print("██", end="")
                    elif not self.hollow and self.pointInNonogon(x, y):
                        print("██", end="")
                    else:
                        print("  ", end="")
                print()
        print(asciiReset)

    def pointInNonogon(self, x, y):
        vertices = [
            (self.radius * math.cos(math.radians(angle)), self.radius * math.sin(math.radians(angle)))
            for angle in range(30, 410, 40)
        ]
        return self.isPointInPolygon(x, y, vertices)

    def pointOnEdge(self, x, y):
        return self.pointInNonogon(x, y) and (not self.pointInNonogon(x-1, y) or not self.pointInNonogon(x+1, y) or not self.pointInNonogon(x, y-1) or not self.pointInNonogon(x, y+1))

    @staticmethod
    def isPointInPolygon(x, y, polygonPoints):
        n = len(polygonPoints)
        inside = False
        p1x, p1y = polygonPoints[0]
        for i in range(n + 1):
            p2x, p2y = polygonPoints[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside
