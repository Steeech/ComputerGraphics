from random import randint

from PIL import ImageDraw

import numpy as np

import paint


class Model:
    vertexes = []
    textures = []
    normals = []
    polygons = []
    z_buffer = []
    K = []
    t = []

    def init_K_t(self, ax, ay, u0, v0, t):
        self.K = np.array([[ax, 0, u0], [0, -ay, v0], [0, 0, 1]])
        self.t = t
        print(self.K)

    def set_ax(self, ax):
        self.K[0][0] = ax

    def set_ay(self, ay):
        self.K[1][1] = ay

    def set_v0(self, v0):
        self.K[0][2] = v0

    def set_v0(self, u0):
        self.K[1][2] = u0

    def set_t(self, t):
        self.t = t

    def get_ax(self):
        return self.K[0][0]

    def get_ay(self):
        return self.K[1][1]

    def get_v0(self):
        return self.K[0][2]

    def get_v0(self):
        return self.K[1][2]

    def get_t(self):
        return self.t

    def init_z_Buffer(self, n, m):
        self.z_buffer = np.array([[10 ** 9 for i in range(m)] for j in range(n)])

    def add_vertex(self, xyz):
        self.vertexes.append(xyz)

    def add_texture(self, xyz):
        self.textures.append(xyz)

    def add_normal(self, xyz):
        self.normals.append(xyz)

    def add_polygon(self, n1, n2, n3):
        self.polygons.append((self.vertexes[n1 - 1], self.vertexes[n2 - 1], self.vertexes[n3 - 1]))

    def projection_transform(self, v):#TODO не работает(
        t1 = np.array([0, 0, 0.5])
        # print(v)
        # print(np.dot(self.K, v+self.t))
        vector = np.dot(self.K, v+self.t)
        return vector

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

        v0 = self.projection_transform(polygon[0])
        v1 = self.projection_transform(polygon[1])
        v2 = self.projection_transform(polygon[2])

        # print(self.projection_transform(v0))

        k = 4000
        r = 500

        x0 = v0[0]/v0[2] #* k + r
        y0 = v0[1]/v0[2] #* -k + r
        x1 = v1[0]/v1[2] #* k + r
        y1 = v1[1]/v1[2] #* -k + r
        x2 = v2[0]/v2[2] #* k + r
        y2 = v2[1]/v2[2] #* -k + r

        # print(x0, y0)

        xmin = max(min(x0, x1, x2), 0)
        ymin = max(min(y0, y1, y2), 0)
        xmax = min(max(x0, x1, x2), 1499)
        ymax = min(max(y0, y1, y2), 1499)


        # print(xmax, ymax)
        for x in range(int(xmin), int(xmax) + 1):
            for y in range(int(ymin), int(ymax) + 1):
                b0, b1, b2 = self.calculate_baricentric_koord(x0, y0, x1, y1, x2, y2, x, y)
                if (b0 > 0) and (b1 > 0) and (b2 > 0):
                    # draw.point([x, y], color)
                    z = b0 * v0[2] + b1 * v1[2] + b2 * v2[2]
                    if z < self.z_buffer[x][y]:
                        draw.point([x, y], color)
                        self.z_buffer[x][y] = z

    def paint_fill_polygons(self, img):
        for polygon in self.polygons:
            # color = (randint(0, 255), randint(0, 255), randint(0, 255))
            cos = self.check_polygon(polygon)
            if (cos < 0):
                color = (int(255 * abs(cos)), int(255 * abs(cos)), int(255 * abs(cos)))
                self.paint_polygon(polygon, img, color)

    def calculate_normal(self, x0, y0, z0, x1, y1, z1, x2, y2, z2):
        return np.cross([x1 - x0, y1 - y0, z1 - z0], [x1 - x2, y1 - y2, z1 - z2])

    def check_polygon(self, polygon):
        l = np.array([0, 0, -1])

        v0 = polygon[0]
        v1 = polygon[1]
        v2 = polygon[2]

        n = self.calculate_normal(v0[0], v0[1], v0[2], v1[0], v1[1], v1[2], v2[0], v2[1], v2[2])

        return np.dot(n, l) / (np.linalg.norm(n) * np.linalg.norm(l))
