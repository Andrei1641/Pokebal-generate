import argparse
import os
import random

from bitmap_calculate.frame import Frame
from bitmap_calculate.objects.figures import *
from bitmap_create.interface.body_and_head import Header, Body
from bitmap_create.objects.pixel import *
from bitmap_create.objects.win_body_head import WinHeader, WinBody
from bitmap_create.objects.file_IO import PictureCreator, PictureReader
def main():
    parser = argparse.ArgumentParser('Draws pokeball', add_help=False)
    parser.add_argument("path", help="place to generate a pokeball")
    parser.add_argument("-w", type=int, help="with of the bitmap")
    parser.add_argument("-h", type=int, help="height of the bitmap")
    parser.add_argument("-x", type=int, help="x position of the pokeball")
    parser.add_argument("-y", type=int, help="y position of the pokeball")
    parser.add_argument("-r", type=int, help="radius of the pokeball")
    parser.add_argument("--pokerush", help="generate random pokeballs in random places in random amount", action="store_true")
    args = parser.parse_args()


    address = args.path
    p = None
    if os.path.exists(address):
        p = PictureReader.get_calculate_pixels(address)

    #logic
    width: int = 200
    height: int = 200
    radius: int = 100
    x: int = 100
    y: int = 100

    if args.w:
        width = args.w
    if args.h:
        height = args.h
    if args.r:
        radius = args.r
    if args.x:
        x = args.x
    if args.y:
        y = args.y


    frame = Frame(width, height, pixels=p)

    if not args.pokerush:
        band_width: int = radius // 8
        frame.draw_circle(Point(x, y), radius, (255, 0, 0))
        frame.draw_circle(Point(x, y), radius, (255, 255, 255), True)
        frame.draw_rectangle(Point(x - radius, y - band_width // 2), 2 * radius, band_width, (0, 0, 0))
        frame.draw_circle(Point(x, y), band_width * 3, (0, 0, 0))
        frame.draw_circle(Point(x, y), band_width, (255, 255, 255))
    else:
        count: int = random.randint(10, 100)
        for _ in range(count):
            smaller: int = width if width <= height else height
            r = random.randint(10, smaller // 2)
            tmp_x = random.randint(0, width)
            tmp_y = random.randint(0, height)
            band_width_tmp: int = r // 8
            frame.draw_circle(Point(tmp_x, tmp_y), r, (255, 0, 0))
            frame.draw_circle(Point(tmp_x, tmp_y), r, (255, 255, 255), True)
            frame.draw_rectangle(Point(tmp_x - r, tmp_y - band_width_tmp // 2), 2 * r, band_width_tmp, (0, 0, 0))
            frame.draw_circle(Point(tmp_x, tmp_y), band_width_tmp * 3, (0, 0, 0))
            frame.draw_circle(Point(tmp_x, tmp_y), band_width_tmp, (255, 255, 255))

    #render
    normalized_render_pixels: list[Pixel] = frame.get_render_pixels()

    pixels: list[Pixel] = normalized_render_pixels
    win_body: Body = WinBody(pixels, width, height)

    win_header: Header = WinHeader(
        54 + (len(pixels) * 3), 0, 54, 40, win_body.get_width(), win_body.get_height(), 1, win_body.get_color_depth(), 0,
        (len(pixels) * 3), 0, 0, 0, 0
    )

    PictureCreator.write_file(win_header, win_body, address)

if __name__ == "__main__":
    main()