import unittest

from tools import Translator, CreationProver


class TestTranslatorNumberOfBitsToRepresentNumber(unittest.TestCase):
    def test_number_is_zero(self):
        answer = Translator.get_number_of_bits_to_represent_number(0)
        self.assertEqual(0, answer)

    def test_number_is_one(self):
        answer = Translator.get_number_of_bits_to_represent_number(1)
        self.assertEqual(1, answer)

    def test_positive_number(self):
        answer = Translator.get_number_of_bits_to_represent_number(50)
        self.assertEqual(6, answer)

    def test_negative_number(self):
        with self.assertRaisesRegex(ValueError, "please write only positive number"):
            Translator.get_number_of_bits_to_represent_number(-5)


class TestTranslatorFromIntToBytes(unittest.TestCase):
    def test_number_is_zero(self):
        answer = Translator.from_int_to_bytes(0)
        self.assertEqual([0], answer)

    def test_positive_number_with_multiple_bytes(self):
        answer = Translator.from_int_to_bytes(300)
        self.assertEqual([1, 44], answer)

    def test_negative_number(self):
        with self.assertRaisesRegex(ValueError, "please write only positive number"):
            Translator.from_int_to_bytes(-300)

class TestTranslatorFromBytesToInt(unittest.TestCase):
    def test_byte_is_zero(self):
        answer = Translator.from_bytes_to_int([0])
        self.assertEqual(0, answer)

    def test_multiple_bytes(self):
        answer = Translator.from_bytes_to_int([1, 44])
        self.assertEqual(300, answer)

    def test_byte_part_is_negative(self):
        with self.assertRaises(ValueError):
            Translator.from_bytes_to_int([1, -44])

class TestTranslatorTranslateEndian(unittest.TestCase):
    def test_one_byte(self):
        answer = Translator.translate_endian([2])
        self.assertEqual([2], answer)

    def test_multiple_bytes(self):
        answer = Translator.translate_endian([1, 44])
        self.assertEqual([44, 1], answer)

class TestTranslatorFillBytesBorder(unittest.TestCase):
    def test_filled_border(self):
        answer = Translator.fill_bytes_border([1, 44], 2)
        self.assertEqual([1, 44], answer)

    def test_fill_empty(self):
        answer = Translator.fill_bytes_border([0], 2)
        self.assertEqual([0, 0], answer)

    def test_fill_standard_case(self):
        answer = Translator.fill_bytes_border([1, 44], 4)
        self.assertEqual([0, 0, 1, 44], answer)

class CreationProverIsOutOfBorder(unittest.TestCase):
    def test_bigger(self):
        number = 256
        with self.assertRaisesRegex(ValueError, f"false number {number}"):
            CreationProver.is_out_of_border(1, number)

    def test_negative_number(self):
        number = -1
        with self.assertRaisesRegex(ValueError, f"false number {number}"):
            CreationProver.is_out_of_border(1, number)

    def test_inside(self):
        answer = CreationProver.is_out_of_border(2, 256)
        self.assertTrue(answer)
