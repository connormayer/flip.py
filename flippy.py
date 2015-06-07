#!/usr/bin/env python3

from argparse import ArgumentParser
from src.Flipbook import Flipbook

DEFAULT_ROWS = 4
DEFAULT_COLS = 6

if __name__ == "__main__":
	parser = ArgumentParser(description="Create a flipbook from GIFs.")
	parser.add_argument('gif1', metavar='G1', type=str, 
						help="The filename of the first GIF to use.")
	parser.add_argument('gif2', metavar='G2', type=str,
						help="The filename of the second GIF to use.")
	parser.add_argument('--rows', type=int, default=DEFAULT_ROWS,
						help="The number of rows per page.")
	parser.add_argument('--cols', type=int, default=DEFAULT_COLS,
						help="The number of columns per page.")

	args = parser.parse_args()

	flipbook = Flipbook(args.gif1, args.gif2, args.rows, args.cols)
	flipbook.create()
	pages = flipbook.getPages()
	for i, page in enumerate(pages):
		page.save("output{}.png".format(i))
