from bitmap_create.interface.body_and_head import Body, Header
from bitmap_create.objects.pixel import Pixel
from tools import CreationProver, Translator


class WinHeader(Header):
    def __init__(self, bfSize: int, bfReserved: int, bfOffbits: int, biSize: int, biWith: int, biHight: int,
                 biPlanes: int, biBitCount: int, biCompression: int, biSizeImage: int, biXPelsPerMeter: int,
                 biYPelsPerMeter: int, biClrUsed: int, biClrImportant: int):
        self.__bfType: int = 19778
        self.__set_bfSize(bfSize)
        self.__set_bfReserved(bfReserved)
        self.__set_bfOffBits(bfOffbits)

        self.__set_biSize(biSize)
        self.__set_biWidth(biWith)
        self.__set_biHeight(biHight)
        self.__set_biPlanes(biPlanes)
        self.__set_biBitCount(biBitCount)
        self.__set_biCompression(biCompression)
        self.__set_biSizeImage(biSizeImage)
        self.__set_biXPelsPerMeter(biXPelsPerMeter)
        self.__set_biYPelsPerMeter(biYPelsPerMeter)
        self.__set_biClrUsed(biClrUsed)
        self.__set_biClrImportant(biClrImportant)


    def get_header(self) -> list[int]:
        header_byte_list: list[int] = []
        header_byte_list += WinHeader.__translate_attr_in_byte_getter(self.__bfType, 2)
        header_byte_list += WinHeader.__translate_attr_in_byte_getter(self.__bfSize, 4)
        header_byte_list += WinHeader.__translate_attr_in_byte_getter(self.__bfReserved, 4)
        header_byte_list += WinHeader.__translate_attr_in_byte_getter(self.__bfOffBits, 4)
        header_byte_list += WinHeader.__translate_attr_in_byte_getter(self.__biSize, 4)
        header_byte_list += WinHeader.__translate_attr_in_byte_getter(self.__biWidth, 4)
        header_byte_list += WinHeader.__translate_attr_in_byte_getter(self.__biHeight, 4)
        header_byte_list += WinHeader.__translate_attr_in_byte_getter(self.__biPlanes, 2)
        header_byte_list += WinHeader.__translate_attr_in_byte_getter(self.__biBitCount, 2)
        header_byte_list += WinHeader.__translate_attr_in_byte_getter(self.__biCompression, 4)
        header_byte_list += WinHeader.__translate_attr_in_byte_getter(self.__biSizeImage, 4)
        header_byte_list += WinHeader.__translate_attr_in_byte_getter(self.__biXPelsPerMeter, 4)
        header_byte_list += WinHeader.__translate_attr_in_byte_getter(self.__biYPelsPerMeter, 4)
        header_byte_list += WinHeader.__translate_attr_in_byte_getter(self.__biClrUsed, 4)
        header_byte_list += WinHeader.__translate_attr_in_byte_getter(self.__biClrImportant, 4)
        return header_byte_list

    @staticmethod
    def __translate_attr_in_byte_getter(attr: int, bytes_border: int) -> list[int]:
        attr_bytes: list[int] = Translator.from_int_to_bytes(attr)
        attr_bytes_filled: list[int] = Translator.fill_bytes_border(attr_bytes, bytes_border)
        return Translator.translate_endian(attr_bytes_filled)

    def get_body_position(self) -> int:
        return self.__bfOffBits

    def get_width(self) -> int:
        return self.__biWidth

    def get_depth(self) -> int:
        return self.__biBitCount

    def __set_bfSize(self, bfSize: int):
        if CreationProver.is_out_of_border(4, bfSize):
            self.__bfSize = bfSize

    def __set_bfReserved(self, bfReserved: int):
        if CreationProver.is_out_of_border(4, bfReserved):
            self.__bfReserved = bfReserved


    def __set_bfOffBits(self, bfOffBits: int):
        if CreationProver.is_out_of_border(4, bfOffBits):
            self.__bfOffBits = bfOffBits


    def __set_biSize(self, biSize: int):
        if CreationProver.is_out_of_border(4, biSize):
            self.__biSize = biSize


    def __set_biWidth(self, biWidth: int):
        if CreationProver.is_out_of_border(4, biWidth):
            self.__biWidth = biWidth


    def __set_biHeight(self, biHeight: int):
        if CreationProver.is_out_of_border(4, biHeight):
            self.__biHeight = biHeight


    def __set_biPlanes(self, biPlanes: int):
        if CreationProver.is_out_of_border(2, biPlanes):
            self.__biPlanes = biPlanes


    def __set_biBitCount(self, biBitCoutn: int):
        if CreationProver.is_out_of_border(2, biBitCoutn):
            self.__biBitCount = biBitCoutn


    def __set_biCompression(self, biCompression: int):
        if CreationProver.is_out_of_border(4, biCompression):
            self.__biCompression = biCompression


    def __set_biSizeImage(self, biSizeImage: int):
        if CreationProver.is_out_of_border(4, biSizeImage):
            self.__biSizeImage = biSizeImage


    def __set_biXPelsPerMeter(self, biXPelsPerMeter: int):
        if CreationProver.is_out_of_border(4, biXPelsPerMeter):
            self.__biXPelsPerMeter = biXPelsPerMeter


    def __set_biYPelsPerMeter(self, biYPelsPerMeter: int):
        if CreationProver.is_out_of_border(4, biYPelsPerMeter):
            self.__biYPelsPerMeter = biYPelsPerMeter


    def __set_biClrUsed(self, biClrUsed: int):
        if CreationProver.is_out_of_border(4, biClrUsed):
            self.__biClrUsed = biClrUsed


    def __set_biClrImportant(self, biClrImportant: int):
        if CreationProver.is_out_of_border(4, biClrImportant):
            self.__biClrImportant = biClrImportant


class WinBody(Body):
    def __init__(self, pixels: list[Pixel], width: int, height: int):
        self.__pixels = pixels
        self.__width = width
        self.__height = height

    def get_body(self) -> list[int]:
        bytes_per_pixel = self.get_color_deph() // 8
        row_bytes = self.get_width() * bytes_per_pixel
        padding_per_row = (4 - (row_bytes % 4)) % 4
        padding_per_row_in_byte = [0] * padding_per_row
        pixels: list[Pixel] = self.pixels
        pixels_in_bytes: list[int] = []
        row_pixel_counter = 0
        for pixel in pixels:
            pixels_in_bytes += pixel.to_bytes()
            row_pixel_counter += 1
            if row_pixel_counter == self.get_width():
                pixels_in_bytes += padding_per_row_in_byte
                row_pixel_counter = 0
        return pixels_in_bytes


    def get_color_deph(self) -> int:
        return type(self.__pixels[0]).get_color_depth()


    def get_height(self) -> int:
        return self.__height


    def get_width(self) -> int:
        return self.__width

    @property
    def pixels(self) -> list[Pixel]:
        return self.__pixels