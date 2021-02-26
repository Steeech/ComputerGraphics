import model


def handler(s):
    sarr = s.split("/")
    return int(sarr[0])


def parse():
    fin = open("Test.obj", "r")
    mod = model.Model()

    for s in fin:
        sarr = s.split()
        if sarr[0] == "v":
            mod.add_vertex((float(sarr[1]), float(sarr[2]), float(sarr[3])))
        if sarr[0] == "vt":
            mod.add_texture((float(sarr[1]), float(sarr[2])))
        if sarr[0] == "vn":
            mod.add_normal((float(sarr[1]), float(sarr[2]), float(sarr[3])))
        if sarr[0] == "f":
            mod.add_polygon(handler(sarr[1]), handler(sarr[2]), handler(sarr[3]))

    return mod
