import numpy as np
from PIL import Image
from random import *
import paint
import math
import my_parser
import model


def create_matrix(element, h, w):
    return np.array([[element for j in range(w)] for i in range(h)]).astype(np.uint8)


def create_random_matrix(h, w):
    return np.array([[(randint(0, 255), randint(0, 255), randint(0, 255)) for j in range(w)] for i in range(h)]).astype(
        np.uint8)


def create_schema_matrix(h, w):
    return np.array([[((i + j) % 256, (i + j) % 256, (i + j) % 256) for j in range(w)] for i in range(h)]).astype(
        np.uint8)


def create_image(img_source, img_name):
    new_image = Image.fromarray(img_source)
    new_image.save(img_name, "PNG")


def draw(func, color, img_name):
    image = Image.new("RGB", (h, w), (0, 0, 0))
    x0, y0 = [100, 100]
    for i in range(0, 13):
        a = 2 * math.pi * i / 13
        x1 = 100 + 95 * math.cos(a)
        y1 = 100 + 95 * math.sin(a)
        func(x0, y0, x1, y1, image, color)
    image.save(img_name, "PNG")


# h = int(input())
# w = int(input())

h = 200
w = 200

# matrix = create_matrix(0, h, w)
# create_image(matrix, 'test/new.png')
#
# matrix = create_matrix(255, h, w)
# create_image(matrix, 'test/new1.png')
#
# matrix = create_matrix((255, 0, 0), h, w)
# create_image(matrix, 'test/new2.png')
#
# matrix = create_random_matrix(h, w)
# create_image(matrix, 'test/new3.png')
#
# matrix = create_schema_matrix(h, w)
# create_image(matrix, 'test/new4.png')
#
# draw(paint.line, (255, 0, 0), "test/new5.png")
# draw(paint.line2, (255, 0, 0), "test/new6.png")
# draw(paint.line3, (255, 0, 0), "test/new7.png")
# draw(paint.line_bresenhema, (255, 0, 0), "test/new8.png")
#
mod = my_parser.parse()
# image = Image.new("RGB", (1000, 1000), (0, 0, 0))
# mod.paint_vertexes(image, (255, 255, 255))
# image.save("test/new9.png", "PNG")
#
# image = Image.new("RGB", (1000, 1000), (0, 0, 0))
# mod.paint_polygons(image, (255, 255, 255))
# image.save("test/new10.png", "PNG")

image = Image.new("RGB", (1000, 1000), (0, 0, 0))
mod.paint_fill_polygons(image)
image.save("test/new11.png", "PNG")

image = Image.new("RGB", (1000, 1000), (0, 0, 0))
mod.paint_polygons(image, (255, 255, 255))
image.save("test/new12.png", "PNG")