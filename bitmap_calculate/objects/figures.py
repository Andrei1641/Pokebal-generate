from abc import ABC, abstractmethod


class Figure(ABC):
    @abstractmethod
    def calculate_point_side(self, point: Point) -> int:
        ...
    @abstractmethod
    def get_slope(self, x: float) -> None|float:
        ...

class Round(Figure):
    """
    f(x) = y_0 +- (r**2 - (x - x_0)**2)**0,5
    """
    def __init__(self, r: float, center: Point):
        self.__x_0: float = center.x
        self.__y_0: float = center.y
        self.__r = r

    def calculate_point_side(self, point: Point) -> int:
        if ((self.__x_0 - point.x)**2 + (self.__y_0 - point.y)**2)** 0.5 < self.__r:
            return -1
        else:
            return 1

    def get_slope(self, x: float = 0) -> None|float:
        """render doesn't need round's slope, it uses only second quadrant for calculations and then mirror the results"""
        return 1

    @property
    def x_0(self) -> float:
        return self.__x_0

    @property
    def y_0(self) -> float:
        return self.__y_0

    @property
    def r(self) -> float:
        return self.__r


class Line(Figure):
    """
    f(x) = mx + b
    """
    def __init__(self, point1: Point, point2: Point):
        self.__m: None|float = (point2.y - point1.y) / (point2.x - point1.x) if point2.x - point1.x != 0 else None
        self.__b: float = point1.y - self.__m * point1.x if self.__m else 0
        self.__x_borders: tuple[float, float] = (point1.x, point2.x) if point1.x < point2.x else (point2.x, point1.x)
        self.__y_borders: tuple[float, float] = (point1.y, point2.y) if point1.y < point2.y else (point2.y, point1.y)


    def get_slope(self, x: float = 0) -> None|float:
        return self.__m

    @property
    def x_borders(self) -> tuple[float, float]:
        return self.__x_borders

    @property
    def y_borders(self) -> tuple[float, float]:
        return self.__y_borders

    def calculate_point_side(self, point: Point) -> int:
        if self.__m:
            if point.y < self.__m * point.x + self.__b:
                return 1
            elif point.y > self.__m * point.x + self.__b:
                return -1
            else:
                return -1
        else:
            if point.x < self.__x_borders[0]:
                return -1
            elif point.x > self.__x_borders[0]:
                return 1
            else:
                return 1


class Point:
    def __init__(self, x: float, y: float):
        self.__x = x
        self.__y = y

    @property
    def x(self) -> float:
        return self.__x

    @x.setter
    def x(self, x: float):
        self.__x = x

    @property
    def y(self) -> float:
        return self.__y

    @y.setter
    def y(self, y: float):
        self.__y = y
