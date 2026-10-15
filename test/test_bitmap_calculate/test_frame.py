import unittest

from bitmap_calculate.frame import Frame
from bitmap_calculate.objects.figures import Line, Point

class TestFrameInit(unittest.TestCase):
    def test_standard_case(self):
        frame: Frame = Frame(10, 10)
        self.assertEqual(len(frame._Frame__pixels), 10)
        self.assertEqual(len(frame._Frame__pixels[0]), 10)




class TestFindNextPoint(unittest.TestCase):
    #if point on the figure find_next_point() has the same algorithm as by right(upper) point
    def test_positive_slope(self):
        positive_line: Line = Line(Point(0,0), Point(1,1))

        left_point: Point = Point(-1, 0)
        left_point = Frame.find_next_point(left_point, positive_line)
        self.assertEqual(round(left_point.x), 0)

        right_point: Point = Point(1, 0)
        right_point = Frame.find_next_point(right_point, positive_line)
        self.assertEqual(round(right_point.y), 1)

    def test_negative_slope(self):
        negative_line: Line = Line(Point(0, 1), Point(1, 0))

        left_point: Point = Point(-1, 0)
        left_point = Frame.find_next_point(left_point, negative_line)
        self.assertEqual(round(left_point.x), 0)

        right_point: Point = Point(2, 0)
        right_point = Frame.find_next_point(right_point, negative_line)
        self.assertEqual(round(right_point.y), -1)

    def test_none_slope(self):
        #none line can grow up only vertical
        none_line: Line = Line(Point(0, 0), Point(0, 1))

        left_point: Point = Point(-1, 0)
        left_point = Frame.find_next_point(left_point, none_line)
        self.assertEqual(round(left_point.y), 1)

        right_point: Point = Point(1, 0)
        right_point = Frame.find_next_point(right_point, none_line)
        self.assertEqual(round(right_point.y), 1)

    def test_zero_slope(self):
        #zero line can grow up only horizontal
        zero_line: Line = Line(Point(0, 0), Point(1, 0))

        point_below: Point = Point(0, -1)
        point_below = Frame.find_next_point(point_below, zero_line)
        self.assertEqual(round(point_below.x), 1)

        point_upper: Point = Point(0, 1)
        point_upper = Frame.find_next_point(point_upper, zero_line)
        self.assertEqual(round(point_upper.x), 1)

class TestDrawPoint(unittest.TestCase):
    def setUp(self) -> None:
        self.frame = Frame(10, 10)

    def test_out_of_border(self):
        self.frame.draw_point(Point(-5, 0), (255, 0, 0))

    def test_standard_case(self):
        self.frame.draw_point(Point(1, 1), (255, 0, 0))
        self.assertEqual(self.frame._Frame__pixels[1][1].red, 255)

class TestDrawLine(unittest.TestCase):
    def setUp(self) -> None:
        self.frame = Frame(10, 10)

    def test_out_of_border(self):
        self.frame.draw_line(Line(Point(-1, -1), Point(9, 9)), (255, 0, 0))
        self.assertEqual(self.frame._Frame__pixels[0][0].red, 255)
        self.assertEqual(self.frame._Frame__pixels[8][8].red, 255)
        self.assertEqual(self.frame._Frame__pixels[5][5].red, 255)

    def test_standard_case(self):
        self.frame.draw_line(Line(Point(1, 1), Point(9, 9)), (255, 0, 0))
        self.assertEqual(self.frame._Frame__pixels[2][2].red, 255)

class TestDrawRectangle(unittest.TestCase):
    def setUp(self) -> None:
        self.frame = Frame(10, 10)

    def test_standard_case(self):
        self.frame.draw_rectangle(Point(0, 0), 5, 5, (255, 0, 0))
        self.assertEqual(self.frame._Frame__pixels[1][1].red, 255)

    def test_out_of_border(self):
        self.frame.draw_rectangle(Point(-1, -1), 5, 5, (255, 0, 0))
        self.assertEqual(self.frame._Frame__pixels[1][1].red, 255)

class TestMirrorPoint(unittest.TestCase):
    def test_mirror_x(self):
        point_reight: Point = Point(5, 0)
        tmp_point: Point = Frame.mirror_point(point_reight, x=1)
        self.assertEqual(round(tmp_point.x), -3)
        point_left: Point = Point(-5, 0)
        tmp_point = Frame.mirror_point(point_left, x=1)
        self.assertEqual(round(tmp_point.x), 7)

    def test_mirror_y(self):
        point_upper: Point = Point(0, 5)
        tmp_point: Point = Frame.mirror_point(point_upper, y=1)
        self.assertEqual(round(tmp_point.y), -3)
        point_bellow: Point = Point(0, -5)
        tmp_point = Frame.mirror_point(point_bellow, y=1)
        self.assertEqual(round(tmp_point.y), 7)

    def test_mirror_xy(self):
        point: Point = Point(1, 1)
        tmp_point: Point = Frame.mirror_point(point, x=0, y=0)
        self.assertEqual(round(tmp_point.x), -1)
        self.assertEqual(round(tmp_point.y), -1)

    def test_no_value_selected(self):
        with self.assertRaisesRegex(ValueError, "select at least one of x and y"):
            Frame.mirror_point(Point(0, 0))

class TestDrawCircle(unittest.TestCase):
    def setUp(self) -> None:
        self.frame = Frame(10, 10)

    def test_standard_case(self):
        self.frame.draw_circle(Point(5, 5),5, (255, 0, 0))
        self.assertEqual(self.frame._Frame__pixels[5][5].red, 255)
        self.assertEqual(self.frame._Frame__pixels[6][5].red, 255)
        self.assertEqual(self.frame._Frame__pixels[5][0].red, 255)

    def test_half(self):
        self.frame.draw_circle(Point(5, 5), 5, (255, 0, 0), True)
        self.assertEqual(self.frame._Frame__pixels[5][5].red, 255)
        self.assertEqual(self.frame._Frame__pixels[6][5].red, 0)
        with self.assertRaises(AssertionError):
            self.assertEqual(self.frame._Frame__pixels[4][5].red, 0)

class TestGetRenderPixels(unittest.TestCase):
    def test_standard_case(self):
        frame = Frame(10, 10)
        render_pixels = frame.get_render_pixels()
        self.assertEqual(len(render_pixels), 100)