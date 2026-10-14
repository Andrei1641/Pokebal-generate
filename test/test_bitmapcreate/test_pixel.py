import unittest

from bitmap_create.objects.pixel import Pixel24Bit


class Test24Bit(unittest.TestCase):
    def setUp(self) -> None:
        self.pixel: Pixel24Bit = Pixel24Bit(0, 100, 255)

    def test_get_color_depth(self):
        self.assertEqual(self.pixel.get_color_depth(), 24)

    def test_to_bytes(self):
        pixel_in_bin = self.pixel.to_bytes()
        self.assertEqual(pixel_in_bin, [255, 100, 0])