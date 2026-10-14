import unittest

from bitmap_calculate.objects.pixel import PixelXXBit, PixelAdapter
from bitmap_create.interface.pixel import Pixel
from bitmap_create.objects.pixel import Pixel24Bit



class TestPixelXXBit(unittest.TestCase):
    def test_set_biggest_number(self):
        pixel1: PixelXXBit = PixelXXBit(50, 60, 0)
        self.assertEqual(PixelXXBit.get_biggest_number(), 60)
        pixel2: PixelXXBit = PixelXXBit(100, 0, 0)
        self.assertEqual(PixelXXBit.get_biggest_number(), 100)


    def test_mul(self):
        pixel1: PixelXXBit = PixelXXBit(50, 60, 0)
        p_list: list[PixelXXBit] = pixel1 * 5

        self.assertEqual(len(p_list), 5)
        self.assertEqual(p_list[-1].red, 50)
        self.assertEqual(p_list[-1].green, 60)
        self.assertEqual(p_list[-1].blue, 0)

        self.assertFalse(p_list[0] is p_list[1])

class TestFindNeededDepth(unittest.TestCase):
    def test_unexpected_bit_depth(self):
        calculate_pixel: list[list[PixelXXBit]] = [[PixelXXBit(500, 60, 0), PixelXXBit(50, 60, 0)],
                                                   [PixelXXBit(50, 60, 0), PixelXXBit(50, 60, 0)]]
        adapter: PixelAdapter = PixelAdapter(calculate_pixel)
        with self.assertRaisesRegex(ValueError, "there is no such bit-depth 500 to represent picture"):
            adapter._PixelAdapter__find_needed_depth()

    def test_standard_case(self):
        calculate_pixel: list[list[PixelXXBit]] = [[PixelXXBit(100, 60, 0), PixelXXBit(50, 60, 0)],
                                                   [PixelXXBit(50, 60, 0), PixelXXBit(50, 60, 0)]]
        adapter: PixelAdapter = PixelAdapter(calculate_pixel)
        render_pixel = adapter._PixelAdapter__find_needed_depth_render_pixel()
        self.assertEqual(render_pixel, Pixel24Bit)

class TestTranslateCalculateToRenderPixels(unittest.TestCase):
    def test_standard_case(self):
        calculate_pixel: list[list[PixelXXBit]] = [[PixelXXBit(100, 60, 0), PixelXXBit(50, 60, 0)],
                                                   [PixelXXBit(50, 60, 0), PixelXXBit(50, 60, 0)]]
        adapter: PixelAdapter = PixelAdapter(calculate_pixel)
        translated_pixels: list[list[Pixel]] = adapter.translate_calculate_to_render_pixels()
        self.assertTrue(issubclass(type(translated_pixels[0][0]), Pixel24Bit))

class TestNormalizePixels(unittest.TestCase):
    def test_standard_case(self):
        render_pixels: list[list[Pixel]] = [[Pixel24Bit(100, 60, 0), Pixel24Bit(50, 60, 0)],
                                                   [Pixel24Bit(50, 60, 0), Pixel24Bit(50, 60, 0)]]

        normalized_pixels = PixelAdapter.normalize_pixels(render_pixels)
        self.assertEqual(len(normalized_pixels), 4)
        self.assertTrue( isinstance(normalized_pixels[0], Pixel24Bit))