# flip.py
flip.py is a command line program that takes one or two GIF images and formats them into images that can easily be printed and cut into a [flip book](http://en.wikipedia.org/wiki/Flip_book).

## Requirements
flip.py is written in Python 3. You will need the [Pillow](https://pillow.readthedocs.org) image processing library.

## Single GIF flip book
If you provide only a single GIF to flip.py, it will format a one-sided flip book.

```
./flip.py test_images/rainbowgoof.gif
```

This will produce a series of images `output-a-<page_num>.png` that can be printed as individual pages and cut along the guidelines into a flip book.

## Double GIF flip book
You can specify two GIFs to produce a two-sided flip book. If the two GIFs are of different lengths, the longer one will be truncated to be the same length as the shorter. The GIFs must be the same dimensions.

```
./flip.py test_images/rainbowboof.gif test_images/rainbowgoof.gif
```

This will produce two series of images: `output-a-<page_num>.png` and `output-b-<page_num>.png`. You can then print all the images in the `output-a-<page_num>.png` series, then put them back into the printer face up with the arrow in the margin pointing into the printer and print the `output-b-<page_num>.png` series. This should provide you a two sided flip book when you cut along the guidelines.

This has only been tested on my printer, so your mileage may vary.

## Other configuration
flip.py will try to fit as many frames as possible on each page using a landscape alignment. If you want to specify the number of rows of frames, or the number of frames per column, you can use the `--rows` or `--cols` arguments respectively. The aspect ratio of your GIF will always be maintained, so only one of these should be specified. If both are specified, `--cols` will be ignored.

```
# scale images to fit 3 rows per page
flip.py test_images/rainbowgoof.gif --rows 3
```

You can also repeat the GIFs multiple times for a longer flip book.

```
# repeat gif 3 times
flip.py test_images/rainbowgoof.gif --repeat 3
```

## Test images and sample outputs
You can see sample outputs in the `sample_outputs` folder and play with the test images in the `test_images` folder.

Sample GIFs and inspiration provided by [Courtney Garvin](http://courtneygarvin.tumblr.com/).

## TODOs
Pull requests are welcome!

* automatically figure out which page orientation (landscape vs portrait) can hold more images, and use it.
* optionally output alternating pages for lucky folks with two-sided printers.
* output as PDF, one PDF per GIF.
* read settings from config file instead of command line
* configurable page size, DPI, margin size, etc.
* For GIFs of different lengths, allow shorter gif to loop until it matches longer gif.
* Do something sensible when GIFs of different dimensions are provided (though you'll have to clobber the aspect ratio of one of them)
* Specify output directory
