from math import ceil
from PIL import Image, ImageDraw

WHITE = (255, 255, 255, 255)
BLACK = (0, 0, 0, 255)

class Flipbook(object):
    def __init__(self, config):
        self._config = config
        self.pages1 = []
        self.pages2 = []

    def create(self):
        gif1 = Image.open(self._config.gif1)
        gif1_frames = [im.copy() for im in ImageSequence(gif1)]

        if self._config.gif2:
            gif2 = Image.open(self._config.gif2)
            assert gif1.size == gif2.size, \
                   "Both gifs must be the same size (for now)"
            gif2_frames = [im.copy() for im in ImageSequence(gif2)]

            # Truncate to length of shortest gif and loop if requested
            min_length = min(len(gif1_frames), len(gif2_frames))
            gif2_frames = gif2_frames[:min_length] * self._config.repeat
        else:
            min_length = len(gif1_frames)

        gif1_frames = gif1_frames[:min_length] * self._config.repeat
        self.add_gif(gif1_frames, gif1.size, self.pages1)

        if self._config.gif2:
            self.add_gif(gif2_frames, gif2.size, self.pages2, backwards=True)

    def add_gif(self, gif, size, pages, backwards=False):
        if backwards:
            gif.reverse()

        page_height = int(self._config.dpi * self._config.page_height)
        page_width = int(self._config.dpi * self._config.page_width)
        margin_size = int (self._config.dpi * self._config.margin)
        available_width = page_width - 2 * margin_size
        available_height = page_height - 2 * margin_size

        # Figure out page layout based on specified rows/cols
        # Images will be resized, but aspect ratio preserved
        if self._config.rows > 0:
            new_height = available_height // self._config.rows
            new_width = int((size[0] / size[1]) * new_height)
            num_rows = self._config.rows
            num_cols = available_width // new_width
        elif self._config.cols > 0:
            new_width = available_width // self._config.cols
            new_height = int((size[1] / size[0]) * new_width)
            num_cols = self._config.cols
            num_rows = available_height // new_height
        else:
            # No rows or cols specified, just use original dimensions
            # and pack as many in as possible
            new_width = size[0]
            new_height = size[1]
            num_cols = available_width // new_width
            num_rows = available_height // new_height

        num_pages = ceil(len(gif) / (num_rows * num_cols))
        for page_num in range(num_pages):
            page = FlipbookPage(
                self._config, num_rows, num_cols, new_width, new_height
            )
            start_frame = page_num * num_rows * num_cols
            end_frame = start_frame + num_rows * num_cols
            page.create(gif[start_frame: end_frame], backwards)
            pages.append(page.get_image())

    def get_all_pages(self):
        return self.pages1 + self.pages2

    def get_grouped_pages(self):
        return (self.pages1, self.pages2)

class FlipbookPage(object):
    def __init__(self, config, rows, cols, frame_width, frame_height):
        self.height = int(config.dpi * config.page_height)
        self.width = int(config.dpi * config.page_width)
        self.im = Image.new('RGBA', (self.width, self.height), color=WHITE)
        self.rows = rows
        self.cols = cols
        self.margin_size = int(config.margin * config.dpi)
        self.frame_width = frame_width
        self.frame_height = frame_height

    def create(self, gif, backwards=False):
        self.draw_guide_lines(backwards)

        row = self.rows - 1 if backwards else 0
        col = 0

        row_offset, col_offset = self.get_offsets(backwards)

        for im in gif:
            row_y = row_offset + self.margin_size + row * self.frame_height
            corner = (col_offset + self.margin_size + col * self.frame_width,
                      row_y)
            resized_im = im.resize(
                (self.frame_width, self.frame_height), 
                Image.ANTIALIAS
            )
            self.im.paste(resized_im, corner)

            col += 1
            if col >= self.cols:
                row += -1 if backwards else 1
                col = 0

    def get_offsets(self, backwards):
        col_offset = 0
        if backwards:
            available_height = self.height - 2 * self.margin_size
            row_offset = available_height % self.frame_height
        else:
            row_offset = 0

        return row_offset, col_offset

    def draw_guide_lines(self, backwards):
        row_offset, col_offset = self.get_offsets(backwards)
        draw = ImageDraw.Draw(self.im)
        for row in range(self.rows + 1):
            y = row_offset + self.margin_size + row * self.frame_height
            draw.line((0, y, self.margin_size / 2, y), fill=BLACK, width=5)
            draw.line(
                (self.width, y, self.width - self.margin_size/ 2, y), 
                fill=BLACK, width=5
            )

        for col in range(self.cols + 1):
            x = col_offset + self.margin_size + col * self.frame_width
            draw.line((x, 0, x, self.margin_size / 2), fill=BLACK, width=5)
            draw.line(
                (x, self.height, x, self.height - self.margin_size/ 2), 
                fill=BLACK, width=5
            )

        # Draw arrow indicating which direction paper should go into printer
        draw.line(
            (self.width, self.height / 2, 
             self.width - self.margin_size * 0.75, self.height / 2),
            fill=BLACK, width=5
        )
        draw.line(
            (self.width, self.height / 2, 
             self.width - self.margin_size / 2, 
             self.height / 2 - self.margin_size / 4),
            fill=BLACK, width=5
        )
        draw.line(
            (self.width, self.height / 2, 
             self.width - self.margin_size / 2, 
             self.height / 2 + self.margin_size / 4),
            fill=BLACK, width=5
        )

    def get_image(self):
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
