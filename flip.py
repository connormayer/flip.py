#!/usr/bin/env python3

from argparse import ArgumentParser
from src.Flipbook import Flipbook

DEFAULT_ROWS = 0
DEFAULT_COLS = 0
DEFAULT_REPEAT = 1

if __name__ == "__main__":
    parser = ArgumentParser(description="Create a flipbook from GIFs.")
    parser.add_argument(
        'gif1', metavar='G1', type=str,  
        help="The filename of the first GIF to use."
    )
    parser.add_argument(
        'gif2', metavar='G2', type=str,
        help="The filename of the second GIF to use."
    )
    parser.add_argument(
        '--rows', type=int, default=DEFAULT_ROWS,
        help="The number of rows per page."
    )
    parser.add_argument(
        '--cols', type=int, default=DEFAULT_COLS,
        help="The number of columns per page. Ignored if rows provided."
    )
    parser.add_argument(
        '--repeat', type=int, default=DEFAULT_REPEAT,
        help="The number of times each animation should be repeated"
    )

    args = parser.parse_args()

    if args.rows > 0 and args.cols > 0:
        print("Cannot specify both number of rows and number of columns"
              "Only number of rows will be used.")

    flipbook = Flipbook(args)
    flipbook.create()
    pages = flipbook.get_all_pages()
    for i, page in enumerate(pages):
        page.save("output{}.png".format(i))
