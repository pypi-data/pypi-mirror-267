class CMDCircle:
    def __init__(self, *, sides: int, radius: int, color: str='#ffffff', hollow: bool):
        self.sides = sides
        self.radius = radius
        self.hollow = hollow

        def hexToAsciiColor(hex_color):
            if hex_color.startswith('#'):
                hex_color = hex_color[1:]

            try:
                r = int(hex_color[0:2], 16)
                g = int(hex_color[2:4], 16)
                b = int(hex_color[4:6], 16)

                ascii_color = f"\033[38;2;{r};{g};{b}m"
                ascii_reset = "\033[0m"
                return ascii_color, ascii_reset
            except ValueError:
                print("Invalid color code!")
                exit()

        ascii_color, ascii_reset = hexToAsciiColor(color)
        print(f"{ascii_color}")

        for y in range(-self.radius, self.radius + 1):
            for x in range(-self.radius, self.radius + 1):
                if self.point_in_polygon(x, y):
                    print("██", end="")
                else:
                    print("  ", end="")
            print()

        print(ascii_reset)

    def pointInPolygon(self, x, y):
        angle = 360 / self.sides
        for i in range(self.sides):
            x1 = self.radius * math.cos(math.radians(angle * i))
            y1 = self.radius * math.sin(math.radians(angle * i))
            x2 = self.radius * math.cos(math.radians(angle * (i + 1)))
            y2 = self.radius * math.sin(math.radians(angle * (i + 1)))

            if self.hollow:
                if self.isPointOnLine(x, y, x1, y1, x2, y2):
                    return True
            elif x ** 2 + y ** 2 <= self.radius ** 2:
                return True
        return False

    @staticmethod
    def isPointOnLine(px, py, x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1
        if dx == 0 and dy == 0:
            return False
        t = ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)
        x = x1 + t * dx
        y = y1 + t * dy
        return x1 <= x <= x2 and y1 <= y <= y2
