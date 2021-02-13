from PIL import ImageDraw

def point(x, y, img, color):
    draw = ImageDraw.Draw(img)
    draw.point([x,y], color)

def line(x0, y0, x1, y1, img, color):
    draw = ImageDraw.Draw(img)
    x0 = int(x0)
    y0 = int(y0)
    x1 = int(x1)
    y1 = int(y1)
    for i in range(100):
        t = i / 100
        x = x0 * (1 - t) + x1 * t
        y = y0 * (1 - t) + y1 * t
        draw.point([x, y], color)



def line2(x0, y0, x1, y1, img, color):
    draw = ImageDraw.Draw(img)
    x0 = int(x0)
    y0 = int(y0)
    x1 = int(x1)
    y1 = int(y1)
    for x in range(x0, x1 + 1):
        t = (x - x0) / (x1 - x0)
        y = y0 * (1 - t) + y1 * t
        draw.point([x, y], color)



def line3(x0, y0, x1, y1, img, color):
    draw = ImageDraw.Draw(img)
    x0 = round(x0)
    y0 = round(y0)
    x1 = round(x1)
    y1 = round(y1)

    steep = abs(x0 - x1) < abs(y0 - y1)
    if abs(x0 - x1) < abs(y0 - y1):
        x0, y0 = y0, x0
        x1, y1 = y1, x1

    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    for x in range(x0, x1 + 1):
        t = (x - x0) / (x1 - x0)
        y = y0 * (1 - t) + y1 * t
        if steep:
            draw.point([y, x], color)
        else:
            draw.point([x, y], color)



def line_bresenhema(x0, y0, x1, y1, img, color):
    draw = ImageDraw.Draw(img)

    x0 = round(x0)
    y0 = round(y0)
    x1 = round(x1)
    y1 = round(y1)

    if (x0==x1 and y0==y1):
        return

    steep = abs(x0 - x1) < abs(y0 - y1)
    if abs(x0 - x1) < abs(y0 - y1):
        x0, y0 = y0, x0
        x1, y1 = y1, x1

    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    dx = x1 - x0
    dy = y1 - y0

    derror = abs(dy / dx)
    error = 0
    y = y0

    for x in range(x0, x1 + 1):
        if steep:
            draw.point([y, x], color)
        else:
            draw.point([x, y], color)
        error += derror
        if error > 0.5:
            y += 1 if y1 > y0 else -1
            error -= 1

