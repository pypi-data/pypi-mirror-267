class hex:
    def __init__(self, value):
        if not isinstance(value, str):
            raise TypeError("Hex code must be a string")
        if not value.startswith('#'):
            raise ValueError("Hex code must start with '#'")
        if not all(c in '0123456789abcdefABCDEF' for c in value[1:]):
            raise ValueError("Invalid hex characters")
        self.value = value
