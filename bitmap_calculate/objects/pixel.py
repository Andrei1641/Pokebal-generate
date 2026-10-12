from bitmap_create.objects.pixel import *
from tools import Translator


class PixelXXBit:
    """
    only for calculation purposes, not for render
    """
    __biggest_number: int = 0

    @classmethod
    def get_biggest_number(cls) -> int:
        return cls.__biggest_number

    @classmethod
    def __set_biggest_number(cls, number: int):
        PixelXXBit.__biggest_number = max(number, cls.__biggest_number)

    def __init__(self, red: int, green: int, blue: int):
        self.__red = 0
        self.__green = 0
        self.__blue = 0

        self.red = red
        self.green = green
        self.blue = blue

    @property
    def red(self) -> int:
        return self.__red

    @red.setter
    def red(self, red: int):
        self.__red = red
        PixelXXBit.__set_biggest_number(red)

    @property
    def green(self) -> int:
        return self.__green

    @green.setter
    def green(self, green: int):
        self.__green = green
        PixelXXBit.__set_biggest_number(green)

    @property
    def blue(self) -> int:
        return self.__blue

    @blue.setter
    def blue(self, blue: int):
        self.__blue = blue
        PixelXXBit.__set_biggest_number(blue)

    def set_color(self, color: tuple[int, int, int]):
        self.__red = color[0]
        self.__green = color[1]
        self.__blue = color[2]

    def __mul__(self, other: int):
        calculation_pixels: list[PixelXXBit] = []
        for _ in range(other):
            calculation_pixels.append(PixelXXBit(self.red, self.__green, self.__blue))
        return calculation_pixels

class PixelAdapter:
    def __init__(self, calculation_pixels: list[list[PixelXXBit]]):
        self.__pixel_classes: list[type[Pixel]] = [Pixel24Bit]   #sorted of Pixel classes by pixel depth (is changeable)
        self.__calculation_pixels = calculation_pixels


    def translate_calculate_to_render_pixels(self) -> list[list[Pixel]]:
        render_pixels: list[list[Pixel]] = []
        pixel_class: type[Pixel] = self.__find_needed_depth()
        for pixel_row in self.__calculation_pixels:
            tmp_render_pixels_row: list[Pixel] = []
            for pixel in pixel_row:
                tmp_render_pixels_row.append(pixel_class(pixel.red, pixel.green, pixel.blue))
            render_pixels.append(tmp_render_pixels_row)
        return render_pixels


    def __find_needed_depth(self) -> type[Pixel]:
        biggest_number = PixelXXBit.get_biggest_number()
        bits_to_represent_number = Translator.get_number_of_bits_to_represent_number(biggest_number)
        for pixel_class in self.__pixel_classes:
            if pixel_class.get_color_depth() // 3 >= bits_to_represent_number:
                return pixel_class
        raise ValueError(f'there is no such bit-depth {biggest_number} to represent picture')


    @staticmethod
    def normalize_pixels(render_pixels: list[list[Pixel]]) -> list[Pixel]:
        normalized_pixels: list[Pixel] = []
        for render_pixel in render_pixels:
            normalized_pixels += render_pixel
        return normalized_pixels



