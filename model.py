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
    R = []
    v = 'vertex'
    vt = 'texture'
    vn = 'normal'
    l = np.array([0, 0, -1])

    def __init__(self):
        self.init_R(0, 0, 0)

    #1 laba
    def add_vertex(self, xyz):
        self.vertexes.append(xyz)

    def add_texture(self, xyz):
        self.textures.append(xyz)

    def add_normal(self, xyz):
        self.normals.append(xyz)

    def get_polygon(self, i):
        return self.polygons[i]

    def add_polygon(self, n1, n2, n3):
        self.polygons.append(({self.v: self.vertexes[n1[0] - 1], self.vt: self.textures[n1[1] - 1], self.vn: self.normals[n1[2] - 1]},
                              {self.v: self.vertexes[n2[0] - 1], self.vt: self.textures[n2[1] - 1], self.vn: self.normals[n2[2] - 1]},
                              {self.v: self.vertexes[n3[0] - 1], self.vt: self.textures[n3[1] - 1], self.vn: self.normals[n3[2] - 1]}))

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
            v1 = polygon[0][self.v]
            v2 = polygon[1][self.v]
            v3 = polygon[2][self.v]
            k = 4000
            r = 500
            paint.line_bresenhema(v1[0] * k + r, v1[1] * -k + r, v2[0] * k + r, v2[1] * -k + r, img, color)
            paint.line_bresenhema(v1[0] * k + r, v1[1] * -k + r, v3[0] * k + r, v3[1] * -k + r, img, color)
            paint.line_bresenhema(v3[0] * k + r, v3[1] * -k + r, v2[0] * k + r, v2[1] * -k + r, img, color)

    # 2 laba

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

        v0 = self.projection_transform(polygon[0][self.v])
        v1 = self.projection_transform(polygon[1][self.v])
        v2 = self.projection_transform(polygon[2][self.v])

        vn0 = polygon[0][self.vn]
        vn1 = polygon[1][self.vn]
        vn2 = polygon[2][self.vn]

        # k = 4000
        # r = 500

        x0 = v0[0] / v0[2]  # * k + r
        y0 = v0[1] / v0[2]  # * -k + r
        x1 = v1[0] / v1[2]  # * k + r
        y1 = v1[1] / v1[2]  # * -k + r
        x2 = v2[0] / v2[2]  # * k + r
        y2 = v2[1] / v2[2]  # * -k + r

        xmin = max(min(x0, x1, x2), 0)
        ymin = max(min(y0, y1, y2), 0)
        xmax = min(max(x0, x1, x2), np.size(self.z_buffer, 0))
        ymax = min(max(y0, y1, y2), np.size(self.z_buffer, 1))

        # print(xmax, ymax)
        for x in range(int(xmin), int(xmax) + 1):
            for y in range(int(ymin), int(ymax) + 1):
                b0, b1, b2 = self.calculate_baricentric_koord(x0, y0, x1, y1, x2, y2, x, y)
                if (b0 > 0) and (b1 > 0) and (b2 > 0):
                    z = b0 * v0[2] + b1 * v1[2] + b2 * v2[2]
                    l0 = self.calculate_l_i(vn0)
                    l1 = self.calculate_l_i(vn1)
                    l2 = self.calculate_l_i(vn2)
                    color = int(255*(b0*l0 + b1*l1 + b2*l2))
                    if z < self.z_buffer[x][y]:
                        draw.point([x, y], (color, color, color))
                        self.z_buffer[x][y] = z

    def paint_fill_polygons(self, img):
        for polygon in self.polygons:
            cos = self.check_polygon(polygon)
            if cos < 0:
                color = (int(255 * abs(cos)), int(255 * abs(cos)), int(255 * abs(cos)))
                self.paint_polygon(polygon, img, color)

    def calculate_normal(self, x0, y0, z0, x1, y1, z1, x2, y2, z2):
        return np.cross([x1 - x0, y1 - y0, z1 - z0], [x1 - x2, y1 - y2, z1 - z2])

    def check_polygon(self, polygon):

        v0 = polygon[0][self.v]
        v1 = polygon[1][self.v]
        v2 = polygon[2][self.v]

        n = self.calculate_normal(v0[0], v0[1], v0[2], v1[0], v1[1], v1[2], v2[0], v2[1], v2[2])
        return np.dot(n, self.l) / (np.linalg.norm(n) * np.linalg.norm(self.l))

    def init_z_Buffer(self, n, m):
        self.z_buffer = np.array([[10 ** 9 for i in range(m)] for j in range(n)])

    # 3 laba
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

    def projection_transform(self, v):
        vector = np.dot(self.K, np.dot(self.R, v) + self.t)
        return vector

    def init_R(self, alpha, beta, gamma):
        alpha_mat = np.array([[1, 0, 0], [0, np.cos(alpha), np.sin(alpha)], [0, -np.sin(alpha), np.cos(alpha)]])
        beta_mat = np.array([[np.cos(beta), 0, np.sin(beta)], [0, 1, 0], [-np.sin(beta), 0, np.cos(beta)]])
        gamma_mat = np.array([[np.cos(gamma), np.sin(gamma), 0], [-np.sin(gamma), np.cos(gamma), 0], [0, 0, 1]])
        self.R  = np.dot(np.dot(alpha_mat, beta_mat), gamma_mat)

    def get_R(self):
        return self.R

    #4 laba
    def calculate_l_i(self, vn):
        return np.dot(vn, self.l) / (np.linalg.norm(vn) * np.linalg.norm(self.l))