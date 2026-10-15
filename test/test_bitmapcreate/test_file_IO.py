import os
import unittest

from bitmap_calculate.frame import Frame
from bitmap_calculate.objects.figures import Point
from bitmap_calculate.objects.pixel import PixelXXBit
from bitmap_create.interface.body_and_head import Header, Body
from bitmap_create.interface.pixel import Pixel
from bitmap_create.objects.file_IO import PictureCreator, PictureReader
from bitmap_create.objects.win_body_head import WinHeader, WinBody

def create_file_obj() -> tuple[str, Body, Header]:
    file_address = "test\\file.bmp"
    width: int = 10
    height: int = 10

    frame = Frame(width, height)

    frame.draw_rectangle(Point(0, 0), width, height, (255, 255, 255))

    normalized_render_pixels: list[Pixel] = frame.get_render_pixels()
    pixels: list[Pixel] = normalized_render_pixels

    win_body: Body = WinBody(pixels, width, height)
    win_header: Header = WinHeader(
        54 + (len(pixels) * 3), 0, 54, 40, win_body.get_width(), win_body.get_height(), 1,
        win_body.get_color_depth(), 0,
        (len(pixels) * 3), 0, 0, 0, 0
    )
    return file_address, win_body, win_header

class TestPictureCreator(unittest.TestCase):   #!only win with 24Pixel depth!
    def setUp(self) -> None:
        self.file_address, self.win_body, self.win_header = create_file_obj()

    def tearDown(self) -> None:
        try:
            os.remove(self.file_address)
        except FileNotFoundError:
            ...

    def test_write_header(self):
        PictureCreator.write_file(self.win_header, self.win_body, self.file_address)
        expected_content = b'BMb\x01\x00\x00\x00\x00\x00\x006\x00\x00\x00(\x00\x00\x00\n\x00\x00\x00\n\x00\x00\x00\x01\x00\x18\x00\x00\x00\x00\x00,\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        with open(self.file_address, "rb") as f:
            content = f.read(54)

        self.assertEqual(expected_content, content)

    def test_write_body(self):
        PictureCreator.write_file(self.win_header, self.win_body, self.file_address)
        expected_content = (b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00'
                            b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00'
                            b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00'
                            b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00'
                            b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00'
                            b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00'
                            b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00'
                            b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00'
                            b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00'
                            b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00')
        with open(self.file_address, "rb") as f:
            f.seek(54)
            content = f.read()

        self.assertEqual(expected_content, content)


class TestPictureReaderFindPadding(unittest.TestCase):
    def test_24_depth(self):
        padding = PictureReader._PictureReader__find_padding(24, 10)
        self.assertEqual(2, padding)
        padding = PictureReader._PictureReader__find_padding(24, 4)
        self.assertEqual(0, padding)

    def test_32_depth(self):
        padding = PictureReader._PictureReader__find_padding(32, 6)
        self.assertEqual(0, padding)

class TestReadHeader(unittest.TestCase):
    def setUp(self) -> None:
        self.file_address, self.win_body, self.win_header = create_file_obj()

    def tearDown(self) -> None:
        try:
            os.remove(self.file_address)
        except FileNotFoundError:
            ...

    def test_unexpected_magic_number(self):
        address: str = "test/test_bitmapcreate/file.txt"
        with open(address, "w") as f:
            f.write("info")
        with self.assertRaises(TypeError):
            PictureReader._PictureReader__read_header(address)
        os.remove(address)

    def test_standard_case(self):
        PictureCreator.write_file(self.win_header, self.win_body, self.file_address)
        header = PictureReader._PictureReader__read_header(self.file_address)
        self.assertTrue(issubclass(type(header), Header))

class TestReadWinHeader(unittest.TestCase):
    def setUp(self) -> None:
        self.file_address, self.win_body, self.win_header = create_file_obj()

    def tearDown(self) -> None:
        try:
            os.remove(self.file_address)
        except FileNotFoundError:
            ...

    def test_is_data_shifted(self):
        PictureCreator.write_file(self.win_header, self.win_body, self.file_address)
        win_header: WinHeader = PictureReader._PictureReader__read_win_header(self.file_address)

        self.assertEqual(54, win_header._WinHeader__bfOffBits)
        self.assertEqual(354, win_header._WinHeader__bfSize)
        self.assertEqual(10, win_header._WinHeader__biWidth)

class TestReadRawBody(unittest.TestCase):
    def setUp(self) -> None:
        self.file_address, self.win_body, self.win_header = create_file_obj()

    def tearDown(self) -> None:
        try:
            os.remove(self.file_address)
        except FileNotFoundError:
            ...

    def test_standard_case(self):
        PictureCreator.write_file(self.win_header, self.win_body, self.file_address)
        expected_raw_body = (b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00'
                            b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00'
                            b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00'
                            b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00'
                            b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00'
                            b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00'
                            b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00'
                            b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00'
                            b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00'
                            b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00')

        raw_body = PictureReader._PictureReader__read_raw_body(self.file_address, self.win_header)
        self.assertEqual(raw_body, expected_raw_body)

class TestCreateCalculatePixels(unittest.TestCase):
    def test_unexpected_header(self):
        class SomeHeader(Header):
            @staticmethod
            def get_magic_number() -> bytes:
                pass
            def set_header(self, b: bytes):
                pass
            def get_header(self) -> list[int]:
                pass
            def get_body_position(self) -> int:
                pass
            def get_width(self) -> int:
                pass
            def get_depth(self) -> int:
                pass
        header: SomeHeader = SomeHeader()
        with self.assertRaisesRegex(TypeError, f'unexpected header type {type(header)}'):
            PictureReader._PictureReader__create_calculate_pixels(b'', header)

    def setUp(self) -> None:
        self.file_address, self.win_body, self.win_header = create_file_obj()

    def tearDown(self) -> None:
        try:
            os.remove(self.file_address)
        except FileNotFoundError:
            ...

    def test_standard_case(self):
        raw_body = (b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00'
                            b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00'
                            b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00'
                            b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00'
                            b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00'
                            b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00'
                            b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00'
                            b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00'
                            b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00'
                            b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00')
        calculate_pixels: list[list[PixelXXBit]] = PictureReader._PictureReader__create_calculate_pixels(raw_body, self.win_header)
        self.assertEqual(len(calculate_pixels[0]), 10)
        self.assertEqual(len(calculate_pixels), 10)
        self.assertEqual(calculate_pixels[9][9].red, 255)
        self.assertEqual(calculate_pixels[9][9].green, 255)
        self.assertEqual(calculate_pixels[9][9].blue, 255)