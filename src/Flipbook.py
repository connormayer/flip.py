from math import ceil
from PIL import Image, ImageDraw

# in pixels
DEFAULT_DPI = 300

# in inches
PAGE_HEIGHT = 8.5
PAGE_WIDTH = 11
MARGIN_SIZE = 0.5

WHITE = (255, 255, 255, 255)
BLACK = (0, 0, 0, 255)

# TODO: figure out which page orientation is better
# TODO: alternating pages or double sided


class Flipbook(object):
	def __init__(self, gif1, gif2, rows, cols):
		assert rows > 0, "Rows must be > 0"
		assert cols > 0, "Columns must be > 0"

		self.gif1 = gif1
		self.gif2 = gif2
		self.rows = rows
		self.cols = cols
		self.pages1 = []
		self.pages2 = []

	def create(self):
		gif1 = Image.open(self.gif1)
		gif2 = Image.open(self.gif2)

		num_frames = self.getMinimumGifLength(gif1, gif2)
		images_per_page = self.rows * self.cols
		num_pages = ceil(num_frames / images_per_page)

		for page_num in range(num_pages):
			page = FlipbookPage(self.rows, self.cols)
			page.create(gif1, num_frames)
			self.pages1.append(page.getImage())

		for page_num in range(num_pages):
			page = FlipbookPage(self.rows, self.cols)
			page.create(gif2, num_frames, backwards=True)
			self.pages2.append(page.getImage())

	def getAllPages(self):
		return self.pages1 + self.pages2

	def getGroupedPages(self):
		return (self.pages1, self.pages2)

	def getMinimumGifLength(self, gif1, gif2):
		gif1_len = getGifLength(gif1)
		gif2_len = getGifLength(gif2)

		# Truncate longer gif to match shorter one
		# TODO: Make this behaviour configurable
		return min(gif1_len, gif2_len)


class FlipbookPage(object):
	def __init__(self, rows, cols):
		self.height = int(DEFAULT_DPI * PAGE_HEIGHT)
		self.width = int(DEFAULT_DPI * PAGE_WIDTH)
		self.im = Image.new('RGBA', (self.width, self.height), 
							color=WHITE)
		self.rows = rows
		self.cols = cols
		self.margin_size = int(MARGIN_SIZE * DEFAULT_DPI)
		self.frame_width = int((PAGE_WIDTH * DEFAULT_DPI - 2 * self.margin_size) / self.cols)
		self.frame_height = int((PAGE_HEIGHT * DEFAULT_DPI - 2 * self.margin_size) / self.rows)

	def create(self, gif, gifLength, backwards=False):
		if not backwards:
			rowRange = range(self.rows)
			colRange = range(self.cols)
			firstRowColRange = range(self.cols)
		else:
			remainingGif = gifLength - gif.tell()
			numFrames = min(remainingGif, self.rows * self.cols)
			startingRow = self.rows - ceil(numFrames / self.cols)
			startingCol = self.cols - ceil(numFrames % self.cols) - 1

			rowRange = range(startingRow, self.rows)
			colRange = range(self.cols - 1, -1, -1)
			firstRowColRange = range(startingCol, -1, -1)

		self.drawGuideLines()

		for i, row in enumerate(rowRange):
			if i == 0:
				thisColRange = firstRowColRange
			else:
				thisColRange = colRange

			rowY = self.margin_size + row * self.frame_height
			for col in thisColRange:
				corner = (self.margin_size + col * self.frame_width, rowY)
				outputImage = gif.resize((self.frame_width, self.frame_height), 
										 Image.ANTIALIAS)
				self.im.paste(outputImage, corner)

				try:
					gif.seek(gif.tell() + 1)
				except EOFError:
					return

	def drawGuideLines(self):
		draw = ImageDraw.Draw(self.im)
		for row in range(self.rows + 1):
			y = self.margin_size + row * self.frame_height
			draw.line((0, y, self.margin_size / 2, y), fill=BLACK, width=5)
			draw.line((self.width, y, self.width - self.margin_size/ 2, y), 
				  	   fill=BLACK, width=5)

		for col in range(self.cols + 1):
			x = self.margin_size + col * self.frame_width
			draw.line((x, 0, x, self.margin_size / 2), fill=BLACK, width=5)
			draw.line((x, self.height, x, self.height - self.margin_size/ 2), 
					   fill=BLACK, width=5)

		# Draw arrow indicating which direction paper should go into printer
		draw.line((self.width, self.height / 2, 
				   self.width - self.margin_size * 0.75, self.height / 2),
				   fill=BLACK, width=5)
		draw.line((self.width, self.height / 2, 
				   self.width - self.margin_size / 2, self.height / 2 - self.margin_size / 4),
				  fill=BLACK, width=5)
		draw.line((self.width, self.height / 2, 
				   self.width - self.margin_size / 2, self.height / 2 + self.margin_size / 4),
				  fill=BLACK, width=5)

	def getImage(self):
		return self.im


class ImageSequence:
    def __init__(self, im):
        self.im = im

    def __getitem__(self, ix):
        try:
            if ix:
                self.im.seek(ix)
            return self.im
        except EOFError:
        	# end of sequence
            raise IndexError

def getGifLength(gif, resetFrame=0):
	length = 0
	for _ in ImageSequence(gif):
		length += 1
	# return to first frame
	gif.seek(resetFrame)
	return length
