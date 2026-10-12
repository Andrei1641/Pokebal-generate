from abc import ABC, abstractmethod


class Pixel(ABC):
    def __init__(self, red: int, green: int, blue: int):
        ...

    @classmethod
    @abstractmethod
    def get_color_depth(cls) -> int:
        ...
    @abstractmethod
    def to_bytes(self) -> list[int]:
        ...