#!/usr/bin/env python3

from argparse import ArgumentParser
from os.path import join
from src.Flipbook import Flipbook

DEFAULT_ROWS = 0
DEFAULT_COLS = 0
DEFAULT_REPEAT = 1
DEFAULT_DIR = '.'
DEFAULT_PAGE_HEIGHT = 8.5
DEFAULT_PAGE_WIDTH = 11.0
DEFAULT_DPI = 300
DEFAULT_MARGIN = 0.5

FILENAME = 'output-{}-{}.png'

if __name__ == '__main__':
    parser = ArgumentParser(description='Create a flipbook from GIFs.')
    parser.add_argument(
        'gif1', metavar='G1', type=str,  
        help='The filename of the first GIF to use.'
    )
    parser.add_argument(
        'gif2', metavar='G2', type=str, nargs='?', default='',
        help='The filename of the second GIF to use.'
    )
    parser.add_argument(
        '-r', '--rows', type=int, default=DEFAULT_ROWS,
        help='The number of rows per page.'
    )
    parser.add_argument(
        '-c', '--cols', type=int, default=DEFAULT_COLS,
        help='The number of columns per page. Ignored if rows provided.'
    )
    parser.add_argument(
        '--repeat', type=int, default=DEFAULT_REPEAT,
        help='The number of times each animation should be repeated.'
    )
    parser.add_argument(
        '-d', '--dir', type=str, default=DEFAULT_DIR,
        help='The directory in which the files should be saved.'
    )
    parser.add_argument(
        '--page_height', type=float, default=DEFAULT_PAGE_HEIGHT,
        help='The height of the page in inches.'
    )
    parser.add_argument(
        '--page_width', type=float, default=DEFAULT_PAGE_WIDTH,
        help='The width of the page in inches.'
    )
    parser.add_argument(
        '--dpi', type=int, default=DEFAULT_DPI,
        help='The DPI of the produced images.'
    )
    parser.add_argument(
        '--margin', type=float, default=DEFAULT_MARGIN,
        help='The size of the page margin in inches.'
    )

    args = parser.parse_args()

    if args.rows > 0 and args.cols > 0:
        print('Cannot specify both number of rows and number of columns'
              'Only number of rows will be used.')

    flipbook = Flipbook(args)
    flipbook.create()
    pages = flipbook.get_grouped_pages()
    filename = join(args.dir, FILENAME)
    for i, page in enumerate(pages[0]):
        page.save(filename.format('a', i))
    for i, page in enumerate(pages[1]):
        page.save(filename.format('b', i))
