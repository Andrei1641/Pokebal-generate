import math

class Translator:
    @staticmethod
    def from_int_to_bytes(number: int) -> list[int]:
        number_of_bits: int = Translator.get_number_of_bits_to_represent_number(number)
        number_of_bytes: int = math.ceil(number_of_bits / 8)
        if not number_of_bytes: return [0]
        return list(number.to_bytes(number_of_bytes))

    @staticmethod
    def from_bytes_to_int(b: list[int]) -> int:
        number = int.from_bytes(bytes(b), byteorder="big")
        return number

    @staticmethod
    def get_number_of_bits_to_represent_number(number: int) -> int:
        if not number: return 0
        if number == 1: return 1
        return math.ceil(math.log(number, 2))

    @staticmethod
    def translate_endian(b: list[int]) -> list[int]:
        return b[::-1]

    @staticmethod
    def fill_bytes_border(attr_bytes: list[int], bytes_border: int):
        if len(attr_bytes) < bytes_border:
            attr_bytes = [0] * (bytes_border - len(attr_bytes)) + attr_bytes
        return attr_bytes


class CreationProver:
    @staticmethod
    def is_out_of_border(byte_number_border: int, number: int) -> bool:
        if 0 <= number < 2 ** (8 * byte_number_border):
            return True
        raise ValueError(f'false number {number}')