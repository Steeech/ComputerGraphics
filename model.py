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
        self.polygons.append((self.vertexes[n1-1], self.vertexes[n2-1], self.vertexes[n3-1]))

    def paint_vertex(self, i, img, color):
        x = self.vertexes[i][0]
        y = self.vertexes[i][1]
        z = self.vertexes[i][2]
        k = 40000
        r = 5000
        paint.point(x * k + r, y * -k + r, img, color)

    def paint_vertexes(self, img, color):
        for i in range(len(self.vertexes)):
            self.paint_vertex(i, img, color)

    def paint_polygons(self, img, color):
        for polygon in self.polygons:
            v1 = polygon[0]
            v2 = polygon[1]
            v3 = polygon[2]
            k = 40000
            r = 5000
            paint.line_bresenhema(v1[0] * k + r, v1[1] * -k + r, v2[0] * k + r, v2[1] * -k + r, img, color)
            paint.line_bresenhema(v1[0] * k + r, v1[1] * -k + r, v3[0] * k + r, v3[1] * -k + r, img, color)
            paint.line_bresenhema(v3[0] * k + r, v3[1] * -k + r, v2[0] * k + r, v2[1] * -k + r, img, color)
