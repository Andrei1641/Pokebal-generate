import unittest

from bitmap_calculate.frame import Frame
from bitmap_calculate.objects.figures import Point
from bitmap_create.interface.body_and_head import Body, Header
from bitmap_create.interface.pixel import Pixel
from bitmap_create.objects.win_body_head import WinHeader, WinBody


class TestTranslateAttrInByteGetter(unittest.TestCase):
    def test_zero_attr(self):
        byte_getter = WinHeader._WinHeader__translate_attr_in_byte_getter(0, 2)
        self.assertEqual(byte_getter, [0, 0])

    def test_attr_multiple_bytes(self):
        byte_getter = WinHeader._WinHeader__translate_attr_in_byte_getter(256, 3)
        self.assertEqual(byte_getter, [0, 1, 0])


class TestGetColorDepth(unittest.TestCase):
    def test_24Bit(self):
        width: int = 10
        height: int = 10
        frame = Frame(width, height)
        frame.draw_point(Point(0,0), (255, 0, 0))   #24BitPixel
        normalized_render_pixels: list[Pixel] = frame.get_render_pixels()
        pixels: list[Pixel] = normalized_render_pixels

        win_body: Body = WinBody(pixels, width, height)
        color_depth: int = win_body.get_color_depth()
        self.assertEqual(color_depth, 24)