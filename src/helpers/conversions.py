def cart_to_isometric(point):
    isoX = point[0] - point[1]
    isoY = (point[0] + point[1])/2
    return [isoX, isoY]

def midpoint(x1, x2, y1, y2):
    return ((x1+x2)/2, (y1+y2)/2)

def convert_to_2d_index(index_1d):
    return [int(index_1d / 8), int(index_1d % 8)]