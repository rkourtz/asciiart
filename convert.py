#!/usr/bin/env python

import os
from PIL import Image
import sys
import tempfile
import urllib2

ASCII_CHARS = [ ' ', '#', '?', '%', '.', 'S', '+', '.', '*', ':', ',', '@']
ASCII_CHARS = [ ' ', '.', ',', '+', ':', ';', '*', '?', 'S', '%', '@', '#']
ASCII_CHARS = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,^`'. ")

def scale_image(image, new_width=100):
    """Resizes an image preserving the aspect ratio.
    """
    (original_width, original_height) = image.size
    aspect_ratio = original_height/float(original_width)
    new_height = int(aspect_ratio * new_width)

    new_image = image.resize((new_width, new_height))
    return new_image

def convert_to_grayscale(image):
    return image.convert('L')

def map_pixels_to_ascii_chars(image, range_width=25):
    """Maps each pixel to an ascii char based on the range
    in which it lies.

    0-255 is divided into 11 ranges of 25 pixels each.
    """
    pixels_to_chars = []
    pixel_values = list(image.getdata())
    for pixel_value in pixel_values:
      idx = pixel_value/len(ASCII_CHARS) - 1
      try:
        pixels_to_chars.append(ASCII_CHARS[idx])
      except:
        print "idx: %i" % idx
        raise

    return "".join(pixels_to_chars)

def convert_image_to_ascii(image, new_width=100):
    image = scale_image(image, new_width)
    image = convert_to_grayscale(image)

    pixels_to_chars = map_pixels_to_ascii_chars(image, new_width)
    len_pixels_to_chars = len(pixels_to_chars)

    image_ascii = [pixels_to_chars[index: index + new_width] for index in
            xrange(0, len_pixels_to_chars, new_width)]

    return "\n".join(image_ascii)

def handle_image_conversion(image_filepath):
    image = None
    try:
        image = Image.open(image_filepath)
    except Exception, e:
        print "Unable to open image file {image_filepath}.".format(image_filepath=image_filepath)
        print e
        return
    try:
      rows, columns = map(lambda x: int(x), os.popen('stty size', 'r').read().split())
    except:
      columns = 100
    image_ascii = convert_image_to_ascii(image, columns)
    print image_ascii

if __name__=='__main__':
    import sys

    image_file_path = sys.argv[1]
    handle_image_conversion(image_file_path)
