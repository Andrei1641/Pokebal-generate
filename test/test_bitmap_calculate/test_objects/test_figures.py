import unittest

from bitmap_calculate.objects.figures import Line, Point, Round


class TestLine(unittest.TestCase):
    def setUp(self) -> None:
        self.horizontal_line: Line = Line(Point(0,0), Point(0, 5))
        self.positive_slope_line: Line = Line(Point(0,0), Point(1, 1))
        self.negative_slope_line: Line = Line(Point(0, 1), Point(1, 0))
        self.constant_line: Line = Line(Point(0, 0), Point(1, 0))

    def test_init_slope(self):
        self.assertTrue(self.horizontal_line.get_slope(0) is None)
        self.assertTrue(self.positive_slope_line.get_slope(0) > 0)
        self.assertTrue(self.negative_slope_line.get_slope(0) < 0)
        self.assertTrue(self.constant_line.get_slope() == 0)

    def test_init_shift(self):
        self.assertEqual(self.horizontal_line._Line__b, 0)
        self.assertEqual(self.negative_slope_line._Line__b, 1)

    def test_set_borders(self):
        line = Line(Point(2, 0), Point(1, 0))
        self.assertEqual(line.x_borders, (1, 2))
        self.assertEqual(self.negative_slope_line.x_borders, (0, 1))

    def test_calculate_point_side(self):
        self.assertEqual(self.horizontal_line.calculate_point_side(Point(-1, 0)), -1)
        self.assertEqual(self.horizontal_line.calculate_point_side(Point(0, 0)), 1)
        self.assertEqual(self.horizontal_line.calculate_point_side(Point(1, 0)), 1)

        self.assertEqual(self.positive_slope_line.calculate_point_side(Point(-3, 0)), -1)
        self.assertEqual(self.positive_slope_line.calculate_point_side(Point(0, 0)), 1)
        self.assertEqual(self.positive_slope_line.calculate_point_side(Point(3, 0)), 1)

        self.assertEqual(self.negative_slope_line.calculate_point_side(Point(-3, 0)), -1)
        self.assertEqual(self.negative_slope_line.calculate_point_side(Point(1, 1)), 1)
        self.assertEqual(self.negative_slope_line.calculate_point_side(Point(3, 0)), 1)

        self.assertEqual(self.constant_line.calculate_point_side(Point(0, -1)), -1)
        self.assertEqual(self.constant_line.calculate_point_side(Point(0, 0)), 1)
        self.assertEqual(self.constant_line.calculate_point_side(Point(0, 1)), 1)

class TestRound(unittest.TestCase):
    def setUp(self) -> None:
        self.round: Round = Round(5, Point(0, 0))

    def test_get_slope(self):  #!!!
        self.assertEqual(self.round.get_slope(0), 1)

    def test_calculate_point_side(self):
        self.assertEqual(self.round.calculate_point_side(Point(-10, 0)), 1)
        self.assertEqual(self.round.calculate_point_side(Point(0, 0)), -1)
        self.assertEqual(self.round.calculate_point_side(Point(10, 0)), 1)
        self.assertEqual(self.round.calculate_point_side(Point(0, 10)), 1)
        self.assertEqual(self.round.calculate_point_side(Point(0, 10)), 1)