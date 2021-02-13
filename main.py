import numpy as np
from PIL import Image
from random import *
import paint
import math


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
        func(x0, y0, x1, y1, image, color, img_name)


# h = int(input())
# w = int(input())

h = 200
w = 200

matrix = create_matrix(0, h, w)
create_image(matrix, 'new.png')

matrix = create_matrix(255, h, w)
create_image(matrix, 'new1.png')

matrix = create_matrix((255, 0, 0), h, w)
create_image(matrix, 'new2.png')

matrix = create_random_matrix(h, w)
create_image(matrix, 'new3.png')

matrix = create_schema_matrix(h, w)
create_image(matrix, 'new4.png')

draw(paint.line, (255, 0, 0), "new5.png")
draw(paint.line2, (255, 0, 0), "new6.png")
draw(paint.line3, (255, 0, 0), "new7.png")
draw(paint.line_bresenhema, (255, 0, 0), "new8.png")
