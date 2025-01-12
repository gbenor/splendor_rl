from dataclasses import dataclass


@dataclass
class Tokens:
    red: int = 0
    green: int = 0
    blue: int = 0
    white: int = 0
    black: int = 0
    gold: int = 0  # Gold tokens are wildcards

    def __add__(self, other):
        if not isinstance(other, Tokens):
            return NotImplemented
        return Tokens(
            red=self.red + other.red,
            green=self.green + other.green,
            blue=self.blue + other.blue,
            white=self.white + other.white,
            black=self.black + other.black,
            gold=self.gold + other.gold
        )

    def __sub__(self, other):
        if not isinstance(other, Tokens):
            return NotImplemented
        return Tokens(
            red=self.red - other.red,
            green=self.green - other.green,
            blue=self.blue - other.blue,
            white=self.white - other.white,
            black=self.black - other.black,
            gold=self.gold - other.gold
        )

    @property
    def count(self):
        """Returns the total count of all tokens."""
        return self.red + self.green + self.blue + self.white + self.black + self.gold

    def __repr__(self):
        return (f"Tokens(red={self.red}, green={self.green}, blue={self.blue}, "
                f"white={self.white}, black={self.black}, gold={self.gold})")
