from copy import deepcopy

from bitmap_calculate.objects.figures import Point, Line, Figure, Round
from bitmap_calculate.objects.pixel import PixelXXBit, PixelAdapter
from bitmap_create.interface.pixel import Pixel


class Frame:
    def __init__(self, width: int, height: int, *, pixels: list[list[PixelXXBit]]| None = None):
        self.__pixels: list[list[PixelXXBit]] = [] #y x    size is 1X1
        if not pixels:
            for _ in range(height):
                self.__pixels.append(PixelXXBit(0,0,0) * width)
        else:
            tmp_pixels = deepcopy(pixels)
            if len(tmp_pixels) > height:
                tmp_pixels = tmp_pixels[:height]
            elif len(tmp_pixels) < height:
                for _ in range(height - len(tmp_pixels)):
                    tmp_pixels.append(PixelXXBit(0,0,0) * width)

            for i in range(len(tmp_pixels)):
                if len(tmp_pixels[i]) > width:
                    tmp_pixels[i] = tmp_pixels[i][:width]
                elif len(tmp_pixels[i]) < width:
                    tmp_pixels[i] = tmp_pixels[i] + PixelXXBit(0,0,0) * (width - len(tmp_pixels[i]))

            self.__pixels = tmp_pixels


    def get_render_pixels(self) -> list[Pixel]:
        adapter: PixelAdapter = PixelAdapter(self.__pixels)
        render_pixels: list[list[Pixel]] = adapter.translate_calculate_to_render_pixels()
        normalized_render_pixels: list[Pixel] = adapter.normalize_pixels(render_pixels)
        return normalized_render_pixels

    def draw_point(self, point: Point, color: tuple[int,int,int]):
        selected_pixel: PixelXXBit = self.__pixels[round(point.y)][round(point.x)]
        selected_pixel.set_color(color)


    def draw_rectangle(self, position: Point, width: int, height: int, color: tuple[int,int,int]):
        for i in range(height):
            self.draw_line(Line(Point(position.x, position.y + i), Point(position.x + width, position.y + i)), color)

    def draw_circle(self, center: Point, radius: int, color: tuple[int,int,int], half = False):
        circle: Round = Round(radius, center)
        tmp_point: Point = Point(circle.x_0, circle.y_0 - circle.r)
        circle_edge_points_bellow: list[tuple[Point, Point]] = [(tmp_point, tmp_point)]
        circle_edge_points_upper: list[tuple[Point, Point]] = [(Frame.mirror_point(tmp_point, y=circle.y_0), Frame.mirror_point(tmp_point, y=circle.y_0))]
        while tmp_point.y <= circle.y_0:
            tmp_point = Frame.find_next_point(tmp_point, circle)
            mirrored_x = Frame.mirror_point(tmp_point, x=circle.x_0)
            mirrored_y = Frame.mirror_point(tmp_point, y=circle.y_0)
            mirrored_x_y = Frame.mirror_point(mirrored_x, y=circle.y_0)
            circle_edge_points_bellow.append((mirrored_x, tmp_point))
            circle_edge_points_upper.append((mirrored_x_y, mirrored_y))

        for borders in circle_edge_points_bellow:
            tmp_line: Line = Line(borders[0], borders[1])
            self.draw_line(tmp_line, color)

        if not half:
            for borders in circle_edge_points_upper:
                tmp_line: Line = Line(borders[0], borders[1])
                self.draw_line(tmp_line, color)

    @staticmethod
    def mirror_point(point: Point, *, x: float|None = None, y: float|None = None) -> Point:
        if x is not None and y is None:
            return Point(2 * x - point.x, point.y)
        elif y is not None and x is None:
            return Point(point.x, 2 * y - point.y)
        else:
            raise ValueError('select only one line')

    def draw_line(self, line: Line, color: tuple[int,int,int]):
        tmp_point: Point = Point(line.x_borders[0], line.y_borders[0])
        bigger_borders: tuple[float, float] = line.x_borders if line.x_borders[1] - line.x_borders[0] > line.y_borders[1] - line.y_borders[0] else line.y_borders
        for i in range(round(bigger_borders[0]), round(bigger_borders[1])):
            try:
                tmp_pixel: PixelXXBit = self.__pixels[round(tmp_point.y)][round(tmp_point.x)]
                tmp_pixel.set_color(color)
            except IndexError:
                pass
            tmp_point = Frame.find_next_point(tmp_point, line)


    @staticmethod
    def find_next_point(point: Point, figure: Figure) -> Point:
        """search next pixel from left to right(from bottom to top)"""
        point_side = figure.calculate_point_side(point)
        slope = figure.get_slope(point.x)
        if slope is None:
            return Point(point.x, point.y + 1)
        elif slope < 0 and point_side == -1:
            return Point(point.x + 1, point.y)
        elif slope < 0 and point_side == 1:
            return Point(point.x, point.y - 1)
        elif slope > 0 and point_side == -1:
            return Point(point.x + 1, point.y)
        elif slope > 0 and point_side == 1:
            return Point(point.x, point.y + 1)
        elif slope == 0:
            return Point(point.x + 1, point.y)
        else:
            return Point(point.x, point.y + 1)