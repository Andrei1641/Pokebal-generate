from abc import ABC, abstractmethod


class Body(ABC):
    @abstractmethod
    def get_body(self) -> list[int]:
        ...

    @abstractmethod
    def get_color_depth(self) -> int:
        ...

    @abstractmethod
    def get_width(self) -> int:
        ...

    @abstractmethod
    def get_height(self) -> int:
        ...

class Header(ABC):

    @staticmethod
    @abstractmethod
    def get_magic_number() -> bytes:
        ...

    @abstractmethod
    def set_header(self, b:bytes):
        ...

    @abstractmethod
    def get_header(self) -> list[int]:
        ...

    @abstractmethod
    def get_body_position(self) -> int:
        ...

    @abstractmethod
    def get_width(self) -> int:
        ...

    @abstractmethod
    def get_depth(self) -> int:
        ...