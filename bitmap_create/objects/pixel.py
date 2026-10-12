from bitmap_create.interface.pixel import Pixel
from tools import Translator


class Pixel24Bit(Pixel):

    @classmethod
    def get_color_depth(cls) -> int:
        return 24

    def __init__(self, red: int, green: int, blue: int):
        super().__init__(red, green, blue)
        self.__red = red
        self.__green = green
        self.__blue = blue


    def to_bytes(self) -> list[int]:
        pixel_in_bin: list[int] = []
        pixel_in_bin += Translator.from_int_to_bytes(self.__blue)
        pixel_in_bin += Translator.from_int_to_bytes(self.__green)
        pixel_in_bin += Translator.from_int_to_bytes(self.__red)
        return pixel_in_bin