from random import randint

from PIL import ImageDraw

import paint


class Model:
    vertexes = []
    textures = []
    normals = []
    polygons = []

    def add_vertex(self, xyz):
        self.vertexes.append(xyz)

    def add_texture(self, xyz):
        self.textures.append(xyz)

    def add_normal(self, xyz):
        self.normals.append(xyz)

    def add_polygon(self, n1, n2, n3):
        self.polygons.append((self.vertexes[n1 - 1], self.vertexes[n2 - 1], self.vertexes[n3 - 1]))

    def paint_vertex(self, i, img, color):
        x = self.vertexes[i]
        y = self.vertexes[i][1]
        z = self.vertexes[i][2]
        k = 4000
        r = 500
        paint.point(x * k + r, y * -k + r, img, color)

    def paint_vertexes(self, img, color):
        for i in range(len(self.vertexes)):
            self.paint_vertex(i, img, color)

    def paint_polygons(self, img, color):
        for polygon in self.polygons:
            v1 = polygon[0]
            v2 = polygon[1]
            v3 = polygon[2]
            k = 4000
            r = 500
            paint.line_bresenhema(v1[0] * k + r, v1[1] * -k + r, v2[0] * k + r, v2[1] * -k + r, img, color)
            paint.line_bresenhema(v1[0] * k + r, v1[1] * -k + r, v3[0] * k + r, v3[1] * -k + r, img, color)
            paint.line_bresenhema(v3[0] * k + r, v3[1] * -k + r, v2[0] * k + r, v2[1] * -k + r, img, color)


    def calculate_baricentric_koord(self, x0, y0, x1, y1, x2, y2, x, y):
        baricentric_koord = [0] * 3
        baricentric_koord[0] = ((x1 - x2) * (y - y2) - (y1 - y2) * (x - x2)) / (
                (x1 - x2) * (y0 - y2) - (y1 - y2) * (x0 - x2))
        baricentric_koord[1] = ((x2 - x0) * (y - y0) - (y2 - y0) * (x - x0)) / (
                (x2 - x0) * (y1 - y0) - (y2 - y0) * (x1 - x0))
        baricentric_koord[2] = ((x0 - x1) * (y - y1) - (y0 - y1) * (x - x1)) / (
                (x0 - x1) * (y2 - y1) - (y0 - y1) * (x2 - x1))

        if round(sum(baricentric_koord)) != 1:
            print(*baricentric_koord)

        return baricentric_koord

    def paint_polygon(self, polygon, img, color):
        draw = ImageDraw.Draw(img)
        v0 = polygon[0]
        v1 = polygon[1]
        v2 = polygon[2]

        k = 4000
        r = 500

        x0 = v0[0] * k + r
        y0 = v0[1] * -k + r
        x1 = v1[0] * k + r
        y1 = v1[1] * -k + r
        x2 = v2[0] * k + r
        y2 = v2[1] * -k + r



        xmin = max(min(x0, x1, x2), 0)
        ymin = max(min(y0, y1, y2), 0)
        xmax = max(x0, x1, x2)
        ymax = max(y0, y1, y2)

        for x in range(int(xmin), int(xmax) + 1):
            for y in range(int(ymin), int(ymax) + 1):
                b0, b1, b2 = self.calculate_baricentric_koord(x0, y0, x1, y1, x2, y2, x, y)
                if (b0 > 0) and (b1 > 0) and (b2 > 0):
                    draw.point([x, y], color)

    def paint_fill_polygons(self, img):
        for polygon in self.polygons:
            color = (randint(0, 255), randint(0, 255), randint(0, 255))
            self.paint_polygon(polygon, img, color)
